import os
import logging
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views
from django.conf.urls import url
from django.urls import include, path
from common.views import handler404, handler500
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib import admin
from django.views.static import serve
from rest_framework.permissions import (IsAuthenticated,)
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework_simplejwt import authentication

from django.core.exceptions import PermissionDenied, ObjectDoesNotExist

from common.access_decorators_mixins import admin_login_required, app_login_required, AdminAccessRequiredMixin
from django.http import HttpResponse
import json
from companies.models import Company
from common.constants import FETCH_URL_NAME
from common.views import FetchView
app_name = 'crm'

logger = logging.getLogger(__name__)

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.IsAdminUser,),
)

@admin_login_required
def admin_serve(request, path, document_root=None, show_indexes=False):
    return serve(request, path, document_root, show_indexes)

@app_login_required
def protected_serve(request, path, document_root=None, show_indexes=False):
    #return 
    #raise PermissionDenied
    #token=OutstandingToken.objects.get(token=request.META['HTTP_AUTHORIZATION'].split("Bearer")[1])
    #return HttpResponse(request.META['HTTP_AUTHORIZATION'].split("Bearer")[1])

    _type,_identity,_param=path.split('/',2)
    if _type=="companies":
        try:
            company=Company.objects.get(id=_identity)
            if company.owner==request.user:
                return serve(request, path, document_root, show_indexes)
            else:
                raise PermissionDenied
        except ObjectDoesNotExist:
            raise PermissionDenied

    raise PermissionDenied
 


        


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('', include('common.urls', namespace="common")),
    path('', include('django.contrib.auth.urls')),
    path('marketing/', include('marketing.urls', namespace="marketing")),
    path('accounts/', include('accounts.urls', namespace="accounts")),
    path('companies/', include('companies.urls', namespace="companies")),
    path('leads/', include('leads.urls', namespace="leads")),
    path('contacts/', include('contacts.urls', namespace="contacts")),
    path('opportunities/',
         include('opportunity.urls', namespace="opportunities")),
    path('cases/', include('cases.urls', namespace="cases")),
    path('tasks/', include('tasks.urls', namespace="tasks")),
    path('invoices/', include('invoices.urls', namespace="invoices")),
    #path('quotations/', include('quotations.urls', namespace="quotations")),
    path('events/', include('events.urls', namespace="events")),
    path('teams/', include('teams.urls', namespace="teams")),
    path('emails/', include('emails.urls', namespace="emails")),
    path('project_items/',include('project_items.urls',namespace="project_items")),
    path('project_misc/',include('project_misc.urls',namespace="project_misc")),
    path('project_expenses/',include('project_expenses.urls',namespace="project_expenses")),
    path('rooms/',include('rooms.urls',namespace="rooms")),
    #path('function_items/',include('function_items.urls',namespace="function_items")),
    # path('planner/', include('planner.urls', namespace="planner")),
    path('logout/', views.LogoutView, {'next_page': '/login/'}, name="logout"),
    path('api/',include('api.urls',namespace="api")),
    #url(r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:], admin_serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^%s/(?P<path>.*)$' % FETCH_URL_NAME,FetchView.as_view(),name=FETCH_URL_NAME),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    #url(r'^api/%s(?P<path>.*)$' % settings.MEDIA_URL[1:], protected_serve, {'document_root': settings.MEDIA_ROOT}),
    
    

]#+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#if settings.DEBUG:
#    urlpatterns = urlpatterns + static(settings.MEDIA_URL,   document_root=settings.MEDIA_ROOT)


handler404 = handler404
handler500 = handler500
