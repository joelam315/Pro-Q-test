from django import forms
from projects.models import Project, Room
from rest_framework import serializers

class CreateProjectSerializer(serializers.ModelSerializer):

	class Meta:
		model=Project
		fields=("project_title","district","work_location","status","start_date","due_date")

	def create(self, validated_data):
		project=Project.objects.create(project_title=validated_data["project_title"],
			district=validated_data["district"],
			work_location=validated_data["validated_data"],
			status=validated_data["status"],
			start_date=validated_data["start_date"],
			due_date=validated_data["due_date"]
		)
		return project