---
title: "PQ Hybrid SSU2"
description: "Variante hybride post-quantique du protocole de transport SSU2 utilisant ML-KEM"
slug: "ssu2-hybrid"
lastupdated: "2026-10"
category: "Transports"
accurateFor: "0.9.71"
---

### Statut

Bêta T2 2026, sortie T3 2026

## Vue d'ensemble

Il s'agit de la variante hybride post-quantique du protocole de transport SSU2, telle que conçue dans la Proposition 169. Consultez cette proposition pour plus d'informations contextuelles.

PQ Hybrid SSU2 est uniquement défini sur la même adresse et le même port que SSU2 standard. Le fonctionnement sur un port différent, ou sans prise en charge de SSU2 standard, n'est pas autorisé, et ne le sera pas avant plusieurs années, lorsque SSU2 standard sera déprécié.

Cette spécification documente uniquement les modifications requises par rapport au standard SSU2 pour prendre en charge le PQ Hybrid. Consultez la spécification SSU2 pour les détails de l'implémentation de base.

## Conception

Nous prenons en charge les normes NIST FIPS 203 et 204 [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) [FIPS 204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf) qui sont basées sur CRYSTALS-Kyber et CRYSTALS-Dilithium (versions 3.1, 3 et antérieures), mais NON compatibles avec ces derniers.

### Échange de clés

PQ KEM ne fournit que des clés éphémères et ne prend pas en charge directement les échanges à clés statiques tels que Noise XK et IK. Les types de chiffrement sont les mêmes que ceux utilisés dans PQ Hybrid Ratchet et sont définis dans le document des structures communes [/docs/specs/common-structures/](/docs/specs/common-structures/). Comme dans [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf), les types hybrides ne sont définis qu'en combinaison avec X25519.

Les types de chiffrement sont :

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">SSU2 Version</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
</tr>
</table>
### Combinaisons légales

Les nouveaux types de chiffrement sont indiqués dans les RouterAddresses. Le type de chiffrement dans le certificat de clé continuera d'être le type 4.

## Spécification

### Modèles de handshake

