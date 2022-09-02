from functools import reduce


def getattr_nl(obj, name, default=None):
    """ Same as getattr(), but allows dot notation lookup.

    Ex: getattr_nl(obj, 'foo.bar')
    """

    try:
        return reduce(getattr, name.split('.'), obj)
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
