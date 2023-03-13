# Generated by Django 2.2.28 on 2023-03-09 17:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_auto_20230309_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer', to='quiz.Question'),
        ),
        migrations.DeleteModel(
            name='UserAnswer',
        ),
    ]