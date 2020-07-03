import datetime
import json
import os


from django.shortcuts import render

from common.models import User
from common.serializers import CreateUserSerializer,LoginSerializer, PhoneVerifySerializer
from common.utils import HK_DISTRICT
from companies.models import Company,DocumentFormat,ChargingStages,GeneralRemark
from companies.serializers import (
	SetCompanySerializer, 
	CompanySerializer, 
	SetDocumentFormatSerializer,
	SetChargingStagesSerializer,
	SetGeneralRemarkSerializer,
	DocumentFormatSerializer,
	ChargingStagesSerializer,
	GeneralRemarkSerializer
)
from companies.utils import UPPER_CHOICES,MIDDLE_CHOICES,LOWER_CHOICES
from projects.models import Project
from projects.utils import ROOM_TYPE
from projects.serializers import CreateProjectSerializer
from rooms.models import Room, RoomType, RoomItem
from rooms.serializers import (
	CreateRoomSerializer,
	UpdateRoomSerializer,
	SetRoomItemSerializer,
	PreCalRoomItemFormulaSerializer
)
from customers.models import Customer
from customers.serializers import SetProjectCustomerSerializer
from project_items.models import ItemType,ItemFormula,ItemTypeMaterial,ProjectMisc
from project_items.serializers import SetProjectMiscSerializer

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
from rest_framework_simplejwt.models import TokenUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import status
from rest_framework import serializers

from django.views.generic import (CreateView, DeleteView, DetailView,
    TemplateView, UpdateView, View)

token_param=openapi.Parameter(name='Authorization',in_=openapi.IN_HEADER,description="Bearer token required", type=openapi.TYPE_STRING)

default_param = openapi.Parameter(name='result', in_=openapi.IN_BODY,description="Return True if there is no internal error", type=openapi.TYPE_BOOLEAN)

#User

class UserRegisterView(APIView):
	model = User
	permission_classes = [AllowAny]
	serializer_class = CreateUserSerializer

	@swagger_auto_schema(
		operation_description="Register a new user", 
		security=None,
		request_body=CreateUserSerializer,
		responses={
			status.HTTP_201_CREATED: "{\n&emsp;result: boolean,\n&emsp;access: string,\n&emsp;refresh:string\n}",
			status.HTTP_400_BAD_REQUEST: "Validation Error"
		}
	)
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
		token = RefreshToken.for_user(user)
		ret["refresh"]=str(token)
		ret["access"]=str(token.access_token)
		#user=User.objects.create_user(phone="request")
		return Response(ret, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
	permission_classes = [AllowAny]

	@swagger_auto_schema(
		operation_description="User login", 
		security=[{'Basic': []}],
		request_body=LoginSerializer,
		responses={
			status.HTTP_200_OK: "{\n&emsp;result: boolean,\n&emsp;access: string,\n&emsp;refresh:string\n}",
			status.HTTP_400_BAD_REQUEST: "Validation Error"
		}
	)
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
			token = RefreshToken.for_user(user)
			ret["refresh"]=str(token)
			ret["access"]=str(token.access_token)
			if not user.phone_verify:
				ret["result"]=False
				ret["reason"]="Need verify phone first."
				raise serializers.ValidationError(ret)
			return Response(ret, status=status.HTTP_200_OK)

class UserPhoneVerifyView(APIView):
	authentication_classes = [authentication.JWTAuthentication]
	permission_classes = [IsAuthenticated]

	@swagger_auto_schema(
		operation_description="Verify phone number for new user", 
		security=[{'Bearer': []}],
		manual_parameters=[token_param],
		request_body=PhoneVerifySerializer,
		responses={
			status.HTTP_200_OK: "{\n&emsp;result: boolean\n}",
			status.HTTP_400_BAD_REQUEST: "Validation Error"
		}
	)
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

	@swagger_auto_schema(
		operation_description="Get user's company \n<b>* the returned value 'logo' is a path to the image resource</b>", 
		security=[{'Bearer': []}],
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: CompanySerializer,
			status.HTTP_400_BAD_REQUEST: "Validation Error"
		}
	)
	def post(self,request, *args, **kwargs):

		company=Company.objects.get(owner=request.user)
		return Response(company.as_json())

'''
class GetCompanyLogoView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=Company

	def post(self,request, *args, **kwargs):

		company=Company.objects.get(owner=request.user)
		return Response(company.as_json())
'''

class SetCompanyView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=Company
	serializer_class = SetCompanySerializer

	@swagger_auto_schema(
		operation_description="Create/update user's company info.", 
		security=[{'Bearer': []}],
		request_body=SetCompanySerializer,
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: "{\n&emsp;result: boolean\n}",
			status.HTTP_400_BAD_REQUEST: "Validation Error"
		}
	)
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

		return Response(ret, status=status.HTTP_200_OK)

