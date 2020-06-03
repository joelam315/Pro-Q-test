import datetime
import json
import os

from django.shortcuts import render

from common.models import User
from common.serializers import CreateUserSerializer

from rest_framework.authentication import SessionAuthentication, BasicAuthentication 
from rest_framework_simplejwt import authentication
from rest_framework.permissions import (IsAuthenticated,AllowAny,)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from phonenumber_field.phonenumber import PhoneNumber, to_python
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from sorl.thumbnail import get_thumbnail
from django.core.files.base import ContentFile
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.views.generic import (CreateView, DeleteView, DetailView,
    TemplateView, UpdateView, View)

#User

class UserRegisterView(APIView):
	model = User
	permission_classes = [AllowAny]
	serializer_class = CreateUserSerializer

	def post(self, request, *args, **kwargs):
		ret={}
		ret["result"]=True
		#return Response(request.data, status=status.HTTP_201_CREATED)
		data = json.loads(request.body)
		serialized = CreateUserSerializer(data=request.data)
		serialized.is_valid(raise_exception=True)
		serialized.save()
		#user=User.objects.create_user(phone="request")
		return Response(ret, status=status.HTTP_201_CREATED)


class UserLoginView(TemplateView):

	def post(self, request, *args, **kwargs):
		ret={}
		ret["result"]=True
		data = json.loads(request.body)

		user=User.objects.filter(phone=data.get("phone")).first()
		matchcheck= check_password(data.get("password"), user.password)
		if matchcheck:
			refresh = RefreshToken.for_user(user)
			ret["token"]=str(refresh.access_token)
			return Response(ret)


