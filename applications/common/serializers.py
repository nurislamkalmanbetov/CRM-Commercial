from rest_framework import serializers
from .models import FooterLink ,Logo



class FooterLinkSerializers(serializers.ModelSerializer):
    created_by = serializers.EmailField(source='created_by.email')

    class Meta:
        model = FooterLink
        fields = ('id', 'instagram_link', 'facebook_link', 'whatsapp_link', 'phone_number', 'address', 'email', 'created_at', 'updated_at', 'created_by', 'text', )
    

class LogoSerializer(serializers.ModelSerializer):
    created_by = serializers.EmailField(source='created_by.email')

    class Meta:
        model = Logo
        fields = ('id', 'image', 'description', 'created_by', 'created_at', 'updated_at', 'external_url')
