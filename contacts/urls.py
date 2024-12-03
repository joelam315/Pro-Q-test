from django.urls import re_path as url
from django.urls import path
from contacts.views import (
    ContactsListView, CreateContactView, ContactDetailView,
    UpdateContactView, RemoveContactView,
    GetContactsView, AddCommentView, UpdateCommentView,
    DeleteCommentView, AddAttachmentsView, DeleteAttachmentsView,ContactsListAPIView,CreateContactAPIView,UpdateContactAPIView,RemoveContactAPIView,DeleteContactProfilePicView)

app_name = 'contacts'


urlpatterns = [
    path('', ContactsListView.as_view(), name='list'),
    path('create/', CreateContactView.as_view(), name='add_contact'),
    path('<int:pk>/view/', ContactDetailView.as_view(), name="view_contact"),
    path('<int:pk>/edit/', UpdateContactView.as_view(), name="edit_contact"),
    path('<int:pk>/delete/',
         RemoveContactView.as_view(),
         name="remove_contact"),

    path('get/list/', GetContactsView.as_view(), name="get_contacts"),

    path('comment/add/', AddCommentView.as_view(), name="add_comment"),
    path('comment/edit/', UpdateCommentView.as_view(), name="edit_comment"),
    path('comment/remove/',
         DeleteCommentView.as_view(),
         name="remove_comment"),

    path('attachment/add/',
         AddAttachmentsView.as_view(),
         name="add_attachment"),
    path('attachment/remove/', DeleteAttachmentsView.as_view(),
         name="remove_attachment"),

    path('profile_pic/remove/',DeleteContactProfilePicView.as_view(),
        name="remove_profile_pic"),
]
