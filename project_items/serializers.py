from django import forms
from project_items.models import ItemFormula
from rest_framework import serializers
from project_items.models import ProjectMisc
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
			raise serializers.ValidationError("You must create a company first.")
		if validated_data["project"].company.owner==user:
			data={}
			data["unit_price"]=validated_data["unit_price"]
			data["quantity"]=validated_data["quantity"]
			data["remark"]=validated_data["remark"]
			project_misc=ProjectMisc.objects.updated_or_create(project=validated_data["project"],misc=validated_data["misc"],defaults=data)
			return project_misc[0]
		else:
			raise PermissionDenied