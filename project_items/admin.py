from django.contrib import admin
from project_items.models import ProjectItem, ProjectItemHistory, SubProjectItem, SubProjectItemHistory

admin.site.register(ProjectItem)
admin.site.register(ProjectItemHistory)

admin.site.register(SubProjectItem)
admin.site.register(SubProjectItemHistory)
