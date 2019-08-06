import txtcr

#Format 1 --------------------------------
exemple = txtcr.decode("""|;#
|;|N#MiniExemple
|;|I#{
	"exemple:
	"patapouf
	}
""")

print(exemple.exemple)

#Format 2 --------------------------------
exemple = txtcr.decode(""";0#
;0N#MiniExemple
;0I#{
	"exemple:1
	"pouet
""")

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

#Format 1 simplifié ---------------------
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