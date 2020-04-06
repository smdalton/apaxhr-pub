from django.contrib import admin

# Register your models here.
from ahr_extras.permissions import DefaultPermissionsMixin
from centers.models import LearningCenter, CenterTeacher
from employment.models import SalariedPosition
from users.models import Employee


class EMPPermissionsMixin(DefaultPermissionsMixin):
    perms_list = [
        'HR Managers',
        'HR Directors',
        'Developers',
        'Teacher Management Directors',
        'Training Directors',
    ]

# SalariedPosition.objects.filter(employee__full_name__icontains='Jill')
@admin.register(SalariedPosition)
class EmployeePositionAdmin(EMPPermissionsMixin):
    def has_delete_permission(self, request, obj=None):
        return False
    model = SalariedPosition
    # search_fields =
    search_fields = ('employee__full_name', 'teacher_salaries__center__code')
    list_display = ( 'name', 'department','title', 'position_start', 'position_end','get_center_name')
    # model = SalariedPosition
    list_filter = ('title','department',)

    def get_center_name(self, obj):
        return CenterTeacher.objects.get(teacher=obj).center

    # def get_queryset(self, request):
    #     return super(EmployeePositionAdmin, self).get_queryset(request).select_related('book')
    #

    verbose_name_plural = u"\u200B" + 'EmployeePosition'
