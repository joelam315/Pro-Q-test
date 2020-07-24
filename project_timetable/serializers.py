from .models import ProjectWork, ProjectMilestone

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.core.exceptions import PermissionDenied,ObjectDoesNotExist

class CreateProjectWorkSerializer:

	class Meta:
		model=ProjectWork
		fields=("name","project","pic","start_date","end_date","description")

	def create(self,validation_data):
		user = None
		request = self.context.get("request")
		if request and hasattr(request, "user"):
			user = request.user
		company=Company.objects.get(owner=user)
		if not company:
			serializers.ValidationError("You must create a company first.")

		project=get_object_or_404(Project,id=instance)

		if user==project.company.owner:
			project_work=ProjectWork.objects.create(**validation_data)

			return project_work
		else:
			raise PermissionDenied

class UpdateProjectWorkSerializer:

	class Meta:
		model=ProjectWork
		fields=("name","pic","start_date","end_date","description")

	def update(slef,instance,validation_data):
		user = None
		request = self.context.get("request")
		if request and hasattr(request, "user"):
			user = request.user
		company=Company.objects.get(owner=user)
		if not company:
			serializers.ValidationError("You must create a company first.")

		project_work=get_object_or_404(ProjectWork,id=instance)

		if user==project_work.project.company.owner:
			if validated_data.get("name"):
				project_work.name=validated_data["name"]
			if validated_data.get("pic"):
				project_work.pic=validated_data["pic"]
			if validated_data.get("start_date"):
				project_work.start_date=validated_data["start_date"]
			if validated_data.get("end_date"):
				project_work.end_date=validated_data["end_date"]
			if validated_data.get("description"):
				project_work.description=validated_data["description"]
			project_work.save()
		else:
			raise PermissionDenied

class CreateProjectMilestoneSerializer:

	class Meta:
		model=ProjectMilestone
		fields=("name","project","pic","date","remind","description")

	def create(self,validation_data):
		user = None
		request = self.context.get("request")
		if request and hasattr(request, "user"):
			user = request.user
		company=Company.objects.get(owner=user)
		if not company:
			serializers.ValidationError("You must create a company first.")

		project=get_object_or_404(Project,id=instance)

		if user==project.company.owner:
			project_milestone=ProjectWork.objects.create(**validation_data)

			return project_milestone
		else:
			raise PermissionDenied

class UpdateProjectMilestoneSerializer:

	class Meta:
		model=ProjectMilestone
		fields=("name","pic","date","remind","description")

	def update(slef,instance,validation_data):
		user = None
		request = self.context.get("request")
		if request and hasattr(request, "user"):
			user = request.user
		company=Company.objects.get(owner=user)
		if not company:
			serializers.ValidationError("You must create a company first.")

		project_milestone=get_object_or_404(ProjectMilestone,id=instance)

		if user==project_milestone.project.company.owner:
			if validated_data.get("name"):
				project_milestone.name=validated_data["name"]
			if validated_data.get("pic"):
				project_milestone.pic=validated_data["pic"]
			if validated_data.get("date"):
				project_milestone.date=validated_data["date"]
			if validated_data.get("remind"):
				project_milestone.remind=validated_data["remind"]
			if validated_data.get("description"):
				project_milestone.description=validated_data["description"]
			project_milestone.save()
		else:
			raise PermissionDenied