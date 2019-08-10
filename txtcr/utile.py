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
			'+-',
			'oø',
			'0',
			'1',
			'>',
			'#']

balises_en_tete =  {'N#':'name',
					'D#':'desc',
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

seps2 	 = [(':', '\: '[:-1]),
			(';', '\; '[:-1])]

expregu2 = [('\t', '\\t'),
			('\n', '\\n'),
			('\v', '\\v'),
			('\f', '\\f'),
			('\b', '\\b'),
			('\r', '\\r'),
			('\s', '\\s')]

def istype(ttype, valeur=None, *, vtype=False):
	if not vtype: vtype = type(valeur).__name__

	if vtype in ttype:
		return True

def isuniforme(valeurs):
	bt = None
	meme_type = True

	for i in valeurs:
		t = type(i).__name__.replace('TXTCR', '')

		if t == 'str':
			t = '"'
		elif t == 'bytes':
			t = "'"
		elif t == 'bool':
			if i == False:
				t = "0"
			elif i == True:
				t = '1'
		elif t in ['int','float']:
			if '-' == str(i)[0]:
				t = '-'
			else:
				t = '+'
		else:
			return None

		if not bt: bt = t
		elif bt != t: meme_type = False

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