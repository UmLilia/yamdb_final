from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    if value < 0 or value > timezone.now().year:
        raise ValidationError(
            ('%(value)s некорректный год выпуска!'),
            params={'value': value},
        )
