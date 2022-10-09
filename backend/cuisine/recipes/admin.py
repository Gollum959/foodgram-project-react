from django.contrib import admin
from django.utils.html import format_html

from recipes.models import (Recipe, Tag, Ingredient, RecipeIngredient)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('colored_cooking_tag', 'slug', 'color', )
    search_fields = ('name', 'slug', )

    def colored_cooking_tag(self, obj):
        return format_html(
            '<span style="color: {};">{}</span>',
            obj.color,
            obj.name,
        )
    colored_cooking_tag.short_description = "Colored tag name"


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit', )
    list_filter = ('name', )
    search_fields = ('name', )


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount', )
    list_filter = ('recipe', )
    list_editable = ('amount', )


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', )
    list_filter = ('author', 'name', 'tags', )
    inlines = (RecipeIngredientInline, )

    def count_subscribers(self, obj):
        count = obj.user_set.count()
        return format_html('{} subscribers', count)

    readonly_fields = ('count_subscribers', )
