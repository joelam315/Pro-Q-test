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
from common.utils import MEASURE_QUANTIFIERS,ITEM_QUANTIFIERS
from django.core.exceptions import PermissionDenied,ObjectDoesNotExist,ValidationError

class RoomProperty(models.Model):
	name=models.CharField(max_length=50)
	symbol=models.CharField(max_length=50,unique=True)
	data_type=models.CharField(max_length=50,choices=DATA_TYPE)
	custom_properties=JSONField(null=True,blank=True)
	custom_property_formulas=JSONField(null=True,blank=True)
	#property_formulas=JSONField(null=True,blank=True)

	def __str__(self):
		return self.name


	def as_json(self):
		return dict(
			name=self.name,
			symbol=self.symbol,
			data_type=self.data_type,
			custom_properties=self.custom_properties,
			custom_property_formulas=self.custom_property_formulas
		)

class RoomType(models.Model):
	name=models.CharField(max_length=50)
	is_active=models.BooleanField(default=True)
	related_items=models.ManyToManyField(Item,blank=True)
	#room_properties=JSONField(null=True,blank=True)
	room_properties=models.ManyToManyField(RoomProperty,blank=True)
	room_type_formulas=JSONField(null=True,blank=True)

	def __str__(self):
		return self.name

	def as_json(self):
		return dict(
			id=self.id,
			name=self.name,
			room_properties=[room_property.as_json() for room_property in self.room_properties.all()]
		)

	def cal_formulas(self,value):
		rtps=self.room_properties.all()
		cal_formulas_obj=self.room_type_formulas
		params=[rtp.as_json() for rtp in rtps]
		var={}
		all_ret={}
		#params.sort(key=len_symbol,reverse=True)
		#return params
		if cal_formulas_obj:
			for cal_formula_obj in cal_formulas_obj:
				cal_formula=cal_formula_obj["formula"]
				for param in params:
					#return param["data_type"]
					if param["data_type"]=="custom property":
						custom_params=param["custom_properties"]
						#return param["custom_property_formulas"]
						if param["custom_property_formulas"]!="null" and param["custom_property_formulas"]!=None:
							for property_formula in param["custom_property_formulas"]:
								#return "\""+param["symbol"]+"."+property_formula_name+"\" :"+cal_formula
								if "\""+param["symbol"]+"."+property_formula["name"]+"\"" in cal_formula or "\'"+param["symbol"]+"."+property_formula["name"]+"\'" in cal_formula:
									#return True
									arr=[]
									
									#return value.get(param["symbol"])
									if value.get(param["symbol"]):
										for custom_property_values in value.get(param["symbol"]):
											current_property_formula=property_formula["formula"]
											for custom_property in param["custom_properties"]:
												
												current_property_formula=current_property_formula.replace("\""+custom_property["symbol"]+"\"",str(custom_property_values.get(custom_property["symbol"],0)))
												current_property_formula=current_property_formula.replace("\'"+custom_property["symbol"]+"\'",str(custom_property_values.get(custom_property["symbol"],0)))
												
											#return current_property_formula
											try:
												arr.append(ne.evaluate(current_property_formula))
											except:
												arr.append(0)
									var[param["symbol"]+"_"+property_formula["name"]]=np.array(arr)
									cal_formula=cal_formula.replace("\""+param["symbol"]+"."+property_formula["name"]+"\"",param["symbol"]+"_"+property_formula["name"])
									cal_formula=cal_formula.replace("\'"+param["symbol"]+"."+property_formula["name"]+"\'",param["symbol"]+"_"+property_formula["name"])
						'''for custom_param in custom_params:
							cal_formula=cal_formula.replace("\""+param["symbol"]+"."+custom_param+"\"",str(value.get(param["symbol"],0).get(custom_param,0)))
							cal_formula=cal_formula.replace("\'"+param["symbol"]+"."+custom_param+"\'",str(value.get(param["symbol"],0).get(custom_param,0)))
						'''
					else:
						cal_formula=cal_formula.replace("\""+param["symbol"]+"\"",str(value.get(param["symbol"],0)))
						cal_formula=cal_formula.replace("\'"+param["symbol"]+"\'",str(value.get(param["symbol"],0)))
				
			#return cal_formula
			#a=
			#return ne.evaluate('sum(array([1,2]))')
			#return var
				try:
					ret=ne.evaluate(cal_formula,var)
				except:
					ret=0
				ret=ret if str(ret)!="[]" else 0
				all_ret[cal_formula_obj["name"]]=ret
		return all_ret


