from django.conf import settings
from django.contrib import admin

from api.models import Favorite, Purchase, Subscriber

EMPTY_VALUE = settings.EMPTY_VALUE


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe'
    )
    search_fields = (
        'user',
    )
    empty_value_display = EMPTY_VALUE


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe'
    )
    search_fields = (
        'user',
    )
    empty_value_display = EMPTY_VALUE


@admin.register(Subscriber)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'author'
    )
    list_filter = (
        'user',
    )
    search_fields = (
        'user',
    )
    empty_value_display = EMPTY_VALUE
