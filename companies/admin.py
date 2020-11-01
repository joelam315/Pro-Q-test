from django.contrib import admin
from companies.models import Company,DocumentFormat,DocumentHeaderInformation,ChargingStages,QuotationGeneralRemark,InvoiceGeneralRemark,ReceiptGeneralRemark
from .forms import ChargingStagesForm
from django.template.defaultfilters import escape
from django.urls import reverse
from django.utils.html import format_html

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
	list_display=["__str__","id","owner_link"]
	readonly_fields = ('id',)

	def owner_link(self, obj):
		return format_html('<a class="related-widget-wrapper-link" href="%s?_popup=1">%s</a>' % (reverse("admin:common_user_change", args=(obj.owner.id,)) , escape(obj.owner)))
	owner_link.allow_tags = True
	owner_link.short_description = "Company Owner" 

admin.site.register(DocumentFormat)
admin.site.register(DocumentHeaderInformation)
admin.site.register(QuotationGeneralRemark)
admin.site.register(InvoiceGeneralRemark)
admin.site.register(ReceiptGeneralRemark)


@admin.register(ChargingStages)
class ChargingStagesAdmin(admin.ModelAdmin):
    form = ChargingStagesForm