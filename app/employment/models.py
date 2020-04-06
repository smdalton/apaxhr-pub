from datetime import datetime, timedelta

from django.db import models
from django.conf import settings
Employee = settings.AUTH_USER_MODEL
# Create your models here.
# from payroll.models import PositionSalaryInfo



class Department(models.Model):
    name = models.CharField(max_length=20, default='Teaching')
    other_title_note = models.CharField(max_length=20, default='other title note')

    def __str__(self):
        return self.name


class EmploymentContract(models.Model):
    # some rules here
    hours = models.SmallIntegerField(default=18)

class BasePositionMixin(models.Model):
    class Meta:
        abstract = True
    department = models.ForeignKey(Department, max_length=25, on_delete=models.PROTECT)
    position_start = models.DateTimeField(auto_now_add=True)
    position_end = models.DateTimeField(null=True, auto_now_add=True)
    active = models.BooleanField(default=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    employment_status_note = models.TextField(max_length=500, default='no one has written about this position yet...')
    employment_contract = models.ForeignKey(EmploymentContract, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return f"{self.employee.full_name} {self.department} {self.get_title_display()}"
    # email_active = models.BooleanField(default=True)



# represents and instance of an employee at a specific job for a duration of time
class SalariedPosition(BasePositionMixin, models.Model):
    # promotable only by an HR manager, area manager, faculty manager, ht or above

    levels = (
        (1,'I'),
        (2,'II'),
        (3, 'III'),
    )

    titles = (
        ('ap', 'Applicant'),
        ('tr', 'Trainee'),
        ('tch', 'Teacher'),
        ('fm', 'Faculty Manager'),
        ('am', 'Area Manager'),
        ('hr', 'HR Manager'),
        ('ht', 'Head Teacher'),  # access to modify the schedules
        ('tchmd', 'Teacher Management Director'),
        ('trd', 'Training Director'),
        ('rcd', 'Recruiting Director'),
        ('hrd', 'HR Director'),
        ('other', 'Other title'),
        ('dev', 'Developer'),
    )

    title = models.CharField(choices=titles, default='tch', max_length=25)


    @property
    def name(self):
        return str(self.employee.full_name)