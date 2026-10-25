---
title: "PQ Hybrid ECIES-X25519-AEAD-Ratchet"
description: "Variante hybride post-quantique du protocole de chiffrement ECIES utilisant ML-KEM"
slug: "ecies-hybrid"
category: "Protocoles"
lastUpdated: "2026-04"
accurateFor: "0.9.69"
---

## Note

Implémentation, tests et déploiement en cours dans les différentes implémentations de router. Consultez la documentation de ces implémentations pour connaître le statut.

## Aperçu

Il s'agit de la variante PQ Hybrid du protocole ECIES-X25519-AEAD-Ratchet [ECIES](/docs/specs/ecies/). C'est la première phase de la proposition PQ globale [Prop169](/proposals/169-pq-crypto/) à être approuvée. Consultez cette proposition pour les objectifs généraux, les modèles de menaces, l'analyse, les alternatives et les informations supplémentaires.

Cette spécification ne contient que les différences par rapport au standard [ECIES](/docs/specs/ecies/) et doit être lue conjointement avec cette spécification.

## Conception

Nous prenons en charge la norme NIST FIPS 203 [FIPS 203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf), qui est basée sur CRYSTALS-Kyber, mais n'est PAS compatible avec celui-ci.

Les handshakes hybrides sont tels que spécifiés dans [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf).

### Échange de clés

Nous définissons un échange de clés hybride pour Ratchet. PQ KEM fournit uniquement des clés éphémères et ne prend pas directement en charge les poignées de main à clé statique telles que Noise IK.

Nous définissons les trois variantes ML-KEM comme dans [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf), pour 3 nouveaux types de chiffrement au total. Les types hybrides ne sont définis qu'en combinaison avec X25519.

Les nouveaux types de chiffrement sont :

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Code</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
</tr>
</table>
La surcharge sera substantielle. Les tailles typiques des messages 1 et 2 (pour IK) sont actuellement d'environ 100 octets (avant toute charge utile supplémentaire). Ceci augmentera de 8x à 15x selon l'algorithme.

### Nouvelle cryptographie requise

