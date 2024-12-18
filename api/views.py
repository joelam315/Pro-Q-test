import datetime
import json
import os
import pdfkit
import braintree
import logging
import re

from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.template.loader import render_to_string
from django.http.response import HttpResponse, JsonResponse
from django.conf import settings
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist, ValidationError
from django.core.validators import URLValidator
from django.db.models import Q
from django.utils.encoding import escape_uri_path

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
	UpdateUserUsernameAndPhoneRequestSerializer,
	VerifyNewUserUsernameAndPhoneSerializer,
	RefreshTokenRequestSerializer,
	GetUserInfoResponseSerializer,
	ListMeasureQuantifierResponseSerializer,
	ListItemQuantifierResponseSerializer
)
from common.utils import HK_DISTRICT,MEASURE_QUANTIFIERS, ITEM_QUANTIFIERS
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
from companies.utils import UPPER_CHOICES,MIDDLE_CHOICES,LOWER_CHOICES,PROJECT_LOWER_CHOICES
from projects.models import Project, ProjectInvoice, ProjectReceipt,CompanyProjectComparison,ProjectImage,ProjectImageSet
from projects.utils import ROOM_TYPE, PROJECT_STATUS
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
	GetProjectProfitAnalysisResponseSerializer,
	ListProjectStatusResponseSerializer,
	ListProjectInvoiceResponseSerializer,
	ListProjectReceiptResponseSerializer,
	SetProjectChargingStagesSerializer,
	SetProjectQuotationRemarksSerializer,
	SetProjectInvoiceRemarksSerializer,
	SetProjectReceiptRemarksSerializer,
	SetCompanyProjectComparisonSerializer,
	GetCompanyProjectComparisonResponseSerializer,
	ListCompanyProjectComparisonSelectionsResponseSerializer,
	ProjectImageSetSerializer,
	CreateProjectImageSetRequestSerializer,
	GetProjectImageSetRequestSerializer,
	GetProjectImageRequestSerializer
)
from rooms.models import Room, RoomType, RoomItem,RoomTypeFormula
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
	GetRoomItemRequestSerializer,
	GetRoomTypeRequestSerializer,
	GetRoomTypeFormulaListResponseSerializer,
	PreCalRoomTypeFormulaResponseSerializer,
	PreCalRoomTypeFormulaSerializer
)
from customers.models import Customer
from customers.serializers import SetProjectCustomerSerializer
from project_items.models import ItemType,ItemFormula,ItemTypeMaterial
from project_items.serializers import (
	GetItemMaterialsRequestSerializer,
	GetItemMaterialsResponseSerializer,
	GetItemTypeListResponseSerializer,
	GetItemRequestSerializer,
	GetItemFormulaListResponseSerializer
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
	GetProjectMilestoneRequestSerializer,
	GetProjectTimetableResponseSerializer

)

from project_expenses.models import (
	ExpenseType,
	ProjectExpense
)
from project_expenses.serializers import (
	GetExpenseTypeListResponseSerializer,
	CreateProjectExpenseSerializer,
	UpdateProjectExpenseSerializer,
	GetProjectExpenseRequestSerializer,
	CreateProjectExpenseResponseSerializer
)

from subscription_plans.models import (
	SubscriptionPlan,
	CompanySubscribedPlan
)

from subscription_plans.serializers import(
	ListSubscriptionPlanResponseSerializer,
	GetCurrentSubscribedPlanResponseSerializer
)

from api.renderers import APIRenderer

from rest_framework.authentication import SessionAuthentication, BasicAuthentication 
from rest_framework_simplejwt import authentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings as simplejwt_api_settings
from rest_framework_simplejwt.state import token_backend
from rest_framework_simplejwt.utils import datetime_from_epoch
from rest_framework_simplejwt.exceptions import TokenError
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
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework import status
from rest_framework import serializers

from django.views.generic import (CreateView, DeleteView, DetailView,
	TemplateView, UpdateView, View)

import magic
from common.crypt import Cryptographer 

logger = logging.getLogger(__name__)

token_param=openapi.Parameter(name='Authorization',in_=openapi.IN_HEADER,description="Bearer token required", type=openapi.TYPE_STRING)

default_param = openapi.Response(name='result', in_=openapi.IN_BODY,description="Return True if there is no internal error", type=openapi.TYPE_BOOLEAN)


#Fetch Encrypted File
class APIFetchView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	renderer_classes=[APIRenderer]

	def get(self,request,*args,**kwargs):

		user=request.user
		path=request.path
		if not path:
			raise PermissionDenied
		_none,_api,_private,path=path.split('/',3)
		#return Response(path)
		_media,_type,_identity,_param=path.split('/',3)
		if _type=="companies":
			try:
				company=Company.objects.get(id=_identity)
				if company.owner==request.user:
					if self._is_url(path):

						content = requests.get(path, stream=True).raw.read()

					else:

						# Normalise the path to strip out naughty attempts
						path = os.path.normpath(path).replace(
							settings.MEDIA_URL, settings.MEDIA_ROOT, 1
						)

						# Evil path request!
						'''if not path.startswith(settings.MEDIA_ROOT):
							return HttpResponse(
								"evil", content_type="application/json"
							)
							raise Http404'''

						# The file requested doesn't exist locally.  A legit 404
						if not os.path.exists(path):
							return HttpResponse(
								"not exist", content_type="application/json"
							)
							raise Http404

						with open(path, "rb") as f:
							content = f.read()
					content = Cryptographer.decrypted(content)
					return HttpResponse(
						content, content_type=magic.Magic(mime=True).from_buffer(content)
					)
					
				else:
					raise PermissionDenied
			except ObjectDoesNotExist:
				raise PermissionDenied

		raise PermissionDenied

	@staticmethod
	def _is_url(path):
		try:
			URLValidator()(path)
			return True
		except ValidationError:
			return False

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
		check_user=User.objects.filter(phone=data["phone"])
		if check_user.exists():
			user=check_user.first()
			if user.is_active==False:
				if user.is_set_inactive:
					ret["result"]=False
					ret["reason"]="你的帳戶已被停用。請聯絡管理員以進一步了解原因。"
					return Response(ret, status=status.HTTP_401_UNAUTHORIZED)
				elif user.is_login_company_inactive:
					user.is_login_company_inactive=False
					user.is_active=True
					user.save()
			serialized = CreateOrGetUserSerializer(instance=user,data=data)
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
		user=User.objects.get(phone=data["phone"])
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

class UpdateUsernameAndPhoneRequestView(APIView):
	model=User
	authentication_classes=[authentication.JWTAuthentication]
	permission_classes=[IsAuthenticated]
	renderer_classes=[APIRenderer]
	serializer_class = UpdateUserUsernameAndPhoneRequestSerializer

	@swagger_auto_schema(
		operation_description="Update user's username and phone", 
		security=[{'Bearer': []}],
		request_body=UpdateUserUsernameAndPhoneRequestSerializer,
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: CommonTrueResponseSerializer,
			status.HTTP_404_NOT_FOUND: CommonFalseResponseSerializer 
		}
	)

	def post(self, request, *args, **kwargs):
		ret={}
		ret["result"]=True
		#return Response(request.data, status=status.HTTP_201_CREATED)
		data = request.data
		try:
			serialized = UpdateUserUsernameAndPhoneRequestSerializer(data=data,context={'request': request})
			serialized.is_valid(raise_exception=True)
			user=serialized.save()
		except ValidationError as err:
			ret["result"]=False
			ret["reason"]=err.messages[0]
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		
		return Response(ret, status=status.HTTP_200_OK)

