from django import forms
from projects.models import Project
from rooms.models import Room
from companies.models import Company
from rest_framework import serializers
from django.core.exceptions import PermissionDenied,ObjectDoesNotExist

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