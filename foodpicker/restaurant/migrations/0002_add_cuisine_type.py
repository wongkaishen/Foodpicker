from django.db import migrations, models
from django.core import validators

class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='cuisine_type',
            field=models.CharField(
                choices=[
                    ('ASIAN', 'Asian'),
                    ('ITALIAN', 'Italian'),
                    ('MEXICAN', 'Mexican'),
                    ('AMERICAN', 'American'),
                    ('INDIAN', 'Indian'),
                    ('MEDITERRANEAN', 'Mediterranean'),
                    ('OTHER', 'Other'),
                ],
                default='OTHER',
                max_length=50,
                verbose_name='Cuisine Type'
            ),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='price_range',
            field=models.CharField(
                choices=[
                    ('$', 'Budget'),
                    ('$$', 'Moderate'),
                    ('$$$', 'Expensive'),
                    ('$$$$', 'Fine Dining'),
                ],
                default='$$',
                max_length=4,
                verbose_name='Price Range'
            ),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='phone',
            field=models.CharField(blank=True, max_length=20, verbose_name='Phone Number'),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='Email'),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='website',
            field=models.URLField(blank=True, verbose_name='Website'),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='average_rating',
            field=models.FloatField(
                default=0,
                validators=[
                    validators.MinValueValidator(0),
                    validators.MaxValueValidator(5)
                ],
                verbose_name='Average Rating'
            ),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='delivery_available',
            field=models.BooleanField(default=False, verbose_name='Delivery Available'),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='takeout_available',
            field=models.BooleanField(default=False, verbose_name='Takeout Available'),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='restaurant',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Active'),
        ),
    ] 