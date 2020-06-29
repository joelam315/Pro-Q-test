import arrow
from django.db import models
from django.utils.translation import ugettext_lazy as _
from common.models import User
from project_items.utils import PROJECT_TYPE, PROJECT_STATUS
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.postgres.fields import JSONField
import numpy as np
import numexpr as ne

class ItemProperty(models.Model):
	name=models.CharField(max_length=50)
	symbol=models.CharField(max_length=50,unique=True)

	def __str__(self):
		return self.name


	def as_json(self):
		return dict(
			name=self.name,
			symbol=self.symbol
		)

class ItemType(models.Model):
	name=models.CharField(max_length=50)
	is_active=models.BooleanField(default=True)

	def __str__(self):
		return self.name

	def as_json(self):
		return dict(
			id=self.id,
			name=self.name
		)

class ItemTypeMaterial(models.Model):
	name=models.CharField(max_length=50)
	item_type=models.ForeignKey(ItemType,related_name="item_type_materials",on_delete=models.PROTECT)
	value_based_price=JSONField(null=True,blank=True)

	def  __str__(self):
		return str(self.item_type)+": "+self.name

	def as_json(self):
		return dict(
			id=self.id,
			name=self.name
		)

class Item(models.Model):

	name=models.CharField(_("Name"),max_length=255)
	item_properties=models.ManyToManyField(ItemProperty,blank=True)
	description= models.TextField(blank=True, null=True)
	item_type=models.ForeignKey(ItemType,related_name="related_items",on_delete=models.PROTECT)
	is_active=models.BooleanField(default=True)
	value_based_price=JSONField(null=True,blank=True)


	def __str__(self):
		return self.name

	'''@property
	def created_on_arrow(self):
		return arrow.get(self.created_on).humanize()

	@property
	def approved_on_arrow(self):
		return arrow.get(self.approved_on).humanize()

	@property
	def last_updated_on_arrow(self):
		return arrow.get(self.last_updated_on).humanize()'''

	def as_json(self):
		return dict(
			id=self.id,
			name=self.name,
			item_properties=[p.as_json() for p in self.item_properties.all()],
			description=self.description,
			item_type=self.item_type.as_json(),
			value_based_price=self.value_based_price
		)

	class Meta:

		verbose_name= 'Item'
		verbose_name_plural= 'Items'
		#ordering = ['item_type']

class ItemFormula(models.Model):
	name=models.CharField(max_length=50)
	item=models.ForeignKey(Item,related_name="item_formulas",on_delete=models.PROTECT)
	formula=models.TextField()

	def cal(self,value,rfps,vbp):
		cal_formula=self.formula
		params=[ip.as_json() for ip in self.item.item_properties.all()]
		#params.sort(key=len_symbol,reverse=True)
		#return params
		for param in params:
			cal_formula=cal_formula.replace("\""+param["symbol"]+"\"",str(value.get(param["name"],0)))
			cal_formula=cal_formula.replace("\'"+param["symbol"]+"\'",str(value.get(param["name"],0)))
		for key in rfps.keys():
			cal_formula=cal_formula.replace("\""+key+"\"",str(rfps[key]))
			cal_formula=cal_formula.replace("\'"+key+"\'",str(rfps[key]))
		cal_formula=cal_formula.replace("\"value_based_price\"",str(vbp))
		cal_formula=cal_formula.replace("\'value_based_price\'",str(vbp))
		return ne.evaluate(cal_formula)

	def __str__(self):
		return str(self.item)+": "+self.name
