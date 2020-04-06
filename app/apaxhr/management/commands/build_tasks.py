from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, Permission
from users.models import Employee


class Command(BaseCommand):

    def __init__(self):
        self.tasks = 'test'

    def handle(self, *args, **options):
        print('Setting permissions')
