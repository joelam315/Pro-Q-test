import datetime
import json
import os
import pdfkit


from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.template.loader import render_to_string
from django.http.response import HttpResponse, JsonResponse
from django.conf import settings
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist, ValidationError

from common.models import User
from common.serializers import (
	CreateOrGetUserSerializer,
	LoginSerializer, 
	PhoneVerifySerializer,
	CommonTrueResponseSerializer,
	CommonFalseResponseSerializer,
	ListDistrictResponseSerializer,
	LoginResponseSerializer,
	RegisterResponseSerializer,
	PhoneVerifySuccessResponseSerializer,
)
from common.utils import HK_DISTRICT
from companies.models import Company,DocumentFormat,DocumentHeaderInformation,ChargingStages,QuotationGeneralRemark,InvoiceGeneralRemark,ReceiptGeneralRemark
from companies.serializers import (
	SetCompanySerializer, 
	CompanySerializer, 
	SetDocumentFormatSerializer,
	SetDocumentHeaderInformationSerializer,
	SetChargingStagesSerializer,
	SetQuotationGeneralRemarkSerializer,
	SetInvoiceGeneralRemarkSerializer,
	SetReceiptGeneralRemarkSerializer,
	DocumentFormatSerializer,
	DocumentHeaderInformationSerializer,
	ChargingStagesSerializer,
	QuotationGeneralRemarkSerializer,
	InvoiceGeneralRemarkSerializer,
	ReceiptGeneralRemarkSerializer,
	GetDocumentHeaderInformationResponseSerializer,
	GetChargingStagesResponseSerializer,
	GetCompanyResponseSerializer,
	GetDocumentFormatResponseSerializer,
	GetDocumentFormatChoiceResponseSerializer,
	GetGeneralRemarksSerializer
)
from companies.utils import UPPER_CHOICES,MIDDLE_CHOICES,LOWER_CHOICES
from projects.models import Project, ProjectInvoice, ProjectReceipt
from projects.utils import ROOM_TYPE
from projects.serializers import (
	CreateProjectSerializer, 
	UpdateProjectSerializer,
	GetProjectRequestSerializer,
	GetProjectResponseSerializer,
	ProjectQutationPreviewResponseSerializer,
	ProjectInvoicePreviewResponseSerializer,
	ProjectReceiptPreviewResponseSerializer,
	ListProjectResponseSerializer,
	GetProjectWithChargingStageRequestSerializer,
	GetProjectAllItemResponseSerializer,
	GetProjectAllRoomItemResponseSerializer,
	GetProjectProfitAnalysisResponseSerializer

)
from rooms.models import Room, RoomType, RoomItem
from rooms.serializers import (
	CreateRoomSerializer,
	UpdateRoomSerializer,
	SetRoomItemSerializer,
	PreCalRoomItemFormulaSerializer,
	CreateRoomResponseSerializer,
	GetRoomRequestSerializer,
	GetProjectRoomListResponseSerializer,
	GetProjectRoomDetailsResponseSerializer,
	PreCalProjectRoomItemFormulaResponseSerializer,
	SetProjectRoomItemResponseSerializer,
	GetRoomTypeListResponseSerializer,
	GetRoomRelatedItemResponseSerializer,
	GetRoomItemRequestSerializer
)
from customers.models import Customer
from customers.serializers import SetProjectCustomerSerializer
from project_items.models import ItemType,ItemFormula,ItemTypeMaterial
from project_items.serializers import (
	GetItemMaterialsRequestSerializer,
	GetItemMaterialsResponseSerializer
)
from project_misc.models import ProjectMisc,Misc
from project_misc.serializers import (
	SetProjectMiscSerializer,
	SetProjectMiscResponseSerializer,
	GetAllProjectMiscResponseSerializer,
	GetProjectMiscRequestSerializer,
	GetMiscListResponseSerializer
)

from project_timetable.models import ProjectWork, ProjectMilestone
from project_timetable.serializers import (
	CreateProjectWorkSerializer,
	UpdateProjectWorkSerializer,
	CreateProjectMilestoneSerializer,
	UpdateProjectMilestoneSerializer,
	CreateProjectWorkResponseSerializer,
	CreateProjectMilestoneResponseSerializer,
	GetProjectWorkRequestSerializer,
	GetProjectMilestoneRequestSerializer

)

from project_expenses.models import (
	ExpenseType,
	ProjectExpense
)
from project_expenses.serializers import (
	GetExpenseTypeListResponseSerializer,
	CreateProjectExpenseSerializer,
	UpdateProjectExpenseSerializer,
	GetProjectExpenseRequestSerializer
)

from api.renderers import APIRenderer

from rest_framework.authentication import SessionAuthentication, BasicAuthentication 
from rest_framework_simplejwt import authentication
from rest_framework.permissions import (IsAuthenticated,AllowAny,)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
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

default_param = openapi.Response(name='result', in_=openapi.IN_BODY,description="Return True if there is no internal error", type=openapi.TYPE_BOOLEAN)





#User

class UserRegisterOrLoginView(APIView):
	model = User
	permission_classes = [AllowAny]
	serializer_class = CreateOrGetUserSerializer
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Register a new user or login", 
		security=None,
		request_body=CreateOrGetUserSerializer,
		responses={
			status.HTTP_200_OK: LoginResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer()
		}
	)
	def post(self, request, *args, **kwargs):
		ret={}
		ret["result"]=True
		#return Response(request.data, status=status.HTTP_201_CREATED)
		data = request.data
		check_user=User.objects.filter(username=data["phone"])
		if check_user.exists():
			serialized = CreateOrGetUserSerializer(instance=check_user.first(),data=data)
		else:
			serialized = CreateOrGetUserSerializer(data=data)
		serialized.is_valid(raise_exception=True)
		user=serialized.save()
		ret["login_token"]=user.login_token
		#token = RefreshToken.for_user(user)
		#ret["refresh"]=str(token)
		#ret["access"]=str(token.access_token)
		#user=User.objects.create_user(phone="request")
		return Response(ret, status=status.HTTP_200_OK)

'''class UserRegisterView(APIView):
	model = User
	permission_classes = [AllowAny]
	serializer_class = CreateUserSerializer
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Register a new user", 
		security=None,
		request_body=CreateUserSerializer,
		responses={
			status.HTTP_201_CREATED: RegisterResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer()
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
		return Response(ret, status=status.HTTP_201_CREATED)'''


'''class UserLoginView(APIView):
	permission_classes = [AllowAny]
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="User login", 
		security=[{'Basic': []}],
		request_body=LoginSerializer,
		responses={
			status.HTTP_200_OK: LoginResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer()
		}
	)
	def post(self, request, *args, **kwargs):
		ret={}
		ret["result"]=True
		data = request.data

		user=User.objects.filter(phone=data.get("phone")).first()
		matchcheck=(data.get("otp")==user.verify_code)
		#matchcheck= check_password(data.get("password"), user.password)
		if matchcheck:
'''			

'''			cur_tokens=OutstandingToken.objects.filter(user=user)
			for cur_token in cur_tokens.all():
				cur_token.expires_at=datetime.datetime.now()
				#cur_token.blacklist()
				cur_token.save()
'''
'''			token = RefreshToken.for_user(user)
			ret["refresh"]=str(token)
			ret["access"]=str(token.access_token)
			if not user.phone_verify:
				ret["result"]=False
				ret["reason"]="Need verify phone first."
				raise serializers.ValidationError(ret)
			return Response(ret, status=status.HTTP_200_OK)'''

class UserPhoneVerifyView(APIView):
	#authentication_classes = [authentication.JWTAuthentication]
	permission_classes = [AllowAny]
	#permission_classes = [IsAuthenticated]
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Verify phone number for new user", 
		request_body=PhoneVerifySerializer,
		responses={
			status.HTTP_200_OK: PhoneVerifySuccessResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer()
		}
	)
	def post(self, request, *args, **kwargs):
		ret={}
		ret["result"]=True
		data = request.data
		user=User.objects.get(username=data["phone"])
		if not user.need_login_verify:
			ret["result"]=False
			ret["reason"]="Please login first"
			return Response(ret, status=status.HTTP_406_NOT_ACCEPTABLE)
		if user.login_token!=data["login_token"]:
			ret["result"]=False
			ret["reason"]="Invalid login token"
			return Response(ret, status=status.HTTP_406_NOT_ACCEPTABLE)
		if user.verify_code==data.get("otp") and user.verify_code.replace(" ", "")!="" and user.verify_code!=None:
			user.phone_verify=True
			user.need_login_verify=False
			user.save()
			if Company.objects.filter(owner=user).exists():
				ret["need_company_setup"]=False
			else:
				ret["need_company_setup"]=True
			token = RefreshToken.for_user(user)
			ret["refresh"]=str(token)
			ret["access"]=str(token.access_token)
			return Response(ret, status=status.HTTP_200_OK)
		else:
			ret["result"]=False
			ret["reason"]="Wrong OTP"
			return Response(ret, status=status.HTTP_400_BAD_REQUEST)

