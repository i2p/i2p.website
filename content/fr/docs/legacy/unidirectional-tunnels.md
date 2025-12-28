---
title: "Tunnels unidirectionnels"
description: "Résumé historique de la conception des tunnels unidirectionnels d'I2P."
slug: "unidirectional"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

> **Avis historique :** Cette page conserve, à titre de référence, l’ancienne discussion « Tunnels unidirectionnels ». Consultez la [documentation de l’implémentation des tunnels](/docs/specs/implementation/) en vigueur pour le comportement actuel.

## Vue d’ensemble

I2P construit des **tunnels unidirectionnels**: un tunnel transporte le trafic sortant et un tunnel distinct transporte les réponses entrantes. Cette structure remonte aux toutes premières conceptions du réseau et demeure un facteur de différenciation majeur par rapport aux systèmes à circuits bidirectionnels comme Tor. Pour la terminologie et les détails d'implémentation, voir l'[aperçu des tunnels](/docs/overview/tunnel-routing/) et la [spécification des tunnels](/docs/specs/implementation/).

## Revue

- Les tunnels unidirectionnels séparent le trafic de requête et de réponse, de sorte que tout groupe de pairs en collusion n’observe que la moitié d’un aller-retour.
- Les attaques temporelles doivent croiser deux pools de tunnels (sortants et entrants) au lieu d’analyser un seul circuit, ce qui rend la corrélation plus difficile.
- Des pools de tunnels entrants et sortants indépendants permettent aux routers d’ajuster, par direction, la latence, la capacité et les caractéristiques de gestion des défaillances.
- Les inconvénients incluent une complexité accrue de la gestion des pairs et la nécessité de maintenir plusieurs ensembles de tunnels pour une prestation de service fiable.

## Anonymat

L'article de Hermann et Grothoff, [*I2P is Slow… and What to Do About It*](http://grothoff.org/christian/i2p.pdf), analyse les attaques du prédécesseur contre des tunnels unidirectionnels, suggérant que des adversaires déterminés peuvent finir par confirmer des pairs persistants. Les retours de la communauté notent que l'étude repose sur des hypothèses spécifiques concernant la patience de l'adversaire et ses pouvoirs juridiques, et ne compare pas cette approche aux attaques par temporisation qui touchent les conceptions bidirectionnelles. Les recherches continues et l'expérience pratique ne cessent de conforter les tunnels unidirectionnels comme un choix délibéré en matière d'anonymat plutôt qu'un oubli.
