import arrow
import math
import decimal
import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.postgres.fields import JSONField,ArrayField
from django.utils import timezone
from colorfield.fields import ColorField
from companies.models import Company

class SubscriptionPlan(models.Model):
	plan_name=models.CharField(_('Plan Name'),max_length=256)
	display_price=models.DecimalField( max_digits=12, decimal_places=2)
	project_quota=models.PositiveIntegerField(null=True,blank=True)
	function_permission=JSONField(blank=True,default=dict)
	description=models.TextField()
	top_bg_color=ColorField()
	bottom_bg_color=ColorField()
	visible=models.BooleanField(default=True)
	is_active=models.BooleanField(default=True)

	def __str__(self):
		return self.plan_name

	def list_data(self):
		ret=dict(
			id=self.id,
			plan_name=self.plan_name,
			display_price=self.display_price,
			description=self.description,
			top_bg_color=self.top_bg_color,
			bottom_bg_color=self.bottom_bg_color
		)
		return ret

class CompanySubscribedPlan(models.Model):
	start_date=models.DateField(default=datetime.datetime.now)
	next_billing_date=models.DateField(blank=True,null=True)
	plan=models.ForeignKey(SubscriptionPlan,related_name="subscriptions",on_delete=models.PROTECT)
	company=models.ForeignKey(Company,related_name="subscription_histories",on_delete=models.PROTECT)

	def __str__(self):
		return str(self.company)+" "+str(self.plan)

	def as_json(self):
		ret=dict(
			start_date=self.start_date,
			next_billing_date=self.next_billing_date if self.next_billing_date else "-",
			plan=self.plan.plan_name
		)
		return ret

	class Meta:
		ordering = ('-start_date',)