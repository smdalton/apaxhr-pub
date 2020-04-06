from __future__ import absolute_import, unicode_literals
from celery import shared_task


from users.models import Employee


@shared_task
def core_hr_task():
    return '------->Task from schedules<-------- test'
