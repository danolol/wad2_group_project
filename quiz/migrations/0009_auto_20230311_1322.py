# Generated by Django 2.2.28 on 2023-03-11 13:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0008_merge_20230311_1321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]