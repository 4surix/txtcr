from ._utile import *

class Bloc_base(list):
    
    def __init__(ss):

        ss.__name__ = ''
        ss.__defauts__= {}

        ss.__vars__ = [
                [],
                ss,
                [],
                [ss.__defauts__]
            ]
        
    def __ne__(ss, obj):
        return None != obj

class bloc:

    def __init__(ss, var_import):
        make_id(ss)

        if not isinstance(var_import, list):
            var_import = []

        ss.__name__ = ''
        ss.__main__ = None
        ss.__defauts__ = {}

        ss.__vars__ = [
                        [], #Variable objets
                        var_import, #Variable local
                        [], #Variables global
                        [ss.__defauts__]
                    ]

    def __len__(ss):
        return len(ss.__dict__)

    def __str__(ss):
        return '<:bloc: %s>'%ss.__name__

    def __repr__(ss): 
        return '<:bloc: %s>'%ss.__name__

    def __getitem__(ss, key):
        return ss.__dict__[key]

    def __setitem__(ss, key, value):

        if key == "N#":
            ss.__name__ = value
        elif key == "D#":
            ss.__doc__ = value
        elif key == "B#":
            for key, value in value.items():
                ss.__defauts__[key] = value
        elif key == "M#":
            ss.__main__ = value
        elif key == "I#":
            for key, value in value.items():
                ss.__dict__[key] = value
        else:
            ss.__dict__[key] = value

    def __call__(ss, cle, ops, variables):
        main = ss.__main__
        if not main:
            return None

        func = ss.__dict__.get(main)
        if callable(func):
            return func(cle, ops, variables)
        else:
            return func

    def __iter__(ss):
        for item in ss.__dict__:
            yield item