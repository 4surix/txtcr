from .str import *

# Bytes ---------------------------------------------------------

class bytes(py_bytes):
    def __init__(ss, texte):
        make_id(ss)

        ss.value = texte
        ss.value_str = ss.value.decode('utf8')

    def __eq__(ss, obj):
        return ss.value_str == obj
    def __ne__(ss, obj):
        return ss.value_str != obj
    
    def __str__(ss):
        return "%s"%ss.value_str
    def __repr__(ss):
        return "'%s'"%ss.value_str

    def __add__(ss, value):
        if not isinstance(value, (int, pos, neg)):
            raise TypeError("%s objet n'est pas additionable pour les types bytes, 'pos' 'neg' seulement"%type(value).__name__)

        l = list(ss.value)
        l.append(value)

        return bytes(py_bytes(l))

    def __hash__(ss):
        return hash(ss.value_str)

    #def __index__(ss): return sum(ss.verif(get_vars(ss.clss)))