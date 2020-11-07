# coding: utf-8
# Python 3.6.2
# ----------------------------------------------------------------------------

from txtcr.core.types import *


def config_indent(profondeur, indent):
    return ('\n' + ' ' * indent * profondeur
            if indent else '')


# Chars escaping
def config_echappement(data):
    return data.replace('\\', '\\\\').replace('\n', '\\n').replace('\t', '\\t')


# Main encoding function
def encode(data, *, profondeur=-1, indent=0):
    profondeur += 1

    # String
    if isinstance(data, str):
        return '"%s"' % config_echappement(data).replace('"', '\\"')

    # Bytes
    elif isinstance(data, bytes):
        return "'%s'" % config_echappement(data.decode()).replace("'", "\\'")

    # Boolean
    elif isinstance(data, bool):
        if data:
            return 'True'
        else:
            return 'False'

    elif isinstance(data, (int, float)):
        return "%s" % data

    elif isinstance(data, dict):
        keys = [
            encode(key, profondeur = profondeur, indent = indent)
            for key in data.keys()
        ]
        values = [
            encode(value, profondeur = profondeur, indent = indent)
            for value in data.values()
        ]

        _indent = config_indent(profondeur, indent)
        sep = _indent + ' '

        return (
            _indent
            + '{'
            + sep.join([' '.join([k, v]) for k, v in zip(keys, values)])
            + _indent
            + "}"
        )

    elif isinstance(data, list):
        _indent = config_indent(profondeur, indent)
        sep = _indent + ' '

        return (
            _indent
            + '['
            + sep.join([
                encode(value, profondeur=profondeur, indent=indent) 
                for value in data
            ])
            + _indent
            + ']'
        )

    elif isinstance(data, tuple):
        _indent = config_indent(profondeur, indent)
        sep = _indent + ' '

        return (
            _indent
            + '('
            + sep.join([
                encode(value, profondeur=profondeur, indent=indent) 
                for value in data
            ])
            + _indent
            + ')'
        )

    elif data is None:
        return 'None'

    elif is_class(data):

        # Instance ou Class

        clss = data.__class__
        clss_info = clss.__dict__

        if '__weakrefoffset__' in clss_info:
            clss = data
            clss_info = clss.__dict__

        balises = [
            'N#',
            'D#',
            'R#',
            'S#',
            'C#',
            'T#',
            'H#',
            'I#'
        ]

        def encode_symlink(value):
            return (
                None if value is None
                else
                    encode(value, profondeur=profondeur, indent=indent)
            )

        valeurs = [
            encode_symlink(clss.__name__ or None),
            encode_symlink(clss.__doc__ or None),
            encode_symlink(getattr(data, 'repr__', None)),
            encode_symlink(getattr(data, 'str__', None)),
            encode_symlink(getattr(data, 'cmdcode__', None)),
            encode_symlink(getattr(data, 'date__', None)),
            encode_symlink(getattr(data, 'hash__', None)),
            encode_symlink(
                {
                    k: v 
                    for k, v in data.__dict__.items() if str(k)[-2:] != '__'
                } or None
            )
        ]

        _indent = config_indent(profondeur, indent)
        sep = _indent + ' '

        return (
            _indent
            + '<'
            + sep.join([
                balise + valeur
                for balise, valeur in zip(balises, valeurs)
                if valeur is not None
            ])
            + _indent
            + '>'
        )

    else:
        raise TypeError('Type %s non compatible !' % type(data))
