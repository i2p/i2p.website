---
title: "ECIES Tunnels"
number: "152"
author: "chisana, zzz, orignal"
created: "2019-07-04"
lastupdated: "2025-03-05"
status: "Fermé"
thread: "http://zzz.i2p/topics/2737"
target: "0.9.48"
implementedin: "0.9.48"
toc: true
---

## Remarque

Déploiement et tests du réseau en cours. Sous réserve de légères révisions. Voir [SPEC](/docs/specs/implementation/) pour la spécification officielle.

## Aperçu

Ce document propose des modifications du chiffrement du Tunnel Build message (message de construction de tunnel) en utilisant des primitives cryptographiques introduites par [ECIES-X25519](/docs/specs/ecies/). Il s'agit d'une partie de la proposition globale [Proposal 156](/proposals/156-ecies-routers) visant à convertir les routers d'ElGamal vers des clés ECIES-X25519.

Aux fins de la transition du réseau d’ElGamal + AES256 vers ECIES + ChaCha20, des tunnels mêlant des routers ElGamal et ECIES sont nécessaires. Des spécifications pour la gestion des sauts de tunnel mixtes sont fournies. Aucune modification ne sera apportée au format, au traitement ni au chiffrement des sauts ElGamal.

Les créateurs de tunnel ElGamal devront créer des paires de clés X25519 éphémères par saut et se conformer à cette spécification lors de la création de tunnel contenant des sauts ECIES (schéma de chiffrement intégré sur courbes elliptiques).

Cette proposition précise les modifications nécessaires pour la construction de tunnels ECIES-X25519. Pour un aperçu de toutes les modifications requises pour les routers ECIES, voir la proposition 156 [Proposition 156](/proposals/156-ecies-routers).

Cette proposition conserve la même taille pour les enregistrements de construction de tunnel, comme l'exige la compatibilité. Des enregistrements de construction et des messages plus petits seront implémentés ultérieurement - voir [Proposition 157](/proposals/157-new-tbm).

### Primitives cryptographiques

Aucune nouvelle primitive cryptographique n’est introduite. Les primitives nécessaires pour mettre en œuvre cette proposition sont :

