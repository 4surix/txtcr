# coding: utf-8
# Python 3.6.2
# ----------------------------------------------------------------------------

from hashlib import md5


from txtcr.core.types import *
from txtcr.util._utile import balises


def check_all_values_is_dict_with_same_keys(data):

    # Si il n'y a pas de dictionnaire ou seulement un seul
    #  cela ne sert à rien de faire des clefs globales.
    # L'aventage des clefs globales c'est quand il y a plusieurs dict
    #  avec les même clefs pour que ça prend moins de place.
    if len(data) < 2:
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
        profondeur = 0,
        position = [0], 
        indent = 0, 
        raccourcis_keys = [],
        verif_hash = False,
        hashs = {},
        positions_sans_marquage = []
    ):

    # String
    if isinstance(data, str):

        str_simple = data and data[0] not in '0123456789'

        if str_simple:
            for carac in data:
                if (
                    carac == ' '
                    or carac == '\n'
                    or carac == '\t'
                    or carac == '\\'
                    or carac in balises
                ):
                    str_simple = False
                    break

        if str_simple:
            value_encoded = value_encoded_NI = data
        else:
            value_encoded = value_encoded_NI = (
                '"%s"'
                % data
                .replace('\\', '\\\\')
                .replace('"', '\\"')
                .replace('\n', '\\n')
                .replace('\t', '\\t')
            )

    # Bytes
    elif isinstance(data, bytes):
        value_encoded = value_encoded_NI = (
            "'%s'"
            % data.decode()
            .replace('\\', '\\\\')
            .replace("'", "\\'")
            .replace('\n', '\\n')
            .replace('\t', '\\t')
        )

    # Boolean
    elif isinstance(data, bool):
        if data:
            value_encoded = value_encoded_NI = 'True'
        else:
            value_encoded = value_encoded_NI = 'False'

    elif isinstance(data, (int, float)):
        value_encoded = value_encoded_NI = "%s" % data

    elif isinstance(data, dict):

        value_encoded = value_encoded_NI = '{'

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
                    profondeur = profondeur + 1,
                    position = position + ['__#KG%s#__' % index_KG],
                    indent = indent
                )

                value_encoded += f"{espacement}{espace}:{key}"
                value_encoded_NI += f"{espace}:{key}"

                if not indent:
                    espace = ' '

                index_KG += 1


        index = 0

        for key__, value__ in sorted(data.items()):

            key = (
                '' if raccourcis_keys
                else
                    encode(
                        key__,
                        profondeur = profondeur + 1,
                        position = position,
                        indent = indent,
                        hashs = hashs
                    )
            )

            value = encode(
                value__,
                positions_sans_marquage = positions_sans_marquage,
                raccourcis_keys = raccourcis_keys__,
                profondeur = profondeur + 1,
                position = position + [
                    key__ if not raccourcis_keys
                    else
                        raccourcis_keys[index]
                ],
                indent = indent,
                hashs = hashs
            )

            index += 1

            value_encoded += f"{espacement}{espace}{key}{milieu}{value}"
            value_encoded_NI += f"{espace}{key} {value}"

            if not indent:
                espace = ' '

        if indent:
            value_encoded += '\n' + ' ' * indent * profondeur

        value_encoded += '}'
        value_encoded_NI += '}'

    elif isinstance(data, (list, tuple)):

        SYMBOL_OPEN, SYMBOL_CLOSE = {
            list: ('[', ']'),
            tuple: ('(', ')')
        }[type(data)]

        value_encoded = value_encoded_NI = SYMBOL_OPEN

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

                ### Positon lock
                #

                locked = '@'

                positions_locks = {
                    tuple(position + [index, key__])
                    for index in range(len(data))
                }

                for position_lock in positions_locks:
                    if position_lock not in hashs:
                        locked = ''
                        break

                if locked: positions_sans_marquage = [
                    *positions_sans_marquage, *positions_locks
                ]

                ### Encode key
                #

                key = encode(
                    key__,
                    profondeur = profondeur + 1,
                    position = position + ['__#KG%s#__' % index_KG],
                    indent = indent,
                    hashs = hashs
                )

                value_encoded += f"{espacement}{espace}{locked}:{key}"
                value_encoded_NI += f"{espace}{locked}:{key}"

                if not indent:
                    espace = ' '

                index_KG += 1


        for index, value in enumerate(data):

            value = encode(
                value,
                positions_sans_marquage = positions_sans_marquage,
                raccourcis_keys = raccourcis_keys__,
                profondeur = profondeur + 1,
                position = position + [index],
                indent = indent,
                hashs = hashs
            )

            value_encoded += f"{espacement}{espace}{value}"
            value_encoded_NI += f"{espace}{value}"

            if not indent:
                espace = ' '

        if indent:
            value_encoded += '\n' + ' ' * indent * profondeur

        value_encoded += SYMBOL_CLOSE
        value_encoded_NI += SYMBOL_CLOSE

    elif data is None:
        value_encoded = value_encoded_NI = 'None'

    elif is_class(data):

        # Instance ou Class

        clss = data.__class__
        clss_info = clss.__dict__

        if '__weakrefoffset__' in clss_info:
            clss = data
            clss_info = clss.__dict__

        value_encoded = value_encoded_NI = '<'

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
                profondeur = profondeur + 1,
                position = position + [balise],
                indent = indent,
                hashs = hashs
            )

            value_encoded += f"{espacement}{espace}{balise}{value}"
            value_encoded_NI += f"{espace}{balise}{value}"

            if not indent:
                espace = ' '

        if indent:
            value_encoded += '\n' + ' ' * indent * profondeur

        value_encoded += '>'
        value_encoded_NI += '>'

    else:
        raise TypeError(
            'Type %s non compatible !' % type(data)
            + '\nTraceback (index/key):'
            + '\n' + '\n'.join(
                ('    ' * i) + str(value)
                for i, value in enumerate(position)
            )
        )


    if hashs:

        position = tuple(position)

        hash__ = hashs.get(position)

        if hash__:

            if hash__ != md5(value_encoded_NI.encode('utf-8')).hexdigest():
                raise ValueError(
                    f'Une valeur bloquée à été modifiée !\nTraceback (index/key):\n'
                    + '\n'.join(
                        ('    ' * i) + str(value)
                        for i, value in enumerate(position)
                    )
                )

            if not verif_hash and position not in positions_sans_marquage:
                value_encoded = '@' + value_encoded


    return value_encoded