from django.conf.urls import include, url
from django.urls import path
from project_expenses.views import (
    ExpenseTypeListView,
    CreateExpenseTypeView,
    ExpenseTypeDetailView,
    UpdateExpenseTypeView,
    RemoveExpenseTypeView
)

app_name = 'project_expense_type'


urlpatterns = [
    
    path('project_expenses/expense_type/', ExpenseTypeListView.as_view(), name='list_expense_types'),
    path('project_expenses/expense_type/create/',CreateExpenseTypeView.as_view(),name="add_expense_type"),
    path('project_expenses/expense_type/<int:pk>/view/', ExpenseTypeDetailView.as_view(), name="view_expense_type"),
    path('project_expenses/expense_type/<int:pk>/edit/', UpdateExpenseTypeView.as_view(), name="edit_expense_type"),
    path('project_expenses/expense_type/<int:pk>/delete/', RemoveExpenseTypeView.as_view(),name="remove_expense_type"),
]
