from .decode import decode as _decode
from .encode import encode as _encode

from .types import * 

from . import requete


def decode(data, **ops):
    return _decode(data, **ops)


def encode(data, **ops):
    return _encode(data, **ops)


### Param

class param:

    class R:

        def __getitem__(self, item):
            class R:
                repr__ = item
            return R
        
    R = R()


    class S:

        def __getitem__(self, item):
            class S:
                str__ = item
            return S
        
    S = S()


    class T:

        def __getitem__(self, item):
            class T:
                date__ = item
            return T
        
    T = T()


### Fichier 

class fichier:
    """
    Ex: 
        with fichier('path/name.tcr') as f:
            f.pouet = "pouf"

            # Save Auto

        # ----------

        f = fichier('path/name.tcr')

        data = f() # Get data
        f(data) # Save data

        # or

        data = f.read()
        f.write(data)
    """

    def __init__(self, chemin, mode='r', *, indent=0, default=None):

        self.chemin = chemin
        self.mode = mode

        self.indent = indent
        self.default = default

    def __enter__(self):

        self.data = self.__open()
        return self.data

    def __exit__(self, exception_type, exception_value, retraçage):

        if self.mode == 'w':
            self.__save(self.data)

    def __open(self):

        try:
            fichier = open(self.chemin, 'r', encoding='utf-8')
            data = _decode(fichier.read())

        except FileNotFoundError as exception:
            # Dans le cas où le fichier n'existerai pas
            # Si une valeur par défaut a été definie, créer un ficher avec celle ci
            # Sinon léve l'erreur

            if self.default:
                fichier = open(self.chemin, 'w', encoding='utf-8')
                data = _decode(self.default)

            else:
                raise exception


        fichier.close()

        return data

    def __save(self, data):

        # Encode avant pour voir si tout est bon avant d'ouvrir le fichier
        data = _encode(data, indent=self.indent)
        # Enregistrement
        fichier = open(self.chemin, 'w', encoding='utf-8')
        fichier.write(data)
        fichier.close()

    def __call__(self, data=None):

        if not data:
            return self.__open()
        else:
            self.__save(data)

    def read(self):
        return self.__open()

    def write(self, data, *, indent=0):
        self.indent = indent if indent else self.indent
        
        self.__save(data)