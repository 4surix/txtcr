# coding: utf-8
# Python 3.6.2
# ----------------------------------------------------------------------------

from functools import partial


from txtcr.core.types import *
from txtcr.core.encode import encode


class ConteneurBase:
    value = None
    key = 0
    keys_generals = []
    position = []


class Conteneur:

    def __init__(self, conteneur_parent, value):

        self.conteneur_parent = conteneur_parent

        self.value = value

        self.__config_add()

        # Les objets qui seront dans ce conteneur
        #  sont d'abors enregistrés en texte 
        #  puis transformés dans self.convert()
        self.texte = ''

        self.type = ''

        # Sert à enregistrer la key ou l'index,
        #  dans le cas de définir la position actuel,
        #  et pour dans le cas d'un dictionnaire 
        #  enregistrer d'abord la clé pour ensuite
        #  l'utiliser quand il faudrat mettre la valeur.
        self.key = 0 if isinstance(value, (list, tuple)) else ''

        if (
            # [
            #    :key
            #    { <--
            #        []
            #    }
            # ]
            conteneur_parent.value.__class__ == dict
            # [ <--
            #    :key
            #    {
            #        []
            #    }
            # ]
            and conteneur_parent.conteneur_parent.keys_generals
        ):
            index = (
                conteneur_parent.conteneur_parent.keys_generals[
                    len(conteneur_parent.value)
                ]
            )

        else:
            index = conteneur_parent.key

        # Retrace tout les keys/indexs précédentes.
        self.position = conteneur_parent.position + [index]

        self.index_KG = 0
        self.keys_generals = []
        self.is_key_general = False

    def convert(self):

        # Convertion texte en type Python

        texte = self.texte

        if self.type == '"':
            value = str(texte)

        elif self.type in ['+', '-']:
            value = mk_nbr(self.type + texte)

        elif self.type == "'":
            value = texte.encode()

        elif self.type in balises_categories:
            value = self.type + '#'

        elif self.type == '##':
            value = str(texte.strip())

            if value == 'True':
                value = True
            elif value == 'False':
                value = False
            elif value == 'None':
                value = None


        if self.is_key_general:
            self.is_key_general = False
            self.keys_generals.append(value)
            self.index_KG += 1

        else:
            self.add(value)


        # Mise à zéro des valeurs pour accueillir le prochain objet
        self.texte = ''
        self.type = ''

    def __dict_add(self, value):

        if self.conteneur_parent.keys_generals:
            self.key = self.conteneur_parent.keys_generals[len(self.value)]

        if self.key != '':
            self.value[self.key] = value
            self.key = ''

        else:
            self.key = value

    def __list_add(self, value):
        self.value.append(value)
        self.key += 1

    def __tuple_add(self, value):
        self.value += (value,)
        self.key += 1

    def __config_add(self):

        if isinstance(self.value, dict):
            self.add = self.__dict_add

        elif isinstance(self.value, list):
            self.add = self.__list_add

        elif isinstance(self.value, tuple):
            self.add = self.__tuple_add

        elif is_class(self.value) and 'repr__' in dir(value):
            self.add = self.__dict_add


def raise_bad_char_close(carac, conteneur):

    raise ValueError(
        'Mauvais carac fermeture " %s " pour type " %s "' % (
            carac,
            conteneur.value.__class__.__name__
        )
        + '\nTraceback (index/key):'
        + '\n' + '\n'.join(
            ('    ' * i) + str(value)
            for i, value in enumerate(conteneur.position)
        )
    )


