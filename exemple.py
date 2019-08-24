import txtcr

#Encodage class -------------------------------

class Pouf:
	pomme = "rouge"
	poire = "jaune"
	seconde = 1234567
	actions = ["bouger", "manger", "sauter"]

texte = txtcr.encode(Pouf)
print('Class :', texte)
clss = txtcr.decode(texte)
print(clss.pomme) #rouge

#Empilement de class comme les dict/list/tuple
class Arbre:
	def __init__(ss):
		ss.espece = 'chêne'

class Pouet:
	arbre = Arbre()

class Pouf:
	def __init__(ss):
		ss.paf = Pouet

info = txtcr.encode(Pouf())
print('Empilement de class :', info)

info = txtcr.decode(info)
print(info.paf.arbre.espece) #chêne

#Encodage dict --------------------------------

dictionnaire = {
	'__name__': 'Pouf',
	"pomme": "rouge",
	"poire": "jaune",
	"seconde": 1234567,
	"actions": ["bouger", "manger", "sauter"]
}

texte = txtcr.encode(dictionnaire)
print('Dict :', texte)
clss = txtcr.decode(texte)
print(clss.pomme) #rouge

#Formats ---------------------------------------

#Format 1
#Obsolète, 1er format créer, son point fort juste la rapidité

texte = """
;0#
;0N#MiniExemple
;0I#{
	"exemple:1
	"pouet
"""
#or texte = """;0#;0N#MiniExemple;0I#{"exemple:1"pouet"""

exemple = txtcr.decode(texte)
print(exemple.exemple)

#Format 2
#Format actuel, + lisible, + balise fermante

texte = """
|;#
|;|N#MiniExemple
|;|I#{
	"balise fermante":
	"possible";
	"exemple:
	"patapouf
	}
"""
#or texte = """|;#|;|N#MiniExemple|;|I#{"exemple:"patapouf}"""

exemple = txtcr.decode(texte)
print(exemple.exemple)

#Fichier ---------------------------------
fichier = open('exemple.txtcr')
exemple = txtcr.decode(fichier=fichier)
fichier.close()

print('Fichier :', exemple.exemple)

fichier = open('exemple.txtcr', 'w')
txtcr.encode(exemple, fichier=fichier)
fichier.close()

#Autre méthode
with txtcr.fichier('exemple.txtcr', 'w') as exemple:
	print('Fichier :', exemple.exemple)
	exemple.exemple = 'plouf'
	#Les modifications sont enregistrées automatiquement à la fin

#Format 2 simplifié ---------------------
#Si tout les éléments d'une liste/tuple sont du même type
#au tout début mettre la balise du type puis | et écrire librement après

exemple = txtcr.decode("""|;#
|;|N#FormatSimplifier
|;|I#{
"exemple: {
	"Texte_in_liste:["|arbre;pomme;poire;];
	"NombrePositif_in_tuple:(+|12;190;145.6)
	}
}
""")

print('Simplifié :', exemple.exemple['Texte_in_liste'][1])

#Mode programme --------------------------

exemple = txtcr.decode("""
|;#
|;|M#début
|;|I#{
"début: "Hello World !
}
""")

print('Resulta :', txtcr.main(exemple))

#Commentaires --------------------------
#Plasable seulement dans un dict comme un key

exemple = txtcr.decode("""
|;#
|;|I#{
/"Commentaire;
"début: "Le truc plus haut est un commentaire;
/"Je suis aussi un commentaire !;
}
""")

print('Resulta :', txtcr.main(exemple))

#Condition -------------------------------

exemple = txtcr.decode("""
|;#
|;|N#Condition
|;|M#début
|;|I#{
"lettre: "a;
"mot: "arbre;
"début: :
#lettre# inn #mot#
>if1
	>aff> "\"#lettre#\" est dans #mot# !"
>if0
	>aff> "\"#lettre#\" n'est pas dans #mot# !"
:
}
""")

print('Resulta :', txtcr.main(exemple))

#Importation de modules ------------------

exemple = txtcr.decode("""
|;#
|;|N#Importation
|;|M#début
|;|I#{
"utile: <#utile#>;
"pouet: <#math#>;
"début: :1
>if1
	>sum> ["a";"b"]
	>get> =3^2V2+2*10/2
	>ale> nbr_alea = +1, +5, +3
	>get> nbr_alea
	>get> suite(début=+0,fin=+10)
	>get> istype(var="test",types=("str"))
	>get> split(texte="test - armoire --- pouet",sep="-")
	>get> fact(nbr=+5)
	>get> fibo(limite=+10)
	>get> alenvers(texte="patate")
:
}
""")

print('Resulta :', txtcr.main(exemple))