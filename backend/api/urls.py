from django.urls import include, path

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
