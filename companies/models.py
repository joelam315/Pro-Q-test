import arrow
import time
from django.db import models
from django.utils.translation import pgettext_lazy
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import JSONField,ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator

from common.models import User
from common.utils import INDCHOICES, COUNTRIES
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.text import slugify
from contacts.models import Contact
from teams.models import Teams
from companies.utils import UPPER_CHOICES,MIDDLE_CHOICES,LOWER_CHOICES


class Tags(models.Model):
    name = models.CharField(max_length=20)
    slug = models.CharField(max_length=20, unique=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tags, self).save(*args, **kwargs)

def br_url(self, filename):
    hash_ = int(time.time())
    return "%s/%s/%s/%s" % ("companies",str(self.id), self.br_prepend,filename)

def logo_url(self, filename):
    hash_ = int(time.time())
    return "%s/%s/%s/%s" % ("companies",str(self.id), self.logo_prepend,filename)

def sign_url(self, filename):
    hash_ = int(time.time())
    return "%s/%s/%s/%s" % ("companies",str(self.id), self.sign_prepend,filename)

class Company(models.Model):

    COMPANY_STATUS_CHOICE = (
        ("open", "Open"),
        ('close', 'Close')
    )
    logo_prepend = "logos"
    br_prepend = "brs"
    sign_prepend = "signs"
    name = models.CharField(pgettext_lazy(
        "Name of Company", "Name"), max_length=64)
    email = models.EmailField(blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True)
    industry = models.CharField(
        _("Industry Type"),
        max_length=255, choices=INDCHOICES,
        blank=True, null=True)
    job_no=models.PositiveIntegerField(default=1)
    # billing_address = models.ForeignKey(
    #     Address, related_name='company_billing_address', on_delete=models.CASCADE, blank=True, null=True)
    # shipping_address = models.ForeignKey(
    #     Address, related_name='company_shipping_address', on_delete=models.CASCADE, blank=True, null=True)
    billing_address_line = models.CharField(
        _("Address"), max_length=255, blank=True, null=True)
    billing_street = models.CharField(
        _("Street"), max_length=55, blank=True, null=True)
    billing_city = models.CharField(
        _("City"), max_length=255, blank=True, null=True)
    billing_state = models.CharField(
        _("State"), max_length=255, blank=True, null=True)
    billing_postcode = models.CharField(
        _("Post/Zip-code"), max_length=64, blank=True, null=True)
    billing_country = models.CharField(
        max_length=3, choices=COUNTRIES, blank=True, null=True)
    website = models.URLField(_("Website"), blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(
        User, related_name='company_created_by',
        on_delete=models.SET_NULL, null=True)
    created_on = models.DateTimeField(_("Created on"), auto_now_add=True)
    is_active = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tags, blank=True)
    br_approved=models.BooleanField(default=False)
    status = models.CharField(
        choices=COMPANY_STATUS_CHOICE, max_length=64, default='open')
    '''lead = models.ForeignKey(
        'leads.Lead', related_name="company_leads",
        on_delete=models.SET_NULL, null=True)'''
    owner =models.OneToOneField(User,related_name='owned_company',on_delete=models.CASCADE)
    logo_pic = models.FileField(
        max_length=1000, upload_to=logo_url, null=True, blank=True)
    br_pic = models.FileField(
        max_length=1000, upload_to=br_url, null=True, blank=True)
    sign = models.FileField(
        max_length=1000, upload_to=sign_url, null=True, blank=True)

    def __str__(self):
        return self.name

    def as_json(self):
        return dict(
            name=self.name,
            logo_path="api/media/"+str(self.logo_pic),
            owner=self.owner.display_name
        )

    class Meta:
        ordering = ['-created_on']

    def get_quotation_general_remarks_json(self):
        general_remarks=self.company_quotation_general_remarks.order_by('index','id')
        return [general_remark.as_json() for general_remark in general_remarks]

    def get_invoice_general_remarks_json(self):
        general_remarks=self.company_invoice_general_remarks.order_by('index','id')
        return [general_remark.as_json() for general_remark in general_remarks]

    def get_receipt_general_remarks_json(self):
        general_remarks=self.company_receipt_general_remarks.order_by('index','id')
        return [general_remark.as_json() for general_remark in general_remarks]

    def get_charging_stages_json(self):
        charging_stages=self.company_charging_stages
        ret=[]
        for i in range(charging_stages.quantity):
            ret.append({"index":i+1,"value":charging_stages.values[i],"content":charging_stages.descriptions[i]})
        return ret

    def get_complete_address(self):
        address = ""
        if self.billing_address_line:
            address += self.billing_address_line
        if self.billing_street:
            if address:
                address += ", " + self.billing_street
            else:
                address += self.billing_street
        if self.billing_city:
            if address:
                address += ", " + self.billing_city
            else:
                address += self.billing_city
        if self.billing_state:
            if address:
                address += ", " + self.billing_state
            else:
                address += self.billing_state
        if self.billing_postcode:
            if address:
                address += ", " + self.billing_postcode
            else:
                address += self.billing_postcode
        if self.billing_country:
            if address:
                address += ", " + self.get_billing_country_display()
            else:
                address += self.get_billing_country_display()
        return address

    @property
    def created_on_arrow(self):
        return arrow.get(self.created_on).humanize()

    @property
    def contact_values(self):
        contacts = list(self.contacts.values_list('id', flat=True))
        return ','.join(str(contact) for contact in contacts)


