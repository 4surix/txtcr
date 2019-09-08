from .decode import decode as _decode
from .encode import encode as _encode

from .types import * 

def decode(data, **ops):
	return _decode(data, with_hashtag=False, **ops)

def encode(data, **ops):
	return _encode(data, **ops)

class fichier:

	def __init__(ss, chemin, mode='r'):
		ss.chemin = chemin
		ss.mode = mode

	def __enter__(ss):
		ss.fichier = open(ss.chemin, 'r')
		ss.data = _decode(ss.fichier.read(), with_hashtag=False)
		return ss.data

	def __exit__(ss):
		ss.fichier.close()
		if ss.mode == 'w':
			#Test
			_encode(ss.data)
			#Enregistrement
			ss.fichier = open(ss.chemin, 'w')
			ss.fichier.write(_encode(ss.data))
			ss.fichier.close()