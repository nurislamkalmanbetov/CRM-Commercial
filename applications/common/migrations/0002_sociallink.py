# Generated by Django 3.2 on 2023-11-29 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Instagram', 'Instagram'), ('Facebook', 'Facebook'), ('WhatsApp', 'WhatsApp')], max_length=50)),
                ('link', models.CharField(max_length=100)),
            ],
        ),
    ]