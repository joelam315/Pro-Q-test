from django.contrib import admin
from rooms.models import RoomProperty,RoomType,RoomTypeFormula,Room,RoomItem
from django.template.defaultfilters import escape
from django.urls import reverse
from django.utils.html import format_html

admin.site.register(RoomProperty)
admin.site.register(RoomType)
admin.site.register(RoomTypeFormula)

@admin.register(Room)
class Room(admin.ModelAdmin):
	list_display=['__str__','id','project_link']
	readonly_fields=('id',)

	def project_link(self, obj):
		return format_html('<a class="related-widget-wrapper-link" href="%s?_popup=1">ID: %s %s</a>' % (reverse("admin:projects_project_change", args=(obj.related_project.id,)) ,escape(obj.related_project.id), escape(obj.related_project)))
	project_link.allow_tags = True
	project_link.short_description = "Related Project" 

admin.site.register(RoomItem)