---
title: "Chiffrement hybride ECIES-X25519-AEAD-Ratchet"
description: "Variante hybride post-quantique du protocole de chiffrement ECIES utilisant ML-KEM (mécanisme d'encapsulation de clés post-quantique basé sur des réseaux modulaires)"
slug: "ecies-hybrid"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Statut de l’implémentation

**Déploiement actuel:** - **i2pd (implémentation C++)**: Entièrement implémenté dans la version 2.58.0 (septembre 2025), avec prise en charge de ML-KEM-512, ML-KEM-768 et ML-KEM-1024. Le chiffrement de bout en bout post-quantique est activé par défaut lorsque OpenSSL 3.5.0 ou une version ultérieure est disponible. - **Java I2P**: Pas encore implémenté à la version 0.9.67 / 2.10.0 (septembre 2025). Spécification approuvée et mise en œuvre prévue pour de prochaines versions.

Cette spécification décrit les fonctionnalités approuvées actuellement déployées dans i2pd et prévues pour les implémentations Java I2P.

## Vue d'ensemble

Ceci est la variante hybride post-quantique du protocole ECIES-X25519-AEAD-Ratchet [ECIES](/docs/specs/ecies/). Elle représente la première phase de la Proposition 169 [Prop169](/proposals/169-pq-crypto/) à être approuvée. Voir cette proposition pour les objectifs globaux, les modèles de menace, l'analyse, les alternatives et des informations supplémentaires.

Statut de la proposition 169 : **Ouvert** (première phase approuvée pour une implémentation ECIES hybride).

La présente spécification ne contient que les différences par rapport à la norme [ECIES](/docs/specs/ecies/) et doit être lue conjointement avec cette dernière.

## Conception

