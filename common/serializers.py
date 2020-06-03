from django import forms
from common.models import Address
from rest_framework import serializers

class AddressSerializer(serializers.ModelSerializer):
	class Meta:
		model=Address
		fields =("id","address_line","lat","lng")

class CreateAddressSerializer(serializers.ModelSerializer):
	class Meta:
		model=Address
		fields =("address_line","lat","lng")

class UpdateAddressSerializer(serializers.ModelSerializer):
	class Meta:
		model=Address
		fields =("id","address_line","lat","lng")
