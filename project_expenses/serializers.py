from datetime import datetime

from .models import ExpenseType,ProjectExpense

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.core.exceptions import PermissionDenied,ObjectDoesNotExist, ValidationError
from common.fields import Base64ImageField

from companies.models import Company
from projects.models import Project


class ExpenseTypeJsonSerializer(serializers.Serializer):
	id=serializers.IntegerField()
	name=serializers.CharField()

class GetExpenseTypeListResponseSerializer(serializers.Serializer):
	result=serializers.BooleanField()
	expense_types=ExpenseTypeJsonSerializer(many=True)

class CreateProjectExpenseSerializer(serializers.ModelSerializer):
	img=Base64ImageField(
		max_length=None, use_url=True,required=False,allow_null=True
	)

	class Meta:
		model=ProjectExpense
		fields=("name","project","expense_type","price","pic","remark","pay_date", "img")

	def create(self, validated_data):
		user = None
		request = self.context.get("request")
		if request and hasattr(request, "user"):
			user = request.user
		company=Company.objects.get(owner=user)
		if not company:
			raise ValidationError("You must create a company first.")

		project=validated_data["project"]

		if user==project.company.owner:
			project_expense=ProjectExpense.objects.create(**validated_data)
			if validated_data.get("img",False)!=False:
				project_expense.img_upload_date=datetime.now()
				project_expense.save()
			return project_expense
		else:
			raise PermissionDenied

class GetProjectExpenseRequestSerializer(serializers.ModelSerializer):
	class Meta:
		model=ProjectExpense
		fields=("id",)

class CreateProjectExpenseResponseSerializer(serializers.Serializer):
	result=serializers.BooleanField()
	project_expense_id=serializers.IntegerField()

class UpdateProjectExpenseSerializer(serializers.ModelSerializer):
	project_expense=serializers.IntegerField()
	img=Base64ImageField(
		max_length=None, use_url=True,required=False,allow_null=True
	)
	expense_type=serializers.IntegerField(required=False)

	class Meta:
		model=ProjectExpense
		fields=("project_expense","name","expense_type","price","pic","remark","pay_date", "img")

	def update(self,instance,validated_data):
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
				try:
					expense_type=ExpenseType.objects.get(id=validated_data["expense_type"])
				except ObjectDoesNotExist:
					raise ValidationError("Expense Type not found")
				project_expense.expense_type=expense_type
			if validated_data.get("pic"):
				project_expense.pic=validated_data["pic"]
			if validated_data.get("price"):
				project_expense.price=validated_data["price"]
			if validated_data.get("pay_date"):
				project_expense.pay_date=validated_data["pay_date"]
			if validated_data.get("remark"):
				project_expense.remark=validated_data["remark"]
			if validated_data.get("img",False)!=False:
				project_expense.img=validated_data["img"]
				project_expense.img_upload_date=datetime.now()
			elif validated_data.get("img")==None:
				project_expense.img_upload_date=None
			project_expense.save()
			return project_expense
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