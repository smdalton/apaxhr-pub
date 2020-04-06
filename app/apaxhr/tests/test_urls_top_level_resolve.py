from django.test import SimpleTestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser, User
from django.urls import resolve


import apaxhr.views
import core_hr.views
import employee_mgmt.views
import employment.views
import users.views



class BaseLandingUrlsResolve(SimpleTestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func.view_class, apaxhr.views.HomePage)

    def test_core_hr_landing_resolves_to_view(self):
        found = resolve('/core_hr/')
        self.assertEqual(found.func.view_class, core_hr.views.CoreHrHome)

    def test_employee_mgmt_resolves_to_view(self):
        found = resolve('/employee_mgmt/')
        self.assertEqual(found.func.view_class, employee_mgmt.views.EmployeeManagementHome)

    def test_lifecycle_landing_resolves_to_view(self):
        found = resolve('/employment/')
        self.assertEqual(found.func.view_class, employment.views.LifeCycleHome)

    def test_users_resolves_to_view(self):
        found = resolve('/users/')
        self.assertEqual(found.func.view_class, users.views.UsersHome)

#
# class CoreHRUrlsResolve(TestCase):
#
#     def test_core_hr_landing_resolves_to_view(self):
#         pass
#
#     def test_core_hr_landing_resolves_to_view(self):
#         pass
#
#     def test_core_hr_landing_resolves_to_view(self):
#         pass
#
#     def test_core_hr_landing_resolves_to_view(self):
#         pass
#
#     def test_core_hr_landing_resolves_to_view(self):
#         pass
#
#     def test_core_hr_landing_resolves_to_view(self):
#         pass
#
#     def test_core_hr_landing_resolves_to_view(self):
#         pass
#
#     def test_core_hr_landing_resolves_to_view(self):
#         pass
#
#

