from django.urls import path
from quotations.views import *
from django.conf.urls import include, url

app_name = 'quotations'


urlpatterns = [
    path('', quotations_list, name='quotations_list'),
    path('create/', quotations_create, name='quotations_create'),
    path('detail/<int:quotation_id>/', quotation_details, name='quotation_details'),
    path('history/<int:quotation_history_id>/', quotation_history_details, name='quotation_history_details'),
    path('edit/<int:quotation_id>/', quotation_edit, name='quotation_edit'),
    path('delete/<int:quotation_id>/', quotation_delete, name='quotation_delete'),
    path('download/<int:quotation_id>/', quotation_download, name='quotation_download'),
    path('send-mail/<int:quotation_id>/', quotation_send_mail, name='quotation_send_mail'),
    path('cancelled-mail/<int:quotation_id>/', quotation_change_status_cancelled, name='quotation_change_status_cancelled'),
    path('paid-mail/<int:quotation_id>/', quotation_change_status_paid, name='quotation_change_status_paid'),

    path('comment/add/', AddCommentView.as_view(), name="add_comment"),
    path('comment/edit/', UpdateCommentView.as_view(), name="edit_comment"),
    path('comment/remove/', DeleteCommentView.as_view(), name="remove_comment"),

    path('attachment/add/', AddAttachmentView.as_view(), name="add_attachment"),
    path('attachment/remove/', DeleteAttachmentsView.as_view(),
         name="remove_attachment"),

    url(r'api/list/',quotations_list_api),
    url(r'api/details/',quotations_details_api),
    url(r'api/create/',quotations_create_api),
]
