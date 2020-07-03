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
    TokenRefreshView,
)

from api.views import (
	UserRegisterView,
	UserLoginView,
	UserPhoneVerifyView,
	SetCompanyView,
	GetCompanyView,
	GetDocumentFormatChoicesView,
	SetDocumentFormatView,
	GetDocumentFormatView,
	SetChargingStagesView,
	GetChargingStagesView,
	SetGeneralRemarksView,
	GetGeneralRemarksView,
	CreateProjectView,
	GetProjectListView,
	SetProjectCustomerView,
	CreateProjectRoomView,
	UpdateProjectRoomView,
	RemoveProjectRoomView,
	GetProjectAllRoomItemView,
	SetProjectRoomItemView,
	PreCalProjectRoomItemFormulaView,
	GetProjectRoomListView,
	SetProjectMiscView,
	GetAllProjectMiscView,
	GetDistrictListView,
	GetRoomTypeListView,
	GetRoomRelatedItemListView,
	GetItemMaterials,
	GetProjectRoomDetailsView,
)

app_name = 'api'

urlpatterns = [
	path('register/',UserRegisterView.as_view(),name='user_register'),
	path('login/',UserLoginView.as_view(),name='user_login'),
	path('check/', TokenVerifyView.as_view(), name='token_check'),
	path('refresh/',TokenRefreshView.as_view(),name='token_refresh'),
	path('verify/phone/',UserPhoneVerifyView.as_view(),name='phone_verify'),
	path('company/set/',SetCompanyView.as_view(),name="set_company"),
	path('company/get/',GetCompanyView.as_view(),name="get_company"),
	path('doc_format/get/choices/',GetDocumentFormatChoicesView.as_view(),name="get_doc_format_choices"),
	path('doc_format/set/',SetDocumentFormatView.as_view(),name="set_doc_format"),
	path('doc_format/get/',GetDocumentFormatView.as_view(),name="get_doc_format"),
	path('charging_stages/set/',SetChargingStagesView.as_view(),name="set_charging_stages"),
	path('charging_stages/get/',GetChargingStagesView.as_view(),name="get_charging_stages"),
	path('general_remarks/set/',SetGeneralRemarksView.as_view(),name="set_general_remarks"),
	path('general_remarks/get/',GetGeneralRemarksView.as_view(),name="get_general_remarks"),
	path('project/create/',CreateProjectView.as_view(),name="create_project"),
	path('project/list/',GetProjectListView.as_view(),name="list_project"),
	path('project/customer/set/',SetProjectCustomerView.as_view(),name="set_project_customer"),
	path('project/room/create/',CreateProjectRoomView.as_view(),name="create_project_room"),
	path('project/room/update/',UpdateProjectRoomView.as_view(),name="update_project_room"),
	path('project/room/remove/',RemoveProjectRoomView.as_view(),name="remove_project_room"),
	path('project/room/list/',GetProjectRoomListView.as_view(),name="list_project_rooms"),
	path('project/room/get/',GetProjectRoomDetailsView.as_view(),name="get_project_room_details"),
	path('project/room/item/set/',SetProjectRoomItemView.as_view(),name="set_project_room_item"),
	path('project/room/item/precal/',PreCalProjectRoomItemFormulaView.as_view(),name="pre_cal_project_room_item_forumla"),
	path('project/item/get/all/',GetProjectAllRoomItemView.as_view(),name="get_project_all_items"),
	path('project/misc/set/',SetProjectMiscView.as_view(),name="set_project_misc"),
	path('project/misc/get/all/',GetAllProjectMiscView.as_view(),name="get_all_project_misc"),
	path('districts/get/',GetDistrictListView.as_view(),name="get_districts"),
	path('room_types/get/',GetRoomTypeListView.as_view(),name="get_room_types"),
	path('room_type/related_items/get/',GetRoomRelatedItemListView.as_view(),name="get_room_type_related_items"),
	path('item/materials/get/',GetItemMaterials.as_view(),name="get_item_materials")
]
