from django.conf import settings
from django.contrib import admin

from users.models import User

EMPTY_VALUE = settings.EMPTY_VALUE


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name'
    )
    list_filter = (
        'email',
        'username'
    )
    search_fields = (
        'username',
        'email',
    )
    empty_value_display = EMPTY_VALUE
