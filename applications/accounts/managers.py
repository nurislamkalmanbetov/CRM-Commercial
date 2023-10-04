import uuid
from django.db import models
from django.db.models import Q
from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ObjectDoesNotExist


class UserManager(BaseUserManager):
    def create_user(self, email=None, phone=None, password=None, is_staff=False, is_superuser=False, **extra_fields):
        if not password:
            raise ValueError('User must have a password.')

        if not email:
            raise ValueError('User must have an email.')

        model_data = {'is_staff': is_staff, 'is_superuser': is_superuser}

        if email:
            model_data['email'] = self.normalize_email(email)

        if phone:
            model_data['phone'] = phone

        user = self.create(**model_data, **extra_fields)
        user.set_password(password)  # Здесь пароль захеширован
        user.save(using=self._db)
        return user

    
    def create_superuser(self, email=None, phone=None, password=None, **extra_fields):
        from applications.accounts.models import Profile

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        user = self.create_user(email, phone, password, **extra_fields)

        Profile.objects.create(user=user)
        return user


class StaffManager(models.Manager):
    def get_queryset(self):
        return super(StaffManager, self).get_queryset().filter(is_staff=True).distinct()


class ProfileNotConfirmedManager(models.Manager):
    def get_queryset(self):
        return super(ProfileNotConfirmedManager, self).get_queryset().filter(
            is_admin_confirmed=False,
            is_refused=False,
            user__is_delete=False,
            creation_date__isnull=False,
        ).distinct().order_by('first_name', 'last_name')


class ProfileInRegistrationManager(models.Manager):
    def get_queryset(self):
        return super(ProfileInRegistrationManager, self).get_queryset().filter(
            is_admin_confirmed=True,
            is_refused=False,
            user__is_delete=False,
            creation_date__isnull=False,
        ).distinct().order_by('first_name', 'last_name')


class ProfileInTerminManager(models.Manager):
    def get_queryset(self):
        return super(ProfileInTerminManager, self).get_queryset().filter(
            is_admin_confirmed=True,
            is_refused=False,
            user__is_delete=False,
            creation_date__isnull=False,
        ).exclude(in_review=True).distinct().order_by('first_name', 'last_name')


class ProfileEssentialInfoManager(models.Manager):
    def get_queryset(self):
        return super(ProfileEssentialInfoManager, self).get_queryset().filter(
            is_admin_confirmed=True,
            is_refused=False,
            user__is_delete=False,
            creation_date__isnull=False,
        ).distinct().order_by('first_name', 'last_name')


class ProfileInInterviewManager(models.Manager):
    def get_queryset(self):
        return super(ProfileInInterviewManager, self).get_queryset().filter(
            is_admin_confirmed=True,
            is_refused=False,
            user__is_delete=False,
            creation_date__isnull=False,
        ).exclude(interviews__student_confirm=True, interviews__vacancy_confirm=True)\
            .distinct().order_by('first_name', 'last_name')


class ProfileInVacancyManager(models.Manager):
    def get_queryset(self):
        return super(ProfileInVacancyManager, self).get_queryset().filter(
            user__is_active=True,
            is_admin_confirmed=True,
            interviews__isnull=False,
            interviews__student_confirm=True,
            interviews__vacancy_confirm=True,
            is_refused=False,
            user__is_delete=False,
            creation_date__isnull=False,
        ).distinct()


class ProfileInEmbassyManager(models.Manager):
    def get_queryset(self):
        return super(ProfileInEmbassyManager, self).get_queryset().filter(
            user__is_active=True,
            is_admin_confirmed=True,
            interviews__isnull=False,
            interviews__student_confirm=True,
            interviews__vacancy_confirm=True,
            is_refused=False,
            user__is_delete=False,
            creation_date__isnull=False,
        ).distinct().order_by('first_name', 'last_name')


class ProfileInSendingManager(models.Manager):
    def get_queryset(self):
        return super(ProfileInSendingManager, self).get_queryset().filter(
            user__is_active=True,
            is_admin_confirmed=True,
            interviews__isnull=False,
            interviews__student_confirm=True,
            interviews__vacancy_confirm=True,
            is_refused=False,
            user__is_delete=False,
            creation_date__isnull=False,
        ).filter(
            Q(start_vise_date__isnull=False) & Q(start_vise_date__isnull=False)
        ).distinct().order_by('first_name', 'last_name')


class ProfileRefusedManager(models.Manager):
    def get_queryset(self):
        return super(ProfileRefusedManager, self).get_queryset().filter(
            is_admin_confirmed=True,
            user__is_delete=False,
            is_refused=True,
            creation_date__isnull=False,
        ).distinct().order_by('first_name', 'last_name')


class ProfileInArchiveManager(models.Manager):
    def get_queryset(self):
        return super(ProfileInArchiveManager, self).get_queryset().filter(user__is_delete=True).distinct()\
            .order_by('first_name', 'last_name')
