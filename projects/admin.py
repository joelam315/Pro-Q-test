from django.contrib import admin
from projects.models import Project, ProjectHistory, ProjectInvoice, ProjectReceipt

@admin.register(Project)
class Project(admin.ModelAdmin):
    readonly_fields = ('created_on','updated_on')

admin.site.register(ProjectHistory)
admin.site.register(ProjectInvoice)
admin.site.register(ProjectReceipt)
