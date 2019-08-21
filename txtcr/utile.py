# -*- coding: utf-8 -*-

def Func():pass
func = type(Func)
class Clss:pass
clss = type(Clss)

balises =  ['{',
			'[',
			'(',
			'"',
			"'",
			'+',
			'-',
			'O',
			'0',
			'1',
			':',
			'=',
			'<']

balises_en_tete =  {'N#':'name',
					'D#':'desc',
					'M#':'main',
					'R#':'repr',
					'B#':'base',
					'T#':'date',
					'E#':'encd',
					'H#':'hash',
					'I#':'info'}


seps 	=  [(':', ':\ '[:-1]),
			(';', ';\ '[:-1])]

expregu =  [('\t', '\/t'),
			('\n', '\/n'),
			('\v', '\/v'),
			('\f', '\/f'),
			('\b', '\/b'),
			('\r', '\/r'),
			('\s', '\/s')]

seps2 	 = [(':', '\\:'),
			(';', '\\;')]

expregu2 = [('\t', '\\t'),
			('\n', '\\n'),
			('\v', '\\v'),
			('\f', '\\f'),
			('\b', '\\b'),
			('\r', '\\r'),
			('\s', '\\s')]

#Type ---------------------------------------------
def gettype(variable):
	if isinstance(variable, (int, float)) and not isinstance(variable, bool):
		if str(variable)[0] == '-':
			return 'neg'
		return 'pos'
	return type(variable).__name__.replace('TXTCR', '')

def istype(types, variable=None, *, vtype=None):
	if not vtype: vtype = gettype(variable)
	if vtype in types:
		return True
	return False

def isuniforme(valeurs):
	bt = None
	meme_type = True

	for valeur in valeurs:
		vtype = gettype(valeur)

		if vtype == 'str':
			balise = '"'
		elif vtype == 'bytes':
			balise = "'"
		elif vtype == 'bool':
			if valeur == False:
				balise = "0"
			elif valeur == True:
				balise = '1'
		elif vtype == 'neg':
			balise = '-'
		elif vtype == 'pos':
			balise = '+'
		else:
			return None

		if not bt: bt = balise
		elif bt != balise: meme_type = False

	return (bt if meme_type else ';')

def is_meme_balise(sep, texte, virg):
	symb = ''

	if sep in texte:
		param = texte.split(sep)[0]

		if param == ';':
			virg = '; '
			texte = texte[2:]
		elif param in ['0','1','"',"'",'+','-']: 
			symb = param
			virg = '; '
			texte = texte[2:]
		elif param == '':
			texte = texte[2:]

	return virg, symb, texte

def is_class(valeur):

	if '__dict__' in dir(valeur.__class__):
		if '__module__' in valeur.__class__.__dict__:
			return True

def verif_contenue(texte, *, decode=False, addsep=True, isformat2=True):

	texte = str(texte)

	if isformat2:
		verifs = expregu2 + (seps2 if addsep else [])
	else:
		verifs = expregu + (seps if addsep else [])

	for param, remplacement in verifs:
		if decode and remplacement in texte: texte = texte.replace(remplacement, param)
		elif not decode and param in texte: texte = texte.replace(param, remplacement)

	return texte