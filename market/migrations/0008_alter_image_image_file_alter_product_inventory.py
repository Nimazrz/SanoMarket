# Generated by Django 5.1.7 on 2025-07-16 01:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0007_alter_product_unique_together_remove_product_starts_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image_file',
            field=models.ImageField(max_length=500, upload_to='None/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='inventory',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
