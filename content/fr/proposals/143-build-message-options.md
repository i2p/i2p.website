---
title: "Options de Message de Construction de Tunnel"
number: "143"
author: "zzz"
created: "2018-01-14"
lastupdated: "2022-01-28"
status: "Rejeté"
thread: "http://zzz.i2p/topics/2500"
toc: true
---

## Remarque
Cette proposition n'a pas été mise en œuvre telle que spécifiée,
cependant, les messages de construction long et court ECIES (propositions 152 et 157)
ont été conçus avec des champs d'options extensibles.
Voir la [spécification Tunnel Creation ECIES](/docs/specs/implementation/#tunnel-creation-ecies) pour la spécification officielle.


## Vue d'ensemble

Ajouter un mécanisme flexible et extensible pour les options dans les Enregistrements de Construction de Tunnel I2NP
qui sont contenus dans les messages de Construction de Tunnel et de Réponse de Construction de Tunnel.


## Motivation


Il y a quelques propositions provisoires et non documentées qui arrivent pour définir des options ou des configurations dans le Message de Construction de Tunnel,
de sorte que le créateur du tunnel puisse passer certains paramètres à chaque saut de tunnel.

Il y a 29 octets disponibles dans le TBM. Nous voulons garder de la flexibilité pour les améliorations futures, mais aussi utiliser l'espace avec sagesse.
Utiliser la construction 'mapping' utiliserait au moins 6 octets par option ("1a=1b;").
Définir plus de champs d'options de manière rigide pourrait poser des problèmes plus tard.

Ce document propose un nouveau schéma de mappage d'options flexible.


## Conception

Nous avons besoin d'une représentation d'option qui soit compacte et pourtant flexible, afin que nous puissions insérer plusieurs
options, de longueurs variables, en 29 octets.
Ces options ne sont pas encore définies, et il n'est pas nécessaire de le faire pour l'instant.
N'utilisez pas la structure "mapping" (qui encode un objet Java Properties), elle est trop gaspilleuse.
Utilisez un nombre pour indiquer chaque option et sa longueur, ce qui permet un encodage compact et flexible.
Les options doivent être enregistrées par numéro dans nos spécifications, mais nous réserverons également une plage pour les options expérimentales.


## Spécification

Préliminaire - plusieurs alternatives sont décrites ci-dessous.

Ceci serait présent uniquement si le bit 5 dans les drapeaux (octet 184) est réglé à 1.

Chaque option est composée d'un numéro d'option sur deux octets et d'une longueur, suivis par des octets de valeur d'option.

Les options commencent à l'octet 193 et continuent jusqu'au dernier octet 221 au maximum.

Numéro/longueur d'option :

Deux octets. Les bits 15-4 sont le numéro d'option sur 12 bits, 1 - 4095.
Les bits 3-0 sont le nombre d'octets de valeur d'option à suivre, 0 - 15.
Une option booléenne pourrait avoir zéro octet de valeur.
Nous tiendrons un registre des numéros d'options dans nos spécifications, et nous définirons également une plage pour les options expérimentales.

La valeur de l'option est de 0 à 15 octets, à interpréter par ce qui a besoin de cette option. Les numéros d'option inconnus devraient être ignorés.

Les options se terminent par un numéro/longueur d'option de 0/0, c'est-à-dire deux octets de 0.
Le reste des 29 octets, le cas échéant, devrait être rempli de remplissage aléatoire, comme d'habitude.

Cet encodage nous donne de la place pour 14 options de 0 octet, ou 9 options de 1 octet, ou 7 options de 2 octets.
Une alternative serait d'utiliser seulement un octet pour le numéro/longueur d'option,
peut-être avec 5 bits pour le numéro d'option (32 max) et 3 bits pour la longueur (7 max).
Cela augmenterait la capacité à 28 options de 0 octet, 14 options de 1 octet, ou 9 options de deux octets.
Nous pourrions également le rendre variable, où un numéro d'option de 5 bits de 31 signifie lire 8 bits supplémentaires pour le numéro d'option.

Si le saut de tunnel doit retourner des options au créateur, nous pouvons utiliser le même format dans le message de réponse de construction de tunnel,
préfixé par un numéro magique de plusieurs octets (puisque nous n'avons pas d'octet de drapeau défini pour indiquer que des options sont présentes).
Il y a 495 octets disponibles dans le TBRM.


## Remarques

Ces changements concernent les Enregistrements de Construction de Tunnel, et peuvent donc être utilisés dans toutes les variantes de Message de Construction -
Demande de Construction de Tunnel, Demande de Construction de Tunnel Variable, Réponse de Construction de Tunnel, et Réponse de Construction de Tunnel Variable.


## Migration

L'espace inutilisé dans les Enregistrements de Construction de Tunnel est rempli de données aléatoires et actuellement ignoré.
L'espace peut être converti pour contenir des options sans problèmes de migration.
Dans le message de construction, la présence d'options est indiquée dans l'octet des drapeaux.
Dans le message de réponse de construction, la présence d'options est indiquée par un numéro magique sur plusieurs octets.
