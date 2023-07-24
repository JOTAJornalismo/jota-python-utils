from unittest import TestCase
import pytz

from dateutil.parser import ParserError

from jota_utils.datetime import utc_to_local


class UtcToLocalTests(TestCase):
    tz = pytz.timezone('America/Sao_Paulo')

    def test_with_iso_date(self):
        self.assertIn('2018-12-31 22:00', str(utc_to_local('2019-01-01T00:00:00', self.tz)))
        self.assertIn('2019-01-01 20:00', str(utc_to_local('2019-01-01T22:00:00', self.tz)))

    def test_without_iso_date(self):
        self.assertIn('2018-12-31 22:00', str(utc_to_local('2019-01-01 00:00:00', self.tz)))

    def test_invalid(self):
        self.assertRaises(TypeError, utc_to_local, None, self.tz)
        self.assertRaises(ParserError, utc_to_local, '', self.tz)