class VerifyNewUserUsernameAndPhoneView(APIView):
	model=User
	authentication_classes=[authentication.JWTAuthentication]
	permission_classes=[IsAuthenticated]
	renderer_classes=[APIRenderer]
	serializer_class = VerifyNewUserUsernameAndPhoneSerializer

	@swagger_auto_schema(
		operation_description="Verify new phone number new user", 
		request_body=VerifyNewUserUsernameAndPhoneSerializer,
		responses={
			status.HTTP_200_OK: CommonTrueResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer()
		}
	)
	def post(self, request, *args, **kwargs):
		ret={}
		ret["result"]=True
		data = request.data
		try:
			serialized = VerifyNewUserUsernameAndPhoneSerializer(data=data,context={'request': request})
			serialized.is_valid(raise_exception=True)
			user=serialized.save()
		except ValidationError as err:
			ret["result"]=False
			ret["reason"]=err.messages[0]
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		
		return Response(ret, status=status.HTTP_200_OK)

class GetUserInfoView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=User
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Get user's information", 
		security=[{'Bearer': []}],
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: GetUserInfoResponseSerializer,
			status.HTTP_404_NOT_FOUND: CommonFalseResponseSerializer 
		}
	)
	def post(self,request, *args, **kwargs):
		ret={}
		user=request.user
		ret["result"]=True
		ret["user_info"]=user.as_json()
		return Response(ret,status=status.HTTP_200_OK)

class UserTokenRefreshView(APIView):
	#authentication_classes = [authentication.JWTAuthentication]
	permission_classes = [AllowAny]
	#permission_classes = [IsAuthenticated]
	renderer_classes=[APIRenderer]

	def post(self,request,*args,**kwargs):
		ret={}
		ret["result"]=True
		data=request.data
		if data.get("refresh"):
			try:
				refresh = RefreshToken(data['refresh'])
			except TokenError as err:
				ret["result"]=False
				ret["reason"]="Token is invalid or expired"
				return Response(ret,status=status.HTTP_400_BAD_REQUEST)
			ret["access"] = str(refresh.access_token)

			if simplejwt_api_settings.ROTATE_REFRESH_TOKENS:
				if simplejwt_api_settings.BLACKLIST_AFTER_ROTATION:
					try:
						# Attempt to blacklist the given refresh token
						refresh.blacklist()
					except AttributeError:
						# If blacklist app not installed, `blacklist` method will
						# not be present
						pass

				refresh.set_jti()
				refresh.set_exp()

				ret['refresh'] = str(refresh)

			user_id=token_backend.decode(str(refresh.access_token),verify=True)["user_id"]
			try:
				user=User.objects.get(pk=user_id)
			except ObjectDoesNotExist:
				ret["result"]=False
				ret["reason"]="Permission Denied"
				return Response(ret,status=status.HTTP_401_UNAUTHORIZED)
			ot=OutstandingToken.objects.create(
				jti=refresh.payload[simplejwt_api_settings.JTI_CLAIM],
				token=str(refresh),
				user=user,
				created_at=refresh.current_time,
				expires_at=datetime_from_epoch(refresh.payload["exp"]),
			)
			return Response(ret,status=status.HTTP_200_OK)

		else:
			ret["result"]=False
			ret["reason"]="Missing refresh"
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)

class UserLogoutView(APIView):
	model=User
	authentication_classes=[authentication.JWTAuthentication]
	permission_classes=[IsAuthenticated]
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Logout", 
		request_body=RefreshTokenRequestSerializer,
		responses={
			status.HTTP_200_OK: CommonTrueResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer()
		}
	)

	def post(self,request, *args, **kwargs):
		ret={}
		ret["result"]=True
		data = request.data
		try:
			ot=OutstandingToken.objects.get(token=data.get("refresh_token"))
		except ObjectDoesNotExist:
			ret["result"]=False
			ret["reason"]="Invalid refresh token"
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		if ot.user!=request.user:
			ret["result"]=False
			ret["reason"]="Invalid refresh token"
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		if BlacklistedToken.objects.filter(token=ot).exists():
			ret["result"]=False
			ret["reason"]="Invalid refresh token"
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		BlacklistedToken.objects.create(token=ot).save()

		return Response(ret,status=status.HTTP_200_OK)

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
			ret["company"]=True
		except ObjectDoesNotExist:
			ret["result"]=False
			#ret["reason"]="You must create a company first."
			#return Response(ret,status=status.HTTP_200_OK)
			ret["company"]=False
		if not company.is_active:
			ret["result"]=False
			ret["company_active"]=False
			return Response(ret,status=status.HTTP_200_OK)
		try:
			ret["charging_stages"]=True
			if company.company_charging_stages is None:
				ret["result"]=False
				#ret["reason"]="You must create company's charging stages first."
				#return Response(ret,status=status.HTTP_200_OK)
				ret["charging_stages"]=False
		except ChargingStages.DoesNotExist:
			ret["result"]=False
			#ret["reason"]="You must create company's charging stages first."
			#return Response(ret,status=status.HTTP_200_OK)
			ret["charging_stages"]=False
		try:
			ret["document_format"]=True
			if company.company_doc_format is None:
				ret["result"]=False
				#ret["reason"]="You must create company's document format first."
				#return Response(ret,status=status.HTTP_200_OK)
				ret["document_format"]=False
		except DocumentFormat.DoesNotExist:
			ret["result"]=False
			#ret["reason"]="You must create company's document format first."
			#return Response(ret,status=status.HTTP_200_OK)
			ret["document_format"]=False
		try:
			ret["document_header"]=True
			if company.company_doc_header is None:
				ret["result"]=False
				#ret["reason"]="You must create company's document header first."
				#return Response(ret,status=status.HTTP_200_OK)
				ret["document_header"]=False
		except DocumentHeaderInformation.DoesNotExist:
			ret["result"]=False
			#ret["reason"]="You must create company's document header first."
			#return Response(ret,status=status.HTTP_200_OK)
			ret["document_header"]=False

		ret["br_approved"]=True
		if not company.br_approved:
			ret["result"]=False
			#ret["reason"]="The BR is not yet approved."
			#return Response(ret,status=status.HTTP_200_OK)
			ret["br_approved"]=False
		return Response(ret,status=status.HTTP_200_OK)

class ListCompanyProjectComparisonSelectionView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=CompanyProjectComparison
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="List company comparison all selections.", 
		security=[{'Bearer': []}],
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: ListCompanyProjectComparisonSelectionsResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer()
		}
	)

	def post(self, request, *args, **kwargs):
		ret={}
		ret["result"]=True
		#return Response(request.data, status=status.HTTP_201_CREATED)
		user=request.user
		try:
			company=Company.objects.get(owner=user)
		except ObjectDoesNotExist:
			ret["result"]=False
			ret["reason"]="You must create a company first."
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)

		ret["selections"]=[project.profit_analyse_for_compare() for project in company.company_projects.all()]

		return Response(ret, status=status.HTTP_200_OK)

class SetCompanyProjectComparisonView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=CompanyProjectComparison
	serializer_class = SetCompanyProjectComparisonSerializer
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Set company's compared projects.", 
		security=[{'Bearer': []}],
		request_body=SetCompanyProjectComparisonSerializer,
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
		serialized = SetCompanyProjectComparisonSerializer(data=data,context={'request': request})
		serialized.is_valid(raise_exception=True)
		try:
			comparison=serialized.save()
		except ValidationError as err:
			ret["result"]=False
			ret["reason"]=err.messages[0]
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)

		return Response(ret, status=status.HTTP_200_OK)

