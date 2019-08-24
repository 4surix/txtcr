# -*- coding: utf-8 -*-

import random

from .. import erreurs
from .fonc_type import *

#-----------------------------------------------------------------------------
#TYPE CONDITION
#-----------------------------------------------------------------------------

#Actions ----------------------------------------------------------------------

class FuncAction:

	def __init__(ss, TXTCRvars, TXTCRtmps, defauts, decode):
		ss.TXTCRvars = TXTCRvars
		ss.TXTCRtmps = TXTCRtmps
		ss.defauts = defauts
		ss.decode = decode
		ss.infos = dict(variables=TXTCRvars,
						defauts=defauts, 
						decode=decode)

	def act_set(ss, value): 
		item, value = ss.get_item_value(value, ' = ')

		if item and value:
			if item[0] in balises: item = ss.decode(item)
			value = convert_variable(value, **ss.infos)
		else:
			raise erreurs.ParamError('>set>')

		is_modifier = False
		for Tvars in ss.TXTCRvars:
			if item in Tvars:
				Tvars[item] = value
				is_modifier = True

		if not is_modifier:
			ss.TXTCRvars[0][item] = value 

	def act_add(ss, value):
		item, value = ss.get_item_value(value, ' + ')

		if item and value:
			if item[0] in balises: item = ss.decode(item)
			value = convert_variable(value, **ss.infos)
		else:
			raise erreurs.ParamError('>add>')

		def verif_existe():
			for Tvars in ss.TXTCRvars:
				if item in Tvars: return
			resulta = recup_default(ss.defauts).get(item)
			if resulta: 
				ss.TXTCRvars[0][item] = resulta
			else:
				raise erreurs.VariableError(item)
		verif_existe()

		for Tvars in ss.TXTCRvars:
			if item in Tvars:
				if isinstance(Tvars[item], list):
					Tvars[item].append(value)
				elif isinstance(Tvars[item], (str, int, float)):
					Tvars[item] += value
				elif isinstance(Tvars[item], dict):
					key, value = value.split(':', 1)
					Tvars[item][key.strip()] = value.strip()
				elif isinstance(Tvars[item], tuple):
					Tvars[item] = Tvars[item] + (value,)

	def act_del(ss, value):
		item, value = ss.get_item_value(value, ' - ')

		if not item:
			item = value
			value = None
		
		if item:
			if item[0] in balises: item = ss.decode(item)
		else:
			raise erreurs.ParamError('>del>')

		if value: 
			value = convert_variable(value, **ss.infos)
			for Tvars in ss.TXTCRvars:
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
			for Tvars in ss.TXTCRvars:
				if item in Tvars:
					del Tvars[item]
					break

	def act_ped(ss, value):
		item, texte = ss.get_item_value(value, ' ? ')
		return ss.sauv_or_retourne(item, ss.decode(input(texte)))

	def act_get(ss, value):
		return convert_variable(value, **ss.infos)

	def act_aff(ss, value):
		if value[0] == '"' and value[-1] == '"':
			value = value[1:-1]
		print(convert_variable(value, exclues=balises+['#'], leve_erreur=False, **ss.infos))

	def act_typ(ss, value):
		item, variable = ss.get_item_value(value, ' = ')

		if variable:
			variable = convert_variable(variable, **ss.infos)
		else:
			raise erreurs.ParamError('>typ>')

		return ss.sauv_or_retourne(item, gettype(variable))

	def act_len(ss, value):
		item, variable = ss.get_item_value(value, ' = ')

		if variable:
			variable = convert_variable(variable, exclues=balises, **ss.infos)
		else:
			raise erreurs.ParamError('>len>')

		return ss.sauv_or_retourne(item, len(variable))

	def act_sum(ss, value):
		item, variable = ss.get_item_value(value, ' = ')

		if variable:
			variable = convert_variable(variable, **ss.infos)
		else:
			raise erreurs.ParamError('>sum>')

		def meme_type():
			Ttype = gettype(variable[0])
			for element in variable:
				if gettype(element) != Ttype:
					return False
			return True

		elements_add = None
		if meme_type():
			if isinstance(variable[0], list):
				elements_add = []
				for element in variable:
					elements_add.extend(element)
			elif isinstance(variable[0], str):
				elements_add = ''
				for element in variable:
					elements_add += element
			elif isinstance(variable[0], (int, float)) and not isinstance(variable[0], bool):
				elements_add = 0
				for element in variable:
					elements_add += element
		else:
			raise Exception('Les élément de la variable dans >sum> ne sont pas identique')

		return ss.sauv_or_retourne(item, elements_add)

	def act_ale(ss, value):
		item, nbrs = ss.get_item_value(value, ' = ')
		nbrs = [convert_variable(nbr.strip(), **ss.infos) for nbr in nbrs.split(',')]

		if len(nbrs) == 2:
			nbr_alea = random.randint(nbrs[0],nbrs[1])
		elif len(nbrs) == 3:
			nbr_alea = float(str(random.uniform(nbrs[0],nbrs[1]))[:nbrs[2]+2])
		else:
			raise erreurs.ParamError('>ale>')

		return ss.sauv_or_retourne(item, nbr_alea)

	#Utile ------------------------------

	def get_item_value(ss, value, symb):
		params = value.split(symb, 1)
		if len(params) == 1:
			return '', params[0]
		else:
			return params[0], params[1]

	def sauv_or_retourne(ss, item, value):
		if not item:
			return value
		else:
			if item[0] in balises: item = ss.decode(item)
			ss.TXTCRvars[0][item] = value

