import arrow
import json
from django.db import models
from django.utils.translation import ugettext_lazy as _
from projects.models import Project
import numpy as np
import numexpr as ne
from django.contrib.postgres.fields import JSONField
from project_items.models import Item, ItemFormula,ItemTypeMaterial
from rooms.utils import DATA_TYPE

class RoomProperty(models.Model):
	name=models.CharField(max_length=50)
	symbol=models.CharField(max_length=50,unique=True)
	data_type=models.CharField(max_length=50,choices=DATA_TYPE)
	custom_properties=JSONField(null=True,blank=True)
	custom_property_formulas=JSONField(null=True,blank=True)
	property_formulas=JSONField(null=True,blank=True)

	def __str__(self):
		return self.name


	def as_json(self):
		return dict(
			name=self.name,
			symbol=self.symbol,
			data_type=self.data_type,
			custom_properties=self.custom_properties
		)

	def custom_property_cal(self):
		if self.data_type!="custom properties":
			return None
		custom_properties=self.custom_properties
		custom_property_formulas=self.custom_property_formulas
		property_formulas=self.property_formulas
		params=[custom_property for custom_property in custom_properties]
		#params.sort(key=len_symbol,reverse=True)
		#return params
		for param in params:
			
			cal_formula=cal_formula.replace("\""+param["symbol"]+"\"",str(value.get(param["symbol"],0)))
			cal_formula=cal_formula.replace("\'"+param["symbol"]+"\'",str(value.get(param["symbol"],0)))
		
		return ne.evaluate(cal_formula)

class RoomType(models.Model):
	name=models.CharField(max_length=50)
	is_active=models.BooleanField(default=True)
	related_items=models.ManyToManyField(Item,blank=True)
	room_properties=models.ManyToManyField(RoomProperty,blank=True)

	def __str__(self):
		return self.name

	def as_json(self):
		return dict(
			id=self.id,
			name=self.name,
			room_properties=[room_property.as_json() for room_property in self.room_properties.all()]
		)


class RoomTypeFormula(models.Model):
	name=models.CharField(max_length=50)
	room_type=models.ForeignKey(RoomType,related_name="room_type_formulas",on_delete=models.PROTECT)
	formula=models.TextField()
	is_active=models.BooleanField(default=True)

	def cal(self,value):
		rtps=self.room_type.room_properties.all()
		cal_formula=self.formula
		params=[rtp.as_json() for rtp in rtps]
		#params.sort(key=len_symbol,reverse=True)
		#return params
		for param in params:
			if param["data_type"]=="custom properties":
				custom_params=param.custom_properties
				for custom_param in custom_params:
					cal_formula=cal_formula.replace("\""+param["symbol"]+"."+custom_param+"\"",str(value.get(param["symbol"],0).get(custom_param,0)))
					cal_formula=cal_formula.replace("\'"+param["symbol"]+"."+custom_param+"\'",str(value.get(param["symbol"],0).get(custom_param,0)))
			else:
				cal_formula=cal_formula.replace("\""+param["symbol"]+"\"",str(value.get(param["symbol"],0)))
				cal_formula=cal_formula.replace("\'"+param["symbol"]+"\'",str(value.get(param["symbol"],0)))
		
		return ne.evaluate(cal_formula)

	def as_json(self):
		return dict(
			name=self.name,
			formula=self.formula
		)

	def __str__(self):
		return str(self.room_type)+": "+self.name

class Room(models.Model):
	name=models.CharField(max_length=50)
	room_type=models.ForeignKey(RoomType,on_delete=models.PROTECT)
	value=JSONField(null=True,blank=True)
	related_project=models.ForeignKey(Project,related_name='project_rooms',on_delete=models.CASCADE)

	def __str__(self):
		return self.related_project.project_title+": "+self.name

	def as_json(self):
		rpis=[rpi.as_json() for rpi in self.room_project_items.all()]
		_sum=0
		ret=dict(
			id=self.id,
			name=self.name,
			room_project_items_count=len(rpis)
			#room_project_items_price_sum=rpis
		)
		ret["sum_price"]=sum((rpi["unit_price"]*rpi["quantity"]) for rpi in rpis)
		return ret

	def details(self):
		ret=dict(
			name=self.name,
			value=self.value,
			room_type=str(self.room_type),
			room_project_items=[rpi.as_json() for rpi in self.room_project_items.all()]
		)
		ret["properties"]=dict()
		formulas=RoomTypeFormula.objects.filter(room_type=self.room_type)
		for formula in formulas:
			ret["properties"][formula.name]=formula.cal(self.value)
		return ret

class RoomItem(models.Model):

	class Meta:
		unique_together = (("item", "room"),)

	item=models.ForeignKey(Item,related_name="related_project_items",on_delete=models.PROTECT)
	room=models.ForeignKey(Room,related_name="room_project_items",on_delete=models.CASCADE)
	material=models.ForeignKey(ItemTypeMaterial,related_name="material_related_project_items",on_delete=models.PROTECT,null=True,blank=True)
	unit_price = models.DecimalField(
        max_digits=12, decimal_places=2)
	value=JSONField(null=True,blank=True)
	quantity=models.PositiveIntegerField()
	remark=models.TextField(blank=True,null=True)

	def __str__(self):
		return str(self.room)+": "+str(self.item)

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
		ret= dict(
			id=self.id,
			name=self.item.name,
			item_type=self.item.item_type.name,
			unit_price=float(self.unit_price),
			room=self.room.name,
			quantity=self.quantity,
			value=self.value,
			remark=self.remark
		)
		if self.material:
			ret["material"]=self.material.name
		formulas=ItemFormula.objects.filter(item=self.item)
		rfps={rfp.name:rfp.cal(self.value) for rfp in RoomTypeFormula.objects.filter(room_type=self.room.room_type)}
		vbp=self.material.value_based_price if self.material!=None and self.material.value_based_price!=None else self.item.value_based_price 
		for formula in formulas:
			ret[formula.name]=formula.cal(self.value,rfps,vbp)
		return ret

	class Meta:

		verbose_name= 'Room Item'
		verbose_name_plural= 'Room Items'
		#ordering = ['created_on']