#company
class GetCompanyView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=Company
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Get user's company \n<b>* the returned value 'logo' is a path to the image resource</b>", 
		security=[{'Bearer': []}],
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: GetCompanyResponseSerializer,
			status.HTTP_404_NOT_FOUND: CommonFalseResponseSerializer 
		}
	)
	def post(self,request, *args, **kwargs):
		ret={}
		try:
			company=Company.objects.get(owner=request.user)
		except ObjectDoesNotExist:
			ret["result"]=False
			ret["reason"]="Please create company first."
			return Response(ret, status=status.HTTP_404_NOT_FOUND)
		ret["result"]=True
		ret["company"]=company.as_json()
		return Response(ret,status=status.HTTP_200_OK)

'''
class GetCompanyLogoView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=Company
	renderer_classes=[APIRenderer]

	def post(self,request, *args, **kwargs):

		company=Company.objects.get(owner=request.user)
		return Response(company.as_json())
'''

class SetCompanyView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=Company
	serializer_class = SetCompanySerializer
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Create/update user's company info.", 
		security=[{'Bearer': []}],
		request_body=SetCompanySerializer,
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: CommonTrueResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer()
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
		try:
			company=serialized.save()
		except ValidationError as err:
			ret["result"]=False
			ret["reason"]=err.messages[0]
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)

		return Response(ret, status=status.HTTP_200_OK)

class CheckReadyToCreateProjectView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	renderer_classes=[APIRenderer]
	@swagger_auto_schema(
		operation_description="Check if all company settings are done to make ready for creating a project.", 
		security=[{'Bearer': []}],
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: CommonTrueResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer()
		}
	)

	def post(self,request, *args, **kwargs):
		ret={}
		ret["result"]=True
		user = request.user
		try:
			company=Company.objects.get(owner=user)
		except ObjectDoesNotExist:
			ret["result"]=False
			ret["reason"]="You must create a company first."
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		try:
			if company.company_charging_stages is None:
				ret["result"]=False
				ret["reason"]="You must create company's charging stages first."
				return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		except ChargingStages.DoesNotExist:
			ret["result"]=False
			ret["reason"]="You must create company's charging stages first."
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		try:
			if company.company_doc_format is None:
				ret["result"]=False
				ret["reason"]="You must create company's document format first."
				return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		except DocumentFormat.DoesNotExist:
			ret["result"]=False
			ret["reason"]="You must create company's document format first."
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		try:
			if company.company_doc_header is None:
				ret["result"]=False
				ret["reason"]="You must create company's document header first."
				return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		except DocumentHeaderInformation.DoesNotExist:
			ret["result"]=False
			ret["reason"]="You must create company's document header first."
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)

		if not company.br_approved:
			ret["result"]=False
			ret["reason"]="The BR is not yet approved."
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		return Response(ret,status=status.HTTP_200_OK)

#docuemnt format
class GetDocumentFormatChoicesView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	renderer_classes=[APIRenderer]
	@swagger_auto_schema(
		operation_description="Get all docuemnt format choices.", 
		security=[{'Bearer': []}],
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: GetDocumentFormatChoiceResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer()
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
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Create/update user's company docuemnt format.", 
		security=[{'Bearer': []}],
		request_body=SetDocumentFormatSerializer,
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: CommonTrueResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer()
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
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Get user's company docuemnt format.", 
		security=[{'Bearer': []}],
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: GetDocumentFormatResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer()
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
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Create/update user's company charging stage(s).", 
		security=[{'Bearer': []}],
		request_body=SetChargingStagesSerializer(),
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: CommonTrueResponseSerializer(),
			status.HTTP_400_BAD_REQUEST:CommonFalseResponseSerializer(),
			status.HTTP_404_NOT_FOUND: CommonFalseResponseSerializer()
		}
	)
	def post(self,request, *args, **kwargs):
		ret={}
		ret["result"]=True
		data = request.data
		
		serialized = SetChargingStagesSerializer(data=data,context={'request': request})
		serialized.is_valid(raise_exception=True)
		try:
			charging_stages=serialized.save()
		except ObjectDoesNotExist:
			ret["result"]=False
			ret["reason"]="Please create company first."
			return Response(ret, status=status.HTTP_404_NOT_FOUND)
		except ValidationError as err:
			ret["result"]=False
			ret["reason"]=err.messages[0]
			return Response(ret, status=status.HTTP_400_BAD_REQUEST)
		return Response(ret, status=status.HTTP_200_OK)

class GetChargingStagesView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=ChargingStages
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Get user's company charging stages.", 
		security=[{'Bearer': []}],
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: GetChargingStagesResponseSerializer(),
			status.HTTP_404_NOT_FOUND: CommonFalseResponseSerializer()
		}
	)
	def post(self, request, *args, **kwargs):
		ret={}
		ret["result"]=True
		try:
			company=Company.objects.get(owner=request.user)
		except ObjectDoesNotExist:
			ret["result"]=False
			ret["reason"]="Please create company first."
			return Response(ret, status=status.HTTP_404_NOT_FOUND)
		ret["charging_stages"]=company.get_charging_stages_json()
		return Response(ret, status=status.HTTP_200_OK)

#doc_header
class SetDocHeaderView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=DocumentHeaderInformation
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Create/update user's company document header.", 
		security=[{'Bearer': []}],
		request_body=SetDocumentHeaderInformationSerializer,
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: CommonTrueResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer()
		}
	)

	def post(self,request, *args, **kwargs):
		ret={}
		ret["result"]=True
		data = request.data
		serialized = SetDocumentHeaderInformationSerializer(data=data,context={'request': request})
		serialized.is_valid(raise_exception=True)
		try:
			doc_header=serialized.save()
		except ValidationError as err:
			ret["result"]=False
			ret["reason"]=err.messages[0]
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)

		doc_header.save()

		return Response(ret, status=status.HTTP_200_OK)

class GetDocHeaderView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=DocumentHeaderInformation
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Get user's company docuemnt header.", 
		security=[{'Bearer': []}],
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: GetDocumentHeaderInformationResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer()
		}
	)
	def post(self, request, *args, **kwargs):
		ret={}
		ret["result"]=True
		company=Company.objects.get(owner=request.user)
		doc_header=DocumentHeaderInformation.objects.get(company=company)
		ret["doc_header"]=doc_header.as_json()
		return Response(ret, status=status.HTTP_200_OK)

#general remarks
class SetQuotationGeneralRemarksView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	serializer_class = SetQuotationGeneralRemarkSerializer
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Create/update user's company quotation general remark.", 
		security=[{'Bearer': []}],
		request_body=SetQuotationGeneralRemarkSerializer,
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: CommonTrueResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer()
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
		serialized = SetQuotationGeneralRemarkSerializer(data=data,context={'request': request},many=True)
		serialized.is_valid(raise_exception=True)
		general_remarks=serialized.save()
		[general_remark.save() for general_remark in general_remarks]
		QuotationGeneralRemark.objects.filter(index__gt=len(data)).delete()
		return Response(ret, status=status.HTTP_200_OK)

class GetQuotationGeneralRemarksView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=QuotationGeneralRemark
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Get user's company quotation general remarks.", 
		security=[{'Bearer': []}],
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: GetGeneralRemarksSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer()
		}
	)
	def post(self, request, *args, **kwargs):
		ret={}
		ret["result"]=True
		company=Company.objects.get(owner=request.user)
		ret["general_remarks"]=company.get_quotation_general_remarks_json()
		return Response(ret, status=status.HTTP_200_OK)

class SetInvoiceGeneralRemarksView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	serializer_class = SetInvoiceGeneralRemarkSerializer
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Create/update user's company invoice general remark.", 
		security=[{'Bearer': []}],
		request_body=SetInvoiceGeneralRemarkSerializer,
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: CommonTrueResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer()
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
		serialized = SetInvoiceGeneralRemarkSerializer(data=data,context={'request': request},many=True)
		serialized.is_valid(raise_exception=True)
		general_remarks=serialized.save()
		[general_remark.save() for general_remark in general_remarks]
		InvoiceGeneralRemark.objects.filter(index__gt=len(data)).delete()
		return Response(ret, status=status.HTTP_200_OK)

class GetInvoiceGeneralRemarksView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=InvoiceGeneralRemark
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Get user's company invoice general remarks.", 
		security=[{'Bearer': []}],
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: GetGeneralRemarksSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer()
		}
	)
	def post(self, request, *args, **kwargs):
		ret={}
		ret["result"]=True
		company=Company.objects.get(owner=request.user)
		ret["general_remarks"]=company.get_general_remarks_json()
		return Response(ret, status=status.HTTP_200_OK)

