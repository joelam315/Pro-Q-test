from django.urls import path
from projects.views import *
from django.conf.urls import include, url

app_name = 'projects'


urlpatterns = [
    path('', projects_list, name='projects_list'),
    path('create/', projects_create, name='projects_create'),
    path('detail/<int:project_id>/', project_details, name='project_details'),
    path('history/<int:project_history_id>/', project_history_details, name='project_history_details'),
    path('edit/<int:project_id>/', project_edit, name='project_edit'),
    path('delete/<int:project_id>/', project_delete, name='project_delete'),
    path('download/<int:project_id>/', project_download, name='project_download'),
    path('send-mail/<int:project_id>/', project_send_mail, name='project_send_mail'),
    path('cancelled-mail/<int:project_id>/', project_change_status_cancelled, name='project_change_status_cancelled'),
    path('paid-mail/<int:project_id>/', project_change_status_paid, name='project_change_status_paid'),

    path('comment/add/', AddCommentView.as_view(), name="add_comment"),
    path('comment/edit/', UpdateCommentView.as_view(), name="edit_comment"),
    path('comment/remove/', DeleteCommentView.as_view(), name="remove_comment"),

    path('attachment/add/', AddAttachmentView.as_view(), name="add_attachment"),
    path('attachment/remove/', DeleteAttachmentsView.as_view(),
         name="remove_attachment"),

    url(r'api/list/',projects_list_api),
    url(r'api/details/',projects_details_api),
    url(r'api/create/',projects_create_api),
]
