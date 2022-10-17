import django_filters

from .models import Ingredient


class IngredientFilter(django_filters.FilterSet):
    """Filter for Recipe by fields: name."""

    name = django_filters.CharFilter(lookup_expr='startswith')

    class Meta:
        model = Ingredient
        fields = ('name', )
