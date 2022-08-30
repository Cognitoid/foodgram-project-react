import re

from django.core.exceptions import ValidationError


def LatinAlphabetNumberValidator(value):
    reg = re.compile('^[-a-zA-Z0-9_]+$')
    if not reg.match(value):
        raise ValidationError(
            'Поле может содержать символы: A-Z, a-z, 0-9'
        )
