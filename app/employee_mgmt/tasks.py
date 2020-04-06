from __future__ import absolute_import, unicode_literals
from celery import shared_task


from users.models import Employee


@shared_task
def employee_management_task():
    return '------->Task from employee management<-------- test'
