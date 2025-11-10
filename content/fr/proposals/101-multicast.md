---
title: "Multidiffusion"
number: "101"
author: "zzz"
created: "2008-12-08"
lastupdated: "2009-03-25"
status: "Inactif"
thread: "http://zzz.i2p/topics/172"
---

## Aperçu

Idée de base : Envoyer une copie à travers votre tunnel sortant, le point de sortie distribue à toutes les passerelles entrantes. Le chiffrement de bout en bout est exclu.

## Conception

- Nouveau type de message de tunnel de multidiffusion (type de livraison = 0x03)
- Le point de sortie distribue en multidiffusion
- Nouveau type de message I2NP Multicast ?
- Nouveau type de message I2CP SendMessageMessage Multicast
- Ne pas chiffrer entre routeurs dans OutNetMessageOneShotJob (ail ?)

Application :

- Proxy RTSP ?

Streamr :

- Ajuster le MTU ? Ou le faire simplement au niveau de l'application ?
- Réception et transmission à la demande
