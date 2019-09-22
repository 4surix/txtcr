from .types import *

from functools import partial

class Conteneur:

    def __init__(ss, last_conteneur, value, bloc, in_=''):
        ss.texte = []
        ss.value = value

        ss.key = ''
        
        ss.type = ''
        ss.sous_type = ''

        ss.bloc = bloc

        ss.in_ = in_

        ss.last_conteneur = last_conteneur

    def __iadd__(ss, carac):
        """
        """
        ss.texte.append(carac)
        return ss

    def config_type(ss, balise, bloc_base):

        if balise in balises[:7] + ['<#']:
            return ss.add_profondeur(balise, bloc_base)
        else:
            if balise in ["r", "1", "0", "O"]:
                ss.sous_type = balise
            else:
                ss.type = balise
            return ss

    def config_call(ss):

        value = ss.end(return_value=True)
        conteneur = Conteneur(ss, call(value, ss.bloc), ss.bloc, ss.in_)
        return conteneur

    def del_profondeur(ss):
        """
        """
        conteneur = ss.last_conteneur
        conteneur.save(ss.value)
        return conteneur

    def add_profondeur(ss, balise, bloc_base):
        """
        """
        in_ = ss.in_

        if balise == '<':
            value = bloc(bloc_base)
            value.__decode__ = ss.bloc.__decode__
            value.__chemin__ = ss.bloc.__chemin__
            ss.bloc = value
        elif balise == '{':
            value = {}
        elif balise == '[':
            value = []
        elif balise == '(':
            value = ()
        elif balise == ':':
            value = cond(ss.bloc, (ss.key if ss.key != '' else ss.value[-1] if isinstance(ss.value, (tuple, list)) and ss.value else ''))
            in_ = 'cond'
        elif balise == '=':
            value = calc(ss.bloc)
            in_ = 'calc'
        elif balise == '#':
            value = redirection(ss.bloc)
        elif balise == '<#':
            value = importation()

        conteneur = Conteneur(ss, value, ss.bloc, in_)
        return conteneur
    
    def end(ss, return_value=False):
        """
        """
        type_ = ss.sous_type + ss.type
        texte = ''.join(ss.texte)
        
        if type_ == '"':
            value = str(texte)
        elif type_ == 'r"':
            value = rstr(texte, ss.bloc)
        elif type_ == "'":
            value = bytes(texte.encode())
        elif type_ == '+':
            value = pos(texte)
        elif type_ == '-':
            value = neg(texte)
        elif type_ == 'n+-':
            value = nbr(texte)
        elif type_ == '1"':
            value = bool(True)
        elif type_ == '0"':
            value = bool(False)
        elif type_ == 'O"':
            value = none(texte)
        elif type_ == '##':
            value = rac(texte)
            value.bloc = ss.bloc
        else:
            value = texte

        if return_value:
            return value
        else:
            ss.save(value)

    def save(ss, obj):
        """
        """

        #Importation
        if isinstance(obj, importation):
            module = obj.module()
            data = get_data_module(module, ss.bloc.__chemin__)

            obj = ss.bloc.__decode__(data)

            value_vars_local = obj.__vars__[1]
            value_vars_global = obj.__vars__[2]

            bloc_vars_local = ss.bloc.__vars__[1]
            bloc_vars_global = ss.bloc.__vars__[2]

            bloc_vars_global.extend(value_vars_local + value_vars_global)

            value_vars_global.extend(bloc_vars_local)

        if isinstance(ss.value, bloc):
            if ss.key != '':
                ss.value[ss.key] = obj
                ss.key = ''
            else:
                ss.key = obj
                
        elif isinstance(ss.value, dict):
            if ss.key != '':
                ss.value[ss.key] = obj
                ss.key = ''
            else:
                ss.key = obj

        elif isinstance(ss.value, (list, cond, calc, call, importation, redirection, Bloc_base)):
            ss.value.append(obj)
            
        elif isinstance(ss.value, tuple):
            ss.value = ss.value + (obj,)
        
        ss.texte = []

        ss.type = ''
        ss.sous_type = ''

