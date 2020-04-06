from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from employment.models import SalariedPosition


# @admin.register(Position)
class EmployeeManagementAdmin(admin.ModelAdmin):
    class Meta:
        model = SalariedPosition

    def has_delete_permission(self, request, obj=None):
        return False

    list_filter = ('employee',)
    verbose_name_plural =  u"\u200B" + 'EmployeePosition'

