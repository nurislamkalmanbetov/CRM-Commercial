# Generated by Django 3.2 on 2023-09-22 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_vacancy_created_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='vacancy',
            name='exchange',
            field=models.CharField(blank=True, choices=[('RUB', 'RUB'), ('USD', 'USD'), ('EUR', 'EUR')], default='', max_length=10),
        ),
    ]