class SetReceiptGeneralRemarksView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	serializer_class = SetReceiptGeneralRemarkSerializer
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Create/update user's company receipt general remark.", 
		security=[{'Bearer': []}],
		request_body=SetReceiptGeneralRemarkSerializer,
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: CommonTrueResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer()
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
		serialized = SetReceiptGeneralRemarkSerializer(data=data,context={'request': request},many=True)
		serialized.is_valid(raise_exception=True)
		general_remarks=serialized.save()
		[general_remark.save() for general_remark in general_remarks]
		ReceiptGeneralRemark.objects.filter(index__gt=len(data)).delete()
		return Response(ret, status=status.HTTP_200_OK)

class GetReceiptGeneralRemarksView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=ReceiptGeneralRemark
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Get user's company receipt general remarks.", 
		security=[{'Bearer': []}],
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: GetGeneralRemarksSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer()
		}
	)
	def post(self, request, *args, **kwargs):
		ret={}
		ret["result"]=True
		company=Company.objects.get(owner=request.user)
		ret["general_remarks"]=company.get_general_remarks_json()
		return Response(ret, status=status.HTTP_200_OK)

#project

class GetProjectListView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=Project
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="List all projects", 
		security=[{'Bearer': []}],
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: ListProjectResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer()
		}
	)

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
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Create a project", 
		security=[{'Bearer': []}],
		request_body=CreateProjectSerializer,
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: CommonTrueResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer()
		}
	)

	def post(self,request,*args, **kwargs):
		ret={}
		ret["result"]=True
		data = request.data
		serialized=CreateProjectSerializer(data=data,context={'request':request})
		serialized.is_valid(raise_exception=True)
		try:
			project=serialized.save()
		except ValidationError as err:
			ret["result"]=False
			ret["reason"]=err.messages[0]
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		ret["project_id"]=project.id
		return Response(ret,status=status.HTTP_200_OK)

class UpdateProjectView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=Project
	serializer_class=UpdateProjectSerializer
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Update a project", 
		security=[{'Bearer': []}],
		request_body=UpdateProjectSerializer,
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: CommonTrueResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer(),
			status.HTTP_401_UNAUTHORIZED: CommonFalseResponseSerializer()
		}
	)

	def post(self,request,*args, **kwargs):
		ret={}
		ret["result"]=True
		data = request.data
		if data.get("project_id"):
			serialized=UpdateProjectSerializer(instance=data.get("project_id"),data=data,context={'request':request})
			serialized.is_valid(raise_exception=True)
			try:
				project=serialized.save()
			except ValidationError as err:
				ret["result"]=False
				ret["reason"]=err.messages[0]
				return Response(ret,status=status.HTTP_400_BAD_REQUEST)
			except PermissionDenied:
				ret["result"]=False
				ret["reason"]="Permission Denied"
				return Response(ret,status=status.HTTP_401_UNAUTHORIZED)
			return Response(ret,status=status.HTTP_200_OK)
		else:
			ret["result"]=False
			ret["reason"]="project_id is required."
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)

class GetProjectView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=Project
	serializer_class=GetProjectRequestSerializer
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Get specify project information", 
		security=[{'Bearer': []}],
		request_body=GetProjectRequestSerializer,
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: GetProjectResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer(),
			status.HTTP_401_UNAUTHORIZED: CommonFalseResponseSerializer()
		}
	)

	def post(self,request,*args,**kwargs):
		ret={}
		ret["result"]=True
		data = request.data
		if data.get("id"):
			project=Project.objects.get(id=data.get("id"))
			ret["project"]=project.as_json()
			return Response(ret,status=status.HTTP_200_OK)
		else:
			raise ValidationError("Missing id")

class RemoveProjectView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=Project
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Remove a project", 
		security=[{'Bearer': []}],
		request_body=GetProjectRequestSerializer,
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: CommonTrueResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer(),
			status.HTTP_401_UNAUTHORIZED: CommonFalseResponseSerializer(),
			status.HTTP_404_NOT_FOUND: CommonFalseResponseSerializer()
		}
	)

	def post(self,request,*args,**kwargs):
		ret={}
		ret['result']=True
		data=request.data
		if data.get("id")==None:
			ret["result"]=False
			ret["reason"]="Missing id"
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		try:
			project=Project.objects.get(id=data["id"])
		except ObjectDoesNotExist:
			ret["result"]=False
			ret["reason"]="Project not found."
			return Response(ret,status=status.HTTP_404_NOT_FOUND)
		if project.company.owner==request.user:
			project.delete()
			return Response(ret, status=status.HTTP_200_OK)
		else:
			ret["result"]=False
			ret["reason"]="Permission Denied"
			return Response(ret,status=status.HTTP_401_UNAUTHORIZED)

class PreviewProjectQuotation(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Preview a project quotation", 
		security=[{'Bearer': []}],
		request_body=GetProjectRequestSerializer,
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: ProjectQutationPreviewResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer(),
			status.HTTP_401_UNAUTHORIZED: CommonFalseResponseSerializer(),
			status.HTTP_404_NOT_FOUND:CommonFalseResponseSerializer()
		}
	)

	def post(self,request,*args,**kwargs):
		ret={}
		ret["result"]=True
		data = request.data
		if data.get("id")==None:
			ret["result"]=False
			ret["reason"]="Missing id"
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)

		try:
			project=Project.objects.get(id=data.get("id"))
		except ObjectDoesNotExist:
			ret["result"]=False
			ret["reason"]="Project Not Found"
			return Response(ret,status=status.HTTP_404_NOT_FOUND)
		if project.company.owner==request.user:

			ret["quot_preview"]=project.quot_preview()
			return Response(ret,status=status.HTTP_200_OK)
		else:
			ret["result"]=False
			ret["reason"]="Permission Denied"
			return Response(ret,status=status.HTTP_401_UNAUTHORIZED)

class UpdateProjectQuotationRemarks(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Update a project quotation remarks to comany latest quotation remarks", 
		security=[{'Bearer': []}],
		request_body=GetProjectRequestSerializer,
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: CommonTrueResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer(),
			status.HTTP_401_UNAUTHORIZED: CommonFalseResponseSerializer(),
			status.HTTP_404_NOT_FOUND:CommonFalseResponseSerializer()
		}
	)

	def post(self,request,*args,**kwargs):
		ret={}
		ret["result"]=True
		data = request.data
		if data.get("id")==None:
			ret["result"]=False
			ret["reason"]="Missing id"
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)

		try:
			project=Project.objects.get(id=data.get("id"))
		except ObjectDoesNotExist:
			ret["result"]=False
			ret["reason"]="Project Not Found"
			return Response(ret,status=status.HTTP_404_NOT_FOUND)
		if project.company.owner==request.user:

			project.quotation_remarks=project.company.get_quotation_general_remarks_json()
			project.save()
			return Response(ret,status=status.HTTP_200_OK)
		else:
			ret["result"]=False
			ret["reason"]="Permission Denied"
			return Response(ret,status=status.HTTP_401_UNAUTHORIZED)


class GenerateProjectQuotation(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Generate a project quotation", 
		security=[{'Bearer': []}],
		request_body=GetProjectWithChargingStageRequestSerializer,
		manual_parameters=[token_param],
		produces='application/pdf',
		responses={
			status.HTTP_200_OK: openapi.Response('File Attachment', schema=openapi.Schema(type=openapi.TYPE_FILE)),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer(),
			status.HTTP_401_UNAUTHORIZED: CommonFalseResponseSerializer(),
			status.HTTP_404_NOT_FOUND:CommonFalseResponseSerializer()
		}
	)

	def post(self,request,*args,**kwargs):
		ret={}
		ret["result"]=True
		data = request.data
		try:
			project=Project.objects.get(id=data.get("id"))
		except ObjectDoesNotExist:
			ret["result"]=False
			ret["reason"]="Permission Denied"
			return Response(ret,status=status.HTTP_404_NOT_FOUND)
		if project.company.owner!=request.user:
			ret["result"]=False
			ret["reason"]="Permission Denied"
			return Response(ret,status=status.HTTP_401_UNAUTHORIZED)
		
		context={}
		context["company"]=project.company
		context["project"]=project
		context["items"]=project.all_items()
		context["date"]=datetime.datetime.now().strftime("%d %B %Y")
		context["general_remarks"]=project.quotation_remarks
		context["charging_stages"]=project.charging_stages
		context["quotation_no"]=project.generate_quot_no()
		html = render_to_string('project_quotation_pdf.html', context=context)
		footer=render_to_string('quotation_footer.html',context=context)
		header=render_to_string('quotation_header.html',context=context,request=request)
		doc_header_path=settings.MEDIA_ROOT+'/companies/'+str(project.company.id)+"/doc_header.html"
		os.makedirs(os.path.dirname(doc_header_path), exist_ok=True)
		with open(doc_header_path, 'w') as static_file:
			static_file.write(header)

		options={
			'enable-local-file-access':'',
			'page-size': 'Letter',
	        'margin-top': '1.8in',
	        'margin-right': '0.75in',
	        'margin-bottom': '0.5in',
	        'margin-left': '0.75in',
	        'encoding': "UTF-8",
	        'header-html': doc_header_path,
	        'footer-center': 'Page [page] of [topage]',
	        'footer-font-name':'Arial,serif',
	        'footer-font-size':'12'
		}
		pdfkit.from_string(html, 'out.pdf', options=options)
		'''options = {
			'quiet': ''
		}

		pdfkit.from_url('https://wkhtmltopdf.org/downloads.html', 'out.pdf', options=options)'''
		pdf = open("out.pdf", 'rb')
		response = HttpResponse(pdf.read(), content_type='application/pdf')
		response['Content-Disposition'] = 'attachment; filename=Quotation.pdf'
		pdf.close()
		os.remove("out.pdf")
		#os.remove(doc_header_path)
		if not project.quotation_generated_on or project.updated_on>project.quotation_generated_on:
			project.quotation_generated_on=datetime.datetime.now()
			project.save()
		return response
		#return Response(ret,status=status.HTTP_200_OK)

