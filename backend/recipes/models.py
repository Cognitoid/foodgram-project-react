from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from recipes.validators import latin_alphabet_number_validator

User = get_user_model()


class Tag(models.Model):
    RED = '#ff0000'
    ORANGE = '#ffa500'
    YELLOW = '#ffff00'
    GREEN = '#008000'
    BLUE = '#0000ff'
    INDIGO = '#4b0082'
    VIOLET = '#ee82ee'
    COLORLESS = 'null'

    COLOR_CHOICES = [
        (RED, 'Красный'),
        (ORANGE, 'Оранжевый'),
        (YELLOW, 'Жёлтый'),
        (GREEN, 'Зелёный'),
        (BLUE, 'Голубой'),
        (INDIGO, 'Синий'),
        (VIOLET, 'Фиолетовый'),
        (COLORLESS, 'Бесцветный')
    ]
    name = models.CharField(
        max_length=200, unique=True,
        verbose_name='Название'
    )
    color = models.CharField(
        max_length=7,
        unique=False,
        choices=COLOR_CHOICES,
        verbose_name='Цвет в HEX'
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        validators=[latin_alphabet_number_validator, ],
        verbose_name='Уникальный слаг'
    )

    class Meta:
        ordering = ['slug']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    GRAM = 'г'
    HANDFUL = 'горсть'
    SLICE = 'доль.'
    STAR = 'зв.'
    CLOVE = 'зуб.'
    DROP = 'кап.'
    KILOGRAM = 'кг'
    PIECE = 'кус.'
    LITER = 'л'
    SHEET = 'лист'
    MILLILITER = 'мл'
    BAG = 'пак.'
    PACK = 'пач.'
    LAYER = 'пласт'
    TOTASTE = 'по вкусу'
    BUNCH = 'пуч.'
    GLASS = 'ст.'
    TABLESPOON = 'ст.л.'
    STEM = 'стеб.'
    POD = 'стр.'
    CARCASS = 'туш.'
    PACKAGING = 'уп.'
    TEASPOON = 'ч.л.'
    PIECES = 'шт.'
    PINCH = 'щеп.'

    name = models.CharField(
        blank=False,
        null=False,
        max_length=200,
        verbose_name='Название ингредиента'
    )

    CHOICES = (
        (GRAM, 'грамм'),
        (HANDFUL, 'горсть'),
        (SLICE, 'долька'),
        (STAR, 'звездочка'),
        (CLOVE, 'зубчик'),
        (DROP, 'капля'),
        (KILOGRAM, 'килограмм'),
        (PIECE, 'кусок'),
        (LITER, 'литр'),
        (SHEET, 'лист'),
        (MILLILITER, 'миллилитр'),
        (BAG, 'пакетик'),
        (PACK, 'пачка'),
        (LAYER, 'пласт'),
        (TOTASTE, 'по вкусу'),
        (BUNCH, 'пучок'),
        (GLASS, 'стакан'),
        (TABLESPOON, 'столовая ложка'),
        (STEM, 'стебель'),
        (POD, 'стручок'),
        (CARCASS, 'тушка'),
        (PACKAGING, 'упаковка'),
        (TEASPOON, 'чайная ложка'),
        (PIECES, 'штук'),
        (PINCH, 'щепотка')
    )

    measurement_unit = models.CharField(
        blank=False,
        null=False,
        max_length=200,
        verbose_name='Единица измерения',
        choices=CHOICES
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Автор',
        related_name='recipes'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Изображение'
    )
    text = models.TextField(
        verbose_name='Описание'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        verbose_name='Ингредиенты',
        related_name='recipes'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тег',
        related_name='recipes'
    )
    cooking_time = models.IntegerField(
        validators=[
            MinValueValidator(
                1, message='Время приготовления не может быть меньше 1 минуты'
            ),
        ],
        verbose_name='Время приготовления'
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='ID ингредиента',
        related_name='recipe_amount'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        verbose_name='В составе рецепта',
        related_name='recipe_amount'
    )
    amount = models.IntegerField(
        validators=[
            MinValueValidator(
                1,
                message='Количество единиц ингредиента должно быть не менее 1!'
            ),
        ],
        blank=False,
        null=False
    )

    class Meta:
        ordering = ['ingredient__name']
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique combination ingredient-recipe'
            )
        ]
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'

    def __str__(self):
        return (
            f'{self.ingredient.name}: {self.amount} '
            f'{self.ingredient.measurement_unit}'
        )
