# Generated by Django 4.0.5 on 2025-01-29 19:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_card_expiration_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='expiration_date',
            field=models.DateField(default=datetime.datetime(2028, 1, 30, 1, 4, 17, 314303), verbose_name='Дата эксплуатации'),
        ),
    ]
