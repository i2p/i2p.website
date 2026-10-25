---
title: "Chiffrement ElGamal/AES + SessionTag"
description: "Chiffrement de bout en bout hérité combinant ElGamal, AES, SHA-256, et des étiquettes de session à usage unique"
slug: "elgamal-aes"
aliases:
  - "/fr/how_elgamalaes"
  - "/fr/how_elgamalaes/"
lastUpdated: "2020-04"
accurateFor: "0.9.46"
---

## Aperçu

ElGamal/AES+SessionTags est utilisé pour le chiffrement de bout en bout.

En tant que système basé sur des messages non fiables et non ordonnés, I2P utilise une combinaison simple d'algorithmes de chiffrement asymétriques et symétriques pour assurer la confidentialité et l'intégrité des données des garlic messages. Dans son ensemble, cette combinaison est appelée ElGamal/AES+SessionTags, mais c'est une façon excessivement verbeuse de décrire l'utilisation d'ElGamal 2048 bits, AES256, SHA256, et de nonces de 32 octets.

La première fois qu'un router veut chiffrer un message garlic vers un autre router, il chiffre le matériel de clé pour une clé de session AES256 avec ElGamal et ajoute la charge utile chiffrée AES256/CBC après ce bloc ElGamal chiffré. En plus de la charge utile chiffrée, la section chiffrée AES contient la longueur de la charge utile, le hachage SHA256 de la charge utile non chiffrée, ainsi qu'un certain nombre de "session tags" - des nonces aléatoires de 32 octets. La prochaine fois que l'expéditeur veut chiffrer un message garlic vers un autre router, plutôt que de chiffrer avec ElGamal une nouvelle clé de session, il sélectionne simplement l'un des session tags précédemment livrés et chiffre la charge utile avec AES comme avant, en utilisant la clé de session utilisée avec ce session tag, précédée du session tag lui-même. Quand un router reçoit un message chiffré garlic, il vérifie les 32 premiers octets pour voir s'ils correspondent à un session tag disponible - si c'est le cas, il déchiffre simplement le message avec AES, mais sinon, il déchiffre le premier bloc avec ElGamal.

Chaque tag de session ne peut être utilisé qu'une seule fois afin d'empêcher les adversaires internes de corréler inutilement différents messages comme étant échangés entre les mêmes routers. L'expéditeur d'un message chiffré ElGamal/AES+SessionTag choisit quand et combien de tags livrer, approvisionnant le destinataire avec suffisamment de tags pour couvrir une volée de messages. Les messages garlic peuvent détecter la livraison réussie de tags en regroupant un petit message supplémentaire comme un clove (un "message de statut de livraison") - lorsque le message garlic arrive au destinataire prévu et est déchiffré avec succès, ce petit message de statut de livraison est l'un des cloves exposés et contient des instructions pour que le destinataire renvoie le clove à l'expéditeur original (à travers un tunnel entrant, bien sûr). Lorsque l'expéditeur original reçoit ce message de statut de livraison, il sait que les tags de session regroupés dans le message garlic ont été livrés avec succès.

Les session tags elles-mêmes ont une durée de vie courte, après laquelle elles sont supprimées si elles ne sont pas utilisées. De plus, la quantité stockée pour chaque clé est limitée, tout comme le nombre de clés elles-mêmes - si trop arrivent, soit les nouveaux messages soit les anciens peuvent être supprimés. L'expéditeur suit si les messages utilisant des session tags passent, et s'il n'y a pas suffisamment de communication, il peut supprimer ceux précédemment supposés être correctement livrés, revenant au chiffrement ElGamal complet et coûteux. Une session continuera d'exister jusqu'à ce que tous ses tags soient épuisés ou expirent.

Les sessions sont unidirectionnelles. Les tags sont transmis d'Alice à Bob, et Alice utilise ensuite les tags, un par un, dans les messages suivants à Bob.

Les sessions peuvent être établies entre Destinations, entre routers, ou entre un router et une Destination. Chaque router et Destination maintient son propre Gestionnaire de Clés de Session pour suivre les Clés de Session et les Étiquettes de Session. Des Gestionnaires de Clés de Session séparés empêchent la corrélation de multiples Destinations entre elles ou avec un router par des adversaires.

## Réception de message

Chaque message reçu a une des deux conditions possibles :

1. Il fait partie d'une session existante et contient un Session Tag et un bloc chiffré AES
2. Il est destiné à une nouvelle session et contient à la fois des blocs chiffrés ElGamal et AES

