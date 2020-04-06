from datetime import datetime

from django.test import TestCase, LiveServerTestCase
import faker
from core_hr.models import Passport
from core_hr.extras.core_hr_mock_factory import create_mock_passport

#http://giflib.sourceforge.net/whatsinagif/bits_and_bytes.html
fake = faker.Faker()
from core_hr.extras.core_hr_mock_factory import create_mock_user, get_mock_photo






class PassportTestCase(TestCase):

    def setUp(self):
        self.employee = create_mock_user()
        self.passport = create_mock_passport(self.employee)

    def test_passport_saves_and_retrieves(self):
        retrieved_passport = Passport.objects.get(id=self.passport.pk)
        self.assertEqual(self.passport, retrieved_passport)

    def test_valid_passport_is_not_expired(self):
        valid_passport = create_mock_passport(create_mock_user())
        self.assertEqual(valid_passport.expired, False)
        self.assertTrue(valid_passport.expiration_date > datetime.now().date())

    def test_expired_passport_is_expired(self):
        expired_passport = create_mock_passport(create_mock_user(), expired=True)
        self.assertEqual(expired_passport.expired, True)
        self.assertTrue(expired_passport.expiration_date < datetime.now().date())

    def test_passport_data_complete(self):
        complete_passport = create_mock_passport(create_mock_user(), has_image=True)

        self.assertEqual(complete_passport.data_complete, True)

    def test_passport_data_not_complete(self):
        incomplete_passport = create_mock_passport(create_mock_user())
        self.assertEqual(incomplete_passport.data_complete, False)



    #
    #
    # def test_passport_expiring_soon(self):
    #     self.fail('ensure the passport is not expiring within the next month')
    #
    # def test_passport_expired(self):
    #     self.fail('create several passports and an expired passport and check for expired passports')
    #
    # def test_user_exists(self):
    #     self.fail('Make an employee test case')

    # def test_employee_exists(self):
