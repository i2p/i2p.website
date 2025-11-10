---
title: "Notes de statut I2P du 2006-05-02"
date: 2006-05-02
author: "jr"
description: "Améliorations de la santé du réseau dans la version 0.6.1.17, progrès en cours sur la refonte de Syndie, et optimisations du router à venir"
categories: ["status"]
---

Salut à tous, revoilà mardi.

* Index

1) Statut du réseau 2) Statut de Syndie 3) ???

* 1) Net status

With another week on 0.6.1.17 under our belt, several of the prime measurements of network health are staying in good shape. We are however seeing some of the remaining problems propogate up to the application layer, namely the recent rise in reconnections on the irc2p servers. Postman, cervantes, Complication, and myself have been digging through various aspects of the network's behavior as it relates to the user-visible performance, and we've tracked down and implemented a few improvements (current CVS HEAD is 0.6.1.17-4). We're still monitoring its behavior and experimenting with some tweaks before pushing it out as 0.6.1.18 though, but thats probably only a few days away.

* 2) Syndie status

Comme mentionné précédemment, syndie fait l’objet d’une refonte massive. Et quand je dis massive, j’entends presque entièrement repensé et réimplémenté ;) Le framework est en place (y compris des tests continus avec gcj), et les premiers éléments commencent à s’assembler, mais il est encore loin d’être fonctionnel. Une fois qu’il sera dans un état où davantage de personnes pourront aider à le faire avancer (et, euh, *l’utiliser*), il y aura plus d’informations disponibles, mais pour l’instant la refonte de syndie est essentiellement reléguée au second plan pendant que nous travaillons sur les améliorations du router.

* 3) ???

C’est à peu près tout à signaler pour le moment - comme toujours, si vous avez quelque chose à évoquer, passez à la réunion dans quelques minutes et venez dire bonjour !

=jr
