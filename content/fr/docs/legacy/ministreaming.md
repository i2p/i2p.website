---
title: "Bibliothèque Ministreaming"
description: "Notes historiques sur la première couche de transport de type TCP d'I2P"
slug: "ministreaming"
aliases:
  - "/fr/ministreaming"
  - "/fr/ministreaming/"
lastUpdated: "2025-02"
accurateFor: "historical"
---

## Note

La bibliothèque ministreaming a été améliorée et étendue par la [bibliothèque streaming](/docs/api/streaming) "complète". Ministreaming est obsolète et incompatible avec les applications actuelles. La documentation suivante est ancienne. Notez également que streaming étend ministreaming dans le même package Java (net.i2p.client.streaming), donc la documentation API actuelle contient les deux. Les classes et méthodes ministreaming obsolètes sont clairement marquées comme dépréciées dans les Javadocs.

## Bibliothèque Ministreaming

La bibliothèque ministreaming est une couche au-dessus du noyau [I2CP](/docs/protocol/i2cp) qui permet aux flux de messages fiables, ordonnés et authentifiés de fonctionner sur une couche de messages non fiable, non ordonnée et non authentifiée. Tout comme la relation TCP vers IP, cette fonctionnalité de streaming dispose de toute une série de compromis et d'optimisations disponibles, mais plutôt que d'intégrer cette fonctionnalité dans le code I2P de base, elle a été extraite dans sa propre bibliothèque à la fois pour garder les complexités de type TCP séparées et pour permettre des implémentations alternatives optimisées.

La bibliothèque ministreaming a été écrite par mihi dans le cadre de son application [I2PTunnel](/docs/api/i2ptunnel) puis extraite et publiée sous licence BSD. Elle est appelée bibliothèque "mini"streaming car elle apporte certaines simplifications dans l'implémentation, alors qu'une bibliothèque streaming plus robuste pourrait être davantage optimisée pour fonctionner sur I2P. Les deux principaux problèmes de la bibliothèque ministreaming sont son utilisation du protocole d'établissement TCP traditionnel à deux phases et la taille de fenêtre fixe actuelle de 1. Le problème d'établissement est mineur pour les flux de longue durée, mais pour les courts, comme les requêtes HTTP rapides, l'impact peut être significatif. Concernant la taille de fenêtre, la bibliothèque ministreaming ne maintient aucun ID ni ordre dans les messages envoyés (et n'inclut aucun ACK ou SACK au niveau applicatif), elle doit donc attendre en moyenne deux fois le temps nécessaire pour envoyer un message avant d'en envoyer un autre.

Malgré ces problèmes, la bibliothèque ministreaming fonctionne assez bien dans de nombreuses situations, et son API est à la fois très simple et capable de rester inchangée lorsque différentes implémentations de streaming sont introduites. La bibliothèque est déployée dans son propre ministreaming.jar. Les développeurs Java qui souhaitent l'utiliser peuvent accéder directement à l'API, tandis que les développeurs utilisant d'autres langages peuvent l'utiliser via le support de streaming de [SAM](/docs/api/samv3).
