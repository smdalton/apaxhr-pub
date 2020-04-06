from django.urls import path, include
from django.conf import settings
from . import views


app_name='employment'

urlpatterns=[
path('',views.LifeCycleHome.as_view(), name='landing'),
]