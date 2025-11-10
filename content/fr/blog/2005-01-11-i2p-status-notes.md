---
title: "Notes de statut I2P du 2005-01-11"
date: 2005-01-11
author: "jr"
description: "Notes hebdomadaires sur l'état du développement d'I2P couvrant l'état du réseau, l'avancement de la 0.5, l'état de la 0.6, azneti2p, le port FreeBSD et hosts.txt comme toile de confiance"
categories: ["status"]
---

Salut tout le monde, c'est l'heure de la mise à jour hebdomadaire

* Index

1) Statut du réseau 2) Avancement 0.5 3) Statut 0.6 4) azneti2p 5) fbsd 6) hosts.txt en tant que WoT (réseau de confiance) 7) ???

* 1) Net status

Dans l’ensemble, le réseau se comporte bien, même si nous avons eu quelques problèmes avec l’un des serveurs IRC hors ligne et mon outproxy qui faisait des siennes. Cependant, l’autre serveur IRC était (et est toujours) là (bien qu’il n’ait pas désactivé le CTCP pour le moment - voir [1]), nous avons donc pu assouvir notre besoin d’IRC :)

[1] http://ugha.i2p/HowTo/IrcAnonymityGuide

* 2) 0.5 progress

Ça avance, toujours plus loin !  Ok, je suppose que je devrais entrer un peu plus dans les détails que ça.  J’ai enfin implémenté et testé la nouvelle cryptographie de routage des tunnel (youpi !), mais au cours de discussions nous avons trouvé un endroit où il pourrait y avoir une fuite d’anonymat à un niveau, donc c’est en cours de révision (le premier saut aurait su qu’il était le premier saut, ce qui est mauvais.  mais vraiment vraiment facile à corriger).  Quoi qu’il en soit, j’espère mettre à jour et publier bientôt la documentation et le code à ce sujet, et publier plus tard la documentation sur le reste du fonctionnement des tunnel 0.5 / pooling (mise en pool) / etc.  Plus de nouvelles quand il y en aura.

* 3) 0.6 status

(quoi !?)

Mule a commencé à étudier le transport UDP, et nous avons sollicité zab pour son retour d’expérience sur le code UDP de LimeWire. Tout cela est très prometteur, mais il reste encore beaucoup de travail à accomplir (et cela n’est prévu que dans plusieurs mois sur la feuille de route [2]). Des idées ou des suggestions ? Impliquez-vous et aidez à orienter l’effort vers ce qui doit être fait !

[2] http://www.i2p.net/roadmap#0.6

* 4) azneti2p

J’ai presque mouillé mon pantalon quand j’ai eu l’info, mais on dirait que l’équipe d’azureus a développé un plugin I2P, permettant à la fois l’utilisation anonyme de trackers et des communications de données anonymes ! Plusieurs torrents fonctionnent également au sein d’une seule destination I2P, et ça utilise directement I2PSocket, ce qui permet une intégration étroite avec la bibliothèque de streaming. Le plugin azneti2p en est encore à ses débuts avec cette version 0.1, et de nombreuses optimisations ainsi que des améliorations d’ergonomie sont en préparation, mais si vous êtes prêt à mettre les mains dans le cambouis, passez sur i2p-bt sur les réseaux IRC d’I2P et venez vous joindre à la fête :)

Pour les plus aventureux, téléchargez la dernière version d’azureus [3], consultez leur tutoriel I2P [4] et récupérez le plugin [5].

[3] http://azureus.sourceforge.net/index_CVS.php [4] http://azureus.sourceforge.net/doc/AnonBT/i2p/I2P_howto.htm [5] http://azureus.sourceforge.net/plugin_details.php?plugin=azneti2p

duck prend des mesures héroïques pour maintenir la compatibilité avec i2p-bt, et il y a du développement frénétique sur #i2p-bt pendant que j’écris ces lignes, alors restez à l’affût d’une nouvelle version d’i2p-bt très bientôt.

* 5) fbsd

Grâce au travail de lioux, il existe désormais un port FreeBSD pour i2p [6]. Même si nous ne cherchons pas vraiment à multiplier les installations spécifiques aux distributions, il promet de le maintenir à jour si nous l’avertissons suffisamment à l’avance d’une nouvelle version. Cela devrait être utile aux utilisateurs de FreeBSD-CURRENT - merci lioux !

[6] http://www.freshports.org/net/i2p/

* 6) hosts.txt as WoT

Maintenant que la version 0.4.2.6 inclut le carnet d’adresses de Ragnarok, le processus consistant à maintenir votre hosts.txt alimenté en nouvelles entrées est entre les mains de chaque utilisateur. Non seulement cela, mais vous pouvez considérer les abonnements au carnet d’adresses comme une toile de confiance du pauvre - vous importez de nouvelles entrées depuis un site auquel vous faites confiance pour vous présenter de nouvelles destinations (par défaut dev.i2p et duck.i2p).

Avec cette capacité s’ouvre une dimension entièrement nouvelle - la possibilité pour les utilisateurs de choisir quels sites ils souhaitent, en substance, référencer dans leurs hosts.txt et lesquels ne pas référencer. Bien qu’il y ait une place pour le libre accès public sans contrôle qui s’est produit par le passé, maintenant que le système de nommage n’est pas seulement théorique mais, en pratique, entièrement distribué, les utilisateurs devront définir leurs propres politiques concernant la publication des destinations d’autrui.

L’élément important en coulisses ici, c’est qu’il s’agit d’une occasion d’apprentissage pour la communauté I2P.  Auparavant, gott et moi essayions d’aider à faire avancer la question du nommage en publiant le site de gott sous jrandom.i2p (c’est lui qui a demandé ce site en premier - pas moi, et je n’ai absolument aucun contrôle sur le contenu de cette URL).  Nous pouvons maintenant commencer à explorer la manière dont nous allons gérer les sites qui ne figurent pas dans http://dev.i2p.net/i2p/hosts.txt ou sur forum.i2p.  Le fait de ne pas être publié à ces emplacements n’empêche en rien un site de fonctionner - votre hosts.txt n’est que votre carnet d’adresses local.

Enfin, trêve de bavardages, je voulais simplement mettre tout le monde au courant pour que nous puissions tous voir ce qu’il y a à faire.

* 7) ???

Waouh, ça fait beaucoup de choses. Semaine chargée, et je ne prévois pas que ça ralentisse de sitôt. Alors, passe à la réunion dans quelques minutes et on pourra parler de tout ça.

=jr
