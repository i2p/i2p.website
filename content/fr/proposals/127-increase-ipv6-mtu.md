---
title: "Augmenter le MTU IPv6"
number: "127"
author: "zzz"
created: "2016-08-23"
lastupdated: "2016-12-02"
status: "Fermé"
thread: "http://zzz.i2p/topics/2181"
target: "0.9.28"
implementedin: "0.9.28"
---

## Vue d'ensemble

Cette proposition vise à augmenter le MTU SSU IPv6 maximal de 1472 à 1488.
Implémenté dans la version 0.9.28.

## Motivation

Le MTU IPv4 doit être un multiple de 16, + 12. Le MTU IPv6 doit être un multiple de 16.

Lorsque la prise en charge de l'IPv6 a été ajoutée pour la première fois il y a quelques années, nous avons fixé le MTU IPv6 maximal à 1472, inférieur au MTU IPv4 de 1484. Cela avait pour but de simplifier les choses et de garantir que le MTU IPv6 soit inférieur au MTU IPv4 existant. Maintenant que la prise en charge de l'IPv6 est stable, nous devrions être capables de définir le MTU IPv6 à une valeur plus élevée que le MTU IPv4.

Le MTU d'interface typique est de 1500, nous pouvons donc raisonnablement augmenter le MTU IPv6 de 16 à 1488.

## Conception

Changer le maximum de 1472 à 1488.

## Spécification

Dans les sections "Adresse du routeur" et "MTU" de l'aperçu SSU,
changer le MTU IPv6 maximal de 1472 à 1488.

## Migration

Nous nous attendons à ce que les routeurs définissent le MTU de connexion comme le minimum entre le MTU local et distant, comme d'habitude. Aucun contrôle de version ne devrait être nécessaire.

Si nous déterminons qu'un contrôle de version est nécessaire, nous fixerons un niveau de version minimum de 0.9.28 pour ce changement.
