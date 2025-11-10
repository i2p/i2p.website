---
title: "Notes de statut I2P du 2006-02-21"
date: 2006-02-21
author: "jr"
description: "Network issues with 0.6.1.10 release, quick 0.6.1.11 follow-up release, and IE security concerns"
categories: ["status"]
---

Salut tout le monde, c'est encore mardi

* Index

1) État du réseau 2) ???

* 1) Net status

Le réseau traverse une période un peu agitée avec la version 0.6.1.10, due en partie à l’incompatibilité avec les versions antérieures, mais aussi à des bogues inattendus.  Ni la fiabilité ni la disponibilité de la version 0.6.1.10 n’étaient suffisantes, si bien que ces 5 derniers jours ont vu une rafale de correctifs, qui a abouti à la nouvelle version 0.6.1.11 - http://dev.i2p.net/pipermail/i2p/2006-February/001263.html

La plupart des bogues découverts dans la 0.6.1.10 étaient présents depuis la sortie 0.6 en septembre dernier, mais n’étaient pas facilement apparents tant qu’il existait des transports alternatifs sur lesquels se replier (TCP). Mon réseau de test local simule des pertes de paquets, mais ne couvrait pas vraiment le churn des router (rotation/instabilité) et d’autres défaillances réseau persistantes. Le réseau de test _PRE incluait également un ensemble auto-sélectionné de pairs assez fiables, de sorte que des situations importantes n’ont pas été pleinement explorées avant la publication complète. C’est un problème, évidemment, et la prochaine fois nous veillerons à inclure une sélection plus large de scénarios.

* 2) ???

Il se passe pas mal de choses en ce moment, mais la nouvelle version 0.6.1.11 est passée en tête de liste. Le réseau restera un peu instable jusqu’à ce qu’un grand nombre de personnes soient à jour, après quoi le travail continuera d’avancer. À noter que cervantes travaille sur une sorte d’exploit lié au domaine de sécurité d’IE, et même si je ne sais pas s’il est prêt à en expliquer les détails, les résultats préliminaires suggèrent qu’il est viable, donc les personnes soucieuses d’anonymat devraient éviter IE entre-temps (mais ça, vous le saviez déjà ;). Peut-être que cervantes pourra nous en faire un résumé lors de la réunion ?

Bref, c'est tout ce que j'ai à mentionner pour le moment - passez faire un tour à la réunion dans quelques minutes pour dire bonjour !

=jr
