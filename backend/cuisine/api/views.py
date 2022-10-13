from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

from api.serializers import (
    TagSerializer, IngredientSerializer, RecipeSerializer,
    RecipeSerializerSave, IsFavoritAndCart, UserSubscriptionSerializer
)
from recipes.models import Tag, Ingredient, Recipe, RecipeIngredient
from api.permissions import IsAuthorOrAdmin
from users.models import User


class TagViewSet(ReadOnlyModelViewSet):
    """Read only view class for Tag model"""

    serializer_class = TagSerializer
    permission_classes = (AllowAny, )
    pagination_class = None
    queryset = Tag.objects.all()


class IngredientViewSet(ReadOnlyModelViewSet):
    """Read only view class for Tag model"""

    serializer_class = IngredientSerializer
    permission_classes = (AllowAny, )
    pagination_class = None
    queryset = Ingredient.objects.all()


class RecipeViewSet(ModelViewSet):
    """View class for Recipes model"""

    filter_backends = (DjangoFilterBackend, )
    permission_classes = (IsAuthorOrAdmin, )
    filterset_fields = ('author',)

    def get_queryset(self):
        queryset = Recipe.objects.all()
        tags = self.request.query_params.getlist('tags')
        is_favorited = self.request.query_params.get('is_favorited')
        shopping_cart = self.request.query_params.get('is_in_shopping_cart')
        if is_favorited == '1' and not self.request.user.is_anonymous:
            queryset = queryset.filter(is_favorite=self.request.user)
        if shopping_cart == '1' and not self.request.user.is_anonymous:
            queryset = queryset.filter(is_in_shopping_cart=self.request.user)
        if tags:
            queryset = queryset.filter(tags__slug__in=tags).distinct()
        return queryset

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'partial_update':
            return RecipeSerializerSave
        return RecipeSerializer


class UserSubscription(generics.ListAPIView):

    serializer_class = UserSubscriptionSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = user.is_subscribed.all().annotate(
            recipes_count=Count('recipe'))
        return queryset


class CuisineSubscriber():

    def subscribe(self, recipe_id, user_filed):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        if recipe in user_filed.get_queryset():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            user_filed.add(recipe)
            serializer = IsFavoritAndCart(recipe)
            return Response(serializer.data)

    def del_subscribe(self, recipe_id, user_filed):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        if recipe in user_filed.get_queryset():
            user_filed.remove(recipe)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class AddRemoveCartView(APIView, CuisineSubscriber):

    def post(self, request, recipe_id):
        resp = self.subscribe(recipe_id, self.request.user.is_in_shopping_cart)
        if resp.status_code == 400:
            resp.data = {'recipe': f'recipe ID={recipe_id} already in cart'}
        return resp

    def delete(self, request, recipe_id):
        resp = self.del_subscribe(
            recipe_id, self.request.user.is_in_shopping_cart)
        if resp.status_code == 400:
            resp.data = {'recipe': f'recipe ID={recipe_id} not in cart'}
        return resp


class AddRemoveFavoriteView(APIView, CuisineSubscriber):

    def post(self, request, recipe_id):
        resp = self.subscribe(recipe_id, self.request.user.is_favorite)
        if resp.status_code == 400:
            resp.data = {
                'recipe': f'recipe ID={recipe_id} already in favorite'}
        return resp

    def delete(self, request, recipe_id):
        resp = self.del_subscribe(recipe_id, self.request.user.is_favorite)
        if resp.status_code == 400:
            resp.data = {'recipe': f'recipe ID={recipe_id} not in favorite'}
        return resp


class AddRemoveSubscriptionView(APIView):

    def post(self, request, user_id):
        sub_user = get_object_or_404(User, pk=user_id)
        if sub_user in self.request.user.is_subscribed.get_queryset():
            return Response(
                {'user': f'user ID={user_id} already in subscribed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            self.request.user.is_subscribed.add(sub_user)
            sub_user.recipes_count = sub_user.recipe.count()
            serializer = UserSubscriptionSerializer(
                instance=sub_user,
                context={'request': request}
            )
            return Response(serializer.data)

    def delete(self, request, user_id):
        sub_user = get_object_or_404(User, pk=user_id)
        if sub_user in self.request.user.is_subscribed.get_queryset():
            self.request.user.is_subscribed.remove(sub_user)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {'user': f'user ID={user_id} not in subscribed'},
                status=status.HTTP_400_BAD_REQUEST
            )


class UserShoppingCart(APIView):

    def get(self, request):
        shoping_cart = {}
        for recipe in self.request.user.is_in_shopping_cart.get_queryset():
            for ingredient in RecipeIngredient.objects.filter(recipe=recipe):
                name = ingredient.ingredient.name
                amount = ingredient.amount
                if name in shoping_cart.keys():
                    shoping_cart[name] += amount
                else:
                    shoping_cart[name] = amount
        print(shoping_cart)
        return Response(
                {'user': 'user ID=jopa already in subscribed'},
                status=status.HTTP_400_BAD_REQUEST
        )
