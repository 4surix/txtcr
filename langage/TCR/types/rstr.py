from .str import *

# Redirection Str -------------------------------------------------------------

class rstr():

    def __init__(ss, texte, bloc):
        make_id(ss)

        ss.value = texte

        ss.callable_with_not_call = False

        ss.bloc = bloc

    def __eq__(ss, obj):
        return ss.value == obj
    def __ne__(ss, obj):
        return ss.value != obj

    def __str__(ss): 
        return '%s'%ss.value

    def __repr__(ss): 
        return 'r"%s"'%ss.value

    def __call__(ss, cle, ops, vars_objets):
        v = get_vars(ss, (), cle, {}, ops, vars_objets)
        return '%s'%ss.verif(v)

    def __add__(ss, obj):
        return rstr(ss.value + py_str(obj))

    def __iadd__(ss, obj):
        return rstr(ss.value + py_str(obj))

    def __sub__(ss, obj):
        return rstr(ss.value.replace(py_str(obj), ''))

    def __isub__(ss, obj):
        return rstr(ss.value.replace(py_str(obj), ''))

    def __hash__(ss):
        return hash(ss.value)

    def verif(ss, variables):

        texte = ss.value[:]
        decode = ss.bloc.__decode__

        for partie in texte.split("#")[1:-1:2]:

            partie_a_remplacer = '#%s#'%partie

            if '(' in partie and ')' == partie[-1]:
                
                variable, parametres = partie[:-1].split('(', 1)

                variable = call(variable, ss.bloc)
                for param in decode(parametres):
                    variable.append(param)

            else:

                variable = redirection(ss.bloc)
                for param in decode(partie):
                    variable.append(param)

            variable = variable((), {}, variables[0])

            texte = texte.replace(partie_a_remplacer, str(variable))

        nouv_texte = str(texte)
        nouv_texte.__id__ = ss.__id__

        return nouv_texte