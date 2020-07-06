import arrow
from django.db import models
from projects.models import Project
from django.utils.translation import ugettext_lazy as _

class Misc(models.Model):
	name=models.CharField(max_length=50)
	suggested_unit_price=models.DecimalField(
        max_digits=12, decimal_places=2)
	is_active=models.BooleanField(default=True)

	def __str__(self):
		return self.name

	def as_json(self):
		return dict(
			id=self.id,
			name=self.name,
			suggested_unit_price=float(self.suggested_unit_price)
		)

	class Meta:

		verbose_name= 'Misc'
		verbose_name_plural= 'Misc'
		#ordering = ['item_type']

class ProjectMisc(models.Model):
	project=models.ForeignKey(Project,related_name="project_misc",on_delete=models.CASCADE)
	misc=models.ForeignKey(Misc,related_name="related_project_misc",on_delete=models.PROTECT)
	unit_price=models.DecimalField(
        max_digits=12, decimal_places=2)
	quantity=models.PositiveIntegerField()
	remark=models.TextField(blank=True,null=True)

	def __str__(self):
		return str(self.project)+": "+str(self.misc)

	def as_json(self):
		ret= dict(
			id=self.id,
			name=self.misc.name,
			unit_price=float(self.unit_price),
			quantity=self.quantity,
			remark=self.remark
		)

		return ret

	class Meta:
		unique_together = (("misc", "project"),)
		verbose_name= 'Project Misc'
		verbose_name_plural= 'Project Misc'
		#ordering = ['created_on']