class GetCompanyProjectComparisonView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=CompanyProjectComparison
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Get company's compared projects.", 
		security=[{'Bearer': []}],
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: GetCompanyProjectComparisonResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer()
		}
	)

	def post(self, request, *args, **kwargs):
		ret={}
		ret["result"]=True
		#return Response(request.data, status=status.HTTP_201_CREATED)
		user=request.user
		try:
			company=Company.objects.get(owner=user)
		except ObjectDoesNotExist:
			ret["result"]=False
			ret["reason"]="You must create a company first."
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		try:
			ret["comparisons"]=company.get_project_comparison()
		except CompanyProjectComparison.DoesNotExist:
			ret["comparisons"]=[]

		return Response(ret, status=status.HTTP_200_OK)

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
		ret["middle_choices"]=[MIDDLE_CHOICE for MIDDLE_CHOICE in MIDDLE_CHOICES]
		ret["lower_choices"]=[LOWER_CHOICE for LOWER_CHOICE in LOWER_CHOICES]
		ret["project_lower_choices"]=[PROJECT_LOWER_CHOICE for PROJECT_LOWER_CHOICE in PROJECT_LOWER_CHOICES]
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
		try:
			doc_format=DocumentFormat.objects.get(company=company)
			ret["doc_format"]=doc_format.as_json()
			return Response(ret, status=status.HTTP_200_OK)
		except ObjectDoesNotExist:

			#return Response(ret, status=status.HTTP_200_OK)
			ret["result"]=False
			#ret["reason"]="DocumentFormat not found"
			return Response(ret,status=status.HTTP_404_NOT_FOUND)

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
		try:
			ret["charging_stages"]=company.get_charging_stages_json()
			return Response(ret, status=status.HTTP_200_OK)
		except ObjectDoesNotExist:

			#return Response(ret, status=status.HTTP_200_OK)
			ret["result"]=False
			#ret["reason"]="ChargingStages not found"
			return Response(ret,status=status.HTTP_404_NOT_FOUND)


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
		try:
			doc_header=DocumentHeaderInformation.objects.get(company=company)
			ret["doc_header"]=doc_header.as_json()
			return Response(ret, status=status.HTTP_200_OK)
		except ObjectDoesNotExist:

			#return Response(ret, status=status.HTTP_200_OK)
			ret["result"]=False
			#ret["reason"]="DocumentHeaderInformation not found"
			return Response(ret,status=status.HTTP_404_NOT_FOUND)


#general remarks
class SetQuotationGeneralRemarksView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	serializer_class = SetQuotationGeneralRemarkSerializer
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Create/update user's company quotation general remark.", 
		security=[{'Bearer': []}],
		request_body=SetQuotationGeneralRemarkSerializer(many=True),
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
		request_body=SetInvoiceGeneralRemarkSerializer(many=True),
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
		ret["general_remarks"]=company.get_invoice_general_remarks_json()
		return Response(ret, status=status.HTTP_200_OK)

class SetReceiptGeneralRemarksView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	serializer_class = SetReceiptGeneralRemarkSerializer(many=True)
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
		ret["general_remarks"]=company.get_receipt_general_remarks_json()
		return Response(ret, status=status.HTTP_200_OK)

#project

class GetProjectStatusListView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Get project status list", 
		security=[{'Bearer': []}],
		manual_parameters=[token_param],
		responses={
			status.HTTP_201_CREATED: ListProjectStatusResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer()
		}
	)

	def post(self,request, *args, **kwargs):
		ret={}
		ret['result']=True
		project_status_list=PROJECT_STATUS
		ret["project_status_list"]=project_status_list
		return Response(ret, status=status.HTTP_200_OK)

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
		user=request.user
		'''cs=Company.objects.filter(owner=user)
		if cs.exists():
			if not cs.first().is_active:
				ret["result"]=False
				ret["reason"]="Company is inactivated"
				return Response(ret, status=status.HTTP_400_BAD_REQUEST)'''
		projects=Project.objects.filter(company__owner=user)
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
		if data.get("project_id"):
			try:
				project=Project.objects.get(id=data.get("project_id"))
			except ObjectDoesNotExist:
				ret["result"]=False
				ret["reason"]="Project not found"
				return Response(ret,status=status.HTTP_404_NOT_FOUND)
			ret["project"]=project.as_json()
			return Response(ret,status=status.HTTP_200_OK)
		else:
			raise ValidationError("Missing project_id")

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
		if data.get("project_id")==None:
			ret["result"]=False
			ret["reason"]="Missing project_id"
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		try:
			project=Project.objects.get(id=data["project_id"])
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

class UpdateProjectChargingStagesView(APIView):
	permission_classes=[IsAuthenticated]
	authentication_classes=[authentication.JWTAuthentication]
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Update project's charging stages",
		security=[{'Bearer':[]}],
		request_body=SetProjectChargingStagesSerializer,
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
		if data.get("project_id")==None:
			ret["result"]=False
			ret["reason"]="Missing project_id"
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)

		try:
			serialized = SetProjectChargingStagesSerializer(data=data,context={'request': request})
			serialized.is_valid(raise_exception=True)
			serialized.save()
			return Response(ret,status=status.HTTP_200_OK)
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

class UpdateProjectQuotationRemarksView(APIView):
	permission_classes=[IsAuthenticated]
	authentication_classes=[authentication.JWTAuthentication]
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Update project's quotation remarks",
		security=[{'Bearer':[]}],
		request_body=SetProjectQuotationRemarksSerializer,
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
		if data.get("project_id")==None:
			ret["result"]=False
			ret["reason"]="Missing project_id"
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)

		try:
			serialized = SetProjectQuotationRemarksSerializer(data=data,context={'request': request})
			serialized.is_valid(raise_exception=True)
			serialized.save()
			return Response(ret,status=status.HTTP_200_OK)
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

class UpdateProjectInvoiceRemarksView(APIView):
	permission_classes=[IsAuthenticated]
	authentication_classes=[authentication.JWTAuthentication]
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Update project's invoice remarks",
		security=[{'Bearer':[]}],
		request_body=SetProjectInvoiceRemarksSerializer,
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
		if data.get("project_id")==None:
			ret["result"]=False
			ret["reason"]="Missing project_id"
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)

		try:
			serialized = SetProjectInvoiceRemarksSerializer(data=data,context={'request': request})
			serialized.is_valid(raise_exception=True)
			serialized.save()
			return Response(ret,status=status.HTTP_200_OK)
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

