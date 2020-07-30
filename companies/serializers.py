import PIL

from companies.models import Company,DocumentFormat,ChargingStages,QuotationGeneralRemark,InvoiceGeneralRemark,ReceiptGeneralRemark
from rest_framework import serializers
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist, ValidationError


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
	logo=serializers.CharField()
	class Meta:
		model=Company
		fields =(
			"id",
			"name",
			"logo"
		)

class SetCompanySerializer(serializers.ModelSerializer):
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
		comapny = Company.objects.update_or_create(owner=user,defaults={"name":validated_data["name"],"logo_pic":validated_data["logo_pic"],"br_pic":validated_data["br_pic"]})[0]
		return comapny

class DocumentFormatSerializer(serializers.ModelSerializer):
	class Meta:
		model=DocumentFormat
		exclude = ('company', )

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

class ChargingStagesSerializer(serializers.ModelSerializer):
	class Meta:
		model=ChargingStages
		fields=(
			"quantity",
			"values",
			"descriptions"
		)

class SetChargingStagesSerializer(serializers.ModelSerializer):
	
	class Meta:
		model=ChargingStages
		fields=(
			"quantity",
			"values",
			"descriptions"
		)

	def create(self, validated_data):
		user = None
		request = self.context.get("request")
		if request and hasattr(request, "user"):
			user = request.user
		company=Company.objects.get(owner=user)
		if not company:
			raise serializers.ValidationError("You must create a company first.")
		sum_percen=0

		for i in range(validated_data.get("quantity")):
			sum_percen+=validated_data["values"][i]
		if sum_percen!=100:
			raise ValidationError("The total percentage is not equal to 100.")
		charging_stages=ChargingStages.objects.update_or_create (company=company,defaults={"quantity":validated_data["quantity"],"values":validated_data["values"],"descriptions":validated_data["descriptions"]})
		return charging_stages[0]

class ChargingStageJsonSerializer(serializers.Serializer):
	index=serializers.IntegerField()
	value=serializers.IntegerField()
	content=serializers.CharField()

class GetChargingStagesResponseSerializer(serializers.Serializer):
	result=serializers.BooleanField()
	charging_stages=ChargingStageJsonSerializer(many=True)



class QuotationGeneralRemarkSerializer(serializers.ModelSerializer):
	class Meta:
		model=QuotationGeneralRemark
		fields=(
			"index",
			"content"
		)

class SetQuotationGeneralRemarkSerializer(serializers.ModelSerializer):
	
	class Meta:
		model=QuotationGeneralRemark
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
		general_remark=QuotationGeneralRemark.objects.update_or_create (company=company,index=validated_data["index"],defaults={"content":validated_data["content"]})
		return general_remark[0]

class InvoiceGeneralRemarkSerializer(serializers.ModelSerializer):
	class Meta:
		model=InvoiceGeneralRemark
		fields=(
			"index",
			"content"
		)

class SetInvoiceGeneralRemarkSerializer(serializers.ModelSerializer):
	
	class Meta:
		model=InvoiceGeneralRemark
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
		general_remark=QuotationGeneralRemark.objects.update_or_create (company=company,index=validated_data["index"],defaults={"content":validated_data["content"]})
		return general_remark[0]

class ReceiptGeneralRemarkSerializer(serializers.ModelSerializer):
	class Meta:
		model=ReceiptGeneralRemark
		fields=(
			"index",
			"content"
		)

class SetReceiptGeneralRemarkSerializer(serializers.ModelSerializer):
	
	class Meta:
		model=ReceiptGeneralRemark
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
		general_remark=QuotationGeneralRemark.objects.update_or_create (company=company,index=validated_data["index"],defaults={"content":validated_data["content"]})
		return general_remark[0]
