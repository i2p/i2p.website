---
title: "Bibliothèque Ministreaming"
description: "Notes historiques sur la première couche de transport de type TCP d’I2P"
slug: "ministreaming"
lastUpdated: "2025-02"
accurateFor: "historical"
---

> **Obsolète :** La bibliothèque ministreaming est antérieure à la [bibliothèque de streaming](/docs/specs/streaming/) actuelle. Les applications modernes doivent utiliser l’API de streaming complète ou SAM v3. Les informations ci-dessous sont conservées pour les développeurs qui examinent du code source hérité fourni dans `ministreaming.jar`.

## Vue d'ensemble

Ministreaming (mécanisme de flux minimal) s'appuie sur [I2CP](/docs/specs/i2cp/) pour fournir une livraison fiable et ordonnée au sein de la couche de messages d'I2P — à l'instar de TCP sur IP. Il a été initialement extrait de l'application **I2PTunnel** des débuts (sous licence BSD) afin que des transports alternatifs puissent évoluer indépendamment.

Principales contraintes de conception :

- Établissement de connexion classique en deux phases (SYN/ACK/FIN) emprunté à TCP
- Taille de fenêtre fixe de **1** paquet
- Pas d'identifiants par paquet ni d'accusés de réception sélectifs

Ces choix ont permis de garder l’implémentation compacte mais limitent le débit—chaque paquet attend généralement presque deux RTT (temps aller-retour) avant que le suivant soit envoyé. Pour les flux de longue durée, la pénalité est acceptable, mais les échanges courts de type HTTP en pâtissent sensiblement.

## Relation avec la bibliothèque de streaming

La bibliothèque de streaming actuelle utilise le même package Java (`net.i2p.client.streaming`). Les classes et méthodes obsolètes restent dans la Javadoc, clairement annotées afin que les développeurs puissent identifier les API de l’ère ministreaming (ancien sous-système « ministreaming »). Lorsque la bibliothèque de streaming a remplacé ministreaming, elle a ajouté :

- Établissement de connexion plus intelligent avec moins d'allers-retours
- Fenêtres de congestion adaptatives et logique de retransmission
- Meilleures performances sur des tunnels avec pertes

## Quand le Ministreaming a-t-il été utile ?

Malgré ses limites, le ministreaming (sous-système de streaming minimaliste) a assuré un transport fiable lors des tout premiers déploiements. L’API était volontairement réduite et pérenne afin que des moteurs de streaming alternatifs puissent être substitués sans rompre la compatibilité avec le code appelant. Les applications Java l’intégraient directement ; les clients non Java accédaient à la même fonctionnalité via la prise en charge de [SAM](/docs/legacy/sam/) pour les sessions de streaming.

À ce jour, considérez `ministreaming.jar` uniquement comme une couche de compatibilité. Les nouveaux développements devraient :

1. Ciblez la bibliothèque de streaming complète (Java) ou SAM v3 (style `STREAM`)  
2. Supprimez toute hypothèse résiduelle de fenêtre fixe lors de la modernisation du code  
3. Privilégiez des tailles de fenêtre plus élevées et des handshakes de connexion optimisés pour améliorer les charges de travail sensibles à la latence

## Référence

- [Documentation de la bibliothèque de streaming](/docs/specs/streaming/)
- [Javadoc de streaming](http://idk.i2p/javadoc-i2p/net/i2p/client/streaming/package-summary.html) – inclut des classes ministreaming obsolètes
- [Spécification SAM v3](/docs/api/samv3/) – prise en charge du streaming pour les applications non Java

Si vous rencontrez du code qui dépend encore de ministreaming (fonctionnalité héritée), prévoyez de le porter vers l’API de streaming moderne — le réseau et ses outils s’attendent au nouveau comportement.
