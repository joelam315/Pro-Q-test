from django import forms
from rest_framework import serializers
from project_misc.models import ProjectMisc
from django.core.exceptions import PermissionDenied,ObjectDoesNotExist

class SetProjectMiscSerializer(serializers.ModelSerializer):
	class Meta:
		model=ProjectMisc
		fields=("project","misc","unit_price","quantity","remark")

	def create(self,validated_data):
		user = None
		request = self.context.get("request")
		if request and hasattr(request, "user"):
			user = request.user
		company=Company.objects.get(owner=user)
		if not company:
			raise ValidationError("You must create a company first.")
		if validated_data["project"].company.owner==user:
			data={}
			data["unit_price"]=validated_data["unit_price"]
			data["quantity"]=validated_data["quantity"]
			data["remark"]=validated_data["remark"]
			project_misc=ProjectMisc.objects.updated_or_create(project=validated_data["project"],misc=validated_data["misc"],defaults=data)
			return project_misc[0]
		else:
			raise PermissionDenied

class SetProjectMiscResponseSerializer(serializers.Serializer):
	result=serializers.BooleanField()
	project_misc_id=serializers.IntegerField()

class ProjectMiscJsonSerializer(serializers.Serializer):
	id=serializers.IntegerField()
	name=serializers.CharField()
	unit_price=serializers.FloatField()
	quantity=serializers.IntegerField()
	remark=serializers.CharField()

class GetAllProjectMiscResponseSerializer(serializers.Serializer):
	result=serializers.BooleanField()
	project_misc=ProjectMiscJsonSerializer(many=True)