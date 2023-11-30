from django import forms
from django.contrib import admin
from applications.common.models import SiteSettings, FooterLink , Logo



@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fields = (('sum1', 'sum1_text'), ('sum2', 'sum2_text'), ('sum3', 'sum3_text'), )




class FooterLinkAdminForm(forms.ModelForm):
    class Meta:
        model = FooterLink
        fields = '__all__'

    def init(self, *args, **kwargs):
        super(FooterLinkAdminForm, self).init(*args, **kwargs)
        self.fields['whatsapp_link'].initial = 'wa.me/+'

class FooterLinkAdmin(admin.ModelAdmin):
    form = FooterLinkAdminForm
    list_display = ('instagram_link', 'facebook_link', 'whatsapp_link', 'phone_number', 'address', 'email', 'created_at', 'updated_at', 'created_by',)
    fieldsets = (
        ('Ссылки', {
            'fields': ('instagram_link', 'facebook_link', 'whatsapp_link'),
        }),
        ('Контактная информация', {
            'fields': ('phone_number', 'address', 'email'),
        }),
        ('Текст для футера', {
            'fields': ('text',),
        }),
    )

    def get_list_display(self, request):
        if request.user.is_superuser:
            return ('id',) + self.list_display
        return self.list_display

    def get_fieldsets(self, request, obj=None):
        if not request.user.is_superuser:
            return (
                ('Ссылки', {
                    'fields': ('instagram_link', 'facebook_link', 'whatsapp_link'),
                }),
                ('Контактная информация', {
                    'fields': ('phone_number', 'address', 'email'),
                }),
            )
        return super().get_fieldsets(request, obj)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user

        obj.whatsapp_link = obj.whatsapp_link.replace('wa.me/+', '') if obj.whatsapp_link.startswith('wa.me/+') else obj.whatsapp_link

        super().save_model(request, obj, form, change)



class LogoAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'description', 'created_by', 'created_at', 'updated_at', 'external_url')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('description', 'created_by__email')
    readonly_fields = ('created_at', 'updated_at')

    def image_thumbnail(self, obj):
        return obj.image.url if obj.image else None
    image_thumbnail.short_description = 'Thumbnail'
    image_thumbnail.allow_tags = True

    fieldsets = (
        ('Logo Details', {
            'fields': ('image', 'description', 'external_url', 'created_by', 'created_at', 'updated_at'),
        }),
    )

    

admin.site.register(Logo, LogoAdmin)
admin.site.register(FooterLink, FooterLinkAdmin)