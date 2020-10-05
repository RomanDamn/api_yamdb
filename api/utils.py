from datetime import datetime

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


def current_year():
    return datetime.now().strftime("%Y")


def max_value_current_year(value):
    if value > 2100:
        raise ValidationError(
            _("%(value)s is not a correct year!"),
            params={"value": value},
        )
