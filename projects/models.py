import arrow
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.postgres.fields import JSONField,ArrayField
from common.models import Address, User
from common.utils import CURRENCY_CODES,HK_DISTRICT
from companies.models import Company
from phonenumber_field.modelfields import PhoneNumberField
from teams.models import Teams
from function_items.models import FunctionItem, FunctionItemHistory,SubFunctionItem, SubFunctionItemHistory
from projects.utils import PROJECT_STATUS


class Project(models.Model):
    """Model definition for Project."""

    project_title = models.CharField(_('Project Title'), max_length=50)
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
                              max_length=15, default="Early Stage")
    details = models.TextField(_('Details'), null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    company = models.ForeignKey(Company, related_name='company_projects',on_delete=models.CASCADE)

    district=models.CharField(choices=HK_DISTRICT,max_length=50)
    work_location=models.CharField(
        _("Details Location"), max_length=1024,null=True, blank=True)
    document_format=JSONField()
    charging_stages=JSONField()

    class Meta:
        """Meta definition for Project."""

        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        
        ordering = ('-created_on',)

    def __str__(self):
        """Unicode representation of Project."""
        return str(self.company)+": "+self.project_title

    def total_amount(self):
        total=0
        
        return total
        #return self.currency + ' ' + str(self.total_amount)

    def formatted_total_amount(self):
        total=0
        
        return 'HK$ ' + str(total)
        #return self.currency + ' ' + str(self.total_amount)

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
            project_title=self.project_title,
            status=self.status,
            details=self.details,
            work_location=self.work_location,
            start_date=str(self.start_date),
            due_date=str(self.due_date),
            customer_contact=self.customer.as_json() if hasattr(self, 'customer') and self.customer!=None else None
        )
    def all_room_items(self):
        items={}
        rooms=self.project_rooms.all()
        for room in rooms:
            items[room.name]=[]
            for item in room.room_project_items.all():
                items[room.name].append(item.as_json())
        return items
    def all_items(self):
        items={}
        rooms=self.project_rooms.all()
        for room in rooms:
            for item in room.room_project_items.all():
                if item.item.item_type.name not in items:
                    items[item.item.item_type.name]={"items":[],"sum_price":0}
                items[item.item.item_type.name]["items"].append(item.as_json())
                items[item.item.item_type.name]["sum_price"]+=item.unit_price*item.quantity
        return items
    def quot_format(self):
        return dict(
            quot_upper_format=self.document_format["quot_upper_format"],
            quot_middle_format=self.document_format["quot_middle_format"],
            quot_lower_format=self.document_format["quot_lower_format"]
        )
    def invoice_format(self):
        return dict(
            invoice_upper_format=self.document_format["invoice_upper_format"],
            invoice_middle_format=self.document_format["invoice_middle_format"],
            invoice_lower_format=self.document_format["invoice_lower_format"]
        )
    def receipt_format(self):
        return dict(
            receipt_upper_format=self.document_format["receipt_upper_format"],
            receipt_middle_format=self.document_format["receipt_middle_format"],
            receipt_lower_format=self.document_format["receipt_lower_format"]
        )
    def quot_preview(self):
        ret=dict(
            quot_format=self.quot_format(),
            items=self.all_items(),
            charging_stages=self.charging_stages
        )
        return ret 

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


class ProjectChargingStages(models.Model):
    project =models.OneToOneField(Project,related_name='project_charging_stages',on_delete=models.CASCADE)

    quantity=models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(99)])

    values=ArrayField(models.PositiveIntegerField(),size=99)

    descriptions=ArrayField(models.TextField(blank=True),size=99)



    def __str__(self):
        return str(self.project)+"'s Charging Stage"

    def as_json(self):
        return dict(
            quantity=self.quantity,
            values=self.values,
            descriptions=self.descriptions
        )