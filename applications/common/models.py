from django.db import models


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
