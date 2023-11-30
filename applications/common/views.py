from rest_framework import generics
from .models import FooterLink , Logo
from .serializers import FooterLinkSerializers , LogoSerializer



class FooterLinkView(generics.ListAPIView):
    queryset = FooterLink.objects.select_related().all()
    serializer_class = FooterLinkSerializers

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class LogoView(generics.ListAPIView):
    queryset = Logo.objects.select_related().all()
    serializer_class = LogoSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)