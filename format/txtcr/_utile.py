
balises_categories = ['N', 'D', 'S', 'R', 'I']

balises_types = ['<', '{', '[', '(', '"', "'", '+', '-', '1', '0', 'O', '/']

def is_class(objet):
    if '__dict__' in dir(objet.__class__):
        if '__dict__' in objet.__class__.__dict__:
            return True