from django import forms
from accounts.models import Account
from rest_framework import serializers

class AccountSerializer(serializers.ModelSerializer):
	class Meta:
		model=Account
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
