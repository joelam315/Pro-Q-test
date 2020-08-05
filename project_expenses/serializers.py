from .models import ExpenseType,ProjectExpense

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.core.exceptions import PermissionDenied,ObjectDoesNotExist, ValidationError

class ExpenseTypeJsonSerializer(serializers.Serializer):
	id=serializers.IntegerField()
	name=serializers.CharField()

class GetExpenseTypeListResponseSerializer(serializers.Serializer):
	result=serializers.BooleanField()
	expense_types=ExpenseTypeJsonSerializer(many=True)

class CreateProjectExpenseSerializer(serializers.ModelSerializer):

	class Meta:
		model=ProjectExpense
		fields=("name","project","expense_type","price","pic","remark","pay_date")

	def create(self, validation_data):
		user = None
		request = self.context.get("request")
		if request and hasattr(request, "user"):
			user = request.user
		company=Company.objects.get(owner=user)
		if not company:
			raise ValidationError("You must create a company first.")

		project=get_object_or_404(Project,id=instance)

		if user==project.company.owner:
			project_expense=ProjectExpense.objects.create(**validation_data)

			return project_milestone
		else:
			raise PermissionDenied


class CreateProjectExpenseResponseSerializer(serializers.Serializer):
	result=serializers.BooleanField()
	project_expense_id=serializers.IntegerField()

class UpdateProjectExpenseSerializer(serializers.ModelSerializer):

	class Meta:
		model=ProjectExpense
		fields=("name","expense_type","price","pic","remark","pay_date")

	def update(self,instance,validation_data):
		user = None
		request = self.context.get("request")
		if request and hasattr(request, "user"):
			user = request.user
		company=Company.objects.get(owner=user)
		if not company:
			raise ValidationError("You must create a company first.")

		project_expense=get_object_or_404(ProjectExpense,id=instance)

		if user==project_expense.project.company.owner:
			if validated_data.get("name"):
				project_expense.name=validated_data["name"]
			if validated_data.get("expense_type"):
				project_expense.expense_type=validated_data["expense_type"]
			if validated_data.get("pic"):
				project_expense.pic=validated_data["pic"]
			if validated_data.get("pay_date"):
				project_expense.pay_date=validated_data["pay_date"]
			if validated_data.get("remark"):
				project_expense.remark=validated_data["remark"]
			project_expense.save()
		else:
			raise PermissionDenied

class ProjectExpenseJsonSerializer(serializers.Serializer):
	id=serializers.IntegerField()
	name=serializers.CharField()
	expense_type=ExpenseTypeJsonSerializer()
	price=serializers.FloatField()
	pic=serializers.CharField()
	remark=serializers.CharField()
	pay_date=serializers.DateField()