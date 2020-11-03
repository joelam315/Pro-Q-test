from django.contrib import admin
from project_items.models import ItemProperty,ItemType,ItemTypeMaterial,Item,ItemFormula

admin.site.register(ItemProperty)
admin.site.register(ItemType)
admin.site.register(ItemTypeMaterial)

@admin.register(Item)
class Item(admin.ModelAdmin):
	list_display=['__str__','id']
	readonly_fields=('id',)

admin.site.register(ItemFormula)

