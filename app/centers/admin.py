from datetime import datetime

from django.conf import settings
from django.contrib import admin, messages
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError
from django.db.models import F, Q
# Register your models here.
from django.contrib import admin
from django.contrib.admin import SimpleListFilter, FieldListFilter, forms
from django_json_widget.widgets import JSONEditorWidget
from guardian.admin import GuardedModelAdmin
# Register your models here.
from ahr_extras.permissions import DefaultPermissionsMixin
from centers.models import LearningCenter, CenterRoom, CenterTeacher, BiWeeklyClass, WeekDays, BiWeeklyClassDetailProxy, \
    CenterWeeklyTimesheet
from core_hr.extras.dummy import get_dummy_user
from employment.models import SalariedPosition
from django_admin_listfilter_dropdown.filters import (
    DropdownFilter, ChoiceDropdownFilter, RelatedDropdownFilter, SimpleDropdownFilter
)


class LCPermissionsMixin(DefaultPermissionsMixin):
    perms_list = ['Head Teachers', 'Area Managers', 'Faculty Managers', '']


# TODO: Remove access to this field for non-priveledged users
@admin.register(LearningCenter)
class LearningCenterAdmin(LCPermissionsMixin):
    model = LearningCenter
    search_fields = ('name', 'code')
    verbose_name_plural = u"\u200B" + 'Learning Centers'


@admin.register(CenterRoom)
class CenterRoomAdmin(LCPermissionsMixin):
    search_fields = ('name',)
    list_filter = ('center__code',)
    ordering = ('name',)
    model = CenterRoom
    verbose_name_plural = u"\u200B" + 'Center Rooms'

    # BiWeeklyClass.objects.filter(day1_teacher__employee.name)
    def get_queryset(self, request):
        # return the request for a specific user here
        return CenterRoom.objects.filter(center=request.user.get_current_center())


@admin.register(CenterTeacher)
class CenterTeacherAdmin(LCPermissionsMixin):
    search_fields = ('teacher__employee__full_name',)
    model = CenterTeacher
    verbose_name_plural = u"\u200B" + 'Center Teacher'
    list_filter = ('center',)

    autocomplete_fields = ('center',)

    def get_queryset(self, request):
        # return the request for a specific user here
        return CenterTeacher.objects.filter(center=request.user.get_current_center())


@admin.register(CenterWeeklyTimesheet)
class CenterWeeklyTimeSheetAdmin(LCPermissionsMixin):
    model = CenterWeeklyTimesheet
    exclude = ('',)
    actions = ["tally_hours_for_week"]

    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget},
    }

    def has_delete_permission(self, request, obj=None):
        False

    def tally_hours_for_week(self, request, queryset):
        print('Counting stuff here for the win')
        meta = self.model._meta
        timesheet = queryset.first()
        start = datetime.now()
        timesheet.tally_hours_for_week()
        delta = datetime.now() - start
        print(delta)

    def get_changeform_initial_data(self, request):
        return {'center': request.user.get_current_center()}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # print(self.request.user)
        # self.request.user = get_dummy_user()
        center = request.user.get_current_center().pk
        # TODO : Add administrator override for area managers to process payroll if shtf
        if db_field.name == "center":
            kwargs["queryset"] = LearningCenter.objects.filter(id=center)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    fieldsets = (
        ('Center', {'fields': ('center',)}),
        ('Week Ending on:',
         {
             'fields':
                 ('week_end',)
         }),
        ('Days to accrue hours',
         {
             'fields':
                 (('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'),)
         }),
        ('Currently Accrued Hours', {
            'fields': ('current_hours',),
        }
         ),
    )
    # def teacher_hours_display(self, obj):
    #     return [[teacher for teacher in teacherweeklytimesheet ] for timesheet in obj.teacherweeklytimesheet_set..all()]


class SameTeacherFilter(SimpleListFilter):
    title = "Shared class status"
    parameter_name = 'shared_status'

    def lookups(self, request, model_admin):
        return [
            ('shared', 'Class has two teachers'),
            ('unshared', 'Class is taught by only one teacher')
        ]

    def queryset(self, request, queryset):
        day1_teachers = queryset.filter(day1_teacher=F('day2_teacher'))
        if self.value() == 'shared':
            return queryset.filter(~Q(day1_teacher=F('day2_teacher')))
        else:
            return queryset.filter(day1_teacher=F('day2_teacher'))


class TeacherFilter(SimpleListFilter):
    title = 'Teacher'
    parameter_name = 'teacher'
    # this template comes from django-admin-list-filter-dropdown package and is subclassed here
    template = 'django_admin_listfilter_dropdown/dropdown_filter.html'

    def lookups(self, request, model_admin):
        day1_teachers = [c.day1_teacher for c in model_admin.model.objects.select_related('day1_teacher')]
        day2_teachers = [c.day2_teacher for c in model_admin.model.objects.select_related('day2_teacher')]
        unique_teachers = set(day1_teachers + day2_teachers)
        return [(teacher.id, teacher) for teacher in unique_teachers]

    def queryset(self, request, queryset):
        if self.value():
            try:
                teacher_id = int(self.value())
            except (ValueError):
                print('teacher error')
                return queryset.none()
            else:
                return queryset.filter(Q(day1_teacher_id=teacher_id) | Q(day2_teacher_id=teacher_id))


