from django.urls import path, include
from django.conf import settings
from . import views
urlpatterns = [
    path('', views.home),
    path('schedules/grid/', views.ScheduleGridDisplay.as_view() ),
]
