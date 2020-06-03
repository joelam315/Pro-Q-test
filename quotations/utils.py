import pytz
from django.utils.translation import ugettext_lazy as _

QUOTATION_STATUS = (
        ('Draft', 'Draft'),
        ('Requested to Approve','Requested to Approve'),
        ('Approved','Approved'),
        ('Requested to Approve Signed','Requested to Approve Signed'),
        ('Signed', 'Signed'),
        ('Requested to Approve Paid','Requested to Approve Paid'),
        ('Paid', 'Paid'),
        ('Pending', 'Pending'),
        ('Cancelled', 'Cancel'),
    )