Lorsqu'un router reçoit un message, il supposera d'abord qu'il provient d'une session existante et tentera de rechercher le Session Tag et de déchiffrer les données suivantes en utilisant AES. Si cela échoue, il supposera qu'il s'agit d'une nouvelle session et tentera de le déchiffrer en utilisant ElGamal.

## Spécification du message de nouvelle session {#new}

Un message ElGamal de nouvelle session contient deux parties, un bloc ElGamal chiffré et un bloc AES chiffré.

Le message chiffré contient :

```
   +----+----+----+----+----+----+----+----+
   |                                       |
   +                                       +
   |       ElGamal Encrypted Block         |
   ~                                       ~
   |                                       |
   +         +----+----+----+----+----+----+
   |         |                             |
   +----+----+                             +
   |                                       |
   +                                       +
   |         AES Encrypted Block           |
   ~                                       ~
   |                                       |
   +         +----+----+----+----+----+----+
   |         +
   +----+----+
```
### Bloc ElGamal

Le bloc ElGamal chiffré fait toujours 514 octets de long.

Les données ElGamal non chiffrées font 222 octets de long et contiennent :

```
   +----+----+----+----+----+----+----+----+
   |                                       |
   +                                       +
   |           Session Key                 |
   +                                       +
   |                                       |
   +                                       +
   |                                       |
   +----+----+----+----+----+----+----+----+
   |                                       |
   +                                       +
   |              Pre-IV                   |
   +                                       +
   |                                       |
   +                                       +
   |                                       |
   +----+----+----+----+----+----+----+----+
   +                                       +
   |                                       |
   +                                       +
   |       158 bytes random padding        |
   ~                                       ~
   |                                       |
   +                             +----+----+
   |                             |
   +----+----+----+----+----+----+
```
La [Clé de Session](/docs/specs/common-structures#type_SessionKey) de 32 octets est l'identifiant de la session. Le Pré-IV de 32 octets sera utilisé pour générer l'IV pour le bloc AES qui suit ; l'IV correspond aux 16 premiers octets du hachage SHA-256 du Pré-IV.

La charge utile de 222 octets est chiffrée [en utilisant ElGamal](/docs/specs/cryptography#elgamal) et le bloc chiffré fait 514 octets de long.

### Bloc AES {#aes}

Les données non chiffrées dans le bloc AES contiennent ce qui suit :

```
   +----+----+----+----+----+----+----+----+
   |tag count|                             |
   +----+----+                             +
   |                                       |
   +                                       +
   |          Session Tags                 |
   ~                                       ~
   |                                       |
   +                                       +
   |                                       |
   +         +----+----+----+----+----+----+
   |         |    payload size   |         |
   +----+----+----+----+----+----+         +
   |                                       |
   +                                       +
   |          Payload Hash                 |
   +                                       +
   |                                       |
   +                             +----+----+
   |                             |flag|    |
   +----+----+----+----+----+----+----+    +
   |                                       |
   +                                       +
   |          New Session Key (opt.)       |
   +                                       +
   |                                       |
   +                                  +----+
   |                                  |    |
   +----+----+----+----+----+----+----+    +
   |                                       |
   +                                       +
   |           Payload                     |
   ~                                       ~
   |                                       |
   +                        +----//---+----+
   |                        |              |
   +----+----+----//---+----+              +
   |          Padding to 16 bytes          |
   +----+----+----+----+----+----+----+----+
```
#### Définition

```
tag count:
    2-byte Integer, 0-200

Session Tags:
    That many 32-byte SessionTags

payload size:
    4-byte Integer

Payload Hash:
    The 32-byte SHA256 Hash of the payload

flag:
    A one-byte value. Normally == 0. If == 0x01, a Session Key follows

New Session Key:
    A 32-byte SessionKey,
    to replace the old key, and is only present if preceding flag is 0x01

Payload:
    the data

Padding:
    Random data to a multiple of 16 bytes for the total length.
    May contain more than the minimum required padding.
```
Longueur minimale : 48 octets

Les données sont ensuite [chiffrées AES](/docs/specs/cryptography), en utilisant la clé de session et l'IV (calculé à partir du pré-IV) de la section ElGamal. La longueur du bloc AES chiffré est variable mais est toujours un multiple de 16 octets.

#### Notes

- La longueur maximale réelle de la charge utile et la longueur maximale de bloc sont inférieures à 64 Ko ; voir l'[Aperçu I2NP](/docs/protocol/i2np).
- La Nouvelle Clé de Session n'est actuellement pas utilisée et n'est jamais présente.

## Spécification des Messages de Session Existante {#existing}

Les session tags livrés avec succès sont mémorisés pendant une brève période (actuellement 15 minutes) jusqu'à ce qu'ils soient utilisés ou supprimés. Un tag est utilisé en l'emballant dans un Existing Session Message qui ne contient qu'un bloc chiffré AES, et n'est pas précédé d'un bloc ElGamal.

Le message de session existant est le suivant :

```
   +----+----+----+----+----+----+----+----+
   |                                       |
   +                                       +
   |            Session Tag                |
   +                                       +
   |                                       |
   +                                       +
   |                                       |
   +----+----+----+----+----+----+----+----+
   |                                       |
   +                                       +
   |         AES Encrypted Block           |
   ~                                       ~
   |                                       |
   +                                       +
   |                                       |
   +----+----+----+----+----+----+----+----+
```
#### Définition

```
Session Tag:
    A 32-byte SessionTag
    previously delivered in an AES block

AES Encrypted Block:
    As specified above.
```
Le tag de session sert également de pré-IV. L'IV correspond aux 16 premiers octets du hachage SHA-256 du sessionTag.

Pour décoder un message d'une session existante, un router recherche le Session Tag pour trouver une Session Key associée. Si le Session Tag est trouvé, le bloc AES est déchiffré en utilisant la Session Key associée. Si le tag n'est pas trouvé, le message est supposé être un [New Session Message](#new).

## Options de configuration des balises de session {#config}

À partir de la version 0.9.2, le client peut configurer le nombre par défaut de Session Tags à envoyer et le seuil bas de tags pour la session actuelle. Pour les connexions streaming courtes ou les datagrammes, ces options peuvent être utilisées pour réduire considérablement la bande passante. Voir la [spécification des options I2CP](/docs/protocol/i2cp#options) pour plus de détails. Les paramètres de session peuvent également être remplacés message par message. Voir la [spécification I2CP Send Message Expires](/docs/specs/i2cp#msg_SendMessageExpires) pour plus de détails.

## Travaux Futurs {#future}

**Remarque :** ElGamal/AES+SessionTags est en cours de remplacement par ECIES-X25519-AEAD-Ratchet (Proposition 144). Les problèmes et idées référencés ci-dessous ont été intégrés dans la conception du nouveau protocole. Les éléments suivants ne seront pas traités dans ElGamal/AES+SessionTags.

Il existe de nombreux domaines possibles pour ajuster les algorithmes du Session Key Manager ; certains peuvent interagir avec le comportement de la bibliothèque de streaming, ou avoir un impact significatif sur les performances globales.

- Le nombre de balises livrées pourrait dépendre de la taille du message, en gardant à l'esprit le remplissage éventuel à 1 Ko au niveau de la couche de message du tunnel.

- Les clients pourraient envoyer une estimation de la durée de vie de la session au router, comme conseil sur le nombre de tags requis.

- La livraison d'un nombre insuffisant de tags pousse le router à revenir à un chiffrement ElGamal coûteux.

- Le router peut supposer la livraison des Session Tags, ou attendre un accusé de réception avant de les utiliser ;
  il existe des compromis pour chaque stratégie.

- Pour les messages très brefs, presque la totalité des 222 octets des champs pre-IV et de remplissage dans le bloc ElGamal pourrait être utilisée pour l'ensemble du message, au lieu d'établir une session.

- Évaluer la stratégie de remplissage ; actuellement nous remplissons jusqu'à un minimum de 128 octets.
  Il serait mieux d'ajouter quelques balises aux petits messages plutôt que de remplir.

- Les choses pourraient peut-être être plus efficaces si le système de Session Tag était bidirectionnel,
  de sorte que les tags livrés dans le chemin 'aller' puissent être utilisés dans le chemin 'retour',
  évitant ainsi ElGamal dans la réponse initiale.
  Le router joue actuellement quelques astuces comme celle-ci lors de l'envoi
  de messages de test de tunnel vers lui-même.

- Passage des Session Tags à
  [un PRNG synchronisé](/docs/overview/performance#future#prng).

- Plusieurs de ces idées peuvent nécessiter un nouveau type de message I2NP, ou
  définir un flag dans les
  [Instructions de Livraison](/docs/specs/tunnel-message#struct_TunnelMessageDeliveryInstructions),
  ou définir un nombre magique dans les premiers octets du champ Session Key
  et accepter un petit risque que la Session Key aléatoire corresponde au nombre magique.
