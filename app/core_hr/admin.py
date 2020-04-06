import csv


from botocore.exceptions import EndpointConnectionError
from django.contrib import admin
import datetime
from django.apps import apps
from django.contrib.admin import SimpleListFilter
from django.db.models import Subquery, Q
from django.http import HttpResponse
from django.utils.safestring import mark_safe

import datedelta
from . import models
from .admin_data import inlines
from core_hr.models import Employee, Passport, RegistryOfStay, WorkPermit, DegreeDocument, AchievementCertificate, \
    TeachingCertificate, Resume


class WorkPermitStatusFilter(SimpleListFilter):
    title='Work Permit Status'
    parameter_name = 'documents'



    def lookups(self, request, model_admin):
        return[
            ('not_complete', 'Work Permit Input not complete'),
            ('expiring_soon', 'Work Permit/Visa exp. w/in 1 month'),
            ('expired', 'Work Permit/Visa expired')
        ]

    def queryset(self, request, queryset):

        if self.value() == 'not_complete':
            return queryset.exclude(pk__in=Subquery(WorkPermit.objects.all().values('owner__pk')))
        elif self.value() == 'expiring_soon':
            now = datetime.datetime.now().date()
            expiring_in_one_month = now + datedelta.datedelta(days=14)
            return queryset.filter(expiration_date__range=[now, expiring_in_one_month])
        # elif self.value() =='expiring_soon':

class ExpiredDocumentStatusFilter(SimpleListFilter):
    title='Document Expiration Status'
    parameter_name = 'exp-info'
    def lookups(self, request, model_admin):
        return[
            ('missing_picture', 'Picture file missing'),
            ('expired', 'Document Expired'),
            ('expiring_very_soon', 'Within 2 weeks'),
            ('expiring_soon', 'Within 1 month'),
            ('expiring_in_six_months', 'Within 6 months'),
        ]


    def queryset(self, request, queryset):
        now = datetime.datetime.now().date()

        if self.value() == 'expiring_in_six_months':
            expiring_in_six_months = now +datedelta.datedelta(days=180)
            return queryset.filter(expiration_date__range=[now, expiring_in_six_months])
        elif self.value() == 'expiring_soon':
            expiring_in_one_month = now + datedelta.datedelta(days=30)
            return queryset.filter(expiration_date__range=[now, expiring_in_one_month])
        elif self.value() == 'expiring_very_soon':
            expiring_in_two_weeks = now + datedelta.datedelta(days=14)
            return queryset.filter(expiration_date__range=[now, expiring_in_two_weeks])
        elif self.value() == 'expired':
            return queryset.filter(expiration_date__lte=datetime.datetime.now().date())
        elif self.value() == 'missing_picture':
            return queryset.filter(Q(image='') | Q(image=None))
        else:
            return queryset.all()


class LegalDocumentAdminMixin(object):
    class Meta:
        abstract = True

    ordering = ('expiration_date',)
    list_filter = (ExpiredDocumentStatusFilter,)
    list_display = ('owner', 'expiration_date', 'valid', )
    search_fields = ('owner__full_name', 'owner__employee_id_number')
    readonly_fields = ('owner', 'document_image',)
    actions=["export_as_csv", "email_selected"]


    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        field_names = ['owner',]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=Expired{}.csv'.format( meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            email = [getattr(obj, field).email for field in field_names if field=='owner']
            row = writer.writerow(
                [getattr(obj, field).email if field=='owner' else getattr(obj, field) for field in field_names] )

        return response

    export_as_csv.short_description = "Export Selected"


    def email_selected(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        for obj in queryset:
            email_addresses = [getattr(obj, field).email for field in field_names if field == 'owner']
            message =' Whatever you want to say here up to and including' \
                     ' a fully formatted html page' \
                     ' Hi user, your document is expired...' \
                     ' please update it or risk being deported and fined'
            for email_address in email_addresses:
                print(f"{email_address} Sent message:{message}")
        pass


    def valid(self, obj):
        return obj.expiration_date > datetime.datetime.now().date()


    def document_image(self, obj):
        try:
            return mark_safe(
                '<img src="{url}" width="{width}" height={height} />'.format(
                    url=obj.image.url,
                    width=obj.image.width / 4,
                    height=obj.image.height / 4,
                )
            )
        except EndpointConnectionError as e:
            return mark_safe(f"'<h4>{e}</h4>")

@admin.register(WorkPermit)
class WorkPermitAdmin(LegalDocumentAdminMixin, admin.ModelAdmin):
    verbose_name_plural = 'Work Permits'
    model = WorkPermit
    #
    # def get_queryset(self, request):

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(RegistryOfStay)
class RegistryOfStayAdmin(LegalDocumentAdminMixin, admin.ModelAdmin):
    model = RegistryOfStay

@admin.register(Passport)
class PassportAdmin(LegalDocumentAdminMixin, admin.ModelAdmin):
    model = Passport
    autocomplete_fields = ('owner',)
    def has_delete_permission(self, request, obj=None):
        return False

class BaseDocumentAdminMixin(object):

    def has_delete_permission(self, request, obj=None):
        return False

    class Meta:
        abstract = True
    list_display = ('owner','date_added')
    search_fields = ('owner__full_name', 'owner__employee_id_number')
    autocomplete_fields = ('owner',)


@admin.register(Resume)
class ResumeAdmin(BaseDocumentAdminMixin, admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False
    model = Resume
    verbose_name_plural =  u"\u200B" + 'Resumes'


@admin.register(AchievementCertificate)
class AchievementCertificateAdmin(BaseDocumentAdminMixin, admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False
    model= AchievementCertificate
    verbose_name=  u"\u200B" + 'FAS/KPI Achievement Certs'


@admin.register(TeachingCertificate)
class TeachingCertificateAdmin(BaseDocumentAdminMixin, admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False
    model = TeachingCertificate
    verbose_name_plural =  u"\u200B" + 'TEFL/CELTA/TESOL etc. Certs.'



@admin.register(DegreeDocument)
class DegreeDocumentAdmin(BaseDocumentAdminMixin, admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False
    model = DegreeDocument

#
# class EmployeeAdmin(ModelAdmin):
#     model = models.Employee
#     fields = ['middle_name','bio','employee_role']
#     search_fields = ['user__first_name','user__last_name','middle_name']
#     inlines= [
#         inlines.PassportInline,
#         #inlines.WorkPermitInline,
#         #inlines.RegistryOfStayInline
#     ]

# admin.site.register(models.Employee, EmployeeAdmin)


#
# hr_models.Passport
#
# hr_models.DocumentationInfo
#
# hr_models.DocumentImage
#
# hr_models.PublicImage
#
# hr_models.RegistryOfStayForm
#
# hr_models.RegistryOfStayForm
#
# hr_models.WorkPermit
