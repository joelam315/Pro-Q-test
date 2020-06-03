from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views
from django.conf.urls import url
from django.urls import include, path
from common.views import handler404, handler500
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib import admin
from rest_framework_simplejwt.views import (
    TokenVerifyView,
)

from api.views import (
	UserRegisterView,
	UserLoginView,
)

app_name = 'api'

urlpatterns = [
	path('register/',UserRegisterView.as_view(),name='user_register'),
	path('login/',UserLoginView.as_view(),name='user_login'),
]
