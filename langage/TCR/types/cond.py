import pytz

from .calc import *

noms_actions = [
    'aff',
    'ped',
    'get',
    'set',
    'typ',
    'cvt',
    'len',
    'ale',
    'now',
    'try',
    'err',
    'add',
    'eli',
    'del'
]

class result:

    def __init__(ss):

        ss.actions = {}
        ss.retours = []

    def __getitem__(ss, item):

        if isinstance(item, (int, pos, neg)):
            return ss.retours[item]
        elif isinstance(item, (str, bytes)):
            retour_act = ss.actions[item]
            if len(retour_act) == 1:
                return retour_act[0]
            else:
                return tuple(retour_act)

    def __setitem__(ss, action, retour):

        if action not in ss.actions:
            ss.actions[action] = []
        ss.actions[action].append(retour)
        ss.retours.append(retour)

    def __len__(ss):
        return len(ss.retours)

    def __repr__(ss):
        return '%s'%ss.retours

    def __str__(ss):
        return '%s'%ss.retours

# Comparaisons ----------------------------------

def _type_in(var1, var2):
    variable = var1
    conteneur = var2
    nom_type = type(variable).__name__
    for partie in conteneur:
        type_partie = type(partie).__name__
        if nom_type == type_partie:
            return True
    return False

def _objet_in(var1, var2):
    variable = var1
    conteneur = var2
    for partie in conteneur:
        if is_id(variable, partie):
            return True
    return False

def _meme_type(var1, var2):
    Ttype = type(var1).__name__
    for element in var2:
        if type(element).__name__ != Ttype:
            return False
    return True

func_comparaisons = {
    '>': lambda var1, var2: var1 > var2,
    '=>': lambda var1, var2: var1 >= var2,
    '<': lambda var1, var2: var1 < var2,
    '<=': lambda var1, var2: var1 <= var2,
    '=': lambda var1, var2: type(var1) == type(var2),
    '==': lambda var1, var2:  var1 == var2,
    '===': lambda var1, var2: is_id(var1, var2),
    'in': lambda var1, var2: _type_in(var1, var2),
    'inn': lambda var1, var2: var1 in var2,
    'innn': lambda var1, var2: _objet_in(var1, var2),
    'innnn': lambda var1, var2: _meme_type(var1, var2),
    '&': lambda var1, var2: var1 and var2,
    '&&': lambda var1, var2: bool(var1) == bool(var2),
    '|': lambda var1, var2: var1 or var2,
    '||': lambda var1, var2: (var1 or var2) != (var1 and var2)
}

# Analise des comparaison, return 1 ou 0 ------------------------------

def _analyse_comparaison(comparaison, variables, defauts, decode):

    def copie(liste):
        return [copie(element)  if isinstance(element, (list, tuple)) 
                                    and len(element) >= 3 
                                        and isinstance(element[1], py_str) 
                                            and element[1].replace('!', '') in func_comparaisons
                                else element for element in liste]

    def verif_type(value):

        if (isinstance(value, list)
            and len(value) >= 3 
            and isinstance(value[1], py_str) 
            and value[1].replace('!', '') in func_comparaisons):
                value = verif_comparaison(value)

        elif callable(value):
            value = value([], {}, variables[0])

        return value

    def get_values_and_symb(liste):
        for nbr in range(0, len(liste)-1, 2):
            yield [nbr+2] + liste[nbr:nbr+3]

    def verif_comparaison(comparaison):

        if len(comparaison) < 3:
            raise Exception('Comparaisons erreur.')

        for place, value_1, symb_comparaison, value_2 in get_values_and_symb(comparaison):

            value_1 = verif_type(value_1)
            value_2 = verif_type(value_2)

            not_inversement = True
            if symb_comparaison[0] == '!':
                not_inversement = False
                symb_comparaison = symb_comparaison[1:]

            func = func_comparaisons.get(symb_comparaison)
            if not func:
                raise Exception("La comparaison \"%s\" n'existe pas !"%symb_comparaison)

            comparaison[place] = func(value_1, value_2) == not_inversement

            #print(value_1, symb_comparaison, value_2, comparaison[place])

        return comparaison[-1]

    return verif_comparaison(copie(comparaison)) #Copie de la liste pour éviter les modifs

