# Generated by Django 5.1.7 on 2025-04-07 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0003_alter_image_image_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('electronics', 'کالای دیجیتال'), ('clothing', 'پوشاک'), ('books', 'کتاب و لوازم تحریر'), ('home_appliances', 'لوازم خانگی'), ('beauty', 'آرایشی و بهداشتی'), ('toys', 'اسباب\u200cبازی و کودک'), ('sports', 'ورزشی و سفر'), ('food', 'خواروبار'), ('automotive', 'خودرو و موتور'), ('jewelry', 'زیورآلات و اکسسوری'), ('furniture', 'مبلمان و دکوراسیون'), ('medical', 'تجهیزات پزشکی'), ('music', 'موسیقی و آلات موسیقی'), ('others', 'چیز های دیگر')], db_index=True, default='electronics', max_length=20),
        ),
    ]
