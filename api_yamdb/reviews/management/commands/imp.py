import csv

from django.core.management.base import BaseCommand
from reviews.models import Category, Genre, Title
from users.models import User

FILE_PREFIX = 'static/data/'


class Command(BaseCommand):
    def handle(self, *args, **options):
        for obj_data in self.read_csv('genre.csv'):
            Genre.objects.create(**obj_data)

        for obj_data in self.read_csv('category.csv'):
            Category.objects.create(**obj_data)

        for obj_data in self.read_csv('titles.csv'):
            Title.objects.create(**obj_data)

        for obj_data in self.read_csv('users.csv'):
            User.objects.create(**obj_data)

        print("Данные в БД из CSV загружены успешно.")

    def read_csv(self, filename):
        with open(FILE_PREFIX + filename, 'r') as csv_file:
            reader = csv.reader(csv_file)
            fields = next(reader)
            res = []
            for row in reader:
                kwargs = {}
                for num in range(0, len(fields)):
                    field_name = fields[num]
                    if field_name == 'id':
                        field_value = int(row[num])
                    elif field_name == 'category':
                        field_value = Category.objects.get(id=int(row[num]))
                    elif field_name == 'genre':
                        field_value = Genre.objects.get(id=int(row[num]))
                    elif field_name == 'title':
                        field_value = Title.objects.get(id=int(row[num]))
                    else:
                        field_value = row[num]

                    kwargs[field_name] = field_value

                res.append(kwargs)
            return res
