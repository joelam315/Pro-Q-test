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
	CreateUserSerializer,
	LoginSerializer, 
	PhoneVerifySerializer,
	CommonTrueResponseSerializer,
	CommonFalseResponseSerializer,
	ListDistrictResponseSerializer,
	LoginResponseSerializer
)
from common.utils import HK_DISTRICT
from companies.models import Company,DocumentFormat,ChargingStages,QuotationGeneralRemark,InvoiceGeneralRemark,ReceiptGeneralRemark
from companies.serializers import (
	SetCompanySerializer, 
	CompanySerializer, 
	SetDocumentFormatSerializer,
	SetChargingStagesSerializer,
	SetQuotationGeneralRemarkSerializer,
	SetInvoiceGeneralRemarkSerializer,
	SetReceiptGeneralRemarkSerializer,
	DocumentFormatSerializer,
	ChargingStagesSerializer,
	QuotationGeneralRemarkSerializer,
	InvoiceGeneralRemarkSerializer,
	ReceiptGeneralRemarkSerializer,
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
	ProjectQutationPreviewResponseSerializer
)
from rooms.models import Room, RoomType, RoomItem
from rooms.serializers import (
	CreateRoomSerializer,
	UpdateRoomSerializer,
	SetRoomItemSerializer,
	PreCalRoomItemFormulaSerializer
)
from customers.models import Customer
from customers.serializers import SetProjectCustomerSerializer
from project_items.models import ItemType,ItemFormula,ItemTypeMaterial
from project_items.serializers import (
	GetItemMaterialsRequestSerializer,
	GetItemMaterialsResponseSerializer
)
from project_misc.models import ProjectMisc
from project_misc.serializers import SetProjectMiscSerializer

from project_timetable.models import ProjectWork, ProjectMilestone
from project_timetable.serializers import (
	CreateProjectWorkSerializer,
	UpdateProjectWorkSerializer,
	CreateProjectMilestoneSerializer,
	UpdateProjectMilestoneSerializer

)

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
			status.HTTP_200_OK: LoginResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer
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
			status.HTTP_200_OK: CommonTrueResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer()
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

#docuemnt format
class GetDocumentFormatChoicesView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
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

#general remarks
class SetQuotationGeneralRemarksView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	serializer_class = SetQuotationGeneralRemarkSerializer

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

class PreviewProjectQuotation(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]

	@swagger_auto_schema(
		operation_description="Preview a project quotation", 
		security=[{'Bearer': []}],
		request_body=GetProjectRequestSerializer,
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: ProjectQutationPreviewResponseSerializer(),
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
			ret["quot_preview"]=project.quot_preview()
			return Response(ret,status=status.HTTP_200_OK)
		else:
			raise serializers.ValidationError("Missing id")


class GenerateProjectQuotation(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]

	def post(self,request,*args,**kwargs):
		ret={}
		ret["result"]=True
		data = request.data
		project=Project.objects.get(id=data.get("id"))
		
		context={}
		context["company"]=project.company
		context["project"]=project
		context["items"]=project.all_items()
		context["date"]=datetime.datetime.now().strftime("%d %B %Y")
		context["general_remarks"]=project.company.get_quotation_general_remarks_json()
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

	def post(self,request,*args,**kwargs):
		ret={}
		ret["result"]=True
		data = request.data
		if data.get("id"):
			project=Project.objects.get(id=data.get("id"))
			ret["invoice_preview"]=project.invoice_preview()
			return Response(ret,status=status.HTTP_200_OK)
		else:
			raise serializers.ValidationError("Missing id")

class GenerateProjectInvoice(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]

	def post(self,request,*args,**kwargs):
		ret={}
		ret["result"]=True
		data = request.data
		project=Project.objects.get(id=data.get("id"))
		if data.get("charging_stage")>len(project.charging_stages)-1:
			return serializers.ValidationError("Charging Stage is not in the Project.")
		charging_stage_id=data.get("charging_stage")
		context={}
		context["company"]=project.company
		context["project"]=project
		context["charging_stage_id"]=charging_stage_id
		context["charging_stage"]=project.charging_stages[charging_stage_id-1]
		context["general_remarks"]=project.company.get_invoice_general_remarks_json()
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

class GenerateProjectReceipt(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]

	def post(self,request,*args,**kwargs):
		ret={}
		ret["result"]=True
		data = request.data
		project=Project.objects.get(id=data.get("id"))
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
		context["general_remarks"]=project.company.get_receipt_general_remarks_json()
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

#project-item

#project-room-item
class GetProjectAllItemView(APIView):
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

	def post(self, request, *args, **kwargs):
		ret={}
		ret["result"]=True
		data=request.data
		project=Project.objects.get(id=data["project_id"])
		if project.company.owner!=request.user:
			raise PermissionDenied
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

#project-project_timetable
class CreateProjectWorkView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=ProjectWork
	serializer_class=CreateProjectWorkSerializer

	def post(self,request,*args, **kwargs):
		ret={}
		ret["result"]=True
		data = request.data
		serialized=CreateProjectWorkSerializer(data=data,context={'request':request})
		serialized.is_valid(raise_exception=True)
		project_work=serialized.save()
		ret["project_work_id"]=project_work.id
		return Response(ret,status=status.HTTP_200_OK)

class UpdateProjectWorkView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=ProjectWork
	serializer_class=UpdateProjectWorkSerializer

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

class CreateProjectMilestoneView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=ProjectMilestone
	serializer_class=CreateProjectMilestoneSerializer

	def post(self,request,*args, **kwargs):
		ret={}
		ret["result"]=True
		data = request.data
		serialized=CreateProjectMilestoneSerializer(data=data,context={'request':request})
		serialized.is_valid(raise_exception=True)
		project_milestone=serialized.save()
		ret["project_milestone_id"]=project_milestone.id
		return Response(ret,status=status.HTTP_200_OK)

class UpdateProjectMilestoneView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=ProjectMilestone
	serializer_class=UpdateProjectMilestoneSerializer

	def post(self,request,*args, **kwargs):
		ret={}
		ret["result"]=True
		data = request.data
		if data.get("project_milestone"):
			serialized=UpdateProjectMilestoneSerializer(instance=data.get("project_milestone"),data=data,context={'request':request})
			serialized.is_valid(raise_exception=True)
			project_milestone=serialized.save()
			ret["project_milestone_id"]=project_milestone.id
			return Response(ret,status=status.HTTP_200_OK)
		else:
			return serializers.ValidationError("project_milestone is required.")


#district

class GetDistrictListView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]

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
	serializer_class=GetItemMaterialsRequestSerializer

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
		try:
			serialized=GetItemMaterialsRequestSerializer(data=data,context={'request':request})
			serialized.is_valid(raise_exception=True)
			ret["materials"]=serialized.save()
			return Response(ret,status=status.HTTP_200_OK)
		except ValidationError as err:
			ret['result']=False
			ret['reason']=err.messages[0]
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)
