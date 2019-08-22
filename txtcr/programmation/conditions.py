# -*- coding: utf-8 -*-

import random

from .. import erreurs
from .fonc_type import *

#-----------------------------------------------------------------------------
#TYPE FONCTION
#-----------------------------------------------------------------------------

#Action ----------------------------------------------------------------------
def _set(TXTCRvars, TXTCRtmps, defauts, decode, value): 
	item, *value = value.split(' = ')
	if item and value:
		if item[0] in balises: item = decode(item)
		value = convert_variable(' = '.join(value), TXTCRvars, defauts, decode)
	else:
		raise erreurs.ParamError('>set>')

	is_modifier = False
	for Tvars in TXTCRvars:
		if item in Tvars:
			Tvars[item] = value
			is_modifier = True

	if not is_modifier:
		TXTCRvars[0][item] = value 

def _add(TXTCRvars, TXTCRtmps, defauts, decode, value):
	item, *value = value.split(' + ')
	if item and value:
		if item[0] in balises: item = decode(item)
		value = convert_variable(' + '.join(value), TXTCRvars, defauts, decode)
	else:
		raise erreurs.ParamError('>add>')

	def verif_existe():
		for Tvars in TXTCRvars:
			if item in Tvars: return
		resulta = recup_default(defauts).get(item)
		if resulta: TXTCRvars[0][item] = resulta
	verif_existe()

	for Tvars in TXTCRvars:
		if item in Tvars:
			if isinstance(Tvars[item], list):
				Tvars[item].append(value)
			elif isinstance(Tvars[item], (str, int, float)):
				Tvars[item] += value
			elif isinstance(Tvars[item], dict):
				key, value = value.split(' : ', 1)
				Tvars[item][key] = value
			elif isinstance(Tvars[item], tuple):
				Tvars[item] = Tvars[item] + (value,)

def _del(TXTCRvars, TXTCRtmps, defauts, decode, value):
	item, *value = value.split(' - ')
	
	if item:
		if item[0] in balises: item = decode(item)
	else:
		raise erreurs.ParamError('>del>')

	if value: 
		value = convert_variable(' - '.join(value), TXTCRvars, defauts, decode)
		for Tvars in TXTCRvars:
			if item in Tvars:
				if isinstance(Tvars[item], list):
					Tvars[item].remove(value)
				elif isinstance(Tvars[item], (int, float)):
					Tvars[item] -= value
				elif isinstance(Tvars[item], dict):
					del Tvars[item][value]
				elif isinstance(Tvars[item], tuple):
					Tvars[item] = Tvars[item] - (value,)
				elif isinstance(Tvars[item], str):
					Tvars[item].replace(value, '')
				break
	else:
		for Tvars in TXTCRvars:
			if item in Tvars:
				del Tvars[item]
				break

def _ped(TXTCRvars, TXTCRtmps, defauts, decode, value):
	item, *texte = value.split(' ? ')
	texte = decode(input(' ? '.join(texte)))
	if item:
		if item[0] in balises: item = decode(item)
		TXTCRvars[-1][item] = texte
	else:
		return texte

def _get(TXTCRvars, TXTCRtmps, defauts, decode, value):
	return convert_variable(value, TXTCRvars, defauts, decode)

def _aff(TXTCRvars, TXTCRtmps, defauts, decode, value):
	if value[0] == '"' and value[-1] == '"':
		value = value[1:-1]
	print(convert_variable(value, TXTCRvars, defauts, decode, exclues=balises+['#'], leve_erreur=False))

def _typ(TXTCRvars, TXTCRtmps, defauts, decode, value):
	*item, variable = value.split(' = ')
	if variable:
		variable = convert_variable(variable, TXTCRvars, defauts, decode)
	else:
		raise erreurs.ParamError('>typ>')

	type_value = gettype(variable)

	if not item:
		return type_value
	else:
		item = ' = '.join(item)
		if item[0] in balises: item = decode(item)
		TXTCRvars[0][item] = type_value

