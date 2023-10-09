# Generated by Django 3.2 on 2023-09-25 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_auto_20230925_0844'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='amount_paid',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='tariff',
        ),
        migrations.AddField(
            model_name='payment',
            name='amount_choice',
            field=models.DecimalField(choices=[(10000, 'Десять тысяч'), (20000, 'Двадцать тысяч'), (35000, 'Тридцать пять тысяч')], decimal_places=2, default=0, max_digits=10, verbose_name='Оплачено'),
        ),
    ]