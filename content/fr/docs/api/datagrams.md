---
title: "Datagrammes"
description: "Formats de messages authentifiés, avec réponse possible et bruts au-dessus d'I2CP"
slug: "datagrams"
aliases:
  - "/fr/datagrams"
  - "/fr/datagrams/"
lastUpdated: "2025-04"
accurateFor: "0.9.66"
---

## Aperçu des datagrammes {#overview}

Les datagrammes s'appuient sur la base [I2CP](/docs/specs/i2cp) pour fournir des messages authentifiés et auxquels on peut répondre dans un format standard. Cela permet aux applications de lire de manière fiable l'adresse "expéditeur" d'un datagramme et de savoir que l'adresse a réellement envoyé le message. Ceci est nécessaire pour certaines applications car le message I2P de base est complètement brut - il n'a pas d'adresse "expéditeur" (contrairement aux paquets IP). De plus, le message et l'expéditeur sont authentifiés en signant la charge utile.

Les datagrammes, comme les [paquets de la bibliothèque de streaming](/docs/api/streaming), sont une construction de niveau application. Ces protocoles sont indépendants des [transports](/docs/overview/transport) de bas niveau ; les protocoles sont convertis en messages I2NP par le router, et chaque protocole peut être transporté par n'importe quel transport.

## Guide d'application {#application}

Les applications écrites en Java peuvent utiliser l'API datagram, tandis que les applications dans d'autres langages peuvent utiliser le support datagram de [SAM](/docs/api/samv3). Il existe également un support limité dans i2ptunnel dans le [proxy SOCKS](/docs/api/socks), les types de tunnel 'streamr', et les classes udpTunnel.

### Longueur du datagramme {#length}

Le concepteur d'application doit soigneusement considérer le compromis entre les datagrammes avec réponse et sans réponse. De plus, la taille du datagramme affectera la fiabilité, en raison de la fragmentation des tunnels en messages de tunnel de 1 Ko. Plus il y a de fragments de message, plus il est probable que l'un d'entre eux soit abandonné par un relais intermédiaire. Les messages de plus de quelques Ko ne sont pas recommandés. Au-delà d'environ 10 Ko, la probabilité de livraison chute considérablement.

[Voir la page de spécification des datagrammes.](/docs/specs/datagrams)

Notez également que les diverses surcharges ajoutées par les couches inférieures, en particulier les messages garlic, imposent une charge importante sur les messages intermittents tels que ceux utilisés par une application Kademlia-over-UDP. Les implémentations sont actuellement ajustées pour un trafic fréquent utilisant la bibliothèque de streaming.

### Numéro de protocole et ports I2CP {#protocol}

Le numéro de protocole I2CP standard pour les datagrammes signés (auxquels on peut répondre) est PROTO_DATAGRAM (17). Les applications peuvent choisir ou non de définir le protocole dans l'en-tête I2CP. La valeur par défaut dépend de l'implémentation. Il doit être défini pour démultiplexer le trafic de datagrammes et de streaming reçu sur la même Destination.

Comme les datagrammes ne sont pas orientés connexion, l'application peut nécessiter des numéros de port pour corréler les datagrammes avec des pairs particuliers ou des sessions de communication, comme c'est traditionnel avec UDP sur IP. Les applications peuvent ajouter des ports 'from' et 'to' à l'en-tête I2CP (gzip) comme décrit dans la [page I2CP](/docs/specs/i2cp#format).

Il n'existe aucune méthode dans l'API datagram pour spécifier s'il est non-répondable (brut) ou répondable. L'application doit être conçue pour attendre le type approprié. Le numéro de protocole I2CP ou le port doit être utilisé par l'application pour indiquer le type de datagram. Les numéros de protocole I2CP PROTO_DATAGRAM (signé, également connu sous le nom de Datagram1), PROTO_DATAGRAM_RAW, PROTO_DATAGRAM2, et PROTO_DATAGRAM3 sont définis dans l'API I2PSession à cette fin. Un modèle de conception courant dans les applications datagram client/serveur consiste à utiliser des datagrams signés pour une requête qui inclut un nonce, et à utiliser un datagram brut pour la réponse, en retournant le nonce de la requête.

**Valeurs par défaut :**

- PROTO_DATAGRAM = 17
- PROTO_DATAGRAM_RAW = 18
- PROTO_DATAGRAM2 = 19
- PROTO_DATAGRAM3 = 20

### Intégrité des données {#integrity}

L'intégrité des données est assurée par la somme de contrôle gzip CRC-32 implémentée dans [la couche I2CP](/docs/specs/i2cp#format). Les datagrammes authentifiés (Datagram1 et Datagram2) garantissent également l'intégrité. Il n'y a pas de champ de somme de contrôle dans le protocole datagramme.

### Encapsulation des paquets {#encapsulation}

Chaque datagramme est envoyé à travers I2P comme un message unique (ou comme un clove individuel dans un [Message Garlic](/docs/overview/garlic-routing)). L'encapsulation des messages est implémentée dans les couches sous-jacentes [I2CP](/docs/specs/i2cp), [I2NP](/docs/specs/i2np), et [message tunnel](/docs/specs/tunnel-message). Il n'y a pas de mécanisme de délimiteur de paquets ou de champ de longueur dans le protocole de datagramme.

## Spécification {#spec}

[Voir la page Spécification des datagrammes.](/docs/specs/datagrams)
