---
title: "Obfuscation NTCP"
number: "106"
author: "zzz"
created: "2010-11-23"
lastupdated: "2014-01-03"
status: "Rejeté"
thread: "http://zzz.i2p/topics/774"
supercededby: "111"
---

## Aperçu

Cette proposition concerne la refonte du transport NTCP pour améliorer sa résistance à l'identification automatisée.

## Motivation

Les données NTCP sont chiffrées après le premier message (et le premier message semble être des données aléatoires), empêchant ainsi l'identification du protocole par "analyse de charge utile". Il reste toutefois vulnérable à l'identification du protocole par "analyse de flux". C'est parce que les 4 premiers messages (c'est-à-dire la poignée de main) ont une longueur fixe (288, 304, 448 et 48 octets).

En ajoutant des quantités aléatoires de données aléatoires à chacun des messages, nous pouvons rendre l'identification beaucoup plus difficile.

## Modifications apportées au NTCP

C'est assez lourd mais cela empêche toute détection par les équipements DPI.

Les données suivantes seront ajoutées à la fin du message de 288 octets 1 :

- Un bloc chiffré ElGamal de 514 octets
- Remplissage aléatoire

Le bloc ElG est chiffré avec la clé publique de Bob. Une fois déchiffré à 222 octets, il contient :
- 214 octets de remplissage aléatoire
- 4 octets 0 réservés
- 2 octets de longueur de remplissage à suivre
- 2 octets de version de protocole et de drapeaux

Dans les messages 2 à 4, les deux derniers octets du remplissage indiqueront maintenant la longueur du remplissage supplémentaire à suivre.

Notez que le bloc ElG ne dispose pas de la confidentialité persistante parfaite mais qu'il n'y a rien d'intéressant dedans.

Pourrions-nous modifier notre bibliothèque ElG pour qu'elle chiffre des tailles de données plus petites si nous pensons que 514 octets est beaucoup trop ? Le chiffrement ElG pour chaque configuration NTCP est-il excessif ?

Le support pour cela serait annoncé dans le netdb RouterAddress avec l'option "version=2". Si seuls 288 octets sont reçus dans le Message 1, on suppose qu'Alice est la version 1 et aucun remplissage n'est envoyé dans les messages suivants. Notez que la communication pourrait être bloquée si un MITM fragmentait l'IP à 288 octets (très improbable selon Brandon).
