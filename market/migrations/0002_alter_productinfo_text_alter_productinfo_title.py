# Generated by Django 5.1.7 on 2025-03-18 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productinfo',
            name='text',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='productinfo',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
