import arrow
import time
from django.db import models
from projects.models import Project
from django.utils.translation import ugettext_lazy as _
from common.fields import EncryptedImageField
from common.constants import FETCH_URL_NAME

def expense_img_url(self, filename):
    hash_ = int(time.time())
    return "%s/%s/%s/%s" % ("companies",str(self.project.company.id), self.expense_prepend,filename)


class ExpenseType(models.Model):
	name=models.CharField(max_length=50)
	is_active=models.BooleanField(default=True)

	def __str__(self):
		return self.name

	def as_json(self):
		return dict(
			id=self.id,
			name=self.name
		)

class ProjectExpense(models.Model):
	expense_prepend = "expense"

	name=models.CharField(max_length=50)
	project=models.ForeignKey(Project,related_name="project_expense",on_delete=models.CASCADE)
	expense_type=models.ForeignKey(ExpenseType,related_name="type_related_expense",on_delete=models.PROTECT)
	price=models.DecimalField(
        max_digits=12, decimal_places=2)
	pic=models.CharField(max_length=50,blank=True,null=True,verbose_name="Person in charge")
	remark=models.TextField(blank=True,null=True,default="")
	pay_date=models.DateField()
	#img=models.FileField(
    #    max_length=1000, upload_to=expense_img_url, null=True, blank=True)
	img=EncryptedImageField(upload_to=expense_img_url,width_field="img_width",height_field="img_height",null=True,blank=True)
	img_width = models.PositiveIntegerField(default=1)
	img_height = models.PositiveIntegerField(default=1)
	img_upload_date=models.DateField(null=True)

	def __str__(self):
		return str(self.project)+" expense: "+self.name

	def as_json(self):
		ret=dict(
			id=self.id,
			name=self.name,
			expense_type=self.expense_type.as_json(),
			price=self.price,
			pic=self.pic,
			remark=self.remark if self.remark else "",
			pay_date=str(self.pay_date)

		)
		if self.img:
			ret["img_path"]="api/"+FETCH_URL_NAME+"/media/"+str(self.img)
		return ret

	def img_record(self):
		ret=dict()
		if self.img:
			ret["img_path"]="api/"+FETCH_URL_NAME+"/media/"+str(self.img)
			ret["date"]=self.img_upload_date
		return ret

