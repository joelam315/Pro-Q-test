from django.contrib import admin
from rooms.models import RoomProperty,RoomType,RoomTypeProperty,RoomTypeFormula,Room

admin.site.register(RoomProperty)
admin.site.register(RoomType)
admin.site.register(RoomTypeProperty)
admin.site.register(RoomTypeFormula)
admin.site.register(Room)