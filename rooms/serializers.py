from django import forms
from projects.models import Project
from project_items.models import ItemFormula
from project_items.serializers import ProjectItemJsonSerializer
from rooms.models import Room,RoomItem,RoomTypeProperties, RoomTypeFormula
from companies.models import Company
from rest_framework import serializers
from django.core.exceptions import PermissionDenied,ObjectDoesNotExist,ValidationError
import json
import numpy as np
import numexpr as ne

class GetRoomRequestSerializer(serializers.Serializer):
	id=serializers.IntegerField()

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
			raise ValidationError("You must create a company first.")
		project=Project.objects.get(id=validated_data["related_project"].id)
		if not project:
			raise ObjectDoesNotExist
		_value={}
		room_properties=RoomTypeProperties.objects.get(room_type=validated_data["room_type"]).room_properties
		if validated_data["value"]:
			for room_property in room_properties.all():
				if room_property.name in validated_data["value"]:
					_value[room_property.name]=validated_data["value"][room_property.name]
				else:
					raise ValidationError("Room value missing: "+room_property.name)
		validated_data["value"]=_value
		if user==project.company.owner:
			room=Room.objects.create(**validated_data)
			return room
		else:
			raise PermissionDenied

class CreateRoomResponseSerializer(serializers.Serializer):
	result=serializers.BooleanField()
	room_id=serializers.IntegerField()

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
			raise ValidationError("You must create a company first.")
		#project=Project.objects.get(id=validated_data["related_project"].id)
		room=Room.objects.get(id=validated_data["room_id"])
		project=room.related_project
		if not project:
			raise ValidationError("Project not found.")
		if user==project.company.owner:
			room=Room.objects.get(id=validated_data["room_id"])
			_value={}
			room_properties=RoomTypeProperties.objects.get(room_type=room.room_type).room_properties
			if validated_data.get("value"):
				for room_property in room_properties.all():
					if room_property.name in validated_data["value"]:
						_value[room_property.name]=validated_data["value"][room_property.name]
					else:
						raise ValidationError("Room value missing: "+room_property.name)
			room.value=_value if validated_data.get("value") else room.value
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
			raise ValidationError("You must create a company first.")
		#project=Project.objects.get(id=validated_data["related_project"].id)
		if user==validated_data["room"].related_project.company.owner:
			data={}
			data["unit_price"]=validated_data["unit_price"]
			_value={}
			if validated_data["value"]:
				for item_property in validated_data["item"].item_properties.all():
					if item_property.name in validated_data["value"]:
						_value[item_property.name]=validated_data["value"][item_property.name]
					else:
						raise ValidationError("Item value missing: "+item_property.name)
			data["value"]=_value
			data["quantity"]=validated_data["quantity"]
			room_item=RoomItem.objects.update_or_create(item=validated_data["item"],room=validated_data["room"],defaults=data)
			return room_item[0]
		else:
			raise PermissionDenied

class GetRoomItemRequestSerializer(serializers.ModelSerializer):
	class Meta:
		model=RoomItem
		fields=("id",)

class PreCalRoomItemFormulaSerializer(serializers.ModelSerializer):
	value=serializers.JSONField(required=True)

	class Meta:
		model = RoomItem
		fields=["item","room","material","value"]

	def create(self,validated_data):
		user = None
		request = self.context.get("request")
		if request and hasattr(request, "user"):
			user = request.user

		if validated_data["room"].related_project.company.owner==user:
			if not validated_data.get("material") or validated_data.get("material").item_type==validated_data["item"].item_type:
				formulas=ItemFormula.objects.filter(item=validated_data["item"])
				rfps={rfp.name:rfp.cal(validated_data["room"].value) for rfp in RoomTypeFormula.objects.filter(room_type=validated_data["room"].room_type)}
				vbp=validated_data.get("material").value_based_price if validated_data.get("material") and validated_data.get("material").value_based_price else (validated_data["item"].value_based_price if validated_data["item"].value_based_price else 0)
				ret={}
				for formula in formulas:
					ret[formula.name]=formula.cal(value=validated_data["value"],rfps=rfps,vbp=vbp)
				return ret
			else:
				raise ValidationError("Material not match to this item.")
		else:
			raise PermissionDenied

class RoomItemJsonSerializer(serializers.Serializer):
	id=serializers.IntegerField()
	name=serializers.CharField()
	unit_price=serializers.FloatField()
	room=serializers.CharField()
	quantity=serializers.IntegerField()
	value=serializers.JSONField()
	remark=serializers.CharField()

class ProjectItemByRoomJsonSerializer(serializers.Serializer):
	items=RoomItemJsonSerializer(many=True)

class ProjectRoomItemJsonSerializer(serializers.Serializer):
	id=serializers.IntegerField()
	name=serializers.CharField()
	unit_price=serializers.FloatField()
	room=serializers.CharField()
	quantity=serializers.IntegerField()
	value=serializers.DictField(child=serializers.FloatField())
	remark=serializers.CharField()

class ProjectRoomJsonSerializer(serializers.Serializer):
	id=serializers.IntegerField()
	name=serializers.CharField()
	room_project_items_count=serializers.IntegerField()


class GetProjectRoomListResponseSerializer(serializers.Serializer):
	result=serializers.BooleanField()
	rooms=ProjectRoomJsonSerializer(many=True)

class ProjectRoomDetailsSerializer(serializers.Serializer):
	name=serializers.CharField()
	value=serializers.DictField(child=serializers.FloatField())
	room_type=serializers.CharField()
	room_project_items=ProjectRoomItemJsonSerializer(many=True)
	properties=serializers.DictField(child=serializers.FloatField())

class GetProjectRoomDetailsResponseSerializer(serializers.Serializer):
	result=serializers.BooleanField()
	room=ProjectRoomDetailsSerializer()

class SetProjectRoomItemResponseSerializer(serializers.Serializer):
	result=serializers.BooleanField()
	room_item_id=serializers.IntegerField()

class PreCalProjectRoomItemFormulaResponseSerializer(serializers.Serializer):
	result=serializers.BooleanField()
	formula=serializers.DictField(child=serializers.FloatField())

class RoomTypeJsonSerializer(serializers.Serializer):
	id=serializers.IntegerField()
	name=serializers.CharField()

class GetRoomTypeListResponseSerializer(serializers.Serializer):
	result=serializers.BooleanField()
	room_type=RoomTypeJsonSerializer(many=True)

class GetRoomRelatedItemResponseSerializer(serializers.Serializer):
	result=serializers.BooleanField()
	related_items=ProjectItemJsonSerializer(many=True)