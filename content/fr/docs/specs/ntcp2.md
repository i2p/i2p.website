---
title: "Transport NTCP2"
description: "Transport TCP basé sur Noise pour les liaisons router-à-router"
slug: "ntcp2"
category: "Transports"
lastUpdated: "2026-07"
accurateFor: "0.9.70"
---

## Aperçu

NTCP2 est un protocole d'accord de clés authentifié qui améliore la résistance de [NTCP](/docs/transport/ntcp) à diverses formes d'identification automatisée et d'attaques.

NTCP2 est conçu pour la flexibilité et la coexistence avec NTCP. Il peut être pris en charge sur le même port que NTCP, ou sur un port différent, ou sans prise en charge simultanée de NTCP du tout. Voir la section Informations du Router Publié ci-dessous pour plus de détails.

Comme pour les autres transports I2P, NTCP2 est défini uniquement pour le transport point-à-point (router vers router) de messages I2NP. Ce n'est pas un canal de données à usage général.

NTCP2 est pris en charge à partir de la version 0.9.36. Voir [Prop111](/proposals/111-ntcp-2) pour la proposition originale, incluant les discussions de contexte et des informations supplémentaires.

## Framework de Protocole Noise

NTCP2 utilise le Noise Protocol Framework [NOISE](https://noiseprotocol.org/noise.html) (Révision 33, 2017-10-04). Noise a des propriétés similaires au protocole Station-To-Station [STS](#references), qui est la base du protocole [SSU](/docs/transport/ssu). Dans la terminologie Noise, Alice est l'initiateur, et Bob est le répondeur.

NTCP2 est basé sur le protocole Noise Noise_XK_25519_ChaChaPoly_SHA256. (L'identifiant réel pour la fonction de dérivation de clé initiale est "Noise_XKaesobfse+hs2+hs3_25519_ChaChaPoly_SHA256" pour indiquer les extensions I2P - voir la section KDF 1 ci-dessous) Ce protocole Noise utilise les primitives suivantes :

- Modèle de poignée de main : XK Alice transmet sa clé à Bob (X) Alice connaît déjà la clé statique de Bob (K)
- Fonction DH : X25519 X25519 DH avec une longueur de clé de 32 octets comme spécifié dans [RFC-7748](https://tools.ietf.org/html/rfc7748).
- Fonction de chiffrement : ChaChaPoly AEAD_CHACHA20_POLY1305 comme spécifié dans [RFC-7539](https://tools.ietf.org/html/rfc7539) section 2.8. Nonce de 12 octets, avec les 4 premiers octets définis à zéro.
- Fonction de hachage : SHA256 Hachage standard de 32 octets, déjà largement utilisé dans I2P.

## Ajouts au Framework

NTCP2 définit les améliorations suivantes à Noise_XK_25519_ChaChaPoly_SHA256. Celles-ci suivent généralement les directives de la section 13 de [NOISE](https://noiseprotocol.org/noise.html).

1) Les clés éphémères en clair sont obscurcies avec le chiffrement AES en utilisant une clé et un IV connus. 2) Un remplissage aléatoire en clair est ajouté aux messages 1 et 2. Le remplissage en clair est inclus dans le calcul de hachage de la poignée de main (MixHash). Voir les sections KDF ci-dessous pour le message 2 et la partie 1 du message 3. Un remplissage AEAD aléatoire est ajouté au message 3 et aux messages de la phase de données. 3) Un champ de longueur de trame de deux octets est ajouté, comme requis pour Noise sur TCP, et comme dans obfs4. Ceci est utilisé uniquement dans les messages de la phase de données. Les trames AEAD des messages 1 et 2 ont une longueur fixe. La trame AEAD de la partie 1 du message 3 a une longueur fixe. La longueur de la trame AEAD de la partie 2 du message 3 est spécifiée dans le message 1. 4) Le champ de longueur de trame de deux octets est obscurci avec SipHash-2-4, comme dans obfs4. 5) Le format de charge utile est défini pour les messages 1, 2, 3, et la phase de données. Bien sûr, ceux-ci ne sont pas définis dans le framework.

## Messages

Tous les messages NTCP2 font 65537 octets ou moins en longueur. Le format de message est basé sur les messages Noise, avec des modifications pour le cadrage et l'indiscernabilité. Les implémentations utilisant les bibliothèques Noise standard peuvent avoir besoin de pré-traiter les messages reçus vers/depuis le format de message Noise. Tous les champs chiffrés sont des textes chiffrés AEAD.

La séquence d'établissement est la suivante :

```
Alice                           Bob

SessionRequest ------------------->
<------------------- SessionCreated
SessionConfirmed ----------------->
```
En utilisant la terminologie Noise, la séquence d'établissement et de données est la suivante : (Propriétés de sécurité de la charge utile de [Noise](https://noiseprotocol.org/noise.html) )

```
XK(s, rs):           Authentication   Confidentiality
  <- s
  ...
  -> e, es                  0                2
  <- e, ee                  2                1
  -> s, se                  2                5
  <-                        2                5
```
Une fois qu'une session a été établie, Alice et Bob peuvent échanger des messages de données.

Tous les types de messages (SessionRequest, SessionCreated, SessionConfirmed, Data et TimeSync) sont spécifiés dans cette section.

Quelques notations :

    - RH_A = Router Hash for Alice (32 bytes)
    - RH_B = Router Hash for Bob (32 bytes)

### Chiffrement authentifié

Il y a trois instances de chiffrement authentifié séparées (CipherStates). Une pendant la phase de négociation, et deux (transmission et réception) pour la phase de données. Chacune a sa propre clé provenant d'une KDF.

Les données chiffrées/authentifiées seront représentées comme

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|   Encrypted and authenticated data    |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
```
#### ChaCha20/Poly1305

Format de données chiffré et authentifié.

Entrées des fonctions de chiffrement/déchiffrement :

```
k :: 32 byte cipher key, as generated from KDF

nonce :: Counter-based nonce, 12 bytes.
         Starts at 0 and incremented for each message.
         First four bytes are always zero.
         Last eight bytes are the counter, little-endian encoded.
         Maximum value is 2**64 - 2.
         Connection must be dropped and restarted after
         it reaches that value.
         The value 2**64 - 1 must never be sent.

ad :: In handshake phase:
      Associated data, 32 bytes.
      The SHA256 hash of all preceding data.
      In data phase:
      Zero bytes

data :: Plaintext data, 0 or more bytes
```
Sortie de la fonction de chiffrement, entrée de la fonction de déchiffrement :

```
+----+----+----+----+----+----+----+----+
|Obfs Len |                             |
+----+----+                             +
|       ChaCha20 encrypted data         |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+              (MAC)                    +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

Obfs Len :: Length of (encrypted data + MAC) to follow, 16 - 65535
            Obfuscation using SipHash (see below)
            Not used in message 1 or 2, or message 3 part 1, where the length is fixed
            Not used in message 3 part 1, as the length is specified in message 1

