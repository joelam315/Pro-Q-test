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
    RemoveItemTypeMaterialView,
    ItemsListView,
    CreateItemView,
    UpdateItemView,
    ItemDetailView,
    RemoveItemView,
    CreateItemFormulaView,
    UpdateItemFormulaView,
    RemoveItemFormulaView,
    ItemPropertiesListView,
    ItemPropertyDetailView,
    CreateItemPropertyView,
    UpdateItemPropertyView,
    RemoveItemPropertyView
)

app_name = 'project_items'


urlpatterns = [
    
    path('item_type/', ItemTypesListView.as_view(), name='list_item_types'),
    path('item_type/create/',CreateItemTypeView.as_view(),name="add_item_type"),
    path('item_type/<int:pk>/view/', ItemTypeDetailView.as_view(), name="view_item_type"),
    path('item_type/<int:pk>/edit/', UpdateItemTypeView.as_view(), name="edit_item_type"),
    path('item_type/<int:pk>/delete/', RemoveItemTypeView.as_view(),name="remove_item_type"),
    path('item_type_material/create/',CreateItemTypeMaterialView.as_view(),name="add_item_type_material"),
    path('item_type_material/edit/<int:pk>',UpdateItemTypeMaterialView.as_view(),name="edit_item_type_material"),
    path('item_type_material/delete/',RemoveItemTypeMaterialView.as_view(),name="remove_item_type_material"),
    path('item/',ItemsListView.as_view(),name="list_items"),
    path('item/create/',CreateItemView.as_view(),name="add_item"),
    path('item/<int:pk>/view/',ItemDetailView.as_view(),name="view_item"),
    path('item/<int:pk>/edit/',UpdateItemView.as_view(),name="edit_item"),
    path('item/<int:pk>/delete',RemoveItemView.as_view(),name='remove_item'),
    path('item_formula/create/',CreateItemFormulaView.as_view(),name="add_item_formula"),
    path('item_formula/edit/<int:pk>',UpdateItemFormulaView.as_view(),name="edit_item_formula"),
    path('item_formula/delete/',RemoveItemFormulaView.as_view(),name="remove_item_formula"),
    path('item_property/',ItemPropertiesListView.as_view(),name='list_item_properties'),
    path('item_property/create/',CreateItemPropertyView.as_view(),name="add_item_property"),
    path('item_property/<int:pk>/view/', ItemPropertyDetailView.as_view(), name="view_item_property"),
    path('item_property/<int:pk>/edit/',UpdateItemPropertyView.as_view(),name="edit_item_property"),
    path('item_property/<int:pk>/delete/',RemoveItemPropertyView.as_view(),name="remove_item_property")
]
