import datetime
import json
import os

from django.shortcuts import render

from common.models import User
from common.serializers import CreateUserSerializer
from companies.models import Company
from projects.models import Project

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
from rest_framework_simplejwt.tokens import SlidingToken
from rest_framework_simplejwt.models import TokenUser
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
		data = request.data
		serialized = CreateUserSerializer(data=data)
		serialized.is_valid(raise_exception=True)
		user=serialized.save()
		user.verify_code="000000"
		user.save()
		#user=User.objects.create_user(phone="request")
		return Response(ret, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
	permission_classes = [AllowAny]

	def post(self, request, *args, **kwargs):
		ret={}
		ret["result"]=True
		data = request.data

		user=User.objects.filter(phone=data.get("phone")).first()
		matchcheck= check_password(data.get("password"), user.password)
		if matchcheck:
			'''cur_tokens=OutstandingToken.objects.filter(user=user)
			for cur_token in cur_tokens.all():
				cur_token.expires_at=datetime.datetime.now()
				#cur_token.blacklist()
				cur_token.save()'''
			sliding = SlidingToken.for_user(user)
			ret["token"]=str(sliding)
			ret["type"]=str(type(sliding))
			ret["data"]=request.data
			if not user.phone_verify:
				ret["need_verify"]=True
			return Response(ret, status=status.HTTP_200_OK)

class UserPhoneVerifyView(APIView):
	authentication_classes = [authentication.JWTAuthentication]
	permission_classes = [IsAuthenticated]

	def post(self, request, *args, **kwargs):
		ret={}
		ret["result"]=True
		data = request.data
		user=request.user
		if user.phone_verify:
			ret["result"]=False
			ret["reason"]="Already Verified"
			return Response(ret, status=status.HTTP_406_NOT_ACCEPTABLE)
		if user.verify_code==data.get("verify_code") and user.verify_code.replace(" ", "")!="" and user.verify_code!=None:
			user.phone_verify=True
			user.save()
			return Response(ret, status=status.HTTP_200_OK)
		else:
			ret["result"]=False
			ret["reason"]="Wrong Verifiy Code"
			return Response(ret, status=status.HTTP_400_BAD_REQUEST)

#company
class GetCompanyView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=Company

class CreateCompanyView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=Company
	serializer_class = CreateUserSerializer

#project

class GetProjectListView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=Project

	def post(self, request, *args, **kwargs):
		ret={}
		ret["result"]=True
		projects=Project.objects.filter()
		ret["projects"]=[project.as_json() for project in projects]
		return Response(ret, status=status.HTTP_200_OK)
