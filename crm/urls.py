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

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = handler404
handler500 = handler500
