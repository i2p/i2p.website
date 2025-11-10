---
title: "LeaseSet 2"
number: "110"
author: "zzz"
created: "2014-01-22"
lastupdated: "2016-04-04"
status: "Rejeté"
thread: "http://zzz.i2p/topics/1560"
supercededby: "123"
---

## Vue d'ensemble

Cette proposition concerne un nouveau format de LeaseSet prenant en charge de
nouveaux types de chiffrement.


## Motivation

La cryptographie de bout en bout utilisée à travers les tunnels I2P dispose de
clés distinctes pour le chiffrement et la signature. Les clés de signature se
trouvent dans la Destination du tunnel, qui a déjà été étendue avec les
KeyCertificates pour prendre en charge de nouveaux types de signature.
Cependant, les clés de chiffrement font partie du LeaseSet, qui ne contient
aucun certificat. Il est donc nécessaire de mettre en œuvre un nouveau format de
LeaseSet et d'ajouter la prise en charge de son stockage dans le netDb.

Un aspect positif est qu'une fois que LS2 est mis en œuvre, toutes les
Destinations existantes pourront utiliser des types de chiffrement plus modernes;
les routeurs capables de récupérer et lire un LS2 seront garantis de prendre en
charge tous les types de chiffrement introduits avec celui-ci.


## Spécification

Le format de base de LS2 serait le suivant :

- dest
- horodatage de publication (8 octets)
- expiration (8 octets)
- sous-type (1 octet) (régulier, chiffré, méta ou service)
- indicateurs (2 octets)

- partie spécifique au sous-type:
  - type de chiffrement, clé de chiffrement et baux pour régulier
  - blob pour chiffré
  - propriétés, hachages, ports, révocations, etc. pour service

- signature
