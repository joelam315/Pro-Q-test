from django import forms
from project_items.models import ProjectItem, SubProjectItem
from rest_framework import serializers

class ProjectItemSerializer(serializers.ModelSerializer):
	class Meta:
		model = ProjectItem
		fields = ["id","name","price","description","type"]


class RequestProjectItemSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = ProjectItem
		fields = ["name","price","description","type"]

class SubProjectItemSerializer(serializers.ModelSerializer):

	class Meta:
		model = SubProjectItem
		fields = ["id","name","price","description"]


class RequestSubProjectItemSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = SubProjectItem
		fields = ["name","price","description"]
