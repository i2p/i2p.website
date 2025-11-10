---
title: "LeaseSet Chiffré"
number: "121"
author: "zzz"
created: "2016-01-11"
lastupdated: "2016-01-12"
status: "Rejeté"
thread: "http://zzz.i2p/topics/2047"
supercededby: "123"
---

## Vue d'ensemble

Cette proposition concerne la refonte du mécanisme de chiffrement des LeaseSets.

## Motivation

L'LS chiffré actuel est horrible et non sécurisé. Je peux dire cela, car je l'ai conçu et
implémenté.

Raisons :

- Chiffrement AES CBC
- Une seule clé AES pour tout le monde
- Les expirations de bail toujours exposées
- La clé publique de chiffrement toujours exposée

## Conception

### Objectifs

- Rendre l'ensemble entièrement opaque
- Clés pour chaque destinataire

### Stratégie

Faire comme le fait GPG/OpenPGP. Chiffrer asymétriquement une clé symétrique pour chaque
destinataire. Les données sont déchiffrées avec cette clé asymétrique. Voir par exemple [RFC-4880-S5.1]_
SI nous pouvons trouver un algo qui soit petit et rapide.

Le défi est de trouver un chiffrement asymétrique qui soit petit et rapide. ElGamal à 514
octets est un peu douloureux ici. Nous pouvons faire mieux.

Voir par exemple http://security.stackexchange.com/questions/824...

Cela fonctionne pour de petits nombres de destinataires (ou en fait, de clés ; vous pouvez toujours
distribuer des clés à plusieurs personnes si vous le souhaitez).

## Spécification

- Destination
- Timestamp publié
- Expiration
- Drapeaux
- Longueur des données
- Données chiffrées
- Signature

Les données chiffrées pourraient être précédées d'un spécificateur enctype, ou non.

## Références

.. [RFC-4880-S5.1]
    https://tools.ietf.org/html/rfc4880#section-5.1
