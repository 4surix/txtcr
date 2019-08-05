class SeparationError(Exception):
	"""Mauvaise séparation"""

	def __init__(ss, valeur, balise, retour, profondeur):
		ss.valeur = valeur
		ss.balise = balise
		ss.retour = retour
		ss.profondeur = profondeur

	def __str__(ss):
		return f'{ss.__doc__}, Valeur : |{ss.valeur}| || Retour : |{ss.retour}| || Profondeur : {ss.profondeur}'

class BaliseError(Exception):
	"""Balise inconue"""

	def __init__(ss, valeur, balise, profondeur):
		ss.valeur = valeur
		ss.balise = balise
		ss.profondeur = profondeur

	def __str__(ss):
		return f"{ss.__doc__} || Balise : |{ss.balise}| || Profondeur : {ss.profondeur} || Valeur : |{ss.valeur}| "

class FormatMauvais(Exception):
	"""Mauvais Format, doit être TXTCR ou fichier"""

	def __init__(ss, f):
		ss.format = f

	def __str__(ss):
		return f'{ss.__doc__}, Format : {ss.format}'

class FormatInconnue(Exception):
	"""Format inconnue, vérifiez la balise du début et celles qui suivent"""

	def __init__(ss, f):
		ss.format = f

	def __str__(ss):
		return f'{ss.__doc__}, Balise début : {ss.format} | Valides : |;# ou ;[0-9]+#'

class TypeMauvais(Exception):
	"""Mauvais Type, doit être dict ou class"""

	def __init__(ss, t):
		ss.type = t

	def __str__(ss):
		return f'{ss.__doc__}, Type : {ss.type}'

class TypeInconnue(Exception):
	"""Type non pris en charge"""

	def __init__(ss, t, p, v):
		ss.type = t
		ss.profondeur = p
		ss.valeur = v

	def __str__(ss):
		return f'{ss.__doc__}, Type : {ss.type} | Profondeur : {ss.profondeur} | Valeur : {ss.valeur}'
