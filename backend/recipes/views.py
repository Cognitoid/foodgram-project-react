from django.db.models.expressions import Exists, OuterRef, Value
from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework import status
from rest_framework.permissions import AllowAny, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.models import Favorites, Purchase
from recipes.models import Ingredient, Recipe, Tag
from recipes.permissions import IsAuthorAdminModeratorOrReadOnly
from recipes.serializers import (
    IngredientSerializer,
    RecipeReadSerializer,
    RecipeWriteSerializer,
    TagSerializer
)


class TagsViewSet(ReadOnlyModelViewSet):
    permission_classes = (AllowAny, )
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientsViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny, )
    search_fields = ['name']
    filter_backends = (filters.SearchFilter, )
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    search_fields = ['name']
    filter_backends = (filters.SearchFilter, )
    permission_classes = [IsAuthorAdminModeratorOrReadOnly, ]

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeWriteSerializer

    def get_queryset(self):
        return Recipe.objects.annotate(
            is_favorited=Exists(
                Favorites.objects.filter(
                    user=self.request.user, recipe=OuterRef('id')
                )
            ),
            is_in_shopping_cart=Exists(
                Purchase.objects.filter(
                    user=self.request.user,
                    recipe=OuterRef('id')
                )
            )
        ).select_related('author').prefetch_related(
            'tags', 'ingredients'
        ) if self.request.user.is_authenticated else Recipe.objects.annotate(
            is_in_shopping_cart=Value(False),
            is_favorited=Value(False)
        ).select_related('author').prefetch_related(
            'tags', 'ingredients'
        )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def delete(self, request, recipe):
        user = request.user
        if user.is_anonymous:
            data = {
                'errors': 'Учетные данные не были предоставлены.'
            }
            return Response(
                data=data,
                status=status.HTTP_401_UNAUTHORIZED
            )
        recipe = get_object_or_404(
            Recipe,
            id=recipe
        )
        recipe.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
