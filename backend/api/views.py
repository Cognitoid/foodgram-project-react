from django.db import IntegrityError
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from api.models import Favorites, Purchase, Subscriber
from api.serializers import (
    FavoriteSerializer,
    PurchaseSerializer,
    UserSubscribeSerializer
)
from recipes.models import IngredientRecipe, Recipe
from users.models import User


@api_view(['GET', ])
@permission_classes([IsAuthenticated])
def DownloadCart(request):
    purchase_list = IngredientRecipe.objects.filter(
        recipe__purchase__user=request.user
    ).values(
        'ingredient__name',
        'ingredient__measurement_unit'
    ).annotate(amount=Sum('amount'))
    shopping_list = []
    for item in purchase_list:
        shopping_list.append(
            f'{item["ingredient__name"]}: {item["amount"]} '
            f'{item["ingredient__measurement_unit"]}\n'
        )
    response = HttpResponse(shopping_list, 'Content-Type: text/plain')
    response['Content-Disposition'] = (
        'attachment;'
        'filename="shopping_list.txt"'
    )
    return response


class FollowListApiView(ListAPIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserSubscribeSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(author__user=user)


class FollowApiView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, users_id):
        user = request.user
        data = {
            'author': users_id,
            'user': user.id
        }
        serializer = UserSubscribeSerializer(
            data=data,
            context={'request': request}
        )
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, users_id):
        user = request.user
        if user.is_anonymous:
            data = {
                'errors': 'Учетные данные не были предоставлены.'
            }
            return Response(
                data=data,
                status=status.HTTP_401_UNAUTHORIZED
            )
        author = get_object_or_404(
            User,
            id=users_id
        )
        if author is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        deleting_entry = Subscriber.objects.filter(
            user=user,
            author=author
        )
        if deleting_entry is not None:
            deleting_entry.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class BaseFavoriteCartViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, ]

    def create(self, request, *args, **kwargs):
        if self.model == Favorites:
            model_context = 'избранное'
        else:
            model_context = 'список покупок'
        user = request.user
        if user.is_anonymous:
            data = {
                'errors': 'Учетные данные не были предоставлены.'
            }
            return Response(
                data=data,
                status=status.HTTP_401_UNAUTHORIZED
            )
        recipe = int(self.kwargs['recipes_id'])
        recipe = get_object_or_404(
            Recipe,
            id=recipe
        )
        try:
            self.model.objects.create(
                user=request.user,
                recipe=recipe
            )
        except IntegrityError:
            data = {
                'errors': f'Ошибка добавления в {model_context}.'
            }
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        data = {
            'status': f'Рецепт успешно добавлен в {model_context}.'
        }
        return Response(data=data, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        if self.model == Favorites:
            model_context = 'избранное'
        else:
            model_context = 'список покупок'
        user = request.user
        if user.is_anonymous:
            data = {
                'errors': 'Учетные данные не были предоставлены.'
            }
            return Response(
                data=data,
                status=status.HTTP_401_UNAUTHORIZED
            )
        recipe = self.kwargs['recipes_id']
        user_id = request.user.id
        try:
            self.model.objects.get(
                user__id=user_id,
                recipe__id=recipe
            ).delete()
        except self.model.DoesNotExist:
            data = {
                'errors': f'Ошибка удаления из {model_context}.'
            }
            return Response(
                data=data,
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'status': f'Рецепт успешно удален из {model_context}.'
        }
        return Response(data=data)


class PurchaseViewSet(BaseFavoriteCartViewSet):
    serializer_class = PurchaseSerializer
    queryset = Purchase.objects.all()
    model = Purchase


class FavoriteViewSet(BaseFavoriteCartViewSet):
    serializer_class = FavoriteSerializer
    queryset = Favorites.objects.all()
    model = Favorites