class UpdateProjectReceiptRemarksView(APIView):
	permission_classes=[IsAuthenticated]
	authentication_classes=[authentication.JWTAuthentication]
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Update project's receipt remarks",
		security=[{'Bearer':[]}],
		request_body=SetProjectReceiptRemarksSerializer,
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
		if data.get("project_id")==None:
			ret["result"]=False
			ret["reason"]="Missing project_id"
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)

		try:
			serialized = SetProjectReceiptRemarksSerializer(data=data,context={'request': request})
			serialized.is_valid(raise_exception=True)
			serialized.save()
			return Response(ret,status=status.HTTP_200_OK)
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
		if data.get("project_id")==None:
			ret["result"]=False
			ret["reason"]="Missing project_id"
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)

		try:
			project=Project.objects.get(id=data.get("project_id"))
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
		if data.get("project_id")==None:
			ret["result"]=False
			ret["reason"]="Missing project_id"
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)

		try:
			project=Project.objects.get(id=data.get("project_id"))
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
		request_body=GetProjectRequestSerializer,
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
		#data={}
		#data["project_id"]=request.GET.get("project_id")
		try:
			project=Project.objects.get(id=data.get("project_id"))
		except ObjectDoesNotExist:
			ret["result"]=False
			ret["reason"]="ObjectDoesNotExist:" +json.dumps(data)
			return Response(ret,status=status.HTTP_404_NOT_FOUND)
		if project.company.owner!=request.user:
			ret["result"]=False
			ret["reason"]="Permission Denied"
			return Response(ret,status=status.HTTP_401_UNAUTHORIZED)
		
		context={}
		context["company"]=project.company
		#return Response(context["company"].logo_pic.path)
		company_path=settings.MEDIA_ROOT+'/companies/'+str(project.company.id)+"/"
		if context["company"].logo_pic!=None:

			with open(context["company"].logo_pic.path, "rb") as f:
				logo_pic = f.read()

			logo_pic = Cryptographer.decrypted(logo_pic)
			
			with open(company_path+context["company"].logo_pic.path.split("/")[-1], 'wb') as static_file:
				static_file.write(logo_pic)

			context["company"].logo_pic=company_path+context["company"].logo_pic.path.split("/")[-1]
		
		if context["company"].sign!=None:

			with open(context["company"].sign.path, "rb") as f:
				sign = f.read()
			
			sign=Cryptographer.decrypted(sign)

			os.makedirs(os.path.dirname(company_path), exist_ok=True)
			with open(company_path+context["company"].sign.path.split("/")[-1], 'wb') as static_file:
				static_file.write(sign)
			context["company"].sign=company_path+context["company"].sign.path.split("/")[-1]

		#return HttpResponse(context["logo_pic"],content_type="image/png")
		context["project"]=project
		context["items"]=project.all_items()
		context["date"]=datetime.datetime.now().strftime("%d %B %Y")
		context["general_remarks"]=project.quotation_remarks
		context["charging_stages"]=project.charging_stages
		context["quotation_no"]=project.generate_quot_no()
		context["doc_header"]=project.company.company_doc_header
		context["job_no"]=project.generate_job_no()
		context["working_day"]=(project.due_date-project.start_date+ datetime.timedelta(days=1)).days

		if not project.quotation_generated_on or project.updated_on>project.quotation_generated_on:
			project.quotation_generated_on=datetime.datetime.now()
			project.quotation_version=project.quotation_version+1
		if project.quotation_no==None or project.quotation_no=="":
			project.quotation_no=context["quotation_no"].rsplit('-', 1)[0].split('-',1)[1]
		project.save()

		html = render_to_string('project_quotation_pdf.html', context=context)
		footer=render_to_string('quotation_footer.html',context=context)
		header=render_to_string('quotation_header.html',context=context,request=request)
		#return HttpResponse(html)
		#return HttpResponse(header)
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
		filename= project.company.name.replace(" ","_").replace(".","").replace(",","")+"_project_"+context["quotation_no"]+"_quotation"+str(context["date"]).replace(" ","_")+".pdf"
		
		pdfkit.from_string(html, company_path+filename, options=options)
		'''options = {
			'quiet': ''
		}

		pdfkit.from_url('https://wkhtmltopdf.org/downloads.html', 'out.pdf', options=options)'''
		pdf = open(company_path+filename, 'rb')
		response = HttpResponse(pdf.read(), content_type='application/pdf')
		response['Content-Disposition'] = "attachment; filename={}".format(escape_uri_path(filename))+"; filename*=UTF-8''{}".format(escape_uri_path(filename))
		pdf.close()
		os.remove(company_path+filename)
		os.remove(context["company"].logo_pic.path)
		os.remove(context["company"].sign.path)
		os.remove(doc_header_path)
		
		company=Company.objects.get(pk=project.company.id)
		if company.gen_quot_date!=datetime.date.today():
			company.gen_quot_date=datetime.date.today()
			company.gen_quot_count=0
		else:
			company.gen_quot_count=company.gen_quot_count+1
		company.save()

		return response
		#return Response(ret,status=status.HTTP_200_OK)

class ListProjectInvoiceView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	serializer_class=GetProjectRequestSerializer
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="List project invoices", 
		security=[{'Bearer': []}],
		request_body=GetProjectRequestSerializer,
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: ListProjectInvoiceResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer(),
			status.HTTP_401_UNAUTHORIZED: CommonFalseResponseSerializer(),
			status.HTTP_404_NOT_FOUND:CommonFalseResponseSerializer()
		}
	)

	def post(self,request,*args,**kwargs):
		ret={}
		ret["result"]=True
		data=request.data
		if data.get("project_id")==None:
			ret["result"]=False
			ret["reason"]="Missing project_id"
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		try:
			project=Project.objects.get(id=data.get("project_id"))
		except ObjectDoesNotExist:
			ret["result"]=False
			ret["reason"]="Project Not Found"
			return Response(ret,status=status.HTTP_404_NOT_FOUND)
		if project.company.owner==request.user:
			ret["charging_stages"]=project.list_charging_stage_amounts()
			return Response(ret,status=status.HTTP_200_OK)
		else:
			ret["result"]=False
			ret["reason"]="Permission Denied"
			return Response(ret,status=status.HTTP_401_UNAUTHORIZED)


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
		if data.get("project_id")==None:
			ret["result"]=False
			ret["reason"]="Missing project_id"
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		if data.get("charging_stage")==None:
			ret["result"]=False
			ret["reason"]="Missing charging_stage"
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		try:
			project=Project.objects.get(id=data.get("project_id"))
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
		if data.get("project_id")==None:
			ret["result"]=False
			ret["reason"]="Missing project_id"
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)

		try:
			project=Project.objects.get(id=data.get("project_id"))
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
			project=Project.objects.get(id=data.get("project_id"))
		except ObjectDoesNotExist:
			ret["result"]=False
			ret["reason"]="Permission Denied"
			return Response(ret,status=status.HTTP_404_NOT_FOUND)
		if project.company.owner!=request.user:
			ret["result"]=False
			ret["reason"]="Permission Denied"
			return Response(ret,status=status.HTTP_401_UNAUTHORIZED)
		if data.get("charging_stage")>len(project.charging_stages)-1:
			ret["result"]=False
			ret["reason"]="Charging Stage is not in the Project."
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		charging_stage_id=data.get("charging_stage")
		context={}
		context["company"]=project.company
		company_path=settings.MEDIA_ROOT+'/companies/'+str(project.company.id)+"/"
		if context["company"].logo_pic!=None:

			with open(context["company"].logo_pic.path, "rb") as f:
				logo_pic = f.read()

			logo_pic = Cryptographer.decrypted(logo_pic)
			
			with open(company_path+context["company"].logo_pic.path.split("/")[-1], 'wb') as static_file:
				static_file.write(logo_pic)

			context["company"].logo_pic=company_path+context["company"].logo_pic.path.split("/")[-1]
		
		if context["company"].sign!=None:

			with open(context["company"].sign.path, "rb") as f:
				sign = f.read()
			
			sign=Cryptographer.decrypted(sign)

			os.makedirs(os.path.dirname(company_path), exist_ok=True)
			with open(company_path+context["company"].sign.path.split("/")[-1], 'wb') as static_file:
				static_file.write(sign)
			context["company"].sign=company_path+context["company"].sign.path.split("/")[-1]

		total=(float(project.total_amount()))
		context["project"]=project
		context["charging_stage_id"]=charging_stage_id
		context["stage_amount"]=round(total*project.charging_stages[charging_stage_id]["value"]/100,2)
		context["charging_stage"]=project.charging_stages[charging_stage_id]
		context["general_remarks"]=project.invoice_remarks
		context["amount"]=total
		context["quotation_no"]=project.generate_quot_no()
		context["quotation_date"]=project.quotation_generated_on.strftime("%d %B %Y")
		context["invoice_no"]=project.generate_invoice_no(charging_stage_id)
		context["job_no"]=project.generate_job_no()
		context["date"]=datetime.datetime.now().strftime("%d %B %Y")
		context["doc_header"]=project.company.company_doc_header
		if len(project.charging_stages)-1<=charging_stage_id:
			amount=total
			i=0
			for cs in project.charging_stages:
				if i!=charging_stage_id:
					i+=1
					amount=round(amount-round(total*cs["value"]/100,2),2)
			context["stage_amount"]=amount
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

		filename= project.company.name.replace(" ","_").replace(".","").replace(",","")+"_project_"+context["quotation_no"]+"_invoice_"+context["invoice_no"]+"_"+str(context["date"]).replace(" ","_")+".pdf"
		pdfkit.from_string(html, company_path+filename, options=options)
		'''options = {
			'quiet': ''
		}

		pdfkit.from_url('https://wkhtmltopdf.org/downloads.html', 'out.pdf', options=options)'''
		#filename=project.company.name.replace(" ","_")+"_project_"+context["quotation_no"]+'_invoice'+str(context["date"]).replace(" ","_")+'.pdf'
		pdf = open(company_path+filename, 'rb')
		response = HttpResponse(pdf.read(), content_type='application/pdf')
		response['Content-Disposition'] = "attachment; filename={}".format(escape_uri_path(filename))+"; filename*=UTF-8''{}".format(escape_uri_path(filename))
		pdf.close()
		os.remove(company_path+filename)
		os.remove(context["company"].logo_pic.path)
		os.remove(context["company"].sign.path)
		#os.remove(doc_header_path)
		ProjectInvoice.objects.get_or_create(project=project,invoice_id=charging_stage_id)
		
		company=Company.objects.get(pk=project.company.id)
		if company.gen_invoice_date!=datetime.date.today():
			company.gen_invoice_date=datetime.date.today()
			company.gen_invoice_count=0
		else:
			company.gen_invoice_count=company.gen_invoice_count+1
		company.save()
		return response
		#return Response(ret,status=status.HTTP_200_OK)

