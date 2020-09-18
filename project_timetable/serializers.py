from .models import ProjectWork, ProjectMilestone
from companies.models import Company
from projects.models import Project
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.core.exceptions import PermissionDenied,ObjectDoesNotExist
from common.fields import Base64ImageField


class GetProjectWorkRequestSerializer(serializers.ModelSerializer):
	class Meta:
		model=ProjectWork
		fields=("id",)

class CreateProjectWorkSerializer(serializers.ModelSerializer):

	class Meta:
		model=ProjectWork
		fields=("name","project","pic","start_date","end_date","description")

	def create(self,validated_data):
		user = None
		request = self.context.get("request")
		if request and hasattr(request, "user"):
			user = request.user
		company=Company.objects.get(owner=user)
		if not company:
			serializers.ValidationError("You must create a company first.")

		project=validated_data["project"]

		if user==project.company.owner:
			project_work=ProjectWork.objects.create(**validated_data)

			return project_work
		else:
			raise PermissionDenied

class UpdateProjectWorkSerializer(serializers.ModelSerializer):
	project_work=serializers.IntegerField(required=True)
	class Meta:
		model=ProjectWork
		fields=("project_work","name","pic","start_date","end_date","description")

	def update(self,instance,validated_data):
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
			return project_work
		else:
			raise PermissionDenied

class GetProjectMilestoneRequestSerializer(serializers.ModelSerializer):
	class Meta:
		model=ProjectMilestone
		fields=("id",)

class CreateProjectMilestoneSerializer(serializers.ModelSerializer):
	img=Base64ImageField(
		max_length=None, use_url=True,required=False,allow_null=True
	)
	class Meta:
		model=ProjectMilestone
		fields=("name","project","pic","date","remind","description", "img")

	def create(self,validated_data):
		user = None
		request = self.context.get("request")
		if request and hasattr(request, "user"):
			user = request.user
		company=Company.objects.get(owner=user)
		if not company:
			raise ValidationError("You must create a company first.")

		project=validated_data["project"]

		if user==project.company.owner:
			project_milestone=ProjectMilestone.objects.create(**validated_data)

			return project_milestone
		else:
			raise PermissionDenied

class UpdateProjectMilestoneSerializer(serializers.ModelSerializer):
	project_milestone=serializers.IntegerField(required=True)
	img=Base64ImageField(
		max_length=None, use_url=True,required=False,allow_null=True
	)
	class Meta:
		model=ProjectMilestone
		fields=("project_milestone","name","pic","date","remind","description", "img")

	def update(self,instance,validated_data):
		user = None
		request = self.context.get("request")
		if request and hasattr(request, "user"):
			user = request.user
		company=Company.objects.get(owner=user)
		if not company:
			raise ValidationError("You must create a company first.")

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
			if validated_data.get("img",False)!=False:
				project_milestone.img=validated_data["img"]
			project_milestone.save()
			return project_milestone
		else:
			raise PermissionDenied

class CreateProjectWorkResponseSerializer(serializers.Serializer):
	result=serializers.BooleanField()
	project_work_id=serializers.IntegerField()

class CreateProjectMilestoneResponseSerializer(serializers.Serializer):
	result=serializers.BooleanField()
	project_milestone_id=serializers.IntegerField()

class ProjectWorkJsonSerializer(serializers.Serializer):
	name=serializers.CharField()
	type=serializers.CharField()
	pic=serializers.CharField()
	start_date=serializers.DateField()
	end_date=serializers.DateField()
	description=serializers.CharField()

class ProjectMilestoneJsonSerializer(serializers.Serializer):
	name=serializers.CharField()
	type=serializers.CharField()
	pic=serializers.CharField()
	date=serializers.DateField()
	remind=serializers.DurationField()
	description=serializers.CharField()
	image_path=serializers.CharField()

class GetProjectTimetableResponseSerializer(serializers.Serializer):
	result=serializers.BooleanField()
	project_works=ProjectWorkJsonSerializer(many=True)
	project_milestones=ProjectMilestoneJsonSerializer(many=True)