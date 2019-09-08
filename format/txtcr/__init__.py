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
		try:
			fichier = open(ss.chemin, 'r')
			ss.data = _decode(fichier.read())
		except FileNotFoundError:
			fichier = open(ss.chemin, 'w')
			ss.data = _decode('<I#{}>')

		fichier.close()

		return ss.data

	def __exit__(ss, exception_type,  exception_value,  retraçage):
		if ss.mode == 'w':
			#Test
			_encode(ss.data)
			#Enregistrement
			fichier = open(ss.chemin, 'w')
			fichier.write(_encode(ss.data))
			fichier.close()