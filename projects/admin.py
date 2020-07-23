from django.contrib import admin
from projects.models import Project, ProjectHistory

@admin.register(Project)
class Project(admin.ModelAdmin):
    readonly_fields = ('created_on','updated_on')

admin.site.register(ProjectHistory)
