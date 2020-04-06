from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from .models import Employee


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Employee
        fields = ('email',)

class EmployeeCreationForm(UserCreationForm):
    class Meta:
        model = Employee
        exclude = (
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
        )
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.add_input((Submit('submit', 'Save person')))


class EmployeeChangeForm(UserChangeForm):
    class Meta:
        model = Employee
        exclude = (
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
        )

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.add_input((Submit('submit', 'Save person')))

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = Employee
        fields = ('email',)

