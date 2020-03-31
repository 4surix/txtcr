from ._utile import *


### Nbr

def mk_nbr(texte):

    if ',' in texte: 
        nbr = float(texte.replace(',', '.'))
    elif '.' in texte: 
        nbr = float(texte)
    else: 
        nbr = int(texte)

    return nbr


### Bool

class bool:

    def __init__(self, value, commentaire=''):
        self.value = value
        self.commentaire = commentaire

    def __bool__(self):
        return self.value

    def __eq__(self, obj):
        return self.value == obj

    def __ne__(self, obj):
        return self.value != obj


    def __str__(self):
        return '%s%s' % (self.value,' #'+self.commentaire if self.commentaire else '')

    def __repr__(self):
        return '%s' % self.value


    def __index__(self): 
        return self.value*1

    def __hash__(self):
        return hash(self.value)


### None

class none:

    def __init__(self, commentaire=''):
        self.commentaire = commentaire


    def __bool__(self):
        return False

    def __eq__(self, obj):
        return None == obj

    def __ne__(self, obj):
        return None != obj


    def __str__(self):
        return 'None%s' % (' #'+self.commentaire if self.commentaire else '')

    def __repr__(self):
        return '%s' % None


    def __hash__(self):
        return hash(None)


### Clss

def new_clss(encode):

    class clss:

        def __init__(self, encode):

            clss.encode__ = encode

            clss.str__ = None
            clss.repr__ = None
            clss.cmdcode__ = None
            clss.date__ = None
            clss.hash__ = None

            clss.name__ = clss.__name__ = ''
            clss.doc__ = clss.__doc__

        def __len__(self):

            return len(self.__dict__)

        def __str__(self):

            istr = clss.str__

            if istr:
                return self.__format(istr)
            else:
                return '<:TCR: %s>' % clss.name__

        def __repr__(self):

            irepr = clss.repr__

            if irepr:
                return self.__format(irepr)
            else:
                return str(self)

        def __format(self, texte):

            return texte.format(**{
                'N#': clss.name__,
                'D#': clss.doc__,
                'S#': clss.str__,
                'R#': clss.repr__,
                'C#': clss.cmdcode__,
                'T#': clss.date__,
                'H#': clss.hash__,
                'I#': self
            })

        def __getitem__(self, item):

            return self.__dict__[item]

        def __setitem__(self, item, value):

            if item == "N#":
                clss.name__ = value

            elif item == "D#":
                clss.doc__ = value

            elif item == 'R#':
                clss.repr__ = value

            elif item == 'S#':
                clss.str__ = value

            elif item == "C#":
                clss.cmdcode__ = value

            elif item == "T#":
                clss.date__ = value

            elif item == "H#":
                clss.hash__ = value

            elif item == "I#":
                for item, value in value.items():
                    self.__dict__[item] = value

            else:
                self.__dict__[item] = value

        def __delitem__(self, item):

            del self.__dict__[item]

        def __iter__(self):

            for item in self.__dict__:
                yield item

        def keys(self):

            for key in self.__dict__.keys():
                yield key

        def values(self):

            for key, value in self.__dict__.items():
                yield value

        def items(self):

            for key, value in self.__dict__.items():
                yield key, value

        def encode(self):
            return clss.encode__(self)

        def get(self, item, defaut=None):

            value = {
                'N#': 'name__',
                'D#': 'doc__',
                'R#': 'repr__',
                'S#': 'str__',
                'C#': 'cmdcode__',
                'T#': 'date__',
                'H#': 'hash__'
            }.get(item)

            if value:
                value = getattr(clss, value, None)
                if value is None:
                    value = defaut
                return value

            elif item == 'I#':
                value = {k:v for k, v in self.__dict__.items()}
                if not value:
                    value = defaut

            else:
                value = self.__dict__.get(item, defaut)

            return value

        def setdefault(self, item, defaut=None):

            value = {
                'N#': 'name__',
                'D#': 'doc__',
                'R#': 'repr__',
                'S#': 'str__',
                'C#': 'cmdcode__',
                'T#': 'date__',
                'H#': 'hash__'
            }.get(item)

            if value:
                value = getattr(clss, value, None)
                if value is None:
                    setattr(clss, value, defaut)
                    value = defaut
                return value

            elif item == 'I#':
                if not self.__dict__:
                    for k, v in defaut.items():
                        self.__dict__[k] = v

                return {k:v for k, v in self.__dict__.items()}

            else:
                value = self.__dict__.setdefault(item, defaut)

            return value

    return clss(encode)