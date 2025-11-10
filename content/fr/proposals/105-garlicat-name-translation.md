---
title: "Traduction de Nom pour GarliCat"
number: "105"
author: "Bernhard R. Fischer"
created: "2009-12-04"
lastupdated: "2009-12-04"
status: "Abandonné"
thread: "http://zzz.i2p/topics/453"
---

## Aperçu

Cette proposition concerne l'ajout de support pour les recherches inverses DNS à I2P.


## Mécanisme de Traduction Actuel

GarliCat (GC) effectue la traduction de nom pour établir des connexions avec d'autres nœuds GC. Cette traduction de nom est simplement un recodage de la représentation binaire d'une adresse en sa forme encodée en Base32. Ainsi, la traduction fonctionne dans les deux sens.

Ces adresses sont choisies pour être longues de 80 bits. C'est parce que Tor utilise des valeurs longues de 80 bits pour l'adressage de ses services cachés. Ainsi, OnionCat (qui est le GC pour Tor) fonctionne avec Tor sans intervention supplémentaire.

Malheureusement (en ce qui concerne ce schéma d'adressage), I2P utilise des valeurs longues de 256 bits pour l'adressage de ses services. Comme déjà mentionné, GC transcode entre une forme binaire et une forme encodée en Base32. En raison de la nature de GC qui est un VPN de couche 3, dans sa représentation binaire, les adresses sont définies comme étant des adresses IPv6 qui ont une longueur totale de 128 bits. Évidemment, les adresses I2P de 256 bits ne peuvent pas y entrer.

Ainsi, une deuxième étape de traduction de nom devient nécessaire :
Adresse IPv6 (binaire) -1a-> Adresse Base32 (80 bits) -2a-> Adresse I2P (256 bits)
-1a- ... Traduction GC
-2a- ... Recherche dans le fichier hosts.txt d'I2P

La solution actuelle est de laisser le routeur I2P faire le travail. Ceci est accompli par l'insertion de l'adresse de 80 bits Base32 et sa destination (l'adresse I2P) comme une paire nom/valeur dans le fichier hosts.txt ou privatehosts.txt du routeur I2P.

Cela fonctionne essentiellement, mais cela dépend d'un service de nom qui (à mon avis) est lui-même en cours de développement et pas assez mature (surtout en ce qui concerne la distribution des noms).


## Une Solution Scalable

Je suggère de changer les étapes de l'adressage en ce qui concerne I2P (et peut-être aussi pour Tor) de telle sorte que GC effectue des recherches inverses sur les adresses IPv6 en utilisant le protocole DNS régulier. La zone inverse doit contenir directement l'adresse I2P de 256 bits dans sa forme encodée en Base32. Cela modifie le mécanisme de recherche en une seule étape ajoutant ainsi des avantages supplémentaires.
Adresse IPv6 (binaire) -1b-> Adresse I2P (256 bits)
-1b- ... Recherche inverse DNS

Les recherches DNS au sein de l'Internet sont connues pour être des fuites d'information en ce qui concerne l'anonymat. Ainsi, ces recherches doivent être effectuées au sein de I2P. Cela implique que plusieurs services DNS devraient exister au sein de I2P. Étant donné que les requêtes DNS sont généralement effectuées en utilisant le protocole UDP, GC lui-même est nécessaire pour le transport des données car il transporte des paquets UDP que I2P ne supporte pas nativement.

D'autres avantages sont associés au DNS :
1) C'est un protocole standard bien connu, donc il est continuellement amélioré et de nombreux outils (clients, serveurs, bibliothèques,...) existent.
2) C'est un système distribué. Il prend en charge l'espace de noms hébergé sur plusieurs serveurs en parallèle par défaut.
3) Il prend en charge la cryptographie (DNSSEC) qui permet l'authentification des enregistrements de ressources. Cela pourrait être directement lié aux clés d'une destination.


## Opportunités Futures

Il est possible que ce service de nom puisse également être utilisé pour effectuer des recherches directes. Cela consiste à traduire des noms d'hôtes en adresses I2P et/ou adresses IPv6. Mais ce type de recherche nécessite des investigations supplémentaires car elles sont généralement effectuées par la bibliothèque de résolveur installée localement qui utilise des serveurs de noms Internet réguliers (par exemple, comme spécifié dans /etc/resolv.conf sur les systèmes Unix-like). Cela est différent des recherches inverses de GC que j'ai expliquées ci-dessus.
Une autre opportunité pourrait être que l'adresse I2P (destination) soit enregistrée automatiquement lors de la création d'un tunnel entrant GC. Cela améliorerait grandement l'utilisabilité.
