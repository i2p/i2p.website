---
title: "SAM v1"
description: "Protocole hérité Simple Anonymous Messaging (déprécié)"
slug: "sam"
lastUpdated: "2025-03"
accurateFor: "0.9.20"
reviewStatus: "needs-review"
---

> **Obsolète :** SAM v1 est conservée uniquement à des fins de référence historique. Les nouvelles applications devraient utiliser [SAM v3](/docs/api/samv3/) ou [BOB](/docs/legacy/bob/). La passerelle d'origine ne prend en charge que les destinations DSA-SHA1 et un jeu d'options limité.

## Bibliothèques

L’arborescence du code source Java d’I2P inclut encore des liaisons héritées pour C, C#, Perl et Python. Elles ne sont plus maintenues et sont principalement distribuées afin d’assurer la compatibilité avec les archives.

## Négociation de version

Les clients se connectent via TCP (par défaut `127.0.0.1:7656`) et échangent:

```
Client → HELLO VERSION MIN=1 MAX=1
Bridge → HELLO REPLY RESULT=OK VERSION=1.0
```
À partir de Java I2P 0.9.14, le paramètre `MIN` est facultatif et `MIN`/`MAX` acceptent tous deux des formes à un chiffre (`"3"` etc.) pour les ponts mis à niveau.

## Création de session

```
SESSION CREATE STYLE={STREAM|DATAGRAM|RAW} DESTINATION={name|TRANSIENT} [DIRECTION={BOTH|RECEIVE|CREATE}] [option=value]*
```
- `DESTINATION=name` charge ou crée une entrée dans `sam.keys`; `TRANSIENT` crée toujours une destination temporaire.
- `STYLE` sélectionne des flux virtuels (de type TCP), des datagrammes signés ou des datagrammes bruts.
- `DIRECTION` s’applique uniquement aux sessions de flux; la valeur par défaut est `BOTH`.
- Des paires clé/valeur supplémentaires sont transmises comme options I2CP (par exemple, `tunnels.quantityInbound=3`).

Le pont répond :

```
SESSION STATUS RESULT=OK DESTINATION=name
```
Les échecs renvoient `DUPLICATED_DEST`, `I2P_ERROR` ou `INVALID_KEY`, plus un message facultatif.

## Formats de messages

Les messages SAM sont en ASCII sur une seule ligne, avec des paires clé/valeur séparées par des espaces. Les clés sont en UTF‑8 ; les valeurs peuvent être entre guillemets si elles contiennent des espaces. Aucun mécanisme d’échappement n’est défini.

Types de communication :

- **Flux** – acheminés via la bibliothèque de streaming I2P
- **Datagrammes répondables** – charges utiles signées (Datagram1)
- **Datagrammes bruts** – charges utiles non signées (Datagram RAW)

## Options ajoutées dans la version 0.9.14

- `DEST GENERATE` accepte `SIGNATURE_TYPE=...` (permettant Ed25519, etc.)
- `HELLO VERSION` considère `MIN` comme facultatif et accepte des chaînes de version à un seul chiffre

## Quand utiliser SAM v1

Uniquement pour l’interopérabilité avec des logiciels hérités qui ne peuvent pas être mis à jour. Pour tout nouveau développement, utilisez :

- [SAM v3](/docs/api/samv3/) pour un accès complet en fonctionnalités aux flux/datagrammes
- [BOB](/docs/legacy/bob/) pour la gestion des destinations (encore limité, mais prend en charge des fonctionnalités plus modernes)

## Références

- [SAM v2](/docs/legacy/samv2/)
- [SAM v3](/docs/api/samv3/)
- [Spécification des datagrammes](/docs/api/datagrams/)
- [Protocole de streaming](/docs/specs/streaming/)

SAM v1 a jeté les bases du développement d’applications indépendant du router, mais l’écosystème a évolué. Considérez ce document comme une aide à la compatibilité plutôt qu’un point de départ.
