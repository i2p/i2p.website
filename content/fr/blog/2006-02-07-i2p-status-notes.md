---
title: "I2P Status Notes for 2006-02-07"
date: 2006-02-07
author: "jr"
description: "Progrès des tests du réseau PRE, optimisation à exposant court pour le chiffrement ElGamal, et I2Phex 0.1.1.37 avec prise en charge de gwebcache"
categories: ["status"]
---

Salut à tous, revoilà mardi

* Index

1) Statut du réseau 2) _PRE progression du réseau 3) I2Phex 0.1.1.37 4) ???

* 1) Net status

Il n’y a pas eu de changements significatifs sur le réseau en production au cours de la semaine écoulée, donc l’état du réseau en production n’a pas beaucoup changé. En revanche...

* 2) _PRE net progress

La semaine dernière, j’ai commencé à valider du code rétro-incompatible pour la version 0.6.1.10 sur une branche distincte dans CVS (i2p_0_6_1_10_PRE), et un groupe de bénévoles a aidé à le tester. Ce nouveau réseau _PRE ne peut pas communiquer avec le réseau en production et n’offre aucun anonymat significatif (puisqu’il y a moins de 10 pairs). Grâce aux pen register logs (journaux de type « pen register ») provenant de ces routers, quelques bogues importants, tant dans le nouveau code que dans l’ancien, ont été identifiés et corrigés, tandis que les tests et les améliorations se poursuivent.

Un aspect du nouveau mécanisme cryptographique de création de tunnel est que le créateur doit effectuer à l’avance le lourd chiffrement asymétrique pour chaque saut, tandis que l’ancien mécanisme de création de tunnel ne réalisait le chiffrement que si le saut précédent acceptait de participer au tunnel. Ce chiffrement peut prendre 400-1000ms ou plus, en fonction à la fois des performances du CPU local et de la longueur du tunnel (il effectue un chiffrement ElGamal complet pour chaque saut). Une optimisation actuellement utilisée sur le _PRE net est l’utilisation d’un exposant court [1] - plutôt que d’utiliser un 'x' de 2048bit comme clé ElGamal, nous utilisons un 'x' de 228bit, ce qui est la longueur recommandée pour correspondre à la charge de calcul du problème du logarithme discret. Cela a réduit le temps de chiffrement par saut d’un ordre de grandeur, sans toutefois affecter le temps de déchiffrement.

Il existe de nombreux avis divergents sur l’utilisation d’exposants courts et, dans le cas général, ce n’est pas sûr, mais d’après ce que j’ai pu comprendre, puisque nous utilisons un nombre premier sûr fixe (Oakley group 14 [2]), l’ordre de q devrait convenir. Si quelqu’un a d’autres réflexions dans ce sens, toutefois, je serais intéressé d’en savoir plus.

La principale alternative consiste à passer à un chiffrement 1024 bits (auquel cas nous pourrions alors utiliser un exposant court de 160 bits, peut-être). Cela peut être approprié quoi qu’il en soit et, si cela s’avère trop pénible avec le chiffrement 2048 bits sur le _PRE net, nous pourrions effectuer la transition au sein du _PRE net. Sinon, nous pourrions attendre la version 0.6.1.10, lorsqu’un déploiement plus large du nouveau chiffrement permettra de déterminer si c’est nécessaire. Beaucoup plus d’informations suivront si un tel changement semble probable.

[1] "On Diffie-Hellman Key Agreement with Short Exponents" -     van Oorschot, Weiner à EuroCrypt 96.  copie miroir à l'adresse     http://dev.i2p.net/~jrandom/Euro96-DH.ps [2] http://www.ietf.org/rfc/rfc3526.txt

Quoi qu’il en soit, beaucoup de progrès sur le _PRE net, la plupart des communications à ce sujet se font au sein du canal #i2p_pre sur irc2p.

* 3) I2Phex 0.1.1.37

Complication a fusionné et corrigé le dernier code d’I2Phex pour prendre en charge des gwebcaches compatibles avec le port pycache de Rawn. Cela signifie que les utilisateurs peuvent télécharger I2Phex, l’installer, cliquer sur "Se connecter au réseau", et au bout d’une minute ou deux, il récupérera quelques références à des pairs I2Phex existants et rejoindra le réseau. Plus de prise de tête avec la gestion manuelle des fichiers i2phex.hosts, ni avec le partage manuel des clés (w00t) ! Il y a deux gwebcaches par défaut, mais on peut les modifier ou en ajouter un troisième en changeant les propriétés i2pGWebCache0, i2pGWebCache1 ou i2pGWebCache2 dans i2phex.cfg.

Beau travail, Complication et Rawn !

* 4) ???

C’est à peu près tout pour le moment, ce qui n’est pas plus mal, puisque je suis déjà en retard pour la réunion :) À tout à l’heure sur #i2p

=jr
