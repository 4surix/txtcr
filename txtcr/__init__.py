from . import convert

encodage = convert.class_vers_texte
decodage = convert.texte_vers_class

def decode(data=None, **ops):
	return decodage(data, **ops)

def encode(data=None, **ops):
	return encodage(data, **ops)
	
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
		ss.txtcr = decodage(encodage({'__name__':'Nouveau'}, format=ss.ops.get('format', 2)))

	def ouverture(ss):
		if ss.mode == 'n':
			ss.file = open(ss.fichier, 'w', encoding=ss.ops.get('encoding', 'utf-8'))
		else:
			ss.file = open(ss.fichier, 'r', encoding=ss.ops.get('encoding', 'utf-8'))
			ss.txtcr = decodage(fichier=ss.file, **ss.ops)
		return ss.txtcr

	def fermeture(ss):
		if ss.mode in ['w','n']:
			encodage(ss.txtcr, format=ss.ops.get('format', 2))
			if ss.mode != 'n':
				ss.file.close()
				ss.file = open(ss.fichier, 'w', encoding=ss.txtcr.get('encd', 'utf-8'))
			encodage(ss.txtcr, fichier=ss.file, format=ss.ops.get('format', 2))
		ss.file.close()