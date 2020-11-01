from django.conf.urls import include, url
from django.urls import path
from rooms.views import (
    RoomTypesListView,
    CreateRoomTypeView,
    RoomTypeDetailView,
    UpdateRoomTypeView,
    RemoveRoomTypeView,
    CreateRoomTypeFormulaView,
    UpdateRoomTypeFormulaView,
    RemoveRoomTypeFormulaView,
    RoomPropertiesListView,
    RoomPropertyDetailView,
    CreateRoomPropertyView,
    UpdateRoomPropertyView,
    RemoveRoomPropertyView
)

app_name = 'rooms'


urlpatterns = [
    
    path('room_type/', RoomTypesListView.as_view(), name='list_room_types'),
    path('room_type/create/',CreateRoomTypeView.as_view(),name="add_room_type"),
    path('room_type/<int:pk>/view/', RoomTypeDetailView.as_view(), name="view_room_type"),
    path('room_type/<int:pk>/edit/', UpdateRoomTypeView.as_view(), name="edit_room_type"),
    path('room_type/<int:pk>/delete/', RemoveRoomTypeView.as_view(),name="remove_room_type"),
    path('room_type_formula/create/',CreateRoomTypeFormulaView.as_view(),name="add_room_type_formula"),
    path('room_type_formula/edit/<int:pk>',UpdateRoomTypeFormulaView.as_view(),name="edit_room_type_formula"),
    path('room_type_formula/delete/',RemoveRoomTypeFormulaView.as_view(),name="remove_room_type_formula"),
    path('room_property/',RoomPropertiesListView.as_view(),name='list_room_properties'),
    path('room_property/create/',CreateRoomPropertyView.as_view(),name="add_room_property"),
    path('room_property/<int:pk>/view/', RoomPropertyDetailView.as_view(), name="view_room_property"),
    path('room_property/<int:pk>/edit/',UpdateRoomPropertyView.as_view(),name="edit_room_property"),
    path('room_property/<int:pk>/delete/',RemoveRoomPropertyView.as_view(),name="remove_room_property")
]
