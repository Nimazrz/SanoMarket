# Generated by Django 5.1.7 on 2025-03-26 11:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_alter_order_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='city',
        ),
        migrations.RemoveField(
            model_name='order',
            name='postal_code',
        ),
        migrations.RemoveField(
            model_name='order',
            name='province',
        ),
    ]
