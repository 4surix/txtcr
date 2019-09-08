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
        if balise in ['1', '0', 'O', '|', "r"]:
            ss.sous_type = balise
            return
        ss.type = balise

    def config_clss(ss, synt, vars_local):

        _clss = new_clss(vars_local)
        _clss.__class__.__synt__ = synt
        _clss.__class__.__decode__ = partial(decode, clss_parent=_clss)

        conteneur = ss.add_profondeur(_clss)

        if conteneur.clss != None:
            value_vars = _clss.__class__.__vars__[2]
            clss_vars = conteneur.clss.__class__.__vars__[2]

            value_vars.append(conteneur.clss)
            clss_vars.append(_clss)

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
            value.clss = ss.clss

        elif ss.type == 'r"':
            value = str(texte)
            value.clss = ss.clss
            value.redirection = True
            value.callable_with_not_call = True
            
        elif ss.type in ['+', '-']:
            value = mk_nbr(ss.type+texte)

        elif ss.type == '1"':
            value = bool(True, texte)
            
        elif ss.type == '0"':
            value = bool(False, texte)
            
        elif ss.type == 'O"':
            value = none(texte)

        elif ss.type == '=':
            value = calc(texte)
            value.clss = ss.clss
            
        elif ss.type == ':':
            value = cond(texte, ss.key)
            value.clss = ss.clss

        elif ss.type == "'":
            value = bytes(texte.encode())
            value.clss = ss.clss

        elif ss.type in balises_categories:
            value = ss.type+'#'

        elif ss.type == '##':
            value = texte.strip()

        elif ss.type == '###':
            if texte[0] == texte[-1] == "#":
                value = texte.strip()
            else:
                value = '#%s#'%texte.strip()

        if save:
            ss.save(value)
        else:
            return value

    def save(ss, value):

        #Importation
        if isinstance(value, rac_clss):
            data = get_data_module(value.module)

            value = ss.clss.__class__.__decode__(data, with_hashtag=False)

            value_vars_global = value.__class__.__vars__[2]
            clss_vars_local = ss.clss.__class__.__vars__[1]
            clss_vars_global = ss.clss.__class__.__vars__[2]

            #Supprime clss en double et ajout des vars_global
            ajout_value_vars_global = value_vars_global[:]
            if ss.clss in ajout_value_vars_global:
                ajout_value_vars_global.remove(ss.clss)
            clss_vars_global.extend(ajout_value_vars_global)

            value_vars_global.extend(clss_vars_local)

        if is_class(ss.value) and '__vars__' in dir(ss.value):

            if ss.key:
                ss.value[ss.key] = value
                ss.key = ''
            else:
                ss.key = value

        elif isinstance(ss.value, dict):
            if ss.key:
                ss.value[ss.key] = value
                ss.key = ''
            else:
                ss.key = value

        elif isinstance(ss.value, (rac_cond, rac_redirection, rac_clss, list)):
            ss.value.append(value)

        elif isinstance(ss.value, tuple):
            ss.value += (value,)

        #Reset des conteneurs
        ss.type = ''
        ss.texte = []
        ss.sous_type = ''

def decode(texte, with_hashtag=True, *, exclues=[], ever_list=False, clss_parent=None):

    vars_local = []

    if clss_parent == None:
        class clss_base:
            def __iter__(ss):
                yield None
            def __repr__(ss):
                return '<:clss_base:>'
            def __ne__(ss, obj):
                return None != obj
        clss_base = clss_base()
        clss_base.__class__.__vars__ = [[], vars_local, []]
        clss_base.__class__.__decode__ = partial(decode, clss_parent=clss_base)
        clss_base.__class__.__defauts__ = {}
        clss_parent = clss_base

    echappement = False
    texte = texte.replace('\n', ' ').replace('\t', ' ').strip()
    conteneur = Conteneur(None, vars_local, _clss=clss_parent)

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
                        if texte[place+1] == '#':
                            conteneur = conteneur.add_profondeur(rac_clss(conteneur.clss))
                        else:
                            conteneur = conteneur.config_clss(0, vars_local)
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

        #Redirection:
        elif (not conteneur.type and carac == '#' 
            and (not isinstance(conteneur.value, rac_redirection) 
                or (not len(conteneur.value) or (not place or texte[place-1] == '|')))):
                    conteneur = conteneur.add_profondeur(rac_redirection(conteneur.clss))

        elif not conteneur.type and carac == 'r' and texte[place+1] in ['"']:
            conteneur.config_type('r')
            
        #Femeture ----------------------------
        #Conteneure
        elif (conteneur.type not in ['"', "'", ':', '=', '/']
            and carac in ['>', '}', ']', ')', '#']):

            key = ''
            if conteneur.ancien_conteneur:
                key = conteneur.ancien_conteneur.key[:]

            if conteneur.texte:
                conteneur.end()
            elif conteneur.type in balises_categories:
                conteneur.end()
                continue
            elif conteneur.type == '|':
                conteneur = conteneur.config_clss(1, vars_local)
                continue

            conteneur = conteneur.rem_profondeur()

            if ((carac == ')' and isinstance(conteneur.value, rac_cond))
                or (carac == '}' 
                    and '__synt__' in dir(conteneur.value.__class__) 
                    and conteneur.value.__class__.__synt__ == 1
                    and key == 'I')):
                conteneur = conteneur.rem_profondeur()

        #Texte, condition
        elif ((carac == conteneur.type and carac in ['"', "'", ":"])
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
                if conteneur.type == ':':
                    conteneur.append('\\')
                echappement = True
            continue

        elif echappement and carac in ['n', 't']:
            if carac == 'n':
                if conteneur.type == ':':
                   conteneur.append('\\n')
                else:     
                    conteneur.append('\n')
            elif carac == 't':
                if conteneur.type == ':':
                    conteneur.append('\\t')
                else:
                    conteneur.append('\t')

        #Ajout de caractére
        elif conteneur.type in ['"', "'", ':']:
            conteneur.append(carac)

        elif conteneur.type in ['+', '-']:
            if carac in '0123456789.':
                conteneur.append(carac)
                if place+1 < len(texte) and texte[place+1] == '(':
                    conteneur = conteneur.config_rac_cond()
            else:
                conteneur.end()

        elif conteneur.type == '=':
            if carac in '0123456789.' + '#+-*/%^V()':
                conteneur.append(carac)
            elif carac.lower() in 'abcdefghijklmnopqrstuvwxyz0123456789_éèçàù':
                conteneur.append(carac)
            else:
                conteneur.end()

        elif conteneur.type == '|':
            if carac in balises_categories:
                conteneur.config_type(carac)
                conteneur.sous_type = ''

        elif conteneur.type == '/':
            continue

        #Texte sans balise -> Str
        elif carac in [',', ' ', '|'] and conteneur.type in ['##', '###']:
            conteneur.end()
        elif carac.lower() in 'abcdefghijklmnopqrstuvwxyz0123456789_éèçàù':
            if not conteneur.type:
                conteneur.config_type('##'+['', '#'][with_hashtag or isinstance(conteneur.value, rac_redirection)])
            conteneur.append(carac)
            if place+1 < len(texte) and texte[place+1] == '(':
                conteneur = conteneur.config_rac_cond()
                
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