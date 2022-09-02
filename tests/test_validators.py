from unittest import TestCase
from django.forms import ValidationError

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
