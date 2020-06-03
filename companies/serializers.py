from django import forms
from companies.models import Company
from rest_framework import serializers

class CompanySerializer(serializers.ModelSerializer):
	class Meta:
		model=Company
		fields =(
			"id",
			"name",
			"email",
			"phone",
			"industry",
			"billing_address_line",
			"billing_street",
			"billing_city",
			"billing_state",
			"billing_postcode",
			"billing_country",
			"website",
			"description"
		)
