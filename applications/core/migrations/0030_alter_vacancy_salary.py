# Generated by Django 3.2 on 2023-11-21 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_vacancy_subcategory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacancy',
            name='salary',
            field=models.IntegerField(verbose_name='Зарплата'),
        ),
    ]