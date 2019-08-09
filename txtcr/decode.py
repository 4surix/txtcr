from .utile import *
from .types import *
from . import erreurs

def separer(texte):

	d = 0
	sep = ''
	symb = ''
	asymb = ''
	liste = []
	in_texte = False
	meme_type = False
	echapement = False
	symb_croiser = 0
	enregistrement = 0

	types_textuel = ['"', "'"]

	for nbr, carac in enumerate(texte+'-'):

		if enregistrement:
			if carac == " ":
				continue
			partie = texte[d:enregistrement]
			if partie:
				liste.append(partie)
			d = nbr
			symb = ''
			meme_type = False
			enregistrement = 0

		if sep in types_textuel:
			if carac == '|':
				meme_type = sep[0]
				continue
			else: 
				in_texte = True
			sep = ''

		if carac == "\\":
			echapement = True
			continue

		elif not in_texte and carac in types_textuel:
			sep = carac
			continue

		elif not symb and carac in '{[(':
			symb = carac
			asymb = {'{':'}','[':']','(':')'}.get(symb)

		elif not echapement and carac == ';':
			if in_texte:
				in_texte = False
			if not symb_croiser:
				enregistrement = nbr
				continue

		elif not echapement and carac == ':' and in_texte:
			in_texte = False
			continue

		echapement = False

		if in_texte:
			continue

		if carac == symb:
			symb_croiser += 1
		elif carac == asymb:
			symb_croiser -= 1

	liste.append(texte[d:nbr])
	
	return liste

def separer_dict_format2(texte, _):

	liste = []
	echapement = False
	enregistrement = False

	for nbr, carac in enumerate(texte):

		if enregistrement:
			if carac == " ":
				continue
			liste.append(texte[nbr:])
			break

		if carac == "\\":
			echapement = True
			continue

		if not echapement and carac == ':':
			enregistrement = True
			liste.append(texte[0:nbr])

		echapement = False

	return liste

def separer_dict_format1(texte, sep):
	return texte.split(sep)

class Decode:

	def __init__(ss, isformat2, variables, remplacement):
		ss.isformat2 = isformat2
		ss.variables = variables
		ss.remplacement = remplacement

	def __call__(ss, *cle):
		return ss.decoder(*cle)

	def decoder(ss, texte, profondeur=-1):

		profondeur += 1

		if not ss.isformat2:
			virg = ';%s' % profondeur
		else:
			virg = ';'

		balise = texte[0]
		texte = texte[1:]

		if balise == "{":
			valeur_decoder = {}

			if ss.isformat2:
				sep_key_value = ':'
				values = separer(texte[:-1])
				balise_value = balise_key = ''
				separer_dict = separer_dict_format2
			else:
				_, balise_key, text = is_meme_balise(':', texte, virg)
				virg, balise_value, text = is_meme_balise('|', text, virg)
				sep_key_value = ":%s" % (' ' if virg == '; ' else profondeur)
				values = text.split(virg)
				separer_dict = separer_dict_format1

			for value in values:
				if not value: continue

				ops = separer_dict(value, sep_key_value)
				if len(ops) != 2: raise erreurs.SeparationError(texte, balise, ops, profondeur)
				valeur_decoder[ss.decoder(balise_key+ops[0], profondeur)] = ss.decoder(balise_value+ops[1], profondeur)

		elif balise == "[":
			virg, balise, texte = is_meme_balise('|', texte, virg)

			if ss.isformat2:
				values = separer(texte[:-1])
			else:
				values = texte.split(virg)

			valeur_decoder = [ss.decoder(balise+v, profondeur) for v in values if v]

		elif balise == "(":
			virg, balise, texte = is_meme_balise('|', texte, virg)

			if ss.isformat2:
				values = separer(texte[:-1])
			else:
				values = texte.split(virg)

			valeur_decoder = tuple([ss.decoder(balise+v, profondeur) for v in values if v])

		elif balise == '"':
			valeur_decoder = verif_contenue(texte, ss.variables, ss.remplacement, decode=True, isformat2=ss.isformat2)
			if valeur_decoder.count('#') >= 2:
				valeur_decoder = TXTCRstr(texte)
				valeur_decoder._variables = ss.variables
				valeur_decoder._remplacement = ss.remplacement

		elif balise == "'":
			valeur_decoder = texte.encode()

		elif balise == "0":
			valeur_decoder = TXTCRbool(False, texte)

		elif balise == "1":
			valeur_decoder = TXTCRbool(True, texte)

		elif balise == '>':
			valeur_decoder = TXTCRcond(texte, ss.variables, ss.remplacement, ss.decoder)

		elif balise == '#':
			data = texte[3:]
			if ss.isformat2:
				data = verif_contenue(data, decode=True, isformat2=ss.isformat2)
			valeur_decoder = ss.convert(data, profondeur, variables=ss.variables, remplacement=ss.remplacement)

		elif balise == '=':
			valeur_decoder = TXTCRcalc(texte, ss.variables, ss.remplacement)

		elif balise in ['+','-']:
			texte = balise+texte
			if ',' in texte: 
				texte = texte.replace(',', '.')
				valeur_decoder = float(texte)
			elif '.' in texte: 
				valeur_decoder = float(texte)
			else: valeur_decoder = int(texte)
					
		elif balise.lower() in ["o", "ø"]:
			valeur_decoder = None

		else: raise erreurs.BaliseError(texte, balise, profondeur)

		return valeur_decoder