from django.urls import path, include
from django.conf import settings
from employee_mgmt import views

app_name='employee_mgmt'

urlpatterns = [
    path('', views.EmployeeManagementHome.as_view(),name='home'),

]