from ._utile import *

# Nbr --------------------------------------------------------

def mk_nbr(texte):

    if ',' in texte: nbr = float(texte.replace(',', '.'))
    elif '.' in texte: nbr = float(texte)
    else: nbr = int(texte)

    return nbr

# Bool -------------------------------------------------------

class bool:
    def __init__(ss, value, commentaire=''):
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

    def __index__(ss): 
        return ss.value*1

    def __hash__(ss):
        return hash(ss.value)

# None -------------------------------------------------------

class none:
    def __init__(ss, commentaire=''):
         ss.commentaire = commentaire

    def __eq__(ss, obj):
        return None == obj
    def __ne__(ss, obj):
        return None != obj
    
    def __str__(ss):
        return 'O"%s"'%(ss.commentaire)
    def __repr__(ss):
        return '%s'%None

    def __hash__(ss):
        return hash(None)

# Clss ------------------------------

def new_clss():

    class clss:

        def __init__(ss):

            ss.__class__.__name__ = ''
            ss.__class__.__istr__ = None
            ss.__class__.__irepr__ = None
            ss.__class__.__cmdcode__ = None
            ss.__class__.__date__ = None

        def __len__(ss):
            return len(ss.__dict__)

        def __str__(ss):
            istr = ss.__class__.__istr__
            if istr:
                return ss.__format(istr)
            else:
                return '<:clss: %s>'%ss.__class__.__name__

        def __repr__(ss): 
            clss = ss.__class__
            irepr = ss.__class__.__irepr__
            if irepr:
                return ss.__format(irepr)
            else:
                return '<:clss: %s>'%ss.__class__.__name__

        def __format(ss, texte):

            return texte.format(
                        N=clss.__name__,
                        D=clss.__doc__,
                        S=clss.__istr__,
                        R=clss.__irepr__,
                        C=clss.__cmdcode__,
                        T=clss.__date__,
                        I=ss
                        )

        def __getitem__(ss, key):
            return ss.__dict__[key]

        def __setitem__(ss, key, value):

            if key == "N#":
                ss.__class__.__name__ = value
            elif key == "D#":
                ss.__class__.__doc__ = value
            elif key == 'R#':
                ss.__class__.__irepr__ = value
            elif key == 'S#':
                ss.__class__.__istr__ = value
            elif key == "C#":
                ss.__class__.__cmdcode__ = value
            elif key == "T#":
                ss.__class__.__date__ = value
            elif key == "I#":
                for key, value in value.items():
                    ss.__dict__[key] = value
            else:
                ss.__dict__[key] = value

        def __iter__(ss):
            for item in ss.__dict__:
                yield item

        def keys(ss):
            for key in ss.__dict__.keys():
                yield key

        def values(ss):
            for value in ss.__dict__.values():
                yield value

        def get(ss, item, defaut=None):

            if item not in ['N#', 'D#', 'R#', 'S#', 'C#', 'T#']:
                value = ss.__dict__.get(item, defaut)

            elif item == 'N#':
                value = ss.__class__.__name__ 
                if not value:
                    value = defaut

            elif item == 'D#':
                value = ss.__class__.__doc__ 
                if not value:
                    value = defaut

            elif item == 'R#':
                value = ss.__class__.__irepr__ 
                if not value:
                    value = defaut

            elif item == 'S#':
                value = ss.__class__.__istr__ 
                if not value:
                    value = defaut

            elif item == 'C#':
                value = ss.__class__.__cmdcode__ 
                if not value:
                    value = defaut

            elif item == 'T#':
                value = ss.__class__.__date__ 
                if not value:
                    value = defaut

            return value

        def getnew(ss, item, nouv=None):

            if item not in ['N#', 'D#', 'R#', 'S#', 'C#', 'T#']:
                value = ss.__dict__.setdefault(item, nouv)

            elif item == 'N#':
                value = ss.__class__.__name__ 
                if not value:
                    ss.__class__.__name__ = nouv
                    value = nouv

            elif item == 'D#':
                value = ss.__class__.__doc__ 
                if not value:
                    ss.__class__.__doc__ = nouv
                    value = nouv

            elif item == 'R#':
                value = ss.__class__.__irepr__ 
                if not value:
                    ss.__class__.__irepr__ = nouv
                    value = nouv

            elif item == 'S#':
                value = ss.__class__.__istr__ 
                if not value:
                    ss.__class__.__istr__ = nouv
                    value = nouv

            elif item == 'C#':
                value = ss.__class__.__cmdcode__ 
                if not value:
                    ss.__class__.__cmdcode__ = nouv
                    value = nouv

            elif item == 'T#':
                value = ss.__class__.__date__ 
                if not value:
                    ss.__class__.__date__ = nouv
                    value = nouv

            return value

    return clss()