import csv
from datetime import datetime, timedelta

from botocore.exceptions import EndpointConnectionError
from django.contrib import admin

from django.apps import apps
from django.contrib.admin import SimpleListFilter
from django.db.models import Subquery
from django.http import HttpResponse
from django.utils.safestring import mark_safe

import datedelta
from core_hr.models import Employee, Passport, RegistryOfStay, WorkPermit, DegreeDocument, AchievementCertificate, \
    TeachingCertificate, Resume


from django.contrib.sessions.models import Session


