---
title: "B32 pour les Leasesets chiffrés"
description: "Format d’adresse Base 32 pour les leaseSets LS2 chiffrés"
slug: "b32-for-encrypted-leasesets"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
status: "Implémenté"
---

## Aperçu

Les adresses Base 32 standard ("b32") contiennent le hachage de la destination. Cela ne fonctionnera pas pour LS2 (leaseSet version 2) chiffré (proposition 123).

Nous ne pouvons pas utiliser une adresse traditionnelle en base 32 pour un LS2 chiffré (proposition 123), car elle ne contient que le hachage de la destination. Elle ne fournit pas la clé publique non aveuglée. Les clients doivent connaître la clé publique de la destination, le type de signature, le type de signature de la clé aveuglée, ainsi qu’un secret ou une clé privée facultatifs pour récupérer et déchiffrer le leaseset. Par conséquent, une adresse en base 32 seule est insuffisante. Le client a besoin soit de la destination complète (qui contient la clé publique), soit de la clé publique seule. Si le client dispose de la destination complète dans un carnet d’adresses, et que ce carnet prend en charge la recherche inverse par hachage, alors la clé publique peut être récupérée.

Ce format place la clé publique, au lieu du hachage, dans une adresse en base32. Ce format doit également contenir le type de signature de la clé publique, ainsi que le type de signature du schéma d’aveuglement.

Ce document spécifie un format b32 pour ces adresses. Bien que nous ayons désigné ce nouveau format, lors des discussions, comme une "adresse b33", le format effectivement retenu conserve le suffixe habituel ".b32.i2p".

## Statut de l'implémentation

Proposition 123 (Nouvelles entrées netDB) a été entièrement implémentée dans la version 0.9.43 (octobre 2019). L'ensemble des fonctionnalités de LS2 (version 2 de leaseSet) chiffré est resté stable jusqu'à la version 2.10.0 (septembre 2025), sans modifications rompant la compatibilité du format d'adressage ni des spécifications cryptographiques.

Jalons clés de l'implémentation : - 0.9.38 : Prise en charge de Floodfill pour LS2 standard avec des clés hors ligne - 0.9.39 : Type de signature RedDSA 11 et chiffrement/déchiffrement de base - 0.9.40 : Prise en charge complète de l'adressage B32 (Proposition 149) - 0.9.41 : Authentification par client basée sur X25519 - 0.9.42 : Toutes les fonctionnalités d'aveuglement opérationnelles - 0.9.43 : Implémentation complète déclarée (octobre 2019)

## Conception

- Le nouveau format contient la clé publique démasquée, le type de signature démasqué et le type de signature masqué.
- Peut indiquer, en option, les exigences de secret et/ou de clé privée pour les liens privés.
- Utilise le suffixe ".b32.i2p" existant, mais avec une longueur plus longue.
- Inclut une somme de contrôle pour la détection d’erreurs.
- Les adresses pour les leasesets chiffrés sont identifiées par 56 caractères codés ou plus (35 octets décodés ou plus), contre 52 caractères (32 octets) pour les adresses traditionnelles en base 32.

## Spécification

### Création et encodage

Construisez un nom d'hôte de {56+ caractères}.b32.i2p (35+ caractères en binaire) comme suit :

```
flag (1 byte)
  bit 0: 0 for one-byte sigtypes, 1 for two-byte sigtypes
  bit 1: 0 for no secret, 1 if secret is required
  bit 2: 0 for no per-client auth,
         1 if client private key is required
  bits 7-3: Unused, set to 0

public key sigtype (1 or 2 bytes as indicated in flags)
  If 1 byte, the upper byte is assumed zero

blinded key sigtype (1 or 2 bytes as indicated in flags)
  If 1 byte, the upper byte is assumed zero

public key
  Number of bytes as implied by sigtype
```
Post-traitement et somme de contrôle:

