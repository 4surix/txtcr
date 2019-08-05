from .utile import *
from . import erreurs

class Encoder:

	def __init__(ss, isformat2, isindent=False):
		ss.isindent = isindent
		ss.isformat2 = isformat2

	def encoder(ss, valeur, nbr, getsymb=0):

		nbr += 1

		if ss.isindent: 
			dklg = '\n'+'\t'*nbr
			virg = '%s\t\t;%s' % (dklg,  nbr)
		else: 
			dklg = ''
			virg = ';%s'%nbr

		vtype = type(valeur).__name__

		if istype('dict', vtype=vtype):
			desc = '{'

			if ss.isformat2:
				sep = ''
				virg = ';'
				pk = pv = False
			else:
				pk = isuniforme(list(valeur.keys()))
				pv = isuniforme(list(valeur.values()))
				sep = (' ' if pv else nbr)
				virg = ('; ' if pv else virg) 

			kgetsymb = (1 if pk and pk != ';' else 0)
			vgetsymb = (1 if pv and pv != ';' else 0)

			for i in valeur:
				if len(desc) > 1: desc += virg
				else:
					if pk and pk != ";": desc += '%s:'%pk
					if pv and (pv != ';' or not ss.isformat2):
						desc += '%s|'%pv
					elif pk and pk != ";": desc += '|'

				value = ss.encoder(valeur[i], nbr, vgetsymb)
				desc += '%s%s:%s%s'%(ss.encoder(i, nbr, kgetsymb),
									('\t' if ss.isindent else ''), 
									sep,
									value)

			if ss.isformat2: 
				desc += '%s}'%((';' if value[0] in '"\'' or (pv and pv in '"\'') else '') if len(desc) > 1 else '')

		elif istype('list', vtype=vtype):
			desc = '['

			iu = isuniforme(valeur)
			getsymb = (1 if iu and iu != ';' else 0)

			if ss.isformat2:
				virg = ';'
			else:
				virg = ('; ' if iu else virg) 

			for i in valeur:
				if len(desc) > 1: desc += virg
				elif iu and (iu != ';' or not ss.isformat2):
						desc += '%s| '%iu

				value = ss.encoder(i, nbr, getsymb)
				desc += value

			if ss.isformat2: 
				desc += '%s]'%(';' if value[0] in '"\'' or (iu and iu in '"\'') else '')


		elif istype('tuple', vtype=vtype):
			desc = '('

			iu = isuniforme(valeur)
			getsymb = (1 if iu and iu != ';' else 0)

			if ss.isformat2:
				virg = ';'
			else:
				virg = ('; ' if iu else virg) 

			for i in valeur:
				if len(desc) > 1: desc += virg
				elif iu and (iu != ';' or not ss.isformat2):
						desc += '%s| '%iu

				desc += ss.encoder(i, nbr, getsymb)

			if ss.isformat2:  desc += ')'


		elif istype('str', vtype=vtype):
			desc = '"%s'[getsymb:] % verif_contenue(valeur, isformat2=ss.isformat2)

		elif istype('bytes', vtype=vtype):
			desc = "'%s"[getsymb:] % str(valeur)[2:-1]

		elif istype(('int','float'), vtype=vtype):
			desc = ('%s'%valeur if str(valeur)[0] == '-' else '+%s'%valeur)[getsymb:]

		elif istype('TXTCRcalc', vtype=vtype):
			desc = '=%s'%valeur.num

		elif istype('TXTCRstr', vtype=vtype):
			desc = '"%s'[getsymb:]%valeur._text

		elif istype('TXTCRfonc', vtype=vtype):
			desc = '>%s' % valeur.fonc

		elif istype('NoneType', vtype=vtype):
			desc = 'o%s'[getsymb:] % valeur

		elif istype('bool', vtype=vtype):
			if valeur == False:
				desc = '0%s'[getsymb:] % valeur
			elif valeur == True:
				desc = '1%s'[getsymb:] % valeur

		elif is_class(valeur) and '__TXTCRvariables__' in valeur.__class__.__dict__:
			desc = '#%s' % ss.encode(valeur, nbr=nbr)

		else:
			raise erreurs.TypeInconnue(type(valeur),nbr,valeur)

		if nbr == 1:
			return (desc if len(desc) > 2 else None)
		return dklg + desc

class Encodage(Encoder):

	def __init__(ss, isformat2, isindent=False):
		ss.isindent = isindent
		ss.isformat2 = isformat2

	def verif_type(ss, data, nbr, **ops):

		if not data: data = {}

		if is_class(data):

			if "<class 'type'>" != str(data.__class__):
				clss = data.__class__
			else:
				clss = data

			return (ops.get('nom', clss.__name__),
					ops.get('desc', clss.__doc__),
					ops.get('repr', clss.__dict__.get('__TXTCRrepr__')),
					ops.get('repr', clss.__dict__.get('__TXTCRbase__')),
					ops.get('date', clss.__dict__.get('__TXTCRdate__')),
					ops.get('hash', clss.__dict__.get('__TXTCRhash__')),
					ops.get('encodage', clss.__dict__.get('__TXTCRencd__')),
					ss.encoder({c:v for c,v in data.__dict__.items() if c not in clss.__TXTCRtmps__}, nbr))

		elif isinstance(data, dict):

			def verif(data, param):
				if param in data: 
					v = data[param]
					del data[param]
					return v

			return (ops.get('nom', verif(data, '__name__')),
					ops.get('desc', verif(data, '__desc__')),
					ops.get('repr', verif(data, '__repr__')),
					ops.get('base', verif(data, '__base__')),
					ops.get('date', verif(data, '__date__')),
					ops.get('hash', verif(data, '__hash__')),
					ops.get('encodage', verif(data, '__encodage__')),
					ss.encoder(data, nbr))

		else:
			raise erreurs.TypeMauvais(type(data))

	def encode(ss, data, *, nbr=-1, **ops):

		nbr += 1
		if ss.isformat2: 
			txtcr = ';|#'
			sep = '|;|'
		else: 
			txtcr = ';%s#'%nbr
			sep = '%s;%s'%('\n\t' if ss.isindent else '', nbr)

		infos = ss.verif_type(data, nbr, **ops)
		balises = list(balises_en_tete.keys())
		for inbr in range(len(infos)):
			info = infos[inbr]
			if str(info) != 'None': 
				balise = balises[inbr]
				txtcr += '%s%s%s'%(sep, balise, (info if balise == 'I#' else verif_contenue(info, addsep=False, isformat2=ss.isformat2)))

		return txtcr

def _encode(datas, fichier=None, *, isformat2=True, aff=False, liste=False, indent=False):

	if not isinstance(datas, (list, tuple)):
		datas = [datas]

	txtcrs = []
	for data in datas:
		encode = Encodage(isformat2, indent)
		txtcrs.append(encode.encode(data))
		encode = None

	if fichier: fichier.write('\n'.join(txtcrs))

	if not aff: 
		for nbr in range(len(txtcrs)):
			txtcrs[nbr] = txtcrs[nbr].replace('\n', '').replace('\t', '')

	return (txtcrs[0] if len(txtcrs) == 1 and not liste else tuple(txtcrs))