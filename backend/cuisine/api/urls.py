from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    TagViewSet, IngredientViewSet, RecipeViewSet, AddRemoveFavoriteView,
    AddRemoveCartView, UserSubscription, AddRemoveSubscriptionView,
    UserShoppingCart)

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('tags', TagViewSet, basename='tags')
router_v1.register('ingredients', IngredientViewSet, basename='ingredients')
router_v1.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path(
        r'recipes/<int:recipe_id>/favorite/',
        AddRemoveFavoriteView.as_view()
    ),
    path(
        r'recipes/<int:recipe_id>/shopping_cart/',
        AddRemoveCartView.as_view()
    ),
    path(
        r'users/<int:user_id>/subscribe/',
        AddRemoveSubscriptionView.as_view()
    ),
    path('users/subscriptions/', UserSubscription.as_view()),
    path('recipes/download_shopping_cart/', UserShoppingCart.as_view()),
    path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