def _len(TXTCRvars, TXTCRtmps, defauts, decode, value):
	*item, variable = value.split(' = ')

	if variable:
		variable = convert_variable(variable, TXTCRvars, defauts, decode, exclues=balises)
	else:
		raise erreurs.ParamError('>len>')

	nbr_element = len(variable)

	if not item:
		return nbr_element
	else:
		item = ' = '.join(item)
		if item[0] in balises: item = decode(item)
		TXTCRvars[0][item] = nbr_element

def _ale(TXTCRvars, TXTCRtmps, defauts, decode, value):
	*item, nbrs = value.split(' = ')
	nbrs = [convert_variable(nbr.strip(), TXTCRvars, defauts, decode) for nbr in nbrs.split(',')]

	if len(nbrs) == 2:
		nbr_alea = random.randint(nbrs[0],nbrs[1])
	elif len(nbrs) == 3:
		nbr_alea = float(str(random.uniform(nbrs[0],nbrs[1]))[:nbrs[2]+2])
	else:
		raise erreurs.ParamError('>ale>')

	if not item:
		return nbr_alea
	else:
		item = ' = '.join(item)
		if item[0] in balises: item = decode(item)
		TXTCRvars[0][item] = nbr_alea

func_actions = {
	#Modification de variable
	'set': _set,
	'get': _get,
	#Intéraction avec l'utiisateur
	'aff': _aff,
	'ped': _ped,
	#Ajout/suppresion
	'add': _add,
	'del': _del,
	#Utilitaire
	'typ': _typ,
	'len': _len,
	'ale': _ale
}

def _verif_type(variable):
	if isinstance(variable, (int, float)) and not isinstance(variable, bool):
		if str(variable)[0] == '-':
			return 'negatif'
		return 'positif'
	return type(variable).__name__.replace('TXTCR', '')

def _type_in(var1, var2):
	variable = var1
	conteneur = var2
	nom_type = _verif_type(variable)
	for partie in conteneur:
		type_partie = _verif_type(partie)
		if nom_type == type_partie:
			return True
	return False

def _objet_in(var1, var2):
	variable = var1
	conteneur = var2
	for partie in conteneur:
		if variable is partie:
			return True
	return False

func_conditions = {
	'>': lambda var1, var2: var1 > var2,
	'=>': lambda var1, var2: var1 >= var2,
	'<': lambda var1, var2: var1 < var2,
	'<=': lambda var1, var2: var1 <= var2,
	'=': lambda var1, var2: _verif_type(var1) == _verif_type(var2),
	'==': lambda var1, var2:  var1 == var2,
	'===': lambda var1, var2: var1 is var2,
	'in': lambda var1, var2: _type_in(var1, var2),
	'inn': lambda var1, var2: var1 in var2,
	'innn': lambda var1, var2: _objet_in(var1, var2),
	'&': lambda var1, var2: var1 and var2,
	'&&': lambda var1, var2: (var1 and var2) == (var1 and var2),
	'|': lambda var1, var2: var1 or var2,
	'||': lambda var1, var2: (var1 or var2) != (var1 and var2),
}

