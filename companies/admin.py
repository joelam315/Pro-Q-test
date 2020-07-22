from django.contrib import admin
from companies.models import Company,DocumentFormat,ChargingStages,QuotationGeneralRemark
from .forms import ChargingStagesForm

admin.site.register(Company)
admin.site.register(DocumentFormat)
admin.site.register(QuotationGeneralRemark)


@admin.register(ChargingStages)
class ChargingStagesAdmin(admin.ModelAdmin):
    form = ChargingStagesForm