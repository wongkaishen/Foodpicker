# Generated by Django 5.0.2 on 2024-03-04 14:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0005_alter_restaurant_rate'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Rating',
        ),
    ]