from django.conf.urls import include, url
from django.urls import path
from project_misc.views import (
    MiscListView,
    CreateMiscView,
    MiscDetailView,
    UpdateMiscView,
    RemoveMiscView
)

app_name = 'project_misc'


urlpatterns = [
    
    path('misc/', MiscListView.as_view(), name='list_miscs'),
    path('misc/create/',CreateMiscView.as_view(),name="add_misc"),
    path('misc/<int:pk>/view/', MiscDetailView.as_view(), name="view_misc"),
    path('misc/<int:pk>/edit/', UpdateMiscView.as_view(), name="edit_misc"),
    path('misc/<int:pk>/delete/', RemoveMiscView.as_view(),name="remove_misc"),
]
