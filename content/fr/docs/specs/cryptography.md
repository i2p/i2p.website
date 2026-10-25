---
title: "Spécification Cryptographique de Bas Niveau"
description: "Détails de bas niveau des algorithmes cryptographiques utilisés dans I2P"
slug: "cryptography"
aliases:
  - "/fr/how_cryptography"
  - "/fr/how_cryptography/"
category: "Conception"
lastUpdated: "2025-05"
accurateFor: "0.9.66"
---

## Aperçu

> **Note :** Ce document est largement obsolète. Consultez les documents suivants pour les spécifications actuelles : > - [ECIES](/docs/specs/ecies) > - [Encrypted LeaseSet](/docs/specs/encryptedleaseset) > - [NTCP2](/docs/specs/ntcp2) > - [Red25519](/docs/specs/red25519) > - [SSU2](/docs/specs/ssu2) > - [Tunnel Creation (ECIES)](/docs/specs/tunnel-creation-ecies)

Cette page spécifie les détails de bas niveau de la cryptographie dans I2P.

Il existe plusieurs algorithmes cryptographiques utilisés dans I2P. Dans la conception originale d'I2P, il n'y en avait qu'un seul de chaque type - un algorithme symétrique, un algorithme asymétrique, un algorithme de signature et un algorithme de hachage. Il n'y avait aucune disposition pour ajouter d'autres algorithmes ou migrer vers des algorithmes offrant plus de sécurité.

Ces dernières années, nous avons ajouté un framework pour prendre en charge plusieurs primitives et combinaisons de manière rétro-compatible. De nombreux algorithmes de signature, avec des longueurs de clés et de signatures variables, sont définis par des "types de signature". Les schémas de chiffrement de bout en bout, utilisant une combinaison de chiffrement asymétrique et symétrique, et avec des longueurs de clés variables, sont définis par des "types de chiffrement".

Divers protocoles et structures de données dans I2P incluent des champs pour spécifier le type de signature et/ou le type de chiffrement. Ces champs, ainsi que les définitions de types, définissent les longueurs de clés et de signatures et les primitives cryptographiques requises pour les utiliser. Les définitions des types de signature et de chiffrement se trouvent dans la [spécification des Structures Communes](/docs/specs/common-structures).

Les protocoles I2P originaux NTCP, SSU et ElGamal/AES+SessionTags utilisent une combinaison de chiffrement asymétrique ElGamal et de chiffrement symétrique AES. Les protocoles plus récents NTCP2 et ECIES-X25519-AEAD-Ratchet utilisent une combinaison d'échange de clés X25519 et de chiffrement symétrique ChaCha20/Poly1305.

- ECIES-X25519-AEAD-Ratchet a remplacé ElGamal/AES+SessionTags.
- NTCP2 a remplacé NTCP.
- SSU2 a remplacé SSU.
- La création de tunnel X25519 a remplacé la création de tunnel ElGamal.

## Chiffrement asymétrique

L'algorithme de chiffrement asymétrique original dans I2P est ElGamal. Le nouvel algorithme, utilisé à plusieurs endroits, est l'échange de clés ECIES X25519 DH.

Nous sommes en train de migrer toute l'utilisation d'ElGamal vers X25519.

NTCP (avec ElGamal) a été migré vers NTCP2 (avec X25519). ElGamal/AES+SessionTag est en cours de migration vers ECIES-X25519-AEAD-Ratchet.

### X25519

Pour les détails sur l'utilisation de X25519, voir [NTCP2](/docs/specs/ntcp2) et [ECIES](/docs/specs/ecies).

### ElGamal

ElGamal est utilisé à plusieurs endroits dans I2P :

- Pour chiffrer les messages TunnelBuild de router à router
- Pour le chiffrement de bout en bout (destination à destination) dans le cadre d'ElGamal/AES+SessionTag en utilisant la clé de chiffrement du leaseSet
- Pour le chiffrement de certains stockages et requêtes netDb envoyés aux routers floodfill dans le cadre d'ElGamal/AES+SessionTag (destination vers router ou router vers router).

