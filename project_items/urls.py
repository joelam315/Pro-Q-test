from django.conf.urls import include, url
from django.urls import path
from project_items.views import (
    ItemTypesListView,
    CreateItemTypeView,
    ItemTypeDetailView,
    UpdateItemTypeView,
    RemoveItemTypeView,
    CreateItemTypeMaterialView,
    UpdateItemTypeMaterialView,
    RemoveItemTypeMaterialView)

app_name = 'project_items'


urlpatterns = [

    path('item_type/', ItemTypesListView.as_view(), name='list_item_types'),
    path('item_type/create/',CreateItemTypeView.as_view(),name="add_item_type"),
    path('item_type/<int:pk>/view/', ItemTypeDetailView.as_view(), name="view_item_type"),
    path('item_type/<int:pk>/edit/', UpdateItemTypeView.as_view(), name="edit_item_type"),
    path('item_type/<int:pk>/delete/', RemoveItemTypeView.as_view(),name="remove_item_type"),
    path('item_type_material/create/',CreateItemTypeMaterialView.as_view(),name="add_item_type_material"),
    path('item_type_material/edit/<int:pk>',UpdateItemTypeMaterialView.as_view(),name="edit_item_type_material"),
    path('item_type_material/delete/',RemoveItemTypeMaterialView.as_view(),name="remove_item_type_material")
]
