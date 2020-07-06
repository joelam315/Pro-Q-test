from django.contrib import admin
from companies.models import Company,DocumentFormat,ChargingStages

admin.site.register(Company)
admin.site.register(DocumentFormat)
admin.site.register(ChargingStages)
