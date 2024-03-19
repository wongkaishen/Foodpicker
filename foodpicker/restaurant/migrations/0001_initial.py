# Generated by Django 5.0.2 on 2024-02-25 09:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categorys',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Location Name')),
                ('address', models.CharField(max_length=200)),
                ('zip_code', models.CharField(blank=True, max_length=200, null=True, verbose_name='Zip Code')),
                ('phone', models.CharField(blank=True, max_length=25, null=True, verbose_name='Contact Phone')),
                ('web', models.URLField(blank=True, verbose_name='Web Address')),
                ('email_address', models.EmailField(blank=True, max_length=200, null=True, verbose_name='Email Address')),
            ],
        ),
        migrations.CreateModel(
            name='Ratings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=200, verbose_name='User Email Address')),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Restaurant Name')),
                ('price', models.DecimalField(decimal_places=2, max_digits=4)),
                ('time', models.DateTimeField(verbose_name='Working Hour')),
                ('rates', models.IntegerField(blank=True, null=True)),
                ('category', models.ManyToManyField(default='Non Categorized', to='restaurant.categorys')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='restaurant.location')),
                ('customer', models.ManyToManyField(blank=True, to='restaurant.user')),
            ],
        ),
    ]