import arrow
import math
import decimal
from decimal import Decimal
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.postgres.fields import JSONField,ArrayField
from common.models import Address, User
from common.utils import CURRENCY_CODES,HK_DISTRICT
from companies.models import Company
from companies.utils import *
from phonenumber_field.modelfields import PhoneNumberField
from teams.models import Teams
from projects.utils import PROJECT_STATUS
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist, ValidationError


def number2alphabet(number):
    str=""
    clone=Decimal(number)
    while clone>0:
        letterNum=Decimal((clone-1)%26)
        letter=chr(letterNum+65)
        str=letter+str
        clone=(clone-(letterNum+1))/26
    
    return str

class Project(models.Model):
    """Model definition for Project."""

    project_title = models.CharField(_('Project Title'), max_length=50)
    quotation_no =models.CharField(max_length=50,blank=True, null=True)
    job_no=models.PositiveIntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, related_name='project_created_by',
        on_delete=models.SET_NULL, null=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    quotation_generated_on = models.DateTimeField(blank=True,null=True)
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
    quotation_remarks=JSONField(null=True,blank=True)
    invoice_remarks=JSONField(null=True,blank=True)
    receipt_remarks=JSONField(null=True,blank=True)

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
        miscs=self.project_misc.all()
        rooms=self.project_rooms.all()
        for misc in miscs:
            total+=misc.unit_price*misc.quantity
        for room in rooms:
            for item in room.room_project_items.all():
                total+=item.unit_price*item.quantity
        return total
        #return self.currency + ' ' + str(self.total_amount)

    def formatted_total_amount(self):
        
        return 'HK$ ' + str(self.total_amount())
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

        ret= dict(
            id=self.id,
            job_no=self.document_format["project_upper_format"],
            project_title=self.project_title,
            status=self.status,
            district=self.district,
            details=self.details,
            work_location=self.work_location,
            start_date=str(self.start_date),
            due_date=str(self.due_date),
            customer_contact=self.customer.as_json() if hasattr(self, 'customer') and self.customer!=None else None
        )
        if self.document_format["project_lower_format"]=="Number":
            ret["job_no"]=ret["job_no"]+format(self.job_no, "04")
        
        return ret
    def all_room_items(self):
        items={}
        rooms=self.project_rooms.all()
        for room in rooms:
            items[room.name]=[]
            for item in room.room_project_items.all():
                items[room.name].append(item.as_json())
        return items
    def all_misc(self):
        miscs=self.project_misc.all()
        items=[misc.as_json() for misc in miscs]
        return items
    def all_items(self):
        items={}
        rooms=self.project_rooms.all()
        miscs=self.project_misc.all()
        items["前期項目"]={"items":[],"sum_price":0}
        for misc in miscs:
            items["前期項目"]["items"].append(misc.as_json())
            items["前期項目"]["sum_price"]+=misc.unit_price*misc.quantity
        for room in rooms:
            for item in room.room_project_items.all():
                if item.item.item_type.name not in items:
                    items[item.item.item_type.name]={"items":[],"sum_price":0}
                items[item.item.item_type.name]["items"].append(item.as_json())
                items[item.item.item_type.name]["sum_price"]+=item.unit_price*item.quantity
        return items
    def all_charging_stages(self):
        items=[]
        charging_stages=self.charging_stages
        i=0
        total=self.total_amount()
        receipts=self.project_receipt_records.all()
        for charging_stage in charging_stages:
            items.append({"value":charging_stage["value"],"description": charging_stage["description"] if charging_stage.get("description") else "","sum_price":(total*decimal.Decimal(charging_stage["value"])/100)})
            try:
                receipt=receipts.get(receipt_id=len(items))
                items[-1]["date"]=receipt.generated_on.strftime("%Y-%m-%d")
            except ObjectDoesNotExist:
                pass
        return items
    def all_expense(self):
        items={}
        expenses=self.project_expense.all()
        for expense in expenses:
            if expense.expense_type.name not in items:
                items[expense.expense_type.name]={"items":[],"sum_price":0}
            items[expense.expense_type.name]["items"].append(expense.as_json())
            items[expense.expense_type.name]["sum_price"]+=expense.price
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
    def generate_quot_no(self):
        quot_no=""
        quot_format=self.quot_format()
        quot_no+=quot_format["quot_upper_format"]
        quot_no+="-"
        if quot_format["quot_middle_format"]=="Date":
            quot_no+=self.created_on.strftime("%Y%m%d")
        elif quot_format["quot_middle_format"]=="Number":
            quot_no+=str(self.job_no)
        elif quot_format["quot_middle_format"]=="Alphabet":
            quot_no+=number2alphabet(self.job_no)

        if quot_format["quot_lower_format"]=="Date":
            quot_no+=self.created_on.strftime("%Y%m%d")
        elif quot_format["quot_lower_format"]=="Number":
            quot_no+=str(self.job_no)
        elif quot_format["quot_lower_format"]=="Alphabet":
            quot_no+=number2alphabet(self.job_no) 

        return quot_no

    def generate_invoice_no(self):
        invoice_no=""
        invoice_format=self.invoice_format()
        invoice_no+=invoice_format["invoice_upper_format"]
        invoice_no+="-"
        if invoice_format["invoice_middle_format"]=="Date":
            invoice_no+=self.created_on.strftime("%Y%m%d")
        elif invoice_format["invoice_middle_format"]=="Number":
            invoice_no+=str(self.job_no)
        elif invoice_format["invoice_middle_format"]=="Alphabet":
            invoice_no+=number2alphabet(self.job_no)

        if invoice_format["invoice_lower_format"]=="Date":
            invoice_no+=self.created_on.strftime("%Y%m%d")
        elif invoice_format["invoice_lower_format"]=="Number":
            invoice_no+=str(self.job_no)
        elif invoice_format["invoice_lower_format"]=="Alphabet":
            invoice_no+=number2alphabet(self.job_no) 

        return invoice_no

    def generate_receipt_no(self):
        receipt_no=""
        receipt_format=self.receipt_format()
        receipt_no+=receipt_format["receipt_upper_format"]
        receipt_no+="-"
        if receipt_format["receipt_middle_format"]=="Date":
            receipt_no+=self.created_on.strftime("%Y%m%d")
        elif receipt_format["receipt_middle_format"]=="Number":
            receipt_no+=str(self.job_no)
        elif receipt_format["receipt_middle_format"]=="Alphabet":
            receipt_no+=number2alphabet(self.job_no)

        if receipt_format["receipt_lower_format"]=="Date":
            receipt_no+=self.created_on.strftime("%Y%m%d")
        elif receipt_format["receipt_lower_format"]=="Number":
            receipt_no+=str(self.job_no)
        elif receipt_format["receipt_lower_format"]=="Alphabet":
            receipt_no+=number2alphabet(self.job_no) 

        return receipt_no
    def quot_preview(self):
        ret=dict(
            job_no=self.document_format["project_upper_format"],
            quot_format=self.quot_format(),
            items=self.all_items(),
            charging_stages=self.charging_stages,
            general_remarks=self.quotation_remarks,
            quotation_no=self.generate_quot_no(),
            customer_contact=self.customer.as_json() if hasattr(self, 'customer') and self.customer!=None else None
        )
        if self.document_format["project_lower_format"]=="Number":
            ret["job_no"]=ret["job_no"]+format(self.job_no, "04")
        return ret 

    def invoice_preview(self,stage_id):
        ret=dict(
            job_no=self.document_format["project_upper_format"],
            invoice_format=self.invoice_format(),
            amount=((float)(self.total_amount())*self.charging_stages[stage_id]["value"]/100),
            total_amount=(float)(self.total_amount()),
            charging_stage=self.charging_stages[stage_id],
            general_remarks=self.invoice_remarks,
            invoice_no=self.generate_invoice_no(),
            customer_contact=self.customer.as_json() if hasattr(self, 'customer') and self.customer!=None else None
        )
        if self.document_format["project_lower_format"]=="Number":
            ret["job_no"]=ret["job_no"]+format(self.job_no, "04")
        return ret
    def receipt_preview(self,stage_id):
        ret=dict(
            job_no=self.document_format["project_upper_format"],
            receipt_format=self.receipt_format(),
            amount=((float)(self.total_amount())*self.charging_stages[stage_id]["value"]/100),
            total_amount=(float)(self.total_amount()),
            charging_stage=self.charging_stages[stage_id],
            general_remarks=self.receipt_remarks,
            receipt_no=self.generate_receipt_no(),
            customer_contact=self.customer.as_json() if hasattr(self, 'customer') and self.customer!=None else None
        )
        if self.document_format["project_lower_format"]=="Number":
            ret["job_no"]=ret["job_no"]+format(self.job_no, "04")
        return ret
    def profit_analyse(self):
        income=self.all_charging_stages()
        outcome=self.all_expense()

        total_income=self.total_amount()

        total_outcome=sum(outcome[item]["sum_price"] for item in outcome.keys())

        ret=dict(
            income_items=income,
            outcome_items=outcome,
            total_income=total_income,
            total_outcome=total_outcome,
            gross_profit_margin=0 if total_income==0 else ((float)((total_income-total_outcome)/total_income))*100
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
    #function_items=models.ManyToManyField(FunctionItemHistory, related_name='projects_history_function_items')
    #sub_function_items=models.ManyToManyField(SubFunctionItemHistory,related_name="projects_history_sub_function_items")


    def __str__(self):
        """Unicode representation of Project."""
        return self.project_number

    def total_amount(self):
        total=0
        return total
        #return self.currency + ' ' + str(self.total_amount)

    def formatted_total_amount(self):
        total=0
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

class ProjectInvoice(models.Model):
    class Meta:
        unique_together = (('project', 'invoice_id'),)
    generated_on = models.DateTimeField(auto_now_add=True)
    project=models.ForeignKey(Project,related_name='project_invoice_records',on_delete=models.CASCADE)
    invoice_id=models.PositiveIntegerField()

    def __str__(self):
        return str(self.project) +" stage "+str(self.invoice_id)

class ProjectReceipt(models.Model):
    class Meta:
        unique_together = (('project', 'receipt_id'),)
    generated_on = models.DateTimeField(auto_now_add=True)
    project=models.ForeignKey(Project,related_name='project_receipt_records',on_delete=models.CASCADE)
    receipt_id=models.PositiveIntegerField()

    def __str__(self):
        return str(self.project) +" stage "+str(self.receipt_id)