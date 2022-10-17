from django.db import transaction
from djoser.serializers import UserSerializer, UserCreateSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import Tag, Ingredient, Recipe, RecipeIngredient
from users.models import User


class UserRegistrationSerializer(UserCreateSerializer):
    """Serializer for User registration."""

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
    """Serializer for User."""
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, user):
        """Returns true if user is subscribed"""
        user = self.context.get('request').user
        return (
            not user.is_anonymous and
            user in user.is_subscribed.get_queryset()
        )

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
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def get_is_favorited(self, obj):
        """Returns true if the recipe is in favorites"""
        user = self.context.get('request').user
        return (
            not user.is_anonymous and
            obj in user.is_favorite.get_queryset()
        )

    def get_is_in_shopping_cart(self, obj):
        """Returns true if the recipe is in shopping carts"""
        user = self.context.get('request').user
        return (
            not user.is_anonymous and
            obj in user.is_in_shopping_cart.get_queryset()
        )

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
            'is_favorited',
            'is_in_shopping_cart'
        )


class IngredientField(serializers.Serializer):
    """Serializer for ingredients inside a recipe"""
    id = serializers.IntegerField(min_value=0,)
    amount = serializers.DecimalField(
        max_digits=5, decimal_places=1, min_value=0.01
    )

    def validate(self, data):
        """Ingredient check"""
        if not Ingredient.objects.filter(pk=data.get('id')).exists():
            raise serializers.ValidationError(
                f'This ingredien id={data["id"]} doesn\'t exist')
        return data


class RecipeSerializerSave(serializers.ModelSerializer):
    """Serialazer for creating and updating model Recipe."""
    ingredients = IngredientField(many=True, allow_empty=False)
    tags = serializers.ListField(
        child=serializers.IntegerField(min_value=0), allow_empty=False,
    )
    image = Base64ImageField()

    def validate(self, data):
        """Tags existence and unique ingredients check"""
        tags = data.get('tags') if 'tags' in data.keys() else []
        for tag in tags:
            if not Tag.objects.filter(pk=tag).exists():
                raise serializers.ValidationError(
                    f'This tag id={tag} doesn\'t exist')
        ingrs = data.get('ingredients') if 'ingredients' in data.keys() else []
        uniq_ingrs = []
        for ingredient in ingrs:
            if ingredient.get('id') not in uniq_ingrs:
                uniq_ingrs.append(ingredient.get('id'))
            else:
                raise serializers.ValidationError(
                    'You have the same ingredients')
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
        validated_data['author'] = self.context.get('request').user
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)

        for ingredient in ingredients:
            current_ingredient = Ingredient.objects.get(
                pk=ingredient.get('id')
            )
            recipe.ingredients.add(
                current_ingredient,
                through_defaults={'amount': ingredient.get('amount')}
            )

        return recipe

    @transaction.atomic
    def update(self, recipe, validated_data):
        """Update record in model Recipes."""
        recipe.image = validated_data.get('image', recipe.image)
        recipe.name = validated_data.get('name', recipe.name)
        recipe.text = validated_data.get('text', recipe.text)
        recipe.cooking_time = validated_data.get(
            'cooking_time', recipe.cooking_time)
        if 'tags' in validated_data.keys():
            recipe.tags.set(validated_data.pop('tags'))
        if 'ingredients' in validated_data.keys():
            ingredients = validated_data.pop('ingredients')
            recipe.ingredients.clear()
            for ingredient in ingredients:
                current_ingredient = Ingredient.objects.get(
                    pk=ingredient.get('id'))
                recipe.ingredients.add(
                    current_ingredient,
                    through_defaults={'amount': ingredient.get('amount')}
                )
        recipe.save()
        return recipe


class IsFavoritAndCart(serializers.ModelSerializer):
    """Serializer for a recipe in favorite or cart"""

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class UserSubscriptionSerializer(SpecialUserSerializer):
    """Serializer for user subscription"""
    recipes = serializers.SerializerMethodField('get_items')
    recipes_count = serializers.IntegerField(read_only=True)

    def get_items(self, user):
        """Limitation on the number of recipes"""
        recipes_limit = self.context.get('request').query_params.get(
            'recipes_limit', default='')
        recipes = user.recipe.all()
        if recipes_limit.isnumeric() and int(recipes_limit) > 0:
            recipes = recipes[:int(recipes_limit)]
        serializer = IsFavoritAndCart(instance=recipes, many=True)
        return serializer.data

    class Meta:
        model = User
        fields = SpecialUserSerializer.Meta.fields + (
            'recipes',
            'recipes_count',
        )
