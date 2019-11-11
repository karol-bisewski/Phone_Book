import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_phone_number(value):
    if not re.match(r"\d{7,}", value):
        raise ValidationError(
            _('%(value) is not a phone number'),
            params={'value': value},
            code='invalid')
