from django.urls import path
from .views import FooterLinkView , LogoView



urlpatterns = [
    path('footer-links/', FooterLinkView.as_view(), name='footer-links'),
    path('logo/', LogoView.as_view(), name='logo'),
]