import arrow
from django.db import models
from django.utils.translation import gettext_lazy as _
from common.models import User
from project_items.utils import PROJECT_TYPE, PROJECT_STATUS
from projects.models import Project
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.postgres.fields import JSONField
from django.apps import apps
import numpy as np
import numexpr as ne
from decimal import *
import logging

logger = logging.getLogger(__name__)

class ItemProperty(models.Model):
	name=models.CharField(max_length=50)
	symbol=models.CharField(max_length=50,unique=True)
	index = models.IntegerField(default=0)

	__original_symbol=None

	def __init__(self, *args, **kwargs):
		super(ItemProperty, self).__init__(*args, **kwargs)
		self.__original_symbol = self.symbol

	def save(self, force_insert=False, force_update=False, *args, **kwargs):
		if self.pk is not None:
			if self.symbol != self.__original_symbol:
				RoomItem = apps.get_model('rooms', 'RoomItem')
				for room_item in RoomItem.objects.all():
					try:
						value=room_item.value.pop(self.__original_symbol)

						room_item.value[self.symbol]=value
						room_item.save()
					except KeyError as e:
						pass
				# name changed - do something here

		super(ItemProperty, self).save(force_insert, force_update, *args, **kwargs)
		self.__original_symbol = self.symbol

	class Meta:
		ordering = ['-index','id']

	def __str__(self):
		return self.name


	def as_json(self):
		return dict(
			name=self.name,
			symbol=self.symbol
		)

class ItemType(models.Model):
	name=models.CharField(max_length=50)
	item_type_materials=JSONField(null=True,blank=True,default=list)
	is_active=models.BooleanField(default=True)

	class Meta:
		ordering = ['-id']

	def clean(self):
		if self.name:
			self.name=self.name.strip()

	def __str__(self):
		return self.name

	def as_json(self):
		return dict(
			id=self.id,
			name=self.name
		)

class ItemTypeMaterial(models.Model):
	name=models.CharField(max_length=50)
	item_type=models.ForeignKey(ItemType,related_name="item_type_materials_s",on_delete=models.PROTECT)
	value_based_price=models.DecimalField(
        max_digits=12, decimal_places=2)
	is_active=models.BooleanField(default=True)

	class Meta:
		ordering = ['-id']

	def  __str__(self):
		return str(self.item_type)+": "+self.name

	def as_json(self):
		return dict(
			id=self.id,
			name=self.name,
			suggested_value_based_price=self.value_based_price
		)

class Item(models.Model):

	name=models.CharField(_("Name"),max_length=255)
	item_properties=models.ManyToManyField(ItemProperty,related_name="property_related_items",blank=True)
	item_properties_sort=JSONField(default=list)
	item_type=models.ForeignKey(ItemType,related_name="related_items",on_delete=models.PROTECT)
	is_active=models.BooleanField(default=True)
	value_based_price=models.DecimalField(
        max_digits=12, decimal_places=2)
	item_formulas=JSONField(null=True,blank=True,default=list)
	index = models.IntegerField(default=0)

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
		item_properties=dict((p.id,p.as_json()) for p in self.item_properties.all())
		return dict(
			id=self.id,
			name=self.name,
			item_properties=[item_properties[_id] for _id in self.item_properties_sort],
			#item_properties=[p.as_json() for p in self.item_properties.all()],
			item_type=self.item_type.as_json(),
			value_based_price=self.value_based_price
		)

	def cal_formulas(self,value,rfps,vbp,mvbp):

		cal_formulas_obj=self.item_formulas
		all_ret={}
		if cal_formulas_obj!=None and cal_formulas_obj!="":
			for cal_formula_obj in cal_formulas_obj:
				cal_formula=cal_formula_obj["formula"]
				params=[ip.as_json() for ip in self.item_properties.all()]
				#params.sort(key=len_symbol,reverse=True)
				#return params
				for param in params:
					cal_formula=cal_formula.replace("\""+param["symbol"]+"\"",str(value.get(param["symbol"],0)))
					cal_formula=cal_formula.replace("\'"+param["symbol"]+"\'",str(value.get(param["symbol"],0)))
				for key in rfps.keys():
					cal_formula=cal_formula.replace("\""+key+"\"",str(rfps[key]))
					cal_formula=cal_formula.replace("\'"+key+"\'",str(rfps[key]))
				cal_formula=cal_formula.replace("\"value_based_price\"",str(vbp))
				cal_formula=cal_formula.replace("\'value_based_price\'",str(vbp))
				cal_formula=cal_formula.replace("\"material.value_based_price\"",str(mvbp))
				cal_formula=cal_formula.replace("\'material.value_based_price\'",str(mvbp))
				#return (cal_formula)
				#logger.debug(cal_formula)
				try:
					ret=ne.evaluate(cal_formula).round(2)
				except TypeError:
					ret=0
				except ValueError:
					ret=0
				#ret=ne.evaluate(cal_formula).round(2)
				'''try:
					ret=ne.evaluate(cal_formula).round(2)
				except TypeError:
					logger.debug(cal_formula)'''
				#ret=cal_formula
				ret=ret if str(ret)!="[]" else 0
				all_ret[cal_formula_obj["name"]]=ret
		return all_ret

	class Meta:

		verbose_name= 'Item'
		verbose_name_plural= 'Items'
		ordering = ['-index','-id']

class ItemFormula(models.Model):
	name=models.CharField(max_length=50)
	item=models.ForeignKey(Item,related_name="item_formulas_s",on_delete=models.PROTECT)
	formula=models.TextField()
	is_active=models.BooleanField(default=True)

	def cal(self,value,rfps,vbp,mvbp):
		cal_formula=self.formula
		params=[ip.as_json() for ip in self.item.item_properties.all()]
		#params.sort(key=len_symbol,reverse=True)
		#return params
		for param in params:
			cal_formula=cal_formula.replace("\""+param["symbol"]+"\"",Decimal(str(value.get(param["symbol"]),0)))
			cal_formula=cal_formula.replace("\'"+param["symbol"]+"\'",Decimal(str(value.get(param["symbol"]),0)))
		for key in rfps.keys():
			cal_formula=cal_formula.replace("\""+key+"\"",str(rfps[key]))
			cal_formula=cal_formula.replace("\'"+key+"\'",str(rfps[key]))
		cal_formula=cal_formula.replace("\"value_based_price\"",str(vbp))
		cal_formula=cal_formula.replace("\'value_based_price\'",str(vbp))
		cal_formula=cal_formula.replace("\"material.value_based_price\"",str(mvbp))
		cal_formula=cal_formula.replace("\'material.value_based_price\'",str(mvbp))
		#return (cal_formula)
		return ne.evaluate(cal_formula).round(2)

	def __str__(self):
		return str(self.item)+": "+self.name

	def as_json(self):
		return dict(
			name=self.name,
			formula=self.formula
		)


