---
title: "ECIES-X25519-AEAD-Ratchet"
description: "Schéma de chiffrement intégré à courbe elliptique pour le chiffrement de bout en bout I2P"
slug: "ecies"
aliases:
  - "/fr/docs/specs/ecies-x25519-aead-ratchet"
  - "/fr/docs/specs/ecies-x25519-aead-ratchet/"
category: "Protocoles"
lastUpdated: "2025-06"
accurateFor: "0.9.67"
---

## Note

Déploiement réseau terminé. Sujet à des révisions mineures. Voir [Prop144](/proposals/144-ecies-x25519/) pour la proposition originale, incluant les discussions de contexte et des informations supplémentaires.

Les fonctionnalités suivantes ne sont pas implémentées à partir de la version 0.9.66 :

- Blocs MessageNumbers, Options et Termination
- Réponses de couche protocole
- Clé statique zéro
- Multidiffusion

Pour la version MLKEM PQ Hybrid de ce protocole, voir [ECIES-HYBRID](/docs/specs/ecies-hybrid/).

## Aperçu

Il s'agit du nouveau protocole de chiffrement de bout en bout destiné à remplacer ElGamal/AES+SessionTags [ElG-AES](/docs/specs/elgamal-aes/).

Il s'appuie sur les travaux précédents comme suit :

- Spécification des structures communes [Common](/docs/specs/common-structures/)
- Spécification [I2NP](/docs/specs/i2np/) incluant LS2
- ElGamal/AES+Session Tags [Elg-AES](/docs/specs/elgamal-aes/)
- <http://zzz.i2p/topics/1768> aperçu de la nouvelle cryptographie asymétrique
- Aperçu de la cryptographie bas niveau [CRYPTO-ELG](/docs/specs/cryptography/#elgamal)
- ECIES <http://zzz.i2p/topics/2418>
- [NTCP2](/docs/specs/ntcp2/) [Prop111](/proposals/111-ntcp2/)
- 123 Nouvelles entrées netDB
- 142 Nouveau modèle cryptographique
- Protocole [Noise](https://noiseprotocol.org/noise.html)
- Algorithme double ratchet de [Signal](https://signal.org/docs/specifications/doubleratchet/)

Il prend en charge un nouveau chiffrement pour la communication de bout en bout, de destination à destination.

La conception utilise un handshake Noise et une phase de données incorporant le double ratchet de Signal.

Toutes les références à Signal et Noise dans cette spécification sont fournies uniquement à titre d'information contextuelle. La connaissance des protocoles Signal et Noise n'est pas requise pour comprendre ou implémenter cette spécification.

Cette spécification est prise en charge à partir de la version 0.9.46.

## Spécification

La conception utilise un handshake Noise et une phase de données incorporant le double ratchet de Signal.

### Résumé de la conception cryptographique

Il y a cinq parties du protocole à reconcevoir :

- 1\) Les nouveaux formats de conteneur de Session et les formats existants sont remplacés par de nouveaux formats.
- 2\) ElGamal (clés publiques de 256 octets, clés privées de 128 octets) est remplacé par ECIES-X25519 (clés publiques et privées de 32 octets)
- 3\) AES est remplacé par AEAD_ChaCha20_Poly1305 (abrégé en ChaChaPoly ci-dessous)
- 4\) Les SessionTags seront remplacés par des ratchets, qui sont essentiellement un PRNG cryptographique synchronisé.
- 5\) La charge utile AES, telle que définie dans la spécification ElGamal/AES+SessionTags, est remplacée par un format de bloc similaire à celui de NTCP2.

Chacun des cinq changements a sa propre section ci-dessous.

### Type de chiffrement

Le type crypto (utilisé dans le LS2) est 4. Ceci indique une clé publique X25519 32-octet little-endian, et le protocole de bout en bout spécifié ici.

Le type de crypto 0 est ElGamal. Les types de crypto 1-3 sont réservés pour ECIES-ECDH-AES-SessionTag, voir la proposition 145 [Prop145](/proposals/145-ecies-ecdh-aes/).

### Framework de Protocole Noise

