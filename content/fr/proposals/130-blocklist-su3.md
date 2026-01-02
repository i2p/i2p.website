---
title: "Blocage dans le format SU3"
number: "130"
author: "psi, zzz"
created: "2016-11-23"
lastupdated: "2016-11-23"
status: "Ouvert"
thread: "http://zzz.i2p/topics/2192"
toc: true
---

## Vue d'ensemble

Cette proposition vise à distribuer les mises à jour de la liste de blocage dans un fichier su3 séparé.


## Motivation

Sans cela, la liste de blocage n'est mise à jour que lors de la sortie.
Ce format pourrait être utilisé dans diverses implémentations de routeur.


## Conception

Définir le format à encapsuler dans un fichier su3.
Permettre le blocage par IP ou hash du routeur.
Les routeurs peuvent s'abonner à une URL, ou importer un fichier obtenu par d'autres moyens.
Le fichier su3 contient une signature qui doit être vérifiée lors de l'importation.


## Spécification

À ajouter à la page de spécification de mise à jour du routeur.

Définir un nouveau type de contenu BLOCKLIST (5).
Définir un nouveau type de fichier TXT_GZ (4) (format .txt.gz).
Les entrées sont une par ligne, soit une adresse IPv4 ou IPv6 littérale,
soit un hash de routeur encodé en base64 de 44 caractères.
Le support du blocage avec un masque de réseau, par exemple x.y.0.0/16, est optionnel.
Pour débloquer une entrée, précédez-la d'un '!'.
Les commentaires commencent par un '#'.


## Migration

n/a


