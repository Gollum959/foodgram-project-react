from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import TagViewSet, IngredientViewSet, RecipeViewSet

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('tags', TagViewSet, basename='tags')
router_v1.register('ingredients', IngredientViewSet, basename='ingredients')
router_v1.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