Nous utilisons des nombres premiers communs pour le chiffrement et déchiffrement ElGamal 2048, tels que définis par l'IETF [RFC-3526](http://tools.ietf.org/html/rfc3526). Nous utilisons actuellement ElGamal uniquement pour chiffrer l'IV et la clé de session dans un seul bloc, suivi de la charge utile chiffrée AES utilisant cette clé et cet IV.

L'ElGamal non chiffré contient :

```
+----+----+----+----+----+----+----+----+
|nonz|           H(data)                |
+----+                                  +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+----+----+----+
|    |  data...
+----+----+----+-//
```
Le H(data) est le SHA256 des données qui sont chiffrées dans le bloc ElGamal, et est précédé d'un octet aléatoire non nul. Cet octet est effectivement aléatoire depuis la version 0.9.28 ; avant cela, il était toujours 0xFF. Il pourrait éventuellement être utilisé pour des drapeaux à l'avenir. Les données chiffrées dans le bloc peuvent avoir une longueur maximale de 222 octets. Comme les données chiffrées peuvent contenir un nombre substantiel de zéros si le texte en clair est plus petit que 222 octets, il est recommandé que les couches supérieures complètent le texte en clair à 222 octets avec des données aléatoires. Longueur totale : typiquement 255 octets.

Le ElGamal chiffré contient :

```
+----+----+----+----+----+----+----+----+
|  zero padding...       |              |
+----+----+----+-//-+----+              +
|                                       |
+                                       +
|       ElG encrypted part 1            |
~                                       ~
|                                       |
+    +----+----+----+----+----+----+----+
|    |   zero padding...      |         |
+----+----+----+----+-//-+----+         +
|                                       |
+                                       +
|       ElG encrypted part 2            |
~                                       ~
|                                       |
+         +----+----+----+----+----+----+
|         +
+----+----+
```
Chaque partie chiffrée est préfixée avec des zéros pour atteindre une taille de exactement 257 octets. Longueur totale : 514 octets. Dans l'usage typique, les couches supérieures complètent les données en clair à 222 octets, résultant en un bloc non chiffré de 255 octets. Ceci est encodé en deux parties chiffrées de 256 octets, et il y a un seul octet de bourrage zéro avant chaque partie à cette couche.

Voir le code ElGamal [ElGamalEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/ElGamalEngine.java).

