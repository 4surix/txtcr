
py_str = str
py_bool = bool


balises_categories = ['N', 'D', 'S', 'R', 'C', 'T', 'I']

balises_types = ['<', '{', '[', '(', '"', "'", '+', '-', '1', '0', 'O', '/']

chiffres = list('0123456789')

caracs_str_simplifié = list('abcdefghijklmnopqrstuvwxyz0123456789_')


def is_class(objet):
    if '__dict__' in dir(objet.__class__):
        if '__dict__' in objet.__class__.__dict__:
            return True