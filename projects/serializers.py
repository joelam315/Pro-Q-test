from django import forms
from projects.models import Project, Room
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

class CreateRoomSerializer(serializers.ModelSerializer):

	class Meta:
		model=Room
		fields=("name","length","width","height","related_project")

	def create(self, validated_data):
		user = None
		request = self.context.get("request")
		if request and hasattr(request, "user"):
			user = request.user
		company=Company.objects.get(owner=user)
		if not company:
			serializers.ValidationError("You must create a company first.")
		project=Project.objects.get(id=validated_data["related_project"].id)
		if not project:
			serializers.ValidationError("Project not found.")
		if user==project.company.owner:
			room=Room.objects.create(**validated_data)
			return room
		else:
			raise PermissionDenied

class UpdateRoomSerializer(serializers.ModelSerializer):
	name=serializers.CharField(max_length=50,required=False)
	length=serializers.IntegerField(min_value=0,required=False)
	width=serializers.IntegerField(min_value=0,required=False)
	height=serializers.IntegerField(min_value=0,required=False)

	class Meta:
		model=Room
		fields=("id","name","length","width","height")

	def update(self,instance,validated_data):
		user = None
		request = self.context.get("request")
		if request and hasattr(request, "user"):
			user = request.user
		room=Room.objects.get(id=instance)
		if not room:
			serializers.ValidationError("Room not found.")
		if room.related_project.company.owner==user:
			room.name=validated_data.get("name",room.name)
			room.length=validated_data.get("length",room.length)
			room.width=validated_data.get("width",room.width)
			room.height=validated_data.get("height",room.height)
			room.save()
			return room
		else:
			raise PermissionDenied
		

