from django.apps import AppConfig
# from jazzmin.settings import JAZZMIN_SETTINGS
from iwex_crm.settings import JAZZMIN_SETTINGS


class JazzminConfig(AppConfig):
    name = 'jazzmin'
    verbose_name = "Jazzmin Config"

    def ready(self):
        # Update Jazzmin settings
        JAZZMIN_SETTINGS.update({
            "site_title": "IWEX CRM",
            "menu_show_home": False,
            "form_inlines_hide_original": True,
            "navigation_expanded": False,
            "menu": [
                {
                    "type": "parent",
                    "title": "CRM",
                    "children": [
                        {"title": "Общий список", "url": "admin:accounts_profilenotconfirmed_changelist"},
                        {"title": "Регистрация", "url": "admin:accounts_profileinregistration_changelist"},
                        {"title": "Термин", "url": "admin:accounts_profileintermin_changelist"},
                        {"title": "Собеседование", "url": "admin:accounts_profileininterview_changelist"},
                        {"title": "Вакансия", "url": "admin:accounts_profileinvacancy_changelist"},
                        {"title": "Посольство", "url": "admin:accounts_profileinembassy_changelist"},
                        {"title": "Отправка", "url": "admin:accounts_profileinsending_changelist"},
                        {"title": "Контактные данные", "url": "admin:accounts_profileincontactdetails_changelist"},
                        {"title": "Оплата", "url": "admin:accounts_profileinpayment_changelist"},
                        {"title": "Отказавшиеся", "url": "admin:accounts_profileinrefused_changelist"},
                        {"title": "Архив", "url": "admin:accounts_profileinarchive_changelist"},
                    ],
                },
                {
                    "type": "parent",
                    "title": "Настройки",
                    "children": [
                        {"title": "Пользователи", "url": "admin:accounts_user_changelist"},
                        {"title": "Сотрудники", "url": "admin:accounts_staff_changelist"},
                        {"title": "Администраторы для договоров", "url": "admin:core_contractadmin_changelist"},
                        {"title": "Профили", "url": "admin:accounts_profile_changelist"},
                        {"title": "Группы", "url": "admin:auth_group_changelist", "perm": "is_superuser"},
                        {"title": "Работодатели", "url": "admin:core_employercompany_changelist", "perm": "is_superuser"},
                        {"title": "Университеты", "url": "admin:core_university_changelist", "perm": "is_superuser"},
                        {"title": "Факультеты", "url": "admin:core_faculty_changelist", "perm": "is_superuser"},
                        {"title": "Оплата", "url": "admin:accounts_bill_changelist"},
                        {"title": "Справочная информация", "url": "admin:accounts_profileinessentialinfo_changelist"},
                        {"title": "Настройки проекта", "url": "admin:common_sitesettings_changelist"},
                    ],
                },
            ],
        })
