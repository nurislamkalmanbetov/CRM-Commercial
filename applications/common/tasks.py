from applications.common.models import SiteSettings
from iwex_crm import celery_app


@celery_app.task
def reset_documents_serial_numbers():
    site_settings = SiteSettings.load()
    site_settings.training_serial_number = 1
    site_settings.employment_serial_number = 1
    site_settings.save(update_fields=['training_serial_number', 'employment_serial_number', ])
    return True