def decode(texte, *, exclues=[], ever_list=False):

    echappement = False
    conteneur = Conteneur(ConteneurBase, [])
    conteneur.position.pop(0)

    taille_texte = len(texte)

    for position, carac in enumerate(texte):

        ### Carac spécial

        if carac == '\n' or carac == '\t':

            if conteneur.type == '"' or conteneur.type == "'":
                """

                {"pouet" "paf"
                 "pomme" "il était une pomme
                 sur un arbre"
                }

                ["pomme"] == "il était une pomme sur un arbre"

                """
                continue

            carac = ' '


        ### Ouverture
            
        if not conteneur.type:

            if carac == ' ':
                continue

            is_continue = True

            carac_suivant = (
                '' if taille_texte == position + 1
                else
                    texte[position + 1]
            ) 

            if carac == '"':
                # "Pouet"
                conteneur.type = carac

            elif carac == "'":
                # 'Pouf'
                conteneur.type = carac

            elif carac in ['+', '-'] and carac_suivant in chiffres:
                # +3456 -876
                conteneur.type = carac

            elif carac in chiffres:
                # 765434
                conteneur.type = '+'
                conteneur.texte += carac

            elif carac == '{':
                # {"pouet" 123456}
                conteneur = Conteneur(conteneur, {})

            elif carac == '[':
                # ["pouf" "poire" 1234]
                conteneur = Conteneur(conteneur, [])

            elif carac == '(':
                # (34.6 "wouf" 'pouet')
                conteneur = Conteneur(conteneur, ())

            elif carac == '<':
                # <I#{}>
                conteneur = Conteneur(conteneur, new_clss(encode))

            elif carac in balises_categories and carac_suivant == '#':
                """
                N#Pouet
                I#{}
                ...
                """
                conteneur.type = carac

            elif carac == '/' and carac_suivant == '/':
                """ Commantaire

                {// Information //
                 ID 123456
                 // Autre //
                 langage "fr"
                 heure "UTC"
                }

                """
                conteneur.type = '//'

            elif carac == ':':
                """
                [
                    : pomme
                    : poire

                    {
                        "rouge"
                        "verte"
                    }
                ]
                """
                conteneur.is_key_general = True

            elif carac not in [
                    '>', '}', ']', ')', # Balises fermante
                    '#', ',', ':', '=' # Séparations
                ]:
                conteneur.type = '##'
                conteneur.texte += carac

            else:
                is_continue = False

            if is_continue:
                continue


        ### Texte

        if (
            not echappement
            and (
                carac == conteneur.type == '"'
                or carac == conteneur.type == "'"
            )
        ):
            conteneur.convert()


        ### Echappement

        elif carac == '\\':

            if echappement:
                # "Pomme \\ poire"
                echappement = False
                conteneur.texte += '\\'

            else:
                # "Pomme \ poire"
                echappement = True

            # Evite que l'échappement revient à False tout en bas
            continue

        elif echappement:

            if carac == 'n':
                # "Pomme \n poire"
                conteneur.texte += '\n'

            elif carac == 't':
                # "Pomme \t poire"
                conteneur.texte += '\t'


        ### Ajout de caractére

        elif (
            conteneur.type == '"'
            or conteneur.type == "'"
        ):
            # "Pomme"
            # 'Pomme'
            conteneur.texte += carac


        ### Chiffres

        elif (
            conteneur.type == '+'
            or conteneur.type == '-'
        ):
            # +123
            # -123
            if carac not in '0123456789.':
                conteneur.convert()
            else:
                conteneur.texte += carac


        ### Fermeture conteneur

        elif carac == ')':
            if conteneur.value.__class__ != tuple:
                raise_bad_char_close(carac, conteneur)

            if conteneur.texte: conteneur.convert()

            conteneur.conteneur_parent.add(conteneur.value)
            conteneur = conteneur.conteneur_parent

        elif carac == ']':
            if conteneur.value.__class__ != list:
                raise_bad_char_close(carac, conteneur)

            if conteneur.texte: conteneur.convert()

            conteneur.conteneur_parent.add(conteneur.value)
            conteneur = conteneur.conteneur_parent

        elif carac == '}':
            if conteneur.value.__class__ != dict:
                raise_bad_char_close(carac, conteneur)

            if conteneur.texte: conteneur.convert()

            conteneur.conteneur_parent.add(conteneur.value)
            conteneur = conteneur.conteneur_parent

        elif carac == '>':
            if not getattr(conteneur.value.__class__, 'encode__', None):
                raise_bad_char_close(carac, conteneur)

            if conteneur.texte: conteneur.convert()

            conteneur.conteneur_parent.add(conteneur.value)
            conteneur = conteneur.conteneur_parent

        elif carac == '#':
            if conteneur.type not in balises_categories:
                raise_bad_char_close(carac, conteneur)

            conteneur.convert()


        ### Fin texte sans balise ou ajout carac

        elif conteneur.type == '##':
            if (
                carac == ' '    # pouet "pomme"
                or carac == ',' # pouet, "pomme"
                or carac == ':' # pouet: "pomme"
                or carac == '=' # pouet= "pomme"
            ):
                conteneur.convert()
            else:
                conteneur.texte += carac


        if echappement:
            echappement = False


    retour = conteneur.value

    if not retour and not ever_list:
        return None

    elif len(retour) == 1 and not ever_list:
        return retour[0]

    else:
        return retour