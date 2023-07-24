from unittest import TestCase
import pytz

from dateutil.parser import ParserError

from jota_utils.datetime import utc_to_local


class UtcToLocalTests(TestCase):
    tz = pytz.timezone('America/Sao_Paulo')

    def test_with_iso_date(self):
        self.assertIn('2023-07-24 16:00', str(utc_to_local('2023-07-24T19:00:00', self.tz)))
        self.assertIn('2023-01-01 19:00', str(utc_to_local('2023-01-01T22:00:00', self.tz)))

    def test_without_iso_date(self):
        self.assertIn('2023-07-24 16:00', str(utc_to_local('2023-07-24 19:00', self.tz)))

    def test_invalid(self):
        self.assertRaises(TypeError, utc_to_local, None, self.tz)
        self.assertRaises(ParserError, utc_to_local, '', self.tz)
