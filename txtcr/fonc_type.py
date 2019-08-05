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
		if num[:1] in '-0123456789':
			variable = variable[int(num)]
		num = '|%s'%num
	else: num = ''
	return num, variable

def replace_variables(texte, variables, remplacement):

	if texte.count('#') > 1:
		
		for morceau in texte.split('#'):
			num = '#'

			if '||' in morceau:
				morceau, num = morceau.split('||')

			variable = variables.get(morceau, '#')
			if variable != '#':
				num, variable = recup_num(num, variable)
				var = '#%s%s#'%(morceau, num)
				texte = texte.replace(var, variable)
				continue

			remplace = ([r for r in [r.get(morceau) for r in remplacement] if r] + [None])[0]
			if remplace:
				num, variable = recup_num(num, variable)
				var = '#%s%s#'%(morceau, num)
				texte = texte.replace(var, remplace)

	return texte

def recup_partie_parentese(texte, fonction=None):
	d = 0
	poc = 0
	pfc = 0

	for nbr, l in enumerate(texte):
		if l == '(':
			if not d: d = nbr
			if not pfc: poc += 1
			else: pfc -= 1
		if l == ')':
			pfc += 1
			if poc == pfc:
				f = nbr
				break

	if not fonction: return d,f

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
		if symb == '^' and n2[0] > 1000: raise Exception('Exposant not < 1000')
		
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

#Type Fonction 
class DefCondition:

	def __init__(ss, fonc, variables):
		ss.fonction = fonc
		ss.variables = variables

	def param(ss, p):
		p = str(p)
		b = p[0]

		if '#' == b: 
			return ss.variables.get(p[1:-1])
		elif b in 'Noø':
			return None
		elif b in 'F0':
			return False
		elif b in 'T1':
			return True
		elif b in '+-0123456789':
			if ',' in p: return float(p.replace(',','.'))
			elif '.' in p: return float(p)
			else: return int(p)

	def verif(ss, symb):
		ss.symb = symb
		p1, p2 = _split(ss.fonc, symb)
		ss.p1, ss.p2 = p1.split()[-1], p2.split()[0]
		return ss.param(ss.p1), ss.param(ss.p2)

	def conditions(ss):
		if ' > ' in ss.fonc: 
			v1, v2 = ss.verif(' > ')
			return v1 > v2
		elif ' < ' in ss.fonc:
			v1, v2 = ss.verif(' < ')
			return v1 < v2
		elif ' = ' in ss.fonc:
			v1, v2 = ss.verif(' = ')
			return v1 == v2
		elif ' ! ' in ss.fonc:
			v1, v2 = ss.verif(' ! ')
			return v1 != v2
		elif ' in ' in ss.fonc:
			v1, v2 = ss.verif(' in ')
			return v1 in v2
		elif ' !in ' in ss.fonc:
			v1, v2 = ss.verif(' !in ')
			return v1 not in v2
		elif ' & ' in ss.fonc:
			v1, v2 = ss.verif(' & ')
			return v1 and v2
		elif ' | ' in ss.fonc:
			v1, v2 = ss.verif(' | ')
			return v1 or v2
		else: return None

	def partie(ss, fonc):
		ss.fonc = fonc
		while 1:
			c = ss.conditions()
			if c is not None:
				ss.fonc = ss.fonc.replace('%s%s%s'%(ss.p1,ss.symb,ss.p2), str(c))
			else: break
		return ss.fonc

	def analyse(ss):

		while '(' in ss.fonction:
			ss.fonction = recup_partie_parentese(ss.fonction, ss.partie)

		return ss.param(ss.partie(ss.fonction).replace(' ',''))