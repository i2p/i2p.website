---
title: "Meta-LeaseSet pour le Multihoming"
number: "120"
author: "zzz"
created: "2016-01-09"
lastupdated: "2016-01-11"
status: "Rejeté"
thread: "http://zzz.i2p/topics/2045"
supercededby: "123"
---

## Vue d'ensemble

Cette proposition concerne la mise en œuvre d'un support adéquat du multihoming dans I2P qui peut
évoluer pour s'adapter à des sites de grande envergure.


## Motivation

Le multihoming est une astuce et ne devrait vraisemblablement pas fonctionner pour, par exemple, facebook.i2p à grande échelle. Supposons que nous ayons 100 multihomes, chacun avec 16 tunnels, cela représente 1600 publications de LS toutes les 10 minutes, soit presque 3 par seconde. Les floodfills seraient submergés et des limitations se mettraient en place. Et cela avant même de mentionner le trafic de recherche.

Nous avons besoin d'une sorte de meta-LS, où le LS liste les 100 vrais hachages de LS. Celui-ci aurait une durée de vie prolongée, bien plus longue que 10 minutes. Il s'agirait donc d'une recherche en deux étapes pour le LS, mais la première étape pourrait être mise en cache pendant des heures.


## Spécification

Le meta-LeaseSet aurait le format suivant :

  - Destination
  - Horodatage de publication
  - Expiration
  - Drapeaux
  - Propriétés
  - Nombre d'entrées
  - Nombre de révocations

  - Entrées. Chaque entrée contient :
    - Hash
    - Drapeaux
    - Expiration
    - Coût (priorité)
    - Propriétés

  - Révocations. Chaque révocation contient :
    - Hash
    - Drapeaux
    - Expiration

  - Signature

Les drapeaux et les propriétés sont inclus pour une flexibilité maximale.


## Commentaires

Cela pourrait ensuite être généralisé pour devenir une recherche de service de n'importe quel type. L'identifiant de service est un hachage SHA256.

Pour une évolutivité encore plus massive, nous pourrions avoir plusieurs niveaux, c’est-à-dire qu’un meta-LS pourrait pointer vers d’autres meta-LS.
