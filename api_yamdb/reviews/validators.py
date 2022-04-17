from django.core.exceptions import ValidationError
from django.utils import timezone


def my_year_validator(value):
    if value < 2000 or value > timezone.now().year:
        raise ValidationError(
            (f'{value} - Вы выбрали неверный год!'),
            params={'value': value},
        )


def my_score_validator(value):
    if value < 1 or value > 10:
        raise ValidationError(
            (f'{value} - Вы выбрали неверное значение рейтинга!'),
            params={'value': value},
        )
