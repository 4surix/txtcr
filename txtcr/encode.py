from .types import *


def config_indent(profondeur, indent):
    return ('\n' + ' ' * indent * profondeur
            if indent else '')


def config_echappement(data):
    return data.replace('\\', '\\\\').replace('\n', '\\n').replace('\t', '\\t')


def encode(data, *, profondeur=-1, indent=0):

    profondeur += 1

    if isinstance(data, str):
        return '"%s"' % config_echappement(data).replace('"', '\\"')

    elif isinstance(data, bytes):
        return "'%s'" % config_echappement(data).replace("'", "\\'")

    elif isinstance(data, (py_bool, bool)):
        comm = ''
        if 'commentaire' in dir(data):
            comm = data.commentaire

        return ['0"%s"', '1"%s"'][data] % comm

    elif isinstance(data, (int, float)):
        return "%s" % data

    elif isinstance(data, dict):
        keys = [encode(key, profondeur=profondeur, indent=indent) for key in data.keys()]
        values = [encode(value, profondeur=profondeur, indent=indent) for value in data.values()]

        _indent = config_indent(profondeur, indent)
        sep = _indent + ' '

        return (_indent
                + '{' 
                + sep.join([' '.join([k, v]) for k, v in zip(keys, values)])
                + _indent 
                + "}")

    elif isinstance(data, list):
        _indent = config_indent(profondeur, indent)
        sep = _indent + ' '

        return (_indent
                + '['
                + sep.join([encode(value, profondeur=profondeur, indent=indent) for value in data])
                + _indent 
                + ']')

    elif isinstance(data, tuple):
        _indent = config_indent(profondeur, indent)
        sep = _indent + ' '

        return (_indent 
                + '(' 
                + sep.join([encode(value, profondeur=profondeur, indent=indent) for value in data])
                + _indent 
                + ')')

    elif isinstance(data, none):
        return 'O"%s"' % data.commentaire 

    elif type(data).__name__ == 'NoneType':
        return 'O""' 

    elif is_class(data):

        # Instance ou Class

        clss = data.__class__
        clss_info = clss.__dict__
        
        if '__weakrefoffset__' in clss_info:
            clss = data
            clss_info = clss.__dict__


        balises =  [
            'N#',
            'D#',
            'R#',
            'S#',
            'C#',
            'T#',
            'I#'
        ]

        syntaxe = getattr(data, 'syntaxe__', 0)

        encode_ = lambda v: None if v is None else encode(v, profondeur=profondeur, indent=indent)

        valeurs = [
                encode_(clss.__name__),
                encode_(clss.__doc__),
                encode_(getattr(data, 'repr__', None)),
                encode_(getattr(data, 'str__', None)),
                encode_(getattr(data, 'cmdcode__', None)),
                encode_(getattr(data, 'date__',  None)),
                encode_({k:v for k,v in data.__dict__.items() if str(k)[-2:] != '__'})
        ]

        _indent = config_indent(profondeur, indent)
        sep = _indent + ' '

        return (_indent
                + '<' 
                + sep.join(
                    [balise + valeur 
                     for balise, valeur in zip(balises, valeurs) 
                     if valeur is not None]
                  )
                + _indent 
                + '>')

    else:
        raise TypeError('Type %s non compatible !' % type(data))