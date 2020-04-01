from .decode import decode as _decode
from .encode import encode as _encode

from .types import *

from . import requete


# Decoder
def decode(data, **ops):
    return _decode(data, **ops)


# Encoder
def encode(data, **ops):
    return _encode(data, **ops)


# Param

class Param:
    """
    Allows to create a class than inherits the given TCR parameter
    Permet de créer une classe qui va hériter d'un paramètre TCR.

    Params:
    - S / STR => class reaction to str() call
    - R / REPR => class reaction to repr() call
    - T / DATE => date the TCR was created at, or anything relevant. This parameter is always user-stated.

    Exemple:
        class Test(txtcr.Param.REPR["<{I#.pouf}>"]):
            # cette classe va hériter de la capacité à afficher la valeur de pouf (rouge) lors d'un repr() de la classe
            # this class will inherit capacity to print pouf value (rouge) when you call repr() with this class or inst
            pouf = rouge
    """

    class R:

        def __getitem__(self, item):
            class R:
                repr__ = item

            return R

    R = REPR = R()

    class S:

        def __getitem__(self, item):
            class S:
                str__ = item

            return S

    S = STR = S()

    class T:

        def __getitem__(self, item):
            class T:
                date__ = item

            return T

    T = DATE = T()


# Fichier
class Fichier:
    """
    Class allowing to quickly edit, save and get TCR files
    Classe permettant de gérer des fichiers rapidement et des les écrire/lire en TCR

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


# For english users
File = Fichier
