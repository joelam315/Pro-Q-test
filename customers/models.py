import arrow
import time
from django.db import models
from django.utils.translation import ugettext_lazy as _

from common.models import Address, User
from phonenumber_field.modelfields import PhoneNumberField
from teams.models import Teams
from sorl.thumbnail import get_thumbnail
from django.conf import settings

def img_url(self, filename):
    hash_ = int(time.time())
    return "%s/%s/%s" % ("customer_profile_pics", hash_, filename)

class Customer(models.Model):
    first_name = models.CharField(_("First name"), max_length=255)
    last_name = models.CharField(_("Last name"), max_length=255)
    email = models.EmailField(blank=True,null=True,unique=True)
    phone = PhoneNumberField(unique=True)
    address = models.ForeignKey(
        Address, related_name='address_customers',
        on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    assigned_to = models.ManyToManyField(
        User, blank=True, related_name='customer_assigned_users')
    created_by = models.ForeignKey(
        User, related_name='customer_created_by',
        on_delete=models.SET_NULL, null=True)
    created_on = models.DateTimeField(_("Created on"), auto_now_add=True)
    is_active = models.BooleanField(default=False)
    teams = models.ManyToManyField(Teams, blank=True, related_name='customer_teams')
    profile_pic = models.FileField(
        max_length=1000, upload_to=img_url, null=True, blank=True)

    def __str__(self):
        return self.first_name

    def as_json(self):
        companies=self.company_customers.all()
        return dict(
            id=self.id,
            first_name = self.first_name,
            last_name = self.last_name,
            email=self.email,
            phone=str(self.phone),
            address=self.address.as_json(),
            description=self.description,
            icon="" if not self.profile_pic else get_thumbnail(self.profile_pic,'100x100').url,
            company=[ (company.id,company.name) for company in companies]
        )

    @property
    def created_on_arrow(self):
        return arrow.get(self.created_on).humanize()

    class Meta:
        ordering = ['-created_on']
