---
title: "Notes d'état d'I2P du 2004-11-02"
date: 2004-11-02
author: "jr"
description: "Mise à jour hebdomadaire sur l'état d'I2P couvrant l'état du réseau, des optimisations de la mémoire du noyau, des correctifs de sécurité pour le routage de tunnel, les progrès de la bibliothèque de streaming et les évolutions pour le courriel et BitTorrent"
categories: ["status"]
---

Salut tout le monde, c'est l'heure de la mise à jour hebdomadaire

## Index:

1. Net status
2. Core updates
3. Streaming lib
4. mail.i2p progress
5. BT progress
6. ???

## 1) État du réseau

Globalement comme auparavant - un nombre stable de pairs, des eepsites(I2P Sites) assez accessibles, et de l’irc pendant des heures d’affilée. Vous pouvez jeter un coup d’œil à la joignabilité de diverses eepsites(I2P Sites) via quelques pages différentes: - `http://gott.i2p/sites.html` - `http://www.baffled.i2p/links.html` - `http://thetower.i2p/pings.txt`

## 2) Mises à jour du cœur

Ceux qui traînent sur le canal (ou lisent les logs CVS) ont vu beaucoup de choses se passer, même s’il s’est écoulé un certain temps depuis la dernière version. Une liste complète des changements depuis la version 0.4.1.3 est disponible en ligne, mais il y a deux modifications majeures, l’une bonne et l’autre mauvaise :

La bonne nouvelle, c’est que nous avons considérablement réduit le memory churn (pression d’allocations/désallocations) provoqué par toutes sortes de créations d’objets temporaires complètement folles. J’en ai finalement eu assez de voir le GC s’emballer pendant le débogage de la nouvelle bibliothèque de streaming, alors après quelques jours de profilage, de réglages et d’optimisation, les pires parties ont été nettoyées.

La mauvaise, c’est une correction de bogue concernant la façon dont certains messages acheminés par tunnel sont traités - il arrivait dans certaines situations qu’un message soit envoyé directement au router ciblé plutôt que d’être acheminé par tunnel avant la livraison, ce qui pouvait être exploité par un adversaire qui sait un peu coder. Nous effectuons désormais correctement un routage par tunnel en cas de doute.

Cela peut sembler bien, mais la partie 'mauvaise', c’est que cela implique un surcroît de latence dû aux sauts supplémentaires, même s’il s’agit de sauts qui auraient de toute façon été nécessaires.

Il y a également d’autres activités de débogage en cours dans le cœur, donc il n’y a pas encore eu de version officielle - CVS HEAD est 0.4.1.3-8. Dans les prochains jours, nous publierons probablement une version 0.4.1.4, juste pour régler tout ça. Elle ne contiendra pas la nouvelle bibliothèque de streaming, bien sûr.

## 3) Bibliothèque de streaming

À propos de la bibliothèque de streaming, nous avons fait beaucoup de progrès, et la comparaison côte à côte de l’ancienne et de la nouvelle bibliothèque est prometteuse. Cependant, il reste du travail à faire et, comme je l’ai dit la dernière fois, nous n’allons pas précipiter la sortie. Cela signifie que la feuille de route a pris du retard, probablement de l’ordre de 2 à 3 semaines. Plus de détails lorsqu’ils seront disponibles.

## 4) Avancement de mail.i2p

Beaucoup de nouveautés cette semaine - des proxies d'entrée et de sortie opérationnels ! Voir www.postman.i2p pour plus d'informations.

## 5) Progression BT

Il y a eu ces derniers temps une forte activité autour du portage d’un client BitTorrent, ainsi que de la mise à jour de certains paramètres de tracker. Peut-être pourrons-nous obtenir des points d’avancement de la part des personnes impliquées pendant la réunion.

## 6) ???

C'est tout pour moi. Désolé pour le retard, j'avais complètement oublié cette histoire de changement d'heure. Bref, à tout à l'heure, tout le monde.

=jr
