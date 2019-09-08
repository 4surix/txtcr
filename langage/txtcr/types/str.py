from .none import *

# Str -------------------------------------------------------------

class str(py_str):

    def __init__(ss, texte):
        make_id(ss)

        ss.value = texte

        ss.callable_with_not_call = False

        ss.redirection = False

        ss.clss = None

    def __eq__(ss, obj):
        return ss.value == obj
    def __ne__(ss, obj):
        return ss.value != obj

    def __str__(ss):
        if ss.redirection:
            return '%s'%ss.verif(get_vars(ss.clss))
        else:
            return ss.value

    def __repr__(ss):
        if ss.redirection:
            return '"%s"'%ss.verif(get_vars(ss.clss))
        else:
            return '"%s"'%ss.value

    def __call__(ss, cle, ops, variables):
        if ss.redirection:
            return '%s'%ss.verif(get_vars(ss.clss, ops, variables))
        else:
            return ss

    def __iadd__(ss, obj):
        ss.value = ss.value + str(obj)
        return ss.value

    def __hash__(ss):
        return hash(ss.value)

    #def __index__(ss): return len(ss.verif(get_vars(ss.clss)))

    def verif(ss, variables):

        texte = ss.value[:]

        for partie in texte.split("#")[1:-1:2]:

            partie_a_remplacer = '#%s#'%partie

            variable = recup_redirection(partie, 
                                        variables, 
                                        ss.clss.__class__.__defauts__,
                                        ss.clss.__class__.__decode__,
                                        hashtag=False)

            if variable != '#':
                texte = texte.replace(partie_a_remplacer, str(variable))

        nouv_texte = str(texte)
        nouv_texte.__id__ = ss.__id__

        return nouv_texte