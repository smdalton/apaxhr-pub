# make a day-selection query manager
# returns classes for a given day at a given center

from django.db import models
from django.db.models import Q

class CenterTeacherManager(models.Manager):

    def get_employee_from_teacher(self):

        pass

    def get_position_from_teacher(self):
        pass


# class LearningCenterManager(models.Manager):



class BiweeklyClassManager(models.Manager):
    # these are the integer choice fields for days of the week
    mon = 1

    tue = 2
    fri = 5

    wed = 3
    sat = 6

    thu = 4
    sun = 7

    def tue_fri(self, center):
        # return sorted by block, then by room
        print('getting tuesday friday classes for center %s', center)
        day_query = Q(day1=self.tue) & Q(day2=self.fri)
        block_query = (Q(block=5) | Q(block=6))
        return self.filter(center=center).filter(day_query).filter(block_query)

    def wed_sat(self, center):
        # return sorted by block, then by room
        print('getting wed sat classes for center %s', center)
        day_query = Q(day1=self.wed) & Q(day2=self.sat)
        block_query = Q(block=5) | Q(block=6)
        return self.filter(center=center).filter(day_query).filter(block_query)

    def thu_sun(self, center):
        # return sorted by block, then by room
        print('getting thu sun classes for center %s', center)
        # filter out am blocks
        day_query = Q(day1=self.thu) & Q(day2=self.sun)
        block_query = Q(block=5) | Q(block=6)
        return self.filter(center=center).filter(day_query).filter(block_query)

    def sat_sun_am(self, center):
        # return sorted by block, then by room
        print('getting sat sun am classes for center %s', center)
        day_query = Q(day1=self.sat) & Q(day2=self.sun)
        block_query = Q(block=1) | Q(block=2)
        return self.filter(center=center).filter(day_query).filter(block_query)

    def sat_sun_pm(self,center):
        # return sorted by block, then by room
        print('getting sat sun pm classes for center %s', center)
        day_query = Q(day1=self.sat) & Q(day2=self.sun)
        block_query = Q(block=3) | Q(block=4)
        return self.filter(center=center).filter(day_query).filter(block_query)