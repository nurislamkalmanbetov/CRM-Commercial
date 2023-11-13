# Generated by Django 3.2 on 2023-09-05 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20230905_0343'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='employercompany',
            options={'verbose_name': 'Работадатель', 'verbose_name_plural': 'Работодатели'},
        ),
        migrations.RemoveField(
            model_name='employercompany',
            name='address',
        ),
        migrations.AddField(
            model_name='employercompany',
            name='country',
            field=models.CharField(blank=True, default='', max_length=128, verbose_name='Страна'),
        ),
    ]