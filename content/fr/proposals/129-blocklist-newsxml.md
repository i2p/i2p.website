---
title: "Liste de blocage dans le fil d'actualités"
number: "129"
author: "zzz"
created: "2016-11-23"
lastupdated: "2016-12-02"
status: "Fermé"
thread: "http://zzz.i2p/topics/2191"
target: "0.9.28"
implementedin: "0.9.28"
---

## Vue d'ensemble

Cette proposition vise à distribuer des mises à jour de la liste de blocage dans le fichier de nouvelles,
qui est distribué au format signé su3.
Implémenté dans la version 0.9.28.

## Motivation

Sans cela, la liste de blocage n'est mise à jour que lors de la publication de la version.
Utilise l'abonnement aux nouvelles existant.
Ce format pourrait être utilisé dans diverses implémentations de routeurs, mais seul le routeur Java
utilise l'abonnement aux nouvelles pour l'instant.

## Conception

Ajouter une nouvelle section au fichier news.xml.
Permettre le blocage par IP ou par hachage de routeur.
La section aura son propre horodatage.
Permettre de débloquer des entrées précédemment bloquées.

Inclure une signature de la section, qui sera spécifiée.
La signature couvrira l'horodatage.
La signature doit être vérifiée à l'importation.
Le signataire sera spécifié et pourrait être différent du signataire su3.
Les routeurs peuvent utiliser une liste de confiance différente pour la liste de blocage.

## Spécification

Maintenant sur la page de spécifications de mise à jour du routeur.

Les entrées sont soit une adresse IPv4 ou IPv6 littérale,
soit un hachage de routeur encodé en base64 sur 44 caractères.
Les adresses IPv6 peuvent être en format abrégé (contenant "::").
Le support pour le blocage avec un masque de réseau, par exemple x.y.0.0/16, est optionnel.
Le support pour les noms d'hôtes est optionnel.

## Migration

Les routeurs qui ne supportent pas cela ignoreront la nouvelle section XML.

## Voir aussi

Proposition 130
