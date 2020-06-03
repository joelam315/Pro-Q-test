from django.conf.urls import include, url
from django.urls import path
from function_items.views import (
    FunctionItemsListView,
    FunctionItemsListAPIView,
    GetAllFunctionItemsTypeAPIView,
    CreateFunctionItemView,
    CreateSubFunctionItemView,
    FunctionItemDetailView,
    UpdateFunctionItemView,
    UpdateSubFunctionItemView,
    RemoveFunctionItemView,
    RequestFunctionItemView,
    RequestFunctionItemAPIView,
    RemoveSubFunctionItemView)

app_name = 'function_items'


urlpatterns = [
    url(r'^api/list/',FunctionItemsListAPIView.as_view()),
    url(r'^api/get/type/',GetAllFunctionItemsTypeAPIView.as_view()),
    url(r'^api/request/',RequestFunctionItemAPIView.as_view()),
    path('', FunctionItemsListView.as_view(), name='list'),
    path('create/',CreateFunctionItemView.as_view(),name="add_function_item"),
    path('sub/create/',CreateSubFunctionItemView.as_view(),name="add_sub_function_item"),
    path('request/',RequestFunctionItemView.as_view(),name="request_function_item"),
    path('<int:pk>/view/', FunctionItemDetailView.as_view(), name="view_function_item"),
    path('<int:pk>/edit/', UpdateFunctionItemView.as_view(), name="edit_function_item"),
    path('sub/edit/<int:pk>',UpdateSubFunctionItemView.as_view(),name="edit_sub_function_item"),
    path('<int:pk>/delete/',
         RemoveFunctionItemView.as_view(),
         name="remove_function_item"),
    path('sub/delete',RemoveSubFunctionItemView.as_view(),name="remove_sub_function_item")
]
