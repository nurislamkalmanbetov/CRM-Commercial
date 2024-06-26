# Generated by Django 3.2 on 2023-09-25 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_auto_20230925_0852'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='amount_choice',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='is_paid',
        ),
        migrations.AddField(
            model_name='payment',
            name='amount_paid',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Оплачено'),
        ),
        migrations.AddField(
            model_name='payment',
            name='is_fully_paid',
            field=models.BooleanField(default=False, verbose_name='Оплачено полностью'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='remaining_amount',
            field=models.DecimalField(decimal_places=2, default=35000, editable=False, max_digits=10, verbose_name='Остаток'),
        ),
    ]