Ce protocole fournit les exigences basées sur le Noise Protocol Framework [NOISE](https://noiseprotocol.org/noise.html) (Révision 34, 2018-07-11). Noise a des propriétés similaires au protocole Station-To-Station [STS](https://en.wikipedia.org/wiki/Station-to-Station_protocol), qui est la base du protocole [SSU](/docs/transport/ssu/). Dans le langage Noise, Alice est l'initiateur, et Bob est le répondeur.

Cette spécification est basée sur le protocole Noise Noise_IK_25519_ChaChaPoly_SHA256. (L'identifiant réel pour la fonction de dérivation de clé initiale est "Noise_IKelg2_25519_ChaChaPoly_SHA256" pour indiquer les extensions I2P - voir la section KDF 1 ci-dessous) Ce protocole Noise utilise les primitives suivantes :

- Motif de négociation interactif : IK Alice transmet immédiatement sa
  clé statique à Bob (I) Alice connaît déjà la clé statique de Bob (K)
- Motif de négociation unidirectionnel : N Alice ne transmet pas sa clé statique à
  Bob (N)
- Fonction DH : X25519 X25519 DH avec une longueur de clé de 32 octets comme
  spécifié dans [RFC-7748](https://tools.ietf.org/html/rfc7748).
- Fonction de chiffrement : ChaChaPoly AEAD_CHACHA20_POLY1305 comme spécifié dans
  [RFC-7539](https://tools.ietf.org/html/rfc7539) section 2.8. Nonce de 12 octets, avec
  les 4 premiers octets définis à zéro. Identique à celui dans
  [NTCP2](/docs/specs/ntcp2/).
- Fonction de hachage : SHA256 Hachage standard de 32 octets, déjà utilisé de manière extensive
  dans I2P.

#### Ajouts au Framework

Cette spécification définit les améliorations suivantes à Noise_IK_25519_ChaChaPoly_SHA256. Celles-ci suivent généralement les directives de la section 13 de [NOISE](https://noiseprotocol.org/noise.html).

1)  Les clés éphémères en clair sont encodées avec

    [Elligator2](https://elligator.cr.yp.to/elligator-20130828.pdf).
2) La réponse est préfixée avec une balise en texte clair. 3) Le format de la charge utile est défini pour les messages 1, 2 et la phase de données.

    Of course, this is not defined in Noise.

Tous les messages incluent un en-tête de message I2NP [Garlic Message](/docs/specs/i2np/). La phase de données utilise un chiffrement similaire à, mais non compatible avec, la phase de données Noise.

### Modèles de négociation

Les handshakes utilisent les modèles de handshake [Noise](https://noiseprotocol.org/noise.html).

Le mappage de lettres suivant est utilisé :

- e = clé éphémère à usage unique
- s = clé statique
- p = charge utile du message

Les sessions One-time et Unbound sont similaires au modèle Noise N.

```
<- s
...
e es p ->
```
Les sessions liées sont similaires au modèle Noise IK.

```
<- s
...
e es s ss p ->
<- tag e ee se
<- p
p ->
```
#### Propriétés de sécurité

En utilisant la terminologie Noise, la séquence d'établissement et de données est la suivante : (Propriétés de sécurité des charges utiles depuis [Noise](https://noiseprotocol.org/noise.html) )

```
IK(s, rs):           Authentication   Confidentiality
  <- s
  ...
  -> e, es, s, ss           1                2
  <- e, ee, se              2                4
  ->                        2                5
  <-                        2                5
```
#### Différences par rapport à XK

Les négociations IK présentent plusieurs différences par rapport aux négociations XK utilisées dans [NTCP2](/docs/specs/ntcp2/) et [SSU2](/docs/specs/ssu2/).

- Quatre opérations DH au total comparé à trois pour XK
- Authentification de l'expéditeur dans le premier message : La charge utile est authentifiée comme appartenant au propriétaire de la clé publique de l'expéditeur, bien que la clé puisse avoir été compromise (Authentification 1) XK nécessite un autre aller-retour avant qu'Alice soit authentifiée.
- Confidentialité persistante complète (Confidentialité 5) après le deuxième message. Bob peut envoyer une charge utile immédiatement après le deuxième message avec une confidentialité persistante complète. XK nécessite un autre aller-retour pour la confidentialité persistante complète.

En résumé, IK permet la livraison en 1-RTT de la charge utile de réponse de Bob vers Alice avec une confidentialité persistante complète, cependant la charge utile de la requête n'est pas à confidentialité persistante.

### Sessions

Le protocole ElGamal/AES+SessionTag est unidirectionnel. À cette couche, le destinataire ne sait pas d'où provient un message. Les sessions sortantes et entrantes ne sont pas associées. Les accusés de réception sont hors-bande en utilisant un DeliveryStatusMessage (encapsulé dans un GarlicMessage) dans le clove.

Pour cette spécification, nous définissons deux mécanismes pour créer un protocole bidirectionnel - "pairing" et "binding". Ces mécanismes offrent une efficacité et une sécurité accrues.

#### Contexte de Session

Comme avec ElGamal/AES+SessionTags, toutes les sessions entrantes et sortantes doivent être dans un contexte donné, soit le contexte du router soit le contexte d'une destination locale particulière. Dans Java I2P, ce contexte est appelé le Session Key Manager.

Les sessions ne doivent pas être partagées entre les contextes, car cela permettrait une corrélation entre les diverses destinations locales, ou entre une destination locale et un router.

Lorsqu'une destination donnée prend en charge à la fois ElGamal/AES+SessionTags et cette spécification, les deux types de sessions peuvent partager un contexte. Voir la section 1c) ci-dessous.

#### Appariement des sessions entrantes et sortantes

Lorsqu'une session sortante est créée chez l'initiateur (Alice), une nouvelle session entrante est créée et appariée avec la session sortante, sauf si aucune réponse n'est attendue (par exemple, les datagrammes bruts).

Une nouvelle session entrante est toujours associée à une nouvelle session sortante, sauf si aucune réponse n'est demandée (par exemple, les datagrammes bruts).

Si une réponse est demandée et liée à une destination ou un router distant, cette nouvelle session sortante est liée à cette destination ou ce router, et remplace toute session sortante précédente vers cette destination ou ce router.

L'appariement des sessions entrantes et sortantes fournit un protocole bidirectionnel avec la capacité de faire progresser les clés DH.

#### Liaison des sessions et des destinations

Il n'y a qu'une seule session sortante vers une destination ou un router donné. Il peut y avoir plusieurs sessions entrantes actuelles depuis une destination ou un router donné. En général, lorsqu'une nouvelle session entrante est créée et que du trafic est reçu sur cette session (ce qui sert d'ACK), toutes les autres seront marquées pour expirer relativement rapidement, dans la minute qui suit environ. La valeur des messages précédents envoyés (PN) est vérifiée, et s'il n'y a pas de messages non reçus (dans la taille de la fenêtre) dans la session entrante précédente, la session précédente peut être supprimée immédiatement.

Lorsqu'une session sortante est créée chez l'expéditeur (Alice), elle est liée à la Destination distante (Bob), et toute session entrante associée sera également liée à la Destination distante. Au fur et à mesure que les sessions progressent, elles continuent d'être liées à la Destination distante.

Lorsqu'une session entrante est créée chez le destinataire (Bob), elle peut être liée à la Destination de l'extrémité distante (Alice), au choix d'Alice. Si Alice inclut des informations de liaison (sa clé statique) dans le message New Session, la session sera liée à cette destination, et une session sortante sera créée et liée à la même Destination. Au fur et à mesure que les sessions progressent par ratchet, elles continuent d'être liées à la Destination de l'extrémité distante.

#### Avantages de la liaison et de l'appairage

Pour le cas courant de streaming, nous nous attendons à ce qu'Alice et Bob utilisent le protocole comme suit :

- Alice associe sa nouvelle session sortante à une nouvelle session entrante, toutes deux
  liées à la destination finale (Bob).
- Alice inclut les informations de liaison et la signature, ainsi qu'une demande de réponse,
  dans le message New Session envoyé à Bob.
- Bob associe sa nouvelle session entrante à une nouvelle session sortante, toutes deux
  liées à la destination finale (Alice).
- Bob envoie une réponse (ack) à Alice dans la session associée, avec un ratchet
  vers une nouvelle clé DH.
- Alice effectue un ratchet vers une nouvelle session sortante avec la nouvelle clé de Bob, associée
  à la session entrante existante.

En liant une session entrante à une Destination distante, et en associant la session entrante à une session sortante liée à la même Destination, nous obtenons deux avantages majeurs :

1)  La réponse initiale de Bob à Alice utilise un DH éphémère-éphémère

2\) Après qu'Alice reçoit la réponse de Bob et effectue le ratchet, tous les messages suivants d'Alice vers Bob utilisent du DH éphémère-éphémère.

#### ACKs de message

Dans ElGamal/AES+SessionTags, lorsqu'un leaseSet est regroupé comme un clou de garlic encryption, ou que des tags sont livrés, le router expéditeur demande un ACK. Il s'agit d'un clou de garlic encryption séparé contenant un message DeliveryStatus. Pour une sécurité supplémentaire, le message DeliveryStatus est encapsulé dans un message Garlic. Ce mécanisme est hors bande du point de vue du protocole.

Dans le nouveau protocole, puisque les sessions entrantes et sortantes sont appariées, nous pouvons avoir des ACKs dans la bande. Aucun clove séparé n'est requis.

Un ACK explicite est simplement un message de Session Existante sans bloc I2NP. Cependant, dans la plupart des cas, un ACK explicite peut être évité, car il y a du trafic inverse. Il peut être souhaitable pour les implémentations d'attendre un court moment (peut-être une centaine de ms) avant d'envoyer un ACK explicite, pour donner au streaming ou à la couche application le temps de répondre.

Les implémentations devront également différer l'envoi de tout ACK jusqu'après le traitement du bloc I2NP, car le message Garlic peut contenir un message Database Store avec un leaseSet. Un leaseSet récent sera nécessaire pour router l'ACK, et la destination distante (contenue dans le leaseSet) sera nécessaire pour vérifier la clé statique de liaison.

#### Délais d'expiration de session

Les sessions sortantes doivent toujours expirer avant les sessions entrantes. Une fois qu'une session sortante expire et qu'une nouvelle est créée, une nouvelle session entrante appariée sera également créée. S'il y avait une ancienne session entrante, elle sera autorisée à expirer.

### Multidiffusion

À déterminer

### Définitions

Nous définissons les fonctions suivantes correspondant aux blocs de construction cryptographiques utilisés.

ZEROLEN

tableau d'octets de longueur zéro

CSRNG(n)

sortie de n octets provenant d'un générateur de nombres aléatoires cryptographiquement sûr

    generator.

H(p, d)

Fonction de hachage SHA-256 qui prend une chaîne de personnalisation p et des données

    d, and produces an output of length 32 bytes. As defined in
    [NOISE](https://noiseprotocol.org/noise.html). || below means append.

    Use SHA-256 as follows:

        H(p, d) := SHA-256(p || d)

MixHash(d)

Fonction de hachage SHA-256 qui prend un hachage précédent h et de nouvelles données d,

    and produces an output of length 32 bytes. || below means append.

    Use SHA-256 as follows:

        MixHash(d) := h = SHA-256(h || d)

STREAM

Le AEAD ChaCha20/Poly1305 tel que spécifié dans

    [RFC-7539](https://tools.ietf.org/html/rfc7539). S_KEY_LEN = 32 and S_IV_LEN =
    12.

    ENCRYPT(k, n, plaintext, ad)

    :   Encrypts plaintext using the cipher key k, and nonce n which
        MUST be unique for the key k. Associated data ad is optional.
        Returns a ciphertext that is the size of the plaintext + 16
        bytes for the HMAC.

        The entire ciphertext must be indistinguishable from random if
        the key is secret.

    DECRYPT(k, n, ciphertext, ad)

    :   Decrypts ciphertext using the cipher key k, and nonce n.
        Associated data ad is optional. Returns the plaintext.

DH

Système d'accord de clés publiques X25519. Clés privées de 32 octets, publiques

    keys of 32 bytes, produces outputs of 32 bytes. It has the following
    functions:

    GENERATE_PRIVATE()

    :   Generates a new private key.

    DERIVE_PUBLIC(privkey)

    :   Returns the public key corresponding to the given private key.

    GENERATE_PRIVATE_ELG2()

    :   Generates a new private key that maps to a public key suitable
        for Elligator2 encoding. Note that half of the
        randomly-generated private keys will not be suitable and must be
        discarded.

    ENCODE_ELG2(pubkey)

    :   Returns the Elligator2-encoded public key corresponding to the
        given public key (inverse mapping). Encoded keys are little
        endian. Encoded key must be 256 bits indistinguishable from
        random data. See Elligator2 section below for specification.

    DECODE_ELG2(pubkey)

    :   Returns the public key corresponding to the given
        Elligator2-encoded public key. See Elligator2 section below for
        specification.

    DH(privkey, pubkey)

    :   Generates a shared secret from the given private and public
        keys.

HKDF(salt, ikm, info, n)

Une fonction de dérivation de clé cryptographique qui prend une clé d'entrée

    material ikm (which should have good entropy but is not required to
    be a uniformly random string), a salt of length 32 bytes, and a
    context-specific 'info' value, and produces an output of n bytes
    suitable for use as key material.

    Use HKDF as specified in [RFC-5869](https://tools.ietf.org/html/rfc5869), using
    the HMAC hash function SHA-256 as specified in
    [RFC-2104](https://tools.ietf.org/html/rfc2104). This means that SALT_LEN is 32
    bytes max.

MixKey(d)

Utilisez HKDF() avec une chainKey précédente et de nouvelles données d, et définit la nouvelle

    chainKey and k. As defined in [NOISE](https://noiseprotocol.org/noise.html).

    Use HKDF as follows:

        MixKey(d) := output = HKDF(chainKey, d, "", 64)
                     chainKey = output[0:31]
                     k = output[32:63]

### 1) Format de message

#### Revue du format de message actuel

Le message garlic tel que spécifié dans [I2NP](/docs/specs/i2np/) est le suivant. Comme un objectif de conception est que les relais intermédiaires ne peuvent pas distinguer la nouvelle cryptographie de l'ancienne, ce format ne peut pas changer, même si le champ de longueur est redondant. Le format est montré avec l'en-tête complet de 16 octets, bien que l'en-tête réel puisse être dans un format différent, selon le transport utilisé.

Une fois déchiffrées, les données contiennent une série de Garlic Cloves et des données supplémentaires, également connues sous le nom de Clove Set.

Voir [I2NP](/docs/specs/i2np/) pour les détails et la spécification complète.

```
+----+----+----+----+----+----+----+----+
|type|      msg_id       |  expiration
+----+----+----+----+----+----+----+----+
                         |  size   |chks|
+----+----+----+----+----+----+----+----+
|      length       |                   |
+----+----+----+----+                   +
|          encrypted data               |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
```
#### Révision du format des données chiffrées

Dans ElGamal/AES+SessionTags, il existe deux formats de message :

1\) Nouvelle session : - bloc ElGamal de 514 octets - bloc AES (128 octets minimum, multiple de 16)

2\) Session existante : - Session Tag de 32 octets - Bloc AES (128 octets minimum, multiple de 16)

Ces messages sont encapsulés dans un message I2NP garlic, qui contient un champ de longueur, donc la longueur est connue.

Le destinataire tente d'abord de rechercher les 32 premiers octets comme Session Tag. S'il est trouvé, il décrypte le bloc AES. S'il n'est pas trouvé, et que les données font au moins (514+16) octets de long, il tente de décrypter le bloc ElGamal, et en cas de succès, décrypte le bloc AES.

#### Nouveaux tags de session et comparaison avec Signal

Dans Signal Double Ratchet, l'en-tête contient :

- DH : Clé publique ratchet actuelle
- PN : Longueur du message de la chaîne précédente
- N : Numéro de message

Les "chaînes d'envoi" de Signal sont à peu près équivalentes à nos ensembles de balises. En utilisant une balise de session, nous pouvons éliminer la plupart de cela.

Dans New Session, nous mettons seulement la clé publique dans l'en-tête non chiffré.

Dans une session existante, nous utilisons une étiquette de session pour l'en-tête. L'étiquette de session est associée à la clé publique ratchet actuelle et au numéro de message.

Dans les sessions nouvelles et existantes, PN et N se trouvent dans le corps chiffré.

Dans Signal, les choses sont constamment en rotation. Une nouvelle clé publique DH nécessite que le destinataire effectue une rotation et renvoie une nouvelle clé publique, ce qui sert également d'accusé de réception pour la clé publique reçue. Cela représenterait bien trop d'opérations DH pour nous. Nous séparons donc l'accusé de réception de la clé reçue et la transmission d'une nouvelle clé publique. Tout message utilisant une balise de session générée à partir de la nouvelle clé publique DH constitue un ACK. Nous ne transmettons une nouvelle clé publique que lorsque nous souhaitons régénérer les clés.

Le nombre maximum de messages avant que le DH doive effectuer un ratchet est de 65535.

Lors de la livraison d'une clé de session, nous dérivons le "Tag Set" à partir de celle-ci, plutôt que d'avoir à livrer également les balises de session. Un Tag Set peut contenir jusqu'à 65536 balises. Cependant, les récepteurs devraient implémenter une stratégie de "look-ahead", plutôt que de générer toutes les balises possibles en une seule fois. Générer au maximum N balises au-delà de la dernière bonne balise reçue. N pourrait être au maximum 128, mais 32 ou même moins pourrait être un meilleur choix.

### 1a) Nouveau format de session

Clé publique à usage unique de nouvelle session (32 octets) Données chiffrées et MAC (octets restants)

Le message New Session peut contenir ou non la clé publique statique de l'expéditeur. Si elle est incluse, la session inverse est liée à cette clé. La clé statique devrait être incluse si des réponses sont attendues, c'est-à-dire pour le streaming et les datagrammes avec réponse possible. Elle ne devrait pas être incluse pour les datagrammes bruts.

Le message New Session est similaire au pattern Noise [NOISE](https://noiseprotocol.org/noise.html) unidirectionnel "N" (si la clé statique n'est pas envoyée), ou au pattern bidirectionnel "IK" (si la clé statique est envoyée).

### 1b) Nouveau format de session (avec liaison)

La longueur est de 96 + longueur de la charge utile. Format chiffré :

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|   New Session Ephemeral Public Key    |
+             32 bytes                  +
|     Encoded with Elligator2           |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+         Static Key                    +
|       ChaCha20 encrypted data         |
+            32 bytes                   +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+    (MAC) for Static Key Section       +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

Public Key :: 32 bytes, little endian, Elligator2, cleartext

Static Key encrypted data :: 32 bytes

Payload Section encrypted data :: remaining data minus 16 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
#### Nouvelle clé éphémère de session

La clé éphémère fait 32 octets, encodée avec Elligator2. Cette clé n'est jamais réutilisée ; une nouvelle clé est générée avec chaque message, y compris les retransmissions.

#### Clé Statique

Une fois déchiffrée, la clé statique X25519 d'Alice, 32 octets.

#### Charge utile

La longueur chiffrée correspond au reste des données. La longueur déchiffrée est inférieure de 16 à la longueur chiffrée. La charge utile doit contenir un bloc DateTime et contiendra généralement un ou plusieurs blocs Garlic Clove. Voir la section charge utile ci-dessous pour le format et les exigences supplémentaires.

### 1c) Nouveau format de session (sans liaison)

Si aucune réponse n'est requise, aucune clé statique n'est envoyée.

La longueur est de 96 + longueur de la charge utile. Format chiffré :

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|   New Session Ephemeral Public Key    |
+             32 bytes                  +
|     Encoded with Elligator2           |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+           Flags Section               +
|       ChaCha20 encrypted data         |
+            32 bytes                   +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for above section       +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

Public Key :: 32 bytes, little endian, Elligator2, cleartext

Flags Section encrypted data :: 32 bytes

Payload Section encrypted data :: remaining data minus 16 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
#### Nouvelle clé éphémère de session

Clé éphémère d'Alice. La clé éphémère fait 32 octets, encodée avec Elligator2, little endian. Cette clé n'est jamais réutilisée ; une nouvelle clé est générée pour chaque message, y compris les retransmissions.

#### Section Flags Données décryptées

La section Flags ne contient rien. Elle fait toujours 32 octets, car elle doit avoir la même longueur que la clé statique pour les messages New Session avec liaison. Bob détermine s'il s'agit d'une clé statique ou d'une section flags en testant si les 32 octets sont tous des zéros.

TODO des drapeaux sont-ils nécessaires ici ?

#### Charge utile

La longueur chiffrée correspond au reste des données. La longueur déchiffrée est inférieure de 16 à la longueur chiffrée. La charge utile doit contenir un bloc DateTime et contiendra généralement un ou plusieurs blocs Garlic Clove. Voir la section charge utile ci-dessous pour le format et les exigences supplémentaires.

### 1d) Format unique (pas de liaison ou de session)

Si un seul message doit être envoyé, aucune configuration de session ou clé statique n'est requise.

La longueur est de 96 + longueur de la charge utile. Format chiffré :

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|       Ephemeral Public Key            |
+             32 bytes                  +
|     Encoded with Elligator2           |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+           Flags Section               +
|       ChaCha20 encrypted data         |
+            32 bytes                   +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for above section       +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

Public Key :: 32 bytes, little endian, Elligator2, cleartext

Flags Section encrypted data :: 32 bytes

Payload Section encrypted data :: remaining data minus 16 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
#### Nouvelle clé de session à usage unique

La clé à usage unique fait 32 octets, encodée avec Elligator2, en little endian. Cette clé n'est jamais réutilisée ; une nouvelle clé est générée pour chaque message, y compris les retransmissions.

#### Section Flags Données décryptées

La section Flags ne contient rien. Elle fait toujours 32 octets, car elle doit avoir la même longueur que la clé statique pour les messages New Session avec liaison. Bob détermine s'il s'agit d'une clé statique ou d'une section flags en testant si les 32 octets sont tous des zéros.

TODO des drapeaux nécessaires ici ?

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|                                       |
+             All zeros                 +
|              32 bytes                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

zeros:: All zeros, 32 bytes.
```
#### Charge utile

La longueur chiffrée correspond au reste des données. La longueur déchiffrée est inférieure de 16 à la longueur chiffrée. La charge utile doit contenir un bloc DateTime et contiendra généralement un ou plusieurs blocs Garlic Clove. Voir la section charge utile ci-dessous pour le format et les exigences supplémentaires.

### 1f) KDF pour le message de nouvelle session

#### KDF pour la ChainKey initiale

Il s'agit du protocole [NOISE](https://noiseprotocol.org/noise.html) standard pour IK avec un nom de protocole modifié. Notez que nous utilisons le même initialiseur pour le motif IK (sessions liées) et pour le motif N (sessions non liées).

Le nom du protocole est modifié pour deux raisons. Premièrement, pour indiquer que les clés éphémères sont encodées avec Elligator2, et deuxièmement, pour indiquer que MixHash() est appelée avant le deuxième message pour incorporer la valeur du tag.

```
This is the "e" message pattern:

// Define protocol_name.
Set protocol_name = "Noise_IKelg2+hs2_25519_ChaChaPoly_SHA256"
 (40 bytes, US-ASCII encoded, no NULL termination).

// Define Hash h = 32 bytes
h = SHA256(protocol_name);

Define ck = 32 byte chaining key. Copy the h data to ck.
Set chainKey = h

// MixHash(null prologue)
h = SHA256(h);

// up until here, can all be precalculated by Alice for all outgoing connections
```
#### KDF pour le contenu chiffré de la section Flags/Static Key

```
This is the "e" message pattern:

// Bob's X25519 static keys
// bpk is published in leaseset
bsk = GENERATE_PRIVATE()
bpk = DERIVE_PUBLIC(bsk)

// Bob static public key
// MixHash(bpk)
// || below means append
h = SHA256(h || bpk);

// up until here, can all be precalculated by Bob for all incoming connections

// Alice's X25519 ephemeral keys
aesk = GENERATE_PRIVATE_ELG2()
aepk = DERIVE_PUBLIC(aesk)

// Alice ephemeral public key
// MixHash(aepk)
// || below means append
h = SHA256(h || aepk);

// h is used as the associated data for the AEAD in the New Session Message
// Retain the Hash h for the New Session Reply KDF
// eapk is sent in cleartext in the
// beginning of the New Session message
elg2_aepk = ENCODE_ELG2(aepk)
// As decoded by Bob
aepk = DECODE_ELG2(elg2_aepk)

End of "e" message pattern.

This is the "es" message pattern:

// Noise es
sharedSecret = DH(aesk, bpk) = DH(bsk, aepk)

// MixKey(DH())
//[chainKey, k] = MixKey(sharedSecret)
// ChaChaPoly parameters to encrypt/decrypt
keydata = HKDF(chainKey, sharedSecret, "", 64)
chainKey = keydata[0:31]

// AEAD parameters
k = keydata[32:63]
n = 0
ad = h
ciphertext = ENCRYPT(k, n, flags/static key section, ad)

End of "es" message pattern.

This is the "s" message pattern:

// MixHash(ciphertext)
// Save for Payload section KDF
h = SHA256(h || ciphertext)

// Alice's X25519 static keys
ask = GENERATE_PRIVATE()
apk = DERIVE_PUBLIC(ask)

End of "s" message pattern.
```
#### KDF pour la section Payload (avec la clé statique d'Alice)

```
This is the "ss" message pattern:

// Noise ss
sharedSecret = DH(ask, bpk) = DH(bsk, apk)

// MixKey(DH())
//[chainKey, k] = MixKey(sharedSecret)
// ChaChaPoly parameters to encrypt/decrypt
// chainKey from Static Key Section
Set sharedSecret = X25519 DH result
keydata = HKDF(chainKey, sharedSecret, "", 64)
chainKey = keydata[0:31]

// AEAD parameters
k = keydata[32:63]
n = 0
ad = h
ciphertext = ENCRYPT(k, n, payload, ad)

End of "ss" message pattern.

// MixHash(ciphertext)
// Save for New Session Reply KDF
h = SHA256(h || ciphertext)
```
#### KDF pour la section Payload (sans la clé statique d'Alice)

Notez qu'il s'agit d'un pattern Noise "N", mais nous utilisons le même initialiseur "IK" que pour les sessions liées.

Les messages New Session ne peuvent pas être identifiés comme contenant ou non la clé statique d'Alice tant que la clé statique n'est pas déchiffrée et inspectée pour déterminer si elle contient uniquement des zéros. Par conséquent, le récepteur doit utiliser la machine d'état "IK" pour tous les messages New Session. Si la clé statique ne contient que des zéros, le modèle de message "ss" doit être ignoré.

```
chainKey = from Flags/Static key section
k = from Flags/Static key section
n = 1
ad = h from Flags/Static key section
ciphertext = ENCRYPT(k, n, payload, ad)
```
### 1g) Format de réponse de nouvelle session

Une ou plusieurs réponses New Session Reply peuvent être envoyées en réponse à un seul message New Session. Chaque réponse est précédée d'une étiquette, qui est générée à partir d'un TagSet pour la session.

La New Session Reply se compose de deux parties. La première partie est l'achèvement de la négociation Noise IK avec une étiquette ajoutée en préfixe. La longueur de la première partie est de 56 octets. La deuxième partie est la charge utile de la phase de données. La longueur de la deuxième partie est de 16 + longueur de la charge utile.

La longueur totale est de 72 + longueur de la charge utile. Format chiffré :

```
+----+----+----+----+----+----+----+----+
|       Session Tag   8 bytes           |
+----+----+----+----+----+----+----+----+
|                                       |
+        Ephemeral Public Key           +
|                                       |
+            32 bytes                   +
|     Encoded with Elligator2           |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+  (MAC) for Key Section (no data)      +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

Tag :: 8 bytes, cleartext

Public Key :: 32 bytes, little endian, Elligator2, cleartext

MAC :: Poly1305 message authentication code, 16 bytes
       Note: The ChaCha20 plaintext data is empty (ZEROLEN)

Payload Section encrypted data :: remaining data minus 16 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
#### Étiquette de Session

Le tag est généré dans le Session Tags KDF, tel qu'initialisé dans le DH Initialization KDF ci-dessous. Ceci corrèle la réponse à la session. La Session Key du DH Initialization n'est pas utilisée.

#### Clé Éphémère de Réponse de Nouvelle Session

Clé éphémère de Bob. La clé éphémère fait 32 octets, encodée avec Elligator2, petit-boutiste. Cette clé n'est jamais réutilisée ; une nouvelle clé est générée avec chaque message, y compris les retransmissions.

#### Charge utile

La longueur chiffrée correspond au reste des données. La longueur déchiffrée est inférieure de 16 à la longueur chiffrée. La charge utile contiendra généralement un ou plusieurs blocs Garlic Clove. Voir la section charge utile ci-dessous pour le format et les exigences supplémentaires.

#### KDF pour Reply TagSet

Un ou plusieurs tags sont créés à partir du TagSet, qui est initialisé en utilisant la KDF ci-dessous, en utilisant la chainKey du message New Session.

```
// Generate tagset

tagsetKey = HKDF(chainKey, ZEROLEN, "SessionReplyTags", 32)
    tagset_nsr = DH_INITIALIZE(chainKey, tagsetKey)

```
#### KDF pour le contenu chiffré de la section de clé de réponse

```
// Keys from the New Session message
// Alice's X25519 keys
// apk and aepk are sent in original New Session message
// ask = Alice private static key
// apk = Alice public static key
// aesk = Alice ephemeral private key
// aepk = Alice ephemeral public key
// Bob's X25519 static keys
// bsk = Bob private static key
// bpk = Bob public static key

// Generate the tag
tagsetEntry = tagset_nsr.GET_NEXT_ENTRY()
tag = tagsetEntry.SESSION_TAG

// MixHash(tag)
h = SHA256(h || tag)

This is the "e" message pattern:

// Bob's X25519 ephemeral keys
besk = GENERATE_PRIVATE_ELG2()
bepk = DERIVE_PUBLIC(besk)

// Bob's ephemeral public key
// MixHash(bepk)
// || below means append
h = SHA256(h || bepk);

// elg2_bepk is sent in cleartext in the
// beginning of the New Session message
elg2_bepk = ENCODE_ELG2(bepk)
// As decoded by Bob
bepk = DECODE_ELG2(elg2_bepk)

End of "e" message pattern.

This is the "ee" message pattern:

// MixKey(DH())
//[chainKey, k] = MixKey(sharedSecret)
// ChaChaPoly parameters to encrypt/decrypt
// chainKey from original New Session Payload Section
sharedSecret = DH(aesk, bepk) = DH(besk, aepk)
keydata = HKDF(chainKey, sharedSecret, "", 32)
chainKey = keydata[0:31]

End of "ee" message pattern.

This is the "se" message pattern:

// MixKey(DH())
//[chainKey, k] = MixKey(sharedSecret)
sharedSecret = DH(ask, bepk) = DH(besk, apk)
keydata = HKDF(chainKey, sharedSecret, "", 64)
chainKey = keydata[0:31]

// AEAD parameters
k = keydata[32:63]
n = 0
ad = h
ciphertext = ENCRYPT(k, n, ZEROLEN, ad)

End of "se" message pattern.

// MixHash(ciphertext)
h = SHA256(h || ciphertext)

chainKey is used in the ratchet below.
```
#### KDF pour le contenu chiffré de la section de charge utile

Ceci ressemble au premier message de Session Existante, post-division, mais sans étiquette séparée. De plus, nous utilisons le hash ci-dessus pour lier la charge utile au message NSR.

```
This is the "ss" message pattern:

// Noise ss
sharedSecret = DH(ask, bpk) = DH(bsk, apk)

// MixKey(DH())
//[chainKey, k] = MixKey(sharedSecret)
// ChaChaPoly parameters to encrypt/decrypt
// chainKey from Static Key Section
Set sharedSecret = X25519 DH result
keydata = HKDF(chainKey, sharedSecret, "", 64)
chainKey = keydata[0:31]

// AEAD parameters
k = keydata[32:63]
n = 0
ad = h
ciphertext = ENCRYPT(k, n, payload, ad)

End of "ss" message pattern.

// MixHash(ciphertext)
// Save for New Session Reply KDF
h = SHA256(h || ciphertext)
```
### Notes

Plusieurs messages NSR peuvent être envoyés en réponse, chacun avec des clés éphémères uniques, selon la taille de la réponse.

Alice et Bob sont tenus d'utiliser de nouvelles clés éphémères pour chaque message NS et NSR.

Alice doit recevoir l'un des messages NSR de Bob avant d'envoyer des messages de Session Existante (ES), et Bob doit recevoir un message ES d'Alice avant d'envoyer des messages ES.

Le `chainKey` et `k` de la section NSR Payload de Bob sont utilisés comme entrées pour les DH Ratchets ES initiaux (dans les deux directions, voir DH Ratchet KDF).

Bob ne doit conserver que les Sessions Existantes pour les messages ES reçus d'Alice. Toutes les autres sessions entrantes et sortantes créées (pour plusieurs NSR) doivent être détruites immédiatement après avoir reçu le premier message ES d'Alice pour une session donnée.

### 1h) Format de session existant

Balise de session (8 octets) Données chiffrées et MAC (voir section 3 ci-dessous)

#### Format

Chiffré :

```
+----+----+----+----+----+----+----+----+
|       Session Tag                     |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+              (MAC)                    +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

Session Tag :: 8 bytes, cleartext

Payload Section encrypted data :: remaining data minus 16 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
#### Charge utile

La longueur chiffrée correspond au reste des données. La longueur déchiffrée est inférieure de 16 à la longueur chiffrée. Voir la section charge utile ci-dessous pour le format et les exigences.

#### KDF

```
See AEAD section below.

// AEAD parameters for Existing Session payload
k = The 32-byte session key associated with this session tag
n = The message number N in the current chain, as retrieved from the associated Session Tag.
ad = The session tag, 8 bytes
ciphertext = ENCRYPT(k, n, payload, ad)
```
### 2) ECIES-X25519

Format : clés publiques et privées de 32 octets, little-endian.

### 2a) Elligator2

Dans les handshakes Noise standard, les messages de handshake initiaux dans chaque direction commencent par des clés éphémères qui sont transmises en clair. Comme les clés X25519 valides sont distinguables des données aléatoires, un homme du milieu peut distinguer ces messages des messages de Session Existante qui commencent par des balises de session aléatoires. Dans [NTCP2](/docs/specs/ntcp2/) ([Prop111](/proposals/111-ntcp2/)), nous avons utilisé une fonction XOR à faible coût utilisant la clé statique hors bande pour obfusquer la clé. Cependant, le modèle de menace ici est différent ; nous ne voulons pas permettre à un MitM d'utiliser quelque moyen que ce soit pour confirmer la destination du trafic, ou pour distinguer les messages de handshake initiaux des messages de Session Existante.

Par conséquent, [Elligator2](https://elligator.cr.yp.to/elligator-20130828.pdf) est utilisé pour transformer les clés éphémères dans les messages New Session et New Session Reply afin qu'elles soient indiscernables de chaînes aléatoires uniformes.

#### Format

Clés publiques et privées de 32 octets. Les clés encodées sont en little endian.

Comme défini dans [Elligator2](https://elligator.cr.yp.to/elligator-20130828.pdf), les clés encodées sont indiscernables de 254 bits aléatoires. Nous avons besoin de 256 bits aléatoires (32 octets). Par conséquent, l'encodage et le décodage sont définis comme suit :

Encodage :

```
ENCODE_ELG2() Definition

// Encode as defined in Elligator2 specification
encodedKey = encode(pubkey)
// OR in 2 random bits to MSB
randomByte = CSRNG(1)
encodedKey[31] |= (randomByte & 0xc0)
```
Décodage :

```
DECODE_ELG2() Definition

// Mask out 2 random bits from MSB
encodedKey[31] &= 0x3f
// Decode as defined in Elligator2 specification
pubkey = decode(encodedKey)
```
#### Notes

Elligator2 double en moyenne le temps de génération de clés, car la moitié des clés privées résultent en des clés publiques qui ne conviennent pas pour l'encodage avec Elligator2. De plus, le temps de génération de clés est non borné avec une distribution exponentielle, car le générateur doit continuer à réessayer jusqu'à ce qu'une paire de clés appropriée soit trouvée.

Cette surcharge peut être gérée en effectuant la génération de clés à l'avance, dans un thread séparé, pour maintenir un pool de clés appropriées.

Le générateur exécute la fonction ENCODE_ELG2() pour déterminer la compatibilité. Par conséquent, le générateur devrait stocker le résultat d'ENCODE_ELG2() afin qu'il n'ait pas à être recalculé.

De plus, les clés inadéquates peuvent être ajoutées au pool de clés utilisées pour [NTCP2](/docs/specs/ntcp2/), où Elligator2 n'est pas utilisé. Les problèmes de sécurité liés à cette pratique restent à déterminer.

### 3) AEAD (ChaChaPoly)

AEAD utilisant ChaCha20 et Poly1305, identique à celui dans [NTCP2](/docs/specs/ntcp2/). Cela correspond à [RFC-7539](https://tools.ietf.org/html/rfc7539), qui est également utilisé de manière similaire dans TLS [RFC-7905](https://tools.ietf.org/html/rfc7905).

#### Entrées de Nouvelle Session et de Réponse de Nouvelle Session

Entrées des fonctions de chiffrement/déchiffrement pour un bloc AEAD dans un message New Session :

```
k :: 32 byte cipher key
     See New Session and New Session Reply KDFs above.

n :: Counter-based nonce, 12 bytes.
     n = 0

ad :: Associated data, 32 bytes.
      The SHA256 hash of the preceding data, as output from mixHash()

data :: Plaintext data, 0 or more bytes
```
#### Entrées de session existantes

Entrées des fonctions de chiffrement/déchiffrement pour un bloc AEAD dans un message de session existante :

```
k :: 32 byte session key
     As looked up from the accompanying session tag.

n :: Counter-based nonce, 12 bytes.
     Starts at 0 and incremented for each message when transmitting.
     For the receiver, the value
     as looked up from the accompanying session tag.
     First four bytes are always zero.
     Last eight bytes are the message number (n), little-endian encoded.
     Maximum value is 65535.
     Session must be ratcheted when N reaches that value.
     Higher values must never be used.

ad :: Associated data
      The session tag

data :: Plaintext data, 0 or more bytes
```
#### Format chiffré

Sortie de la fonction de chiffrement, entrée de la fonction de déchiffrement :

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|       ChaCha20 encrypted data         |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+              (MAC)                    +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

encrypted data :: Same size as plaintext data, 0 - 65519 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
#### Remarques

- Étant donné que ChaCha20 est un chiffrement par flux, les textes en clair n'ont pas besoin d'être complétés par du bourrage.
  Les octets de flux de clés supplémentaires sont supprimés.
- La clé pour le chiffrement (256 bits) est convenue au moyen du
  KDF SHA256. Les détails du KDF pour chaque message sont dans des
  sections séparées ci-dessous.
- Les trames ChaChaPoly sont de taille connue car elles sont encapsulées dans le
  message de données I2NP.
- Pour tous les messages, le bourrage se trouve à l'intérieur de la trame de données authentifiées.

#### Gestion des erreurs AEAD

Toutes les données reçues qui échouent à la vérification AEAD doivent être supprimées. Aucune réponse n'est retournée.

### 4) Ratchets

Nous utilisons toujours les session tags, comme auparavant, mais nous utilisons des ratchets pour les générer. Les session tags avaient aussi une option de renouvellement de clé que nous n'avons jamais implémentée. C'est donc comme un double ratchet mais nous n'avons jamais fait le second.

Ici, nous définissons quelque chose de similaire au Double Ratchet de Signal. Les balises de session sont générées de manière déterministe et identique côté récepteur et côté expéditeur.

En utilisant un mécanisme de clé symétrique/tag ratchet, nous éliminons l'utilisation de mémoire pour stocker les session tags du côté expéditeur. Nous éliminons également la consommation de bande passante nécessaire à l'envoi des ensembles de tags. L'utilisation côté récepteur reste significative, mais nous pouvons la réduire davantage car nous allons réduire le session tag de 32 octets à 8 octets.

Nous n'utilisons pas le chiffrement d'en-tête tel que spécifié (et optionnel) dans Signal, nous utilisons des étiquettes de session à la place.

En utilisant un ratchet DH, nous obtenons la confidentialité persistante, qui n'a jamais été implémentée dans ElGamal/AES+SessionTags.

Note : La clé publique à usage unique de Nouvelle Session ne fait pas partie du ratchet, sa seule fonction est de chiffrer la clé de ratchet DH initiale d'Alice.

#### Numéros de message

Le Double Ratchet gère les messages perdus ou désordonnés en incluant dans chaque en-tête de message une étiquette. Le récepteur recherche l'index de l'étiquette, qui correspond au numéro de message N. Si le message contient un bloc Message Number avec une valeur PN, le destinataire peut supprimer toutes les étiquettes supérieures à cette valeur dans le jeu d'étiquettes précédent, tout en conservant les étiquettes ignorées du jeu d'étiquettes précédent au cas où les messages ignorés arriveraient plus tard.

#### Implémentation d'exemple

Nous définissons les structures de données et fonctions suivantes pour implémenter ces ratchets.

TAGSET_ENTRY

Une entrée unique dans un TAGSET.

    INDEX

    :   An integer index, starting with 0

    SESSION_TAG

    :   An identifier to go out on the wire, 8 bytes

    SESSION_KEY

    :   A symmetric key, never goes on the wire, 32 bytes

TAGSET

Une collection de TAGSET_ENTRIES.

    CREATE(key, n)

    :   Generate a new TAGSET using initial cryptographic key material
        of 32 bytes. The associated session identifier is provided. The
        initial number of of tags to create is specified; this is
        generally 0 or 1 for an outgoing session. LAST_INDEX = -1
        EXTEND(n) is called.

    EXTEND(n)

    :   Generate n more TAGSET_ENTRIES by calling EXTEND() n times.

    EXTEND()

    :   Generate one more TAGSET_ENTRY, unless the maximum number
        SESSION_TAGS have already been generated. If LAST_INDEX is
        greater than or equal to 65535, return. ++ LAST_INDEX Create a
        new TAGSET_ENTRY with the LAST_INDEX value and the calculated
        SESSION_TAG. Calls RATCHET_TAG() and (optionally) RATCHET_KEY().
        For inbound sessions, the calculation of the SESSION_KEY may be
        deferred and calculated in GET_SESSION_KEY(). Calls EXPIRE()

    EXPIRE()

    :   Remove tags and keys that are too old, or if the TAGSET size
        exceeds some limit.

    RATCHET_TAG()

    :   Calculates the next SESSION_TAG based on the last SESSION_TAG.

    RATCHET_KEY()

    :   Calculates the next SESSION_KEY based on the last SESSION_KEY.

    SESSION

    :   The associated session.

    CREATION_TIME

    :   When the TAGSET was created.

    LAST_INDEX

    :   The last TAGSET_ENTRY INDEX generated by EXTEND().

    GET_NEXT_ENTRY()

    :   Used for outgoing sessions only. EXTEND(1) is called if there
        are no remaining TAGSET_ENTRIES. If EXTEND(1) did nothing, the
        max of 65535 TAGSETS have been used, and return an error.
        Returns the next unused TAGSET_ENTRY.

    GET_SESSION_KEY(sessionTag)

    :   Used for incoming sessions only. Returns the TAGSET_ENTRY
        containing the sessionTag. If found, the TAGSET_ENTRY is
        removed. If the SESSION_KEY calculation was deferred, it is
        calculated now. If there are few TAGSET_ENTRIES remaining,
        EXTEND(n) is called.

#### 4a) DH Ratchet

Ratchets mais pas aussi rapidement que Signal. Nous séparons l'accusé de réception de la clé reçue de la génération de la nouvelle clé. Dans un usage typique, Alice et Bob vont chacun faire un ratchet (deux fois) immédiatement dans une Nouvelle Session, mais ne feront plus de ratchet par la suite.

Notez qu'un ratchet est pour une seule direction, et génère une chaîne de ratchet New Session tag / clé de message pour cette direction. Pour générer des clés pour les deux directions, vous devez faire un ratchet deux fois.

Vous effectuez un ratchet à chaque fois que vous générez et envoyez une nouvelle clé. Vous effectuez un ratchet à chaque fois que vous recevez une nouvelle clé.

Alice effectue un ratchet une fois lors de la création d'une session sortante non liée, elle ne crée pas de session entrante (non liée signifie non-répondable).

Bob effectue un ratchet une fois lors de la création d'une session entrante non liée, et ne crée pas de session sortante correspondante (non liée signifie non répondable).

Alice continue d'envoyer des messages New Session (NS) à Bob jusqu'à recevoir l'un des messages New Session Reply (NSR) de Bob. Elle utilise ensuite les résultats KDF de la Section Payload du NSR comme entrées pour les ratchets de session (voir DH Ratchet KDF), et commence à envoyer des messages Existing Session (ES).

Pour chaque message NS reçu, Bob crée une nouvelle session entrante, en utilisant les résultats KDF de la section Payload de réponse comme entrées pour le nouveau DH Ratchet ES entrant et sortant.

Pour chaque réponse requise, Bob envoie à Alice un message NSR avec la réponse dans la charge utile. Il est obligatoire que Bob utilise de nouvelles clés éphémères pour chaque NSR.

Bob doit recevoir un message ES d'Alice sur l'une des sessions entrantes, avant de créer et d'envoyer des messages ES sur la session sortante correspondante.

Alice devrait utiliser un minuteur pour recevoir un message NSR de Bob. Si le minuteur expire, la session devrait être supprimée.

Pour éviter une attaque KCI et/ou d'épuisement des ressources, où un attaquant supprime les réponses NSR de Bob pour maintenir Alice en envoi de messages NS, Alice devrait éviter de démarrer de nouvelles sessions vers Bob après un certain nombre de tentatives dues à l'expiration du temporisateur.

Alice et Bob effectuent chacun un ratchet DH pour chaque bloc NextKey reçu.

Alice et Bob génèrent chacun de nouveaux ratchets d'ensembles de balises et deux ratchets de clés symétriques après chaque ratchet DH. Pour chaque nouveau message ES dans une direction donnée, Alice et Bob font progresser les ratchets de balise de session et de clé symétrique.

La fréquence des ratchets DH après la négociation initiale dépend de l'implémentation. Bien que le protocole place une limite de 65535 messages avant qu'un ratchet soit requis, un ratcheting plus fréquent (basé sur le nombre de messages, le temps écoulé, ou les deux) peut fournir une sécurité supplémentaire.

Après le KDF de handshake final sur les sessions liées, Bob et Alice doivent exécuter la fonction Noise Split() sur le CipherState résultant pour créer des clés symétriques et de chaîne de tags indépendantes pour les sessions entrantes et sortantes.

##### IDS DE CLÉS ET D'ENSEMBLES D'ÉTIQUETTES

Les numéros d'identification des clés et des ensembles de tags sont utilisés pour identifier les clés et les ensembles de tags. Les ID de clés sont utilisés dans les blocs NextKey pour identifier la clé envoyée ou utilisée. Les ID d'ensembles de tags sont utilisés (avec le numéro de message) dans les blocs ACK pour identifier le message accusé de réception. Les ID de clés et d'ensembles de tags s'appliquent aux ensembles de tags pour une seule direction. Les numéros d'identification des clés et des ensembles de tags doivent être séquentiels.

Dans les premiers ensembles de tags utilisés pour une session dans chaque direction, l'ID de l'ensemble de tags est 0. Aucun bloc NextKey n'a été envoyé, il n'y a donc pas d'ID de clé.

Pour commencer un DH ratchet, l'expéditeur transmet un nouveau bloc NextKey avec un ID de clé de 0. Le récepteur répond avec un nouveau bloc NextKey avec un ID de clé de 0. L'expéditeur commence alors à utiliser un nouveau jeu de tags avec un ID de jeu de tags de 1.

Les ensembles d'étiquettes suivants sont générés de manière similaire. Pour tous les ensembles d'étiquettes utilisés après les échanges NextKey, le numéro de l'ensemble d'étiquettes est (1 + ID de clé d'Alice + ID de clé de Bob).

Les ID d'ensemble de clés et d'étiquettes commencent à 0 et s'incrémentent séquentiellement. L'ID maximum d'ensemble d'étiquettes est 65535. L'ID maximum de clé est 32767. Lorsqu'un ensemble d'étiquettes est presque épuisé, l'expéditeur de l'ensemble d'étiquettes doit initier un échange NextKey. Lorsque l'ensemble d'étiquettes 65535 est presque épuisé, l'expéditeur de l'ensemble d'étiquettes doit initier une nouvelle session en envoyant un message New Session.

Avec une taille maximale de message en streaming de 1730, et en supposant aucune retransmission, le transfert de données théorique maximum utilisant un seul ensemble de balises est de 1730 * 65536 ~= 108 MB. Le maximum réel sera plus faible en raison des retransmissions.

Le transfert de données théorique maximum avec tous les 65536 ensembles de tags disponibles, avant que la session doive être supprimée et remplacée, est de 64K * 108 MB ~= 6,9 TB.

##### FLUX DE MESSAGES DH RATCHET

Le prochain échange de clés pour un jeu de balises doit être initié par l'expéditeur de ces balises (le propriétaire du jeu de balises sortant). Le destinataire (propriétaire du jeu de balises entrant) répondra. Pour un trafic HTTP GET typique au niveau de la couche application, Bob enverra plus de messages et effectuera le ratchet en premier en initiant l'échange de clés ; le diagramme ci-dessous le montre. Quand Alice effectue le ratchet, la même chose se produit en sens inverse.

Le premier ensemble de tags utilisé après la négociation NS/NSR est l'ensemble de tags 0. Lorsque l'ensemble de tags 0 est presque épuisé, de nouvelles clés doivent être échangées dans les deux directions pour créer l'ensemble de tags 1. Après cela, une nouvelle clé n'est envoyée que dans une seule direction.

Pour créer l'ensemble de tags 2, l'expéditeur de tags envoie une nouvelle clé et le récepteur de tags envoie l'ID de son ancienne clé comme accusé de réception. Les deux côtés effectuent un DH.

Pour créer le jeu de tags 3, l'expéditeur de tag envoie l'ID de son ancienne clé et demande une nouvelle clé au récepteur de tag. Les deux parties effectuent un DH.

Les ensembles de balises suivants sont générés comme pour les ensembles de balises 2 et 3. Le numéro d'ensemble de balises est (1 + ID de clé expéditeur + ID de clé destinataire).

```
Tag Sender                    Tag Receiver

                 ... use tag set #0 ...


(Tagset #0 almost empty)
(generate new key #0)

Next Key, forward, request reverse, with key #0  -------->
(repeat until next key received)

                            (generate new key #0, do DH, create IB Tagset #1)

        <-------------      Next Key, reverse, with key #0
                            (repeat until tag received on new tagset)

(do DH, create OB Tagset #1)


                 ... use tag set #1 ...


(Tagset #1 almost empty)
(generate new key #1)

Next Key, forward, with key #1        -------->
(repeat until next key received)

                            (reuse key #0, do DH, create IB Tagset #2)

        <--------------     Next Key, reverse, id 0
                            (repeat until tag received on new tagset)

(do DH, create OB Tagset #2)


                 ... use tag set #2 ...


(Tagset #2 almost empty)
(reuse key #1)

Next Key, forward, request reverse, id 1  -------->
(repeat until next key received)

                            (generate new key #1, do DH, create IB Tagset #3)

        <--------------     Next Key, reverse, with key #1

(do DH, create OB Tagset #3)
(reuse key #1, do DH, create IB Tagset #3)



                 ... use tag set #3 ...



     After tag set 3, repeat the above
     patterns as shown for tag sets 2 and 3.

     To create a new even-numbered tag set, the sender sends a new key
     to the receiver. The receiver sends his old key ID
     back as an acknowledgement.

     To create a new odd-numbered tag set, the sender sends a reverse request
     to the receiver. The receiver sends a new reverse key to the sender.
```
Une fois que le ratchet DH est terminé pour un jeu de tags sortant, et qu'un nouveau jeu de tags sortant est créé, il devrait être utilisé immédiatement, et l'ancien jeu de tags sortant peut être supprimé.

Une fois que le DH ratchet est terminé pour un tagset entrant et qu'un nouveau tagset entrant est créé, le récepteur doit écouter les tags dans les deux tagsets et supprimer l'ancien tagset après un court délai, environ 3 minutes.

Le résumé de la progression de l'ensemble de balises et de l'ID de clé est dans le tableau ci-dessous. * indique qu'une nouvelle clé est générée.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">New Tag Set ID</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Sender key ID</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Rcvr key ID</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">n/a</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">n/a</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 *</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 *</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 *</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 *</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2 *</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2 *</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">...</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">...</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">...</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">65534</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32767 *</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32766</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">65535</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32767</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32767 *</td>
</tr>
</table>
Les numéros d'ID des ensembles de clés et d'étiquettes doivent être séquentiels.

##### KDF D'INITIALISATION DH

Ceci est la définition de DH_INITIALIZE(rootKey, k) pour une seule direction. Elle crée un ensemble de tags et une "clé racine suivante" à utiliser pour un ratchet DH ultérieur si nécessaire.

Nous utilisons l'initialisation DH à trois endroits. Premièrement, nous l'utilisons pour générer un ensemble de balises pour les New Session Replies. Deuxièmement, nous l'utilisons pour générer deux ensembles de balises, un pour chaque direction, à utiliser dans les messages Existing Session. Enfin, nous l'utilisons après un DH Ratchet pour générer un nouvel ensemble de balises dans une seule direction pour des messages Existing Session supplémentaires.

```
Inputs:
1) rootKey = chainKey from Payload Section
2) k from the New Session KDF or split()

// KDF_RK(rk, dh_out)
keydata = HKDF(rootKey, k, "KDFDHRatchetStep", 64)

// Output 1: The next Root Key (KDF input for the next DH ratchet)
nextRootKey = keydata[0:31]
// Output 2: The chain key to initialize the new
// session tag and symmetric key ratchets
// for the tag set
ck = keydata[32:63]

// session tag and symmetric key chain keys
keydata = HKDF(ck, ZEROLEN, "TagAndKeyGenKeys", 64)
sessTag_ck = keydata[0:31]
symmKey_ck = keydata[32:63]
```
##### DH RATCHET KDF

Ceci est utilisé après l'échange de nouvelles clés DH dans les blocs NextKey, avant qu'un tagset soit épuisé.

```
// Tag sender generates new X25519 ephemeral keys
// and sends rapk to tag receiver in a NextKey block
rask = GENERATE_PRIVATE()
rapk = DERIVE_PUBLIC(rask)

// Tag receiver generates new X25519 ephemeral keys
// and sends rbpk to Tag sender in a NextKey block
rbsk = GENERATE_PRIVATE()
rbpk = DERIVE_PUBLIC(rbsk)

sharedSecret = DH(rask, rbpk) = DH(rbsk, rapk)
tagsetKey = HKDF(sharedSecret, ZEROLEN, "XDHRatchetTagSet", 32)
rootKey = nextRootKey // from previous tagset in this direction
newTagSet = DH_INITIALIZE(rootKey, tagsetKey)
```
#### 4b) Session Tag Ratchet

Ratchets pour chaque message, comme dans Signal. Le ratchet de balise de session est synchronisé avec le ratchet de clé symétrique, mais le ratchet de clé de réception peut "prendre du retard" pour économiser la mémoire.

L'émetteur effectue un ratchet une fois pour chaque message transmis. Aucune balise supplémentaire ne doit être stockée. L'émetteur doit également conserver un compteur pour 'N', le numéro de message du message dans la chaîne actuelle. La valeur 'N' est incluse dans le message envoyé. Voir la définition du bloc Message Number.

Le récepteur doit faire avancer le ratchet de la taille maximale de la fenêtre et stocker les tags dans un "ensemble de tags", qui est associé à la session. Une fois reçu, le tag stocké peut être supprimé, et s'il n'y a pas de tags précédents non reçus, la fenêtre peut être avancée. Le récepteur devrait conserver la valeur 'N' associée à chaque tag de session, et vérifier que le numéro dans le message envoyé correspond à cette valeur. Voir la définition du bloc Message Number.

##### KDF

Ceci est la définition de RATCHET_TAG().

```
Inputs:
1) Session Tag Chain key sessTag_ck
   First time: output from DH ratchet
   Subsequent times: output from previous session tag ratchet

Generated:
2) input_key_material = SESSTAG_CONSTANT
   Must be unique for this tag set (generated from chain key),
   so that the sequence isn't predictable, since session tags
   go out on the wire in plaintext.

Outputs:
1) N (the current session tag number)
2) the session tag (and symmetric key, probably)
3) the next Session Tag Chain Key (KDF input for the next session tag ratchet)

Initialization:
keydata = HKDF(sessTag_ck, ZEROLEN, "STInitialization", 64)
// Output 1: Next chain key
sessTag_chainKey = keydata[0:31]
// Output 2: The constant
SESSTAG_CONSTANT = keydata[32:63]

// KDF_ST(ck, constant)
keydata_0 = HKDF(sessTag_chainkey, SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
// Output 1: Next chain key
sessTag_chainKey_0 = keydata_0[0:31]
// Output 2: The session tag
// or more if tag is longer than 8 bytes
tag_0 = keydata_0[32:39]

// repeat as necessary to get to tag_n
keydata_n = HKDF(sessTag_chainKey_(n-1), SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
// Output 1: Next chain key
sessTag_chainKey_n = keydata_n[0:31]
// Output 2: The session tag
// or more if tag is longer than 8 bytes
tag_n = keydata_n[32:39]
```
#### 4c) Ratchet de clé symétrique

Ratchets pour chaque message, comme dans Signal. Chaque clé symétrique a un numéro de message et une étiquette de session associés. Le ratchet de clé de session est synchronisé avec le ratchet d'étiquette symétrique, mais le ratchet de clé de réception peut "prendre du retard" pour économiser la mémoire.

Le transmetteur effectue un cliquet une fois pour chaque message transmis. Aucune clé supplémentaire ne doit être stockée.

Lorsque le destinataire reçoit une étiquette de session, s'il n'a pas encore fait progresser le cliquet de clé symétrique jusqu'à la clé associée, il doit "rattraper" la clé associée. Le destinataire mettra probablement en cache les clés pour toutes les étiquettes précédentes qui n'ont pas encore été reçues. Une fois reçues, la clé stockée peut être supprimée, et s'il n'y a pas d'étiquettes précédentes non reçues, la fenêtre peut être avancée.

Pour des raisons d'efficacité, les ratchets de session tag et de clé symétrique sont séparés afin que le ratchet de session tag puisse prendre de l'avance sur le ratchet de clé symétrique. Cela fournit également une sécurité supplémentaire, puisque les session tags sont transmis sur le réseau.

##### KDF

Voici la définition de RATCHET_KEY().

```
Inputs:
1) Symmetric Key Chain key symmKey_ck
   First time: output from DH ratchet
   Subsequent times: output from previous symmetric key ratchet

Generated:
2) input_key_material = SYMMKEY_CONSTANT = ZEROLEN
   No need for uniqueness. Symmetric keys never go out on the wire.
   TODO: Set a constant anyway?

Outputs:
1) N (the current session key number)
2) the session key
3) the next Symmetric Key Chain Key (KDF input for the next symmetric key ratchet)

// KDF_CK(ck, constant)
SYMMKEY_CONSTANT = ZEROLEN
// Output 1: Next chain key
keydata_0 = HKDF(symmKey_ck, SYMMKEY_CONSTANT, "SymmetricRatchet", 64)
symmKey_chainKey_0 = keydata_0[0:31]
// Output 2: The symmetric key
k_0 = keydata_0[32:63]

// repeat as necessary to get to k[n]
keydata_n = HKDF(symmKey_chainKey_(n-1), SYMMKEY_CONSTANT, "SymmetricRatchet", 64)
// Output 1: Next chain key
symmKey_chainKey_n = keydata_n[0:31]
// Output 2: The symmetric key
k_n = keydata_n[32:63]
```
### 5) Charge utile

Ceci remplace le format de section AES défini dans la spécification ElGamal/AES+SessionTags.

Cela utilise le même format de bloc que celui défini dans la spécification [NTCP2](/docs/specs/ntcp2/). Les types de blocs individuels sont définis différemment.

Il existe des préoccupations selon lesquelles encourager les implémenteurs à partager du code pourrait entraîner des problèmes d'analyse syntaxique. Les implémenteurs doivent soigneusement considérer les avantages et les risques du partage de code, et s'assurer que les règles d'ordonnancement et de blocs valides sont différentes pour les deux contextes.

#### Section de charge utile Données déchiffrées

La longueur chiffrée correspond au reste des données. La longueur déchiffrée est inférieure de 16 à la longueur chiffrée. Tous les types de blocs sont pris en charge. Le contenu typique comprend les blocs suivants :

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Payload Block Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type Number</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Block Length</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">DateTime</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Termination (TBD)</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">9 typ.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Options (TBD)</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">21+</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Message Number (TBD)</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">TBD</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Next Key</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3 or 35</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">ACK</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">8</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4 typ.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">ACK Request</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">9</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Garlic Clove</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">varies</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Padding</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">254</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">varies</td>
</tr>
</table>
#### Données non chiffrées

Il y a zéro ou plusieurs blocs dans la trame chiffrée. Chaque bloc contient un identifiant d'un octet, une longueur de deux octets, et zéro ou plusieurs octets de données.

Pour l'extensibilité, les récepteurs DOIVENT ignorer les blocs avec des numéros de type inconnus, et les traiter comme du remplissage.

Les données chiffrées font au maximum 65535 octets, incluant un en-tête d'authentification de 16 octets, donc les données non chiffrées font au maximum 65519 octets.

(Tag d'authentification Poly1305 non affiché) :

```
+----+----+----+----+----+----+----+----+
|blk |  size   |       data             |
+----+----+----+                        +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
|blk |  size   |       data             |
+----+----+----+                        +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
~               .   .   .               ~

blk :: 1 byte
       0 datetime
       1-3 reserved
       4 termination
       5 options
       6 previous message number
       7 next session key
       8 ack
       9 ack request
       10 reserved
       11 Garlic Clove
       224-253 reserved for experimental features
       254 for padding
       255 reserved for future extension
size :: 2 bytes, big endian, size of data to follow, 0 - 65516
data :: the data

Maximum ChaChaPoly frame is 65535 bytes.
Poly1305 tag is 16 bytes
Maximum total block size is 65519 bytes
Maximum single block size is 65519 bytes
Block type is 1 byte
Block length is 2 bytes
Maximum single block data size is 65516 bytes.
```
#### Règles d'ordonnancement des blocs

Dans le message New Session, le bloc DateTime est requis et doit être le premier bloc.

Autres blocs autorisés :

- Garlic Clove (type 11)
- Options (type 5)
- Padding (type 254)

Dans le message New Session Reply, aucun bloc n'est requis.

Autres blocs autorisés :

- Garlic Clove (type 11)
- Options (type 5)
- Padding (type 254)

Aucun autre bloc n'est autorisé. Le remplissage, s'il est présent, doit être le dernier bloc.

Dans le message de session existante, aucun bloc n'est requis, et l'ordre n'est pas spécifié, à l'exception des exigences suivantes :

La terminaison, si présente, doit être le dernier bloc à l'exception du remplissage. Le remplissage, s'il est présent, doit être le dernier bloc.

Il peut y avoir plusieurs blocs Garlic Clove dans une seule trame. Il peut y avoir jusqu'à deux blocs Next Key dans une seule trame. Plusieurs blocs Padding ne sont pas autorisés dans une seule trame. Les autres types de blocs n'auront probablement pas plusieurs blocs dans une seule trame, mais cela n'est pas interdit.

#### DateTime

Une expiration. Aide à la prévention de la rejouabilité. Bob doit valider que le message est récent, en utilisant cet horodatage. Bob doit implémenter un filtre de Bloom ou un autre mécanisme pour prévenir les attaques par rejeu, si l'heure est valide. Bob peut également utiliser une vérification de détection de rejeu antérieure pour une clé éphémère dupliquée (soit pré- soit post-décodage Elligator2) pour détecter et supprimer les messages NS dupliqués récents avant le déchiffrement. Généralement inclus uniquement dans les messages New Session.

```
+----+----+----+----+----+----+----+
| 0  |    4    |     timestamp     |
+----+----+----+----+----+----+----+

blk :: 0
size :: 2 bytes, big endian, value = 4
timestamp :: Unix timestamp, unsigned seconds.
             Wraps around in 2106
```
#### Gousse de Garlic

Un seul Garlic Clove déchiffré tel que spécifié dans [I2NP](/docs/specs/i2np/), avec des modifications pour supprimer les champs inutilisés ou redondants. Attention : Ce format est significativement différent de celui pour ElGamal/AES. Chaque clove est un bloc de charge utile séparé. Les Garlic Cloves ne peuvent pas être fragmentés entre les blocs ou entre les trames ChaChaPoly.

```
+----+----+----+----+----+----+----+----+
| 11 |  size   |                        |
+----+----+----+                        +
|      Delivery Instructions            |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|type|  Message_ID       | Expiration   
+----+----+----+----+----+----+----+----+
     |      I2NP Message body           |
+----+                                  +
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

size :: size of all data to follow

Delivery Instructions :: As specified in
       the Garlic Clove section of [I2NP]_.
       Length varies but is typically 1, 33, or 37 bytes

type :: I2NP message type

Message_ID :: 4 byte `Integer` I2NP message ID

Expiration :: 4 bytes, seconds since the epoch
```
Notes :

- Les implémenteurs doivent s'assurer que lors de la lecture d'un bloc, des données malformées ou malveillantes ne provoqueront pas de débordements de lecture dans le bloc suivant.
- Le format Clove Set spécifié dans [I2NP](/docs/specs/i2np/) n'est pas utilisé. Chaque clove est contenu dans son propre bloc.
- L'en-tête du message I2NP fait 9 octets, avec un format identique à celui utilisé dans [NTCP2](/docs/specs/ntcp2/).
- Le Certificate, l'ID du message et l'Expiration de la définition du Garlic Message dans [I2NP](/docs/specs/i2np/) ne sont pas inclus.
- Le Certificate, l'ID du Clove et l'Expiration de la définition du Garlic Clove dans [I2NP](/docs/specs/i2np/) ne sont pas inclus.

#### Terminaison

L'implémentation est optionnelle. Abandonner la session. Ceci doit être le dernier bloc non-rembourré dans la trame. Aucun autre message ne sera envoyé dans cette session.

Non autorisé dans NS ou NSR. Inclus uniquement dans les messages de session existante.

```
+----+----+----+----+----+----+----+----+
| 4  |  size   | rsn|     addl data     |
+----+----+----+----+                   +
~               .   .   .               ~
+----+----+----+----+----+----+----+----+

blk :: 4
size :: 2 bytes, big endian, value = 1 or more
rsn :: reason, 1 byte:
       0: normal close or unspecified
       1: termination received
       others: optional, impementation-specific
addl data :: optional, 0 or more bytes, for future expansion, debugging,
             or reason text.
             Format unspecified and may vary based on reason code.
```
#### Options

NON IMPLÉMENTÉ, à étudier ultérieurement. Transmet les options mises à jour. Les options incluent divers paramètres pour la session. Voir la section Analyse de la longueur des étiquettes de session ci-dessous pour plus d'informations.

Le bloc d'options peut avoir une longueur variable, car more_options peut être présent.

```
+----+----+----+----+----+----+----+----+
| 5  |  size   |ver |flg |STL |STimeout |
+----+----+----+----+----+----+----+----+
|  SOTW   |  RITW   |tmin|tmax|rmin|rmax|
+----+----+----+----+----+----+----+----+
|  tdmy   |  rdmy   |  tdelay |  rdelay |
+----+----+----+----+----+----+----+----+
|              more_options             |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

blk :: 5
size :: 2 bytes, big endian, size of options to follow, 21 bytes minimum
ver :: Protocol version, must be 0
flg :: 1 byte flags
       bits 7-0: Unused, set to 0 for future compatibility
STL :: Session tag length (must be 8), other values unimplemented
STimeout :: Session idle timeout (seconds), big endian
SOTW :: Sender Outbound Tag Window, 2 bytes big endian
RITW :: Receiver Inbound Tag Window 2 bytes big endian

tmin, tmax, rmin, rmax :: requested padding limits
    tmin and rmin are for desired resistance to traffic analysis.
    tmax and rmax are for bandwidth limits.
    tmin and tmax are the transmit limits for the router sending this options block.
    rmin and rmax are the receive limits for the router sending this options block.
    Each is a 4.4 fixed-point float representing 0 to 15.9375
    (or think of it as an unsigned 8-bit integer divided by 16.0).
    This is the ratio of padding to data. Examples:
    Value of 0x00 means no padding
    Value of 0x01 means add 6 percent padding
    Value of 0x10 means add 100 percent padding
    Value of 0x80 means add 800 percent (8x) padding
    Alice and Bob will negotiate the minimum and maximum in each direction.
    These are guidelines, there is no enforcement.
    Sender should honor receiver's maximum.
    Sender may or may not honor receiver's minimum, within bandwidth constraints.

tdmy: Max dummy traffic willing to send, 2 bytes big endian, bytes/sec average
rdmy: Requested dummy traffic, 2 bytes big endian, bytes/sec average
tdelay: Max intra-message delay willing to insert, 2 bytes big endian, msec average
rdelay: Requested intra-message delay, 2 bytes big endian, msec average

more_options :: Format undefined, for future use
```
SOTW est la recommandation de l'expéditeur au destinataire pour la fenêtre de tags entrants du destinataire (l'anticipation maximale). RITW est la déclaration de l'expéditeur concernant la fenêtre de tags entrants (anticipation maximale) qu'il prévoit d'utiliser. Chaque côté définit ou ajuste ensuite l'anticipation basée sur un calcul de minimum, maximum ou autre.

Notes :

- Le support pour une longueur de balise de session non-par défaut ne sera heureusement jamais requis.
- La fenêtre de balise est MAX_SKIP dans la documentation Signal.

Problèmes :

- La négociation des options reste à définir.
- Les valeurs par défaut restent à définir.
- Les options de remplissage et de délai sont copiées depuis NTCP2, mais ces options n'ont pas été entièrement implémentées ou étudiées là-bas.

#### Numéros de Message

L'implémentation est optionnelle. La longueur (nombre de messages envoyés) dans le jeu d'étiquettes précédent (PN). Le récepteur peut immédiatement supprimer les étiquettes supérieures à PN du jeu d'étiquettes précédent. Le récepteur peut faire expirer les étiquettes inférieures ou égales à PN du jeu d'étiquettes précédent après un court délai (par exemple 2 minutes).

```
+----+----+----+----+----+
| 6  |  size   |  PN    |
+----+----+----+----+----+

blk :: 6
size :: 2
PN :: 2 bytes big endian. The index of the last tag sent in the previous tag set.
```
Remarques :

- Le PN maximum est 65535.
- Les définitions de PN sont égales à la définition Signal, moins un.
  Ceci est similaire à ce que fait Signal, mais dans Signal, PN et N sont dans
  l'en-tête. Ici, ils sont dans le corps du message chiffré.
- Ne pas envoyer ce bloc dans le tag set 0, car il n'y avait pas de tag
  set précédent.

#### Clé publique du prochain cliquet DH

La prochaine clé de ratchet DH est dans la charge utile, et elle est optionnelle. Nous ne faisons pas de ratchet à chaque fois. (Ceci est différent de Signal, où elle se trouve dans l'en-tête et est envoyée à chaque fois)

Pour le premier ratchet, Key ID = 0.

Non autorisé dans NS ou NSR. Inclus uniquement dans les messages de Session Existante.

```
+----+----+----+----+----+----+----+----+
| 7  |  size   |flag|  key ID |         |
+----+----+----+----+----+----+         +
|                                       |
+                                       +
|     Next DH Ratchet Public Key        |
+                                       +
|                                       |
+                             +----+----+
|                             |
+----+----+----+----+----+----+

blk :: 7
size :: 3 or 35
flag :: 1 byte flags
        bit order: 76543210
        bit 0: 1 for key present, 0 for no key present
        bit 1: 1 for reverse key, 0 for forward key
        bit 2: 1 to request reverse key, 0 for no request
               only set if bit 1 is 0
        bits 7-2: Unused, set to 0 for future compatibility
key ID :: The key ID of this key. 2 bytes, big endian
          0 - 32767
Public Key :: The next X25519 public key, 32 bytes, little endian
              Only if bit 0 is 1
```
Notes :

- L'ID de clé est un compteur incrémental pour la clé locale utilisée pour cet ensemble de tags, commençant à 0.
- L'ID ne doit pas changer sauf si la clé change.
- Ce n'est peut-être pas strictement nécessaire, mais c'est utile pour le débogage. Signal n'utilise pas d'ID de clé.
- L'ID de clé maximum est 32767.
- Dans le rare cas où les ensembles de tags dans les deux directions effectuent un ratcheting en même temps, une trame contiendra deux blocs Next Key, un pour la clé avant et un pour la clé arrière.
- Les numéros d'ID de clé et d'ensemble de tags doivent être séquentiels.
- Voir la section DH Ratchet ci-dessus pour les détails.

#### Accusé de réception

Ceci n'est envoyé que si un bloc de demande d'accusé de réception a été reçu. Plusieurs accusés de réception peuvent être présents pour accuser réception de plusieurs messages.

Non autorisé dans NS ou NSR. Inclus uniquement dans les messages de session existante.

```
+----+----+----+----+----+----+----+----+
| 8  |  size   |tagsetid |   N     |    |
+----+----+----+----+----+----+----+    +
|             more acks                 |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

blk :: 8
size :: 4 * number of acks to follow, minimum 1 ack
for each ack:
tagsetid :: 2 bytes, big endian, from the message being acked
N :: 2 bytes, big endian, from the message being acked
```
Notes :

- L'ID du jeu de tags et N identifient de manière unique le message accusé réception.
- Dans les premiers jeux de tags utilisés pour une session dans chaque direction, l'ID du jeu de tags est 0.
- Aucun bloc NextKey n'a été envoyé, il n'y a donc pas d'ID de clé.
- Pour tous les jeux de tags utilisés après les échanges NextKey, le numéro du jeu de tags est (1 + ID de clé d'Alice + ID de clé de Bob).

#### Demande d'acquittement

Demander un accusé de réception intégré. Pour remplacer le message DeliveryStatus hors-bande dans le Garlic Clove.

Si un accusé de réception explicite est demandé, l'ID du tagset actuel et le numéro de message (N) sont retournés dans un bloc d'accusé de réception.

Non autorisé dans NS ou NSR. Inclus uniquement dans les messages de Session Existante.

```
+----+----+----+----+
|  9 |  size   |flg |
+----+----+----+----+

blk :: 9
size :: 1
flg :: 1 byte flags
       bits 7-0: Unused, set to 0 for future compatibility
```
#### Remplissage

Tout le remplissage se trouve à l'intérieur des trames AEAD. TODO Le remplissage à l'intérieur d'AEAD devrait approximativement respecter les paramètres négociés. TODO Alice a envoyé ses paramètres min/max tx/rx demandés dans le message NS. TODO Bob a envoyé ses paramètres min/max tx/rx demandés dans le message NSR. Les options mises à jour peuvent être envoyées pendant la phase de données. Voir les informations du bloc d'options ci-dessus.

Si présent, ceci doit être le dernier bloc dans la trame.

```
+----+----+----+----+----+----+----+----+
|254 |  size   |      padding           |
+----+----+----+                        +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

blk :: 254
size :: 2 bytes, big endian, 0-65516
padding :: zeros or random data
```
Notes :

- Le bourrage tout-zéro est acceptable, car il sera chiffré.
- Les stratégies de bourrage sont à définir.
- Les trames contenant uniquement du bourrage sont autorisées.
- Le bourrage par défaut est de 0-15 octets.
- Voir le bloc d'options pour la négociation des paramètres de bourrage
- Voir le bloc d'options pour les paramètres de bourrage min/max
- La réponse du router en cas de violation du bourrage négocié dépend de
  l'implémentation.

#### Autres types de blocs

Les implémentations devraient ignorer les types de blocs inconnus pour assurer la compatibilité ascendante.

#### Travaux futurs

- La longueur de padding doit soit être décidée message par message avec des estimations de la distribution des longueurs, soit des délais aléatoires doivent être ajoutés. Ces contre-mesures doivent être incluses pour résister à la DPI, car les tailles de messages révéleraient sinon que du trafic I2P est transporté par le protocole de transport. Le schéma exact de padding est un domaine de travail futur, l'Annexe A fournit plus d'informations sur le sujet.

## Modèles d'utilisation typiques

### HTTP GET

Il s'agit du cas d'usage le plus typique, et la plupart des cas d'usage de streaming non-HTTP seront identiques à celui-ci également. Un petit message initial est envoyé, une réponse suit, et des messages supplémentaires sont envoyés dans les deux directions.

Une requête HTTP GET tient généralement dans un seul message I2NP. Alice envoie une petite requête avec un seul nouveau message Session, incluant un leaseset de réponse. Alice inclut un ratchet immédiat vers une nouvelle clé. Inclut une signature pour lier à la destination. Aucun accusé de réception demandé.

Bob effectue un ratchet immédiatement.

Alice effectue immédiatement la rotation des clés.

Continue avec ces sessions.

```
Alice                           Bob

  New Session (1b)     ------------------->
  with ephemeral key 1
  with static key for binding
  with next key
  with bundled HTTP GET
  with bundled LS
  without bundled Delivery Status Message

  any retransmissions, same as above

  following messages may arrive in any order:

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 1
                      with bundled HTTP reply part 1

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 2
                      with bundled HTTP reply part 2

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 3
                      with bundled HTTP reply part 3

  After reception of any of these messages,
  Alice switches to use Existing Session messages,
  creates a new inbound + outbound session pair,
  and ratchets.


  Existing Session     ------------------->
  with bundled streaming ack


  Existing Session     ------------------->
  with bundled streaming ack


  After reception of any of these messages,
  Bob switches to use Existing Session messages.


  <--------------     Existing Session
                      with bundled HTTP reply part 4


  Existing Session     ------------------->
  with bundled streaming ack

  <--------------     Existing Session
                      with bundled HTTP reply part 5
```
### HTTP POST

Alice a trois options :

1)  Envoyer seulement le premier message (taille de fenêtre = 1), comme dans HTTP GET. Pas

    recommended.
2)  Envoyer jusqu'à la fenêtre de streaming, mais en utilisant le même encodage Elligator2

    cleartext public key. All messages contain same next public key
    (ratchet). This will be visible to OBGW/IBEP because they all start
    with the same cleartext. Things proceed as in 1). Not recommended.
3)  Implémentation recommandée. Envoyer jusqu'à la fenêtre de streaming, mais en utilisant un

    different Elligator2-encoded cleartext public key (session) for
    each. All messages contain same next public key (ratchet). This will
    not be visible to OBGW/IBEP because they all start with different
    cleartext. Bob must recognize that they all contain the same next
    public key, and respond to all with the same ratchet. Alice uses
    that next public key and continues.

Flux de messages Option 3 :

```
Alice                           Bob

  New Session (1b)     ------------------->
  with ephemeral key 1
  with static key for binding
  with bundled HTTP POST part 1
  with bundled LS
  without bundled Delivery Status Message


  New Session (1b)     ------------------->
  with ephemeral key 2
  with static key for binding
  with bundled HTTP POST part 2
  with bundled LS
  without bundled Delivery Status Message


  New Session (1b)     ------------------->
  with ephemeral key 3
  with static key for binding
  with bundled HTTP POST part 3
  with bundled LS
  without bundled Delivery Status Message


  following messages can arrive in any order:

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 1
                      with bundled streaming ack

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key 2
                      with bundled streaming ack

  After reception of any of these messages,
  Alice switches to use Existing Session messages,
  creates a new inbound + outbound session pair,
  and ratchets.


  following messages can arrive in any order:


  Existing Session     ------------------->
  with bundled HTTP POST part 4

  Existing Session     ------------------->
  with next key
  with bundled HTTP POST part 5


  After reception of any of these messages,
  Bob switches to use Existing Session messages.


  <--------------     Existing Session
                      with bundled streaming ack

  After reception of any of this message,
  Alice switches to use Existing Session messages,
  and Alice ratchets.


  Existing Session     ------------------->
  with next key
  with bundled HTTP POST part 4

  after reception of this message, Bob ratchets

  Existing Session     ------------------->
  with next key
  with bundled HTTP POST part 5

  <--------------     Existing Session
                      with bundled streaming ack
```
### Datagramme avec Réponse

Un seul message, avec une seule réponse attendue. Des messages ou réponses supplémentaires peuvent être envoyés.

Similaire à HTTP GET, mais avec des options plus petites pour la taille de fenêtre des balises de session et la durée de vie. Peut-être ne pas demander de cliquet.

```
Alice                           Bob

  New Session (1b)     ------------------->
  with static key for binding
  with next key
  with bundled repliable datagram
  with bundled LS
  without bundled Delivery Status Message


  <--------------     New Session Reply (1g)
                      with Bob ephemeral key
                      with bundled reply part 1

  <--------------     New Session Reply (1g)
                      with Bob ephemeral key
                      with bundled reply part 2

  After reception of either message,
  Alice switches to use Existing Session messages,
  and ratchets.

  If the Existing Session message arrives first,
  Alice ratchets on the existing inbound and outbound
  sessions.

  When the New Session Reply arrives, Alice
  sets the existing inbound session to expire,
  creates a new inbound and outbound session,
  and sends Existing Session messages on
  the new outbound session.

  Alice keeps the expiring inbound session
  around for a while to process the Existing Session
  message sent to Alice.
  If all expected original Existing Session message replies
  have been processed, Alice can expire the original
  inbound session immediately.

  if there are any other messages:

  Existing Session     ------------------->
  with bundled message

  Existing Session     ------------------->
  with bundled streaming ack

  <--------------     Existing Session
                      with bundled message
```
### Datagrammes Bruts Multiples

Plusieurs messages anonymes, sans réponses attendues.

Dans ce scénario, Alice demande une session, mais sans liaison. Un nouveau message de session est envoyé. Aucun leaseSet de réponse n'est inclus. Un DSM de réponse est inclus (c'est le seul cas d'usage qui nécessite des DSM inclus). Aucune clé suivante n'est incluse. Aucune réponse ou ratchet n'est demandé. Aucun ratchet n'est envoyé. Les options définissent la fenêtre des balises de session à zéro.

```
Alice                           Bob

  New Session (1c)     ------------------->
  with bundled message
  without bundled LS
  with bundled Delivery Status Message 1

  New Session (1c)     ------------------->
  with bundled message
  without bundled LS
  with bundled Delivery Status Message 2

  New Session (1c)     ------------------->
  with bundled message
  without bundled LS
  with bundled Delivery Status Message 3
 
  following messages can arrive in any order:

  <--------------     Delivery Status Message 1

  <--------------     Delivery Status Message 2

  <--------------     Delivery Status Message 3

  After reception of any of these messages,
  Alice switches to use Existing Session messages.

  Existing Session     ------------------->

  Existing Session     ------------------->

  Existing Session     ------------------->
```
### Datagramme brut simple

Un seul message anonyme, sans réponse attendue.

Un message à usage unique est envoyé. Aucun LS de réponse ou DSM n'est groupé. Aucune clé suivante n'est incluse. Aucune réponse ou ratchet n'est demandé. Aucun ratchet n'est envoyé. Les options définissent la fenêtre des balises de session à zéro.

```
Alice                           Bob

  One-Time Message (1d)   ------------------->
  with bundled message
  without bundled LS
  without bundled Delivery Status Message
```
### Sessions de longue durée

Les sessions de longue durée peuvent effectuer un ratchet, ou demander un ratchet, à tout moment, pour maintenir la confidentialité persistante à partir de ce moment. Les sessions doivent effectuer un ratchet lorsqu'elles approchent de la limite de messages envoyés par session (65535).

## Considérations d'implémentation

### Défense

Comme avec le protocole ElGamal/AES+SessionTag existant, les implémentations doivent limiter le stockage des balises de session et se protéger contre les attaques d'épuisement de la mémoire.

Quelques stratégies recommandées incluent :

- Limite stricte du nombre de session tags stockés
- Expiration agressive des sessions entrantes inactives en cas de pression mémoire
- Limite du nombre de sessions entrantes liées à une seule destination distante
- Réduction adaptative de la fenêtre de session tag et suppression des anciens tags inutilisés en cas de pression mémoire
- Refus de faire le ratchet lorsque demandé, si sous pression mémoire

### Paramètres

Paramètres et délais d'expiration recommandés :

- Taille du tagset NSR : 12 tsmin et tsmax
- Taille du tagset ES 0 : tsmin 24, tsmax 160
- Taille du tagset ES (1+) : 160 tsmin et tsmax
- Délai d'expiration du tagset NSR : 3 minutes pour le récepteur
- Délai d'expiration du tagset ES : 8 minutes pour l'expéditeur, 10 minutes pour le récepteur
- Supprimer le tagset ES précédent après : 3 minutes
- Anticipation du tagset pour le tag N : min(tsmax, tsmin + N/4)
- Réduction du tagset derrière le tag N : min(tsmax, tsmin + N/4) / 2
- Envoyer la clé suivante au tag : 4096
- Envoyer la clé suivante après la durée de vie du tagset : TBD
- Remplacer la session si NS reçu après : 3 minutes
- Décalage d'horloge maximum : -5 minutes à +2 minutes
- Durée du filtre de rejeu NS : 5 minutes
- Taille du padding : 0-15 octets (autres stratégies TBD)

### Classification

Voici les recommandations pour classifier les messages entrants.

#### X25519 Uniquement

Sur un tunnel qui est utilisé exclusivement avec ce protocole, effectuer l'identification comme cela se fait actuellement avec ElGamal/AES+SessionTags :

D'abord, traiter les données initiales comme une balise de session, et rechercher cette balise de session. Si elle est trouvée, déchiffrer en utilisant les données stockées associées à cette balise de session.

Si non trouvé, traiter les données initiales comme une clé publique DH et un nonce. Effectuer une opération DH et le KDF spécifié, et tenter de déchiffrer les données restantes.

#### X25519 partagé avec ElGamal/AES+SessionTags

Sur un tunnel qui prend en charge à la fois ce protocole et ElGamal/AES+SessionTags, classifiez les messages entrants comme suit :

En raison d'un défaut dans la spécification ElGamal/AES+SessionTags, le bloc AES n'est pas complété à une longueur aléatoire non-multiple de 16. Par conséquent, la longueur des messages de session existante modulo 16 est toujours 0, et la longueur des messages de nouvelle session modulo 16 est toujours 2 (puisque le bloc ElGamal fait 514 octets de long).

Si la longueur modulo 16 n'est pas 0 ou 2, traiter les données initiales comme un session tag, et rechercher le session tag. Si trouvé, déchiffrer en utilisant les données stockées associées à ce session tag.

Si non trouvé, et que la longueur mod 16 n'est pas 0 ou 2, traiter les données initiales comme une clé publique DH et un nonce. Effectuer une opération DH et le KDF spécifié, puis tenter de déchiffrer les données restantes. (en fonction du mélange de trafic relatif et des coûts relatifs des opérations DH X25519 et ElGamal, cette étape peut être effectuée en dernier à la place)

Sinon, si la longueur mod 16 est égale à 0, traiter les données initiales comme un tag de session ElGamal/AES, et rechercher ce tag de session. Si trouvé, déchiffrer en utilisant les données stockées associées à ce tag de session.

Si non trouvé, et que les données font au moins 642 (514 + 128) octets de long, et que la longueur modulo 16 est égale à 2, traiter les données initiales comme un bloc ElGamal. Tenter de déchiffrer les données restantes.

Notez que si la spécification ElGamal/AES+SessionTag est mise à jour pour permettre un rembourrage non-mod-16, les choses devront être faites différemment.

### Retransmissions et Transitions d'État

La couche ratchet ne fait pas de retransmissions, et à deux exceptions près, n'utilise pas de minuteurs pour les transmissions. Les minuteurs sont également requis pour l'expiration des tagsets.

Les minuteurs de transmission sont utilisés uniquement pour envoyer des NSR et pour répondre avec un ES lorsqu'un ES reçu contient une demande d'ACK. Le délai d'expiration recommandé est d'une seconde. Dans presque tous les cas, la couche supérieure (datagramme ou streaming) répondra, forçant un NSR ou ES, et le minuteur peut être annulé. Si le minuteur se déclenche, envoyez une charge utile vide avec le NSR ou ES.

#### Réponses de la couche Ratchet

Les implémentations initiales s'appuient sur le trafic bidirectionnel aux couches supérieures. C'est-à-dire que les implémentations supposent que le trafic dans la direction opposée sera bientôt transmis, ce qui forcera toute réponse requise au niveau de la couche ECIES.

Cependant, certains trafics peuvent être unidirectionnels ou de très faible bande passante, de sorte qu'il n'y ait pas de trafic de couche supérieure pour générer une réponse en temps opportun.

La réception de messages NS et NSR nécessite une réponse ; la réception de blocs ACK Request et Next Key nécessite également une réponse.

Les implémentations doivent démarrer un minuteur lorsqu'un de ces messages nécessitant une réponse est reçu, et générer une réponse "vide" (sans bloc Garlic Clove) au niveau de la couche ECIES si aucun trafic de retour n'est envoyé dans un court délai (par exemple 1 seconde).

Il peut également être approprié d'utiliser un délai d'expiration encore plus court pour les réponses aux messages NS et NSR, afin de basculer le trafic vers les messages ES efficaces dès que possible.

#### Liaison NS pour NSR

Au niveau de la couche ratchet, en tant que Bob, Alice n'est connue que par sa clé statique. Le message NS est authentifié (authentification de l'expéditeur [Noise](https://noiseprotocol.org/noise.html) IK 1). Cependant, cela n'est pas suffisant pour que la couche ratchet puisse envoyer quoi que ce soit à Alice, car le routage réseau nécessite une Destination complète.

Avant que le NSR puisse être envoyé, la Destination complète d'Alice doit être découverte soit par la couche ratchet soit par un protocole de couche supérieure capable de réponse, soit des [Datagrams](/docs/specs/datagrams/) avec réponse soit du [Streaming](/docs/specs/streaming/). Après avoir trouvé le leaseSet pour cette Destination, ce leaseSet contiendra la même clé statique que celle contenue dans le NS.

Typiquement, la couche supérieure répondra, forçant une recherche dans la base de données réseau du leaseSet d'Alice par le hachage de destination d'Alice. Ce leaseSet sera presque toujours trouvé localement, car le NS contenait un bloc Garlic Clove, contenant un message Database Store, contenant le leaseSet d'Alice.

Pour que Bob soit prêt à envoyer un NSR de couche ratchet, et pour lier la session en attente à la Destination d'Alice, Bob devrait "capturer" la Destination lors du traitement de la charge utile NS. Si un message Database Store est trouvé contenant un Leaseset avec une clé correspondant à la clé statique dans le NS, la session en attente est maintenant liée à cette Destination, et Bob sait où envoyer tout NSR si le minuteur de réponse expire. Il s'agit de l'implémentation recommandée.

Une conception alternative consiste à maintenir un cache ou une base de données où la clé statique est mappée vers une Destination. La sécurité et la praticité de cette approche constituent un sujet d'étude approfondie.

Ni cette spécification ni d'autres n'exigent strictement que chaque NS contienne le Leaseset d'Alice. Cependant, en pratique, cela devrait être le cas. Le délai d'expiration recommandé pour l'expéditeur du tagset ES (8 minutes) est plus court que le délai d'expiration maximum du Leaseset (10 minutes), il pourrait donc y avoir une petite fenêtre où la session précédente a expiré, Alice pense que Bob a encore son Leaseset valide, et n'envoie pas un nouveau Leaseset avec le nouveau NS. C'est un sujet qui mérite une étude plus approfondie.

#### Messages NS Multiples

Si aucune réponse NSR n'est reçue avant que la couche supérieure (datagramme ou streaming) n'envoie plus de données, éventuellement comme une retransmission, Alice doit composer un nouveau NS, en utilisant une nouvelle clé éphémère. Ne réutilisez pas la clé éphémère d'un NS précédent. Alice doit maintenir l'état de handshake supplémentaire et l'ensemble de tags de réception dérivé, pour recevoir les messages NSR en réponse à tout NSR qui a été envoyé.

Les implémentations peuvent limiter le nombre total de messages NS envoyés, ou le taux d'envoi des messages NS, soit en mettant en file d'attente soit en supprimant les messages de couche supérieure avant qu'ils ne soient envoyés.

Dans certaines situations, lors d'une charge élevée ou sous certains scénarios d'attaque, il peut être approprié pour Bob de mettre en file d'attente, d'abandonner ou de limiter les messages NS apparents sans tenter de les déchiffrer, afin d'éviter une attaque par épuisement des ressources.

Pour chaque NS reçu, Bob génère un tagset sortant NSR, envoie un NSR, effectue un split(), et génère les tagsets ES entrants et sortants. Cependant, Bob n'envoie aucun message ES jusqu'à ce que le premier message ES sur le tagset entrant correspondant soit reçu. Après cela, Bob peut supprimer tous les états de handshake et tagsets pour tout autre NS reçu ou NSR envoyé, ou les laisser expirer rapidement. N'utilisez pas les tagsets NSR pour les messages ES.

C'est un sujet d'étude supplémentaire de savoir si Bob peut choisir d'envoyer de manière spéculative des messages ES immédiatement après le NSR, même avant de recevoir le premier ES d'Alice. Dans certains scénarios et modèles de trafic, cela pourrait économiser une bande passante et du CPU considérables. Cette stratégie peut être basée sur des heuristiques telles que les modèles de trafic, le pourcentage d'ES reçus sur le tagset de la première session, ou d'autres données.

#### Multiples messages NSR

Pour chaque message NS reçu, jusqu'à ce qu'un message ES soit reçu, Bob doit répondre avec un nouveau NSR, soit en raison du trafic de couche supérieure envoyé, soit en raison de l'expiration du minuteur d'envoi NSR.

Chaque NSR utilise l'état de handshake et le tagset correspondant au NS entrant. Bob doit maintenir l'état de handshake et le tagset pour tous les messages NS reçus, jusqu'à ce qu'un message ES soit reçu.

Les implémentations peuvent limiter le nombre total de messages NSR envoyés, ou le taux d'envoi des messages NSR, soit en mettant en file d'attente soit en supprimant les messages de couche supérieure avant qu'ils ne soient envoyés. Ces limitations peuvent s'appliquer soit lorsqu'elles sont causées par des messages NS entrants, soit par du trafic sortant supplémentaire de couche supérieure.

Dans certaines situations, lors de forte charge, ou dans certains scénarios d'attaque, il peut être approprié pour Alice de mettre en file d'attente, supprimer ou limiter les messages NSR sans tenter de les déchiffrer, afin d'éviter une attaque par épuisement des ressources. Ces limites peuvent être soit totales sur toutes les sessions, par session, ou les deux.

Une fois qu'Alice reçoit un NSR, Alice effectue un split() pour dériver les clés de session ES. Alice devrait définir un minuteur et envoyer un message ES vide si la couche supérieure n'envoie aucun trafic, généralement dans la seconde.

Les autres tagsets NSR entrants peuvent être supprimés prochainement ou autorisés à expirer, mais Alice devrait les conserver pendant un court moment, pour déchiffrer tout autre message NSR qui pourrait être reçu.

### Prévention de la Rejeu

Bob doit implémenter un filtre de Bloom ou un autre mécanisme pour empêcher les attaques par rejeu NS, si le DateTime inclus est récent, et rejeter les messages NS où le DateTime est trop ancien. Bob peut également utiliser une vérification de détection de rejeu antérieure pour une clé éphémère dupliquée (avant ou après le décodage Elligator2) pour détecter et abandonner les messages NS dupliqués récents avant le déchiffrement.

Les messages NSR et ES ont une prévention intégrée contre la rejeu car la balise de session est à usage unique.

Les messages garlic disposent également d'une protection contre la rejeu si le router implémente un filtre de Bloom au niveau du router basé sur l'ID du message I2NP.

## Modifications associées

Recherches de base de données depuis les destinations ECIES : Voir [Prop154](/proposals/154-ratchet/), maintenant intégrée dans [I2NP](/docs/specs/i2np/) pour la version 0.9.46.

Cette spécification nécessite le support LS2 pour publier la clé publique X25519 avec le leaseset. Aucune modification n'est requise pour les spécifications LS2 dans [I2NP](/docs/specs/i2np/). Tout le support a été conçu, spécifié et implémenté dans [Prop123](/proposals/123-new-netdb-entries/) implémenté dans la version 0.9.38.

Cette spécification nécessite qu'une propriété soit définie dans les options I2CP pour être activée. Tout le support a été conçu, spécifié et implémenté dans [Prop123](/proposals/123-new-netdb-entries/) implémentée dans la version 0.9.38.

L'option requise pour activer ECIES est une seule propriété I2CP pour I2CP, BOB, SAM, ou i2ptunnel.

Les valeurs typiques sont i2cp.leaseSetEncType=4 pour ECIES uniquement, ou i2cp.leaseSetEncType=4,0 pour les clés doubles ECIES et ElGamal.

## Compatibilité

Tout router supportant LS2 avec des clés doubles (0.9.38 ou supérieur) devrait supporter la connexion aux destinations avec des clés doubles.

Les destinations ECIES uniquement nécessitent qu'une majorité des floodfills soit mise à jour vers la version 0.9.46 pour obtenir des réponses de recherche chiffrées. Voir [Prop154](/proposals/154-ratchet/).

Les destinations ECIES uniquement peuvent seulement se connecter avec d'autres destinations qui sont soit ECIES uniquement, soit à double clé.

## Références

- [Common](/docs/specs/common-structures/)
- [CRYPTO-ELG](/docs/specs/cryptography/#elgamal)
- [Datagrammes](/docs/specs/datagrams/)
- [ECIES-HYBRID](/docs/specs/ecies-hybrid/)
- [ElG-AES](/docs/specs/elgamal-aes/)
- [Elligator2](https://elligator.cr.yp.to/elligator-20130828.pdf) - Voir aussi [article Elligator](https://www.imperialviolet.org/2013/12/25/elligator.html) et code OBFS4
- [GARLICSPEC](/docs/overview/garlic-routing/)
- [I2CP](/docs/specs/i2cp/)
- [I2NP](/docs/specs/i2np/)
- [NOISE](https://noiseprotocol.org/noise.html)
- [NTCP2](/docs/specs/ntcp2/)
- [Prop111](/proposals/111-ntcp2/)
- [Prop123](/proposals/123-new-netdb-entries/)
- [Prop142](/proposals/142-ecies-template/)
- [Prop144](/proposals/144-ecies-x25519/)
- [Prop145](/proposals/145-ecies-ecdh-aes/)
- [Prop152](/proposals/152-ecies-config/)
- [Prop153](/proposals/153-chacha20-layer/)
- [Prop154](/proposals/154-ratchet/)
- [RFC-2104](https://tools.ietf.org/html/rfc2104)
- [RFC-4880-S5.1](https://tools.ietf.org/html/rfc4880#section-5.1)
- [RFC-5869](https://tools.ietf.org/html/rfc5869)
- [RFC-7539](https://tools.ietf.org/html/rfc7539)
- [RFC-7748](https://tools.ietf.org/html/rfc7748)
- [RFC-7905](https://tools.ietf.org/html/rfc7905)
- [Signal](https://signal.org/docs/specifications/doubleratchet/)
- [SSU](/docs/transport/ssu/)
- [SSU2](/docs/specs/ssu2/)
- [STS](https://en.wikipedia.org/wiki/Station-to-Station_protocol) - Diffie, W.; van Oorschot P. C.; Wiener M. J., Authentification et Échanges de Clés Authentifiés
- [Streaming](/docs/specs/streaming/)
