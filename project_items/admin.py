from django.contrib import admin
from project_items.models import ItemProperty,ItemType,ItemTypeMaterial,Item,ItemFormula

admin.site.register(ItemProperty)
admin.site.register(ItemType)
admin.site.register(ItemTypeMaterial)
admin.site.register(Item)
admin.site.register(ItemFormula)

