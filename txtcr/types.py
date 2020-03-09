from ._utile import *


### Nbr

def mk_nbr(texte):

    if ',' in texte: nbr = float(texte.replace(',', '.'))
    elif '.' in texte: nbr = float(texte)
    else: nbr = int(texte)

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

            self.encode__ = encode

            self.str__ = None
            self.repr__ = None
            self.cmdcode__ = None
            self.date__ = None

            self.name__ = self.__class__.__name__ = ''
            self.doc__ = self.__class__.__doc__

        def __len__(self):
            return len(self.__dict__)

        def __str__(self):
            istr = self.str__
            if istr:
                return self.__format(istr)
            else:
                return '<:TCR: %s>' % self.name__

        def __repr__(self): 
            irepr = self.repr__
            if irepr:
                return self.__format(irepr)
            else:
                return str(self)

        def __format(self, texte):

            return texte.format(**{
                'N#': self.__class__.__name__,
                'D#': self.__class__.__doc__,
                'S#': self.str__,
                'R#': self.repr__,
                'C#': self.cmdcode__,
                'T#': self.date__,
                'I#': self
            })

        def __getitem__(self, item):
            return self.__dict__[item]

        def __setitem__(self, item, value):

            if item == "N#":
                self.__class__.__name__ = self.name__ = value

            elif item == "D#":
                self.__class__.__doc__ = self.doc__ = value

            elif item == 'R#':
                self.repr__ = '"%s"' % value

            elif item == 'S#':
                self.str__ = '"%s"' % value

            elif item == "C#":
                self.cmdcode__ = value

            elif item == "T#":
                self.date__ = value

            elif item == "H#":
                self.hash__ = value

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
                if str(key)[-2:] != '__':
                    yield key

        def values(self):
            for key, value in self.__dict__.items():
                if str(key)[-2:] != '__':
                    yield value

        def items(self):
            for key, value in self.__dict__.items():
                if str(key)[-2:] != '__':
                    yield key, value

        def encode(self):
            return self.encode__(self)

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
                value = self.__dict__.get(value)
                if value is None:
                    value = defaut
                return value

            elif item == 'I#':
                value = {k:v for k, v in self.__dict__.items() if str(k)[-2:] != '__'}
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
                value = self.__dict__.get(value)
                if not value:
                    self.__dict__[item] = value = defaut
                return value

            elif item == 'I#':
                if not self.__dict__:
                    for k, v in defaut.items():
                        self.__dict__[k] = v

                return {k:v for k, v in self.__dict__.items() if str(k)[-2:] != '__'}

            else:
                value = self.__dict__.setdefault(item, defaut)

            return value

    return clss(encode)