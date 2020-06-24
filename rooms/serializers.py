from django import forms
from projects.models import Project
from rooms.models import Room,RoomItem
from companies.models import Company
from rest_framework import serializers
from django.core.exceptions import PermissionDenied,ObjectDoesNotExist

class CreateRoomSerializer(serializers.ModelSerializer):

	class Meta:
		model=Room
		fields=("name","room_type","value","related_project")

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
	room_id=serializers.IntegerField()
	class Meta:
		model=Room
		fields=("room_id","name","room_type","value")

	def create(self, validated_data):
		user = None
		request = self.context.get("request")
		if request and hasattr(request, "user"):
			user = request.user
		company=Company.objects.get(owner=user)
		if not company:
			serializers.ValidationError("You must create a company first.")
		#project=Project.objects.get(id=validated_data["related_project"].id)
		room=Room.objects.get(id=validated_data["room_id"])
		project=room.related_project
		if not project:
			serializers.ValidationError("Project not found.")
		if user==project.company.owner:
			room=Room.objects.get(id=validated_data["room_id"])

			room.value=validated_data.get("value",room.value)
			room.name=validated_data.get("name",room.name)
			room.room_type=validated_data.get("room_type",room.room_type)

			room.save()
			return room
		else:
			raise PermissionDenied

class SetRoomItemSerializer(serializers.ModelSerializer):
	class Meta:
		model=RoomItem
		fields=("item","room","unit_price","value","quantity")

	def create(self,validated_data):
		user = None
		request = self.context.get("request")
		if request and hasattr(request, "user"):
			user = request.user
		company=Company.objects.get(owner=user)
		if not company:
			serializers.ValidationError("You must create a company first.")
		#project=Project.objects.get(id=validated_data["related_project"].id)
		if user==validated_data["room"].related_project.company.owner:
			room_item=RoomItem.objects.update_or_create(item=validated_data["item"],room=validated_data["room"],defaults={"unit_price":validated_data["unit_price"],"value":validated_data["value"],"quantity":validated_data["quantity"]})
			return room_item[0]
		else:
			raise PermissionDenied
