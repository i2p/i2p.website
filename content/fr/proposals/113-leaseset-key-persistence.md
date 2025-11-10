---
title: "Persistance des Clés LeaseSet"
number: "113"
author: "zzz"
created: "2014-12-13"
lastupdated: "2016-12-02"
status: "Fermé"
thread: "http://zzz.i2p/topics/1770"
target: "0.9.18"
implementedin: "0.9.18"
---

## Vue d'ensemble

Cette proposition concerne la persistance de données supplémentaires dans le LeaseSet qui est actuellement éphémère. Implémentée dans la version 0.9.18.


## Motivation

Dans la version 0.9.17, la persistance a été ajoutée pour la clé de découpage netDb, stockée dans i2ptunnel.config. Cela aide à prévenir certaines attaques en gardant la même découpe après redémarrage, et empêche également une possible corrélation avec un redémarrage du routeur.

Il y a deux autres éléments qui sont encore plus faciles à corréler avec le redémarrage du routeur : les clés de chiffrement et de signature du leaseset. Celles-ci ne sont actuellement pas persistantes.


## Modifications Proposées

Les clés privées sont stockées dans i2ptunnel.config, en tant que i2cp.leaseSetPrivateKey et i2cp.leaseSetSigningPrivateKey.
