import pytz
from django.utils.translation import ugettext_lazy as _

PROJECT_STATUS = (
        ('Early Stage', _('未開始')),
        ('In Progress',_('進行中')),
        ('Finished',_('已完成')),
    )

ROOM_TYPE = (
    ('Toilet',_('廁所')),
    ('Kitchen',_('廚房')),
    ('Living Room',_('客廳')),
    ('Dinning Room',_('飯廳')),
    ('1 Person Bed Room',_('一人睡房')),
    ('2 Persons Bed Room',_('兩人睡房')),
)