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
- **`M#`** Main 
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
- **`>`** Class
- **`/`** Commentaire  

### Balise fermante (seulement format 2)

- **`}`** Dict
- **`]`** List
- **`)`** Tuple  

_Ex format 1: `{"wouf:1"pouet`_  
_Ex format 2: `{"wouf:"pouet}`_
