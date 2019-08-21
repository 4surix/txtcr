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
	>get> istype(var="test",types=("str"))
	>get> split(texte="test - armoire - pouet",sep="-")
	>get> fact(nbr=+5)
	>get> fibo(limite=+10)
:
}
""")

print('Resulta :', txtcr.main(exemple))

#Importation de modules ------------------
exemple = txtcr.decode("""
|;#
|;|M#début
|;|I#{
"math: <#math#>;
"nbr: +0;
"début: :
nbr < +100
>if1
    >aff> "fibo(#nbr#) = #fibo(limite=nbr)#"
    >add> nbr + +20
    >get> début(nbr)
>if0
    >aff> "Fin"
:
}
""")

print('Resulta :', txtcr.main(exemple))