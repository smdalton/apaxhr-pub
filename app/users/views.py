
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, UpdateView, ListView, TemplateView
from django.urls import reverse

from core_hr.extras.dummy import get_dummy_user
from users.forms import EmployeeCreationForm

# Create your views here.
from users.models import Employee



class UsersHome(TemplateView):
    template_name = 'users/users_home.html'



class UserCreateView(CreateView):
    model = Employee
    form_class = EmployeeCreationForm
    template_name = 'users/user_creation.html'

    def get_context_data(self, **kwargs):
        context = super(UserCreateView, self).get_context_data()
        context['page_name'] = 'Personnel Registration Page'
        return context

    def get_success_url(self):
        return reverse('core_hr:self_service')




class UserUpdateView(UpdateView):
    model = Employee
    template_name = 'users/user_creation.html'

    fields = [
        'id',
        'last_login',
        'password',
        'is_superuser',
        'employee_id_number',
        'is_staff',
        'is_active',
        'employment_status',
        'employment_status_note',
        'user_permissions',
        'groups'
    ]

    def get_object(self, *args, **kwargs):
        #TODO: replace this stub with the request.user
        self.request.user = get_dummy_user()
        return self.request.user


    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data()
        context['page_name'] = 'User Account Information Update'
        return context

    def get_success_url(self):
        return reverse('core_hr:self_service')


class UserLoginView(LoginView):
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse('core_hr:self_service')