class ListProjectReceiptView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	serializer_class=GetProjectRequestSerializer
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="List project receipts", 
		security=[{'Bearer': []}],
		request_body=GetProjectRequestSerializer,
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: ListProjectReceiptResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer(),
			status.HTTP_401_UNAUTHORIZED: CommonFalseResponseSerializer(),
			status.HTTP_404_NOT_FOUND:CommonFalseResponseSerializer()
		}
	)

	def post(self,request,*args,**kwargs):
		ret={}
		ret["result"]=True
		data=request.data
		if data.get("project_id")==None:
			ret["result"]=False
			ret["reason"]="Missing project_id"
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		try:
			project=Project.objects.get(id=data.get("project_id"))
		except ObjectDoesNotExist:
			ret["result"]=False
			ret["reason"]="Project Not Found"
			return Response(ret,status=status.HTTP_404_NOT_FOUND)
		if project.company.owner==request.user:
			ret["charging_stages"]=project.list_charging_stage_amounts()
			return Response(ret,status=status.HTTP_200_OK)
		else:
			ret["result"]=False
			ret["reason"]="Permission Denied"
			return Response(ret,status=status.HTTP_401_UNAUTHORIZED)

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
		if data.get("project_id")==None:
			ret["result"]=False
			ret["reason"]="Missing project_id"
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		if data.get("charging_stage")==None:
			ret["result"]=False
			ret["reason"]="Missing charging_stage"
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		try:
			project=Project.objects.get(id=data.get("project_id"))
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
		if data.get("project_id")==None:
			ret["result"]=False
			ret["reason"]="Missing project_id"
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)

		try:
			project=Project.objects.get(id=data.get("project_id"))
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
			project=Project.objects.get(id=data.get("project_id"))
		except ObjectDoesNotExist:
			ret["result"]=False
			ret["reason"]="Permission Denied"
			return Response(ret,status=status.HTTP_404_NOT_FOUND)
		if project.company.owner!=request.user:
			ret["result"]=False
			ret["reason"]="Permission Denied"
			return Response(ret,status=status.HTTP_401_UNAUTHORIZED)
		if data.get("charging_stage")>len(project.charging_stages)-1:
			ret["result"]=False
			ret["reason"]="Charging Stage is not in the Project."
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		try:
			project_invoice=ProjectInvoice.objects.get(project=project,invoice_id=data.get("charging_stage"))
		except ObjectDoesNotExist:
			ret["result"]=False
			ret["reason"]="Please Generate Invoice First"
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)
			
		charging_stage_id=data.get("charging_stage")
		context={}
		context["company"]=project.company
		company_path=settings.MEDIA_ROOT+'/companies/'+str(project.company.id)+"/"
		
		if context["company"].logo_pic!=None:

			with open(context["company"].logo_pic.path, "rb") as f:
				logo_pic = f.read()

			logo_pic = Cryptographer.decrypted(logo_pic)
			
			with open(company_path+context["company"].logo_pic.path.split("/")[-1], 'wb') as static_file:
				static_file.write(logo_pic)

			context["company"].logo_pic=company_path+context["company"].logo_pic.path.split("/")[-1]
		
		if context["company"].sign!=None:

			with open(context["company"].sign.path, "rb") as f:
				sign = f.read()
			
			sign=Cryptographer.decrypted(sign)

			os.makedirs(os.path.dirname(company_path), exist_ok=True)
			with open(company_path+context["company"].sign.path.split("/")[-1], 'wb') as static_file:
				static_file.write(sign)
			context["company"].sign=company_path+context["company"].sign.path.split("/")[-1]
		
		total=(float(project.total_amount()))
		context["project"]=project
		context["charging_stage_id"]=charging_stage_id
		context["stage_amount"]=round(total*project.charging_stages[charging_stage_id]["value"]/100,2)
		context["charging_stage"]=project.charging_stages[charging_stage_id]
		context["general_remarks"]=project.receipt_remarks
		context["amount"]=total
		context["quotation_no"]=project.generate_quot_no()
		context["quotation_date"]=project.quotation_generated_on.strftime("%d %B %Y")
		context["invoice_no"]=project.generate_invoice_no(charging_stage_id)
		context["invoice_date"]=project_invoice.generated_on.strftime("%d-%B-%Y")
		context["receipt_no"]=project.generate_receipt_no(charging_stage_id)
		context["job_no"]=project.generate_job_no()
		context["date"]=datetime.datetime.now().strftime("%d %B %Y")
		context["doc_header"]=project.company.company_doc_header
		if len(project.charging_stages)-1<=charging_stage_id:
			amount=total
			i=0
			for cs in project.charging_stages:
				if i!=charging_stage_id:
					i+=1
					amount=round(amount-round(total*cs["value"]/100,2),2)
			context["stage_amount"]=amount
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
		
		filename= project.company.name.replace(" ","_").replace(".","").replace(",","")+"_project_"+context["quotation_no"]+"_receipt_"+context["receipt_no"]+"_"+str(context["date"]).replace(" ","_")+".pdf"
		pdfkit.from_string(html, company_path+filename, options=options)
		'''options = {
			'quiet': ''
		}

		pdfkit.from_url('https://wkhtmltopdf.org/downloads.html', 'out.pdf', options=options)'''
		pdf = open(company_path+filename, 'rb')
		response = HttpResponse(pdf.read(), content_type='application/pdf')
		response['Content-Disposition'] = "attachment; filename={}".format(escape_uri_path(filename))+"; filename*=UTF-8''{}".format(escape_uri_path(filename))
		pdf.close()
		os.remove(company_path+filename)
		os.remove(context["company"].logo_pic.path)
		os.remove(context["company"].sign.path)
		#os.remove(doc_header_path)
		ProjectReceipt.objects.get_or_create(project=project,receipt_id=charging_stage_id)
		company=Company.objects.get(pk=project.company.id)
		if company.gen_receipt_date!=datetime.date.today():
			company.gen_receipt_date=datetime.date.today()
			company.gen_receipt_count=0
		else:
			company.gen_receipt_count=company.gen_receipt_count+1
		company.save()
		return response
		#return Response(ret,status=status.HTTP_200_OK)

