# Generated by Django 5.1.7 on 2025-04-08 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_remove_customuser_is_seller_verified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='phone',
            field=models.CharField(max_length=15, unique=True),
        ),
    ]
