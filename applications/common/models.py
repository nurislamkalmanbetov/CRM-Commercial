from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField

class SingletonModel(models.Model):

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class SiteSettings(SingletonModel):
    employment_serial_number = models.PositiveIntegerField(default=1)
    training_serial_number = models.PositiveIntegerField(default=1)

    def get_serial_number(self, doc_type):
        if doc_type in ['employment', 'training']:
            serial_number = str(getattr(self, f'{doc_type}_serial_number'))
            return serial_number if len(serial_number) > 1 else f'0{serial_number}'
        return None

    def __str__(self):
        return 'Настройки CRM'

    class Meta:
        verbose_name = 'Настройки CRM'
        verbose_name_plural = 'Настройки CRM'


class FooterLink(models.Model):
    instagram_link = models.CharField(max_length=100, blank=True, null=True, verbose_name="Ссылка на Instagram")
    facebook_link = models.CharField(max_length=100, blank=True, null=True, verbose_name="Ссылка на Facebook")
    whatsapp_link = models.CharField(max_length=100, blank=True, null=True, verbose_name="Ссылка на WhatsApp")
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="Номер телефона")
    address = models.CharField(max_length=200, blank=True, null=True, verbose_name="Адрес")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    created_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='created_footer_links', verbose_name="Создано пользователем")
    text = RichTextField(verbose_name="Текст для футера")

    def str(self):
        return f"Контактная информация для {self.email if self.email else 'Пользователя'}"

    def save(self, *args, **kwargs):
        if self.whatsapp_link and not self.whatsapp_link.startswith('wa.me/') and not self.whatsapp_link.startswith('+'):
            self.whatsapp_link = f'wa.me/{self.whatsapp_link}'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Информация внизу сайта'
        verbose_name_plural = 'Информации внизу сайта'


class Logo(models.Model):
    image = models.ImageField(upload_to='logos/', verbose_name='Изображение логотипа')
    description = models.TextField(blank=True, verbose_name='Описание логотипа')
    created_by = models.ForeignKey('accounts.User', on_delete=models.CASCADE, verbose_name='Создано пользователем')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата последнего обновления')
    external_url = models.URLField(blank=True, verbose_name='Внешний URL логотипа')

    def __str__(self):
        return f"Логотип {self.id}"
    
    class Meta:
        verbose_name = 'Лого сайта'
        verbose_name_plural = 'Лого сайтов'