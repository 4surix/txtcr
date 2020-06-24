# TXTCR (TCR)

[![Build Status](https://travis-ci.com/4surix/txtcr.svg?branch=master)](https://travis-ci.com/4surix/txtcr)  
  
Format de données simple et efficace, créé pour l'envoie par sockets et la sauvegarde sur disques.  
  
Tout est expliqué dans le [wiki](https://github.com/4surix/txtcr/wiki) (encore en construction) ! Bonne lecture ! ✨  
  
# Aperçu
  
## Non indenté

```
<N#"Profil" I#{"uid" 12345678 "nom" "Petite patate" "langues" ["français" "español"] "réseaux" [("discord" "Patatie#1234") ("email" "patate@puree.com")] "activités favorites" ["manger" "dormir"] "connectée" True "description" None}>
```
  
## Indenté

```
<N#"Profil"
 I#
    {"uid" 12345678
     "nom" "Petite patate"
     "langues" 
        ["français"
         "español"
        ]
     "réseaux" 
        [
            ("discord"
             "Patatie#1234"
            )
         
            ("email"
             "patate@puree.com"
            )
        ]
     "activités favorites" 
        ["manger"
         "dormir"
        ]
     "connectée" True
     "description" None
    }
>
```