#docuemnt format
class GetDocumentFormatChoicesView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	@swagger_auto_schema(
		operation_description="Get all docuemnt format choices.", 
		security=[{'Bearer': []}],
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: "{\n&emsp;upper_choice: array[string],\n&emsp;middle_choice: array[string],\n&emsp;lower_choice: array[string],\n}",
			status.HTTP_400_BAD_REQUEST: "Validation Error"
		}
	)
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

	@swagger_auto_schema(
		operation_description="Create/update user's company docuemnt format.", 
		security=[{'Bearer': []}],
		request_body=SetDocumentFormatSerializer,
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: "{\n&emsp;result: boolean\n}",
			status.HTTP_400_BAD_REQUEST: "Validation Error"
		}
	)
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

	@swagger_auto_schema(
		operation_description="Get user's company docuemnt format.", 
		security=[{'Bearer': []}],
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: DocumentFormatSerializer,
			status.HTTP_400_BAD_REQUEST: "Validation Error"
		}
	)
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
	serializer_class = SetChargingStagesSerializer

	@swagger_auto_schema(
		operation_description="Create/update user's company charging stage(s).", 
		security=[{'Bearer': []}],
		request_body=SetChargingStagesSerializer(many=True),
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: "{\n&emsp;result: boolean\n}",
			status.HTTP_400_BAD_REQUEST: "Validation Error"
		}
	)
	def post(self,request, *args, **kwargs):
		ret={}
		ret["result"]=True
		data = request.data
		sum_percen=0

		for i in range(data.get("quantity")):
			sum_percen+=data["values"][i]
		if sum_percen!=100:
			ret["result"]=False
			ret["reason"]="The total percentage is not equal to 100."
			raise serializers.ValidationError(ret)
		serialized = SetChargingStagesSerializer(data=data,context={'request': request})
		serialized.is_valid(raise_exception=True)
		charging_stages=serialized.save()
		return Response(ret, status=status.HTTP_200_OK)

class GetChargingStagesView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=ChargingStages

	@swagger_auto_schema(
		operation_description="Get user's company charging stages.", 
		security=[{'Bearer': []}],
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: ChargingStagesSerializer(many=True),
			status.HTTP_400_BAD_REQUEST: "Validation Error"
		}
	)
	def post(self, request, *args, **kwargs):
		ret={}
		ret["result"]=True
		company=Company.objects.get(owner=request.user)
		charging_stages=ChargingStages.objects.get(company=company)
		ret["charging_stages"]=charging_stages.as_json()
		return Response(ret, status=status.HTTP_200_OK)

#general remarks
class SetGeneralRemarksView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	serializer_class = SetGeneralRemarkSerializer

	@swagger_auto_schema(
		operation_description="Create/update user's company general remark.", 
		security=[{'Bearer': []}],
		request_body=SetGeneralRemarkSerializer,
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: "{\n&emsp;result: boolean\n}",
			status.HTTP_400_BAD_REQUEST: "Validation Error"
		}
	)
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

	@swagger_auto_schema(
		operation_description="Get user's company general remarks.", 
		security=[{'Bearer': []}],
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: GeneralRemarkSerializer(many=True),
			status.HTTP_400_BAD_REQUEST: "Validation Error"
		}
	)
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

class GetProjectView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=Project

	def post(self,request,*args,**kwargs):
		ret={}
		ret["result"]=True
		data = request.data
		project=Project.objects.get(id=data.get("id"))
	
#project-customer
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

#project-room

class CreateProjectRoomView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=Room
	serializer_class=CreateRoomSerializer

	def post(self, request, *args, **kwargs):
		ret={}
		ret['result']=True
		data=request.data
		serialized=CreateRoomSerializer(data=data,context={'request':request})
		serialized.is_valid(raise_exception=True)
		room=serialized.save()
		ret["room_id"]=room.id
		return Response(ret,status=status.HTTP_200_OK)

class UpdateProjectRoomView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=Room
	serializer_class=UpdateRoomSerializer

	def post(self, request, *args, **kwargs):
		ret={}
		ret['result']=True
		data=request.data
		serialized=UpdateRoomSerializer(instance=data.get("id"),data=data,context={'request':request})
		serialized.is_valid(raise_exception=True)
		room=serialized.save()

		return Response(ret,status=status.HTTP_200_OK)

class RemoveProjectRoomView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=Room

	def post(self,request,*args,**kwargs):
		ret={}
		ret['result']=True
		data=request.data
		room=get_object_or_404(Room, id=data.get("id"))
		if room.related_project.company.owner==request.user:
			room.delete()
			return Response(ret, status=status.HTTP_200_OK)
		else:
			raise PermissionDenied

