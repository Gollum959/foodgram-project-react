from django.contrib import admin
from django.utils.html import format_html

from recipes.models import (Recipe, Tag, Ingredient, RecipeIngredient)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Displaying the Tag model in the admin panel."""

    list_display = ('colored_cooking_tag', 'slug', 'color', )
    search_fields = ('name', 'slug', )

    def colored_cooking_tag(self, obj):
        """Color display tags."""

        return format_html(
            '<span style="color: {};">{}</span>',
            obj.color,
            obj.name,
        )
    colored_cooking_tag.short_description = "Colored tag name"


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Displaying the Ingredient model in the admin panel."""

    list_display = ('name', 'measurement_unit', )
    list_filter = ('name', )
    search_fields = ('name', )


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    """Displaying the RecipeIngredient model in the admin panel."""

    list_display = ('recipe', 'ingredient', 'amount', )
    list_filter = ('recipe', )
    list_editable = ('amount', )


class RecipeIngredientInline(admin.TabularInline):
    """Display ingredients in recipe"""

    model = RecipeIngredient
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Displaying the Recipe model in the admin panel."""

    list_display = ('name', 'author', )
    list_filter = ('author', 'name', 'tags', )
 #   inlines = (RecipeIngredientInline, )

    def count_subscribers(self, obj):
        count = obj.user_set.count()
        return format_html('{} subscribers', count)

    readonly_fields = ('count_subscribers', )
