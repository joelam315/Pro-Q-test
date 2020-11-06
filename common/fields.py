import PIL
from rest_framework import serializers
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist, ValidationError

from io import BytesIO

from django.db.models.fields.files import (
	FieldFile,
	FileField,
	ImageField,
	ImageFieldFile,
)

from django.urls import reverse

from .constants import FETCH_URL_NAME
from .crypt import Cryptographer

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

class EncryptedFile(BytesIO):
	def __init__(self, content):
		self.size = content.size
		BytesIO.__init__(self, Cryptographer.encrypted(content.file.read()))


class EncryptionMixin:
	def save(self, name, content, save=True):
		return super().save(name, EncryptedFile(content), save=save)

	save.alters_data = True

	'''def __str__(self):
		return FETCH_URL_NAME+super().url'''

	def _get_url(self):
		return reverse(FETCH_URL_NAME, kwargs={"path": super().url.replace("/","",1)})

	url = property(_get_url)


class EncryptedFieldFile(EncryptionMixin, FieldFile):
	pass


class EncryptedImageFieldFile(EncryptionMixin, ImageFieldFile):
	pass


class EncryptedFileField(FileField):
	attr_class = EncryptedFieldFile


class EncryptedImageField(ImageField):

	attr_class = EncryptedImageFieldFile

	def update_dimension_fields(self, instance, force=False, *args, **kwargs):
		"""
		Since we're encrypting the file, any attempts to force recalculation of
		the dimensions will always fail, resulting in a null value for height
		and width.  To avoid that, we just set force=False all the time and
		expect that if you want to change those values, you'll do it on your
		own.
		"""
		ImageField.update_dimension_fields(
			self, instance, force=False, *args, **kwargs
		)