# Comparaisons -------------------------------------------------------------------

def _type_in(var1, var2):
	variable = var1
	conteneur = var2
	nom_type = gettype(variable)
	for partie in conteneur:
		type_partie = gettype(partie)
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

def _meme_type(var1, var2):
	Ttype = gettype(var1)
	for element in var2:
		if gettype(element) != Ttype:
			return False
	return True

func_conditions = {
	'>': lambda var1, var2: var1 > var2,
	'=>': lambda var1, var2: var1 >= var2,
	'<': lambda var1, var2: var1 < var2,
	'<=': lambda var1, var2: var1 <= var2,
	'=': lambda var1, var2: gettype(var1) == gettype(var2),
	'==': lambda var1, var2:  var1 == var2,
	'===': lambda var1, var2: var1 is var2,
	'in': lambda var1, var2: _type_in(var1, var2),
	'inn': lambda var1, var2: var1 in var2,
	'innn': lambda var1, var2: _objet_in(var1, var2),
	'innnn': lambda var1, var2: _meme_type(var1, var2),
	'&': lambda var1, var2: var1 and var2,
	'&&': lambda var1, var2: (var1 and var2) == (var1 and var2),
	'|': lambda var1, var2: var1 or var2,
	'||': lambda var1, var2: (var1 or var2) != (var1 and var2),
}

#Condition --------------------------------------------------------------------

class Condition:

	def __init__(ss, fonc, vars_tempo, variables, defauts, decode, acts_true, acts_false):
		ss.fonction = fonc
		ss.vars_tempo = vars_tempo
		ss.variables = variables
		ss.defauts = defauts
		ss.decode = decode
		ss.acts_true  = acts_true
		ss.acts_false = acts_false
		ss.func_actions = FuncAction(TXTCRvars=ss.variables, TXTCRtmps=ss.vars_tempo, defauts=ss.defauts, decode=ss.decode)

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
		if isinstance(value, list) and len(value) >= 3 and isinstance(value[1], str) and value[1].replace('!', '') in func_conditions:
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
			try:
				func = getattr(ss.func_actions, 'act_'+nom_action)
			except AttributeError:
				raise Exception("L'action >%s> n'existe pas !"%nom_action)

			retour = func(value)
			if retour != None:
				retours.append(retour)

		if not retours:
			return None
		elif len(retours) == 1:
			return retours[0]
		else:
			return tuple(retours)

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