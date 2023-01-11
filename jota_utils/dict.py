from contextlib import suppress
from functools import reduce
import json


def getattr_nl(obj, name, default=None):
    """ Allows dot notation lookup for dicts and class instances.

    Ex: getattr_nl(obj, 'foo.bar')
    """

    try:
        is_dict = lambda obj: obj and isinstance(obj, dict)
        extract_key = lambda value, key: value.get(key) if is_dict(value) else getattr(value, key)

        return reduce(extract_key, name.split('.'), obj)
    except (AttributeError, TypeError):
        return default


def pluck(key, obj):
    """ Given a list of dictionaries, extracts all
    values for a specific key.

    Ex: data = [{value: 1}, {value: 2}]
        pluck('value', data)
        -> [1, 2]
    """

    return [getattr_nl(item, key) for item in obj]


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


def with_except(obj, keys):
    """ Returns a dictionary without the specified keys. """

    return with_only(obj, set(obj.keys()) - set(keys))


def with_only(obj, keys):
    """ Returns a dictionary only with the specified keys. """

    return {key: value for key, value in obj.items() if key in keys}


def find_in_dict_list(search_key, value, dict):
    """ Search in a list of dicts by a specific key and value,
    returns a list of dicts corresponding to the search.

    Ex: data = [{'fruit': 'orange'}, {'fruit': 'apple'}, {'fruit': 'orange'}]
        find_in_dict_list('fruit', 'orange', data)
        -> [{'fruit': 'orange'}, {'fruit': 'orange'}]
    """

    return list(filter(lambda data: getattr_nl(data, search_key) == value, dict))


def find_first_in_dict_list(search_key, value, dict):
    """ Same as find_in_dict_list but returns only the first result. """

    result = find_in_dict_list(search_key, value, dict)

    return result[0] if result else None


def duplicates(key, obj):
    """ Given a list of dictionaries, returns the value of all keys
    which are present more than once.

    Ex: data = [{'value': 1}, {'value': 2}, {'value': 1}]
        duplicates('value', data)
        -> [1]
    """

    keys = pluck(key, obj)

    return list(set([i for i in keys if keys.count(i) > 1]))


def remove_duplicates(key, obj):
    """ Given a list of dictionaries, remove the items in
    which the key value is present more than once.

    Ex: data = [{'value': 1}, {'value': 2}, {'value': 1}]
        remove_duplicates('value', data)
        print(data)
        -> [{'value': 2}, {'value': 1}]
    """

    for item in obj.copy():
        if item[key] in duplicates(key, obj):
            obj.remove(item)
