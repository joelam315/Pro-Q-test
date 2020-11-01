import PIL
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
		from django.core.validators import URLValidator
		import base64
		import six
		import uuid
		import requests

		# Check if this is a base64 string
		if isinstance(data, six.string_types):
			# Check if the base64 string is in the "data:" format
			if 'data:' in data and ';base64,' in data:
				# Break out the header from the base64 content
				header, data = data.split(';base64,')
			else:
				try:
					validate = URLValidator(data)
					data=base64.b64encode(requests.get(data).content).decode('utf-8')
					if 'data:' in data and ';base64,' in data:
						header, data = data.split(';base64,')
				except ValidationError as exception:
					pass
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

def foreign_field(field_name):
	def accessor(obj):
		val = obj
		for part in field_name.split('__'):
			val = getattr(val, part)
		return val
	accessor.__name__ = field_name
	return accessor