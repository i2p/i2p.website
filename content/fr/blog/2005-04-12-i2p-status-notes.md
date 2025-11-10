---
title: "Notes d'état I2P du 2005-04-12"
date: 2005-04-12
author: "jr"
description: "Mise à jour hebdomadaire portant sur les correctifs netDb de la version 0.5.0.6, les progrès du transport UDP SSU, les résultats du profilage bayésien des pairs et le développement de Q"
categories: ["status"]
---

Salut à tous, c'est à nouveau l'heure de la mise à jour

* Index

1) Statut du réseau 2) Statut SSU 3) Profilage bayésien des pairs 4) Statut Q 5) ???

* 1) Net status

La version 0.5.0.6 de la semaine dernière semble avoir corrigé les problèmes de netDb que nous constations (hourra). Les sites et services sont bien plus fiables qu’ils ne l’étaient sous 0.5.0.5, bien qu’il y ait eu quelques signalements indiquant qu’un site ou un service pouvait devenir injoignable après quelques jours de fonctionnement continu.

* 2) SSU status

Beaucoup de progrès ont été accomplis sur le code UDP 0.6, avec une première série de commits déjà effectuée dans CVS. Ce n’est pas encore quelque chose que vous pourriez réellement utiliser, mais les fondamentaux sont en place. La négociation de session fonctionne bien et l’acheminement semi-fiable des messages se comporte comme prévu. Il reste toutefois beaucoup de travail, des cas de test à écrire et des situations atypiques à déboguer, mais c’est un progrès.

Si tout se passe bien, nous pourrions effectuer des tests alpha la semaine prochaine, uniquement pour les personnes capables de configurer explicitement leurs pare-feu/NAT. J'aimerais d'abord mettre au point le fonctionnement général avant d'ajouter le gestionnaire de relais, d'ajuster le netDb pour une expiration plus rapide des routerInfo (informations du routeur) et de sélectionner les relais à publier. Je vais également en profiter pour effectuer toute une série de tests, car plusieurs facteurs critiques de mise en file d'attente sont en cours de traitement.

* 3) Bayesian peer profiling

bla travaille d'arrache-pied sur des révisions de la manière dont nous décidons quels pairs utiliser comme relais dans les tunnels, et même si bla n'a pas pu assister à la réunion, il y a des données intéressantes à présenter :

<+bla> J'ai effectué des mesures directes de vitesse des nœuds : j'ai profilé environ 150 nœuds en utilisant des tunnels OB de longueur 0, des tunnels IB de longueur 1, batching-interval = 0ms
<+bla> De plus, je viens de faire une estimation de vitesse _très_ basique et _préliminaire_ en utilisant une classification bayésienne naïve
<+bla> Cette dernière a été faite en utilisant les longueurs de tunnels expl. par défaut
<+bla> L'intersection entre l'ensemble des nœuds pour lesquels je dispose d'une "ground truth" (référence réelle), et l'ensemble des nœuds dans les mesures actuelles, est de 117 nœuds
<+bla> Les résultats ne sont pas _si_ mauvais, mais ils ne sont pas très impressionnants non plus
<+bla> Voir http://theland.i2p/estspeed.png
<+bla> La séparation de base entre très lents et rapides est plutôt correcte, mais la séparation fine entre les pairs plus rapides pourrait être bien meilleure
<+jrandom2p> hmm, comment les valeurs réelles sont-elles calculées - est-ce le RTT complet ou est-ce RTT/longueur ?
<+bla> En utilisant les tunnels expl. normaux, il est quasiment impossible d'empêcher les retards de batching (regroupement par lots).
<+bla> Les valeurs réelles sont les valeurs de ground-truth : celles obtenues avec OB=0 et IB=1
<+bla> (et variance=0, et aucun retard de batching)
<+jrandom2p> les résultats ont l'air plutôt bons d'ici quand même
<+bla> Les temps estimés sont ceux obtenus par inférence bayésienne à partir de tunnels expl. _réels_ de longueur 2 +/- 1
<+bla> Ceci est obtenu à partir de 3000 RTT, enregistrés sur une période d'environ 3 heures (c'est long)
<+bla> Ça suppose (pour le moment) que la vitesse des pairs est statique. Je dois encore implémenter la pondération
<+jrandom2p> ça déchire.  beau travail bla
<+jrandom2p> hmm, donc l'estimation devrait être égale à 1/4 de la valeur réelle
<+bla> jrandom : Non : Tous les RTT mesurés (en utilisant les tunnels expl. normaux), sont corrigés du nombre de sauts dans l'aller-retour
<+jrandom2p> ah ok
<+bla> Ce n'est qu'après cela que le classificateur bayésien est entraîné
<+bla> Pour l'instant, je regroupe les temps mesurés par saut en 10 classes : 50, 100, ..., 450 ms, et une classe supplémentaire >500 ms
<+bla> Par exemple, les petits délais par saut pourraient être pondérés avec un facteur plus grand, tout comme les échecs complets (>60000 ms).
<+bla> Cela dit... 65 % des temps estimés se situent à moins de 0,5 écart-type du temps réel du nœud
<+bla> Cependant, il faut refaire ce calcul, car l'écart-type est fortement influencé par les échecs >60000 ms

Après de plus amples discussions, bla a établi une comparaison avec le calculateur de vitesse existant, publiée à l’adresse http://theland.i2p/oldspeed.png Des miroirs de ces PNG sont disponibles à http://dev.i2p.net/~jrandom/estspeed.png et http://dev.i2p.net/~jrandom/oldspeed.png

(pour la terminologie, IB=sauts de tunnel entrant, OB=sauts de tunnel sortant, et après quelques clarifications, les mesures "ground truth" (valeur de référence) ont été obtenues avec 1 saut de tunnel sortant et 0 saut de tunnel entrant, et non l'inverse)

* 4) Q status

Aum a également beaucoup progressé sur Q, en travaillant tout récemment sur une interface client Web. La prochaine version de Q ne sera pas rétrocompatible, car elle inclut toute une série de nouvelles fonctionnalités, mais je suis sûr que nous aurons plus d’informations de la part d’Aum quand il y aura davantage à annoncer :)

* 5) ???

C’est à peu près tout pour le moment (je dois boucler ça avant l’heure de la réunion). Ah, au passage, il semble que je vais déménager plus tôt que prévu, donc il se peut que certaines dates de la feuille de route se décalent pendant que je serai en transit vers l’endroit où je finirai par atterrir. Bref, passez sur le canal dans quelques minutes pour nous harceler avec de nouvelles idées !

=jr
