# -*- coding: utf-8 -*-

class TypeInconnue(Exception):
	"""Type non pris en charge"""

	def __init__(ss, t, p, v):
		ss.type = t
		ss.profondeur = p
		ss.valeur = v

	def __str__(ss):
		return f'{ss.__doc__}, Type : {ss.type} | Profondeur : {ss.profondeur} | Valeur : {ss.valeur}'

class VariableError(Exception):
	"""Variable introuvable, verifiez son nom ou si elle est bien définie !"""

	def __init__(ss, variable):
		ss.variable = variable

	def __str__(ss):
		return f'{ss.__doc__}, Nom variable : "{ss.variable}"'

class ParamError(Exception):
	"""Paramètres incorrects"""

	def __init__(ss, action):
		ss.action = action

	def __str__(ss):
		return f'{ss.__doc__}, Nom action : "{ss.action}"'