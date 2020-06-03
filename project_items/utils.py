import pytz
from django.utils.translation import ugettext_lazy as _

PROJECT_TYPE=(
	('Frotn-end','Front-end'),
	('Back-end','Back-end'),
	('System','System'),
	('Design','Design')
)

PROJECT_STATUS=(
	('Requested','Requested'),
	('Pending','Pending'),
	('Rejected','Rejected'),
	('Approved','Approved')
)