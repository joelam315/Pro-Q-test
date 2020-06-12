from django import forms
from projects.models import Project
from companies.models import Company
from customers.models import Customer
from rest_framework import serializers
from django.core.exceptions import PermissionDenied,ObjectDoesNotExist

class SetProjectCustomerSerializer(serializers.ModelSerializer):

	class Meta:
		model=Customer
		fields=("name","company_name","email","phone","address","project")

	def create(self,validated_data):
		user = None
		request = self.context.get("request")
		if request and hasattr(request, "user"):
			user = request.user
		company=Company.objects.get(owner=user)
		if not company:
			serializers.ValidationError("You must create a company first.")
		project=Project.objects.get(id=2)
		if user==project.company.owner:
			info={}
			if validated_data.get("name"):
				info.update(name=validated_data["name"])
			if validated_data.get("company_name"):
				info.update(company_name=validated_data["company_name"])
			if validated_data.get("email"):
				info.update(email=validated_data["email"])
			if validated_data.get("phone"):
				info.update(phone=validated_data["phone"])
			customer=Customer.objects.update_or_create(
				project=project,
				defaults={"name":validated_data["name"]}
			)[0]
			return customer
		else:
			raise PermissionDenied

