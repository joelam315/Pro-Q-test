from django.contrib import admin
from projects.models import Project, ProjectHistory

admin.site.register(Project)
admin.site.register(ProjectHistory)
