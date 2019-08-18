# -*- coding: utf-8 -*-

class TXTCRbool:
	def __init__(ss, status, commentaire=''):
		ss.status = status
		ss.commentaire = commentaire

class TXTCRstr(str):
	def __init__(ss, text):
		ss.text = text

class TXTCRcalc:
	def __init__(ss, calcul, *cle, **ops):
		ss.calcul = calcul
		
class TXTCRcond:
	def __init__(ss, condition, *cle, **ops):
		ss.condition = condition

try:
	from .programmation.types import *
except ImportError as e:
	pass