class PreviewProjectInvoice(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	serializer_class=GetProjectWithChargingStageRequestSerializer
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Preview a project invoice", 
		security=[{'Bearer': []}],
		request_body=GetProjectWithChargingStageRequestSerializer,
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: ProjectInvoicePreviewResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer(),
			status.HTTP_401_UNAUTHORIZED: CommonFalseResponseSerializer(),
			status.HTTP_404_NOT_FOUND:CommonFalseResponseSerializer()
		}
	)

	def post(self,request,*args,**kwargs):
		ret={}
		ret["result"]=True
		data = request.data
		if data.get("id")==None:
			ret["result"]=False
			ret["reason"]="Missing id"
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		if data.get("charging_stage")==None:
			ret["result"]=False
			ret["reason"]="Missing charging_stage"
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		try:
			project=Project.objects.get(id=data.get("id"))
		except ObjectDoesNotExist:
			ret["result"]=False
			ret["reason"]="Project Not Found"
			return Response(ret,status=status.HTTP_404_NOT_FOUND)
		if project.company.owner==request.user:
			ret["invoice_preview"]=project.invoice_preview(data.get("charging_stage"))
			return Response(ret,status=status.HTTP_200_OK)
		else:
			ret["result"]=False
			ret["reason"]="Permission Denied"
			return Response(ret,status=status.HTTP_401_UNAUTHORIZED)
			
class UpdateProjectInvoiceRemarks(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Update a project invoice remarks to comany latest invoice remarks", 
		security=[{'Bearer': []}],
		request_body=GetProjectRequestSerializer,
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: CommonTrueResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer(),
			status.HTTP_401_UNAUTHORIZED: CommonFalseResponseSerializer(),
			status.HTTP_404_NOT_FOUND:CommonFalseResponseSerializer()
		}
	)

	def post(self,request,*args,**kwargs):
		ret={}
		ret["result"]=True
		data = request.data
		if data.get("id")==None:
			ret["result"]=False
			ret["reason"]="Missing id"
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)

		try:
			project=Project.objects.get(id=data.get("id"))
		except ObjectDoesNotExist:
			ret["result"]=False
			ret["reason"]="Project Not Found"
			return Response(ret,status=status.HTTP_404_NOT_FOUND)
		if project.company.owner==request.user:

			project.invoice_remarks=project.company.get_invoice_general_remarks_json()
			project.save()
			return Response(ret,status=status.HTTP_200_OK)
		else:
			ret["result"]=False
			ret["reason"]="Permission Denied"
			return Response(ret,status=status.HTTP_401_UNAUTHORIZED)			

class GenerateProjectInvoice(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Generate a project invoice", 
		security=[{'Bearer': []}],
		request_body=GetProjectWithChargingStageRequestSerializer,
		manual_parameters=[token_param],
		produces='application/pdf',
		responses={
			status.HTTP_200_OK: openapi.Response('File Attachment', schema=openapi.Schema(type=openapi.TYPE_FILE)),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer(),
			status.HTTP_401_UNAUTHORIZED: CommonFalseResponseSerializer(),
			status.HTTP_404_NOT_FOUND:CommonFalseResponseSerializer()
		}
	)

	def post(self,request,*args,**kwargs):
		ret={}
		ret["result"]=True
		data = request.data
		try:
			project=Project.objects.get(id=data.get("id"))
		except ObjectDoesNotExist:
			ret["result"]=False
			ret["reason"]="Permission Denied"
			return Response(ret,status=status.HTTP_404_NOT_FOUND)
		if project.company.owner!=request.user:
			ret["result"]=False
			ret["reason"]="Permission Denied"
			return Response(ret,status=status.HTTP_401_UNAUTHORIZED)
		if data.get("charging_stage")>len(project.charging_stages)-1:
			return serializers.ValidationError("Charging Stage is not in the Project.")
		charging_stage_id=data.get("charging_stage")
		context={}
		context["company"]=project.company
		context["project"]=project
		context["charging_stage_id"]=charging_stage_id
		context["charging_stage"]=project.charging_stages[charging_stage_id-1]
		context["general_remarks"]=project.invoice_remarks
		context["amount"]=project.total_amount()
		context["quotation_no"]=project.generate_quot_no()
		context["quotation_date"]=project.quotation_generated_on.strftime("%d %B %Y")
		context["invoice_no"]=project.generate_invoice_no()
		context["date"]=datetime.datetime.now().strftime("%d %B %Y")
		html = render_to_string('project_invoice_pdf.html', context=context)
		header=render_to_string('invoice_header.html',context=context,request=request)
		doc_header_path=settings.MEDIA_ROOT+'/companies/'+str(project.company.id)+"/doc_header.html"
		os.makedirs(os.path.dirname(doc_header_path), exist_ok=True)
		with open(doc_header_path, 'w') as static_file:
			static_file.write(header)

		options={
			'enable-local-file-access':'',
			'page-size': 'Letter',
	        'margin-top': '1.8in',
	        'margin-right': '0.75in',
	        'margin-bottom': '0.5in',
	        'margin-left': '0.75in',
	        'encoding': "UTF-8",
	        'header-html': doc_header_path
		}
		pdfkit.from_string(html, 'out.pdf', options=options)
		'''options = {
			'quiet': ''
		}

		pdfkit.from_url('https://wkhtmltopdf.org/downloads.html', 'out.pdf', options=options)'''
		pdf = open("out.pdf", 'rb')
		response = HttpResponse(pdf.read(), content_type='application/pdf')
		response['Content-Disposition'] = 'attachment; filename=Invoice.pdf'
		pdf.close()
		os.remove("out.pdf")
		#os.remove(doc_header_path)
		ProjectInvoice.objects.get_or_create(project=project,invoice_id=charging_stage_id)
		return response
		#return Response(ret,status=status.HTTP_200_OK)

class PreviewProjectReceipt(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	serializer_class=GetProjectWithChargingStageRequestSerializer
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Preview a project receipt", 
		security=[{'Bearer': []}],
		request_body=GetProjectWithChargingStageRequestSerializer,
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: ProjectReceiptPreviewResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer(),
			status.HTTP_401_UNAUTHORIZED: CommonFalseResponseSerializer(),
			status.HTTP_404_NOT_FOUND:CommonFalseResponseSerializer()
		}
	)

	def post(self,request,*args,**kwargs):
		ret={}
		ret["result"]=True
		data = request.data
		if data.get("id")==None:
			ret["result"]=False
			ret["reason"]="Missing id"
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		if data.get("charging_stage")==None:
			ret["result"]=False
			ret["reason"]="Missing charging_stage"
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		try:
			project=Project.objects.get(id=data.get("id"))
		except ObjectDoesNotExist:
			ret["result"]=False
			ret["reason"]="Project Not Found"
			return Response(ret,status=status.HTTP_404_NOT_FOUND)
		if project.company.owner==request.user:
			ret["receipt_preview"]=project.receipt_preview(data.get("charging_stage"))
			return Response(ret,status=status.HTTP_200_OK)
		else:
			ret["result"]=False
			ret["reason"]="Permission Denied"
			return Response(ret,status=status.HTTP_401_UNAUTHORIZED)

class UpdateProjectReceiptRemarks(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Update a project receipt remarks to comany latest receipt remarks", 
		security=[{'Bearer': []}],
		request_body=GetProjectRequestSerializer,
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: CommonTrueResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer(),
			status.HTTP_401_UNAUTHORIZED: CommonFalseResponseSerializer(),
			status.HTTP_404_NOT_FOUND:CommonFalseResponseSerializer()
		}
	)

	def post(self,request,*args,**kwargs):
		ret={}
		ret["result"]=True
		data = request.data
		if data.get("id")==None:
			ret["result"]=False
			ret["reason"]="Missing id"
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)

		try:
			project=Project.objects.get(id=data.get("id"))
		except ObjectDoesNotExist:
			ret["result"]=False
			ret["reason"]="Project Not Found"
			return Response(ret,status=status.HTTP_404_NOT_FOUND)
		if project.company.owner==request.user:

			project.receipt_remarks=project.company.get_receipt_general_remarks_json()
			project.save()
			return Response(ret,status=status.HTTP_200_OK)
		else:
			ret["result"]=False
			ret["reason"]="Permission Denied"
			return Response(ret,status=status.HTTP_401_UNAUTHORIZED)

