from django.db import models


class GenreCategoryTitleAbstractModel(models.Model):
    """
    Абстрактная модель для хранения общих данных моделей Genre Category Title
    """

    name = models.CharField(
        max_length=256,
        verbose_name='Название',
        help_text='Укажите название',
    )

    class Meta:
        abstract = True


class GenreCategoryAbstractModel(models.Model):
    """
    Абстрактная модель для хранения общих данных моделей Genre Category
    """

    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Семантический URL для страницы',
        help_text=(
            'Укажите уникальный адрес для страницы. '
            'Используйте только латиницу, '
            'цифры, дефисы и знаки подчёркивания'
        ),
    )

    class Meta:
        abstract = True


class ReviewCommentAbstractModel(models.Model):
    """
    Абстрактная модель для хранения общих данных моделей Review Comment
    """

    text = models.TextField(
        verbose_name='Текст',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        abstract = True
