---
title: "Nouvelles entrées netDB"
number: "123"
author: "zzz, str4d, orignal"
created: "2016-01-16"
lastupdated: "2020-07-18"
status: "Ouvrir"
thread: "http://zzz.i2p/topics/2051"
supercedes: "110, 120, 121, 122"
---

## Statut

Des portions de cette proposition sont terminées et implémentées dans les versions 0.9.38 et 0.9.39. Les spécifications Common Structures, I2CP, I2NP et autres sont maintenant mises à jour pour refléter les changements qui sont actuellement pris en charge.

Les parties terminées sont encore sujettes à des révisions mineures. D'autres parties de cette proposition sont encore en développement et sujettes à des révisions substantielles.

Service Lookup (types 9 et 11) sont de faible priorité et non programmés, et pourraient faire l'objet d'une proposition séparée.

## Aperçu

Il s'agit d'une mise à jour et d'une agrégation des 4 propositions suivantes :

- 110 LS2
- 120 Meta LS2 pour multihébergement massif
- 121 LS2 chiffré
- 122 Recherche de service non authentifiée (anycast)

Ces propositions sont en grande partie indépendantes, mais par souci de cohérence nous définissons et utilisons un format commun pour plusieurs d'entre elles.

Les propositions suivantes sont quelque peu liées :

- 140 Multihébergement invisible (incompatible avec cette proposition)
- 142 Nouveau modèle cryptographique (pour la nouvelle cryptographie symétrique)
- 144 ECIES-X25519-AEAD-Ratchet
- 145 ECIES-P256
- 146 Red25519
- 148 EdDSA-BLAKE2b-Ed25519
- 149 B32 pour LS2 chiffré
- 150 Protocole Garlic Farm
- 151 Masquage ECDSA

## Proposition

Cette proposition définit 5 nouveaux types de DatabaseEntry et le processus pour les stocker dans et les récupérer depuis la base de données réseau, ainsi que la méthode pour les signer et vérifier ces signatures.

### Goals

- Rétrocompatible
- LS2 utilisable avec l'ancien style de multihoming
- Aucune nouvelle crypto ou primitive requise pour le support
- Maintenir le découplage de la crypto et de la signature ; supporter toutes les versions actuelles et futures
- Activer les clés de signature hors ligne optionnelles
- Réduire la précision des horodatages pour réduire le fingerprinting
- Activer la nouvelle crypto pour les destinations
- Activer le multihoming massif
- Corriger plusieurs problèmes avec les LS chiffrés existants
- Blinding optionnel pour réduire la visibilité par les floodfills
- Le chiffré supporte à la fois les clés uniques et les clés révocables multiples
- Recherche de service pour une recherche plus facile des outproxies, bootstrap DHT d'application,
  et autres utilisations
