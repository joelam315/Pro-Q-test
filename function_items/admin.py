from django.contrib import admin
from function_items.models import FunctionItem, FunctionItemHistory, SubFunctionItem, SubFunctionItemHistory

admin.site.register(FunctionItem)
admin.site.register(FunctionItemHistory)

admin.site.register(SubFunctionItem)
admin.site.register(SubFunctionItemHistory)
