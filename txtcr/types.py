# -*- coding: utf-8 -*-

class TXTCRbool:
	def __init__(ss, status, commentaire=''):
		ss.status = status
		ss.commentaire = commentaire
	def __eq__(ss, status): return ss.status == status
	def __ne__(ss, status): return not ss.status == status
	def __bool__(ss): return ss.status
	def __repr__(ss): return ss.status
	def __str__(ss): return '%s%s'%(1 if ss.status else 0, ' #%s'%ss.commentaire if ss.commentaire else '')
	def comm(commentaire):
		ss.commentaire = commentaire

class TXTCRstr(str):
	def __init__(ss, text):
		ss.text = text
	def __str__(ss): return str(ss.verif())
	def __repr__(ss): return str(ss.verif())

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