class GetProjectImageRecordsView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	serializer_class=GetProjectRequestSerializer
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Get project's image records", 
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

	def post (self,request,*args,**kwargs):
		ret={}
		ret["result"]=True
		data=request.data

		if data.get("project_id"):
			try:
				project=Project.objects.get(id=data.get("project_id"))
			except ObjectDoesNotExist:
				ret["result"]=False
				ret["reason"]="Project not found"
				return Response(ret,status=status.HTTP_404_NOT_FOUND)
			ret["images"]=dict()
			ret["images"]["項目相片"]=[]
			ret["images"]["工程相片"]=[]
			ret["images"]["收據相片"]=[]
			for project_image_set in project.project_img_set.all().order_by('-upload_date','-id'):
				img_set=project_image_set.img_record()
				ret["images"]["項目相片"].append(img_set)
			for project_milestone in project.project_milestones.exclude(img_upload_date=None).order_by('-img_upload_date','-id'):
				if hasattr(project_milestone,"project_milestone_img_set"):
					img_set=project_milestone.img_record()
					ret["images"]["工程相片"].append(img_set)
			for project_expense in project.project_expense.exclude(img_upload_date=None).order_by('-img_upload_date','-id'):
				img=project_expense.img_record()
				if img!={}:
					ret["images"]["收據相片"].append(img)
			#ret["images"]["工程相片"]=[project_milestone.img_record() ]
			#ret["images"]["收據相片"]=[project_expense.img_record() for project_expense in project.project_expense.exclude(img_upload_date=None).order_by('-img_upload_date')]
			return Response(ret,status=status.HTTP_200_OK)
		else:
			raise ValidationError("Missing project_id")
	
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
		customer=Customer.objects.filter(project=data.get("project"))
		try:
			customer=Customer.objects.get(project=data.get("project"))
			serialized=SetProjectCustomerSerializer(data=data,instance=customer,context={'request':request})
		except ObjectDoesNotExist:
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

class ListMeasureQuantifiersView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	renderer_classes=[APIRenderer]
	@swagger_auto_schema(
		operation_description="List all measure quantifier.", 
		security=[{'Bearer': []}],
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: ListMeasureQuantifierResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer()
		}
	)
	def post(self,request, *args, **kwargs):
		ret={}
		ret["result"]=True
		ret["measure_quantifier"]=[MEASURE_QUANTIFIER[0] for MEASURE_QUANTIFIER in MEASURE_QUANTIFIERS]
		return Response(ret,status=status.HTTP_200_OK)

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
			room.related_project.updated_on=datetime.datetime.now()
			room.related_project.save()
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
class ListItemQuantifiersView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	renderer_classes=[APIRenderer]
	@swagger_auto_schema(
		operation_description="List all item quantifier.", 
		security=[{'Bearer': []}],
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: ListItemQuantifierResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer()
		}
	)
	def post(self,request, *args, **kwargs):
		ret={}
		ret["result"]=True
		ret["item_quantifier"]=[ITEM_QUANTIFIER[0] for ITEM_QUANTIFIER in ITEM_QUANTIFIERS]
		return Response(ret,status=status.HTTP_200_OK)

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
		try:
			room_item=RoomItem.objects.get(id=data.get("room_item_id"))
			serialized=SetRoomItemSerializer(instance=room_item,data=data,context={'request':request})
		except ObjectDoesNotExist:
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
		except KeyError as e:
			ret["reason"]=False
			ret["reason"]="Missing paramater in value: "+str(e)
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		ret["room_item_id"]=room_item.id
		#ret["remark"]=data.get("remark")+": "+room_item.remark
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
			ri.room.related_project.updated_on=datetime.datetime.now()
			ri.room.related_project.save()
			ri.delete()
			return Response(ret, status=status.HTTP_200_OK)
		else:
			ret["result"]=False
			ret["reason"]="Permission Denied"
			return Response(ret,status=status.HTTP_401_UNAUTHORIZED)

class PreCalRoomTypeFormulaView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=RoomType
	serializer_class=PreCalRoomTypeFormulaSerializer
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Pre-calculate room type formula", 
		security=[{'Bearer': []}],
		request_body=PreCalRoomTypeFormulaSerializer,
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: PreCalRoomTypeFormulaResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer(),
			status.HTTP_401_UNAUTHORIZED: CommonFalseResponseSerializer(),
			status.HTTP_404_NOT_FOUND:CommonFalseResponseSerializer()
		}
	)

	def post(self,request,*args,**kwargs):
		ret={}
		ret["result"]=True
		data=request.data
		serialized=PreCalRoomTypeFormulaSerializer(data=data,context={'request':request})
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
			ret["reason"]="Room type not found."
			return Response(ret,status=status.HTTP_404_NOT_FOUND)
		ret["formula"]=(result)
		return Response(ret,status=status.HTTP_200_OK)

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
		ret["formula"]=(result)
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
		try:
			instance=ProjectMisc.objects.get(id=data.get("id"))
			#instance=ProjectMisc.objects.get(misc=data.get("misc"),project=data.get("project"))
			serialized=SetProjectMiscSerializer(instance=instance,data=data,context={'request':request})
		except ObjectDoesNotExist:
			serialized=SetProjectMiscSerializer(data=data,context={'request':request})
		serialized.is_valid(raise_exception=True)
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
		if data.get("project_id")==None:
			ret["result"]=False
			ret["reason"]="Missing project_id"
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		if data.get("misc_id")==None:
			ret["result"]=False
			ret["reason"]="Missing misc_id"
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		try:
			pm=ProjectMisc.objects.get(project=data["project_id"],misc=data["misc_id"])
		except ObjectDoesNotExist:
			ret["result"]=False
			ret["reason"]="Project misc not found."
			return Response(ret,status=status.HTTP_404_NOT_FOUND)
		if pm.project.company.owner==request.user:
			pm.project.updated_on=datetime.datetime.now()
			pm.project.save()
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
		except KeyError:
			ret["result"]=False
			ret["reason"]="Missing project_id"
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		if project.company.owner!=request.user:
			ret["result"]=False
			ret["reason"]="Permission Denied"
			return Response(ret,status=status.HTTP_401_UNAUTHORIZED)
		ret["project_misc"]=[project_misc.as_json() for project_misc in project.project_misc.all()]
		
		return Response(ret,status=status.HTTP_200_OK)

#project-image_set
class CreateProjectImageSetView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=ProjectWork
	serializer_class=ProjectImageSetSerializer
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Create a image set for project", 
		security=[{'Bearer': []}],
		request_body=CreateProjectImageSetRequestSerializer,
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: GetProjectTimetableResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer(),
			status.HTTP_401_UNAUTHORIZED: CommonFalseResponseSerializer(),
			status.HTTP_404_NOT_FOUND: CommonFalseResponseSerializer()
		}
	)

	def post(self,request,*args,**kwargs):
		ret={}
		ret["result"]=True
		data=request.data
		serialized=ProjectImageSetSerializer(data=data,context={'request':request})
		serialized.is_valid(raise_exception=True)
		try:
			pis=serialized.save()
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
		ret["project_image_set_id"]=pis.id
		return Response(ret,status=status.HTTP_200_OK)
		return ret

class RemoveProjectImageSetView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=ProjectImageSet
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Remove a project image set", 
		security=[{'Bearer': []}],
		request_body=GetProjectImageSetRequestSerializer,
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
			pis=ProjectImageSet.objects.get(id=data["id"])
		except ObjectDoesNotExist:
			ret["result"]=False
			ret["reason"]="Project image set not found."
			return Response(ret,status=status.HTTP_404_NOT_FOUND)
		if pis.related_project.company.owner==request.user:
			pis.delete()
			return Response(ret, status=status.HTTP_200_OK)
		else:
			ret["result"]=False
			ret["reason"]="Permission Denied"
			return Response(ret,status=status.HTTP_401_UNAUTHORIZED)

