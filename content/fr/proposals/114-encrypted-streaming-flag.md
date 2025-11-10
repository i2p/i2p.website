---
title: "'Drapeau' de Streaming Crypté"
number: "114"
author: "orignal"
created: "2015-01-21"
lastupdated: "2015-01-21"
status: "Besoin-de-Recherche"
thread: "http://zzz.i2p/topics/1795"
---

## Vue d'ensemble

Cette proposition concerne l'ajout d'un drapeau au streaming spécifiant le type de chiffrement bout-en-bout utilisé.


## Motivation

Les applications très chargées peuvent rencontrer une pénurie de tags ElGamal/AES+SessionTags.


## Conception

Ajouter un nouveau drapeau quelque part dans le protocole de streaming. Si un paquet arrive avec ce drapeau, cela signifie que la charge utile est chiffrée en AES avec une clé obtenue à partir de la clé privée et la clé publique du pair. Cela permettrait d'éliminer le chiffrement garlic (ElGamal/AES) et le problème de pénurie de tags.

Peut être défini par paquet ou par flux via SYN.
