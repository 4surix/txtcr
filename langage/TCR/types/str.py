from .rac import *

# Str -------------------------------------------------------------

class str(py_str):

    def __init__(ss, texte):
        make_id(ss)

        ss.value = texte

    def __eq__(ss, obj):
        return ss.value == obj
    def __ne__(ss, obj):
        return ss.value != obj

    def __str__(ss):
        return '%s'%ss.value

    def __repr__(ss):
        return '"%s"'%ss.value

    def __add__(ss, obj):
        return str(ss.value + py_str(obj))

    def __iadd__(ss, obj):
        return str(ss.value + py_str(obj))

    def __sub__(ss, obj):
        return str(ss.value.replace(py_str(obj), ''))

    def __isub__(ss, obj):
        return str(ss.value.replace(py_str(obj), ''))

    def __hash__(ss):
        return hash(ss.value)