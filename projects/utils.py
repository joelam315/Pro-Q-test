import pytz
from django.utils.translation import ugettext_lazy as _

PROJECT_STATUS = (
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

ROOM_TYPE = (
    ('Toilet',_('廁所')),
    ('Kitchen',_('廚房')),
    ('Living Room',_('客廳')),
    ('Dinning Room',_('飯廳')),
    ('1 Person Bed Room',_('一人睡房')),
    ('2 Persons Bed Room',_('兩人睡房')),
)