from core_hr import models
from django.contrib import admin


class PassportInline(admin.TabularInline):
    verbose_name_plural = 'Passport'
    can_delete = False
    max_num = 1
    model = models.Passport

class WorkPermitInline(admin.TabularInline):
    verbose_name_plural = 'Work Permit'
    can_delete = False
    model = models.WorkPermit
    max_num = 1

class RegistryOfStayInline(admin.TabularInline):
    verbose_name_plural = 'Registry Of Stay'
    can_delete = False
    model = models.RegistryOfStay
    max_num = 1