# Cond -------------------------------------------

class cond:
    def __init__(ss, bloc, nom=''):
        ss.nom = nom

        ss.if_ = False
        ss.type = 'cond'
        
        ss.params = []
        ss.clones = []
        ss.kwargs = {}

        ss.bloc = bloc

        ss.remonter = []
        ss.comparaison = []
        ss.actions = [[], []]

    def append(ss, obj):
        
        if not ss.if_ and not any([ss.params, ss.clones, ss.kwargs, ss.comparaison, ss.actions[True], ss.actions[False]]) and isinstance(obj, tuple):
            
            type_param = 'params'

            for param in obj:

                if param == '~':
                    type_param = 'kwargs'
                    continue

                if type_param == 'params':
                    ss.params.append(param)

                elif type_param == 'kwargs':
                    for k, v in param.items():
                        ss.kwargs[k] = v

        else:
            if obj == 'if':
                ss.if_ = True
            elif obj == 'acts':
                ss.type = 'acts'
            elif obj == 'then':
                ss.type = 'then'
            elif obj == 'else':
                ss.type = 'else'
            elif obj == 'up':
                ss.type = 'up'
            else:
                if ss.type == 'cond':
                    ss.comparaison.append(obj)

                elif ss.type == 'up':
                    ss.remonter.append(obj)

                elif ss.type == 'acts':
                    if isinstance(obj, py_str) and obj.replace('~', '') in noms_actions:
                        ss.actions[True].append([obj, []])
                    else:
                        ss.actions[True][-1][-1].append(obj)

                elif ss.type == 'then':
                    if isinstance(obj, py_str) and obj.replace('~', '') in noms_actions:
                        ss.actions[True].append([obj, []])
                    else:
                        ss.actions[True][-1][-1].append(obj)

                elif ss.type == 'else':
                    if isinstance(obj, py_str) and obj.replace('~', '') in noms_actions:
                        ss.actions[False].append([obj, []])
                    else:
                        ss.actions[False][-1][-1].append(obj)


    def __str__(ss):
        return ':%s:'%ss.comparaison
    def __repr__(ss):
        return ':%s:'%ss.comparaison

    def __iter__(ss):
        yield None

    def __bool__(ss):
        return True

    def __call__(ss, params, kwargs, vars_objets):
        variables = get_vars(ss, ss.params, params, ss.kwargs, kwargs, vars_objets)

        act_variables = variables
        act_defauts = ss.bloc.__defauts__
        act_decode = ss.bloc.__decode__

        act_utile =(act_variables,
                    act_defauts,
                    act_decode)

        #Pour changer/créer la value d'une variable -----------------
        def set_var(var, value, nouv_var=None, *, fonction=None, existe=False, nouv=False):

            #Def variables (str, pos, neg, tuple) et params (si redirection)
            params = []
            if isinstance(var, redirection):
                params = [verif_callable(param, (), {}, variables[0]) for param in var.params[1:]]
                var = var.params[0]
            
            if isinstance(var, rac):
                var = var.value

            if callable(var):
                var = var((), {}, variables[0])

            variable = var

            #Set value en fonction des params
            def _set_params(variables, variable, value):

                if params:
                    variable = variables[variable]
                    for param in params[:-1]:
                        variable = variable[param]

                    if fonction:
                        return fonction(variable, params[-1], value)
                    else:
                        variable[params[-1]] = value
                else:
                    if fonction:
                        return fonction(variables, variable, value)
                    else:
                        variables[variable] = value

            #Recherche de la variable si existe déjà ou non
            if not nouv: #Pour les cas où il faut obligatoirement créer une nouv var
                for zone in act_variables:
                    for variables in zone:
                        if variable in variables:
                            return _set_params(variables, variable, value)

            if not existe: #Pour les cas où il faut obligatoirement que la var existe déjà
                return _set_params(act_variables[0][0], variable, value)
            else:
                raise erreurs.VariableError(variable)
        #--------------------------------------------------------------

        nbr_boucle = 0

        while True:

            nbr_boucle += 1

            if nbr_boucle > 1000:
                raise Exception('Module : %s, Cond : %s, Text : Le nombre de remontée à atteint le max (1000)'%(ss.bloc.__name__, ss.nom))

            if ss.comparaison:
                status = _analyse_comparaison(ss.comparaison, *act_utile)
            else:
                status = True

            # --------------------------------------------------
            #                     ACTIONS
            # --------------------------------------------------

            actions = ss.actions[status]

            if actions:

                resultats = result()

                resultat = None

                for action, values in actions:

                    retour = False
                    if action[0] == '~':
                        action = action[1:]
                        retour = True

                    if action == 'aff':

                        for value in values:
                            value = verif_callable(value, (), {}, variables[0])
                            print(value)

                        if retour:
                            resultat = none()

                    elif action == 'ped':

                        def demander(value):
                            texte_a_afficher = verif_callable(value, (), {}, variables[0])
                            resultat = input(texte_a_afficher).strip()
                            if resultat:
                                return str(resultat)

                        if retour:

                            resultat = []
                            for value in values:
                                resultat.append(demander(value))

                            if len(resultat) == 1:
                                resultat = resultat[0]

                        else:
                            for variable, value in get_variable_value(values):
                                set_var(variable, demander(value))

                    elif action == 'set':

                        for variable, value in get_variable_value(values):
                            set_var(variable, verif_callable(value, (), {}, variables[0]))

                        if retour:
                            resultat = none()

                    elif action == 'get':

                        resultat = []

                        for value in values:
                            value = verif_callable(value, (), {}, variables[0])
                            if value is not None:
                                resultat.append(value)

                        if not resultat:
                            resultat = None
                        elif len(resultat) == 1:
                            resultat = resultat[0]

                    elif action == 'len':
                        """
                        >len> nouv_var variable
                        Récupére le nombre d'élement 
                        """

                        def nombre_element(value):
                            return mk_nbr(len(verif_callable(value, (), {}, variables[0])))

                        if retour:

                            resultat = []
                            for value in values:
                                resultat.append(nombre_element(value))

                            if len(resultat) == 1:
                                resultat = resultat[0]
                                
                        else:

                            for variable, value in get_variable_value(values):
                                set_var(variable, nombre_element(value))

                    elif action == 'ale':
                        """
                        >ale> nouv_var (min, max, decimal)
                        Génére un nombre aléatoire entre min et max inclue, 
                        si décimal est indiqué renvoie un nombre à virgule avec le nombre de chiffre après la virgule
                        """

                        def creer_nbr_alea(nbrs):

                            if len(nbrs) == 2:
                                return mk_nbr(random.randint(nbrs[0].value, nbrs[1].value))
                            elif len(nbrs) == 3:
                                return mk_nbr(float(str(random.uniform(nbrs[0].value, nbrs[1].value))[:nbrs[2]+pos(2)]))
                            else:
                                raise erreurs.ParamError('>ale>')

                        if retour:

                            resultat = []
                            for value in values:
                                resultat.append(creer_nbr_alea(verif_callable(value, (), {}, variables[0])))

                            if len(resultat) == 1:
                                resultat = resultat[0]
                                
                        else:

                            for variable, value in get_variable_value(values):
                                set_var(variable, creer_nbr_alea(verif_callable(value, (), {}, variables[0])))

                    elif action == 'now':
                        """
                        >now> nouv_var (début, fin, TZ)
                        Renvoie une liste de la date actuel de TZ (Par défaut UTC)
                        """

                        ops = {
                            "A": 0,
                            "Y": 0,
                            "M": 1,
                            "J": 2,
                            "D": 2,
                            "h": 3,
                            "m": 4,
                            "s": 5,
                            "ms": 6
                        }

                        def get_debut_fin(d, f):
                            return ops.get(d, d), ops.get(f, f)

                        def get_time_now(params=[]):
                            début = 0
                            limite = 6
                            tz = pytz.utc

                            if not params:
                                pass

                            elif len(params) == 2:
                                début, limite = get_debut_fin(*params)

                            elif len(params) == 3:
                                début, limite = get_debut_fin(*params[0:2])
                                try: tz = pytz.timezone(params[2])
                                except pytz.exceptions.UnknownTimeZoneError:
                                    raise Exception("Le time zone \"%s\" n'existe pas ! (https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)"%params[2])

                            return tuple([nbr(int(nbr_)) for nbr_ in datetime.now(tz=tz).strftime("%Y/%m/%d/%H/%M/%S/%f").split('/')][début:limite+1])

                        if retour:

                            resultat = []
                            for value in values:
                                resultat.append(get_time_now(verif_callable(value, (), {}, variables[0])))

                            if len(resultat) == 1:
                                resultat = resultat[0]
                                
                        else:

                            for variable, value in get_variable_value(values):
                                set_var(variable, get_time_now(verif_callable(value, (), {}, variables[0])))

                    elif action == 'try':
                        """
                        """

                        def get_try(obj, retour=None):

                            try:
                                verif_callable(obj, (), {}, variables[0])
                            except Exception as e:
                                if retour:
                                    return verif_callable(retour, (), {}, variables[0])
                                else:
                                    return 'Exception: %s'%e

                        if retour:

                            resultat = []
                            for value in values:
                                resultat.append(get_try(*verif_callable(value, (), {}, variables[0])))

                            if len(resultat) == 1:
                                resultat = resultat[0]

                        else:

                            for variable, value in get_variable_value(values):
                                set_var(variable, get_try(*verif_callable(value, (), {}, variables[0])))

                    elif action == 'err':
                        """
                        >err> texte
                        Léve une erreur en affichant texte
                        """
                        value = values[0]
                        raise Exception('Module : %s, Cond : %s, Text : %s'%(ss.bloc.__name__, ss.nom, value))

                    elif action == 'typ':

                        def get_type(value):
                            if isinstance(value, (rac, redirection)):
                                value = value((), {}, variables[0])
                            return type(value).__name__

                        if retour:
                            resultat = []
                            for value in values:
                                resultat.append(get_type(value))

                            if len(resultat) == 1:
                                resultat = resultat[0]

                        else:
                            for variable, value in get_variable_value(values):
                                set_var(variable, get_type(value))

                    elif action == 'add':
                        """
                        add var (value nouv_var)
                        """

                        obj_vars = variables[0][0]

                        def ajout(variable, value, nouv_var=None):
                            value = verif_callable(value, (), {}, variables[0])

                            def _ajout(variables, variable, value):

                                if isinstance(variables[variable], list):
                                    if retour:
                                        return variables[variable][:].append(value)
                                    if nouv_var:
                                        obj_vars[nouv_var] = variables[variable][:].append(value)
                                    else:
                                        variables[variable].append(value)

                                elif isinstance(variables[variable], dict):
                                    if retour:
                                        return dict(zip(
                                                    list(variables[variable].keys()) + list(value.keys()),
                                                    list(variables[variable].values()) + list(value.values())
                                                ))
                                    elif nouv_var:
                                        obj_vars[nouv_var] = dict(zip(
                                                                list(variables[variable].keys()) + list(value.keys()),
                                                                list(variables[variable].values()) + list(value.values())
                                                            ))
                                    else:
                                        for k, v in value.items():
                                            variables[variable][k] = v

                                else:
                                    if retour:
                                        return variables[variable] + value
                                    elif nouv_var:
                                        obj_vars[nouv_var] = variables[variable] + value
                                    else:
                                        variables[variable] += value

                            return set_var(variable, value, fonction=_ajout)

                        if retour:
                            resultat = []
                            for value in values:
                                resultat.append(ajout(*verif_callable(value, (), {}, variables[0])))

                            if len(resultat) == 1:
                                resultat = resultat[0]

                        else:
                            for value in values:
                                ajout(*verif_callable(value, (), {}, variables[0]))

                    elif action == 'del':

                        def supr(value):

                            for zone in variables:
                                for vars_ in zone:
                                    if value in vars_:
                                        del vars_[value]
                                        return

                            raise Exception("La variable '%s' n'existe pas !"%value)

                        for value in values:
                            supr(value)

                    elif action == 'eli':

                        def eliminar(variable, value, nouv_var=None):
                            value = verif_callable(value, (), {}, variables[0])

                            def _eli(variables, variable, value):

                                if isinstance(variables[variable], list):
                                    if retour:
                                        return [val for val in variables[variable] if val not in value]
                                    elif nouv_var:
                                        obj_vars[nouv_var] = [val for val in variables[variable] if val not in value]
                                    else:
                                        for val in value:
                                            variables[variable].remove(val)

                                elif isinstance(variables[variable], dict):
                                    if retour:
                                        return {k:v for k,v in variables[variable].items() if k not in value}
                                    elif nouv_var:
                                        obj_vars[nouv_var] = {k:v for k,v in variables[variable].items() if k not in value}
                                    else:
                                        for k in value:
                                            del variables[variable][k]

                                else:
                                    if retour:
                                        return variables[variable] - value
                                    elif nouv_var:
                                        obj_vars[nouv_var] = variables[variable] - value
                                    else:
                                        variables[variable] -= value

                            return set_var(variable, value, fonction=_eli)
     
                        if retour:
                            resultat = []
                            for value in values:
                                resultat.append(eliminar(*verif_callable(value, (), {}, variables[0])))

                            if len(resultat) == 1:
                                resultat = resultat[0]

                        else:
                            for value in values:
                                eliminar(*verif_callable(value, (), {}, variables[0]))

                    elif action == 'cvt':

                        def convertion(type_, variable):
                            variable = verif_callable(variable, (), {}, variables[0])

                            if type_ == type(variable).__name__:
                                var = variable

                            elif type_ == 'pos':
                                var = pos(variable)

                            elif type_ == 'neg':
                                var = neg(variable)

                            elif type_ == 'nbr':
                                var = nbr(variable)

                            elif type_ == 'bool':
                                var = bool(variable)

                            elif type_ == 'str':
                                var = str(variable)

                            elif type_ == 'bytes':
                                if isinstance(variable, str):
                                    var = bytes(variable.encode())
                                else:
                                    var = bytes(variable)

                            elif type_ == 'tuple':
                                var = tuple(variable)

                            elif type_ == 'list':
                                var = list(variable)

                            elif type_ == 'dict':
                                var = dict(variable)
                                
                            else:
                                raise TypeError('Type %s inconnue !'%type_)

                            return var

                        if retour:
                            resultat = [convertion(*verif_callable(value, (), {}, variables[0])) for value in values]
                            if len(resultat) == 1:
                                resultat = resultat[0]

                        else:
                            for variable, value in get_variable_value(values):
                                set_var(variable, convertion(*verif_callable(value, (), {}, variables[0])))

                    else:
                        raise Exception("L'action \"%s\" n'existe pas !"%action)

                    if resultat is not None:
                        resultats[action] = resultat

                    resultat = None

                if len(ss.remonter) == 1:
                    if py_bool(ss.remonter[0]) == status:
                        continue
                elif ss.remonter:
                    if _analyse_comparaison(ss.remonter, *act_utile):
                        continue

                #Retourne résulta(s)
                if not len(resultats):
                    return None
                elif len(resultats) == 1:
                    return resultats[0]
                else:
                    return resultats

            else:
                #Dans le cas où il n'y a pas d'actions corespondant au status
                return bool(status)