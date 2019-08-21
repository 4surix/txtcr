# -*- coding: utf-8 -*-

from .utile import *
from . import erreurs

class Encode:

	def __init__(ss, isformat2, isindent=False):
		ss.isindent = isindent
		ss.isformat2 = isformat2

	def __call__(ss, *cle):
		return ss.encode(*cle)

	def encode(ss, valeur, profondeur=-1, getsymb=0):

		profondeur += 1

		def balises_virg_obligatoire(values, param): 
			return values and (isinstance(values[-1], (str, bytes)) or param in ['"', "'"])

		if ss.isindent: 
			indentation = '\n'+'\t'*profondeur
		else: 
			indentation = ''

		if ss.isformat2:
			virg = ';'
		else:
			virg = ';%s'%profondeur

		vtype = type(valeur).__name__

		if 'dict' == vtype:

			keys = list(valeur.keys())
			values = list(valeur.values())

			if ss.isformat2:
				sep_key_value = ('\t' if ss.isindent else '')+':'
				param_key = param_value = False
			else:
				param_key   = isuniforme(keys)
				param_value = isuniforme(values)
				sep_key_value = '%s:%s'%('\t' if ss.isindent else '', ' ' if param_value else profondeur)
				if param_value: virg = '; '

			simplification = ''

			key_getbalise = 0
			if param_key and param_key != ";": 
				simplification += '%s:'%param_key
				key_getbalise = 1

			value_getbalise = 0
			if param_value and (param_value != ';' or not ss.isformat2):
				simplification += '%s|'%param_value
				if param_value != ';': value_getbalise = 1

			keys_encode   = [ss.encode(key, profondeur, key_getbalise) for key in keys]
			values_encode = [ss.encode(value, profondeur, value_getbalise) for value in values]
			keys_values = [''.join([keys_encode[nbr], sep_key_value, values_encode[nbr]]) for nbr in range(len(keys))]

			fin = ''
			if ss.isformat2:
				if balises_virg_obligatoire(values, param_value):
					fin = ';'
				fin = '%s%s}'%(fin,indentation)

			texte = '{%s%s%s'%(simplification,
							virg.join(keys_values),
							fin)
			
		elif 'list' == vtype:
			param = isuniforme(valeur)
			getsymb = (1 if param and param != ';' else 0)

			values_encode = [ss.encode(value, profondeur, getsymb) for value in valeur]

			simplification = ''
			if param:
				if param != ';' or not ss.isformat2: simplification = '%s|'%param 
				if not ss.isformat2: virg = '; '

			fin = ''
			if ss.isformat2:
				if balises_virg_obligatoire(valeur, param):
					fin = ';'
				fin = '%s%s]'%(fin,indentation)

			texte = '[%s%s%s'%(simplification,
							virg.join(values_encode),
							fin)


		elif 'tuple' == vtype:
			param = isuniforme(valeur)
			getsymb = (1 if param and param != ';' else 0)

			values = [ss.encode(value, profondeur, getsymb) for value in valeur]

			simplification = ''
			if param:
				if param != ';' or not ss.isformat2: simplification = '%s|'%param 
				if not ss.isformat2: virg = '; '

			fin = ''
			if ss.isformat2:
				if balises_virg_obligatoire(valeur, param):
					fin = ';'
				fin = '%s%s)'%(fin,indentation)

			texte = '(%s%s%s'%(simplification,
							virg.join(values),
							fin)


		elif 'str' == vtype:
			texte = '"%s'[getsymb:] % verif_contenue(valeur, isformat2=ss.isformat2)

		elif 'bytes' == vtype:
			texte = "'%s"[getsymb:] % valeur.decode()

		elif vtype in ('int','float'):
			texte = ('%s'%valeur if str(valeur)[0] == '-' else '+%s'%valeur)[getsymb:]

		elif 'NoneType' == vtype:
			texte = 'O%s'[getsymb:] % valeur

		elif 'bool' == vtype:
			if valeur == False:
				texte = '0%s'[getsymb:] % valeur
			elif valeur == True:
				texte = '1%s'[getsymb:] % valeur

		elif 'TXTCRcalc' == vtype:
			texte = '=%s'% verif_contenue(valeur.calcul, isformat2=ss.isformat2)

		elif 'TXTCRstr' == vtype:
			texte = '"%s'[getsymb:]%valeur.text

		elif 'TXTCRcond' == vtype:
			texte = ':%s' % verif_contenue(valeur.condition, isformat2=ss.isformat2, addsep=False)

		elif 'TXTCRbool' == vtype:
			texte = '%s%s'%(1 if valeur.status else 0, valeur.commentaire)

		elif is_class(valeur) and '__TXTCRvars__' in valeur.__class__.__dict__:
			data = ss.convert(valeur, profondeur=profondeur)
			texte = '<%s>' % data[3:]

		else:
			raise erreurs.TypeInconnue(type(valeur),profondeur,valeur)

		if profondeur == 1:
			return (texte if len(texte) > 2 else None)
		return indentation + texte