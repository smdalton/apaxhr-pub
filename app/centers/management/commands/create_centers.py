import time
import os
import random
from itertools import cycle

from django.core.management.base import BaseCommand
from django.db import IntegrityError
from faker import Faker
from colorama import Back, Fore
from centers.models import TimeBlocks, LearningCenter, CenterRoom, CenterTeacher, BiWeeklyClass
from employment.models import SalariedPosition, Department
from users.models import Employee

fake = Faker()
Faker.seed(2323)


# fake.phone_number()
# fake.city()`
# fake.building_number()
# fake.address()
# fake.date_between(start_date="-30y", end_date="today")
# fake.date_of_birth(tzinfo=None, minimum_age=0, maximum_age=115)
# fake.day_of_month()
# fake.month()
# fake.year()
# fake.bs()
# fake.latlng()
# fake.local_latlng(country_code="US", coords_only=False)
# fake.local_latlng(country_code='VN', coords_only=True)
# fake.date(pattern="%Y-%m-%d", end_datetime=None)


class Command(BaseCommand):
    help = "Initializes users, clears db, makes and applies migrations, runs server"
    users = []
    centers = []
    april_rooms = [str(i) for i in range(1, 13)]
    igarten_rooms = ['iG-' + str(i) for i in range(1, 5)]
    center_names = (('HP', 'Hai Phong'), ('HN', 'Hanoi'), ('HCMC', 'Ho Chi Minh City'))
    center_teachers = []
    cms = [fake.name() for x in range(1,7)]
    course_titles = ('Caterpillar'
                     , 'Cocoon'
                     , 'Sunflower'
                     , 'Rookie'
                     , 'Rookie'
                     , 'Seedbed'
                     , 'Sprout'
                     , 'Sapling'
                     , 'Junior_Master'
                     , 'Extra_Care'
                     , 'Hangout'
                     , 'Lighthouse')

    def create_centers(self):
        for center_code, center_name in self.center_names:
                center = LearningCenter.objects.update_or_create(
                    code=center_code,
                    name=center_name,
                    city=center_name,
                    address=fake.address(),
                )
                print(f"Created: {center_code}")

    def create_and_assign_center_rooms(self):
        for center in LearningCenter.objects.all():
            print(f"creating {center} rooms")
            for room in self.april_rooms:
                try:
                    CenterRoom.objects.create(center=center, name=room)
                except Exception as e:
                    print(e)
            for room in self.igarten_rooms:
                try:
                    CenterRoom.objects.create(center=center, name=room)
                except Exception as e:
                    print(e)


    def create_center_teachers(self):
        # get teachers from positions of type teacher

        teachers = SalariedPosition.objects.filter(title='tch').exclude(employee__full_name='')

        hp_teachers = teachers[:10]
        hn_teachers = teachers[10:20]
        hcmc_teachers = teachers[20:25]

        hp_center = LearningCenter.objects.get(code='HP')
        hn_center = LearningCenter.objects.get(code='HN')
        hcmc_center = LearningCenter.objects.get(code='HCMC')

        # assign teachers for Hai Phong
        num = 1
        for teacher in hp_teachers:
            result = CenterTeacher.objects.get_or_create(
                center=hp_center,
                teacher=teacher,
                preferred_room=str(num),
            )
            num += 1
            if result[1]:
                self.center_teachers.append(result[0])

        for teacher in hn_teachers:
            result = CenterTeacher.objects.get_or_create(
                center=hn_center,
                teacher=teacher,
                preferred_room=str(num),
            )
            num += 1
            if result[1]:
                self.center_teachers.append(result[0])
            pass

        for teacher in hcmc_teachers:
            result = CenterTeacher.objects.get_or_create(
                center=hcmc_center,
                teacher=teacher,
                preferred_room=str(num),
            )
            num += 1
            if result[1]:
                self.center_teachers.append(result[0])
            pass
    course_titles_cycle = cycle(course_titles)

    def create_weekday_biweekly_courses(self):
        global cm, block, class_title
        center = LearningCenter.objects.get(code='HP')
        tu_fri = (2, 5)
        wed_sat = (3, 6)
        thu_sun = (4, 7)
        sat_sun = (6, 7)
        weekday_sets = [tu_fri, wed_sat, thu_sun]

        teacher_pks = CenterTeacher.objects.filter(center__code='HP').values_list('pk',flat=True)
        rooms = CenterRoom.objects.filter(center__code='HP').all()

        # make 26 classes per day set
        # cycle the teachers evenly
        for day_set in weekday_sets:
            for block in [5,6]:
                teachers = cycle(list(CenterTeacher.objects.filter(center__code='HP').all())[:12])
                for room in list(CenterRoom.objects.filter(center__code='HP').all()):
                    class_title = random.choice(self.course_titles)
                    try:
                        teacher = next(teachers)
                        BiWeeklyClass.objects.create(
                            room=room,
                            center=center,
                            block=block,
                            day1_teacher=teacher,
                            day2_teacher=teacher,
                            day1=day_set[0],
                            day2=day_set[1],
                            class_title=class_title,
                            cm=random.choice(self.cms)
                        )
                    except Exception as e:
                        print(e)
        # just weekend classes now
        for block in [1,2,3,4]:
            teachers = cycle(list(CenterTeacher.objects.filter(center__code='HP').all()))
            for room in list(CenterRoom.objects.filter(center__code='HP').all()):
                class_title = random.choice(self.course_titles)
                try:
                    teacher = next(teachers)
                    BiWeeklyClass.objects.create(
                        room=room,
                        center=center,
                        block=block,
                        day1_teacher=teacher,
                        day2_teacher=teacher,
                        day1=sat_sun[0],
                        day2=sat_sun[1],
                        class_title=class_title,
                        cm=random.choice(self.cms)
                    )
                except Exception as e:
                    print(e)


    def handle(self, **args):
        # os.system('export DJANGO_COLORS="light;error=yellow/blue,blink;notice=magenta"')
        print(Fore.CYAN)
        print('---> Creating Centers')
        self.create_centers()
        print('---> Creating Rooms')
        self.create_and_assign_center_rooms()
        time.sleep(1)
        print('---> Creating Center Teachers')
        self.create_center_teachers()
        print('---> Creating BiWeeklyCenterCourses')
        self.create_weekday_biweekly_courses()
        print(Fore.BLACK)
