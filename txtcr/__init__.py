# -*- coding: utf-8 -*-

from . import convert

try:
	from .programmation.utile import *
except ImportError:
	pass

encodage = convert.class_vers_texte
decodage = convert.texte_vers_class

#Convert
def decode(data=None, **ops):
	return decodage(data, **ops)

def encode(data=None, **ops):
	return encodage(data, **ops)

#Fichier
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