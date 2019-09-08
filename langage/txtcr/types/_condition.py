from ._base import *

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
    '&&': lambda var1, var2: (var1 and var2) == (var1 and var2),
    '|': lambda var1, var2: var1 or var2,
    '||': lambda var1, var2: (var1 or var2) != (var1 and var2),
}


class Actions:

    def __init__(ss):
        ss.actions = []
        ss.texte = ''
        ss.name = ''
        ss.act = ''

    def __str__(ss):
        return '%s %s'%(ss.name, ss.act)

    def append(ss, carac):
        ss.texte += carac

    def end(ss, carac):
        if not ss.name:
            ss.name = ss.texte[:]
            ss.type = carac
            ss.texte = ''
        else:
            ss.act = ss.texte[:]
            ss.actions.append([ss.name.strip(), ss.type, ss.act.strip()])
            ss.texte = ''
            ss.name = ''
            ss.type = ''
            ss.act = ''

def get_actions(actions_texte):

    if actions_texte is None:
        return

    in_texte = False
    actions = Actions()

    for place, carac in enumerate(actions_texte.strip()):

        if carac in ['>', '<'] and not in_texte:
            actions.end(carac)

        elif carac == '"' and not echappement:
            actions.append(carac)
            if in_texte:
                in_texte = False
            else:
                in_texte = True

        elif carac == '\\':
            if echappement:
                actions.append('\\')
            else:
                echappement = True
                continue
            
        else:
            actions.append(carac)

        echappement = False

    actions.end('')

    return actions.actions

def get_comparaison_actions(condition):

    if0 = ''
    if1 = ''
    parametres = ''
    comparaison = condition

    if ' acts ' in comparaison:
        parametres, if1 = comparaison.split(' acts ')
        comparaison = ''
    else:
        if ' else ' in comparaison:
            comparaison, if0 = comparaison.split(' else ')
        elif ' alors ' in comparaison:
            comparaison, if0 = comparaison.split(' alors ')

        if ' then ' in comparaison:
            comparaison, if1 = comparaison.split(' then ')
        elif ' sinon ' in comparaison:
            comparaison, if1 = comparaison.split(' sinon ')

        if ' if ' in comparaison:
            parametres, comparaison = comparaison.split(' if ')
        elif ' si ' in comparaison:
            parametres, comparaison = comparaison.split(' si ')

    def config_comparaison(condition):
        valeur = []
        comparaison = []

        def ajout_valeur(valeur):
            if valeur:
                valeur = ' '.join(valeur).strip()
                comparaison.append(valeur)
            return []

        for partie in condition.split(' '):

            if partie.replace('!', '') in func_comparaisons:
                valeur = ajout_valeur(valeur)
                comparaison.append(partie)
            elif partie or valeur:
                valeur.append(partie)

        ajout_valeur(valeur)

        return comparaison

    def decoupe_comparaison(texte):
        if not texte:
            return []

        liste_condition = []
        while 1:
            début, fin = recup_partie_parentese(texte)
            if fin:
                if début: liste_condition.extend(config_comparaison(texte[:début]))
                liste_condition.append(decoupe_comparaison(texte[début+1:fin]))
                texte = texte[fin+1:]
            else:
                liste_condition.extend(config_comparaison(texte))
                break
        return liste_condition

    return parametres.strip(), decoupe_comparaison(comparaison.strip()), get_actions(if0.strip()), get_actions(if1.strip())

#--------------------------------------------

def analyse_comparaison(comparaison, variables, defauts, decode):

    def copie(liste):
        return [copie(element) if len(element) == 3 and isinstance(element, list) else element for element in liste]

    def verif_type(value):

        if (isinstance(value, list)
            and len(value) >= 3 
            and isinstance(value[1], str) 
            and value[1].replace('!', '') in func_comparaisons):
                value = verif_comparaison(value)
        elif isinstance(value, str):
            value = decode(value)
            value = recup_redirection(value, variables, defauts, decode)

        if callable(value):
            value = value([], {}, variables[0])

        return value

    def get_values_and_symb(liste):
        for nbr in range(0, len(liste)-1, 2):
            yield [nbr+2] + liste[nbr:nbr+3]

    def verif_comparaison(comparaison):

        if len(comparaison) < 3:
            return True

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

        return comparaison[-1]

    return verif_comparaison(copie(comparaison)) #Copie de la liste pour éviter les modifs