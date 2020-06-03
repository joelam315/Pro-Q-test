from django import forms
from contacts.models import Contact
from common.serializers import AddressSerializer, CreateAddressSerializer,UpdateAddressSerializer
from companies.serializers import CompanySerializer
from rest_framework import serializers

class ContactSerializer(serializers.ModelSerializer):
	address=AddressSerializer(required=False)
	company=CompanySerializer(required=False)
	icon =serializers.CharField(required=False,help_text="Image URL")

	class Meta:
		model = Contact
		fields = ["id","first_name","last_name","email","phone","address","description","assigned_to","teams","icon","company"]


class CreateContactSerializer(serializers.ModelSerializer):
	address=CreateAddressSerializer(required=False)
	icon =serializers.FileField(required=False,help_text="Base64 format")

	class Meta:
		model = Contact
		fields = ["first_name","last_name","email","phone","address","description","assigned_to","teams","icon"]

class UpdateContactSerializer(serializers.ModelSerializer):
	id=serializers.IntegerField(required=True)
	first_name=serializers.CharField(required=False)
	last_name=serializers.CharField(required=False)
	phone=serializers.CharField(required=False)
	address=UpdateAddressSerializer(required=False)
	icon =serializers.FileField(required=False,help_text="Base64 format")

	class Meta:
		model = Contact
		fields = ["id","first_name","last_name","email","phone","address","description","assigned_to","teams","icon"]

class RemoveContactSerializer(serializers.ModelSerializer):

	class Meta:
		model = Contact
		fields = ["id"]
