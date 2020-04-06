import time
import os
import random

from django.core.management.base import BaseCommand
from faker import Faker
from colorama import Back, Fore
from centers.models import LearningCenter, CenterRoom
from employment.models import SalariedPosition, Department
from users.models import Employee

fake = Faker()
Faker.seed(2323)
# fake.phone_number()
# fake.city()
# fake.building_number()
# fake.address()
# fake.date_between(start_date="-30y", end_date="today")
# fake.date_of_birth(tzinfo=None, minimum_age=0, maximum_age=115)
# fake.day_of_month()
# fake.month()
# fake.year()
# fake.bs()
# fake.latlng()
# fake.local_latlng(country_code="US", coords_only=False)
# fake.local_latlng(country_code='VN', coords_only=True)
# fake.date(pattern="%Y-%m-%d", end_datetime=None)


class Command(BaseCommand):
    help = "Initializes users, clears db, makes and applies migrations, runs server"
    users = []
    centers = []
    placed_employees = []
    # get all employees in the teachers/head teachers/ faculty managers groups
    def create_departments(self):
        from employment.models import Department
        try:
            # creates teaching department
            Department.objects.create(id=1)
        except:
            pass

    def assign_employees_to_teaching_positions(self):
        department = Department.objects.get(id=1)
        for employee in list(Employee.objects.all()):
            self.placed_employees.append(
                SalariedPosition.objects.create(
                    title='tch',
                    employee=employee,
                    department=department,
                    active=True
                )
            )


    def handle(self, **args):
        # os.system('export DJANGO_COLORS="light;error=yellow/blue,blink;notice=magenta"')
        print(Fore.LIGHTMAGENTA_EX)
        print('---> Creating Departments')
        self.create_departments()
        print('---> Assigning employees to positions type: teacher')
        self.assign_employees_to_teaching_positions()
        print(Fore.BLACK)
