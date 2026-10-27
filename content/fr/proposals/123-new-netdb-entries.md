---
title: "Nouvelles entrées netDB"
number: "123"
author: "zzz, str4d, orignal"
created: "2016-01-16"
lastupdated: "2020-07-18"
status: "Ouvrir"
thread: "http://zzz.i2p/topics/2051"
supercedes: "110, 120, 121, 122"
toc: true
---

## Statut

Certaines parties de cette proposition sont terminées et implémentées dans les versions 0.9.38 et 0.9.39.   Les spécifications des Structures Communes, I2CP, I2NP et autres   ont maintenant été mises à jour pour refléter les changements actuellement pris en charge.

Les parties terminées restent sujettes à de légères révisions.   D'autres parties de cette proposition sont encore en cours de développement   et sujettes à des révisions importantes.

La recherche de service (types 9 et 11) est une priorité faible,   non planifiée, et pourrait être séparée en une proposition distincte.

## Aperçu

Il s'agit d'une mise à jour et d'une agrégation des 4 propositions suivantes :

- 110 LS2
- 120 Meta LS2 pour multihébergement massif
- 121 LS2 Chiffré
- 122 Recherche de service non authentifiée (anycast)

Ces propositions sont principalement indépendantes, mais par souci de cohérence, nous définissons et utilisons un   format commun pour plusieurs d'entre elles.

Les propositions suivantes sont partiellement liées :

- 140 Multihébergement Invisible (incompatible avec cette proposition)
- 142 Nouveau Modèle de Cryptographie (pour une nouvelle cryptographie symétrique)
- 144 ECIES-X25519-AEAD-Ratchet
- 145 ECIES-P256
- 146 Red25519
- 148 EdDSA-BLAKE2b-Ed25519
- 149 B32 pour LS2 Chiffré
- 150 Protocole Garlic Farm
- 151 ECDSA Blinding

## Proposition

Cette proposition définit 5 nouveaux types DatabaseEntry et le processus pour   les stocker et les récupérer depuis la base de données du réseau,   ainsi que la méthode pour les signer et vérifier ces signatures.

### Objectifs

- Compatibilité ascendante
- LS2 utilisable avec le multihébergement ancien style
- Aucune nouvelle cryptographie ou primitive requise pour le support
- Maintenir la découplage entre crypto et signature ; supporter toutes les versions actuelles et futures
- Permettre des clés de signature hors ligne optionnelles
- Réduire la précision des horodatages pour limiter le fingerprinting
- Permettre une nouvelle cryptographie pour les destinations
- Permettre un multihébergement massif
- Corriger plusieurs problèmes avec le LS chiffré existant
- Option de masquage (blinding) pour réduire la visibilité par les floodfills
- Le chiffré supporte à la fois une clé unique et des clés multiples révocables
- Recherche de service pour faciliter la recherche de outproxies, le bootstrap DHT d'application,  
  et autres usages
