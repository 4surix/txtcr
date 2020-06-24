
import txtcr


print("-" * 30)

class Pouf(txtcr.Param.S["{N#}"]):
    pomme = "rouge"
    nombre = 10
    fraise = ["rouge", "blanche"]

class Pouet(txtcr.Param.S["<{I#.pouf}>"]):
    pouf = Pouf
    patapouf = True

# Avec et sans indent
r = txtcr.encode(Pouet)
print(r)
r = txtcr.encode(Pouet, indent=4)
print(r)

print("-" * 30)

r = txtcr.decode(r)
print(r)

print("-" * 30)

class Exemple:
    uid = 1234
    nom = "pouet"
    conn = True
    absent = False
    img = None
        
tcr = txtcr.encode(Exemple)

print(tcr)

print("-" * 30)

# Tester si l'encodage/decodage simmultané fonctionne
for _ in range(3):
    tcr = txtcr.decode(tcr)

    print(tcr)

    tcr = txtcr.encode(tcr, indent=4)

    print(tcr)

print("-" * 30)

# L'ouverture de fichier
with txtcr.fichier('fichier.tcr', 'w', indent=4) as tcr:
    tcr.pomme = "rouge"
    tcr.poire = "jaune"
    #Enregistrement automatique

print(tcr)

print("-" * 30)

# Test ancienne et nouvelle syntaxe

tcr = """
// AncienneSyntaxe //

{"None" O"bla bla"
 "False" 0"bla bla"
 "True" 1"bla bla"
}
"""

print(txtcr.decode(tcr))

tcr = """
// NouvelleSyntaxe //

{"None" None
 "False" False
 "True" True
}
"""

print(txtcr.decode(tcr))

print("-" * 30)

input('Pressez entrée pour quitter.')
