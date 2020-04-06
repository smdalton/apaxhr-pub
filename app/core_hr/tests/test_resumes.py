from random import random

import faker
from django.test import TestCase

from core_hr.extras.core_hr_mock_factory import create_mock_user, get_mock_photo
from core_hr.models import Resume

fake = faker.Faker()

def get_mock_resume(employee, has_image=True):
    owner = employee
    type = random.choice([x[0] for x in Resume.choices])
    image= None
    if has_image:
        image = get_mock_photo()
    added = fake.date_between(start_date='-5y', end_date='-1d')
    resume = Resume.objects.create(
        owner=owner,
        type=type,
        image=image,
        added=added
    )
    return resume



class ResumeFormTestCase(TestCase):

    def setUp(self):
        self.employee = create_mock_user()
        self.valid_resume = get_mock_resume(self.employee)

