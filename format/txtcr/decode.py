from .types import *

from functools import partial

class Conteneur:

    def __init__(ss, ancien_conteneur, value, _clss=None):
        ss.ancien_conteneur = ancien_conteneur
        ss.clss = _clss
        ss.value = value

        ss.sous_type = ''
        ss.texte = []
        ss.type = ''
        ss.key = ''
        
    def add_profondeur(ss, value):
        #print('>>>', value)
        return Conteneur(ss, value, ss.clss)

    def rem_profondeur(ss):
        #print('<<<', ss.value)
        conteneur = ss.ancien_conteneur
        conteneur.save(ss.value)
        return conteneur

    def config_type(ss, balise):
        if balise in ['1', '0', 'O', '|']:
            ss.sous_type = balise
            return
        ss.type = balise

    def config_clss(ss, synt):

        _clss = new_clss()
        _clss.__class__.__synt__ = synt
        _clss.__class__.__decode__ = partial(decode, clss_parent=_clss)

        conteneur = ss.add_profondeur(_clss)

        if conteneur.clss != None:
            conteneur.ancien_clss = conteneur.clss

        conteneur.clss = _clss

        return conteneur

    def config_rac_cond(ss):
        conteneur = ss.add_profondeur(rac_cond(ss.end(save=False), ss.clss))
        ss.texte = []
        ss.type = ''
        return conteneur
        
    def append(ss, value):
        ss.texte.append(value)

    def end(ss, save=True):

        #Convertion texte en son type

        ss.type = ss.sous_type + ss.type

        texte = ''.join(ss.texte)
            
        if ss.type == '"':
            value = str(texte)
            
        elif ss.type in ['+', '-']:
            value = mk_nbr(ss.type+texte)

        elif ss.type == '1"':
            value = bool(True, texte)
            
        elif ss.type == '0"':
            value = bool(False, texte)
            
        elif ss.type == 'O"':
            value = none(texte)

        elif ss.type == "'":
            value = texte.encode()

        elif ss.type in balises_categories:
            value = ss.type+'#'

        elif ss.type == '##':
            value = texte.strip()

        if save:
            ss.save(value)
        else:
            return value

    def save(ss, value):

        if is_class(ss.value) and '__irepr__' in dir(ss.value):

            if ss.key != '':
                ss.value[ss.key] = value
                ss.key = ''
            else:
                ss.key = value

        elif isinstance(ss.value, dict):
            if ss.key != '':
                ss.value[ss.key] = value
                ss.key = ''
            else:
                ss.key = value

        elif isinstance(ss.value, list):
            ss.value.append(value)

        elif isinstance(ss.value, tuple):
            ss.value += (value,)

        #Reset des conteneurs
        ss.type = ''
        ss.texte = []
        ss.sous_type = ''

def decode(texte, *, exclues=[], ever_list=False):

    vars_local = []

    echappement = False
    texte = texte.replace('\n', ' ').replace('\t', ' ').strip()
    conteneur = Conteneur(None, vars_local)

    for place, carac in enumerate(texte):

        #print(place, carac, conteneur.type, conteneur.value)

        #Ouverture -------------------------
        if not conteneur.type and carac in balises_types + balises_categories + ['|']:

            #Texte, nombre, bool, calcul, cond
            if (carac not in exclues
                and carac in balises_types[4:]):
                    conteneur.config_type(carac)

            #Conteneurs
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

            #Catégories
            elif carac in balises_categories :
                conteneur.config_type(carac)

            elif carac == '|' and texte[place+1] == ';':
                conteneur.type = '|'
            
        #Femeture ----------------------------
        #Conteneure
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

            if ((carac == ')' and isinstance(conteneur.value, rac_cond))
                or (carac == '}' 
                    and '__synt__' in dir(conteneur.value.__class__) 
                    and conteneur.value.__class__.__synt__ == 1
                    and key == 'I')):
                conteneur = conteneur.rem_profondeur()

        #Texte, condition
        elif ((carac == conteneur.type and carac in ['"', "'"])
            and not echappement):
            if place+1 < len(texte) and texte[place+1] == '(':
                conteneur = conteneur.config_rac_cond()
            else:
                conteneur.end()

        #Commentaire
        elif conteneur.type == carac == '/':
            conteneur.type = ''

        #Echappement
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

        #Ajout de caractére
        elif conteneur.type in ['"', "'"]:
            conteneur.append(carac)

        elif conteneur.type in ['+', '-']:
            if carac in '0123456789.':
                conteneur.append(carac)
                if place+1 < len(texte) and texte[place+1] == '(':
                    conteneur = conteneur.config_rac_cond()
            else:
                conteneur.end()

        elif conteneur.type == '|':
            if carac in balises_categories:
                conteneur.config_type(carac)
                conteneur.sous_type = ''

        elif conteneur.type == '/':
            continue

        #Texte sans balise -> Str
        elif carac in [',', ' ', '|'] and conteneur.type == '##':
            conteneur.end()
        elif carac.lower() in 'abcdefghijklmnopqrstuvwxyz0123456789_éèçàù':
            if not conteneur.type:
                conteneur.config_type('##')
            conteneur.append(carac)
                
        if echappement:
            echappement = False

    #Si il reste du texte non enregistré
    if conteneur.texte:
        conteneur.end()

    retour = conteneur.value

    if not retour:
        return None
    elif len(retour) == 1 and not ever_list:
        return retour[0]
    else:
        return retour