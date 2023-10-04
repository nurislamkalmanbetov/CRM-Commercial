# Generated by Django 3.2 on 2023-09-05 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_favoritevacancy'),
    ]

    operations = [
        migrations.AddField(
            model_name='vacancy',
            name='language',
            field=models.CharField(blank=True, choices=[('de', 'Немецкий'), ('ru', 'Руский'), ('en', 'Английский')], default='', max_length=2, verbose_name='Язык'),
        ),
        migrations.AddField(
            model_name='vacancy',
            name='proficiency',
            field=models.CharField(blank=True, choices=[('A1', 'A1'), ('A2', 'A2'), ('B1', 'B1'), ('B2', 'B2'), ('C1', 'C1'), ('C2', 'C2')], default='', max_length=2, verbose_name='Уровень владения'),
        ),
    ]
