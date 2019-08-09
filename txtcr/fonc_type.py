
def recup_variables(_variables):
	variables = {}
	def decompose(d):
		for c,v in d.items():
			if isinstance(v, dict):
				decompose(v)
			else: variables[c] = v
	for v in _variables: decompose(v)
	return variables

def recup_num(num, variable):
	if num != '#':
		if num[:1] in '-+0123456789':
			variable = variable[int(num)]
		num = '|%s'%num
	else: num = ''
	return num, variable

def replace_variables(texte_precedent, variables, remplacement):

	values_not_str = {}

	texte = texte_precedent[:]

	while texte.count('#') > 1:
		
		for morceau in texte.split('#'):
			num = '#'

			if '|' in morceau:
				morceau, num = morceau.split('|')

			m = values_not_str.get(morceau, '#')
			if m != '#': morceau = m

			variable = variables.get(morceau, '#')
			if variable != '#':
				num, value = recup_num(num, variable)
				values_not_str[str(value)] = value
				texte = texte.replace('#%s%s#'%(morceau, num), str(value))

			else:
				remplace = ([r for r in [r.get(morceau) for r in remplacement] if r] + [None])[-1]
				if remplace:
					num, variable = recup_num(num, variable)
					var = '#%s%s#'%(morceau, num)
					texte = texte.replace(var, remplace)

		if texte_precedent == texte:
			break
		texte_precedent = texte

	return values_not_str.get(texte, texte)
			
def recup_partie_parentese(texte, fonction=None):
	début = 0
	fin = 0
	parentese_ouverture_croiser = 0
	parentese_fermeture_croiser = 0

	for nbr, carac in enumerate(texte):
		if carac == '(':
			if not début: début = nbr
			if not parentese_fermeture_croiser: parentese_ouverture_croiser += 1
			else: parentese_fermeture_croiser -= 1
		elif carac == ')':
			parentese_fermeture_croiser += 1
			if parentese_ouverture_croiser == parentese_fermeture_croiser:
				fin = nbr
				break

	if not fonction: return début, fin

	resulta = fonction(texte[d+1:f])
	text = list(texte)
	del text[d:f+1]
	text.insert(d, resulta)

	return ''.join(text)

def _split(texte, symb):
	r = texte.split(symb)
	if not r[0]: n1, n2 = r[1], r[2]
	elif r[1]: n1, n2 = r[0], r[1]
	else: n1, n2 = r[0], symb+r[2]
	return n1, n2

class Calcul:
	
	nums = [str(num) for num in range(10)] + ['.', ',']
	
	def getnbr(ss, v, alinvers=False):
		v = list(v)
		if alinvers: v.reverse()

		num = v.pop(0)
		
		for carac in v:
			if carac in ss.nums:
				num += carac
			elif alinvers and carac in ['-']:
				num += carac
				break
			else: break

		if alinvers: num = num[::-1]
			
		if ',' in num: nbr = float(num.replace(',', '.'))
		elif '.' in num: nbr = float(num)
		else: nbr = int(num)
		return nbr, num

	def sep(ss, equ, symb):
		n1, n2 = _split(equ, symb)
		n1, n2 = ss.getnbr(n1, True), ss.getnbr(n2)
		expr = n1[1]+symb+n2[1]
		if symb == '^' and n2[0] > 1000: raise Exception('Exposant not > 1000')
		
		return equ.replace(expr, str(eval(expr)))

	def equation(ss, equation):
		if not all([True if symb in '0123456789+-*/.,^' else False for symb in equation]):
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

#Type Fonction --------------------------------------

func_conditions = {
	'>': lambda var1, var2: var1 > var2,
	'<': lambda var1, var2: var1 < var2,
	'=': lambda var1, var2: var1 == var2,
	'!': lambda var1, var2: var1 != var2,
	'in': lambda var1, var2: var1 in var2,
	'!in': lambda var1, var2: var1 not in var2,
	'&': lambda var1, var2: var1 and var2,
	'|': lambda var1, var2: var1 or var2
}

class DefCondition:

	def __init__(ss, fonc, variables, remplacement, decode):
		ss.fonction = fonc
		ss.variables = variables
		ss.remplacement = remplacement
		ss.decode = decode

	def convert(ss, value):
		if value[0] == '#':
			value = replace_variables(value, ss.variables, ss.remplacement)
		else:
			value = ss.decode(value)
		return value

	def config_condition(ss, texte):
		valeur_actuel = []
		condition_actuel = []

		def ajout_valeur(va):
			if va: condition_actuel.append(ss.convert(' '.join(va)))
		
		for partie in texte.split(' '):
			if not partie: continue
			
			if partie in func_conditions:
				ajout_valeur(valeur_actuel)
				condition_actuel.append(partie)
				valeur_actuel = []
					
			else: valeur_actuel.append(partie)

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
		if isinstance(value, list) and len(value) >= 3 and value[1] in func_conditions:
			return True

	def applique_condition(ss, liste_conditions):
		for place, value1, symb, value2 in ss.get_values_and_symb(liste_conditions):
			if ss.is_condition(value1):
				value1 = ss.applique_condition(value1)
			if ss.is_condition(value2):
				value2 = ss.applique_condition(value2)
			liste_conditions[place] = func_conditions.get(symb)(value1, value2)
		return liste_conditions[-1]

	def analyse(ss):
		return ss.applique_condition(ss.decoupe_condition(ss.fonction))