#Condition + Action --------------------------------------------------------------------
class Condition:

	def __init__(ss, fonc, vars_tempo, variables, defauts, decode, acts_true, acts_false):
		ss.fonction = fonc
		ss.vars_tempo = vars_tempo
		ss.variables = variables
		ss.defauts = defauts
		ss.decode = decode
		ss.acts_true  = acts_true
		ss.acts_false = acts_false

	def config_condition(ss, texte):
		valeur_actuel = []
		condition_actuel = []

		def ajout_valeur(valeur):
			if valeur: condition_actuel.append(convert_variable(' '.join(valeur), ss.variables, ss.defauts, ss.decode))
		
		for partie in texte.split(' '):

			if partie.replace('!', '') in func_conditions:
				ajout_valeur(valeur_actuel)
				condition_actuel.append(partie)
				valeur_actuel = []
					
			elif partie or valeur_actuel: valeur_actuel.append(partie)

		ajout_valeur(valeur_actuel)
		return condition_actuel

	def decoupe_condition(ss, texte):
		liste_condition = []
		while 1:
			début, fin = recup_partie_parentese(texte)
			if fin:
				if début: liste_condition.extend(ss.config_condition(texte[:début]))
				liste_condition.append(ss.decoupe_condition(texte[début+1:fin]))
				texte = texte[fin+1:]
			else:
				liste_condition.extend(ss.config_condition(texte))
				break
		return liste_condition

	def get_values_and_symb(ss, liste):
		for nbr in range(0, len(liste)-1, 2):
			yield [nbr+2] + liste[nbr:nbr+3]

	def is_condition(ss, value):
		if isinstance(value, list) and len(value) >= 3 and value[1].replace('!', '') in func_conditions:
			return True

	def applique_condition(ss, liste_conditions):
		for place, value1, symb, value2 in ss.get_values_and_symb(liste_conditions):

			if ss.is_condition(value1):
				value1 = ss.applique_condition(value1)
			if ss.is_condition(value2):
				value2 = ss.applique_condition(value2)

			notnegation = True
			if symb[0] == '!': symb = symb[1:]; notnegation = False

			liste_conditions[place] = func_conditions.get(symb)(value1, value2) == notnegation

		return liste_conditions[-1]

	def analyse(ss):
		resultat = ss.applique_condition(ss.decoupe_condition(ss.fonction))

		if resultat == False and ss.acts_false:
			resultat = ss.action(ss.acts_false)

		elif resultat == True and ss.acts_true:
			resultat = ss.action(ss.acts_true)

		return resultat

	def action(ss, actions):
		retours = []

		def get_values_and_symb():
			for nbr in range(0, len(actions)-1, 2):
				yield actions[nbr:nbr+2]

		for nom_action, value in get_values_and_symb():
			func = func_actions.get(nom_action)
			if not func:
				raise Exception("L'action >%s> n'existe pas !"%nom_action)

			retour = func(value=value, TXTCRvars=ss.variables, TXTCRtmps=ss.vars_tempo, defauts=ss.defauts, decode=ss.decode)
			if retour != None:
				retours.append(retour)

		if not retours:
			return None
		elif len(retours) == 1:
			return retours[0]
		else:
			return tuple(retours)

#Fonction -------------------------------------------------------------
class DefCondition:

	def __init__(ss, vars_tempo, variables, defauts, decode):
		ss.vars_tempo = vars_tempo
		ss.variables = variables
		ss.defauts = defauts
		ss.decode = decode

	def decoupe_action(ss, texte):

		ifs = ['if1','if0']
		func_actions = []

		fin = 0
		mot = ''
		début = 0
		action = []
		actions = []
		in_texte = False
		echapement = False
		balise_fin = ''
		balises_texte = ["'", '"']

		for place, carac in enumerate(texte):

			if not in_texte and carac in balises_texte:
				in_texte = True
				balise_fin = carac

			elif not echapement and carac in [balise_fin] + [';']:
				in_texte = False

			elif carac in ['\\', '=']:
				echapement = True
				continue

			elif not echapement and not in_texte and carac == '>':

				mot = texte[début:place].strip()

				if mot in ifs:
					actions.append(action)
					action = []

				action.append(mot)
				début = place + 1

			echapement = False

		mot = texte[début:place].strip()
		if mot: action.append(mot)
		actions.append(action)

		return actions

	def recup_condition_acts(ss, actions):

		ifs = ['if0','if1']
		
		condition = None
		acts_false = None
		acts_true = None

		for action in ss.decoupe_action(actions):
			if action[0] not in ifs:
				condition = ' > '.join(action)
			elif action[0] == ifs[0]:
				acts_false = action[1:]
			elif action[0] == ifs[1]:
				acts_true = action[1:]

		#print(condition, acts_true, acts_false)

		return Condition(condition, ss.vars_tempo, ss.variables, ss.defauts, ss.decode, acts_true, acts_false)