class RoomTypeFormula(models.Model):
	name=models.CharField(max_length=50)
	room_type=models.ForeignKey(RoomType,related_name="room_type_formulas_s",on_delete=models.PROTECT)
	formula=models.TextField()
	is_active=models.BooleanField(default=True)

	def cal(self,value):
		rtps=self.room_type.room_properties.all()
		cal_formula=self.formula
		params=[rtp.as_json() for rtp in rtps]
		var={}
		#params.sort(key=len_symbol,reverse=True)
		#return params
		for param in params:
			#return param["data_type"]
			if param["data_type"]=="custom property":
				custom_params=param["custom_properties"]
				#return param["custom_property_formulas"]
				if param["custom_property_formulas"]!="null" and param["custom_property_formulas"]!=None:
					for property_formula in param["custom_property_formulas"]:
						#return "\""+param["symbol"]+"."+property_formula_name+"\" :"+cal_formula
						if "\""+param["symbol"]+"."+property_formula["name"]+"\"" in cal_formula or "\'"+param["symbol"]+"."+property_formula["name"]+"\'" in cal_formula:
							#return True
							arr=[]
							
							#return value.get(param["symbol"])
							if value.get(param["symbol"]):
								for custom_property_values in value.get(param["symbol"]):
									current_property_formula=property_formula["formula"]
									for custom_property in param["custom_properties"]:
										
										current_property_formula=current_property_formula.replace("\""+custom_property["symbol"]+"\"",str(custom_property_values.get(custom_property["symbol"],0)))
										current_property_formula=current_property_formula.replace("\'"+custom_property["symbol"]+"\'",str(custom_property_values.get(custom_property["symbol"],0)))
										
									#return current_property_formula
									arr.append(ne.evaluate(current_property_formula))
							var[param["symbol"]+"_"+property_formula["name"]]=np.array(arr)
							cal_formula=cal_formula.replace("\""+param["symbol"]+"."+property_formula["name"]+"\"",param["symbol"]+"_"+property_formula["name"])
							cal_formula=cal_formula.replace("\'"+param["symbol"]+"."+property_formula["name"]+"\'",param["symbol"]+"_"+property_formula["name"])
				'''for custom_param in custom_params:
					cal_formula=cal_formula.replace("\""+param["symbol"]+"."+custom_param+"\"",str(value.get(param["symbol"],0).get(custom_param,0)))
					cal_formula=cal_formula.replace("\'"+param["symbol"]+"."+custom_param+"\'",str(value.get(param["symbol"],0).get(custom_param,0)))
				'''
			else:
				cal_formula=cal_formula.replace("\""+param["symbol"]+"\"",str(value.get(param["symbol"],0)))
				cal_formula=cal_formula.replace("\'"+param["symbol"]+"\'",str(value.get(param["symbol"],0)))
		
		#return cal_formula
		#a=
		#return ne.evaluate('sum(array([1,2]))')
		#return var
		ret=ne.evaluate(cal_formula,var)
		return ret if str(ret)!="[]" else 0

	def custom_property_cal(self):
		if self.data_type!="custom properties":
			return None
		custom_properties=self.custom_properties
		custom_property_formulas=self.custom_property_formulas
		custom_property_formulas=self.custom_property_formulas
		params=[custom_property for custom_property in custom_properties]
		#params.sort(key=len_symbol,reverse=True)
		#return params
		for param in params:
			
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
	measure_quantifier=models.CharField(choices=MEASURE_QUANTIFIERS,max_length=20)

	class Meta:
		ordering = ['id']

	def __str__(self):
		return self.related_project.project_title+": "+self.name

	def as_json(self):
		rpis=[rpi.as_json() for rpi in self.room_project_items.all()]
		_sum=0
		ret=dict(
			id=self.id,
			name=self.name,
			room_project_items_count=len(rpis),
			room_type_id=self.room_type.id,
			#measure_quantifier=self.measure_quantifier
			#room_project_items_price_sum=rpis
		)
		ret["sum_price"]=sum((rpi["unit_price"]*rpi["quantity"]) for rpi in rpis)
		return ret

	def details(self):
		ret=dict(
			name=self.name,
			value=self.value,
			room_type=(self.room_type.id,str(self.room_type)),
			room_project_items=[rpi.as_json() for rpi in self.room_project_items.all()],
			measure_quantifier=self.measure_quantifier
		)
		ret["properties"]=dict()
		formulas=self.room_type.cal_formulas(self.value)
		for name in formulas:
			ret["properties"][name]=formulas[name]
		'''formulas=RoomTypeFormula.objects.filter(room_type=self.room_type)
		for formula in formulas:
			ret["properties"][formula.name]=formula.cal(self.value)'''
		return ret

