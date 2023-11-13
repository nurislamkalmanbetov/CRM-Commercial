# Generated by Django 3.2 on 2023-09-14 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_user_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='birth_country',
            field=models.CharField(blank=True, choices=[('Кыргызстан', 'Кыргызстан'), ('Казахстан', 'Казахстан'), ('Узбекистан', 'Узбекистан'), ('Таджикистан', 'Таджикистан'), ('Россия', 'Россия'), ('Türkei', 'Турция')], default='', max_length=50, verbose_name='Страна рождения'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='birth_region',
            field=models.CharField(blank=True, choices=[('chui', 'Чуйская область'), ('Naryn', 'Нарынская область'), ('Talas', 'Таласская область'), ('Issik-Kul', 'Ыссык-Кульская область'), ('Zhalal-Abad', 'Жалал-Абадская область'), ('Osh', 'Ошская область'), ('Batken', 'Баткенская область')], default='', max_length=50, verbose_name='Область рождения'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='chinese',
            field=models.CharField(blank=True, choices=[('Понимаю и разговариваю без проблем', 'Понимаю и разговариваю без проблем'), ('Если что-то не понимаю, то переспрашиваю', 'Если что-то не понимаю, то переспрашиваю'), ('Понимаю многое, но плохо говорю', 'Понимаю многое, но плохо говорю'), ('Понимаю немного, когда говорят очень медленно, но плохо говорю', 'Понимаю немного, когда говорят очень медленно, но плохо говорю'), ('Не разговариваю совсем', 'Не разговариваю совсем')], default='', max_length=150, verbose_name='Знание китайского языка'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='country1',
            field=models.CharField(blank=True, choices=[('Кыргызстан', 'Кыргызстан'), ('Россия', 'Россия'), ('Турция', 'Турция'), ('Казахстан', 'Казахстан'), ('Германия', 'Германия'), ('Узбекистан', 'Узбекистан'), ('Таджикистан', 'Таджикистан'), ('Дубай', 'Дубай'), ('USA', 'Америка'), ('другое', 'другое')], default='', max_length=50, verbose_name='Страна (1 место работы)'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='country2',
            field=models.CharField(blank=True, choices=[('Кыргызстан', 'Кыргызстан'), ('Россия', 'Россия'), ('Турция', 'Турция'), ('Казахстан', 'Казахстан'), ('Германия', 'Германия'), ('Узбекистан', 'Узбекистан'), ('Таджикистан', 'Таджикистан'), ('Дубай', 'Дубай'), ('USA', 'Америка'), ('другое', 'другое')], default='', max_length=50, verbose_name='Страна (2 место работы)'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='country3',
            field=models.CharField(blank=True, choices=[('Кыргызстан', 'Кыргызстан'), ('Россия', 'Россия'), ('Турция', 'Турция'), ('Казахстан', 'Казахстан'), ('Германия', 'Германия'), ('Узбекистан', 'Узбекистан'), ('Таджикистан', 'Таджикистан'), ('Дубай', 'Дубай'), ('USA', 'Америка'), ('другое', 'другое')], default='', max_length=50, verbose_name='Страна (3 место работы)'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='degree',
            field=models.CharField(blank=True, choices=[('Бакалавр', 'Бакалавр'), ('Магистр', 'Магистр'), ('Колледж', 'Колледж')], default='', max_length=20, verbose_name='Академическая степень'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='driving_experience',
            field=models.CharField(blank=True, choices=[('0', 'до 1 года'), ('1', '1 год'), ('2', '2 года'), ('3', '3 года'), ('4', '4 и более лет')], default='', max_length=1, verbose_name='Стаж вождения'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='english',
            field=models.CharField(blank=True, choices=[('Понимаю и разговариваю без проблем', 'Понимаю и разговариваю без проблем'), ('Если что-то не понимаю, то переспрашиваю', 'Если что-то не понимаю, то переспрашиваю'), ('Понимаю многое, но плохо говорю', 'Понимаю многое, но плохо говорю'), ('Понимаю немного, когда говорят очень медленно, но плохо говорю', 'Понимаю немного, когда говорят очень медленно, но плохо говорю'), ('Не разговариваю совсем', 'Не разговариваю совсем')], default='', max_length=150, verbose_name='Знание английского языка'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', 'Мужской'), ('W', 'Женский')], default='', max_length=1, verbose_name='Пол'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='german',
            field=models.CharField(blank=True, choices=[('Понимаю и разговариваю без проблем', 'Понимаю и разговариваю без проблем'), ('Если что-то не понимаю, то переспрашиваю', 'Если что-то не понимаю, то переспрашиваю'), ('Понимаю многое, но плохо говорю', 'Понимаю многое, но плохо говорю'), ('Понимаю немного, когда говорят очень медленно, но плохо говорю', 'Понимаю немного, когда говорят очень медленно, но плохо говорю'), ('Не разговариваю совсем', 'Не разговариваю совсем')], default='', max_length=150, verbose_name='Знание немецкого языка'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='nationality',
            field=models.CharField(blank=True, choices=[('Кыргызстан', 'Кыргызстан'), ('Казахстан', 'Казахстан'), ('Узбекистан', 'Узбекистан'), ('Таджикистан', 'Таджикистан'), ('Россия', 'Россия'), ('другое', 'другое')], default='', max_length=50, verbose_name='Гражданство'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='russian',
            field=models.CharField(blank=True, choices=[('Понимаю и разговариваю без проблем', 'Понимаю и разговариваю без проблем'), ('Если что-то не понимаю, то переспрашиваю', 'Если что-то не понимаю, то переспрашиваю'), ('Понимаю многое, но плохо говорю', 'Понимаю многое, но плохо говорю'), ('Понимаю немного, когда говорят очень медленно, но плохо говорю', 'Понимаю немного, когда говорят очень медленно, но плохо говорю'), ('Не разговариваю совсем', 'Не разговариваю совсем')], default='', max_length=150, verbose_name='Знание русского языка'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='turkish',
            field=models.CharField(blank=True, choices=[('Понимаю и разговариваю без проблем', 'Понимаю и разговариваю без проблем'), ('Если что-то не понимаю, то переспрашиваю', 'Если что-то не понимаю, то переспрашиваю'), ('Понимаю многое, но плохо говорю', 'Понимаю многое, но плохо говорю'), ('Понимаю немного, когда говорят очень медленно, но плохо говорю', 'Понимаю немного, когда говорят очень медленно, но плохо говорю'), ('Не разговариваю совсем', 'Не разговариваю совсем')], default='', max_length=150, verbose_name='Знание турецкого языка'),
        ),
    ]