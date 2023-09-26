import xlrd

from django.core.management.base import BaseCommand
from django.conf import settings

from applications.core.models import University, Faculty


def capitalize(name):
    n = name[0].upper()
    name = n + name[1:]
    return name

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        self.create_universities()
        self.create_faculties()

    def create_universities(self):
        wb = self.open_file()
        universities_sheet = wb.sheet_by_index(0)
        universities = list()
        for i in range(1, len(universities_sheet.col_slice(0, 0))):
            name = universities_sheet.cell_value(i, 5)
            if not University.objects.filter(name=name).exists():
                universities.append(University(
                    name=capitalize(name),
                    name_ru=universities_sheet.cell_value(i, 6),
                    name_de=universities_sheet.cell_value(i, 1),
                    address=universities_sheet.cell_value(i, 2),
                    phone=str(universities_sheet.cell_value(i, 3)),
                    site=universities_sheet.cell_value(i, 4),
                ))
                print(f'Added university {capitalize(name)}')

        if len(universities):
            University.objects.bulk_create(universities)
            print('Universities successfully created!')
        else:
            print('Universities already exists')

    def create_faculties(self):
        wb = self.open_file()
        faculties_sheet = wb.sheet_by_index(1)
        faculties = list()
        for i in range(1, len(faculties_sheet.col_slice(0, 0))):
            name = faculties_sheet.cell_value(i, 1)
            if not Faculty.objects.filter(name_ru=name).exists():
                faculties.append(Faculty(
                    name_ru=capitalize(name),
                    name_de=faculties_sheet.cell_value(i, 2),
                ))
                print(f'Added faculty {capitalize(name)}')

        if len(faculties):
            Faculty.objects.bulk_create(faculties)
            print('Faculties successfully created!')
        else:
            print('Faculties already exist')

    def open_file(self):
        loc = settings.BASE_DIR + '/common_docs/documents/universities.xlsx'
        wb = xlrd.open_workbook(filename=loc)
        return wb
