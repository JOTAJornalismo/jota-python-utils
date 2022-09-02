def decode_utf8(iterator):
    """ Generator for utf-8 decoding """
    for line in iterator:
        yield line.decode('utf-8')
