from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from recipes.validators import hex_color_valid
from users.models import User


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='Recipe author'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Recipe name',
    )
    text = models.TextField(
        verbose_name='Recipe description',
    )
    image = models.ImageField(
        upload_to='recipe',
        verbose_name='Recipe image',
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='RecipeIngredient',
    )
    tags = models.ManyToManyField('Tag')
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Cooking time',
        validators=(
            MinValueValidator(1),
            MaxValueValidator(1440)
        )
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('pub_date', )

    def __str__(self) -> str:
        return self.name


class Tag(models.Model):
    name = models.CharField(
        unique=True,
        max_length=200,
        verbose_name='Cooking tag',
        help_text='Name cooking tag'
    )
    color = models.CharField(
        unique=True,
        max_length=7,
        validators=[hex_color_valid],
        verbose_name='Tag color',
    )
    slug = models.SlugField(
        unique=True,
        help_text='Cooking slug'
    )

    class Meta:
        ordering = ('name', )

    def __str__(self) -> str:
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Recipe ingredient'
    )
    measurement_unit = models.CharField(
        max_length=30,
        verbose_name='Unit'
    )

    class Meta:
        ordering = ('name', )

    def __str__(self) -> str:
        return f'{self.name}, {self.measurement_unit}'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE
    )
    amount = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        validators=(
            MinValueValidator(0.01),
        )
    )

    class Meta:
        ordering = ('recipe', 'ingredient', )
