from django.contrib import admin
from project_expenses.models import ExpenseType, ProjectExpense

admin.site.register(ExpenseType)
admin.site.register(ProjectExpense)
# Register your models here.
