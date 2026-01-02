---
title: "Ancienne implémentation de Tunnel (héritée)"
description: "Description archivée de la conception du tunnel utilisée avant I2P 0.6.1.10."
slug: "old-implementation"
lastUpdated: "2005-06"
accurateFor: "0.6.1"
reviewStatus: "needs-review"
---

> **Statut hérité :** Ce contenu est conservé uniquement à des fins de référence historique. Il documente le système de tunnel livré avant I2P&nbsp;0.6.1.10 et ne doit pas être utilisé pour le développement moderne. Reportez-vous à l’[implémentation actuelle](/docs/specs/implementation/) pour des recommandations destinées à la production.

Le sous-système de tunnel d'origine utilisait lui aussi des tunnels unidirectionnels, mais différait par la structure des messages, la détection des doublons et la stratégie de construction. De nombreuses sections ci-dessous reprennent la structure du document obsolète pour faciliter la comparaison.

## 1. Vue d’ensemble du Tunnel

- Les tunnels étaient construits sous forme de séquences ordonnées de pairs sélectionnés par le créateur.
- Les longueurs de tunnels allaient de 0–7 sauts, avec plusieurs paramètres pour le bourrage, la limitation de débit et la génération de trafic leurre.
- Les tunnels entrants acheminaient les messages d'une passerelle non fiable jusqu'au créateur (endpoint, point de terminaison); les tunnels sortants envoyaient les données loin du créateur.
- La durée de vie des tunnels était de 10 minutes, après quoi de nouveaux tunnels étaient construits (souvent en utilisant les mêmes pairs mais avec des identifiants de tunnel différents).

## 2. Fonctionnement dans l’ancienne conception

### 2.1 Prétraitement des messages

Les passerelles ont accumulé ≤32&nbsp;KB de charge utile I2NP, sélectionné un bourrage, et produit une charge utile contenant:

- Un champ de longueur de bourrage sur deux octets et autant d'octets aléatoires
- Une séquence de paires `{instructions, I2NP message}` décrivant les cibles de livraison, la fragmentation et des retards optionnels
- Des I2NP messages complets, complétés par bourrage jusqu'à un alignement sur 16 octets

Les instructions de livraison compactaient les informations de routage dans des champs de bits (type de livraison, indicateurs de délai, indicateurs de fragmentation et extensions facultatives). Les messages fragmentés comportaient un identifiant de message de 4 octets ainsi qu’un indicateur index/dernier-fragment.

### 2.2 Chiffrement de passerelle

La conception héritée fixait, pour la phase de chiffrement, la longueur du tunnel à huit sauts. Les passerelles superposaient des blocs AES-256/CBC ainsi que des blocs de somme de contrôle afin que chaque saut puisse vérifier l’intégrité sans réduire la charge utile. La somme de contrôle elle-même était un bloc dérivé de SHA-256, intégré au sein du message.

### 2.3 Comportement des participants

Les participants suivaient les identifiants de tunnels entrants, vérifiaient l’intégrité dès réception et éliminaient les doublons avant l’acheminement. Comme le bourrage et les blocs de vérification étaient intégrés, la taille du message restait constante quel que soit le nombre de sauts.

### 2.4 Traitement du point de terminaison

Les points de terminaison ont déchiffré séquentiellement les blocs en couches, validé les sommes de contrôle et scindé à nouveau la charge utile en instructions encodées ainsi qu'en messages I2NP pour un acheminement ultérieur.

## 3. Construction de Tunnel (Processus obsolète)

1. **Sélection des pairs:** Les pairs étaient choisis à partir de profils maintenus localement (exploratoires vs client). Le document d’origine soulignait déjà l’atténuation de la [prédecessor attack](https://en.wikipedia.org/wiki/Predecessor_attack) en réutilisant des listes de pairs ordonnées pour chaque pool de tunnels.
2. **Acheminement des requêtes:** Les Build messages (messages de construction) étaient transférés saut par saut, avec des sections chiffrées pour chaque pair. Des idées alternatives telles que l’extension télescopique, le réacheminement en cours de route ou la suppression des blocs de somme de contrôle ont été évoquées comme expérimentations, mais n’ont jamais été adoptées.
3. **Regroupement:** Chaque destination locale disposait de pools entrants et sortants distincts. Les paramètres incluaient la quantité souhaitée, des tunnels de secours, la variance de longueur, la limitation de débit et les politiques de bourrage.

## 4. Concepts de limitation de débit et de mélange

Le document ancien proposait plusieurs stratégies qui ont guidé les versions ultérieures :

- Rejet aléatoire précoce pondéré (WRED) pour le contrôle de congestion
- Limitations de débit par tunnel basées sur des moyennes mobiles de l'utilisation récente
- Contrôles facultatifs de chaff (trafic leurre) et de mise en lots (pas entièrement mis en œuvre)

## 5. Alternatives archivées

Des sections du document original exploraient des idées qui n'ont jamais été déployées :

- Supprimer les blocs de somme de contrôle afin de réduire le traitement par saut
- Télescopage des tunnels en cours de route pour modifier la composition des pairs
- Passer à des tunnels bidirectionnels (finalement rejeté)
- Utiliser des hachages plus courts ou des schémas de bourrage différents

Ces idées restent un contexte historique précieux, mais ne reflètent pas la base de code moderne.

## Références

- Archive originale des documents hérités (avant 0.6.1.10)
- [Aperçu du Tunnel](/docs/overview/tunnel-routing/) pour la terminologie actuelle
- [Profilage et sélection des pairs](/docs/overview/tunnel-routing#peer-selection/) pour les heuristiques modernes
