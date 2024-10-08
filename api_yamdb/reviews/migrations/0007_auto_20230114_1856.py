# Generated by Django 3.2 on 2023-01-14 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0006_alter_title_genre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(help_text='Укажите название', max_length=256, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(help_text='Укажите уникальный адрес для страницы. Используйте только латиницу, цифры, дефисы и знаки подчёркивания', unique=True, verbose_name='Семантический URL для страницы'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(verbose_name='Текст'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(help_text='Укажите название', max_length=256, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='slug',
            field=models.SlugField(help_text='Укажите уникальный адрес для страницы. Используйте только латиницу, цифры, дефисы и знаки подчёркивания', unique=True, verbose_name='Семантический URL для страницы'),
        ),
        migrations.AlterField(
            model_name='review',
            name='text',
            field=models.TextField(verbose_name='Текст'),
        ),
        migrations.AlterField(
            model_name='title',
            name='name',
            field=models.CharField(help_text='Укажите название', max_length=256, verbose_name='Название'),
        ),
    ]
