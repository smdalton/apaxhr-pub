from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'core_hr'

urlpatterns = [
    path('', views.CoreHrHome.as_view(), name='self_service'),
    path('documents/', views.DocumentCenter.as_view(), name='document_center'),

    path('documents/passport/view/', views.PassportView.as_view(), name='passport_view'),
    path('documents/passport/update/', views.PassportUpdateCreate.as_view(), name='passport_update'),

    path('documents/ros/view/', views.RosView.as_view(), name='ros_view'),
    path('documents/ros/update/', views.ROSUpdateCreate.as_view(), name='ros_update'),

    path('documents/workpermit/view/', views.WorkPermitView.as_view(), name='work_permit_view'),
    path('documents/workpermit/update/', views.WorkPermitUpdateCreate.as_view(), name='work_permit_update'),

    path('documents/resume/view/', views.ResumeView.as_view(), name='resume_view'),
    path('documents/resume/update/', views.ResumeUpdateCreate.as_view(), name='resume_update'),

    path('documents/certificate/view/', views.TeachingCertificateView.as_view(), name='teach_certificate_view'),
    path('documents/certificate/update/', views.TeachingCertificateUpdateCreate.as_view(), name='teach_certificate_update'),

    path('documents/degree/view/', views.DegreeView.as_view(), name='degree_view'),
    path('documents/degree/update/', views.DegreeUpdateCreate.as_view(), name='degree_update'),

    path('documents/achcert/view/', views.AchievementCertificateView.as_view(), name='ach_cert_view')

]
