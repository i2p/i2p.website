---
title: "Notes d'état I2P du 2005-11-01"
date: 2005-11-01
author: "jr"
description: "Mise à jour hebdomadaire couvrant la réussite de la sortie de la version 0.6.1.4, l’analyse des attaques de bootstrap, les correctifs de sécurité d’I2Phex 0.1.1.34, le développement de l’application vocale voi2p et l’intégration du flux RSS de Syndie"
categories: ["status"]
---

Salut à tous, c'est reparti pour notre rendez-vous hebdomadaire

* Index

1) 0.6.1.4 et statut du réseau 2) amorçages, prédécesseurs, adversaires passifs globaux, et CBR 3) i2phex 0.1.1.34 4) application voi2p 5) syndie et sucker 6) ???

* 1) 0.6.1.4 and net status

La sortie de la version 0.6.1.4 samedi dernier semble s’être déroulée plutôt bien - 75 % du réseau a déjà été mis à jour (merci !), et la plupart des autres sont de toute façon en 0.6.1.3. Tout semble fonctionner raisonnablement bien, et même si je n’ai pas reçu beaucoup de retours à ce sujet - ni positifs ni négatifs, j’imagine que vous vous plaindriez bruyamment si ça se passait mal :)

En particulier, je serais intéressé par tout retour de la part de personnes utilisant des connexions par modem commuté, car les tests que j’ai effectués ne sont qu’une simulation de base de ce type de connexion.

* 2) boostraps, predecessors, global passive adversaries, and CBR

Il y a eu beaucoup plus de discussions sur la liste de diffusion à propos de quelques idées, avec un résumé des attaques de bootstrap en ligne [1]. J’ai fait des progrès en spécifiant la crypto pour l’option 3 et, même si rien n’a encore été publié, c’est assez simple.

[1] http://dev.i2p.net/pipermail/i2p/2005-October/001146.html

Des discussions supplémentaires ont eu lieu sur la manière d’améliorer la résistance face à des adversaires puissants au moyen de tunnels à débit binaire constant (CBR), et même si nous avons la possibilité d’explorer cette piste, elle est actuellement prévue pour I2P 3.0, car son bon usage nécessite des ressources importantes et aurait probablement un impact mesurable sur les personnes prêtes à utiliser I2P avec une telle surcharge, ainsi que sur les groupes qui seraient ou ne seraient même pas en mesure de le faire.

* 3) I2Phex 0.1.1.34

Samedi dernier, nous avons également publié une nouvelle version d'I2Phex [2], corrigeant une fuite de descripteurs de fichiers qui finirait par entraîner une défaillance d'I2Phex (merci Complication !) et supprimant du code qui permettait à des tiers d’ordonner à distance à votre instance I2Phex de télécharger certains fichiers particuliers (merci GregorK !). La mise à jour est fortement recommandée.

Il y a également eu une mise à jour de la version CVS (pas encore publiée) qui résout certains problèmes de synchronisation — Phex part du principe que certaines opérations réseau sont traitées immédiatement, alors qu’I2P peut parfois mettre un certain temps à faire les choses :) Cela se manifeste par le gel de l’interface graphique (GUI) pendant un moment, des téléchargements ou téléversements qui se bloquent, ou des connexions refusées (et peut‑être de quelques autres façons). Elle n’a pas encore été beaucoup testée, mais sera probablement intégrée dans la 0.1.1.35 cette semaine. Je suis sûr que d’autres nouvelles seront publiées sur le forum quand il y en aura davantage.

[2] http://forum.i2p.net/viewtopic.php?t=1143

* 4) voi2p app

Aum travaille d'arrache-pied sur sa nouvelle application de voix (et de texte) via I2P, et même si je ne l’ai pas encore vue, ça semble prometteur. Peut-être qu’Aum pourra nous donner des nouvelles lors de la réunion, ou bien nous pouvons simplement attendre patiemment la première version alpha :)

* 5) syndie and sucker

dust travaille d’arrache-pied sur syndie et sucker, et la dernière build CVS d’I2P vous permet désormais d’importer automatiquement du contenu depuis des flux RSS et Atom et de le publier sur votre blog syndie. Pour l’instant, vous devez ajouter explicitement lib/rome-0.7.jar et lib/jdom.jar à votre wrapper.config (wrapper.java.classpath.20 et 21), mais nous les intégrerons pour que cela ne soit plus nécessaire plus tard. C’est encore en cours de développement, et rome 0.8 (pas encore publiée) semble offrir des fonctionnalités vraiment intéressantes, comme la possibilité de récupérer les enclosures (pièces jointes des flux) à partir d’un flux, que sucker pourra ensuite importer comme pièce jointe à une publication syndie (pour l’instant, il gère déjà aussi les images et les liens !)

Comme tous les flux RSS, il semble y avoir quelques incohérences dans la manière dont le contenu est intégré, donc certains flux passent mieux que d’autres. Je pense que si des personnes pouvaient aider à le tester avec différents flux et informer dust de tout problème sur lequel il bugue, cela pourrait être utile. Quoi qu’il en soit, tout ça a l’air plutôt enthousiasmant, beau travail, dust !

* 6) ???

C’est à peu près tout pour le moment, mais si quelqu’un a des questions ou souhaite approfondir certains points, passez à la réunion à 20 h GMT (n’oubliez pas l’heure d’été !)

=jr
