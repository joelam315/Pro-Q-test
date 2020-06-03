from django import forms
from customers.models import Customer
from common.serializers import AddressSerializer, CreateAddressSerializer,UpdateAddressSerializer
from companies.serializers import CompanySerializer
from rest_framework import serializers

class CustomerSerializer(serializers.ModelSerializer):
	address=AddressSerializer(required=False)
	company=CompanySerializer(required=False)
	icon =serializers.CharField(required=False,help_text="Image URL")

	class Meta:
		model = Customer
		fields = ["id","first_name","last_name","email","phone","address","description","assigned_to","teams","icon","company"]


class CreateCustomerSerializer(serializers.ModelSerializer):
	address=CreateAddressSerializer(required=False)
	icon =serializers.FileField(required=False,help_text="Base64 format")

	class Meta:
		model = Customer
		fields = ["first_name","last_name","email","phone","address","description","assigned_to","teams","icon"]

class UpdateCustomerSerializer(serializers.ModelSerializer):
	id=serializers.IntegerField(required=True)
	first_name=serializers.CharField(required=False)
	last_name=serializers.CharField(required=False)
	phone=serializers.CharField(required=False)
	address=UpdateAddressSerializer(required=False)
	icon =serializers.FileField(required=False,help_text="Base64 format")

	class Meta:
		model = Customer
		fields = ["id","first_name","last_name","email","phone","address","description","assigned_to","teams","icon"]

class RemoveCustomerSerializer(serializers.ModelSerializer):

	class Meta:
		model = Customer
		fields = ["id"]
