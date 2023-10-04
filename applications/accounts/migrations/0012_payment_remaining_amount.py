# Generated by Django 3.2 on 2023-09-25 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='remaining_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Остаток'),
        ),
    ]