class GenerateProjectReceipt(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Generate a project receipt", 
		security=[{'Bearer': []}],
		request_body=GetProjectWithChargingStageRequestSerializer,
		manual_parameters=[token_param],
		produces='application/pdf',
		responses={
			status.HTTP_200_OK: openapi.Response('File Attachment', schema=openapi.Schema(type=openapi.TYPE_FILE)),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer(),
			status.HTTP_401_UNAUTHORIZED: CommonFalseResponseSerializer(),
			status.HTTP_404_NOT_FOUND:CommonFalseResponseSerializer()
		}
	)

	def post(self,request,*args,**kwargs):
		ret={}
		ret["result"]=True
		data = request.data
		try:
			project=Project.objects.get(id=data.get("id"))
		except ObjectDoesNotExist:
			ret["result"]=False
			ret["reason"]="Permission Denied"
			return Response(ret,status=status.HTTP_404_NOT_FOUND)
		if project.company.owner!=request.user:
			ret["result"]=False
			ret["reason"]="Permission Denied"
			return Response(ret,status=status.HTTP_401_UNAUTHORIZED)
		try:
			project_invoice=ProjectInvoice.objects.get(project=project,invoice_id=data.get("charging_stage"))
		except ObjectDoesNotExist:
			return serializers.ValidationError("Please Generate Invoice First")
			
		charging_stage_id=data.get("charging_stage")
		context={}
		context["company"]=project.company
		context["project"]=project
		context["charging_stage_id"]=charging_stage_id
		context["charging_stage"]=project.charging_stages[charging_stage_id-1]
		context["general_remarks"]=project.receipt_remarks
		context["amount"]=project.total_amount()
		context["quotation_no"]=project.generate_quot_no()
		context["quotation_date"]=project.quotation_generated_on.strftime("%d %B %Y")
		context["invoice_no"]=project.generate_invoice_no()
		context["invoice_date"]=project_invoice.generated_on.strftime("%d-%B-%Y")
		context["receipt_no"]=project.generate_receipt_no()
		context["date"]=datetime.datetime.now().strftime("%d %B %Y")
		html = render_to_string('project_receipt_pdf.html', context=context)
		header=render_to_string('receipt_header.html',context=context,request=request)
		doc_header_path=settings.MEDIA_ROOT+'/companies/'+str(project.company.id)+"/doc_header.html"
		os.makedirs(os.path.dirname(doc_header_path), exist_ok=True)
		with open(doc_header_path, 'w') as static_file:
			static_file.write(header)

		options={
			'enable-local-file-access':'',
			'page-size': 'Letter',
	        'margin-top': '1.8in',
	        'margin-right': '0.75in',
	        'margin-bottom': '0.5in',
	        'margin-left': '0.75in',
	        'encoding': "UTF-8",
	        'header-html': doc_header_path
		}
		pdfkit.from_string(html, 'out.pdf', options=options)
		'''options = {
			'quiet': ''
		}

		pdfkit.from_url('https://wkhtmltopdf.org/downloads.html', 'out.pdf', options=options)'''
		pdf = open("out.pdf", 'rb')
		response = HttpResponse(pdf.read(), content_type='application/pdf')
		response['Content-Disposition'] = 'attachment; filename=Receipt.pdf'
		pdf.close()
		os.remove("out.pdf")
		#os.remove(doc_header_path)
		return response
		#return Response(ret,status=status.HTTP_200_OK)
	
#project-customer
class SetProjectCustomerView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=Customer
	serializer_class=SetProjectCustomerSerializer
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Create/update a customer to a project", 
		security=[{'Bearer': []}],
		request_body=SetProjectCustomerSerializer,
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: CommonTrueResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer(),
			status.HTTP_401_UNAUTHORIZED: CommonFalseResponseSerializer(),
			status.HTTP_404_NOT_FOUND:CommonFalseResponseSerializer()
		}
	)

	def post(self,request,*args, **kwargs):
		ret={}
		ret["result"]=True
		data = request.data
		serialized=SetProjectCustomerSerializer(data=data,context={'request':request})
		serialized.is_valid(raise_exception=True)
		try:
			customer=serialized.save()
		except ValidationError as err:
			ret["result"]=False
			ret["reason"]=err.messages[0]
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		except PermissionDenied:
			ret["result"]=False
			ret["reason"]="Permission PermissionDenied"
			return Response(ret,status=status.HTTP_401_UNAUTHORIZED)
		except ObjectDoesNotExist:
			ret["result"]=False
			ret["reason"]="Project not found."
			return Response(ret,status=status.HTTP_404_NOT_FOUND)
		return Response(ret,status=status.HTTP_200_OK)

#project-room

class CreateProjectRoomView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=Room
	serializer_class=CreateRoomSerializer
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Create a room to a project", 
		security=[{'Bearer': []}],
		request_body=CreateRoomSerializer,
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: CreateRoomResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer(),
			status.HTTP_401_UNAUTHORIZED: CommonFalseResponseSerializer(),
			status.HTTP_404_NOT_FOUND: CommonFalseResponseSerializer()
		}
	)

	def post(self, request, *args, **kwargs):
		ret={}
		ret['result']=True
		data=request.data
		serialized=CreateRoomSerializer(data=data,context={'request':request})
		serialized.is_valid(raise_exception=True)
		try:
			room=serialized.save()
		except ValidationError as err:
			ret["result"]=False
			ret["reason"]=err.messages[0]
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		except PermissionDenied:
			ret["result"]=False
			ret["reason"]="Permission Denied"
			return Response(ret,status=status.HTTP_401_UNAUTHORIZED)
		except ObjectDoesNotExist:
			ret["result"]=False
			ret["reason"]="Project not found."
			return Response(ret,status=status.HTTP_404_NOT_FOUND)
		ret["room_id"]=room.id
		return Response(ret,status=status.HTTP_200_OK)

class UpdateProjectRoomView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=Room
	serializer_class=UpdateRoomSerializer
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Update a room in a project", 
		security=[{'Bearer': []}],
		request_body=UpdateRoomSerializer,
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: CommonTrueResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer(),
			status.HTTP_401_UNAUTHORIZED: CommonFalseResponseSerializer(),
			status.HTTP_404_NOT_FOUND: CommonFalseResponseSerializer()
		}
	)

	def post(self, request, *args, **kwargs):
		ret={}
		ret['result']=True
		data=request.data
		serialized=UpdateRoomSerializer(instance=data.get("id"),data=data,context={'request':request})
		serialized.is_valid(raise_exception=True)
		try:
			room=serialized.save()
		except ValidationError as err:
			ret["result"]=False
			ret["reason"]=err.messages[0]
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		except PermissionDenied:
			ret["result"]=False
			ret["reason"]="Permission Denied"
			return Response(ret,status=status.HTTP_401_UNAUTHORIZED)
		except ObjectDoesNotExist:
			ret["result"]=False
			ret["reason"]="Project room not found."
			return Response(ret,status=status.HTTP_404_NOT_FOUND)

		return Response(ret,status=status.HTTP_200_OK)

class RemoveProjectRoomView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=Room
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Remove a room in a project", 
		security=[{'Bearer': []}],
		request_body=GetRoomRequestSerializer,
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: CommonTrueResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer(),
			status.HTTP_401_UNAUTHORIZED: CommonFalseResponseSerializer(),
			status.HTTP_404_NOT_FOUND: CommonFalseResponseSerializer()
		}
	)

	def post(self,request,*args,**kwargs):
		ret={}
		ret['result']=True
		data=request.data
		if data.get("id")==None:
			ret["result"]=False
			ret["reason"]="Missing id"
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		try:
			room=Room.objects.get(id=data["id"])
		except ObjectDoesNotExist:
			ret["result"]=False
			ret["reason"]="Project room not found."
			return Response(ret,status=status.HTTP_404_NOT_FOUND)
		if room.related_project.company.owner==request.user:
			room.delete()
			return Response(ret, status=status.HTTP_200_OK)
		else:
			ret["result"]=False
			ret["reason"]="Permission Denied"
			return Response(ret,status=status.HTTP_401_UNAUTHORIZED)

