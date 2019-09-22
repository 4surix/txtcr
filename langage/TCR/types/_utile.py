import os

import random

from datetime import datetime

py_str = str
py_bytes = bytes
py_bool = bool

balises  = [
    "<",
    "{",
    "[",
    "(",
    ":",
    '#',
    "=",
    'r',
    '"',
    "'",
    "+",
    "-",
    "1",
    "0",
    "O"
]

balises_categories = [
    'N',
    'D',
    'B',
    'M',
    'I'
]

alphabets = 'abcdefghijklmnopqrstuvwxyz' + 'éèàù'

lettres = list(alphabets) + list(alphabets.upper())

chiffres = list('0123456789')

operations = ['+','-','*','/','%','V','^']

comparaisons = ['&', '|', '<', '=', '>', '!']

def make_id(ss):
    ss.__id__ = int(datetime.now().strftime("%Y%m%d%H%M%S%f")+str(random.randint(0, 1000)))

def is_id(obj1, obj2):
    if '__id__' in dir(obj1) and '__id__' in dir(obj2):
        return obj1.__id__ == obj2.__id__
    else:
        return obj1 is obj2
        
def verif_callable(obj, params, kwargs, vars_objets):
    if callable(obj):
        obj = obj(params, kwargs, vars_objets)
    return obj

def get_vars(ss, obj_params, params, obj_kwargs, kwargs, vars_objets):

    bloc = ss.bloc

    if bloc is None:
        return []

    variables = bloc.__vars__[:]

    kwargs = dict(zip(list(obj_kwargs.keys()) + list(kwargs.keys()), list(obj_kwargs.values()) + list(kwargs.values())))

    vars_objets = vars_objets[:]
    vars_objets.insert(0, kwargs)
    variables[0] = vars_objets

    if len(obj_params) == len(params):
        if obj_params:
            vars_objet = variables[0][0]
            for variable, value in zip(obj_params, params):
                vars_objet[variable] = value

    elif len(obj_params) > len(params):
        args = obj_params[len(params):]
        raise TypeError("%s() manque %s arguments: %s"%(ss.nom, len(args), ", ".join(map(repr, args))))

    else:
        raise TypeError("%s() à %s arguments, mais %s sont donnés: %s"%(ss.nom, len(obj_params), len(params), ", ".join(map(repr, params))))

    return variables

def get_var(variable, variables):

    for zone in variables:
        for vars_ in zone:
            if variable in vars_ and not isinstance(vars_, str):
                return vars_[variable]

    raise Exception("La variable \"%s\" n'existe pas !"%variable)

def get_variable_value(params):
    if (len(params) % 2) != 0:
        raise ValueError("Les éléments de params n'est pas pair")

    for nbr in range(0, len(params), 2):
        yield params[nbr:nbr+2]

def get_args_kwargs(parametres, variables):

    args = []
    kwargs = {}

    type_param = 'args'

    for params in parametres:

        if params == '~':
            type_param = 'clones'
            continue

        if params == '~~':
            type_param = 'kwargs'
            continue

        if type_param == 'args':
            args.append(verif_callable(params, (), {}, variables[0]))

        elif type_param == 'clones':
            for param in params:
                kwargs[param] = get_var(param)

        elif type_param == 'kwargs':
            for key, value in params.items():
                kwargs[key] = verif_callable(value, (), {}, variables[0])

    return args, kwargs

def main(obj, *, accept_not_callable=True):

    if callable(obj):
        return obj([], {}, [{}])
    elif accept_not_callable:
        return obj

def run(obj, *, accept_not_callable=True):

    if not isinstance(obj, list):
        obj = [obj] 

    resultats = []
    for tcr in obj:
        resultat = main(tcr, accept_not_callable=accept_not_callable)
        if resultat is not None:
            resultats.append(resultat)

    return resultats

#Modules -------------------------------------------
chemin_modules = "C:/Users/%s/AppData/Roaming/TCR/modules"%os.environ['USERNAME']
#Création du dossier "modules" si n'existe pas
os.makedirs(chemin_modules, exist_ok=True)

def get_modules():
    return [m.split('.')[0] for m in os.listdir(chemin_modules)]

def get_data_module(module, chemin=None):
    if chemin:
        fichier = '%s/%s.tcr'%(chemin, module)
        if not os.path.exists(fichier):
            fichier = '%s/%s.tcr'%(chemin_modules,module)
    else:
        fichier = '%s/%s.tcr'%(chemin_modules,module)

    try:
        with open(fichier, encoding='utf-8') as m:
            data = m.read()
        return data
    except FileNotFoundError:
        raise FileNotFoundError("Le modules \"%s\" n'existe pas !"%module)