class GetProjectRoomListView(APIView):
	permission_classes=[IsAuthenticated]
	authentication_classes=[authentication.JWTAuthentication]
	model=Room

	def post(self, request, *args, **kwargs):
		ret={}
		ret["result"]=True
		data=request.data
		project=Project.objects.get(id=data["project_id"])
		ret["rooms"]=[room.as_json() for room in project.project_rooms.all()]
		return Response(ret, status=status.HTTP_200_OK)		

class GetProjectRoomDetailsView(APIView):
	permission_classes=[IsAuthenticated]
	authentication_classes=[authentication.JWTAuthentication]
	model=Room

	def post(self, request, *args, **kwargs):
		ret={}
		ret["result"]=True
		data=request.data
		room=Room.objects.get(id=data["room_id"])
		ret["room"]=room.details()
		return Response(ret, status=status.HTTP_200_OK)		

#project-room-item
class GetProjectAllRoomItemView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=RoomItem

	def post(self, request, *args, **kwargs):
		ret={}
		ret["result"]=True
		data=request.data
		project=Project.objects.get(id=data["project_id"])
		if project.company.owner!=request.user:
			raise PermissionDenied
		rooms=project.project_rooms.all()
		items={}
		for room in rooms:
			items[room.name]=[]
			for item in room.room_project_items.all():
				items[room.name].append(item.as_json())


		ret["items"]=items
		return Response(ret,status=status.HTTP_200_OK)


class SetProjectRoomItemView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=RoomItem
	serializer_class=SetRoomItemSerializer

	def post(self, request, *args, **kwargs):
		ret={}
		ret["result"]=True
		data=request.data
		serialized=SetRoomItemSerializer(data=data,context={'request':request})
		serialized.is_valid(raise_exception=True)
		room_item=serialized.save()
		ret["room_item_id"]=room_item.id
		return Response(ret,status=status.HTTP_200_OK)

class PreCalProjectRoomItemFormulaView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=RoomItem
	serializer_class=PreCalRoomItemFormulaSerializer

	def post(self,request, *args, **kwargs):
		ret={}
		ret["result"]=True
		data=request.data
		serialized=PreCalRoomItemFormulaSerializer(data=data,context={'request':request})
		serialized.is_valid(raise_exception=True)
		result=serialized.save()
		ret.update(result)
		return Response(ret,status=status.HTTP_200_OK)


#project-misc
class SetProjectMiscView(APIView):
	permission_classes=[IsAuthenticated]
	authentication_classes=[authentication.JWTAuthentication]
	model=ProjectMisc
	serializer_class=SetProjectMiscSerializer

	def post(self,request,*args, **kwargs):
		ret={}
		ret["result"]=True
		data=request.data
		serialized=SetProjectMiscSerializer(data=data,context={'request':request})
		serialized=is_valid(raise_exception=True)
		project_misc=serialized.save()
		ret["project_misc_id"]=project_misc.id
		return Response(ret,status=status.HTTP_200_OK)

class GetAllProjectMiscView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=ProjectMisc

	def post(self, request, *args, **kwargs):
		ret={}
		ret["result"]=True
		data=request.data
		project=Project.objects.get(id=data["project_id"])
		if project.company.owner!=request.user:
			raise PermissionDenied
		ret["project_misc"]=[project_misc.as_json() for project_misc in project.project_misc.all()]
		
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
		room_types=[rt.as_json() for rt in RoomType.objects.filter(is_active=True).all()]
		ret["room_types"]=room_types
		return Response(ret, status=status.HTTP_200_OK)

#room - item
class GetRoomRelatedItemListView(APIView):
	permission_classes=[IsAuthenticated]
	authentication_classes=[authentication.JWTAuthentication]

	def post(self,request,*args,**kwargs):
		ret={}
		ret['result']=True
		data=request.data
		room_type=RoomType.objects.get(id=data["room_type"])
		related_items=room_type.related_items
		ret["related_items"]=[ri.as_json() for ri in related_items.all()]
		return Response(ret,status=status.HTTP_200_OK)

#item
class GetItemMaterials(APIView):
	permission_classes=[IsAuthenticated]
	authentication_classes=[authentication.JWTAuthentication]
	model=ItemTypeMaterial

	def post(self,request,*args,**kwargs):
		ret={}
		ret['result']=True
		data=request.data
		if data.get("item_type"):
			ret["materials"]=[itm.as_json() for itm in ItemTypeMaterial.objects.filter(item_type=data.get("item_type"))]
			return Response(ret,status=status.HTTP_200_OK)
		else:
			raise serializers.ValidationError("Missing item_type.")
