from django import forms
from project_items.models import ItemFormula, ItemTypeMaterial
from rest_framework import serializers
from django.core.exceptions import PermissionDenied,ObjectDoesNotExist,ValidationError

class GetItemMaterialsRequestSerializer(serializers.ModelSerializer):

	class Meta:
		model=ItemTypeMaterial
		fields=("item_type",)

	def create(self,validation_data):
		if validation_data.get("item_type"):
			return [itm.as_json() for itm in ItemTypeMaterial.objects.filter(item_type=validation_data.get("item_type"),is_active=True)]
		else:
			raise ValidationError("Missing item_type.")

class ItemMaterialJsonSerializer(serializers.Serializer):
	id=serializers.IntegerField()
	name=serializers.CharField()

class GetItemMaterialsResponseSerializer(serializers.Serializer):
	result=serializers.BooleanField()
	materials=ItemMaterialJsonSerializer(many=True)

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

