---
title: "Notes de statut I2P du 2005-04-19"
date: 2005-04-19
author: "jr"
description: "Mise à jour hebdomadaire portant sur les correctifs à venir pour la version 0.5.0.7, les progrès du transport SSU sur UDP, les modifications de la feuille de route reportant la version 0.6 à juin, et le développement de Q"
categories: ["status"]
---

Salut à tous, c'est encore ce moment de la semaine,

* Index

1) État du réseau 2) État de SSU 3) Mise à jour de la feuille de route 4) État de Q 5) ???

* 1) Net status

Au cours des près de deux semaines qui ont suivi la sortie de 0.5.0.6, les choses ont été globalement positives, même si les fournisseurs de services (eepsites(I2P Sites), ircd, etc) se sont heurtés dernièrement à quelques bogues. Même si les clients fonctionnent bien, au fil du temps un serveur peut se retrouver dans une situation où des tunnels défaillants déclenchent un code de limitation de débit excessif, empêchant la reconstruction et la publication correctes du leaseSet.

Il y a eu quelques correctifs dans CVS, entre autres, et je m’attends à ce que nous publiions une nouvelle version 0.5.0.7 d’ici un jour ou deux.

* 2) SSU status

Pour ceux qui ne suivent pas mon blog (ô combien passionnant), nous avons fait beaucoup de progrès avec le transport UDP et, à l’heure actuelle, on peut dire sans trop se tromper que le transport UDP ne sera pas notre goulot d’étranglement en termes de débit :) En déboguant ce code, j’en ai profité pour travailler aussi sur la mise en file d’attente aux niveaux supérieurs, en repérant les endroits où nous pouvons supprimer des points d’étranglement inutiles. Comme je l’ai dit la semaine dernière, il reste encore beaucoup de travail à faire. Plus d’infos seront disponibles quand il y aura plus d’infos.

* 3) Roadmap update

Nous sommes en avril maintenant, donc la feuille de route [1] a été mise à jour en conséquence - en supprimant 0.5.1 et en décalant certaines dates. La grande modification, c'est de déplacer 0.6 d'avril à juin, même si en réalité ce n'est pas un changement aussi important qu'il n'y paraît. Comme je l'ai mentionné la semaine dernière, mon propre calendrier a un peu bougé, et plutôt que de déménager à $somewhere en juin, je déménage à $somewhere en mai. Même si nous pourrions avoir prêt ce qui est nécessaire pour 0.6 ce mois-ci, il est hors de question que je sorte une mise à jour majeure de ce genre puis que je disparaisse pendant un mois, puisque la réalité du logiciel, c'est qu'il y aura des bogues qui ne seront pas détectés lors des tests.

[1] http://www.i2p.net/roadmap

* 4) Q status

Aum se déchaîne sur Q, en ajoutant encore des nouveautés pour nous, avec les dernières captures d’écran publiées sur son site [2]. Il a également intégré le code dans CVS (youpi), ce qui devrait nous permettre de commencer les tests alpha bientôt. Je suis sûr que nous aurons d’autres nouvelles d’aum avec des détails sur la façon d’aider, ou vous pouvez explorer le contenu dans CVS à i2p/apps/q/

[2] http://aum.i2p/q/

* 5) ???

Il s'est passé beaucoup d'autres choses aussi, avec des discussions animées sur la liste de diffusion, le forum et irc. Je ne vais pas essayer de les résumer ici, puisqu'il ne reste que quelques minutes avant la réunion, mais passez faire un tour s'il y a quelque chose qui n'a pas été abordé et que vous souhaitez soulever !

=jr
