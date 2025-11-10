---
title: "Notes d'état d'I2P du 2004-09-21"
date: 2004-09-21
author: "jr"
description: "Mise à jour hebdomadaire de l'état d'I2P couvrant les progrès du développement, les améliorations du transport TCP et la nouvelle fonctionnalité userhosts.txt"
categories: ["status"]
---

Salut à tous, petite mise à jour cette semaine

## Index

1. Dev status
2. New userhosts.txt vs. hosts.txt
3. ???

## 1) Statut du développement

Le réseau a été assez stable au cours de la semaine écoulée, j’ai donc pu consacrer mon temps à la version 0.4.1 - remanier le transport TCP, ajouter la prise en charge de la détection des adresses IP et supprimer cet ancien message « target changed identities ». Cela devrait également éliminer la nécessité d’enregistrements dyndns.

Ce ne sera pas la configuration sans clic idéale pour les personnes derrière des NAT ou des pare-feux — elles devront tout de même configurer la redirection de ports afin de pouvoir recevoir des connexions TCP entrantes. Cela devrait toutefois être moins sujet aux erreurs. Je fais de mon mieux pour conserver la rétrocompatibilité, mais je ne promets rien à ce sujet. Plus d’informations quand ce sera prêt.

## 2) Nouveau userhosts.txt vs. hosts.txt

Dans la prochaine version, nous offrirons la prise en charge, souvent demandée, d’une paire de fichiers hosts.txt - l’un qui est écrasé lors des mises à jour (ou depuis `http://dev.i2p.net/i2p/hosts.txt`) et l’autre que l’utilisateur peut maintenir localement. Dans la prochaine version (ou CVS HEAD) vous pouvez modifier le fichier "userhosts.txt", qui est consulté avant hosts.txt pour toutes les entrées - veuillez y effectuer vos modifications locales, car le processus de mise à jour écrasera hosts.txt (mais pas userhosts.txt).

## 3) ???

Comme je l’ai dit, juste quelques notes rapides cette semaine. Quelqu’un a-t-il autre chose à aborder ? Passez donc à la réunion dans quelques minutes.

=jr