- AES-256-CBC comme dans [Cryptographie](/docs/specs/cryptography/)
- Fonctions STREAM ChaCha20/Poly1305:
  ENCRYPT(k, n, plaintext, ad) et DECRYPT(k, n, ciphertext, ad) - comme dans [NTCP2](/docs/specs/ntcp2/) [ECIES-X25519](/docs/specs/ecies/) et [RFC-7539](https://tools.ietf.org/html/rfc7539)
- Fonctions DH X25519 - comme dans [NTCP2](/docs/specs/ntcp2/) et [ECIES-X25519](/docs/specs/ecies/)
- HKDF(salt, ikm, info, n) - comme dans [NTCP2](/docs/specs/ntcp2/) et [ECIES-X25519](/docs/specs/ecies/)

Autres fonctions de Noise définies ailleurs :

- MixHash(d) - comme dans [NTCP2](/docs/specs/ntcp2/) et [ECIES-X25519](/docs/specs/ecies/)
- MixKey(d) - comme dans [NTCP2](/docs/specs/ntcp2/) et [ECIES-X25519](/docs/specs/ecies/)

### Objectifs

- Augmenter la vitesse des opérations cryptographiques
- Remplacer ElGamal + AES256/CBC par des primitives ECIES pour les BuildRequestRecords et BuildReplyRecords de tunnel.
- Aucun changement de la taille des BuildRequestRecords et BuildReplyRecords chiffrés (528 octets) pour la compatibilité
- Aucun nouveau message I2NP
- Maintenir la taille des enregistrements de construction chiffrés pour la compatibilité
- Ajouter la confidentialité persistante pour les messages de construction de tunnel.
- Ajouter le chiffrement authentifié
- Détecter les sauts réordonnant les BuildRequestRecords
- Augmenter la résolution de l’horodatage afin que la taille du filtre de Bloom puisse être réduite
- Ajouter un champ pour l’expiration du tunnel afin que des durées de vie de tunnel variables soient possibles (tunnels tout-ECIES uniquement)
- Ajouter un champ d’options extensible pour des fonctionnalités futures
- Réutiliser les primitives cryptographiques existantes
- Améliorer la sécurité des messages de construction de tunnel lorsque possible tout en maintenant la compatibilité
- Prendre en charge les tunnels avec des pairs mixtes ElGamal/ECIES
- Améliorer les défenses contre les attaques de "tagging" sur les messages de construction
- Les sauts n’ont pas besoin de connaître le type de chiffrement du prochain saut avant de traiter le message de construction,
  car ils peuvent ne pas avoir le RI du prochain saut à ce moment-là
- Maximiser la compatibilité avec le réseau actuel
- Aucun changement au chiffrement AES des requêtes/réponses de construction de tunnel pour les routers ElGamal
- Aucun changement au chiffrement AES "layer" du tunnel, pour cela voir [Proposal 153](/proposals/153-chacha20-layer-encryption)
- Continuer à prendre en charge à la fois le TBM/TBRM à 8 enregistrements et le VTBM/VTBRM de taille variable
- Ne pas exiger une mise à niveau "flag day" (migration synchronisée de tout le réseau) de l’ensemble du réseau

### Hors objectifs

- Refonte complète des messages de construction de tunnel nécessitant un « flag day » (jour de bascule planifiée).
- Réduction de la taille des messages de construction de tunnel (nécessite que tous les sauts soient en ECIES et une nouvelle proposition)
- Utilisation des options de construction de tunnel telles que définies dans [Proposition 143](/proposals/143-build-message-options), uniquement requise pour les messages de petite taille
- Tunnels bidirectionnels - pour cela, voir [Proposition 119](/proposals/119-bidirectional-tunnels)
- Messages de construction de tunnel plus petits - pour cela, voir [Proposition 157](/proposals/157-new-tbm)

## Modèle de menace

### Objectifs de conception

- Aucun saut n'est en mesure de déterminer l'initiateur du tunnel.

- Les relais intermédiaires ne doivent pas pouvoir déterminer la direction du tunnel
  ni leur position dans le tunnel.

- Aucun saut ne peut lire le contenu des autres enregistrements de requête ou de réponse, à l'exception
  du hachage de router tronqué et de la clé éphémère du prochain saut

- Aucun membre du tunnel de réponse utilisé pour la construction d'un tunnel sortant ne peut lire aucun enregistrement de réponse.

- Aucun membre du tunnel sortant utilisé pour la construction d'un tunnel entrant ne peut lire aucun enregistrement de requête,
  sauf que l'OBEP peut voir le hachage tronqué du router et la clé éphémère pour l'IBGW

### Attaques par marquage

Un objectif majeur de la conception de la construction de tunnels est de rendre plus difficile pour les routers X et Y agissant de concert de savoir qu’ils se trouvent dans un seul tunnel. Si le router X est au saut m et le router Y est au saut m+1, ils le sauront évidemment. Mais si le router X est au saut m et le router Y est au saut m+n pour n>1, cela devrait être beaucoup plus difficile.

Les attaques par marquage se produisent lorsqu’un router intermédiaire X modifie le message de construction de tunnel de telle sorte que le router Y puisse détecter l’altération lorsque le message de construction y parvient. L’objectif est que tout message altéré soit rejeté par un router entre X et Y avant d’atteindre le router Y. Pour les messages modifiés qui ne sont pas rejetés avant le router Y, le créateur du tunnel devrait détecter la corruption dans la réponse et abandonner le tunnel.

Attaques possibles :

- Modifier un enregistrement de construction
- Remplacer un enregistrement de construction
- Ajouter ou supprimer un enregistrement de construction
- Réordonner les enregistrements de construction

À vérifier : La conception actuelle empêche-t-elle toutes ces attaques ?

## Conception

### Noise Protocol Framework (cadre de protocoles cryptographiques « Noise »)

Cette proposition énonce les exigences fondées sur le Noise Protocol Framework (cadre de protocole Noise) [NOISE](https://noiseprotocol.org/noise.html) (révision 34, 2018-07-11). Dans la terminologie de Noise, Alice est l'initiateur et Bob est le répondant.

Cette proposition est basée sur le protocole Noise Noise_N_25519_ChaChaPoly_SHA256. Ce protocole Noise utilise les primitives suivantes :

- Modèle de poignée de main unidirectionnelle : N
  Alice ne transmet pas sa clé statique à Bob (N)

- Fonction DH : X25519
  DH X25519 avec une longueur de clé de 32 octets, conformément à [RFC-7748](https://tools.ietf.org/html/rfc7748).

- Fonction de chiffrement : ChaChaPoly
  AEAD_CHACHA20_POLY1305 tel que spécifié dans [RFC-7539](https://tools.ietf.org/html/rfc7539) section 2.8.
  Nonce (valeur unique) de 12 octets, dont les 4 premiers octets sont à zéro.
  Identique à celui de [NTCP2](/docs/specs/ntcp2/).

- Fonction de hachage: SHA256
  Hachage standard de 32 octets, déjà largement utilisé dans I2P.

#### Ajouts au framework (cadre logiciel)

Aucun.

### Modèles de poignée de main

Les échanges d'initialisation utilisent les schémas de handshake de [Noise](https://noiseprotocol.org/noise.html).

La correspondance suivante des lettres est utilisée :

- e = clé éphémère à usage unique
- s = clé statique
- p = charge utile du message

La requête de construction est identique au schéma Noise N. Elle est également identique au premier message (« Session Request ») du schéma XK utilisé dans [NTCP2](/docs/specs/ntcp2/).

```text
<- s
  ...
  e es p ->
```
### Chiffrement des requêtes

Les enregistrements de requête de construction sont créés par le créateur du tunnel et chiffrés de manière asymétrique à destination de chaque saut individuel. Ce chiffrement asymétrique des enregistrements de requête est actuellement ElGamal tel que défini dans [Cryptography](/docs/specs/cryptography/) et inclut une somme de contrôle SHA-256. Cette conception n'offre pas de forward secrecy (confidentialité persistante).

La nouvelle conception utilisera le modèle Noise unidirectionnel "N" avec ECIES-X25519 ephemeral-static DH, un HKDF, et ChaCha20/Poly1305 AEAD pour assurer la confidentialité persistante, l'intégrité et l'authentification. Alice est l'initiatrice de la construction du tunnel. Chaque relais dans le tunnel est un Bob.

(Propriétés de sécurité de la charge utile)

```text
N:                      Authentication   Confidentiality
    -> e, es                  0                2

    Authentication: None (0).
    This payload may have been sent by any party, including an active attacker.

    Confidentiality: 2.
    Encryption to a known recipient, forward secrecy for sender compromise
    only, vulnerable to replay.  This payload is encrypted based only on DHs
    involving the recipient's static key pair.  If the recipient's static
    private key is compromised, even at a later date, this payload can be
    decrypted.  This message can also be replayed, since there's no ephemeral
    contribution from the recipient.

    "e": Alice generates a new ephemeral key pair and stores it in the e
         variable, writes the ephemeral public key as cleartext into the
         message buffer, and hashes the public key along with the old h to
         derive a new h.

    "es": A DH is performed between the Alice's ephemeral key pair and the
          Bob's static key pair.  The result is hashed along with the old ck to
          derive a new ck and k, and n is set to zero.
```
### Chiffrement des réponses

Les Build reply records (enregistrements de réponse de construction) sont créés par le créateur du saut et chiffrés symétriquement à l’intention du créateur. Ce chiffrement symétrique des Build reply records utilise actuellement AES avec une somme de contrôle SHA-256 préfixée. et contient une somme de contrôle SHA-256. Cette conception n’offre pas de confidentialité persistante (forward secrecy).

La nouvelle conception utilisera ChaCha20/Poly1305 AEAD (chiffrement authentifié avec données associées) pour l’intégrité et l’authentification.

### Justification

La clé publique éphémère dans la requête n’a pas besoin d’être obfusquée avec AES ou Elligator2 (méthode d’obfuscation pour courbes elliptiques). Le saut précédent est le seul à pouvoir la voir, et ce saut sait que le saut suivant utilise ECIES.

Les enregistrements de réponse n'ont pas besoin d'un chiffrement asymétrique complet avec un autre DH (échange de clés Diffie-Hellman).

## Spécification

### Enregistrements de requête de construction

Les BuildRequestRecords (enregistrements de requête de construction) chiffrés sont de 528 octets, tant pour ElGamal que pour ECIES, pour des raisons de compatibilité.

#### Enregistrement de requête non chiffré (ElGamal)

À titre de référence, voici la spécification actuelle du BuildRequestRecord de tunnel pour les routers ElGamal, tirée de [I2NP](/docs/specs/i2np/). Les données non chiffrées sont préfixées par un octet non nul et par le hachage SHA-256 des données avant chiffrement, comme défini dans [Cryptography](/docs/specs/cryptography/).

Tous les champs sont en big-endian (octet de poids fort en premier).

Taille non chiffrée : 222 octets

```text
bytes     0-3: tunnel ID to receive messages as, nonzero
  bytes    4-35: local router identity hash
  bytes   36-39: next tunnel ID, nonzero
  bytes   40-71: next router identity hash
  bytes  72-103: AES-256 tunnel layer key
  bytes 104-135: AES-256 tunnel IV key
  bytes 136-167: AES-256 reply key
  bytes 168-183: AES-256 reply IV
  byte      184: flags
  bytes 185-188: request time (in hours since the epoch, rounded down)
  bytes 189-192: next message ID
  bytes 193-221: uninterpreted / random padding
```
#### Enregistrement de requête chiffré (ElGamal)

À titre de référence, voici la spécification actuelle du BuildRequestRecord de tunnel pour les routers ElGamal, tirée de [I2NP](/docs/specs/i2np/).

Taille chiffrée: 528 octets

```text
bytes    0-15: Hop's truncated identity hash
  bytes  16-528: ElGamal encrypted BuildRequestRecord
```
#### Enregistrement de requête non chiffré (ECIES, schéma de chiffrement intégré à courbe elliptique)

Ceci est la spécification proposée du BuildRequestRecord (enregistrement de requête de construction) de tunnel pour les routers ECIES-X25519. Résumé des modifications :

- Supprimer le hachage de 32 octets du router inutilisé
- Passer le temps de requête des heures aux minutes
- Ajouter un champ d'expiration pour une durée de tunnel variable à l'avenir
- Ajouter plus d'espace pour les drapeaux
- Ajouter un Mapping (mappage) pour des options de construction supplémentaires
- La clé de réponse AES-256 et l'IV (vecteur d'initialisation) ne sont pas utilisées pour l'enregistrement de réponse du saut lui-même
- L'enregistrement non chiffré est plus long car il y a moins de surcharge de chiffrement

L'enregistrement de la requête ne contient aucune clé de réponse ChaCha. Ces clés sont dérivées via une fonction de dérivation de clés (KDF). Voir ci-dessous.

Tous les champs sont en big-endian.

Taille non chiffrée : 464 octets

```text
bytes     0-3: tunnel ID to receive messages as, nonzero
  bytes     4-7: next tunnel ID, nonzero
  bytes    8-39: next router identity hash
  bytes   40-71: AES-256 tunnel layer key
  bytes  72-103: AES-256 tunnel IV key
  bytes 104-135: AES-256 reply key
  bytes 136-151: AES-256 reply IV
  byte      152: flags
  bytes 153-155: more flags, unused, set to 0 for compatibility
  bytes 156-159: request time (in minutes since the epoch, rounded down)
  bytes 160-163: request expiration (in seconds since creation)
  bytes 164-167: next message ID
  bytes   168-x: tunnel build options (Mapping)
  bytes     x-x: other data as implied by flags or options
  bytes   x-463: random padding
```
Le champ flags est identique à celui défini dans [Tunnel Creation](/docs/specs/implementation/) et contient ce qui suit::

Ordre des bits: 76543210 (le bit 7 est le MSB)  bit 7: si positionné, autoriser les messages de n'importe qui  bit 6: si positionné, autoriser l'envoi de messages à n'importe qui, et envoyer la réponse à

        specified next hop in a Tunnel Build Reply Message
bits 5 à 0 : Non définis, doivent être mis à 0 pour la compatibilité avec de futures options

Le bit 7 indique que le saut sera une passerelle entrante (IBGW). Le bit 6 indique que le saut sera un point de sortie (OBEP). Si aucun des bits n’est positionné, le saut sera un participant intermédiaire. Les deux ne peuvent pas être positionnés simultanément.

L’expiration de la requête est destinée à une future durée de tunnel variable. Pour l’instant, la seule valeur prise en charge est 600 (10 minutes).

Les options de construction de tunnel constituent une structure Mapping (structure clé-valeur) telle que définie dans [Common Structures](/docs/specs/common-structures/). Ceci est destiné à un usage futur. Aucune option n’est actuellement définie. Si la structure Mapping est vide, cela correspond à deux octets 0x00 0x00. La taille maximale du Mapping (champ de longueur inclus) est de 296 octets, et la valeur maximale du champ de longueur du Mapping est de 294.

#### Enregistrement de requête chiffré (ECIES, schéma de chiffrement intégré à courbes elliptiques)

Tous les champs sont en big-endian, à l’exception de la clé publique éphémère qui est en little-endian.

Taille chiffrée : 528 octets

```text
bytes    0-15: Hop's truncated identity hash
  bytes   16-47: Sender's ephemeral X25519 public key
  bytes  48-511: ChaCha20 encrypted BuildRequestRecord
  bytes 512-527: Poly1305 MAC
```
### Enregistrements de réponse de construction

Les BuildReplyRecords (enregistrements de réponse de construction) chiffrés ont une taille de 528 octets, tant pour ElGamal que pour ECIES, par souci de compatibilité.

#### Enregistrement de réponse non chiffré (ElGamal, cryptosystème de chiffrement asymétrique)

Les réponses ElGamal sont chiffrées avec AES.

Tous les champs sont en big-endian (ordre des octets du plus significatif au moins significatif).

Taille non chiffrée : 528 octets

```text
bytes   0-31: SHA-256 Hash of bytes 32-527
  bytes 32-526: random data
  byte     527: reply

  total length: 528
```
#### Enregistrement de réponse non chiffré (ECIES)

Il s’agit de la spécification proposée du tunnel BuildReplyRecord (enregistrement de réponse de construction) pour les routers ECIES-X25519. Résumé des changements :

- Ajouter un mappage pour les options de réponse de construction
- L’enregistrement non chiffré est plus long parce qu’il y a moins de surcharge liée au chiffrement

Les réponses ECIES (schéma de chiffrement intégré sur courbes elliptiques) sont chiffrées avec ChaCha20/Poly1305.

Tous les champs sont en big-endian.

Taille non chiffrée : 512 octets

```text
bytes    0-x: Tunnel Build Reply Options (Mapping)
  bytes    x-x: other data as implied by options
  bytes  x-510: Random padding
  byte     511: Reply byte
```
Les options de réponse de construction de tunnel constituent une structure Mapping (structure de correspondance) telle que définie dans [Common Structures](/docs/specs/common-structures/). Ceci est prévu pour un usage futur. Aucune option n’est actuellement définie. Si la structure Mapping est vide, cela correspond à deux octets 0x00 0x00. La taille maximale du Mapping (champ de longueur inclus) est de 511 octets, et la valeur maximale du champ de longueur du Mapping est de 509.

L'octet de réponse est l'une des valeurs suivantes, telles que définies dans [Tunnel Creation](/docs/specs/implementation/) pour éviter le fingerprinting :

- 0x00 (accepter)
- 30 (TUNNEL_REJECT_BANDWIDTH)

#### Enregistrement de réponse chiffré (ECIES)

Taille chiffrée: 528 octets

```text
bytes   0-511: ChaCha20 encrypted BuildReplyRecord
  bytes 512-527: Poly1305 MAC
```
Après la transition complète vers les enregistrements ECIES (schéma de chiffrement intégré à courbes elliptiques), les règles de ranged padding (bourrage par plages) sont identiques à celles des enregistrements de requête.

### Chiffrement symétrique des enregistrements

Les tunnels mixtes sont autorisés et nécessaires pour la transition d’ElGamal vers ECIES. Pendant la période de transition, un nombre croissant de routers seront dotés de clés ECIES.

Le prétraitement de la cryptographie symétrique s’effectuera de la même manière :

- "encryption":

- chiffreur exécuté en mode déchiffrement
  - enregistrements de requête déchiffrés de manière anticipée lors du prétraitement (masquant les enregistrements de requête chiffrés)

- "déchiffrement":

- algorithme de chiffrement utilisé en mode chiffrement
  - enregistrements de requête chiffrés par les sauts participants (révélant l'enregistrement de requête en clair suivant)

- ChaCha20 n'a pas de "modes", il est donc simplement exécuté trois fois :

- une fois lors du prétraitement
  - une fois par le relais
  - une fois lors du traitement final de la réponse

Lorsque des tunnels mixtes sont utilisés, les créateurs de tunnels devront baser le chiffrement symétrique de BuildRequestRecord (enregistrement de demande de construction) sur le type de chiffrement du saut actuel et du saut précédent.

Chaque saut utilisera son propre type de chiffrement pour chiffrer les BuildReplyRecords et les autres enregistrements dans la VariableTunnelBuildMessage (VTBM).

Sur le chemin de réponse, l'extrémité (expéditeur) devra déchiffrer le [chiffrement multiple](https://en.wikipedia.org/wiki/Multiple_encryption), en utilisant la clé de réponse de chaque saut.

Pour clarifier, examinons un tunnel sortant avec ECIES (schéma de chiffrement intégré à courbe elliptique) entouré par ElGamal (schéma de chiffrement asymétrique) :

- Expéditeur (OBGW) -> ElGamal (H1) -> ECIES (H2) -> ElGamal (H3)

Tous les BuildRequestRecords (enregistrements de requête de construction) sont à l’état chiffré (à l’aide d’ElGamal ou d’ECIES).

Le chiffrement AES256/CBC, lorsqu'il est utilisé, est toujours appliqué à chaque enregistrement, sans chaînage entre plusieurs enregistrements.

De même, ChaCha20 sera utilisé pour chiffrer chaque enregistrement, et non pas en flux sur l'ensemble du VTBM.

Les enregistrements de requêtes sont prétraités par l’émetteur (OBGW) :

- L'enregistrement de H3 est "chiffré" à l'aide de :

- La clé de réponse de H2 (ChaCha20)
  - La clé de réponse de H1 (AES256/CBC)

- L'enregistrement de H2 est "chiffré" à l'aide de:

- La clé de réponse de H1 (AES256/CBC)

- L'enregistrement de H1 est envoyé sans chiffrement symétrique

Seul H2 vérifie l'indicateur de chiffrement de la réponse, et constate que celui-ci est suivi de AES256/CBC.

Après avoir été traités par chaque saut, les enregistrements sont dans un état "déchiffré":

- L'enregistrement de H3 est "déchiffré" à l'aide de :

- clé de réponse de H3 (AES256/CBC)

- L'enregistrement de H2 est « déchiffré » à l'aide de :

- Clé de réponse de H3 (AES256/CBC)
  - Clé de réponse de H2 (ChaCha20-Poly1305)

- L'enregistrement de H1 est « déchiffré » à l'aide de :

- Clé de réponse de H3 (AES256/CBC)
  - Clé de réponse de H2 (ChaCha20)
  - Clé de réponse de H1 (AES256/CBC)

Le créateur de tunnel, également appelé Inbound Endpoint (IBEP, point de terminaison entrant), post-traite la réponse :

- L'enregistrement de H3 est "chiffré" à l'aide de :

- La clé de réponse de H3 (AES256/CBC)

- L'enregistrement de H2 est "chiffré" à l'aide de :

- clé de réponse de H3 (AES256/CBC)
  - clé de réponse de H2 (ChaCha20-Poly1305)

- L'enregistrement de H1 est "chiffré" à l'aide de :

- Clé de réponse de H3 (AES256/CBC)
  - Clé de réponse de H2 (ChaCha20)
  - Clé de réponse de H1 (AES256/CBC)

### Clés des enregistrements de requête (ECIES)

Ces clés sont explicitement incluses dans les BuildRequestRecords (enregistrements de requête de construction) ElGamal. Pour les BuildRequestRecords ECIES, les clés de tunnel et les clés de réponse AES sont incluses, mais les clés de réponse ChaCha sont dérivées de l’échange DH (Diffie-Hellman). Voir [Proposition 156](/proposals/156-ecies-routers) pour des détails sur les clés ECIES statiques du router.

Vous trouverez ci-dessous une description de la manière de dériver les clés précédemment transmises dans les enregistrements de requête.

#### Fonction de dérivation de clé (KDF) pour ck et h initiaux

Il s’agit de [NOISE](https://noiseprotocol.org/noise.html) standard pour le modèle "N" avec un nom de protocole standard.

```text
This is the "e" message pattern:

  // Define protocol_name.
  Set protocol_name = "Noise_N_25519_ChaChaPoly_SHA256"
  (31 bytes, US-ASCII encoded, no NULL termination).

  // Define Hash h = 32 bytes
  // Pad to 32 bytes. Do NOT hash it, because it is not more than 32 bytes.
  h = protocol_name || 0

  Define ck = 32 byte chaining key. Copy the h data to ck.
  Set chainKey = h

  // MixHash(null prologue)
  h = SHA256(h);

  // up until here, can all be precalculated by all routers.
```
#### KDF (fonction de dérivation de clé) pour l’enregistrement de requête

Les créateurs de tunnel ElGamal génèrent une paire de clés X25519 éphémère pour chaque saut ECIES dans le tunnel, et utilisent le schéma ci-dessus pour chiffrer leur BuildRequestRecord (enregistrement de requête de construction). Les créateurs de tunnel ElGamal utiliseront le schéma antérieur à cette spécification pour chiffrer à destination des sauts ElGamal.

Les créateurs de tunnel ECIES devront chiffrer avec la clé publique de chaque saut ElGamal en utilisant le schéma défini dans [Tunnel Creation](/docs/specs/implementation/). Les créateurs de tunnel ECIES utiliseront le schéma ci-dessus pour chiffrer à destination des sauts ECIES.

Cela signifie que les sauts de tunnel ne voient que des enregistrements chiffrés correspondant à leur propre type de chiffrement.

Les créateurs de tunnel ElGamal et ECIES généreront des paires de clés X25519 éphémères uniques par saut afin de chiffrer à destination des sauts ECIES.

**IMPORTANT**: Les clés éphémères doivent être uniques pour chaque saut ECIES et pour chaque enregistrement de construction. Le fait de ne pas utiliser des clés uniques ouvre un vecteur d’attaque permettant à des nœuds relais en collusion de confirmer qu’ils se trouvent dans le même tunnel.

```text
// Each hop's X25519 static keypair (hesk, hepk) from the Router Identity
  hesk = GENERATE_PRIVATE()
  hepk = DERIVE_PUBLIC(hesk)

  // MixHash(hepk)
  // || below means append
  h = SHA256(h || hepk);

  // up until here, can all be precalculated by each router
  // for all incoming build requests

  // Sender generates an X25519 ephemeral keypair per ECIES hop in the VTBM (sesk, sepk)
  sesk = GENERATE_PRIVATE()
  sepk = DERIVE_PUBLIC(sesk)

  // MixHash(sepk)
  h = SHA256(h || sepk);

  End of "e" message pattern.

  This is the "es" message pattern:

  // Noise es
  // Sender performs an X25519 DH with Hop's static public key.
  // Each Hop, finds the record w/ their truncated identity hash,
  // and extracts the Sender's ephemeral key preceding the encrypted record.
  sharedSecret = DH(sesk, hepk) = DH(hesk, sepk)

  // MixKey(DH())
  //[chainKey, k] = MixKey(sharedSecret)
  // ChaChaPoly parameters to encrypt/decrypt
  keydata = HKDF(chainKey, sharedSecret, "", 64)
  // Save for Reply Record KDF
  chainKey = keydata[0:31]

  // AEAD parameters
  k = keydata[32:63]
  n = 0
  plaintext = 464 byte build request record
  ad = h
  ciphertext = ENCRYPT(k, n, plaintext, ad)

  End of "es" message pattern.

  // MixHash(ciphertext)
  // Save for Reply Record KDF
  h = SHA256(h || ciphertext)
```
``replyKey``, ``layerKey`` et ``layerIV`` doivent toujours être inclus dans les enregistrements ElGamal et peuvent être générés aléatoirement.

### Chiffrement de l'enregistrement de requête (ElGamal)

Tel que défini dans [Création de tunnels](/docs/specs/implementation/). Aucune modification du chiffrement pour les sauts ElGamal.

### Chiffrement de l’enregistrement de réponse (ECIES)

L’enregistrement de réponse est chiffré avec ChaCha20/Poly1305.

```text
// AEAD parameters
  k = chainkey from build request
  n = 0
  plaintext = 512 byte build reply record
  ad = h from build request

  ciphertext = ENCRYPT(k, n, plaintext, ad)
```
### Chiffrement de l’enregistrement de réponse (ElGamal)

Comme défini dans [Création de tunnel](/docs/specs/implementation/). Il n’y a aucun changement concernant le chiffrement des sauts ElGamal.

### Analyse de sécurité

ElGamal ne garantit pas la confidentialité persistante pour les messages de construction de tunnel.

AES256/CBC est dans une position légèrement meilleure, n’étant vulnérable qu’à un affaiblissement théorique dû à une attaque `biclique` par texte en clair connu.

La seule attaque pratique connue contre AES256/CBC est une attaque par oracle de bourrage, lorsque le vecteur d'initialisation (IV) est connu de l'attaquant.

Un attaquant devrait casser le chiffrement ElGamal du prochain saut pour obtenir les informations de clé AES256/CBC (clé de réponse et IV (vecteur d'initialisation)).

ElGamal est nettement plus gourmand en ressources processeur qu’ECIES, ce qui peut entraîner un épuisement des ressources.

ECIES, utilisé avec de nouvelles clés éphémères pour chaque BuildRequestRecord ou VariableTunnelBuildMessage, fournit la confidentialité persistante.

ChaCha20Poly1305 fournit un chiffrement AEAD (chiffrement authentifié avec données associées), permettant au destinataire de vérifier l'intégrité du message avant de tenter le déchiffrement.

## Justification

Cette conception maximise la réutilisation des primitives cryptographiques, des protocoles et du code existants. Cette conception minimise le risque.

## Notes d’implémentation

* Les anciens routers ne vérifient pas le type de chiffrement du saut et enverront des enregistrements chiffrés en ElGamal
  enregistrements. Certains routers récents sont bogués et enverront divers types d’enregistrements malformés.
  Les implémenteurs devraient détecter et rejeter ces enregistrements avant l’opération DH (Diffie-Hellman)
  si possible, afin de réduire l’utilisation du processeur.

## Problèmes

## Migration

Voir [Proposition 156](/proposals/156-ecies-routers).

## Références

* [Structures communes](/docs/specs/common-structures/)
* [Cryptographie](/docs/specs/cryptography/)
* [ECIES-X25519](/docs/specs/ecies/)
* [I2NP](/docs/specs/i2np/)
* [NOISE](https://noiseprotocol.org/noise.html)
* [NTCP2](/docs/specs/ntcp2/)
* [Prop119](/proposals/119-bidirectional-tunnels/)
* [Prop143](/proposals/143-build-message-options/)
* [Prop153](/proposals/153-chacha20-layer-encryption/)
* [Prop156](/proposals/156-ecies-routers/)
* [Prop157](/proposals/157-new-tbm/)
* [SPEC](/docs/specs/implementation/#tunnel-creation-ecies)
* [Création de tunnel](/docs/specs/implementation/)
* [Chiffrement multiple](https://en.wikipedia.org/wiki/Multiple_encryption)
* [RFC-7539](https://tools.ietf.org/html/rfc7539)
* [RFC-7748](https://tools.ietf.org/html/rfc7748)
