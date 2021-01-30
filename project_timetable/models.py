import os
import arrow
import time
import datetime
from django.db import models
from projects.models import Project
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver
from common.fields import  EncryptedImageField
from common.constants import FETCH_URL_NAME

def milestone_img_url(self, filename):
    hash_ = int(time.time())
    return "%s/%s/%s/%s" % ("companies",str(self.project.company.id), self.milestone_prepend,filename)

class ProjectWork(models.Model):
	name=models.CharField(max_length=50)
	project=models.ForeignKey(Project,on_delete=models.CASCADE,related_name="project_works")
	pic=models.CharField(max_length=50,blank=True,null=True)
	start_date=models.DateField()
	end_date=models.DateField()
	description=models.TextField(blank=True,null=True)

	class Meta:
		ordering = ['id']

	def __str__(self):
		return str(self.project)+" work "+str(self.id) +" "+self.name

	def as_json(self):
		return dict(
			id=self.id,
			type="project_work",
			name=self.name,
			pic=self.pic,
			start_date=self.start_date,
			end_date=self.end_date,
			description=self.description
		)

class ProjectMilestone(models.Model):
	milestone_prepend = "milestone"

	name=models.CharField(max_length=50)
	project=models.ForeignKey(Project,on_delete=models.CASCADE,related_name="project_milestones")
	date=models.DateField()
	remind=models.DurationField(null=True)
	pic=models.CharField(max_length=50,blank=True,null=True)
	description=models.TextField(blank=True,null=True)
	#img=models.FileField(max_length=1000, upload_to=milestone_img_url, null=True, blank=True)
	img=EncryptedImageField(upload_to=milestone_img_url,width_field="img_width",height_field="img_height",null=True,blank=True)
	img_width = models.PositiveIntegerField(default=1)
	img_height = models.PositiveIntegerField(default=1)
	img_upload_date=models.DateField(default=datetime.date.today,null=True)

	class Meta:
		ordering = ['id']

	def __str__(self):
		return str(self.project)+" milestone "+str(self.id) +" "+self.name

	def as_json(self):
		ret= dict(
			id=self.id,
			type="project_milestone",
			name=self.name,
			pic=self.pic,
			date=self.date,
			remind=self.remind,
			description=self.description if self.description else "",

		)
		if hasattr(self,"project_milestone_img_set"):
			ret["img_set"]=self.project_milestone_img_set.img_record()
		return ret

	def img_record(self):
		ret=dict()
		if hasattr(self,"project_milestone_img_set"):
			ret=self.project_milestone_img_set.img_record()
		return ret

@receiver(models.signals.post_delete, sender=ProjectMilestone)
def auto_delete_img_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `ProjectMilestone` object is deleted.
    """
    if instance.img:
        if os.path.isfile(instance.img.path):
            os.remove(instance.img.path)