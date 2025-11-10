---
title: "ECIES-P256"
number: "145"
author: "orignal"
created: "2019-01-23"
lastupdated: "2019-01-24"
status: "Ouvert"
thread: "http://zzz.i2p/topics/2418"
---

## Motivation

ECIES-P256 est beaucoup plus rapide qu'ElGamal. Il existe quelques eepsites i2pd avec le type de cryptographie ECIES-P256 déjà intégré, et Java devrait être capable de communiquer avec eux et vice-versa. i2pd le prend en charge depuis la version 2.16.0 (0.9.32 Java).

## Aperçu

Cette proposition introduit un nouveau type de cryptographie ECIES-P256 qui peut apparaître dans la partie du certificat de l'identité, ou comme type de clé de chiffrement séparé dans LeaseSet2. Peut être utilisé dans RouterInfo, LeaseSet1 et LeaseSet2.

### Emplacements des clés ElGamal

En révision,
les clés publiques ElGamal de 256 octets peuvent être trouvées dans les structures de données suivantes.
Référez-vous à la spécification des structures communes.

- Dans une identité de routeur
  C'est la clé de chiffrement du routeur.

- Dans une destination
  La clé publique de la destination était utilisée pour l'ancien chiffrement i2cp-à-i2cp
  qui a été désactivé dans la version 0.6, elle est actuellement inutilisée sauf pour
  l'IV pour le chiffrement LeaseSet, qui est déprécié.
  La clé publique dans le LeaseSet est utilisée à la place.

- Dans un LeaseSet
  C'est la clé de chiffrement de la destination.

Dans le 3 ci-dessus, la clé publique ECIES prend encore 256 octets, bien que la longueur réelle de la clé soit de 64 octets.
Le reste doit être rempli avec un bourrage aléatoire.

- Dans un LS2
  C'est la clé de chiffrement de la destination. La taille de la clé est de 64 octets.

### TypesEnc dans les Certificats de Clés

ECIES-P256 utilise le type de chiffrement 1.
Les types de chiffrement 2 et 3 doivent être réservés pour ECIES-P284 et ECIES-P521.

### Utilisations de Cryptographie Asymétrique

Cette proposition décrit le remplacement d'ElGamal pour :

1) Les messages de construction du tunnel (la clé est dans RouterIdentity). Le bloc ElGamal est de 512 octets
  
2) ElGamal+AES/SessionTag de bout en bout client (la clé est dans LeaseSet, la clé de destination est inutilisée). Le bloc ElGamal est de 514

3) Le chiffrement routeur-à-routeur des netdb et autres messages I2NP. Le bloc ElGamal est de 514 octets

### Objectifs

- Compatible avec les versions antérieures
- Aucun changement pour la structure de données existante
- Beaucoup plus efficace au niveau CPU qu'ElGamal

### Non-Objectifs

- RouterInfo et LeaseSet1 ne peuvent pas publier ElGamal et ECIES-P256 ensemble

### Justification

Le moteur ElGamal/AES+SessionTag est toujours bloqué par le manque de tags, ce qui provoque une dégradation dramatique des performances dans les communications I2P. La construction du tunnel est l'opération la plus lourde car l'initiateur doit exécuter le chiffrement ElGamal 3 fois par demande de construction de tunnel.

## Primitives Cryptographiques requises

1) Génération de clé de courbe EC P256 et DH

2) AES-CBC-256

3) SHA256

## Proposition Détaillée

Une destination avec ECIES-P256 se publie avec le type de cryptographie 1 dans le certificat. Les 64 premiers octets des 256 identifiés doivent être interprétés comme clé publique ECIES et le reste doit être ignoré. La clé de chiffrement séparée de LeaseSet est basée sur le type de clé de l'identité.

### Bloc ECIES pour ElGamal/AES+SessionTags
Le bloc ECIES remplace le bloc ElGamal pour ElGamal/AES+SessionTags. La longueur est de 514 octets. Il est constitué de deux parties de 257 octets chacune. La première partie commence par un zéro puis une clé publique éphémère P256 de 64 octets, le reste de 192 octets est un bourrage aléatoire. La deuxième partie commence par un zéro puis un chiffrement AES-CBC-256 de 256 octets avec le même contenu que dans ElGamal.

### Bloc ECIES pour l'enregistrement de construction de tunnel
L'enregistrement de construction de tunnel est le même, mais sans zéros initiaux dans les blocs. Un tunnel peut s'étendre à travers n'importe quelle combinaison de types de cryptographie de routeurs et cela est fait par enregistrement. L'initiateur du tunnel chiffre les enregistrements en fonction du type de cryptographie publié du participant au tunnel, le participant au tunnel déchiffre en fonction de son propre type de cryptographie.

### Clé AES-CBC-256
Il s'agit du calcul des clés partagées ECDH où KDF est SHA256 sur la coordonnée x. Prenons Alice comme chiffreuse et Bob comme déchiffreur. Supposons que k soit la clé privée P256 éphémère choisie au hasard par Alice et P soit la clé publique de Bob. S est le secret partagé S(Sx, Sy). Alice calcule S en "convenant" k avec P, par exemple S = k*P.

Supposons que K soit la clé publique éphémère d'Alice et p soit la clé privée de Bob. Bob prend K du premier bloc du message reçu et calcule S = p*K.

La clé de chiffrement AES est SHA256(Sx) et l'iv est Sy.
