import arrow
from django.db import models
from django.utils.translation import ugettext_lazy as _
from common.models import Address, User
from common.utils import CURRENCY_CODES
from companies.models import Company
from phonenumber_field.modelfields import PhoneNumberField
from teams.models import Teams
from function_items.models import FunctionItem, FunctionItemHistory,SubFunctionItem, SubFunctionItemHistory
from projects.utils import PROJECT_STATUS


class Project(models.Model):
    """Model definition for Project."""

    project_title = models.CharField(_('Project Title'), max_length=50)
    project_number = models.CharField(_('Project Number'), max_length=50)
    from_address = models.ForeignKey(
        Address, related_name='project_from_address', on_delete=models.SET_NULL, null=True)
    to_address = models.ForeignKey(
        Address, related_name='project_to_address', on_delete=models.SET_NULL, null=True)
    name = models.CharField(_('Name'), max_length=100)
    email = models.EmailField(_('Email'))
    assigned_to = models.ManyToManyField(
        User, related_name='project_assigned_to')
    # quantity is the number of hours worked
    quantity = models.PositiveIntegerField(default=0)
    # rate is the rate charged
    rate = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    # total amount is product of rate and quantity
    #total_amount = models.DecimalField(
    #    blank=True, null=True, max_digits=12, decimal_places=2)
    #currency = models.CharField(
    #    max_length=3, choices=CURRENCY_CODES, blank=True, null=True)
    phone = PhoneNumberField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, related_name='project_created_by',
        on_delete=models.SET_NULL, null=True)

    amount_due = models.DecimalField(
        blank=True, null=True, max_digits=12, decimal_places=2)
    amount_paid = models.DecimalField(
        blank=True, null=True, max_digits=12, decimal_places=2)
    is_email_sent = models.BooleanField(default=False)
    status = models.CharField(choices=PROJECT_STATUS,
                              max_length=15, default="Draft")
    details = models.TextField(_('Details'), null=True, blank=True)
    due_date = models.DateField(blank=True, null=True)
    companies = models.ManyToManyField(Company, related_name='companies_projects')
    teams = models.ManyToManyField(Teams, related_name='projects_teams')
    function_items=models.ManyToManyField(FunctionItem, related_name='projects_function_items')
    sub_function_items=models.ManyToManyField(SubFunctionItem,related_name="projects_sub_function_items")
    approved_by = models.ForeignKey(User, related_name='project_approved_by',on_delete=models.SET_NULL, null=True)
    approved_on = models.DateTimeField(null=True)
    last_updated_by = models.ForeignKey(User, related_name='project_last_updated_by',on_delete=models.SET_NULL, null=True)
    last_updated_on = models.DateTimeField(auto_now_add=True)


    class Meta:
        """Meta definition for Project."""

        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        
        ordering = ('-created_on',)

    def __str__(self):
        """Unicode representation of Project."""
        return self.project_number

    def total_amount(self):
        total=0
        for function_item in self.function_items.all():
            total+=function_item.price
        for sub_function_item in self.sub_function_items.all():
            total+=sub_function_item.price
        return total
        #return self.currency + ' ' + str(self.total_amount)

    def formatted_total_amount(self):
        total=0
        for function_item in self.function_items.all():
            total+=function_item.price
        for sub_function_item in self.sub_function_items.all():
            total+=sub_function_item.price
        return 'HK$ ' + str(total)
        #return self.currency + ' ' + str(self.total_amount)

    def formatted_rate(self):
        return str(self.rate) + ' ' + self.currency

    def formatted_total_quantity(self):
        return str(self.quantity) + ' ' + 'Hours'

    def is_draft(self):
        if self.status == 'Draft':
            return True
        else:
            return False

    def is_sent(self):
        if self.status == 'Sent' and self.is_email_sent == False:
            return True
        else:
            return False

    def is_resent(self):
        if self.status == 'Sent' and self.is_email_sent == True:
            return True
        else:
            return False

    def is_paid_or_cancelled(self):
        if self.status in ['Paid', 'Cancelled']:
            return True
        else:
            return False
    def as_intro(self):
        return dict(
            id=self.id,
            project_number=self.project_number,
            project_title=self.project_title,
            status=self.status,

        )
    def as_json(self):
        fis=[]
        for fi in self.function_items.all():
            fis.append(fi.as_json())
            sfis=self.sub_function_items.filter(related_function_item=fi)
            fis[-1]["sub_function_items"]=[sfi.as_json() for sfi in sfis]
        return dict(
            id=self.id,
            project_number=self.project_number,
            project_title=self.project_title,
            status=self.status,
            function_items=fis,#[fi.as_json() for fi in self.function_items.all()],
            details=self.details,
            name=self.name,
            due_date=str(self.due_date),
            email=self.email

        )


    @property
    def created_on_arrow(self):
        return arrow.get(self.created_on).humanize()


