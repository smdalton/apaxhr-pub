from datetime import datetime, timedelta

from django.db.models import ImageField
from django.test import TestCase
import faker
from core_hr.models import Passport, RegistryOfStay, WorkPermit, Resume, AchievementCertificate, TeachingCertificate, \
    DegreeDocument
from users.models import Employee
from django_countries.fields import CountryField
from django.contrib.auth import get_user_model
import random
import mock
from django.core.files.uploadedfile import SimpleUploadedFile
import os

fake = faker.Faker()

small_gif = (
    b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
    b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
    b'\x02\x4c\x01\x00\x3b'
)


def get_mock_photo():
    return SimpleUploadedFile('small.gif', small_gif, 'content_type=image/gif')


def create_mock_user():
    User = Employee
    full_name = f"{fake.first_name()} {fake.last_name()} {fake.last_name()}"
    gender = random.choice([x[0] for x in Employee.genders])
    employee_id_number = f"G-{fake.ean8()}"
    employment_status = random.choice(
        [x[0] for x in Employee.lifecycle_statuses])
    employment_status_note = fake.bs()

    phone_number = fake.phone_number()
    email = fake.email()
    personal_email = fake.email()

    date_joined = fake.past_date(start_date="-120d", tzinfo=None)

    user = User.objects.create_user(
        full_name=full_name,
        gender=gender,
        employee_id_number=employee_id_number,
        employment_status=employment_status,
        employment_status_note=employment_status_note,
        phone_number=phone_number,
        personal_email=personal_email,
        date_joined=date_joined,
        email=email,
        password='foo'
    )

    return user


def create_mock_passport(employee, expired=False, has_image=False):
    dob = fake.date_between(start_date="-49y", end_date="-21y")
    date_of_expiration = fake.date_between(start_date="-6m", end_date="+9y")
    place_of_issue = fake.country_code()
    date_of_issue = fake.date_between(start_date="-9y", end_date="-1m")
    owner = Employee.objects.get(pk=employee.pk)
    passport_number = fake.numerify('#########')
    passport = ''
    if expired:
        date_of_expiration = fake.date_between(start_date="-1y", end_date='-1d')
    if has_image:
        photo = get_mock_photo()
        passport = Passport.objects.create(
            owner=owner,
            place_of_issue=place_of_issue,
            issue_date=date_of_issue,
            expiration_date=date_of_expiration,
            dob=dob,
            image=photo,
            passport_number=passport_number,

        )

    else:
        passport = Passport.objects.create(
            owner=owner,
            place_of_issue=place_of_issue,
            issue_date=date_of_issue,
            expiration_date=date_of_expiration,
            passport_number=passport_number,
            dob=dob,
        )

    return passport


def create_mock_ros_form(employee, expired=False, has_image=False):
    employee_address = fake.address()
    landlords_name = fake.name()
    landlords_cell_phone = fake.phone_number()
    landlords_email = fake.email()
    issued = fake.date_between(start_date="-15d", end_date="-1d")
    expiration_date = datetime.now().date() + timedelta(days=180)
    form = ''
    if expired:
        expiration_date = fake.date_between(start_date="-6m", end_date='-1d')
    # Had to split the two save methods only because terribly slow internet connection in vietnam
    # was significantly delaying test and mock object creation
    if has_image:
        photo = get_mock_photo()
        form = RegistryOfStay.objects.create(
            owner=employee,
            employee_address=employee_address,
            landlords_name=landlords_name,
            landlords_cell_phone=landlords_cell_phone,
            landlords_email=landlords_email,
            issue_date=issued,
            expiration_date=expiration_date,
            image=photo
        )
    else:
        form = RegistryOfStay.objects.create(
            owner=employee,
            employee_address=employee_address,
            landlords_name=landlords_name,
            landlords_cell_phone=landlords_cell_phone,
            landlords_email=landlords_email,
            issue_date=issued,
            expiration_date=expiration_date,
        )

    return form


def create_mock_work_permit(employee, type='visa', expired=False, has_image=False):
    date_of_expiration = ''
    if expired == False:
        date_of_expiration = fake.date_between(start_date="+6m", end_date="+2y")
    date_of_issue = fake.date_between(start_date="-9y", end_date="-1m")
    owner = Employee.objects.get(pk=employee.pk)
    if expired == True:
        date_of_expiration = fake.date_between(start_date="-1y", end_date='-1m')
    if has_image:
        photo = get_mock_photo()
        work_permit = WorkPermit.objects.create(
            owner=owner,
            type=random.choice(['wp', 'wp', 'wp', 'vs']),
            issue_date=date_of_issue,
            expiration_date=date_of_expiration,
            image=photo,
        )
    else:
        work_permit = WorkPermit.objects.create(
            owner=owner,
            type=random.choice(['wp', 'wp', 'wp', 'vs']),
            issue_date=date_of_issue,
            expiration_date=date_of_expiration,
        )
    return work_permit


def create_mock_resume(employee):
    try:
        resume = Resume.objects.get(owner=employee)
    except Resume.DoesNotExist:
        resume = Resume.objects.create(
        owner=employee,
        type = random.choice(['rs','cv']),
        image = get_mock_photo(),
    )
    return resume


def create_mock_achievement_certificate(employee):
    try:
        cert = AchievementCertificate.objects.get(owner=employee)
    except AchievementCertificate.DoesNotExist:
        cert = AchievementCertificate.objects.create(
            owner=employee,
            image=get_mock_photo(),
            message_text=fake.paragraphs(nb=4)
        )
    return cert


def create_mock_teaching_certificate(employee):
    try:
        cert = TeachingCertificate.objects.get(owner=employee)
    except TeachingCertificate.DoesNotExist:
        cert=TeachingCertificate.objects.create(
            owner=employee,
            id_number=fake.numerify('###-###-####'),
            type = random.choice(['c','ts','tf','ot']),
            image=get_mock_photo(),
        )
    return cert


def create_mock_degree(employee):
    try:
        degree = DegreeDocument.objects.get(owner=employee)
    except DegreeDocument.DoesNotExist:
        degree =DegreeDocument.objects.create(
            owner=employee,
            image=get_mock_photo(),
        )
    return degree