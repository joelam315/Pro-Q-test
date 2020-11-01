import arrow
import time
from django.db import models
from projects.models import Project
from django.utils.translation import ugettext_lazy as _

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
	img=models.FileField(
        max_length=1000, upload_to=milestone_img_url, null=True, blank=True)
	img_upload_date=models.DateField(null=True)

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
		if self.img:
			ret["img_path"]="api/media/"+str(self.img)
		return ret

	def img_record(self):
		ret=dict()
		if self.img:
			ret["img_path"]="api/media/"+str(self.img)
			ret["date"]=self.img_upload_date
		return ret