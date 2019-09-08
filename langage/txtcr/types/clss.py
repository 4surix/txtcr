from ._base import *


def new_clss(var_import):

    class clss:

        def __init__(ss, var_import):
            make_id(ss)

            if not isinstance(var_import, list):
                var_import = []

            ss.__class__.__name__ = ''
            ss.__class__.__main__ = None
            ss.__class__.__vars__ = [
                                [], #Variable objets
                                var_import, #Variable local
                                [] #Variables global
                                ]
            ss.__class__.__defauts__ = {}

        def __len__(ss):
            return len(ss.__dict__)

        def __str__(ss):
            return '<:clss: %s>'%ss.__class__.__name__

        def __repr__(ss): 
            return '<:clss: %s>'%ss.__class__.__name__

        def __getitem__(ss, key):
            return ss.__dict__[key]

        def __setitem__(ss, key, value):

            if key == "N#":
                ss.__class__.__name__ = value
            elif key == "D#":
                ss.__class__.__doc__ = value
            elif key == "B#":
                ss.__class__.__defauts__ = value
            elif key == "M#":
                ss.__class__.__main__ = value
            elif key == "I#":
                for key, value in value.items():
                    ss.__dict__[key] = value
            else:
                ss.__dict__[key] = value

        def __call__(ss, cle, ops, variables):
            main = ss.__class__.__main__
            if not main:
                return None

            func = ss.__dict__.get(main)
            return func(cle, ops, variables)

        def __iter__(ss):
            for item in ss.__dict__:
                yield item

    return clss(var_import)