import arrow
import time
from django.db import models
from django.utils.translation import ugettext_lazy as _

from common.models import Address, User
from phonenumber_field.modelfields import PhoneNumberField
from teams.models import Teams
from sorl.thumbnail import get_thumbnail
from django.conf import settings
from projects.models import Project

def img_url(self, filename):
    hash_ = int(time.time())
    return "%s/%s/%s" % ("customer_profile_pics", hash_, filename)

class Customer(models.Model):
    name = models.CharField(max_length=255)
    company_name= models.CharField(max_length=255,blank=True,null=True)
    email = models.EmailField(blank=True,null=True)
    phone = PhoneNumberField(blank=True,null=True)
    address = models.CharField(
        _("Contact Address"), max_length=1024, default="Pending", blank=True, null=True)
    project=models.OneToOneField(Project,on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, related_name='customer_created_by',
        on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

    def as_json(self):
        return dict(
            name = self.name,
            company_name = self.company_name,
            email=self.email,
            phone=str(self.phone) if str(self.phone)!="None" else "",
            address=self.address,
        )

    @property
    def created_on_arrow(self):
        return arrow.get(self.created_on).humanize()

    class Meta:
        ordering = ['-created_on']