class GetProjectRoomListView(APIView):
	permission_classes=[IsAuthenticated]
	authentication_classes=[authentication.JWTAuthentication]
	model=Room
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Get all rooms in a project", 
		security=[{'Bearer': []}],
		request_body=GetProjectRequestSerializer,
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: GetProjectRoomListResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer(),
			status.HTTP_401_UNAUTHORIZED: CommonFalseResponseSerializer(),
			status.HTTP_404_NOT_FOUND: CommonFalseResponseSerializer()
		}
	)

	def post(self, request, *args, **kwargs):
		ret={}
		ret["result"]=True
		data=request.data
		try:
			project=Project.objects.get(id=data["project_id"])
		except ObjectDoesNotExist:
			ret["result"]=False
			ret["reason"]="Project not found."
			return Response(ret,status=status.HTTP_404_NOT_FOUND)
		if project.company.owner==request.user:
			ret["rooms"]=[room.as_json() for room in project.project_rooms.all()]
			return Response(ret, status=status.HTTP_200_OK)		
		else:
			ret["result"]=False
			ret["reason"]="Permission Denied"
			return Response(ret,status=status.HTTP_401_UNAUTHORIZED)

class GetProjectRoomDetailsView(APIView):
	permission_classes=[IsAuthenticated]
	authentication_classes=[authentication.JWTAuthentication]
	model=Room
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Get a specific room in a project", 
		security=[{'Bearer': []}],
		request_body=GetRoomRequestSerializer,
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: GetProjectRoomDetailsResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer(),
			status.HTTP_401_UNAUTHORIZED: CommonFalseResponseSerializer(),
			status.HTTP_404_NOT_FOUND: CommonFalseResponseSerializer()
		}
	)

	def post(self, request, *args, **kwargs):
		ret={}
		ret["result"]=True
		data=request.data
		try:
			room=Room.objects.get(id=data["room_id"])
		except ObjectDoesNotExist:
			ret["result"]=False
			ret["reason"]="Project room not found."
			return Response(ret,status=status.HTTP_404_NOT_FOUND)

		if room.related_project.company.owner==request.user:

			ret["room"]=room.details()
			return Response(ret, status=status.HTTP_200_OK)
		else:
			ret["result"]=False
			ret["reason"]="Permission Denied"
			return Response(ret,status=status.HTTP_401_UNAUTHORIZED)

#project-item

#project-room-item
class GetProjectAllItemView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=RoomItem
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Get all items by type in a project", 
		security=[{'Bearer': []}],
		request_body=GetProjectRequestSerializer,
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: GetProjectAllItemResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer(),
			status.HTTP_401_UNAUTHORIZED: CommonFalseResponseSerializer(),
			status.HTTP_404_NOT_FOUND: CommonFalseResponseSerializer()
		}
	)

	def post(self, request, *args, **kwargs):
		ret={}
		ret["result"]=True
		data=request.data
		if data.get("id")==None:
			ret["result"]=False
			ret["reason"]="Missing id"
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		try:
			project=Project.objects.get(id=data["id"])
		except ObjectDoesNotExist:
			ret["result"]=False
			ret["reason"]="Project not found."
			return Response(ret,status=status.HTTP_404_NOT_FOUND)
		if project.company.owner!=request.user:
			ret["result"]=False
			ret["reason"]="Permission Denied"
			return Response(ret,status=status.HTTP_401_UNAUTHORIZED)
		'''rooms=project.project_rooms.all()
		items={}
		for room in rooms:
			items[room.name]=[]
			for item in room.room_project_items.all():
				items[room.name].append(item.as_json())'''


		ret["items"]=project.all_items()
		return Response(ret,status=status.HTTP_200_OK)		

#project-room-item
class GetProjectAllRoomItemView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=RoomItem
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Get all items by room in a project", 
		security=[{'Bearer': []}],
		request_body=GetProjectRequestSerializer,
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: GetProjectAllRoomItemResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer(),
			status.HTTP_401_UNAUTHORIZED: CommonFalseResponseSerializer(),
			status.HTTP_404_NOT_FOUND: CommonFalseResponseSerializer()
		}
	)

	def post(self, request, *args, **kwargs):
		ret={}
		ret["result"]=True
		data=request.data
		if data.get("id")==None:
			ret["result"]=False
			ret["reason"]="Missing id"
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		try:
			project=Project.objects.get(id=data["project_id"])
		except ObjectDoesNotExist:
			ret["result"]=False
			ret["reason"]="Project not found."
			return Response(ret,status=status.HTTP_404_NOT_FOUND)
		if project.company.owner!=request.user:
			ret["result"]=False
			ret["reason"]="Permission Denied"
			return Response(ret,status=status.HTTP_401_UNAUTHORIZED)
		'''rooms=project.project_rooms.all()
		items={}
		for room in rooms:
			items[room.name]=[]
			for item in room.room_project_items.all():
				items[room.name].append(item.as_json())'''


		ret["items"]=project.all_room_items()
		return Response(ret,status=status.HTTP_200_OK)


class SetProjectRoomItemView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=RoomItem
	serializer_class=SetRoomItemSerializer
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Create/update a project room item", 
		security=[{'Bearer': []}],
		request_body=SetRoomItemSerializer,
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: SetProjectRoomItemResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer(),
			status.HTTP_401_UNAUTHORIZED: CommonFalseResponseSerializer(),
			status.HTTP_404_NOT_FOUND:CommonFalseResponseSerializer()
		}
	)

	def post(self, request, *args, **kwargs):
		ret={}
		ret["result"]=True
		data=request.data
		serialized=SetRoomItemSerializer(data=data,context={'request':request})
		serialized.is_valid(raise_exception=True)
		try:
			room_item=serialized.save()
		except ValidationError as err:
			ret["result"]=False
			ret["reason"]=err.messages[0]
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		except PermissionDenied:
			ret["result"]=False
			ret["reason"]="Permission Denied"
			return Response(ret,status=status.HTTP_401_UNAUTHORIZED)
		except ObjectDoesNotExist:
			ret["result"]=False
			ret["reason"]="Project room not found."
			return Response(ret,status=status.HTTP_404_NOT_FOUND)
		ret["room_item_id"]=room_item.id
		return Response(ret,status=status.HTTP_200_OK)

class RemoveProjectRoomItemView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=RoomItem
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Remove a item from project's room", 
		security=[{'Bearer': []}],
		request_body=GetRoomItemRequestSerializer,
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: CommonTrueResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer(),
			status.HTTP_401_UNAUTHORIZED: CommonFalseResponseSerializer(),
			status.HTTP_404_NOT_FOUND: CommonFalseResponseSerializer()
		}
	)

	def post(self,request,*args,**kwargs):
		ret={}
		ret['result']=True
		data=request.data
		if data.get("id")==None:
			ret["result"]=False
			ret["reason"]="Missing id"
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		try:
			ri=RoomItem.objects.get(id=data["id"])
		except ObjectDoesNotExist:
			ret["result"]=False
			ret["reason"]="Room item not found."
			return Response(ret,status=status.HTTP_404_NOT_FOUND)
		if ri.room.related_project.company.owner==request.user:
			ri.delete()
			return Response(ret, status=status.HTTP_200_OK)
		else:
			ret["result"]=False
			ret["reason"]="Permission Denied"
			return Response(ret,status=status.HTTP_401_UNAUTHORIZED)

class PreCalProjectRoomItemFormulaView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=RoomItem
	serializer_class=PreCalRoomItemFormulaSerializer
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Pre-calculate project room item formula", 
		security=[{'Bearer': []}],
		request_body=PreCalRoomItemFormulaSerializer,
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: PreCalProjectRoomItemFormulaResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer(),
			status.HTTP_401_UNAUTHORIZED: CommonFalseResponseSerializer(),
			status.HTTP_404_NOT_FOUND:CommonFalseResponseSerializer()
		}
	)

	def post(self,request, *args, **kwargs):
		ret={}
		ret["result"]=True
		data=request.data
		serialized=PreCalRoomItemFormulaSerializer(data=data,context={'request':request})
		serialized.is_valid(raise_exception=True)
		try:
			result=serialized.save()
		except ValidationError as err:
			ret["result"]=False
			ret["reason"]=err.messages[0]
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		except PermissionDenied:
			ret["result"]=False
			ret["reason"]="Permission Denied"
			return Response(ret,status=status.HTTP_401_UNAUTHORIZED)
		except ObjectDoesNotExist:
			ret["result"]=False
			ret["reason"]="Project room not found."
			return Response(ret,status=status.HTTP_404_NOT_FOUND)
		ret["formula"](result)
		return Response(ret,status=status.HTTP_200_OK)


