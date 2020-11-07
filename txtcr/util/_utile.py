# coding: utf-8
# Python 3.6.2
# ----------------------------------------------------------------------------

py_str = str
py_bool = bool


balises_categories = ['N', 'D', 'S', 'R', 'C', 'T', 'L', 'I']

balises_ouvrantes = ['<', '{', '[', '(', '"', "'", '+', '-', '/']

balises_fermentes = ['>', '}', ']', ')']

balises_separations = ['#', '=', ',', ':']

chiffres = list('0123456789')

balises = (
    balises_ouvrantes
    + balises_fermentes
    + balises_separations
)


def is_class(obj):
    if '__dict__' in dir(obj.__class__) and '__dict__' in obj.__class__.__dict__:
        return True
