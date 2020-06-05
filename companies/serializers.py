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

class CreateCompanySerializer(serializers.ModelSerializer):

	class Meta:
		model=Company
		fields=("name","logo_pic","br_pic")

	def create(self, validated_data):
		if validated_data["password"]!=validated_data["confirm_password"]:
			raise serializers.ValidationError("Password and confirm password are not matched.")
		comapny = Company.objects.create_user(name=validated_data["name"],phone=validated_data["logo_pic"],password=validated_data["br_pic"])
		return comapny
