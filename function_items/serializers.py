from django import forms
from function_items.models import FunctionItem, SubFunctionItem
from rest_framework import serializers

class FunctionItemSerializer(serializers.ModelSerializer):
	class Meta:
		model = FunctionItem
		fields = ["id","name","price","description","type"]


class RequestFunctionItemSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = FunctionItem
		fields = ["name","price","description","type"]

class SubFunctionItemSerializer(serializers.ModelSerializer):

	class Meta:
		model = SubFunctionItem
		fields = ["id","name","price","description"]


class RequestSubFunctionItemSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = SubFunctionItem
		fields = ["name","price","description"]
