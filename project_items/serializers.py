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
			return [itm.as_json() for itm in ItemTypeMaterial.objects.filter(item_type=validation_data.get("item_type"))]
		else:
			raise ValidationError("Missing item_type.")

class ItemMaterialJsonSerializer(serializers.Serializer):
	id=serializers.IntegerField()
	name=serializers.CharField()

class GetItemMaterialsResponseSerializer(serializers.Serializer):
	result=serializers.BooleanField()
	materials=ItemMaterialJsonSerializer(many=True)
