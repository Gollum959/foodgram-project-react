# Generated by Django 2.2.16 on 2022-09-29 15:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_auto_20220929_1712'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ingredient',
            old_name='units',
            new_name='measurement_unit',
        ),
    ]
