from .clss import *

#Raccourcie -------------------------------------------------

class rac_cond:

    def __init__(ss, nom, clss):
        ss.nom_fonc = recup_redirection(nom)
        ss.params = []
        ss.clss = clss

    def __call__(ss, cle, ops, variables):
        return recup_redirection(ss,ss.clss.__class__.__vars__, 
                                    ss.clss.__class__.__defauts__, 
                                    ss.clss.__class__.__decode__)

    def __iter__(ss):
        yield None

    def append(ss, item):
        ss.params = item

class rac_clss:

    def __init__(ss, clss):
        ss.module = ''
        ss.clss = clss

    def __iter__(ss):
        yield None

    def append(ss, item):
        ss.module = item.params[0]

class rac_redirection:

    def __init__(ss, clss):
        ss.params = []
        ss.clss = clss

    def __call__(ss, cle, ops, variables):
        return recup_redirection(ss,ss.clss.__class__.__vars__, 
                                    ss.clss.__class__.__defauts__, 
                                    ss.clss.__class__.__decode__)

    def __iter__(ss):
        yield None
        
    def __len__(ss):
        return len(ss.params)

    def append(ss, item):
        ss.params.append(item)