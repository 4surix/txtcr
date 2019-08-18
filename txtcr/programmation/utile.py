# -*- coding: utf-8 -*-

import os
from .types import *

#Variable temporaire
def tmp(clss, values, *, silent=False):
	vals = clss.get('I')
	tmps = clss.__class__.__TXTCRtmps__

	if isinstance(values, dict):
		for item, value in values.item():
			if item not in tmps:
				if item not in vals:
					setattr(clss, item, value)
				tmps.append(item)
			elif not silent: raise Exception('%s est déjà une valeur temporaire !'%item)

	elif isinstance(values, list):
		for item in values:
			if item not in tmps:
				if item in vals:
					tmps.append(item)
				elif not silent: raise Exception("%s n'existe pas !"%item)
			elif not silent: raise Exception('%s est déjà une valeur temporaire !'%item)

def rmtmp(clss, cle, *, silent=False):
	tmps = clss.__class__.__TXTCRtmps__
	for item in cle:
		if item in tmps:
			tmps.remove(item)
		elif not silent: raise Exception("%s n'est pas une valeur temporaire !"%item)

#Type
class types:

	def calc(clss, **ops):
		item, value = tuple(ops.items())[0]
		clss[item] = types.TXTCRcalc(calcul,  
									clss.get('variables'),
									clss.get('defauts'),
									clss.__decode__)

	def cond(clss, **ops):
		item, value = tuple(ops.items())[0]
		clss[item] = types.TXTCRcond(value,  
									clss.get('variables'),
									clss.get('defauts'),
									clss.__decode__)

	def str(clss, **ops):
		item, value = tuple(ops.items())[0]
		TXTCRstr = types.TXTCRstr(value)
		TXTCRstr._variables = clss.get('variables')
		TXTCRstr._remplacement = clss.get('defauts')
		TXTCRstr._decode = clss.__decode__
		clss[item] = TXTCRstr

	def bool(clss, **ops):
		item, values = tuple(ops.items())[0]
		if not isinstance(values, tuple): values = (values,)
		clss[item] = types.TXTCRbool(*values)

#-------------------
def main(clss, **ops):
	main = clss.__class__.__TXTCRmain__
	if main:
		main = clss.get('I', key=main)

		if callable(main):
			variables = {k:v for k,v in ops.items() if type(k) == str}
			return main(**variables)
		else:
			return main
	else:
		return "<#M is not defined>"

#Modules -------------------------------------------
chemin_modules = os.getcwd() + '/txtcr/programmation/modules'
os.makedirs(chemin_modules, exist_ok=True)
def get_modules():
	return [m.split('.')[0] for m in os.listdir(chemin_modules)]
def get_data_module(module, sep):
	with open('%s/%s.txtcr'%(chemin_modules,module), encoding='utf-8') as m:
		data = m.read().split(sep, 1)[1]
	return data