from django.db.models.expressions import Exists, OuterRef
from django.shortcuts import get_object_or_404
from rest_framework.filters import DjangoFilterBackend, SearchFilter
from rest_framework import status
from rest_framework.permissions import AllowAny, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.models import Favorite, Purchase
from recipes.filters import IngredientFilter, RecipeFilter
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
    filter_backends = [IngredientFilter]
    search_fields = ('^name', )
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    search_fields = ['name']
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filter_class = RecipeFilter
    permission_classes = [IsAuthorAdminModeratorOrReadOnly, ]

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeWriteSerializer

    def get_queryset(self):
        queryset = Recipe.objects.all()
        slug = self.request.query_params.get('tags')
        if slug is not None:
            queryset = queryset.filter(tags__slug=slug)
        author = self.request.query_params.get('author')
        if author is not None:
            queryset = queryset.filter(author__id=author)
        user = self.request.user
        if user.is_anonymous:
            return queryset
        queryset_filtered = queryset.annotate(
            is_favorited=Exists(Favorite.objects.filter(
                user=user, recipe_id=OuterRef('id')
            )),
            is_in_shopping_cart=Exists(Purchase.objects.filter(
                user=user, recipe_id=OuterRef('id')
            ))
        )
        if self.request.GET.get('is_favorited'):
            return queryset_filtered.filter(is_favorited=True)
        elif self.request.GET.get('is_in_shopping_cart'):
            return queryset_filtered.filter(is_in_shopping_cart=True)
        return queryset

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