#project-misc
class SetProjectMiscView(APIView):
	permission_classes=[IsAuthenticated]
	authentication_classes=[authentication.JWTAuthentication]
	model=ProjectMisc
	serializer_class=SetProjectMiscSerializer
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Create/update project miscellaneous", 
		security=[{'Bearer': []}],
		request_body=SetProjectMiscSerializer,
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: SetProjectMiscResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer(),
			status.HTTP_401_UNAUTHORIZED: CommonFalseResponseSerializer(),
			status.HTTP_404_NOT_FOUND:CommonFalseResponseSerializer()
		}
	)

	def post(self,request,*args, **kwargs):
		ret={}
		ret["result"]=True
		data=request.data
		serialized=SetProjectMiscSerializer(data=data,context={'request':request})
		serialized=is_valid(raise_exception=True)
		try:
			project_misc=serialized.save()
		except ValidationError as err:
			ret["result"]=False
			ret["reason"]=err.messages[0]
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		except PermissionDenied:
			ret["result"]=False
			ret["reason"]="Permission Denied"
			return Response(ret,status=status.HTTP_401_UNAUTHORIZED)
		except ObjectDoesNotExist:
			ret["result"]=False
			ret["reason"]="Project not found."
			return Response(ret,status=status.HTTP_404_NOT_FOUND)
		ret["project_misc_id"]=project_misc.id
		return Response(ret,status=status.HTTP_200_OK)

class RemoveProjectMiscView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=ProjectMisc
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Remove a project misc", 
		security=[{'Bearer': []}],
		request_body=GetProjectMiscRequestSerializer,
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: CommonTrueResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer(),
			status.HTTP_401_UNAUTHORIZED: CommonFalseResponseSerializer(),
			status.HTTP_404_NOT_FOUND: CommonFalseResponseSerializer()
		}
	)

	def post(self,request,*args,**kwargs):
		ret={}
		ret['result']=True
		data=request.data
		if data.get("id")==None:
			ret["result"]=False
			ret["reason"]="Missing id"
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		try:
			pm=ProjectMisc.objects.get(id=data["id"])
		except ObjectDoesNotExist:
			ret["result"]=False
			ret["reason"]="Project misc not found."
			return Response(ret,status=status.HTTP_404_NOT_FOUND)
		if pm.project.company.owner==request.user:
			pm.delete()
			return Response(ret, status=status.HTTP_200_OK)
		else:
			ret["result"]=False
			ret["reason"]="Permission Denied"
			return Response(ret,status=status.HTTP_401_UNAUTHORIZED)

class GetAllProjectMiscView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=ProjectMisc
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Get all miscellaneous in a project", 
		security=[{'Bearer': []}],
		request_body=GetProjectRequestSerializer,
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: GetAllProjectMiscResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer(),
			status.HTTP_401_UNAUTHORIZED: CommonFalseResponseSerializer(),
			status.HTTP_404_NOT_FOUND: CommonFalseResponseSerializer()
		}
	)

	def post(self, request, *args, **kwargs):
		ret={}
		ret["result"]=True
		data=request.data
		try:
			project=Project.objects.get(id=data["project_id"])
		except ObjectDoesNotExist:
			ret["result"]=False
			ret["reason"]="Project not found."
			return Response(ret,status=status.HTTP_404_NOT_FOUND)
		if project.company.owner!=request.user:
			ret["result"]=False
			ret["reason"]="Permission Denied"
			return Response(ret,status=status.HTTP_401_UNAUTHORIZED)
		ret["project_misc"]=[project_misc.as_json() for project_misc in project.project_misc.all()]
		
		return Response(ret,status=status.HTTP_200_OK)

#project-project_timetable
class CreateProjectWorkView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=ProjectWork
	serializer_class=CreateProjectWorkSerializer
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Create a work to project timetable", 
		security=[{'Bearer': []}],
		request_body=CreateProjectWorkSerializer,
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: CreateProjectWorkResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer(),
			status.HTTP_401_UNAUTHORIZED: CommonFalseResponseSerializer(),
			status.HTTP_404_NOT_FOUND: CommonFalseResponseSerializer()
		}
	)

	def post(self,request,*args, **kwargs):
		ret={}
		ret["result"]=True
		data = request.data
		serialized=CreateProjectWorkSerializer(data=data,context={'request':request})
		serialized.is_valid(raise_exception=True)
		try:
			project_work=serialized.save()
		except ValidationError as err:
			ret["result"]=False
			ret["reason"]=err.messages[0]
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		except PermissionDenied:
			ret["result"]=False
			ret["reason"]="Permission Denied"
			return Response(ret,status=status.HTTP_401_UNAUTHORIZED)
		except ObjectDoesNotExist:
			ret["result"]=False
			ret["reason"]="Project not found."
			return Response(ret,status=status.HTTP_404_NOT_FOUND)
		ret["project_work_id"]=project_work.id
		return Response(ret,status=status.HTTP_200_OK)

class UpdateProjectWorkView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=ProjectWork
	serializer_class=UpdateProjectWorkSerializer
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Update a work in project timetable", 
		security=[{'Bearer': []}],
		request_body=UpdateProjectWorkSerializer,
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: CommonTrueResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer(),
			status.HTTP_401_UNAUTHORIZED: CommonFalseResponseSerializer(),
			status.HTTP_404_NOT_FOUND: CommonFalseResponseSerializer()
		}
	)

	def post(self,request,*args, **kwargs):
		ret={}
		ret["result"]=True
		data = request.data
		if data.get("project_work"):
			serialized=UpdateProjectWorkSerializer(instance=data.get("project_work"),data=data,context={'request':request})
			serialized.is_valid(raise_exception=True)
			project_work=serialized.save()
			ret["project_work_id"]=project_work.id
			return Response(ret,status=status.HTTP_200_OK)
		else:
			return serializers.ValidationError("project_work is required.")

class RemoveProjectWorkView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=ProjectWork
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Remove a project work", 
		security=[{'Bearer': []}],
		request_body=GetProjectWorkRequestSerializer,
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: CommonTrueResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer(),
			status.HTTP_401_UNAUTHORIZED: CommonFalseResponseSerializer(),
			status.HTTP_404_NOT_FOUND: CommonFalseResponseSerializer()
		}
	)

	def post(self,request,*args,**kwargs):
		ret={}
		ret['result']=True
		data=request.data
		if data.get("id")==None:
			ret["result"]=False
			ret["reason"]="Missing id"
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		try:
			pw=ProjectWork.objects.get(id=data["id"])
		except ObjectDoesNotExist:
			ret["result"]=False
			ret["reason"]="Project work not found."
			return Response(ret,status=status.HTTP_404_NOT_FOUND)
		if pw.project.company.owner==request.user:
			pw.delete()
			return Response(ret, status=status.HTTP_200_OK)
		else:
			ret["result"]=False
			ret["reason"]="Permission Denied"
			return Response(ret,status=status.HTTP_401_UNAUTHORIZED)


class CreateProjectMilestoneView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=ProjectMilestone
	serializer_class=CreateProjectMilestoneSerializer
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Create a milestone to project timetable", 
		security=[{'Bearer': []}],
		request_body=CreateProjectMilestoneSerializer,
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: CreateProjectMilestoneResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer(),
			status.HTTP_401_UNAUTHORIZED: CommonFalseResponseSerializer(),
			status.HTTP_404_NOT_FOUND: CommonFalseResponseSerializer()
		}
	)

	def post(self,request,*args, **kwargs):
		ret={}
		ret["result"]=True
		data = request.data
		serialized=CreateProjectMilestoneSerializer(data=data,context={'request':request})
		serialized.is_valid(raise_exception=True)
		try:
			project_milestone=serialized.save()
		except ValidationError as err:
			ret["result"]=False
			ret["reason"]=err.messages[0]
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		except PermissionDenied:
			ret["result"]=False
			ret["reason"]="Permission Denied"
			return Response(ret,status=status.HTTP_401_UNAUTHORIZED)
		except ObjectDoesNotExist:
			ret["result"]=False
			ret["reason"]="Project not found."
			return Response(ret,status=status.HTTP_404_NOT_FOUND)
		return Response(ret,status=status.HTTP_200_OK)

class UpdateProjectMilestoneView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=ProjectMilestone
	serializer_class=UpdateProjectMilestoneSerializer
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Update a milestone in project timetable", 
		security=[{'Bearer': []}],
		request_body=UpdateProjectWorkSerializer,
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: CommonTrueResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer(),
			status.HTTP_401_UNAUTHORIZED: CommonFalseResponseSerializer(),
			status.HTTP_404_NOT_FOUND: CommonFalseResponseSerializer()
		}
	)

	def post(self,request,*args, **kwargs):
		ret={}
		ret["result"]=True
		data = request.data
		if data.get("project_milestone"):
			serialized=UpdateProjectMilestoneSerializer(instance=data.get("project_milestone"),data=data,context={'request':request})
			serialized.is_valid(raise_exception=True)
			project_milestone=serialized.save()
			return Response(ret,status=status.HTTP_200_OK)
		else:
			ret["result"]=False
			ret["reason"]="project_milestone is required."
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)

