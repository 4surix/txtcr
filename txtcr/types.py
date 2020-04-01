from ._utile import *


# Nbr
def mk_nbr(texte):
    if ',' in texte:
        nbr = float(texte.replace(',', '.'))
    elif '.' in texte:
        nbr = float(texte)
    else:
        nbr = int(texte)

    return nbr


# Bool
class TCRBool:

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
        return '%s%s' % (self.value, ' #' + self.commentaire if self.commentaire else '')

    def __repr__(self):
        return '%s' % self.value

    def __index__(self):
        return self.value * 1

    def __hash__(self):
        return hash(self.value)


# None
class TCRNone:

    def __init__(self, commentaire=''):
        self.commentaire = commentaire

    def __bool__(self):
        return False

    def __eq__(self, obj):
        return obj is None

    def __ne__(self, obj):
        return obj is not None

    def __str__(self):
        return 'None%s' % (' #' + self.commentaire if self.commentaire else '')

    def __repr__(self):
        return '%s' % None

    def __hash__(self):
        return hash(None)


# Class
def new_clss(encode):
    class Clss:

        str__ = None
        repr__ = None
        cmdcode__ = None
        date__ = None
        hash__ = None
        encode__ = None

        __name__ = ''

        def __init__(self, encode_):

            Clss.encode__ = encode_

        def __len__(self):
            return len(self.__dict__)

        def __str__(self):

            istr = Clss.str__

            if istr:
                return self.__format(istr)
            else:
                return '<:TCR: %s>' % Clss.__name__

        def __repr__(self):

            irepr = Clss.repr__

            if irepr:
                return self.__format(irepr)
            else:
                return str(self)

        def __format(self, texte):

            return texte.format(**{
                'N#': Clss.__name__,
                'D#': Clss.__doc__,
                'S#': Clss.str__,
                'R#': Clss.repr__,
                'C#': Clss.cmdcode__,
                'T#': Clss.date__,
                'H#': Clss.hash__,
                'I#': self
            })

        def __getitem__(self, item):

            return self.__dict__[item]

        def __setitem__(self, item, value):

            if item == "N#":
                Clss.__name__ = value

            elif item == "D#":
                Clss.__doc__ = value

            elif item == 'R#':
                Clss.repr__ = value

            elif item == 'S#':
                Clss.str__ = value

            elif item == "C#":
                Clss.cmdcode__ = value

            elif item == "T#":
                Clss.date__ = value

            elif item == "H#":
                Clss.hash__ = value

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
            return Clss.encode__(self)

        def get(self, item, defaut=None):

            value = {
                'N#': '__name__',
                'D#': '__doc__',
                'R#': 'repr__',
                'S#': 'str__',
                'C#': 'cmdcode__',
                'T#': 'date__',
                'H#': 'hash__'
            }.get(item)

            if value:
                value = getattr(Clss, value, None)
                if value is None:
                    value = defaut
                return value

            elif item == 'I#':
                value = {k: v for k, v in self.__dict__.items()}
                if not value:
                    value = defaut

            else:
                value = self.__dict__.get(item, defaut)

            return value

        def setdefault(self, item, defaut=None):

            value = {
                'N#': '__name__',
                'D#': '__doc__',
                'R#': 'repr__',
                'S#': 'str__',
                'C#': 'cmdcode__',
                'T#': 'date__',
                'H#': 'hash__'
            }.get(item)

            if value:
                value = getattr(Clss, value, None)
                if value is None:
                    setattr(Clss, value, defaut)
                    value = defaut
                return value

            elif item == 'I#':
                if not self.__dict__:
                    for k, v in defaut.items():
                        self.__dict__[k] = v

                return {k: v for k, v in self.__dict__.items()}

            else:
                value = self.__dict__.setdefault(item, defaut)

            return value

    return Clss(encode)
