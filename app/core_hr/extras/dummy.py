from django.contrib.auth.models import Group
from users.models import Employee


def get_dummy_user():
    # tier1 = Group.objects.get(name='Teacher')
    try:
        user = Employee.objects.get(id=4)
    except:
        user = None
    return user