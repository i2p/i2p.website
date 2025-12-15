---
title: "Obfuscation de clé ECDSA"
number: "151"
author: "orignal"
created: "2019-05-21"
lastupdated: "2019-05-29"
status: "Open"
thread: "http://zzz.i2p/topics/2717"
toc: true
---

## Motivation

Certaines personnes n'aiment pas EdDSA ou RedDSA. Nous devrions offrir des alternatives et leur permettre d'obfusquer les signatures ECDSA.

## Vue d'ensemble

Cette proposition décrit l'obfuscation des clés pour les types de signatures ECDSA 1, 2, 3.

## Proposition

Fonctionne de la même manière que RedDSA, mais tout est en Big Endian.
Seuls les mêmes types de signatures sont autorisés, par ex. 1->1, 2->2, 3->3.

### Définitions

B
    Point de base de la courbe 

L
   Ordre du groupe de la courbe elliptique. Propriété de la courbe.

DERIVE_PUBLIC(a)
    Convertir une clé privée en publique, en multipliant B sur une courbe elliptique

alpha
    Un nombre aléatoire de 32 octets connu de ceux qui connaissent la destination.

GENERATE_ALPHA(destination, date, secret)
    Générer alpha pour la date courante, pour ceux qui connaissent la destination et le secret.

a
    La clé privée de signature non obfusquée de 32 octets utilisée pour signer la destination

A
    La clé publique de signature non obfusquée de 32 octets dans la destination,
    = DERIVE_PUBLIC(a), comme dans la courbe correspondante

a'
    La clé privée de signature obfusquée de 32 octets utilisée pour signer le leaseset chiffré
    C'est une clé privée ECDSA valide.

A'
    La clé publique de signature ECDSA obfusquée de 32 octets dans la destination,
    peut être générée avec DERIVE_PUBLIC(a'), ou à partir de A et alpha.
    C'est une clé publique ECDSA valide sur la courbe

H(p, d)
    Fonction de hachage SHA-256 qui prend une chaîne de personnalisation p et des données d, et
    produit une sortie de longueur 32 octets.

    Utilisez SHA-256 de la manière suivante::

        H(p, d) := SHA-256(p || d)

HKDF(salt, ikm, info, n)
    Fonction de dérivation de clé cryptographique qui prend un matériel clé initial ikm (qui
    devrait avoir une bonne entropie mais ne doit pas nécessairement être une chaîne aléatoire uniforme), un sel
    de longueur 32 octets, et une valeur 'info' spécifique au contexte, et produit une sortie
    de n octets appropriée pour être utilisée comme matériel clé.

    Utilisez HKDF comme spécifié dans [RFC-5869](https://tools.ietf.org/html/rfc5869), en utilisant la fonction de hachage HMAC SHA-256
    comme spécifié dans [RFC-2104](https://tools.ietf.org/html/rfc2104). Cela signifie que SALT_LEN est de 32 octets max.


### Calculs d'obfuscation

Un nouveau secret alpha et des clés obfusquées doivent être générés chaque jour (UTC).
Le secret alpha et les clés obfusquées sont calculés comme suit.

GENERATE_ALPHA(destination, date, secret), pour toutes les parties :

```text
// GENERATE_ALPHA(destination, date, secret)

  // secret est optionnel, sinon de longueur zéro
  A = clé publique de signature de la destination
  stA = type de signature de A, 2 octets en big endian (0x0001, 0x0002 ou 0x0003)
  stA' = type de signature de la clé publique obfusquée A', 2 octets en big endian, toujours le même que stA
  keydata = A || stA || stA'
  datestring = 8 octets ASCII YYYYMMDD à partir de la date actuelle UTC
  secret = chaîne encodée en UTF-8
  seed = HKDF(H("I2PGenerateAlpha", keydata), datestring || secret, "i2pblinding1", 64)
  // traiter seed comme une valeur de 64 octets en big endian
  alpha = seed mod L
```


BLIND_PRIVKEY(), pour le propriétaire publiant le leaseset :

```text
// BLIND_PRIVKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  a = clé privée de signature de la destination
  // Addition en utilisant l'arithmétique scalaire
  clé privée de signature obfusquée = a' = BLIND_PRIVKEY(a, alpha) = (a + alpha) mod L
  clé publique de signature obfusquée = A' = DERIVE_PUBLIC(a')
```


BLIND_PUBKEY(), pour les clients récupérant le leaseset :

```text
// BLIND_PUBKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  A = clé publique de signature de la destination
  // Addition en utilisant les éléments du groupe (points sur la courbe)
  clé publique obfusquée = A' = BLIND_PUBKEY(A, alpha) = A + DERIVE_PUBLIC(alpha)
```


Les deux méthodes de calcul de A' donnent le même résultat, comme requis.

## Adresse b33

La clé publique d'ECDSA est une paire (X,Y), donc pour P256, par exemple, c'est 64 octets, plutôt que 32 comme pour RedDSA.
Soit l'adresse b33 sera plus longue, soit la clé publique peut être stockée sous forme compressée comme dans les portefeuilles bitcoin.


## Références

* [RFC-2104](https://tools.ietf.org/html/rfc2104)
* [RFC-5869](https://tools.ietf.org/html/rfc5869)
