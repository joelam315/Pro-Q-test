import arrow
from django.db import models
from projects.models import Project
from django.utils.translation import ugettext_lazy as _

class ProjectWork(models.Model):
	name=models.CharField(max_length=50)
	project=models.ForeignKey(Project,on_delete=models.CASCADE,related_name="project_works")
	pic=models.CharField(max_length=50,blank=True,null=True)
	start_date=models.DateField()
	end_date=models.DateField()
	description=models.TextField(blank=True,null=True)

class ProjectMilestone(models.Model):
	name=models.CharField(max_length=50)
	project=models.ForeignKey(Project,on_delete=models.CASCADE,related_name="project_milestones")
	date=models.DateField()
	remind=models.DurationField(null=True)
	pic=models.CharField(max_length=50,blank=True,null=True)
	description=models.TextField(blank=True,null=True)