class RoomItem(models.Model):

	class Meta:
		unique_together = (("item", "room","material","value"),)

	item=models.ForeignKey(Item,related_name="related_project_items",on_delete=models.PROTECT)
	room=models.ForeignKey(Room,related_name="room_project_items",on_delete=models.CASCADE)
	material=models.TextField(null=True,blank=True)
	material_value_based_price= models.DecimalField(
        max_digits=12, decimal_places=2)
	#material=models.ForeignKey(ItemTypeMaterial,related_name="material_related_project_items",on_delete=models.PROTECT,null=True,blank=True)
	unit_price = models.DecimalField(
        max_digits=12, decimal_places=2)
	value=JSONField(null=True,blank=True)
	quantity=models.DecimalField(
        max_digits=12, decimal_places=2)
	remark=models.TextField(blank=True,null=True)
	measure_quantifier=models.CharField(choices=MEASURE_QUANTIFIERS,max_length=20)
	item_quantifier=models.CharField(choices=ITEM_QUANTIFIERS,max_length=20)

	class Meta:
		ordering = ['id']

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
			item_type=(self.item.item_type.id,self.item.item_type.name),
			material_value_based_price=float(self.material_value_based_price),
			unit_price=float(self.unit_price),
			room=self.room.name,
			quantity=float(self.quantity),
			value=self.value,
			remark=self.remark if self.remark!=None else "",
			measure_quantifier=self.measure_quantifier,
			item_quantifier=self.item_quantifier,
			value_based_price=self.item.value_based_price
		)
		if self.material:
			ret["material"]=self.material
		#formulas=ItemFormula.objects.filter(item=self.item)
		#rfps={rfp.name:rfp.cal(self.value) for rfp in RoomTypeFormula.objects.filter(room_type=self.room.room_type)}
		rfps=self.room.room_type.cal_formulas(self.room.value)
		
		#set vbp
		vbp=self.item.value_based_price
		mvbp=0
		if self.material!=None and self.material!="":
			itm=self.item.item_type.item_type_materials
			if itm!=None and itm!=dict():
				mvbp=self.material_value_based_price
				'''for material in itm:
					if material["name"].strip()==self.material.strip():
						if material["value_based_price"]!=None and material["value_based_price"]!="" and int(material["value_based_price"])>0:
							mvbp=material["value_based_price"]
						break'''
		#vbp=self.material.value_based_price if self.material!=None and self.material.value_based_price!=None else self.item.value_based_price 
		#//

		#for formula in formulas:
		#	ret[formula.name]=formula.cal(self.value,rfps,vbp,mvbp)
		ret.update(self.item.cal_formulas(self.value,rfps,vbp,mvbp))
		return ret

	class Meta:

		verbose_name= 'Room Item'
		verbose_name_plural= 'Room Items'
		#ordering = ['created_on']

