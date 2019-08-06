from .decode import _decode
from .encode import _encode

def decode(data=None, **ops):
	return _decode(data, **ops)

def encode(data=None, **ops):
	return _encode(data, **ops)
	
def tmp(clss, values, *, silent=False):
	vals = clss.get('I')
	tmps = clss.__class__.__TXTCRtmps__

	if isinstance(values, dict):
		for item, value in values.item():
			if item not in tmps:
				if item not in vals:
					setattr(clss, item, value)
				tmps.append(item)
			elif not silent: raise Exception('%s est déjà une valeur temporaire !'%item)

	elif isinstance(values, list):
		for item in values:
			if item not in tmps:
				if item in vals:
					tmps.append(item)
				elif not silent: raise Exception("%s n'existe pas !"%item)
			elif not silent: raise Exception('%s est déjà une valeur temporaire !'%item)

def rmtmp(clss, cle, *, silent=False):
	tmps = clss.__class__.__TXTCRtmps__
	for item in cle:
		if item in tmps:
			tmps.remove(item)
		elif not silent: raise Exception("%s n'est pas une valeur temporaire !"%item)

class fichier:
	def __init__(ss, *cle, **ops):
		ss.params(*cle,  **ops)

	def __enter__(ss):
		return ss.ouverture()

	def __exit__(ss, type, value, traceback):
		ss.fermeture()

	def params(ss, fichier, mode='r', **ops):
		ss.fichier = fichier
		ss.mode = mode
		ss.ops = ops
		ss.txtcr = _decode(_encode({'__name__':'Nouveau'}))

	def ouverture(ss):
		if ss.mode == 'n':
			ss.file = open(ss.fichier, 'w', encoding=ss.ops.get('encoding', 'utf-8'))
		else:
			ss.file = open(ss.fichier, 'r', encoding=ss.ops.get('encoding', 'utf-8'))
			ss.txtcr = _decode(fichier=ss.file, **ss.ops)
		return ss.txtcr

	def fermeture(ss):
		if ss.mode in ['w','n']:
			_encode(ss.txtcr, isformat2=ss.ops.get('isformat2', True))
			if ss.mode != 'n':
				ss.file.close()
				ss.file = open(ss.fichier, 'w', encoding=ss.txtcr.get('encd', 'utf-8'))
			_encode(ss.txtcr, fichier=ss.file, isformat2=ss.ops.get('isformat2', True))
		ss.file.close()