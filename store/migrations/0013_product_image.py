# Generated by Django 5.1.5 on 2025-02-08 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_product_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='product_images/'),
        ),
    ]
