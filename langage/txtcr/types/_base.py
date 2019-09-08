import random

from .. import erreurs

from .._utile import *

from datetime import datetime

py_str = str
py_bytes = bytes

def make_id(ss):
    ss.__id__ = int(datetime.now().strftime("%Y%m%d%H%M%S%f")+str(random.randint(0, 1000)))

def is_id(obj1, obj2):
    if '__id__' in dir(obj1) and '__id__' in dir(obj2):
        return obj1.__id__ == obj2.__id__
    else:
        return obj1 is obj2

def get_vars(clss, params={}, var_objets=[]):
    if not clss:
        return []
    variables = clss.__class__.__vars__[:]
    var_objets = var_objets[:]
    var_objets.insert(0, params)
    variables[0] = var_objets
    return variables

def recup_redirection(redirection, *cle, silent=False, hashtag=True):

    rem_hastague = False

    if isinstance(redirection, str) and redirection and redirection[0] == redirection[-1] == '#':
        redirection = redirection[1:-1]
        rem_hastague = True

    if not cle:
        return redirection

    variables, defauts, decode = cle

    args = []
    kwargs = {}

    params = []

    call = False
    index = False

    #Call fonction ----------
    if (rem_hastague or not hashtag) and isinstance(redirection, str):
        if ('(' in redirection and ')' == redirection[-1]):

            call = True
            
            redirection, parametres = redirection[:-1].split('(', 1)
            parametres = [recup_redirection(param, variables, defauts, decode) for param in decode(parametres, ever_list=True)]

        elif '|' in redirection:

            index = True

            params = decode(redirection)

    elif 'rac_cond' in str(type(redirection)):

        call = True
        redirection, parametres = (redirection.nom_fonc, 
                                    [recup_redirection(param, variables, defauts, decode) for param in redirection.params])

    elif 'rac_redirection' in str(type(redirection)):

        index = True
        params = redirection.params

    if call:

        for params in parametres:
            if isinstance(params, tuple):
                for param in params:
                	value = recup_redirection(param, variables, defauts, decode)
                	args.append(value)

            elif isinstance(params, list):
                for variable in params:
                    kwargs[recup_redirection(variable)] = recup_redirection(variable, variables, defauts, decode)

            elif isinstance(params, dict):
                for key, value in params.items():
                    value = recup_redirection(value, variables, defauts, decode)
                    kwargs[recup_redirection(key)] = value

    elif index:

        if len(params) >=2:
            value = recup_redirection(params[0], variables, defauts, decode)

            for param in params[1:]:
                param = recup_redirection(param, variables, defauts, decode)
                value = value[param]

            return value
        else:
            redirection = recup_redirection(params[0], variables, defauts, decode)

    elif hashtag and not rem_hastague:
        return redirection

    #Get variable rediretion
    variable = '#'
    variables_defauts = variables[:]
    variables_defauts.append([defauts])
    #print('v', variables_defauts)
    for zone in variables_defauts:
        for vars_ in zone:
            if redirection in vars_:
                variable = vars_[redirection]

                if (callable(variable) 
                and (call or variable.callable_with_not_call)):

                    variable = variable(args, kwargs, variables[0])

                return variable

    #Léve une erreur ou retourne la redirection
    if not silent:
        raise Exception("La variable \"%s\" n'existe pas !"%redirection)
    return redirection

def recup_partie_parentese(texte, fonction=None):
    début = 0
    fin = 0
    parentese_ouverture_croiser = 0
    parentese_fermeture_croiser = 0
    fin_condition = -1

    for nbr, carac in enumerate(texte):
        if nbr <= fin_condition:
            continue

        if carac == '(':
            if nbr and texte[nbr-1] not in [' '] + symbs_calcul:
                _, fin_condition = recup_partie_parentese(texte[nbr:])
                fin_condition += nbr
            else:
                if not début: début = nbr
                if not parentese_fermeture_croiser: parentese_ouverture_croiser += 1
                else: parentese_fermeture_croiser -= 1
        elif carac == ')':
            parentese_fermeture_croiser += 1
            if parentese_ouverture_croiser == parentese_fermeture_croiser:
                fin = nbr
                break

    if not fonction: return début, fin

    resulta = fonction(texte[début+1:fin])
    text = list(texte)
    del text[début:fin+1]
    text.insert(début, resulta)

    return ''.join(text)