from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User

from .mixins import (GenreCategoryAbstractModel,
                     GenreCategoryTitleAbstractModel,
                     ReviewCommentAbstractModel)
from .validators import validate_year


class Genre(GenreCategoryTitleAbstractModel, GenreCategoryAbstractModel):
    """Модель для хранения данных Жарн"""

    class Meta:
        ordering = (
            'name',
        )
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Category(GenreCategoryTitleAbstractModel, GenreCategoryAbstractModel):
    """Модель для хранения данных Категория"""

    class Meta:
        ordering = (
            'name',
        )
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Title(GenreCategoryTitleAbstractModel):
    """Модель для хранения данных Произведение"""

    year = models.IntegerField(
        validators=(validate_year, ),
        verbose_name="Год выпуска произведения",
        help_text="Укажите год выпуска произведения в формате YYYY",
    )
    description = models.TextField(
        verbose_name='Описание произведения',
        help_text="Укажите описание произведения",
        blank=True,
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        related_name='titles',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True,
    )

    class Meta:
        ordering = (
            'year',
        )
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name

    def get_genres_list(self):
        return list(self.genre.values_list('name', flat=True))


class GenreTitle(models.Model):
    """Модель для хранения данных о связи Жанров и Произведений"""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=['title', 'genre'],
                name='unique_title_genre',
            ),
        )


class Review(ReviewCommentAbstractModel):
    """Модель для хранения данных Отзыв"""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
    )
    score = models.IntegerField(
        verbose_name='Оценка',
        validators=(
            MaxValueValidator(10),
            MinValueValidator(1),
        ),
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )

    class Meta:
        verbose_name = "Отзывы"

        constraints = (
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_author_title',
            ),
        )

    def __str__(self):
        return self.text


class Comment(ReviewCommentAbstractModel):
    """Модель для хранения данных Комментарий"""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )

    class Meta:
        verbose_name = "Комментарий к отзыву"

    def __str__(self):
        return self.text
