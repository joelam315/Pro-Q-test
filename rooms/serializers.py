from datetime import datetime
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
		fields=("name","room_type","value","related_project","measure_quantifier")

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
			project.updated_on=datetime.now()
			project.save()
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
		fields=("room_id","name","measure_quantifier")

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
			room.name=validated_data.get("name",room.name)
			room.measure_quantifier=validated_data.get("measure_quantifier",room.measure_quantifier)
			room.save()
			project.updated_on=datetime.now()
			project.save()
			return room
		else:
			raise PermissionDenied

class SetRoomItemSerializer(serializers.ModelSerializer):
	room_item_id=serializers.IntegerField(required=False)
	class Meta:
		model=RoomItem
		fields=("room_item_id","item","room","material","material_value_based_price","unit_price","value_based_price","value","quantity","remark","measure_quantifier","item_quantifier")

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
			data["material_value_based_price"]=validated_data["material_value_based_price"]
			data["value_based_price"]=validated_data["value_based_price"]
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
			data["measure_quantifier"]=validated_data["measure_quantifier"]
			data["item_quantifier"]=validated_data["item_quantifier"]
			if validated_data.get("remark"):
				data["remark"]=validated_data["remark"]
			room_item=RoomItem.objects.update_or_create(item=validated_data["item"],room=validated_data["room"],material=validated_data["material"],value=_value, defaults=data)
			project=room_item[0].room.related_project
			project.updated_on=datetime.now()
			project.save()
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
			room_item.material_value_based_price=validated_data["material_value_based_price"]
			room_item.value_based_price=validated_data["value_based_price"]
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
			room_item.measure_quantifier=validated_data["measure_quantifier"]
			#room_item=RoomItem.objects.update_or_create(item=validated_data["item"],room=validated_data["room"],defaults=data)
			
			room_item.save()
			project=room_item.room.related_project
			project.updated_on=datetime.now()
			project.save()
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
		fields=["item","room","value","material_value_based_price","value_based_price"]

	def create(self,validated_data):
		user = None
		request = self.context.get("request")
		if request and hasattr(request, "user"):
			user = request.user

		if validated_data["room"].related_project.company.owner==user:
			'''cur_material=None
			if validated_data.get("material"):
				if validated_data["item"].item_type.item_type_materials:
					for material in validated_data["item"].item_type.item_type_materials:
						if material["name"].strip()==validated_data.get("material").strip():
							cur_material=material
							break
				if cur_material==None:
					#raise ValidationError(validated_data["item"].item_type.item_type_materials[0]["name"]+":"+validated_data.get("material"))
					raise ValidationError("Material not match to this item.")'''
			
			#formulas=ItemFormula.objects.filter(item=validated_data["item"])
			rfps=validated_data["room"].room_type.cal_formulas(validated_data["room"].value)
			#rfps={rfp.name:rfp.cal(validated_data["room"].value) for rfp in RoomTypeFormula.objects.filter(room_type=validated_data["room"].room_type)}
			mvbp=validated_data["material_value_based_price"]
			#mvbp= cur_material["value_based_price"] if cur_material!=None and cur_material["value_based_price"] else 0
			vbp=validated_data["value_based_price"]
			#vbp= validated_data["item"].value_based_price if validated_data["item"].value_based_price else 0
			ret={}
			ret.update(validated_data["item"].cal_formulas(value=validated_data["value"],rfps=rfps,vbp=vbp,mvbp=mvbp))
			#for formula in formulas:
			#	ret[formula.name]=formula.cal(value=validated_data["value"],rfps=rfps,vbp=vbp,mvbp=mvbp)
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
	material_value_based_price=serializers.FloatField()
	unit_price=serializers.FloatField()
	room=serializers.CharField()
	quantity=serializers.FloatField()
	value=serializers.DictField(child=serializers.FloatField())
	measure_quantifier=serializers.CharField()
	item_quantifier=serializers.CharField()
	remark=serializers.CharField()
	measure_quantifier=serializers.CharField()
	item_quantifier=serializers.CharField()
	value_based_price=serializers.FloatField()

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
	measure_quantifier=serializers.CharField()
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