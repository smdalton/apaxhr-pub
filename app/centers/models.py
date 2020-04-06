import logging
from calendar import calendar
from collections import defaultdict
from datetime import timedelta

from django.contrib.postgres.fields import JSONField, ArrayField
from django.db import models

# Create your models here.

from .managers import BiweeklyClassManager
from employment.models import SalariedPosition
from django.utils.translation import gettext_lazy as _
from django.db.models import IntegerField, Model, Q, UniqueConstraint
from django.conf import settings

Employee = settings.AUTH_USER_MODEL


class WeekDays(models.IntegerChoices):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7
    UNUSED = 8
    # SATURDAY_AM = 9


class TimeBlocks(models.IntegerChoices):
    BLOCK_1 = 1, _('Block 1 8:00 - 9:30')
    BLOCK_2 = 2, _('Block 2 9:30 - 11:15 ')
    BLOCK_3 = 3, _('Block 3 14:00 - 15:30')
    BLOCK_4 = 4, _('Block 4 15:45 - 17:15')
    BLOCK_5 = 5, _('Block 5 17:30 - 19:00')
    BLOCK_6 = 6, _('Block 6 19:15 - 20:45')


class LearningCenter(models.Model):
    code = models.CharField(max_length=6, unique=True)
    name = models.CharField(max_length=40, unique=True)
    city = models.CharField(max_length=25)
    address = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)

    def query_test(self):
        print('getting tuesday friday classes for center %s', self)
        day_query = Q(day1=self.tu_fri[0]) & Q(day2=self.tu_fri[1]) & Q(block=5) & Q(block=6)
        return BiWeeklyClass.objects.filter(center=self)

    def __str__(self):
        return f" {self.code}"


class CenterTeacher(models.Model):
    class Meta:
        verbose_name = u"\u200B" + 'Teacher'
        constraints = [
            models.UniqueConstraint(fields=['center', 'teacher'], name='teacher_constraint')
        ]

    is_active = models.BooleanField(default=True)  # deactivate to "delete"
    center = models.ForeignKey(LearningCenter, on_delete=models.CASCADE)
    teacher = models.OneToOneField(SalariedPosition, on_delete=models.CASCADE, related_name='teacher_salaries')
    preferred_room = models.SmallIntegerField(default=-1)

    def get_blocks_worked_from_weekly_schedule(self):
        day1 = self.biweekly_day1_teacher_set.count()
        day2 = self.biweekly_day2_teacher_set.count()
        return day1 + day2

    # TODO HAVE TO COUNT DAY2!!!!
    def monday_block_count(self):
        # query all blocks worked by this teacher on a monday
        # in day: day1 or day2
        day_query = (Q(day1=WeekDays.MONDAY) | Q(day2=WeekDays.MONDAY))
        # Collect the union of all biweekly classes the teacher may have taught
        queryset = self.biweekly_day1_teacher_set.all()|self.biweekly_day2_teacher_set.all()
        return queryset.filter(day_query).count()

    def tuesday_block_count(self):
        day_query = (Q(day1=WeekDays.TUESDAY) | Q(day2=WeekDays.TUESDAY))
        queryset = self.biweekly_day1_teacher_set.all() | self.biweekly_day2_teacher_set.all()
        return queryset.filter(day_query).count()

    def wednesday_block_count(self):
        day_query = (Q(day1=WeekDays.WEDNESDAY) | Q(day2=WeekDays.WEDNESDAY))
        return self.biweekly_day1_teacher_set.filter(day_query).count()

    def thursday_block_count(self):
        day_query = (Q(day1=WeekDays.THURSDAY) | Q(day2=WeekDays.THURSDAY))
        queryset = self.biweekly_day1_teacher_set.all() | self.biweekly_day2_teacher_set.all()
        return queryset.filter(day_query).count()

    def friday_block_count(self):
        day_query = (Q(day1=WeekDays.FRIDAY) | Q(day2=WeekDays.FRIDAY))
        queryset = self.biweekly_day1_teacher_set.all() | self.biweekly_day2_teacher_set.all()
        return queryset.filter(day_query).count()

    def saturday_block_count(self):
        day_query = (Q(day1=WeekDays.SATURDAY) | Q(day2=WeekDays.SATURDAY))
        queryset = self.biweekly_day1_teacher_set.all() | self.biweekly_day2_teacher_set.all()
        return queryset.filter(day_query).count()

    def sunday_block_count(self):
        day_query = (Q(day1=WeekDays.SUNDAY) | Q(day2=WeekDays.SUNDAY))
        queryset = self.biweekly_day1_teacher_set.all() | self.biweekly_day2_teacher_set.all()
        return queryset.filter(day_query).count()

    def get_all_blocks(self):
        total = self.monday_block_count() + self.tuesday_block_count() \
                + self.wednesday_block_count() + self.thursday_block_count() \
                + self.friday_block_count() + self.saturday_block_count() \
                + self.sunday_block_count()
        return total

    def __str__(self):
        return f"{self.teacher.employee.full_name} {self.center_id}"


