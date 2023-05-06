import csv
import os

from django.core.management.base import BaseCommand
from reviews.models import (Category, Comment, Genre, GenreTitle, Review,
                            Title, User)

from api_yamdb.settings import BASE_DIR

DIR_CSV_FILE = os.path.join(BASE_DIR, 'static/data')

FILE_TO_UPLOAD = {
    'users.csv': User,
    'titles.csv': Title,
    'genre.csv': Genre,
    'category.csv': Category,
    'genre_title.csv': GenreTitle,
    'comments.csv': Comment,
    'review.csv': Review,
}


class Command(BaseCommand):
    help = 'Загрузка данных из CSV файлов в базу данных'

    def handle(self, *args, **kwargs):
        for file, model in FILE_TO_UPLOAD.items():
            print(f'Импорт из файла: {file}, в модель: {model}')
            file_name = str(os.path.join(DIR_CSV_FILE, file))
            with open(file_name, 'r', newline='', encoding='utf-8') as csvfile:
                csv_data = csv.reader(csvfile, delimiter=',')
                count = 0
                for row in csv_data:
                    if count == 0:
                        fields = row
                    else:
                        data = dict(zip(fields, row))
                        obj, created = model.objects.get_or_create(**data)
                    count += 1
                print(f'{count} записей добавлено в {model} из {file}')
