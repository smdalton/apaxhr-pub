from datetime import datetime
import datetime as dt

from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import resolve, reverse
from django_countries.fields import CountryField
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import timezone, timedelta
from django.conf import settings
from apaxhr.storage_backends import PublicMediaStorage
Employee = settings.AUTH_USER_MODEL
from apaxhr.storage_backends import PrivateMediaStorage

# debug settings
if not settings.USE_S3:
    from django.core.files.storage import FileSystemStorage
    PrivateMediaStorage = FileSystemStorage

#Default work permit expiration time is 2 years or 730 days, I have set
def default_work_permit_expiration(expiration_period=680):
    return dt.datetime.now().date()+timedelta(days=expiration_period)

def default_ros_expiration(expiration_period=170):
    now = dt.datetime.now()
    return now + timedelta(days=expiration_period)

class TrackingUtilitiesMixin(models.Model):
    class Meta:
        abstract = True

    verified = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    #email_active = models.BooleanField(default=True)
    @property
    def data_complete(self):
        ''' Checks if all the fields have been filled '''
        fields_names = [f.name for f in self._meta.get_fields()]
        for field_name in fields_names:
            value = getattr(self, field_name)
            if value is None or value == '':
                print(self._meta.verbose_name, field_name)
                return False
        return True

class LegalDocument(models.Model):
    class Meta:
        abstract = True
    owner = models.OneToOneField(Employee, on_delete=models.CASCADE)
    issue_date = models.DateField(_('Document Date of Issue'),blank=False)
    expiration_date = models.DateField(_('Document Expiration Date'),blank=False)
    image_dir = 'default_images'
    image = models.ImageField(storage=PrivateMediaStorage(), upload_to=image_dir, blank=False)

    @property
    def expired(self):
        return dt.datetime.now().date() > self.expiration_date

    @property
    def get_photo_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return "No image"

class Passport(TrackingUtilitiesMixin, LegalDocument):
    "https://pypi.org/project/django-countries/"
    #place_of_issue = CountryField(blank=False,null=True)

    class Meta:
        verbose_name = 'Passport'
    dob = models.DateField(blank=False, null=False)
    place_of_issue = CountryField(blank_label="select country used in your passport",default='AQ')
    image = models.ImageField(storage=PrivateMediaStorage(), upload_to='passports',blank=False)
    passport_number = models.IntegerField(blank=False)

    def get_view_url(self):
        return reverse('core_hr:passport_view')
    def get_update_url(self):
        return reverse('core_hr:passport_update')

    def __str__(self):
        expiration_data = 'Expired' if self.expired else 'Valid'
        formatted_date = self.expiration_date.strftime("%d-%m-%Y")
        return f"{expiration_data}, exp. date: {formatted_date}"

    @property
    def owners_name(self):
        return self.owner.full_name
    @property
    def employee_number(self):
        return self.owner.employee_id_number


# actual default is 180 days, 170 is for a 10 day warning reminder

class RegistryOfStay(TrackingUtilitiesMixin,  LegalDocument):
    class Meta:
        verbose_name = 'Registry of Stay Form'
    employee_address = models.CharField(max_length=100,blank=False)
    landlords_name = models.CharField(max_length=100,blank=False)
    landlords_cell_phone = models.CharField(max_length=25, blank=False)
    landlords_email = models.EmailField(max_length=40, blank=False)
    image = models.ImageField(
            storage=PrivateMediaStorage(),
            upload_to='ros_images',
            blank=False
    )

    def get_update_url(self):
        return reverse('core_hr:ros_update')
    def get_view_url(self):
        return reverse('core_hr:ros_view')

    @property
    def phone_number(self):
        return self.owner.phone_number


    def __str__(self):
        expiration_data = 'Expired' if self.expired else 'Valid'
        formatted_date = self.expiration_date.strftime("%d-%m-%Y")
        return f"{expiration_data}, exp. date: {formatted_date}"


class WorkPermit(TrackingUtilitiesMixin, LegalDocument):
    class Meta:
        verbose_name ='Work Permit and Visa'
    document_choices = (('wp','Work Permit'),('vs','visa'))
    type = models.CharField(choices=document_choices, blank=False, max_length=2)
    image = models.ImageField(
        storage=PrivateMediaStorage(),
        upload_to='work_permit_images',
        blank=False
    )

    def owners_name(self):
        return self.owner.full_name
    def owners_id(self):
        return self.owner.employee_id_number

    def get_view_url(self):
        return reverse('core_hr:work_permit_view')
    def get_update_url(self):
        return reverse('core_hr:work_permit_update')


    def __str__(self):
        expiration_data = 'Expired' if self.expired else 'Valid'
        formatted_date = self.expiration_date.strftime("%d-%m-%Y")
        return f"{expiration_data}, exp. date: {formatted_date}"


class BaseDocument(TrackingUtilitiesMixin, models.Model):
    class Meta:
        abstract = True
    owner = models.OneToOneField(Employee, on_delete=models.CASCADE)
    image = models.FileField(
        storage=PrivateMediaStorage(),
        upload_to='base_documents', blank=False, null=False)

    @property
    def get_file_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            return "No image"


class Resume(BaseDocument):
    class Meta:

        verbose_name = u"\u200B" + 'Resume and CV\''
    help = "Stores a resume or CV document"
    document_choices = (('rs','Resume'),('cv','Curriculum Vitae'))
    type =  models.CharField(max_length=20,choices=document_choices)
    image = models.FileField(
        storage=PrivateMediaStorage(),
        upload_to='resumes_cvs', blank=False, null=False
    )

    def get_update_url(self):
        return reverse('core_hr:resume_update')
    def get_view_url(self):
        return reverse('core_hr:resume_view')


class TeachingCertificate(BaseDocument):
    class Meta:
        verbose_name = u"\u200B" + 'TESL/TESOL/CELTA/TEFL etc. certifcates'
    help = "Stores a teaching certificate"
    certificate_choices = (('c', 'CELTA'), ('ts', 'TESOL'), ('tf', 'TEFL'), ('ot', 'other'))
    id_number = models.CharField(max_length=100)
    # issue_date = models.DateField(default=datetime.now())
    type  = models.CharField(max_length=15, choices=certificate_choices, blank=False, null=False)
    image = models.FileField(
        storage=PrivateMediaStorage(),
        upload_to='tefl_certs',
        blank=False,
        null=False
    )

    def get_update_url(self):
        return reverse('core_hr:teach_certificate_update')
    def get_view_url(self):
        return reverse('core_hr:teach_certificate_view')

class DegreeDocument(BaseDocument):
    class Meta:
        verbose_name = u"\u200B" + 'Degree Document'
    help = "Stores a College diploma document"
    image = models.FileField(
        storage=PrivateMediaStorage(),
        upload_to='degree_certs',
        blank=False,
        null=False
    )

    def get_update_url(self):
        return reverse('core_hr:degree_update')
    def get_view_url(self):
        return reverse('core_hr:degree_view')



class AchievementCertificate(BaseDocument):
    class Meta:
        verbose_name =u"\u200B" + 'FAS/KPI Certificate'
    help = "Store information for KPI and FAS certificates of achievement"
    email_sent = models.BooleanField(default=False)
    owner = models.ForeignKey(Employee, on_delete=models.CASCADE)
    image = models.ImageField(
        storage=PrivateMediaStorage(),
        upload_to='kpi_certificates',
        blank=False,
        null=False
    )
    message_text = models.TextField(_('Enter award message for email here'), max_length=1000, blank=False)

    def get_view_url(self):
        return reverse('core_hr:ach_cert_view')