encrypted data :: Same size as plaintext data, 0 - 65519 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
Pour ChaCha20, ce qui est décrit ici correspond à [RFC-7539](https://tools.ietf.org/html/rfc7539), qui est également utilisé de manière similaire dans TLS [RFC-7905](https://tools.ietf.org/html/rfc7905).

#### Notes

- Puisque ChaCha20 est un chiffrement de flux, les textes en clair n'ont pas besoin d'être complétés par du bourrage. Les octets de flux de clés supplémentaires sont supprimés.
- La clé pour le chiffrement (256 bits) est convenue au moyen du KDF SHA256. Les détails du KDF pour chaque message sont dans des sections séparées ci-dessous.
- Les trames ChaChaPoly pour les messages 1, 2, et la première partie du message 3, sont de taille connue. En commençant par la deuxième partie du message 3, les trames sont de taille variable. La taille de la partie 1 du message 3 est spécifiée dans le message 1. En commençant par la phase de données, les trames sont précédées d'une longueur de deux octets obfusquée avec SipHash comme dans obfs4.
- Le bourrage est à l'extérieur de la trame de données authentifiées pour les messages 1 et 2. Le bourrage est utilisé dans le KDF pour le message suivant donc la falsification sera détectée. En commençant dans le message 3, le bourrage est à l'intérieur de la trame de données authentifiées.

#### Gestion des erreurs AEAD

- Dans les messages 1, 2, et les parties 1 et 2 du message 3, la taille du message AEAD est connue à l'avance. En cas d'échec d'authentification AEAD, le destinataire doit arrêter le traitement ultérieur des messages et fermer la connexion sans répondre. Ceci devrait être une fermeture anormale (TCP RST).
- Pour la résistance au probing, dans le message 1, après un échec AEAD, Bob devrait définir un délai d'attente aléatoire (plage à déterminer) puis lire un nombre aléatoire d'octets (plage à déterminer) avant de fermer la socket. Bob devrait maintenir une liste noire d'IP avec des échecs répétés.
- Dans la phase de données, la taille du message AEAD est "chiffrée" (obfusquée) avec SipHash. Il faut prendre soin d'éviter de créer un oracle de déchiffrement. En cas d'échec d'authentification AEAD dans la phase de données, le destinataire devrait définir un délai d'attente aléatoire (plage à déterminer) puis lire un nombre aléatoire d'octets (plage à déterminer). Après la lecture, ou en cas de délai d'attente de lecture, le destinataire devrait envoyer une charge utile avec un bloc de terminaison contenant un code de raison "échec AEAD", et fermer la connexion.
- Prendre la même action d'erreur pour une valeur de champ de longueur invalide dans la phase de données.

### Fonction de Dérivation de Clé (KDF) (pour le message de handshake 1)

Le KDF génère une clé de chiffrement de phase handshake k à partir du résultat DH, en utilisant HMAC-SHA256(key, data) comme défini dans [RFC-2104](https://tools.ietf.org/html/rfc2104). Ce sont les fonctions InitializeSymmetric(), MixHash(), et MixKey(), exactement comme définies dans la spécification Noise.

```
This is the "e" message pattern:

// Define protocol_name.
Set protocol_name = "Noise_XKaesobfse+hs2+hs3_25519_ChaChaPoly_SHA256"
 (48 bytes, US-ASCII encoded, no NULL termination).

// Define Hash h = 32 bytes
h = SHA256(protocol_name);

Define ck = 32 byte chaining key. Copy the h data to ck.
Set ck = h

Define rs = Bob's 32-byte static key as published in the RouterInfo

// MixHash(null prologue)
h = SHA256(h);

// up until here, can all be precalculated by Alice for all outgoing connections

// Alice must validate that Bob's static key is a valid point on the curve here.

// Bob static key
// MixHash(rs)
// || below means append
h = SHA256(h || rs);

// up until here, can all be precalculated by Bob for all incoming connections

This is the "e" message pattern:

Alice generates her ephemeral DH key pair e.

// Alice ephemeral key X
// MixHash(e.pubkey)
// || below means append
h = SHA256(h || e.pubkey);

// h is used as the associated data for the AEAD in message 1
// Retain the Hash h for the message 2 KDF


End of "e" message pattern.

This is the "es" message pattern:

// DH(e, rs) == DH(s, re)
Define input_key_material = 32 byte DH result of Alice's ephemeral key and Bob's static key
Set input_key_material = X25519 DH result

// MixKey(DH())

Define temp_key = 32 bytes
Define HMAC-SHA256(key, data) as in [RFC-2104]_
// Generate a temp key from the chaining key and DH result
// ck is the chaining key, defined above
temp_key = HMAC-SHA256(ck, input_key_material)
// overwrite the DH result in memory, no longer needed
input_key_material = (all zeros)

// Output 1
// Set a new chaining key from the temp key
// byte() below means a single byte
ck =       HMAC-SHA256(temp_key, byte(0x01)).

// Output 2
// Generate the cipher key k
Define k = 32 bytes
// || below means append
// byte() below means a single byte
k =        HMAC-SHA256(temp_key, ck || byte(0x02)).
// overwrite the temp_key in memory, no longer needed
temp_key = (all zeros)

// retain the chaining key ck for message 2 KDF


End of "es" message pattern.
```
### 1) SessionRequest

Alice envoie à Bob.

Contenu Noise : clé éphémère X d'Alice Charge utile Noise : bloc d'option de 16 octets Charge utile non-Noise : remplissage aléatoire

(Propriétés de sécurité de la charge utile d'après [Noise](https://noiseprotocol.org/noise.html))

```
XK(s, rs):           Authentication   Confidentiality
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
La valeur X est chiffrée pour garantir l'indiscernabilité et l'unicité de la charge utile, qui sont des contre-mesures DPI nécessaires. Nous utilisons le chiffrement AES pour y parvenir, plutôt que des alternatives plus complexes et plus lentes telles qu'elligator2. Le chiffrement asymétrique avec la clé publique du router de Bob serait bien trop lent. Le chiffrement AES utilise le hash du router de Bob comme clé et l'IV de Bob tel que publié dans la base de données réseau.

Le chiffrement AES sert uniquement à la résistance contre l'inspection approfondie de paquets (DPI). Toute partie connaissant le hachage du router de Bob et l'IV, qui sont publiés dans la base de données réseau, peut déchiffrer la valeur X dans ce message.

Le padding n'est pas chiffré par Alice. Il peut être nécessaire pour Bob de déchiffrer le padding, pour empêcher les attaques temporelles.

Contenu brut :

```
+----+----+----+----+----+----+----+----+
|                                       |
+        obfuscated with RH_B           +
|       AES-CBC-256 encrypted X         |
+             (32 bytes)                +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|   ChaChaPoly encrypted data           |
+             (16 bytes)                +
|   k defined in KDF for message 1      |
+   n = 0                               +
|   see KDF for associated data         |
+----+----+----+----+----+----+----+----+
|                                       |
+        Poly1305 MAC (16 bytes)        +
|                                       |
+----+----+----+----+----+----+----+----+
|     unencrypted authenticated         |
~         padding (optional)            ~
|     length defined in options block   |
+----+----+----+----+----+----+----+----+

X :: 32 bytes, AES-256-CBC encrypted X25519 ephemeral key, little endian
        key: RH_B
        iv: As published in Bobs network database entry

padding :: Random data, 0 or more bytes.
           Total message length must be 65535 bytes or less.
           Total message length must be 287 bytes or less if
           Bob is publishing his address as NTCP
           (see Version Detection section below).
           Alice and Bob will use the padding data in the KDF for message 2.
           It is authenticated so that any tampering will cause the
           next message to fail.
```
Données non chiffrées (étiquette d'authentification Poly1305 non affichée) :

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|                   X                   |
+              (32 bytes)               +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|               options                 |
+              (16 bytes)               +
|                                       |
+----+----+----+----+----+----+----+----+
|     unencrypted authenticated         |
+         padding (optional)            +
|     length defined in options block   |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

X :: 32 bytes, X25519 ephemeral key, little endian

options :: options block, 16 bytes, see below

padding :: Random data, 0 or more bytes.
           Total message length must be 65535 bytes or less.
           Total message length must be 287 bytes or less if
           Bob is publishing his address as "NTCP"
           (see Version Detection section below)
           Alice and Bob will use the padding data in the KDF for message 2.
           It is authenticated so that any tampering will cause the
           next message to fail.
```
Bloc d'options : Remarque : Tous les champs sont en big-endian.

```
+----+----+----+----+----+----+----+----+
| id | ver|  padLen | m3p2len | Rsvd(0) |
+----+----+----+----+----+----+----+----+
|        tsA        |   Reserved (0)    |
+----+----+----+----+----+----+----+----+

id :: 1 byte, the network ID (currently 2, except for test networks)
      As of 0.9.42. See proposal 147.

ver :: 1 byte, protocol version (currently 2)

padLen :: 2 bytes, length of the padding, 0 or more
          See below for max guidelines. Random size from 0 to 64 bytes minimum is recommended.
          (Distribution is implementation-dependent)

m3p2Len :: 2 bytes, length of the the second AEAD frame in SessionConfirmed
           (message 3 part 2) See notes below

Rsvd :: 2 bytes, set to 0 for compatibility with future options

tsA :: 4 bytes, Unix timestamp, unsigned seconds.
       Wraps around in 2106

Reserved :: 4 bytes, set to 0 for compatibility with future options
```
#### Notes

- Lorsque l'adresse publiée est "NTCP", Bob prend en charge à la fois NTCP et NTCP2 sur le même port. Pour des raisons de compatibilité, lors de l'initiation d'une connexion vers une adresse publiée comme "NTCP", Alice doit limiter la taille maximale de ce message, y compris le padding, à 287 octets ou moins. Cela facilite l'identification automatique du protocole par Bob. Lorsqu'elle est publiée comme "NTCP2", il n'y a aucune restriction de taille. Voir les sections Adresses Publiées et Détection de Version ci-dessous.

- La valeur X unique dans le bloc AES initial garantit que le texte chiffré est différent pour chaque session.

- Bob doit rejeter les connexions où la valeur de l'horodatage est trop éloignée de l'heure actuelle. Appelons le delta de temps maximum "D". Bob doit maintenir un cache local des valeurs de handshake précédemment utilisées et rejeter les doublons, pour éviter les attaques de rejeu. Les valeurs dans le cache doivent avoir une durée de vie d'au moins 2*D. Les valeurs du cache dépendent de l'implémentation, cependant la valeur X de 32 octets (ou son équivalent chiffré) peut être utilisée.

- Les clés éphémères Diffie-Hellman ne doivent jamais être réutilisées, pour prévenir les attaques cryptographiques, et la réutilisation sera rejetée comme une attaque par rejeu.

- Les options "KE" et "auth" doivent être compatibles, c'est-à-dire que le secret partagé K doit avoir la taille appropriée. Si davantage d'options "auth" sont ajoutées, cela pourrait implicitement changer la signification du flag "KE" pour utiliser un KDF différent ou une taille de troncature différente.

- Bob doit valider que la clé éphémère d'Alice est un point valide sur la courbe ici.

- Le rembourrage devrait être limité à une quantité raisonnable. Bob peut rejeter les connexions avec un rembourrage excessif. Bob spécifiera ses options de rembourrage dans le message 2. Directives min/max à déterminer. Taille aléatoire de 0 à 31 octets minimum ? (La distribution dépend de l'implémentation) Les implémentations Java limitent actuellement le rembourrage à 256 octets maximum.

- En cas d'erreur, y compris AEAD, DH, horodatage, rejeu apparent, ou échec de validation de clé, Bob doit arrêter le traitement ultérieur des messages et fermer la connexion sans répondre. Cela devrait être une fermeture anormale (TCP RST). Pour la résistance au sondage, après un échec AEAD, Bob devrait définir un délai d'attente aléatoire (plage à déterminer) puis lire un nombre aléatoire d'octets (plage à déterminer), avant de fermer la socket.

- Bob peut effectuer une vérification MSB rapide pour une clé valide (X[31] & 0x80 == 0) avant de tenter le déchiffrement. Si le bit de poids fort est défini, implémenter une résistance au sondage comme pour les échecs AEAD.

- Atténuation DoS : DH est une opération relativement coûteuse. Comme avec le protocole NTCP précédent, les routers doivent prendre toutes les mesures nécessaires pour prévenir l'épuisement du CPU ou des connexions. Placer des limites sur le nombre maximum de connexions actives et le nombre maximum d'établissements de connexion en cours. Appliquer des délais de lecture (à la fois par lecture et total pour "slowloris"). Limiter les connexions répétées ou simultanées depuis la même source. Maintenir des listes noires pour les sources qui échouent de manière répétée. Ne pas répondre aux échecs AEAD.

- Pour faciliter la détection rapide de version et la négociation, les implémentations doivent s'assurer qu'Alice met en mémoire tampon puis vide entièrement le contenu du premier message d'un coup, y compris le remplissage. Cela augmente la probabilité que les données soient contenues dans un seul paquet TCP (sauf si segmentées par l'OS ou les middleboxes), et reçues d'un coup par Bob. De plus, les implémentations doivent s'assurer que Bob met en mémoire tampon puis vide entièrement le contenu du deuxième message d'un coup, y compris le remplissage. et que Bob met en mémoire tampon puis vide entièrement le contenu du troisième message d'un coup. Ceci est également pour l'efficacité et pour garantir l'efficacité du remplissage aléatoire.

- Champ "ver" : Le protocole Noise global, les extensions, et le protocole NTCP incluant les spécifications de charge utile, indiquant NTCP2. Ce champ peut être utilisé pour indiquer la prise en charge de futurs changements.

- Longueur de la partie 2 du message 3 : Il s'agit de la taille de la seconde trame AEAD (incluant le MAC de 16 octets) contenant les informations du router d'Alice et un remplissage optionnel qui sera envoyé dans le message SessionConfirmed. Comme les routers régénèrent et republient périodiquement leurs informations de router, la taille des informations actuelles du router peut changer avant l'envoi du message 3. Les implémentations doivent choisir l'une des deux stratégies suivantes :

a\) sauvegarder les informations actuelles du router à envoyer dans le message 3, afin que la taille soit connue, et éventuellement ajouter de l'espace pour le rembourrage ;

b) augmenter la taille spécifiée suffisamment pour permettre une éventuelle augmentation de la taille du Router Info, et toujours ajouter un rembourrage lorsque le message 3 est effectivement envoyé. Dans les deux cas, la longueur "m3p2len" incluse dans le message 1 doit être exactement la taille de cette trame lors de l'envoi dans le message 3.

- Bob doit faire échouer la connexion s'il reste des données entrantes après avoir validé le message 1 et lu le rembourrage. Il ne devrait y avoir aucune donnée supplémentaire d'Alice, car Bob n'a pas encore répondu avec le message 2.

- Le champ ID réseau est utilisé pour identifier rapidement les connexions inter-réseaux. Si ce champ est non nul et ne correspond pas à l'ID réseau de Bob, Bob devrait se déconnecter et bloquer les connexions futures. Toute connexion provenant de réseaux de test devrait avoir un ID différent et échouera au test. Depuis la version 0.9.42. Voir la proposition 147 pour plus d'informations.

- Jusqu'à l'API 0.9.68 (version 2.11.0), Java I2P implémentait un maximum de 256 octets de remplissage pour les connexions non-PQ, cependant cela n'était pas documenté précédemment.
  À partir de l'API 0.9.69 (version 2.12.0), Java I2P implémente le même remplissage maximum pour les connexions non-PQ
  que pour MLKEM-512. Le remplissage maximum est de 880 octets.

### Fonction de Dérivation de Clé (KDF) (pour le message de handshake 2 et la partie 1 du message 3)

```
// take h saved from message 1 KDF
// MixHash(ciphertext)
h = SHA256(h || 32 byte encrypted payload from message 1)

// MixHash(padding)
// Only if padding length is nonzero
h = SHA256(h || random padding from message 1)

This is the "e" message pattern:

Bob generates his ephemeral DH key pair e.

// h is from KDF for handshake message 1
// Bob ephemeral key Y
// MixHash(e.pubkey)
// || below means append
h = SHA256(h || e.pubkey);

// h is used as the associated data for the AEAD in message 2
// Retain the Hash h for the message 3 KDF

End of "e" message pattern.

This is the "ee" message pattern:

// DH(e, re)
Define input_key_material = 32 byte DH result of Alice's ephemeral key and Bob's ephemeral key
Set input_key_material = X25519 DH result
// overwrite Alice's ephemeral key in memory, no longer needed
// Alice:
e(public and private) = (all zeros)
// Bob:
re = (all zeros)

// MixKey(DH())

Define temp_key = 32 bytes
Define HMAC-SHA256(key, data) as in [RFC-2104]_
// Generate a temp key from the chaining key and DH result
// ck is the chaining key, from the KDF for handshake message 1
temp_key = HMAC-SHA256(ck, input_key_material)
// overwrite the DH result in memory, no longer needed
input_key_material = (all zeros)

// Output 1
// Set a new chaining key from the temp key
// byte() below means a single byte
ck =       HMAC-SHA256(temp_key, byte(0x01)).

// Output 2
// Generate the cipher key k
Define k = 32 bytes
// || below means append
// byte() below means a single byte
k =        HMAC-SHA256(temp_key, ck || byte(0x02)).
// overwrite the temp_key in memory, no longer needed
temp_key = (all zeros)

// retain the chaining key ck for message 3 KDF

End of "ee" message pattern.
```
### 2) SessionCreated

Bob envoie à Alice.

Contenu Noise : clé éphémère Y de Bob Charge utile Noise : bloc d'option de 16 octets Charge utile non-noise : Remplissage aléatoire

(Propriétés de sécurité de la charge utile de [Noise](https://noiseprotocol.org/noise.html) )

```
XK(s, rs):           Authentication   Confidentiality
  <- e, ee                  2                1

  Authentication: 2.
  Sender authentication resistant to key-compromise impersonation (KCI).
  The sender authentication is based on an ephemeral-static DH ("es" or "se")
  between the sender's static key pair and the recipient's ephemeral key pair.
  Assuming the corresponding private keys are secure, this authentication cannot be forged.

  Confidentiality: 1.
  Encryption to an ephemeral recipient.
  This payload has forward secrecy, since encryption involves an ephemeral-ephemeral DH ("ee").
  However, the sender has not authenticated the recipient,
  so this payload might be sent to any party, including an active attacker.


  "e": Bob generates a new ephemeral key pair and stores it in the e variable,
  writes the ephemeral public key as cleartext into the message buffer,
  and hashes the public key along with the old h to derive a new h.

  "ee": A DH is performed between the Bob's ephemeral key pair and the Alice's ephemeral key pair.
  The result is hashed along with the old ck to derive a new ck and k, and n is set to zero.
```
La valeur Y est chiffrée pour garantir l'indiscernabilité et l'unicité de la charge utile, qui sont des contre-mesures DPI nécessaires. Nous utilisons le chiffrement AES pour y parvenir, plutôt que des alternatives plus complexes et plus lentes comme elligator2. Le chiffrement asymétrique vers la clé publique du router d'Alice serait bien trop lent. Le chiffrement AES utilise le hash du router de Bob comme clé et l'état AES du message 1 (qui a été initialisé avec l'IV de Bob tel que publié dans la base de données réseau).

Le chiffrement AES est uniquement destiné à résister à l'inspection approfondie de paquets (DPI). Toute partie connaissant le hash du router de Bob et l'IV, qui sont publiés dans la base de données réseau, et ayant capturé les 32 premiers octets du message 1, peut déchiffrer la valeur Y dans ce message.

Contenu brut :

```
+----+----+----+----+----+----+----+----+
|                                       |
+        obfuscated with RH_B           +
|       AES-CBC-256 encrypted Y         |
+              (32 bytes)               +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|   ChaChaPoly encrypted data (options) |
+   16 bytes                            +
|   k defined in KDF for message 2      |
+   n = 0; see KDF for associated data  +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+        Poly1305 MAC (16 bytes)        +
|                                       |
+----+----+----+----+----+----+----+----+
|     unencrypted authenticated         |
+         padding (optional)            +
|     length defined in options block   |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

Y :: 32 bytes, AES-256-CBC encrypted X25519 ephemeral key, little endian
        key: RH_B
        iv: Using AES state from message 1
```
Données non chiffrées (balise d'authentification Poly1305 non affichée) :

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|                  Y                    |
+              (32 bytes)               +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|               options                 |
+              (16 bytes)               +
|                                       |
+----+----+----+----+----+----+----+----+
|     unencrypted authenticated         |
+         padding (optional)            +
|     length defined in options block   |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

Y :: 32 bytes, X25519 ephemeral key, little endian

options :: options block, 16 bytes, see below

padding :: Random data, 0 or more bytes.
           Total message length must be 65535 bytes or less.
           Alice and Bob will use the padding data in the KDF for message 3 part 1.
           It is authenticated so that any tampering will cause the
           next message to fail.
```
#### Notes

- Alice doit valider que la clé éphémère de Bob est un point valide sur la courbe ici.
- Le padding devrait être limité à une quantité raisonnable. Alice peut rejeter les connexions avec un padding excessif. Alice spécifiera ses options de padding dans le message 3. Directives min/max à déterminer. Taille aléatoire de 0 à 31 octets minimum ? (La distribution dépend de l'implémentation)
- En cas d'erreur, y compris AEAD, DH, horodatage, replay apparent, ou échec de validation de clé, Alice doit arrêter tout traitement ultérieur de message et fermer la connexion sans répondre. Cela devrait être une fermeture anormale (TCP RST).
- Pour faciliter un handshake rapide, les implémentations doivent s'assurer que Bob met en tampon puis vide tout le contenu du premier message d'un coup, y compris le padding. Cela augmente la probabilité que les données soient contenues dans un seul paquet TCP (sauf si segmenté par l'OS ou les middleboxes), et reçues d'un coup par Alice. C'est aussi pour l'efficacité et pour assurer l'efficacité du padding aléatoire.
- Alice doit faire échouer la connexion si des données entrantes restent après avoir validé le message 2 et lu le padding. Il ne devrait y avoir aucune donnée supplémentaire de Bob, car Alice n'a pas encore répondu avec le message 3.

Bloc d'options : Remarque : Tous les champs sont en big-endian.

```
+----+----+----+----+----+----+----+----+
| Rsvd(0) | padLen  |   Reserved (0)    |
+----+----+----+----+----+----+----+----+
|        tsB        |   Reserved (0)    |
+----+----+----+----+----+----+----+----+

Reserved :: 10 bytes total, set to 0 for compatibility with future options

padLen :: 2 bytes, big endian, length of the padding, 0 or more
          See below for max guidelines. Random size from 0 to 64 bytes minimum is recommended.
          (Distribution is implementation-dependent)

tsB :: 4 bytes, big endian, Unix timestamp, unsigned seconds.
       Wraps around in 2106
```
#### Notes

- Alice doit rejeter les connexions où la valeur de l'horodatage est trop éloignée de l'heure actuelle. Appelons le delta de temps maximum "D". Alice doit maintenir un cache local des valeurs de handshake précédemment utilisées et rejeter les doublons, pour empêcher les attaques par rejeu. Les valeurs dans le cache doivent avoir une durée de vie d'au moins 2*D. Les valeurs du cache dépendent de l'implémentation, cependant la valeur Y de 32 octets (ou son équivalent chiffré) peut être utilisée.

- Jusqu'à l'API 0.9.68 (version 2.11.0), Java I2P implémentait un maximum de 256 octets de padding pour les connexions non-PQ, cependant cela n'était pas documenté auparavant.
  À partir de l'API 0.9.69 (version 2.12.0), Java I2P implémente le même padding maximum pour les connexions non-PQ
  que pour MLKEM-512. Le padding maximum est de 848 octets.

#### Problèmes

- Inclure ici les options de remplissage min/max ?

### Chiffrement pour la partie 1 du message 3 de handshake, en utilisant le KDF du message 2)

```
// take h saved from message 2 KDF
// MixHash(ciphertext)
h = SHA256(h || 24 byte encrypted payload from message 2)

// MixHash(padding)
// Only if padding length is nonzero
h = SHA256(h || random padding from message 2)
// h is used as the associated data for the AEAD in message 3 part 1, below

This is the "s" message pattern:

Define s = Alice's static public key, 32 bytes

// EncryptAndHash(s.publickey)
// EncryptWithAd(h, s.publickey)
// AEAD_ChaCha20_Poly1305(key, nonce, associatedData, data)
// k is from handshake message 1
// n is 1
ciphertext = AEAD_ChaCha20_Poly1305(k, n++, h, s.publickey)
// MixHash(ciphertext)
// || below means append
h = SHA256(h || ciphertext);

// h is used as the associated data for the AEAD in message 3 part 2

End of "s" message pattern.
```
### Fonction de dérivation de clé (KDF) (pour la partie 2 du message 3 de handshake)

```
This is the "se" message pattern:

// DH(s, re) == DH(e, rs)
Define input_key_material = 32 byte DH result of Alice's static key and Bob's ephemeral key
Set input_key_material = X25519 DH result
// overwrite Bob's ephemeral key in memory, no longer needed
// Alice:
re = (all zeros)
// Bob:
e(public and private) = (all zeros)

// MixKey(DH())

Define temp_key = 32 bytes
Define HMAC-SHA256(key, data) as in [RFC-2104]_
// Generate a temp key from the chaining key and DH result
// ck is the chaining key, from the KDF for handshake message 1
temp_key = HMAC-SHA256(ck, input_key_material)
// overwrite the DH result in memory, no longer needed
input_key_material = (all zeros)

// Output 1
// Set a new chaining key from the temp key
// byte() below means a single byte
ck =       HMAC-SHA256(temp_key, byte(0x01)).

// Output 2
// Generate the cipher key k
Define k = 32 bytes
// || below means append
// byte() below means a single byte
k =        HMAC-SHA256(temp_key, ck || byte(0x02)).

// h from message 3 part 1 is used as the associated data for the AEAD in message 3 part 2

// EncryptAndHash(payload)
// EncryptWithAd(h, payload)
// AEAD_ChaCha20_Poly1305(key, nonce, associatedData, data)
// n is 0
ciphertext = AEAD_ChaCha20_Poly1305(k, n++, h, payload)
// MixHash(ciphertext)
// || below means append
h = SHA256(h || ciphertext);

// retain the chaining key ck for the data phase KDF
// retain the hash h for the data phase Additional Symmetric Key (SipHash) KDF

End of "se" message pattern.

// overwrite the temp_key in memory, no longer needed
temp_key = (all zeros)
```
### 3) SessionConfirmed

Alice envoie à Bob.

Contenu Noise : clé statique d'Alice Charge utile Noise : RouterInfo d'Alice et remplissage aléatoire Charge utile non-noise : aucune

(Propriétés de sécurité de la charge utile tirées de [Noise](https://noiseprotocol.org/noise.html) )

```
XK(s, rs):           Authentication   Confidentiality
  -> s, se                  2                5

  Authentication: 2.
  Sender authentication resistant to key-compromise impersonation (KCI).  The
  sender authentication is based on an ephemeral-static DH ("es" or "se")
  between the sender's static key pair and the recipient's ephemeral key
  pair.  Assuming the corresponding private keys are secure, this
  authentication cannot be forged.

  Confidentiality: 5.
  Encryption to a known recipient, strong forward secrecy.  This payload is
  encrypted based on an ephemeral-ephemeral DH as well as an ephemeral-static
  DH with the recipient's static key pair.  Assuming the ephemeral private
  keys are secure, and the recipient is not being actively impersonated by an
  attacker that has stolen its static private key, this payload cannot be
  decrypted.

  "s": Alice writes her static public key from the s variable into the
  message buffer, encrypting it, and hashes the output along with the old h
  to derive a new h.

  "se": A DH is performed between the Alice's static key pair and the Bob's
  ephemeral key pair.  The result is hashed along with the old ck to derive a
  new ck and k, and n is set to zero.
```
Cela contient deux trames ChaChaPoly. La première est la clé publique statique chiffrée d'Alice. La seconde est la charge utile Noise : le RouterInfo chiffré d'Alice, les options facultatives et le rembourrage optionnel. Elles utilisent des clés différentes, car la fonction MixKey() est appelée entre les deux.

Contenu brut :

```
+----+----+----+----+----+----+----+----+
|                                       |
+   ChaCha20 encrypted data (32 bytes)  +
|   Alice static key S                  |
+     k defined in KDF for message 2    +
|   n = 1 see KDF for associated data   |
+----+----+----+----+----+----+----+----+
|                                       |
+        Poly1305 MAC (16 bytes)        +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+   ChaCha20 encrypted data             +
|     Length specified in message 1     |
+     (including 16 byte MAC to follow) +
|                                       |
+       Alice RouterInfo                +
|       using block format 2            |
+       Alice Options (optional)        +
|       using block format 1            |
+       Arbitrary padding               +
|       using block format 254          |
+                                       +
| k defined in KDF for message 3 part 2 |
+     n = 0                             +
|     see KDF for associated data       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+        Poly1305 MAC (16 bytes)        +
|                                       |
+----+----+----+----+----+----+----+----+

S :: 32 bytes, ChaChaPoly encrypted Alice's X25519 static key, little endian
     inside 48 byte ChaChaPoly frame
```
Données non chiffrées (balises d'authentification Poly1305 non affichées) :

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|              S                        |
+       Alice static key                +
|          (32 bytes)                   |
+                                       +
|                                       |
+                                       +
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|                                       |
+                                       +
|       Alice RouterInfo block          |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+       Optional Options block          +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+       Optional Padding block          +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

S :: 32 bytes, Alice's X25519 static key, little endian
```
#### Notes

- Bob doit effectuer la validation habituelle des Router Info. S'assurer que le type de signature est pris en charge, vérifier la signature, vérifier que l'horodatage est dans les limites acceptables, et effectuer toute autre vérification nécessaire.

- Bob doit vérifier que la clé statique d'Alice reçue dans la première trame correspond à la clé statique dans le Router Info. Bob doit d'abord rechercher dans le Router Info une Router Address NTCP ou NTCP2 avec une option de version (v) correspondante. Voir les sections Router Info Publié et Router Info Non Publié ci-dessous.

- Si Bob a une version plus ancienne du RouterInfo d'Alice dans sa netdb, vérifier que la clé statique dans les informations du routeur est la même dans les deux versions, si elle est présente, et si la version plus ancienne a moins de XXX âge (voir temps de rotation des clés ci-dessous)

- Bob doit valider que la clé statique d'Alice est un point valide sur la courbe ici.

- Les options doivent être incluses, pour spécifier les paramètres de remplissage.

- En cas d'erreur, y compris d'échec de validation AEAD, RI, DH, d'horodatage ou de clé, Bob doit arrêter le traitement des messages et fermer la connexion sans répondre. Cela devrait être une fermeture anormale (TCP RST).

- Pour faciliter une négociation rapide, les implémentations doivent s'assurer qu'Alice met en mémoire tampon puis envoie l'intégralité du contenu du troisième message d'un coup, y compris les deux trames AEAD. Cela augmente la probabilité que les données soient contenues dans un seul paquet TCP (sauf si segmentées par l'OS ou les middleboxes), et reçues en une seule fois par Bob. Ceci est également pour l'efficacité et pour assurer l'efficacité du remplissage aléatoire.

- Longueur de la trame partie 2 du message 3 : La longueur de cette trame (y compris MAC) est envoyée par Alice dans le message 1. Voir ce message pour des notes importantes sur l'allocation d'un espace suffisant pour le padding.

- Contenu de la trame partie 2 du message 3 : Le format de cette trame est identique au format des trames de la phase de données, sauf que la longueur de la trame est envoyée par Alice dans le message 1. Voir ci-dessous pour le format des trames de la phase de données. La trame doit contenir 1 à 3 blocs dans l'ordre suivant :

1)  Bloc d'informations du router d'Alice (requis)   2)  Bloc d'options (optionnel)

3\) Bloc de remplissage (optionnel) Cette trame ne doit jamais contenir d'autre type de bloc.

- Le padding de la partie 2 du message 3 n'est pas requis si Alice ajoute une trame de phase de données (contenant optionnellement du padding) à la fin du message 3 et envoie les deux en même temps, car cela apparaîtra comme un gros flux d'octets à un observateur. Comme Alice aura généralement, mais pas toujours, un message I2NP à envoyer à Bob (c'est pourquoi elle s'est connectée à lui), c'est l'implémentation recommandée, pour l'efficacité et pour garantir l'efficacité du padding aléatoire.

- La longueur théorique maximale totale des deux trames AEAD du message 3 (parties 1 et 2) est de 65535 octets ; la partie 1 fait 48 octets, donc la longueur maximale de la trame de la partie 2 est de 65487 ; la longueur maximale du texte en clair de la partie 2, hors MAC, est de 65471.
  AVERTISSEMENT : Certaines implémentations appliquent des limites beaucoup plus strictes. Java I2P limite actuellement la longueur totale à 4096 octets. N'ajoutez pas de remplissage excessif.

### Fonction de dérivation de clé (KDF) (pour la phase de données)

La phase de données utilise une entrée de données associées de longueur nulle.

Le KDF génère deux clés de chiffrement k_ab et k_ba à partir de la clé de chaînage ck, en utilisant HMAC-SHA256(key, data) tel que défini dans [RFC-2104](https://tools.ietf.org/html/rfc2104). Il s'agit de la fonction Split(), exactement comme définie dans la spécification Noise.

```
ck = from handshake phase

// k_ab, k_ba = HKDF(ck, zerolen)
// ask_master = HKDF(ck, zerolen, info="ask")

// zerolen is a zero-length byte array
temp_key = HMAC-SHA256(ck, zerolen)
// overwrite the chaining key in memory, no longer needed
ck = (all zeros)

// Output 1
// cipher key, for Alice transmits to Bob (Noise doesn't make clear which is which, but Java code does)
k_ab =   HMAC-SHA256(temp_key, byte(0x01)).

// Output 2
// cipher key, for Bob transmits to Alice (Noise doesn't make clear which is which, but Java code does)
k_ba =   HMAC-SHA256(temp_key, k_ab || byte(0x02)).


KDF for SipHash for length field:
Generate an Additional Symmetric Key (ask) for SipHash
SipHash uses two 8-byte keys (big endian) and 8 byte IV for first data.

// "ask" is 3 bytes, US-ASCII, no null termination
ask_master = HMAC-SHA256(temp_key, "ask" || byte(0x01))
// sip_master = HKDF(ask_master, h || "siphash")
// "siphash" is 7 bytes, US-ASCII, no null termination
// overwrite previous temp_key in memory
// h is from KDF for message 3 part 2
temp_key = HMAC-SHA256(ask_master, h || "siphash")
// overwrite ask_master in memory, no longer needed
ask_master = (all zeros)
sip_master = HMAC-SHA256(temp_key, byte(0x01))

Alice to Bob SipHash k1, k2, IV:
// sipkeys_ab, sipkeys_ba = HKDF(sip_master, zerolen)
// overwrite previous temp_key in memory
temp_key = HMAC-SHA256(sip_master, zerolen)
// overwrite sip_master in memory, no longer needed
sip_master = (all zeros)

sipkeys_ab = HMAC-SHA256(temp_key, byte(0x01)).
sipk1_ab = sipkeys_ab[0:7], little endian
sipk2_ab = sipkeys_ab[8:15], little endian
sipiv_ab = sipkeys_ab[16:23]

Bob to Alice SipHash k1, k2, IV:

sipkeys_ba = HMAC-SHA256(temp_key, sipkeys_ab || byte(0x02)).
sipk1_ba = sipkeys_ba[0:7], little endian
sipk2_ba = sipkeys_ba[8:15], little endian
sipiv_ba = sipkeys_ba[16:23]

// overwrite the temp_key in memory, no longer needed
temp_key = (all zeros)
```
### 4) Phase de données

Charge utile Noise : Comme défini ci-dessous, incluant un remplissage aléatoire Charge utile non-Noise : aucune

À partir de la 2ème partie du message 3, tous les messages sont à l'intérieur d'une "frame" ChaChaPoly authentifiée et chiffrée avec une longueur obfusquée de deux octets en préfixe. Tout le padding est à l'intérieur de la frame. À l'intérieur de la frame se trouve un format standard avec zéro ou plusieurs "blocs". Chaque bloc a un type d'un octet et une longueur de deux octets. Les types incluent date/heure, message I2NP, options, terminaison et padding.

Note : Bob peut, mais n'est pas tenu, d'envoyer ses RouterInfo à Alice comme premier message à Alice dans la phase de données.

(Propriétés de sécurité de la charge utile d'après [Noise](https://noiseprotocol.org/noise.html))

```
XK(s, rs):           Authentication   Confidentiality
  <-                        2                5
  ->                        2                5

  Authentication: 2.
  Sender authentication resistant to key-compromise impersonation (KCI).
  The sender authentication is based on an ephemeral-static DH ("es" or "se")
  between the sender's static key pair and the recipient's ephemeral key pair.
  Assuming the corresponding private keys are secure, this authentication cannot be forged.

  Confidentiality: 5.
  Encryption to a known recipient, strong forward secrecy.
  This payload is encrypted based on an ephemeral-ephemeral DH as well as
  an ephemeral-static DH with the recipient's static key pair.
  Assuming the ephemeral private keys are secure, and the recipient is not being actively impersonated
  by an attacker that has stolen its static private key, this payload cannot be decrypted.
```
#### Notes

- Pour l'efficacité et pour minimiser l'identification du champ de longueur, les implémentations doivent s'assurer que l'expéditeur met en mémoire tampon puis vide l'intégralité du contenu des messages de données d'un coup, incluant le champ de longueur et la trame AEAD. Ceci augmente la probabilité que les données soient contenues dans un seul paquet TCP (sauf si segmentées par l'OS ou les middleboxes), et reçues d'un coup par l'autre partie. C'est aussi pour l'efficacité et pour assurer l'efficacité du padding aléatoire.
- Le router peut choisir de terminer la session en cas d'erreur AEAD, ou peut continuer à tenter de communiquer. S'il continue, le router devrait terminer après des erreurs répétées.

#### Longueur obscurcie SipHash

Référence : [SipHash](https://www.131002.net/siphash/)

Une fois que les deux côtés ont terminé la négociation, ils transfèrent des charges utiles qui sont alors chiffrées et authentifiées dans des "trames" ChaChaPoly.

Chaque trame est précédée d'une longueur de deux octets, en big endian. Cette longueur spécifie le nombre d'octets de trame chiffrés qui suivent, y compris le MAC. Pour éviter de transmettre des champs de longueur identifiables dans le flux, la longueur de la trame est obfusquée en appliquant un XOR avec un masque dérivé de SipHash, tel qu'initialisé à partir du KDF de la phase de données. Notez que les deux directions ont des clés SipHash et des IV uniques provenant du KDF.

```
    sipk1, sipk2 = The SipHash keys from the KDF.  (two 8-byte long integers)
    IV[0] = sipiv = The SipHash IV from the KDF. (8 bytes)
    length is big endian.
    For each frame:
      IV[n] = SipHash-2-4(sipk1, sipk2, IV[n-1])
      Mask[n] = First 2 bytes of IV[n]
      obfuscatedLength = length ^ Mask[n]

    The first length output will be XORed with with IV[1].
```
Le récepteur possède les mêmes clés SipHash et IV. Le décodage de la longueur se fait en dérivant le masque utilisé pour obfusquer la longueur et en appliquant un XOR au condensé tronqué pour obtenir la longueur de la trame. La longueur de la trame est la longueur totale de la trame chiffrée incluant le MAC.

#### Notes

- Si vous utilisez une fonction de bibliothèque SipHash qui retourne un entier long non signé, utilisez les deux octets les moins significatifs comme Masque. Convertissez l'entier long vers le prochain IV en little endian.

#### Contenu brut

```
+----+----+----+----+----+----+----+----+
|obf size |                             |
+----+----+                             +
|                                       |
+   ChaChaPoly frame                    +
|   Encrypted and authenticated         |
+   key is k_ab for Alice to Bob        +
|   key is k_ba for Bob to Alice        |
+   as defined in KDF for data phase    +
|   n starts at 0 and increments        |
+   for each frame in that direction    +
|   no associated data                  |
+   16 bytes minimum                    +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

obf size :: 2 bytes length obfuscated with SipHash
            when de-obfuscated: 16 - 65535

Minimum size including length field is 18 bytes.
Maximum size including length field is 65537 bytes.
Obfuscated length is 2 bytes.
Maximum ChaChaPoly frame is 65535 bytes.
```
#### Notes

- Comme le récepteur doit obtenir la trame entière pour vérifier le MAC, il est recommandé que l'expéditeur limite les trames à quelques Ko plutôt que de maximiser la taille de trame. Cela minimisera la latence au niveau du récepteur.

#### Données non chiffrées

Il y a zéro ou plusieurs blocs dans la trame chiffrée. Chaque bloc contient un identifiant d'un octet, une longueur de deux octets et zéro ou plusieurs octets de données.

Pour l'extensibilité, les récepteurs doivent ignorer les blocs avec des identifiants inconnus et les traiter comme du remplissage.

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
       0 for datetime
       1 for options
       2 for RouterInfo
       3 for I2NP message
       4 for termination
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

Dans le message de négociation 3 partie 2, l'ordre doit être : RouterInfo, suivi des Options si présentes, suivi du Padding si présent. Aucun autre bloc n'est autorisé.

Dans la phase de données, l'ordre n'est pas spécifié, sauf pour les exigences suivantes : Le Padding, s'il est présent, doit être le dernier bloc. La Termination, si elle est présente, doit être le dernier bloc sauf pour le Padding.

Il peut y avoir plusieurs blocs I2NP dans une seule trame. Plusieurs blocs de bourrage ne sont pas autorisés dans une seule trame. D'autres types de blocs n'auront probablement pas plusieurs blocs dans une seule trame, mais ce n'est pas interdit.

#### DateTime

Cas particulier pour la synchronisation temporelle :

```
+----+----+----+----+----+----+----+
| 0  |    4    |     timestamp     |
+----+----+----+----+----+----+----+

blk :: 0
size :: 2 bytes, big endian, value = 4
timestamp :: Unix timestamp, unsigned seconds.
             Wraps around in 2106
```
NOTE : Les implémentations doivent arrondir à la seconde la plus proche pour éviter un biais d'horloge dans le réseau.

#### Options

Transmettre les options mises à jour. Les options incluent : Rembourrage minimum et maximum.

Le bloc d'options aura une longueur variable.

```
+----+----+----+----+----+----+----+----+
| 1  |  size   |tmin|tmax|rmin|rmax|tdmy|
+----+----+----+----+----+----+----+----+
|tdmy|  rdmy   |  tdelay |  rdelay |    |
~----+----+----+----+----+----+----+    ~
|              more_options             |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

blk :: 1
size :: 2 bytes, big endian, size of options to follow, 12 bytes minimum

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

Padding distribution specified as additional parameters?
Random delay specified as additional parameters?

more_options :: Format TBD
```
#### Problèmes d'options

- Le format des options est à déterminer.
- La négociation des options est à déterminer.

#### RouterInfo

Transmettre le RouterInfo d'Alice à Bob. Utilisé dans la partie 2 du message 3 de l'établissement de connexion. Transmettre le RouterInfo d'Alice à Bob, ou celui de Bob à Alice. Utilisé optionnellement dans la phase de données.

```
+----+----+----+----+----+----+----+----+
| 2  |  size   |flg |    RouterInfo     |
+----+----+----+----+                   +
| (Alice RI in handshake msg 3 part 2)  |
~ (Alice, Bob, or third-party           ~
|  RI in data phase)                    |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

blk :: 2
size :: 2 bytes, big endian, size of flag + router info to follow
flg :: 1 byte flags
       bit order: 76543210
       bit 0: 0 for local store, 1 for flood request
       bits 7-1: Unused, set to 0 for future compatibility
routerinfo :: Alice's or Bob's RouterInfo
```
#### Notes

- Lorsque utilisé dans la phase de données, le destinataire (Alice ou Bob) doit valider qu'il s'agit du même Router Hash que celui initialement envoyé (pour Alice) ou auquel il a été envoyé (pour Bob). Ensuite, le traiter comme un message I2NP DatabaseStore local. Valider la signature, valider l'horodatage plus récent, et stocker dans la netdb locale. Si le bit de flag 0 est 1, et que la partie réceptrice est floodfill, le traiter comme un message DatabaseStore avec un jeton de réponse non nul, et le diffuser vers les floodfills les plus proches.
- Le Router Info n'est PAS compressé avec gzip (contrairement à un message DatabaseStore, où il l'est)
- La diffusion ne doit pas être demandée à moins qu'il y ait des RouterAddresses publiées dans le RouterInfo. Le router récepteur ne doit pas diffuser le RouterInfo à moins qu'il contienne des RouterAddresses publiées.
- Les implémenteurs doivent s'assurer que lors de la lecture d'un bloc, des données mal formées ou malveillantes ne provoqueront pas de débordement de lecture dans le bloc suivant.
- Ce protocole ne fournit pas d'accusé de réception indiquant que le RouterInfo a été reçu, stocké, ou diffusé (que ce soit dans la phase de handshake ou de données). Si un accusé de réception est souhaité, et que le destinataire est floodfill, l'expéditeur devrait plutôt envoyer un message I2NP DatabaseStoreMessage standard avec un jeton de réponse.

#### Problèmes

- Pourrait également être utilisé dans la phase de données, au lieu d'un I2NP DatabaseStoreMessage. Par exemple, Bob pourrait l'utiliser pour initier la phase de données.
- Est-il autorisé que ceci contienne le RI pour des routers autres que l'initiateur, comme un remplacement général pour les DatabaseStoreMessages, par exemple pour le flooding par les floodfills ?

#### Message I2NP

Un seul message I2NP avec un en-tête modifié. Les messages I2NP ne peuvent pas être fragmentés entre les blocs ou entre les trames ChaChaPoly.

Ceci utilise les 9 premiers octets de l'en-tête I2NP NTCP standard, et supprime les 7 derniers octets de l'en-tête, comme suit : raccourcir l'expiration de 8 à 4 octets (secondes au lieu de millisecondes, comme pour SSU), supprimer la longueur de 2 octets (utiliser la taille du bloc - 9), et supprimer la somme de contrôle SHA256 d'un octet.

```
+----+----+----+----+----+----+----+----+
| 3  |  size   |type|    msg id         |
+----+----+----+----+----+----+----+----+
|   short exp       |     message       |
+----+----+----+----+                   +
|                                       |
~               .   .   .               ~
|                                       |
+----+----+----+----+----+----+----+----+

blk :: 3
size :: 2 bytes, big endian, size of type + msg id + exp + message to follow
        I2NP message body size is (size - 9).
type :: 1 byte, I2NP msg type, see I2NP spec
msg id :: 4 bytes, big endian, I2NP message ID
short exp :: 4 bytes, big endian, I2NP message expiration, Unix timestamp, unsigned seconds.
             Wraps around in 2106
message :: I2NP message body
```
#### Notes

- Les implémenteurs doivent s'assurer que lors de la lecture d'un bloc, des données mal formées ou malveillantes ne provoqueront pas de débordement de lecture dans le bloc suivant.

#### Terminaison

Noise recommande un message de terminaison explicite. Le NTCP original n'en a pas. Fermer la connexion. Ceci doit être le dernier bloc non-padding dans la trame.

```
+----+----+----+----+----+----+----+----+
| 4  |  size   |    valid data frames   |
+----+----+----+----+----+----+----+----+
    received   | rsn|     addl data     |
+----+----+----+----+                   +
~               .   .   .               ~
+----+----+----+----+----+----+----+----+

blk :: 4
size :: 2 bytes, big endian, value = 9 or more
valid data frames received :: The number of valid AEAD data phase frames received
                              (current receive nonce value)
                              0 if error occurs in handshake phase
                              8 bytes, big endian
rsn :: reason, 1 byte:
       0: normal close or unspecified
       1: termination received
       2: idle timeout
       3: router shutdown
       4: data phase AEAD failure
       5: incompatible options
       6: incompatible signature type
       7: clock skew
       8: padding violation
       9: AEAD framing error
       10: payload format error
       11: message 1 error
       12: message 2 error
       13: message 3 error
       14: intra-frame read timeout
       15: RI signature verification fail
       16: s parameter missing, invalid, or mismatched in RouterInfo
       17: banned
addl data :: optional, 0 or more bytes, for future expansion, debugging,
             or reason text.
             Format unspecified and may vary based on reason code.
```
#### Notes

Toutes les raisons ne peuvent pas être réellement utilisées, cela dépend de l'implémentation. Les échecs de handshake entraîneront généralement une fermeture avec TCP RST à la place. Voir les notes dans les sections des messages de handshake ci-dessus. Les raisons supplémentaires listées sont pour la cohérence, la journalisation, le débogage, ou en cas de changements de politique.

#### Remplissage

Ceci concerne le remplissage à l'intérieur des trames AEAD. Le remplissage pour les messages 1 et 2 se trouve à l'extérieur des trames AEAD. Tout le remplissage pour le message 3 et la phase de données se trouve à l'intérieur des trames AEAD.

Le padding à l'intérieur d'AEAD devrait approximativement respecter les paramètres négociés. Bob a envoyé ses paramètres tx/rx min/max demandés dans le message 2. Alice a envoyé ses paramètres tx/rx min/max demandés dans le message 3. Des options mises à jour peuvent être envoyées pendant la phase de données. Voir les informations sur le bloc d'options ci-dessus.

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
size :: 2 bytes, big endian, size of padding to follow
padding :: random data
```
#### Notes

- Taille = 0 est autorisée.
- Stratégies de remplissage à déterminer.
- Remplissage minimum à déterminer.
- Les trames de remplissage uniquement sont autorisées.
- Valeurs par défaut du remplissage à déterminer.
- Voir le bloc d'options pour la négociation des paramètres de remplissage
- Voir le bloc d'options pour les paramètres de remplissage min/max
- Noise limite les messages à 64KB. Si plus de remplissage est nécessaire, envoyer plusieurs trames.
- La réponse du router en cas de violation du remplissage négocié dépend de l'implémentation.

#### Autres types de blocs

Les implémentations doivent ignorer les types de blocs inconnus pour la compatibilité ascendante, sauf dans la partie 2 du message 3, où les blocs inconnus ne sont pas autorisés.

#### Travaux futurs

- La longueur du rembourrage doit être décidée soit au cas par cas pour chaque message avec des estimations de la distribution des longueurs, soit des délais aléatoires doivent être ajoutés. Ces contre-mesures doivent être incluses pour résister à l'inspection approfondie de paquets (DPI), car les tailles des messages révéleraient sinon que du trafic I2P est transporté par le protocole de transport. Le schéma de rembourrage exact constitue un domaine de travail futur.

### 5) Résiliation

Les connexions peuvent être fermées via une fermeture normale ou anormale du socket TCP, ou, comme Noise le recommande, un message de terminaison explicite. Le message de terminaison explicite est défini dans la phase de données ci-dessus.

Lors de toute terminaison normale ou anormale, les routers doivent remettre à zéro toutes les données éphémères en mémoire, y compris les clés éphémères de handshake, les clés cryptographiques symétriques et les informations associées.

## Informations du Router Publiées

### Capacités

À partir de la version 0.9.50, l'option "caps" est prise en charge dans les adresses NTCP2, similaire à SSU. Une ou plusieurs capacités peuvent être publiées dans l'option "caps". Les capacités peuvent être dans n'importe quel ordre, mais "46" est l'ordre recommandé, pour la cohérence entre les implémentations. Il y a deux capacités définies :

4: Indique la capacité IPv4 sortante. Si une IP est publiée dans le champ host, cette capacité n'est pas nécessaire. Si le router est caché, ou si NTCP2 est en sortie uniquement, '4' et '6' peuvent être combinés dans une seule adresse.

6: Indique la capacité IPv6 sortante. Si une IP est publiée dans le champ host, cette capacité n'est pas nécessaire. Si le router est caché, ou si NTCP2 est en sortie uniquement, '4' et '6' peuvent être combinés dans une seule adresse.

### Adresses publiées

L'adresse RouterAddress publiée (partie des RouterInfo) aura un identifiant de protocole soit "NTCP" soit "NTCP2".

Le RouterAddress doit contenir les options "host" et "port", comme dans le protocole NTCP actuel.

La RouterAddress doit contenir trois options pour indiquer le support NTCP2 :

- s=(Clé Base64) La clé publique statique Noise (s) actuelle pour cette RouterAddress. Encodée en Base 64 en utilisant l'alphabet I2P Base 64 standard. 32 octets en binaire, 44 octets encodés en Base 64, clé publique X25519 little-endian.
- i=(IV Base64) L'IV actuel pour chiffrer la valeur X dans le message 1 pour cette RouterAddress. Encodé en Base 64 en utilisant l'alphabet I2P Base 64 standard. 16 octets en binaire, 24 octets encodés en Base 64, big-endian.
- v=2 La version actuelle (2). Lorsque publié comme "NTCP", un support additionnel pour la version 1 est implicite. Le support pour les versions futures se fera avec des valeurs séparées par des virgules, par exemple v=2,3. L'implémentation doit vérifier la compatibilité, incluant les versions multiples si une virgule est présente. Les versions séparées par des virgules doivent être dans l'ordre numérique.

Alice doit vérifier que les trois options sont présentes et valides avant de se connecter en utilisant le protocole NTCP2.

Lorsqu'il est publié comme "NTCP" avec les options "s", "i" et "v", le router doit accepter les connexions entrantes sur cet hôte et ce port pour les protocoles NTCP et NTCP2, et détecter automatiquement la version du protocole.

Lorsqu'il est publié comme "NTCP2" avec les options "s", "i" et "v", le router accepte les connexions entrantes sur cet hôte et ce port pour le protocole NTCP2 uniquement.

Si un router prend en charge les connexions NTCP1 et NTCP2 mais n'implémente pas la détection automatique de version pour les connexions entrantes, il doit annoncer à la fois les adresses "NTCP" and "NTCP2", et inclure les options NTCP2 dans l'adresse "NTCP2" uniquement. Le router devrait définir une valeur de coût plus faible (priorité plus élevée) dans l'adresse "NTCP2" que dans l'adresse "NTCP", afin que NTCP2 soit préféré.

Si plusieurs NTCP2 RouterAddresses (soit comme "NTCP" ou "NTCP2") sont publiées dans le même RouterInfo (pour des adresses IP ou ports supplémentaires), toutes les adresses spécifiant le même port doivent contenir les options et valeurs NTCP2 identiques. En particulier, toutes doivent contenir la même clé statique et le même iv.

### Adresse NTCP2 non publiée

Si Alice ne publie pas son adresse NTCP2 (comme "NTCP" ou "NTCP2") pour les connexions entrantes, elle doit publier une adresse router "NTCP2" contenant uniquement sa clé statique et sa version NTCP2, afin que Bob puisse valider la clé après avoir reçu le RouterInfo d'Alice dans la partie 2 du message 3.

- s=(clé Base64) Comme défini ci-dessus pour les adresses publiées.
- v=2 Comme défini ci-dessus pour les adresses publiées.

Cette adresse de router ne contiendra pas les options "i", "host" ou "port", car elles ne sont pas requises pour les connexions NTCP2 sortantes. Le coût publié pour cette adresse n'a pas strictement d'importance, car elle est uniquement entrante ; cependant, il peut être utile aux autres routers si le coût est défini plus élevé (priorité plus faible) que les autres adresses. La valeur suggérée est 14.

Alice peut également simplement ajouter les options "s" et "v" à une adresse "NTCP" publiée existante.

### Rotation de la clé publique et de l'IV

En raison de la mise en cache des RouterInfos, les routers ne doivent pas faire la rotation de la clé publique statique ou de l'IV pendant que le router est en fonctionnement, que ce soit dans une adresse publiée ou non. Les routers doivent stocker de manière persistante cette clé et cet IV pour les réutiliser après un redémarrage immédiat, afin que les connexions entrantes continuent de fonctionner et que les temps de redémarrage ne soient pas exposés. Les routers doivent stocker de manière persistante, ou déterminer autrement, l'heure du dernier arrêt, afin que le temps d'arrêt précédent puisse être calculé au démarrage.

Sous réserve des préoccupations concernant l'exposition des heures de redémarrage, les routers peuvent effectuer une rotation de cette clé ou IV au démarrage si le router était précédemment arrêté pendant un certain temps (au moins quelques heures).

Si le router a des RouterAddresses NTCP2 publiées (en tant que NTCP ou NTCP2), le temps d'arrêt minimum avant la rotation devrait être beaucoup plus long, par exemple un mois, sauf si l'adresse IP locale a changé ou si le router "rekeys".

Si le router a des RouterAddresses SSU publiées, mais pas NTCP2 (en tant que NTCP ou NTCP2), le temps d'arrêt minimum avant la rotation devrait être plus long, par exemple un jour, sauf si l'adresse IP locale a changé ou si le router effectue un "rekeys". Ceci s'applique même si l'adresse SSU publiée a des introducers.

Si le router n'a pas de RouterAddresses publiées (NTCP, NTCP2, ou SSU), le temps d'arrêt minimum avant la rotation peut être aussi court que deux heures, même si l'adresse IP change, à moins que le router ne « renouvelle ses clés ».

Si le router "rekeys" vers un Router Hash différent, il devrait également générer une nouvelle clé noise et un nouvel IV.

Les implémentations doivent être conscientes que le changement de la clé publique statique ou de l'IV interdira les connexions NTCP2 entrantes des routeurs qui ont mis en cache une RouterInfo plus ancienne. La publication de RouterInfo, la sélection des pairs de tunnel (y compris OBGW et le saut le plus proche IB), la sélection de tunnel à zéro saut, la sélection de transport et d'autres stratégies d'implémentation doivent en tenir compte.

La rotation d'IV est soumise aux mêmes règles que la rotation de clés, sauf que les IV ne sont présents que dans les RouterAddresses publiées, il n'y a donc pas d'IV pour les routeurs cachés ou derrière un pare-feu. Si quoi que ce soit change (version, clé, options ?) il est recommandé que l'IV change également.

Note : Le temps d'arrêt minimum avant la regénération des clés peut être modifié pour assurer la santé du réseau et empêcher le reseeding par un router arrêté pendant une durée modérée.

## Détection de version

Lorsqu'il est publié comme "NTCP", le router doit automatiquement détecter la version du protocole pour les connexions entrantes.

Cette détection dépend de l'implémentation, mais voici quelques conseils généraux.

Pour détecter la version d'une connexion NTCP entrante, Bob procède comme suit :

- Attendre au moins 64 octets (taille minimale du message 1 NTCP2)

- Si les données initiales reçues font 288 octets ou plus, la connexion entrante est en version 1.

- Si moins de 288 octets, soit

> - Attendre un court moment pour plus de données (bonne stratégie avant l'adoption généralisée de NTCP2) si au moins 288 octets ont été reçus au total, c'est NTCP 1.   >   > - Essayer les premières étapes de décodage en version 2, si cela échoue, attendre un court moment pour plus de données (bonne stratégie après l'adoption généralisée de NTCP2)   >   >   > - Déchiffrer les 32 premiers octets (la clé X) du paquet SessionRequest en utilisant AES-256 avec la clé RH_B.   >   > - Vérifier un point valide sur la courbe. Si cela échoue, attendre un court moment pour plus de données pour NTCP 1   >   > - Vérifier la trame AEAD. Si cela échoue, attendre un court moment pour plus de données pour NTCP 1

Notez que des modifications ou des stratégies supplémentaires peuvent être recommandées si nous détectons des attaques de segmentation TCP actives sur NTCP 1.

Pour faciliter la détection rapide de version et l'établissement de liaison, les implémentations doivent s'assurer qu'Alice met en mémoire tampon puis transmet d'un coup tout le contenu du premier message, y compris le remplissage. Cela augmente la probabilité que les données soient contenues dans un seul paquet TCP (sauf si segmentées par l'OS ou des équipements intermédiaires), et reçues d'un coup par Bob. C'est aussi pour l'efficacité et pour garantir l'efficacité du remplissage aléatoire. Ceci s'applique aux établissements de liaison NTCP et NTCP2.

## Variantes, Solutions de Repli et Problèmes Généraux

- Si Alice et Bob prennent tous deux en charge NTCP2, Alice devrait se connecter avec NTCP2.
- Si Alice échoue à se connecter à Bob en utilisant NTCP2 pour une raison quelconque, la connexion échoue. Alice ne peut pas réessayer en utilisant NTCP 1.

## Directives sur la dérive d'horloge

Les horodatages des pairs sont inclus dans les deux premiers messages de négociation, Session Request et Session Created. Un décalage d'horloge entre deux pairs supérieur à +/- 60 secondes est généralement fatal. Si Bob pense que son horloge locale est incorrecte, il peut ajuster son horloge en utilisant le décalage calculé, ou une source externe. Sinon, Bob devrait répondre avec un Session Created même si le décalage maximum est dépassé, plutôt que de simplement fermer la connexion. Cela permet à Alice d'obtenir l'horodatage de Bob et de calculer le décalage, et de prendre des mesures si nécessaire. Bob n'a pas l'identité du router d'Alice à ce stade, mais pour préserver les ressources, il peut être souhaitable pour Bob de bannir les connexions entrantes depuis l'IP d'Alice pendant une certaine période, ou après des tentatives de connexion répétées avec un décalage excessif.

Alice devrait ajuster le décalage d'horloge calculé en soustrayant la moitié du RTT. Si Alice pense que son horloge locale est défaillante, elle peut ajuster son horloge en utilisant le décalage calculé, ou une source externe. Si Alice pense que l'horloge de Bob est défaillante, elle peut bannir Bob pendant une certaine période. Dans les deux cas, Alice devrait fermer la connexion.

Si Alice répond effectivement avec Session Confirmed (probablement parce que le décalage est très proche de la limite de 60s, et que les calculs d'Alice et Bob ne sont pas exactement identiques à cause du RTT), Bob devrait ajuster le décalage d'horloge calculé en soustrayant la moitié du RTT. Si le décalage d'horloge ajusté dépasse le maximum, Bob devrait alors répondre avec un message Disconnect contenant un code de raison de décalage d'horloge, et fermer la connexion. À ce stade, Bob a l'identité du router d'Alice, et peut bannir Alice pendant une certaine période.

## Références

- [Structures Communes](/docs/specs/common-structures)
- [I2NP](/docs/specs/i2np)
- [Base de Données Réseau](/docs/overview/network-database)
- [NOISE - Framework de Protocole Noise](https://noiseprotocol.org/noise.html)
- [NTCP](/docs/transport/ntcp)
- [Prop104](/proposals/104-tls-transport)
- [Prop109](/proposals/109-pt-transport)
- [Prop111](/proposals/111-ntcp-2)
- [RFC-2104 - HMAC](https://tools.ietf.org/html/rfc2104)
- [RFC-3526 - Groupes DH](https://tools.ietf.org/html/rfc3526)
- [RFC-6151](https://tools.ietf.org/html/rfc6151)
- [RFC-7539 - ChaCha20-Poly1305](https://tools.ietf.org/html/rfc7539)
- [RFC-7748 - X25519](https://tools.ietf.org/html/rfc7748)
- [RFC-7905](https://tools.ietf.org/html/rfc7905)
- [SipHash](https://www.131002.net/siphash/)
- [SSU](/docs/transport/ssu)
- **[STS]** Diffie, W.; van Oorschot P. C.; Wiener M. J., Authentification et Échanges de Clés Authentifiés
