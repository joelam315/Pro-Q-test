from rest_framework.renderers import JSONRenderer
from rest_framework.utils import json

class APIRenderer(JSONRenderer):
	charset="utf-8"