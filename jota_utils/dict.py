from contextlib import suppress
from functools import reduce
import json


def getattr_nl(obj, name, default=None):
    """ Allows dot notation lookup for dicts and class instances.

    Ex: getattr_nl(obj, 'foo.bar')
    """

    try:
        fn_lookup = dict.get if obj and isinstance(obj, dict) else getattr

        return reduce(fn_lookup, name.split('.'), obj)
    except AttributeError:
        return default


def pluck(key, obj):
    """ Given a list of dictionaries, extracts all
    values for a specific key.

    Ex: data = [{value: 1}, {value: 2}]
        pluck('value', data)
        -> [1, 2]
    """

    return [item[key] for item in obj]


def setattrs(obj, attrs):
    """ Fills a dict with multiple attributes."""

    for key, value in attrs:
        setattr(obj, key, value)


def is_superset(superset, smallset):
    """ Returns true if `smallset` has one or more attributes from `superset`. """

    if not smallset and superset:
        return False

    return smallset.items() <= superset.items()


def json_loads(json_string, default=None):
    """ Decode a JSON string, allowing default value on decoding error."""

    with suppress(json.decoder.JSONDecodeError, TypeError):
        return json.loads(json_string)

    return default
