# Generated by Django 3.2 on 2023-11-29 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_sociallink'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sociallink',
            name='link',
        ),
        migrations.RemoveField(
            model_name='sociallink',
            name='name',
        ),
        migrations.AddField(
            model_name='sociallink',
            name='address',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='sociallink',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='sociallink',
            name='facebook_link',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='sociallink',
            name='instagram_link',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='sociallink',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='sociallink',
            name='whatsapp_link',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
