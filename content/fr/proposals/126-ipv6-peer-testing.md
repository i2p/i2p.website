---
title: "Test de Pair-à-Pair IPv6"
number: "126"
author: "zzz"
created: "2016-05-02"
lastupdated: "2018-03-19"
status: "Closed"
thread: "http://zzz.i2p/topics/2119"
target: "0.9.27"
implementedin: "0.9.27"
---

## Vue d'ensemble

Cette proposition vise à implémenter le test de pair-à-pair SSU pour IPv6.
Implémenté dans la version 0.9.27.


## Motivation

Nous ne pouvons pas déterminer et suivre de manière fiable si notre adresse IPv6 est bloquée par un pare-feu.

Lorsque nous avons ajouté la prise en charge de l’IPv6 il y a des années, nous avons supposé que l’IPv6 n’était jamais bloqué par un pare-feu.

Plus récemment, dans la version 0.9.20 (mai 2015), nous avons séparé le statut de connectivité v4/v6 en interne (ticket #1458).
Voir ce ticket pour des informations détaillées et des liens.

Si vous avez à la fois v4 et v6 bloqués par un pare-feu, vous pouvez simplement forcer le blocage dans la section de configuration TCP sur /confignet.

Nous n’avons pas de test de pair-à-pair pour v6. C'est interdit dans la spécification SSU.
Si nous ne pouvons pas tester régulièrement la connectivité v6, nous ne pouvons pas raisonnablement passer d'un état accessible à un état inaccessible et vice versa.
Ce qu’il nous reste, c’est de supposer que nous sommes accessibles si nous recevons une connexion entrante,
et de supposer que nous ne le sommes pas si nous n’avons pas reçu de connexion entrante depuis un moment.
Le problème est qu'une fois que vous déclarez être inaccessible, vous ne publiez plus votre IP v6,
et ensuite vous n'en recevez plus (après l'expiration du RI dans la base de données réseau de tout le monde).


## Conception

Implémenter le test de pair-à-pair pour IPv6,
en supprimant les restrictions précédentes qui limitaient le test de pair-à-pair à IPv4 uniquement.
Le message de test de pair a déjà un champ pour la longueur de l'IP.


## Spécification

Dans la section Capabilities de l'aperçu SSU, faire l'ajout suivant :

Jusqu'à la version 0.9.26, le test de pair-à-pair n’était pas pris en charge pour les adresses IPv6, et
la capacité 'B', si présente pour une adresse IPv6, doit être ignorée.
À partir de la version 0.9.27, le test de pair-à-pair est pris en charge pour les adresses IPv6, et
la présence ou l'absence de la capacité 'B' dans une adresse IPv6
indique le support réel (ou l'absence de support).


Dans les sections de Test de Pair-à-Pair de l'aperçu SSU et de la spécification SSU, faire les changements suivants :

Notes IPv6 :
Jusqu'à la version 0.9.26, seul le test des adresses IPv4 est pris en charge.
Par conséquent, toute communication Alice-Bob et Alice-Charlie doit être via IPv4.
Cependant, la communication Bob-Charlie peut être via IPv4 ou IPv6.
L'adresse d'Alice, quand elle est spécifiée dans le message PeerTest, doit être de 4 octets.
À partir de la version 0.9.27, le test des adresses IPv6 est pris en charge, et la communication Alice-Bob et Alice-Charlie peut se faire via IPv6,
si Bob et Charlie indiquent le support avec une capacité 'B' dans leur adresse IPv6 publiée.

Alice envoie la requête à Bob en utilisant une session existante sur le transport (IPv4 ou IPv6) qu'elle souhaite tester.
Lorsque Bob reçoit une requête d'Alice via IPv4, Bob doit sélectionner un Charlie qui annonce une adresse IPv4.
Lorsque Bob reçoit une requête d'Alice via IPv6, Bob doit sélectionner un Charlie qui annonce une adresse IPv6.
La communication réelle Bob-Charlie peut se faire via IPv4 ou IPv6 (c'est-à-dire indépendamment du type d'adresse d'Alice).


## Migration

Les routeurs peuvent soit :

1) Ne pas incrémenter leur version à 0.9.27 ou plus

2) Supprimer la capacité 'B' de toute adresse SSU IPv6 publiée

3) Implémenter le test de pair-à-pair IPv6
