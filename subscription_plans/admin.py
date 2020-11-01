from django.contrib import admin
from .models import SubscriptionPlan, CompanySubscribedPlan
from django.template.defaultfilters import escape
from django.urls import reverse
from django.utils.html import format_html

admin.site.register(SubscriptionPlan)

@admin.register(CompanySubscribedPlan)
class CompanySubscribedPlanAdmin(admin.ModelAdmin):
	list_display=['__str__','start_date','next_billing_date','company_link','plan_link']

	def company_link(self, obj):
		return format_html('<a class="related-widget-wrapper-link" href="%s?_popup=1">ID: %s %s</a>' % (reverse("admin:companies_company_change", args=(obj.company.id,)) ,escape(obj.company.id), escape(obj.company)))
	company_link.allow_tags = True
	company_link.short_description = "Company" 

	def plan_link(self, obj):
		return format_html('<a class="related-widget-wrapper-link" href="%s?_popup=1">ID: %s %s</a>' % (reverse("admin:subscription_plans_subscriptionplan_change", args=(obj.plan.id,)) ,escape(obj.plan.id), escape(obj.plan)))
	plan_link.allow_tags = True
	plan_link.short_description = "Subscription Plan" 