```
Construct the binary data as above.
Treat checksum as little-endian.
Calculate checksum = CRC-32(data[3:end])
data[0] ^= (byte) checksum
data[1] ^= (byte) (checksum >> 8)
data[2] ^= (byte) (checksum >> 16)

hostname = Base32.encode(data) || ".b32.i2p"
```
Tous les bits non utilisés à la fin du b32 (base32) doivent être à 0. Il n’y a pas de bits non utilisés pour une adresse standard de 56 caractères (35 octets).

### Décodage et vérification

```
strip the ".b32.i2p" from the hostname
data = Base32.decode(hostname)
Calculate checksum = CRC-32(data[3:end])
Treat checksum as little-endian.
flags = data[0] ^ (byte) checksum
if 1 byte sigtypes:
  pubkey sigtype = data[1] ^ (byte) (checksum >> 8)
  blinded sigtype = data[2] ^ (byte) (checksum >> 16)
else (2 byte sigtypes):
  pubkey sigtype = data[1] ^ ((byte) (checksum >> 8)) || data[2] ^ ((byte) (checksum >> 16))
  blinded sigtype = data[3] || data[4]
parse the remainder based on the flags to get the public key
```
### Bits des clés secrètes et privées

Les indicateurs de clé secrète et de clé privée sont utilisés pour signaler aux clients, aux proxies ou à tout autre code côté client que la clé secrète et/ou la clé privée seront nécessaires pour déchiffrer le leaseSet (ensemble de baux). Certaines implémentations peuvent demander à l’utilisateur de fournir les données requises, ou rejeter les tentatives de connexion si les données requises sont absentes.

Ces bits ne servent que d'indicateurs. La clé secrète ou privée ne doit jamais être incluse dans l'adresse B32 elle-même, car cela compromettrait la sécurité.

## Détails cryptographiques

### Schéma d’aveuglement

Le schéma d’aveuglement utilise RedDSA, basé sur Ed25519 et sur la conception de ZCash, pour produire des signatures Red25519 sur la courbe Ed25519 en utilisant SHA-512. Cette approche garantit que les clés publiques aveuglées restent dans le sous-groupe d’ordre premier, évitant ainsi les problèmes de sécurité présents dans certaines conceptions alternatives.

Les clés aveuglées sont renouvelées quotidiennement en fonction de la date UTC à l'aide de la formule :

```
blinded_key = BLIND(unblinded_key, date, optional_secret)
```
L’emplacement de stockage de la table de hachage distribuée (DHT) est calculé comme suit :

```
SHA256(type_byte || blinded_public_key)
```
### Chiffrement

Le leaseset (ensemble de baux) chiffré utilise l’algorithme de chiffrement en flux ChaCha20, choisi pour ses performances supérieures sur les appareils dépourvus d’accélération matérielle AES. La spécification emploie HKDF pour la dérivation de clés et X25519 pour les opérations Diffie-Hellman.

