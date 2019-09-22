from .bool import *

# None -------------------------------------------------------

class none:
    def __init__(ss, commentaire=''):
         make_id(ss)

         ss.commentaire = commentaire

    def __eq__(ss, obj):
        return None == obj
    def __ne__(ss, obj):
        return None != obj
    
    def __str__(ss):
        return 'O"%s"'%(ss.commentaire)
    def __repr__(ss):
        return '%s'%None
    
    def __iter__(ss):
        yield None

    def __hash__(ss):
        return hash(None)