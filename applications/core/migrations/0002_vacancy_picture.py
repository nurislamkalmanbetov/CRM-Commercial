# Generated by Django 3.2 on 2023-08-30 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vacancy',
            name='picture',
            field=models.ImageField(blank=True, upload_to='vacancy_pics/'),
        ),
    ]