class RemoveProjectMilestoneView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=ProjectMilestone
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Remove a project milestone", 
		security=[{'Bearer': []}],
		request_body=GetProjectMilestoneRequestSerializer,
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: CommonTrueResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer(),
			status.HTTP_401_UNAUTHORIZED: CommonFalseResponseSerializer(),
			status.HTTP_404_NOT_FOUND: CommonFalseResponseSerializer()
		}
	)

	def post(self,request,*args,**kwargs):
		ret={}
		ret['result']=True
		data=request.data
		if data.get("id")==None:
			ret["result"]=False
			ret["reason"]="Missing id"
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		try:
			pm=ProjectMilestone.objects.get(id=data["id"])
		except ObjectDoesNotExist:
			ret["result"]=False
			ret["reason"]="Project milestone not found."
			return Response(ret,status=status.HTTP_404_NOT_FOUND)
		if pm.project.company.owner==request.user:
			pm.delete()
			return Response(ret, status=status.HTTP_200_OK)
		else:
			ret["result"]=False
			ret["reason"]="Permission Denied"
			return Response(ret,status=status.HTTP_401_UNAUTHORIZED)


#district

class GetDistrictListView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Get district list", 
		security=[{'Bearer': []}],
		manual_parameters=[token_param],
		responses={
			status.HTTP_201_CREATED: ListDistrictResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer()
		}
	)

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
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Get room type list", 
		security=[{'Bearer': []}],
		manual_parameters=[token_param],
		responses={
			status.HTTP_201_CREATED: GetRoomTypeListResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer()
		}
	)

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
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Get room related item list by room type id", 
		security=[{'Bearer': []}],
		manual_parameters=[token_param],
		responses={
			status.HTTP_201_CREATED: GetRoomRelatedItemResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer()
		}
	)

	def post(self,request,*args,**kwargs):
		ret={}
		ret['result']=True
		data=request.data
		if data.get("room_type")==None:
			ret["result"]=False
			ret["reason"]="Missing room_type"
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		try:
			room_type=RoomType.objects.get(id=data["room_type"])
		except ObjectDoesNotExist:
			ret["result"]=False
			ret["reason"]="Room type not found"
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		except ValueError:
			ret["result"]=False
			ret["reason"]="Please confirm you input the room type id, not the name"
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		related_items=room_type.related_items
		ret["related_items"]=[ri.as_json() for ri in related_items.all()]
		return Response(ret,status=status.HTTP_200_OK)

#item
class GetItemMaterials(APIView):
	permission_classes=[IsAuthenticated]
	authentication_classes=[authentication.JWTAuthentication]
	model=ItemTypeMaterial
	serializer_class=GetItemMaterialsRequestSerializer
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Get Item Material List", 
		security=[{'Bearer': []}],
		request_body=GetItemMaterialsRequestSerializer(),
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: GetItemMaterialsResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer()
		}
	)

	def post(self,request,*args,**kwargs):
		ret={}
		ret['result']=True
		data=request.data
		serialized=GetItemMaterialsRequestSerializer(data=data,context={'request':request})
		serialized.is_valid(raise_exception=True)
		try:
			ret["materials"]=serialized.save()
		except PermissionDenied:
			ret["result"]=False
			ret["reason"]="Permission Denied"
			return Response(ret,status=status.HTTP_401_UNAUTHORIZED)
		except ObjectDoesNotExist:
			ret["result"]=False
			ret["reason"]="Item type not found."
			return Response(ret,status=status.HTTP_404_NOT_FOUND)
			return Response(ret,status=status.HTTP_200_OK)
		except ValidationError as err:
			ret['result']=False
			ret['reason']=err.messages[0]
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		except ValueError:
			ret['result']=False
			ret['reason']="Please input item type id, not name."
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)

#misc
class GetMiscListView(APIView):
	permission_classes=[IsAuthenticated]
	authentication_classes=[authentication.JWTAuthentication]
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Get misc list", 
		security=[{'Bearer': []}],
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: GetMiscListResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer()
		}
	)

	def post(self,request,*args,**kwargs):
		ret={}
		ret['result']=True
		misc_list=Misc.objects.filter(is_active=True)
		ret["misc_list"]=[misc.as_json() for misc in misc_list.all()]
		return Response(ret,status=status.HTTP_200_OK)

#project-expense

class GetExpenseTypeListView(APIView):
	permission_classes=[IsAuthenticated]
	authentication_classes=[authentication.JWTAuthentication]
	model=ExpenseType
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Get expense type list", 
		security=[{'Bearer': []}],
		manual_parameters=[token_param],
		responses={
			status.HTTP_201_CREATED: GetExpenseTypeListResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer()
		}
	)

	def post(self,request,*args,**kwargs):
		ret={}
		ret['result']=True
		data=request.data
		ret["expense_types"]=[et.as_json() for et in ExpenseType.objects.filter(is_active=True)]
		return Response(ret, status=status.HTTP_200_OK)

class CreateProjectExpenseView(APIView):
	permission_classes=[IsAuthenticated]
	authentication_classes=[authentication.JWTAuthentication]
	model=ProjectExpense
	serializer_class=CreateProjectExpenseSerializer
	renderer_classes=[APIRenderer]

	def post(self,request,*args,**kwargs):
		ret={}
		ret["result"]=True
		data=request.data
		serialized=CreateProjectExpenseSerializer(data=data,context={'request':request})
		serialized.is_valid(raise_exception=True)
		try:
			project_expense=serialized.save()
		except ValidationError as err:
			ret["result"]=False
			ret["reason"]=err.messages[0]
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		except PermissionDenied:
			ret["result"]=False
			ret["reason"]="Permission Denied"
			return Response(ret,status=status.HTTP_401_UNAUTHORIZED)
		except ObjectDoesNotExist:
			ret["result"]=False
			ret["reason"]="Project not found."
			return Response(ret,status=status.HTTP_404_NOT_FOUND)
		ret["project_expense_id"]=project_expense.id
		return Response(ret,status=status.HTTP_200_OK)



class UpdateProjectExpenseView(APIView):
	permission_classes=[IsAuthenticated]
	authentication_classes=[authentication.JWTAuthentication]
	model=ProjectExpense
	serializer_class=UpdateProjectExpenseSerializer
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Update a expense in project", 
		security=[{'Bearer': []}],
		request_body=UpdateProjectExpenseSerializer,
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: CommonTrueResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer(),
			status.HTTP_401_UNAUTHORIZED: CommonFalseResponseSerializer(),
			status.HTTP_404_NOT_FOUND: CommonFalseResponseSerializer()
		}
	)

	def post(self,request,*args, **kwargs):
		ret={}
		ret["result"]=True
		data = request.data
		if data.get("project_expense"):
			serialized=UpdateProjectExpenseSerializer(instance=data.get("project_expense"),data=data,context={'request':request})
			serialized.is_valid(raise_exception=True)
			project_expense=serialized.save()
			return Response(ret,status=status.HTTP_200_OK)
		else:
			ret["result"]=False
			ret["reason"]="project_expense is required."
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)

class RemoveProjectExpenseView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=ProjectExpense
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Remove a project expense", 
		security=[{'Bearer': []}],
		request_body=GetProjectExpenseRequestSerializer,
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: CommonTrueResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer(),
			status.HTTP_401_UNAUTHORIZED: CommonFalseResponseSerializer(),
			status.HTTP_404_NOT_FOUND: CommonFalseResponseSerializer()
		}
	)

	def post(self,request,*args,**kwargs):
		ret={}
		ret['result']=True
		data=request.data
		if data.get("id")==None:
			ret["result"]=False
			ret["reason"]="Missing id"
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		try:
			pe=ProjectExpense.objects.get(id=data["id"])
		except ObjectDoesNotExist:
			ret["result"]=False
			ret["reason"]="Project expense not found."
			return Response(ret,status=status.HTTP_404_NOT_FOUND)
		if pe.project.company.owner==request.user:
			pe.delete()
			return Response(ret, status=status.HTTP_200_OK)
		else:
			ret["result"]=False
			ret["reason"]="Permission Denied"
			return Response(ret,status=status.HTTP_401_UNAUTHORIZED)

class GetProjectProfitAnalysisView(APIView):
	permission_classes=[IsAuthenticated]
	authentication_classes=[authentication.JWTAuthentication]
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Get specify project profit analysis", 
		security=[{'Bearer': []}],
		request_body=GetProjectRequestSerializer,
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: GetProjectProfitAnalysisResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer(),
			status.HTTP_401_UNAUTHORIZED: CommonFalseResponseSerializer()
		}
	)

	def post(self,request,*args,**kwargs):
		ret={}
		ret["result"]=True
		data = request.data
		if data.get("id"):
			try:
				project=Project.objects.get(id=data.get("id"))
			except ObjectDoesNotExist:
				ret["result"]=False
				ret["reason"]="Project not found"
				return Response(ret,status=status.HTTP_404_NOT_FOUND)
			if project.company.owner==request.user:

				ret["project_profit_analysis"]=project.profit_analyse()
				return Response(ret,status=status.HTTP_200_OK)
			else:
				ret["result"]=False
				ret["reason"]="Permission Denied"
				return Response(ret,status=status.HTTP_401_UNAUTHORIZED)

			return Response(ret,status=status.HTTP_200_OK)
		else:
			raise ValidationError("Missing id")

