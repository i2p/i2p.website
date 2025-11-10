---
title: "Notes d'état d'I2P du 2004-11-16"
date: 2004-11-16
author: "jr"
description: "Mise à jour hebdomadaire sur l’état d’I2P couvrant les problèmes de congestion du réseau, les avancées de la bibliothèque de streaming, les progrès de BitTorrent et les plans pour les prochaines versions"
categories: ["status"]
---

Salut à tous, c'est encore mardi

## Index

1. Congestion
2. Streaming
3. BT
4. ???

## 1) Congestion

Je sais, je romps avec l'habitude d'intituler le point 1 "État du réseau", mais cette semaine "congestion" semble approprié. Le réseau lui-même fonctionnait plutôt bien, mais à mesure que l'utilisation de bittorrent augmentait, les choses ont commencé à s'engorger de plus en plus, conduisant, pour l'essentiel, à un effondrement dû à la congestion.

C’était attendu, et cela ne fait que renforcer notre plan - publier la nouvelle bibliothèque de streaming, et refondre notre gestion des tunnels afin de disposer de données suffisantes sur les pairs, utilisables lorsque nos pairs rapides défaillent. Il y avait d’autres facteurs en jeu dans les récents problèmes du réseau, mais l’essentiel peut être attribué à l’augmentation de la congestion et aux défaillances de tunnels qui en ont résulté (ce qui a, à son tour, provoqué toutes sortes de sélections de pairs chaotiques).

## 2) Streaming

Il y a eu beaucoup de progrès avec la streaming lib (bibliothèque de streaming), et j’ai configuré un proxy Squid pour l’utiliser via le réseau en production ; je l’utilise fréquemment pour ma navigation web normale. Avec l’aide de mule, nous avons aussi mis les flux à rude épreuve en faisant transiter frost et FUQID à travers le réseau (mon dieu, je n’avais jamais réalisé à quel point frost était agressif avant de faire ça !). Quelques bogues importants de longue date ont été débusqués de cette manière, et des ajustements ont été ajoutés pour mieux gérer un très grand nombre de connexions.

Les flux massifs fonctionnent très bien eux aussi, avec à la fois le démarrage lent et l’évitement de congestion, et les connexions d’envoi/réponse rapides (à la HTTP get+response) font exactement ce qu’elles doivent faire.

Je m’attends à ce que nous mobilisions quelques volontaires pour poursuivre son déploiement au cours des prochains jours et, avec un peu de chance, atteindre bientôt la version 0.4.2. Je ne veux pas prétendre que ce sera au point de faire la vaisselle à votre place, et je suis sûr qu’il y aura des bogues qui nous échapperont, mais cela semble prometteur.

## 3) BT

Mis à part les récents problèmes réseau, le portage i2p-bt a progressé à pas de géant. Je sais que quelques personnes ont téléchargé plus d’un Go de données par son intermédiaire, et les performances ont été conformes aux attentes (en raison de l’ancienne bibliothèque de streaming, ~4 Ko/s par pair dans l’essaim). J’essaie de suivre le travail discuté sur le canal #i2p-bt — peut-être que duck pourrait nous en faire un résumé lors de la réunion ?

## 4) ???

C’est tout pour moi pour l’instant. On se voit à la réunion dans quelques minutes.

=jr
