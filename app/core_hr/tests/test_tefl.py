from django.test import TestCase

from core_hr.extras.core_hr_mock_factory import create_mock_user

class RosFormTestCase(TestCase):

    def setUp(self):
        self.employee = create_mock_user()