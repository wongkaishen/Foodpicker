# Generated by Django 5.0.2 on 2024-02-25 09:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0002_rename_ratings_rating_rename_rates_restaurant_rate'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Categorys',
            new_name='Category',
        ),
    ]