Le nombre premier partagé est le nombre premier Oakley pour les clés de 2048 bits [RFC-3526-S3](http://tools.ietf.org/html/rfc3526#section-3) :

```
2^2048 - 2^1984 - 1 + 2^64 * { [2^1918 pi] + 124476 }
```
ou comme une valeur hexadécimale :

```
FFFFFFFF FFFFFFFF C90FDAA2 2168C234 C4C6628B 80DC1CD1
29024E08 8A67CC74 020BBEA6 3B139B22 514A0879 8E3404DD
EF9519B3 CD3A431B 302B0A6D F25F1437 4FE1356D 6D51C245
E485B576 625E7EC6 F44C42E9 A637ED6B 0BFF5CB6 F406B7ED
EE386BFB 5A899FA5 AE9F2411 7C4B1FE6 49286651 ECE45B3D
C2007CB8 A163BF05 98DA4836 1C55D39A 69163FA8 FD24CF5F
83655D23 DCA3AD96 1C62F356 208552BB 9ED52907 7096966D
670C354E 4ABC9804 F1746C08 CA18217C 32905E46 2E36CE3B
E39E772C 180E8603 9B2783A2 EC07A28F B5C55DF0 6F4C52C9
DE2BCBF6 95581718 3995497C EA956AE5 15D22618 98FA0510
15728E5A 8AACAA68 FFFFFFFF FFFFFFFF
```
Utilisation de 2 comme générateur.

#### Exposant court {#exponent}

Bien que la taille d'exposant standard soit de 2048 bits (256 octets) et que la PrivateKey I2P fasse 256 octets complets, dans certains cas nous utilisons la taille d'exposant courte de 226 bits (28,25 octets). Cela devrait être sûr pour une utilisation avec les nombres premiers Oakley [vanOorschot1996] [BENCHMARKS].

De plus, [Koshiba2004] semble apparemment soutenir cela, selon ce fil sci.crypt [SCI.CRYPT]. Le reste de la PrivateKey est complété avec des zéros.

Avant la version 0.9.8, tous les routers utilisaient l'exposant court. Depuis la version 0.9.8, les routers x86 64 bits utilisent un exposant complet de 2048 bits. Tous les routers utilisent maintenant l'exposant complet, à l'exception d'un petit nombre de routers sur du matériel très lent, qui continuent d'utiliser l'exposant court en raison de préoccupations concernant la charge processeur. La transition vers un exposant plus long pour ces plateformes est un sujet d'étude approfondie.

#### Obsolescence

La vulnérabilité du réseau à une attaque ElGamal et l'impact de la transition vers une longueur de bits plus importante doivent être étudiés. Il pourrait être très difficile de rendre tout changement rétrocompatible.

## Chiffrement symétrique

L'algorithme de chiffrement symétrique original dans I2P est AES. Le nouvel algorithme, utilisé à plusieurs endroits, est l'Authenticated Encryption with Associated Data (AEAD) ChaCha20/Poly1305.

Nous sommes en cours de migration de toute utilisation d'AES vers ChaCha20/Poly1305.

NTCP (avec AES) a été migré vers NTCP2 (avec ChaCha20/Poly1305). ElGamal/AES+SessionTag est en cours de migration vers ECIES-X25519-AEAD-Ratchet.

### ChaCha20/Poly1305

Pour les détails sur l'utilisation de ChaCha20/Poly1305, voir [NTCP2](/docs/specs/ntcp2) et [ECIES](/docs/specs/ecies).

### AES

AES est utilisé pour le chiffrement symétrique, dans plusieurs cas :

- Pour le chiffrement du transport SSU (voir section "Transports") après l'échange de clés DH
- Pour le chiffrement de bout en bout (destination à destination) dans le cadre d'ElGamal/AES+SessionTag
- Pour le chiffrement de certains stockages et requêtes netDb envoyés aux routeurs floodfill dans le cadre d'ElGamal/AES+SessionTag (destination vers routeur ou routeur vers routeur).
- Pour le chiffrement des messages de test périodiques des tunnels envoyés du routeur vers lui-même, à travers ses propres tunnels.

Nous utilisons AES avec des clés de 256 bits et des blocs de 128 bits en mode CBC. Le remplissage utilisé est spécifié dans l'IETF [RFC-2313](http://tools.ietf.org/html/rfc2313) (PKCS#5 1.5, section 8.1 (pour le type de bloc 02)). Dans ce cas, le remplissage consiste en octets générés de manière pseudo-aléatoire pour correspondre aux blocs de 16 octets. Spécifiquement, voir le code CBC [CryptixAESEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/CryptixAESEngine.java) et l'implémentation AES Cryptix [CryptixRijndael_Algorithm](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/CryptixRijndael_Algorithm.java), ainsi que le remplissage, trouvé dans la fonction ElGamalAESEngine.getPadding [ElGamalAESEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/ElGamalAESEngine.java).

#### Obsolescence

La vulnérabilité du réseau à une attaque AES et l'impact de la transition vers une longueur de bits plus importante doivent être étudiés. Il pourrait être assez difficile de rendre tout changement rétrocompatible.

## Signatures {#sig}

De nombreux algorithmes de signature, avec des longueurs de clés et de signatures variables, sont définis par les types de signature. Il est relativement facile d'ajouter d'autres types de signature.

EdDSA-SHA512-Ed25519 est l'algorithme de signature par défaut actuel. DSA, qui était l'algorithme original avant que nous ajoutions le support des types de signature, est toujours utilisé dans le réseau.

### DSA

Les signatures sont générées et vérifiées avec [DSA](http://en.wikipedia.org/wiki/Digital_Signature_Algorithm) 1024 bits (L=1024, N=160), tel qu'implémenté dans [DSAEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/DSAEngine.java). DSA a été choisi car il est beaucoup plus rapide pour les signatures qu'ElGamal.

#### SEED

160 bit :

```
86108236b8526e296e923a4015b4282845b572cc
```
#### Compteur

```
33
```
#### Premier DSA (p)

1024 bit :

```
9C05B2AA 960D9B97 B8931963 C9CC9E8C 3026E9B8 ED92FAD0
A69CC886 D5BF8015 FCADAE31 A0AD18FA B3F01B00 A358DE23
7655C496 4AFAA2B3 37E96AD3 16B9FB1C C564B5AE C5B69A9F
F6C3E454 8707FEF8 503D91DD 8602E867 E6D35D22 35C1869C
E2479C3B 9D5401DE 04E0727F B33D6511 285D4CF2 9538D9E3
B6051F5B 22CC1C93
```
#### Quotient DSA (q)

```
A5DFC28F EF4CA1E2 86744CD8 EED9D29D 684046B7
```
#### Générateur DSA (g)

1024 bit :

```
0C1F4D27 D40093B4 29E962D7 223824E0 BBC47E7C 832A3923
6FC683AF 84889581 075FF908 2ED32353 D4374D73 01CDA1D2
3C431F46 98599DDA 02451824 FF369752 593647CC 3DDC197D
E985E43D 136CDCFC 6BD5409C D2F45082 1142A5E6 F8EB1C3A
B5D0484B 8129FCF1 7BCE4F7F 33321C3C B3DBB14A 905E7B2B
3E93BE47 08CBCC82
```
La SigningPublicKey fait 1024 bits. La SigningPrivateKey fait 160 bits.

#### Obsolescence

[NIST-800-57](http://csrc.nist.gov/publications/nistpubs/800-57/sp800-57-Part1-revised2_Mar08-2007.pdf) recommande un minimum de (L=2048, N=224) pour un usage au-delà de 2010. Ceci peut être quelque peu atténué par la "cryptopériode", ou durée de vie d'une clé donnée.

Le nombre premier a été choisi en 2003, et la personne qui a choisi ce nombre (TheCrypto) n'est actuellement plus un développeur I2P. Par conséquent, nous ne savons pas si le nombre premier choisi est un 'nombre premier fort'. Si un nombre premier plus grand est choisi à des fins futures, celui-ci devrait être un nombre premier fort, et nous documenterons le processus de construction.

## Nouveaux algorithmes de signature

À partir de la version 0.9.12, le router prend en charge des algorithmes de signature supplémentaires qui sont plus sécurisés que le DSA 1024 bits. La première utilisation concernait les Destinations ; la prise en charge des Router Identities a été ajoutée dans la version 0.9.16. Les Destinations existantes ne peuvent pas être migrées des anciennes signatures vers les nouvelles ; cependant, il existe une prise en charge d'un tunnel unique avec plusieurs Destinations, ce qui fournit un moyen de passer à des types de signature plus récents. Le type de signature est encodé dans la Destination et la Router Identity, de sorte que de nouveaux algorithmes de signature ou courbes peuvent être ajoutés à tout moment.

Les types de signature actuellement pris en charge sont les suivants :

- DSA-SHA1
- ECDSA-SHA256-P256
- ECDSA-SHA384-P384 (pas largement utilisé)
- ECDSA-SHA512-P521 (pas largement utilisé)
- EdDSA-SHA512-Ed25519 (par défaut depuis la version 0.9.15)
- RedDSA-SHA512-Ed25519 (depuis la version 0.9.39)

Des types de signature supplémentaires sont utilisés uniquement au niveau de la couche application, principalement pour signer et vérifier les fichiers su3. Ces types de signature sont les suivants :

- RSA-SHA256-2048 (peu utilisé)
- RSA-SHA384-3072 (peu utilisé)
- RSA-SHA512-4096
- EdDSA-SHA512-Ed25519ph (depuis la version 0.9.25 ; peu utilisé)

### ECDSA

ECDSA utilise les courbes NIST standard et les hachages SHA-2 standard.

Nous avons migré les nouvelles destinations vers ECDSA-SHA256-P256 dans la période des versions 0.9.16 - 0.9.19. L'utilisation pour les Router Identities est prise en charge depuis la version 0.9.16 et la migration des routers existants a eu lieu en 2015.

### RSA

RSA PKCS#1 v1.5 standard (RFC 2313) avec l'exposant public F4 = 65537.

RSA est maintenant utilisé pour signer tout le contenu de confiance hors-bande, y compris les mises à jour du router, le reseeding, les plugins et les actualités. Les signatures sont intégrées dans le format "su3" [UPDATES]. Les clés de 4096 bits sont recommandées et utilisées par tous les signataires connus. RSA n'est pas utilisé, ni prévu pour utilisation, dans les Destinations ou Identités de Router du réseau.

### EdDSA 25519

EdDSA standard utilisant la courbe 25519 et les hachages SHA-2 standard de 512 bits.

Pris en charge depuis la version 0.9.15.

Les Destinations et les Router Identities ont été migrées fin 2015.

### RedDSA 25519

EdDSA standard utilisant la courbe 25519 et les hachages SHA-2 standard de 512 bits, mais avec des clés privées différentes et des modifications mineures pour la signature. Pour les leaseSets chiffrés. Voir [EncryptedLeaseSet](/docs/specs/encryptedleaseset) et [Red25519](/docs/specs/red25519) pour plus de détails.

Pris en charge à partir de la version 0.9.39.

## Hachages

Les hachages sont utilisés dans les algorithmes de signature et comme clés dans la DHT du réseau.

Les anciens algorithmes de signature utilisent SHA1 et SHA256. Les nouveaux algorithmes de signature utilisent SHA512. La DHT utilise SHA256.

### SHA256

Les hachages DHT dans I2P utilisent le standard SHA256.

#### Obsolescence

La vulnérabilité du réseau face à une attaque SHA-256 et l'impact de la transition vers un hash plus long doivent être étudiés. Il pourrait être assez difficile de rendre tout changement rétrocompatible.

## Transports

Au niveau le plus bas de la couche protocole, la communication point-à-point entre routeurs est protégée par la sécurité de la couche transport.

Les connexions NTCP2 utilisent X25519 Diffie-Hellman et le chiffrement authentifié ChaCha20/Poly1305.

Les transports SSU et NTCP obsolète utilisent un échange de clés Diffie-Hellman de 256 octets (2048 bits) en utilisant le même nombre premier partagé et générateur que spécifié ci-dessus pour ElGamal, suivi d'un chiffrement symétrique AES comme décrit ci-dessus.

SSU est prévu pour être migré vers SSU2 (avec X25519 et ChaCha20/Poly1305).

Tous les transports fournissent une confidentialité persistante [PFS](http://en.wikipedia.org/wiki/Perfect_forward_secrecy) sur les liens de transport.

### Connexions NTCP2 {#tcp}

Les connexions NTCP2 utilisent X25519 Diffie-Hellman et le chiffrement authentifié ChaCha20/Poly1305, ainsi que le framework de protocole Noise [Noise](https://noiseprotocol.org/noise.html).

Voir la spécification NTCP2 [NTCP2](/docs/specs/ntcp2) pour les détails et références.

### Connexions UDP {#udp}

SSU (le transport UDP) chiffre chaque paquet avec AES256/CBC avec à la fois un IV explicite et un MAC (HMAC-MD5-128) après avoir convenu d'une clé de session éphémère via un échange Diffie-Hellman 2048 bits, une authentification station-à-station avec la clé DSA de l'autre router, et chaque message réseau a son propre hash pour la vérification d'intégrité locale.

Voir la spécification SSU pour plus de détails.

AVERTISSEMENT - Le HMAC-MD5-128 d'I2P utilisé dans SSU est apparemment non-standard. Apparemment, une version précoce de SSU utilisait HMAC-SHA256, puis il a été remplacé par MD5-128 pour des raisons de performance, mais la taille de buffer de 32 octets a été laissée intacte. Voir HMACGenerator.java et les notes de statut du 2005-07-05 pour plus de détails.

### Connexions NTCP

NTCP n'est plus utilisé, il a été remplacé par NTCP2.

Les connexions NTCP étaient négociées avec une implémentation Diffie-Hellman 2048, utilisant l'identité du router pour procéder à un accord station à station, suivi de certains champs spécifiques au protocole chiffrés, avec toutes les données suivantes chiffrées avec AES (comme ci-dessus). La raison principale de faire la négociation DH au lieu d'utiliser ElGamalAES+SessionTag est qu'elle fournit la 'confidentialité persistante (parfaite)' [PFS](http://en.wikipedia.org/wiki/Perfect_forward_secrecy), alors qu'ElGamalAES+SessionTag ne le fait pas.

## Références

- [BENCHMARKS](https://web.archive.org/web/20080423000000*/http://www.eskimo.com/~weidai/benchmarks.html) - Benchmarks Crypto++, originalement sur http://www.eskimo.com/~weidai/benchmarks.html (maintenant mort), récupéré depuis http://www.archive.org/, daté du 23 avril 2008.
- [Common](/docs/specs/common-structures) - Spécification des Structures Communes
- [CryptixAESEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/CryptixAESEngine.java)
- [CryptixRijndael_Algorithm](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/CryptixRijndael_Algorithm.java)
- [DSA](http://en.wikipedia.org/wiki/Digital_Signature_Algorithm)
- [DSAEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/DSAEngine.java)
- [ECIES](/docs/specs/ecies)
- [ElGamalAESEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/ElGamalAESEngine.java)
- [ElGamalEngine](https://github.com/i2p/i2p.i2p/tree/master/core/java/src/net/i2p/crypto/ElGamalEngine.java)
- [EncryptedLeaseSet](/docs/specs/encryptedleaseset)
- [Koshiba2004](http://www.springerlink.com/content/2jry7cftp5bpdghm/) - Koshiba & Kurosawa. Short Exponent Diffie-Hellman Problems. PKC 2004, LNCS 2947, pp. 173-186
- [NIST-800-57](http://csrc.nist.gov/publications/nistpubs/800-57/sp800-57-Part1-revised2_Mar08-2007.pdf)
- [Noise](https://noiseprotocol.org/noise.html)
- [NTCP2](/docs/specs/ntcp2)
- [PFS](http://en.wikipedia.org/wiki/Perfect_forward_secrecy)
- [Red25519](/docs/specs/red25519)
- [RFC-2313](http://tools.ietf.org/html/rfc2313)
- [RFC-3526](http://tools.ietf.org/html/rfc3526)
- [RFC-3526-S3](http://tools.ietf.org/html/rfc3526#section-3)
- [SCI.CRYPT](https://groups.google.com/forum/#!topic/sci.crypt/GFWl76dBZnc)
- [SHA-2](https://en.wikipedia.org/wiki/SHA-2)
- [SSU2](/docs/specs/ssu2)
- [UPDATES](/docs/specs/updates)
- [vanOorschot1996](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.14.5952&rep=rep1&type=pdf) - van Oorschot, Weiner. On Diffie-Hellman Key Agreement with Short Exponents. EuroCrypt '96
