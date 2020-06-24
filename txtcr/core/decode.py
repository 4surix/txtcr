from txtcr.core.types import *

from txtcr.core.encode import encode
from functools import partial


class Conteneur:

    def __init__(self, ancien_conteneur, value):
        self.ancien_conteneur = ancien_conteneur

        self.value = value

        # Les objets qui seront dans ce conteneur
        #  sont d'abors enregistrés en texte 
        #  puis transformés dans self.end()
        self.texte = []

        self.type = ''
        self.sous_type = ''

        # Si le conteneur actuel est un dictionnaire
        #  sert à enregistrer d'abord la clé pour ensuite
        #  l'utiliser quand il faudrat mettre la valeur
        self.key = ''
        
    def add_profondeur(self, value):
        return Conteneur(self, value)

    def rem_profondeur(self):
        conteneur = self.ancien_conteneur
        conteneur.save(self.value)
        return conteneur

    def config_clss(self, synt):

        clss = new_clss(encode)
        clss.__class__.__synt__ = synt # syntaxe

        conteneur = self.add_profondeur(clss)

        return conteneur
        
    def append(self, value):
        self.texte.append(value)

    def end(self):

        # Convertion texte en type Python

        self.type = self.sous_type + self.type

        texte = ''.join(self.texte)

        if self.type == '"':
            value = str(texte)

        elif self.type in ['+', '-']:
            value = mk_nbr(self.type+texte)

        elif self.type == '1"':
            value = True

        elif self.type == '0"':
            value = False

        elif self.type == 'O"':
            value = None

        elif self.type == "'":
            value = texte.encode()

        elif self.type in balises_categories:
            value = self.type+'#'

        elif self.type == '##':
            value = str(texte.strip())

            if value == 'True':
                value = True
            elif value == 'False':
                value = False
            elif value == 'None':
                value = None

        self.save(value)

    def save(self, value):

        if is_class(self.value) and 'repr__' in dir(self.value):

            if self.key != '':
                self.value[self.key] = value
                self.key = ''

            else:
                self.key = value

        elif isinstance(self.value, dict):

            if self.key != '':
                self.value[self.key] = value
                self.key = ''

            else:
                self.key = value

        elif isinstance(self.value, list):
            self.value.append(value)

        elif isinstance(self.value, tuple):
            self.value += (value,)

        # Mise à zéro des valeurs pour accueillir le prochain objet
        self.texte = []

        self.type = ''
        self.sous_type = ''


def decode(texte, *, exclues=[], ever_list=False):

    echappement = False
    conteneur = Conteneur(None, [])

    for place, carac in enumerate(texte):

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

            is_continue = True

            carac_suivant = texte[place+1] if len(texte) != place + 1 else ''

            if carac == '/' and carac_suivant == '/':
                """ Commantaire

                {// Information //
                 ID "dfeghyt"
                 // Autre //
                 langage "fr"
                 heure "UTC"
                }

                """
                conteneur.type = '//'

            elif carac == '<':
                conteneur = conteneur.config_clss(0)
            elif carac == '{':
                conteneur = conteneur.add_profondeur({})
            elif carac == '[':
                conteneur = conteneur.add_profondeur([])
            elif carac == '(':
                conteneur = conteneur.add_profondeur(())

            elif carac == '"':
                # "Pouet"
                conteneur.type = carac

            elif carac == "'":
                # 'Pouf'
                conteneur.config_type(carac)

            elif carac_suivant == '"':
                """Ancienne syntaxe pour None, False, True

                [O"None"
                 0"False"
                 1"True"
                ]
                """
                if carac == "O" or carac == "0" or carac == "1":
                    conteneur.sous_type = carac

            elif carac in ['+', '-'] and carac_suivant in chiffres:
                # +3456 -876
                conteneur.type = carac

            elif carac in chiffres:
                # 765434
                conteneur.append(carac)
                conteneur.type = '+'

            elif carac in balises_categories and carac_suivant == '#':
                """
                N#
                T#
                I#
                ...
                """
                conteneur.type = carac

            elif carac == '|' and carac_suivant == ';':
                conteneur.type = '|'

            elif carac not in [
                    '>', '}', ']', ')', # Balises fermante
                    '#', ' ', ':', ',', '|' # Séparations
                ]:
                conteneur.append(carac)
                conteneur.type = '##'

            else:
                is_continue = False

            if is_continue:
                continue


        ### Femeture

        # Commentaire
        if conteneur.type == '//':
            # On remplace le type commentaire indiquant qu'il vient d'être créé
            #  par le type indiquant qu'on est à l'intérieure d'un commentaire
            conteneur.type = '/'

        elif conteneur.type == '/':
            # On rentre forcément dans la condition si c'est un commentaire 
            #  car tout est ignoré dedans

            if '/' == carac == texte[place-1]:
                conteneur.type = ''

        # Conteneure
        elif (conteneur.type not in ['"', "'"]
            and carac in ['>', '}', ']', ')','#']):

            # Sert pour la syntaxe 1
            """
            |;#
            |;I#{
                "pomme" "poire"
                "pouf" "paf"
            }
            """
            #  dans le but que si le conteneur actuel est un dict
            #  vérifier si on est dans la catégorie I#
            key = ''
            if conteneur.ancien_conteneur:
                key = conteneur.ancien_conteneur.key


            if conteneur.texte:
                conteneur.end()
            
            elif conteneur.type in balises_categories:
                conteneur.end()
                continue
            
            elif conteneur.type == '|':
                conteneur = conteneur.config_clss(1)
                continue


            conteneur = conteneur.rem_profondeur()


            if (carac == '}' 
                and '__synt__' in dir(conteneur.value.__class__) 
                and conteneur.value.__class__.__synt__ == 1
                and key == 'I'):
                conteneur = conteneur.rem_profondeur()

        # Texte
        elif ((carac == conteneur.type and carac in ['"', "'"])
            and not echappement):
            conteneur.end()


        ### Echappement

        elif carac == '\\':
            if echappement:
                echappement = False
                conteneur.append('\\')
            else:
                echappement = True
            continue

        elif echappement:
            if carac == 'n':
                conteneur.append('\n')
            elif carac == 't':
                conteneur.append('\t')


        ### Ajout de caractére

        elif conteneur.type in ['"', "'"]:
            conteneur.append(carac)

        elif conteneur.type in ['+', '-']:
            if carac not in '0123456789.':
                conteneur.end()
            else:
                conteneur.append(carac)

        elif conteneur.type == '|':
            if carac in balises_categories:
                # |;N#
                # |;I#
                # ...
                conteneur.type = carac


        ### Fin texte sans balise ou ajout carac

        elif carac == ' ' or carac == ':' or carac == ',' or carac == '|':
            if conteneur.type == '##':
                conteneur.end()

        elif conteneur.type == '##':
            conteneur.append(carac)


        if echappement:
            echappement = False


    retour = conteneur.value

    if not retour and not ever_list:
        return None

    elif len(retour) == 1 and not ever_list:
        return retour[0]

    else:
        return retour