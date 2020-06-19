from django import forms
from projects.models import Project
from companies.models import Company
from customers.models import Customer
from rest_framework import serializers
from django.core.exceptions import PermissionDenied,ObjectDoesNotExist

class CreateProjectSerializer(serializers.ModelSerializer):

	class Meta:
		model=Project
		fields=("project_title","district","work_location","status","start_date","due_date")

	def create(self, validated_data):
		user = None
		request = self.context.get("request")
		if request and hasattr(request, "user"):
			user = request.user
		company=Company.objects.get(owner=user)
		if not company:
			serializers.ValidationError("You must create a company first.")
		project=Project.objects.create(project_title=validated_data["project_title"],
			district=validated_data["district"],
			company=company
		)
		if validated_data.get("work_location"):
			project.work_location=validated_data["work_location"]
		if validated_data.get("status"):
			project.status=validated_data["status"]
		if validated_data.get("start_date"):
			project.start_date=validated_data["start_date"]
		if validated_data.get("due_date"):
			project.due_date=validated_data["due_date"]
		project.save()
		return project


