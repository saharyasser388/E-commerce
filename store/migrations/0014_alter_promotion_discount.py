# Generated by Django 5.1.5 on 2025-02-09 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotion',
            name='discount',
            field=models.IntegerField(),
        ),
    ]
