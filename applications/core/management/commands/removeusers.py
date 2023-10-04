from django.core.management.base import BaseCommand

from applications.accounts.models import User, Profile

class Command(BaseCommand):

    def handle(self, *args, **options):
        users = User.objects.all()

        for u in users:
            if not u.is_staff:
                mail = u.email
                u.delete()
                print(f'User {mail} successfully deleted.')
