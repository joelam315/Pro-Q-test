from django.conf.urls import include, url
from django.urls import path
from customers.views import (
    CustomersListView, CreateCustomerView, CustomerDetailView,
    UpdateCustomerView, RemoveCustomerView,
    GetCustomersView, AddCommentView, UpdateCommentView,
    DeleteCommentView, AddAttachmentsView, DeleteAttachmentsView,CustomersListAPIView,CreateCustomerAPIView,UpdateCustomerAPIView,RemoveCustomerAPIView,DeleteCustomerProfilePicView)

app_name = 'customers'


urlpatterns = [
    url(r'^api/list/',CustomersListAPIView.as_view()),
    url(r'^api/create/',CreateCustomerAPIView.as_view()),
    url(r'^api/update/',UpdateCustomerAPIView.as_view()),
    url(r'^api/remove/',RemoveCustomerAPIView.as_view()),
    path('', CustomersListView.as_view(), name='list'),
    path('create/', CreateCustomerView.as_view(), name='add_customer'),
    path('<int:pk>/view/', CustomerDetailView.as_view(), name="view_customer"),
    path('<int:pk>/edit/', UpdateCustomerView.as_view(), name="edit_customer"),
    path('<int:pk>/delete/',
         RemoveCustomerView.as_view(),
         name="remove_customer"),

    path('get/list/', GetCustomersView.as_view(), name="get_customers"),

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

    path('profile_pic/remove/',DeleteCustomerProfilePicView.as_view(),
        name="remove_profile_pic"),
]
