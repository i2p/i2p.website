---
title: "NTCP (TCP basé sur NIO)"
description: "Transport TCP basé sur Java NIO hérité pour I2P, remplacé par NTCP2"
slug: "ntcp"
aliases:
  - "/fr/docs/transport/ntcp"
  - "/fr/docs/transport/ntcp/"
  - "/fr/docs/ntcp"
  - "/fr/docs/ntcp/"
  - "/fr/ntcp"
  - "/fr/ntcp/"
lastUpdated: "2021-10"
accurateFor: "0.9.52"
---

OBSOLÈTE, PLUS PRIS EN CHARGE. Désactivé par défaut depuis la version 0.9.40 de mai 2019. Support supprimé depuis la version 0.9.50 de mai 2021. Remplacé par [NTCP2](/docs/specs/ntcp2). NTCP est un transport basé sur Java NIO introduit dans la version 0.6.1.22 d'I2P. Java NIO (new I/O) ne souffre pas des problèmes de 1 thread par connexion de l'ancien transport TCP. NTCP-over-IPv6 est pris en charge depuis la version 0.9.8.

Par défaut, NTCP utilise l'IP/Port détectés automatiquement par SSU. Lorsqu'activé sur config.jsp, SSU notifiera/redémarrera NTCP quand l'adresse externe change ou quand le statut du pare-feu change. Vous pouvez maintenant activer TCP entrant sans IP statique ou service dyndns.

Le code NTCP dans I2P est relativement léger (1/4 de la taille du code SSU) car il utilise le transport TCP Java sous-jacent pour une livraison fiable.

## Spécification d'adresse router {#ra}

Les propriétés suivantes sont stockées dans la base de données réseau.

- **Nom du transport :** NTCP
- **host :** IP (IPv4 ou IPv6).
  Les adresses IPv6 raccourcies (avec "::") sont autorisées.
  Les noms d'hôte étaient précédemment autorisés, mais sont dépréciés depuis la version 0.9.32. Voir la proposition 141.
- **port :** 1024 - 65535

## Spécification du protocole NTCP

### Format de Message Standard

Après établissement, le transport NTCP envoie des messages I2NP individuels, avec une somme de contrôle simple. Le message non chiffré est encodé comme suit :

```
+-------+-------+-------+-------+-------+-------+-------+-------+
| sizeof(data)  |                                               |
+-------+-------+                                               +
|                            data                               |
~                                                               ~
|                                                               |
+                                       +-------+-------+-------+
|                                       |        padding
+-------+-------+-------+-------+-------+-------+-------+-------+
                                | Adler checksum of sz+data+pad |
+-------+-------+-------+-------+-------+-------+-------+-------+
```
Les données sont ensuite chiffrées avec AES/256/CBC. La clé de session pour le chiffrement est négociée lors de l'établissement (en utilisant Diffie-Hellman 2048 bits). L'établissement entre deux routers est implémenté dans la classe EstablishState et détaillé ci-dessous. L'IV pour le chiffrement AES/256/CBC correspond aux 16 derniers octets du message chiffré précédent.

0 à 15 octets de remplissage sont nécessaires pour amener la longueur totale du message (y compris les six octets de taille et de somme de contrôle) à un multiple de 16. La taille maximale du message est actuellement de 16 Ko. Par conséquent, la taille maximale des données est actuellement de 16 Ko - 6, soit 16378 octets. La taille minimale des données est de 1.

### Format des Messages de Synchronisation Temporelle

Un cas particulier est un message de métadonnées où sizeof(data) est 0. Dans ce cas, le message non chiffré est encodé comme suit :

```
+-------+-------+-------+-------+-------+-------+-------+-------+
|       0       |      timestamp in seconds     | uninterpreted
+-------+-------+-------+-------+-------+-------+-------+-------+
        uninterpreted           | Adler checksum of bytes 0-11  |
+-------+-------+-------+-------+-------+-------+-------+-------+
```
Longueur totale : 16 octets. Le message de synchronisation temporelle est envoyé à intervalles d'environ 15 minutes. Le message est chiffré de la même manière que les messages standards.

### Sommes de contrôle

