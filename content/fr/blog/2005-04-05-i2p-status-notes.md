---
title: "Notes d'état d'I2P du 2005-04-05"
date: 2005-04-05
author: "jr"
description: "Mise à jour hebdomadaire portant sur les problèmes de la version 0.5.0.5, la recherche sur le profilage bayésien des pairs et l'avancement de l'application Q"
categories: ["status"]
---

Salut tout le monde, c'est l'heure de la mise à jour hebdomadaire

* Index

1) 0.5.0.5 2) Profilage bayésien des pairs 3) Q 4) ???

* 1) 0.5.0.5

La version 0.5.0.5 publiée la semaine dernière a connu des hauts et des bas - la modification majeure visant à contrer certaines attaques dans le netDb semble fonctionner comme prévu, mais elle a mis en lumière quelques bogues longtemps négligés dans le fonctionnement du netDb. Cela a provoqué d'importants problèmes de fiabilité, en particulier pour les eepsites(I2P Sites). Les bogues ont toutefois été identifiés et corrigés dans CVS, et ces correctifs, parmi quelques autres, seront publiés sous la forme d'une version 0.5.0.6 d'ici demain.

* 2) Bayesian peer profiling

bla a mené des recherches visant à améliorer notre profilage des pairs en exploitant un filtrage bayésien simple à partir des statistiques collectées [1]. Cela paraît très prometteur, bien que je ne sache pas exactement où cela en est pour le moment - peut-être pourrions-nous obtenir une mise à jour de la part de bla pendant la réunion ?

[1] http://forum.i2p.net/viewtopic.php?t=598     http://theland.i2p/nodemon.html

* 3) Q

Il y a de nombreuses avancées autour de l'application Q d'aum, tant au niveau des fonctionnalités de base que grâce à quelques personnes qui développent diverses interfaces XML-RPC. La rumeur veut que nous pourrions voir une nouvelle build de Q ce week-end, avec toute une série de nouveautés décrites sur http://aum.i2p/q/

* 4) ???

Ok, ouais, quelques notes de statut très brèves, car je me suis trompé de fuseaux horaires *encore* (en fait, je me suis aussi trompé de jour, je pensais que c’était lundi jusqu’à il y a quelques heures). Quoi qu’il en soit, il se passe plein de choses qui ne sont pas mentionnées ci-dessus, alors passez à la réunion pour voir ce qui se passe !

=jr
