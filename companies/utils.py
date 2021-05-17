import pytz
from django.utils.translation import ugettext_lazy as _

UPPER_CHOICES=(
	("A","A"),
	("B","B"),
	("C","C"),
	("D","D"),
	("E","E"),
	("F","F"),
	("H","H"),
	("I","I"),
	("J","J"),
	("K","K"),
	("L","L"),
	("M","M"),
	("N","N"),
	("O","O"),
	("P","P"),
	("Q","Q"),
	("R","R"),
	("S","S"),
	("T","T"),
	("U","U"),
	("V","V"),
	("W","W"),
	("X","X"),
	("Y","Y"),
	("Z","Z")
)

MIDDLE_CHOICES=(
	("Date",_("日期(YYYYMMDD)")),
	("Number",_("4位數字(0000-9999)")),
	("Alphabet",_("英文字母(A-Z)"))
)

LOWER_CHOICES=(
	("Number",_("4位數字(0000-9999)")),
	("Alphabet",_("英文字母(A-Z)"))
)

PROJECT_LOWER_CHOICES=(
	("Number",_("4位數字(0000-9999)")),
)