"""apaxhr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views

import os
admin.site.site_header = "APAX Admin"
admin.site.site_title = "APAX Admin Portal"
admin.site.index_title = "APAX HR administrator Portal"

app_name='apaxhr'
# path('employee_management/', include('employee_management.urls')),
urlpatterns = [
    path('', views.HomePage.as_view(),name='home_simple'),
    path('logout/', views.logout_view, name='logout'),
    # path('home/', views.HomePage.as_view(), name='home'),
    path('home/<access_tier>', views.HomePage.as_view(), name='home'),


    path('core_hr/', include('core_hr.urls')),
    path('users/', include('users.urls')),
    path('employee_mgmt/', include('employee_mgmt.urls')),
    path('employment/', include('employment.urls')),
    path('centers/', include('centers.urls')),


    # auth routes
    # path('login/', auth_views.auth_login),
    # path('logout/', auth_views.auth_logout),
    path('admin/', admin.site.urls),

]

# path('employee_management/', include('employee_management.urls')),

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += path('__debug__/', include(debug_toolbar.urls)),


if not settings.USE_S3:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

