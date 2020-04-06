from django.contrib.admin.sites import AdminSite
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import TestCase
from django.test import RequestFactory
import core_hr.models
# https://www.argpar.se/posts/programming/testing-django-admin/

class MockSuperUser:
    def has_perm(self, perm):
        return True

request_factory = RequestFactory()
request = request_factory.get('/admin')
request.user = MockSuperUser()

class PassportAdminTest(TestCase):

    def setUp(self):
        site = AdminSite()
        #self.admin = MyAdmin(MyModel, site)