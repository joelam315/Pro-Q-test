from django import forms
from django.shortcuts import get_object_or_404
from projects.models import Project
from datetime import datetime
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
		ccss=company.company_charging_stages
		cs=[]
		for i in range(ccss.quantity):
			r={}
			r["value"]=ccss.values[i]
			if ccss.descriptions[i]!=None and ccss.descriptions[i]!="":
				r["description"]=ccss.descriptions[i]
			cs.append(r)
		cdf=company.company_doc_format
		df={
			"quot_upper_format":cdf.quot_upper_format,
			"quot_middle_format":cdf.quot_middle_format,
			"quot_lower_format":cdf.quot_lower_format,
			"invoice_upper_format":cdf.invoice_upper_format,
			"invoice_middle_format":cdf.invoice_middle_format,
			"invoice_lower_format":cdf.invoice_lower_format,
			"receipt_upper_format":cdf.receipt_upper_format,
			"receipt_middle_format":cdf.receipt_middle_format,
			"receipt_lower_format":cdf.receipt_lower_format
		}

		project=Project.objects.create(project_title=validated_data["project_title"],
			district=validated_data["district"],
			company=company,
			charging_stages=cs,
			document_format=df,
			created_by=user,
			job_no=company.job_no
		)
		company.job_no+=1
		company.save()
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

class UpdateProjectSerializer(serializers.ModelSerializer):
	class Meta:
		model=Project
		fields=("project_title","district","work_location","status","start_date","due_date")

	def update(self, instance,validated_data):
		user = None
		request = self.context.get("request")
		if request and hasattr(request, "user"):
			user = request.user
		company=Company.objects.get(owner=user)
		if not company:
			serializers.ValidationError("You must create a company first.")

		project=get_object_or_404(Project,id=instance)

		if user==project.company.owner:

			if validated_data.get("project_title"):
				project.work_location=validated_data["project_title"]
			if validated_data.get("district"):
				project.work_location=validated_data["district"]
			if validated_data.get("work_location"):
				project.work_location=validated_data["work_location"]
			if validated_data.get("status"):
				project.status=validated_data["status"]
			if validated_data.get("start_date"):
				project.start_date=validated_data["start_date"]
			if validated_data.get("due_date"):
				project.due_date=validated_data["due_date"]
			project.updated_on=datetime.now()
			project.save()
			return project
		else:
			raise PermissionDenied