class DayFilter(SimpleListFilter):
    title = 'day'
    parameter_name = 'day'

    def lookups(self, request, queryset):
        return [
            ('tu-fr', 'Tuesday/Friday'),
            ('wed-sat', 'Wednesday/Saturday'),
            ('thu-sun', 'Thursday/Sunday'),
            ('sat-sun', 'Saturday/Sunday B:1,2,3,4'),
            ('single-day', 'All Single Day Classes')
        ]

    def queryset(self, request, queryset):
        w = WeekDays
        if self.value() == 'tu-fr':
            return queryset.filter(Q(day1=w.TUESDAY) & Q(day2=w.FRIDAY))
        elif self.value() == 'wed-sat':
            return queryset.filter(Q(day1=w.WEDNESDAY) & Q(day2=w.SATURDAY))
        elif self.value() == 'thu-sun':
            return queryset.filter(Q(day1=w.THURSDAY) & Q(day2=w.SUNDAY))
        elif self.value() == 'sat-sun':
            return queryset.filter(Q(day1=w.SATURDAY) & Q(day2=w.SUNDAY))
        elif self.value() == 'one-day':
            return queryset.filter(Q(day1=w.UNUSED) | Q(day2=w.UNUSED))

        pass


@admin.register(BiWeeklyClass)
class MultiClassEditAdmin(LCPermissionsMixin):
    model = BiWeeklyClass
    list_display = ('class_title', 'block', 'room', 'day1', 'day1_teacher', 'day2', 'day2_teacher', 'is_active',)
    list_display_links = None
    autocomplete_fields = ('day1_teacher', 'day2_teacher')
    list_editable = ('block', 'room', 'day1_teacher', 'day2_teacher',)

    exclude = ('center',)
    list_filter = (
        TeacherFilter,
        ('block', ChoiceDropdownFilter),
        DayFilter,
        ('class_title', DropdownFilter),
        'is_active',
        SameTeacherFilter,
    )
    list_select_related = (
        'day1_teacher__teacher',
        'day2_teacher__teacher',
        'day1_teacher__teacher__employee',
        'day2_teacher__teacher__employee',
        'room'
    )
    if settings.DEBUG:
        list_per_page = 8
    else:
        list_per_page = 20

    def change_view(self, request, object_id, form_url='', extra_context=None):
        try:
            return super().change_view(request, object_id, form_url, extra_context)
        except Exception as e:
            print(e)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # print(self.request.user)
        # self.request.user = get_dummy_user()
        center = request.user.get_current_center().pk
        self.center = center
        if db_field.name == "room":
            kwargs["queryset"] = CenterRoom.objects.filter(
                center_id=center
            )
        if db_field.name == "day1_teacher":
            kwargs["queryset"] = CenterTeacher.objects.filter(
                center_id=center
            )
        if db_field.name == "day2_teacher":
            kwargs["queryset"] = CenterTeacher.objects.filter(
                center_id=center
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        # HACK to work around bug 13091
        try:
            obj.full_clean()
            obj.save()
        except ValidationError as e:
            messages.set_level(request, messages.ERROR)
            for message in e.messages:
                messages.error(request, 'Could not save %s because %s' % (obj, message))

    def get_queryset(self, request):
        # return the request for a specific user here
        self.request = request
        queryset = super(MultiClassEditAdmin, self).get_queryset(self.request)
        queryset.filter(center=self.request.user.get_current_center())
        # select_related('day1_teacher__teacher__employee','day2_teacher__teacher__employee','room')
        return queryset


@admin.register(BiWeeklyClassDetailProxy)
class ClassDetailAdmin(LCPermissionsMixin):
    model = BiWeeklyClass
    list_display = ('class_title', 'day1_teacher', 'day2_teacher', 'block', 'cm')
    search_fields = [
        'day1_teacher__teacher__employee__full_name',
        'day2_teacher__teacher__employee__full_name',
        'cm'
    ]
    exclude= ('',)
    if settings.DEBUG:
        list_per_page = 5
    else:
        list_per_page = 20
    list_filter = (
        TeacherFilter,
        ('block', ChoiceDropdownFilter),
        DayFilter,
        ('class_title', DropdownFilter),
        'is_active',
        SameTeacherFilter,
    )
    list_select_related = (
        'day1_teacher__teacher',
        'day2_teacher__teacher',
        'day1_teacher__teacher__employee',
        'day2_teacher__teacher__employee',
        'room'
    )

    def change_view(self, request, object_id, form_url='', extra_context=None):
        try:
            return super().change_view(request, object_id, form_url, extra_context)
        except Exception as e:
            print(e)

    def save_model(self, request, obj, form, change):
        # HACK to work around bug 13091
        print(str(obj))
        try:
            obj.full_clean()
            obj.save()
        except ValidationError as e:
            messages.set_level(request, messages.ERROR)
            for message in e.messages:
                messages.error(request, 'Could not save %s because %s' % (obj, message))


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # print(self.request.user)
        # self.request.user = get_dummy_user()
        center = request.user.get_current_center().pk
        self.center = center
        if db_field.name == "room":
            kwargs["queryset"] = CenterRoom.objects.filter(
                center_id=center
            )
        if db_field.name == "day1_teacher":
            kwargs["queryset"] = CenterTeacher.objects.filter(
                center_id=center
            )
        if db_field.name == "day2_teacher":
            kwargs["queryset"] = CenterTeacher.objects.filter(
                center_id=center
            )

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        # return the request for a specific user here
        self.request = request
        queryset = super(ClassDetailAdmin, self).get_queryset(self.request)
        queryset.filter(center=self.request.user.get_current_center())
        return queryset
