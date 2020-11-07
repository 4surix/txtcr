# coding: utf-8
# Python 3.6.2
# ----------------------------------------------------------------------------

from .decode import decode
from .encode import encode


class FileManager:
    """
    Class allowing to quickly edit, save and get TCR files
    Classe permettant de gérer des fichiers rapidement 
      et des les écrire/lire en TCR

    Ex:
        with fichier('path/name.tcr') as f:
            f.pouet = "pouf"

            # Save Auto

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

    def __exit__(self, exception_type, exception_value, tracing):

        if self.mode == 'w':
            self.__save(self.data)

    def __open(self):

        try:
            fichier = open(self.chemin, 'r', encoding='utf-8')
            data = decode(fichier.read())

        except FileNotFoundError as exception:
            # Dans le cas où le fichier n'existerai pas,
            #   si une valeur par défaut a été definie
            #     alors créer un ficher avec celle ci,
            #   sinon léve l'erreur.

            if self.default:
                fichier = open(self.chemin, 'w', encoding='utf-8')
                data = decode(self.default)

            else:
                raise exception

        fichier.close()

        return data

    def __save(self, data):

        # Encode avant pour voir si tout est bon avant d'ouvrir le fichier.
        data = encode(data, indent=self.indent)
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