class Email(models.Model):
    from_company = models.ForeignKey(
        Company, related_name='sent_email2', on_delete=models.SET_NULL, null=True)
    recipients = models.ManyToManyField(Contact, related_name='recieved_email2')
    message_subject = models.TextField(null=True)
    message_body = models.TextField(null=True)
    timezone = models.CharField(max_length=100, default='UTC')
    scheduled_date_time = models.DateTimeField(null=True)
    scheduled_later = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    from_email = models.EmailField()
    rendered_message_body = models.TextField(null=True)


    def __str__(self):
        return self.message_subject



class EmailLog(models.Model):
    """ this model is used to track if the email is sent or not """

    email = models.ForeignKey(Email, related_name='email_log2', on_delete=models.SET_NULL, null=True)
    contact = models.ForeignKey(Contact, related_name='contact_email_log2', on_delete=models.SET_NULL, null=True)
    is_sent = models.BooleanField(default=False)

class DocumentFormat(models.Model):
    company =models.OneToOneField(Company,related_name='company_doc_format',on_delete=models.CASCADE)
    
    quot_upper_format=models.CharField(choices=UPPER_CHOICES,max_length=20)
    quot_middle_format=models.CharField(choices=MIDDLE_CHOICES,max_length=20)
    quot_lower_format=models.CharField(choices=LOWER_CHOICES,max_length=20)

    invoice_upper_format=models.CharField(choices=UPPER_CHOICES,max_length=20)
    invoice_middle_format=models.CharField(choices=MIDDLE_CHOICES,max_length=20)
    invoice_lower_format=models.CharField(choices=LOWER_CHOICES,max_length=20)

    receipt_upper_format=models.CharField(choices=UPPER_CHOICES,max_length=20)
    receipt_middle_format=models.CharField(choices=MIDDLE_CHOICES,max_length=20)
    receipt_lower_format=models.CharField(choices=LOWER_CHOICES,max_length=20)

    def __str__(self):
        return str(self.company)+" Document Format"

    def as_json(self):
        return dict(
            quot_upper_format=self.quot_upper_format,
            quot_middle_format=self.quot_middle_format,
            quot_lower_format=self.quot_lower_format,
            invoice_upper_format=self.invoice_upper_format,
            invoice_middle_format=self.invoice_middle_format,
            invoice_lower_format=self.invoice_lower_format,
            receipt_upper_format=self.receipt_upper_format,
            receipt_middle_format=self.receipt_middle_format,
            receipt_lower_format=self.receipt_lower_format
        )

class DocumentHeaderInformation(models.Model):
    company =models.OneToOneField(Company,related_name='company_doc_header',on_delete=models.CASCADE)

    tel=models.CharField(max_length=20,blank=True, null=True)
    email=models.EmailField(blank=True, null=True)
    fax=models.CharField(max_length=20,blank=True, null=True)
    address= models.CharField(max_length=512, blank=True, null=True)

    def __str__(self):
        return str(self.company)+" Document Header"

    def as_json(self):
        return dict(
            tel=self.tel,
            email=self.email,
            fax=self.fax,
            address=self.address
        )



class ChargingStages(models.Model):
    company =models.OneToOneField(Company,related_name='company_charging_stages',on_delete=models.CASCADE)

    quantity=models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(99)])

    values=ArrayField(models.PositiveIntegerField(),size=99)

    descriptions=ArrayField(models.TextField(blank=True),size=99)



    def __str__(self):
        return str(self.company)+"'s Charging Stage"

    def as_json(self):
        return dict(
            quantity=self.quantity,
            values=self.values,
            descriptions=self.descriptions
        )

class QuotationGeneralRemark(models.Model):
    company =models.ForeignKey(Company,related_name='company_quotation_general_remarks',on_delete=models.CASCADE)

    index=models.PositiveIntegerField()
    content=models.TextField()

    def __str__(self):
        return str(self.company)+"Quotation Remark: "+str(self.index)

    def as_json(self):
        return dict(
            index=self.index,
            content=self.content
        )

class InvoiceGeneralRemark(models.Model):
    company =models.ForeignKey(Company,related_name='company_invoice_general_remarks',on_delete=models.CASCADE)

    index=models.PositiveIntegerField()
    content=models.TextField()

    def __str__(self):
        return str(self.company)+"Invoice Remark: "+str(self.index)

    def as_json(self):
        return dict(
            index=self.index,
            content=self.content
        )

class ReceiptGeneralRemark(models.Model):
    company =models.ForeignKey(Company,related_name='company_receipt_general_remarks',on_delete=models.CASCADE)

    index=models.PositiveIntegerField()
    content=models.TextField()

    def __str__(self):
        return str(self.company)+"Receipt Remark: "+str(self.index)

    def as_json(self):
        return dict(
            index=self.index,
            content=self.content
        )