# Generated by Django 2.2.16 on 2022-10-05 12:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0007_auto_20220930_1130'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipeingredient',
            old_name='quantity',
            new_name='amount',
        ),
    ]