- Ne pas casser tout ce qui repose sur les hachages de destination binaires de 32 octets, par exemple bittorrent
- Ajouter de la flexibilité aux leasesets via des propriétés, comme nous en avons dans les routerinfos
- Mettre l'horodatage publié et l'expiration variable dans l'en-tête, pour que cela fonctionne même
  si le contenu est chiffré (ne pas dériver l'horodatage du lease le plus ancien)
- Tous les nouveaux types vivent dans le même espace DHT et aux mêmes emplacements que les leasesets existants,
  de sorte que les utilisateurs puissent migrer de l'ancien LS vers LS2,
  ou changer entre LS2, Meta et Encrypted,
  sans changer la Destination ou le hachage.
- Une Destination existante peut être convertie pour utiliser des clés hors ligne,
  ou revenir aux clés en ligne, sans changer la Destination ou le hachage.

### Non-Goals / Out-of-scope

- Nouvel algorithme de rotation DHT ou génération aléatoire partagée
- Le type de chiffrement spécifique et le schéma de chiffrement de bout en bout
  pour utiliser ce nouveau type feraient l'objet d'une proposition séparée.
  Aucune nouvelle cryptographie n'est spécifiée ou discutée ici.
- Nouveau chiffrement pour les RI ou la construction de tunnels.
  Cela ferait l'objet d'une proposition séparée.
- Méthodes de chiffrement, transmission et réception des messages I2NP DLM / DSM / DSRM.
  Pas de changement.
- Comment générer et prendre en charge Meta, incluant la communication inter-router backend, la gestion, le basculement et la coordination.
  Le support peut être ajouté à I2CP, ou i2pcontrol, ou un nouveau protocole.
  Cela peut ou peut ne pas être standardisé.
- Comment réellement implémenter et gérer des tunnels à expiration plus longue, ou annuler des tunnels existants.
  C'est extrêmement difficile, et sans cela, vous ne pouvez pas avoir un arrêt propre raisonnable.
- Changements du modèle de menace
- Format de stockage hors ligne, ou méthodes pour stocker/récupérer/partager les données.
- Les détails d'implémentation ne sont pas discutés ici et sont laissés à chaque projet.

### Justification

LS2 ajoute des champs pour modifier le type de chiffrement et pour les futurs changements de protocole.

Le LS2 chiffré corrige plusieurs problèmes de sécurité du LS chiffré existant en utilisant un chiffrement asymétrique de l'ensemble complet des leases.

Meta LS2 fournit un multihébergement flexible, efficace, effectif et à grande échelle.

Service Record et Service List fournissent des services anycast tels que la recherche de noms et l'amorçage DHT.

### Objectifs

Les numéros de type sont utilisés dans les messages de recherche/stockage de base de données I2NP.

La colonne end-to-end indique si les requêtes/réponses sont envoyées vers une Destination dans un Garlic Message.

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
### Objectifs non visés / Hors du périmètre

- Les types de recherche sont actuellement les bits 3-2 dans le Database Lookup Message.
  Tout type supplémentaire nécessiterait l'utilisation du bit 4.

- Tous les types de stockage sont impairs car les bits supérieurs dans le champ de type du message Database Store sont ignorés par les anciens routeurs.
  Nous préférerions que l'analyse échoue en tant que LS plutôt qu'en tant que RI compressé.

- Le type devrait-il être explicite ou implicite ou ni l'un ni l'autre dans les données couvertes par la signature ?

### Justification

Les types 3, 5 et 7 peuvent être retournés en réponse à une recherche de leaseSet standard (type 1). Le type 9 n'est jamais retourné en réponse à une recherche. Le type 11 est retourné en réponse à un nouveau type de recherche de service (type 11).

Seul le type 3 peut être envoyé dans un message Garlic client-à-client.

### Types de données NetDB

Les types 3, 7 et 9 ont tous un format commun ::

En-tête LS2 Standard   - comme défini ci-dessous

Partie Spécifique au Type   - comme définie ci-dessous dans chaque partie

Signature LS2 standard : - Longueur implicite selon le type de signature de la clé de signature

Le Type 5 (Chiffré) ne commence pas par une Destination et a un format différent. Voir ci-dessous.

Le Type 11 (Service List) est une agrégation de plusieurs Service Records et a un format différent. Voir ci-dessous.

### Notes

TBD

## Standard LS2 Header

Les types 3, 7 et 9 utilisent l'en-tête LS2 standard, spécifié ci-dessous :

### Processus de recherche/stockage

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
### Format

- Unpublished/published : À utiliser lors de l'envoi d'un stockage de base de données de bout en bout,
  le router expéditeur peut souhaiter indiquer que ce leaseSet ne doit pas être
  envoyé à d'autres. Nous utilisons actuellement des heuristiques pour maintenir cet état.

- Published: Remplace la logique complexe nécessaire pour déterminer la 'version' du
  leaseSet. Actuellement, la version est l'expiration du lease qui expire en dernier,
  et un routeur qui publie doit incrémenter cette expiration d'au moins 1ms lors de
  la publication d'un leaseSet qui ne fait que supprimer un lease plus ancien.

- Expires : Permet à une entrée netDb d'expirer plus tôt que son leaseSet expirant en dernier. Peut ne pas être utile pour LS2, où les leaseSets sont censés conserver une expiration maximale de 11 minutes, mais pour d'autres nouveaux types, c'est nécessaire (voir Meta LS et Service Record ci-dessous).

- Les clés hors ligne sont optionnelles, pour réduire la complexité d'implémentation initiale/requise.

### Considérations de confidentialité/sécurité

- Pourrait réduire encore plus la précision des horodatages (10 minutes ?) mais il faudrait ajouter un numéro de version. Cela pourrait casser le multihoming, à moins d'avoir un chiffrement préservant l'ordre ? On ne peut probablement pas se passer complètement des horodatages.

- Alternative : horodatage de 3 octets (époque / 10 minutes), version de 1 octet, expiration de 2 octets

- Le type est-il explicite ou implicite dans les données / signature ? Constantes de "domaine" pour la signature ?

### Notes

- Les routeurs ne doivent pas publier un LS plus d'une fois par seconde.
  S'ils le font, ils doivent artificiellement incrémenter l'horodatage publié de 1
  par rapport au LS précédemment publié.

- Les implémentations de router pourraient mettre en cache les clés transitoires et la signature pour éviter la vérification à chaque fois. En particulier, les floodfills et les routers aux deux extrémités de connexions de longue durée pourraient en bénéficier.

- Les clés hors ligne et la signature ne conviennent qu'aux destinations à longue durée de vie,
  c'est-à-dire aux serveurs, pas aux clients.

## New DatabaseEntry types

### Format

Changements par rapport au LeaseSet existant :

- Ajouter l'horodatage de publication, l'horodatage d'expiration, les flags et les propriétés
- Ajouter le type de chiffrement
- Supprimer la clé de révocation

Recherche avec

    Standard LS flag (1)
Stocker avec

    Standard LS2 type (3)
Stocker à

    Hash of destination
    This hash is then used to generate the daily "routing key", as in LS1
Expiration typique

    10 minutes, as in a regular LS.
Publié par

    Destination

### Justification

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
### Problèmes

- Properties: Expansion future et flexibilité.
  Placé en premier au cas où cela serait nécessaire pour l'analyse des données restantes.

- Plusieurs paires type de chiffrement/clé publique permettent
  de faciliter la transition vers de nouveaux types de chiffrement. L'autre façon de procéder
  est de publier plusieurs leaseSets, possiblement en utilisant les mêmes tunnels,
  comme nous le faisons actuellement pour les destinations DSA et EdDSA.
  L'identification du type de chiffrement entrant sur un tunnel
  peut être effectuée avec le mécanisme de session tag existant,
  et/ou par déchiffrement d'essai en utilisant chaque clé. Les longueurs des messages
  entrants peuvent également fournir un indice.

### Notes

Cette proposition continue d'utiliser la clé publique dans le leaseset pour la clé de chiffrement de bout en bout, et laisse le champ de clé publique dans la Destination inutilisé, comme c'est le cas actuellement. Le type de chiffrement n'est pas spécifié dans le certificat de clé Destination, il restera 0.

Une alternative rejetée consiste à spécifier le type de chiffrement dans le certificat de clé de Destination, utiliser la clé publique dans la Destination, et ne pas utiliser la clé publique dans le leaseset. Nous ne prévoyons pas de faire cela.

Avantages de LS2 :

- L'emplacement de la clé publique réelle ne change pas.
- Le type de chiffrement, ou la clé publique, peut changer sans modifier la Destination.
- Supprime le champ de révocation inutilisé
- Compatibilité de base avec les autres types DatabaseEntry dans cette proposition
- Permet plusieurs types de chiffrement

Inconvénients de LS2 :

- L'emplacement de la clé publique et le type de chiffrement diffèrent du RouterInfo
- Maintient une clé publique inutilisée dans le leaseset
- Nécessite une implémentation à travers le réseau ; en alternative, des
  types de chiffrement expérimentaux peuvent être utilisés, s'ils sont autorisés par les floodfills
  (mais voir les propositions connexes 136 et 137 concernant le support des types de signature expérimentaux).
  La proposition alternative pourrait être plus facile à implémenter et tester pour les types de chiffrement expérimentaux.

### New Encryption Issues

Une partie de ceci dépasse le cadre de cette proposition, mais nous notons ces éléments ici pour l'instant car nous n'avons pas encore de proposition séparée pour le chiffrement. Voir aussi les propositions ECIES 144 et 145.

- Le type de chiffrement représente la combinaison
  de courbe, longueur de clé, et schéma de bout en bout,
  incluant KDF et MAC, le cas échéant.

- Nous avons inclus un champ de longueur de clé, de sorte que le LS2 soit
  analysable et vérifiable par le floodfill même pour les types de chiffrement inconnus.

- Le premier nouveau type de chiffrement qui sera probablement proposé sera
  ECIES/X25519. La façon dont il sera utilisé de bout en bout
  (soit une version légèrement modifiée d'ElGamal/AES+SessionTag
  ou quelque chose de complètement nouveau, par exemple ChaCha/Poly) sera spécifiée
  dans une ou plusieurs propositions séparées.
  Voir également les propositions ECIES 144 et 145.

### LeaseSet 2

- Expiration de 8 octets dans les leases changée à 4 octets.

- Si nous implémentons un jour la révocation, nous pouvons le faire avec un champ expires à zéro,
  ou zéro leases, ou les deux. Pas besoin d'une clé de révocation séparée.

- Les clés de chiffrement sont classées par ordre de préférence du serveur, la plus préférée en premier.
  Le comportement client par défaut consiste à sélectionner la première clé avec
  un type de chiffrement supporté. Les clients peuvent utiliser d'autres algorithmes de sélection
  basés sur la prise en charge du chiffrement, les performances relatives et d'autres facteurs.

### Format

Objectifs :

- Ajouter l'aveuglement
- Permettre plusieurs types de signatures
- Ne nécessiter aucune primitive cryptographique nouvelle
- Optionnellement chiffrer pour chaque destinataire, révocable
- Prendre en charge le chiffrement des Standard LS2 et Meta LS2 uniquement

Le LS2 chiffré n'est jamais envoyé dans un message garlic de bout en bout. Utilisez le LS2 standard comme ci-dessus.

Modifications par rapport au LeaseSet chiffré existant :

- Chiffrer l'ensemble pour la sécurité
- Chiffrer de manière sécurisée, pas seulement avec AES
- Chiffrer pour chaque destinataire

Rechercher avec

    Standard LS flag (1)
Stocker avec

    Encrypted LS2 type (5)
Stocker à

    Hash of blinded sig type and blinded public key
    Two byte sig type (big endian, e.g. 0x000b) || blinded public key
    This hash is then used to generate the daily "routing key", as in LS1
Expiration typique

    10 minutes, as in a regular LS, or hours, as in a meta LS.
Publié par

    Destination


### Justification

Nous définissons les fonctions suivantes correspondant aux blocs de construction cryptographiques utilisés pour les LS2 chiffrés :

CSRNG(n)

    n-byte output from a cryptographically-secure random number generator.

    In addition to the requirement of CSRNG being cryptographically-secure (and thus
    suitable for generating key material), it MUST be safe
    for some n-byte output to be used for key material when the byte sequences immediately
    preceding and following it are exposed on the network (such as in a salt, or encrypted
    padding). Implementations that rely on a potentially-untrustworthy source should hash
    any output that is to be exposed on the network. See [PRNG references](http://projectbullrun.org/dual-ec/ext-rand.html) and [Tor dev discussion](https://lists.torproject.org/pipermail/tor-dev/2015-November/009954.html).

H(p, d)

    SHA-256 hash function that takes a personalization string p and data d, and
    produces an output of length 32 bytes.

    Use SHA-256 as follows::

        H(p, d) := SHA-256(p || d)

STREAM

    The ChaCha20 stream cipher as specified in [RFC 7539 Section 2.4](https://tools.ietf.org/html/rfc7539#section-2.4), with the initial counter
    set to 1. S_KEY_LEN = 32 and S_IV_LEN = 12.

    ENCRYPT(k, iv, plaintext)
        Encrypts plaintext using the cipher key k, and nonce iv which MUST be unique for
        the key k. Returns a ciphertext that is the same size as the plaintext.

        The entire ciphertext must be indistinguishable from random if the key is secret.

    DECRYPT(k, iv, ciphertext)
        Decrypts ciphertext using the cipher key k, and nonce iv. Returns the plaintext.


SIG

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

DH

    X25519 public key agreement system. Private keys of 32 bytes, public keys of 32
    bytes, produces outputs of 32 bytes. It has the following
    functions:

    GENERATE_PRIVATE()
        Generates a new private key.

    DERIVE_PUBLIC(privkey)
        Returns the public key corresponding to the given private key.

    DH(privkey, pubkey)
        Generates a shared secret from the given private and public keys.

HKDF(salt, ikm, info, n)

    A cryptographic key derivation function which takes some input key material ikm (which
    should have good entropy but is not required to be a uniformly random string), a salt
    of length 32 bytes, and a context-specific 'info' value, and produces an output
    of n bytes suitable for use as key material.

    Use HKDF as specified in [RFC 5869](https://tools.ietf.org/html/rfc5869), using the HMAC hash function SHA-256
    as specified in [RFC 2104](https://tools.ietf.org/html/rfc2104). This means that SALT_LEN is 32 bytes max.


### Discussion

Le format LS2 chiffré consiste en trois couches imbriquées :

- Une couche externe contenant les informations en texte clair nécessaires pour le stockage et la récupération.
- Une couche intermédiaire qui gère l'authentification du client.
- Une couche interne qui contient les données LS2 réelles.

Le format général ressemble à ceci ::

    Layer 0 data + Enc(layer 1 data + Enc(layer 2 data)) + Signature

Notez que le LS2 chiffré est aveuglé. La Destination n'est pas dans l'en-tête. L'emplacement de stockage DHT est SHA-256(type de sig || clé publique aveuglée), et fait l'objet d'une rotation quotidienne.

N'utilise PAS l'en-tête LS2 standard spécifié ci-dessus.

#### Layer 0 (outer)

Type

    1 byte

    Not actually in header, but part of data covered by signature.
    Take from field in Database Store Message.

Type de signature de clé publique aveuglée

    2 bytes, big endian
    This will always be type 11, identifying a Red25519 blinded key.

Clé Publique Aveuglée

    Length as implied by sig type

Horodatage de publication

    4 bytes, big endian

    Seconds since epoch, rolls over in 2106

Expire

    2 bytes, big endian

    Offset from published timestamp in seconds, 18.2 hours max

Drapeaux

    2 bytes

    Bit order: 15 14 ... 3 2 1 0

    Bit 0: If 0, no offline keys; if 1, offline keys

    Other bits: set to 0 for compatibility with future uses

Données de clé transitoire

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

lenOuterCiphertext

    2 bytes, big endian

outerCiphertext

    lenOuterCiphertext bytes

    Encrypted layer 1 data. See below for key derivation and encryption algorithms.

Signature

    Length as implied by sig type of the signing key used

    The signature is of everything above.

    If the flag indicates offline keys, the signature is verified with the transient
    public key. Otherwise, the signature is verified with the blinded public key.


#### Layer 1 (middle)

Drapeaux

    1 byte
    
    Bit order: 76543210

    Bit 0: 0 for everybody, 1 for per-client, auth section to follow

    Bits 3-1: Authentication scheme, only if bit 0 is set to 1 for per-client, otherwise 000
              000: DH client authentication (or no per-client authentication)
              001: PSK client authentication

    Bits 7-4: Unused, set to 0 for future compatibility

Données d'authentification client DH

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

Données d'authentification client PSK

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


innerCiphertext

    Length implied by lenOuterCiphertext (whatever data remains)

    Encrypted layer 2 data. See below for key derivation and encryption algorithms.


#### Layer 2 (inner)

Type

    1 byte

    Either 3 (LS2) or 7 (Meta LS2)

Données

    LeaseSet2 data for the given type.

    Includes the header and signature.


### Nouveaux problèmes de chiffrement

Nous utilisons le schéma suivant pour l'aveuglement de clés, basé sur Ed25519 et [ZCash RedDSA](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf). Les signatures Re25519 sont sur la courbe Ed25519, utilisant SHA-512 pour le hachage.

Nous n'utilisons pas l'[appendice A.2 du rend-spec-v3.txt de Tor](https://spec.torproject.org/rend-spec-v3), qui a des objectifs de conception similaires, car ses clés publiques masquées peuvent être en dehors du sous-groupe d'ordre premier, avec des implications de sécurité inconnues.

#### Goals

- La clé publique de signature dans la destination non aveuglée doit être
  Ed25519 (type de signature 7) ou Red25519 (type de signature 11) ;
  aucun autre type de signature n'est pris en charge
- Si la clé publique de signature est hors ligne, la clé publique de signature transitoire doit également être Ed25519
- L'aveuglement est computationnellement simple
- Utilise des primitives cryptographiques existantes
- Les clés publiques aveuglées ne peuvent pas être désaveuglées
- Les clés publiques aveuglées doivent être sur la courbe Ed25519 et le sous-groupe d'ordre premier
- Doit connaître la clé publique de signature de la destination
  (destination complète non requise) pour dériver la clé publique aveuglée
- Fournit optionnellement un secret supplémentaire requis pour dériver la clé publique aveuglée

#### Security

La sécurité d'un schéma de masquage exige que la distribution d'alpha soit la même que celle des clés privées non masquées. Cependant, lorsque nous masquons une clé privée Ed25519 (type de signature 7) en une clé privée Red25519 (type de signature 11), la distribution est différente. Pour répondre aux exigences de [zcash section 4.1.6.1](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf), Red25519 (type de signature 11) devrait également être utilisé pour les clés non masquées, de sorte que "la combinaison d'une clé publique re-randomisée et de signature(s) sous cette clé ne révèle pas la clé à partir de laquelle elle a été re-randomisée." Nous autorisons le type 7 pour les destinations existantes, mais recommandons le type 11 pour les nouvelles destinations qui seront chiffrées.

#### Definitions

B

    The Ed25519 base point (generator) 2^255 - 19 as in [Ed25519](http://cr.yp.to/papers.html#ed25519)

L

    The Ed25519 order 2^252 + 27742317777372353535851937790883648493
    as in [Ed25519](http://cr.yp.to/papers.html#ed25519)

DERIVE_PUBLIC(a)

    Convert a private key to public, as in Ed25519 (mulitply by G)

alpha

    A 32-byte random number known to those who know the destination.

GENERATE_ALPHA(destination, date, secret)

    Generate alpha for the current date, for those who know the destination and the secret.
    The result must be identically distributed as Ed25519 private keys.

a

    The unblinded 32-byte EdDSA or RedDSA signing private key used to sign the destination

A

    The unblinded 32-byte EdDSA or RedDSA signing public key in the destination,
    = DERIVE_PUBLIC(a), as in Ed25519

a'

    The blinded 32-byte EdDSA signing private key used to sign the encrypted leaseset
    This is a valid EdDSA private key.

A'

    The blinded 32-byte EdDSA signing public key in the Destination,
    may be generated with DERIVE_PUBLIC(a'), or from A and alpha.
    This is a valid EdDSA public key, on the curve and on the prime-order subgroup.

LEOS2IP(x)

    Flip the order of the input bytes to little-endian

H*(x)

    32 bytes = (LEOS2IP(SHA512(x))) mod B, same as in Ed25519 hash-and-reduce


#### Blinding Calculations

De nouvelles clés alpha secrètes et aveugles doivent être générées chaque jour (UTC). L'alpha secret et les clés aveugles sont calculées comme suit.

GENERATE_ALPHA(destination, date, secret), pour toutes les parties :

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
BLIND_PRIVKEY(), pour le propriétaire publiant le leaseSet :

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
BLIND_PUBKEY(), pour les clients récupérant le leaseset :

```text
// BLIND_PUBKEY()

  alpha = GENERATE_ALPHA(destination, date, secret)
  A = destination's signing public key
  // Addition using group elements (points on the curve)
  blinded public key = A' = BLIND_PUBKEY(A, alpha) = A + DERIVE_PUBLIC(alpha)
```
Les deux méthodes de calcul de A' donnent le même résultat, comme requis.

#### Signing

Le leaseSet non-aveuglé est signé par la clé privée de signature Ed25519 ou Red25519 non-aveuglée et vérifié avec la clé publique de signature Ed25519 ou Red25519 non-aveuglée (types de signature 7 ou 11) comme d'habitude.

Si la clé publique de signature est hors ligne, le leaseset non-aveuglé est signé par la clé privée de signature transitoire Ed25519 ou Red25519 non-aveuglée et vérifié avec la clé publique de signature transitoire Ed25519 ou Red25519 non-aveuglée (types de signature 7 ou 11) comme d'habitude. Voir ci-dessous pour des notes supplémentaires sur les clés hors ligne pour les leasesets chiffrés.

Pour la signature du leaseset chiffré, nous utilisons Red25519, basé sur [RedDSA](https://github.com/zcash/zips/tree/master/protocol/protocol.pdf) pour signer et vérifier avec des clés aveugles. Les signatures Red25519 utilisent la courbe Ed25519, avec SHA-512 pour le hachage.

Red25519 est identique à l'Ed25519 standard sauf comme spécifié ci-dessous.

#### Sign/Verify Calculations

La partie externe du leaseset chiffré utilise des clés et signatures Red25519.

Red25519 est presque identique à Ed25519. Il y a deux différences :

Les clés privées Red25519 sont générées à partir de nombres aléatoires et doivent ensuite être réduites modulo L, où L est défini ci-dessus. Les clés privées Ed25519 sont générées à partir de nombres aléatoires puis "bridées" en utilisant un masquage au niveau des bits pour les octets 0 et 31. Ceci n'est pas fait pour Red25519. Les fonctions GENERATE_ALPHA() et BLIND_PRIVKEY() définies ci-dessus génèrent des clés privées Red25519 appropriées en utilisant mod L.

Dans Red25519, le calcul de r pour la signature utilise des données aléatoires supplémentaires, et utilise la valeur de la clé publique plutôt que le hachage de la clé privée. En raison des données aléatoires, chaque signature Red25519 est différente, même lors de la signature des mêmes données avec la même clé.

Signature :

```text
T = 80 random bytes
  r = H*(T || publickey || message)
  // rest is the same as in Ed25519
```
Vérification :

```text
// same as in Ed25519
```
### Notes

#### Derivation of subcredentials

Dans le cadre du processus d'aveuglement, nous devons nous assurer qu'un LS2 chiffré ne peut être déchiffré que par quelqu'un qui connaît la clé publique de signature de la Destination correspondante. La Destination complète n'est pas requise. Pour y parvenir, nous dérivons un identifiant de la clé publique de signature :

```text
A = destination's signing public key
  stA = signature type of A, 2 bytes big endian (0x0007 or 0x000b)
  stA' = signature type of A', 2 bytes big endian (0x000b)
  keydata = A || stA || stA'
  credential = H("credential", keydata)
```
La chaîne de personnalisation garantit que les identifiants ne rentrent pas en collision avec tout hash utilisé comme clé de recherche DHT, comme le hash de Destination simple.

Pour une clé aveuglée donnée, nous pouvons alors dériver une sous-credential :

```text
subcredential = H("subcredential", credential || blindedPublicKey)
```
Le sous-identifiant est inclus dans les processus de dérivation de clés ci-dessous, ce qui lie ces clés à la connaissance de la clé publique de signature de la Destination.

#### Layer 1 encryption

Premièrement, l'entrée du processus de dérivation de clé est préparée :

```text
outerInput = subcredential || publishedTimestamp
```
Ensuite, un sel aléatoire est généré :

```text
outerSalt = CSRNG(32)
```
Ensuite, la clé utilisée pour chiffrer la couche 1 est dérivée :

```text
keys = HKDF(outerSalt, outerInput, "ELS2_L1K", 44)
  outerKey = keys[0:31]
  outerIV = keys[32:43]
```
Enfin, le texte en clair de la couche 1 est chiffré et sérialisé :

```text
outerCiphertext = outerSalt || ENCRYPT(outerKey, outerIV, outerPlaintext)
```
#### Layer 1 decryption

Le salt est analysé à partir du texte chiffré de la couche 1 :

```text
outerSalt = outerCiphertext[0:31]
```
Ensuite, la clé utilisée pour chiffrer la couche 1 est dérivée :

```text
outerInput = subcredential || publishedTimestamp
  keys = HKDF(outerSalt, outerInput, "ELS2_L1K", 44)
  outerKey = keys[0:31]
  outerIV = keys[32:43]
```
Enfin, le texte chiffré de la couche 1 est déchiffré :

```text
outerPlaintext = DECRYPT(outerKey, outerIV, outerCiphertext[32:end])
```
#### Layer 2 encryption

Lorsque l'autorisation client est activée, ``authCookie`` est calculé comme décrit ci-dessous. Lorsque l'autorisation client est désactivée, ``authCookie`` est le tableau d'octets de longueur nulle.

Le chiffrement procède de manière similaire à la couche 1 :

```text
innerInput = authCookie || subcredential || publishedTimestamp
  innerSalt = CSRNG(32)
  keys = HKDF(innerSalt, innerInput, "ELS2_L2K", 44)
  innerKey = keys[0:31]
  innerIV = keys[32:43]
  innerCiphertext = innerSalt || ENCRYPT(innerKey, innerIV, innerPlaintext)
```
#### Layer 2 decryption

Lorsque l'autorisation client est activée, ``authCookie`` est calculé comme décrit ci-dessous. Lorsque l'autorisation client est désactivée, ``authCookie`` est le tableau d'octets de longueur nulle.

Le déchiffrement procède de manière similaire à la couche 1 :

```text
innerInput = authCookie || subcredential || publishedTimestamp
  innerSalt = innerCiphertext[0:31]
  keys = HKDF(innerSalt, innerInput, "ELS2_L2K", 44)
  innerKey = keys[0:31]
  innerIV = keys[32:43]
  innerPlaintext = DECRYPT(innerKey, innerIV, innerCiphertext[32:end])
```
### LS2 Chiffré

Lorsque l'autorisation client est activée pour une Destination, le serveur maintient une liste des clients qu'il autorise à déchiffrer les données LS2 chiffrées. Les données stockées par client dépendent du mécanisme d'autorisation et incluent une certaine forme de matériel cryptographique que chaque client génère et envoie au serveur via un mécanisme sécurisé hors bande.

Il existe deux alternatives pour implémenter l'autorisation par client :

#### DH client authorization

Chaque client génère une paire de clés DH ``[csk_i, cpk_i]``, et envoie la clé publique ``cpk_i`` au serveur.

Traitement serveur
^^^^^^^^^^^^^^^^^

Le serveur génère un nouveau ``authCookie`` et une paire de clés DH éphémère :

```text
authCookie = CSRNG(32)
  esk = GENERATE_PRIVATE()
  epk = DERIVE_PUBLIC(esk)
```
Ensuite, pour chaque client autorisé, le serveur chiffre ``authCookie`` avec sa clé publique :

```text
sharedSecret = DH(esk, cpk_i)
  authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
  okm = HKDF(epk, authInput, "ELS2_XCA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
  clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
```
Le serveur place chaque tuple ``[clientID_i, clientCookie_i]`` dans la couche 1 du LS2 chiffré, ainsi que ``epk``.

Traitement du client
^^^^^^^^^^^^^^^^^

Le client utilise sa clé privée pour dériver son identifiant client attendu ``clientID_i``, sa clé de chiffrement ``clientKey_i``, et son IV de chiffrement ``clientIV_i`` :

```text
sharedSecret = DH(csk_i, epk)
  authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
  okm = HKDF(epk, authInput, "ELS2_XCA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
```
Ensuite, le client recherche dans les données d'autorisation de couche 1 une entrée qui contient ``clientID_i``. Si une entrée correspondante existe, le client la déchiffre pour obtenir ``authCookie`` :

```text
authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie_i)
```
#### Pre-shared key client authorization

Chaque client génère une clé secrète de 32 octets ``psk_i``, et l'envoie au serveur. Alternativement, le serveur peut générer la clé secrète, et l'envoyer à un ou plusieurs clients.

Traitement du serveur
^^^^^^^^^^^^^^^^^

Le serveur génère un nouveau ``authCookie`` et salt :

```text
authCookie = CSRNG(32)
  authSalt = CSRNG(32)
```
Ensuite, pour chaque client autorisé, le serveur chiffre ``authCookie`` avec sa clé pré-partagée :

```text
authInput = psk_i || subcredential || publishedTimestamp
  okm = HKDF(authSalt, authInput, "ELS2PSKA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
  clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
```
Le serveur place chaque tuple ``[clientID_i, clientCookie_i]`` dans la couche 1 du LS2 chiffré, ainsi que ``authSalt``.

Traitement côté client
^^^^^^^^^^^^^^^^^^^^^^^^^

Le client utilise sa clé pré-partagée pour dériver son identifiant client attendu ``clientID_i``, sa clé de chiffrement ``clientKey_i``, et son vecteur d'initialisation de chiffrement ``clientIV_i`` :

```text
authInput = psk_i || subcredential || publishedTimestamp
  okm = HKDF(authSalt, authInput, "ELS2PSKA", 52)
  clientKey_i = okm[0:31]
  clientIV_i = okm[32:43]
  clientID_i = okm[44:51]
```
Ensuite, le client recherche dans les données d'autorisation de la couche 1 une entrée qui contient ``clientID_i``. Si une entrée correspondante existe, le client la déchiffre pour obtenir ``authCookie`` :

```text
authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie_i)
```
#### Security considerations

Les deux mécanismes d'autorisation client ci-dessus offrent une confidentialité pour l'appartenance des clients. Une entité qui ne connaît que la Destination peut voir combien de clients sont abonnés à tout moment, mais ne peut pas suivre quels clients sont ajoutés ou révoqués.

Les serveurs DEVRAIENT randomiser l'ordre des clients à chaque fois qu'ils génèrent un LS2 chiffré, pour empêcher les clients d'apprendre leur position dans la liste et de déduire quand d'autres clients ont été ajoutés ou révoqués.

Un serveur PEUT choisir de masquer le nombre de clients abonnés en insérant des entrées aléatoires dans la liste des données d'autorisation.

Avantages de l'autorisation client DH
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- La sécurité du schéma ne dépend pas uniquement de l'échange hors bande du matériel de   clé client. La clé privée du client n'a jamais besoin de quitter son appareil, et donc   un adversaire qui est capable d'intercepter l'échange hors bande, mais ne peut pas   casser l'algorithme DH, ne peut pas déchiffrer le LS2 chiffré, ou déterminer combien   de temps l'accès est accordé au client.

Inconvénients de l'autorisation client DH
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Nécessite N + 1 opérations DH côté serveur pour N clients.
- Nécessite une opération DH côté client.
- Nécessite que le client génère la clé secrète.

Avantages de l'autorisation client PSK
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Ne nécessite aucune opération DH.
- Permet au serveur de générer la clé secrète.
- Permet au serveur de partager la même clé avec plusieurs clients, si souhaité.

Inconvénients de l'autorisation client PSK
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- La sécurité du schéma dépend de manière critique de l'échange hors bande du matériel de clé client. Un adversaire qui intercepte l'échange pour un client particulier peut déchiffrer tout leaseSet LS2 chiffré ultérieur pour lequel ce client est autorisé, ainsi que déterminer quand l'accès du client est révoqué.

### Définitions

Voir la proposition 149.

Vous ne pouvez pas utiliser un LS2 chiffré pour bittorrent, à cause des réponses d'annonce compactes qui font 32 octets. Les 32 octets ne contiennent que le hash. Il n'y a pas de place pour une indication que le leaseSet est chiffré, ou les types de signature.

### Format

Pour les leaseSets chiffrés avec des clés hors ligne, les clés privées masquées doivent également être générées hors ligne, une pour chaque jour.

Comme le bloc de signature hors ligne optionnel se trouve dans la partie en clair du leaseset chiffré, toute personne récupérant les données des floodfills pourrait l'utiliser pour suivre le leaseset (mais pas le déchiffrer) sur plusieurs jours. Pour éviter cela, le propriétaire des clés devrait également générer de nouvelles clés transitoires pour chaque jour. Les clés transitoires et aveugles peuvent être générées à l'avance et livrées au router par lots.

Il n'y a pas de format de fichier défini dans cette proposition pour empaqueter plusieurs clés transitoires et aveugles et les fournir au client ou au router. Il n'y a pas d'amélioration du protocole I2CP définie dans cette proposition pour prendre en charge les leasesets chiffrés avec des clés hors ligne.

### Notes

- Un service utilisant des leaseSets chiffrés publierait la version chiffrée vers les
  floodfills. Cependant, pour des raisons d'efficacité, il enverrait des leaseSets non chiffrés aux
  clients dans le message garlic encapsulé, une fois authentifiés (via une liste blanche, par
  exemple).

- Les floodfills peuvent limiter la taille maximale à une valeur raisonnable pour éviter les abus.

- Après le déchiffrement, plusieurs vérifications doivent être effectuées, notamment que
  l'horodatage interne et l'expiration correspondent à ceux du niveau supérieur.

- ChaCha20 a été choisi plutôt qu'AES. Bien que les vitesses soient similaires si le support matériel AES est disponible, ChaCha20 est 2,5 à 3 fois plus rapide lorsque le support matériel AES n'est pas disponible, comme sur les appareils ARM d'entrée de gamme.

- Nous ne nous préoccupons pas suffisamment de la vitesse pour utiliser BLAKE2b avec clé. Il a une taille de sortie suffisamment grande pour accommoder le plus grand n dont nous avons besoin (ou nous pouvons l'appeler une fois par clé désirée avec un argument de compteur). BLAKE2b est beaucoup plus rapide que SHA-256, et keyed-BLAKE2b réduirait le nombre total d'appels de fonction de hachage.
  Cependant, voir la proposition 148, où il est proposé que nous passions à BLAKE2b pour d'autres raisons.
  Voir [Secure key derivation performance](https://www.lvh.io/posts/secure-key-derivation-performance.html).

### Meta LS2

Ceci est utilisé pour remplacer le multihoming. Comme tout leaseSet, celui-ci est signé par le créateur. Il s'agit d'une liste authentifiée de hashes de destination.

Le Meta LS2 est au sommet de, et possiblement aux nœuds intermédiaires de, une structure arborescente. Il contient un certain nombre d'entrées, chacune pointant vers un LS, LS2, ou un autre Meta LS2 pour supporter un multihébergement massif. Un Meta LS2 peut contenir un mélange d'entrées LS, LS2, et Meta LS2. Les feuilles de l'arbre sont toujours un LS ou LS2. L'arbre est un DAG ; les boucles sont interdites ; les clients effectuant des recherches doivent détecter et refuser de suivre les boucles.

Un Meta LS2 peut avoir une expiration beaucoup plus longue qu'un LS ou LS2 standard. Le niveau supérieur peut avoir une expiration plusieurs heures après la date de publication. Le temps d'expiration maximum sera appliqué par les floodfills et les clients, et reste à déterminer.

L'utilisation prévue pour Meta LS2 est le multihoming massif, mais sans plus de protection contre la corrélation des routers aux leasesets (au moment du redémarrage du router) que celle fournie actuellement avec LS ou LS2. Ceci est équivalent au cas d'usage "facebook", qui n'a probablement pas besoin de protection contre la corrélation. Ce cas d'usage nécessite probablement des clés hors ligne, qui sont fournies dans l'en-tête standard à chaque nœud de l'arbre.

Le protocole back-end pour la coordination entre les routeurs feuilles, les signataires Meta LS intermédiaires et maîtres n'est pas spécifié ici. Les exigences sont extrêmement simples - il suffit de vérifier que le pair est actif, et publier un nouveau LS toutes les quelques heures. La seule complexité consiste à choisir de nouveaux éditeurs pour les Meta LSes de niveau supérieur ou intermédiaire en cas de défaillance.

Mix-and-match leasesets où les leases de plusieurs routers sont combinés, signés et publiés dans un seul leaseset est documenté dans la proposition 140, "invisible multihoming". Cette proposition est intenable telle qu'écrite, car les connexions streaming ne seraient pas "collantes" à un seul router, voir http://zzz.i2p/topics/2335 .

Le protocole back-end, et l'interaction avec les composants internes du router et du client, seraient assez complexes pour le multihoming invisible.

Pour éviter de surcharger le floodfill pour le Meta LS de niveau supérieur, l'expiration devrait être d'au moins plusieurs heures. Les clients doivent mettre en cache le Meta LS de niveau supérieur et le conserver lors des redémarrages s'il n'a pas expiré.

Nous devons définir un algorithme pour que les clients traversent l'arbre, y compris les solutions de repli, afin que l'utilisation soit dispersée. Une fonction basée sur la distance de hachage, le coût et le caractère aléatoire. Si un nœud possède à la fois LS ou LS2 et Meta LS, nous devons savoir quand il est permis d'utiliser ces leasesets, et quand continuer à traverser l'arbre.

Rechercher avec

    Standard LS flag (1)
Stocker avec

    Meta LS2 type (7)
Stocker à

    Hash of destination
    This hash is then used to generate the daily "routing key", as in LS1
Expiration typique

    Hours. Max 18.2 hours (65535 seconds)
Publié par

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
Drapeaux et propriétés : pour usage futur

### Dérivation de Clé d'Aveuglement

- Un service distribué utilisant ceci aurait un ou plusieurs "maîtres" avec la
  clé privée de la destination du service. Ils détermineraient (hors bande) la
  liste actuelle des destinations actives et publieraient le Meta LS2. Pour la
  redondance, plusieurs maîtres pourraient faire du multihoming (c'est-à-dire publier
  simultanément) le Meta LS2.

- Un service distribué pourrait commencer avec une destination unique ou utiliser l'ancien style de multihébergement, puis passer à un Meta LS2. Une recherche LS standard pourrait retourner n'importe lequel parmi un LS, LS2, ou Meta LS2.

- Lorsqu'un service utilise un Meta LS2, il n'a pas de tunnels (leases).

### Service Record

Il s'agit d'un enregistrement individuel indiquant qu'une destination participe à un service. Il est envoyé du participant vers le floodfill. Il n'est jamais envoyé individuellement par un floodfill, mais uniquement comme partie d'une Service List. Le Service Record est également utilisé pour révoquer la participation à un service, en définissant l'expiration à zéro.

Ceci n'est pas un LS2 mais il utilise le format d'en-tête et de signature LS2 standard.

Recherche avec

    n/a, see Service List
Stocker avec

    Service Record type (9)
Stocker à

    Hash of service name
    This hash is then used to generate the daily "routing key", as in LS1
Expiration typique

    Hours. Max 18.2 hours (65535 seconds)
Publié par

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

- Si expires est composé uniquement de zéros, le floodfill devrait révoquer l'enregistrement et ne plus l'inclure dans la liste de services.

- Stockage : Le floodfill peut strictement limiter le stockage de ces enregistrements et
  restreindre le nombre d'enregistrements stockés par hash ainsi que leur expiration. Une liste blanche
  de hashs peut également être utilisée.

- Tout autre type netdb au même hash a la priorité, donc un enregistrement de service ne peut jamais
  écraser un LS/RI, mais un LS/RI écrasera tous les enregistrements de service à ce hash.

### Service List

Ceci n'a rien à voir avec un LS2 et utilise un format différent.

La liste de services est créée et signée par le floodfill. Elle n'est pas authentifiée dans le sens où n'importe qui peut rejoindre un service en publiant un Service Record vers un floodfill.

Une Liste de Services contient des Enregistrements de Service Courts, pas des Enregistrements de Service complets. Ceux-ci contiennent des signatures mais seulement des hachages, pas des destinations complètes, donc ils ne peuvent pas être vérifiés sans la destination complète.

La sécurité, le cas échéant, et la pertinence des listes de services reste à déterminer. Les floodfills pourraient limiter la publication, et les recherches, à une liste blanche de services, mais cette liste blanche peut varier selon l'implémentation ou les préférences de l'opérateur. Il pourrait ne pas être possible d'atteindre un consensus sur une liste blanche commune de base entre les implémentations.

Si le nom du service est inclus dans l'enregistrement de service ci-dessus, alors les opérateurs de floodfill peuvent s'opposer ; si seul le hash est inclus, il n'y a pas de vérification, et un enregistrement de service pourrait « s'introduire » avant tout autre type netDb et être stocké dans le floodfill.

Recherche avec

    Service List lookup type (11)
Stocker avec

    Service List type (11)
Stocker à

    Hash of service name
    This hash is then used to generate the daily "routing key", as in LS1
Expiration typique

    Hours, not specified in the list itself, up to local policy
Publié par

    Nobody, never sent to floodfill, never flooded.

### Format

N'utilise PAS l'en-tête LS2 standard spécifié ci-dessus.

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
Pour vérifier la signature de la Service List :

- ajouter le hash du nom du service au début
- supprimer le hash du créateur
- Vérifier la signature du contenu modifié

Pour vérifier la signature de chaque Short Service Record :

- Récupérer la destination
- Vérifier la signature de (horodatage publié + expiration + drapeaux + port + Hash du
  nom de service)

Pour vérifier la signature de chaque Enregistrement de Révocation :

- Récupérer la destination
- Vérifier la signature de (horodatage publié + 4 octets zéro + drapeaux + port + Hash
  du nom de service)

### Notes

- Nous utilisons la longueur de signature au lieu du type de signature afin de pouvoir prendre en charge les types de signature inconnus.

- Il n'y a pas d'expiration d'une liste de services, les destinataires peuvent prendre leur propre décision basée sur la politique ou l'expiration des enregistrements individuels.

- Les listes de services ne sont pas diffusées, seuls les enregistrements de service individuels le sont. Chaque floodfill crée, signe et met en cache une liste de services. Le floodfill utilise sa propre politique pour le temps de mise en cache et le nombre maximum d'enregistrements de service et de révocation.

## Common Structures Spec Changes Required

### Chiffrement et traitement

Hors du périmètre de cette proposition. À ajouter aux propositions ECIES 144 et 145.

### New Intermediate Structures

Ajouter de nouvelles structures pour Lease2, MetaLease, LeaseSet2Header, et OfflineSignature. Effectif à partir de la version 0.9.38.

### New NetDB Types

Ajouter des structures pour chaque nouveau type de leaseset, incorporées depuis ci-dessus. Pour LeaseSet2, EncryptedLeaseSet, et MetaLeaseSet, effectif à partir de la version 0.9.38. Pour Service Record et Service List, préliminaire et non programmé.

### New Signature Type

Ajouter RedDSA_SHA512_Ed25519 Type 11. La clé publique fait 32 octets ; la clé privée fait 32 octets ; le hachage fait 64 octets ; la signature fait 64 octets.

## Encryption Spec Changes Required

Hors du périmètre de cette proposition. Voir les propositions 144 et 145.

## I2NP Changes Required

Ajouter une note : LS2 ne peut être publié que vers des floodfills avec une version minimale.

### Database Lookup Message

Ajouter le type de recherche de liste de services.

### Changes

```
Flags byte: Lookup type field, currently bits 3-2, expands to bits 4-2.
  Lookup type 0x04 is defined as the service list lookup.

  Add note: Service list loookup may only be sent to floodfills with a minimum version.
  Minimum version is 0.9.38.
```
### Autorisation par client

Ajouter tous les nouveaux types de magasin.

### Changes

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
## I2CP Changes Required

### I2CP Options

Nouvelles options interprétées côté router, envoyées dans le Mapping SessionConfig :

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
### Session Config

Notez que pour les signatures hors ligne, les options i2cp.leaseSetOfflineExpiration, i2cp.leaseSetTransientPublicKey, et i2cp.leaseSetOfflineSignature sont requises, et la signature est effectuée par la clé privée de signature transitoire.

### LS chiffré avec adresses Base 32

Routeur vers client. Aucun changement. Les leases sont envoyés avec des horodatages de 8 octets, même si le leaseSet retourné sera un LS2 avec des horodatages de 4 octets. Notez que la réponse peut être un message Create Leaseset ou Create Leaseset2.

### LS chiffré avec clés hors ligne

Routeur vers client. Aucun changement. Les baux sont envoyés avec des horodatages de 8 octets, même si le leaseSet retourné sera un LS2 avec des horodatages de 4 octets. Notez que la réponse peut être un message Create Leaseset ou Create Leaseset2.

### Notes

Client vers routeur. Nouveau message, à utiliser à la place du message Create Leaseset.

### Meta LS2

- Pour que le routeur analyse le type de stockage, le type doit être dans le message,
  sauf s'il est transmis au routeur au préalable dans la configuration de session.
  Pour un code d'analyse commun, il est plus facile de l'avoir dans le message lui-même.

- Pour que le routeur connaisse le type et la longueur de la clé privée,
  elle doit être placée après le lease set, sauf si l'analyseur connaît le type à l'avance
  dans la configuration de session.
  Pour un code d'analyse commun, il est plus facile de le connaître depuis le message lui-même.

- La clé privée de signature, précédemment définie pour la révocation et non utilisée,
  n'est pas présente dans LS2.

### Format

Le type de message pour le message Create Leaseset2 est 41.

### Notes

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
### Enregistrement de Service

- La version minimale du routeur est 0.9.39.
- La version préliminaire avec le type de message 40 était dans la 0.9.38 mais le format a été modifié.
  Le type 40 est abandonné et n'est plus pris en charge.

### Format

- D'autres modifications sont nécessaires pour prendre en charge les LS chiffrés et méta.

### Notes

Client vers routeur. Nouveau message.

### Liste des Services

- Le routeur doit savoir si une destination est masquée.
  Si elle est masquée et utilise une authentification secrète ou par client,
  il doit également disposer de cette information.

- Une Recherche d'Hôte d'une adresse b32 de nouveau format ("b33")
  indique au router que l'adresse est aveuglée, mais il n'y a aucun mécanisme pour
  transmettre la clé secrète ou privée au router dans le message de Recherche d'Hôte.
  Bien que nous puissions étendre le message de Recherche d'Hôte pour ajouter cette information,
  il est plus propre de définir un nouveau message.

- Nous avons besoin d'un moyen programmatique pour que le client informe le router.
  Sinon, l'utilisateur devrait configurer manuellement chaque destination.

### Format

Avant qu'un client envoie un message vers une destination aveuglée, il doit soit rechercher le "b33" dans un message Host Lookup, soit envoyer un message Blinding Info. Si la destination aveuglée nécessite un secret ou une authentification par client, le client doit envoyer un message Blinding Info.

Le routeur n'envoie pas de réponse à ce message.

### Notes

Le type de message pour le Message d'Information de Masquage est 42.

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
### Certificats de Clé

- La version minimale du router est 0.9.43

### Nouvelles Structures Intermédiaires

### Nouveaux types NetDB

Pour prendre en charge les recherches de noms d'hôte "b33" et retourner une indication si le router ne possède pas les informations requises, nous définissons des codes de résultat supplémentaires pour le message de réponse d'hôte (Host Reply Message), comme suit :

```
2: Lookup password required
   3: Private key required
   4: Lookup password and private key required
   5: Leaseset decryption failure
```
Les valeurs 1-255 sont déjà définies comme des erreurs, il n'y a donc aucun problème de rétrocompatibilité.

### Nouveau type de signature

Routeur vers client. Nouveau message.

### Justification

Un client ne sait pas a priori qu'un Hash donné se résoudra en un Meta LS.

Si une recherche de leaseset pour une Destination renvoie un Meta LS, le router effectuera la résolution récursive. Pour les datagrammes, le côté client n'a pas besoin de le savoir ; cependant, pour le streaming, où le protocole vérifie la destination dans le SYN ACK, il doit savoir quelle est la destination "réelle". Par conséquent, nous avons besoin d'un nouveau message.

### Usage

Le router maintient un cache pour la destination réelle utilisée à partir d'un meta LS. Lorsque le client envoie un message à une destination qui se résout en meta LS, le router vérifie le cache pour la destination réelle utilisée en dernier. Si le cache est vide, le router sélectionne une destination du meta LS et recherche le leaseSet. Si la recherche du leaseSet réussit, le router ajoute cette destination au cache et envoie au client un Meta Redirect Message. Ceci n'est fait qu'une seule fois, sauf si la destination expire et doit être changée. Le client doit également mettre en cache l'information si nécessaire. Le Meta Redirect Message n'est PAS envoyé en réponse à chaque SendMessage.

Le routeur n'envoie ce message qu'aux clients avec la version 0.9.47 ou supérieure.

Le client n'envoie pas de réponse à ce message.

### Message de Recherche de Base de Données

Le type de message pour le Meta Redirect Message est 43.

### Changements

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
### Message de stockage de base de données

Comment générer et prendre en charge Meta, y compris la communication et la coordination entre routeurs, dépasse le cadre de cette proposition. Voir la proposition connexe 150.

### Changements

Les signatures hors ligne ne peuvent pas être vérifiées dans les datagrammes en streaming ou avec réponse. Voir les sections ci-dessous.

## Private Key File Changes Required

Le format du fichier de clé privée (eepPriv.dat) ne fait pas partie officielle de nos spécifications mais il est documenté dans la [javadoc Java I2P](http://idk.i2p/javadoc-i2p/net/i2p/data/PrivateKeyFile.html) et d'autres implémentations le prennent en charge. Ceci permet la portabilité des clés privées vers différentes implémentations.

Des modifications sont nécessaires pour stocker la clé publique temporaire et les informations de signature hors ligne.

### Changes

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
### Options I2CP

Ajouter la prise en charge des options suivantes :

```
-d days              (specify expiration in days of offline sig, default 365)
      -o offlinedestfile   (generate the online key file,
                            using the offline key file specified)
      -r sigtype           (specify sig type of transient key, default Ed25519)
```
## Streaming Changes Required

Les signatures hors ligne ne peuvent actuellement pas être vérifiées dans le streaming. Le changement ci-dessous ajoute le bloc de signature hors ligne aux options. Cela évite d'avoir à récupérer cette information via I2CP.

### Configuration de session

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
### Message de Demande de Leaseset

- L'alternative est d'ajouter simplement un flag, et de récupérer la clé publique transitoire via I2CP
  (Voir les sections Message de Recherche d'Hôte / Message de Réponse d'Hôte ci-dessus)

## En-tête LS2 standard

Les signatures hors ligne ne peuvent pas être vérifiées dans le traitement des datagrammes répondables. Nécessite un indicateur pour signaler une signature hors ligne mais il n'y a pas d'endroit où placer un indicateur. Cela nécessitera un numéro de protocole et un format entièrement nouveaux.

### Message de Demande de LeaseSet Variable

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
### Créer un message Leaseset2

- L'alternative est d'ajouter simplement un flag, et de récupérer la clé publique transiente via I2CP
  (Voir les sections Host Lookup / Host Reply Message ci-dessus)
- Y a-t-il d'autres options que nous devrions ajouter maintenant que nous avons des octets de flag ?

## SAM V3 Changes Required

SAM doit être amélioré pour prendre en charge les signatures hors ligne dans le DESTINATION base 64.

### Justification

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
Notez que les signatures hors ligne ne sont prises en charge que pour STREAM et RAW, pas pour DATAGRAM (jusqu'à ce que nous définissions un nouveau protocole DATAGRAM).

Notez que le SESSION STATUS retournera une Signing Private Key composée uniquement de zéros et les données Offline Signature exactement telles que fournies dans le SESSION CREATE.

Notez que DEST GENERATE et SESSION CREATE DESTINATION=TRANSIENT ne peuvent pas être utilisés pour créer une destination signée hors ligne.

### Type de message

Augmenter la version à 3.4, ou la laisser à 3.1/3.2/3.3 pour qu'elle puisse être ajoutée sans nécessiter tout le contenu 3.2/3.3 ?

Autres changements à déterminer. Voir la section Message de réponse d'hôte I2CP ci-dessus.

## BOB Changes Required

BOB devrait être amélioré pour prendre en charge les signatures hors ligne et/ou les Meta LS. Ceci est de faible priorité et ne sera probablement jamais spécifié ou implémenté. SAM V3 est l'interface privilégiée.

## Publishing, Migration, Compatibility

LS2 (autre que LS2 chiffré) est publié au même emplacement DHT que LS1. Il n'y a aucun moyen de publier à la fois un LS1 et un LS2, à moins que LS2 ne soit à un emplacement différent.

Le LS2 chiffré est publié au hash du type de clé aveuglée et des données de clé. Ce hash est ensuite utilisé pour générer la "clé de routage" quotidienne, comme dans LS1.

LS2 ne serait utilisé que lorsque de nouvelles fonctionnalités sont requises (nouvelle crypto, LS chiffré, méta, etc.). LS2 ne peut être publié que vers des floodfills d'une version spécifiée ou supérieure.

Les serveurs publiant des LS2 sauraient que tous les clients se connectant supportent LS2. Ils pourraient envoyer des LS2 dans le garlic.

Les clients enverraient les LS2 dans les garlics uniquement s'ils utilisent la nouvelle cryptographie. Les clients partagés utiliseraient les LS1 indéfiniment ? TODO : Comment avoir des clients partagés qui supportent à la fois l'ancienne et la nouvelle cryptographie ?

## Rollout

0.9.38 contient le support floodfill pour LS2 standard, y compris les clés hors ligne.

La version 0.9.39 contient le support I2CP pour LS2 et Encrypted LS2, la signature/vérification de type sig 11, le support floodfill pour Encrypted LS2 (types sig 7 et 11, sans clés hors ligne), et le chiffrement/déchiffrement LS2 (sans autorisation par client).

0.9.40 est prévue pour inclure la prise en charge du chiffrement/déchiffrement des LS2 avec autorisation par client, le support floodfill et I2CP pour Meta LS2, la prise en charge des LS2 chiffrées avec clés hors ligne, et le support b32 pour les LS2 chiffrées.

## Nouveaux types de DatabaseEntry

La conception du LS2 chiffré est fortement influencée par [les descripteurs de services cachés v3 de Tor](https://spec.torproject.org/rend-spec-v3), qui avaient des objectifs de conception similaires.
