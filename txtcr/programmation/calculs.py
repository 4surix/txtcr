# -*- coding: utf-8 -*-

from .fonc_type import *

#-----------------------------------------------------------------------------
#TYPE CALCUL
#-----------------------------------------------------------------------------

symbs_calcul = [
	'-',
	'+',
	'*',
	'/',
	'%',
	'^',
	'V'
]

class Calcul:

	def __call__(ss, equation):
		return ss.parentheses(equation)

	def equation(ss, equ):

		nbr = ''
		nbrs = []
		symb = ''

		def ajout_nbr(nbr):
			if ',' in nbr: nbr = float(nbr.replace(',', '.'))
			elif '.' in nbr: nbr = float(nbr)
			else: nbr = int(nbr)
			nbrs.append(nbr)
			return ''
					
		for carac in equ[:]:
			if (not nbr and carac in '+-') or carac in '.,0123456789':
				nbr += carac
			else:
				nbr = ajout_nbr(nbr)
				if carac not in symbs_calcul:
					raise Exception("Le symbole %s n'existe pas !"%carac)
				nbrs.append(carac)
		ajout_nbr(nbr)

		def get_nbrs(place):
			place_gauche = place - 1
			place_droite = place + 1
			n1, n2 = nbrs[place_gauche], nbrs[place_droite]
			del nbrs[place_gauche:place_droite]
			return n1, n2, place_gauche

		place = 0
		while nbrs.count('^') or nbrs.count('V'):
			partie = nbrs[place]
			if partie == '^':
				n1, n2, place = get_nbrs(place)
				nbrs[place] = n1 ** n2
			elif partie == 'V':
				n1, n2, place = get_nbrs(place)
				nbrs[place] = n1 ** (1 / n2)
			else:
				place += 1

		place = 0
		while nbrs.count('*') or nbrs.count('/'):
			partie = nbrs[place]
			if partie == '*':
				n1, n2, place = get_nbrs(place)
				nbrs[place] = n1 * n2
			elif partie == '/':
				n1, n2, place = get_nbrs(place)
				nbrs[place] = n1 / n2
			elif partie == '%':
				n1, n2, place = get_nbrs(place)
				nbrs[place] = n1 % n2
			else:
				place += 1

		place = 0
		while nbrs.count('+') or nbrs.count('-'):
			partie = nbrs[place]
			if partie == '+':
				n1, n2, place = get_nbrs(place)
				nbrs[place] = n1 + n2
			elif partie == '-':
				n1, n2, place = get_nbrs(place)
				nbrs[place] = n1 - n2
			else:
				place += 1

		return nbrs[-1]

	def parentheses(ss, equation):

		while '(' in equation:
			equation = recup_partie_parentese(equation, ss.parentheses)
		
		return ss.equation(equation)

calcul = Calcul()