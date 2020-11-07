
from functools import partial


from txtcr.core.types import *
from txtcr.core.encode import encode


class Conteneur:

    def __init__(self, ancien_conteneur, value):
        self.ancien_conteneur = ancien_conteneur

        self.value = value

        # Les objets qui seront dans ce conteneur
        #  sont d'abors enregistrés en texte 
        #  puis transformés dans self.end()
        self.texte = ''

        self.type = ''

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

    def config_clss(self):
        return self.add_profondeur(new_clss(encode))

    def end(self):

        # Convertion texte en type Python

        texte = self.texte

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
        self.texte = ''
        self.type = ''


def decode(texte, *, exclues=[], ever_list=False):

    echappement = False
    conteneur = Conteneur(None, [])

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

                ["pomme"] == "il était une pomme  sur un arbre"

                """
                continue

            carac = ' '


        ### Ouverture
            
        if not conteneur.type:

            is_continue = True

            carac_suivant = texte[position + 1] if taille_texte != position + 1 else ''

            if carac == '/' and carac_suivant == '/':
                """ Commantaire

                {// Information //
                 ID 123456
                 // Autre //
                 langage "fr"
                 heure "UTC"
                }

                """
                conteneur.type = '//'

            elif carac == '<':
                # <I#{}>
                conteneur = conteneur.config_clss()

            elif carac == '{':
                # {"pouet" 123456}
                conteneur = conteneur.add_profondeur({})

            elif carac == '[':
                # ["pouf" "poire" 1234]
                conteneur = conteneur.add_profondeur([])

            elif carac == '(':
                # (34.6 "wouf" 'pouet')
                conteneur = conteneur.add_profondeur(())

            elif carac == '"':
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

            elif carac in balises_categories and carac_suivant == '#':
                """
                N#Pouet
                I#{}
                ...
                """
                conteneur.type = carac

            elif carac not in [
                    '>', '}', ']', ')', # Balises fermante
                    '#', ' ', ',', ':', '=' # Séparations
                ]:
                conteneur.type = '##'
                conteneur.texte += carac

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

            if '/' == carac == texte[position - 1]: # [...] blabla//
                conteneur.type = ''

        # Conteneure
        elif (conteneur.type not in ['"', "'"]
            and carac in ['>', '}', ']', ')', '#']):

            if conteneur.texte:
                # (pomme), [pomme], {name Pouf}
                conteneur.end()

            elif conteneur.type in balises_categories:
                # <I#{}>
                conteneur.end()
                continue

            conteneur = conteneur.rem_profondeur()

        # Texte
        elif (carac == conteneur.type 
              and carac in ['"', "'"]
              and not echappement
            ):
            conteneur.end()


        ### Echappement

        elif carac == '\\':

            if echappement:
                # "Pomme \\ poire"
                echappement = False
                conteneur.texte += '\\'

            else:
                # "Pomme \ poire"
                echappement = True

            continue

        elif echappement:

            if carac == 'n':
                # "Pomme \n poire"
                conteneur.texte += '\n'

            elif carac == 't':
                # "Pomme \t poire"
                conteneur.texte += '\t'


        ### Ajout de caractére

        elif conteneur.type in ['"', "'"]:
            # "Pomme"
            # 'Pomme'
            conteneur.texte += carac

        elif conteneur.type in ['+', '-']:
            # +123
            # -123
            if carac not in '0123456789.':
                conteneur.end()
            else:
                conteneur.texte += carac


        ### Fin texte sans balise ou ajout carac

        elif (carac == ' '    # pouet "pomme"
              or carac == ',' # pouet, "pomme"
              or carac == ':' # pouet: "pomme"
              or carac == '=' # pouet= "pomme"
            ):
            if conteneur.type == '##':
                conteneur.end()

        elif conteneur.type == '##':
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