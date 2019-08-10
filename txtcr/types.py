# -*- coding: utf-8 -*-

from .fonc_type import *

class TXTCRbool:
	def __init__(ss, status, commentaire=''):
		ss.status = status
		ss.commentaire = commentaire
	def __eq__(ss, status): return ss.status == status
	def __ne__(ss, status): return not ss.status == status
	def __bool__(ss): return ss.status
	def __repr__(ss): return ss.status
	def __str__(ss): return '%s #%s'%(ss.status, ss.text)
	def comm(commentaire):
		ss.commentaire = commentaire

class TXTCRstr(str):
	def __init__(ss, text):
		ss.text = text
	def __str__(ss): return str(ss.verif())
	def __repr__(ss): return str(ss.verif())
	def __call__(ss, *cle, **ops): return ss.verif(*cle, **ops)
	def verif(ss, *cle, **ops):
		variables = recup_variables(ss._variables)
		for k,v in ops.items(): variables[k] = v
		return replace_variables(ss.text, variables, ss._remplacement)

class TXTCRcalc:
	def __init__(ss, calcul, variables, remplacement):
		ss._remplacement = remplacement
		ss._variables = variables
		ss.calcul = calcul
	def __str__(ss):
		ss.verif()
		return str(ss.nbr)
	def __repr__(ss):
		ss.verif()
		return str(ss.nbr)
	def verif(ss):
		ss.nbr = calc.getnbr(calc.parentheses(replace_variables(ss.calcul, recup_variables(ss._variables), ss._remplacement)))[0]

class TXTCRcond:
	def __init__(ss, condition, variables, remplacement, decode):
		ss._remplacement = remplacement
		ss._variables = variables
		ss._decode = decode
		ss.condition = condition

		ss.action_if_true = None
		ss.action_if_false = None

	def __eq__(ss, condition): return str(ss) == str(condition)
	def __ne__(ss, condition): return not str(ss) == str(condition)
	def __call__(ss, *cle, **ops): return ss.verif(*cle, **ops)
	def action_if(ss, true=None, false=None):
		if true: ss.action_if_true = true
		if false: ss.action_if_false = false

	def modif(ss, nouv_condition):
		ss.condition = nouv_condition

	def verif(ss, *cle, **ops):
		variables = recup_variables(ss._variables)
		for k,v in ops.items(): variables[k] = v

		def_condition = DefCondition(ss.condition, variables, ss._remplacement, ss._decode)
		resulta = def_condition.analyse()
		def_condition = None

		variables = {k:v for k,v in variables.items() if isinstance(k, str)}
		if resulta == True and ss.action_if_true:
			ss.action_if_true(**variables)
		elif resulta == False and ss.action_if_false:
			ss.action_if_false(**variables)

		return resulta