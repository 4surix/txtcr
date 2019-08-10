import txtcr

#Format 1 --------------------------------
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

#Format 2 --------------------------------
texte = """
|;#
|;|N#MiniExemple
|;|I#{
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

print(exemple.exemple)

fichier = open('exemple.txtcr', 'w')
txtcr.encode(exemple, fichier=fichier)
fichier.close()

#Autre méthode
with txtcr.fichier('exemple.txtcr', 'w') as exemple:
	print(exemple.exemple)
	exemple.exemple = 'plouf'
	#Les modifications sont enregistrées automatiquement à la fin

#Format 2 simplifié ---------------------
exemple = txtcr.decode("""|;#
|;|N#FormatSimplifier
|;|I#{
	"exemple:
	{
	"Texte_in_liste:["|arbre;pomme;poire;];
	"NombrePositif_in_tuple:(+|12;190;145.6)
	}
}
""")

print(exemple.exemple['Texte_in_liste'][1])

#Conditions -----------------------------
exemple = txtcr.decode("""|;#
|;|N#Condition
|;|I#{
	+0: -12.5;
	-12.5: 'armoire;
	"nbr: +0;
	"exemple:
	> ###nbr### = #value# = 1 C'est égal à value & (+1 in [+2] | (+3.5 > +1 & -4 < +2))
}
""")

def aff(value, **ops): 
	print("C'est égal à %s"%(value))

exemple.exemple.action_if(true=aff, false=lambda **ops: print('Oups !'))
exemple.exemple(value=b'armoire')

#Types ----------------------------------
exemple = txtcr.decode("""|;#
|;|N#Types
""")

txtcr.cond(exemple, if_modo='#id# in #modos#')
txtcr.bool(exemple, pouet=False) #Pas très utile, cela revient à faire exemple.pouet = True, 
								#mais possibilité de mettre un commentaire par la suite avec exemple.pouet.comm('Commentaire')
txtcr.bool(exemple, arbre=(False, "Ce n'est pas un arbre"))

exemple.pouet = True
exemple.if_modo = '> #id# in #ids_modos#'
print(exemple.encode())