- ML-KEM (anciennement CRYSTALS-Kyber) [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
- SHA3-128 (anciennement Keccak-256) [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf) Utilisé uniquement pour SHAKE128
- SHA3-256 (anciennement Keccak-512) [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
- SHAKE128 et SHAKE256 (extensions XOF pour SHA3-128 et SHA3-256)
  [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)

Les vecteurs de test pour SHA3-256, SHAKE128, et SHAKE256 sont disponibles sur [NIST-VECTORS](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values).

Notez que la bibliothèque Java bouncycastle prend en charge tout ce qui précède. La prise en charge de la bibliothèque C++ se trouve dans OpenSSL 3.5 [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

## Spécification

### Structures Communes

Voir la spécification des structures communes [COMMON](/docs/specs/common-structures/) pour les longueurs de clés et les identifiants.

### Modèles de négociation

Les handshakes utilisent les modèles de handshake [Noise](https://noiseprotocol.org/noise.html).

La correspondance de lettres suivante est utilisée :

- e = clé éphémère à usage unique
- s = clé statique
- p = charge utile du message
- e1 = clé PQ éphémère à usage unique, envoyée d'Alice à Bob
- ekem1 = le texte chiffré KEM, envoyé de Bob à Alice

Les modifications suivantes à XK et IK pour la confidentialité persistante hybride (hfs) sont spécifiées dans [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) section 5 :

```
IK:                         IKhfs:
<- s                        <- s
...                         ...
-> e, es, s, ss, p          -> e, es, e1, s, ss, p
<- tag, e, ee, se, p        <- tag, e, ee, ekem1, se, p
<- p                        <- p
p ->                        p ->

e1 and ekem1 are encrypted. See pattern definitions below.
NOTE: e1 and ekem1 are different sizes (unlike X25519)
```
Le motif e1 est défini comme suit, tel que spécifié dans [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) section 4 :

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
Le motif ekem1 est défini comme suit, tel que spécifié dans la section 4 de [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf) :

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
### Opérations ML-KEM définies

Nous définissons les fonctions suivantes correspondant aux blocs de construction cryptographiques utilisés tels que définis dans [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf).

**(encap_key, decap_key) = PQ_KEYGEN()**

Alice crée les clés d'encapsulation et de décapsulation. La clé d'encapsulation est envoyée dans le message NS. Les tailles d'encap_key et decap_key varient selon la variante ML-KEM.

**(ciphertext, kem_shared_key) = ENCAPS(encap_key)**

Bob calcule le texte chiffré et la clé partagée, en utilisant le texte chiffré reçu dans le message NS. Le texte chiffré est envoyé dans le message NSR. La taille du texte chiffré varie selon la variante ML-KEM. La kem_shared_key fait toujours 32 octets.

**kem_shared_key = DECAPS(ciphertext, decap_key)**

Alice calcule la clé partagée, en utilisant le texte chiffré reçu dans le message NSR. La kem_shared_key fait toujours 32 octets.

Notez que l'encap_key et le texte chiffré sont tous deux chiffrés à l'intérieur des blocs ChaCha/Poly dans les messages 1 et 2 de la négociation Noise. Ils seront déchiffrés dans le cadre du processus de négociation.

La kem_shared_key est mélangée dans la clé de chaînage avec MixHash(). Voir ci-dessous pour les détails.

### KDF de handshake Noise

#### Aperçu

Le handshake hybride est défini dans [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf). Le premier message, d'Alice à Bob, contient e1, la clé d'encapsulation, avant la charge utile du message. Ceci est traité comme une clé statique supplémentaire ; appelez EncryptAndHash() dessus (en tant qu'Alice) ou DecryptAndHash() (en tant que Bob). Ensuite, traitez la charge utile du message comme d'habitude.

Le deuxième message, de Bob à Alice, contient ekem1, le texte chiffré, avant la charge utile du message. Ceci est traité comme une clé statique supplémentaire ; appelez EncryptAndHash() dessus (en tant que Bob) ou DecryptAndHash() (en tant qu'Alice). Ensuite, calculez la kem_shared_key et appelez MixKey(kem_shared_key). Puis traitez la charge utile du message comme d'habitude.

#### Identifiants Noise

Voici les chaînes d'initialisation Noise :

- "Noise_IKhfselg2_25519+MLKEM512_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM768_ChaChaPoly_SHA256"
- "Noise_IKhfselg2_25519+MLKEM1024_ChaChaPoly_SHA256"

#### Alice KDF pour message NS

Après le modèle de message 'es' et avant le modèle de message 's', ajoutez :

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

NOTE: For the next section (static key for IK),
the keydata and chain key remain the same, and n now equals 1
(instead of 0 for non-hybrid).
```
#### KDF de Bob pour le message NS

Après le motif de message 'es' et avant le motif de message 's', ajoutez :

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

NOTE: For the next section (static key for IK),
the keydata and chain key remain the same, and n now equals 1
(instead of 0 for non-hybrid).
```
#### Bob KDF pour Message NSR

Après le motif de message 'ee' et avant le motif de message 'se', ajoutez :

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
```
#### KDF d'Alice pour le message NSR

Après le modèle de message 'ee' et avant le modèle de message 'ss', ajouter :

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
```
#### KDF pour split()

inchangé

### Format du Message

#### Format NS

Changements : Le ratchet actuel contenait la clé statique dans la première section ChaCha, et la charge utile dans la seconde section. Avec ML-KEM, il y a maintenant trois sections. La première section contient la clé publique PQ chiffrée. La deuxième section contient la clé statique. La troisième section contient la charge utile.

Format chiffré :

```
+----+----+----+----+----+----+----+----+
|                                       |
+         New Session Ephemeral         +
|            Public Key                 |
+            32 bytes                   +
|      Encoded with Elligator2          |
+----+----+----+----+----+----+----+----+
|                                       |
+         ML-KEM encap_key              +
|       ChaCha20 encrypted data         |
+   (see table below for length)        +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+      (MAC) for encap_key Section      +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
|                                       |
+         X25519 Static Key             +
|       ChaCha20 encrypted data         |
+            32 bytes                   +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+     (MAC) for Static Key Section      +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
|                                       |
+          Payload Section              +
|       ChaCha20 encrypted data         |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+      (MAC) for Payload Section        +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
```
Format décrypté :

```
Payload Part 1:

+----+----+----+----+----+----+----+----+
|                                       |
+         ML-KEM encap_key              +
|                                       |
+   (see table below for length)        +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

Payload Part 2:

+----+----+----+----+----+----+----+----+
|                                       |
+         X25519 Static Key             +
|            (32 bytes)                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

Payload Part 3:

+----+----+----+----+----+----+----+----+
|                                       |
+          Payload Section              +
|                                       |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
Tailles :

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">X len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NS len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NS Enc len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NS Dec len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">PQ key len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">pl len</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">96+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">64+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">--</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">912+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">880+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">800+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">800</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1296+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1360+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1184+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1184</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1680+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1648+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1568+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1568</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
</table>
Notez que la charge utile doit contenir un bloc DateTime, donc la taille minimale de la charge utile est de 7. Les tailles NS minimales peuvent être calculées en conséquence.

#### Format NSR

Changements : Le ratchet actuel a une charge utile vide pour la première section ChaCha, et la charge utile dans la seconde section. Avec ML-KEM, il y a maintenant trois sections. La première section contient le texte chiffré PQ chiffré. La seconde section a une charge utile vide. La troisième section contient la charge utile.

Format chiffré :

```
+----+----+----+----+----+----+----+----+
|       Session Tag 8 bytes             |
+----+----+----+----+----+----+----+----+
|                                       |
+       Ephemeral Public Key            +
|            32 bytes                   |
+      Encoded with Elligator2          +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+         ML-KEM ciphertext             +
|       ChaCha20 encrypted data         |
+   (see table below for length)        +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+     (MAC) for ciphertext Section      +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+   (MAC) for key Section (no data)     +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
|                                       |
+          Payload Section              +
|       ChaCha20 encrypted data         |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+      (MAC) for Payload Section        +
|              16 bytes                 |
+----+----+----+----+----+----+----+----+
```
Format décrypté :

```
Payload Part 1:

+----+----+----+----+----+----+----+----+
|                                       |
+         ML-KEM ciphertext             +
|                                       |
+   (see table below for length)        +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

Payload Part 2:

empty

Payload Part 3:

+----+----+----+----+----+----+----+----+
|                                       |
+          Payload Section              +
|                                       |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
Tailles :

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Y len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NSR len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NSR Enc len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">NSR Dec len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">PQ CT len</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">opt len</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">72+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">--</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">856+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">816+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">768+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">768</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1176+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1136+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1088+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1088</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1656+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1616+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1568+pl</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1568</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">pl</td>
</tr>
</table>
Notez que bien que NSR ait normalement une charge utile non nulle, la spécification ratchet [ECIES](/docs/specs/ecies/) ne l'exige pas, donc la taille minimale de charge utile est 0. Les tailles NSR minimales peuvent être calculées en conséquence.

## Analyse des frais généraux

### Échange de clés

Augmentation de taille (octets) :

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Pubkey (NS)</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Ciphertext (NSR)</th>
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
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+1584</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">+1584</td>
</tr>
</table>
Vitesse :

Vitesses rapportées par [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/) :

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Relative speed</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">X25519 DH/keygen</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">baseline</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2.25x faster</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1.5x faster</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1x (same)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">XK</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4x DH (keygen + 3 DH)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM512_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4x DH + 2x PQ (keygen + enc/dec) = 4.9x DH = 22% slower</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM768_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4x DH + 2x PQ (keygen + enc/dec) = 5.3x DH = 32% slower</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024_X25519</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4x DH + 2x PQ (keygen + enc/dec) = 6x DH = 50% slower</td>
</tr>
</table>
## Analyse de sécurité

Les catégories de sécurité NIST sont résumées dans [NIST-PQ-END](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf) diapositive 10. Critères préliminaires : Notre catégorie de sécurité NIST minimale devrait être 2 pour les protocoles hybrides et 3 pour PQ uniquement.

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
### Négociations

Ce sont tous des protocoles hybrides. Il faut probablement privilégier MLKEM768 ; MLKEM512 n'est pas suffisamment sécurisé.

Catégories de sécurité NIST [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf) :

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
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">MLKEM1024</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
</tr>
</table>
## Préférences de type

Le type recommandé pour le support initial, basé sur la catégorie de sécurité et la longueur de clé, est :

MLKEM768_X25519 (type 6)

## Notes d'implémentation

### Support de Bibliothèque

Les bibliothèques Bouncycastle, BoringSSL et WolfSSL prennent désormais en charge MLKEM. Le support d'OpenSSL est prévu dans leur version 3.5 du 8 avril 2025 [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/).

### Tunnels Partagés

La classification/détection automatique de plusieurs protocoles sur les mêmes tunnels devrait être possible en se basant sur une vérification de la longueur du message 1 (New Session Message). En utilisant MLKEM512_X25519 comme exemple, la longueur du message 1 est de 816 octets plus grande que le protocole ratchet actuel, et la taille minimale du message 1 (avec seulement une charge utile DateTime incluse) est de 919 octets. La plupart des tailles de message 1 avec le ratchet actuel ont une charge utile de moins de 816 octets, elles peuvent donc être classifiées comme ratchet non-hybride. Les messages volumineux sont probablement des POST qui sont rares.

La stratégie recommandée est donc :

- Si le message 1 fait moins de 919 octets, c'est le protocole ratchet actuel.
- Si le message 1 fait 919 octets ou plus, c'est probablement MLKEM512_X25519. Essayez d'abord MLKEM512_X25519, et si cela échoue, essayez le protocole ratchet actuel.

Cela devrait nous permettre de prendre en charge efficacement le ratchet standard et le ratchet hybride sur la même destination, tout comme nous avons précédemment pris en charge ElGamal et ratchet sur la même destination. Par conséquent, nous pouvons migrer vers le protocole hybride MLKEM beaucoup plus rapidement que si nous ne pouvions pas prendre en charge des protocoles doubles pour la même destination, car nous pouvons ajouter la prise en charge de MLKEM aux destinations existantes.

Les combinaisons prises en charge requises sont :

- X25519 + MLKEM512
- X25519 + MLKEM768
- X25519 + MLKEM1024

Les combinaisons suivantes peuvent être complexes et ne sont PAS obligatoirement supportées, mais peuvent l'être, selon l'implémentation :

- Plus d'un MLKEM
- ElG + un ou plusieurs MLKEM
- X25519 + un ou plusieurs MLKEM
- ElG + X25519 + un ou plusieurs MLKEM

Il n'est pas nécessaire de prendre en charge plusieurs algorithmes MLKEM (par exemple, MLKEM512_X25519 et MLKEM_768_X25519) sur la même destination. Choisissez-en un seul. Dépendant de l'implémentation.

Il n'est pas obligatoire de prendre en charge trois algorithmes (par exemple X25519, MLKEM512_X25519, et MLKEM769_X25519) sur la même destination. La classification et la stratégie de nouvelle tentative peuvent être trop complexes. La configuration et l'interface utilisateur de configuration peuvent être trop complexes. Dépendant de l'implémentation.

Il n'est pas requis de prendre en charge les algorithmes ElGamal et hybrides sur la même destination. ElGamal est obsolète, et ElGamal + hybride uniquement (pas de X25519) n'a pas beaucoup de sens. De plus, les messages de nouvelle session ElGamal et hybrides sont tous deux volumineux, donc les stratégies de classification devraient souvent essayer les deux déchiffrements, ce qui serait inefficace. Dépendant de l'implémentation.

Les clients peuvent utiliser les mêmes clés statiques X25519 ou des clés différentes pour les protocoles X25519 et hybride sur les mêmes tunnels, selon l'implémentation.

### Confidentialité persistante

La spécification ECIES permet les Garlic Messages dans la charge utile du New Session Message, ce qui permet la livraison 0-RTT du paquet de streaming initial, généralement un HTTP GET, conjointement avec le leaseset du client. Cependant, la charge utile du New Session Message n'a pas de confidentialité persistante. Étant donné que cette proposition met l'accent sur une confidentialité persistante renforcée pour le ratchet, les implémentations peuvent ou devraient différer l'inclusion de la charge utile de streaming, ou du message de streaming complet, jusqu'au premier Existing Session Message. Cela se ferait au détriment de la livraison 0-RTT. Les stratégies peuvent également dépendre du type de trafic ou du type de tunnel, ou de GET vs. POST, par exemple. Dépendant de l'implémentation.

### Taille de nouvelle session

MLKEM augmentera considérablement la taille du New Session Message, comme décrit ci-dessus. Cela peut diminuer significativement la fiabilité de la livraison du New Session Message à travers les tunnels, où ils doivent être fragmentés en plusieurs messages tunnel de 1024 octets. Le succès de livraison est proportionnel au nombre exponentiel de fragments. Les implémentations peuvent utiliser diverses stratégies pour limiter la taille du message, au détriment de la livraison 0-RTT. Dépendant de l'implémentation.

## Références

- [CLOUDFLARE](https://blog.cloudflare.com/pq-2024/)
- [COMMON](/docs/specs/common-structures/)
- [ECIES](/docs/specs/ecies/)
- [FIPS202](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf)
- [FIPS203](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf)
- [FORUM](http://zzz.i2p/topics/3294)
- [NIST-PQ-END](https://www.nccoe.nist.gov/sites/default/files/2023-08/pqc-light-at-the-end-of-the-tunnel-presentation.pdf)
- [NIST-VECTORS](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/example-values)
- [Noise](https://noiseprotocol.org/noise.html)
- [Noise-Hybrid](https://github.com/noiseprotocol/noise_hfs_spec/blob/master/output/noise_hfs.pdf)
- [OPENSSL](https://openssl-library.org/post/2025-02-04-release-announcement-3.5/)
- [PQ-WIREGUARD](https://eprint.iacr.org/2020/379.pdf)
- [Prop169](/proposals/169-pq-crypto/)