def decode(data, chemin=None, *, bloc_vars=None):

    data = ' '+data.strip().replace('\n', ' ').replace('\t', ' ')+' '

    echappement = False
    in_commentaire = False
    debut_commentaire = False
    sortie_de_cond_red = False

    bloc_base = Bloc_base()

    if not bloc_vars:
        bloc_vars = bloc_base

    bloc_base.__decode__ = partial(decode, bloc_vars=bloc_vars)
    bloc_base.__chemin__ = chemin

    conteneur = Conteneur(None, bloc_base, bloc_vars)
    
    for place, carac in enumerate(data):

        #Print pour débuger
        #print(place, carac, conteneur.type, conteneur.texte, conteneur, conteneur.value, conteneur.key)

        if in_commentaire:
            if carac == '/' and data[place-1] == '/' and not debut_commentaire:
                in_commentaire = False
            if debut_commentaire:
                debut_commentaire = False
            continue

        elif (not conteneur.type and carac in balises
              #Pour les bool/none et les chiffres/variable commançant par 1, 0 ou O
              and (carac not in ["r", "1", "0", "O"] or data[place+1] == '"')
              #Pour les calculs et les comparaisons = == === =>, et les fermeture
              and (carac != '=' or data[place+1] not in ['=', " ", '>'])
              #Pour fermeture de condition et redirection
              and (carac not in [':', '#'] 
                        or data[place+1] not in ['|'] 
                            and data[place-1] not in balises_categories)
              #Pour la comparaison < <=
              and (carac not in ['<'] or data[place+1] not in ['=', " "])
              #Pour les calcul, -1 + 1
              and (carac not in ['+', '-'] 
                or (conteneur.in_ != 'calc' 
                    or (not conteneur.value[:]
                        or str(conteneur.value[-1])[-1] in operations)))):

            #Si il reste du texte
            if conteneur.texte:
                conteneur.end()

            #Pour les importations <#math#>
            if carac == '<' and data[place+1] == '#':
                carac = '<#'
                
            conteneur = conteneur.config_type(carac, bloc_base)

        elif (not conteneur.type and carac in balises_categories and data[place+1] == '#'):
            conteneur.save(carac+'#')

        elif ((carac in ["}", "]", ")", ";"] 
            or (carac in [':', '#'] and data[place+1] == '|') 
                or (carac in ['>'] and isinstance(conteneur.value, (bloc, importation))))
                    and conteneur.type not in ['"', "'"]):

            if conteneur.texte:
                conteneur.end()

            conteneur = conteneur.del_profondeur()

            #Dans la cas d'une fermeture d'un call, pouet() "pomme"()
            if carac == ')' and isinstance(conteneur.value, call):
                conteneur = conteneur.del_profondeur()
            elif carac in [':', '#']:
                sortie_de_cond_red = True
                continue

        elif((carac == conteneur.type
              and carac in ['"', "'"])
            and not echappement):
            #Dans le cas d'un call "pomme"()
            if data[place+1] == '(':
                conteneur = conteneur.config_call()
            else:
                conteneur.end()

        elif conteneur.type in ['+', '-', 'n+-']:
            conteneur += carac
            
            if data[place+1] not in chiffres + ['.']:
                conteneur.end()

        elif carac == '\\':
            if echappement:
                echappement = False
                conteneur += '\\'
            else:
                echappement = True
                continue

        elif echappement:
            if carac == 'n':
                conteneur += '\n'
            elif carac == 't':
                conteneur += '\t'

        elif conteneur.type in ['"', "'"]:
            conteneur += carac

        elif carac == '/' and data[place+1] == '/':
            in_commentaire = True
            debut_commentaire = True
            
        elif carac in operations and conteneur.in_ == 'calc':
            if conteneur.texte:
                conteneur.end()

            conteneur.save(carac)

        elif (carac in comparaisons 
                and conteneur.in_ == 'cond' 
                    #and conteneur.value.type in ['up','cond']
                        and not sortie_de_cond_red):
            if conteneur.texte and not all([symb in comparaisons for symb in conteneur.texte]):
                conteneur.end()

            conteneur += carac
            
        elif carac in lettres + chiffres + ['~', '_']:

            if not conteneur.type:
                if conteneur.texte:
                    conteneur.end()

                if carac in chiffres:
                    conteneur = conteneur.config_type('n+-', bloc_base)
                else:
                    conteneur = conteneur.config_type('##', bloc_base)

            conteneur += carac

            if conteneur.type == 'n+-' and data[place+1] not in chiffres + ['.']:
                conteneur.end()

            #Dans le cas d'un call, pouet()
            if data[place+1] == '(':
                conteneur = conteneur.config_call()
            
        elif conteneur.type in ['##']:
            conteneur.end()

        echappement = False
        sortie_de_cond_red = False
        
    return conteneur.value