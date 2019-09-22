from .decode import decode as _decode
from .encode import encode as _encode

from .types import * 

def decode(data, **ops):
	return _decode(data, **ops)

def encode(data, **ops):
	return _encode(data, **ops)

class fichier:

	def __init__(ss, chemin, mode='r'):

		ss.chemin = chemin
		ss.mode = mode

	def __enter__(ss):

		ss.data = ss.__open()
		return ss.data

	def __exit__(ss, exception_type,  exception_value,  retraçage):

		if ss.mode == 'w':
			ss.__save(ss.data)

	def __open(ss):

		try:
			fichier = open(ss.chemin, 'r')
			data = _decode(fichier.read())
		except FileNotFoundError:
			fichier = open(ss.chemin, 'w')
			data = _decode('<I#{}>')

		fichier.close()

		return data

	def __save(ss, data):

		#Encodde une fois avant pour voir si tout est bon
		_encode(data)
		#Enregistrement
		fichier = open(ss.chemin, 'w')
		fichier.write(_encode(data))
		fichier.close()

	def __call__(ss, data=None):

		if not data:
			return ss.__open()
		else:
			ss.__save(data)