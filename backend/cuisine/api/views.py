from urllib import request
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from api.serializers import (
    TagSerializer, IngredientSerializer, RecipeSerializer,
    RecipeSerializerSave
)
from recipes.customfilters import RecipeFilter
from recipes.models import Tag, Ingredient, Recipe


class TagViewSet(ReadOnlyModelViewSet):
    """Read only view class for Tag model"""

    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(ReadOnlyModelViewSet):
    """Read only view class for Tag model"""

    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()


class RecipeViewSet(ModelViewSet):
    """View class for Recipes model"""

    filter_backends = (DjangoFilterBackend, )
    filterset_fields = ('author',)

    def get_queryset(self):
        queryset = Recipe.objects.all()
        tags = self.request.query_params.getlist('tags')
        is_favorited = self.request.query_params.get('is_favorited')
        shopping_cart = self.request.query_params.get('is_in_shopping_cart')
        if is_favorited == '1':
            queryset = queryset.filter(is_favorite=self.request.user)
        if shopping_cart == '1':
            queryset = queryset.filter(is_in_shopping_cart=self.request.user)
        if tags:
            queryset = queryset.filter(tags__slug__in=tags).distinct()
        return queryset

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'partial_update':
            return RecipeSerializerSave
        return RecipeSerializer
