from django.contrib import admin
from companies.models import Company,DocumentFormat,ChargingStages,GeneralRemark
from .forms import ChargingStagesForm

admin.site.register(Company)
admin.site.register(DocumentFormat)
admin.site.register(GeneralRemark)


@admin.register(ChargingStages)
class ChargingStagesAdmin(admin.ModelAdmin):
    form = ChargingStagesForm