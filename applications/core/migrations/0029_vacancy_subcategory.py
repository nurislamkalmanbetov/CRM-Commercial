# Generated by Django 3.2 on 2023-11-10 08:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_auto_20231110_0719'),
    ]

    operations = [
        migrations.AddField(
            model_name='vacancy',
            name='subcategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.subcategory', verbose_name='Подкатегория'),
        ),
    ]
