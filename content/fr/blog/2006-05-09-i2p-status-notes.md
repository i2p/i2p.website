---
title: "Notes d’état d’I2P du 2006-05-09"
date: 2006-05-09
author: "jr"
description: "0.6.1.18 release with network stability improvements, new development server 'baz', and GCJ Windows compatibility challenges"
categories: ["status"]
---

Salut à tous, nous revoilà mardi.

* Index

1) État du réseau et 0.6.1.18 2) baz 3) ???

* 1) Net status and 0.6.1.18

Après une nouvelle semaine de tests et d’ajustements, nous avons publié une nouvelle version plus tôt cet après-midi, qui devrait nous placer dans un environnement plus stable sur lequel nous pourrons nous appuyer pour apporter des améliorations. Nous ne verrons probablement pas beaucoup d’effets tant qu’elle ne sera pas largement déployée, il faudra donc peut-être attendre quelques jours pour voir comment cela évolue, mais les mesures continueront bien sûr.

Un aspect des dernières builds et releases que zzz a évoqué l’autre jour est que l’augmentation du nombre de tunnels de secours peut désormais avoir un impact conséquent lorsqu’elle est effectuée tout en réduisant le nombre de tunnels parallèles. Nous ne créons pas de nouveaux leases (entrées de leaseSet) tant que nous n’avons pas un nombre suffisant de tunnels actifs, de sorte que les tunnels de secours peuvent être déployés rapidement en cas de défaillance d’un tunnel actif, ce qui réduit la fréquence à laquelle un client se retrouve sans lease actif. Ce n’est toutefois qu’un ajustement sur un symptôme, et la dernière release devrait aider à traiter la cause profonde.

* 2) baz

« baz », la nouvelle machine que bar a donnée est enfin arrivée, un ordinateur portable AMD64 Turion (avec Windows XP sur le disque d’amorçage, et quelques autres OS en préparation via des disques externes). Je l’ai aussi passée au crible ces derniers jours, en essayant d’y tester quelques idées de déploiement. Un problème auquel je me heurte toutefois est de faire fonctionner gcj sous Windows. Plus précisément, un gcj avec un gnu/classpath moderne. La rumeur n’est toutefois pas très encourageante — on peut le construire soit nativement dans mingw, soit le cross-compiler depuis linux, mais il a des problèmes comme des segfaults (erreurs de segmentation) dès qu’une exception traverse une frontière de dll. Ainsi, par exemple, si java.io.File (situé dans libgcj.dll) lève une exception, si elle est interceptée par quelque chose dans net.i2p.* (situé dans libi2p.dll ou i2p.exe), *poof*, l’appli disparaît.

Bon, ça ne s’annonce pas très bien. Les gens de gcj seraient très intéressés si quelqu’un pouvait venir donner un coup de main sur le développement win32, mais un support viable n’a pas l’air imminent. Donc il semble que nous devrons prévoir de continuer à utiliser une JVM Sun sous Windows, tout en prenant en charge gcj/kaffe/sun/ibm/etc sur *nix (systèmes de type Unix). Je suppose que ce n’est pas si terrible que ça, puisque ce sont les utilisateurs *nix qui ont des problèmes pour packager et distribuer des JVM.

* 3) ???

Ok, je suis déjà en retard pour la réunion, donc je devrais conclure et basculer sur la fenêtre IRC, je suppose... on se retrouve dans quelques minutes ;)

=jr
