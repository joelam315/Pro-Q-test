from django.contrib import admin
from companies.models import Company,DocumentFormat,DocumentHeaderInformation,ChargingStages,QuotationGeneralRemark,InvoiceGeneralRemark,ReceiptGeneralRemark
from .forms import ChargingStagesForm

admin.site.register(Company)
admin.site.register(DocumentFormat)
admin.site.register(DocumentHeaderInformation)
admin.site.register(QuotationGeneralRemark)
admin.site.register(InvoiceGeneralRemark)
admin.site.register(ReceiptGeneralRemark)


@admin.register(ChargingStages)
class ChargingStagesAdmin(admin.ModelAdmin):
    form = ChargingStagesForm