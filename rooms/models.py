import arrow
from django.db import models
from django.utils.translation import ugettext_lazy as _
from projects.models import Project
import numpy as np
import numexpr as ne
from django.contrib.postgres.fields import JSONField
from project_items.models import Item, ItemFormula,ItemTypeMaterial

class RoomProperty(models.Model):
	name=models.CharField(max_length=50)
	symbol=models.CharField(max_length=50,unique=True)

	def __str__(self):
		return self.name


	def as_json(self):
		return dict(
			name=self.name,
			symbol=self.symbol
		)

class RoomType(models.Model):
	name=models.CharField(max_length=50)
	is_active=models.BooleanField(default=True)
	related_items=models.ManyToManyField(Item,blank=True)

	def __str__(self):
		return self.name

	def as_json(self):
		return dict(
			id=self.id,
			name=self.name
		)

class RoomTypeProperties(models.Model):

	room_type=models.OneToOneField(RoomType,related_name="room_type_properties",on_delete=models.PROTECT)
	room_properties=models.ManyToManyField(RoomProperty,blank=True)

	def __str__(self):
		return str(self.room_type)+"'s Properties"

class RoomTypeFormula(models.Model):
	name=models.CharField(max_length=50)
	room_type=models.ForeignKey(RoomType,on_delete=models.PROTECT)
	formula=models.TextField()

	def cal(self,value):
		rtps=RoomTypeProperties.objects.get(room_type=self.room_type)
		cal_formula=self.formula
		params=[rtp.as_json() for rtp in rtps.room_properties.all()]
		#params.sort(key=len_symbol,reverse=True)
		#return params
		for param in params:
			cal_formula=cal_formula.replace("\""+param["symbol"]+"\"",str(value.get(param["name"],0)))
			cal_formula=cal_formula.replace("\'"+param["symbol"]+"\'",str(value.get(param["name"],0)))
		
		return ne.evaluate(cal_formula)

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
		ret=dict(
			id=self.id,
			name=self.name,
			value=self.value,
			room_type=str(self.room_type),
			room_project_items=[rpi.as_json() for rpi in self.room_project_items.all()]
		)
		formulas=RoomTypeFormula.objects.filter(room_type=self.room_type)
		for formula in formulas:
			ret[formula.name]=formula.cal(self.value)
		return ret

class RoomItem(models.Model):

	class Meta:
		unique_together = (("item", "room"),)

	item=models.ForeignKey(Item,related_name="related_project_items",on_delete=models.PROTECT)
	room=models.ForeignKey(Room,related_name="room_project_items",on_delete=models.PROTECT)
	material=models.ForeignKey(ItemTypeMaterial,related_name="material_related_project_items",on_delete=models.PROTECT)
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
			price=float(self.unit_price),
			material=self.material.name,
			quantity=self.quantity,
			value=self.value,
			description=self.item.description,
			remark=self.remark
		)
		formulas=ItemFormula.objects.filter(item=self.item)
		for formula in formulas:
			ret[formula.name]=formula.cal(self.value)
		return ret

	class Meta:

		verbose_name= 'Room Item'
		verbose_name_plural= 'Room Items'
		#ordering = ['created_on']

