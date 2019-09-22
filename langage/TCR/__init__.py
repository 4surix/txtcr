__version__ = '0.9.0'

from .decode import *

decode = decode
_run = run

def run(data, chemin=None, *, silent=True):

	if not silent:
		return _run(decode(data, chemin), accept_not_callable=False)

	else:
		try:
			data = decode(data, chemin)
		except Exception as e:
			print("Exception decode: %s"%e)
			return

		try:
			return _run(data, accept_not_callable=False)
		except Exception as e:
			print("Exception run: %s"%e)
			return
