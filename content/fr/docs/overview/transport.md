---
title: "Aperçu du transport"
description: "Aperçu de la couche transport d'I2P pour la communication router à router point-à-point"
slug: "transport"
aliases:
  - "/fr/transport"
  - "/fr/transport/"
lastUpdated: "2026-03"
accurateFor: "0.9.69"
---

## Transports dans I2P

Un "transport" dans I2P est une méthode de communication directe, point à point entre deux routers. Les transports doivent fournir la confidentialité et l'intégrité contre les adversaires externes tout en authentifiant que le router contacté est bien celui qui devrait recevoir un message donné.

I2P prend en charge plusieurs transports simultanément. Il existe actuellement trois transports implémentés :

1. [NTCP](/docs/legacy/ntcp/), un transport TCP Java New I/O (NIO)
2. [SSU](/docs/legacy/ssu/), ou Secure Semireliable UDP
3. [NTCP2](/docs/specs/ntcp2/), une nouvelle version de NTCP

Chacun fournit un paradigme de "connexion", avec authentification, contrôle de flux, accusés de réception et retransmission.

- Livraison fiable des messages [I2NP](/docs/specs/i2np/). Les transports prennent en charge la livraison de messages I2NP UNIQUEMENT. Ce ne sont pas des canaux de données à usage général.
- La livraison ordonnée des messages n'est PAS garantie par tous les transports.
- Maintenir un ensemble d'adresses de router, une ou plusieurs pour chaque transport, que le router publie comme ses informations de contact globales (le RouterInfo). Chaque transport peut se connecter en utilisant l'une de ces adresses, qui peut être IPv4 ou (à partir de la version 0.9.8) IPv6.
- Sélection du meilleur transport pour chaque message sortant
- Mise en file d'attente des messages sortants par priorité
- Limitation de bande passante, tant sortante qu'entrante, selon la configuration du router
- Établissement et rupture des connexions de transport
- Chiffrement des communications point à point
- Maintien des limites de connexion pour chaque transport, mise en œuvre de divers seuils pour ces limites, et communication du statut des seuils au router afin qu'il puisse apporter des modifications opérationnelles basées sur le statut
- Ouverture de port de pare-feu utilisant UPnP (Universal Plug and Play)
- Traversée coopérative de NAT/Pare-feu
- Détection d'IP locale par diverses méthodes, incluant UPnP, inspection des connexions entrantes, et énumération des périphériques réseau
- Coordination du statut de pare-feu et de l'IP locale, et des changements de l'un ou l'autre, parmi les transports
- Communication du statut de pare-feu et de l'IP locale, et des changements de l'un ou l'autre, au router et à l'interface utilisateur
- Détermination d'une horloge de consensus, qui est utilisée pour mettre à jour périodiquement l'horloge du router, comme sauvegarde pour NTP
- Maintien du statut pour chaque pair, incluant s'il est connecté, s'il était récemment connecté, et s'il était atteignable lors de la dernière tentative
- Qualification des adresses IP valides selon un ensemble de règles locales
- Respect des listes automatisées et manuelles de pairs bannis maintenues par le router, et refus des connexions sortantes et entrantes vers ces pairs

---

Le sous-système de transport dans I2P fournit les services suivants :

## Services de transport

---

- Un router n'a pas d'adresses publiées, il est donc considéré comme "caché" et ne peut pas recevoir de connexions entrantes
- Un router est derrière un pare-feu, et publie donc une adresse SSU qui contient une liste de pairs coopérants ou "introducers" qui aideront à la traversée NAT (voir [la spécification SSU](/docs/legacy/ssu/) pour plus de détails)
- Un router n'est pas derrière un pare-feu ou ses ports NAT sont ouverts ; il publie des adresses NTCP et SSU contenant des IP et ports directement accessibles.

Le sous-système de transport maintient un ensemble d'adresses de router, chacune répertoriant une méthode de transport, une IP et un port. Ces adresses constituent les points de contact annoncés et sont publiées par le router dans la base de données réseau. Les adresses peuvent également contenir un ensemble arbitraire d'options supplémentaires.

## Adresses de transport

Chaque méthode de transport peut publier plusieurs adresses de router.

Les scénarios typiques sont :

---

- Configuration des préférences de transport
- Si le transport est déjà connecté au pair
- Le nombre de connexions actuelles comparé aux différents seuils de limite de connexion
- Si les tentatives de connexion récentes au pair ont échoué
- La taille du message, car différents transports ont des limites de taille différentes
- Si le pair peut accepter des connexions entrantes pour ce transport, comme annoncé dans son RouterInfo
- Si la connexion serait indirecte (nécessitant des introducers) ou directe
- La préférence de transport du pair, comme annoncée dans son RouterInfo

Le système de transport livre uniquement les [messages I2NP](/docs/specs/i2np/). Le transport sélectionné pour tout message est indépendant des protocoles et contenus des couches supérieures (messages de router ou de client, qu'une application externe utilise TCP ou UDP pour se connecter à I2P, que la couche supérieure utilise [la bibliothèque de streaming](/docs/api/streaming/) ou les [datagrammes](/docs/api/datagrams/), etc.).

## Sélection du transport

Pour chaque message sortant, le système de transport sollicite des "offres" de chaque transport. Le transport offrant la valeur la plus basse (meilleure) remporte l'enchère et reçoit le message à livrer. Un transport peut refuser de faire une offre.

Le fait qu'un transport fasse une offre, et avec quelle valeur, dépend de nombreux facteurs :

En général, les valeurs d'enchères sont sélectionnées de sorte que deux routeurs ne soient connectés que par un seul transport à la fois. Cependant, ce n'est pas une exigence.

- Un transport ressemblant à TLS/SSH
- Un transport "indirect" pour les routeurs qui ne sont pas accessibles par tous les autres routeurs (une forme de "routes restreintes")
- Des transports enfichables compatibles avec Tor

---

Des transports supplémentaires peuvent être développés, notamment :

## Nouveaux Transports et Travaux Futurs

Le travail continue sur l'ajustement des limites de connexion par défaut pour chaque transport. I2P est conçu comme un "réseau maillé", où il est supposé que tout router peut se connecter à tout autre router. Cette supposition peut être compromise par des routers qui ont dépassé leurs limites de connexion, et par des routers qui sont derrière des pare-feu d'état restrictifs (routes restreintes).

- Un transport similaire à TLS/SSH
- Un transport « indirect » pour les routeurs qui ne sont pas accessibles par tous les autres routeurs (une forme de « routes restreintes »)
- Des transports extensibles compatibles avec Tor

Les limites de connexion actuelles sont plus élevées pour SSU que pour NTCP, basées sur l'hypothèse que les exigences mémoire pour une connexion NTCP sont plus élevées que celles pour SSU. Cependant, comme les tampons NTCP sont partiellement dans le noyau et les tampons SSU sont sur le tas Java, cette hypothèse est difficile à vérifier.

Analysez [Breaking and Improving Protocol Obfuscation](http://www.iis.se/docs/hjelmvik_breaking.pdf) et voyez comment le remplissage au niveau de la couche transport pourrait améliorer les choses.

Analyser [Breaking and Improving Protocol Obfuscation](http://www.iis.se/docs/hjelmvik_breaking.pdf) et voir comment le bourrage au niveau de la couche transport pourrait améliorer les choses.
