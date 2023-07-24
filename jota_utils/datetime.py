import pytz

from dateutil.parser import parse


def utc_to_local(utc_date, local_tz):
    """Converts a UTC datetime to a local datetime.

    Ex: str(utc_to_local('2023-07-24T19:00:00', pytz.timezone('America/Sao_Paulo')))
        -> '2023-07-24 16:00'
    """

    return parse(utc_date).replace(tzinfo=pytz.utc).astimezone(local_tz)
