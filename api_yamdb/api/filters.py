from django_filters import rest_framework as filters
from reviews.models import Title


class TitleFilter(filters.FilterSet):
    name = filters.Filter(field_name="name", lookup_expr='icontains')
    year = filters.NumberFilter(field_name="year", lookup_expr='exact')
    genre = filters.Filter(field_name="genre__slug", lookup_expr='icontains')
    category = filters.Filter(
        field_name="category__slug", lookup_expr='icontains'
    )

    class Meta:
        model = Title
        fields = ('name', 'year', 'genre', 'category')
