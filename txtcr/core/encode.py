# coding: utf-8
# Python 3.6.2
# ----------------------------------------------------------------------------

from txtcr.core.types import *
from txtcr.util._utile import balises


def check_all_values_is_dict_with_same_keys(data):

    if not data:
        return

    if data[0].__class__ != dict:
        return

    keys = data[0].keys()

    for element in data:
        if element.__class__ != dict or element.keys() != keys:
            return

    return sorted(keys)


def encode(
        data, 
        *, 
        profondeur = -1, position = [0], indent = 0, raccourcis_keys = []
    ):

    profondeur += 1

    # String
    if isinstance(data, str):

        str_simple = data and data[0] not in '0123456789'

        if str_simple:
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

        milieu = ' ' if not raccourcis_keys else ''

        index_KG = 0

        raccourcis_keys__ = []

        keys = check_all_values_is_dict_with_same_keys(list(data.values()))

        if keys:

            for key__ in keys:

                raccourcis_keys__.append(key__)

                ### Encode key
                #

                key = encode(
                    key__,
                    profondeur = profondeur,
                    position = position + ['__#KG%s#__' % index_KG],
                    indent = indent
                )

                value_encoded += f"{espacement}{espace}:{key}"

                if not indent:
                    espace = ' '

                index_KG += 1


        index = 0

        for key__, value__ in data.items():

            key = (
                '' if raccourcis_keys
                else
                    encode(
                        key__,
                        profondeur = profondeur,
                        position = position,
                        indent = indent
                    )
            )

            value = encode(
                value__,
                raccourcis_keys = raccourcis_keys__,
                profondeur = profondeur,
                position = position + [
                    key__ if not raccourcis_keys
                    else
                        raccourcis_keys[index]
                ],
                indent = indent
            )

            index += 1

            value_encoded += f"{espacement}{espace}{key}{milieu}{value}"

            if not indent:
                espace = ' '

        if indent:
            value_encoded += '\n' + ' ' * indent * profondeur

        value_encoded += '}'

    elif isinstance(data, list):

        value_encoded = '['

        espace = ''

        espacement = (
            '' if not indent
            else
                '\n' + ' ' * indent * (profondeur + 1)
        )

        ### Keys globals
        #

        index_KG = 0

        raccourcis_keys__ = []

        keys = check_all_values_is_dict_with_same_keys(data)

        if keys:

            for key__ in keys:

                raccourcis_keys__.append(key__)

                ### Encode key
                #

                key = encode(
                    key__,
                    profondeur = profondeur,
                    position = position + ['__#KG%s#__' % index_KG],
                    indent = indent
                )

                value_encoded += f"{espacement}{espace}:{key}"

                if not indent:
                    espace = ' '

                index_KG += 1


        for index, value in enumerate(data):

            value = encode(
                value,
                raccourcis_keys = raccourcis_keys__,
                profondeur = profondeur,
                position = position + [index],
                indent = indent
            )

            value_encoded += f"{espacement}{espace}{value}"

            if not indent:
                espace = ' '

        if indent:
            value_encoded += '\n' + ' ' * indent * profondeur

        value_encoded += ']'

    elif isinstance(data, tuple):

        value_encoded = '('

        espace = ''

        espacement = (
            '' if not indent
            else
                '\n' + ' ' * indent * (profondeur + 1)
        )

        ### Keys globals
        #

        index_KG = 0

        raccourcis_keys__ = []

        keys = check_all_values_is_dict_with_same_keys(data)

        if keys:

            for key__ in keys:

                raccourcis_keys__.append(key__)

                ### Encode key
                #

                key = encode(
                    key__,
                    profondeur = profondeur,
                    position = position + ['__#KG%s#__' % index_KG],
                    indent = indent
                )

                value_encoded += f"{espacement}{espace}:{key}"

                if not indent:
                    espace = ' '

                index_KG += 1


        for index, value in enumerate(data):

            value = encode(
                value,
                raccourcis_keys = raccourcis_keys__,
                profondeur = profondeur,
                position = position + [index],
                indent = indent
            )

            value_encoded += f"{espacement}{espace}{value}"

            if not indent:
                espace = ' '

        if indent:
            value_encoded += '\n' + ' ' * indent * profondeur

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
                position = position + [balise],
                indent = indent
            )

            value_encoded += f"{espacement}{espace}{balise}{value}"

            if not indent:
                espace = ' '

        if indent:
            value_encoded += '\n' + ' ' * indent * profondeur

        value_encoded += '>'

    else:
        raise TypeError(
            'Type %s non compatible !' % type(data)
            + '\nTraceback (index/key):'
            + '\n' + '\n'.join(
                ('    ' * i) + str(value)
                for i, value in enumerate(position)
            )
        )


    return value_encoded