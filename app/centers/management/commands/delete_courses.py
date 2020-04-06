from itertools import cycle

from django.core.management.base import BaseCommand
from django.db import IntegrityError
from faker import Faker
from colorama import Back, Fore
from centers.models import TimeBlocks, LearningCenter, CenterRoom, CenterTeacher, BiWeeklyClass
from employment.models import SalariedPosition, Department
from users.models import Employee




class Command(BaseCommand):

    def handle(self, **args):
        BiWeeklyClass.objects.all().delete()