# Generated by Django 2.2.28 on 2023-03-22 15:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0017_auto_20230321_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='quiz.UserProfile'),
        ),
    ]
