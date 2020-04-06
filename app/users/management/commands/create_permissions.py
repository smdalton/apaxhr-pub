from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, Permission
from users.models import Employee
from .create_users_and_documents import assign_documents_to_user
import ahr_extras.permissions as p
from ahr_extras.permissions import permissions_groups as pg
class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.groups = p.get_all_permissions_groups()
        self.tier1 = pg['tier1']
        self.tier2 = pg['tier2']
        self.tier3 = pg['tier3']
        self.tier4 = pg['tier4']
        self.tier5 = pg['tier5']


    def create_groups(self):
        for group_name in self.groups:
            obj, created = Group.objects.get_or_create(name=group_name)

    def make_super_user_all_groups_member(self):
        superuser=Employee.objects.get(email='smd@gmail.com')
        for name in self.groups:
            group=Group.objects.get(name=name)
            superuser.groups.add(group)

    def make_all_tiers_employee(self):
        tier1 = Employee.objects.create(
            email='tier1@gmail.com',
            password='pass1234',
        )

        # applicants
        teachers = Group.objects.get(name='Teachers')
        teachers.user_set.add(tier1)

        tier2 = Employee.objects.create(
            email='tier2@gmail.com',
            password='pass1234'
        )
        fms = Group.objects.get(name='Faculty Managers')
        fms.user_set.add(tier2)

        tier3 = Employee.objects.create(
            email='tier3@gmail.com',
            password='pass1234'
        )
        ams = Group.objects.get(name='Area Managers')
        ams.user_set.add(tier3)

        tier4 = Employee.objects.create(
            email='tier4@gmail.com',
            password='pass1234'
        )
        directors = Group.objects.get(name='Area Managers')
        directors.user_set.add(tier4)

        assign_documents_to_user(tier1)
        assign_documents_to_user(tier2)
        assign_documents_to_user(tier3)
        assign_documents_to_user(tier4)

    def assign_tier1_permissions(self, user_list):

        permissions = []
        # document creation, document viewing, no admin access


        for group_name in self.tier1:
            group = Group.objects.get(name=group_name)
            group.permissions = permissions

            pass
        # document creation
    def assign_tier2_permissions(self, user_list):

        """"""
        permissions = []
        for group_name in self.tier2:
            group = Group.objects.get(name=group_name)
            group.permissions = permissions

            pass

    def assign_tier3_permissions(self, user_list):
        permissions = []

        for group_name in self.tier3:
            group = Group.objects.get(name=group_name)
            group.permissions = permissions

            pass


    def assign_tier4_permissions(self):
        permissions = []

        for group_name in self.tier4:
            group = Group.objects.get(name=group_name)
            group.permissions = permissions

            pass


    def assign_permissions(self):
        pass


    def create_permission_users(self):
        pass




    def handle(self, *args, **options):
        print('Setting permissions')
        self.create_groups()
        self.make_super_user_all_groups_member()
        self.make_all_tiers_employee()
