from django.conf.urls import include, url
from django.urls import path
from project_items.views import (
    ProjectItemsListView,
    ProjectItemsListAPIView,
    GetAllProjectItemsTypeAPIView,
    CreateProjectItemView,
    CreateSubProjectItemView,
    ProjectItemDetailView,
    UpdateProjectItemView,
    UpdateSubProjectItemView,
    RemoveProjectItemView,
    RequestProjectItemView,
    RequestProjectItemAPIView,
    RemoveSubProjectItemView)

app_name = 'project_items'


urlpatterns = [
    url(r'^api/list/',ProjectItemsListAPIView.as_view()),
    url(r'^api/get/type/',GetAllProjectItemsTypeAPIView.as_view()),
    url(r'^api/request/',RequestProjectItemAPIView.as_view()),
    path('', ProjectItemsListView.as_view(), name='list'),
    path('create/',CreateProjectItemView.as_view(),name="add_project_item"),
    path('sub/create/',CreateSubProjectItemView.as_view(),name="add_sub_project_item"),
    path('request/',RequestProjectItemView.as_view(),name="request_project_item"),
    path('<int:pk>/view/', ProjectItemDetailView.as_view(), name="view_project_item"),
    path('<int:pk>/edit/', UpdateProjectItemView.as_view(), name="edit_project_item"),
    path('sub/edit/<int:pk>',UpdateSubProjectItemView.as_view(),name="edit_sub_project_item"),
    path('<int:pk>/delete/',
         RemoveProjectItemView.as_view(),
         name="remove_project_item"),
    path('sub/delete',RemoveSubProjectItemView.as_view(),name="remove_sub_project_item")
]
