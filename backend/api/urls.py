from django.conf.urls import url
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from api.views import (
    FavoriteViewSet,
    FollowApiView,
    FollowListApiView,
    PurchaseViewSet,
    download_cart
)

app_name = 'api'


urlpatterns = [
    path(
        'users/subscriptions/',
        FollowListApiView.as_view(),
        name='subscriptions'
    ),
    path(
        'recipes/download_shopping_cart/',
        download_cart, name='download'
    ),
    path(
        'users/<int:users_id>/subscribe/',
        FollowApiView.as_view(),
        name='subscribe',
    ),
    path(
        'recipes/<recipes_id>/favorite/',
        FavoriteViewSet.as_view(
            {'post': 'create', 'delete': 'delete'}
        ),
        name='favorite'
    ),
    path(
        'recipes/<recipes_id>/shopping_cart/',
        PurchaseViewSet.as_view(
            {'post': 'create', 'delete': 'delete'}
        ),
        name='cart'
    ),
    path(
        '',
        include('users.urls')
    ),
    path(
        '',
        include('recipes.urls')
    ),
]

schema_view = get_schema_view(
    openapi.Info(
        title='Foodgram API',
        default_version='v1',
        description='Документация для проекта Foodgram',
        contact=openapi.Contact(email='admin@foodgram.ru'),
        license=openapi.License(name='BSD License'),
    ),
    public=True,
    permission_classes=(
        permissions.AllowAny,
    ),
)

urlpatterns += [
    url(
        r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'
    ),
    url(
        r'^swagger/$',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),
    url(
        r'^redoc/$',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'
    ),
]
