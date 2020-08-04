from django import forms
from common.models import Address, User
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField

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

class RegisterResponseSerializer(serializers.Serializer):
	result=serializers.BooleanField()
	access=serializers.CharField()
	refresh=serializers.CharField()

class LoginSerializer(serializers.ModelSerializer):
	phone=PhoneNumberField()
	password=serializers.CharField()

	class Meta:
		model=User
		fields=("phone","password")

class LoginResponseSerializer(serializers.Serializer):
	result=serializers.BooleanField()
	access=serializers.CharField()
	refresh=serializers.CharField()

class PhoneVerifySerializer(serializers.ModelSerializer):
	phone=PhoneNumberField()

	class Meta:
		model=User
		fields=("phone",)

class CommonTrueResponseSerializer(serializers.Serializer):
	result=serializers.BooleanField()

class CommonFalseResponseSerializer(serializers.Serializer):
	result=serializers.BooleanField()
	reason=serializers.CharField()

class DistrictJsonSerializer(serializers.Serializer):
	district=serializers.ListField(child=serializers.CharField(),max_length=2,min_length=2)

class ListDistrictResponseSerializer(serializers.Serializer):
	result=serializers.BooleanField()
	districts=DistrictJsonSerializer()


