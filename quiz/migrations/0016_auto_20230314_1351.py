# Generated by Django 2.2.28 on 2023-03-14 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0015_auto_20230313_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outcome',
            name='image',
            field=models.ImageField(upload_to='outcome_images'),
        ),
    ]