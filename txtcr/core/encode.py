# coding: utf-8
# Python 3.6.2
# ----------------------------------------------------------------------------

from txtcr.core.types import *
from txtcr.util._utile import balises


def encode(data, *, profondeur = -1, indent = 0):

    profondeur += 1

    # String
    if isinstance(data, str):

        str_simple = False

        if data and data[0] not in '0123456789.':
            str_simple = True

            for carac in data:
                if carac == ' ' or carac in balises:
                    str_simple = False
                    break

        if str_simple:
            value_encoded = data
        else:
            value_encoded = (
                '"%s"'
                % data
                .replace('"', '\\"')
                .replace('\\', '\\\\')
                .replace('\n', '\\n')
                .replace('\t', '\\t')
            )

    # Bytes
    elif isinstance(data, bytes):
        value_encoded = (
            "'%s'"
            % data.decode()
            .replace("'", "\\'")
            .replace('\\', '\\\\')
            .replace('\n', '\\n')
            .replace('\t', '\\t')
        )

    # Boolean
    elif isinstance(data, bool):
        if data:
            value_encoded = 'True'
        else:
            value_encoded = 'False'

    elif isinstance(data, (int, float)):
        value_encoded = "%s" % data

    elif isinstance(data, dict):

        value_encoded = '{'

        espace = ''

        espacement = (
            '' if not indent
            else
                '\n' + ' ' * indent * (profondeur + 1)
        )

        for key, value in data.items():

            key = encode(
                key,
                profondeur = profondeur,
                indent = indent
            )

            value = encode(
                value,
                profondeur = profondeur,
                indent = indent
            )

            value_encoded += f"{espacement}{espace}{key} {value}"

            if not indent:
                espace = ' '

        value_encoded += (
            '' if not indent
            else
                '\n' + ' ' * indent * profondeur
        )

        value_encoded += '}'

    elif isinstance(data, list):

        value_encoded = '['

        espace = ''

        espacement = (
            '' if not indent
            else
                '\n' + ' ' * indent * (profondeur + 1)
        )

        for value in data:

            value = encode(
                value, 
                profondeur = profondeur,
                indent = indent
            )

            value_encoded += f"{espacement}{espace}{value}"

            if not indent:
                espace = ' '

        value_encoded += (
            '' if not indent
            else
                '\n' + ' ' * indent * profondeur
        )

        value_encoded += ']'

    elif isinstance(data, tuple):

        value_encoded = '('

        espace = ''

        espacement = (
            '' if not indent
            else
                '\n' + ' ' * indent * (profondeur + 1)
        )

        for value in data:

            value = encode(
                value, 
                profondeur = profondeur,
                indent = indent
            )

            value_encoded += f"{espacement}{espace}{value}"

            if not indent:
                espace = ' '

        value_encoded += (
            '' if not indent
            else
                '\n' + ' ' * indent * profondeur
        )

        value_encoded += ')'

    elif data is None:
        value_encoded = 'None'

    elif is_class(data):

        # Instance ou Class

        clss = data.__class__
        clss_info = clss.__dict__

        if '__weakrefoffset__' in clss_info:
            clss = data
            clss_info = clss.__dict__

        value_encoded = '<'

        espace = ''

        espacement = (
            '' if not indent
            else
                '\n' + ' ' * indent * (profondeur + 1)
        )

        for balise, value in zip(
                [
                    'N#',
                    'D#',
                    'R#',
                    'S#',
                    'C#',
                    'T#',
                    'H#',
                    'I#'
                ],
                [
                    clss.__name__ or None,
                    clss.__doc__ or None,
                    getattr(data, 'repr__', None),
                    getattr(data, 'str__', None),
                    getattr(data, 'cmdcode__', None),
                    getattr(data, 'date__', None),
                    getattr(data, 'hash__', None),
                    {
                        k: v 
                        for k, v in data.__dict__.items() 
                        if str(k)[-2:] != '__'
                    } or None
                ]
            ):

            if value is None:
                continue

            value = encode(
                value, 
                profondeur = profondeur,
                indent = indent
            )

            value_encoded += f"{espacement}{espace}{balise}{value}"

            if not indent:
                espace = ' '

        value_encoded += (
            '' if not indent
            else
                '\n' + ' ' * indent * profondeur
        )

        value_encoded += '>'

    else:
        raise TypeError('Type %s non compatible !' % type(data))


    return value_encoded