Les leaseSet chiffrés ont une structure en trois couches : - Couche externe : métadonnées en clair - Couche intermédiaire : authentification du client (méthodes DH ou PSK) - Couche interne : données LS2 proprement dites contenant les informations de lease (période et paramètres d'un tunnel)

### Méthodes d'authentification

L'authentification par client prend en charge deux méthodes :

**Authentification DH**: Utilise l'accord de clés X25519. Chaque client autorisé fournit sa clé publique au serveur, et le serveur chiffre la couche intermédiaire à l'aide d'un secret partagé dérivé d'ECDH.

**Authentification PSK**: Utilise directement des clés pré-partagées pour le chiffrement.

Le bit de drapeau 2 de l’adresse B32 indique si une authentification par client est requise.

## Mise en cache

Bien que cela soit hors du champ de cette spécification, les routers et les clients doivent mémoriser et mettre en cache (de préférence de manière persistante) la correspondance entre la clé publique et la destination, et inversement.

Le service de nommage blockfile (fichier en blocs), système de carnet d’adresses par défaut d’I2P depuis la version 0.9.8, gère plusieurs carnets d’adresses avec un mappage de recherche inversée dédié, permettant des recherches rapides par hachage. Cette fonctionnalité est essentielle pour la résolution de leaseSet chiffré lorsqu’au départ seul un hachage est connu.

## Types de signature

À partir de la version 2.10.0 d'I2P, les types de signature de 0 à 11 sont définis. L'encodage sur un octet reste la norme, tandis que l'encodage sur deux octets est disponible mais n'est pas utilisé en pratique.

**Types couramment utilisés:** - Type 0 (DSA_SHA1): Déprécié pour les router, pris en charge pour les destinations - Type 7 (EdDSA_SHA512_Ed25519): Norme actuelle pour les identités de router et les destinations - Type 11 (RedDSA_SHA512_Ed25519): Exclusivement pour les LS2 leasesets chiffrés avec prise en charge du blinding (aveuglement)

**Remarque importante** : Seuls Ed25519 (type 7) et Red25519 (type 11) prennent en charge le blindage (aveuglement cryptographique) nécessaire aux leasesets chiffrés. Les autres types de signature ne peuvent pas être utilisés avec cette fonctionnalité.

Les types 9-10 (algorithmes GOST) restent réservés mais non implémentés. Les types 4-6 et 8 sont marqués "offline only" pour les clés de signature hors ligne.

## Remarques

- Distinguer les anciennes des nouvelles variantes par la longueur. Les anciennes adresses b32 sont toujours {52 caractères}.b32.i2p. Les nouvelles sont {56+ caractères}.b32.i2p
- L’encodage base32 suit la norme RFC 4648, avec un décodage insensible à la casse et une sortie en minuscules privilégiée
- Les adresses peuvent dépasser 200 caractères lorsqu’on utilise des types de signature avec des clés publiques plus grandes (par exemple, ECDSA P521 avec des clés de 132 octets)
- Le nouveau format peut être utilisé dans des liens de saut (et servi par des serveurs de saut) si souhaité, tout comme le b32 standard
- Les clés aveuglées sont renouvelées quotidiennement en fonction de la date UTC afin d’améliorer la confidentialité
- Ce format s’écarte de l’approche de l’annexe A.2 de rend-spec-v3.txt de Tor, qui présente des implications potentielles en matière de sécurité avec des clés publiques aveuglées hors courbe

## Compatibilité des versions

Cette spécification est valide pour I2P de la version 0.9.47 (août 2020) à la version 2.10.0 (septembre 2025). Aucun changement rétro-incompatible n’a affecté le format d’adressage B32, la structure LS2 (LeaseSet, version 2) chiffrée, ni les implémentations cryptographiques durant cette période. Toutes les adresses créées avec la 0.9.47 restent entièrement compatibles avec les versions actuelles.

## Références

**CRC-32** - [CRC-32 (Wikipédia)](https://en.wikipedia.org/wiki/CRC-32) - [RFC 3309 : Somme de contrôle du Stream Control Transmission Protocol (protocole de transport gérant des flux)](https://tools.ietf.org/html/rfc3309)

**Spécifications I2P** - [Spécification du LeaseSet chiffré](/docs/specs/encryptedleaseset/) - [Proposition 123 : Nouvelles entrées du netDB](/proposals/123-new-netdb-entries/) - [Proposition 149 : B32 pour LS2 chiffré](/proposals/149-b32-encrypted-ls2/) - [Spécification des structures communes](/docs/specs/common-structures/) - [Nommage et carnet d’adresses](/docs/overview/naming/)

**Comparaison avec Tor** - [Fil de discussion Tor (contexte de conception)](https://lists.torproject.org/pipermail/tor-dev/2017-January/011816.html)

**Ressources supplémentaires** - [Projet I2P](/) - [Forum I2P](https://i2pforum.net) - [Documentation de l'API Java](http://docs.i2p-projekt.de/javadoc/)
