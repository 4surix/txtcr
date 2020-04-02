py_str = str
py_bool = bool


balises_categories = ['N', 'D', 'S', 'R', 'C', 'T', 'I']

balises_types = ['<', '{', '[', '(', '"', "'", '+', '-', '1', '0', 'O', '/']

chiffres = list('0123456789')

chars_to_str = list('abcdefghijklmnopqrstuvwxyz0123456789_')


def is_class(obj):
    if '__dict__' in dir(obj.__class__) and '__dict__' in obj.__class__.__dict__:
        return True
