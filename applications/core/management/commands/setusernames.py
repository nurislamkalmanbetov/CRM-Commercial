import random

from django.core.management.base import BaseCommand

from applications.accounts.models import Profile


class Command(BaseCommand):

    def handle(self, *args, **options):
        first_names = ['John', 'Jack', 'Sam', 'Ben', 'Alan', ]
        last_names = ['Smith', 'Black', 'Grey', 'Sanders', 'Reed', ]

        profiles = Profile.objects.all()

        for profile in profiles:
            random_int = random.randint(0, len(first_names)-1)
            profile.first_name = first_names[random_int]
            random_int = random.randint(0, len(last_names) - 1)
            profile.last_name = last_names[random_int]
            profile.save(update_fields=['first_name', 'last_name', ])
