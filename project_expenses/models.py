import arrow
from django.db import models
from projects.models import Project
from django.utils.translation import ugettext_lazy as _

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
	name=models.CharField(max_length=50)
	project=models.ForeignKey(Project,related_name="project_expend",on_delete=models.CASCADE)
	expend_type=models.ForeignKey(ExpenseType,related_name="type_related_expend",on_delete=models.PROTECT)
	price=models.DecimalField(
        max_digits=12, decimal_places=2)
	pic=models.CharField(max_length=50,blank=True,null=True)
	remark=models.TextField(blank=True,null=True)
	pay_date=models.DateField()

	def __str__(self):
		return str(self.project)+": "+self.name

	def as_json(self):
		ret=dict(
			id=self.id,
			name=self.name,
			expend_type=self.expend_type.as_json(),
			price=self.price,
			pic=self.pic,
			remark=self.remark,
			pay_date=str(models.pay_date)

		)

		return ret


