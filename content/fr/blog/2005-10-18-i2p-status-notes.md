---
title: "Notes d'état I2P du 2005-10-18"
date: 2005-10-18
author: "jr"
description: "Mise à jour hebdomadaire couvrant le succès de la version 0.6.1.3, la discussion sur la collaboration avec Freenet, l’analyse des attaques d’amorçage des tunnels, les progrès concernant le bogue de téléversement d’I2Phex, et la prime relative au NAT symétrique"
categories: ["status"]
---

Salut tout le monde, c'est encore mardi

* Index

1) 0.6.1.3
2) Freenet, I2P et les darknets (oh là là)
3) Attaques d’amorçage de tunnel
4) I2Phex
5) Syndie/Sucker
6) ??? [prime de 500+ pour NAT symétrique]

* 1) 0.6.1.3

Vendredi dernier, nous avons publié une nouvelle version 0.6.1.3, et avec 70 % du réseau mis à jour, les retours ont été très positifs. Les nouvelles améliorations SSU semblent avoir réduit les retransmissions inutiles, permettant une utilisation plus efficace de la bande passante à des débits plus élevés, et à ma connaissance, il n’y a pas eu de problèmes majeurs avec le proxy IRC ni avec les améliorations de Syndie.

Il convient de noter qu’Eol a proposé une prime pour la prise en charge du NAT symétrique sur rentacoder[1], nous pouvons donc espérer des progrès sur ce front !

[1] http://rentacoder.com/RentACoder/misc/BidRequests/ShowBidRequest.asp?lngBidRequestId=349320

* 2) Freenet, I2P, and darknets (oh my)

Nous avons enfin bouclé ce fil de discussion de plus de 100 messages, avec une vision plus claire des deux réseaux, de leur place, et de la marge dont nous disposons pour une collaboration plus poussée. Je ne rentrerai pas ici dans le détail des topologies ou des modèles de menace auxquels ils sont le mieux adaptés, mais vous pouvez consulter les listes si vous voulez en savoir plus. Côté collaboration, j’ai envoyé à toad quelques exemples de code pour réutiliser notre transport SSU, ce qui pourrait être utile à l’équipe Freenet à court terme, et par la suite nous pourrions travailler ensemble pour offrir du premix routing (routage prémélangé) aux utilisateurs de Freenet dans des environnements où I2P est viable. À mesure que Freenet progresse, nous pourrions aussi parvenir à faire fonctionner Freenet au-dessus d’I2P en tant qu’application cliente, permettant une distribution automatisée de contenu entre les utilisateurs qui l’exécutent (par exemple en diffusant des archives et des messages Syndie), mais nous verrons d’abord comment fonctionneront les systèmes de charge et de distribution de contenu prévus par Freenet.

* 3) Tunnel bootstrap attacks

Michael Rogers a pris contact au sujet de nouvelles attaques intéressantes contre la création de tunnel d’I2P [2][3][4]. L’attaque principale (mener avec succès une attaque par prédécesseur pendant tout le processus d’amorçage) est intéressante, mais pas vraiment pratique - la probabilité de réussite est (c/n)^t, avec c attaquants, n pairs dans le réseau, et t tunnels construits par la cible (sur l’ensemble de sa durée de vie) - inférieure à la probabilité qu’un adversaire prenne le contrôle de tous les h sauts dans un tunnel (P(success) = (c/n)^h) après que le router a construit h tunnels.

Michael a publié une autre attaque sur la liste, que nous examinons en ce moment ; vous pourrez donc la suivre là-bas aussi.

[2] http://dev.i2p.net/pipermail/i2p/2005-October/001005.html [3] http://dev.i2p.net/pipermail/i2p/2005-October/001008.html [4] http://dev.i2p.net/pipermail/i2p/2005-October/001006.html

* 4) I2Phex

Striker fait encore des progrès sur le bogue de téléversement, et les rapports indiquent qu’il l’a isolé. Avec un peu de chance, cela sera intégré dans CVS ce soir, et sera publié en version 0.1.1.33 peu après. Gardez un œil sur le forum [5] pour plus d’informations.

[5] http://forum.i2p.net/viewforum.i2p?f=25

La rumeur dit que redzara fait de bons progrès pour fusionner à nouveau avec la branche principale de Phex ; espérons qu'avec l'aide de Gregor, nous pourrons tout remettre à jour bientôt !

* 5) Syndie/Sucker

dust a également travaillé d’arrache-pied avec Sucker, avec du code qui permet d’alimenter Syndie avec davantage de données RSS/Atom. Peut-être pourrons-nous intégrer plus étroitement Sucker et le post CLI à Syndie, voire une interface web pour planifier l’importation de divers flux RSS/Atom dans différents blogs. Nous verrons...

* 6) ???

Il se passe beaucoup d’autres choses au-delà de ce qui précède, mais voilà l’essentiel de ce dont je suis au courant. Si quelqu’un a des questions/préoccupations, ou veut soulever d’autres points, venez faire un tour à la réunion ce soir à 20 h UTC sur #i2p!

=jr
