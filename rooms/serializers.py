from django import forms
from projects.models import Project
from project_items.models import ItemFormula
from project_items.serializers import ProjectItemJsonSerializer
from rooms.models import Room,RoomItem,RoomType, RoomTypeFormula
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
		#room_properties=RoomType.objects.get(id=validated_data["room_type"]).room_properties
		room_properties=validated_data["room_type"].room_properties
		if validated_data["value"]:
			for room_property in room_properties.all():
				if room_property.symbol in validated_data["value"]:
					_value[room_property.symbol]=json.loads(validated_data["value"])[room_property.symbol]
				else:
					raise ValidationError("Room value missing: "+room_property.symbol)
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
			room_properties=RoomType.objects.get(id=room.room_type).room_properties
			if validated_data.get("value"):
				for room_property in room_properties.all():
					if room_property.symbol in validated_data["value"]:
						_value[room_property.symbol]=validated_data["value"][room_property.symbol]
					else:
						raise ValidationError("Room value missing: "+room_property.symbol)
			room.value=_value if validated_data.get("value") else room.value
			room.name=validated_data.get("name",room.name)
			room.room_type=validated_data.get("room_type",room.room_type)

			room.save()
			return room
		else:
			raise PermissionDenied

class SetRoomItemSerializer(serializers.ModelSerializer):
	room_item_id=serializers.IntegerField(required=False)
	class Meta:
		model=RoomItem
		fields=("room_item_id","item","room","material","unit_price","value","quantity","remark")

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
					if item_property.symbol in validated_data["value"]:
						_value[item_property.symbol]=json.loads(validated_data["value"])[item_property.symbol]
					else:
						raise ValidationError("Item value missing: "+item_property.symbol)
			#data["value"]=_value
			data["quantity"]=validated_data["quantity"]
			if validated_data.get("remark"):
				data["remark"]=validated_data["remark"]
			room_item=RoomItem.objects.update_or_create(item=validated_data["item"],room=validated_data["room"],material=validated_data["material"],value=_value, defaults=data)
			return room_item[0]
		else:
			raise PermissionDenied

	def update(self,instance,validated_data):
		user = None
		request = self.context.get("request")
		if request and hasattr(request, "user"):
			user = request.user
		company=Company.objects.get(owner=user)
		if not company:
			raise ValidationError("You must create a company first.")
		#project=Project.objects.get(id=validated_data["related_project"].id)
		if user==validated_data["room"].related_project.company.owner:
			room_item=instance

			room_item.unit_price=validated_data["unit_price"]
			_value={}
			input_value=json.loads(validated_data["value"])
			if validated_data["value"]:
				for item_property in validated_data["item"].item_properties.all():
					if item_property.symbol in validated_data["value"]:
						_value[item_property.symbol]=input_value[item_property.symbol]
					else:
						raise ValidationError("Item value missing: "+item_property.symbol)
			if RoomItem.objects.filter(item=validated_data["item"],room=validated_data["room"],material=validated_data["material"],value=_value).exclude(id=room_item.id).exists():
				raise ValidationError("Same properties item is already existed")
			room_item.value=_value
			room_item.quantity=validated_data["quantity"]
			if validated_data.get("remark"):
				room_item.remark=validated_data["remark"]
			else:
				room_item.remark=""
			room_item.material=validated_data["material"]
			room_item.item=validated_data["item"]
			#room_item=RoomItem.objects.update_or_create(item=validated_data["item"],room=validated_data["room"],defaults=data)
			
			room_item.save()
			return room_item
		else:
			raise PermissionDenied

class GetRoomItemRequestSerializer(serializers.ModelSerializer):
	class Meta:
		model=RoomItem
		fields=("id",)

class GetRoomTypeRequestSerializer(serializers.Serializer):
	room_type=serializers.IntegerField()

class PreCalRoomTypeFormulaSerializer(serializers.ModelSerializer):
	value=serializers.JSONField(required=True)

	class Meta:
		model = Room
		fields=["room_type","value"]

	def create(self,validated_data):
		user=None
		request=self.context.get("request")
		if request and hasattr(request,"user"):
			user=request.user

		try:
			Company.objects.get(owner=user)
		except ObjectDoesNotExist:
			raise ValidationError("Please create a company first")

		formulas=RoomTypeFormula.objects.filter(room_type=validated_data["room_type"])
		ret={}

		for formula in formulas:
			ret[formula.name]=formula.cal(value=validated_data["value"])

		return ret

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
			cur_material=None
			if validated_data.get("material"):
				for material in validated_data["item"].item_type.item_type_materials:
					if material["name"]==validated_data.get("material"):
						cur_material=material
						break
				if cur_material==None:
					raise ValidationError("Material not match to this item.")
			
			formulas=ItemFormula.objects.filter(item=validated_data["item"])
			rfps=validated_data["room"].room_type.cal_formulas(validated_data["room"].value)
			#rfps={rfp.name:rfp.cal(validated_data["room"].value) for rfp in RoomTypeFormula.objects.filter(room_type=validated_data["room"].room_type)}
			mvbp=cur_material["value_based_price"] if cur_material!=None and cur_material["value_based_price"] else 0
			vbp= validated_data["item"].value_based_price if validated_data["item"].value_based_price else 0
			ret={}
			for formula in formulas:
				ret[formula.name]=formula.cal(value=validated_data["value"],rfps=rfps,vbp=vbp,mvbp=mvbp)
			return ret

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
	item_type=serializers.CharField()
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

class PreCalRoomTypeFormulaResponseSerializer(serializers.Serializer):
	result=serializers.BooleanField()
	formula=serializers.DictField(child=serializers.FloatField())

class GetRoomTypeFormulaListResponseSerializer(serializers.Serializer):
	result=serializers.BooleanField()
	room_type_formula_list=serializers.DictField(child=serializers.CharField())

class RoomPropertyJsonSerializer(serializers.Serializer):
	name=serializers.CharField()
	symbol=serializers.CharField()

class RoomTypeJsonSerializer(serializers.Serializer):
	id=serializers.IntegerField()
	name=serializers.CharField()
	room_properties=RoomPropertyJsonSerializer(many=True)

class GetRoomTypeListResponseSerializer(serializers.Serializer):
	result=serializers.BooleanField()
	room_type=RoomTypeJsonSerializer(many=True)

class GetRoomRelatedItemResponseSerializer(serializers.Serializer):
	result=serializers.BooleanField()
	related_items=ProjectItemJsonSerializer(many=True)