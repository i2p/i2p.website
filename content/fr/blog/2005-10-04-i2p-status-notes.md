---
title: "Notes de statut I2P du 2005-10-04"
date: 2005-10-04
author: "jr"
description: "Mise à jour hebdomadaire portant sur le succès de la version 0.6.1.1 avec 300 à 400 pairs, les efforts de réconciliation du fork i2phex, et les progrès de l’automatisation de Syndie avec des pet names (noms familiers) et des récupérations planifiées"
categories: ["status"]
---

Salut tout le monde, c'est l'heure de nos notes d'avancement hebdomadaires (insérer des applaudissements ici)

* Index

1) 0.6.1.1 2) i2phex 3) syndie 4) ???

* 1) 0.6.1.1

Comme annoncé sur les canaux habituels, la 0.6.1.1 est sortie l’autre jour et, jusqu’à présent, les retours ont été positifs. Le réseau a atteint un niveau stable de 3-400 pairs connus et les performances ont été plutôt bonnes, bien que l’utilisation du CPU ait un peu augmenté. Cela est probablement dû à des bugs de longue date qui permettent à tort à des adresses IP invalides de se faire accepter, ce qui entraîne à son tour un churn (rotation/instabilité des pairs) plus élevé que nécessaire. Des correctifs ont été apportés à cela et à d’autres points dans les builds CVS depuis la 0.6.1.1, donc nous publierons probablement la 0.6.1.2 plus tard cette semaine.

* 2) i2phex

Bien que certains aient pu remarquer des discussions sur divers forums au sujet d’i2phex et du fork de legion, il y a eu des échanges supplémentaires entre legion et moi, et nous travaillons à réunifier les deux. Plus d’informations à ce sujet dès qu’elles seront disponibles.

De plus, redzara travaille d'arrache-pied à fusionner i2phex avec la version actuelle de phex, et striker a proposé d'autres améliorations, si bien que des nouveautés intéressantes sont en préparation.

* 3) syndie

Ragnarok a travaillé d’arrache-pied sur syndie ces derniers jours, en intégrant la base de données de pet names (noms personnalisés) de syndie avec celle du router, ainsi qu’en automatisant la syndication avec des récupérations planifiées depuis des archives distantes sélectionnées. La partie automatisation est terminée et, même s’il reste un peu de travail sur l’UI (interface utilisateur), l’ensemble est en assez bon état !

* 4) ???

Il se passe aussi pas mal d’autres choses ces jours-ci, notamment du travail sur les nouveaux documents d’introduction technique, la migration IRC et la refonte du site web. Si quelqu’un a quelque chose à aborder, venez à la réunion dans quelques minutes et dites bonjour !

=jr
