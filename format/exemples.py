import txtcr

class Exemple:
	pomme = "rouge"
	poire = "verte"

tcr = txtcr.encode(Exemple)

print(tcr)

tcr = txtcr.decode(tcr)

print(tcr)

tcr = txtcr.encode(Exemple)

print(tcr)

with txtcr.fichier('fichier.tcr', 'w') as tcr:
	tcr.pomme = "rouge"
	tcr.poire = "verte"
	#Enregistrement automatique

print(tcr)