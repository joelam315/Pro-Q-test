import arrow
from django.db import models
from django.utils.translation import ugettext_lazy as _
from projects.models import Project
import numpy as np
import numexpr as ne

class RoomProperty(models.Model):
	name=models.CharField(max_length=50)
	symbol=models.CharField(max_length=50,unique=True)

	def __str__(self):
		return self.name

class RoomType(models.Model):
	name=models.CharField(max_length=50)
	is_active=models.BooleanField(default=True)

	def __str__(self):
		return self.name

class RoomTypeProperty(models.Model):
	class Meta:
		unique_together = (('room_type', 'room_property'),)
	room_type=models.ForeignKey(RoomType,on_delete=models.PROTECT)
	room_property=models.ForeignKey(RoomProperty,on_delete=models.PROTECT)

class RoomTypeFormula(models.Model):
	name=models.CharField(max_length=50)
	room_type=models.ForeignKey(RoomType,on_delete=models.PROTECT)
	formula=models.TextField()

	def cal(self):
		rtps=RoomTypeProperty.objects.filter(room_type=self.room_type)
		cal_formula=formula
		for rtp in rtps:
			cal_formula=cal_formula.replace("\""+rtp.room_property.symbol+"\"",rtp.value)
			cal_formula=cal_formula.replace("\'"+rtp.room_property.symbol+"\'",rtp.value)
		
		return ne.evaluate(cal_formula)

class Room(models.Model):
    name=models.CharField(max_length=50)
    length=models.PositiveIntegerField()
    width=models.PositiveIntegerField()
    height=models.PositiveIntegerField()
    related_project=models.ForeignKey(Project,related_name='project_rooms',on_delete=models.CASCADE)

    def __str__(self):
        return self.related_project.project_title+": "+self.name

    def floor_size(self):
        return self.length*self.width

    def wall_size(self):
        return self.length*self.height*2+self.width*self.height*2

    def as_json(self):
        return dict(
            id=self.id,
            name=self.name,
            length=self.length,
            width=self.width,
            height=self.height,
            floor_size=self.floor_size(),
            wall_size=self.wall_size()
        )
