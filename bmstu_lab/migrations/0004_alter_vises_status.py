# Generated by Django 4.2.4 on 2023-10-19 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bmstu_lab', '0003_alter_vises_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vises',
            name='status',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
