import txtcr


print("-"*30)

class Pouf(txtcr.Param.PrebuiltStr["{N#}"]):
    pomme = "rouge"
    nombre = 10
    fraise = ["rouge", "blanche"]

class Pouet(txtcr.Param.PrebuiltStr["<{I#.pouf}>"]):
    pouf = Pouf
    patapouf = True   

# Avec et sans indent
r = txtcr.encode(Pouet)
print(r)
r = txtcr.encode(Pouet, indent=4)
print(r)

print("-"*30)

r = txtcr.decode(r)
print(r)

print("-"*30)

class Exemple:
    bid = 1234
    nom = "pouet"
    img = None
        
tcr = txtcr.encode(Exemple)

print(tcr)

print("-"*30)

# Tester si l'encodage/decode simmultaner fonctionne
for _ in range(3):
    tcr = txtcr.decode(tcr)

    print(tcr)

    tcr = txtcr.encode(tcr, indent=4)

    print(tcr)

print("-"*30)

# L'ouverture de fichier
with txtcr.Fichier('fichier.tcr', 'w', indent=4) as tcr:
    tcr.pomme = "rouge"
    tcr.poire = "jaune"
    #Enregistrement automatique

print(tcr)

print("-"*30)

input('Pressez entrée pour quitter.')
