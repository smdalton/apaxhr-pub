from django.contrib import admin

# Register your models here.
from centers.models import CenterTeacher
from payroll.models import PositionSalaryInfo, SalarySteps, SalariedPosition, CityStipend, Bonus, CompletionBonus
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group
admin.site.unregister(Group)

class PRLPermissionsMixin(admin.ModelAdmin):

    def has_module_permission(self,request, obj=None):
        perms = list(request.user.groups.values_list('name', flat=True))
        if any(item in ['HR Directors', 'HR Managers',] for item in perms):
            print('has change permission')
            return True
        else:
            print('Permission Denied ')

    def has_delete_permission(self, request, obj=None):
        return False


class UserInLine(admin.TabularInline):
    model = Group.user_set.through
    extra = 0

@admin.register(Group)
class GenericGroup(GroupAdmin):
    inlines = [UserInLine]


@admin.register(PositionSalaryInfo)
class EmployeePositionAdmin(PRLPermissionsMixin):
    def has_delete_permission(self, request, obj=None):
        return False

    search_fields = ('position__employee__full_name',)
    # autocomplete_fields = ('salaried_position__employee_full_name',)
    list_display = ('name','salary_step','get_center_name')
    def get_center_name(self, obj):

        return
    model = PositionSalaryInfo
    verbose_name_plural =  u"\u200B" + 'PositionSalaryInfo'

    def get_center_name(self, obj):
        return CenterTeacher.objects.get(teacher=obj.position).center


# @admin.register(Bonus)
# class BonusAdmin()

#@admin.register(SalariedPosition)
class EmployeePositionAdmin(object):
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

