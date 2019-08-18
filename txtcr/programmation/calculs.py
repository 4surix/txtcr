# -*- coding: utf-8 -*-

from .fonc_type import *

#-----------------------------------------------------------------------------
#TYPE CALCUL
#-----------------------------------------------------------------------------

#Sert à récupérer les 2 nombres à côter d'un symbole, n1 = Nombre 1, n2 = Nombre 2
def _split(texte, symb):
	r = texte.split(symb)
	if not r[0]: n1, n2 = r[1], r[2]
	elif r[1]: n1, n2 = r[0], r[1]
	else: n1, n2 = r[0], symb+r[2]
	return n1, n2

class Calcul:
	
	caracs_nombre = list(map(str, range(10))) + ['.', ',']
	
	def getnbr(ss, v, alinvers=False):
		v = list(v)
		if alinvers: v.reverse()

		num = v.pop(0)
		
		for carac in v:
			if carac in ss.caracs_nombre:
				num += carac
			elif alinvers and carac in ['-']:
				num += carac
				break
			else: break

		if alinvers: num = num[::-1]
			
		#Convertion Nombre str en Int/Float
		if ',' in num: nbr = float(num.replace(',', '.'))
		elif '.' in num: nbr = float(num)
		else: nbr = int(num)

		return nbr, num

	def sep(ss, equ, symb):
		n1, n2 = _split(equ, symb)
		n1, n2 = ss.getnbr(n1, True), ss.getnbr(n2)
		expr = n1[1]+symb+n2[1]
		if symb == '**' and n2[0] > 1000: raise Exception('Exposant > 1000')
		
		return equ.replace(expr, str(eval(expr)))

	def equation(ss, equation):
		if not all([True if symb in '0123456789+-*/.,^ ' else False for symb in equation]):
			raise Exception('Equation non valide ! %s'%equation)
		equ = equation.replace('^', '**')
		while 1:
			if '**' in equ: equ = ss.sep(equ, '**')
			elif '*' in equ: equ = ss.sep(equ, '*')
			elif '/' in equ: equ = ss.sep(equ, '/')
			elif '+' in equ[1:]: equ = ss.sep(equ, '+')
			elif '-' in equ[1:]: equ = ss.sep(equ, '-')
			else: return equ
			
	def parentheses(ss, equation):

		while '(' in equation:
			equation = recup_partie_parentese(equation, ss.parentheses)
		
		return ss.equation(equation)

calc = Calcul()