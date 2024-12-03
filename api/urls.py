from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views
from django.urls import re_path as url
from django.urls import include, path
from common.views import handler404, handler500
from common.constants import FETCH_URL_NAME
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib import admin
from rest_framework_simplejwt.views import (
    TokenVerifyView,
    TokenRefreshView,
)

from api.views import (
	#UserRegisterView,
	#UserLoginView,
	UserRegisterOrLoginView,
	UserPhoneVerifyView,
	SetCompanyView,
	GetCompanyView,
	GetDocumentFormatChoicesView,
	SetDocumentFormatView,
	GetDocumentFormatView,
	SetDocHeaderView,
	GetDocHeaderView,
	SetChargingStagesView,
	GetChargingStagesView,
	SetQuotationGeneralRemarksView,
	GetQuotationGeneralRemarksView,
	SetInvoiceGeneralRemarksView,
	GetInvoiceGeneralRemarksView,
	SetReceiptGeneralRemarksView,
	GetReceiptGeneralRemarksView,
	CreateProjectView,
	UpdateProjectView,
	GetProjectView,
	GetProjectListView,
	SetProjectCustomerView,
	CreateProjectRoomView,
	UpdateProjectRoomView,
	RemoveProjectRoomView,
	GetProjectAllItemView,
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
	PreviewProjectQuotation,
	GenerateProjectQuotation,
	PreviewProjectInvoice,
	GenerateProjectInvoice,
	PreviewProjectReceipt,
	GenerateProjectReceipt,
	CreateProjectWorkView,
	UpdateProjectWorkView,
	CreateProjectMilestoneView,
	UpdateProjectMilestoneView,
	UpdateProjectQuotationRemarks,
	UpdateProjectInvoiceRemarks,
	UpdateProjectReceiptRemarks,
	GetExpenseTypeListView,
	CreateProjectExpenseView,
	UpdateProjectExpenseView,
	GetProjectProfitAnalysisView,
	CheckReadyToCreateProjectView,
	RemoveProjectView,
	RemoveProjectWorkView,
	RemoveProjectMilestoneView,
	RemoveProjectMiscView,
	RemoveProjectExpenseView,
	RemoveProjectRoomItemView,
	GetMiscListView,
	GetItemTypeListView,
	GetRoomTypeFormulaListView,
	UpdateUsernameAndPhoneRequestView,
	VerifyNewUserUsernameAndPhoneView,
	UserLogoutView,
	GetUserInfoView,
	GetProjectTimetableView,
	GetProjectStatusListView,
	PreCalRoomTypeFormulaView,
	ListProjectInvoiceView,
	ListProjectReceiptView,
	UpdateProjectChargingStagesView,
	UpdateProjectQuotationRemarksView,
	UpdateProjectInvoiceRemarksView,
	UpdateProjectReceiptRemarksView,
	SetCompanyProjectComparisonView,
	GetCompanyProjectComparisonView,
	GetProjectImageRecordsView,
	ListCompanyProjectComparisonSelectionView,
	ListSubscriptionPlansView,
	GetCurrentSubscribedPlanView,
	GetBraintreeClientTokenView,
	SubsribePlanView,
	CancelSubsriptionView,
	UserTokenRefreshView,
	APIFetchView,
	ListMeasureQuantifiersView,
	ListItemQuantifiersView,
	CreateProjectImageSetView,
	RemoveProjectImageSetView,
	RemoveProjectImageView
)


app_name = 'api'

