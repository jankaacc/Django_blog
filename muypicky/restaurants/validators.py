from django.core.exceptions import ValidationError


def validate_even(value):
    if value % 2 != 0:
        raise ValidationError(
            ('%(value)s is not an even number'),
            params={'value': value},
        )


def validate_email(value):
        email = value
        if ".edu" in email:
            raise ValidationError("We do not accept edu emails")


CATEGORIES = ['Mexican', 'American', 'Polskie']

def validate_category(value):
    CAT = map(lambda x:x.upper(), CATEGORIES)
    # cat = value.capitalize()
    if not value.upper() in CAT:
        raise ValidationError("{} is not in categories".format(value))