Nous utilisons la norme NIST FIPS 203 [FIPS203](https://csrc.nist.gov/pubs/fips/203/final) qui est basée sur, mais n'est pas compatible avec, CRYSTALS-Kyber (versions 3.1, 3 et antérieures).

Les poignées de main hybrides combinent le Diffie-Hellman X25519 classique avec des mécanismes d’encapsulation de clés post-quantiques ML-KEM. Cette approche s’appuie sur des concepts de confidentialité persistante hybride documentés dans la recherche PQNoise et sur des implémentations similaires dans TLS 1.3, IKEv2 et WireGuard.

### Échange de clés

Nous définissons un échange de clés hybride pour Ratchet. Un KEM post-quantique (mécanisme d'encapsulation de clé) ne fournit que des clés éphémères et ne prend pas directement en charge les échanges initiaux à clés statiques tels que Noise IK.

Nous définissons les trois variantes ML-KEM (mécanisme d'encapsulation de clés post-quantique à réseaux modulaires) telles que spécifiées dans [FIPS203](https://csrc.nist.gov/pubs/fips/203/final), ce qui représente au total 3 nouveaux types de chiffrement. Les types hybrides ne sont définis qu'en combinaison avec X25519.

Les nouveaux types de chiffrement sont :

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Security Level</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">ML-KEM Variant</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NIST Category 1 (AES-128 equivalent)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ML-KEM-512</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NIST Category 3 (AES-192 equivalent)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ML-KEM-768 (Recommended)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NIST Category 5 (AES-256 equivalent)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ML-KEM-1024</td>
    </tr>
  </tbody>
</table>
**Remarque:** MLKEM768_X25519 (Type 6) est la variante par défaut recommandée, offrant une sécurité post-quantique robuste avec un surcoût raisonnable.

La surcharge est considérable par rapport au chiffrement reposant uniquement sur X25519. Les tailles typiques des messages 1 et 2 (pour l'IK pattern (schéma IK)) sont actuellement d'environ 96 à 103 octets (avant toute charge utile supplémentaire). Cela augmentera d'environ 9-12x pour MLKEM512, 13-16x pour MLKEM768, et 17-23x pour MLKEM1024, selon le type de message.

### Nouveau chiffrement requis

- **ML-KEM** (anciennement CRYSTALS-Kyber) [FIPS203](https://csrc.nist.gov/pubs/fips/203/final) - Norme relative au mécanisme d’encapsulation de clés basé sur des réseaux modulaires
- **SHA3-256** (anciennement Keccak-512) [FIPS202](https://csrc.nist.gov/pubs/fips/202/final) - Partie de la norme SHA-3
- **SHAKE128 et SHAKE256** (extensions XOF (fonctions à sortie extensible) de SHA3) [FIPS202](https://csrc.nist.gov/pubs/fips/202/final) - Fonctions à sortie extensible

Des vecteurs de test pour SHA3-256, SHAKE128 et SHAKE256 sont disponibles dans le [Programme de validation des algorithmes cryptographiques du NIST](https://csrc.nist.gov/Projects/cryptographic-algorithm-validation-program).

**Prise en charge des bibliothèques:** - Java: la bibliothèque Bouncycastle à partir de la version 1.79 prend en charge toutes les variantes de ML-KEM et les fonctions SHA3/SHAKE - C++: OpenSSL à partir de la version 3.5 inclut une prise en charge complète de ML-KEM (publiée en avril 2025) - Go: plusieurs bibliothèques sont disponibles pour l'implémentation de ML-KEM et de SHA3

## Spécification

### Structures courantes

Voir la [Spécification des structures communes](/docs/specs/common-structures/) pour les longueurs de clés et les identifiants.

### Schémas de poignée de main

Les handshakes (échanges d'initialisation) utilisent les modèles de handshake du [Noise Protocol Framework](https://noiseprotocol.org/noise.html) avec des adaptations spécifiques à I2P pour une sécurité post-quantique hybride.

La table de correspondance suivante est utilisée :

- **e** = clé éphémère à usage unique (X25519)
- **s** = clé statique
- **p** = charge utile du message
- **e1** = clé post-quantique (PQ) éphémère à usage unique, envoyée d'Alice à Bob (jeton spécifique à I2P)
- **ekem1** = le texte chiffré KEM, envoyé de Bob à Alice (jeton spécifique à I2P)

**Note importante :** Les noms de patrons "IKhfs" et "IKhfselg2" et les jetons "e1" et "ekem1" sont des adaptations spécifiques à I2P qui ne sont pas documentées dans la spécification officielle du Noise Protocol Framework. Ils représentent des définitions personnalisées pour intégrer ML-KEM dans le Noise IK pattern (patron IK du protocole Noise). Bien que l’approche hybride X25519 + ML-KEM soit largement reconnue dans la recherche en cryptographie post-quantique et dans d’autres protocoles, la nomenclature utilisée ici est spécifique à I2P.

Les modifications suivantes apportées à IK pour une confidentialité persistante hybride sont appliquées :

```
Standard IK:              I2P IKhfs (Hybrid):
<- s                      <- s
...                       ...
-> e, es, s, ss, p        -> e, es, e1, s, ss, p
<- e, ee, se, p           <- e, ee, ekem1, se, p
<- p                      <- p
p ->                      p ->

Note: e1 and ekem1 are encrypted within ChaCha20-Poly1305 AEAD blocks.
Note: e1 (ML-KEM public key) and ekem1 (ML-KEM ciphertext) have different sizes.
```
Le modèle **e1** est défini comme suit :

```
For Alice (sender):
(encap_key, decap_key) = PQ_KEYGEN()

// EncryptAndHash(encap_key)
ciphertext = ENCRYPT(k, n, encap_key, ad)
n++
MixHash(ciphertext)

For Bob (receiver):
// DecryptAndHash(ciphertext)
encap_key = DECRYPT(k, n, ciphertext, ad)
n++
MixHash(ciphertext)
```
Le modèle **ekem1** est défini comme suit:

```
For Bob (receiver of encap_key):
(kem_ciphertext, kem_shared_key) = ENCAPS(encap_key)

// EncryptAndHash(kem_ciphertext)
ciphertext = ENCRYPT(k, n, kem_ciphertext, ad)
MixHash(ciphertext)

// MixKey
MixKey(kem_shared_key)

For Alice (sender of encap_key):
// DecryptAndHash(ciphertext)
kem_ciphertext = DECRYPT(k, n, ciphertext, ad)
MixHash(ciphertext)

// MixKey
kem_shared_key = DECAPS(kem_ciphertext, decap_key)
MixKey(kem_shared_key)
```
### Opérations ML-KEM définies

Nous définissons les fonctions suivantes correspondant aux primitives cryptographiques telles que spécifiées dans [FIPS203](https://csrc.nist.gov/pubs/fips/203/final).

**(encap_key, decap_key) = PQ_KEYGEN()** : Alice crée les clés d’encapsulation et de décapsulation. La clé d’encapsulation est envoyée dans le message NS. Tailles des clés :   - ML-KEM-512: encap_key = 800 octets, decap_key = 1632 octets   - ML-KEM-768: encap_key = 1184 octets, decap_key = 2400 octets   - ML-KEM-1024: encap_key = 1568 octets, decap_key = 3168 octets

**(ciphertext, kem_shared_key) = ENCAPS(encap_key)** : Bob calcule le texte chiffré et la clé partagée en utilisant la clé d'encapsulation reçue dans le message NS. Le texte chiffré est envoyé dans le message NSR. Tailles du texte chiffré:   - ML-KEM-512: 768 octets   - ML-KEM-768: 1088 octets   - ML-KEM-1024: 1568 octets

La kem_shared_key est toujours de **32 octets** pour les trois variantes.

**kem_shared_key = DECAPS(ciphertext, decap_key)** : Alice calcule la clé partagée en utilisant le texte chiffré reçu dans le message NSR. La kem_shared_key est toujours de 32 octets.

**Important:** L'encap_key et le texte chiffré sont tous deux chiffrés dans des blocs ChaCha20-Poly1305 dans les messages 1 et 2 du handshake (négociation initiale) Noise. Ils seront déchiffrés dans le cadre du processus de handshake.

La kem_shared_key est intégrée à la clé de chaînage avec MixKey(). Voir ci-dessous pour plus de détails.

### Fonction de dérivation de clés du handshake Noise

#### Aperçu

Le handshake hybride (poignée de main hybride) combine X25519 ECDH classique avec ML-KEM post-quantique. Le premier message, d’Alice à Bob, contient e1 (la clé d’encapsulation ML-KEM) avant la charge utile du message. Celle-ci est traitée comme un matériau de clé supplémentaire ; appelez EncryptAndHash() sur e1 (en tant qu’Alice) ou DecryptAndHash() (en tant que Bob). Traitez ensuite la charge utile du message comme d’habitude.

Le deuxième message, de Bob à Alice, contient ekem1 (le texte chiffré ML-KEM) avant la charge utile du message. Ceci est traité comme du matériel de clé supplémentaire; appelez EncryptAndHash() sur celui-ci (en tant que Bob) ou DecryptAndHash() (en tant qu’Alice). Calculez ensuite kem_shared_key et appelez MixKey(kem_shared_key). Traitez ensuite la charge utile du message comme d’habitude.

#### Identifiants Noise (cadre de protocoles cryptographiques)

Voici les chaînes d'initialisation Noise (spécifiques à I2P) :

- `Noise_IKhfselg2_25519+MLKEM512_ChaChaPoly_SHA256`
- `Noise_IKhfselg2_25519+MLKEM768_ChaChaPoly_SHA256`
- `Noise_IKhfselg2_25519+MLKEM1024_ChaChaPoly_SHA256`

#### KDF (fonction de dérivation de clés) d’Alice pour le message NS

Après le motif de message 'es' et avant le motif de message 's', ajoutez :

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
#### KDF (fonction de dérivation de clé) de Bob pour le message NS

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

NOTE: For the next section (payload for XK or static key for IK),
the keydata and chain key remain the same,
and n now equals 1 (instead of 0 for non-hybrid).
```
#### Fonction de dérivation de clé (KDF) de Bob pour le message NSR

Après le modèle de message 'ee' et avant le modèle de message 'se', ajoutez :

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
#### Fonction de dérivation de clé (KDF) d'Alice pour le message NSR

Après le motif de message 'ee' et avant le motif de message 'ss', ajoutez:

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
#### Fonction de dérivation de clé (KDF) pour split()

La fonction split() reste inchangée par rapport à la spécification standard d’ECIES. Après l’achèvement du handshake (négociation de session) :

```
keydata = HKDF(chainKey, ZEROLEN, "", 64)
k_ab = keydata[0:31]
k_ba = keydata[32:63]
```
Ce sont les clés de session bidirectionnelles pour la communication en cours.

### Format du message

#### Format de NS (New Session)

**Modifications :** Le ratchet (mécanisme de cliquet cryptographique) actuel contient la clé statique dans la première section ChaCha20-Poly1305 et la charge utile dans la deuxième section. Avec ML-KEM, il y a désormais trois sections. La première section contient la clé publique ML-KEM chiffrée (encap_key). La deuxième section contient la clé statique. La troisième section contient la charge utile.

**Tailles des messages :**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">X25519 len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NS len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NS Enc len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NS Dec len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">PQ key len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">pl len</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">96+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">--</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">912+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">880+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">800+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">800</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1296+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1264+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1184+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1184</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1680+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1648+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1568+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1568</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
  </tbody>
</table>
**Remarque :** La charge utile doit contenir un bloc DateTime (date-heure) (minimum 7 octets : type sur 1 octet, taille sur 2 octets, horodatage sur 4 octets). Les tailles NS minimales peuvent être calculées en conséquence. La taille NS pratique minimale est donc de 103 octets pour X25519 et va de 919 à 1687 octets pour les variantes hybrides.

Les augmentations de taille de 816, 1200 et 1584 octets pour les trois variantes de ML-KEM (mécanisme d’encapsulation de clés basé sur des réseaux modulaires) s’expliquent par l’ajout de la clé publique ML-KEM et d’un MAC Poly1305 de 16 octets pour le chiffrement authentifié.

#### NSR (réponse de nouvelle session) Format

**Modifications:** Le ratchet (mécanisme de cliquet cryptographique) actuel a une charge utile vide pour la première section ChaCha20-Poly1305 et place la charge utile dans la deuxième section. Avec ML-KEM, il y a désormais trois sections. La première section contient le texte chiffré de ML-KEM, lui-même chiffré. La deuxième section a une charge utile vide. La troisième section contient la charge utile.

**Tailles des messages:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">X25519 len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NSR len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NSR Enc len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NSR Dec len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">PQ ct len</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">pl len</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">72+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">40+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">--</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">856+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">824+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">784+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">768</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1176+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1144+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1104+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1088</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1656+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1624+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1584+pl</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1568</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">pl</td>
    </tr>
  </tbody>
</table>
Les augmentations de taille de 784, 1104 et 1584 octets pour les trois variantes de ML-KEM s’expliquent par le texte chiffré ML-KEM, ainsi qu’un MAC Poly1305 de 16 octets pour le chiffrement authentifié.

## Analyse de la surcharge

### Échange de clés

La surcharge du chiffrement hybride est considérable par rapport à X25519 seul :

- **MLKEM512_X25519**: Augmentation d'environ 9-12x de la taille du message de poignée de main (NS: 9.5x, NSR: 11.9x)
- **MLKEM768_X25519**: Augmentation d'environ 13-16x de la taille du message de poignée de main (NS: 13.5x, NSR: 16.3x)
- **MLKEM1024_X25519**: Augmentation d'environ 17-23x de la taille du message de poignée de main (NS: 17.5x, NSR: 23x)

Cette surcharge est acceptable compte tenu des avantages supplémentaires en matière de sécurité post-quantique. Les multiplicateurs varient selon le type de message, car les tailles de base des messages diffèrent (NS minimum 96 octets, NSR minimum 72 octets).

### Considérations sur la bande passante

Pour un établissement de session typique avec des charges utiles minimales: - X25519 uniquement: ~200 octets au total (NS + NSR) - MLKEM512_X25519: ~1,800 octets au total (augmentation de 9x) - MLKEM768_X25519: ~2,500 octets au total (augmentation de 12.5x) - MLKEM1024_X25519: ~3,400 octets au total (augmentation de 17x)

Après l’établissement de la session, le chiffrement continu des messages utilise le même format de transport de données que les sessions utilisant uniquement X25519, de sorte qu’il n’y a pas de surcharge pour les messages ultérieurs.

## Analyse de sécurité

### Poignées de main

Le handshake hybride offre une sécurité classique (X25519) et post-quantique (ML-KEM, mécanisme d'encapsulation de clé). Un attaquant doit casser **à la fois** l'ECDH classique et le KEM post-quantique pour compromettre les clés de session.

Cela fournit: - **Sécurité actuelle**: X25519 ECDH fournit une sécurité contre des adversaires classiques (niveau de sécurité de 128 bits) - **Sécurité future**: ML-KEM (mécanisme d’encapsulation de clé post-quantique) fournit une sécurité contre des adversaires quantiques (varie selon le jeu de paramètres) - **Sécurité hybride**: Les deux doivent être brisés pour compromettre la session (niveau de sécurité = maximum des deux composants)

### Niveaux de sécurité

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Variant</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">NIST Category</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Classical Security</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">PQ Security</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Hybrid Security</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Category 1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit (X25519)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-128 equivalent</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Category 3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit (X25519)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-192 equivalent</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Category 5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit (X25519)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256 equivalent</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128-bit</td>
    </tr>
  </tbody>
</table>
**Remarque :** Le niveau de sécurité hybride est borné par le plus faible des deux composants. Dans tous les cas, X25519 offre une sécurité classique de 128 bits. Si un ordinateur quantique pertinent du point de vue cryptographique devenait disponible, le niveau de sécurité dépendrait du jeu de paramètres ML-KEM choisi.

### Confidentialité persistante

L'approche hybride préserve les propriétés de confidentialité persistante. Les clés de session sont dérivées des deux échanges de clés éphémères, X25519 et ML-KEM. Si les clés privées éphémères X25519 ou ML-KEM sont détruites après le handshake (échange initial), les sessions passées ne peuvent pas être déchiffrées, même si les clés statiques à long terme sont compromises.

Le pattern IK (modèle IK) fournit une confidentialité persistante complète (confidentialité Noise niveau 5) après l’envoi du deuxième message (NSR).

## Préférences de type

Les implémentations devraient prendre en charge plusieurs types hybrides et négocier la variante la plus sûre mutuellement prise en charge. L’ordre de préférence devrait être :

1. **MLKEM768_X25519** (Type 6) - Valeur par défaut recommandée, meilleur équilibre entre sécurité et performances
2. **MLKEM1024_X25519** (Type 7) - Sécurité maximale pour les applications sensibles
3. **MLKEM512_X25519** (Type 5) - Niveau de sécurité post-quantique de base pour les scénarios avec ressources limitées
4. **X25519** (Type 4) - Classique uniquement, solution de repli pour la compatibilité

**Justification:** MLKEM768_X25519 est recommandé comme valeur par défaut car il offre une sécurité de catégorie 3 du NIST (équivalent AES-192), jugée suffisante pour se protéger contre les ordinateurs quantiques tout en conservant des tailles de messages raisonnables. MLKEM1024_X25519 offre une sécurité plus élevée, mais au prix d'une surcharge considérablement accrue.

## Notes d'implémentation

### Prise en charge des bibliothèques

- **Java**: La bibliothèque Bouncycastle à partir de la version 1.79 (août 2024) prend en charge toutes les variantes ML-KEM (mécanisme d'encapsulation de clés basé sur des réseaux modulaires) requises ainsi que les fonctions SHA3/SHAKE. Utilisez `org.bouncycastle.pqc.crypto.mlkem.MLKEMEngine` pour la conformité FIPS 203.
- **C++**: OpenSSL 3.5 (avril 2025) et versions ultérieures incluent la prise en charge de ML-KEM via l'interface EVP_KEM. Il s'agit d'une version à support à long terme (LTS) maintenue jusqu'en avril 2030.
- **Go**: Plusieurs bibliothèques tierces sont disponibles pour ML-KEM et SHA3, dont la bibliothèque CIRCL de Cloudflare.

### Stratégie de migration

Les implémentations devraient : 1. Prendre en charge à la fois X25519 seul et les variantes hybrides ML-KEM (mécanisme d’encapsulation de clé basé sur des réseaux modulaires, standard post-quantique) pendant la période de transition 2. Privilégier les variantes hybrides lorsque les deux pairs les prennent en charge 3. Conserver une solution de repli vers X25519 seul pour la rétrocompatibilité 4. Prendre en compte les contraintes de bande passante du réseau lors du choix de la variante par défaut

### Tunnels partagés

L’augmentation de la taille des messages peut affecter l’utilisation des tunnel partagés. Les implémentations devraient envisager: - Regrouper les handshakes (échanges d’amorçage) lorsque c’est possible pour amortir la surcharge - Utiliser des durées d’expiration plus courtes pour les sessions hybrides afin de réduire l’état stocké - Surveiller l’utilisation de la bande passante et ajuster les paramètres en conséquence - Mettre en œuvre un contrôle de congestion pour le trafic d’établissement de session

### Considérations sur la taille des nouvelles sessions

En raison de messages de handshake (négociation initiale) plus volumineux, les implémentations pourraient avoir besoin de: - augmenter les tailles de tampon pour la négociation de session (minimum de 4 Ko recommandé) - ajuster les valeurs de délai d'expiration pour les connexions plus lentes (tenir compte de messages ~3-17x plus volumineux) - envisager la compression des données de charge utile dans les messages NS/NSR - implémenter la gestion de la fragmentation si la couche de transport l'exige

### Tests et validation

Les implémentations devraient vérifier: - Exactitude de la génération de clés ML-KEM, de l'encapsulation et de la décapsulation - Intégration correcte de kem_shared_key dans Noise KDF - Les calculs de la taille des messages correspondent à la spécification - Interopérabilité avec d'autres implémentations de router I2P - Comportement de repli lorsque ML-KEM n'est pas disponible

Les vecteurs de test pour les opérations ML-KEM sont disponibles dans le [Programme de validation des algorithmes cryptographiques (Cryptographic Algorithm Validation Program)](https://csrc.nist.gov/Projects/cryptographic-algorithm-validation-program) du NIST.

## Compatibilité des versions

**Numérotation des versions d'I2P :** I2P maintient deux numéros de version parallèles : - **Version de publication du router** : format 2.x.x (par exemple, 2.10.0 publiée en septembre 2025) - **Version de l'API/protocole** : format 0.9.x (par exemple, 0.9.67 correspond au router 2.10.0)

Cette spécification fait référence à la version 0.9.67 du protocole, laquelle correspond à la version 2.10.0 du router et aux versions ultérieures.

**Matrice de compatibilité:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Implementation</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">ML-KEM Support</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2pd</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.58.0+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Full (512/768/1024)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deployed September 2025</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Java I2P</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67 / 2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Not yet</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Planned for future release</td>
    </tr>
  </tbody>
</table>
## Références

- **[ECIES]**: [Spécification ECIES-X25519-AEAD-Ratchet](/docs/specs/ecies/)
- **[Prop169]**: [Proposition 169 : cryptographie post-quantique](/proposals/169-pq-crypto/)
- **[FIPS203]**: [NIST FIPS 203 - Norme ML-KEM](https://csrc.nist.gov/pubs/fips/203/final)
- **[FIPS202]**: [NIST FIPS 202 - Norme SHA-3](https://csrc.nist.gov/pubs/fips/202/final)
- **[Noise]**: [Cadre du protocole Noise](https://noiseprotocol.org/noise.html)
- **[COMMON]**: [Spécification des structures communes](/docs/specs/common-structures/)
- **[RFC7539]**: [RFC 7539 - ChaCha20 et Poly1305](https://www.rfc-editor.org/rfc/rfc7539)
- **[RFC5869]**: [RFC 5869 - HKDF](https://www.rfc-editor.org/rfc/rfc5869)
- **[OpenSSL]**: [Documentation OpenSSL 3.5 ML-KEM](https://docs.openssl.org/3.5/man7/EVP_KEM-ML-KEM/)
- **[Bouncycastle]**: [Bibliothèque de cryptographie Java Bouncycastle](https://www.bouncycastle.org/)

---
