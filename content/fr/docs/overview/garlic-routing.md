---
title: "Garlic Routing"
description: "Comprendre la terminologie, l'architecture et l'implémentation du garlic routing dans I2P"
slug: "garlic-routing"
aliases:
  - "/fr/how_garlicrouting"
  - "/fr/how_garlicrouting/"
lastUpdated: "2025-10"
accurateFor: "0.9.12"
---

## Routage Garlic et Terminologie "Garlic"

Les termes "garlic routing" et "garlic encryption" sont souvent utilisés de manière assez vague lorsqu'on fait référence à la technologie d'I2P. Ici, nous expliquons l'historique de ces termes, leurs différentes significations, et l'utilisation des méthodes "garlic" dans I2P.

Le terme "Garlic routing" a été utilisé pour la première fois par [Michael J. Freedman](https://www.cs.princeton.edu/~mfreed/) dans la [thèse de Master](https://www.freehaven.net/papers.html) de Roger Dingledine sur Free Haven, Section 8.1.1 (juin 2000), comme dérivé du [Onion Routing](https://www.onion-router.net/).

"Garlic" a peut-être été utilisé à l'origine par les développeurs I2P parce qu'I2P implémente une forme de regroupement comme le décrit Freedman, ou simplement pour souligner les différences générales avec Tor. Le raisonnement spécifique a peut-être été perdu dans l'histoire. En général, lorsqu'on fait référence à I2P, le terme "garlic" peut signifier l'une des trois choses suivantes :

1. Chiffrement par couches
2. Regroupement de plusieurs messages ensemble
3. Chiffrement ElGamal/AES

Malheureusement, l'usage de la terminologie "garlic" par I2P au cours des dernières années n'a pas toujours été précis ; par conséquent, le lecteur doit faire preuve de prudence lorsqu'il rencontre ce terme. Espérons que l'explication ci-dessous clarifiera les choses.

### Chiffrement en couches

Le routage en oignon est une technique pour construire des chemins, ou tunnels, à travers une série de pairs, puis utiliser ce tunnel. Les messages sont chiffrés de manière répétée par l'expéditeur, puis déchiffrés par chaque saut. Pendant la phase de construction, seules les instructions de routage pour le saut suivant sont exposées à chaque pair. Pendant la phase de fonctionnement, les messages sont transmis à travers le tunnel, et le message ainsi que ses instructions de routage ne sont exposés qu'au point de terminaison du tunnel.

Ceci est similaire à la façon dont Mixmaster (voir [comparaisons de réseaux](/docs/overview/comparison/)) envoie les messages - prendre un message, le chiffrer avec la clé publique du destinataire, prendre ce message chiffré et le chiffrer (avec les instructions spécifiant le saut suivant), puis prendre ce message chiffré résultant et ainsi de suite, jusqu'à avoir une couche de chiffrement par saut le long du chemin.

En ce sens, le "garlic routing" en tant que concept général est identique au "onion routing". Tel qu'implémenté dans I2P, bien sûr, il existe plusieurs différences par rapport à l'implémentation dans Tor ; voir ci-dessous. Même ainsi, il y a des similitudes substantielles de sorte qu'I2P bénéficie d'une [grande quantité de recherches académiques sur l'onion routing](https://www.onion-router.net/Publications.html), [Tor, et des mixnets similaires](https://freehaven.net/anonbib/topic.html).

### Regroupement de plusieurs messages

Michael Freedman a défini le "garlic routing" comme une extension de l'onion routing, dans laquelle plusieurs messages sont regroupés ensemble. Il a appelé chaque message un "bulb". Tous les messages, chacun avec ses propres instructions de livraison, sont exposés au point de terminaison. Cela permet le regroupement efficace d'un "reply block" d'onion routing avec le message original.

Ce concept est implémenté dans I2P, comme décrit ci-dessous. Notre terme pour les "bulbes" de garlic encryption est "cloves" (gousses). N'importe quel nombre de messages peut être contenu, au lieu d'un seul message. Il s'agit d'une distinction importante par rapport au routage en oignon implémenté dans Tor. Cependant, ce n'est qu'une des nombreuses différences architecturales majeures entre I2P et Tor ; peut-être que cela ne suffit pas, en soi, à justifier un changement de terminologie.

Une autre différence par rapport à la méthode décrite par Freedman est que le chemin est unidirectionnel - il n'y a pas de "point de retournement" comme on le voit dans le routage en oignon ou les blocs de réponse mixmaster, ce qui simplifie grandement l'algorithme et permet une livraison plus flexible et fiable.

### Chiffrement ElGamal/AES

Dans certains cas, "garlic encryption" peut simplement signifier un chiffrement [ElGamal/AES+SessionTag](/docs/specs/elgamal-aes/) (sans plusieurs couches).

---

## Méthodes "Garlic" dans I2P

Maintenant que nous avons défini les différents termes liés au "garlic", nous pouvons dire qu'I2P utilise le routage garlic, le regroupement et le chiffrement à trois endroits :

1. Pour construire et router à travers les tunnels (chiffrement en couches)
2. Pour déterminer le succès ou l'échec de la livraison de messages de bout en bout (groupement)
3. Pour publier certaines entrées de la base de données réseau (atténuant la probabilité d'une attaque d'analyse de trafic réussie) (ElGamal/AES)

Il existe également des moyens significatifs d'utiliser cette technique pour améliorer les performances du réseau, en exploitant les compromis latence/débit de transport, et en distribuant les données à travers des chemins redondants pour augmenter la fiabilité.

### Construction et routage des tunnels

Dans I2P, les tunnels sont unidirectionnels. Chaque partie construit deux tunnels, un pour le trafic sortant et un pour le trafic entrant. Par conséquent, quatre tunnels sont nécessaires pour un seul message aller-retour et sa réponse.

Les tunnels sont construits, puis utilisés, avec un chiffrement en couches. Ceci est décrit sur la [page d'implémentation des tunnels](/docs/specs/tunnel-implementation/). Nous utilisons [ElGamal/AES+SessionTag](/docs/specs/elgamal-aes/) pour le chiffrement.

Les tunnels sont un mécanisme polyvalent pour transporter tous les [messages I2NP](/docs/specs/i2np/), et les messages Garlic ne sont pas utilisés pour construire les tunnels. Nous ne regroupons pas plusieurs messages I2NP dans un seul message Garlic pour le déballage au point de terminaison du tunnel sortant ; le chiffrement du tunnel est suffisant.

### Regroupement de messages de bout en bout

À la couche au-dessus des tunnels, I2P livre des messages de bout en bout entre les [Destinations](/docs/specs/common-structures/). Tout comme à l'intérieur d'un seul tunnel, nous utilisons [ElGamal/AES+SessionTag](/docs/specs/elgamal-aes/) pour le chiffrement. Chaque message client livré au router via l'[interface I2CP](/docs/api/i2cp/) devient un seul Garlic Clove avec ses propres Instructions de Livraison, à l'intérieur d'un Message Garlic. Les Instructions de Livraison peuvent spécifier une Destination, un Router, ou un Tunnel.

En général, un Garlic Message ne contiendra qu'un seul clove. Cependant, le router regroupera périodiquement deux cloves supplémentaires dans le Garlic Message :

![Garlic Message Cloves](/images/garliccloves.svg)

1. **Un Message de Statut de Livraison**, avec des Instructions de Livraison spécifiant qu'il doit être renvoyé au router d'origine comme accusé de réception. Ceci est similaire au "bloc de réponse" ou "oignon de réponse" décrit dans les références. Il est utilisé pour déterminer le succès ou l'échec de la livraison de message de bout en bout. Le router d'origine peut, en cas d'échec de réception du Message de Statut de Livraison dans la période de temps attendue, modifier le routage vers la Destination distante, ou prendre d'autres actions.

2. **Un message Database Store**, contenant un LeaseSet pour la Destination d'origine, avec des Instructions de Livraison spécifiant le router de destination finale. En regroupant périodiquement un LeaseSet, le router s'assure que l'extrémité distante sera capable de maintenir les communications. Sinon, l'extrémité distante devrait interroger un router floodfill pour l'entrée de la base de données réseau, et tous les LeaseSets devraient être publiés dans la base de données réseau, comme expliqué sur la [page de la base de données réseau](/docs/specs/common-structures/).

Par défaut, les messages Delivery Status et Database Store sont regroupés lorsque le LeaseSet local change, lorsque des Session Tags supplémentaires sont livrées, ou si les messages n'ont pas été regroupés dans la minute précédente.

Évidemment, les messages supplémentaires sont actuellement regroupés à des fins spécifiques, et ne font pas partie d'un système de routage à usage général.

À partir de la version 0.9.12, le Message de Statut de Livraison est encapsulé dans un autre Message Garlic par l'expéditeur de sorte que le contenu soit chiffré et non visible aux routeurs sur le chemin de retour.

### Stockage dans la base de données réseau Floodfill

Comme expliqué sur la [page de base de données réseau](/docs/specs/common-structures/), les leaseSets locaux sont envoyés aux routeurs floodfill dans un message Database Store encapsulé dans un message garlic afin qu'il ne soit pas visible à la passerelle sortante du tunnel.

---

## Travaux futurs

Le mécanisme de message Garlic est très flexible et fournit une structure pour implémenter de nombreux types de méthodes de livraison de mixnet. Avec l'option de délai inutilisée dans les instructions de livraison des messages de tunnel, un large éventail de stratégies de traitement par lots, de délai, de mélange et de routage sont possibles.

En particulier, il existe un potentiel pour beaucoup plus de flexibilité au point de terminaison du tunnel sortant. Les messages pourraient éventuellement être routés de là vers l'un de plusieurs tunnels (minimisant ainsi les connexions point-à-point), ou diffusés en multicast vers plusieurs tunnels pour la redondance, ou pour la diffusion audio et vidéo en streaming.

De telles expériences peuvent entrer en conflit avec le besoin d'assurer la sécurité et l'anonymat, comme limiter certains chemins de routage, restreindre les types de messages I2NP qui peuvent être transférés le long de divers chemins, et faire respecter certains délais d'expiration des messages.

Dans le cadre du chiffrement ElGamal/AES, un message garlic contient une quantité de données de remplissage spécifiée par l'expéditeur, permettant à celui-ci de prendre des contre-mesures actives contre l'analyse de trafic. Ceci n'est actuellement pas utilisé, au-delà de l'exigence de compléter à un multiple de 16 octets.

Chiffrement de messages supplémentaires vers et depuis les [floodfill routers](/docs/specs/common-structures/).

---

## Références

- Le terme garlic routing a été utilisé pour la première fois dans la [thèse de maîtrise](https://www.freehaven.net/papers.html) de Roger Dingledine sur Free Haven (juin 2000), voir la Section 8.1.1 rédigée par [Michael J. Freedman](https://www.cs.princeton.edu/~mfreed/).
- [Publications Onion Router](https://www.onion-router.net/Publications.html)
- [Routage en oignon (Wikipedia)](https://en.wikipedia.org/wiki/Onion_routing)
- [Garlic Routing (Wikipedia)](https://en.wikipedia.org/wiki/Garlic_routing)
- [Projet Tor](https://www.torproject.org/)
- [Free Haven Anonbib](https://freehaven.net/anonbib/topic.html)
- Le routage en oignon a été décrit pour la première fois dans [Hiding Routing Information](https://www.onion-router.net/Publications/IH-1996.pdf) par David M. Goldschlag, Michael G. Reed, et Paul F. Syverson en 1996.
