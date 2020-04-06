from __future__ import absolute_import, unicode_literals
from django.apps import apps
import os
from celery import Celery

from django.conf import settings

# epriodic task not showing https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=3&ved=2ahUKEwieuYDq5PPnAhWXYysKHTO9CDoQFjACegQIAhAB&url=https%3A%2F%2Fdev.to%2Fvergeev%2Fdjango-celery-beat-how-to-get-the-last-time-a-periodictask-was-run-39k9&usg=AOvVaw2NDy43cX6JFznG5ryyQ0pP

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apaxhr.settings')

app = Celery('app')

app.config_from_object(settings, namespace='CELERY')

# load tasks from each django app config in settings
# lambda: settings.INSTALLED_APPS
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request{0!r}'.format(self.request))

# @app.on_after_finalize.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # sender.add_periodic_task(2.0, tasks.core_hr_task.s(), name='core_hr_task')

@app.task
def test(arg):
    print(arg)