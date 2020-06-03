from django import forms
from common.models import Address, User
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

class CreateUserSerializer(serializers.ModelSerializer):
	confirm_password=serializers.CharField()

	class Meta:
		model=User
		fields=("phone","password","confirm_password")

	def create(self, validated_data):
		if validated_data["password"]!=validated_data["confirm_password"]:
			raise serializers.ValidationError("Password and confirm password are not matched.")
		user = User.objects.create_user(username=validated_data["phone"],phone=validated_data["phone"],password=validated_data["password"])
		return user
