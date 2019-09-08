from .cond import *

class _types:

    def __init__(ss):
        ss.pos = pos
        ss.neg = neg
        ss.bool = bool
        ss.str = str
        ss.bytes = bytes
        ss.calc = calc
        ss.cond = cond

    def __iter__(ss):
        for t in ss.__dict__:
            if t[:2] != '__':
                yield t

types = _types()