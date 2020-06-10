import os
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

from common.access_decorators_mixins import admin_login_required
from django.http import HttpResponse
import json
from rest_framework_simplejwt.state import token_backend
from common.models import User

app_name = 'crm'

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
    permission_classes=(permissions.AllowAny,),
)

@admin_login_required
def admin_serve(request, path, document_root=None, show_indexes=False):
    return serve(request, path, document_root, show_indexes)

@authentication_classes(authentication.JWTAuthentication)
@permission_classes(IsAuthenticated)
def protected_serve(request, path, document_root=None, show_indexes=False):
    #return 
    #raise PermissionDenied
    #token=OutstandingToken.objects.get(token=request.META['HTTP_AUTHORIZATION'].split("Bearer")[1])
    user_id=token_backend.decode("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoic2xpZGluZyIsImV4cCI6MTU5OTEyNjk5MywianRpIjoiNmFkM2Q2MTRhYWFiNGFkNjk3Y2YzNDBiNTNlNmY2ZDkiLCJyZWZyZXNoX2V4cCI6MTU5OTEyNjk5MywidXNlcl9pZCI6Mn0.tWfyr-t4phoOcST2--ORYhcoiB6sLAtwXYVnrtBa_UI",verify=True)["user_id"]
    user=User.objects.get(pk=user_id)
    return HttpResponse(user.role)
    return serve(request, path, document_root, show_indexes)


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
    path('quotations/', include('quotations.urls', namespace="quotations")),
    path('events/', include('events.urls', namespace="events")),
    path('teams/', include('teams.urls', namespace="teams")),
    path('emails/', include('emails.urls', namespace="emails")),
    path('function_items/',include('function_items.urls',namespace="function_items")),
    # path('planner/', include('planner.urls', namespace="planner")),
    path('logout/', views.LogoutView, {'next_page': '/login/'}, name="logout"),
    path('api/',include('api.urls',namespace="api")),
    url(r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:], admin_serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    url(r'^api/%s(?P<path>.*)$' % settings.MEDIA_URL[1:], protected_serve, {'document_root': settings.MEDIA_ROOT}),
    
    

]#+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#if settings.DEBUG:
#    urlpatterns = urlpatterns + static(settings.MEDIA_URL,   document_root=settings.MEDIA_ROOT)


handler404 = handler404
handler500 = handler500
