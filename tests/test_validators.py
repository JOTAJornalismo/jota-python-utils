from unittest import TestCase
from django.forms import ValidationError
from jota_utils.validators import validate_min_length
import os

from django.conf import settings
import django

if not settings.configured:
    settings.configure(
        SECRET_KEY="dummy",
        INSTALLED_APPS=[],
        PHONENUMBER_DEFAULT_REGION='BR',
    )
    
    django.setup()


from jota_utils.validators import validate_phone, validate_url

VALID_PHONE = '+5511923456789'
INVALID_PHONE = '+5511123456789'


# TODO Add tests with different phone format and region
class ValidatePhoneTest(TestCase):
    
    def test_valid_phone(self):
        self.assertIsNone(validate_phone(VALID_PHONE))

    def test_invalid_phone(self):
        with self.assertRaises(ValidationError) as e:
            validate_phone(INVALID_PHONE)
            self.assertEqual('Phone is not valid', str(e.exception))


class ValidateURLTest(TestCase):

    def test_valid_url(self):
        self.assertIsNone(validate_url('https://www.jota.pro'))

    def test_invalid_url(self):
        with self.assertRaises(ValidationError):
            validate_url('wwwjotapro')

class ValidateMinLengthTest(TestCase):
    
    def test_valid_min_length(self):
        self.assertIsNone(validate_min_length(5, 'abcdefgh'))

    def test_invalid_min_length(self):

        with self.assertRaises(ValidationError) as e:
            validate_min_length(10, 'abc')
            self.assertIn('Ensure this value has at least 10 characters', str(e.exception))            
