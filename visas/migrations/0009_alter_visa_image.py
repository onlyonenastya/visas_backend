# Generated by Django 4.2.7 on 2024-01-03 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visas', '0008_alter_order_date_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visa',
            name='image',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Фото'),
        ),
    ]