Les poignées de main utilisent les modèles de poignées de main du [Protocole Noise](https://noiseprotocol.org/noise.html).

Le mappage de lettres suivant est utilisé :

- e = clé éphémère à usage unique
- s = clé statique
- p = charge utile du message
- e1 = clé PQ éphémère à usage unique, envoyée d'Alice à Bob
- ekem1 = le texte chiffré KEM, envoyé de Bob à Alice

Les modifications suivantes de XK et IK pour la confidentialité persistante hybride (hfs) sont telles que spécifiées dans la section 5 de la [spécification Noise HFS](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) :

```
XK:                       XKhfs:
  <- s                      <- s
  ...                       ...
  -> e, es, p               -> e, es, e1, p
  <- e, ee, p               <- e, ee, ekem1, p
  -> s, se                  -> s, se
  <- p                      <- p
  p ->                      p ->


  e1 and ekem1 are encrypted. See pattern definitions below.
  NOTE: e1 and ekem1 are different sizes (unlike X25519)
```
Le motif e1 est défini comme suit, tel que spécifié dans la section 4 de la [spécification Noise HFS](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) :

```
For Alice:
  (encap_key, decap_key) = PQ_KEYGEN()

  // EncryptAndHash(encap_key)
  ciphertext = ENCRYPT(k, n, encap_key, ad)
  n++
  MixHash(ciphertext)

  For Bob:

  // DecryptAndHash(ciphertext)
  encap_key = DECRYPT(k, n, ciphertext, ad)
  n++
  MixHash(ciphertext)
```
Le pattern ekem1 est défini comme suit, tel que spécifié dans la section 4 de la [spécification Noise HFS](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) :

```
For Bob:

  (kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

  // EncryptAndHash(kem_ciphertext)
  ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)
  MixHash(ciphertext)

  // MixKey
  MixKey(kem_shared_key)


  For Alice:

  // DecryptAndHash(ciphertext)
  kem_ciphertext = DECRYPT(k, n, ciphertext, ad)
  MixHash(ciphertext)

  // MixKey
  kem_shared_key = DECAPS(kem_ciphertext, decap_key)
  MixKey(kem_shared_key)
```
### KDF de l'échange Noise

#### Vue d'ensemble

La poignée de main hybride est définie dans la [spécification Noise HFS](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf). Le premier message, d'Alice vers Bob, contient e1, la clé d'encapsulation, avant la charge utile du message. Celle-ci est traitée comme une clé statique supplémentaire ; appelez `EncryptAndHash()` (en tant qu'Alice) ou `DecryptAndHash()` (en tant que Bob). Traitez ensuite la charge utile du message normalement.

Le deuxième message, de Bob à Alice, contient ekem1, le texte chiffré, avant la charge utile du message. Celui-ci est traité comme une clé statique supplémentaire ; appelez EncryptAndHash() (en tant que Bob) ou DecryptAndHash() (en tant qu'Alice). Ensuite, calculez le kem_shared_key et appelez MixKey(kem_shared_key). Puis traitez la charge utile du message normalement.

#### Opérations ML-KEM définies

Nous définissons les fonctions suivantes correspondant aux blocs de construction cryptographiques utilisés tels que définis dans [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

(encap_key, decap_key) = PQ_KEYGEN()

    Alice creates the encapsulation and decapsulation keys
    The encapsulation key is sent in message 1.
    encap_key and decap_key sizes vary based on ML-KEM variant.

(ciphertext, kem_shared_key) = ENCAPS(encap_key)

    Bob calculates the ciphertext and shared key,
    using the ciphertext received in message 1.
    The ciphertext is sent in message 2.
    ciphertext size varies based on ML-KEM variant.
    The kem_shared_key is always 32 bytes.

kem_shared_key = DECAPS(ciphertext, decap_key)

    Alice calculates the shared key,
    using the ciphertext received in message 2.
    The kem_shared_key is always 32 bytes.

Notez que l'encap_key et le texte chiffré sont tous deux chiffrés à l'intérieur des blocs ChaCha/Poly dans les messages de handshake Noise 1 et 2. Ils seront déchiffrés dans le cadre du processus de handshake.

La kem_shared_key est intégrée à la clé de chaînage via MixHash(). Voir ci-dessous pour plus de détails.

#### KDF d'Alice pour le Message 1

Après le modèle de message 'es' et avant la charge utile, ajouter :

```
This is the "e1" message pattern:
  (encap_key, decap_key) = PQ_KEYGEN()

  // EncryptAndHash(encap_key)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, encap_key, ad)
  n++

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)


  End of "e1" message pattern.

  NOTE: For the next section (payload for XK or static key for IK),
  the keydata and chain key remain the same,
  and n now equals 1 (instead of 0 for non-hybrid).
```
#### KDF de Bob pour le Message 1

Après le modèle de message 'es' et avant la charge utile, ajouter :

```
This is the "e1" message pattern:

  // DecryptAndHash(encap_key_section)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  encap_key = DECRYPT(k, n, encap_key_section, ad)
  n++

  // MixHash(encap_key_section)
  h = SHA256(h || encap_key_section)

  End of "e1" message pattern.

  NOTE: For the next section (payload for XK or static key for IK),
  the keydata and chain key remain the same,
  and n now equals 1 (instead of 0 for non-hybrid).
```
#### KDF Bob pour le Message 2

Pour XK : Après le pattern de message 'ee' et avant le payload, ajouter :

```
This is the "ekem1" message pattern:

  (kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

  // EncryptAndHash(kem_ciphertext)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)

  // MixHash(ciphertext)
  h = SHA256(h || ciphertext)

  // MixKey(kem_shared_key)
  keydata = HKDF(chainKey, kem_shared_key, "", 64)
  chainKey = keydata[0:31]

  End of "ekem1" message pattern.

  // AEAD parameters for payload section
  ... as in standard SSU2 ...
  k = keydata[32:63]
  ...

```
#### KDF d'Alice pour le Message 2

Après le schéma de message 'ee', ajouter :

```
This is the "ekem1" message pattern:

  // DecryptAndHash(kem_ciphertext_section)
  // AEAD parameters
  k = keydata[32:63]
  n = 0
  ad = h
  kem_ciphertext = DECRYPT(k, n, kem_ciphertext_section, ad)

  // MixHash(kem_ciphertext_section)
  h = SHA256(h || kem_ciphertext_section)

  // MixKey(kem_shared_key)
  kem_shared_key = DECAPS(kem_ciphertext, decap_key)
  keydata = HKDF(chainKey, kem_shared_key, "", 64)
  chainKey = keydata[0:31]

  End of "ekem1" message pattern.

  // AEAD parameters for payload section
  ... as in standard SSU2 ...
  k = keydata[32:63]
  ...

```
#### KDF pour le Message 3

unchanged

#### KDF pour split()

unchanged

### Détails de la négociation

#### Identifiants Noise

- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_XKhfschaobfse+hs1+hs2+hs3_25519+MLKEM768_ChaChaPoly_SHA256"

Notez que MLKEM-1024 n'est PAS pris en charge pour SSU2, car les clés sont trop volumineuses pour tenir dans un datagramme standard de 1500 octets.

#### En-tête long

Le long en-tête fait 32 octets. Il est utilisé avant qu'une session soit créée, pour les messages Token Request, SessionRequest, SessionCreated et Retry. Il est également utilisé pour les messages Peer Test et Hole Punch hors session.

Dans les messages suivants, définissez le champ ver (version) dans l'en-tête long à 3 ou 4, pour indiquer MLKEM-512 ou MLKEM-768.

- (0) Demande de session
- (1) Session créée
- (9) Nouvelle tentative
- (10) Demande de jeton
- (11) Hole Punch

Dans les messages suivants, définissez le champ ver (version) dans l'en-tête long à 2, comme d'habitude, même si MLKEM-512 ou MLKEM-768 est pris en charge. Les implémentations peuvent également définir la valeur à 3 ou 4, si l'autre extrémité le prend en charge, mais ce n'est pas nécessaire. Les implémentations doivent accepter toute valeur comprise entre 2 et 4.

- (7) Test de pair (messages hors session 5-7)

Discussion : Définir le champ de version à 3 ou 4 n'est pas forcément indispensable pour tous les types de messages, mais cela facilite la détection précoce des échecs pour les connexions post-quantiques non prises en charge. Les messages Token Request et Retry (types 9 et 10) devraient utiliser les versions 3/4 par souci de cohérence. Les messages Hole Punch (type 11) ne nécessitent peut-être pas ce traitement, mais nous suivrons le même schéma par uniformité. Les messages Peer Test (type 7) sont hors session et n'indiquent pas l'intention d'initier une session.

- Relay Request
- Relay Response
- Relay Intro
- Peer Test

Avant le chiffrement de l'en-tête :

Avant le chiffrement de l'en-tête :

```

  +----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+

  Destination Connection ID :: 8 bytes, unsigned big endian integer

  Packet Number :: 4 bytes, unsigned big endian integer

  type :: The message type = 0, 1, 7, 9, 10, or 11

  ver :: The protocol version = 2, 3, or 4 for non-PQ, MLKEM512, MLKEM768

  id :: 1 byte, the network ID (currently 2, except for test networks)

  flag :: 1 byte, unused, set to 0 for future compatibility

  Source Connection ID :: 8 bytes, unsigned big endian integer

  Token :: 8 bytes, unsigned big endian integer

```
#### En-tête court

unchanged

#### SessionRequest (Type 0)

Modifications : Le SSU2 actuel ne contient que les données de bloc dans la section ChaCha. Avec ML-KEM, la section ChaCha contiendra également la clé publique PQ chiffrée.

Modification du KDF pour la protection contre l'usurpation d'identité : Pour résoudre les problèmes soulevés dans la Proposition 165 [Prop165]_, mais avec une solution différente, nous modifions le KDF pour la Session Request. Cela s'applique uniquement aux sessions PQ. Le KDF pour les sessions non-PQ reste inchangé.

```

// End of KDF for initial chain key (unchanged)
  // Bob static key
  // MixHash(bpk)
  h = SHA256(h || bpk);

  // Start of KDF for session request
  // NEW for PQ only
  // bhash = Bob router hash (32 bytes)
  // MixHash(bhash)
  h = SHA256(h || bhash);

  // Rest of KDF for session request, unchanged, as in SSU2 spec
  // MixHash(header)
  h = SHA256(h || header)

  ...

```
Contenu brut :

```
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 0-15, ChaCha20     |
  +  encrypted with Bob intro key         +
  |    See Header Encryption KDF          |
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 16-31, ChaCha20    |
  +  encrypted with Bob intro key n=0     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +       X, ChaCha20 encrypted           +
  |       with Bob intro key n=0          |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (MLKEM)     |
  +          (length varies)              +
  |  k defined in KDF for Session Request |
  +  n = 0                                +
  |  see KDF for associated data          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |   ChaCha20 encrypted data (payload)   |
  +          (length varies)              +
  |  k defined in KDF for Session Request |
  +  n = 1                                +
  |  see KDF for associated data          |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```
Données non chiffrées (balise d'authentification Poly1305 non affichée) :

```
  +----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                   X                   |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM encap_key            |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     Noise payload (block data)        |
  +          (length varies)              +
  |     see below for allowed blocks      |
  +----+----+----+----+----+----+----+----+
```
Tailles, sans compter la surcharge IP :

| Type | Code du type | Longueur X | Longueur msg 1 | Longueur msg 1 chiffré | Longueur msg 1 déchiffré | Longueur clé PQ | Longueur pl |
|------|--------------|------------|----------------|------------------------|--------------------------|-----------------|-------------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 896+pl | 832+pl | 800+pl | 800 | pl |
| MLKEM768_X25519 | 6 | 32 | 1280+pl | 1216+pl | 1184+pl | 1184 | pl |
| MLKEM1024_X25519 | 7 | n/a | trop grand | | | | |
Remarque : Les codes de type sont réservés à un usage interne uniquement. Les routeurs resteront de type 4, et la prise en charge sera indiquée dans les adresses du routeur.

MTU minimum pour MLKEM768_X25519 : 1318 pour IPv4 et 1338 pour IPv6. Voir ci-dessous.

Changements : le SSU2 actuel contient uniquement la charge utile dans une seule section ChaCha. Avec ML-KEM, une nouvelle section ChaCha sera ajoutée avant la charge utile, contenant le chiffré PQC (cryptographie post-quantique) chiffré.

#### SessionCreated (Type 1)

Modifications : le SSU2 actuel contient uniquement la charge utile dans une seule section ChaCha. Avec ML-KEM, une nouvelle section ChaCha sera ajoutée avant la charge utile, contenant le chiffré au post-quantique encrypté.

Contenu brut :

```
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 0-15, ChaCha20     |
  +  encrypted with Bob intro key and     +
  | derived key, see Header Encryption KDF|
  +----+----+----+----+----+----+----+----+
  |  Long Header bytes 16-31, ChaCha20    |
  +  encrypted with derived key n=0       +
  |  See Header Encryption KDF            |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +       Y, ChaCha20 encrypted           +
  |       with derived key n=0            |
  +              (32 bytes)               +
  |       See Header Encryption KDF       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 data (MLKEM)               |
  +   Encrypted and authenticated data    +
  |  length varies                        |
  +  k defined in KDF for Session Created +
  |  (before mixKey)                      |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |   ChaCha20 data (payload)             |
  +   Encrypted and authenticated data    +
  |  length varies                        |
  +  k defined in KDF for Session Created +
  |  (after mixKey)                       |
  +  n = 0; see KDF for associated data   +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +        Poly1305 MAC (16 bytes)        +
  |                                       |
  +----+----+----+----+----+----+----+----+


```
Données non chiffrées (balise d'authentification Poly1305 non affichée) :

```
  +----+----+----+----+----+----+----+----+
  |      Destination Connection ID        |
  +----+----+----+----+----+----+----+----+
  |   Packet Number   |type| ver| id |flag|
  +----+----+----+----+----+----+----+----+
  |        Source Connection ID           |
  +----+----+----+----+----+----+----+----+
  |                 Token                 |
  +----+----+----+----+----+----+----+----+
  |                                       |
  +                                       +
  |                  Y                    |
  +              (32 bytes)               +
  |                                       |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |           ML-KEM Ciphertext           |
  +      (see table below for length)     +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |     Noise payload (block data)        |
  +          (length varies)              +
  |      see below for allowed blocks     |
  +----+----+----+----+----+----+----+----+
```
Tailles, sans compter la surcharge IP :

| Type | Code de type | Longueur Y | Longueur Msg 2 | Longueur Msg 2 enc | Longueur Msg 2 déc | Longueur CT PQ | Longueur pl |
|------|-----------|-------|-----------|---------------|---------------|-----------|--------|
| X25519 | 4 | 32 | 80+pl | 16+pl | pl | -- | pl |
| MLKEM512_X25519 | 5 | 32 | 864+pl | 800+pl | 768+pl | 768 | pl |
| MLKEM768_X25519 | 6 | 32 | 1184+pl | 1120+pl | 1088+pl | 1088 | pl |
| MLKEM1024_X25519 | 7 | n/a | trop grand | | | | |
Remarque : Les codes de type sont réservés à un usage interne uniquement. Les routeurs resteront de type 4, et la prise en charge sera indiquée dans les adresses du routeur.

MTU minimum pour MLKEM768_X25519 : 1318 pour IPv4 et 1338 pour IPv6. Voir ci-dessous.

Taille maximale : Alice ne possède pas encore le RouterInfo de Bob et ne connaît pas son MTU publié. Pour ce message, utilisez un MTU temporaire comme suit. Pour MLKEM512_X25519, utilisez le maximum entre 1280 et la taille du SessionRequest reçu comme MTU. Pour MLKEM768_X25519, utilisez le maximum entre (1318 pour IPv4 ou 1338 pour IPv6) et la taille du SessionRequest reçu comme MTU. La surcharge de SessionCreated est plus faible que celle de SessionRequest, car le chiffré MLKEM est plus petit que la clé publique MLKEM. Cela permet une plage de tailles de bourrage dans SessionCreated, même s’il y avait peu ou pas de bourrage dans le SessionRequest.

#### SessionConfirmed (Type 2)

unchanged

#### KDF pour la phase de données

unchanged

#### Relais et test de pairs

Les blocs suivants contiennent des champs de version. Ils resteront en version 2 (pour assurer la compatibilité avec un Bob non-PQ) et ne passeront pas en version 3/4 pour le PQ.

* [CABFORUM](https://cabforum.org/2024/10/10/2024-10-10-minutes-of-the-code-signing-certificate-working-group/)
* [Choosing-Hash](https://kerkour.com/fast-secure-hash-function-sha256-sha512-sha3-blake3)
* [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/)
* [COMMON](/docs/specs/common-structures/)
* [COMPOSITE-SIGS](https://datatracker.ietf.org/doc/draft-ietf-lamps-pq-composite-sigs/)
* [ECIES](/docs/specs/ecies/)
* [FORUM](http://zzz.i2p/topics/3294)
* [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
* [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
* [FIPS204](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf)
* [FIPS205](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.205.pdf)
* [MLDSA-OIDS](https://datatracker.ietf.org/doc/draft-ietf-lamps-dilithium-certificates/)
* [NIST-PQ](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards)
* [NIST-PQ-UPDATE](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf)
* [NIST-PQ-END](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf)
* [NIST-VECTORS](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values)
* [Noise](https://noiseprotocol.org/noise.html)
* [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf)
* [NSA-PQ](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF)
* [NTCP2](/docs/specs/ntcp2/)
* [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/)
* [Prop165](/docs/proposals/165/)
* [PQ-WIREGUARD](https://eprint.iacr.org/2020/379.pdf)
* [RFC-2104](https://tools.ietf.org/html/rfc2104)
* [Rosenpass](https://rosenpass.eu/)
* [Rosenpass-Whitepaper](https://raw.githubusercontent.com/rosenpass/rosenpass/papers-pdf/whitepaper.pdf)
* [SSH-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-sshm-mlkem-hybrid-kex/)
* [SSU2](/docs/specs/ssu2/)
* [TLS-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-tls-hybrid-design/)

#### Adresses publiées

Dans tous les cas, utilisez le nom de transport SSU2 comme d'habitude. MLKEM-1024 n'est pas pris en charge.

Utilisez la même adresse/port que pour les configurations non-PQ et non-firewallées. Une ou les deux variantes PQ sont prises en charge. Dans l'adresse du router, publiez v=2 (comme d'habitude) ainsi que le nouveau paramètre pq=[3|4|3,4|4,3] pour indiquer MLKEM 512/768/les deux. Les routers dont le MTU est inférieur au minimum spécifié ci-dessous ne doivent pas publier un paramètre « pq » contenant « 4 ». Publiez 4,3 pour indiquer une préférence pour MLKEM-768, ou 3,4 pour indiquer une préférence pour MLKEM-512. La version réelle est laissée à la discrétion de l'initiateur, et la préférence peut ne pas être respectée. Les routers dont le MTU est inférieur au minimum spécifié ci-dessous ne doivent pas se connecter en utilisant MLKEM768. Les routers plus anciens ignoreront le paramètre pq et se connecteront en mode non-pq comme d'habitude.

Une adresse/port différent(e) pour non-PQ, ou PQ uniquement, non-firewallé n'est PAS supporté. Cela ne sera pas implémenté avant que SSU2 non-PQ soit désactivé, dans plusieurs années. Lorsque le non-PQ sera désactivé, une ou les deux variantes PQ seront supportées. Dans l'adresse du router, publier v=[3|4|3,4|4,3] pour indiquer MLKEM 512/768/les deux. Les routers plus anciens vérifieront le paramètre v et ignoreront cette adresse comme non supportée.

Adresses derrière un pare-feu (aucune IP publiée) : Dans l'adresse du router, publier v=2 (comme d'habitude). Le paramètre pq DOIT être publié dans les adresses derrière un pare-feu, afin de prendre en charge le relais.

Alice peut se connecter à un Bob PQ en utilisant la variante PQ que Bob publie, que Alice annonce ou non la prise en charge de PQ dans ses informations de routeur, ou qu'elle annonce la même variante.

#### MTU

Veillez à ne pas dépasser le MTU avec MLKEM768. Le MTU minimum pour MLKEM768_X25519 est de 1318 pour IPv4 et 1338 pour IPv6 (en supposant un payload minimal de 10 octets avec un bloc DateTime et un bloc Padding ou RelayTagRequest). Le MTU minimum pour SSU2 en général est de 1280, donc tous les pairs ne pourront pas utiliser MLKEM768. Ne publiez pas et n'utilisez pas MLKEM768 si le MTU réel est inférieur au minimum, que ce soit localement ou tel qu'annoncé par le pair. Veillez à ne pas inclure un rembourrage (padding) tel que le message 1 ou 2 dépasserait le MTU local ou distant.

## Analyse des surcoûts

### Échange de clés

Augmentation de taille (octets) :

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Pubkey (Msg 1)</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Ciphertext (Msg 2)</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+816</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+784</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+1200</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+1104</td>
</tr>
</table>
## Analyse de sécurité

Les catégories de sécurité NIST sont résumées dans la [présentation NIST](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf), diapositive 10. Critères préliminaires : notre catégorie de sécurité NIST minimale devrait être 2 pour les protocoles hybrides et 3 pour les protocoles PQ uniquement.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Category</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">As Secure As</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES128</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">SHA256</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES192</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">SHA384</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES256</td>
</tr>
</table>
### Handshakes

Ce sont tous des protocoles hybrides. Les implémentations devraient préférer MLKEM768 ; MLKEM512 n'est pas suffisamment sécurisé.

Catégories de sécurité NIST [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) :

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Algorithm</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Security Category</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
</tr>
</table>
## Notes d'implémentation

### Support de bibliothèque

Les bibliothèques Bouncycastle, BoringSSL et WolfSSL prennent désormais en charge MLKEM et MLDSA. Le support OpenSSL sera inclus dans leur version 3.5 prévue le 8 avril 2025 [OpenSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

### Identification du trafic entrant

Nous définissons le bit de poids fort de la clé éphémère (key[31] & 0x80) dans la demande de session pour indiquer qu'il s'agit d'une connexion hybride. Cela nous permet de faire fonctionner simultanément le NTCP standard et le NTCP hybride sur le même port. Une seule variante hybride est prise en charge pour les connexions entrantes, et est annoncée dans l'adresse du router. Par exemple, pq=3 ou pq=4.

## Compatibilité des routeurs

### Noms des transports

En tant qu'Alice, pour une connexion PQ, avant l'obfuscation, définir X[31] |= 0x80. Cela rend X une clé publique X25519 invalide. Après l'obfuscation, AES-CBC va la randomiser. Le bit de poids fort de X sera aléatoire après l'obfuscation.

## Références

* [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/)
* [COMMON](/docs/specs/common-structures/)
* [ECIES](/docs/specs/ecies/)
* [FORUM](http://zzz.i2p/topics/3294)
* [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
* [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
* [NIST-PQ](https://www.nist.gov/news-events/news/2024/08/nist-releases-first-3-finalized-post-quantum-encryption-standards)
* [NIST-PQ-UPDATE](https://csrc.nist.gov/csrc/media/Presentations/2022/update-on-post-quantum-encryption-and-cryptographi/Day%202%20-%20230pm%20Chen%20PQC%20ISPAB.pdf)
* [NIST-PQ-END](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf)
* [NIST-VECTORS](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values)
* [Noise](https://noiseprotocol.org/noise.html)
* [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf)
* [NSA-PQ](https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF)
* [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/)
* [Prop165](/docs/proposals/165/)
* [PQ-WIREGUARD](https://eprint.iacr.org/2020/379.pdf)
* [RFC-2104](https://tools.ietf.org/html/rfc2104)
* [Rosenpass](https://rosenpass.eu/)
* [Rosenpass-Whitepaper](https://raw.githubusercontent.com/rosenpass/rosenpass/papers-pdf/whitepaper.pdf)
* [SSH-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-sshm-mlkem-hybrid-kex/)
* [SSU2](/docs/specs/ssu2/)
* [TLS-HYBRID](https://datatracker.ietf.org/doc/draft-ietf-tls-hybrid-design/)
