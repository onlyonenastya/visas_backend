# Generated by Django 4.2.5 on 2023-12-26 22:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visas', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='accepted',
            new_name='delivery_date',
        ),
        migrations.AlterField(
            model_name='order',
            name='date_created',
            field=models.DateField(blank=True, default=datetime.datetime(2023, 12, 26, 22, 28, 36, 805167, tzinfo=datetime.timezone.utc), null=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='order',
            name='date_of_formation',
            field=models.DateField(blank=True, default=datetime.datetime(2023, 12, 26, 22, 28, 36, 805167, tzinfo=datetime.timezone.utc), null=True, verbose_name='Дата формирования'),
        ),
    ]
