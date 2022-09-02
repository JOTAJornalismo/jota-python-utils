from django.core.validators import MinLengthValidator, URLValidator
from django.forms import ValidationError
from phonenumbers import format_number, is_valid_number, parse, PhoneNumberFormat
from phonenumber_field.phonenumber import PhoneNumber


def validate_phone(phone, region=None, number_format=PhoneNumberFormat.E164):
    phone = format_number(
        PhoneNumber.from_string(phone),
        number_format
    )

    if not is_valid_number(parse(phone, region)):
        raise ValidationError('Phone is not valid')


def validate_url(text):
    url_validator = URLValidator()
    url_validator(text)


def validate_min_length(limit, text, message=None):
    validator = MinLengthValidator(limit, message)
    validator(text)
