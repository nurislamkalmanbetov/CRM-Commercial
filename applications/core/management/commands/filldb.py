import random

from django.core.management.base import BaseCommand

from applications.accounts.models import User, Profile, Interview
from applications.core.models import Vacancy
from applications.core.utils import (
    generate_random_email,
    generate_random_phone,
    generate_random_string,
)


class Command(BaseCommand):

    def handle(self, *args, **options):
        for i in range(int(options['count'])):
            u = self.create_user()
            if u:
                u.save()
                print(f'User {u} successfully created.')
            profile = Profile.objects.create(user=u)
            entries_list = []
            vacancies = Vacancy.objects.all()
            if len(vacancies) != 0:
                for i in range(8):
                    random_vacancy_int = random.randint(0, len(vacancies)-1)
                    vacancy = vacancies[random_vacancy_int]
                    entries_list.append(
                        Interview(profile=profile, company=vacancy.employer_company, vacancy=vacancy)
                    )
                Interview.objects.bulk_create(entries_list)

    def create_user(self):
        email = generate_random_email()
        phone = generate_random_phone()

        if User.objects.filter(email=email).exists():
            self.create_user()
            return None

        u = User(
            email=email,
            phone=phone,
            whatsapp_phone=phone,
            password=generate_random_string(10),
        )
        return u

    def add_arguments(self, parser):
        parser.add_argument(
            '-C',
            '--count',
            action='store',
            default=10,
            help='Количество пользователей',
        )
