import pprint


def pp(obj, indent=4):
    """ Pretty printer for debugging purposes """
    p = pprint.PrettyPrinter(indent=indent)
    p.pprint(obj)


def throw(msg):
    raise Exception(msg)


class NoSuchKeyError(Exception):
    pass
