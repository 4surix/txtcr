# coding: utf-8
# Python 3.6.2
# ----------------------------------------------------------------------------

from txtcr.util._utile import *


# Nbr
def mk_nbr(texte):
    if ',' in texte:
        nbr = float(texte.replace(',', '.'))
    elif '.' in texte:
        nbr = float(texte)
    else:
        nbr = int(texte)

    return nbr


# Class
def new_clss(encode):
    class Clss:

        str__ = None
        repr__ = None
        cmdcode__ = None
        date__ = None
        hash__ = None

        def __init__(self):

            Clss.__name__ = ''
            Clss.encode__ = encode

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

            return self.__dict__.keys()

        def values(self):

            return self.__dict__.items()

        def items(self):

            return self.__dict__.items()

        def encode(self, indent = 0):

            return Clss.encode__(self, indent = indent)

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
                return getattr(Clss, value, defaut)

            elif item == 'I#':
                return (
                    {**self.__dict__} if self.__dict__
                    else
                        defaut
                )

            else:
                return self.__dict__.get(item, defaut)

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

                return {**self.__dict__}

            else:
                return self.__dict__.setdefault(item, defaut)


    return Clss()