- Ne rien casser qui dépend des hachages binaires de destination de 32 octets, par exemple bittorrent
- Ajouter de la flexibilité aux leasesets via des propriétés, comme nous en avons dans les routerinfos.
- Placer l'horodatage de publication et l'expiration variable dans l'en-tête, pour que cela fonctionne même  
  si le contenu est chiffré (ne pas dériver l'horodatage à partir de la location la plus ancienne)
- Tous les nouveaux types vivent dans le même espace DHT et aux mêmes emplacements que les leasesets existants,  
  afin que les utilisateurs puissent migrer du vieux LS vers LS2,  
  ou changer entre LS2, Meta et Chiffré,  
  sans changer la Destination ou son hachage.
- Une Destination existante peut être convertie pour utiliser des clés hors ligne,  
  ou revenir à des clés en ligne, sans changer la Destination ou son hachage.

### Non-objectifs / Hors-scope

- Nouvel algorithme de rotation DHT ou génération de nombres aléatoires partagés
- Le type de chiffrement spécifique et le schéma de chiffrement de bout en bout  
  utilisant ce nouveau type seraient dans une proposition séparée.  
  Aucune nouvelle cryptographie n'est spécifiée ou discutée ici.
- Nouveau chiffrement pour les RIs ou la construction de tunnels.  
  Ce serait dans une proposition séparée.
- Méthodes de chiffrement, transmission et réception des messages I2NP DLM / DSM / DSRM.  
  Non modifiées.
- Comment générer et gérer Meta, y compris la communication inter-routeurs, gestion, basculement et coordination.  
  Le support pourrait être ajouté à I2CP, ou i2pcontrol, ou un nouveau protocole.  
  Cela pourrait ou non être standardisé.
- Comment implémenter et gérer réellement des tunnels à expiration prolongée, ou annuler des tunnels existants.  
  C'est extrêmement difficile, et sans cela, vous ne pouvez pas avoir un arrêt gracieux raisonnable.
- Changements du modèle de menace
- Format de stockage hors ligne, ou méthodes pour stocker/récupérer/partager les données.
- Les détails d'implémentation ne sont pas discutés ici et sont laissés à chaque projet.

### Justification

LS2 ajoute des champs pour changer le type de chiffrement et pour les futurs changements de protocole.

LS2 Chiffré corrige plusieurs problèmes de sécurité du LS chiffré existant en   utilisant un chiffrement asymétrique de l'ensemble des locations.

Meta LS2 fournit un multihébergement flexible, efficace, performant et à grande échelle.

Les enregistrements et listes de service fournissent des services anycast tels que la recherche de noms   et le bootstrap DHT.

### Types de données NetDB

Les numéros de type sont utilisés dans les messages I2NP Database Lookup/Store.

La colonne « end-to-end » indique si les requêtes/réponses sont envoyées à une Destination dans un message Garlic.

Types existants :

| NetDB Data | Lookup Type | Store Type |
|------------|-------------|------------|
| any        | 0           | any        |
| LS         | 1           | 1          |
| RI         | 2           | 0          |
| exploratory| 3           | DSRM       |
Nouveaux types :

| NetDB Data     | Lookup Type | Store Type | Std. LS2 Header? | Sent end-to-end? |
|----------------|-------------|------------|------------------|------------------|
| LS2            | 1           | 3          | yes              | yes              |
| Encrypted LS2  | 1           | 5          | no               | no               |
| Meta LS2       | 1           | 7          | yes              | no               |
| Service Record | n/a         | 9          | yes              | no               |
| Service List   | 4           | 11         | no               | no               |
### Notes

- Les types de recherche sont actuellement les bits 3-2 du message Database Lookup.  
  Tout type supplémentaire nécessiterait l'utilisation du bit 4.

- Tous les types de stockage sont impairs car les bits supérieurs du champ type dans le message Database Store  
  sont ignorés par les anciens routeurs.  
  Nous préférons que l'analyse échoue comme un LS plutôt que comme un RI compressé.

- Le type doit-il être explicite, implicite ou ni l'un ni l'autre dans les données couvertes par la signature ?

### Processus de recherche / stockage

Les types 3, 5 et 7 peuvent être retournés en réponse à une recherche standard de leaseset (type 1).   Le type 9 n'est jamais retourné en réponse à une recherche.   Le type 11 est retourné en réponse à un nouveau type de recherche de service (type 11).

Seul le type 3 peut être envoyé dans un message Garlic client-à-client.

### Format

Les types 3, 7 et 9 ont un format commun ::

```text
Standard LS2 Header
- as defined below

Type-Specific Part
- as defined below in each part

Standard LS2 Signature:
- Length as implied by sig type of signing key
```
En-tête standard LS2

Partie spécifique au type

### Considérations de confidentialité/sécurité

Signature standard LS2 :

## En-tête standard LS2

Le type 5 (Chiffré) ne commence pas par une Destination et a un   format différent. Voir ci-dessous.

### Format

```
Standard LS2 Header:
  - Type (1 byte)
    Not actually in header, but part of data covered by signature.
    Take from field in Database Store Message.
  - Destination (387+ bytes)
  - Published timestamp (4 bytes, big endian, seconds since epoch, rolls over in 2106)
  - Expires (2 bytes, big endian) (offset from published timestamp in seconds, 18.2 hours max)
  - Flags (2 bytes)
    Bit order: 15 14 ... 3 2 1 0
    Bit 0: If 0, no offline keys; if 1, offline keys
    Bit 1: If 0, a standard published leaseset.
           If 1, an unpublished leaseset. Should not be flooded, published, or
           sent in response to a query. If this leaseset expires, do not query the
           netdb for a new one, unless bit 2 is set.
    Bit 2: If 0, a standard published leaseset.
           If 1, this unencrypted leaseset will be blinded and encrypted when published.
           If this leaseset expires, query the blinded location in the netdb for a new one.
           If this bit is set to 1, set bit 1 to 1 also.
           As of release 0.9.42.
    Bits 3-15: set to 0 for compatibility with future uses
  - If flag indicates offline keys, the offline signature section:
    Expires timestamp (4 bytes, big endian, seconds since epoch, rolls over in 2106)
    Transient sig type (2 bytes, big endian)
    Transient signing public key (length as implied by sig type)
    Signature of expires timestamp, transient sig type, and public key,
    by the destination public key,
    length as implied by destination public key sig type.
    This section can, and should, be generated offline.
```
### Justification

  - tel que défini ci-dessous

  - tel que défini ci-dessous pour chaque partie

  - Longueur implicite par le type de signature de la clé de signature

- Non publié/publié : À utiliser lors de l'envoi d'un stockage de base de données de bout en bout,  
  le routeur émetteur peut souhaiter indiquer que ce leaseset ne doit pas être  
  envoyé à d'autres. Nous utilisons actuellement des heuristiques pour maintenir cet état.

### Problèmes

- Publié : Remplace la logique complexe nécessaire pour déterminer la « version » du  
  leaseset. Actuellement, la version est l'expiration de la location expirant en dernier, et un routeur de publication doit incrémenter cette expiration d'au moins 1 ms lorsqu'il  
  publie un leaseset qui supprime uniquement une ancienne location.

- Expiration : Permet à l'expiration d'une entrée netdb d'être antérieure à celle de  
  sa location expirant en dernier. Peut ne pas être utile pour LS2, où les leasesets  
  sont censés rester avec une expiration maximale de 11 minutes, mais  
  pour d'autres nouveaux types, c'est nécessaire (voir Meta LS et Service Record ci-dessous).

- Les clés hors ligne sont optionnelles, pour réduire la complexité initiale/requise de l'implémentation.

### Notes

- Pourrait réduire encore plus la précision de l'horodatage (10 minutes ?) mais devrait ajouter  
  un numéro de version. Cela pourrait casser le multihébergement, sauf si nous avons un chiffrement préservant l'ordre ?  
  Probablement impossible sans horodatages du tout.

- Alternative : horodatage de 3 octets (époque / 10 minutes), version de 1 octet, expiration de 2 octets

- Le type est-il explicite ou implicite dans les données / signature ? Constantes « Domaine » pour la signature ?

## Nouveaux types DatabaseEntry

### LeaseSet 2

Le type 11 (Service List) est une agrégation de plusieurs Service Records et a un   format différent. Voir ci-dessous.

- Les routeurs ne devraient pas publier un LS plus d'une fois par seconde.  
  S'ils le font, ils doivent artificiellement incrémenter l'horodatage de publication de 1  
  par rapport au LS précédemment publié.

TBD

    Standard LS flag (1)
Les types 3, 7 et 9 utilisent l'en-tête standard LS2, spécifié ci-dessous :

    Standard LS2 type (3)
Changements par rapport au LeaseSet existant :

    Hash of destination
    This hash is then used to generate the daily "routing key", as in LS1
Recherche avec

    10 minutes, as in a regular LS.
Stockage avec

    Destination

### Format

```
Standard LS2 Header as specified above

  Standard LS2 Type-Specific Part
  - Properties (Mapping as specified in common structures spec, 2 zero bytes if none)
  - Number of key sections to follow (1 byte, max TBD)
  - Key sections:
    - Encryption type (2 bytes, big endian)
    - Encryption key length (2 bytes, big endian)
      This is explicit, so floodfills can parse LS2 with unknown encryption types.
    - Encryption key (number of bytes specified)
  - Number of lease2s (1 byte)
  - Lease2s (40 bytes each)
    These are leases, but with a 4-byte instead of an 8-byte expiration,
    seconds since the epoch (rolls over in 2106)

  Standard LS2 Signature:
  - Signature
    If flag indicates offline keys, this is signed by the transient pubkey,
    otherwise, by the destination pubkey
    Length as implied by sig type of signing key
    The signature is of everything above.
```
### Justification

- Les implémentations de routeurs pourraient mettre en cache les clés temporaires et la signature pour  
  éviter la vérification à chaque fois. En particulier, les floodfills et les routeurs aux  
  deux extrémités de connexions longues pourraient bénéficier de cela.

- Les clés et signature hors ligne ne conviennent que pour les destinations à longue durée de vie,  
  c'est-à-dire les serveurs, pas les clients.

### Discussion

Stockage à

Expiration typique

Publié par

- Ajout de l'horodatage de publication, de l'horodatage d'expiration, des flags et des propriétés
- Ajout du type de chiffrement
- Suppression de la clé de révocation

Cette proposition continue d'utiliser la clé publique dans le leaseset comme clé de chiffrement de bout en bout, et laisse le champ de clé publique dans la   Destination inutilisé, comme actuellement. Le type de chiffrement n'est pas spécifié   dans le certificat de clé de Destination, il restera 0.

- Propriétés : Extension et flexibilité futures.  
  Placées en premier au cas où nécessaires pour l'analyse des données restantes.

### Nouveaux problèmes de chiffrement

Une alternative rejetée consiste à spécifier le type de chiffrement dans le certificat de clé de Destination,   utiliser la clé publique dans la Destination, et ne pas utiliser la clé publique   dans le leaseset. Nous n'avons pas l'intention de faire cela.

- Plusieurs paires type de chiffrement/clé publique sont  
  destinées à faciliter la transition vers de nouveaux types de chiffrement. L'autre façon de faire  
  est de publier plusieurs leasesets, éventuellement en utilisant les mêmes tunnels,  
  comme nous le faisons actuellement pour les destinations DSA et EdDSA.  
  L'identification du type de chiffrement entrant sur un tunnel  
  peut être faite avec le mécanisme existant de session tag,  
  et/ou par déchiffrement d'essai avec chaque clé. La longueur des messages entrants  
  peut également fournir un indice.

- L'emplacement de la clé publique réelle ne change pas.
- Le type de chiffrement ou la clé publique peut changer sans changer la Destination.
- Supprime le champ de révocation inutilisé
- Compatibilité de base avec d'autres types DatabaseEntry dans cette proposition
- Permet plusieurs types de chiffrement

- L'emplacement de la clé publique et du type de chiffrement diffère de RouterInfo
- Maintient la clé publique inutilisée dans le leaseset
- Nécessite une implémentation à travers le réseau ; dans l'alternative, des types de chiffrement expérimentaux peuvent être utilisés, si autorisés par les floodfills  
  (mais voir les propositions connexes 136 et 137 concernant le support des types de signature expérimentaux).  
  La proposition alternative pourrait être plus facile à implémenter et tester pour des types de chiffrement expérimentaux.

### Notes

- Le type de chiffrement représente la combinaison  
  de courbe, longueur de clé et schéma de bout en bout,  
  incluant KDF et MAC, le cas échéant.

- Nous avons inclus un champ de longueur de clé, afin que le LS2 soit  
  analysable et vérifiable par le floodfill même pour des types de chiffrement inconnus.

- Le premier nouveau type de chiffrement proposé sera  
  probablement ECIES/X25519. Comment il est utilisé de bout en bout  
  (soit une version légèrement modifiée d'ElGamal/AES+SessionTag  
  soit quelque chose de complètement nouveau, par exemple ChaCha/Poly) sera spécifié  
  dans une ou plusieurs propositions séparées.  
  Voir aussi les propositions ECIES 144 et 145.

### LS2 Chiffré

Avantages de LS2 :

- L'expiration de 8 octets dans les locations passe à 4 octets.

Inconvénients de LS2 :

Certains points sont hors-scope pour cette proposition,   mais nous mettons ici des notes car nous n'avons pas encore   de proposition de chiffrement séparée.   Voir aussi les propositions ECIES 144 et 145.

- Si nous implémentons jamais la révocation, nous pouvons le faire avec un champ d'expiration à zéro,  
  ou des locations nulles, ou les deux. Pas besoin d'une clé de révocation séparée.

Objectifs :

    Standard LS flag (1)
Le LS2 chiffré n'est jamais envoyé dans un message garlic de bout en bout.   Utilisez le LS2 standard comme ci-dessus.

    Encrypted LS2 type (5)
Changements par rapport au LeaseSet chiffré existant :

    Hash of blinded sig type and blinded public key
    Two byte sig type (big endian, e.g. 0x000b) || blinded public key
    This hash is then used to generate the daily "routing key", as in LS1
Recherche avec

    10 minutes, as in a regular LS, or hours, as in a meta LS.
Stockage avec

    Destination


### Définitions

Stockage à

Expiration typique

    n-byte output from a cryptographically-secure random number generator.

    In addition to the requirement of CSRNG being cryptographically-secure (and thus
    suitable for generating key material), it MUST be safe
    for some n-byte output to be used for key material when the byte sequences immediately
    preceding and following it are exposed on the network (such as in a salt, or encrypted
    padding). Implementations that rely on a potentially-untrustworthy source should hash
    any output that is to be exposed on the network. See [PRNG references](http://projectbullrun.org/dual-ec/ext-rand.html) and [Tor dev discussion](https://lists.torproject.org/pipermail/tor-dev/2015-November/009954.html).

Publié par

    SHA-256 hash function that takes a personalization string p and data d, and
    produces an output of length 32 bytes.

    Use SHA-256 as follows::

        H(p, d) := SHA-256(p || d)

Nous définissons les fonctions suivantes correspondant aux blocs cryptographiques utilisés   pour le LS2 chiffré :

    The ChaCha20 stream cipher as specified in [RFC 7539 Section 2.4](https://tools.ietf.org/html/rfc7539#section-2.4), with the initial counter
    set to 1. S_KEY_LEN = 32 and S_IV_LEN = 12.

    ENCRYPT(k, iv, plaintext)
        Encrypts plaintext using the cipher key k, and nonce iv which MUST be unique for
        the key k. Returns a ciphertext that is the same size as the plaintext.

        The entire ciphertext must be indistinguishable from random if the key is secret.

    DECRYPT(k, iv, ciphertext)
        Decrypts ciphertext using the cipher key k, and nonce iv. Returns the plaintext.


CSRNG(n)

    The RedDSA signature scheme (corresponding to SigType 11) with key blinding.
    It has the following functions:

    DERIVE_PUBLIC(privkey)
        Returns the public key corresponding to the given private key.

    SIGN(privkey, m)
        Returns a signature by the private key privkey over the given message m.

    VERIFY(pubkey, m, sig)
        Verifies the signature sig against the public key pubkey and message m. Returns
        true if the signature is valid, false otherwise.

    It must also support the following key blinding operations:

    GENERATE_ALPHA(data, secret)
        Generate alpha for those who know the data and an optional secret.
        The result must be identically distributed as the private keys.

    BLIND_PRIVKEY(privkey, alpha)
        Blinds a private key, using a secret alpha.

    BLIND_PUBKEY(pubkey, alpha)
        Blinds a public key, using a secret alpha.
        For a given keypair (privkey, pubkey) the following relationship holds::

            BLIND_PUBKEY(pubkey, alpha) ==
            DERIVE_PUBLIC(BLIND_PRIVKEY(privkey, alpha))

H(p, d)

    X25519 public key agreement system. Private keys of 32 bytes, public keys of 32
    bytes, produces outputs of 32 bytes. It has the following
    functions:

    GENERATE_PRIVATE()
        Generates a new private key.

    DERIVE_PUBLIC(privkey)
        Returns the public key corresponding to the given private key.

    DH(privkey, pubkey)
        Generates a shared secret from the given private and public keys.

STREAM

    A cryptographic key derivation function which takes some input key material ikm (which
    should have good entropy but is not required to be a uniformly random string), a salt
    of length 32 bytes, and a context-specific 'info' value, and produces an output
    of n bytes suitable for use as key material.

    Use HKDF as specified in [RFC 5869](https://tools.ietf.org/html/rfc5869), using the HMAC hash function SHA-256
    as specified in [RFC 2104](https://tools.ietf.org/html/rfc2104). This means that SALT_LEN is 32 bytes max.


### Format

SIG

- Les clés de chiffrement sont dans l'ordre de préférence du serveur, la plus préférée en premier.  
  Le comportement par défaut du client est de sélectionner la première clé avec  
  un type de chiffrement pris en charge. Les clients peuvent utiliser d'autres algorithmes de sélection  
  basés sur le support du chiffrement, les performances relatives et d'autres facteurs.

DH

    Layer 0 data + Enc(layer 1 data + Enc(layer 2 data)) + Signature

HKDF(salt, ikm, info, n)

Le format du LS2 chiffré consiste en trois couches imbriquées :

#### Couche 0 (externe)

Le format global ressemble à ::

    1 byte

    Not actually in header, but part of data covered by signature.
    Take from field in Database Store Message.

Notez que le LS2 chiffré est masqué. La Destination n'est pas dans l'en-tête.   L'emplacement de stockage DHT est SHA-256(type de signature || clé publique masquée), et tourne quotidiennement.

    2 bytes, big endian
    This will always be type 11, identifying a Red25519 blinded key.

N'utilise PAS l'en-tête LS2 standard spécifié ci-dessus.

    Length as implied by sig type

Type

    4 bytes, big endian

    Seconds since epoch, rolls over in 2106

Type de signature de la clé publique masquée

    2 bytes, big endian

    Offset from published timestamp in seconds, 18.2 hours max

Clé publique masquée

    2 bytes

    Bit order: 15 14 ... 3 2 1 0

    Bit 0: If 0, no offline keys; if 1, offline keys

    Other bits: set to 0 for compatibility with future uses

Horodatage de publication

    Present if flag indicates offline keys

    Expires timestamp
        4 bytes, big endian

        Seconds since epoch, rolls over in 2106

    Transient sig type
        2 bytes, big endian

    Transient signing public key
        Length as implied by sig type

    Signature
        Length as implied by blinded public key sig type

        Over expires timestamp, transient sig type, and transient public key.

        Verified with the blinded public key.

Expiration

    2 bytes, big endian

Flags

    lenOuterCiphertext bytes

    Encrypted layer 1 data. See below for key derivation and encryption algorithms.

Données de clé temporaire

    Length as implied by sig type of the signing key used

    The signature is of everything above.

    If the flag indicates offline keys, the signature is verified with the transient
    public key. Otherwise, the signature is verified with the blinded public key.


#### Couche 1 (intermédiaire)

lenOuterCiphertext

    1 byte
    
    Bit order: 76543210

    Bit 0: 0 for everybody, 1 for per-client, auth section to follow

    Bits 3-1: Authentication scheme, only if bit 0 is set to 1 for per-client, otherwise 000
              000: DH client authentication (or no per-client authentication)
              001: PSK client authentication

    Bits 7-4: Unused, set to 0 for future compatibility

outerCiphertext

    Present if flag bit 0 is set to 1 and flag bits 3-1 are set to 000.

    ephemeralPublicKey
        32 bytes

    clients
        2 bytes, big endian

        Number of authClient entries to follow, 40 bytes each

    authClient
        Authorization data for a single client.
        See below for the per-client authorization algorithm.

        clientID_i
            8 bytes

        clientCookie_i
            32 bytes

Signature

    Present if flag bit 0 is set to 1 and flag bits 3-1 are set to 001.

    authSalt
        32 bytes

    clients
        2 bytes, big endian

        Number of authClient entries to follow, 40 bytes each

    authClient
        Authorization data for a single client.
        See below for the per-client authorization algorithm.

        clientID_i
            8 bytes

        clientCookie_i
            32 bytes


Flags

    Length implied by lenOuterCiphertext (whatever data remains)

    Encrypted layer 2 data. See below for key derivation and encryption algorithms.


#### Couche 2 (interne)

Données d'auth DH client

    1 byte

    Either 3 (LS2) or 7 (Meta LS2)

Données d'auth PSK client

    LeaseSet2 data for the given type.

    Includes the header and signature.


### Dérivation de clé masquée

innerCiphertext

Type

#### Objectifs

- Ajouter le masquage (blinding)
- Permettre plusieurs types de signature
- Ne pas nécessiter de nouvelles primitives cryptographiques
- Chiffrer éventuellement à chaque destinataire, révocable
- Supporter le chiffrement de LS2 standard et Meta LS2 uniquement

#### Sécurité

Données

#### Définitions

Nous utilisons le schéma suivant pour le masquage de clé,   basé sur Ed25519 et [ZCash RedDSA](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf).   Les signatures Re25519 sont sur la courbe Ed25519, en utilisant SHA-512 pour le hachage.

    The Ed25519 base point (generator) 2^255 - 19 as in [Ed25519](http://cr.yp.to/papers.html#ed25519)

Nous n'utilisons pas [Tor's rend-spec-v3.txt appendix A.2](https://spec.torproject.org/rend-spec-v3),   qui a des objectifs de conception similaires, car ses clés publiques masquées   peuvent être en dehors du sous-groupe d'ordre premier, avec des implications de sécurité inconnues.

    The Ed25519 order 2^252 + 27742317777372353535851937790883648493
    as in [Ed25519](http://cr.yp.to/papers.html#ed25519)

La sécurité d'un schéma de masquage exige que la   distribution d'alpha soit la même que celle des clés privées non masquées.   Cependant, lorsque nous masquons une clé privée Ed25519 (type de signature 7)   vers une clé privée Red25519 (type de signature 11), la distribution est différente.   Pour répondre aux exigences de [zcash section 4.1.6.1](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf),   Red25519 (type de signature 11) devrait être utilisé pour les clés non masquées également, afin que   « la combinaison d'une clé publique ré-randomisée et de signature(s)   sous cette clé ne révèle pas la clé à partir de laquelle elle a été ré-randomisée ».   Nous autorisons le type 7 pour les destinations existantes, mais recommandons   le type 11 pour les nouvelles destinations qui seront chiffrées.

    Convert a private key to public, as in Ed25519 (mulitply by G)

B

    A 32-byte random number known to those who know the destination.

L

    Generate alpha for the current date, for those who know the destination and the secret.
    The result must be identically distributed as Ed25519 private keys.

DERIVE_PUBLIC(a)

    The unblinded 32-byte EdDSA or RedDSA signing private key used to sign the destination

alpha

    The unblinded 32-byte EdDSA or RedDSA signing public key in the destination,
    = DERIVE_PUBLIC(a), as in Ed25519

GENERATE_ALPHA(destination, date, secret)

    The blinded 32-byte EdDSA signing private key used to sign the encrypted leaseset
    This is a valid EdDSA private key.

a

    The blinded 32-byte EdDSA signing public key in the Destination,
    may be generated with DERIVE_PUBLIC(a'), or from A and alpha.
    This is a valid EdDSA public key, on the curve and on the prime-order subgroup.

A

    Flip the order of the input bytes to little-endian

a'

    32 bytes = (LEOS2IP(SHA512(x))) mod B, same as in Ed25519 hash-and-reduce


#### Calculs de masquage

A'

LEOS2IP(x)

```text
// GENERATE_ALPHA(destination, date, secret)

  // secret is optional, else zero-length
  A = destination's signing public key
  stA = signature type of A, 2 bytes big endian (0x0007 or 0x000b)
  stA' = signature type of blinded public key A', 2 bytes big endian (0x000b)
  keydata = A || stA || stA'
  datestring = 8 bytes ASCII YYYYMMDD from the current date UTC
  secret = UTF-8 encoded string
  seed = HKDF(H("I2PGenerateAlpha", keydata), datestring || secret, "i2pblinding1", 64)
  // treat seed as a 64 byte little-endian value
  alpha = seed mod L
```
H*(x)

```text
// BLIND_PRIVKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  // If for a Ed25519 private key (type 7)
  seed = destination's signing private key
  a = left half of SHA512(seed) and clamped as usual for Ed25519
  // else, for a Red25519 private key (type 11)
  a = destination's signing private key
  // Addition using scalar arithmentic
  blinded signing private key = a' = BLIND_PRIVKEY(a, alpha) = (a + alpha) mod L
  blinded signing public key = A' = DERIVE_PUBLIC(a')
```
Un nouveau secret alpha et des clés masquées doivent être générés chaque jour (UTC).   Le secret alpha et les clés masquées sont calculés comme suit.

```text
// BLIND_PUBKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  A = destination's signing public key
  // Addition using group elements (points on the curve)
  blinded public key = A' = BLIND_PUBKEY(A, alpha) = A + DERIVE_PUBLIC(alpha)
```
GENERATE_ALPHA(destination, date, secret), pour toutes les parties :

#### Signature

BLIND_PRIVKEY(), pour le propriétaire publiant le leaseset :

BLIND_PUBKEY(), pour les clients récupérant le leaseset :

Les deux méthodes de calcul de A' donnent le même résultat, comme requis.

Le leaseset non masqué est signé par la clé privée de signature Ed25519 ou Red25519 non masquée   et vérifié avec la clé publique de signature Ed25519 ou Red25519 non masquée (types de signature 7 ou 11) comme d'habitude.

#### Calculs de signature/vérification

Si la clé publique de signature est hors ligne,   le leaseset non masqué est signé par la clé privée de signature temporaire Ed25519 ou Red25519 non masquée   et vérifié avec la clé publique de signature temporaire Ed25519 ou Red25519 non masquée (types de signature 7 ou 11) comme d'habitude.   Voir ci-dessous pour des notes supplémentaires sur les clés hors ligne pour les leasesets chiffrés.

Pour la signature du leaseset chiffré, nous utilisons Red25519, basé sur [RedDSA](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf)   pour signer et vérifier avec des clés masquées.   Les signatures Red25519 sont sur la courbe Ed25519, en utilisant SHA-512 pour le hachage.

Red25519 est identique à Ed25519 standard sauf spécifié ci-dessous.

La partie externe du leaseset chiffré utilise des clés et signatures Red25519.

Red25519 est presque identique à Ed25519. Deux différences :

```text
T = 80 random bytes
  r = H*(T || publickey || message)
  // rest is the same as in Ed25519
```
Les clés privées Red25519 sont générées à partir de nombres aléatoires puis doivent être réduites mod L, où L est défini ci-dessus.   Les clés privées Ed25519 sont générées à partir de nombres aléatoires puis « clampées » en utilisant   un masquage bit à bit sur les octets 0 et 31. Cela n'est pas fait pour Red25519.   Les fonctions GENERATE_ALPHA() et BLIND_PRIVKEY() définies ci-dessus génèrent des clés privées Red25519 correctes en utilisant mod L.

```text
// same as in Ed25519
```
### Chiffrement et traitement

#### Dérivation des sous-identifiants

Dans Red25519, le calcul de r pour la signature utilise des données aléatoires supplémentaires,   et utilise la valeur de la clé publique plutôt que le hachage de la clé privée.   À cause des données aléatoires, chaque signature Red25519 est différente, même   en signant les mêmes données avec la même clé.

```text
A = destination's signing public key
  stA = signature type of A, 2 bytes big endian (0x0007 or 0x000b)
  stA' = signature type of A', 2 bytes big endian (0x000b)
  keydata = A || stA || stA'
  credential = H("credential", keydata)
```
Signature :

Vérification :

```text
subcredential = H("subcredential", credential || blindedPublicKey)
```
Dans le cadre du processus de masquage, nous devons nous assurer qu'un LS2 chiffré ne peut être   déchiffré que par quelqu'un qui connaît la clé publique de signature de la Destination correspondante.   La Destination complète n'est pas requise.   Pour y parvenir, nous dérivons un identifiant à partir de la clé publique de signature :

#### Chiffrement couche 1

La chaîne de personnalisation garantit que l'identifiant ne collisionne avec aucun hachage utilisé   comme clé de recherche DHT, comme le hachage de Destination brut.

```text
outerInput = subcredential || publishedTimestamp
```
Pour une clé masquée donnée, nous pouvons ensuite dériver un sous-identifiant :

```text
outerSalt = CSRNG(32)
```
Le sous-identifiant est inclus dans les processus de dérivation de clé ci-dessous, ce qui lie ces   clés à la connaissance de la clé publique de signature de la Destination.

```text
keys = HKDF(outerSalt, outerInput, "ELS2_L1K", 44)
  outerKey = keys[0:31]
  outerIV = keys[32:43]
```
D'abord, l'entrée pour le processus de dérivation de clé est préparée :

```text
outerCiphertext = outerSalt || ENCRYPT(outerKey, outerIV, outerPlaintext)
```
#### Déchiffrement couche 1

Ensuite, un sel aléatoire est généré :

```text
outerSalt = outerCiphertext[0:31]
```
Puis la clé utilisée pour chiffrer la couche 1 est dérivée :

```text
outerInput = subcredential || publishedTimestamp
  keys = HKDF(outerSalt, outerInput, "ELS2_L1K", 44)
  outerKey = keys[0:31]
  outerIV = keys[32:43]
```
Enfin, le texte clair de la couche 1 est chiffré et sérialisé :

```text
outerPlaintext = DECRYPT(outerKey, outerIV, outerCiphertext[32:end])
```
#### Chiffrement couche 2

Le sel est analysé à partir du texte chiffré de la couche 1 :

Puis la clé utilisée pour chiffrer la couche 1 est dérivée :

```text
innerInput = authCookie || subcredential || publishedTimestamp
  innerSalt = CSRNG(32)
  keys = HKDF(innerSalt, innerInput, "ELS2_L2K", 44)
  innerKey = keys[0:31]
  innerIV = keys[32:43]
  innerCiphertext = innerSalt || ENCRYPT(innerKey, innerIV, innerPlaintext)
```
#### Déchiffrement couche 2

Enfin, le texte chiffré de la couche 1 est déchiffré :

Lorsque l'autorisation client est activée, ``authCookie`` est calculé comme décrit ci-dessous.   Lorsque l'autorisation client est désactivée, ``authCookie`` est un tableau d'octets de longueur nulle.

```text
innerInput = authCookie || subcredential || publishedTimestamp
  innerSalt = innerCiphertext[0:31]
  keys = HKDF(innerSalt, innerInput, "ELS2_L2K", 44)
  innerKey = keys[0:31]
  innerIV = keys[32:43]
  innerPlaintext = DECRYPT(innerKey, innerIV, innerCiphertext[32:end])
```
### Autorisation par-client

Le chiffrement procède de manière similaire à la couche 1 :

Lorsque l'autorisation client est activée, ``authCookie`` est calculé comme décrit ci-dessous.   Lorsque l'autorisation client est désactivée, ``authCookie`` est un tableau d'octets de longueur nulle.

#### Autorisation client DH

Le déchiffrement procède de manière similaire à la couche 1 :

Lorsque l'autorisation client est activée pour une Destination, le serveur maintient une liste de   clients qu'il autorise à déchiffrer les données du LS2 chiffré. Les données stockées par-client   dépendent du mécanisme d'autorisation, et incluent une forme de matériel de clé que chaque   client génère et envoie au serveur via un mécanisme sécurisé hors bande.

```text
authCookie = CSRNG(32)
  esk = GENERATE_PRIVATE()
  epk = DERIVE_PUBLIC(esk)
```
Il existe deux alternatives pour implémenter l'autorisation par-client :

```text
sharedSecret = DH(esk, cpk_i)
  authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
  okm = HKDF(epk, authInput, "ELS2_XCA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
  clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
```
Chaque client génère une paire de clés DH ``[csk_i, cpk_i]``, et envoie la clé publique ``cpk_i``   au serveur.

Traitement du serveur   ^^^^^^^^^^^^^^^^^ Le serveur génère un nouveau ``authCookie`` et une paire de clés DH éphémère :

```text
sharedSecret = DH(csk_i, epk)
  authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
  okm = HKDF(epk, authInput, "ELS2_XCA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
```
Puis pour chaque client autorisé, le serveur chiffre ``authCookie`` à sa clé publique :

```text
authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie_i)
```
#### Autorisation client par clé pré-partagée (PSK)

Le serveur place chaque tuple ``[clientID_i, clientCookie_i]`` dans la couche 1 du   LS2 chiffré, avec ``epk``.

Traitement du client   ^^^^^^^^^^^^^^^^^ Le client utilise sa clé privée pour dériver son identifiant client attendu ``clientID_i``,   la clé de chiffrement ``clientKey_i``, et le vecteur d'initialisation ``clientIV_i`` :

```text
authCookie = CSRNG(32)
  authSalt = CSRNG(32)
```
Puis le client recherche dans les données d'autorisation de la couche 1 une entrée contenant   ``clientID_i``. Si une entrée correspondante existe, le client la déchiffre pour obtenir   ``authCookie`` :

```text
authInput = psk_i || subcredential || publishedTimestamp
  okm = HKDF(authSalt, authInput, "ELS2PSKA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
  clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
```
Chaque client génère une clé secrète de 32 octets ``psk_i``, et l'envoie au serveur.   Alternativement, le serveur peut générer la clé secrète, et l'envoyer à un ou plusieurs clients.

Traitement du serveur   ^^^^^^^^^^^^^^^^^ Le serveur génère un nouveau ``authCookie`` et un sel :

```text
authInput = psk_i || subcredential || publishedTimestamp
  okm = HKDF(authSalt, authInput, "ELS2PSKA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
```
Puis pour chaque client autorisé, le serveur chiffre ``authCookie`` à sa clé pré-partagée :

```text
authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie_i)
```
#### Considérations de sécurité

Le serveur place chaque tuple ``[clientID_i, clientCookie_i]`` dans la couche 1 du   LS2 chiffré, avec ``authSalt``.

Traitement du client   ^^^^^^^^^^^^^^^^^ Le client utilise sa clé pré-partagée pour dériver son identifiant client attendu ``clientID_i``,   la clé de chiffrement ``clientKey_i``, et le vecteur d'initialisation ``clientIV_i`` :

Puis le client recherche dans les données d'autorisation de la couche 1 une entrée contenant   ``clientID_i``. Si une entrée correspondante existe, le client la déchiffre pour obtenir   ``authCookie`` :

Les deux mécanismes d'autorisation client ci-dessus fournissent une confidentialité pour l'appartenance aux clients.   Une entité qui connaît uniquement la Destination peut voir combien de clients sont abonnés à tout   moment, mais ne peut pas suivre quels clients sont ajoutés ou révoqués.

- Chiffrer l'ensemble pour la sécurité
- Chiffrer de manière sécurisée, pas seulement avec AES.
- Chiffrer à chaque destinataire

Les serveurs DEVRAIENT randomiser l'ordre des clients chaque fois qu'ils génèrent un LS2 chiffré, pour   empêcher les clients de connaître leur position dans la liste et d'inférer quand d'autres clients ont été ajoutés ou révoqués.

- Une couche externe contenant les informations en clair nécessaires pour le stockage et la récupération.
- Une couche intermédiaire qui gère l'authentification du client.
- Une couche interne qui contient les données LS2 réelles.

Un serveur PEUT choisir de cacher le nombre de clients abonnés en insérant des entrées aléatoires dans la liste des données d'autorisation.

- La clé publique de signature dans la destination non masquée doit être  
  Ed25519 (type de signature 7) ou Red25519 (type de signature 11) ;  
  aucun autre type de signature n'est supporté
- Si la clé publique de signature est hors ligne, la clé publique de signature temporaire doit aussi être Ed25519
- Le masquage est computationnellement simple
- Utiliser des primitives cryptographiques existantes
- Les clés publiques masquées ne peuvent pas être démascarquées
- Les clés publiques masquées doivent être sur la courbe Ed25519 et dans le sous-groupe d'ordre premier
- Doit connaître la clé publique de signature de la destination  
  (destination complète non requise) pour dériver la clé publique masquée
- Optionnellement fournir un secret supplémentaire requis pour dériver la clé publique masquée

Avantages de l'autorisation client DH   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- La sécurité du schéma ne dépend pas uniquement de l'échange hors bande du matériel de clé client.  
  La clé privée du client n'a jamais besoin de quitter son appareil, donc un  
  adversaire capable d'intercepter l'échange hors bande, mais incapable de casser l'algorithme DH,  
  ne peut pas déchiffrer le LS2 chiffré, ni déterminer combien de temps le client a accès.

### LS chiffré avec adresses Base 32

Inconvénients de l'autorisation client DH   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Avantages de l'autorisation client PSK   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

### LS chiffré avec clés hors ligne

Inconvénients de l'autorisation client PSK   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Voir proposition 149.

Vous ne pouvez pas utiliser un LS2 chiffré pour bittorrent, à cause des réponses compactes d'annonce qui font 32 octets.   Les 32 octets contiennent uniquement le hachage. Il n'y a pas de place pour indiquer que le   leaseset est chiffré, ou les types de signature.

### Notes

- Nécessite N + 1 opérations DH côté serveur pour N clients.
- Nécessite une opération DH côté client.
- Nécessite que le client génère la clé secrète.

- Ne nécessite aucune opération DH.
- Permet au serveur de générer la clé secrète.
- Permet au serveur de partager la même clé avec plusieurs clients, si souhaité.

- La sécurité du schéma dépend critique de l'échange hors bande du matériel de clé client.  
  Un adversaire qui intercepte l'échange pour un client particulier peut déchiffrer  
  tout LS2 chiffré ultérieur pour lequel ce client est autorisé, ainsi que déterminer  
  quand l'accès du client est révoqué.

- Un service utilisant des leasesets chiffrés publierait la version chiffrée aux  
  floodfills. Cependant, par souci d'efficacité, il enverrait des leasesets non chiffrés aux  
  clients dans le message garlic encapsulé, une fois authentifié (via liste blanche, par  
  exemple).

- Les floodfills peuvent limiter la taille maximale à une valeur raisonnable pour éviter les abus.

### Meta LS2

Pour les leasesets chiffrés avec clés hors ligne, les clés privées masquées doivent également être générées hors ligne,   une pour chaque jour.

Comme le bloc de signature hors ligne optionnel est dans la partie en clair du leaseset chiffré,   n'importe qui scrapant les floodfills pourrait l'utiliser pour suivre le leaseset (mais pas le déchiffrer)   sur plusieurs jours.   Pour l'éviter, le propriétaire des clés devrait générer de nouvelles clés temporaires   pour chaque jour également.   Les clés temporaires et masquées peuvent être générées à l'avance, et livrées au routeur   par lots.

Il n'y a pas de format de fichier défini dans cette proposition pour empaqueter plusieurs clés temporaires et   masquées et les fournir au client ou au routeur.   Il n'y a pas d'amélioration du protocole I2CP définie dans cette proposition pour supporter   les leasesets chiffrés avec clés hors ligne.

Ceci est utilisé pour remplacer le multihébergement. Comme tout leaseset, ceci est signé par le   créateur. C'est une liste authentifiée de hachages de destination.

Le Meta LS2 est le nœud supérieur, et éventuellement des nœuds intermédiaires,   d'une structure en arbre.   Il contient plusieurs entrées, chacune pointant vers un LS, LS2 ou un autre Meta LS2   pour supporter un multihébergement massif.   Un Meta LS2 peut contenir un mélange d'entrées LS, LS2 et Meta LS2.   Les feuilles de l'arbre sont toujours un LS ou LS2.   L'arbre est un DAG ; les boucles sont interdites ; les clients effectuant des recherches doivent détecter et   refuser de suivre les boucles.

Un Meta LS2 peut avoir une expiration beaucoup plus longue qu'un LS ou LS2 standard.   Le niveau supérieur peut avoir une expiration plusieurs heures après la date de publication.   Le temps d'expiration maximal sera appliqué par les floodfills et clients, et est à déterminer.

L'utilisation de Meta LS2 est le multihébergement massif, mais sans plus   de protection contre la corrélation des routeurs aux leasesets (au redémarrage du routeur) que   celle fournie actuellement avec LS ou LS2.   Ceci équivaut au cas d'usage « facebook », qui n'a probablement pas besoin   de protection contre la corrélation. Ce cas d'usage a probablement besoin de clés hors ligne,   qui sont fournies dans l'en-tête standard à chaque nœud de l'arbre.

Le protocole backend pour la coordination entre les routeurs feuilles, les signataires intermédiaires et principaux de Meta LS   n'est pas spécifié ici. Les exigences sont extrêmement simples - juste vérifier que le pair est en ligne,   et publier un nouveau LS toutes les quelques heures. La seule complexité est pour choisir de nouveaux   éditeurs pour les Meta LS de niveau supérieur ou intermédiaire en cas de panne.

Le mélange de leasesets où des locations de plusieurs routeurs sont combinées, signées et publiées   dans un seul leaseset est documenté dans la proposition 140, « multihébergement invisible ».   Cette proposition est irréalisable telle quelle, car les connexions en streaming ne seraient pas   « collantes » à un seul routeur, voir http://zzz.i2p/topics/2335 .

Le protocole backend, et l'interaction avec les composants internes du routeur et du client, serait   très complexe pour le multihébergement invisible.

    Standard LS flag (1)
Pour éviter de surcharger le floodfill pour le Meta LS de niveau supérieur, l'expiration devrait   être d'au moins plusieurs heures. Les clients doivent mettre en cache le Meta LS de niveau supérieur, et le conserver   entre les redémarrages s'il n'est pas expiré.

    Meta LS2 type (7)
Nous devons définir un algorithme pour que les clients parcourent l'arbre, y compris des solutions de secours,   afin que l'utilisation soit dispersée. Une fonction de distance de hachage, coût et aléatoire.   Si un nœud a à la fois LS ou LS2 et Meta LS, nous devons savoir quand il est autorisé   d'utiliser ces leasesets, et quand continuer à parcourir l'arbre.

    Hash of destination
    This hash is then used to generate the daily "routing key", as in LS1
Recherche avec

    Hours. Max 18.2 hours (65535 seconds)
Stockage avec

    "master" Destination or coordinator, or intermediate coordinators

### Format

```
Standard LS2 Header as specified above

  Meta LS2 Type-Specific Part
  - Properties (Mapping as specified in common structures spec, 2 zero bytes if none)
  - Number of entries (1 byte) Maximum TBD
  - Entries. Each entry contains: (40 bytes)
    - Hash (32 bytes)
    - Flags (2 bytes)
      TBD. Set all to zero for compatibility with future uses.
    - Type (1 byte) The type of LS it is referencing;
      1 for LS, 3 for LS2, 5 for encrypted, 7 for meta, 0 for unknown.
    - Cost (priority) (1 byte)
    - Expires (4 bytes) (4 bytes, big endian, seconds since epoch, rolls over in 2106)
  - Number of revocations (1 byte) Maximum TBD
  - Revocations: Each revocation contains: (32 bytes)
    - Hash (32 bytes)

  Standard LS2 Signature:
  - Signature (40+ bytes)
    The signature is of everything above.
```
Stockage à

### Notes

- Après déchiffrement, plusieurs vérifications doivent être effectuées, notamment que  
  l'horodatage interne et l'expiration correspondent à ceux du niveau supérieur.

- ChaCha20 a été choisi plutôt qu'AES. Bien que les vitesses soient similaires si le  
  support matériel AES est disponible, ChaCha20 est 2,5 à 3 fois plus rapide lorsque  
  le support matériel AES n'est pas disponible, comme sur les appareils ARM bas de gamme.

- Nous ne nous soucions pas assez de la vitesse pour utiliser BLAKE2b avec clé. Il a une taille de sortie  
  suffisamment grande pour accommoder le plus grand n requis (ou nous pouvons l'appeler une fois par  
  clé souhaitée avec un argument compteur). BLAKE2b est beaucoup plus rapide que SHA-256, et  
  BLAKE2b avec clé réduirait le nombre total d'appels à la fonction de hachage.  
  Cependant, voir la proposition 148, où il est proposé que nous passions à BLAKE2b pour d'autres raisons.  
  Voir [Secure key derivation performance](https://www.lvh.io/posts/secure-key-derivation-performance.html).

### Enregistrement de service

Expiration typique

Publié par

Flags et propriétés : pour usage futur

    n/a, see Service List
Ceci est un enregistrement individuel indiquant qu'une destination participe à un   service. Il est envoyé du participant au floodfill. Il n'est jamais envoyé   individuellement par un floodfill, mais seulement comme partie d'une liste de service. L'enregistrement de service est également utilisé pour révoquer la participation à un service, en fixant l'   expiration à zéro.

    Service Record type (9)
Ce n'est pas un LS2 mais il utilise le format d'en-tête et de signature standard LS2.

    Hash of service name
    This hash is then used to generate the daily "routing key", as in LS1
Recherche avec

    Hours. Max 18.2 hours (65535 seconds)
Stockage avec

    Destination

### Format

```
Standard LS2 Header as specified above

  Service Record Type-Specific Part
  - Port (2 bytes, big endian) (0 if unspecified)
  - Hash of service name (32 bytes)

  Standard LS2 Signature:
  - Signature (40+ bytes)
    The signature is of everything above.
```
### Notes

- Un service distribué utilisant ceci aurait un ou plusieurs « maîtres » avec la  
  clé privée de la destination du service. Ils détermineraient (hors bande) la  
  liste actuelle des destinations actives et publieraient le Meta LS2. Pour  
  la redondance, plusieurs maîtres pourraient multihéberger (c'est-à-dire publier simultanément) le  
  Meta LS2.

- Un service distribué pourrait commencer avec une destination unique ou utiliser le  
  multihébergement ancien style, puis passer à un Meta LS2. Une recherche LS standard pourrait retourner  
  n'importe lequel parmi LS, LS2 ou Meta LS2.

- Lorsqu'un service utilise un Meta LS2, il n'a pas de tunnels (locations).

### Liste de service

Stockage à

Expiration typique

Publié par

Ceci n'est rien comme un LS2 et utilise un format différent.

La liste de service est créée et signée par le floodfill. Elle est non authentifiée   dans le sens où n'importe qui peut rejoindre un service en publiant un Enregistrement de service à un   floodfill.

Une Liste de service contient des Enregistrements de service courts, pas des Enregistrements complets. Ceux-ci   contiennent des signatures mais seulement des hachages, pas des destinations complètes, donc ils ne peuvent pas être   vérifiés sans la destination complète.

    Service List lookup type (11)
La sécurité, s'il y en a une, et la désirabilité des listes de service sont à déterminer.   Les floodfills pourraient limiter la publication et les recherches à une liste blanche de services,   mais cette liste blanche peut varier selon l'implémentation ou les préférences de l'opérateur.   Il peut ne pas être possible d'atteindre un consensus sur une liste blanche commune de base   entre les implémentations.

    Service List type (11)
Si le nom du service est inclus dans l'enregistrement de service ci-dessus,   les opérateurs de floodfill peuvent s'y opposer ; si seul le hachage est inclus,   il n'y a pas de vérification, et un enregistrement de service pourrait « entrer » avant   tout autre type netdb et être stocké dans le floodfill.

    Hash of service name
    This hash is then used to generate the daily "routing key", as in LS1
Recherche avec

    Hours, not specified in the list itself, up to local policy
Stockage avec

    Nobody, never sent to floodfill, never flooded.

### Format

Stockage à

```
- Type (1 byte)
    Not actually in header, but part of data covered by signature.
    Take from field in Database Store Message.
  - Hash of the service name (implicit, in the Database Store message)
  - Hash of the Creator (floodfill) (32 bytes)
  - Published timestamp (8 bytes, big endian)

  - Number of Short Service Records (1 byte)
  - List of Short Service Records:
    Each Short Service Record contains (90+ bytes)
    - Dest hash (32 bytes)
    - Published timestamp (8 bytes, big endian)
    - Expires (4 bytes, big endian) (offset from published in ms)
    - Flags (2 bytes)
    - Port (2 bytes, big endian)
    - Sig length (2 bytes, big endian)
    - Signature of dest (40+ bytes)

  - Number of Revocation Records (1 byte)
  - List of Revocation Records:
    Each Revocation Record contains (86+ bytes)
    - Dest hash (32 bytes)
    - Published timestamp (8 bytes, big endian)
    - Flags (2 bytes)
    - Port (2 bytes, big endian)
    - Sig length (2 bytes, big endian)
    - Signature of dest (40+ bytes)

  - Signature of floodfill (40+ bytes)
    The signature is of everything above.
```
Expiration typique

- Si l'expiration est à zéro, le floodfill devrait révoquer l'enregistrement et ne plus  
  l'inclure dans la liste de service.

Publié par

- Stockage : Le floodfill peut strictement limiter le stockage de ces enregistrements et  
  limiter le nombre d'enregistrements stockés par hachage et leur expiration. Une liste blanche  
  de hachages peut également être utilisée.

N'utilise PAS l'en-tête standard LS2 spécifié ci-dessus.

- Tout autre type netdb au même hachage a priorité, donc un enregistrement de service ne peut jamais  
  écraser un LS/RI, mais un LS/RI écrasera tous les enregistrements de service à ce hachage.

### Notes

- Nous utilisons la longueur de la signature plutôt que le sig type afin de pouvoir prendre en charge des types de signature inconnus.

- Une liste de services n'expire pas ; les destinataires peuvent prendre leur propre décision en fonction de leur politique ou de l'expiration des enregistrements individuels.

- Les listes de services ne sont pas inondées, seuls les enregistrements de service individuels le sont. Chaque
  floodfill crée, signe et met en cache une liste de services. Le floodfill applique sa
  propre politique pour la durée de cache et le nombre maximal d'enregistrements de service et de révocation.

## Modifications requises de la Common Structures Spec

### Certificats de clés

Hors périmètre de cette proposition. Ajouter aux propositions ECIES 144 et 145.

### Nouvelles structures intermédiaires

Ajout de nouvelles structures pour Lease2, MetaLease, LeaseSet2Header et OfflineSignature. Effectif depuis la version 0.9.38.

### Nouveaux types de NetDB

Ajouter des structures pour chaque nouveau type de leaseSet, intégrées depuis ci-dessus. Pour LeaseSet2, EncryptedLeaseSet et MetaLeaseSet, effectif à partir de la version 0.9.38. Pour Service Record et Service List, préliminaires et non planifiés.

### Nouveau type de signature

Ajouter le type 11 RedDSA_SHA512_Ed25519. La clé publique est de 32 octets ; la clé privée est de 32 octets ; le hash est de 64 octets ; la signature est de 64 octets.

## Modifications requises de la spécification de chiffrement

Hors du périmètre de cette proposition. Voir les propositions 144 et 145.

## Modifications requises pour I2NP

Ajouter une note : LS2 ne peut être publié qu'auprès de floodfills disposant d'une version minimale.

### Message de consultation de la base de données

Ajouter le type de recherche de liste de services.

### Modifications

```
Flags byte: Lookup type field, currently bits 3-2, expands to bits 4-2.
  Lookup type 0x04 is defined as the service list lookup.

  Add note: Service list loookup may only be sent to floodfills with a minimum version.
  Minimum version is 0.9.38.
```
### Message de stockage de base de données

Ajouter tous les nouveaux types de store.

### Modifications

```
Type byte: Type field, currently bit 0, expands to bits 3-0.
  Type 3 is defined as a LS2 store.
  Type 5 is defined as a encrypted LS2 store.
  Type 7 is defined as a meta LS2 store.
  Type 9 is defined as a service record store.
  Type 11 is defined as a service list store.
  Other types are undefined and invalid.

  Add note: All new types may only be published to floodfills with a minimum version.
  Minimum version is 0.9.38.
```
## Modifications requises pour I2CP

### Options I2CP

Nouvelles options interprétées côté router, envoyées dans le SessionConfig Mapping :

```

  i2cp.leaseSetType=nnn       The type of leaseset to be sent in the Create Leaseset Message
                              Value is the same as the netdb store type in the table above.
                              Interpreted client-side, but also passed to the router in the
                              SessionConfig, to declare intent and check support.

  i2cp.leaseSetEncType=nnn[,nnn]  The encryption types to be used.
                                  Interpreted client-side, but also passed to the router in
                                  the SessionConfig, to declare intent and check support.
                                  See proposals 144 and 145.

  i2cp.leaseSetOfflineExpiration=nnn  The expiration of the offline signature, ASCII,
                                      seconds since the epoch.

  i2cp.leaseSetTransientPublicKey=[type:]b64  The base 64 of the transient private key,
                                              prefixed by an optional sig type number
                                              or name, default DSA_SHA1.
                                              Length as inferred from the sig type

  i2cp.leaseSetOfflineSignature=b64   The base 64 of the offline signature.
                                      Length as inferred from the destination
                                      signing public key type

  i2cp.leaseSetSecret=b64     The base 64 of a secret used to blind the
                              address of the leaseset, default ""

  i2cp.leaseSetAuthType=nnn   The type of authentication for encrypted LS2.
                              0 for no per-client authentication (the default)
                              1 for DH per-client authentication
                              2 for PSK per-client authentication

  i2cp.leaseSetPrivKey=b64    A base 64 private key for the router to use to
                              decrypt the encrypted LS2,
                              only if per-client authentication is enabled
```
Nouvelles options interprétées côté client :

```

  i2cp.leaseSetType=nnn     The type of leaseset to be sent in the Create Leaseset Message
                            Value is the same as the netdb store type in the table above.
                            Interpreted client-side, but also passed to the router in the
                            SessionConfig, to declare intent and check support.

  i2cp.leaseSetEncType=nnn[,nnn]  The encryption types to be used.
                                  Interpreted client-side, but also passed to the router in
                                  the SessionConfig, to declare intent and check support.
                                  See proposals 144 and 145.

  i2cp.leaseSetSecret=b64     The base 64 of a secret used to blind the
                              address of the leaseset, default ""

  i2cp.leaseSetAuthType=nnn       The type of authentication for encrypted LS2.
                                  0 for no per-client authentication (the default)
                                  1 for DH per-client authentication
                                  2 for PSK per-client authentication

  i2cp.leaseSetBlindedType=nnn   The sig type of the blinded key for encrypted LS2.
                                 Default depends on the destination sig type.

  i2cp.leaseSetClient.dh.nnn=b64name:b64pubkey   The base 64 of the client name (ignored, UI use only),
                                                 followed by a ':', followed by the base 64 of the public
                                                 key to use for DH per-client auth. nnn starts with 0

  i2cp.leaseSetClient.psk.nnn=b64name:b64privkey   The base 64 of the client name (ignored, UI use only),
                                                   followed by a ':', followed by the base 64 of the private
                                                   key to use for PSK per-client auth. nnn starts with 0
```
### Configuration de session

Il convient de noter que pour les signatures hors ligne, les options i2cp.leaseSetOfflineExpiration, i2cp.leaseSetTransientPublicKey et i2cp.leaseSetOfflineSignature sont requises, et la signature est effectuée par la clé privée de signature transitoire.

### Message de demande de LeaseSet

Router vers client. Aucun changement. Les leases sont envoyés avec des timestamps de 8 octets, même si le leaseSet retourné sera un LS2 avec des timestamps de 4 octets. Noter que la réponse peut être un message Create Leaseset ou Create Leaseset2.

### Requête de message leaseset variable

Router vers client. Aucun changement. Les leases sont envoyés avec des timestamps de 8 octets, même si le leaseSet retourné sera un LS2 avec des timestamps de 4 octets. Noter que la réponse peut être un message Create Leaseset ou Create Leaseset2.

### Créer un message Leaseset2

Client vers router. Nouveau message, à utiliser en remplacement de Create Leaseset Message.

### Justification

Afin que le router puisse analyser le type de stockage, ce type doit être présent dans le message, à moins qu'il ne soit transmis au router au préalable dans la configuration de session. Pour le code d'analyse commun, il est plus simple de le trouver dans le message lui-même.

- Pour que le router connaisse le type et la longueur de la clé privée,
  elle doit se trouver après le lease set, sauf si le parseur connaît le type au préalable
  dans la configuration de session.
  Pour du code de parsing courant, il est plus facile de le connaître à partir du message lui-même.

- La clé privée de signature, précédemment définie pour la révocation et inutilisée, n'est pas présente dans LS2.

### Type de message

Le type de message du message Create Leaseset2 est 41.

### Format

```
Session ID
  Type byte: Type of lease set to follow
             Type 1 is a LS
             Type 3 is a LS2
             Type 5 is a encrypted LS2
             Type 7 is a meta LS2
  LeaseSet: type specified above
  Number of private keys to follow (1 byte)
  Encryption Private Keys: For each public key in the lease set,
                           in the same order
                           (Not present for Meta LS2)
                           - Encryption type (2 bytes, big endian)
                           - Encryption key length (2 bytes, big endian)
                           - Encryption key (number of bytes specified)
```
### Notes

- La version minimale du router est 0.9.39.
- Une version préliminaire avec le type de message 40 était présente dans 0.9.38, mais le format a été modifié.
  Le type 40 est abandonné et n'est pas pris en charge.

### Problèmes

- D'autres changements sont nécessaires pour prendre en charge les LS chiffrés et les LS meta.

### Message d'information sur le blinding

Du client au router. Nouveau message.

### Justification

- Le router doit savoir si une destination est aveuglée.
  Si elle est aveuglée et utilise une authentification secrète ou propre à chaque client,
  il doit également disposer de ces informations.

- Un Host Lookup d'une adresse b32 au nouveau format (« b33 »)
  indique au router que l'adresse est aveuglée, mais il n'existe aucun mécanisme
  permettant de transmettre la clé secrète ou privée au router dans le message Host Lookup.
  Bien que l'on puisse étendre le message Host Lookup pour y ajouter cette information,
  il est plus propre de définir un nouveau message.

- Nous avons besoin d'une approche programmatique permettant au client d'indiquer au router. Autrement, l'utilisateur devrait configurer manuellement chaque destination.

### Utilisation

Avant qu’un client n’envoie un message à une destination aveuglée, il doit soit rechercher le « b33 » dans un message Host Lookup, soit envoyer un message Blinding Info. Si la destination aveuglée exige un secret ou une authentification par client, le client doit envoyer un message Blinding Info.

Le router n'envoie pas de réponse à ce message.

### Type de message

Le type de message du Blinding Info Message est 42.

### Format

```
Session ID
  Flags:       1 byte
               Bit order: 76543210
               Bit 0: 0 for everybody, 1 for per-client
               Bits 3-1: Authentication scheme, if bit 0 is set to 1 for per-client, otherwise 000
                         000: DH client authentication (or no per-client authentication)
                         001: PSK client authentication
               Bit 4: 1 if secret required, 0 if no secret required
               Bits 7-5: Unused, set to 0 for future compatibility
  Type byte:   Endpoint type to follow
               Type 0 is a Hash
               Type 1 is a host name String
               Type 2 is a Destination
               Type 3 is a Sig Type and Signing Public Key
  Blind Type:  2 byte blinded sig type (big endian)
  Expiration:  4 bytes, big endian, seconds since epoch
  Endpoint:    Data as specified above
               For type 0: 32 byte binary hash
               For type 1: host name String
               For type 2: binary Destination
               For type 3: 2 byte sig type (big endian)
                           Signing Public Key (length as implied by sig type)
  Private Key: Only if flag bit 0 is set to 1
               A 32-byte ECIES_X25519 private key
  Secret:      Only if flag bit 4 is set to 1
               A secret String
```
### Notes

- La version minimale du router est 0.9.43

### Problèmes

### Message de réponse de l'hôte (enc)

Pour prendre en charge les recherches de noms d'hôte « b33 » et renvoyer une indication si le router ne dispose pas des informations requises, nous définissons des codes de résultat supplémentaires pour le Host Reply Message, comme suit :

```
2: Lookup password required
   3: Private key required
   4: Lookup password and private key required
   5: Leaseset decryption failure
```
Les valeurs 1 à 255 sont déjà définies comme des erreurs, il n'y a donc pas de problème de rétrocompatibilité.

### Message de redirection Meta

Router vers le client. Nouveau message.

### Justification

Un client ne sait pas a priori qu'un Hash donné correspondra à un Meta LS.

Si une recherche de leaseset pour une Destination renvoie un Meta LS, le router effectue la résolution récursive. Pour les datagrammes, le côté client n'a pas besoin de le savoir ; toutefois, pour le streaming, où le protocole vérifie la destination dans le SYN ACK, il doit savoir quelle est la « vraie » destination. Par conséquent, un nouveau message est nécessaire.

### Utilisation

Le router maintient un cache pour la destination réelle utilisée à partir d'un meta LS. Lorsqu'un client envoie un message à une destination qui se résout en un meta LS, le router vérifie le cache pour la destination réelle utilisée en dernier. Si le cache est vide, le router sélectionne une destination depuis le meta LS et recherche le leaseset. Si la recherche du leaseset réussit, le router ajoute cette destination au cache et envoie au client un Meta Redirect Message. Cette opération n'est effectuée qu'une seule fois, sauf si la destination expire et doit être changée. Le client doit également mettre en cache les informations si nécessaire. Le Meta Redirect Message n'est PAS envoyé en réponse à chaque SendMessage.

Le router n'envoie ce message qu'aux clients dont la version est 0.9.47 ou supérieure.

Le client n'envoie pas de réponse à ce message.

### Type de message

Le type de message du Meta Redirect Message est 43.

### Format

```
Session ID (2 bytes) The value from the Send Message.
  Message ID generated by the router (4 bytes)
  4 byte nonce previously generated by the client
               (the value from the Send Message, may be zero)
  Flags:       2 bytes, bit order 15...0
               Unused, set to 0 for future compatibility
               Bit 0: 0 - the destination is no longer meta
                      1 - the destination is now meta
               Bits 15-1: Unused, set to 0 for future compatibility
  Original Destination (387+ bytes)
  (following fields only present if flags bit 0 is 1)
  MFlags:      2 bytes
               Unused, set to 0 for future compatibility
               From the Meta Lease for the actual Destination
  Expiration:  4 bytes, big endian, seconds since epoch
               From the Meta Lease for the actual Destination
  Cost (priority) 1 byte
               From the Meta Lease for the actual Destination
  Actual (real) Destination (387+ bytes)
```
### Modifications pour la prise en charge de Meta

La manière de générer et de prendre en charge Meta, y compris la communication et la coordination entre routers, ne relève pas du champ d'application de cette proposition. Voir la proposition connexe 150.

### Modifications pour prendre en charge les clés hors ligne

Les signatures hors ligne ne peuvent être vérifiées ni dans le streaming ni dans les datagrammes avec réponse. Voir les sections ci-dessous.

## Modifications requises du fichier de clé privée

Le format du fichier de clé privée (eepPriv.dat) ne fait pas partie officielle de nos spécifications, mais il est documenté dans les [javadocs de Java I2P](http://idk.i2p/javadoc-i2p/net/i2p/data/PrivateKeyFile.html) et d'autres implémentations le prennent en charge. Cela permet la portabilité des clés privées entre différentes implémentations.

Des modifications sont nécessaires pour stocker la clé publique transiente et les informations de signature hors ligne.

### Modifications

```
If the signing private key is all zeros, the offline information section follows:

  - Expires timestamp
    (4 bytes, big endian, seconds since epoch, rolls over in 2106)
  - Sig type of transient Signing Public Key (2 bytes, big endian)
  - Transient Signing Public key
    (length as specified by transient sig type)
  - Signature of above three fields by offline key
    (length as specified by destination sig type)
  - Transient Signing Private key
    (length as specified by transient sig type)
```
### Modifications requises de la CLI du fichier de clé privée

Ajouter la prise en charge des options suivantes :

```
-d days              (specify expiration in days of offline sig, default 365)
      -o offlinedestfile   (generate the online key file,
                            using the offline key file specified)
      -r sigtype           (specify sig type of transient key, default Ed25519)
```
## Modifications du streaming requises

Les signatures hors ligne ne peuvent actuellement pas être vérifiées en streaming. La modification ci-dessous ajoute le bloc de signature hors ligne aux options. Cela évite de devoir récupérer cette information via I2CP.

### Modifications

```
Add new option:
  Bit:          11
  Flag:         OFFLINE_SIGNATURE
  Option order: 4
  Option data:  Variable bytes
  Function:     Contains the offline signature section from LS2.
                FROM_INCLUDED must also be set.
                Expires timestamp
                (4 bytes, big endian, seconds since epoch, rolls over in 2106)
                Transient sig type (2 bytes, big endian)
                Transient signing public key (length as implied by sig type)
                Signature of expires timestamp, transient sig type,
                and public key, by the destination public key,
                length as implied by destination public key sig type.

  Change option:
  Bit:          3
  Flag:         SIGNATURE_INCLUDED
  Option order: Change from 4 to 5

  Add information about transient keys to the
  Variable Length Signature Notes section:
  The offline signature option does not needed to be added for a CLOSE packet if
  a SYN packet containing the option was previously acked.
  More info TODO
```
### Notes

- Une alternative consiste simplement à ajouter un flag, et à récupérer la clé publique transiente via I2CP
  (Voir les sections Host Lookup / Host Reply Message ci-dessus)

## Modifications requises pour les datagrammes repliables

Les signatures hors ligne ne peuvent pas être vérifiées dans le traitement des datagrammes répondables. Il faudrait un flag pour indiquer une signature hors ligne, mais il n'y a nulle part où le placer. Cela nécessitera un tout nouveau numéro de protocole et un nouveau format.

### Modifications

```
Define new protocol 19 - Repliable datagram with options?
  - Destination (387+ bytes)
  - Flags (2 bytes)
    Bit order: 15 14 ... 3 2 1 0
    Bit 0: If 0, no offline keys; if 1, offline keys
    Bits 1-15: set to 0 for compatibility with future uses
  - If flag indicates offline keys, the offline signature section:
    Expires timestamp
    (4 bytes, big endian, seconds since epoch, rolls over in 2106)
    Transient sig type (2 bytes, big endian)
    Transient signing public key (length as implied by sig type)
    Signature of expires timestamp, transient sig type,
    and public key, by the destination public key,
    length as implied by destination public key sig type.
    This section can, and should, be generated offline.
  - Data
```
### Notes

- L'alternative consiste simplement à ajouter un flag et à récupérer la clé publique transitoire via I2CP
  (Voir les sections Host Lookup / Host Reply Message ci-dessus)
- Y a-t-il d'autres options que nous devrions ajouter maintenant que nous disposons d'octets de flag ?

## Modifications requises pour SAM V3

SAM doit être amélioré pour prendre en charge les signatures hors ligne dans le DESTINATION en base 64.

### Modifications

```
Note that in the SESSION CREATE DESTINATION=$privkey,
  the $privkey raw data (before base64 conversion)
  may be optionally followed by the Offline Signature as specified in the
  Common Structures Specification.

  If the signing private key is all zeros, the offline information section follows:

  - Expires timestamp
    (4 bytes, big endian, seconds since epoch, rolls over in 2106)
  - Sig type of transient Signing Public Key (2 bytes, big endian)
  - Transient Signing Public key
    (length as specified by transient sig type)
  - Signature of above three fields by offline key
    (length as specified by destination sig type)
  - Transient Signing Private key (length as specified by transient sig type)
```
Noter que les signatures hors ligne ne sont prises en charge que pour STREAM et RAW, et non pour DATAGRAM (jusqu'à ce qu'un nouveau protocole DATAGRAM soit défini).

Il est à noter que le SESSION STATUS renverra une Signing Private Key composée uniquement de zéros et les données Offline Signature exactement telles que fournies dans le SESSION CREATE.

Notez que DEST GENERATE et SESSION CREATE DESTINATION=TRANSIENT ne peuvent pas être utilisés pour créer une destination signée hors ligne.

### Problèmes

Passer la version à 3.4, ou la laisser à 3.1/3.2/3.3 pour qu'elle puisse être ajoutée sans nécessiter tout ce qui concerne les versions 3.2/3.3 ?

Autres modifications à déterminer. Voir la section I2CP Host Reply Message ci-dessus.

## Modifications requises pour BOB

BOB devrait être amélioré pour prendre en charge les signatures hors ligne et/ou Meta LS. Ceci est de faible priorité et ne sera probablement jamais spécifié ni implémenté. SAM V3 est l'interface préférée.

## Publication, migration, compatibilité

LS2 (autre qu'un LS2 chiffré) est publié au même emplacement DHT que le LS1. Il n'existe aucun moyen de publier à la fois un LS1 et un LS2, à moins que le LS2 ne se trouve à un emplacement différent.

Le LS2 chiffré est publié à l'emplacement du hash du type de clé aveuglée et des données de clé. Ce hash est ensuite utilisé pour générer la « clé de routage » quotidienne, comme dans LS1.

LS2 ne serait utilisé que lorsque de nouvelles fonctionnalités sont requises (nouvelle cryptographie, LS chiffré, méta, etc.). LS2 ne peut être publié qu'auprès de floodfills d'une version spécifiée ou supérieure.

Les routeurs publiant des LS2 sauraient que tout client se connectant prend en charge LS2. Ils pourraient envoyer le LS2 dans le garlic.

Les clients n'enverraient des LS2 dans des garlics que s'ils utilisent la nouvelle crypto. Les clients partagés utiliseraient-ils LS1 indéfiniment ? TODO : comment avoir des clients partagés qui prennent en charge à la fois l'ancienne et la nouvelle crypto ?

## Déploiement

0.9.38 inclut la prise en charge du floodfill pour LS2 standard, y compris les clés hors ligne.

La version 0.9.39 inclut la prise en charge I2CP de LS2 et d'Encrypted LS2, la signature/vérification avec le type de sig 11, la prise en charge floodfill pour Encrypted LS2 (types de sig 7 et 11, sans clés hors ligne), ainsi que le chiffrement/déchiffrement de LS2 (sans autorisation par client).

La version 0.9.40 doit inclure la prise en charge du chiffrement/déchiffrement des LS2 avec autorisation par client, la prise en charge de Meta LS2 par floodfill et I2CP, la prise en charge des LS2 chiffrés avec des clés hors ligne, ainsi que la prise en charge de b32 pour les LS2 chiffrés.

## Remerciements

La conception du LS2 chiffré est fortement influencée par les [descripteurs de services cachés v3 de Tor](https://spec.torproject.org/rend-spec-v3), qui poursuivaient des objectifs de conception similaires.

## Références

* ["High-speed high-security signatures" par Daniel J. Bernstein, Niels Duif, Tanja Lange, Peter Schwabe et Bo-Yin Yang](https://ed25519.cr.yp.to/)
* [KEYBLIND-PROOF](https://lists.torproject.org/pipermail/tor-dev/2013-December/005943.html)
* [KEYBLIND-REFS](https://gitlab.torproject.org/tpo/core/tor/-/issues/8106)
* [PRNG-REFS](http://projectbullrun.org/dual-ec/ext-rand.html)
* [RFC-2104](https://tools.ietf.org/html/rfc2104)
* [RFC-4880-S5.1](https://tools.ietf.org/html/rfc4880#section-5.1)
* [RFC-5869](https://tools.ietf.org/html/rfc5869)
* [RFC-7539-S2.4](https://tools.ietf.org/html/rfc7539#section-2.4)
* [TOR-REND-SPEC-V3](https://spec.torproject.org/rend-spec-v3)
* [UNSCIENTIFIC-KDF-SPEEDS](https://www.lvh.io/posts/secure-key-derivation-performance.html)
* [ZCASH](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf)
