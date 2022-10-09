from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from api.serializers import (
    TagSerializer, IngredientSerializer, RecipeSerializer,
    RecipeSerializerSave
)
from recipes.customfilters import RecipeFilterBackend
from recipes.customfilters import RecipeFilter
from recipes.models import Tag, Ingredient, Recipe
from users.models import User


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

    queryset = Recipe.objects.all()
    filter_backends = (RecipeFilterBackend, )
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'partial_update':
            return RecipeSerializerSave
        return RecipeSerializer
