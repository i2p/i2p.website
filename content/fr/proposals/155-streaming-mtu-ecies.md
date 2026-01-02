---
title: "MTU de Streaming pour Destinations ECIES"
number: "155"
author: "zzz"
created: "2020-05-06"
lastupdated: "2020-05-30"
status: "Fermé"
thread: "http://zzz.i2p/topics/2886"
target: "0.9.47"
implementedin: "0.9.47"
toc: true
---

## Note
Déploiement et test du réseau en cours.
Sujet à des révisions mineures.


## Vue d'ensemble


### Résumé

ECIES réduit la surcharge des messages de session existants (ES) d'environ 90 octets.
Par conséquent, nous pouvons augmenter le MTU d'environ 90 octets pour les connexions ECIES.
Voir the [ECIES specification](/docs/specs/ecies/#overhead), [Streaming specification](/docs/specs/streaming/#flags-and-option-data-fields), and [Streaming API documentation](/docs/api/streaming/).

Sans augmenter le MTU, dans de nombreux cas, les économies de surcharge ne sont pas vraiment 'sauvées',
car les messages seront remplis pour utiliser deux messages de tunnel complets de toute façon.

Cette proposition ne nécessite aucun changement aux spécifications.
Elle est postée en tant que proposition uniquement pour faciliter la discussion et la construction d'un consensus
sur la valeur recommandée et les détails de l'implémentation.


### Objectifs

- Augmenter le MTU négocié
- Maximiser l'utilisation des messages de tunnel de 1 Ko
- Ne pas changer le protocole de streaming


## Conception

Utiliser l'option existante MAX_PACKET_SIZE_INCLUDED et la négociation MTU.
Le streaming continue d'utiliser le minimum du MTU envoyé et reçu.
La valeur par défaut reste 1730 pour toutes les connexions, peu importe les clés utilisées.

Les implémentations sont encouragées à inclure l'option MAX_PACKET_SIZE_INCLUDED dans tous les paquets SYN, dans les deux sens,
bien que cela ne soit pas une exigence.

Si une destination est uniquement ECIES, utilisez la valeur plus élevée (en tant qu'Alice ou Bob).
Si une destination est à double clé, le comportement peut varier :

Si le client à double clé est à l'extérieur du routeur (dans une application externe),
il peut ne pas "savoir" la clé utilisée à l'extrémité opposée, et Alice peut demander
une valeur plus élevée dans le SYN, tandis que les données max dans le SYN restent 1730.

Si le client à double clé est à l'intérieur du routeur, l'information sur la clé
utilisée peut ou non être connue du client.
Le leaseset peut ne pas avoir encore été récupéré, ou les interfaces API internes
peuvent ne pas facilement rendre cette information disponible pour le client.
Si l'information est disponible, Alice peut utiliser la valeur plus élevée ;
sinon, Alice doit utiliser la valeur standard de 1730 jusqu'à négociation.

Un client à double clé en tant que Bob peut envoyer la valeur plus élevée en réponse,
même si aucune valeur ou une valeur de 1730 n'a été reçue d'Alice ;
cependant, il n'y a pas de disposition pour négocier vers le haut dans le streaming,
donc le MTU devrait rester à 1730.


Comme noté dans the [Streaming API documentation](/docs/api/streaming/),
les données dans les paquets SYN envoyés d'Alice à Bob peuvent dépasser le MTU de Bob.
C'est une faiblesse dans le protocole de streaming.
Par conséquent, les clients à double clé doivent limiter les données dans les paquets SYN envoyés
à 1730 octets, tout en envoyant une option MTU plus élevée.
Une fois que le MTU plus élevé est reçu de Bob, Alice peut augmenter la charge utile maximum
réellement envoyée.


### Analyse

Comme décrit dans the [ECIES specification](/docs/specs/ecies/#overhead), la surcharge ElGamal pour les messages de session existants est
de 151 octets, et la surcharge Ratchet est de 69 octets.
Par conséquent, nous pouvons augmenter le MTU pour les connexions ratchet de (151 - 69) = 82 octets,
passant de 1730 à 1812.


## Spécification

Ajoutez les modifications et clarifications suivantes à la section Sélection et Négociation du MTU de the [Streaming API documentation](/docs/api/streaming/).
Aucun changement à the [Streaming specification](/docs/specs/streaming/).


La valeur par défaut de l'option i2p.streaming.maxMessageSize reste 1730 pour toutes les connexions, peu importe les clés utilisées.
Les clients doivent utiliser le minimum du MTU envoyé et reçu, comme d'habitude.

Il y a quatre constantes et variables MTU liées :

- DEFAULT_MTU: 1730, inchangé, pour toutes les connexions
- i2cp.streaming.maxMessageSize: par défaut 1730 ou 1812, peut être modifié par configuration
- ALICE_SYN_MAX_DATA: Les données maximum qu'Alice peut inclure dans un paquet SYN
- negotiated_mtu: Le minimum du MTU d'Alice et de Bob, à utiliser comme taille max de données
  dans le SYN ACK de Bob à Alice, et dans tous les paquets suivants envoyés dans les deux sens


Il y a cinq cas à considérer :


### 1) Alice uniquement ElGamal
Aucun changement, MTU de 1730 dans tous les paquets.

- ALICE_SYN_MAX_DATA = 1730
- i2cp.streaming.maxMessageSize par défaut : 1730
- Alice peut envoyer MAX_PACKET_SIZE_INCLUDED dans SYN, non requis sauf si != 1730


### 2) Alice uniquement ECIES
MTU de 1812 dans tous les paquets.

- ALICE_SYN_MAX_DATA = 1812
- i2cp.streaming.maxMessageSize par défaut : 1812
- Alice doit envoyer MAX_PACKET_SIZE_INCLUDED dans SYN


### 3) Alice Double Clé et sait que Bob est ElGamal
MTU de 1730 dans tous les paquets.

- ALICE_SYN_MAX_DATA = 1730
- i2cp.streaming.maxMessageSize par défaut : 1812
- Alice peut envoyer MAX_PACKET_SIZE_INCLUDED dans SYN, non requis sauf si != 1730


### 4) Alice Double Clé et sait que Bob est ECIES
MTU de 1812 dans tous les paquets.

- ALICE_SYN_MAX_DATA = 1812
- i2cp.streaming.maxMessageSize par défaut : 1812
- Alice doit envoyer MAX_PACKET_SIZE_INCLUDED dans SYN


### 5) Alice Double Clé et Bob clé inconnue
Envoyez 1812 comme MAX_PACKET_SIZE_INCLUDED dans le paquet SYN mais limitez les données du paquet SYN à 1730.

- ALICE_SYN_MAX_DATA = 1730
- i2cp.streaming.maxMessageSize par défaut : 1812
- Alice doit envoyer MAX_PACKET_SIZE_INCLUDED dans SYN


### Pour tous les cas

Alice et Bob calculent
negotiated_mtu, le minimum du MTU d'Alice et de Bob, à utiliser comme taille max de données
dans le SYN ACK de Bob à Alice, et dans tous les paquets suivants envoyés dans les deux sens.


## Justification

Voir the [Java I2P source code](https://github.com/i2p/i2p.i2p/blob/master/apps/streaming/java/src/net/i2p/client/streaming/impl/ConnectionOptions.java#L220) pour savoir pourquoi la valeur actuelle est 1730.
Voir the [ECIES specification](/docs/specs/ecies/#overhead) pour savoir pourquoi la surcharge ECIES est de 82 octets de moins que ElGamal.


## Notes d'implémentation

Si le streaming crée des messages de taille optimale, il est très important que
la couche ECIES-Ratchet ne remplisse pas au-delà de cette taille.

La taille optimale du message Garlic à intégrer dans deux messages de tunnel,
y compris l'en-tête I2NP du message Garlic de 16 octets, la longueur du message Garlic de 4 octets,
le tag ES de 8 octets, et le MAC de 16 octets, est de 1956 octets.

Un algorithme de remplissage recommandé dans ECIES est le suivant :

- Si la longueur totale du message Garlic serait de 1954 à 1956 octets,
  ne pas ajouter de bloc de remplissage (pas de place)
- Si la longueur totale du message Garlic serait de 1938 à 1953 octets,
  ajouter un bloc de remplissage pour remplir exactement à 1956 octets.
- Sinon, remplir comme d'habitude, par exemple avec une quantité aléatoire de 0 à 15 octets.

Des stratégies similaires pourraient être utilisées à la taille optimale pour un message de tunnel (964)
et la taille pour trois messages de tunnel (2952), bien que ces tailles devraient être rares en pratique.


## Problèmes

La valeur de 1812 est préliminaire. À confirmer et éventuellement ajuster.


## Migration

Aucun problème de compatibilité rétroactive.
C'est une option existante et la négociation MTU fait déjà partie de la spécification.

Les destinations ECIES plus anciennes prendront en charge 1730.
Tout client recevant une valeur plus élevée répondra avec 1730, et l'extrémité opposée
négociera à la baisse, comme d'habitude.


