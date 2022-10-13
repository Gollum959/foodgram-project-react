from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLES = [
        ('user', 'USER'),
        ('moderator', 'MODERATOR'),
        ('admin', 'ADMINISTRATOR'),
    ]

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    role = models.CharField(
        verbose_name='User role',
        max_length=15,
        choices=ROLES,
        default='user',
        help_text='The rights that the user has'
    )
    is_superuser = models.BooleanField(null=True)
    is_favorite = models.ManyToManyField(
        'recipes.Recipe',
        related_name='is_favorite',
        blank=True
    )
    is_subscribed = models.ManyToManyField(
        'User',
        related_name='subscribed',
        blank=True
    )
    is_in_shopping_cart = models.ManyToManyField(
        'recipes.Recipe',
        related_name='is_in_shopping_cart',
        blank=True)

    class Meta:
        ordering = ('id', )
