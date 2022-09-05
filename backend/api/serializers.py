from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api.models import Purchase, Subscriber
from recipes.models import Recipe
from recipes.serializers import RecipeReadSerializer
from users.models import User


class RecipeSubscriptionSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class UserSubscribeSerializer(serializers.ModelSerializer):

    author = serializers.SlugRelatedField(
        slug_field='id',
        queryset=User.objects.all()
    )
    user = serializers.SlugRelatedField(
        slug_field='id',
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = '__all__'
        model = Subscriber
        validators = [
            UniqueTogetherValidator(
                queryset=Subscriber.objects.all(),
                fields=('user', 'author'),
                message='Такая подписка уже существует'
            )
        ]

    def validate(self, data):
        if (data['user'] == data['author']
                and self.context['request'].method == 'GET'):
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя'
            )
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        try:
            return SubscribeListSerializer(
                instance.author,
                context={'request': request}
            ).data
        except AttributeError:
            return SubscribeListSerializer(
                instance,
                context={'request': request}
            ).data


class SubscribeListSerializer(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_is_subscribed(self, user):
        current_user = self.context.get('current_user')
        other_user = user.author.all()
        if user.is_anonymous:
            return False
        if other_user.count() == 0:
            return False
        return Subscriber.objects.filter(
            user=user,
            author=current_user
        ).exists()

    def get_recipes(self, obj):
        recipes_limit = self.context.get('request').GET.get(
            'recipes_limit',
            None
        )
        if recipes_limit is not None:
            recipes = obj.recipes.all()[:int(recipes_limit)]
        else:
            recipes = obj.recipes.all()
        request = self.context.get('request')
        return RecipeReadSerializer(
            recipes,
            many=True,
            context={'request': request}
        ).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = (
            'user',
            'recipe'
        )
