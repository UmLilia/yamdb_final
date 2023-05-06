import csv
import os
from datetime import datetime

import pytz
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from reviews.models import (Category, Comment, Genre, GenreTitle, Review,
                            Title, User)

from api_yamdb.settings import BASE_DIR

DIR_CSV_FILE = os.path.join(BASE_DIR, 'static/data')

FILE_TO_UPLOAD = {
    'users.csv': User,
    'category.csv': Category,
    'genre.csv': Genre,
    'titles.csv': Title,
    'genre_title.csv': GenreTitle,
    'review.csv': Review,
    'comments.csv': Comment,
}

TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


class Command(BaseCommand):
    help = 'Загрузка данных из CSV файлов в базу данных'

    def handle(self, *args, **kwargs):
        for file, model in FILE_TO_UPLOAD.items():
            print(
                f'Импорт из файла: {file}, в таблицу {model._meta.db_table}, '
                f'модель: {model.__name__}'
            )
            file_name = str(os.path.join(DIR_CSV_FILE, file))
            with open(file_name, 'r', newline='', encoding='utf-8') as csvfile:
                csv_data = csv.reader(csvfile, delimiter=',')
                count_add_record = 0
                count_read_record = -1
                for row in csv_data:
                    if count_read_record == -1:
                        fields = row
                    else:
                        data = dict(zip(fields, row))
                        try:
                            obj = model.objects.get(id=data['id'])
                        except ObjectDoesNotExist:
                            obj = model.objects.create(**data)
                            count_add_record += 1
                            if model in (Review, Comment):
                                obj.pub_date = datetime.strptime(
                                    data['pub_date'],
                                    TIME_FORMAT,
                                ).replace(tzinfo=pytz.timezone('Asia/Kolkata'))
                                obj.save()
                    count_read_record += 1
                print(f'записей прочитано: {count_read_record}')
                print(
                    f'{count_add_record} записей добавлено в '
                    f'{model._meta.db_table} из {file}'
                )
