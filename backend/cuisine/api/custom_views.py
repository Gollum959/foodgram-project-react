from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import IsFavoritAndCart
from recipes.models import Recipe


class CuisineSubscriber(APIView):
    """Custom class for subscription."""

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
