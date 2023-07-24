import pytz

from dateutil.parser import parse


def utc_to_local(utc_date, local_tz):
    """Converts a UTC datetime to a local datetime.

    Ex: str(utc_to_local('2019-01-01T00:00:00', pytz.timezone('America/Sao_Paulo')))
        -> '2018-12-31 22:00:00-03:00'
    """

    return parse(utc_date).replace(tzinfo=pytz.utc).astimezone(local_tz)