class CenterRoom(models.Model):
    class Meta:
        verbose_name = u"\u200B" + 'Room'
        constraints = [
            models.UniqueConstraint(fields=['center', 'name'], name='room_constraint')
        ]

    is_active = models.BooleanField(default=True)
    center = models.ForeignKey(LearningCenter, on_delete=models.CASCADE)
    name = models.CharField(_('unique room'),
                            default=-1, max_length=12)
    note = models.TextField(_('Note any important details about a room here'), max_length=250)

    def __str__(self):
        return self.name


class BiWeeklyClass(models.Model):

    class Meta:
        verbose_name =  'Class Schedule'
        constraints = [
            # uniqueness for rooms, only one class can be scheduled per room, per center, per day, per block
            models.UniqueConstraint(fields=['center', 'room', 'day1', 'block'], name='day1 room conflict'),
            models.UniqueConstraint(fields=['center', 'room', 'day2', 'block'], name='day2 room conflict'),

            # uniqueness for teachers, a teacher can only be scheduled for one block per each day
            models.UniqueConstraint(fields=['center',  'block', 'day1','day1_teacher'], name='day1 teacher already booked'),
            models.UniqueConstraint(fields=['center',  'block', 'day2','day2_teacher'], name='day2 teacher already booked'),


        ]
    center = models.ForeignKey(LearningCenter, on_delete=models.CASCADE)
    block = models.SmallIntegerField(choices=TimeBlocks.choices)
    room = models.ForeignKey(CenterRoom, on_delete=models.CASCADE)

    other_note = models.TextField(
        _('Fill out this note if you have selected an other type class'),
        max_length=85,
        default='not an other course')

    day1_teacher = models.ForeignKey(CenterTeacher, on_delete=models.CASCADE, related_name='biweekly_day1_teacher_set')
    day2_teacher = models.ForeignKey(CenterTeacher, on_delete=models.CASCADE, related_name='biweekly_day2_teacher_set')

    day1 = models.SmallIntegerField(choices=WeekDays.choices, default=9)
    day2 = models.SmallIntegerField(choices=WeekDays.choices, default=9)

    is_active = models.BooleanField(default=True)

    class_title = models.CharField(max_length=25)
    cm = models.CharField(max_length=30, blank=True)
    objects = BiweeklyClassManager()

    def block_display(self):
        return self.get_block_display()

    def __str__(self):
        return f"{self.class_title} Block {self.block_display()} {self.get_day1_display(), self.get_day2_display()} "

class BiWeeklyClassDetailProxy(BiWeeklyClass):
    class Meta:
        verbose_name = 'Class \u200B Detail'
        proxy = True

