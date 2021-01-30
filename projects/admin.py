from django.contrib import admin
from projects.models import Project, ProjectHistory, ProjectInvoice, ProjectReceipt, ProjectImage,ProjectImageSet
from django.template.defaultfilters import escape
from django.urls import reverse
from django.utils.html import format_html

@admin.register(Project)
class Project(admin.ModelAdmin):
	list_display = ['__str__','id','owner_link']
	readonly_fields = ('id','created_on','updated_on')

	def owner_link(self, obj):
		return format_html('<a class="related-widget-wrapper-link" href="%s?_popup=1">%s</a>' % (reverse("admin:common_user_change", args=(obj.company.owner.id,)) , escape(obj.company.owner)))
	owner_link.allow_tags = True
	owner_link.short_description = "Company Owner" 

admin.site.register(ProjectHistory)
admin.site.register(ProjectInvoice)
admin.site.register(ProjectReceipt)
admin.site.register(ProjectImage)
admin.site.register(ProjectImageSet)
