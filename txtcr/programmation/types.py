# -*- coding: utf-8 -*-

from .conditions import *
from .calculs import *

def get_vars(clss, parametres):
	#Get variables globals
	vars_globals = clss.get('variables')
	#Mise en avant des variables locals
	vars_locals = clss.get('I')
	if vars_globals.index(vars_locals) != 0:
		vars_globals.remove(vars_locals)
		vars_globals.insert(0, vars_locals)
	#Set variables à retourner
	variables = vars_globals[:]
	#Variables objet
	variables.insert(0, {})
	for variable, value in parametres.items(): 
		existe = False
		for Tvars in variables:
			if variable in Tvars:
				Tvars[variable] = value
				existe = True
		if not existe:
			variables[0][variable] = value
	#Retourne Variable objet, local, global
	return variables

class TXTCRbool:
	def __init__(ss, status, commentaire=''):
		ss.status = status
		ss.commentaire = commentaire
	def __eq__(ss, status): return ss.status == status
	def __ne__(ss, status): return not ss.status == status
	def __bool__(ss): return ss.status
	def __str__(ss): return '%s%s'%(1 if ss.status else 0, ' #%s'%ss.commentaire if ss.commentaire else '')
	def __repr__(ss): return '%s'%ss.status
	def comm(commentaire):
		ss.commentaire = commentaire

class TXTCRstr(str):
	def __init__(ss, text):
		ss.text = text
	def __str__(ss): return str(ss.verif())
	def __repr__(ss): return str(ss.verif())
	def __call__(ss, *cle, **ops): return ss.verif(*cle, **ops)
	def verif(ss, *cle, **ops):
		variables = get_vars(ss._clss, ops)
		return convert_variable(ss.text, variables, ss._clss.get('defauts'), ss._decode, exclues=balises+['#'], leve_erreur=False)

class TXTCRcalc:
	def __init__(ss, calcul, clss, decode):
		ss._clss = clss
		ss.calcul = calcul
		ss._decode = decode
	def __str__(ss): return str(ss.verif())
	def __repr__(ss): return '%s'%ss.verif()
	def __call__(ss, *cle, **ops): return ss.verif(*cle, **ops)
	def verif(ss, *cle, **ops):
		variables = get_vars(ss._clss, ops)
		return calc.getnbr(
					calc.parentheses(
							convert_variable(ss.calcul, variables, ss._clss.get('defauts'), ss._decode, exclues=balises+['#'], leve_erreur=False)))[0]

class TXTCRcond:
	def __init__(ss, condition, clss, decode):
		ss._clss = clss
		ss._decode = decode
		ss.condition = condition

		ss.action_if_true = None
		ss.action_if_false = None

	def __eq__(ss, condition): return str(ss) == str(condition)
	def __ne__(ss, condition): return not (str(ss) == str(condition))
	def __str__(ss): return '<%s: %s>'%(ss.__class__.__name__, ss.condition)
	def __call__(ss, *cle, **ops): return ss.verif(*cle, **ops)
	def action_if(ss, true=None, false=None):
		if true: ss.action_if_true = true
		if false: ss.action_if_false = false

	def modif(ss, nouv_condition):
		ss.condition = nouv_condition

	def verif(ss, *cle, **ops):
		variables = get_vars(ss._clss, ops)

		deffonc = DefCondition({}, variables, ss._clss.get('defauts'), ss._decode)
		resulta = deffonc.recup_condition_acts(ss.condition).analyse()
		deffonc = None

		if isinstance(resulta, bool):
			resulta = TXTCRbool(resulta)

		if ss.action_if_true or ss.action_if_false:
			variables = recup_variables(ss._variables)
			variables = {k:v for k,v in variables.items() if type(k) == str}

		if resulta == True:
			if ss.action_if_true:
				resulta = ss.action_if_true(**variables)
		elif resulta == False:
			if ss.action_if_false:
				resulta = ss.action_if_false(**variables)

		return resulta