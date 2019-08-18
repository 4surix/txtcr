# -*- coding: utf-8 -*-

from .conditions import *
from .calculs import *

class TXTCRbool:
	def __init__(ss, status, commentaire=''):
		ss.status = status
		ss.commentaire = commentaire
	def __eq__(ss, status): return ss.status == status
	def __ne__(ss, status): return not ss.status == status
	def __bool__(ss): return ss.status
	def __repr__(ss): return ss.status
	def __str__(ss): return '%s%s'%(1 if ss.status else 0, ss.commentaire)
	def comm(commentaire):
		ss.commentaire = commentaire

class TXTCRstr(str):
	def __init__(ss, text):
		ss.text = text
	def __str__(ss): return str(ss.verif())
	def __repr__(ss): return str(ss.verif())
	def __call__(ss, *cle, **ops): return ss.verif(*cle, **ops)
	def verif(ss, *cle, **ops):
		variables = ss._variables[:]
		variables.append({})
		for k,v in ops.items(): variables[-1][k] = v
		return replace_variables(ss.text, variables, ss._remplacement, ss._decode)

class TXTCRcalc:
	def __init__(ss, calcul, variables, remplacement, decode):
		ss._remplacement = remplacement
		ss._variables = variables
		ss.calcul = calcul
		ss.decode = decode
	def __str__(ss): return 'None' #str(ss.verif())
	def __repr__(ss): return 'None' #ss.verif()
	def __call__(ss, *cle, **ops): return ss.verif(*cle, **ops)
	def verif(ss, *cle, **ops):
		for k,v in ops.items(): ss._variables[0][k] = v
		return calc.getnbr(calc.parentheses(replace_variables(ss.calcul, ss._variables, ss._remplacement, ss.decode)))[0]

class TXTCRcond:
	def __init__(ss, condition, variables, remplacement, decode):
		ss._remplacement = remplacement
		ss._variables = variables
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
		variables = ss._variables[:]
		variables.append({})
		for k,v in ops.items(): variables[-1][k] = v

		deffonc = DefCondition({}, variables, ss._remplacement, ss._decode)
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