class RemoveProjectImageView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	model=ProjectImage
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Remove a project image set", 
		security=[{'Bearer': []}],
		request_body=GetProjectImageRequestSerializer,
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
			pi=ProjectImage.objects.get(id=data["id"])
		except ObjectDoesNotExist:
			ret["result"]=False
			ret["reason"]="Project image not found."
			return Response(ret,status=status.HTTP_404_NOT_FOUND)
		if pi.related_project.company.owner==request.user:
			pi.delete()
			return Response(ret, status=status.HTTP_200_OK)
		else:
			ret["result"]=False
			ret["reason"]="Permission Denied"
			return Response(ret,status=status.HTTP_401_UNAUTHORIZED)

#project-project_timetable

class GetProjectTimetableView(APIView):
	permission_classes = [IsAuthenticated]
	authentication_classes = [authentication.JWTAuthentication]
	serializer_class=GetProjectRequestSerializer
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Get project timetable", 
		security=[{'Bearer': []}],
		request_body=GetProjectRequestSerializer,
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: GetProjectTimetableResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer(),
			status.HTTP_401_UNAUTHORIZED: CommonFalseResponseSerializer(),
			status.HTTP_404_NOT_FOUND: CommonFalseResponseSerializer()
		}
	)

	def post(self,request,*args,**kwargs):
		ret={}
		ret["result"]=True
		data=request.data
		try:
			project=Project.objects.get(id=data["project_id"])
		except ObjectDoesNotExist:
			ret["result"]=False
			ret["reason"]="Project not found."
			return Response(ret,status=status.HTTP_404_NOT_FOUND)
		except KeyError:
			ret["result"]=False
			ret["reason"]="Missing project_id"
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		if project.company.owner!=request.user:
			ret["result"]=False
			ret["reason"]="Permission Denied"
			return Response(ret,status=status.HTTP_401_UNAUTHORIZED)
		ret["project_works"]=[project_work.as_json() for project_work in project.project_works.all()]
		ret["project_milestone"]=[project_milestone.as_json() for project_milestone in project.project_milestones.all()]

		return Response(ret,status=status.HTTP_200_OK)

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
			status.HTTP_200_OK: GetProjectTimetableResponseSerializer(),
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
			ret["result"]=False
			ret["reason"]="project_work is required."
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)

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
		ret["project_milestone_id"]=project_milestone.id
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
		request_body=UpdateProjectMilestoneSerializer,
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

class GetRoomTypeFormulaListView(APIView):
	permission_classes=[IsAuthenticated]
	authentication_classes=[authentication.JWTAuthentication]
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Get room type formula list", 
		security=[{'Bearer': []}],
		request_body=GetRoomTypeRequestSerializer,
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: GetRoomTypeFormulaListResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer()
		}
	)

	def post(self,request,*args,**kwargs):
		ret={}
		ret['result']=True
		data=request.data
		if data.get("room_type"):
			#room_type_formula_list=RoomTypeFormula.objects.filter(room_type=data["room_type"],is_active=True)
			#ret["room_type_formula_list"]=[room_type_formula.as_json() for room_type_formula in room_type_formula_list.all()]
			
			ret["room_type_formula_list"]=RoomType.objects.get(id=data["room_type"]).get_formulas()
			return Response(ret,status=status.HTTP_200_OK)
		else:
			ret["result"]=False
			ret["reason"]="Missing room_type"
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)

#room - item
class GetRoomRelatedItemListView(APIView):
	permission_classes=[IsAuthenticated]
	authentication_classes=[authentication.JWTAuthentication]
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Get room related item list by room type id", 
		security=[{'Bearer': []}],
		request_body=GetRoomTypeRequestSerializer,
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
		#related_items=dict((ri.id,ri.as_json()) for ri in room_type.related_items.all())
		#ret["related_items"]=[related_items[_id] for _id in room_type.related_items_sort]
		ret["related_items"]=[ri.as_json() for ri in room_type.related_items.all()]
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
		except ValidationError as err:
			ret['result']=False
			ret['reason']=err.messages[0]
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		except ValueError:
			ret['result']=False
			ret['reason']="Please input item type id, not name."
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		return Response(ret,status=status.HTTP_200_OK)

class GetItemTypeListView(APIView):
	permission_classes=[IsAuthenticated]
	authentication_classes=[authentication.JWTAuthentication]
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Get item type list", 
		security=[{'Bearer': []}],
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: GetItemTypeListResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer()
		}
	)

	def post(self,request,*args,**kwargs):
		ret={}
		ret['result']=True
		item_type_list=ItemType.objects.filter(is_active=True)
		ret["item_type_list"]=[item_type.as_json() for item_type in item_type_list.all()]
		return Response(ret,status=status.HTTP_200_OK)

class GetItemFormulaListView(APIView):
	permission_classes=[IsAuthenticated]
	authentication_classes=[authentication.JWTAuthentication]
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Get item formula list", 
		security=[{'Bearer': []}],
		request_body=GetItemRequestSerializer,
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: GetItemFormulaListResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer()
		}
	)

	def post(self,request,*args,**kwargs):
		ret={}
		ret['result']=True
		item_formula_list=ItemFormula.objects.filter(is_active=True)
		ret["item_formula_list"]=[item_formula.as_json() for item_formula in item_formula_list.all()]
		return Response(ret,status=status.HTTP_200_OK)

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

	@swagger_auto_schema(
		operation_description="Create a project expense", 
		security=[{'Bearer': []}],
		request_body=CreateProjectExpenseSerializer,
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: CreateProjectExpenseResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer(),
			status.HTTP_401_UNAUTHORIZED: CommonFalseResponseSerializer(),
			status.HTTP_404_NOT_FOUND: CommonFalseResponseSerializer()
		}
	)

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
		if data.get("project_id"):
			try:
				project=Project.objects.get(id=data.get("project_id"))
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
			raise ValidationError("Missing project_id")

#subscription_plan
class ListSubscriptionPlansView(APIView):
	permission_classes=[IsAuthenticated]
	authentication_classes=[authentication.JWTAuthentication]
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="List all subscription plans", 
		security=[{'Bearer': []}],
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: ListSubscriptionPlanResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer(),
			status.HTTP_401_UNAUTHORIZED: CommonFalseResponseSerializer()
		}
	)

	def post(self,request,*args,**kwargs):
		ret={}
		ret["result"]=True
		user=request.user
		try:
			company=Company.objects.get(owner=user)
		except ObjectDoesNotExist:
			ret["result"]=False
			ret["reason"]="Please create company first."
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)

		ret["subscription_plans"]=[subscription_plan.list_data() for subscription_plan in SubscriptionPlan.objects.filter(visible=True,is_active=True)]
		return Response(ret,status=status.HTTP_200_OK)

