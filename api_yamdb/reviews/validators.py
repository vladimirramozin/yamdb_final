from django.utils import timezone
from django.core.exceptions import ValidationError


def year_not_in_future_validator(value):
    if value > timezone.now().year:
        raise ValidationError("Год из будущего!")
