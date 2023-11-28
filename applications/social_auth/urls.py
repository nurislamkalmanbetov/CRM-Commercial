from django.urls import path

from .views import GoogleSocialAuthView, FacebookSocialAuthView, TwitterSocialAuthView, LoginGooglePage

urlpatterns = [
    path('login/', LoginGooglePage.as_view()),
    path('google/', GoogleSocialAuthView.as_view()),
    path('facebook/', FacebookSocialAuthView.as_view()),
    path('twitter/', TwitterSocialAuthView.as_view()),


]