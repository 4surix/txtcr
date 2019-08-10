# -*- coding: utf-8 -*-

from .utile import *
from . import erreurs
from . import txtcr_class
from .encode import Encode
from .decode import Decode

class ClassVersTexte(Encode):

	def __init__(ss, isformat2, isindent=False):
		ss.isindent = isindent
		ss.isformat2 = isformat2

	def __call__(ss, *cle, **ops):
		return ss.convert(*cle, **ops)

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
					ss.encode({c:v for c,v in data.__dict__.items() if c not in clss.__TXTCRtmps__}, nbr))

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
					ss.encode(data, nbr))

		else:
			raise erreurs.TypeMauvais(type(data))

	def convert(ss, data, *, nbr=-1, **ops):

		nbr += 1
		if ss.isformat2: 
			txtcr = '|;#'
			sep = '%s|;|'%('\n' if ss.isindent else '')
		else: 
			txtcr = ';%s#'%nbr
			sep = '%s;%s'%('\n' if ss.isindent else '', nbr)

		infos = ss.verif_type(data, nbr, **ops)
		balises = list(balises_en_tete.keys())
		for inbr in range(len(infos)):
			info = infos[inbr]
			if info:
				balise = balises[inbr]
				txtcr += '%s%s%s'%(sep, balise, (info if balise == 'I#' else verif_contenue(info, addsep=False, isformat2=ss.isformat2)))

		return txtcr

def class_vers_texte(datas, fichier=None, *, format=2, aff=False, liste=False, indent=True, **ops):

	if not isinstance(datas, (list, tuple)):
		datas = [datas]

	txtcrs = []
	for data in datas:
		encode = ClassVersTexte(format-1, indent)
		txtcrs.append(encode(data, **ops))
		encode = None

	if fichier: fichier.write('\n'.join(txtcrs))

	if not aff: 
		for nbr in range(len(txtcrs)):
			txtcrs[nbr] = txtcrs[nbr].replace('\n', '').replace('\t', '')

	return (txtcrs[0] if len(txtcrs) == 1 and not liste else txtcrs)

#-----------------------------------------------------------------------

class TexteVersClass(Decode):

	def __init__(ss, isformat2):
		ss.variables = []
		ss.remplacement = []
		ss.isformat2 = isformat2

	def __call__(ss, *cle, **ops):
		return ss.convert(*cle, **ops)

	def convert(ss, data, nbr=-1, parentclass=None, **ops):

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

		return txtcr_class.new(ss, nbr, **params)

def texte_vers_class(datas=None, fichier=None, liste=False, **ops):

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
		decode = TexteVersClass(isformat2)
		txtcrs.append(decode(data, **ops))
		decode = None

	return (txtcrs[0] if len(txtcrs) == 1 and not liste else txtcrs)