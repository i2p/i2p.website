---
title: "Spécification des messages de tunnel"
description: "Spécification du format des messages de tunnel dans I2P"
slug: "tunnel-message"
aliases:
  - "/fr/docs/legacy/tunnel-message"
  - "/fr/docs/legacy/tunnel-message/"
  - "/fr/tunnel_message_spec"
  - "/fr/tunnel_message_spec/"
category: "Conception"
lastUpdated: "2021-01"
accurateFor: "0.9.49"
---

## Aperçu

Ce document spécifie le format des messages de tunnel. Pour des informations générales sur les tunnels, voir la [documentation des tunnels](/docs/specs/tunnel-implementation).

## Prétraitement des messages

Un *tunnel gateway* est l'entrée, ou premier saut, d'un tunnel. Pour un tunnel sortant, le gateway est le créateur du tunnel. Pour un tunnel entrant, le gateway se trouve à l'extrémité opposée du créateur du tunnel.

Une passerelle *prétraite* les messages [I2NP](/docs/specs/i2np) en les fragmentant et en les combinant dans des messages de tunnel.

Bien que les messages I2NP soient de taille variable, de 0 à près de 64 Ko, les messages de tunnel ont une taille fixe d'environ 1 Ko. La taille fixe des messages limite plusieurs types d'attaques qui seraient possibles en observant la taille des messages.

Après la création des messages de tunnel, ils sont chiffrés comme décrit dans la [documentation des tunnels](/docs/specs/tunnel-implementation).

### Message de tunnel (chiffré)

Voici le contenu d'un message de données de tunnel après chiffrement.

