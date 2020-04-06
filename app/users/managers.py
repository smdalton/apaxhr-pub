from datetime import datetime, timedelta

from datedelta import datedelta
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.db.models import Q, Subquery
from django.utils.translation import ugettext_lazy as _

from core_hr.models import \
    Passport, RegistryOfStay, WorkPermit, AchievementCertificate, DegreeDocument\


"""
https://testdriven.io/blog/django-custom-user-model/
"""


class CustomUserManager(BaseUserManager):
    """
    Custom User model with email as unique identifier
    for authentication
    instead of default username
    """
    use_for_related_fields = True

    def create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


    def has_documents_expiring_soon(self, days=60):
        now = datetime.now().date()
        expiration = now + timedelta(days=days)
        passports = Q(passport__expiration_date__range=[now, expiration])
        ros_forms = Q(registryofstay__expiration_date__range=[now, expiration])
        work_permits = Q(workpermit__expiration_date__range=[now, expiration])
        return self.filter(passports|ros_forms|work_permits).filter(is_active=True)


    def has_documents_expiring_very_soon(self):
        now = datetime.now().date()
        future = datetime.now().date() + datedelta(days=14)
        passports = Q(passport__expiration_date__range=[now, future])
        ros_forms = Q(registryofstay__expiration_date__range=[now, future])
        work_permits = Q(workpermit__expiration_date__range=[now, future])
        return self.filter(passports|ros_forms|work_permits).filter(is_active=True)

    def has_expired_documents(self):
        now = datetime.now().date()
        passports = Q(passport__expiration_date__lt=now)
        ros_forms = Q(registryofstay__expiration_date__lt=now)
        work_permits = Q(workpermit__expiration_date__lt=now)
        return self.filter(passports|ros_forms|work_permits).filter(is_active=True)

    def has_expired_documents_inactive(self):
        now = datetime.now().date()
        passports = Q(passport__expiration_date__lt=now)
        ros_forms = Q(registryofstay__expiration_date__lt=now)
        work_permits = Q(workpermit__expiration_date__lt=now)
        return self.filter(passports | ros_forms | work_permits).filter(is_active=False)

    def passports_are_created(self, **kwargs):
        return self.filter(pk__in=Subquery(Passport.objects.values('owner__pk')))
    #
    # def passports_are_complete(self):
    #     pass
    #
    # def passports_expiring_very_soon(self):
    #
    #     return self.filter()
    #     pass
    #
    # def passports_expiring_soon(self):
    #     return self.filter()
    #
    # def expired_passports(self):
    #     return self.filter()

    def ros_created(self, **kwargs):
        return self.filter(pk__in=Subquery(RegistryOfStay.objects.values('owner__pk')))

    # def ros_complete(self):
    #     return self.filter()
    #
    # def ros_forms_expiring(self):
    #     return self.filter()
    #
    # def ros_forms_expiring_soon(self):
    #     return self.filter()
    #
    # def passport_valid(self):
    #     return self.filter()

    def work_permit_created(self, **kwargs):
        return self.filter(pk__in=Subquery(WorkPermit.objects.filter(type='wp').values('owner__pk')))

    def passport_valid(self):
        return self.filter()



    def has_valid_documents(self):
        result = self.has_passport().intersection(
            self.has_valid_ros(),
            self.has_valid_work_permits()
        )
        return result




    def has_resume(self, **kwargs):
        try:
            print(arg for arg in kwargs.keys())
        except:
            print('nothing in employee has passport manager args')

        return self.all()


    def has_teaching_certificate(self, **kwargs):
        try:
            print(arg for arg in kwargs.keys())
        except:
            print('nothing in employee has passport manager args')

        return self.all()


    def has_degree(self, **kwargs):
        try:
            print(arg for arg in kwargs.keys())
        except:
            print('nothing in employee has passport manager args')

        return self.all()



