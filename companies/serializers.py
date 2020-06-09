import PIL

from django import forms
from companies.models import Company,DocumentFormat,ChargingStage,GeneralRemark
from rest_framework import serializers


class Base64ImageField(serializers.ImageField):
	"""
	A Django REST framework field for handling image-uploads through raw post data.
	It uses base64 for encoding and decoding the contents of the file.

	Heavily based on
	https://github.com/tomchristie/django-rest-framework/pull/1268

	Updated for Django REST framework 3.
	"""

	def to_internal_value(self, data):
		from django.core.files.base import ContentFile
		import base64
		import six
		import uuid

		# Check if this is a base64 string
		if isinstance(data, six.string_types):
			# Check if the base64 string is in the "data:" format
			if 'data:' in data and ';base64,' in data:
				# Break out the header from the base64 content
				header, data = data.split(';base64,')

			# Try to decode the file. Return validation error if it fails.
			try:
				decoded_file = base64.b64decode(data)
			except TypeError:
				self.fail('invalid_image')

			# Generate file name:
			file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
			# Get the file name extension:
			file_extension = self.get_file_extension(file_name, decoded_file)

			complete_file_name = "%s.%s" % (file_name, file_extension, )

			data = ContentFile(decoded_file, name=complete_file_name)

		return super(Base64ImageField, self).to_internal_value(data)

	def get_file_extension(self, file_name, decoded_file):
		import imghdr

		extension = imghdr.what(file_name, decoded_file)
		extension = "jpg" if extension == "jpeg" else extension

		return extension

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
	logo_pic=Base64ImageField(
		max_length=None, use_url=True,
	)
	br_pic=Base64ImageField(
		max_length=None, use_url=True,
	)

	class Meta:
		model=Company
		fields=("name","logo_pic","br_pic")

	def create(self, validated_data):
		user = None
		request = self.context.get("request")
		if request and hasattr(request, "user"):
			user = request.user
		comapny = Company.objects.create(name=validated_data["name"],logo_pic=validated_data["logo_pic"],br_pic=validated_data["br_pic"],owner=user)
		return comapny

class SetDocumentFormatSerializer(serializers.ModelSerializer):

	class Meta:
		model=DocumentFormat
		fields=("quot_upper_format",
			"quot_middle_format",
			"quot_lower_format",
			"invoice_upper_format",
			"invoice_middle_format",
			"invoice_lower_format",
			"receipt_upper_format",
			"receipt_middle_format",
			"receipt_lower_format"
		)

	def create(self, validated_data):
		user = None
		request = self.context.get("request")
		if request and hasattr(request, "user"):
			user = request.user
		company=Company.objects.get(owner=user)
		if not company:
			raise serializers.ValidationError("You must create a company first.")
		doc_format=DocumentFormat.objects.update_or_create (company=company,defaults={"quot_upper_format":validated_data["quot_upper_format"],"quot_middle_format":validated_data["quot_middle_format"],"quot_lower_format":validated_data["quot_lower_format"],"invoice_upper_format":validated_data["invoice_upper_format"],"invoice_middle_format":validated_data["invoice_middle_format"],"invoice_lower_format":validated_data["invoice_lower_format"],"receipt_upper_format":validated_data["receipt_upper_format"],"receipt_middle_format":validated_data["receipt_middle_format"],"receipt_lower_format":validated_data["receipt_lower_format"]})
		return doc_format[0]

class SetChargingStageSerializer(serializers.ModelSerializer):
	
	class Meta:
		model=ChargingStage
		fields=(
			"index",
			"percentage",
			"description"
		)

	def create(self, validated_data):
		user = None
		request = self.context.get("request")
		if request and hasattr(request, "user"):
			user = request.user
		company=Company.objects.get(owner=user)
		if not company:
			raise serializers.ValidationError("You must create a company first.")
		charging_stage=ChargingStage.objects.update_or_create (company=company,index=validated_data["index"],defaults={"percentage":validated_data["percentage"],"description":validated_data["description"]})
		return charging_stage[0]

class SetGeneralRemarkSerializer(serializers.ModelSerializer):
	
	class Meta:
		model=GeneralRemark
		fields=(
			"index",
			"content"
		)

	def create(self, validated_data):
		user = None
		request = self.context.get("request")
		if request and hasattr(request, "user"):
			user = request.user
		company=Company.objects.get(owner=user)
		if not company:
			raise serializers.ValidationError("You must create a company first.")
		general_remark=GeneralRemark.objects.update_or_create (company=company,index=validated_data["index"],defaults={"content":validated_data["content"]})
		return general_remark[0]
