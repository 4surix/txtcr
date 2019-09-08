from .rac import *

# Pos et Neg ------------------------------------------------

def mk_nbr(nbr):
    nbr = py_str(nbr)

    if ',' in nbr: value = nbr.replace(',', '.')

    if '.' in nbr: 
        if nbr.split('.')[-1] == '0': 
            value = int(nbr.split('.')[0])
        else:
            value = float(nbr)
    else: value = int(nbr)
        
    if nbr[0] == '-':
        return neg(value)
    return pos(value)

class _nbr:

    def _if_pos_neg(ss, obj):
        if isinstance(obj, (neg, pos)):
            return obj.value
        return obj

    def __lt__(ss, obj):
        return ss.value < ss._if_pos_neg(obj)
    def __le__(ss, obj):
        return ss.value <= ss._if_pos_neg(obj)
    def __eq__(ss, obj):
        return ss.value == ss._if_pos_neg(obj)
    def __ne__(ss, obj):
        return ss.value != ss._if_pos_neg(obj)
    def __ge__(ss, obj):
        return ss.value >= ss._if_pos_neg(obj)
    def __gt__(ss, obj):
        return ss.value > ss._if_pos_neg(obj)
    
    def __iter__(ss):
        yield None
    
    def __abs__(ss):
        return abs(ss.value)
    
    def __pos__(ss):
        if isinstance(ss, pos):
            return ss
        return pos(-ss.value)
    def __neg__(ss):
        if isinstance(ss, neg):
            return ss
        return neg(-ss.value)

    def __add__(ss, obj):
        return mk_nbr(ss.value + ss._if_pos_neg(obj))
    def __sub__(ss, obj):
        return mk_nbr(ss.value - ss._if_pos_neg(obj))
    def __mul__(ss, obj):
        return mk_nbr(ss.value * ss._if_pos_neg(obj))
    def __truediv__(ss, obj):
        return mk_nbr(ss.value / ss._if_pos_neg(obj))
    def __floordiv__(ss, obj):
        return mk_nbr(ss.value // ss._if_pos_neg(obj))
    def __mod__(ss, obj):
        return mk_nbr(ss.value % ss._if_pos_neg(obj))
    def __pow__(ss, obj):
        return mk_nbr(ss.value ** ss._if_pos_neg(obj))

    def __hash__(ss):
        return hash(repr(ss))

    def __index__(ss):
        return int(ss.value)

    def __float__(ss):
        ss.value = float(ss.value)
        return ss

    def __int__(ss):
        ss.value = int(ss.value)
        return ss
    
class pos(_nbr):
    def __init__(ss, nbr):
        make_id(ss)

        if isinstance(nbr, (neg, pos)):
            ss.value = +abs(nbr.value)
        else:
            ss.value = +abs(nbr)

    def __str__(ss):
        return '+%s'%ss.value
    def __repr__(ss):
        return '+%s'%ss.value

class neg(_nbr):
    def __init__(ss, nbr):
        make_id(ss)

        if isinstance(nbr, (neg, pos)):
            ss.value = -abs(nbr.value)
        else:
            ss.value = -abs(nbr)

    def __str__(ss):
        return '%s'%ss.value
    def __repr__(ss):
        return '%s'%ss.value