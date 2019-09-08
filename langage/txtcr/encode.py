from .types import *

def config_echappemet(data):
    return data.replace('\\', '\\\\').replace('\n', '\\n').replace('\t', '\\t')

def encode(data):

    if isinstance(data, (str, py_str)):
        return '"%s"' % config_echappemet(data).replace('"', '\\"')

    elif isinstance(data, bytes):
        return "'%s'" % config_echappemet(data).replace("'", "\\'")

    elif isinstance(data, (int, float)):
        if py_str(data)[0] == '-':
        	return "%s" % data
        else:
        	return "+%s" % data

    elif isinstance(data, pos):
        return "%s" % py_str(data)

    elif isinstance(data, neg):
        return "%s" % py_str(data)

    elif isinstance(data, dict):
        keys = [encode(key) for key in data.keys()]
        values = [encode(value) for value in data.values()]
        return "{%s}" % ' '.join([' '.join([k,v]) for k,v in zip(keys, values)])

    elif isinstance(data, list):
        return '[%s]' % ' '.join([encode(value) for value in data])

    elif isinstance(data, tuple):
        return '(%s)' % ' '.join([encode(value) for value in data])

    elif isinstance(data, bool):
        if data == True:
            return '1""'
        elif data == False:
            return '0""'

    elif type(data).__name__ == 'NoneType':
        return 'O""'

    elif is_class(data):
        clss = data.__class__
        clss_info = clss.__dict__
        if '__weakrefoffset__' in clss_info:
            clss = data
            clss_info = clss.__dict__

        balises =  ['N#',
                    'D#',
                    'M#',
                    'B#',
                    'I#'
        ]

        infos= [clss.__name__, 
                clss.__doc__, 
                clss_info.get('__main__'),
                clss_info.get('__defauts__'),
                encode({k:v for k,v in data.__dict__.items() if k[:2] != '__'})
        ]
        
        return '<%s>'%' '.join(['%s%s'%(balise, info) for balise, info in zip(balises, infos) if info != None])