class GetCurrentSubscribedPlanView(APIView):
	permission_classes=[IsAuthenticated]
	authentication_classes=[authentication.JWTAuthentication]
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Get current subscribed plan info", 
		security=[{'Bearer': []}],
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: GetCurrentSubscribedPlanResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer(),
			status.HTTP_401_UNAUTHORIZED: CommonFalseResponseSerializer()
		}
	)

	def post(self,request,*args,**kwargs):
		ret={}
		ret["result"]=True
		user=request.user
		try:
			company=Company.objects.get(owner=user)
		except ObjectDoesNotExist:
			ret["result"]=False
			ret["reason"]="Please create company first."
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		now=datetime.datetime.now()
		collection = settings.GATEWAY.customer.search(
			braintree.CustomerSearch.company == str(company.id)+": "+company.name,
			braintree.CustomerSearch.phone == str(user.phone)
		)

		if len(list(collection.items))==0:
			free_plan=SubscriptionPlan.objects.get(display_price=0)
			ret["subscribed_plan"]=dict(
				start_date=company.created_on.date(),
				next_billing_date="-",
				plan=free_plan.plan_name)
			return Response(ret,status=status.HTTP_200_OK)
		elif len(list(collection.items))==1:
			customer=list(collection.items)[0]

			subscribed_plans=[]
			for payment_method in customer.payment_methods:
				for subscription in payment_method.subscriptions:
					try:
						plan_name=SubscriptionPlan.objects.get(id=subscription.plan_id).plan_name
					except ObjectDoesNotExist:
						plan_name="Lost Plan Name"
					if subscription.status==braintree.Subscription.Status.Active:
						subscribed_plans.append(
							dict(
								id=subscription.id,
								start_date=subscription.first_billing_date,
								next_billing_date=subscription.next_billing_date,
								plan=plan_name
							)
						)

			if(len(subscribed_plans)==0):# have no subscribed plan
				free_plan=SubscriptionPlan.objects.get(display_price=0)
				ret["subscribed_plan"]=dict(
				start_date=company.created_on.date(),
				next_billing_date="-",
				plan=free_plan.plan_name)
			elif(len(subscribed_plans)==1):# have 1 subscribed plan
				ret["subscribed_plan"]=subscribed_plans[0]
			else:# have more than one subscribed plan
				ret["duplicated_subscription"]=True
				ret["subscribed_plan"]=subscribed_plans

			return Response(ret,status=status.HTTP_200_OK)
				
		

class GetBraintreeClientTokenView(APIView):
	permission_classes=[IsAuthenticated]
	authentication_classes=[authentication.JWTAuthentication]
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Get braintree client token to create a payment", 
		security=[{'Bearer': []}],
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: CommonTrueResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer(),
			status.HTTP_401_UNAUTHORIZED: CommonFalseResponseSerializer()
		}
	)

	def post(self, request, *args, **kwargs):
		ret={}
		ret["result"]=True
		user=request.user
		try:
			company=Company.objects.get(owner=user)
		except ObjectDoesNotExist:
			ret["result"]=False
			ret["reason"]="Please create company first."
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)

		collection = settings.GATEWAY.customer.search(
			braintree.CustomerSearch.company == str(company.id)+": "+company.name,
			braintree.CustomerSearch.phone == str(company.owner.phone)
		)

		if len(list(collection.items))==0:
			result = settings.GATEWAY.customer.create({
				"company": str(company.id)+": "+company.name,
				"phone": str(company.owner.phone),
			})
			if result.is_success:
				customer_id=result.customer.id
		else:
			customer_id=list(collection.items)[0].id

		client_token=settings.GATEWAY.client_token.generate({
			"customer_id": customer_id
		})
		ret["client_token"]=client_token
		return Response(ret,status=status.HTTP_200_OK)

class SubsribePlanView(APIView):
	permission_classes=[IsAuthenticated]
	authentication_classes=[authentication.JWTAuthentication]
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Subsribe a subscription plan", 
		security=[{'Bearer': []}],
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: CommonTrueResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer(),
			status.HTTP_401_UNAUTHORIZED: CommonFalseResponseSerializer()
		}
	)

	def post(self, request, *args, **kwargs):
		ret={}
		ret["result"]=True
		user=request.user
		data=request.data
		try:
			company=Company.objects.get(owner=user)
		except ObjectDoesNotExist:
			ret["result"]=False
			ret["reason"]="Please create company first."
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		now=datetime.datetime.now()
		

		if data.get("nonce"):
			if data.get("plan_id"):

				collection = settings.GATEWAY.customer.search(
					braintree.CustomerSearch.company == str(company.id)+": "+company.name,
					braintree.CustomerSearch.phone == str(user.phone)
				)

				if len(list(collection.items))==0:
					result = settings.GATEWAY.customer.create({
						"company": str(company.id)+": "+company.name,
						"phone": str(user.phone),
					})
					if result.is_success:
						customer=result.customer
				else:
					customer=list(collection.items)[0]

				subscribed_plans=[]
				for payment_method in customer.payment_methods:
					for subscription in payment_method.subscriptions:
						if subscription.status==braintree.Subscription.Status.Active:
							subscribed_plans.append({"id":subscription.id})
				try:
					plan=SubscriptionPlan.objects.get(id=data.get("plan_id"))
				except ObjectDoesNotExist:
					ret["reason"]="Invalid plan_id"
					return Response(ret,status=status.HTTP_400_BAD_REQUEST)
				if(len(subscribed_plans)==0):# have no subscribed plan

					result = settings.GATEWAY.subscription.create({
						"payment_method_nonce": data.get("nonce"),
						"plan_id": plan.id,
						"merchant_account_id":"interiumdesign"
					})
					ret["created"]=False
					ret["status"]=result.subscription.status
					ret["plan"]=plan.plan_name
				elif(len(subscribed_plans)==1):# have 1 subscribed plan
					result = settings.GATEWAY.subscription.update(subscribed_plans[0]["id"],{
						"payment_method_nonce": data.get("nonce"),
						"plan_id": plan.id,
						"price": plan.display_price,
						"options":{
							"prorate_charges":True,
							"revert_subscription_on_proration_failure":True,
							"replace_all_add_ons_and_discounts":True
						}
					})
					ret["created"]=True
					ret["status"]=result.subscription.status
					ret["plan"]=plan.plan_name
				else:# have more than one subscribed plan
					for subscription in subscription_plans:
						settings.GATEWAY.subscription.cancel(subscription.id)
					result = settings.GATEWAY.subscription.create({
						"payment_method_nonce": data.get("nonce"),
						"plan_id": plan.id,
						"merchant_account_id":"interiumdesign"
					})
					ret["created"]=True
					ret["status"]=result.subscription.status
					ret["plan"]=plan.plan_name
				try:
					return Response(ret,status=status.HTTP_200_OK)
				except Exception as e:
					ret["reason"]=str(e)
					return Response(ret,status=status.HTTP_400_BAD_REQUEST)
			else:
				ret["reason"]="Missing plan_id"
				return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		else:
			ret["reason"]="Missing nonce"
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)

class CancelSubsriptionView(APIView):
	permission_classes=[IsAuthenticated]
	authentication_classes=[authentication.JWTAuthentication]
	renderer_classes=[APIRenderer]

	@swagger_auto_schema(
		operation_description="Subsribe a subscription plan", 
		security=[{'Bearer': []}],
		manual_parameters=[token_param],
		responses={
			status.HTTP_200_OK: CommonTrueResponseSerializer(),
			status.HTTP_400_BAD_REQUEST: CommonFalseResponseSerializer(),
			status.HTTP_401_UNAUTHORIZED: CommonFalseResponseSerializer()
		}
	)

	def post(self, request, *args, **kwargs):
		ret={}
		ret["result"]=True
		user=request.user
		data=request.data
		try:
			company=Company.objects.get(owner=user)
		except ObjectDoesNotExist:
			ret["result"]=False
			ret["reason"]="Please create company first."
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		now=datetime.datetime.now()
		if data.get("subscription_id"):
			result = settings.GATEWAY.subscription.cancel(data.get("subscription_id"))
			if result.is_success:
				return Response(ret,status=status.HTTP_200_OK)
			else:
				ret["reason"]=""
				for error in result.errors.deep_errors:
					ret["reason"]=ret["reason"]+error.message+"\n"
				return Response(ret,status=status.HTTP_400_BAD_REQUEST)
		else:
			ret["reason"]="Missing subscription_id"
			return Response(ret,status=status.HTTP_400_BAD_REQUEST)