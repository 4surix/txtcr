# -*- coding: utf-8 -*-

from .utile import *
from .types import *
from . import erreurs

def separer(texte):

	symb = ''
	asymb = ''
	début = 0
	balise = ''
	valeurs = []
	in_cond = False
	in_texte = False
	in_txtcr = False
	in_parent = False
	meme_type = False
	echapement = False
	symb_croiser = 0
	enregistrement = 0

	types_textuel = ['"', "'", '=']

	for nbr, carac in enumerate(texte+'-'):

		#print(carac, in_texte, in_cond, in_txtcr, symb_croiser)

		if enregistrement:
			if carac == " ":
				continue
			partie = texte[début:enregistrement]
			if partie:
				valeurs.append(partie)
			début = nbr
			symb = ''
			meme_type = False
			enregistrement = 0

		if balise in types_textuel:
			if carac == '|':
				meme_type = balise
				continue
			else: 
				in_texte = True
			balise = ''

		if carac == "\\":
			echapement = True
			continue

		elif carac == '<' and not in_texte and not in_cond:
			in_txtcr = True
			continue

		elif carac == '>' and not in_texte and not in_cond:
			in_txtcr = False
			continue

		elif not in_texte and carac in types_textuel:
			balise = carac
			continue

		elif carac in '{[(' and not in_texte and not in_cond and not symb:
			symb = carac
			asymb = {'{':'}','[':']','(':')'}.get(symb)

		elif carac == ';' and not echapement:
			if in_texte:
				in_texte = False
			if not symb_croiser and not in_cond and not in_txtcr:
				enregistrement = nbr
				continue

		elif not echapement and carac == ':':
			if in_texte: 
				in_texte = False
			if in_cond:
				if not in_parent: 
					in_cond = False
			elif balise == ':':
				in_cond = True
				balise = ''
			else:
				balise = ':'
			continue

		echapement = False

		if in_texte:
			continue

		if carac == symb:
			symb_croiser += 1
		elif carac == asymb:
			symb_croiser -= 1

	valeurs.append(texte[début:nbr])

	return valeurs

def separer_dict_format2(texte, _):

	key_value = []
	echapement = False
	enregistrement = False

	for nbr, carac in enumerate(texte):

		if enregistrement:
			key_value.append(texte[nbr:].strip())
			break

		if carac == "\\":
			echapement = True
			continue

		if not echapement and carac == ':':
			enregistrement = True
			key_value.append(texte[0:nbr].strip())

		echapement = False

	return key_value

def separer_dict_format1(texte, sep):
	return texte.split(sep)

class Decode:

	def __init__(ss, isformat2, variables, defauts):
		ss.isformat2 = isformat2
		ss.variables = variables
		ss.defauts = defauts

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
			valeur_decodée = {}

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
				if not value or value[0] == '/': continue

				ops = separer_dict(value, sep_key_value)
				if len(ops) != 2: raise erreurs.SeparationError(texte, balise, ops, profondeur)
				valeur_decodée[ss.decoder(balise_key+ops[0], profondeur)] = ss.decoder(balise_value+ops[1], profondeur)

		elif balise == "[":
			virg, balise, texte = is_meme_balise('|', texte, virg)

			if ss.isformat2:
				values = separer(texte[:-1])
			else:
				values = texte.split(virg)

			valeur_decodée = [ss.decoder(balise+v, profondeur) for v in values if v]

		elif balise == "(":
			virg, balise, texte = is_meme_balise('|', texte, virg)

			if ss.isformat2:
				values = separer(texte[:-1])
			else:
				values = texte.split(virg)

			valeur_decodée = tuple([ss.decoder(balise+v, profondeur) for v in values if v])

		elif balise == '"':
			if len(texte) >= 2 and texte[-2] != '\\' and texte[-1] in ['"',';'] : texte = texte[:-1]
			valeur_decodée = verif_contenue(texte, decode=True, isformat2=ss.isformat2)

			if valeur_decodée.count('#') >= 2:
				valeur_decodée = TXTCRstr(valeur_decodée)
				valeur_decodée._clss = ss.clss
				valeur_decodée._decode = ss.decoder

		elif balise == "'":
			if len(texte) >= 2 and texte[-2] != '\\' and texte[-1] in ['"',';'] : texte = texte[:-1]
			valeur_decodée = texte.encode()

		elif balise == "O":
			valeur_decodée = None
			
		elif balise == "0":
			valeur_decodée = TXTCRbool(False, texte)

		elif balise == "1":
			valeur_decodée = TXTCRbool(True, texte)

		elif balise == ':':
			valeur_decodée = TXTCRcond(verif_contenue(texte, decode=True, addsep=False, isformat2=ss.isformat2), ss.clss, ss.decoder)

		elif balise == '=':
			if len(texte) >= 2 and texte[-2] != '\\' and texte[-1] == ';': texte = texte[:-1]
			valeur_decodée = TXTCRcalc(verif_contenue(texte, decode=True, isformat2=ss.isformat2), ss.clss, ss.decoder)

		elif balise == '<':
			data = texte[:-1]
			if ss.isformat2:
				data = verif_contenue(data, decode=True, isformat2=ss.isformat2)
				
			ancien_clss = ss.clss
			valeur_decodée = ss.convert(data, profondeur)
			ss.clss = ancien_clss

		elif balise in ['+','-']:
			texte = balise+texte
			if ',' in texte: valeur_decodée = float(texte.replace(',', '.'))
			elif '.' in texte: valeur_decodée = float(texte)
			else: valeur_decodée = int(texte)

		else: raise erreurs.BaliseError(texte, balise, profondeur)

		return valeur_decodée