class ProjectHistory(models.Model):
    """Model definition for ProjectHistory.
    This model is used to track/keep a record of the updates made to original project object."""


    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='project_history')
    project_title = models.CharField(_('Project Title'), max_length=50)
    project_number = models.CharField(_('Project Number'), max_length=50)
    from_address = models.ForeignKey(
        Address, related_name='project_history_from_address', on_delete=models.SET_NULL, null=True)
    to_address = models.ForeignKey(
        Address, related_name='project_history_to_address', on_delete=models.SET_NULL, null=True)
    name = models.CharField(_('Name'), max_length=100)
    email = models.EmailField(_('Email'))
    assigned_to = models.ManyToManyField(
        User, related_name='project_history_assigned_to')
    # quantity is the number of hours worked
    quantity = models.PositiveIntegerField(default=0)
    # rate is the rate charged
    rate = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    # total amount is product of rate and quantity
    total_amount = models.DecimalField(
        blank=True, null=True, max_digits=12, decimal_places=2)
    #currency = models.CharField(
    #    max_length=3, choices=CURRENCY_CODES, blank=True, null=True)
    phone = PhoneNumberField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    # created_by = models.ForeignKey(
    #     User, related_name='project_history_created_by',
    #     on_delete=models.SET_NULL, null=True)
    updated_by = models.ForeignKey(
        User, related_name='project_history_created_by',
        on_delete=models.SET_NULL, null=True)

    amount_due = models.DecimalField(
        blank=True, null=True, max_digits=12, decimal_places=2)
    amount_paid = models.DecimalField(
        blank=True, null=True, max_digits=12, decimal_places=2)
    is_email_sent = models.BooleanField(default=False)
    status = models.CharField(choices=PROJECT_STATUS,
                              max_length=15, default="Draft")
    # details or description here stores the fields changed in the original project object
    details = models.TextField(_('Details'), null=True, blank=True)
    due_date = models.DateField(blank=True, null=True)
    function_items=models.ManyToManyField(FunctionItemHistory, related_name='projects_history_function_items')
    sub_function_items=models.ManyToManyField(SubFunctionItemHistory,related_name="projects_history_sub_function_items")


    def __str__(self):
        """Unicode representation of Project."""
        return self.project_number

    def total_amount(self):
        total=0
        for function_item in self.function_items.all():
            total+=function_item.price
        for sub_function_item in self.sub_function_items.all():
            total+=sub_function_item.price
        return total
        #return self.currency + ' ' + str(self.total_amount)

    def formatted_total_amount(self):
        total=0
        for function_item in self.function_items.all():
            total+=function_item.price
        for sub_function_item in self.sub_function_items.all():
            total+=sub_function_item.price
        return 'HK$ ' + str(total)
        #return self.currency + ' ' + str(self.total_amount)

    def formatted_rate(self):
        return str(self.rate) + ' ' + self.currency

    def formatted_total_quantity(self):
        return str(self.quantity) + ' ' + 'Hours'

    @property
    def created_on_arrow(self):
        return arrow.get(self.created_on).humanize()

    class Meta:
        ordering = ('-created_on',)