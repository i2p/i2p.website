---
title: "Notes d'état I2P du 2006-01-03"
date: 2006-01-03
author: "jr"
description: "Mise à jour du Nouvel An couvrant la stabilité de la version 0.6.1.8, les résultats des tests de charge et le profilage des pairs pour l'optimisation du débit, ainsi qu'un bilan complet de 2005 avec un aperçu de la feuille de route 2006"
categories: ["status"]
---

Salut à tous, bonne année ! Replongeons dans nos notes de statut hebdomadaires après une semaine sans elles -

* Index

1) État du réseau et 0.6.1.8 2) Résultats des tests de charge et profilage des pairs 3) Bilan 2005 / aperçu 2006 / ???

* 1) Net status and 0.6.1.8

Il y a quelques semaines, nous avons publié 0.6.1.8 et les retours du terrain indiquent que les modifications de zzz ont beaucoup aidé, et que les choses semblent assez stables sur le réseau, même avec l’augmentation substantielle du trafic réseau ces derniers temps (la moyenne semble avoir doublé au cours du dernier mois, selon stats.i2p). I2PSnark semble aussi assez bien fonctionner - bien que nous ayons rencontré quelques accrocs, nous en avons repéré et corrigé la plupart dans les versions suivantes. Il n’y a pas eu beaucoup de retours concernant la nouvelle interface de blog de Syndie, mais on observe une légère hausse du trafic de Syndie (en partie due à la découverte par protocol de l’importeur RSS/Atom de dust :)

* 2) Load testing results and peer profiling

Depuis quelques semaines, j’essaie de cerner précisément notre goulet d’étranglement de débit. Les différents composants logiciels sont tous capables d’acheminer des données à des débits bien supérieurs à ceux que l’on observe généralement pour des communications de bout en bout sur I2P, donc j’effectue des mesures de performance sur le réseau en production avec du code personnalisé pour les soumettre à des tests de charge. La première série de tests, consistant à construire des tunnels entrants à un seul saut à travers tous les routers du réseau et à transmettre des données via ce tunnel au plus vite, a donné des résultats très prometteurs, avec des routers gérant des débits dans l’ordre de grandeur attendu de leurs capacités (par ex. la plupart ne gérant qu’une moyenne historique de 4-16KBps, mais d’autres poussant 20-120KBps à travers un seul tunnel). Ce test a constitué une bonne base de référence pour des explorations ultérieures et a montré que le traitement du tunnel lui-même est capable de pousser bien plus que ce que l’on observe habituellement.

Les tentatives de reproduire ces résultats via des tunnels en conditions réelles n’ont pas été aussi concluantes. Ou, peut-être pourrait-on dire qu’elles ont été plus concluantes, puisqu’elles ont montré un débit similaire à ce que nous observons actuellement, ce qui signifiait que nous étions sur la bonne voie. En revenant aux résultats des tests 1hop, j’ai modifié le code pour sélectionner des pairs que j’avais identifiés manuellement comme rapides et j’ai relancé les tests de charge via des tunnels en conditions réelles avec cette sélection de pairs "truquée", et même si cela n’a pas atteint la barre des 120KBps, cela a montré une amélioration raisonnable.

Malheureusement, demander aux gens de sélectionner manuellement leurs pairs pose de sérieux problèmes tant pour l’anonymat que, eh bien, l’ergonomie, mais, armé des données issues des tests de charge, il semble y avoir une issue. Ces derniers jours, j’ai expérimenté une nouvelle méthode de profilage des pairs en fonction de leur vitesse - en surveillant essentiellement leur débit maximal soutenu, plutôt que leur latence récente. Des implémentations naïves se sont avérées assez efficaces, et même si elle n’a pas choisi exactement les pairs que j’aurais sélectionnés manuellement, elle s’en est plutôt bien sortie. Il reste toutefois quelques détails à régler, comme s’assurer que nous sommes capables de promouvoir les tunnels exploratoires au niveau rapide, mais je mène actuellement quelques expériences dans ce sens.

Dans l’ensemble, je pense que nous approchons de la fin de cette phase d’optimisation du débit, car nous poussons contre le goulot d’étranglement le plus étroit et l’élargissons. Je suis sûr que nous nous heurterons au prochain assez vite, et cela ne nous donnera certainement pas des débits Internet normaux, mais ça devrait aider.

* 3) 2005 review / 2006 preview / ???

Dire que 2005 a marqué une avancée majeure est un euphémisme - nous avons amélioré I2P de nombreuses façons dans les 25 versions publiées l’année dernière, quintuplé la taille du réseau, déployé plusieurs nouvelles applications clientes (Syndie, I2Phex, I2PSnark, I2PRufus), migré vers le nouveau réseau IRC irc2p de postman et cervantes, et vu fleurir quelques eepsites(I2P Sites) utiles (tels que stats.i2p de zzz, orion.i2p d’orion, et les services de proxy et de surveillance de tino, pour n’en citer que quelques-uns). La communauté a également gagné en maturité, en grande partie grâce aux efforts de support de Complication et d’autres sur le forum et dans les canaux, et la qualité ainsi que la diversité des rapports de bogues provenant de tous les secteurs se sont nettement améliorées. Le soutien financier continu de la communauté a été impressionnant et, même s’il n’est pas encore au niveau nécessaire pour un développement entièrement durable, nous disposons d’une marge qui peut me nourrir pendant l’hiver.

À tous ceux qui ont été impliqués au cours de l’année écoulée, que ce soit techniquement, socialement ou financièrement, merci pour votre aide !

2006 va être une grande année pour nous, avec la 0.6.2 qui arrive cet hiver, notre version 1.0 prévue pour le printemps ou l'été, et la 2.0 à l'automne, si ce n'est pas plus tôt. C'est l'année où nous verrons ce que nous pouvons faire, et le travail dans la couche applicative sera encore plus crucial qu'auparavant. Donc si vous avez des idées, c'est le moment de vous y mettre :)

Quoi qu'il en soit, notre réunion de suivi hebdomadaire commence dans quelques minutes, donc si vous avez quelque chose que vous souhaitez discuter plus en détail, passez sur #i2p aux endroits habituels [1] et venez dire bonjour !

=jr [1] http://forum.i2p.net/viewtopic.php?t=952
