---
title: "Notes d'état I2P du 2006-01-31"
date: 2006-01-31
author: "jr"
description: "Défis de fiabilité du réseau, prochaine version 0.6.1.10 avec une nouvelle cryptographie de création de tunnel, et modifications rompant la rétrocompatibilité"
categories: ["status"]
---

Salut à tous, mardi revient encore une fois,

* Index

1) Statut du réseau 2) Statut 0.6.1.10 3) ???

* 1) Net status

Au cours de la semaine dernière, j’ai essayé quelques ajustements différents pour améliorer la fiabilité de la création de tunnels sur le réseau en production, mais il n’y a pas encore eu de percée. Il y a toutefois eu des changements substantiels dans CVS, mais je ne les qualifierais pas de... stables. Donc, en général, je recommanderais aux gens soit d’utiliser la version la plus récente (0.6.1.9, taguée dans CVS sous i2p_0_6_1_9), soit des tunnels ne dépassant pas 1 saut avec les dernières builds. D’un autre côté...

* 2) 0.6.1.10 status

Plutôt que de me battre indéfiniment avec des ajustements mineurs, je travaille sur mon réseau de test local pour migrer vers la nouvelle cryptographie et le nouveau processus de création de tunnel [1]. Cela devrait réduire une large part des échecs de création de tunnel, après quoi nous pourrons l’optimiser davantage, si nécessaire.

[1] http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/router/doc/                                tunnel-alt-creation.html?rev=HEAD

Une conséquence regrettable est que la version 0.6.1.10 ne sera pas rétrocompatible. Cela fait longtemps que nous n'avons pas eu de version non rétrocompatible, mais aux débuts nous l'avons fait à plusieurs reprises, donc cela ne devrait pas poser trop de problèmes. En gros, une fois que cela fonctionnera très bien sur mon réseau de test local, nous le déploierons en parallèle auprès de quelques volontaires courageux pour des tests précoces, puis, lorsqu'elle sera prête pour la publication, nous basculerons simplement les références de seeds (nœuds initiaux) vers les seeds du nouveau réseau et la publierons.

Je n’ai pas de date estimée pour la version 0.6.1.10, mais cela s’annonce plutôt bien pour le moment (la plupart des longueurs de tunnel fonctionnent bien, mais il y a quelques branches que je n’ai pas encore mises à l’épreuve).  Plus de nouvelles quand il y en aura, bien sûr.

* 3) ???

C’est à peu près tout ce que j’ai à dire pour le moment, même si je sais que d’autres travaillent sur des trucs et que j’ai encore quelques tours dans ma manche pour plus tard, mais on en saura davantage quand le moment sera venu. Bref, on se retrouve dans quelques minutes !

=jr
