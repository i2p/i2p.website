---
title: "Bonjour Git, au revoir Monotone"
date: 2020-12-10
author: "idk"
description: "Bonjour git, au revoir mtn"
categories: ["Status"]
---

## Bonjour Git, adieu Monotone

### The I2P Git Migration is nearly concluded

Depuis plus d’une décennie, I2P s’appuie sur le vénérable service Monotone pour répondre à ses besoins en gestion de versions, mais ces dernières années, la majeure partie du monde est passée au désormais universel système de gestion de versions Git. Dans le même temps, le réseau I2P est devenu plus rapide et plus fiable, et des solutions de contournement accessibles pour pallier l’impossibilité de reprendre les transferts avec Git ont été développées.

Aujourd’hui marque une étape importante pour I2P, puisque nous avons désactivé l’ancienne branche mtn i2p.i2p et avons officiellement migré le développement des bibliothèques I2P Java de base de Monotone vers Git.

Bien que notre utilisation de mtn ait été remise en question par le passé, et qu’elle n’ait pas toujours été un choix populaire, je voudrais profiter de ce moment, en tant que peut-être tout dernier projet à utiliser Monotone, pour remercier les développeurs de Monotone, actuels et anciens, où qu’ils soient, pour le logiciel qu’ils ont créé.

## GPG Signing

Les contributions aux dépôts du projet I2P exigent que vous configuriez la signature GPG de vos commits Git, y compris pour les Merge Requests (demandes de fusion) et les Pull Requests (demandes d’intégration). Veuillez configurer votre client Git pour la signature GPG avant de forker i2p.i2p et de soumettre quoi que ce soit.

## Signature GPG

Le dépôt officiel est celui hébergé sur https://i2pgit.org/i2p-hackers/i2p.i2p et sur https://git.idk.i2p/i2p-hackers/i2p.i2p, mais il existe un "miroir" disponible sur Github à l'adresse https://github.com/i2p/i2p.i2p.

Maintenant que nous utilisons Git, nous pouvons synchroniser des dépôts depuis notre propre instance GitLab auto-hébergée, vers GitHub, et inversement. Cela signifie qu’il est possible de créer et de soumettre une demande de fusion sur GitLab et, lorsqu’elle est fusionnée, le résultat sera synchronisé avec GitHub, et une Pull Request (demande de fusion) sur GitHub, une fois fusionnée, apparaîtra sur GitLab.

Cela signifie qu’il est possible de nous soumettre du code via notre instance Gitlab ou via Github selon votre préférence ; cependant, davantage de développeurs I2P surveillent régulièrement Gitlab que Github. Les MR (Merge Requests) vers Gitlab ont plus de chances d’être fusionnées plus rapidement que les PR (Pull Requests) vers Github.

## Dépôts officiels et synchronisation Gitlab/Github

Félicitations et merci à tous ceux qui ont aidé à la migration vers Git, en particulier zzz, eche|on, nextloop et nos opérateurs de miroirs du site !
Même si Monotone manquera à certains d’entre nous, il est devenu un obstacle pour les participants au développement d’I2P, qu’ils soient nouveaux ou déjà impliqués, et nous sommes enthousiastes à l’idée de rejoindre le monde des développeurs qui utilisent Git pour gérer leurs projets distribués.
