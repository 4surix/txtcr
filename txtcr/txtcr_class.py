from .decode import Decode
from .encode import Encode
from . import convert
from .utile import *

def new(ss, nbr, **params):

	def base_to_dict(decodage, txt_base):
		return {c:decodage(v, 0) for c,v in [p.split('= ') for p in txt_base.split('; ') if p]}
	
	decode = Decode(ss.isformat2, ss.variables, ss.remplacement)
	pc = params.get('parentclass', Clss)

	class Class(pc):

		__encodage__ = convert.ClassVersTexte(ss.isformat2)
		__decode__ = decode
		__encode__ = Encode(ss.isformat2)

		def __setitem__(ss, item, valeur):
			ss.__dict__[item] = valeur

		def __getitem__(ss, item):
			return ss.__dict__[item]

		def __setattr__(ss, item, valeur): 
			if (is_class(valeur) 
			and '__TXTCRvars__' in valeur.__class__.__dict__):
				ss.__class__.__TXTCRvars__.append(valeur.__dict__)
				valeur.__class__.__TXTCRvars__.append(ss.__dict__)
			ss.__dict__[item] = valeur

		def get(ss, balise, defaut=None, *, param=None):
			css = ss.__class__

			valeur = ([v for c,v in {
				('N', 'name')	: css.__name__,
				('T', 'date')	: css.__TXTCRdate__,
				('D', 'desc')	: css.__doc__,
				('H', 'hash')	: css.__TXTCRhash__,
				('E', 'encd')	: css.__TXTCRencd__,
				('I', 'info')	: (ss.__dict__.get(param, defaut) if param else {c:v for c,v in ss.__dict__.items()}),
				('B', 'base')	: (base_to_dict(ss.__decodage__, css.__TXTCRbase__).get(param, defaut) if param else css.__TXTCRbase__),
			}.items() if balise in c] + [False])[0]

			if valeur is None:
				valeur = defaut
			return valeur

		def getornew(ss, balise, new, *, param=None):
			r = ss.get(balise, param=param)
			if r is None:
				if param: param = {balise:{param:new}}
				else: param = {balise:new}
				ss.config(mode='A', **param)
				return new
			return r

		def config(ss, mode='A', **params):

			def modifdict(info, data):

				if mode == 'W': #Ouverture en mode "Ecrasement"
					for c in [c for c in info]:
						del info[c]
					for c,v in data.items():
						info[c] = v
				elif 'A' in mode: #Ouverture en mode "Ajout"
					for c,v in data.items():
						if c not in info:
							info[c] = v
				elif 'E' in mode: #Ouverture en mode "Modif"
					for c,v in data.items():
						if c in info:
							info[c] = v
				else:
					raise Exception('Mode incorecte !')

			def modif(*valeur):

				if mode == 'W':
					valeur[0] = valeur[1]
				elif mode == 'A':
					if not valeur[0]:
						valeur[0] = valeur[1]
				elif mode == 'E':
					if valeur[0]:
						valeur[0] = valeur[1]
				else:
					raise Exception('Mode incorecte !')

			for param, data in params.items():

				if param == 'N': 
					modif(ss.__class__.__name__, data)
				elif param == 'D':
					modif(ss.__class__.__doc__, data)
				elif param == 'R':
					modif(ss.__class__.__TXTCRrepr__, data)
				elif param == 'T':
					modif(ss.__class__.__TXTCRdate__, data)
				elif param == 'E':
					modif(ss.__class__.__TXTCRencd__, data)
				elif param == 'H':
					modif(ss.__class__.__TXTCRhash__, data)
				elif param == 'B':
					info = base_to_dict(ss.__decodage__, ss.__class__.__TXTCRbase__)
					modifdict(info, data)
					ss.__class__.__TXTCRbase__ = '; '.join(['%s= %s'%(c, ss.__encode__(v)) for c,v in info.items()])
				elif param == 'I':
					if isinstance(data, dict):
						modifdict(ss.__dict__, data)
					else:
						modifdict(ss.__dict__, ss.__decodage__(data.replace('\n', '').replace('\t', ''),  nbr))
				else:
					raise Exception('Param incorecte !')

		def encode(ss, **ops):
			return ss.__encodage__(ss, **ops)

		def __eq__(ss, clss):
			return str(ss) == str(clss)

		def __repr__(ss):
			clss = ss.__class__
			if not ss.__TXTCRrepr__:
				return '<Not R#>'
			return str(ss.__TXTCRrepr__).format(
					N=clss.__name__,
					D=clss.__doc__,
					T=clss.__TXTCRdate__,
					E=clss.__TXTCRencd__,
					H=clss.__TXTCRhash__,
					I=ss
										)

	remplacement = params.get('base', '')
	ss.remplacement.append(base_to_dict(decode, remplacement))

	newclass = Class()
	newclass.__class__.__name__				= params.get('name', '')
	newclass.__class__.__doc__				= params.get('desc')
	newclass.__class__.__TXTCRdate__		= params.get('date')
	newclass.__class__.__TXTCRencd__		= params.get('encd')
	newclass.__class__.__TXTCRhash__		= params.get('hash')
	newclass.__class__.__TXTCRrepr__		= params.get('repr')
	newclass.__class__.__TXTCRbase__		= remplacement
	newclass.__class__.__TXTCRtmps__		= []
	newclass.__class__.__TXTCRvars__		= ss.variables

	ss.variables.append(newclass.__dict__)
	for key, value in decode(params.get('info', '{'), nbr).items():
		newclass.__dict__[key] = value

	return newclass