```
+----+----+----+----+----+----+----+----+
|    Tunnel ID      |       IV          |
+----+----+----+----+                   +
|                                       |
+                   +----+----+----+----+
|                   |                   |
+----+----+----+----+                   +
|                                       |
+           Encrypted Data              +
~                                       ~
|                                       |
+                   +-------------------+
|                   |
+----+----+----+----+
```
**ID de Tunnel** :: [TunnelId](/docs/specs/common-structures#tunnelid) : 4 octets. L'ID du prochain saut, non nul.

**IV** :: : 16 octets. Le vecteur d'initialisation.

**Données Chiffrées** :: : 1008 octets. Le message tunnel chiffré.

**Taille totale : 1028 octets**

### Message de Tunnel (Déchiffré)

Voici le contenu d'un message de données de tunnel une fois déchiffré.

```
+----+----+----+----+----+----+----+----+
|    Tunnel ID      |       IV          |
+----+----+----+----+                   +
|                                       |
+                   +----+----+----+----+
|                   |     Checksum      |
+----+----+----+----+----+----+----+----+
|          nonzero padding...           |
~                                       ~
|                                       |
+                                  +----+
|                                  |zero|
+----+----+----+----+----+----+----+----+
|                                       |
|       Delivery Instructions  1        |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+       I2NP Message Fragment 1         +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
|       Delivery Instructions 2...      |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+       I2NP Message Fragment 2...      +
|                                       |
~                                       ~
|                                       |
+                   +-------------------+
|                   |
+----+----+----+----+
```
**ID de tunnel** :: [TunnelId](/docs/specs/common-structures#tunnelid) : 4 octets. L'ID du prochain saut, non nul.

**IV** :: : 16 octets. Le vecteur d'initialisation.

**Checksum** :: : 4 octets. Les 4 premiers octets du hachage SHA256 de (le contenu du message (après l'octet zéro) + IV).

**Bourrage non nul** :: : 0 ou plusieurs octets. Données aléatoires non nulles pour le bourrage.

**Zero** :: : 1 octet. La valeur 0x00.

**Instructions de livraison** :: TunnelMessageDeliveryInstructions : La longueur varie mais est généralement de 7, 39, 43 ou 47 octets. Indique le fragment et le routage pour le fragment.

**Fragment de Message** :: : 1 à 996 octets, le maximum réel dépend de la taille de l'instruction de livraison. Un message I2NP partiel ou complet.

**Taille totale : 1028 octets**

#### Notes

- Le remplissage, s'il y en a, doit être avant les paires instruction/message. Il n'y a pas de disposition pour le remplissage à la fin.
- La somme de contrôle ne couvre PAS le remplissage ou l'octet zéro. Prenez le message en commençant aux premières instructions de livraison, concaténez l'IV, et calculez le Hash de cela.

## Instructions de livraison des messages tunnel

Les instructions sont encodées avec un seul octet de contrôle, suivi de toute information supplémentaire nécessaire. Le premier bit (MSB) de cet octet de contrôle détermine comment le reste de l'en-tête est interprété - s'il n'est pas défini, le message n'est soit pas fragmenté, soit il s'agit du premier fragment du message. S'il est défini, il s'agit d'un fragment suivant.

Cette spécification concerne uniquement les Instructions de Livraison à l'intérieur des Messages de tunnel. Notez que les "Instructions de Livraison" sont également utilisées à l'intérieur des Garlic Cloves, où le format est significativement différent. Voir la [documentation I2NP](/docs/specs/i2np#garlicclovedeliveryinstructions) pour plus de détails. N'utilisez PAS la spécification suivante pour les Instructions de Livraison des Garlic Cloves !

### Instructions de livraison du premier fragment

Si le MSB du premier octet est 0, ceci est un fragment de message I2NP initial, ou un message I2NP complet (non fragmenté), et les instructions sont :

```
+----+----+----+----+----+----+----+----+
|flag|  Tunnel ID (opt)  |              |
+----+----+----+----+----+              +
|                                       |
+                                       +
|         To Hash (optional)            |
+                                       +
|                                       |
+                        +--------------+
|                        |dly | Message
+----+----+----+----+----+----+----+----+
 ID (opt) |extended opts (opt)|  size   |
+----+----+----+----+----+----+----+----+
```
**flag** :: : 1 octet. Ordre des bits : 76543210   - bit 7 : 0 pour spécifier un fragment initial ou un message non fragmenté   - bits 6-5 : type de livraison

    - 0x0 = LOCAL
    - 0x01 = TUNNEL
    - 0x02 = ROUTER
    - 0x03 = unused, invalid
    - Note: LOCAL is used for inbound tunnels only, unimplemented for outbound tunnels
- bit 4 : délai inclus ? Non implémenté, toujours 0. Si 1, un octet de délai est inclus.
  - bit 3 : fragmenté ? Si 0, le message n'est pas fragmenté, ce qui suit est le message entier. Si 1, le message est fragmenté, et les instructions contiennent un ID de message.
  - bit 2 : options étendues ? Non implémenté, toujours 0. Si 1, les options étendues sont incluses.
  - bits 1-0 : réservés, définis à 0 pour la compatibilité avec les utilisations futures

**ID de tunnel** :: [TunnelId](/docs/specs/common-structures#tunnelid) : 4 octets. Optionnel, présent si le type de livraison est TUNNEL. L'ID du tunnel de destination, non nul.

**To Hash** :: : 32 octets. Optionnel, présent si le type de livraison est ROUTER ou TUNNEL. Si ROUTER, le hachage SHA256 du router. Si TUNNEL, le hachage SHA256 du router de passerelle.

**Délai** :: : 1 octet. Optionnel, présent si le flag d'inclusion du délai est défini. Dans les messages tunnel : Non implémenté, jamais présent ; spécification originale : bit 7 : type (0 = strict, 1 = randomisé), bits 6-0 : exposant du délai (2^valeur minutes).

**ID du Message** :: : 4 octets. Optionnel, présent si ce message est le premier de 2 fragments ou plus (c'est-à-dire si le bit fragmenté est à 1). Un ID qui identifie de manière unique tous les fragments comme appartenant à un seul message (l'implémentation actuelle utilise I2NPMessageHeader.msg_id).

**Options étendues** :: : 2 octets ou plus. Optionnel, présent si le drapeau d'options étendues est défini. Non implémenté, jamais présent ; spécification originale : Un octet de longueur puis autant d'octets.

**size** :: : 2 octets. La longueur du fragment qui suit. Valeurs valides : 1 à environ 960 dans un message de tunnel.

**Longueur totale :** La longueur typique est : - 3 octets pour la livraison LOCAL (message tunnel) - 35 octets pour la livraison ROUTER ou 39 octets pour la livraison TUNNEL (message tunnel non fragmenté) - 39 octets pour la livraison ROUTER ou 43 octets pour la livraison TUNNEL (premier fragment)

### Instructions de livraison des fragments de suivi

Si le MSB du premier octet est 1, il s'agit d'un fragment de continuation, et les instructions sont :

```
+----+----+----+----+----+----+----+
|frag|     Message ID    |  size   |
+----+----+----+----+----+----+----+
```
**frag** :: : 1 octet. Ordre des bits : 76543210. Binaire 1nnnnnnd :   - bit 7 : 1 pour indiquer qu'il s'agit d'un fragment de suivi   - bits 6-1 : nnnnnn est le numéro de fragment sur 6 bits de 1 à 63   - bit 0 : d est 1 pour indiquer le dernier fragment, 0 sinon

**ID de Message** :: : 4 octets. Identifie la séquence de fragments à laquelle ce fragment appartient. Ceci correspondra à l'ID de message d'un fragment initial (un fragment avec le bit de flag 7 défini à 0 et le bit de flag 3 défini à 1).

**size** :: : 2 octets. La longueur du fragment qui suit. Valeurs valides : 1 à 996.

**Longueur totale : 7 octets**

## Notes

### Taille maximale des messages I2NP

Bien que la taille maximale des messages I2NP soit nominalement de 64 Ko, la taille est davantage contrainte par la méthode de fragmentation des messages I2NP en plusieurs messages tunnel de 1 Ko. Le nombre maximum de fragments est de 64, et le fragment initial peut ne pas être parfaitement aligné au début d'un message tunnel. Ainsi, le message doit nominalement tenir dans 63 fragments.

La taille maximale d'un fragment initial est de 956 octets (en supposant le mode de livraison TUNNEL) ; la taille maximale d'un fragment de suivi est de 996 octets. Par conséquent, la taille maximale est d'environ 956 + (62 * 996) = 62708 octets, soit 61,2 Ko.

### Ordonnancement, Regroupement, Empaquetage

Les messages de tunnel peuvent être supprimés ou réordonnés. Le tunnel gateway, qui crée les messages de tunnel, est libre d'implémenter toute stratégie de mise en lot, de mélange ou de réordonnancement pour fragmenter les messages I2NP et empaqueter efficacement les fragments dans les messages de tunnel. En général, un empaquetage optimal n'est pas possible (le "problème d'empaquetage"). Les gateways peuvent implémenter diverses stratégies de délai et de réordonnancement.

### Trafic de Couverture

Les messages de tunnel peuvent contenir uniquement du remplissage (c'est-à-dire aucune instruction de livraison ou fragment de message) pour le trafic de couverture. Ceci n'est pas implémenté.

## Références

- **[I2NP]** [Protocole I2NP](/docs/specs/i2np)
- **[I2NP-GC]** [GarlicClove](/docs/specs/i2np#garlicclove)
- **[I2NP-GCDI]** [GarlicCloveDeliveryInstructions](/docs/specs/i2np#garlicclovedeliveryinstructions)
- **[TUNNEL-IMPL]** [Implémentation des tunnels](/docs/specs/tunnel-implementation)
