# Generated by Django 3.2 on 2023-11-10 07:19

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_auto_20231109_0844'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Категория', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='subcategory',
            options={'verbose_name': 'Подкатегория', 'verbose_name_plural': 'Подкатегории'},
        ),
        migrations.RemoveField(
            model_name='vacancy',
            name='subcategory',
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(db_index=True, max_length=255, verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcategories', to='core.category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='name',
            field=models.CharField(db_index=True, max_length=255, verbose_name='Подкатегория'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата публикации'),
        ),
    ]