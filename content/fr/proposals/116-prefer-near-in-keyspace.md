---
title: "Préférer les routeurs proches dans l'espace de clés"
number: "116"
author: "chisquare"
created: "2015-04-25"
lastupdated: "2015-04-25"
status: "Needs-Research"
thread: "http://zzz.i2p/topics/1874"
---

## Vue d'ensemble

Ceci est une proposition pour organiser les pairs afin qu'ils préfèrent se connecter à d'autres pairs proches d'eux dans l'espace de clés.

## Motivation

L'idée est d'améliorer le succès de la construction des tunnels, en augmentant la probabilité qu'un routeur soit déjà connecté à un autre.

## Conception

### Modifications requises

Ce changement nécessiterait :

1. Chaque routeur préfère les connexions proches d'eux dans l'espace de clés.
2. Chaque routeur soit conscient que chaque routeur préfère les connexions proches d'eux dans l'espace de clés.

### Avantages pour la construction de tunnels

Si vous construisez un tunnel :

    A -long-> B -short-> C -short-> D

(long/aléatoire vs saut court dans l'espace de clés), vous pouvez deviner où la construction du tunnel a probablement échoué et essayer un autre pair à ce moment-là. De plus, cela vous permettrait de détecter les parties plus denses dans l'espace de clés et de faire en sorte que les routeurs ne les utilisent pas car cela pourrait être quelqu'un collusionnant.

Si vous construisez un tunnel :

    A -long-> B -long-> C -short-> D

et que cela échoue, vous pouvez en déduire qu'il a plus probablement échoué à C -> D et vous pouvez choisir un autre saut D.

Vous pouvez également construire des tunnels afin que l'OBEP soit plus proche de l'IBGW et utiliser ces tunnels avec des OBEP qui sont plus proches de l'IBGW donné dans un LeaseSet.

## Implications sur la sécurité

Si vous randomisez le placement de sauts courts vs longs dans l'espace de clés, un attaquant ne gagnera probablement pas beaucoup d'avantages.

Le principal inconvénient est qu'il peut rendre l'énumération des utilisateurs un peu plus facile.
