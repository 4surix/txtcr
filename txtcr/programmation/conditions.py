# -*- coding: utf-8 -*-

from .fonc_type import *

#-----------------------------------------------------------------------------
#TYPE FONCTION
#-----------------------------------------------------------------------------

#Action ----------------------------------------------------------------------
def _set(TXTCRvars, TXTCRtmps, defauts, decode, value): 
	item, *value = value.split(' = ')
	item = convert_variable(item, TXTCRvars, defauts, decode, convert_redirection=False)
	if value:
		value = convert_variable(' = '.join(value), TXTCRvars, defauts, decode)

		is_modifier = False
		for Tvars in TXTCRvars:
			if item in Tvars:
				Tvars[item] = value
				is_modifier = True

		if not is_modifier:
			TXTCRvars[-1][item] = value 

def _add(TXTCRvars, TXTCRtmps, defauts, decode, value):
	item, *value = value.split(' + ')
	if item[0] in balises: item = decode(item)

	def verif_existe():
		for Tvars in TXTCRvars:
			if item in Tvars: return
		resulta = recup_default(defauts).get(item)
		if resulta: TXTCRvars[-1][item] = resulta
	verif_existe()

	if value:
		value = convert_variable(' + '.join(value), TXTCRvars, defauts, decode)
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
	item = convert_variable(item, TXTCRvars, defauts, decode, convert_redirection=False)
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
	else:
		for Tvars in TXTCRvars:
			if item in Tvars:
				del Tvars[item]

def _ped(TXTCRvars, TXTCRtmps, defauts, decode, value):
	item, *texte = value.split(' ? ')
	texte = input(' ? '.join(texte))
	item = convert_variable(item, TXTCRvars, defauts, decode, convert_redirection=False)
	TXTCRvars[-1][item] = decode(texte)

def _get(TXTCRvars, TXTCRtmps, defauts, decode, value):
	return convert_variable(value, TXTCRvars, defauts, decode)

def _aff(TXTCRvars, TXTCRtmps, defauts, decode, value):
	if value[0] == '"' and value[-1] == '"':
		value = value[1:-1]
	print(replace_variables(value, TXTCRvars, defauts, decode))

def _typ(TXTCRvars, TXTCRtmps, defauts, decode, value):
	*item, variable = value.split(' = ')
	variable = convert_variable(variable, TXTCRvars, defauts, decode)
	vtype = gettype(variable)
	if not item:
		return vtype
	else:
		TXTCRvars[-1][decode(' = '.join(item))] = vtype

func_actions = {
	#Modification de variable
	'set': lambda **ops: _set(**ops),
	'get': lambda **ops: _get(**ops),
	#Intéraction avec l'utiisateur
	'aff': lambda **ops: _aff(**ops),
	'ped': lambda **ops: _ped(**ops),
	#Ajout/suppresion
	'add': lambda **ops: _add(**ops),
	'del': lambda **ops: _del(**ops),
	#Utilisataire
	'typ': lambda **ops: _typ(**ops)
}

def _len_comparaison(var1, symb, var2):

	if isinstance(var1, (int, float)):
		if isinstance(var2, (str, bytes, tuple, list, dict)):
			return eval('%s %s %s'%(var1, symb, len(var2)))
	if isinstance(var1, (str, bytes, tuple, list, dict)):
		if isinstance(var2, (int, float)):
			return eval('%s %s %s'%(len(var1), symb, var2))

	if symb == '>': return var1 > var2
	if symb == '>=': return var1 >= var2
	if symb == '<': return var1 < var2
	if symb == '<=': return var1 <= var2
	if symb == '==': return var1 == var2

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
	'>': lambda var1, var2: _len_comparaison(var1, '>', var2),
	'=>': lambda var1, var2: _len_comparaison(var1, '>=', var2),
	'<': lambda var1, var2: _len_comparaison(var1, '<', var2),
	'<=': lambda var1, var2: _len_comparaison(var1, '<=', var2),
	'=': lambda var1, var2: _verif_type(var1) == _verif_type(var2),
	'==': lambda var1, var2: _len_comparaison(var1, '==', var2),
	'===': lambda var1, var2: var1 is var2,
	'in': lambda var1, var2: _type_in(var1, var2),
	'inn': lambda var1, var2: var1 in var2,
	'innn': lambda var1, var2: _objet_in(var1, var2),
	'&': lambda var1, var2: var1 and var2,
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

		for symb, value in get_values_and_symb():
			func = func_actions.get(symb)
			if not func:
				raise Exception('Func')

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