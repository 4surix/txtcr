# Format TXTCR
Text Class Request  

## Balise Format

- **`;[0-9]+#`** Format 1
- **`;|#`** Format 2  

## Séparations

- **`;`** Valeurs
- **`:`** Key/Values in Dict  

- **`[symb]\`** Caractére d'échappement format 1
- **`\[symb]`** Caractére d'échappement format 2  

- **`;[0-9]+`** Balise basique format 1
- **`|;|`** Balise basique format 2  
  
_Ex format 1: `"Pouf ;\ pif :\ paf`_  
_Ex format 2: `"Pouf \; pif \: paf`_  

## Balises basique

- **`N#`** Name
- **`M#`** Main (Première variable appelée)
- **`D#`** Description
- **`R#`** Affichage
- **`T#`** Time/Date
- **`B#`** Valeurs de Base des variables
- **`E#`** Encodage
- **`H#`** Hash
- **`I#`** Info/Contenue  

_Ex format 1: `;0N#Pouf`_  
_Ex format 2: `|;|N#Pouf`_  

## Balises

- **`<`** Class
- **`{`** Dict
- **`[`** List
- **`(`** Tuple
- **`"`** Str
- **`'`** Bytes
- **`=`** Calc
- **`+`** Int/Float Positif
- **`-`** Int/Float Negatif
- **`O`** None
- **`0`** False
- **`1`** True
- **`:`** Condition
- **`/`** Commentaire  

### Balise fermante (seulement format 2)

- **`>`** Class
- **`}`** Dict
- **`]`** List
- **`)`** Tuple  

_Ex format 1: `{"wouf:1"pouet`_  
_Ex format 2: `{"wouf:"pouet}`_

## Comparaison

- **`>`** : Supérieur  
- **`=>`** : Egal ou supérieur
- **`<`** : Inférieur  
- **`<=`** : Inférieur ou égal  
- **`=`** : Même type
- **`==`** : Même valeur
- **`===`** : Même objet
- **`in`** : Type est dedans
- **`inn`** : Valeur est dedans
- **`innn`** : Objet est dedans
- **`&`** : Tout les 2 vrai
- **`|`** : Soit l'un des 2
- **`||`** : Seulement l'un des 2

Il suffit d'ajouter "`!`" à n'importe quel symbole pour avoir le contraire, exemple : "`==`" : Même valeur, "`!==`" Valeur différente  
Le symbole "`===`" et "`innn`" qui sert aux objets ne fonctionnent pas corectement pour les nombres entre -6 et +256 ainsi que les str/bytes  

## Actions :
- **`>aff> texte`** : Afficher texte
- **`>ped> variable ? texte`** : Afficher texte (falcultatif) et demander variable
- **`>add> variable + valeur`** : Ajouter valeur à variable
- **`>del> variable - valeur`** : Supprimer valeur à variable, si " - valeur" n'est pas indiquer supprime la variable
- **`>set> variable = valeur`** : Changer la valeur de variable (si n'existe pas créer une variable)
- **`>get> valeur/variable`** : Retourne valeur/variable
- **`>typ> nouv_var = variable`** Enregistre le type de la variable dans nouv_var
- **`>len> nouv_var = variable`** Enregistre le nombre d'élément de la variable dans nouv_var
