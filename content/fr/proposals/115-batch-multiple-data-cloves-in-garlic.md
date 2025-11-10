---
title: "Regrouper Plusieurs Gousses de Données en Ail"
number: "115"
author: "orignal"
created: "2015-01-22"
lastupdated: "2015-01-22"
status: "Besoin-de-Recherche"
thread: "http://zzz.i2p/topics/1797"
---

## Vue d'ensemble

Cette proposition concerne l'envoi de plusieurs Gousses d'Ail de Données à l'intérieur d'un message d'ail de bout en bout, au lieu d'une seule.


## Motivation

Pas clair.


## Changements Requis

Les changements seraient nécessaires dans OCMOSJ et les classes d'aide associées, ainsi que dans ClientMessagePool. Comme il n'y a pas de file d'attente actuellement, une nouvelle file d'attente et un certain délai seraient nécessaires. Tout regroupement devrait respecter une taille maximale d'ail pour minimiser les pertes. Peut-être 3KB ? Il serait souhaitable de mesurer d'abord à quelle fréquence cela serait utilisé.


## Réflexions

Il n'est pas clair si cela aura un effet utile, car le streaming effectue déjà un regroupement et sélectionne le MTU optimal. Le regroupement augmenterait la taille des messages et la probabilité exponentielle de perte.

L'exception concerne le contenu non compressé, compressé en gzip au niveau I2CP. Mais le trafic HTTP est déjà compressé à un niveau supérieur, et les données Bittorrent sont généralement incompressibles. Que reste-t-il ? I2pd ne fait actuellement pas la compression x-i2p-gzip, donc cela pourrait beaucoup aider. Mais l'objectif déclaré de ne pas manquer de tags est mieux résolu avec une implémentation correcte de fenêtre dans sa bibliothèque de streaming.


## Compatibilité

Ceci est rétro-compatible, car le récepteur d'ail traitera déjà toutes les gousses qu'il reçoit.
