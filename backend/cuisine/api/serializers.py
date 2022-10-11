from django.db import transaction
from djoser.serializers import UserSerializer, UserCreateSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import Tag, Ingredient, Recipe, RecipeIngredient
from users.models import User


class UserRegistrationSerializer(UserCreateSerializer):

    class Meta(UserCreateSerializer.Meta):
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password'
        )


class SpecialUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        request = self.context.get('request', None)
        if request:
            return obj in request.user.is_subscribed.get_queryset()
        return False

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )


class TagSerializer(serializers.ModelSerializer):
    """Serializer for model Tag"""

    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for model Ingredient"""

    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount'
        )


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Serializer for model RecipeIngredient"""
    name = serializers.CharField(source='ingredient.name')
    id = serializers.IntegerField(source='ingredient.pk')
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )


class RecipeSerializer(serializers.ModelSerializer):
    """Serialazer for geting model Recipe."""

    tags = TagSerializer(many=True, )
    author = SpecialUserSerializer()
    ingredients = RecipeIngredientSerializer(
        source='recipeingredient_set', many=True,
    )
    is_favorite = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def get_is_favorite(self, obj):
        request = self.context.get('request', None)
        if request:
            return obj in request.user.is_favorite.get_queryset()
        return False

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request', None)
        if request:
            return obj in request.user.is_in_shopping_cart.get_queryset()
        return False

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
            'is_favorite',
            'is_in_shopping_cart'
        )


class IngredientField(serializers.Serializer):
    id = serializers.IntegerField(min_value=0)
    amount = serializers.DecimalField(
        max_digits=5, decimal_places=1, min_value=0.01
    )

    def validate(self, data):
        if not Ingredient.objects.filter(pk=data['id']).exists():
            raise serializers.ValidationError('This ingredien doesn\'t exist')
        return data


class RecipeSerializerSave(serializers.ModelSerializer):

    ingredients = IngredientField(many=True, allow_empty=False)
    tags = serializers.ListField(
        child=serializers.IntegerField(min_value=0), allow_empty=False
    )
    image = Base64ImageField()

    def validate(self, data):
        for tag in data['tags']:
            if not Tag.objects.filter(pk=tag).exists():
                raise serializers.ValidationError('This tag doesn\'t exist')
        return data

    class Meta:
        model = Recipe
        fields = (
            'image',
            'name',
            'text',
            'cooking_time',
            'ingredients',
            'tags',
        )

    def to_representation(self, recipe):
        """Creates response using serializer RecipesSerializer."""
        serializer = RecipeSerializer(instance=recipe, context=self.context)
        return serializer.data

    @transaction.atomic
    def create(self, validated_data):
        """Creates record in model Recipes."""
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        validated_data['author'] = self.context['request'].user
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)

        for ingredient in ingredients:
            current_ingredient = Ingredient.objects.get(pk=ingredient['id'])
            recipe.ingredients.add(
                current_ingredient,
                through_defaults={'amount': ingredient['amount']}
            )

        return recipe

    @transaction.atomic
    def update(self, recipe, validated_data):
        recipe.image = validated_data.get('image', recipe.image)
        recipe.name = validated_data.get('name', recipe.name)
        recipe.text = validated_data.get('text', recipe.text)
        recipe.cooking_time = validated_data.get(
            'cooking_time', recipe.cooking_time)
        recipe.tags.set(validated_data.pop('tags'))
        ingredients = validated_data.pop('ingredients')
        recipe.ingredients.clear()
        for ingredient in ingredients:
            current_ingredient = Ingredient.objects.get(pk=ingredient['id'])
            recipe.ingredients.add(
                current_ingredient,
                through_defaults={'amount': ingredient['amount']}
            )
        recipe.save()
        return recipe


class IsFavoritAndCart(serializers.ModelSerializer):
    """Serializer for """

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class UserSubscriptionSerializer(SpecialUserSerializer):
    """Serializer for """
    recipe = serializers.SerializerMethodField('get_items')
    is_subscribed = serializers.SerializerMethodField()
    recipes_count = serializers.IntegerField(read_only=True)

    def get_items(self, data):
        recipes_limit = self.context['request'].query_params.get(
            'recipes_limit', default='')
        recipes = Recipe.objects.filter(author=data)
        if recipes_limit.isnumeric() and int(recipes_limit) > 0:
            recipes = Recipe.objects.filter(author=data)[:int(recipes_limit)]
        serializer = IsFavoritAndCart(instance=recipes, many=True)
        return serializer.data

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
            'is_subscribed',
            'recipe',
            'recipes_count',
        )
