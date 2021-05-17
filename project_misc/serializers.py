from datetime import datetime
from django import forms
from rest_framework import serializers
from companies.models import Company
from project_misc.models import ProjectMisc, Misc
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
			if validated_data.get("remark"):
				data["remark"]=validated_data["remark"]
			project_misc=ProjectMisc.objects.update_or_create(project=validated_data["project"],misc=validated_data["misc"],defaults=data)
			project=project_misc[0].project
			project.updated_on=datetime.now()
			project.save()
			return project_misc[0]
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
		if validated_data["project"].company.owner==user:
			project_misc=instance
			project_misc.unit_price=validated_data["unit_price"]
			project_misc.quantity=validated_data["quantity"]
			project_misc.misc=validated_data["misc"]
			if validated_data.get("remark"):
				project_misc.remark=validated_data["remark"]
			else:
				project_misc.remark=""
			project_misc.save()
			project=project_misc.project;
			project.updated_on=datetime.now()
			project.save()
			return project_misc
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

class GetProjectMiscRequestSerializer(serializers.Serializer):
	project_id=serializers.IntegerField()
	misc_id=serializers.IntegerField()

class GetAllProjectMiscResponseSerializer(serializers.Serializer):
	result=serializers.BooleanField()
	project_misc=ProjectMiscJsonSerializer(many=True)

class MiscJsonSerializer(serializers.Serializer):
	id=serializers.IntegerField()
	name=serializers.CharField()
	suggested_unit_price=serializers.FloatField()

class GetMiscListResponseSerializer(serializers.Serializer):
	result=serializers.BooleanField()
	misc_list=MiscJsonSerializer(many=True)