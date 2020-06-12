import datetime
import json
import os


from django.shortcuts import render

from common.models import User
from common.serializers import CreateUserSerializer
from common.utils import HK_DISTRICT
from companies.models import Company,DocumentFormat,ChargingStage,GeneralRemark
from companies.serializers import SetCompanySerializer, SetDocumentFormatSerializer,SetChargingStageSerializer,SetGeneralRemarkSerializer
from companies.utils import UPPER_CHOICES,MIDDLE_CHOICES,LOWER_CHOICES
from projects.models import Project
from projects.utils import ROOM_TYPE
from projects.serializers import CreateProjectSerializer
from customers.models import Customer
from customers.serializers import SetProjectCustomerSerializer

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

	def post(self,request, *args, **kwargs):

		company=Company.objects.get(owner=request.user)
		return Response(company.as_json())

class GetCompanyLogoView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=Company

	def post(self,request, *args, **kwargs):

		company=Company.objects.get(owner=request.user)
		return Response(company.as_json())

class SetCompanyView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=Company
	serializer_class = SetCompanySerializer

	def post(self, request, *args, **kwargs):
		ret={}
		ret["result"]=True
		#return Response(request.data, status=status.HTTP_201_CREATED)
		data = request.data
		serialized = SetCompanySerializer(data=data,context={'request': request})
		serialized.owner=request.user
		serialized.is_valid(raise_exception=True)
		company=serialized.save()
		company.save()

		return Response(ret, status=status.HTTP_201_CREATED)

#docuemnt format
class GetDocumentFormatChoicesView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]

	def post(self,request, *args, **kwargs):
		ret={}
		ret["result"]=True
		ret["upper_choices"]=[UPPER_CHOICE[0] for UPPER_CHOICE in UPPER_CHOICES]
		ret["middle_choices"]=[MIDDLE_CHOICE[0] for MIDDLE_CHOICE in MIDDLE_CHOICES]
		ret["lower_choices"]=[LOWER_CHOICE[0] for LOWER_CHOICE in LOWER_CHOICES]

		return Response(ret,status=status.HTTP_200_OK)

class SetDocumentFormatView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=DocumentFormat
	serializer_class = SetDocumentFormatSerializer

	def post(self,request, *args, **kwargs):
		ret={}
		ret["result"]=True
		data = request.data
		serialized = SetDocumentFormatSerializer(data=data,context={'request': request})
		serialized.is_valid(raise_exception=True)
		doc_format=serialized.save()
		doc_format.save()

		return Response(ret, status=status.HTTP_200_OK)

class GetDocumentFormatView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=DocumentFormat

	def post(self, request, *args, **kwargs):
		ret={}
		ret["result"]=True
		company=Company.objects.get(owner=request.user)
		doc_format=DocumentFormat.objects.get(company=company)
		ret["doc_format"]=doc_format.as_json()
		return Response(ret, status=status.HTTP_200_OK)

#charging stage
class SetChargingStagesView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	serializer_class = SetChargingStageSerializer

	def post(self,request, *args, **kwargs):
		ret={}
		ret["result"]=True
		data = request.data
		sum_percen=0
		if len(data)<0:
			ret["result"]=False
			ret["reason"]="There must have at least 1 record"
			return Response(ret, status=status.HTTP_400_BAD_REQUEST)
		if len(data)>99:
			ret["result"]=False
			ret["reason"]="Too many records"
			return Response(ret, status=status.HTTP_400_BAD_REQUEST)
		for i in range(len(data)):
			data[i]["index"]=i+1
			sum_percen+=data[i]["percentage"]
		if sum_percen!=100:
			ret["result"]=False
			ret["reason"]="The total percentage is not equal to 100."
			return Response(ret, status=status.HTTP_400_BAD_REQUEST) 
		serialized = SetChargingStageSerializer(data=data,context={'request': request},many=True)
		serialized.is_valid(raise_exception=True)
		charging_stages=serialized.save()
		[charging_stage.save() for charging_stage in charging_stages]
		ChargingStage.objects.filter(index__gt=len(data)).delete()
		return Response(ret, status=status.HTTP_200_OK)

class GetChargingStagesView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=ChargingStage

	def post(self, request, *args, **kwargs):
		ret={}
		ret["result"]=True
		company=Company.objects.get(owner=request.user)
		charging_stages=ChargingStage.objects.filter(company=company).order_by('index')
		ret["charging_stages"]=[charging_stage.as_json() for charging_stage in charging_stages]
		return Response(ret, status=status.HTTP_200_OK)

#general remarks
class SetGeneralRemarksView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	serializer_class = SetGeneralRemarkSerializer

	def post(self,request, *args, **kwargs):
		ret={}
		ret["result"]=True
		data = request.data
		if len(data)>99:
			ret["result"]=False
			ret["reason"]="Too many remarks"
			return Response(ret, status=status.HTTP_400_BAD_REQUEST)
		for i in range(len(data)):
			data[i]["index"]=i+1
		serialized = SetGeneralRemarkSerializer(data=data,context={'request': request},many=True)
		serialized.is_valid(raise_exception=True)
		general_remarks=serialized.save()
		[general_remark.save() for general_remark in general_remarks]
		GeneralRemark.objects.filter(index__gt=len(data)).delete()
		return Response(ret, status=status.HTTP_200_OK)

class GetGeneralRemarksView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=GeneralRemark

	def post(self, request, *args, **kwargs):
		ret={}
		ret["result"]=True
		company=Company.objects.get(owner=request.user)
		general_remarks=GeneralRemark.objects.filter(company=company).order_by('index')
		ret["general_remarks"]=[general_remark.as_json() for general_remark in general_remarks]
		return Response(ret, status=status.HTTP_200_OK)

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

class CreateProjectView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=Project
	serializer_class=CreateProjectSerializer

	def post(self,request,*args, **kwargs):
		ret={}
		ret["result"]=True
		data = request.data
		serialized=CreateProjectSerializer(data=data,context={'request':request})
		serialized.is_valid(raise_exception=True)
		project=serialized.save()
		ret["project_id"]=project.id
		return Response(ret,status=status.HTTP_200_OK)

class SetProjectCustomerView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=Customer
	serializer_class=SetProjectCustomerSerializer

	def post(self,request,*args, **kwargs):
		ret={}
		ret["result"]=True
		data = request.data
		serialized=SetProjectCustomerSerializer(data=data,context={'request':request})
		serialized.is_valid(raise_exception=True)
		customer=serialized.save()
		return Response(ret,status=status.HTTP_200_OK)


#district

class GetDistrictListView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]

	def post(self,request, *args, **kwargs):
		ret={}
		ret['result']=True
		districts=HK_DISTRICT
		ret["districts"]=districts
		return Response(ret, status=status.HTTP_200_OK)

#room
class GetRoomTypeListView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]

	def post(self,request, *args, **kwargs):
		ret={}
		ret['result']=True
		room_types=ROOM_TYPE
		ret["room_types"]=room_types
		return Response(ret, status=status.HTTP_200_OK)

class CreateRoomView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]

	def post(self, request, *args, **kwargs):
		ret={}
		ret['result']=True
		return Response(ret,status=status.HTTP_200_OK)
