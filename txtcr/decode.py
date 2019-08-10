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

		elif not in_texte and carac in types_textuel:
			balise = carac
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

	valeurs.append(texte[début:nbr])
	
	return valeurs

def separer_dict_format2(texte, _):

	key_value = []
	echapement = False
	enregistrement = False

	for nbr, carac in enumerate(texte):

		if enregistrement:
			if carac == " ":
				continue
			key_value.append(texte[nbr:])
			break

		if carac == "\\":
			echapement = True
			continue

		if not echapement and carac == ':':
			enregistrement = True
			key_value.append(texte[0:nbr])

		echapement = False

	return key_value

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
				if not value: continue

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
			valeur_decodée = verif_contenue(texte, decode=True, isformat2=ss.isformat2)
			if valeur_decodée.count('#') >= 2:
				valeur_decodée = TXTCRstr(texte)
				valeur_decodée._variables = ss.variables
				valeur_decodée._remplacement = ss.remplacement

		elif balise == "'":
			valeur_decodée = texte.encode()

		elif balise == "0":
			valeur_decodée = TXTCRbool(False, texte)

		elif balise == "1":
			valeur_decodée = TXTCRbool(True, texte)

		elif balise == '>':
			valeur_decodée = TXTCRcond(texte, ss.variables, ss.remplacement, ss.decoder)

		elif balise == '#':
			data = texte[3:]
			if ss.isformat2:
				data = verif_contenue(data, decode=True, isformat2=ss.isformat2)
			valeur_decodée = ss.convert(data, profondeur, variables=ss.variables, remplacement=ss.remplacement)

		elif balise == '=':
			valeur_decodée = TXTCRcalc(texte, ss.variables, ss.remplacement)

		elif balise in ['+','-']:
			texte = balise+texte
			if ',' in texte: valeur_decodée = float(texte.replace(',', '.'))
			elif '.' in texte: valeur_decodée = float(texte)
			else: valeur_decodée = int(texte)
					
		elif balise.lower() in ["o", "ø"]:
			valeur_decodée = None

		else: raise erreurs.BaliseError(texte, balise, profondeur)

		return valeur_decodée