Les messages standard et de synchronisation temporelle utilisent la somme de contrôle Adler-32 telle que définie dans la [Spécification ZLIB](http://tools.ietf.org/html/rfc1950).

### Délai d'inactivité

Le délai d'expiration d'inactivité et la fermeture de connexion sont à la discrétion de chaque point de terminaison et peuvent varier. L'implémentation actuelle diminue le délai d'expiration lorsque le nombre de connexions approche du maximum configuré, et augmente le délai d'expiration lorsque le nombre de connexions est faible. Le délai d'expiration minimum recommandé est de deux minutes ou plus, et le délai d'expiration maximum recommandé est de dix minutes ou plus.

### Échange de RouterInfo

Après l'établissement, et toutes les 30-60 minutes par la suite, les deux routers devraient généralement échanger des RouterInfos en utilisant un DatabaseStoreMessage. Cependant, Alice devrait vérifier si le premier message en file d'attente est un DatabaseStoreMessage afin de ne pas envoyer un message en double ; c'est souvent le cas lors de la connexion à un router floodfill.

### Séquence d'établissement

Dans l'état d'établissement, il y a une séquence de messages à 4 phases pour échanger les clés DH et les signatures. Dans les deux premiers messages, il y a un échange Diffie Hellman de 2048 bits. Ensuite, les signatures des données critiques sont échangées pour confirmer la connexion.

```
Alice                   contacts                      Bob
=========================================================
 X+(H(X) xor Bob.identHash)----------------------------->
 <----------------------------------------Y+E(H(X+Y)+tsB+padding, sk, Y[239:255])
 E(sz+Alice.identity+tsA+padding+S(X+Y+Bob.identHash+tsA+tsB), sk, hX_xor_Bob.identHash[16:31])--->
 <----------------------E(S(X+Y+Alice.identHash+tsA+tsB)+padding, sk, prev)
```
```
  Legend:
    X, Y: 256 byte DH public keys
    H(): 32 byte SHA256 Hash
    E(data, session key, IV): AES256 Encrypt
    S(): Signature
    tsA, tsB: timestamps (4 bytes, seconds since epoch)
    sk: 32 byte Session key
    sz: 2 byte size of Alice identity to follow
```
#### Échange de clés DH {#DH}

L'échange de clés DH initial de 2048 bits utilise le même nombre premier partagé (p) et générateur (g) que celui utilisé pour le [chiffrement ElGamal](/docs/specs/cryptography#elgamal) d'I2P.

L'échange de clés DH consiste en un certain nombre d'étapes, affichées ci-dessous. La correspondance entre ces étapes et les messages envoyés entre les routers I2P est marquée en gras.

1. Alice génère un entier secret x. Elle calcule ensuite `X = g^x mod p`.
2. Alice envoie X à Bob **(Message 1)**.
3. Bob génère un entier secret y. Il calcule ensuite `Y = g^y mod p`.
4. Bob envoie Y à Alice. **(Message 2)**
5. Alice peut maintenant calculer `sessionKey = Y^x mod p`.
6. Bob peut maintenant calculer `sessionKey = X^y mod p`.
7. Alice et Bob ont maintenant tous les deux une clé partagée `sessionKey = g^(x*y) mod p`.

La sessionKey est ensuite utilisée pour échanger les identités dans le **Message 3** et le **Message 4**. La longueur de l'exposant (x et y) pour l'échange DH est documentée sur la [page de cryptographie](/docs/specs/cryptography#exponent).

#### Détails de la clé de session

La clé de session de 32 octets est créée comme suit :

1. Prendre la clé DH échangée, représentée comme un tableau d'octets BigInteger de longueur minimale positive (complément à deux big-endian)
2. Si le bit le plus significatif est 1 (c'est-à-dire array[0] & 0x80 != 0), ajouter un octet 0x00 au début, comme dans la représentation Java BigInteger.toByteArray()
3. Si ce tableau d'octets fait 32 octets ou plus, utiliser les 32 premiers octets (les plus significatifs)
4. Si ce tableau d'octets fait moins de 32 octets, ajouter des octets 0x00 à la fin pour étendre à 32 octets. *(extrêmement improbable)*

#### Message 1 (Demande de session)

Il s'agit de la requête DH. Alice possède déjà l'[Identity du Router](/docs/specs/common-structures#struct_RouterIdentity) de Bob, son adresse IP et son port, tels que contenus dans ses [Informations de Router](/docs/specs/common-structures#struct_RouterInfo), qui ont été publiées dans la [base de données réseau](/docs/overview/network-database). Alice envoie à Bob :

```
 X+(H(X) xor Bob.identHash)----------------------------->

    Size: 288 bytes
```
Sommaire :

```
 +----+----+----+----+----+----+----+----+
 |         X, as calculated from DH      |
 +                                       +
 |                                       |
 ~               .   .   .               ~
 |                                       |
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |              HXxorHI                  |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +----+----+----+----+----+----+----+----+

  X :: 256 byte X from Diffie Hellman

  HXxorHI :: SHA256 Hash(X) xored with SHA256 Hash(Bob's RouterIdentity)
             (32 bytes)
```
**Remarques :**

- Bob vérifie HXxorHI en utilisant son propre hash de router. Si cela ne se vérifie pas, Alice a contacté le mauvais router, et Bob ferme la connexion.

#### Message 2 (Session créée)

Ceci est la réponse DH. Bob envoie à Alice :

```
 <----------------------------------------Y+E(H(X+Y)+tsB+padding, sk, Y[239:255])

    Size: 304 bytes
```
Contenus non chiffrés :

```
 +----+----+----+----+----+----+----+----+
 |         Y as calculated from DH       |
 +                                       +
 |                                       |
 ~               .   .   .               ~
 |                                       |
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |              HXY                      |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +----+----+----+----+----+----+----+----+
 |        tsB        |     padding       |
 +----+----+----+----+                   +
 |                                       |
 +----+----+----+----+----+----+----+----+

  Y :: 256 byte Y from Diffie Hellman

  HXY :: SHA256 Hash(X concatenated with Y)
         (32 bytes)

  tsB :: 4 byte timestamp (seconds since the epoch)

  padding :: 12 bytes random data
```
Contenus Chiffrés :

```
 +----+----+----+----+----+----+----+----+
 |         Y as calculated from DH       |
 +                                       +
 |                                       |
 ~               .   .   .               ~
 |                                       |
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |             encrypted data            |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +----+----+----+----+----+----+----+----+

  Y: 256 byte Y from Diffie Hellman

  encrypted data: 48 bytes AES encrypted using the DH session key and
                  the last 16 bytes of Y as the IV
```
**Remarques :**

- Alice peut abandonner la connexion si l'écart d'horloge avec Bob est trop élevé tel que calculé en utilisant tsB.

#### Message 3 (Confirmation de Session A)

Ceci contient l'identité du router d'Alice, et une signature des données critiques. Alice envoie à Bob :

```
 E(sz+Alice.identity+tsA+padding+S(X+Y+Bob.identHash+tsA+tsB), sk, hX_xor_Bob.identHash[16:31])--->

    Size: 448 bytes (typ. for 387 byte identity and DSA signature), see notes below
```
Contenus non chiffrés :

```
 +----+----+----+----+----+----+----+----+
 |   sz    | Alice's Router Identity     |
 +----+----+                             +
 |                                       |
 ~               .   .   .               ~
 |                                       |
 +                        +----+----+----+
 |                        |     tsA
 +----+----+----+----+----+----+----+----+
      |             padding              |
 +----+                                  +
 |                                       |
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |              signature                |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +----+----+----+----+----+----+----+----+

  sz :: 2 byte size of Alice's router identity to follow (387+)

  ident :: Alice's 387+ byte RouterIdentity

  tsA :: 4 byte timestamp (seconds since the epoch)

  padding :: 0-15 bytes random data

  signature :: the Signature of the following concatenated data:
               X, Y, Bob's RouterIdentity, tsA, tsB.
               Alice signs it with the SigningPrivateKey associated with
               the SigningPublicKey in her RouterIdentity
```
Contenu chiffré :

```
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |             encrypted data            |
 ~               .   .   .               ~
 |                                       |
 +----+----+----+----+----+----+----+----+

  encrypted data: 448 bytes AES encrypted using the DH session key and
                  the last 16 bytes of HXxorHI (i.e., the last 16 bytes
                  of message #1) as the IV
                  448 is the typical length, but it could be longer, see below.
```
**Remarques :**

- Bob vérifie la signature, et en cas d'échec, ferme la connexion.
- Bob peut fermer la connexion si le décalage d'horloge avec Alice est trop élevé tel que calculé en utilisant tsA.
- Alice utilisera les 16 derniers octets du contenu chiffré de ce message comme IV pour le message suivant.
- Jusqu'à la version 0.9.15, la router identity faisait toujours 387 octets, la signature était toujours une signature DSA de 40 octets, et le padding était toujours de 15 octets. À partir de la version 0.9.16, la router identity peut faire plus de 387 octets, et le type et la longueur de la signature sont implicites selon le type de la [Signing Public Key](/docs/specs/common-structures#type_SigningPublicKey) dans la [Router Identity](/docs/specs/common-structures#struct_RouterIdentity) d'Alice. Le padding est appliqué selon les besoins pour obtenir un multiple de 16 octets pour l'ensemble du contenu non chiffré.
- La longueur totale du message ne peut pas être déterminée sans le déchiffrer partiellement pour lire la Router Identity. Comme la longueur minimale de la Router Identity est de 387 octets, et la longueur minimale de Signature est de 40 (pour DSA), la taille minimale totale du message est de 2 + 387 + 4 + (longueur de signature) + (padding à 16 octets), soit 2 + 387 + 4 + 40 + 15 = 448 pour DSA. Le récepteur pourrait lire cette quantité minimale avant de déchiffrer pour déterminer la longueur réelle de la Router Identity. Pour les petits Certificates dans la Router Identity, ce sera probablement l'ensemble du message, et il n'y aura pas d'autres octets dans le message nécessitant une opération de déchiffrement supplémentaire.

#### Message 4 (Confirmation de session B)

Ceci est une signature des données critiques. Bob envoie à Alice :

```
 <----------------------E(S(X+Y+Alice.identHash+tsA+tsB)+padding, sk, prev)

    Size: 48 bytes (typ. for DSA signature), see notes below
```
Contenus non chiffrés :

```
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |              signature                |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +                                       +
 |                                       |
 +----+----+----+----+----+----+----+----+
 |               padding                 |
 +----+----+----+----+----+----+----+----+

  signature :: the Signature of the following concatenated data:
               X, Y, Alice's RouterIdentity, tsA, tsB.
               Bob signs it with the SigningPrivateKey associated with
               the SigningPublicKey in his RouterIdentity

  padding :: 0-15 bytes random data
```
Contenu chiffré :

```
 +----+----+----+----+----+----+----+----+
 |                                       |
 +                                       +
 |             encrypted data            |
 ~               .   .   .               ~
 |                                       |
 +----+----+----+----+----+----+----+----+

  encrypted data: Data AES encrypted using the DH session key and
                  the last 16 bytes of the encrypted contents of message #2 as the IV
                  48 bytes for a DSA signature, may vary for other signature types
```
**Notes :**

- Alice vérifie la signature, et en cas d'échec, abandonne la connexion.
- Bob utilisera les 16 derniers octets du contenu chiffré de ce message comme IV pour le message suivant.
- Jusqu'à la version 0.9.15, la signature était toujours une signature DSA de 40 octets et le remplissage était toujours de 8 octets. À partir de la version 0.9.16, le type et la longueur de la signature sont implicites selon le type de la [Clé Publique de Signature](/docs/specs/common-structures#type_SigningPublicKey) dans l'[Identité de Routeur](/docs/specs/common-structures#struct_RouterIdentity) de Bob. Le remplissage est ajusté selon les besoins pour obtenir un multiple de 16 octets pour l'ensemble du contenu non chiffré.

#### Après l'établissement

La connexion est établie, et des messages standard ou de synchronisation temporelle peuvent être échangés. Tous les messages suivants sont chiffrés AES en utilisant la clé de session DH négociée. Alice utilisera les 16 derniers octets du contenu chiffré du message #3 comme prochain IV. Bob utilisera les 16 derniers octets du contenu chiffré du message #4 comme prochain IV.

### Message de vérification de connexion

Alternativement, lorsque Bob reçoit une connexion, il pourrait s'agir d'une connexion de vérification (peut-être déclenchée par Bob demandant à quelqu'un de vérifier son écouteur). Check Connection n'est actuellement pas utilisé. Cependant, pour mémoire, les connexions de vérification sont formatées comme suit. Une connexion d'information de vérification recevra 256 octets contenant :

- 32 octets de données non interprétées, ignorées
- 1 octet de taille
- ce nombre d'octets constituant l'adresse IP du router local (tel qu'atteint par le côté distant)
- numéro de port sur 2 octets sur lequel le router local a été atteint
- temps réseau i2p sur 4 octets tel que connu par le côté distant (secondes depuis l'époque)
- données de remplissage non interprétées, jusqu'à l'octet 223
- xor du hash d'identité du router local et du SHA256 des octets 32 à 223

La vérification de connexion est complètement désactivée depuis la version 0.9.12.

## Discussion

Maintenant sur la [Page de discussion NTCP](/docs/discussions/ntcp).

## Travaux futurs {#future}

- La taille maximale des messages devrait être augmentée à environ 32 Ko.

- Un ensemble de tailles de paquets fixes pourrait être approprié pour masquer davantage la
  fragmentation des données aux adversaires externes, mais le remplissage au niveau du tunnel, garlic, et bout à
  bout devrait être suffisant pour la plupart des besoins d'ici là.
  Cependant, il n'y a actuellement aucune disposition pour le remplissage au-delà de la prochaine limite de 16 octets,
  pour créer un nombre limité de tailles de messages.

- L'utilisation de la mémoire (y compris celle du noyau) pour NTCP doit être comparée à celle pour SSU.

- Les messages d'établissement peuvent-ils être remplis de manière aléatoire d'une façon ou d'une autre, pour empêcher l'identification du trafic I2P basée sur les tailles de paquets initiaux ?
