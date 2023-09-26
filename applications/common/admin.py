from django.contrib import admin

from applications.common.models import SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fields = (('sum1', 'sum1_text'), ('sum2', 'sum2_text'), ('sum3', 'sum3_text'), )
