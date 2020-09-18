import random
import string

from django import forms
from common.models import Address, User
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from django.db import IntegrityError
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from django.core.exceptions import PermissionDenied,ObjectDoesNotExist, ValidationError

def get_random_alphanumeric_string(length):
	letters_and_digits = string.ascii_letters + string.digits
	result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
	return result_str

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

class CreateOrGetUserSerializer(serializers.ModelSerializer):
	#confirm_password=serializers.CharField()

	class Meta:
		model=User
		fields=("phone",)
		#fields=("phone","password","confirm_password")

	def create(self, validated_data):
		#if validated_data["password"]!=validated_data["confirm_password"]:
		#	raise serializers.ValidationError("Password and confirm password are not matched.")
		user = User.objects.create_user(username=validated_data["phone"],phone=validated_data["phone"],password=User.objects.make_random_password(),login_token=get_random_alphanumeric_string(12))
		user.verify_code="000000"
		user.need_login_verify=True
		user.save()
		return user

	def update(self,instance,validated_data):
		user = instance
		user.login_token=get_random_alphanumeric_string(12)
		user.verify_code="000000"
		user.need_login_verify=True
		user.save()
		return user

class UpdateUserUsernameAndPhoneRequestSerializer(serializers.ModelSerializer):
	class Meta:
		model=User
		fields=("new_phone",)

	def create(self,validated_data):
		user = None
		request = self.context.get("request")
		if request and hasattr(request, "user"):
			user = request.user
		if validated_data.get("new_phone"):
			if User.objects.filter(phone=validated_data["new_phone"]).exists():
				raise ValidationError("The new phone number is already using")

			user.new_phone=validated_data["new_phone"]
			user.new_phone_verify_code="000000"
			user.save()
			return user
		else:
			raise ValidationError("Missing new_phone")

class VerifyNewUserUsernameAndPhoneSerializer(serializers.ModelSerializer):
	class Meta:
		model=User
		fields=("new_phone_verify_code",)

	def create(self,validated_data):
		user = None
		request = self.context.get("request")
		if request and hasattr(request, "user"):
			user = request.user
		if user.new_phone==None:
			raise ValidationError("Please make phone number update requeest first.")

		if validated_data.get("new_phone_verify_code"):
			if User.objects.filter(phone=user.new_phone).exists():
				raise ValidationError("The new phone number is already using")

			if user.new_phone_verify_code==validated_data["new_phone_verify_code"]:

				user.username=user.new_phone
				user.phone=user.new_phone
				user.new_phone=None
				user.new_phone_verify_code=None
				user.save()

				cur_tokens=OutstandingToken.objects.filter(user=user)
				for cur_token in cur_tokens.all():
					BlacklistedToken.objects.update_or_create(token=cur_token)

				return user
			else:
				raise ValidationError("Wrong Verify Code")
		else:
			raise ValidationError("Missing new_phone_verify_code")

class RegisterResponseSerializer(serializers.Serializer):
	result=serializers.BooleanField()
	access=serializers.CharField()
	refresh=serializers.CharField()

class GetUserInfoResponseSerializer(serializers.Serializer):
	result=serializers.BooleanField()
	phone=serializers.CharField()

class RefreshTokenRequestSerializer(serializers.Serializer):
	refresh_token=serializers.CharField()

class LoginSerializer(serializers.ModelSerializer):
	phone=PhoneNumberField()
	otp=serializers.CharField()
	#password=serializers.CharField()

	class Meta:
		model=User
		fields=("phone","otp")

class LoginResponseSerializer(serializers.Serializer):
	result=serializers.BooleanField()
	login_token=serializers.CharField()

class PhoneVerifySuccessResponseSerializer(serializers.Serializer):
	result=serializers.BooleanField()
	access=serializers.CharField()
	refresh=serializers.CharField()
	need_company_setup=serializers.CharField()

class PhoneVerifySerializer(serializers.ModelSerializer):
	phone=PhoneNumberField()
	login_token=serializers.CharField()
	otp=serializers.CharField()
	class Meta:
		model=User
		fields=("phone","login_token","otp")

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


