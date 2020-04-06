from cached_property import cached_property
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from centers.models import LearningCenter
from core_hr.models import Passport, RegistryOfStay, WorkPermit, Resume, TeachingCertificate, DegreeDocument, \
    AchievementCertificate
from .managers import CustomUserManager
from apaxhr.storage_backends import PublicMediaStorage, PrivateMediaStorage
from django.core.validators import RegexValidator

name_validator = RegexValidator(r'^[a-z A-Z]*$', 'Only Alphabetic characters allowed')

# Make Proxy models for different admin interfaces

"""Core Info:
Employment Status: Applicant/Initial Training/Active/Pause **New Field Suggestion**
Employment Status Note
Full Name First, Middle, Last
Gender
Employee ID Code
Apax email
Personal Email	
Phone Number
"""


class Employee(AbstractBaseUser, PermissionsMixin):
    lifecycle_statuses = (
        ('ap', 'Applicant'),
        ('trial', 'Initial Training'),
        ('em', 'Employed'),
        ('ps', 'Pause')
    )
    genders = (('M', 'male'), ('F', 'female'))
    # core information

    full_name = models.CharField(_('Name as on Passport'), validators=[name_validator], max_length=45, blank=False,)

    # employment data

    gender = models.CharField(max_length=1, choices=genders)
    employee_id_number = models.CharField(_('employee id number'), max_length=20, null=True)

    # activity Status
    employment_status = models.CharField(choices=lifecycle_statuses, max_length=30)
    employment_status_note = models.TextField(max_length=500)

    # contact information
    phone_number = models.CharField(max_length=25, unique=False)
    email = models.EmailField(_('APAX email address'), unique=True)
    personal_email = models.EmailField(_('Personal Email Address'), unique=False)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)

    # Permissions

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def get_legal_documents(self):
        docs = {}

        try:
            docs['Passport'] = Passport.objects.get(owner__id=self.pk)
        except:
            docs['Passport'] = 'not found'

        try:
            docs['ROS'] = RegistryOfStay.objects.get(owner__id=self.pk)
        except:
            docs['ROS'] = 'not found'
        try:
            docs['Work Permit'] = WorkPermit.objects.get(owner__id=self.pk)
        except:
            docs['Work Permit'] = 'not found'

        return docs
    def get_other_documents(self):
        docs = {}

        try:
            docs['Resume'] = Resume.objects.get(owner__id=self.pk)
        except:
            docs['Resume'] = 'not found'

        try:
            docs['Certificate'] = TeachingCertificate.objects.get(owner__id=self.pk)
        except:
            docs['Certificate'] = 'not found'
        try:
            docs['Degree'] = DegreeDocument.objects.get(owner__id=self.pk)
        except:
            docs['Degree'] = 'not found'


        return docs
    def get_achievement_certificates(self):
        docs = {}
        try:
            docs['Achievment Certificates'] = AchievementCertificate.objects.get(id=self.pk)
        except:
            docs['Achievement Certificates'] = 'not found'
        return docs
    def test_passports(self):
        from core_hr.models import Passport
        owners_passport = Passport.objects.get(owner__pk=self.id)
        if owners_passport.image == None:
            print('image is none')
    def get_contact_info(self):
        try:
            return f"{self.phone_number}, {self.email}, {self.personal_email}"
        except:
            return "Error during retrieval of contact info, perhaps it isn't complete"

    def get_current_center(self):
        # query the employees current center
        center = LearningCenter.objects.get(
            centerteacher__teacher__employee_id=self.pk
        )
        return center

    @property
    def passport_complete(self):
        from core_hr.models import Passport
        try:
            passport = self.passport
            return passport.data_complete
        except ObjectDoesNotExist:
            return ["Couldn't query passport, perhaps it was not created?", False]

    @property
    def ros_form_complete(self):
        from core_hr.models import RegistryOfStay
        try:
            ros_form = RegistryOfStay.objects.get(owner=self)
            return ros_form.data_complete
        except ObjectDoesNotExist:
            return ["Couldn't query Registry of stay, perhaps it was not created", False]
        pass

    @property
    def documents_complete(self):
        completion_statuses = [self.passport_complete, self.ros_form_complete]
        return False if False in completion_statuses else True

    @property
    def first_name(self):
        try:
            return str(self.full_name.split()[1])
        except:
            return self.full_name
    def middle_name(self):
        try:
            return str(self.full_name.split()[2])
        except:
            pass
    def last_name(self):
        try:
            return str(self.full_name.split()[0])
        except:
            pass


    def __str__(self):
        try:
            return f"{self.full_name} {self.email}"
        except Exception as e:
            return 'name-error'


#
# class EmployeePermissions(models.Model):
#     owner = models.OneToOneField(Employee, on_delete=models.CASCADE)
#     # 12 total permissions
#
#     # document access only
#     # James:
#     """
#     Applicants, Trainees, Teachers, Head teachers,
#     Faculty managers, Area managers, HR manager, HR director,
#     Teacher employee_management Director,
#     Training director & Recruiting director.
#     """
#     is_applicant = models.BooleanField(default=True)
#     is_trainee = models.BooleanField(default=False)
#
#     # + schedule access
#     is_teacher = models.BooleanField(default=False)
#     # employee_management
#     is_head_teacher = models.BooleanField(default=False)
#     is_faculty_manager = models.BooleanField(default=False)
#     is_area_manager = models.BooleanField(default=False)
#     is_hr_manager = models.BooleanField(default=False)
#
#
#     # full access
#     is_hr_director = models.BooleanField(default=False)
#     is_teacher_management_director = models.BooleanField(default=False)
#     is_training_director = models.BooleanField(default=False)
#     is_recruiting_director = models.BooleanField(default=False)
#     is_head_office = models.BooleanField(default=False)
#
#     def current_perms(self):
#         fields_names = [f.name for f in self._meta.get_fields()]
#         results = []
#         excluded_fields = ['id','owner']
#         for field_name  in fields_names:
#             if field_name not in excluded_fields:
#                 value = getattr(self, field_name)
#
#                 if value is None or value == '':
#                     continue
#                 results.append(( field_name, value))
#         return results
#
#     def active_perm(self):
#         if [value for label,value in self.current_perms()].count(True) > 1:
#             return False
#         for label, value in self.current_perms():
#             if value == True:
#                 return label
#
#
#     def __str__(self):
#         permissions =[field for field in self._meta.fields if field is True]
#
#         return self.owner.full_name + str(permissions)


class EmployeeProfile(models.Model):
    owner = models.ForeignKey(Employee, on_delete=models.CASCADE)
    img = models.ImageField(_('Upload Profile Image'), upload_to='profile_images')
    bio = models.TextField(_('Personal Biography'), max_length=500, blank=True, null=True)
