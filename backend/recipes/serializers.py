from rest_framework.serializers import (
    IntegerField,
    ModelSerializer,
    PrimaryKeyRelatedField,
    ReadOnlyField,
    SerializerMethodField,
    ValidationError
)

from api.models import Purchase
from recipes.fields import Base64ImageField
from recipes.models import (
    Ingredient,
    IngredientRecipe,
    Recipe,
    Tag
)
from users.serializers import SpecialUserSerializer


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug'
        )


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit'
        )


class IngredientRecipeReadSerializer(ModelSerializer):
    id = ReadOnlyField(source='ingredient.id')
    name = ReadOnlyField(source='ingredient.name')
    measurement_unit = ReadOnlyField(
        source='ingredient.measurement_unit'
    )
    amount = ReadOnlyField()

    class Meta:
        model = IngredientRecipe
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount'
        )


class IngredientRecipeWriteSerializer(ModelSerializer):
    id = IntegerField(write_only=True)
    amount = IntegerField()

    class Meta:
        model = IngredientRecipe
        fields = (
            'id',
            'amount'
        )


class RecipeWriteSerializer(ModelSerializer):
    image = Base64ImageField()
    tags = PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    ingredients = IngredientRecipeWriteSerializer(
        many=True,
        required=True
    )

    class Meta:
        model = Recipe
        fields = '__all__'
        read_only_fields = ('author',)

    def validate(self, data):
        ingredients = data['ingredients']
        if not ingredients:
            raise ValidationError(
                {'ingredients': 'Добавьте не менее 1 ингредиента для рецепта'}
            )
        ingredients_set = set()
        for ingredient in ingredients:
            if ingredient['id'] in ingredients_set:
                raise ValidationError(
                    f'Ингредиент с ID={ingredient["id"]} не должен повторяться'
                )
            if ingredient['amount'] < 1:
                raise ValidationError(
                    f'Количество ингредиента {ingredient["name"]}'
                    f' не может быть отрицательным'
                )
            ingredients_set.add(ingredient['id'])
        data['ingredients'] = ingredients
        tags = data['tags']
        tags_set = set()
        for tag in tags:
            if tag in tags_set:
                raise ValidationError(
                    f'Тег с ID={tag} не должен повторяться'
                )
            tags_set.add(tag)
        data['tags'] = tags
        return data

    @staticmethod
    def add_ingredients(ingredients, recipe):
        IngredientRecipe.objects.bulk_create(
            [
                IngredientRecipe(
                    ingredient_id=ingredient['id'],
                    recipe=recipe,
                    amount=ingredient['amount'],
                ) for ingredient in ingredients
            ]
        )

    @staticmethod
    def add_tags(tags, recipe):
        for tag in tags:
            recipe.tags.add(tag)

    def create(self, validated_data):
        tags_data = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredients')
        validated_data.pop('author')
        recipe = Recipe.objects.create(
            author=self.context.get('request').user,
            image=validated_data.pop('image'),
            cooking_time=validated_data.pop('cooking_time'),
            **validated_data
        )

        self.add_ingredients(ingredients_data, recipe)
        self.add_tags(tags_data, recipe)
        return recipe

    def update(self, instance, validated_data):
        instance.tags.clear()
        IngredientRecipe.objects.filter(recipe=instance).delete()
        self.add_tags(
            validated_data.pop('tags'),
            instance
        )
        self.add_ingredients(
            validated_data.pop('ingredients'),
            instance
        )
        return super().update(
            instance,
            validated_data
        )

    def to_representation(self, instance):
        return RecipeReadSerializer(
            instance,
            context={
                'request': self.context.get('request')
            }).data


class RecipeReadSerializer(ModelSerializer):
    image = SerializerMethodField()
    tags = TagSerializer(
        many=True,
        read_only=True)
    author = SpecialUserSerializer(
        read_only=True
    )
    ingredients = IngredientRecipeReadSerializer(
        source='recipe_amount',
        many=True,
        read_only=True
    )
    is_favorited = SerializerMethodField(
        read_only=True
    )
    is_in_shopping_cart = SerializerMethodField(
        read_only=True
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(
            favorite__user=user,
            id=obj.id
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Purchase.objects.filter(
            user=self.context.get('request').user,
            recipe=obj
        ).exists()

    def get_image(self, obj):
        return obj.image.url
