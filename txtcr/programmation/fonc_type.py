# -*- coding: utf-8 -*-

from ..utile import *

#Variable ------------------------------------------
def recup_variables(_variables):
	variables = {}
	def decompose(d):
		for c,v in d.items():
			#if isinstance(v, dict): decompose(v)
			variables[c] = v
	for v in _variables: decompose(v)
	return variables

def recup_default(_variables):
	variables = {}
	def decompose(d):
		for c,v in d.items():
			#if isinstance(v, dict): decompose(v)
			variables[c] = v
	for v in _variables: decompose(v)
	return variables

def recup_partie_variable(num, variables, variable, decode):

	if num != '#':
		if decode and num[0] in balises:
			num = decode(num)

		if not isinstance(num, int):
			num = recup_variables(variables).get(num)

		variable = variable[num]

	return variable

def recup_partie_condition(variable, variables, remplacement, decode):
	nom_cond, *parties = variable[:-1].split('(')
	kwargs = [kwarg.split('=') for kwarg in '('.join(parties).split(',')]
	kwargs = [kwarg if len(kwarg) == 2 else kwarg*2 for kwarg in kwargs]
	kwargs = {k.strip():convert_variable(v.strip(), variables, remplacement, decode) for k, v in kwargs if type(k) == str}

	return nom_cond, kwargs

def convert_variable(value, variables, remplacement, decode, *, convert_redirection=True):

	if value[0] not in balises:
		if convert_redirection:
			if value[0] != '#':
				value = '#%s#'%value
			value = replace_variables(value, variables, remplacement, decode)
	else:
		value = decode(value)

	return value

def replace_variables(texte_precedent, variables, remplacement, decode=None):

	texte = str(texte_precedent)[:]

	nbr_boucle = 0
	values_not_str = {}
	is_condition = False

	while texte.count('#') > 1:

		nbr_boucle += 1

		if nbr_boucle > 1000:
			raise Exception("Boucle infinie détectée !")
		
		for morceau in texte.split('#')[1:-1]:
			if not morceau: continue

			#print('------ morc : ', morceau)

			kwargs = {}
			num = '#'
			base_variable = '#%s#'%morceau

			if '|' in morceau:
				morceau, num = morceau.split('|')
			if ')' == morceau[-1] and '(' != morceau[0] and decode:
				morceau, kwargs = recup_partie_condition(morceau, variables, remplacement, decode)
				is_condition = True

			m = values_not_str.get(morceau, '#')
			if m != '#': morceau = m
			elif morceau[0] in balises: 
				morceau = decode(morceau)

			variable = (['#'] + [r for r in [r.get(morceau, '#') for r in remplacement] if r != '#'])[-1]
			#print('------ vars : ', variables)
			for Tvars in variables:
				if morceau in Tvars:
					variable = Tvars[morceau]
					break
					
			if variable != '#':
				if is_condition:
					is_condition = False
					value = variable(**kwargs)
				else:
					value = recup_partie_variable(num, variables, variable, decode)
				value_str = str(value)
				if not isinstance(value, str):
					values_not_str[value_str] = value
				if not callable(variable) or kwargs:
					texte = texte.replace(base_variable, value_str)
				else:
					values_not_str[base_variable] = value

		if texte_precedent == texte:
			break
		texte_precedent = texte

	return values_not_str.get(texte, texte)

def recup_partie_parentese(texte, fonction=None):
	début = 0
	fin = 0
	parentese_ouverture_croiser = 0
	parentese_fermeture_croiser = 0
	fin_condition = -1

	for nbr, carac in enumerate(texte):
		if nbr <= fin_condition:
			continue

		if carac == '(':
			if nbr and texte[nbr-1] not in [' ', '*', '+', '-', '/']:
				_, fin_condition = recup_partie_parentese(texte[nbr:])
				fin_condition += nbr
			else:
				if not début: début = nbr
				if not parentese_fermeture_croiser: parentese_ouverture_croiser += 1
				else: parentese_fermeture_croiser -= 1
		elif carac == ')':
			parentese_fermeture_croiser += 1
			if parentese_ouverture_croiser == parentese_fermeture_croiser:
				fin = nbr
				break

	if not fonction: return début, fin

	resulta = fonction(texte[début+1:fin])
	text = list(texte)
	del text[début:fin+1]
	text.insert(début, resulta)

	return ''.join(text)