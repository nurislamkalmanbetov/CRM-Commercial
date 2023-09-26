import random

from django.core.management.base import BaseCommand

from applications.core.models import EmployerCompany, Vacancy


class Command(BaseCommand):

    def handle(self, *args, **options):
        company_names = ['McDonalds', 'Starbucks', 'Facebook', 'Netflix', 'WarnerBros', 'Valve', ]
        cities = ['San Francisco', 'New York', 'Mexico', 'Palo Alto', 'Paris', 'Bishkek', 'Moscow', ]
        vacancies = ['Developer', 'Cook', 'Public Speaker', 'CEO', 'Doctor', 'Nurse', ]
        salaries = ['1000', '2000', '3000', '5000', '100000', ]

        for i in range(int(options['count'])):
            random_company_int = random.randint(0, len(company_names)-1)
            random_city_int = random.randint(0, len(cities)-1)
            company = EmployerCompany.objects.create(
                name=company_names[random_company_int],
                address=cities[random_city_int]
            )
            random_vacancy_int = random.randint(0, len(vacancies)-1)
            random_salary_int = random.randint(0, len(salaries)-1)
            Vacancy.objects.create(
                employer_company=company,
                name=vacancies[random_vacancy_int],
                salary=salaries[random_salary_int]
            )
            print(f'Company {company.name} has been created')

    def add_arguments(self, parser):
        parser.add_argument(
            '-C',
            '--count',
            action='store',
            default=10,
            help='Количество компаний',
        )
