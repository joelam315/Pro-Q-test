from django.contrib import admin
from rooms.models import RoomProperty,RoomType,RoomTypeProperties,RoomTypeFormula,Room

admin.site.register(RoomProperty)
admin.site.register(RoomType)
admin.site.register(RoomTypeProperties)
admin.site.register(RoomTypeFormula)
admin.site.register(Room)