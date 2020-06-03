from django.urls import path
from companies.views import (
    CompaniesListView, CreateCompanyView, CompanyDetailView, CompanyUpdateView,
    CompanyDeleteView, AddCommentView, UpdateCommentView, DeleteCommentView,
    AddAttachmentView, DeleteAttachmentsView, create_mail,  # get_company_details,
    get_contacts_for_company, get_email_data_for_company
)

app_name = 'companies'

urlpatterns = [
    path('', CompaniesListView.as_view(), name='list'),
    path('create/', CreateCompanyView.as_view(), name='new_company'),
    path('<int:pk>/view/', CompanyDetailView.as_view(), name="view_company"),
    path('<int:pk>/edit/', CompanyUpdateView.as_view(), name="edit_company"),
    path('<int:pk>/delete/', CompanyDeleteView.as_view(),
         name="remove_company"),
    path('comment/add/', AddCommentView.as_view(), name="add_comment"),
    path('comment/edit/', UpdateCommentView.as_view(), name="edit_comment"),
    path('comment/remove/', DeleteCommentView.as_view(),
         name="remove_comment"),

    path('attachment/add/', AddAttachmentView.as_view(),
         name="add_attachment"),
    path('attachment/remove/', DeleteAttachmentsView.as_view(),
         name="remove_attachment"),
    path('create-mail', create_mail, name="create_mail"),
    path('get_contacts_for_company/', get_contacts_for_company,
         name="get_contacts_for_company"),
    path('get_email_data_for_company/', get_email_data_for_company,
         name="get_email_data_for_company"),
    #     path('get-company-details/<int:company_id>/', get_company_details, name="get_company_details"),

]
