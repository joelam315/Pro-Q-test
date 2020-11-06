from django.contrib import admin
from project_expenses.models import ExpenseType, ProjectExpense

admin.site.register(ExpenseType)

@admin.register(ProjectExpense)
class ProjectExpense(admin.ModelAdmin):
	list_display=["__str__","id"]

# Register your models here.
