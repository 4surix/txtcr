from .pos_neg import *

# Bool -------------------------------------------------------

class bool:
    def __init__(ss, value, commentaire=''):
         make_id(ss)

         ss.value = value
         ss.commentaire = commentaire

    def __bool__(ss):
        return ss.value
    def __eq__(ss, obj):
        return ss.value == obj
    def __ne__(ss, obj):
        return ss.value != obj
    
    def __str__(ss):
        return '%s"%s"'%(ss.value*1, ss.commentaire)
    def __repr__(ss):
        return '%s'%ss.value
    
    def __iter__(ss):
        yield None

    def __index__(ss): 
        return ss.value*1

    def __hash__(ss):
        return hash(ss.value)