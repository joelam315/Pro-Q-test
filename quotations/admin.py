from django.contrib import admin
from quotations.models import Quotation, QuotationHistory

admin.site.register(Quotation)
admin.site.register(QuotationHistory)
