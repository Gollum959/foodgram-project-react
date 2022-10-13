import django_filters

from recipes.models import Recipe


class CharInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass


class RecipeFilter(django_filters.FilterSet):
    """Filter for Recepi by fields: author, tags."""

    tags = django_filters.MultipleChoiceFilter(
        field_name="tags__slug",
        lookup_expr='in',
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author',)
