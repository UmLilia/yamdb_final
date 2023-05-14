from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from reviews.models import Category, Comment, Genre, Review, Title

from .filters import TitleFilter
from .pagination import PagePagination
from .permissions import AdminOrReadOnly, IsAdmin, IsObjectOwner
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ListTitleSerializer,
                          PostTitleSerializer, ReviewSerializer,
                          UserSerializer)

User = get_user_model()


class GenreViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Genre.objects.all()
    pagination_class = PagePagination
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Category.objects.all()
    pagination_class = PagePagination
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = (
        Title.objects.select_related('category')
        .prefetch_related('genre')
        .annotate(rating=Avg('reviews__score'))
    )
    pagination_class = PagePagination
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year', 'genre', 'category')
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return ListTitleSerializer
        return PostTitleSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    pagination_class = PagePagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        methods=('patch', 'get'),
        detail=False,
        url_path='me',
        url_name='me',
        permission_classes=(IsAuthenticated,),
    )
    def get_me(self, request):
        user = self.request.user
        serializer = self.get_serializer(user)
        if self.request.method == 'PATCH':
            serializer = self.get_serializer(
                user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsObjectOwner,)
    pagination_class = PagePagination

    def get_queryset(self):
        return Review.objects.filter(title=self.kwargs.get('title_id'))

    def perform_create(self, serializer):
        current_title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        if Review.objects.filter(
            author=self.request.user, title=current_title
        ).exists():
            raise ValidationError('Вы уже оставляли отзыв к этой записи!')
        serializer.save(author=self.request.user, title=current_title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsObjectOwner,)
    pagination_class = PagePagination

    def get_queryset(self):
        return Comment.objects.filter(
            review__title_id=self.kwargs.get('title_id'),
            review_id=self.kwargs.get('review_id'),
        ).select_related('author')

    def perform_create(self, serializer):
        current_review = get_object_or_404(Review, pk=self.kwargs['review_id'])
        serializer.save(
            author=self.request.user,
            review=current_review,
        )
