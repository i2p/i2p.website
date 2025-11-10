---
title: "Messages I2NP Plus Grands"
number: "103"
author: "zzz"
created: "2009-04-05"
lastupdated: "2009-05-27"
status: "Abandonné"
thread: "http://zzz.i2p/topics/258"
---

## Aperçu

Cette proposition concerne l'augmentation de la limite de taille des messages I2NP.


## Motivation

L'utilisation par iMule de datagrammes de 12 Ko a révélé de nombreux problèmes. La limite actuelle est plutôt de 10 Ko.


## Conception

À faire :

- Augmenter la limite NTCP - pas si facile ?

- Plus d'ajustements de la quantité de tags de session. Peut nuire à la taille maximale de la fenêtre ? Y a-t-il des statistiques à consulter ? Rendre le nombre variable en fonction de combien nous pensons qu'ils ont besoin ? Peuvent-ils demander plus ? demander une quantité ?

- Enquêter sur l'augmentation de la taille maximale SSU (en augmentant le MTU ?)

- Beaucoup de tests

- Enfin vérifier les améliorations du fragmentateur ? - Besoin de faire des tests de comparaison d'abord !
