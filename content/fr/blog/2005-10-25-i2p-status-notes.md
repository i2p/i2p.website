---
title: "Notes d'état d'I2P du 2005-10-25"
date: 2005-10-25
author: "jr"
description: "Mise à jour hebdomadaire portant sur la croissance du réseau à 400-500 pairs, l’intégration de Fortuna (générateur de nombres pseudo-aléatoires, PRNG), la prise en charge de la compilation native avec GCJ, i2psnark, client torrent léger, et l’analyse de l’attaque d’amorçage des tunnels"
categories: ["status"]
---

Salut à tous, encore des nouvelles du front

* Index

1) Statut du réseau 2) Intégration de Fortuna 3) Statut de GCJ 4) i2psnark est de retour 5) Plus sur l’amorçage 6) Enquêtes sur les virus 7) ???

* 1) Net status

La semaine passée s’est plutôt bien déroulée sur le réseau : la situation semble assez stable, le débit est normal, et le réseau continue de croître pour atteindre de l’ordre de 400 à 500 pairs. Il y a également eu des améliorations significatives depuis la version 0.6.1.3 et, comme elles affectent les performances et la fiabilité, je m’attends à ce que nous publiions une version 0.6.1.4 plus tard cette semaine.

* 2) Fortuna integration

Grâce à la correction rapide de Casey Marshall [1], nous avons pu intégrer le générateur de nombres pseudo-aléatoires Fortuna [2] de GNU-Crypto. Cela supprime la cause de nombreuses frustrations avec la JVM Blackdown et nous permet de travailler sans problème avec GCJ. L'intégration de Fortuna dans I2P était l'une des principales raisons pour lesquelles smeghead a développé "pants" (un 'portage' basé sur 'ant'), nous avons donc désormais une nouvelle utilisation réussie de pants :)

[1] http://lists.gnu.org/archive/html/gnu-crypto-discuss/2005-10/msg00007.html [2] http://en.wikipedia.org/wiki/Fortuna

* 3) GCJ status

Comme mentionné sur la liste [3], nous pouvons désormais exécuter le router et la plupart des clients de manière transparente avec GCJ [4]. La console web elle-même ne fonctionne pas encore complètement, vous devez donc effectuer vous-même la configuration du router avec router.config (même si cela devrait « Just Work » et lancer vos tunnels après environ une minute). Je ne suis pas tout à fait sûr de la façon dont GCJ s’intégrera à nos plans de publication, même si je penche actuellement pour distribuer du pur java tout en prenant en charge à la fois des versions java et des versions compilées nativement. C’est un peu pénible de devoir compiler et distribuer de nombreuses builds différentes pour différents systèmes d’exploitation (OS) et versions de bibliothèques, etc. Quelqu’un a-t-il un avis tranché à ce sujet ?

Une autre caractéristique positive de la prise en charge de GCJ est la possibilité d'utiliser la bibliothèque de streaming depuis C/C++/Python/etc. Je ne sais pas si quelqu'un travaille sur ce type d'intégration, mais cela vaudrait probablement la peine, donc si cela vous intéresse de travailler dans ce domaine, merci de me le faire savoir !

[3] http://dev.i2p.net/pipermail/i2p/2005-October/001021.html [4] http://gcc.gnu.org/java/

* 4) i2psnark returns

Bien que i2p-bt ait été le premier client BitTorrent porté sur I2P à être largement utilisé, eco a été le premier sur le coup avec son portage de snark [5] il y a bien longtemps. Malheureusement, il n’est pas resté à jour ni compatible avec les autres clients BitTorrent anonymes, et il a donc quelque peu disparu pendant un certain temps. La semaine dernière toutefois, j’ai eu des difficultés liées à des problèmes de performances quelque part dans la chaîne i2p-bt<->sam<->streaming lib<->i2cp, alors je me suis tourné vers le code original de snark de mjw et j’ai effectué un portage simple [6], en remplaçant tous les appels java.net.*Socket par des appels I2PSocket*, les InetAddresses par des Destinations, et les URLs par des appels EepGet. Le résultat est un minuscule client BitTorrent en ligne de commande (environ 60KB compilé) que nous allons désormais livrer avec la version d’I2P.

Ragnarok a déjà commencé à y travailler pour améliorer son algorithme de sélection des blocs, et nous espérons y intégrer à la fois une interface web et des fonctionnalités multi-torrent avant la sortie 0.6.2. Si vous souhaitez aider, contactez-nous ! :)

[5] http://klomp.org/snark/ [6] http://dev.i2p.net/~jrandom/snark_diff.txt

* 5) More on bootstrapping

La liste de diffusion a été assez active dernièrement, avec les nouvelles simulations de Michael et son analyse de la construction de tunnel. La discussion est toujours en cours, avec de bonnes idées de la part de Toad, Tom et polecat, alors allez voir si vous voulez donner votre avis sur les compromis concernant certaines questions de conception liées à l’anonymat que nous allons remanier pour la version 0.6.2 [7].

Pour ceux qui aiment un peu de joli rendu visuel, Michael a aussi ce qu'il vous faut, avec une simulation de la probabilité que l'attaque vous identifie - en fonction du pourcentage du réseau qu'ils contrôlent [8], et en fonction du niveau d'activité de votre tunnel [9]

(beau travail, Michael, merci !)

[7] http://dev.i2p.net/pipermail/i2p/2005-October/thread.html     (suivez le fil de discussion "i2p tunnel bootstrap attack") [8] http://dev.i2p.net/~jrandom/fraction-of-attackers.png [9] http://dev.i2p.net/~jrandom/messages-per-tunnel.png

* 6) Virus investigations

Il y a eu des discussions au sujet de problèmes potentiels de logiciels malveillants distribués avec une application particulière compatible I2P, et Complication a fait un excellent travail en creusant la question. Les données sont disponibles, vous pouvez donc vous faire votre propre opinion. [10]

Merci Complication pour toutes vos recherches à ce sujet !

[10] http://forum.i2p.net/viewtopic.php?t=1122

* 7) ???

Il se passe énormément de choses, comme vous pouvez le voir, mais comme je suis déjà en retard pour la réunion, je ferais mieux d’enregistrer ceci et de l’envoyer, hein ? À bientôt sur #i2p :)

=jr