urlpatterns = [
	#path('register/',UserRegisterView.as_view(),name='user_register'),
	#path('login/',UserLoginView.as_view(),name='user_login'),
	url(r'^%s/(?P<path>.*)$' % FETCH_URL_NAME,APIFetchView.as_view(),name="api_"+FETCH_URL_NAME),
	path('login/',UserRegisterOrLoginView.as_view(),name="user_login"),
	path('check/', TokenVerifyView.as_view(), name='token_check'),
	path('profile/',GetUserInfoView.as_view(),name="get_user_info"),
	path('check/ready_to_create/project/',CheckReadyToCreateProjectView.as_view(),name="ready_create_project_check"),
	path('refresh/',UserTokenRefreshView.as_view(),name='token_refresh'),
	path('logout/',UserLogoutView.as_view(),name="user_logout"),
	path('verify/phone/',UserPhoneVerifyView.as_view(),name='phone_verify'),
	path('update/phone/',UpdateUsernameAndPhoneRequestView.as_view(),name='update_new_phone_request'),
	path('verify/new_phone/',VerifyNewUserUsernameAndPhoneView.as_view(),name="new_phone_verify"),
	path('company/set/',SetCompanyView.as_view(),name="set_company"),
	path('company/get/',GetCompanyView.as_view(),name="get_company"),
	path('company/project_comparison/selection/list/',ListCompanyProjectComparisonSelectionView.as_view(),name="list_company_project_comparison_selections"),
	path('company/project_comparison/set/',SetCompanyProjectComparisonView.as_view(),name="set_company_project_comparison"),
	path('company/project_comparison/get/',GetCompanyProjectComparisonView.as_view(),name="get_company_project_comparison"),
	path('doc_format/get/choices/',GetDocumentFormatChoicesView.as_view(),name="get_doc_format_choices"),
	path('doc_format/set/',SetDocumentFormatView.as_view(),name="set_doc_format"),
	path('doc_format/get/',GetDocumentFormatView.as_view(),name="get_doc_format"),
	path('doc_header/set/',SetDocHeaderView.as_view(),name="set_doc_header"),
	path('doc_header/get/',GetDocHeaderView.as_view(),name="get_doc_header"),
	path('charging_stages/set/',SetChargingStagesView.as_view(),name="set_charging_stages"),
	path('charging_stages/get/',GetChargingStagesView.as_view(),name="get_charging_stages"),
	path('quotation_general_remarks/set/',SetQuotationGeneralRemarksView.as_view(),name="set_quotation_general_remarks"),
	path('quotation_general_remarks/get/',GetQuotationGeneralRemarksView.as_view(),name="get_quotation_general_remarks"),
	path('invoice_general_remarks/set/',SetInvoiceGeneralRemarksView.as_view(),name="set_invoice_general_remarks"),
	path('invoice_general_remarks/get/',GetInvoiceGeneralRemarksView.as_view(),name="get_invoice_general_remarks"),
	path('receipt_general_remarks/set/',SetReceiptGeneralRemarksView.as_view(),name="set_receipt_general_remarks"),
	path('receipt_general_remarks/get/',GetReceiptGeneralRemarksView.as_view(),name="get_receipt_general_remarks"),
	path('project/create/',CreateProjectView.as_view(),name="create_project"),
	path('project/update/',UpdateProjectView.as_view(),name="update_project"),
	path('project/get/',GetProjectView.as_view(),name="get_project"),
	path('project/list/',GetProjectListView.as_view(),name="list_project"),
	path('project/remove/',RemoveProjectView.as_view(),name="remove_project"),
	path('project/image/list/',GetProjectImageRecordsView.as_view(),name="list_project_images"),
	path('project/customer/set/',SetProjectCustomerView.as_view(),name="set_project_customer"),
	path('project/room/create/',CreateProjectRoomView.as_view(),name="create_project_room"),
	path('project/room/update/',UpdateProjectRoomView.as_view(),name="update_project_room"),
	path('project/room/remove/',RemoveProjectRoomView.as_view(),name="remove_project_room"),
	path('project/room/list/',GetProjectRoomListView.as_view(),name="list_project_rooms"),
	path('project/room/get/',GetProjectRoomDetailsView.as_view(),name="get_project_room_details"),
	path('project/room/item/set/',SetProjectRoomItemView.as_view(),name="set_project_room_item"),
	path('project/room/item/remove/',RemoveProjectRoomItemView.as_view(),name="remove_project_room_item"),
	path('project/room/item/precal/',PreCalProjectRoomItemFormulaView.as_view(),name="pre_cal_project_room_item_forumla"),
	path('project/item/get/all/byroom/',GetProjectAllRoomItemView.as_view(),name="get_project_all_room_items"),
	path('project/item/get/all/',GetProjectAllItemView.as_view(),name="get_project_all_items"),
	path('project/misc/set/',SetProjectMiscView.as_view(),name="set_project_misc"),
	path('project/misc/remove/',RemoveProjectMiscView.as_view(),name="remove_project_misc"),
	path('project/misc/get/all/',GetAllProjectMiscView.as_view(),name="get_all_project_misc"),
	path('project/charging_stages/update/',UpdateProjectChargingStagesView.as_view(),name="update_project_charging_stages"),
	path('project/quotation_remarks/update/',UpdateProjectQuotationRemarksView.as_view(),name="update_project_quotation_remarks"),
	path('project/invoice_remarks/update/',UpdateProjectInvoiceRemarksView.as_view(),name="update_project_invoice_remarks"),
	path('project/receipt_remarks/update/',UpdateProjectReceiptRemarksView.as_view(),name="update_project_receipt_remarks"),
	path('project/quot/preview/',PreviewProjectQuotation.as_view(),name="preview_project_quotation"),
	path('project/quot/remarks/update/',UpdateProjectQuotationRemarks.as_view(),name="update_project_quotation_remarks"),
	path('project/quot/generate/',GenerateProjectQuotation.as_view(),name="generate_project_quotation"),
	path('project/invoice/list/',ListProjectInvoiceView.as_view(),name="list_project_invoice"),
	path('project/invoice/preview/',PreviewProjectInvoice.as_view(),name="preivew_project_invoice"),
	path('project/invoice/remarks/update/',UpdateProjectInvoiceRemarks.as_view(),name="update_project_invoice_remarks"),
	path('project/invoice/generate/',GenerateProjectInvoice.as_view(),name="generate_project_invoice"),
	path('project/receipt/list/',ListProjectReceiptView.as_view(),name="list_project_receipt"),
	path('project/receipt/preview/',PreviewProjectReceipt.as_view(),name="preview_project_receipt"),
	path('project/receipt/remarks/update/',UpdateProjectReceiptRemarks.as_view(),name="update_project_receipt_remarks"),
	path('project/receipt/generate/',GenerateProjectReceipt.as_view(),name="generate_project_receipt"),
	path('project/timetable/get/',GetProjectTimetableView.as_view(),name="get_project_timetable"),
	path('project/work/create/',CreateProjectWorkView.as_view(),name="create_project_work"),
	path('project/work/update/',UpdateProjectWorkView.as_view(),name="update_project_work"),
	path('project/work/remove/',RemoveProjectWorkView.as_view(),name="remove_project_work"),
	path('project/milestone/create/',CreateProjectMilestoneView.as_view(),name="create_project_milestone"),
	path('project/milestone/update/',UpdateProjectMilestoneView.as_view(),name="update_project_milestone"),
	path('project/milestone/remove/',RemoveProjectMilestoneView.as_view(),name="remove_project_milestone"),
	path('project/expense/create/',CreateProjectExpenseView.as_view(),name="create_project_expense"),
	path('project/expense/update/',UpdateProjectExpenseView.as_view(),name="update_project_expense"),
	path('project/expense/remove/',RemoveProjectExpenseView.as_view(),name="remove_project_expense"),
	path('project/image_set/create/',CreateProjectImageSetView.as_view(),name="create_project_image_set"),
	path('project/image_set/remove/',RemoveProjectImageSetView.as_view(),name="remove_project_image_set"),
	path('project/image/remove/',RemoveProjectImageView.as_view(),name="remove_project_image"),
	path('project/profit/analysis/get/',GetProjectProfitAnalysisView.as_view(),name="get_project_profit_analysis"),
	path('project_status/get/',GetProjectStatusListView.as_view(),name="get_project_status_list"),
	path('districts/get/',GetDistrictListView.as_view(),name="get_districts"),
	path('measure_quantifier/list/',ListMeasureQuantifiersView.as_view(),name="list_measure_quantifiers"),
	path('item_quantifier/list/',ListItemQuantifiersView.as_view(),name="list_item_quantifier"),
	path('room_types/get/',GetRoomTypeListView.as_view(),name="get_room_types"),
	path('room_type/related_items/get/',GetRoomRelatedItemListView.as_view(),name="get_room_type_related_items"),
	path('room_type/formula/get/',GetRoomTypeFormulaListView.as_view(),name="get_room_types"),
	path('room_type/precal/',PreCalRoomTypeFormulaView.as_view(),name="precal_room_type_formula"),
	path('item/materials/get/',GetItemMaterials.as_view(),name="get_item_materials"),
	path('item_types/get/',GetItemTypeListView.as_view(),name="get_item_types"),
	path('expense_types/get/',GetExpenseTypeListView.as_view(),name="get_expense_types"),
	path('misc/list/',GetMiscListView.as_view(),name="get_misc_list"),
	path('subscription_plan/client_token/get/',GetBraintreeClientTokenView.as_view(),name="get_braintree_client_token"),
	path('subscription_plan/list/',ListSubscriptionPlansView.as_view(),name="list_subscription_plans"),
	path('subscription_plan/current/get/',GetCurrentSubscribedPlanView.as_view(),name="get_current_subscribed_plan"),
	path('subscription_plan/subscribe/',SubsribePlanView.as_view(),name="subscribe_plan"),
	path('subscription_plan/cancel/',CancelSubsriptionView.as_view(),name="cancel_subscription"),
]
