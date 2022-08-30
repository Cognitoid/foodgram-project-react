from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Загрузка ингредиентов из csv-файла.'

    def handle(self, *args, **kwargs):

        from csv import reader

        from recipes.models import Ingredient

        with open(
                'data/ingredients.csv', 'r', encoding='UTF-8') as ingredients:
            for row in reader(ingredients):
                if len(row) == 2:
                    Ingredient.objects.get_or_create(
                        name=row[0], measurement_unit=row[1],
                    )
