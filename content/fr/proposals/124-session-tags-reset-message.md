---
title: "Message de Réinitialisation pour ElGamal/AES+SessionTags"
number: "124"
author: "orignal"
created: "2016-01-24"
lastupdated: "2016-01-26"
status: "Ouvert"
thread: "http://zzz.i2p/topics/2056"
---

## Vue d'ensemble

Cette proposition concerne un message I2NP qui peut être utilisé pour réinitialiser les tags de session entre deux Destinations.


## Motivation

Imaginez qu'une destination ait un tas de tags confirmés pour une autre destination. Mais cette destination a redémarré ou a perdu ces tags d'une autre manière. La première destination continue d'envoyer des messages avec des tags et la seconde destination ne peut pas les déchiffrer. La seconde destination devrait avoir un moyen de dire à la première destination de réinitialiser (recommencer à zéro) à travers une gousse d'ail supplémentaire de la même manière qu'elle envoie un LeaseSet mis à jour.


## Conception

### Message Proposé

Cette nouvelle gousse doit contenir un type de livraison "destination" avec un nouveau message I2NP appelé "Réinitialisation des tags" et contenant le hash d'identification de l'expéditeur. Il devrait inclure un horodatage et une signature.

Peut être envoyé à tout moment si une destination ne peut pas déchiffrer les messages.


### Utilisation

Si je redémarre mon routeur et j'essaie de me connecter à une autre destination, j'envoie une gousse avec mon nouveau LeaseSet, et j'enverrais une gousse supplémentaire avec ce message contenant mon adresse. Une destination distante reçoit ce message, supprime tous les tags sortants vers moi et recommence à partir d'ElGamal.

Il est assez courant qu'une destination soit en communication avec une seule destination distante. En cas de redémarrage, elle devrait envoyer ce message à tout le monde avec le premier message de streaming ou de datagramme.
