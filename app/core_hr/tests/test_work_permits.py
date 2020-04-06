from datetime import datetime

from django.test import TestCase
import faker
import random
from core_hr.models import WorkPermit
from users.models import Employee
from core_hr.extras.core_hr_mock_factory import create_mock_user, create_mock_work_permit
fake = faker.Faker()




class RosFormTestCase(TestCase):

    def setUp(self):
        self.employee = create_mock_user()
        self.work_permit = create_mock_work_permit(self.employee)

    def test_work_permit_saves_and_retrieves(self):
        retrieved_work_permit = WorkPermit.objects.get(id=self.work_permit.pk)
        self.assertEqual(self.work_permit, retrieved_work_permit)

    def test_valid_work_permit_is_not_expired(self):
        valid_work_permit = create_mock_work_permit(create_mock_user(), expired=False, has_image=False)
        self.assertEqual(valid_work_permit.expired, False, valid_work_permit.expired)
        self.assertTrue(valid_work_permit.expiration_date > datetime.now().date(),(
            'exp. date',valid_work_permit.expiration_date.isoformat(),
            'curr date', datetime.now().date().isoformat())
                        )

    def test_expired_work_permit_is_expired(self):
        expired_work_permit = create_mock_work_permit(create_mock_user(), expired=True)
        self.assertEqual(expired_work_permit.expired, True,(
            'exp. date',expired_work_permit.expiration_date.isoformat(),
            'curr date', datetime.now().date().isoformat())
                         )
        self.assertTrue(expired_work_permit.expiration_date < datetime.now().date())

    def test_work_permit_data_complete(self):
        complete_work_permit = create_mock_work_permit(employee=create_mock_user(), expired=False, has_image=True)
        self.assertEqual(complete_work_permit.data_complete, True)

    def test_work_permit_data_not_complete(self):
        incomplete_work_permit = create_mock_work_permit(create_mock_user(), has_image=False)
        self.assertEqual(incomplete_work_permit.data_complete, False)

#