from .types import *

from .encode import encode
from functools import partial


class Conteneur:

    def __init__(self, ancien_conteneur, value, _clss=None):
        self.ancien_conteneur = ancien_conteneur
        self.clss = _clss
        self.value = value

        self.sous_type = ''
        self.texte = []
        self.type = ''
        self.key = ''
        
    def add_profondeur(self, value):
        return Conteneur(self, value, self.clss)

    def rem_profondeur(self):
        conteneur = self.ancien_conteneur
        conteneur.save(self.value)
        return conteneur

    def config_type(self, balise):
        if balise in ['1', '0', 'O', '|']:
            self.sous_type = balise
            return
        self.type = balise

    def config_clss(self, synt):

        _clss = new_clss(encode)
        _clss.__class__.__synt__ = synt
        _clss.__class__.__decode__ = partial(decode, clss_parent=_clss)

        conteneur = self.add_profondeur(_clss)

        if conteneur.clss != None:
            conteneur.ancien_clss = conteneur.clss

        conteneur.clss = _clss

        return conteneur
        
    def append(self, value):
        self.texte.append(value)

    def end(self, save=True):

        #Convertion texte en son type

        self.type = self.sous_type + self.type

        texte = ''.join(self.texte)
            
        if self.type == '"':
            value = str(texte)
            
        elif self.type in ['+', '-']:
            value = mk_nbr(self.type+texte)

        elif self.type == '1"':
            value = bool(True, texte)
            
        elif self.type == '0"':
            value = bool(False, texte)
            
        elif self.type == 'O"':
            value = none(texte)

        elif self.type == "'":
            value = texte.encode()

        elif self.type in balises_categories:
            value = self.type+'#'

        elif self.type == '##':
            value = str(texte.strip())

        if save:
            self.save(value)
        else:
            return value

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

        #Reset des conteneurs
        self.type = ''
        self.texte = []
        self.sous_type = ''


def decode(texte, *, exclues=[], ever_list=False):

    echappement = False
    texte = ' ' + texte.replace('\n', ' ').replace('\t', ' ').strip() + ' '
    conteneur = Conteneur(None, [])

    for place, carac in enumerate(texte):

        # Ouverture -------------------------
        if (not conteneur.type 
        and (  (carac in ['<', '{', '[', '(', '"', "'"])
            or (carac in ['O', '0', '1']
                and texte[place+1] == '"')
            or (carac in ['+', '-']
                and texte[place+1] in list('0123456789'))
            or (carac in balises_categories 
                and texte[place+1] == '#')
            or (carac == '|'
                and texte[place+1] == ';'))):
            
            # Texte, nombre, bool, calcul, cond
            if (carac not in exclues
                and carac in balises_types[4:]):
                    conteneur.config_type(carac)

            # Conteneurs
            elif (carac not in exclues
                and carac in balises_types[:4]):
                    if carac == '<':
                        conteneur = conteneur.config_clss(0)
                    elif carac == '{':
                        conteneur = conteneur.add_profondeur({})
                    elif carac == '[':
                        conteneur = conteneur.add_profondeur([])
                    elif carac == '(':
                        conteneur = conteneur.add_profondeur(())

            # Catégories
            elif carac in balises_categories and texte[place+1] == '#':
                conteneur.config_type(carac)

            #
            elif carac == '|' and texte[place+1] == ';':
                conteneur.type = '|'
            
        # Femeture ----------------------------
        
        # Conteneure
        elif (conteneur.type not in ['"', "'", '/']
            and carac in ['>', '}', ']', ')','#']):

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

        # Commentaire
        elif conteneur.type == carac == '/':
            conteneur.type = ''

        # Echappement
        elif carac == '\\':
            if echappement:
                echappement = False
                conteneur.append('\\')
            else:
                echappement = True
            continue

        elif echappement and carac in ['n', 't']:
            if carac == 'n':
                conteneur.append('\n')
            elif carac == 't':
                conteneur.append('\t')

        # Ajout de caractére
        elif conteneur.type in ['"', "'"]:
            conteneur.append(carac)

        elif conteneur.type in ['+', '-']:
            if carac not in '0123456789.':
                conteneur.end()
            else:
                conteneur.append(carac)

        elif conteneur.type == '|':
            if carac in balises_categories:
                conteneur.config_type(carac)
                conteneur.sous_type = ''

        elif conteneur.type == '/':
            continue

        # Texte sans balise -> Str or Int/Float
        elif carac in [':', ',', ' ', '|'] and conteneur.type == '##':
            conteneur.end()

        elif carac != ' ':
            if not conteneur.type:
                if carac in chiffres:
                    conteneur.config_type('+')
                else:
                    conteneur.config_type('##')

            conteneur.append(carac)
                
        if echappement:
            echappement = False

    #Si il reste du texte non enregistré
    if conteneur.texte:
        conteneur.end()

    retour = conteneur.value

    if not retour and not ever_list:
        return None

    elif len(retour) == 1 and not ever_list:
        return retour[0]

    else:
        return retour