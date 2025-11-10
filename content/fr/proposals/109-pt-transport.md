---
title: "PT Transport"
number: "109"
author: "zzz"
created: "2014-01-09"
lastupdated: "2014-09-28"
status: "Ouvert"
thread: "http://zzz.i2p/topics/1551"
---

## Aperçu

Cette proposition concerne la création d'un transport I2P qui se connecte à d'autres routeurs
via des transports modulaires.


## Motivation

Les transports modulaires (PT) ont été développés par Tor comme moyen d'ajouter des transports d'obfuscation
aux ponts Tor de manière modulaire.

I2P dispose déjà d'un système de transport modulaire qui réduit la barrière pour ajouter
des transports alternatifs. Ajouter la prise en charge des PT fournirait à I2P un moyen facile
d'expérimenter avec des protocoles alternatifs et de se préparer à une résistance au blocage.


## Conception

Il existe quelques couches potentielles d'implémentation :

1. Un PT générique qui implémente SOCKS et ExtORPort et configure et bifurque les
   processus entrants et sortants, et s'enregistre avec le système de communication. Cette couche ne
   connaît rien de NTCP, et elle peut ou non utiliser NTCP. Utile pour les tests.

2. En s'appuyant sur 1), un PT NTCP générique qui s'appuie sur le code NTCP et dirige
   NTCP vers 1).

3. En s'appuyant sur 2), un PT NTCP-xxxx spécifique configuré pour exécuter un processus 
   externe donné en entrée et en sortie.
