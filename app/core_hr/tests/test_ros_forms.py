import faker
from django.core.files.uploadedfile import SimpleUploadedFile

from core_hr.models import RegistryOfStay
from django.test import TestCase
from datetime import datetime
from core_hr.extras.core_hr_mock_factory import create_mock_user, create_mock_ros_form
from django.utils.timezone import  timedelta

#http://giflib.sourceforge.net/whatsinagif/bits_and_bytes.html

fake = faker.Faker()




class RosFormTestCase(TestCase):


    def setUp(self):
        self.employee = create_mock_user()
        self.ros_form = create_mock_ros_form(self.employee)

    def test_ros_form_saves_and_retrieves(self):
        retrieved_ros_form = RegistryOfStay.objects.get(id=self.ros_form.pk)
        self.assertEqual(self.ros_form, retrieved_ros_form)

    def test_ros_form_is_not_expired(self):
        valid_ros_form = create_mock_ros_form(employee=create_mock_user(), has_image=False)
        self.assertEqual(valid_ros_form.expired, False)
        self.assertTrue(valid_ros_form.expiration_date > datetime.now().date())

    def test_ros_form_is_expired(self):
        expired_ros_form = create_mock_ros_form(employee=create_mock_user(), expired=True)
        self.assertEqual(expired_ros_form.expired, True)
        self.assertTrue(expired_ros_form.expiration_date < datetime.now().date())

    def test_ros_form_data_complete(self):
        complete_ros_form = create_mock_ros_form(employee=create_mock_user(), has_image=True)
        self.assertEqual(complete_ros_form.data_complete, True)

    def test_ros_form_data_not_complete(self):
        incomplete_ros_form = create_mock_ros_form(employee=create_mock_user(), has_image=False)
        self.assertEqual(incomplete_ros_form.data_complete, False)