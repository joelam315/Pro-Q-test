import arrow
from django.db import models
from django.utils.translation import ugettext_lazy as _
from common.models import User
from function_items.utils import FUNCTION_TYPE, FUNCTION_STATUS
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

class FunctionItem(models.Model):

	name=models.CharField(_("Name"),max_length=255)
	price = models.DecimalField(
        max_digits=12, decimal_places=2, default=0)
	description= models.TextField(blank=True, null=True)
	type=models.CharField(choices=FUNCTION_TYPE,max_length=20,default='Front-end')
	status=models.CharField(choices=FUNCTION_STATUS, max_length=20,default='Requested')
	created_on = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(User, related_name='function_items_created_by',on_delete=models.SET_NULL, null=True)
	approved_by = models.ForeignKey(User, related_name='function_items_approved_by',on_delete=models.SET_NULL, null=True)
	approved_on = models.DateTimeField(null=True)
	last_updated_by = models.ForeignKey(User, related_name='function_items_last_updated_by',on_delete=models.SET_NULL, null=True)
	last_updated_on = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return self.name

	@property
	def created_on_arrow(self):
		return arrow.get(self.created_on).humanize()

	@property
	def approved_on_arrow(self):
		return arrow.get(self.approved_on).humanize()

	@property
	def last_updated_on_arrow(self):
		return arrow.get(self.last_updated_on).humanize()

	def as_json(self):
		return dict(
			id=self.id,
			name=self.name,
			price=float(self.price),
			description=self.description,
			type=self.type
		)

	class Meta:

		verbose_name= 'Function Item'
		verbose_name_plural= 'Function Items'
		ordering = ['type','-created_on']

class FunctionItemHistory(models.Model):

	function_item=models.ForeignKey(
        FunctionItem, on_delete=models.SET_NULL, related_name='function_item_history',null=True)
	name=models.CharField(_("Name"),max_length=255)
	price = models.DecimalField(
        max_digits=12, decimal_places=2, default=0)
	description= models.TextField(blank=True, null=True)
	type=models.CharField(choices=FUNCTION_TYPE,max_length=20,default='Front-end')
	status=models.CharField(choices=FUNCTION_STATUS, max_length=20,default='Requested')
	changed_data=models.TextField(_('Changed Data'), null=True, blank=True)
	created_on = models.DateTimeField(auto_now_add=True)
	updated_by = models.ForeignKey(
        User, related_name='function_item_history_created_by',
        on_delete=models.SET_NULL, null=True)
	def __str__(self):
		return self.name

	@property
	def created_on_arrow(self):
		return arrow.get(self.created_on).humanize()

	class Meta:
		ordering = ['type','-created_on']

class SubFunctionItem(models.Model):

	name=models.CharField(_("Name"),max_length=255)
	price = models.DecimalField(
        max_digits=12, decimal_places=2, default=0)
	description= models.TextField(blank=True, null=True)
	status=models.CharField(choices=FUNCTION_STATUS, max_length=20,default='Requested')
	created_on = models.DateTimeField(auto_now_add=True)
	created_by = models.ForeignKey(User, related_name='sub_function_items_created_by',on_delete=models.SET_NULL, null=True)
	approved_by = models.ForeignKey(User, related_name='sub_function_items_approved_by',on_delete=models.SET_NULL, null=True)
	approved_on = models.DateTimeField(null=True)
	last_updated_by = models.ForeignKey(User, related_name='sub_function_items_last_updated_by',on_delete=models.SET_NULL, null=True)
	last_updated_on = models.DateTimeField(auto_now_add=True)
	related_function_item = models.ForeignKey(FunctionItem, related_name='sub_function_items',on_delete=models.CASCADE)
	def __str__(self):
		return self.name

	@property
	def created_on_arrow(self):
		return arrow.get(self.created_on).humanize()

	@property
	def approved_on_arrow(self):
		return arrow.get(self.approved_on).humanize()

	@property
	def last_updated_on_arrow(self):
		return arrow.get(self.last_updated_on).humanize()

	def as_json(self):
		return dict(
			id=self.id,
			name=self.name,
			price=float(self.price),
			description=self.description
		)

	class Meta:

		verbose_name= 'Sub Function Item'
		verbose_name_plural= 'Sub Function Items'
		ordering = ['created_on']

class SubFunctionItemHistory(models.Model):

	sub_function_item=models.ForeignKey(
        SubFunctionItem, on_delete=models.SET_NULL, related_name='sub_function_item_history',null=True)
	name=models.CharField(_("Name"),max_length=255)
	price = models.DecimalField(
        max_digits=12, decimal_places=2, default=0)
	description= models.TextField(blank=True, null=True)
	status=models.CharField(choices=FUNCTION_STATUS, max_length=20,default='Requested')
	changed_data=models.TextField(_('Changed Data'), null=True, blank=True)
	created_on = models.DateTimeField(auto_now_add=True)
	updated_by = models.ForeignKey(
        User, related_name='sub_function_item_history_created_by',
        on_delete=models.SET_NULL, null=True)
	def __str__(self):
		return self.name

	@property
	def created_on_arrow(self):
		return arrow.get(self.created_on).humanize()

	def as_json(self):
		return dict(
			id=self.id,
			name=self.name,
			price=float(self.price),
			description=self.description
		)

	class Meta:
		ordering = ['-created_on']