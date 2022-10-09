import django_filters
from django_filters.rest_framework import DjangoFilterBackend

from recipes.models import Recipe


class RecipeFilterBackend(DjangoFilterBackend):
    def get_filterset_kwargs(self, request, queryset, view):
        kwargs = super().get_filterset_kwargs(request, queryset, view)

        # merge filterset kwargs provided by view class
        #if hasattr(view, 'currentUser'):
        kwargs.update({'currentUser': request.user})

        return kwargs

class EmptyStringFilter(django_filters.BooleanFilter):
    def filter(self, qs, value):
        if value:
            return qs.filter(is_subscribe = self.user)
        else:
            return qs    


class RecipeFilter(django_filters.FilterSet):
    """Filter for Recepi by fields: author, tags."""

    def __init__(self, *args, **kwargs):
  #      self.user = kwargs.pop('user')
        self.user = kwargs['currentUser']
        kwargs.pop('currentUser')
        super(RecipeFilter, self).__init__(*args, **kwargs)
        print(self.user)

    tags = django_filters.CharFilter(
        field_name="tags__slug",
    )

    is_favorite = EmptyStringFilter(field_name='is_subscribed')

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorite')


