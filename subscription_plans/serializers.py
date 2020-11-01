from .models import SubscriptionPlan, CompanySubscribedPlan
from companies.models import Company
from rest_framework import serializers
from django.core.exceptions import PermissionDenied,ObjectDoesNotExist,ValidationError
import json

class SubsribePlanSerializer(serializers.ModelSerializer):
	class Meta:
		model=CompanySubscribedPlan
		fields=("plan",)

	def create(self,validated_data):
		user = None
		request = self.context.get("request")
		if request and hasattr(request, "user"):
			user = request.user
		company=Company.objects.get(owner=user)
		if not company:
			raise ValidationError("You must create a company first.")

		return True

class ListSubscriptionPlanJsonSerializer(serializers.Serializer):
	plan_name=serializers.CharField()
	display_price=serializers.DecimalField(max_digits=12,decimal_places=2)
	description=serializers.CharField()
	top_bg_color=serializers.CharField()
	bottom_bg_color=serializers.CharField()


class ListSubscriptionPlanResponseSerializer(serializers.Serializer):
	result=serializers.BooleanField()
	subscription_plans=ListSubscriptionPlanJsonSerializer(many=True)

class CurrentSubscribedPlanJsonSerializer(serializers.Serializer):
	start_date=serializers.DateField()
	next_billing_date=serializers.DateField(allow_null=True)
	plan=serializers.CharField()

class GetCurrentSubscribedPlanResponseSerializer(serializers.Serializer):
	result=serializers.BooleanField()
	subscribed_plan=CurrentSubscribedPlanJsonSerializer()