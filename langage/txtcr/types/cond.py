import pytz

from ._condition import *

from .calc import *

# Retour -------------------------------------------------------------

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

# Condition -----------------------------------------------------------

class cond:
    def __init__(ss, condition, nom):
        make_id(ss)

        ss.nom = nom

        ss.value = condition

        ss.parametres, ss.comparaison, *ss.actions = get_comparaison_actions(condition)

        ss.callable_with_not_call = False

        ss.clss = None
        
    def __eq__(ss, obj):
        return ss.value == obj.value
    def __ne__(ss, obj):
        return ss.value != obj.value
    
    def __str__(ss):
        return ':%s:'%ss.value
    def __repr__(ss):
        return ':%s:'%ss.value

    def __iter__(ss):
        yield None

    def __call__(ss, cle, ops, variables):
        variables = get_vars(ss.clss, ops, variables)
        decode = ss.clss.__class__.__decode__

        if ss.parametres:
            for key, value in zip(decode(ss.parametres, with_hashtag=False), cle):
                if callable(value):
                    value = value([], {}, variables[0])
                variables[0][0][key] = value

        act_variables = variables
        act_defauts = ss.clss.__class__.__defauts__
        act_decode = decode

        act_utile =(act_variables,
                    act_defauts,
                    act_decode)

        status = analyse_comparaison(ss.comparaison, *act_utile)

        #----------------------------------------------------------
        #                       ACTIONS
        #----------------------------------------------------------

        actions = ss.actions[status]

        if actions: 

            def set_var(var, new=None):

                for zone in act_variables:
                    for vars_ in zone:
                        if var in vars_:
                            if new != None: vars_[var] = new
                            return {'var':vars_[var]}

                if new is None:
                    raise erreurs.VariableError(var)
                else:
                    act_variables[0][0][var] = new

            def get_variable_value(params):

                for nbr in range(0, len(params), 2):
                    yield params[nbr:nbr+2]

            resultats = result()
            
            for action, type_, value in actions:

                resultat = None

                if action == 'aff':
                    """
                    >aff> texte
                    Sert à afficher un texte à partir d'une variable ou d'une valeur directement
                    """
                    for value in act_decode(value, ever_list=True):
                        value = recup_redirection(value, act_variables, act_defauts, act_decode)
                        if callable(value):
                            value = value([], {}, act_variables[0])
                        print(value)

                elif action == 'ped':
                    """
                    >ped> nouv_var texte
                    Sert à demander une valeur à l'utilisateur, si le paramétre nouv_var est indiqué, l'enregistre dedans
                    """
                    params = act_decode(value, ever_list=True)

                    if not params:
                        resultat = act_decode(input())

                    elif len(params) == 1:
                        if type_ == '<':
                            resultat = recup_redirection(act_decode(input(params[0])), act_variables, act_defauts, act_decode)
                        elif type_ == '>':
                            act_variables[0][0][recup_redirection(params[0])] = recup_redirection(act_decode(input()), act_variables, act_defauts, act_decode)

                    elif len(params) == 2:
                        act_variables[0][0][recup_redirection(params[0])] = recup_redirection(act_decode(input(params[1])), act_variables, act_defauts, act_decode)

                    else:
                        raise erreurs.ParamError('ped')

                elif action == 'get':
                    """
                    >get> variable/value
                    Retourne la valeur d'une variable ou la valeur indiquée
                    """
                    params = act_decode(value, ever_list=True)
                    
                    if params and type_ == '<':

                        def verif_callable(obj):
                            if callable(obj):
                                obj = obj([], {}, act_variables[0])
                            return obj

                        resultat = [verif_callable(recup_redirection(element, act_variables, act_defauts, act_decode)) for element in params]
                        if len(resultat) == 1:
                            resultat = resultat[0]

                    else:
                        raise erreurs.ParamError('get')

                elif action == 'set':
                    """
                    >set> variable value
                    Créer/modifie une variable avec la valeur indiquée
                    """
                    params = act_decode(value, ever_list=True)

                    if (len(params) % 2) == 0 and type_ == '>':

                        for variable, value in get_variable_value(params):

                            variable = recup_redirection(variable)
                            value = recup_redirection(value, act_variables, act_defauts, act_decode)
                            if callable(value):
                                value = value([], {}, act_variables[0])

                            act_variables[0][0][variable] = value

                    else:
                        raise erreurs.ParamError('>set>')

                elif action == 'add':
                    """
                    >add> variable value
                    Ajout la valeur à la variable
                    """
                    params = act_decode(value, ever_list=True)

                    if len(params) == 2:

                        variable, element = params

                        var = recup_redirection(variable)
                        element = recup_redirection(element, act_variables, act_defauts, act_decode)

                        if callable(element):
                            element = element([], {}, act_variables[0])

                        trouver = False

                        for zone in act_variables:
                            for vars_ in zone:
                                if var in vars_:
                                    if isinstance(vars_[var], list):
                                        vars_[var].append(element)
                                    elif isinstance(vars_[var], dict):
                                        for key, value in element.items():
                                            vars_[var][key] = value
                                    elif isinstance(vars_[var], tuple):
                                        vars_[var] = vars_[var] + (element,)
                                    else:
                                        vars_[var] += element

                                    trouver = True; break
                            if trouver: break
                        if not trouver:
                            raise erreurs.VariableError(var)

                    elif len(params) == 3:

                        variable, element, nouv_var = params

                        var = recup_redirection(variable)
                        element = recup_redirection(element, act_variables, act_defauts, act_decode)

                        if callable(element):
                            element = element([], {}, act_variables[0])

                        trouver = False

                        for zone in act_variables:
                            for vars_ in zone:
                                if var in vars_:
                                    if isinstance(vars_[var], list):
                                        nouv_val = vars_[var][:]
                                        nouv_val.append(element)
                                    elif isinstance(vars_[var], dict):
                                        nouv_val = {}
                                        for key, value in vars_[var].items():
                                            nouv_val[key] = value
                                        for key, value in element.items():
                                            nouv_val[key] = value
                                    elif isinstance(vars_[var], tuple):
                                        nouv_val = vars_[var] + (element,)
                                    else:
                                        nouv_val = vars_[var] + element

                                    trouver = True; break
                            if trouver: break
                        if not trouver:
                            raise erreurs.VariableError(var)

                        act_variables[0][0][nouv_var] = nouv_val

                    else:
                        raise erreurs.ParamError('>add>')

                elif action == 'del':
                    """
                    >del> variable value
                    Supprime la valeur à la variable
                    """
                    params = act_decode(value, ever_list=True)

                    trouver = False

                    if len(params) == 1:
                        var = recup_redirection(params[0])
                        for zone in act_variables:
                            for vars_ in zone:
                                if var in vars_:
                                    del vars_[var]

                                    trouver = True; break
                            if trouver: break
                        if not trouver:
                            raise erreurs.VariableError(var)

                    elif len(params) == 2:

                        var = recup_redirection(params[0])
                        element = recup_redirection(params[1], act_variables, act_defauts, act_decode)

                        if callable(element):
                            element = element([], {}, act_variables[0])
                        
                        for zone in act_variables:
                            for vars_ in zone:
                                if var in vars_:

                                    if isinstance(vars_[var], list):
                                        vars_[var].remove(element)
                                    elif isinstance(vars_[var], dict):
                                        del vars_[var][element]
                                    elif isinstance(vars_[var], tuple):
                                        vars_[var] = vars_[var] - (element,)
                                    elif isinstance(vars_[var], str):
                                        vars_[var] = vars_[var].replace(element, '')
                                    else:
                                        vars_[var] -= element

                                    trouver = True; break
                            if trouver: break
                        if not trouver:
                            raise erreurs.VariableError(var)

                    elif len(params) == 3:

                        var = recup_redirection(params[0])
                        element = recup_redirection(params[1], act_variables, act_defauts, act_decode)
                        nouv_var = params[2]

                        if callable(element):
                            element = element([], {}, act_variables[0])
                        
                        for zone in act_variables:
                            for vars_ in zone:
                                if var in vars_:

                                    if isinstance(vars_[var], list):
                                        nouv_val = vars_[var][:]
                                        nouv_val.remove(element)
                                    elif isinstance(vars_[var], dict):
                                        nouv_val = {k:v for k,v in vars_[var].items()}
                                        del nouv_val[element]
                                    elif isinstance(vars_[var], tuple):
                                        nouv_val = vars_[var] - (element,)
                                    elif isinstance(vars_[var], str):
                                        nouv_val = vars_[var].replace(element, '')
                                    else:
                                        nouv_val = vars_[var] - element

                                    trouver = True; break
                            if trouver: break
                        if not trouver:
                            raise erreurs.VariableError(var)

                        act_variables[0][0][nouv_var] = nouv_val

                    else:
                        raise erreurs.ParamError('>del>')

                elif action == 'typ':
                    """
                    >typ> nouv_var variable
                    Récupére le type de la variable, la retourne ou le met dans nouv_var si indiqué
                    """
                    params = act_decode(value, ever_list=True)

                    if type_ == '<':

                        resultat = [type(recup_redirection(element, act_variables, act_defauts, act_decode)).__name__ for element in params]
                        if len(resultat) == 1:
                            resultat = resultat[0]

                    elif type_ == '>':

                        if (len(params) % 2) == 0:

                            for variable, value in get_variable_value(params):

                                act_variables[0][0][recup_redirection(variable)] = type(recup_redirection(value, 
                                                                                                        act_variables, 
                                                                                                        act_defauts, 
                                                                                                        act_decode)).__name__
                        else:
                            raise erreurs.ParamError('>typ>')

                elif action == 'len':
                    """
                    >len> nouv_var variable
                    Récupére le nombre d'élement 
                    """
                    params = act_decode(value, ever_list=True)

                    if type_ == '<':
                        resultat = [len(recup_redirection(element, act_variables, act_defauts, act_decode)) for element in params]
                        if len(resultat) == 1:
                            resultat = resultat[0]

                    elif type_ == '>':

                        if (len(params) % 2) == 0:

                            for variable, value in get_variable_value(params):
                                act_variables[0][0][recup_redirection(variable)] = len(recup_redirection(value, 
                                                                                                        act_variables, 
                                                                                                        act_defauts, 
                                                                                                        act_decode))
                        else:
                            raise erreurs.ParamError('>len>')

                elif action == 'ale':
                    """
                    >ale> nouv_var (min, max, decimal)
                    Génére un nombre aléatoire entre min et max inclue, 
                    si décimal est indiqué renvoie un nombre à virgule avec le nombre de chiffre après la virgule
                    """
                    params = act_decode(value, ever_list=True)

                    def creer_nbr_alea(nbrs):

                        if len(nbrs) == 2:
                            return random.randint(nbrs[0].value, nbrs[1].value)
                        elif len(nbrs) == 3:
                            return float(str(random.uniform(nbrs[0].value, nbrs[1].value))[:nbrs[2]+2])
                        else:
                            raise erreurs.ParamError('>ale>')

                    if type_ == '<':
                        resultat = [creer_nbr_alea(element) for element in params]
                        if len(resultat) == 1:
                            resultat = resultat[0]

                    elif type_ == '>':

                        if (len(params) % 2) == 0:

                            for variable, value in get_variable_value(params):
                                act_variables[0][0][recup_redirection(variable)] = creer_nbr_alea(value)

                        else:
                            raise erreurs.ParamError('>ale>')

                elif action == 'now':
                    """
                    >now> nouv_var (début, fin, TZ)
                    Renvoie une liste de la date actuel de TZ
                    """
                    params = act_decode(value, ever_list=True)

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

                        return tuple([pos(int(nbr)) for nbr in datetime.now(tz=tz).strftime("%Y/%m/%d/%H/%M/%S/%f").split('/')][début:limite+1])

                    if not params:
                        resultat = get_time_now()
                    elif len(params) == 1:
                        param = recup_redirection(params[0], act_variables, act_defauts, act_decode)
                        if type_ == '<':
                            resultat = get_time_now(param)
                        elif type_ == '>':
                            set_var(param, get_time_now())
                    elif len(params) == 2:
                        variable = recup_redirection(params[0])
                        param = recup_redirection(params[1], act_variables, act_defauts, act_decode)
                        set_var(variable, get_time_now(param))
                    else:
                        raise erreurs.ParamError('>now>')

                elif action == 'err':
                    """
                    >err> texte
                    Léve une erreur en affichant texte
                    """
                    raise Exception('Module : %s, Cond : %s, Text : %s'%(ss.clss.__class__.__name__, ss.nom, value))

                elif action == 'try':
                    """
                    >try> var texte
                    """
                    params = act_decode(value, ever_list=True)

                    def try_cond(condition, retour=None):

                        try:
                            return recup_redirection(condition, act_variables, act_defauts, act_decode)
                        except Exception as e:
                            if retour == None:
                                return 'Exception: %s'%e
                            else:
                                return retour

                    if type_ == '<':

                        resultat = [try_cond(*element) for element in params]
                        if len(resultat) == 1:
                            resultat = resultat[0]

                    elif type_ == '>':

                        if (len(params) % 2) == 0:

                            for variable, value in get_variable_value(params):

                                act_variables[0][0][recup_redirection(variable)] = try_cond(*value)
                        else:
                            raise erreurs.ParamError('>try>')

                elif action == 'run':
                    """
                    >run>
                    """
                    params = act_decode(value, ever_list=True)

                    variable = None

                    if type_ == '<':
                        resultat = [main(recup_redirection(prog, act_variables, act_defauts, act_decode)) for prog in params]
                        if len(resultat) == 1:
                            resultat = resultat[0]

                    elif type_ == '>':

                        if (len(params) % 2) == 0:

                            for variable, value in get_variable_value(params):
                                act_variables[0][0][recup_redirection(variable)] = main(recup_redirection(value, 
                                                                                                        act_variables,
                                                                                                        act_defauts, 
                                                                                                        act_decode))
                        else:
                            raise erreurs.ParamError('>run>')

                #A faire --------------
                elif action == 'for':
                    pass

                elif action == 'log':
                    pass
                #----------------------

                else:
                    raise Exception("L'action >%s> n'existe pas !"%action)

                if resultat != None:
                    resultats[action] = resultat

            #Retourne résulta(s)
            if not len(resultats):
                return None
            elif len(resultats) == 1:
                return resultats[0]
            else:
                return resultats

        return bool(status)
    
    def is_(ss, obj):
        return ss.__class__.__id__ == obj.__class__.__id__
    def not_is(ss, obj):
        return ss.__class__.__id__ != obj.__class__.__id__