from .types import *

def config_echappemet(data):
    return data.replace('\\', '\\\\').replace('\n', '\\n').replace('\t', '\\t')

def encode(data):

    if isinstance(data, str):
        return '"%s"' % config_echappemet(data).replace('"', '\\"')

    elif isinstance(data, bytes):
        return "'%s'" % config_echappemet(data).replace("'", "\\'")

    elif isinstance(data, (int, float)):
        if py_str(data)[0] == '-':
        	return "%s" % data
        else:
        	return "+%s" % data

    elif isinstance(data, dict):
        keys = [encode(key) for key in data.keys()]
        values = [encode(value) for value in data.values()]
        return "{%s}" % ' '.join([' '.join([k,v]) for k,v in zip(keys, values)])

    elif isinstance(data, list):
        return '[%s]' % ' '.join([encode(value) for value in data])

    elif isinstance(data, tuple):
        return '(%s)' % ' '.join([encode(value) for value in data])

    elif isinstance(data, bool):
        comm = ''
        if 'commentaire' in dir(data):
            comm = data.commentaire

        if data == True:
            return '1"%s"'%comm
        elif data == False:
            return '0"%s"'%comm

    elif isinstance(data, none):
        return 'O"%s"'(data.commentaire if 'commentaire' in dir(data) else '')

    elif is_class(data):
        clss = data.__class__
        clss_info = clss.__dict__
        if '__weakrefoffset__' in clss_info:
            clss = data
            clss_info = clss.__dict__

        balises =  ['N#',
                    'D#',
                    'R#',
                    'S#',
                    'I#'
        ]

        infos= [clss.__name__, 
                clss.__doc__, 
                clss_info.get('__irepr__'),
                clss_info.get('__istr__'),
                encode({k:v for k,v in data.__dict__.items() if k[:2] != '__'})
        ]
        return '<%s>'%' '.join(['%s%s'%(balise, info) for balise, info in zip(balises, infos) if info])