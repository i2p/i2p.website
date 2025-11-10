---
title: "Notes de statut I2P du 2005-11-08"
date: 2005-11-08
author: "jr"
description: "Mise à jour hebdomadaire couvrant la stabilité de la version 0.6.1.4, la feuille de route d’optimisation des performances, la sortie d’I2Phex 0.1.1.35, le développement du client BT I2P-Rufus, les progrès d’I2PSnarkGUI et les refontes de l’interface utilisateur de Syndie"
categories: ["status"]
---

Salut la bande, déjà mardi

* Index

1) État du réseau / feuille de route à court terme 2) I2Phex 3) I2P-Rufus 4) I2PSnarkGUI 5) Syndie 6) ???

* 1) Net status / short term roadmap

La 0.6.1.4 semble encore plutôt stable, même s’il y a eu depuis quelques correctifs de bogues dans CVS. J’ai également ajouté quelques optimisations pour SSU afin de transférer les données plus efficacement, ce qui, je l’espère, aura un impact sensible sur le réseau une fois qu’elles seront largement déployées. Je mets toutefois 0.6.1.5 en attente pour le moment, car il y a encore quelques éléments que je veux intégrer dans la prochaine version. Le plan actuel est de la publier ce week-end, donc restez à l’affût des dernières nouvelles.

La version 0.6.2 inclura beaucoup de nouveautés importantes pour faire face à des adversaires encore plus puissants, mais une chose qu’elle n’affectera pas, ce sont les performances. Bien que l’anonymat soit assurément le but même d’I2P, si le débit et la latence sont médiocres, nous n’aurons aucun utilisateur. Dans cette optique, mon plan est d’amener les performances au niveau nécessaire avant de passer à la mise en œuvre des stratégies d’ordonnancement des pairs de la version 0.6.2 et des nouvelles techniques de création de tunnel.

* 2) I2Phex

Il y a eu beaucoup d’activité du côté d’I2Phex ces derniers temps également, avec une nouvelle version 0.1.1.35 [1]. Il y a également eu d’autres changements dans CVS (merci Legion!), donc je ne serais pas surpris de voir une version 0.1.1.36 plus tard cette semaine.

Il y a également eu de bons progrès sur le front du gwebcache (voir http://awup.i2p/), bien que, à ma connaissance, personne n’ait commencé à travailler sur la modification d’I2Phex pour utiliser un gwebcache compatible avec I2P (intéressé ? faites-le-moi savoir !)

[1] http://forum.i2p.net/viewtopic.php?t=1157

* 3) I2P-Rufus

Selon les bruits qui courent, defnax et Rawn ont fait du hacking sur le client BT Rufus, en y fusionnant du code lié à I2P provenant d'I2P-BT. Je ne connais pas l'état actuel du portage, mais il semblerait qu'il offrira des fonctionnalités intéressantes. Je suis sûr que nous en entendrons davantage quand il y aura plus à en dire.

* 4) I2PSnarkGUI

Une autre rumeur qui circule est que Markus a bricolé une nouvelle interface graphique en C#... les captures d’écran sur PlanetPeer ont l’air très sympas [2]. Il y a toujours des plans pour une interface web indépendante de la plateforme, mais cela a l’air très réussi. Je suis sûr que nous en saurons davantage de la part de Markus au fur et à mesure que l’interface graphique progressera.

[2] http://board.planetpeer.de/index.php?topic=1338

* 5) Syndie

Il y a également eu des discussions au sujet des refontes de l’interface utilisateur de Syndie [3], et je m’attends à ce que nous voyions des progrès sur ce front dans un avenir proche. dust travaille aussi d’arrache-pied sur Sucker, en ajoutant une meilleure prise en charge de l’intégration d’un plus grand nombre de flux RSS/Atom dans Syndie, ainsi que quelques améliorations de SML lui-même.

[3] http://syndiemedia.i2p.net:8000/index.jsp?blog=ovpBy2mpO1CQ7deYhQ1cDGAwI6pQzLbWOm1Sdd0W06c=&entry=1131235200000&expand=true

* 6) ???

Énormément de choses en cours, comme toujours. Rejoignez-nous sur #i2p dans quelques minutes pour notre réunion hebdomadaire des développeurs.

=jr
