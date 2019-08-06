from .utile import *
from . import erreurs
from . import encode

def separer(texte):

	d = 0
	sep = ''
	symb = ''
	asymb = ''
	liste = []
	in_texte = False
	meme_type = False
	echapement = False
	symb_croiser = 0
	enregistrement = 0

	types_simplifiables = ['"', "'", "+", "-", "0", "1"]

	for nbr, carac in enumerate(texte+'-'):

		if enregistrement:
			if carac == " ":
				continue
			partie = texte[d:enregistrement]
			if partie:
				liste.append(partie)
			d = nbr
			symb = ''
			meme_type = False
			enregistrement = 0

		if sep in types_simplifiables:
			if carac == '|':
				meme_type = sep[0]
				continue
			else: 
				in_texte = True
			sep = ''

		if carac == "\\":
			echapement = True
			continue

		elif carac in types_simplifiables:
			sep = carac
			continue

		elif not symb and carac in '{[(':
			symb = carac
			asymb = {'{':'}','[':']','(':')'}.get(symb)

		elif not echapement and carac == ';':
			if in_texte:
				in_texte = False
			if not symb_croiser:
				enregistrement = nbr
				continue

		elif not echapement and carac == ':' and in_texte:
			in_texte = False
			continue

		echapement = False

		if in_texte:
			continue

		if carac == symb:
			symb_croiser += 1
		elif carac == asymb:
			symb_croiser -= 1

	liste.append(texte[d:nbr])
	
	return liste

def separer_dict_format2(texte, _):

	liste = []
	echapement = False
	enregistrement = False

	for nbr, carac in enumerate(texte):

		if enregistrement:
			if carac == " ":
				continue
			liste.append(texte[nbr:])
			return liste

		if carac == "\\":
			echapement = True
			continue

		if not echapement and carac == ':':
			enregistrement = True
			liste.append(texte[0:nbr])

		echapement = False

def separer_dict_format1(texte, sep):
	return texte.split(sep)

class Decoder:

	def decoder(ss, texte, nbr, *, bdict=False):

		nbr += 1

		if not ss.isformat2:
			virg = ';%s' % nbr
		else:
			virg = '; '

		balise = texte[0]
		texte = texte[1:]

		if balise == "{":
			desc = {}

			if ss.isformat2:
				sep = ':'
				values = separer(texte[:-1])
				symb_value = symb_key = ''
				separer_dict = separer_dict_format2
			else:
				_, symb_key, text = isparam(':', texte, virg)
				virg, symb_value, text = isparam('|', text, virg)
				sep = ":%s" % (' ' if virg == '; ' else nbr)
				values = text.split(virg)
				separer_dict = separer_dict_format1

			for v in values:
				if not v: continue

				ops = separer_dict(v, sep)
				if not isinstance(ops, (tuple, list)) or len(ops) != 2:
					raise erreurs.SeparationError(texte, balise, ops, nbr)
				cle, value = ss.decoder(symb_key+ops[0], nbr), ss.decoder(symb_value+ops[1], nbr)
				desc[cle] = value

				if bdict: bdict.__dict__[cle] = value

		elif balise == "[":
			desc = []

			virg, symb, texte = isparam('|', texte, virg)

			if ss.isformat2:
				values = separer(texte[:-1])
			else:
				values = texte.split(virg)

			for v in values:
				if not v: continue
				desc.append(ss.decoder(symb+v, nbr))

		elif balise == "(":
			desc = ()

			virg, symb, texte = isparam('|', texte, virg)

			if ss.isformat2:
				values = separer(texte[:-1])
			else:
				values = texte.split(virg)

			for v in values:
				if not v: continue
				desc += (ss.decoder(symb+v, nbr),)

		elif balise == '"':
			desc = verif_contenue(texte, ss.variables, ss.remplacement, decode=True, isformat2=ss.isformat2)

		elif balise == "'":
			desc = texte.encode()

		elif balise == "0":
			desc = False

		elif balise == "1":
			desc = True

		elif balise == '>':
			desc = TXTCRfonc(texte, ss.variables, ss.remplacement)

		elif balise == '#':
			data = texte[3:]
			if ss.isformat2:
				data = verif_contenue(data, decode=True, isformat2=ss.isformat2, istexte=False)
			desc = ss.decode(data, nbr, variables=ss.variables, remplacement=ss.remplacement)

		elif balise == '=':
			desc = TXTCRcalc(texte, ss.variables, ss.remplacement)

		elif balise in ['+','-']:
			texte = balise+texte
			if ',' in texte: desc = float(texte.replace(',', '.'))
			elif '.' in texte: desc = float(texte)
			else: desc = int(texte)
				
		elif balise.lower() in ["o", "ø"]:
			desc = None

		else:
			raise erreurs.BaliseError(texte, balise, nbr)

		return desc

class Decodage(Decoder):

	def __init__(ss, isformat2):
		ss.variables = []
		ss.remplacement = []
		ss.isformat2 = isformat2

	def new_class(ss, nbr, **params):
		
		pc = params.get('parentclass', Clss)
		class Class(pc):

			__decodage__ = ss.decoder
			__encodage__ = encode.Encodage(ss.isformat2).encode
			__encode__ = encode.Encoder(ss.isformat2).encoder

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

			def get(ss, balise, param=None, *, defaut=None):
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

			def getnew(ss, balise, param=None, *, new):
				r = ss.get(balise, param)
				if r is None:
					if param: param = {balise:{param:new}}
					else: param = {balise:new}
					ss.config(mode='A', **param)
					return new
				return r

			def config(ss, mode='A', **params):

				def modifdict(info, data):

					if mode == 'W':
						for c in [c for c in info]:
							del info[c]
						for c,v in data.items():
							info[c] = v
					elif 'A' in mode:
						for c,v in data.items():
							if c not in info:
								info[c] = v
					elif 'E' in mode:
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
						ss.__class__.__TXTCRbase__ = '; '.join(['%s= %s'%(c, ss.__encode__(v, 0)) for c,v in info.items()])
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
		ss.remplacement.append(base_to_dict(ss.decoder, remplacement))

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
		ss.decoder(params.get('info', '{'), nbr, bdict=newclass)

		return newclass

	def decode(ss, data, nbr=-1, parentclass=None, **ops):

		params = {}
		if parentclass: params['parentclass']=parentclass

		nbr += 1

		if ss.isformat2:
			sep = '|;|'
		else:
			sep = ";%s"%nbr

		for d in data.split(sep):
			if not d: continue
			balise = balises_en_tete[d[:2]]
			params[balise] = d[2:] if balise == 'info' else verif_contenue(d[2:], decode=True, addsep=False, isformat2=ss.isformat2)

		return ss.new_class(nbr, **params)

def _decode(datas=None, fichier=None, liste=False, **ops):

	if fichier: datas = fichier.read()
	if not datas or not isinstance(datas, str):
		raise erreurs.FormatMauvais(type(datas))

	datas = datas.replace('\n', '').replace('\t', '')

	txtcr_format = datas[:3]
	if txtcr_format == ';0#':
		isformat2 = False
	elif txtcr_format == '|;#':
		isformat2 = True
	else:
		raise erreurs.FormatInconnue(txtcr_format)

	txtcrs = []
	for data in datas.split(txtcr_format):
		if not data: continue
		decode = Decodage(isformat2)
		txtcrs.append(decode.decode(data, **ops))
		decode = None

	return (txtcrs[0] if len(txtcrs) == 1 and not liste else txtcrs)