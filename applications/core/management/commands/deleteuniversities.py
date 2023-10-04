from django.core.management.base import BaseCommand

from applications.core.models import University, Faculty

class Command(BaseCommand):
    def handle(self, *args, **options):
        universities = University.objects.all()
        faculties = Faculty.objects.all()

        for u in universities:
            u.delete()

        for f in faculties:
            f.delete()