# logs all hours worked for a week based on scheduled classes
class CenterWeeklyTimesheet(models.Model):
    center = models.ForeignKey(LearningCenter, on_delete=models.CASCADE)
    week_end = models.DateField(editable=True)
    # for each day in the week

    # selectively skip payroll processing for specific days with these checkboxes based on business needs
    monday = models.BooleanField(default=False)
    tuesday = models.BooleanField(default=True)
    wednesday = models.BooleanField(default=True)
    thursday = models.BooleanField(default=True)
    friday = models.BooleanField(default=True)
    saturday = models.BooleanField(default=True)
    sunday = models.BooleanField(default=True)

    current_hours = JSONField(default={'hours not tallied yet':0})
    # translate the boolean selected dates to actual dates for hourly queries
    def get_dates_based_on_week_end(self):
        if self.week_end.weekday() != 0:
            print('task not executed with monday set as the weekend date')
            return ('Schedule Not set to start on a monday, please correct')
        end = self.week_end
        day_dict = {}

        if self.monday:
            day_dict['monday'] = end - timedelta(days=7)
        if self.tuesday:
            day_dict['tuesday'] = end - timedelta(days=6)
            #calculate tuesday
        if self.wednesday:
            day_dict['wednesday'] = end - timedelta(days=5)
            #calculate wednesday
        if self.thursday:
            day_dict['thursday'] = end - timedelta(days=4)
            #calculate thursday
        if self.friday:
            #calculate friday
            day_dict['friday'] = end - timedelta(days=3)
        if self.saturday:
            #calculate saturday
            day_dict['saturday'] = end - timedelta(days=2)
        if self.sunday:
            #calculate_sunday
            day_dict['sunday'] = end - timedelta(days=1)
        self.day_dict = day_dict

        return day_dict

    def tally_hours_for_week(self):

        dates = self.get_dates_based_on_week_end()
        results = defaultdict(int)
        for day in dates.keys():
            # print(f"--------------------    {day}        -----------------------")
            for teacher in self.center.centerteacher_set.all():
                # print(f"calculating {teacher} hours")
                day_block_count = 0

                if day == 'monday':
                    day_block_count = teacher.monday_block_count()
                if day == 'tuesday':
                    day_block_count = teacher.tuesday_block_count()
                if day == 'wednesday':
                    day_block_count = teacher.wednesday_block_count()
                if day == 'thursday':
                    day_block_count = teacher.thursday_block_count()
                if day == 'friday':
                    day_block_count = teacher.friday_block_count()
                if day == 'saturday':
                    day_block_count = teacher.saturday_block_count()
                if day == 'sunday':
                    day_block_count = teacher.sunday_block_count()

                results[str(teacher)] += day_block_count

                # TODO: Implement multiplier for blocks here
                hours = day_block_count * 1.5
                # print(self.center, dates[day],hours,day_block_count)
                try:
                    TeacherDailyTimesheet.objects.update_or_create(
                        teacher=teacher,
                        center = self.center,
                        date=dates[day],
                        blocks = day_block_count,
                        hours=hours,
                    )

                except Exception as e:
                    print(e)

                # save the intermediate results to the json field for admin teacher view
        self.current_hours = results
        self.save()
        return results
    #prepopulate the form

    def reconcile_hours(self):
        pass

    def __str__(self):
        days = self.get_dates_based_on_week_end()
        if type(days)== type(dict()):
            days = "".join([str((key, days[key].day)) for key in days.keys()])
        else:
            print(f"its a {type(days)}")
        return f"{self.center.code}" \
               f" {self.week_end.strftime('%B %Y')}" \
               f" Hours for days: {days} "

# we need to log these in center report

class TeacherDailyTimesheet(models.Model):
    class Meta:
        constraints = [
            # ensure that only
            models.UniqueConstraint(
                fields=['teacher', 'center', 'date'],
                name='already logged hours, if needed delete teacherdailytimesheet manually from admin panel'),
        ]

    center = models.ForeignKey(LearningCenter, on_delete=models.CASCADE)
    teacher = models.ForeignKey(CenterTeacher, on_delete=models.CASCADE)
    date = models.DateField(blank=False)
    blocks = models.PositiveSmallIntegerField(default=0)
    hours = models.DecimalField(max_digits=4, decimal_places=2, default=0)
