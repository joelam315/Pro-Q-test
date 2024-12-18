import arrow
from django.db import models
from django.utils.translation import pgettext_lazy
from django.utils.translation import gettext_lazy as _

from companies.models import Company, Tags
from contacts.models import Contact
from common.models import User
from common.utils import STAGES, SOURCES, CURRENCY_CODES
from teams.models import Teams


class Opportunity(models.Model):
    name = models.CharField(pgettext_lazy(
        "Name of Opportunity", "Name"), max_length=64)
    company = models.ForeignKey(
        Company, related_name='opportunities',
        on_delete=models.CASCADE, blank=True, null=True)
    stage = models.CharField(
        pgettext_lazy("Stage of Opportunity",
                      "Stage"), max_length=64, choices=STAGES)
    currency = models.CharField(
        max_length=3, choices=CURRENCY_CODES, blank=True, null=True)
    amount = models.DecimalField(
        _("Opportunity Amount"),
        decimal_places=2, max_digits=12, blank=True, null=True)
    lead_source = models.CharField(
        _("Source of Lead"), max_length=255,
        choices=SOURCES, blank=True, null=True)
    probability = models.IntegerField(default=0, blank=True, null=True)
    contacts = models.ManyToManyField(Contact)
    closed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # closed_on = models.DateTimeField(blank=True, null=True)
    closed_on = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    assigned_to = models.ManyToManyField(
        User, related_name='opportunity_assigned_to')
    created_by = models.ForeignKey(
        User, related_name='opportunity_created_by',
        on_delete=models.SET_NULL, null=True)
    created_on = models.DateTimeField(_("Created on"), auto_now_add=True)
    is_active = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tags, blank=True)
    teams = models.ManyToManyField(Teams, related_name='oppurtunity_teams')

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.name

    @property
    def created_on_arrow(self):
        return arrow.get(self.created_on).humanize()
