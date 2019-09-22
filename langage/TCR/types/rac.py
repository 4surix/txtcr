
from .bloc import *

class importation:
    def __init__(ss):
        ss.value = []

    def module(ss):
        return ss.value.value[0]

    def append(ss, obj):
        #Toujours redirection
        ss.value = obj

class rac(py_str):
    def __init__(ss, value):
        ss.value = value

        ss.bloc = None

    def __call__(ss, params, kwargs, variables):
        variables = get_vars(ss, (), params, {}, kwargs, variables)
        variable = get_var(ss.value, variables)
        return verif_callable(variable, (), {}, variables[0])

    def __str__(ss):
        return '%s'%ss.value

    def __repr__(ss):
        return '#%s#'%ss.value

    def __iter__(ss):
        yield None

class call:
    def __init__(ss, variable, bloc):
        ss.values = []
        ss.variable = variable

        ss.bloc = bloc

    def __call__(ss, params, kwargs, vars_objets):
        variables = get_vars(ss, (), params, {}, kwargs, vars_objets)

        parametres = ss.values

        args, kwargs = get_args_kwargs(parametres, variables)

        variable = get_var(ss.variable, variables)
        return variable(args, kwargs, variables[0])

    def __iter__(ss):
        yield None

    def append(ss, obj):
        ss.values = obj

class redirection:
    def __init__(ss, bloc):
        ss.value = []

        ss.bloc = bloc

    def __call__(ss, params, kwargs, vars_objets):
        variables = get_vars(ss, (), params, {}, kwargs, vars_objets)

        variable = ss.value[0]
        if callable(variable):
            variable = variable((), {}, variables[0])

        for index in ss.value[1:]:
            variable = variable[verif_callable(index, (), {}, variables[0])]
            
        if not ss.value[1:]:
            variable = get_var(variable, variables)

        return variable #verif_callable(variable, (), {}, variables[0])

    def __str__(ss):
        return '#%s#|'%(ss.value)

    def __repr__(ss):
        return '#%s#|'%(ss.value)

    def __iter__(ss):
        yield None

    def append(ss, obj):
        ss.value.append(obj)