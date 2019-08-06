from .fonc_type import *

class TXTCRcalc:
	def __init__(ss, num, variables, remplacement):
		ss._remplacement = remplacement
		ss._variables = variables
		ss.num = num
	def __str__(ss):
		ss.verif()
		return str(ss.nbr)
	def __repr__(ss):
		ss.verif()
		return str(ss.nbr)
	def verif(ss):
		ss.nbr = calc.getnbr(calc.parentheses(replace_variables(ss.num, recup_variables(ss._variables), ss._remplacement)))[0]

class TXTCRfonc:
	def __init__(ss, fonc, variables, remplacement):
		ss._remplacement = remplacement
		ss._variables = variables
		ss.fonc = fonc
	def __eq__(ss, fonc): return str(ss) == str(fonc)
	def __ne__(ss, fonc): return not str(ss) == str(fonc)
	def __call__(ss, *cle, **ops): return ss.verif(*cle, **ops)
	def verif(ss, *cle, **ops):
		variables = recup_variables(ss._variables)
		for c,v in ops.items(): variables[c] = v
		fonc = replace_variables(ss.fonc, variables, ss._remplacement)
		return DefCondition(fonc, variables).analyse()

class TXTCRstr(str):
	def __init__(ss, text):
		ss.text = text
	def __str__(ss): return ss.verif()
	def __repr__(ss): return ss.text
	def verif(ss):
		return replace_variables(ss.text, recup_variables(ss._variables), ss._remplacement)