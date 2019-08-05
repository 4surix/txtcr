# Format TXTCR
Text Class Request  

## Balise Format

- **`;[0-9]+#`** Format 1
- **`;|#`** Format 2  

## Séparations

- **`;`** Valeurs
- **`:`** Key/Values in Dict  

- **`[Sep]\`** Caractére d'échappement format 1
- **`\[Sep]`** Caractére d'échappement format 2  

- **`;[0-9]+`** Balise basique format 1
- **`|;|`** Balise basique format 2  
  
_Ex format 1: `"Pouf ;\ pif :\ paf`_
_Ex format 2: `"Pouf \; pif \: paf`_  

## Balises basique

- **`N#`** Name
- **`D#`** Description
- **`R#`** Affichage
- **`T#`** Time/Date
- **`B#`** Variable de Base
- **`E#`** Encodage
- **`H#`** Hash
- **`I#`** Info/Contenue  

_Ex format 1: `|;|N#Pouf`_
_Ex format 2: `;0N#Pouf`_  

## Balises

- **`{`** Dict
- **`[`** List
- **`(`** Tuple
- **`"`** Str
- **`'`** Bytes
- **`=`** Calc
- **`+`** Int/Float Positif
- **`-`** Int/Float Negatif
- **`o`** None
- **`0`** False
- **`1`** True
- **`>`** Func
- **`#`** Class  

### Balise fermante (seulement format 2)

- **`}`** Dict
- **`]`** List
- **`)`** Tuple  

_Ex format 1: `{"wouf:1"pouet`_
_Ex format 2: `{"wouf:"pouet}`_
