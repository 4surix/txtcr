import os

balises_categories = ['N', 'D', 'B', 'M', 'I']

balises_types = ['<', '{', '[', '(', '"', "'", '+', '-', '1', '0', 'O', ':', '=', '/']

symbs_calcul = [
    '-',
    '+',
    '*',
    '/',
    '%',
    '^',
    'V'
]

def is_class(objet):
    if '__dict__' in dir(objet.__class__):
        if '__dict__' in objet.__class__.__dict__:
            return True

#Main-----------------------------------------------
params = [{}]

def main(obj, accept_not_callable=True):

    if callable(obj):
        return obj([], {}, params)
    elif accept_not_callable:
        return obj

def run(obj, *, accept_not_callable=True, ever_list=False):

    if not isinstance(obj, list):
        obj = [obj] 

    resultats = []
    for tcr in obj:
        resultat = main(tcr, accept_not_callable)
        if resultat is not None:
            resultats.append(resultat)

    if not resultats:
        return None
    elif len(resultats) == 1 and not ever_list:
        return resultats[0]
    else:
        return resultats

#Modules -------------------------------------------
chemin_modules = os.path.dirname(__file__) + "/modules"
#Création du dossier "modules" si n'existe pas
os.makedirs(chemin_modules, exist_ok=True)

def get_modules():
    return [m.split('.')[0] for m in os.listdir(chemin_modules)]

def get_data_module(module):
    try:
        fichier = '%s/%s.tcr'%(chemin_modules,module)
        with open(fichier, encoding='utf-8') as m:
            data = m.read()
        return data
    except FileNotFoundError:
        raise FileNotFoundError("Le modules \"%s\" n'existe pas !"%module)