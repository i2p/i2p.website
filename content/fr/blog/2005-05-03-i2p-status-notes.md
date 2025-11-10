---
title: "Notes de statut d'I2P du 2005-05-03"
date: 2005-05-03
author: "jr"
description: "Mise à jour hebdomadaire portant sur la stabilité du réseau, le succès des tests en conditions réelles du transport UDP SSU, les progrès du partage de fichiers i2phex et une absence à venir de 3 à 4 semaines"
categories: ["status"]
---

Salut à tous, beaucoup de choses au programme cette semaine

* Index

1) État du réseau 2) État de SSU 3) i2phex 4) porté disparu 5) ???

* 1) Net status

Pas de grands changements concernant la santé globale du réseau - les choses semblent assez stables, et bien que nous ayons quelques à-coups occasionnels, les services semblent bien fonctionner. Il y a eu beaucoup de mises à jour dans CVS depuis la dernière version, mais pas de corrections de bogues bloquantes. Il est possible que nous fassions une version supplémentaire avant mon déménagement, simplement pour diffuser plus largement les dernières mises à jour de CVS, mais je n’en suis pas encore sûr.

* 2) SSU status

Vous en avez assez de m’entendre dire qu’il y a eu beaucoup de progrès sur le transport UDP ? Eh bien, tant pis - il y a eu beaucoup de progrès sur le transport UDP. Ce week-end, nous avons quitté les tests sur le réseau privé pour passer sur le réseau réel, et une douzaine de routers environ ont effectué une mise à niveau et ont exposé leur adresse SSU - ce qui les rend accessibles via le transport TCP pour la plupart des utilisateurs tout en permettant aux routers compatibles SSU de communiquer via UDP.

Les tests en sont encore à un stade très précoce, mais cela s’est déroulé bien mieux que je ne m’y attendais. Le contrôle de congestion s’est très bien comporté et le débit comme la latence étaient tout à fait suffisants - il a su identifier correctement les limites réelles de bande passante et partager efficacement la liaison avec des flux TCP concurrents.

Grâce aux statistiques recueillies auprès des bénévoles, il est apparu clairement à quel point le code d’accusé de réception sélectif est important pour le bon fonctionnement dans des réseaux fortement congestionnés. J’ai passé ces derniers jours à implémenter et tester ce code, et j’ai mis à jour la spécification SSU [1] pour inclure une nouvelle technique SACK efficace. Elle ne sera pas rétrocompatible avec l’ancien code SSU, par conséquent les personnes qui ont participé aux tests devraient désactiver le transport SSU jusqu’à ce qu’une nouvelle version soit prête pour les tests (espérons-le d’ici un jour ou deux).

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/udp.html?rev=HEAD

* 3) i2phex

sirup travaille d'arrache-pied sur un portage de phex vers i2p, et même s'il reste beaucoup de travail avant que ce soit prêt pour monsieur Tout-le-monde, plus tôt ce soir j'ai pu le lancer, parcourir les fichiers partagés de sirup, récupérer quelques données et utiliser son interface de chat *tousse* "instantanée".

Il y a beaucoup plus d’informations sur l’eepsite de sirup (site I2P) [2], et l’aide aux tests par des personnes déjà dans la communauté i2p serait la bienvenue (mais s’il vous plaît, jusqu’à ce que sirup l’avalise comme une version publique, et qu’i2p en soit au moins à la 0.6, sinon 1.0, gardons cela au sein de la communauté i2p). Je pense que sirup sera présent à la réunion de cette semaine, nous pourrons peut-être obtenir plus d’informations à ce moment-là !

[2] http://sirup.i2p/

* 4) awol

À propos, je ne serai probablement pas là pour la réunion de la semaine prochaine et je serai hors ligne pendant les 3 à 4 semaines suivantes. Même si cela signifie probablement qu'il n'y aura pas de nouvelles versions, il reste toute une série de choses vraiment intéressantes sur lesquelles les gens peuvent travailler :  = des applications comme feedspace, i2p-bt/ducktorrent, i2phex, fire2pe,
     addressbook, susimail, q, ou quelque chose de complètement nouveau.  = l'eepproxy - ce serait génial d'obtenir le filtrage, la prise en charge des
     connexions HTTP persistantes, des 'listen on' ACLs, et peut-être un
     backoff exponentiel pour gérer les délais d'expiration de l'outproxy (mandataire sortant) (plutôt que
     du simple round robin)  = le PRNG (générateur pseudo-aléatoire, comme discuté sur la liste)  = une bibliothèque PMTU (soit en Java, soit en C avec JNI)  = la prime pour tests unitaires et la prime GCJ  = profilage de la mémoire du router et optimisation  = et bien d'autres choses encore.

Donc, si vous vous ennuyez et souhaitez donner un coup de main, mais avez besoin d’inspiration, peut-être que l’un des éléments ci-dessus pourrait vous lancer. Je passerai probablement dans un cybercafé de temps en temps, donc je resterai joignable par email, mais le délai de réponse sera O(days).

* 5) ???

OK, c'est à peu près tout ce que j'ai à aborder pour le moment. Pour ceux qui souhaitent aider aux tests SSU la semaine prochaine, guettez des infos sur mon blog [3]. Pour le reste d'entre vous, on se voit à la réunion !

=jr [3] http://jrandom.dev.i2p/
