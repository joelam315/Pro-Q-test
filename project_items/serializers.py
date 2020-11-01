from django import forms
from project_items.models import ItemFormula, ItemTypeMaterial, Item
from rest_framework import serializers
from django.core.exceptions import PermissionDenied,ObjectDoesNotExist,ValidationError

class GetItemMaterialsRequestSerializer(serializers.ModelSerializer):

	class Meta:
		model=ItemTypeMaterial
		fields=("item_type",)

	def create(self,validation_data):
		if validation_data.get("item_type"):
			ret=[]
			if validation_data.get("item_type").item_type_materials!=None and validation_data.get("item_type").item_type_materials!="":
				for material in validation_data.get("item_type").item_type_materials:
					if material["is_active"]=="True":
						ret.append(material)
			return ret
			#return [itm.as_json() for itm in ItemTypeMaterial.objects.filter(item_type=validation_data.get("item_type"),is_active=True)]
		else:
			raise ValidationError("Missing item_type.")

class ItemMaterialJsonSerializer(serializers.Serializer):
	id=serializers.IntegerField()
	name=serializers.CharField()

class GetItemMaterialsResponseSerializer(serializers.Serializer):
	result=serializers.BooleanField()
	materials=ItemMaterialJsonSerializer(many=True)

class GetItemRequestSerializer(serializers.ModelSerializer):
	class Meta:
		model=Item
		fields=("id",)

class GetItemFormulaListResponseSerializer(serializers.Serializer):
	result=serializers.BooleanField()
	item_formula_list=serializers.DictField(child=serializers.CharField())

class ProjectItemPropertyJsonSerializer(serializers.Serializer):
	name=serializers.CharField()
	symbol=serializers.CharField()

class ProjectItemTypeJsonSerializer(serializers.Serializer):
	id=serializers.IntegerField()
	name=serializers.CharField()

class ProjectItemJsonSerializer(serializers.Serializer):
	id=serializers.IntegerField()
	name=serializers.CharField()
	item_properties=ProjectItemPropertyJsonSerializer(many=True)
	item_type=ProjectItemTypeJsonSerializer()
	value_based_price=serializers.FloatField()

class GetItemTypeListResponseSerializer(serializers.Serializer):
	result=serializers.BooleanField()
	item_type_list=ProjectItemTypeJsonSerializer(many=True)

