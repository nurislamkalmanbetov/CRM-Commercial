# Generated by Django 3.2 on 2023-10-25 07:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0025_alter_invitation_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='employercompany',
            name='background_picture',
            field=models.ImageField(blank=True, upload_to='company_background_pictures/', verbose_name='Фон'),
        ),
        migrations.AddField(
            model_name='employercompany',
            name='description',
            field=models.TextField(blank=True, default='', verbose_name='Описание'),
        ),
        migrations.AddField(
            model_name='employercompany',
            name='icon',
            field=models.ImageField(blank=True, upload_to='company_icons/', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='employercompany',
            name='name',
            field=models.CharField(blank=True, max_length=255, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='employercompany',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Работодатель'),
        ),
    ]