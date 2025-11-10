---
title: "Notes de statut d'I2P pour 2005-03-01"
date: 2005-03-01
author: "jr"
description: "Notes hebdomadaires sur l’état d’avancement du développement d’I2P couvrant les bogues de la version 0.5.0.1 et la version 0.5.0.2 à venir, des mises à jour de la feuille de route, l’éditeur du carnet d’adresses et des mises à jour d’i2p-bt"
categories: ["status"]
---

Salut tout le monde, il est temps de faire notre point d'avancement

* Index

1) 0.5.0.1 2) feuille de route 3) éditeur du carnet d'adresses et configuration 4) i2p-bt 5) ???

* 1) 0.5.0.1

Comme nous l'avons évoqué la semaine dernière, quelques heures après la réunion, nous avons publié une nouvelle version 0.5.0.1 corrigeant les bogues de la 0.5 qui avaient provoqué la construction d’un nombre massif de tunnels (entre autres). Globalement, cette version a amélioré la situation, mais lors de tests plus étendus, nous avons découvert des bogues supplémentaires qui ont affecté quelques personnes. En particulier, la version 0.5.0.1 peut consommer énormément de CPU si votre machine est lente ou si les tunnels de votre router échouent massivement, et certains serveurs I2PTunnel de longue durée de vie peuvent engloutir la RAM jusqu’à provoquer un OOM (épuisement de la mémoire). Il existe également un bogue ancien dans la bibliothèque de streaming, où l’établissement d’une connexion peut échouer si la combinaison de défaillances adéquate survient.

La plupart d’entre eux (entre autres) ont été corrigés dans CVS, mais certains restent en suspens. Une fois qu’ils seront tous corrigés, nous empaquetterons le tout et le livrerons en version 0.5.0.2. Je ne sais pas exactement quand cela sera, avec un peu de chance cette semaine, mais nous verrons.

* 2) roadmap

Après les versions majeures, la feuille de route [1] a tendance à être... ajustée.  La version 0.5 n'a pas fait exception.  Cette page reflète ce que je considère raisonnable et approprié pour la suite, mais bien sûr, si davantage de personnes se joignent pour aider, elle peut certainement être ajustée.  Vous remarquerez l'importante pause entre 0.6 et 0.6.1, et si cela reflète beaucoup de travail, cela reflète aussi le fait que je vais déménager (c'est à nouveau cette période de l'année).

[1] http://www.i2p.net/roadmap

* 3) addressbook editor and config

Detonate a commencé à travailler sur une interface web pour gérer les entrées du carnet d’adresses (hosts.txt), et cela semble très prometteur. Peut-être pourrons-nous obtenir un point d’avancement de la part de detonate pendant la réunion ?

De plus, smeghead a travaillé sur une interface web pour gérer la configuration de l’addressbook (carnet d’adresses) (les fichiers subscriptions.txt, config.txt).  Peut-être pourrions-nous obtenir une mise à jour de la part de smeghead pendant la réunion ?

* 4) i2p-bt

Il y a eu des progrès sur le front i2p-bt, avec une nouvelle version 0.1.8 qui corrige les problèmes de compatibilité azneti2p, comme discuté lors de la réunion de la semaine dernière. Peut-être pourrions-nous obtenir une mise à jour de la part de duck ou de smeghead pendant la réunion ?

Legion a également créé un fork à partir de i2p-bt rev, y a intégré d’autres morceaux de code, corrigé certaines choses, et propose un binaire Windows sur son eepsite(I2P Site). L’annonce [2] semble indiquer que le code source pourrait être mis à disposition, bien qu’il ne soit pas sur l’eepsite(I2P Site) pour le moment. Les développeurs I2P n’ont pas audité (ni même vu) le code de ce client, donc ceux qui ont besoin d’anonymat voudront peut‑être d’abord récupérer et examiner une copie du code.

[2] http://forum.i2p.net/viewtopic.php?t=382

Il y a également des travaux en cours sur une version 2 du client BT de Legion, bien que je n’en connaisse pas l’état d’avancement. Peut-être pourrons-nous obtenir une mise à jour de la part de Legion pendant la réunion ?

* 5) ???

C’est à peu près tout ce que j’ai à dire pour l’instant, il se passe énormément de choses. Quelqu’un d’autre travaille-t-il sur des sujets pour lesquels nous pourrions obtenir une mise à jour pendant la réunion ?

=jr
