from django.db import models
from djmoney.models.fields import MoneyField
from djmoney.money import Money
import calendar
from calendar import monthrange
# Create your models here.
from centers.models import LearningCenter, CenterTeacher
from employment.models import SalariedPosition

# Build data for salaries, that is then applied in a monthly task object which generates
# all teacher payroll

# make city stipends editable
class CityStipend(models.IntegerChoices):
    TIER_1 = 1, ('Tier 1 City')
    TIER_2 = 2, ('Tier 2 City')
    TIER_3 = 3, ('Tier 3 City')
    TIER_4 = 4, ('Tier 4 City')
    TIER_5 = 5, ('Tier 5 City')
    TIER_6 = 6, ('Tier 6 City')


class CompletionBonus(models.IntegerChoices):
    MONTH_4 = 1, ('4 month')
    MONTH_8 = 2, ('8 month')
    MONTH_12 = 3,('12 month')


class SalarySteps(models.IntegerChoices):
    STEP_1 = 1, ('Salary Step 1')
    STEP_2 = 2, ('Salary Step 2')
    STEP_3 = 3, ('Salary Step 3')
    STEP_4 = 4, ('Salary Step 4')
    STEP_5 = 5, ('Salary Step 5')
    STEP_6 = 6, ('Salary Step 6')
    STEP_7 = 7, ('Salary Step 7')
    STEP_8 = 8, ('Salary Step 8')
    STEP_9 = 9, ('Salary Step 9')
    STEP_10 = 10, ('Salary Step 10')
    STEP_11 = 11, ('Salary Step 11')
    STEP_12 = 12, ('Salary Step 12')



class PositionSalaryInfo(models.Model):
    position = models.OneToOneField(SalariedPosition, on_delete=models.CASCADE)
    city_stipend = models.SmallIntegerField(choices=CityStipend.choices, default=1)
    salary_step = models.SmallIntegerField(choices=SalarySteps.choices, default=1)
    leave_hours = models.SmallIntegerField(default=0)

    def name(self):
        return self.position.employee
    def __str__(self):
        return f"{self.position.employee} step:{self.salary_step}"

class Bonus(models.Model):
    related_salary = models.ForeignKey(PositionSalaryInfo, on_delete=models.CASCADE)
    amount1 = models.PositiveIntegerField(default=0)
    amount_2 = models.PositiveIntegerField(default=0)
    description = models.TextField(max_length=100)
    part_1_awarded = models.BooleanField(default=False)
    part_1_awarded_on = models.DateTimeField(default=None)
    part_2_awarded = models.BooleanField(default=False)
    part_2_awarded_on = models.DateTimeField(default=None)


#
# # make an annual payroll period for each year
# class AnnualCompanyPayroll(models.Model):
#     year = models.DateField()
#     pass
#
# class MonthlyCompanyPayroll(models.Model):
#     payroll_year = models.ForeignKey(AnnualCompanyPayroll, on_delete=models.CASCADE)
#     month_start_date = models.DateField(auto_now_add=True)
#     month_end_date = models.DateField(auto_now_add=False, default=-1)
#
#     pass
#
# # make a center monthly payroll period
# class CenterMonthlyPayrollPeriod(models.Model):
#     monthly_payroll = models.ForeignKey(MonthlyCompanyPayroll, on_delete=models.CASCADE)
#     center = models.ForeignKey(LearningCenter, on_delete=models.CASCADE)
#
#     def get_month_name(self):
#         pass
#
#     def __str__(self):
#         return f"{self.month_start_date.strftime('%B')} pay period   days: {self.month_start_date} - {self.month_end_date}"
#     pass
#
#
#
#
#
#
#
#
# def compute_monthly_pay():
    # compute salary
    # compute hours
    # compute overtime hours
    # apply stipends
    # apply applicable bonuses
    # set bonuses to completed
    # apply taxes
    # print readable report

#
# teacher.get_hours_from_schedule()
