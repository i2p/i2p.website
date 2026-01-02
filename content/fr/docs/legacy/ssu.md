---
title: "SSU (ancien)"
description: "Transport UDP sécurisé semi-fiable d'origine"
slug: "ssu"
lastUpdated: "2025-01"
accurateFor: "0.9.64"
reviewStatus: "needs-review"
---

> **Obsolète:** SSU a été remplacé par SSU2. La prise en charge a été supprimée dans i2pd 2.44.0 (API 0.9.56, nov 2022) et dans Java I2P 2.4.0 (API 0.9.61, déc 2023).

SSU fournissait un acheminement semi-fiable basé sur UDP avec contrôle de congestion, traversée de NAT et prise en charge des introducers (relais d'introduction). Il complétait NTCP en gérant les routers derrière des NAT/pare-feux et en coordonnant la découverte de l'adresse IP.

## Éléments d'adresse

- `transport`: `SSU`
- `caps`: indicateurs de capacité (`B`, `C`, `4`, `6`, etc.)
- `host` / `port`: écouteur IPv4 ou IPv6 (facultatif lorsque le router est derrière un pare-feu)
- `key`: clé d'introduction Base64
- `mtu`: Facultatif; valeur par défaut 1484 (IPv4) / 1488 (IPv6)
- `ihost/ikey/iport/itag/iexp`: entrées d'introducteur lorsque le router est derrière un pare-feu

## Fonctionnalités

- Traversée NAT coopérative à l'aide d'introducers (nœuds introducteurs)
- Détection de l'IP locale via des tests entre pairs et l'inspection des paquets entrants
- État du pare-feu relayé automatiquement aux autres transports et à la console du router
- Livraison semi-fiable : messages retransmis jusqu'à une limite, puis abandonnés
- Contrôle de congestion avec augmentation additive / diminution multiplicative et champs de bits d'ACK de fragments

SSU gérait également des tâches liées aux métadonnées telles que les balises de synchronisation temporelle et la négociation de la MTU. Toutes ces fonctionnalités sont désormais fournies (avec une cryptographie moderne) par [SSU2](/docs/specs/ssu2/).
