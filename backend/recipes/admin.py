from django.conf import settings
from django.contrib import admin

from api.models import Favorite
from recipes.models import Ingredient, IngredientRecipe, Recipe, Tag

EMPTY_VALUE = settings.EMPTY_VALUE
STANDARD_INGREDIENT_QUANTITY = settings.STANDARD_INGREDIENT_QUANTITY


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'color',
        'slug'
    )
    list_filter = (
        'name',
        'color',
        'slug'
    )
    ordering = ('slug',)
    empty_value_display = EMPTY_VALUE


class IngredientRecipeInline(admin.TabularInline):
    model = IngredientRecipe
    extra = STANDARD_INGREDIENT_QUANTITY


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit'
    )
    search_fields = ('name',)
    list_filter = ('measurement_unit',)
    empty_value_display = EMPTY_VALUE


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientRecipeInline, )
    list_display = (
        'author',
        'name',
        'favorited'
    )
    search_fields = (
        'name',
        'author'
    )
    list_filter = ('tags',)
    readonly_fields = ['favorited']
    empty_value_display = EMPTY_VALUE

    def favorited(self, obj):
        return Favorite.objects.filter(recipe=obj).count()

    favorited.short_description = 'В избранном'
