---
title: "LeaseSet (ensemble de baux I2P) chiffré"
description: "Format de LeaseSet avec contrôle d'accès pour les Destinations privées"
slug: "encryptedleaseset"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Aperçu

Ce document spécifie l’aveuglement, le chiffrement et le déchiffrement du LeaseSet2 (LS2) chiffré. Les LeaseSets chiffrés permettent la publication, avec contrôle d’accès, d’informations relatives aux services cachés dans la base de données du réseau I2P.

**Fonctionnalités clés:** - Rotation quotidienne des clés pour une confidentialité persistante - Autorisation client à deux niveaux (basée sur DH et basée sur PSK) - Chiffrement ChaCha20 pour des performances accrues sur les appareils sans accélération matérielle AES - Signatures Red25519 avec aveuglement de clé - Adhésion des clients respectueuse de la vie privée

**Documentation associée :** - [Spécification des structures communes](/docs/specs/common-structures/) - Structure de LeaseSet (jeu de baux I2P) chiffré - [Proposition 123 : Nouvelles entrées netDB](/proposals/123-new-netdb-entries/) - Contexte sur les LeaseSets chiffrés - [Documentation de la base de données réseau](/docs/specs/common-structures/) - Utilisation de NetDB (base de données réseau I2P)

---

## Historique des versions et état de l’implémentation

### Chronologie du développement du protocole

**Note importante sur la numérotation des versions :**   I2P utilise deux systèmes distincts de numérotation des versions : - **Version API/Router :** série 0.9.x (utilisée dans les spécifications techniques) - **Version de publication du produit :** série 2.x.x (utilisée pour les versions publiques)

Les spécifications techniques font référence aux versions de l'API (p. ex., 0.9.41), tandis que les utilisateurs finaux voient des versions du produit (p. ex., 2.10.0).

### Jalons d’implémentation

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Release Date</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Features</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.38</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">January 2019</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Floodfill support for standard LS2, offline keys</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.39</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">March 2019</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Full encrypted LS2 support, Red25519 (sig type&nbsp;11)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.40</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">May 2019</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Per-client authorization, encrypted LS2 with offline keys, B32 support</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.41</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">June 2019</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Protocol finalized as stable</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>2.10.0</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">September 2025</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Latest Java implementation (API version 0.9.61)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>i2pd 2.58.0</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">September 2025</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Full C++ implementation compatibility</td></tr>
  </tbody>
</table>
### État actuel

- ✅ **État du protocole:** Stable et inchangé depuis juin 2019
- ✅ **Java I2P:** Entièrement implémenté à partir de la version 0.9.40+
- ✅ **i2pd (C++):** Entièrement implémenté à partir de la version 2.58.0+
- ✅ **Interopérabilité:** Complète entre les implémentations
- ✅ **Déploiement réseau:** Prêt pour la production, avec plus de 6 ans d'expérience opérationnelle

---

## Définitions cryptographiques

### Notations et conventions

- `||` désigne la concaténation
- `mod L` désigne la réduction modulo l’ordre d’Ed25519
- Tous les tableaux d’octets sont en ordre d’octets réseau (big-endian) sauf indication contraire
- Les valeurs little-endian sont explicitement indiquées

### CSRNG(n)

**Générateur de nombres aléatoires cryptographiquement sûr**

Produit `n` octets de données aléatoires cryptographiquement sûres, adaptées à la génération de key material (matériel de clés).

**Exigences de sécurité:** - Doit être sécurisé sur le plan cryptographique (adapté à la génération de clés) - Doit rester sûr lorsque des séquences d’octets adjacentes sont exposées sur le réseau - Les implémentations devraient hacher la sortie provenant de sources potentiellement non fiables

**Références :** - [Considérations de sécurité concernant les PRNG](http://projectbullrun.org/dual-ec/ext-rand.html) - [Discussion des développeurs de Tor](https://lists.torproject.org/pipermail/tor-dev/2015-November/009954.html)

### H(p, d)

**Hachage SHA-256 avec personnalisation**

Fonction de hachage à séparation de domaine qui prend: - `p`: chaîne de personnalisation (fournit la séparation de domaine) - `d`: données à hacher

**Implémentation:**

```
H(p, d) := SHA-256(p || d)
```
**Utilisation:** Fournit une séparation de domaines cryptographique pour empêcher les attaques par collision entre différents usages protocolaires de SHA-256.

### Chiffrement par flux: ChaCha20

**Chiffre de flux : ChaCha20 conformément à la RFC 7539, section 2.4**

**Paramètres:** - `S_KEY_LEN = 32` (clé de 256 bits) - `S_IV_LEN = 12` (nonce de 96 bits, nombre utilisé une seule fois) - Compteur initial: `1` (RFC 7539 autorise 0 ou 1 ; 1 est recommandé pour les contextes AEAD)

**CHIFFRER(k, iv, plaintext)**

Chiffre le texte en clair à l'aide de: - `k`: clé de chiffrement de 32 octets - `iv`: nonce de 12 octets (DOIT être unique pour chaque clé) - Renvoie un texte chifré de la même taille que le texte en clair

**Propriété de sécurité :** L’intégralité du texte chiffré doit être indiscernable d’une donnée aléatoire si la clé est secrète.

**DÉCHIFFRER(k, iv, ciphertext)**

Déchiffre le texte chiffré en utilisant: - `k`: clé de chiffrement de 32 octets - `iv`: nonce de 12 octets - Renvoie le texte en clair

**Justification de la conception :** ChaCha20 a été préféré à AES car : - 2,5 à 3× plus rapide qu’AES sur les appareils sans accélération matérielle - Implémentation en temps constant plus facile à réaliser - Sécurité et vitesse comparables lorsque AES-NI est disponible

**Références:** - [RFC 7539](https://datatracker.ietf.org/doc/html/rfc7539) - ChaCha20 et Poly1305 pour les protocoles de l'IETF

### SIG : Red25519 (algorithme de signature Ed25519 utilisé par I2P)

**Schéma de signature : Red25519 (SigType 11) avec Key Blinding (aveuglement de clé)**

Red25519 est basé sur des signatures Ed25519 sur la courbe Ed25519, utilisant SHA-512 pour le hachage, avec prise en charge de l'aveuglement de clé tel que spécifié dans ZCash RedDSA.

**Fonctions :**

#### DERIVE_PUBLIC(privkey)

Renvoie la clé publique correspondant à la clé privée fournie. - Utilise la multiplication scalaire standard d'Ed25519 par le point de base

#### SIGN(privkey, m)

Renvoie une signature générée par la clé privée `privkey` pour le message `m`.

**Différences de signature Red25519 par rapport à Ed25519 :** 1. **Nonce aléatoire (valeur aléatoire à usage unique) :** Utilise 80 octets de données aléatoires supplémentaires

   ```
   T = CSRNG(80)  // 80 random bytes
   r = H*(T || publickey || message)
   ```
Cela rend chaque signature Red25519 (variante randomisée d'Ed25519) unique, même pour le même message et la même clé.

2. **Génération de clés privées:** Les clés privées Red25519 sont générées à partir de nombres aléatoires et réduites `mod L`, plutôt que d'utiliser l'approche de bit-clamping d'Ed25519 (ajustement des bits par masquage).

#### VERIFY(pubkey, m, sig)

Vérifie la signature `sig` par rapport à la clé publique `pubkey` et au message `m`. - Renvoie `true` si la signature est valide, `false` sinon - La vérification est identique à celle d’Ed25519

**Opérations d'aveuglement de clé:**

#### GENERATE_ALPHA(data, secret)

Génère alpha pour l'aveuglement de clé. - `data`: Contient généralement la clé publique de signature et les types de signature - `secret`: Secret additionnel optionnel (de longueur nulle s'il n'est pas utilisé) - Le résultat a la même distribution que les clés privées Ed25519 (après réduction mod L)

#### BLIND_PRIVKEY(privkey, alpha)

Procède à l’aveuglement d’une clé privée à l’aide du secret `alpha`. - Implémentation : `blinded_privkey = (privkey + alpha) mod L` - Utilise l’arithmétique scalaire dans le corps

#### BLIND_PUBKEY(pubkey, alpha)

Aveugle une clé publique à l'aide du secret `alpha`. - Implémentation: `blinded_pubkey = pubkey + DERIVE_PUBLIC(alpha)` - Utilise l'addition d'éléments du groupe (points) sur la courbe

**Propriété critique:**

```
BLIND_PUBKEY(pubkey, alpha) == DERIVE_PUBLIC(BLIND_PRIVKEY(privkey, alpha))
```
**Considérations de sécurité :**

D’après la spécification du protocole ZCash, section 5.4.6.1 : Pour des raisons de sécurité, alpha doit avoir la même distribution que les clés privées démasquées. Cela garantit que "la combinaison d’une clé publique ré-aléatoirisée et de signature(s) effectuée(s) avec cette clé ne révèle pas la clé d’origine à partir de laquelle elle a été ré-aléatoirisée".

**Types de signatures pris en charge:** - **Type 7 (Ed25519):** Pris en charge pour les destinations existantes (rétrocompatibilité) - **Type 11 (Red25519):** Recommandé pour les nouvelles destinations utilisant le chiffrement - **Clés aveuglées:** Utilisez toujours le type 11 (Red25519)

**Références:** - [Spécification du protocole ZCash](https://zips.z.cash/protocol/protocol.pdf) - Section 5.4.6 RedDSA - [Spécification Red25519 d'I2P](/docs/specs/red25519-signature-scheme/)

### DH: X25519

**Diffie-Hellman sur courbe elliptique: X25519**

Système de négociation de clé publique basé sur Curve25519.

**Paramètres:** - Clés privées: 32 octets - Clés publiques: 32 octets - Sortie du secret partagé: 32 octets

**Fonctions :**

#### GENERATE_PRIVATE()

Génère une nouvelle clé privée de 32 octets à l'aide d'un CSRNG (générateur de nombres aléatoires cryptographiquement sécurisé).

#### DERIVE_PUBLIC(privkey)

Dérive la clé publique de 32 octets à partir de la clé privée donnée. - Utilise la multiplication scalaire sur Curve25519

#### DH(privkey, pubkey)

Effectue un accord de clé Diffie-Hellman. - `privkey`: Clé privée locale de 32 octets - `pubkey`: Clé publique distante de 32 octets - Renvoie: Secret partagé de 32 octets

**Propriétés de sécurité:** - Hypothèse Diffie-Hellman computationnelle sur Curve25519 - Confidentialité persistante lorsque des clés éphémères sont utilisées - Implémentation en temps constant requise pour prévenir les attaques temporelles

**Références:** - [RFC 7748](https://datatracker.ietf.org/doc/html/rfc7748) - Courbes elliptiques pour la sécurité

### HKDF (fonction de dérivation de clés basée sur HMAC)

**Fonction de dérivation de clé basée sur HMAC**

Extrait et étend des données de clé à partir des données de clé d'entrée.

**Paramètres:** - `salt`: 32 octets maximum (généralement 32 octets pour SHA-256) - `ikm`: matériau de clé d'entrée (de longueur quelconque, doit présenter une bonne entropie) - `info`: informations spécifiques au contexte (séparation des domaines) - `n`: longueur de sortie en octets

**Implémentation:**

Utilise HKDF (fonction de dérivation de clés basée sur HMAC) tel que spécifié dans la RFC 5869 avec: - **Fonction de hachage:** SHA-256 - **HMAC:** Tel que spécifié dans la RFC 2104 - **Longueur du sel:** Maximum 32 octets (HashLen pour SHA-256)

**Schéma d’utilisation:**

```
keys = HKDF(salt, ikm, info, n)
```
**Séparation des domaines:** Le paramètre `info` assure une séparation cryptographique des domaines entre les différentes utilisations de HKDF dans le protocole.

**Valeurs d'informations vérifiées:** - "ELS2_L1K" - Chiffrement de la couche 1 (externe) - "ELS2_L2K" - Chiffrement de la couche 2 (interne) - "ELS2_XCA" - Autorisation client DH - "ELS2PSKA" - Autorisation client PSK - "i2pblinding1" - Génération alpha

**Références:** - [RFC 5869](https://datatracker.ietf.org/doc/html/rfc5869) - Spécification HKDF - [RFC 2104](https://datatracker.ietf.org/doc/html/rfc2104) - Spécification HMAC

---

## Spécification du format

LS2 (version 2 de LeaseSet) chiffré se compose de trois couches imbriquées :

1. **Couche 0 (Externe):** Informations en clair pour le stockage et la récupération
2. **Couche 1 (Intermédiaire):** Données d'authentification du client (chiffrées)
3. **Couche 2 (Interne):** Données LeaseSet2 proprement dites (chiffrées)

**Structure générale:**

```
Layer 0 data + Enc(layer 1 data + Enc(layer 2 data)) + Signature
```
**Important:** Le LS2 (format LeaseSet de seconde génération) chiffré utilise des clés aveuglées. La Destination (identité publique I2P) ne figure pas dans l'en-tête. L'emplacement de stockage dans la DHT est `SHA-256(sig type || blinded public key)`, avec rotation quotidienne.

### Couche 0 (Externe) - Texte en clair

La couche 0 n'utilise PAS l'en-tête LS2 standard. Elle utilise un format personnalisé optimisé pour les clés aveuglées.

**Structure:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Type</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Not in header, from DatabaseStore message field</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded Public Key Sig Type</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, always <code>0x000b</code> (Red25519 type 11)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded Public Key</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Red25519 blinded public key</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Published Timestamp</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, seconds since epoch (rolls over in 2106)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Expires</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, offset from published in seconds (max 65,535 &asymp; 18.2 hours)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Flags</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Bit flags (see below)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">[Optional] Transient Key Data</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Variable</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Present if flag bit&nbsp;0 is set</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">lenOuterCiphertext</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, length of outer ciphertext</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">outerCiphertext</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">lenOuterCiphertext</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted Layer&nbsp;1 data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Red25519 signature over all preceding data</td></tr>
  </tbody>
</table>
**Champ Flags (2 octets, bits 15-0):** - **Bit 0:** Indicateur de clés hors ligne   - `0` = Aucune clé hors ligne   - `1` = Clés hors ligne présentes (des données de clés éphémères suivent) - **Bits 1-15:** Réservés, doivent être à 0 pour une compatibilité future

**Données de clé éphémère (présent si le bit de drapeau 0 = 1):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Expires Timestamp</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, seconds since epoch</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Transient Sig Type</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, signature type</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Transient Signing Public Key</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Variable</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Length implied by signature type</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signed by blinded public key; covers expires timestamp, transient sig type, and transient public key</td></tr>
  </tbody>
</table>
**Vérification de la signature :** - **Sans clés hors ligne :** Vérifier avec une clé publique aveuglée - **Avec des clés hors ligne :** Vérifier avec une clé publique temporaire

La signature couvre toutes les données de Type à outerCiphertext (inclus).

### Couche 1 (Intermédiaire) - Autorisation du client

**Déchiffrement:** Voir la section [Chiffrement de la couche 1](#layer-1-encryption).

**Structure:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Flags</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Authorization flags (see below)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">[Optional] Auth Data</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Variable</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Present based on flags</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">innerCiphertext</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Variable</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted Layer&nbsp;2 data (remainder)</td></tr>
  </tbody>
</table>
**Champ Flags (1 octet, bits 7-0):** - **Bit 0:** Mode d'autorisation   - `0` = Aucune autorisation par client (tout le monde)   - `1` = Autorisation par client (section d'authentification suivante) - **Bits 3-1:** Schéma d'authentification (uniquement si bit 0 = 1)   - `000` = authentification client DH   - `001` = authentification client PSK   - Autres réservés - **Bits 7-4:** Non utilisés, doivent être 0

**Données d'autorisation client DH (flags = 0x01, bits 3-1 = 000):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ephemeralPublicKey</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Server's ephemeral X25519 public key</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">clients</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, number of client entries</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">authClient[]</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">40 bytes each</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Array of client authorization entries</td></tr>
  </tbody>
</table>
**Entrée authClient (40 octets):** - `clientID_i`: 8 octets - `clientCookie_i`: 32 octets (authCookie chiffré)

**Données d'autorisation du client PSK (clé pré-partagée) (flags = 0x03, bits 3-1 = 001):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">authSalt</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Salt for PSK key derivation</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">clients</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big endian, number of client entries</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">authClient[]</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">40 bytes each</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Array of client authorization entries</td></tr>
  </tbody>
</table>
**Entrée authClient (40 octets):** - `clientID_i`: 8 octets - `clientCookie_i`: 32 octets (authCookie chiffré)

### Couche 2 (interne) - Données du LeaseSet

**Déchiffrement :** Voir la section [Chiffrement de couche 2](#layer-2-encryption).

**Structure :**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Type</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>3</code> (LS2) or <code>7</code> (Meta LS2)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Variable</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Complete LeaseSet2 or MetaLeaseSet2</td></tr>
  </tbody>
</table>
La couche interne contient la structure LeaseSet2 (deuxième version de LeaseSet) complète, incluant : - en-tête LS2 - informations de bail - signature LS2

**Exigences de vérification :** Après déchiffrement, les implémentations doivent vérifier : 1. L'horodatage interne correspond à l'horodatage externe publié 2. L'expiration interne correspond à l'expiration externe 3. La signature LS2 (leaseSet v2) est valide 4. Les données de lease sont bien formées

**Références:** - [Spécification des structures communes](/docs/specs/common-structures/) - détails du format LeaseSet2 (jeu de baux version 2)

---

## Dérivation de la clé d'aveuglement

### Aperçu

I2P utilise un schéma d'aveuglement de clé additif basé sur Ed25519 et ZCash RedDSA. Les clés aveuglées sont renouvelées quotidiennement (à minuit UTC) afin d'assurer la confidentialité persistante (forward secrecy).

**Justification de la conception:**

I2P a explicitement choisi de NE PAS utiliser l’approche de l’annexe A.2 du document rend-spec-v3.txt de Tor. Selon la spécification :

> "Nous n'utilisons pas l'annexe A.2 de rend-spec-v3.txt de Tor, dont les objectifs de conception sont similaires, car ses clés publiques aveuglées peuvent être hors du sous-groupe d'ordre premier, avec des implications de sécurité inconnues."

L'aveuglement additif d'I2P garantit que les clés aveuglées restent dans le sous-groupe d'ordre premier de la courbe Ed25519.

### Définitions mathématiques

**Paramètres Ed25519:** - `B`: point de base Ed25519 (générateur) = `2^255 - 19` - `L`: ordre Ed25519 = `2^252 + 27742317777372353535851937790883648493`

**Variables clés:** - `A`: Clé publique de signature de 32 octets désaveuglée (dans la Destination) - `a`: Clé privée de signature de 32 octets désaveuglée - `A'`: Clé publique de signature de 32 octets aveuglée (utilisée dans le LeaseSet chiffré) - `a'`: Clé privée de signature de 32 octets aveuglée - `alpha`: Facteur d'aveuglement de 32 octets (secret)

**Fonctions utilitaires:**

#### LEOS2IP(x)

"Conversion d’une chaîne d’octets Little-Endian en entier"

Convertit un tableau d’octets en ordre little-endian en valeur entière.

#### H*(x)

"Hachage et réduction"

```
H*(x) = (LEOS2IP(SHA512(x))) mod L
```
Même opération que lors de la génération de clés Ed25519.

### Génération Alpha

**Rotation quotidienne:** Un nouvel alpha et des clés aveuglées DOIVENT être générés chaque jour à minuit UTC (00:00:00 UTC).

**GENERATE_ALPHA(destination, date, secret) Algorithme:**

```python
# Input parameters
A = destination's signing public key (32 bytes)
stA = signature type of A (2 bytes, big endian)
     # 0x0007 for Ed25519 or 0x000b for Red25519
stA' = signature type of blinded key A' (2 bytes, big endian) 
     # Always 0x000b (Red25519)
datestring = "YYYYMMDD" (8 bytes ASCII from current UTC date)
secret = optional UTF-8 encoded string (zero-length if not used)

# Computation
keydata = A || stA || stA'  # 36 bytes total
seed = HKDF(
    salt=H("I2PGenerateAlpha", keydata),
    ikm=datestring || secret,
    info="i2pblinding1",
    n=64
)

# Treat seed as 64-byte little-endian integer and reduce
alpha = seed mod L
```
**Paramètres vérifiés:** - Personnalisation du sel: `"I2PGenerateAlpha"` - Info HKDF: `"i2pblinding1"` - Sortie: 64 octets avant réduction - Distribution d'alpha: Identique à celle des clés privées Ed25519 après `mod L`

### Aveuglement de clé privée

**Algorithme BLIND_PRIVKEY(a, alpha):**

Pour le propriétaire de la destination qui publie le LeaseSet chiffré :

```python
# For Ed25519 private key (type 7)
if sigtype == 7:
    seed = destination's signing private key (32 bytes)
    a = left_half(SHA512(seed))  # 32 bytes
    a = clamp(a)  # Ed25519 clamping
    
# For Red25519 private key (type 11)
elif sigtype == 11:
    a = destination's signing private key (32 bytes)
    # No clamping for Red25519

# Additive blinding using scalar arithmetic
blinded_privkey = a' = (a + alpha) mod L

# Derive blinded public key
blinded_pubkey = A' = DERIVE_PUBLIC(a')
```
**Critique:** La réduction `mod L` est essentielle pour maintenir la relation algébrique correcte entre la clé privée et la clé publique.

### Aveuglement de clé publique

**Algorithme BLIND_PUBKEY(A, alpha):**

Pour les clients récupérant et vérifiant le LeaseSet chiffré :

```python
alpha = GENERATE_ALPHA(destination, date, secret)
A = destination's signing public key (32 bytes)

# Additive blinding using group elements (curve points)
blinded_pubkey = A' = A + DERIVE_PUBLIC(alpha)
```
**Équivalence mathématique :**

Les deux méthodes produisent des résultats identiques :

```
BLIND_PUBKEY(A, alpha) == DERIVE_PUBLIC(BLIND_PRIVKEY(a, alpha))
```
C’est parce que :

```
A' = A + [alpha]B
   = [a]B + [alpha]B
   = [a + alpha]B  (group operation)
   = DERIVE_PUBLIC(a + alpha mod L)
```
### Signature avec des clés aveuglées

**Signature de LeaseSet non aveuglé:**

Le LeaseSet non aveuglé (envoyé directement aux clients authentifiés) est signé avec : - Signature Ed25519 standard (type 7) ou Red25519 (type 11) - Clé privée de signature non aveuglée - Vérifiée avec la clé publique non aveuglée

**Avec des clés hors ligne:** - Signé par une clé privée transitoire désaveuglée - Vérifié avec une clé publique transitoire désaveuglée - Les deux doivent être de type 7 ou 11

**Signature d'un LeaseSet chiffré :**

La partie externe d'un LeaseSet chiffré utilise des signatures Red25519 avec des clés aveuglées.

**Algorithme de signature Red25519:**

```python
# Generate per-signature random nonce
T = CSRNG(80)  # 80 random bytes

# Calculate r (differs from Ed25519)
r = H*(T || blinded_pubkey || message)

# Rest is same as Ed25519
R = [r]B
S = (r + H(R || A' || message) * a') mod L
signature = R || S  # 64 bytes total
```
**Principales différences par rapport à Ed25519:** 1. Utilise 80 octets de données aléatoires `T` (et non le hachage de la clé privée) 2. Utilise directement la valeur de la clé publique (et non le hachage de la clé privée) 3. Chaque signature est unique, même pour le même message et la même clé

**Vérification:**

Identique à Ed25519 :

```python
# Parse signature
R = signature[0:32]
S = signature[32:64]

# Verify equation: [S]B = R + [H(R || A' || message)]A'
return [S]B == R + [H(R || A' || message)]A'
```
### Considérations de sécurité

**Distribution alpha:**

Pour des raisons de sécurité, alpha doit suivre la même distribution que les clés privées non aveuglées. Lors de l'aveuglement d'Ed25519 (type 7) en Red25519 (type 11), les distributions diffèrent légèrement.

**Recommandation :** Utilisez Red25519 (type 11) pour les clés à la fois désaveuglées et aveuglées afin de respecter les exigences de ZCash : "la combinaison d’une clé publique ré-aléatoirisée et de signature(s) produite(s) avec cette clé ne révèle pas la clé source de la ré-aléatoirisation."

**Prise en charge du type 7 :** Ed25519 est pris en charge pour assurer la rétrocompatibilité avec les destinations existantes, mais le type 11 est recommandé pour les nouvelles destinations chiffrées.

**Avantages de la rotation quotidienne :** - Confidentialité persistante (PFS) : La compromission de la clé aveuglée d'aujourd'hui ne révèle pas celle d'hier - Non-corrélabilité : La rotation quotidienne empêche le suivi à long terme via la DHT (table de hachage distribuée) - Séparation des clés : Des clés différentes pour des périodes distinctes

**Références :** - [Spécification du protocole ZCash](https://zips.z.cash/protocol/protocol.pdf) - Section 5.4.6.1 - [Discussion Tor sur le Key Blinding (aveuglement de clé)](https://lists.torproject.org/pipermail/tor-dev/2013-December/005943.html) - [Ticket Tor n° 8106](https://trac.torproject.org/projects/tor/ticket/8106)

---

## Chiffrement et traitement

### Dérivation du Subcredential (élément d'identification dérivé)

Avant le chiffrement, nous dérivons un credential (valeur d'authentification) et un subcredential (sous-valeur d'authentification) afin d'associer les couches chiffrées à la connaissance de la clé publique de signature de la Destination.

**Objectif:** Garantir que seuls ceux qui connaissent la clé publique de signature de la Destination (identifiant de service I2P) peuvent déchiffrer le LeaseSet chiffré. La Destination complète n'est pas nécessaire.

#### Calcul des informations d'identification

```python
A = destination's signing public key (32 bytes)
stA = signature type of A (2 bytes big endian)
     # 0x0007 for Ed25519 or 0x000b for Red25519
stA' = signature type of blinded key A' (2 bytes big endian)
     # Always 0x000b (Red25519)

keydata = A || stA || stA'  # 36 bytes

credential = H("credential", keydata)  # 32 bytes
```
**Séparation de domaines:** La chaîne de personnalisation `"credential"` garantit que ce hachage n'entre pas en collision avec les clés de recherche de la DHT ni avec d'autres usages du protocole.

#### Calcul du Subcredential (identifiant dérivé)

```python
blindedPublicKey = A' (32 bytes, from blinding process)

subcredential = H("subcredential", credential || blindedPublicKey)  # 32 bytes
```
**Objectif:** Le subcredential (identifiant secondaire) lie le LeaseSet chiffré à: 1. La Destination spécifique (via l’identifiant) 2. La clé aveuglée spécifique (via blindedPublicKey) 3. Le jour spécifique (via la rotation quotidienne de blindedPublicKey)

Cela empêche les attaques par rejeu et les recoupements d'un jour à l'autre.

### Chiffrement de la couche 1

**Contexte :** La couche 1 contient des données d’autorisation du client et est chiffrée à l’aide d’une clé dérivée du subcredential (sous‑identifiant d’authentification).

#### Algorithme de chiffrement

```python
# Prepare input
outerInput = subcredential || publishedTimestamp
# publishedTimestamp: 4 bytes from Layer 0

# Generate random salt
outerSalt = CSRNG(32)  # 32 bytes

# Derive encryption key and IV
keys = HKDF(
    salt=outerSalt,
    ikm=outerInput,
    info="ELS2_L1K",  # Domain separation
    n=44  # 32 bytes key + 12 bytes IV
)

outerKey = keys[0:31]    # 32 bytes (indices 0-31 inclusive)
outerIV = keys[32:43]    # 12 bytes (indices 32-43 inclusive)

# Encrypt and prepend salt
outerPlaintext = [Layer 1 data]
outerCiphertext = outerSalt || ENCRYPT(outerKey, outerIV, outerPlaintext)
```
**Sortie:** `outerCiphertext` est de `32 + len(outerPlaintext)` octets.

**Propriétés de sécurité:** - Le sel garantit des paires clé/IV uniques, même pour le même subcredential (sous-identifiant d’authentification) - La chaîne de contexte `"ELS2_L1K"` assure une séparation des domaines - ChaCha20 assure une sécurité sémantique (texte chiffré indiscernable du hasard)

#### Algorithme de déchiffrement

```python
# Parse salt from ciphertext
outerSalt = outerCiphertext[0:31]  # First 32 bytes

# Derive decryption key and IV (same process as encryption)
outerInput = subcredential || publishedTimestamp
keys = HKDF(
    salt=outerSalt,
    ikm=outerInput,
    info="ELS2_L1K",
    n=44
)

outerKey = keys[0:31]    # 32 bytes
outerIV = keys[32:43]    # 12 bytes

# Decrypt (skip salt bytes)
outerPlaintext = DECRYPT(outerKey, outerIV, outerCiphertext[32:end])
```
**Vérification:** Après déchiffrement, vérifiez que la structure de la couche 1 est bien formée avant de passer à la couche 2.

### Chiffrement de la couche 2

**Contexte:** La couche 2 contient les données LeaseSet2 proprement dites et est chiffrée avec une clé dérivée d'authCookie (si l'authentification par client est activée) ou de la chaîne vide (sinon).

#### Algorithme de chiffrement

```python
# Determine authCookie based on authorization mode
if per_client_auth_enabled:
    authCookie = [32-byte cookie from client authorization process]
else:
    authCookie = b''  # Zero-length byte array

# Prepare input
innerInput = authCookie || subcredential || publishedTimestamp

# Generate random salt
innerSalt = CSRNG(32)  # 32 bytes

# Derive encryption key and IV
keys = HKDF(
    salt=innerSalt,
    ikm=innerInput,
    info="ELS2_L2K",  # Domain separation
    n=44  # 32 bytes key + 12 bytes IV
)

innerKey = keys[0:31]    # 32 bytes
innerIV = keys[32:43]    # 12 bytes

# Encrypt and prepend salt
innerPlaintext = [Layer 2 data: LS2 type byte + LeaseSet2 data]
innerCiphertext = innerSalt || ENCRYPT(innerKey, innerIV, innerPlaintext)
```
**Sortie :** `innerCiphertext` fait `32 + len(innerPlaintext)` octets.

**Liaison de clé:** - Si aucune authentification client : Associée uniquement à subcredential (sous-jeton d’authentification) et à l’horodatage - Si l’authentification client est activée : Associée en plus à authCookie (différent pour chaque client autorisé)

#### Algorithme de déchiffrement

```python
# Determine authCookie (same as encryption)
if per_client_auth_enabled:
    authCookie = [32-byte cookie from client authorization process]
else:
    authCookie = b''  # Zero-length byte array

# Parse salt from ciphertext
innerSalt = innerCiphertext[0:31]  # First 32 bytes

# Derive decryption key and IV
innerInput = authCookie || subcredential || publishedTimestamp
keys = HKDF(
    salt=innerSalt,
    ikm=innerInput,
    info="ELS2_L2K",
    n=44
)

innerKey = keys[0:31]    # 32 bytes
innerIV = keys[32:43]    # 12 bytes

# Decrypt (skip salt bytes)
innerPlaintext = DECRYPT(innerKey, innerIV, innerCiphertext[32:end])
```
**Vérification :** Après déchiffrement : 1. Vérifier que l’octet de type LS2 est valide (3 ou 7) 2. Analyser la structure LeaseSet2 (deuxième génération de LeaseSet) 3. Vérifier que l’horodatage interne correspond à l’horodatage externe publié 4. Vérifier que l’expiration interne correspond à l’expiration externe 5. Vérifier la signature de LeaseSet2

### Résumé de la couche de chiffrement

```
┌─────────────────────────────────────────────────┐
│ Layer 0 (Plaintext)                             │
│ - Blinded public key                            │
│ - Timestamps                                    │
│ - Signature                                     │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │ Layer 1 (Encrypted with subcredential)  │   │
│  │ - Authorization flags                   │   │
│  │ - Client auth data (if enabled)         │   │
│  │                                          │   │
│  │  ┌────────────────────────────────┐     │   │
│  │  │ Layer 2 (Encrypted with        │     │   │
│  │  │          authCookie + subcred) │     │   │
│  │  │ - LeaseSet2 type               │     │   │
│  │  │ - LeaseSet2 data               │     │   │
│  │  │ - Leases                       │     │   │
│  │  │ - LS2 signature                │     │   │
│  │  └────────────────────────────────┘     │   │
│  └─────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```
**Flux de déchiffrement :** 1. Vérifier la signature de la couche 0 avec la clé publique aveuglée 2. Déchiffrer la couche 1 à l'aide de subcredential (justificatif dérivé) 3. Traiter les données d'autorisation (si présentes) pour obtenir authCookie (jeton d'authentification) 4. Déchiffrer la couche 2 en utilisant authCookie et subcredential 5. Vérifier et analyser LeaseSet2

---

## Autorisation par client

### Vue d'ensemble

Lorsque l’autorisation par client est activée, le serveur conserve une liste de clients autorisés. Chaque client dispose de données de clé qui doivent être transmises de manière sécurisée par un canal hors bande.

**Deux mécanismes d’autorisation :** 1. **Autorisation client DH (Diffie-Hellman):** Plus sécurisé, utilise l’accord de clé X25519 2. **Autorisation PSK (clé pré-partagée):** Plus simple, utilise des clés symétriques

**Propriétés de sécurité courantes :** - Confidentialité de l’appartenance des clients : Les observateurs voient le nombre de clients mais ne peuvent pas identifier de clients spécifiques - Ajout/révocation de clients de façon anonyme : Impossible de déterminer quand des clients spécifiques sont ajoutés ou retirés - Probabilité de collision d’un identifiant client sur 8 octets : ~1 sur 18 milliards de milliards (négligeable)

### Autorisation du client via DH (échange de clés Diffie–Hellman)

**Aperçu:** Chaque client génère une paire de clés X25519 et envoie sa clé publique au serveur via un canal hors bande sécurisé. Le serveur utilise un Diffie-Hellman éphémère pour chiffrer un authCookie unique pour chaque client.

#### Génération des clés client

```python
# Client generates keypair
csk_i = GENERATE_PRIVATE()  # 32-byte X25519 private key
cpk_i = DERIVE_PUBLIC(csk_i)  # 32-byte X25519 public key

# Client sends cpk_i to server via secure out-of-band channel
# Client KEEPS csk_i secret (never transmitted)
```
**Avantage de sécurité :** La clé privée du client ne quitte jamais son appareil. Un adversaire qui intercepte la transmission hors bande ne peut pas déchiffrer de futurs LeaseSets chiffrés sans casser X25519 DH (échange de clés Diffie-Hellman X25519).

#### Traitement côté serveur

```python
# Server generates new auth cookie and ephemeral keypair
authCookie = CSRNG(32)  # 32-byte cookie

esk = GENERATE_PRIVATE()  # 32-byte ephemeral private key
epk = DERIVE_PUBLIC(esk)  # 32-byte ephemeral public key

# For each authorized client i
for cpk_i in authorized_clients:
    # Perform DH key agreement
    sharedSecret = DH(esk, cpk_i)  # 32 bytes
    
    # Derive client-specific encryption key
    authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp
    okm = HKDF(
        salt=epk,  # Ephemeral public key as salt
        ikm=authInput,
        info="ELS2_XCA",  # Domain separation
        n=52  # 32 key + 12 IV + 8 ID
    )
    
    # Extract components
    clientKey_i = okm[0:31]    # 32 bytes
    clientIV_i = okm[32:43]    # 12 bytes
    clientID_i = okm[44:51]    # 8 bytes
    
    # Encrypt authCookie for this client
    clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
    
    # Store [clientID_i, clientCookie_i] entry in Layer 1
```
**Structure de données de la couche 1:**

```
ephemeralPublicKey (32 bytes)
clients (2 bytes) = N
[clientID_1 (8 bytes) || clientCookie_1 (32 bytes)]
[clientID_2 (8 bytes) || clientCookie_2 (32 bytes)]
...
[clientID_N (8 bytes) || clientCookie_N (32 bytes)]
```
**Recommandations serveur:** - Générer une nouvelle paire de clés éphémère pour chaque LeaseSet chiffré publié - Randomiser l'ordre des clients pour empêcher le suivi basé sur la position - Envisager d'ajouter des entrées factices pour masquer le nombre réel de clients

#### Traitement côté client

```python
# Client has: csk_i (their private key), destination, date, secret
# Client receives: encrypted LeaseSet with epk in Layer 1

# Perform DH key agreement with server's ephemeral public key
sharedSecret = DH(csk_i, epk)  # 32 bytes

# Derive expected client identifier and decryption key
cpk_i = DERIVE_PUBLIC(csk_i)  # Client's own public key
authInput = sharedSecret || cpk_i || subcredential || publishedTimestamp

okm = HKDF(
    salt=epk,
    ikm=authInput,
    info="ELS2_XCA",
    n=52
)

clientKey_i = okm[0:31]    # 32 bytes
clientIV_i = okm[32:43]    # 12 bytes
clientID_i = okm[44:51]    # 8 bytes

# Search Layer 1 authorization data for clientID_i
for (clientID, clientCookie) in layer1_auth_entries:
    if clientID == clientID_i:
        # Found matching entry, decrypt authCookie
        authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie)
        # Use authCookie to decrypt Layer 2
        break
else:
    # No matching entry - client not authorized or revoked
    raise AuthorizationError("Client not authorized")
```
**Gestion des erreurs côté client:** - Si `clientID_i` est introuvable : le client a été révoqué ou n'a jamais été autorisé - Si le déchiffrement échoue : données corrompues ou clés incorrectes (extrêmement rare) - Les clients devraient réinterroger périodiquement pour détecter une révocation

### Autorisation du client par PSK

**Vue d'ensemble :** Chaque client possède une clé symétrique de 32 octets pré-partagée (PSK). Le serveur chiffre le même authCookie à l'aide de la PSK de chaque client.

#### Génération de clés

```python
# Option 1: Client generates key
psk_i = CSRNG(32)  # 32-byte pre-shared key
# Client sends psk_i to server via secure out-of-band channel

# Option 2: Server generates key
psk_i = CSRNG(32)  # 32-byte pre-shared key
# Server sends psk_i to one or more clients via secure out-of-band channel
```
**Note de sécurité:** Le même PSK (clé pré-partagée) peut être partagé entre plusieurs clients si désiré (crée une autorisation de type "groupe").

#### Traitement côté serveur

```python
# Server generates new auth cookie and salt
authCookie = CSRNG(32)  # 32-byte cookie
authSalt = CSRNG(32)     # 32-byte salt

# For each authorized client i
for psk_i in authorized_clients:
    # Derive client-specific encryption key
    authInput = psk_i || subcredential || publishedTimestamp
    
    okm = HKDF(
        salt=authSalt,
        ikm=authInput,
        info="ELS2PSKA",  # Domain separation
        n=52  # 32 key + 12 IV + 8 ID
    )
    
    # Extract components
    clientKey_i = okm[0:31]    # 32 bytes
    clientIV_i = okm[32:43]    # 12 bytes
    clientID_i = okm[44:51]    # 8 bytes
    
    # Encrypt authCookie for this client
    clientCookie_i = ENCRYPT(clientKey_i, clientIV_i, authCookie)
    
    # Store [clientID_i, clientCookie_i] entry in Layer 1
```
**Structure de données de la couche 1:**

```
authSalt (32 bytes)
clients (2 bytes) = N
[clientID_1 (8 bytes) || clientCookie_1 (32 bytes)]
[clientID_2 (8 bytes) || clientCookie_2 (32 bytes)]
...
[clientID_N (8 bytes) || clientCookie_N (32 bytes)]
```
#### Traitement côté client

```python
# Client has: psk_i (their pre-shared key), destination, date, secret
# Client receives: encrypted LeaseSet with authSalt in Layer 1

# Derive expected client identifier and decryption key
authInput = psk_i || subcredential || publishedTimestamp

okm = HKDF(
    salt=authSalt,
    ikm=authInput,
    info="ELS2PSKA",
    n=52
)

clientKey_i = okm[0:31]    # 32 bytes
clientIV_i = okm[32:43]    # 12 bytes
clientID_i = okm[44:51]    # 8 bytes

# Search Layer 1 authorization data for clientID_i
for (clientID, clientCookie) in layer1_auth_entries:
    if clientID == clientID_i:
        # Found matching entry, decrypt authCookie
        authCookie = DECRYPT(clientKey_i, clientIV_i, clientCookie)
        # Use authCookie to decrypt Layer 2
        break
else:
    # No matching entry - client not authorized or revoked
    raise AuthorizationError("Client not authorized")
```
### Comparaison et recommandations

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">DH Authorization</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">PSK Authorization</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Key Exchange</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Asymmetric (X25519)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Symmetric (shared secret)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Security</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Higher (forward secrecy)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Lower (depends on PSK secrecy)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Client Privacy</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Private key never transmitted</td><td style="border:1px solid var(--color-border); padding:0.5rem;">PSK must be transmitted securely</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Performance</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">N+1 DH operations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">No DH operations</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Key Sharing</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">One key per client</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Can share key among multiple clients</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Revocation Detection</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Adversary cannot tell when revoked</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Adversary can track revocation if PSK intercepted</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Use Case</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">High security requirements</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Performance-critical or group access</td></tr>
  </tbody>
</table>
**Recommandation:** - **Utilisez l’autorisation DH** pour des applications hautement sécurisées où la forward secrecy (confidentialité persistante) est importante - **Utilisez l’autorisation PSK** lorsque les performances sont critiques ou lors de la gestion de groupes de clients - **Ne réutilisez jamais les PSK** entre différents services ou périodes - **Utilisez toujours des canaux sécurisés** pour la distribution des clés (p. ex., Signal, OTR, PGP)

### Considérations de sécurité

**Confidentialité de l'appartenance des clients:**

Les deux mécanismes assurent la confidentialité de l’appartenance des clients grâce à : 1. **Identifiants client chiffrés :** clientID de 8 octets dérivé de la sortie de HKDF 2. **Cookies indiscernables :** tous les clientCookie de 32 octets semblent aléatoires 3. **Aucune métadonnée spécifique à un client :** aucun moyen d’identifier quelle entrée appartient à quel client

Un observateur peut voir : - Nombre de clients autorisés (d'après le champ `clients`) - Évolution du nombre de clients au fil du temps

Un observateur NE PEUT PAS voir: - Quels clients spécifiques sont autorisés - Quand des clients spécifiques sont ajoutés ou supprimés (si le nombre reste inchangé) - Toute information permettant d’identifier un client

**Recommandations de randomisation :**

Les serveurs DEVRAIENT mélanger aléatoirement l’ordre des clients chaque fois qu’ils génèrent un LeaseSet chiffré :

```python
import random

# Before serializing
auth_entries = [(clientID_i, clientCookie_i) for each client]
random.shuffle(auth_entries)
# Now serialize in randomized order
```
**Avantages :** - Empêche les clients de connaître leur position dans la liste - Empêche les attaques d'inférence basées sur des changements de position - Rend indiscernables l'ajout et la révocation de clients

**Masquer le nombre de clients:**

Les serveurs PEUVENT insérer des entrées factices aléatoires :

```python
# Add dummy entries
num_dummies = random.randint(0, max_dummies)
for _ in range(num_dummies):
    dummy_id = CSRNG(8)
    dummy_cookie = CSRNG(32)
    auth_entries.append((dummy_id, dummy_cookie))

# Randomize all entries (real + dummy)
random.shuffle(auth_entries)
```
**Coût:** Les entrées factices augmentent la taille du LeaseSet chiffré (40 octets chacune).

**Rotation d'AuthCookie (cookie d'authentification):**

Les serveurs devraient générer un nouvel authCookie: - Chaque fois qu'un LeaseSet chiffré est publié (toutes les quelques heures, en général) - Immédiatement après la révocation d'un client - Selon un calendrier régulier (p. ex., quotidien), même si aucun client ne change

**Avantages:** - Limite l'exposition si authCookie est compromis - Garantit que les clients révoqués perdent rapidement l'accès - Fournit la confidentialité persistante pour la couche 2

---

## Adressage en Base32 pour les LeaseSets chiffrés (ensembles de baux)

### Vue d'ensemble

Les adresses I2P en base32 traditionnelles ne contiennent que le hachage de la Destination (32 octets → 52 caractères). Cela est insuffisant pour les LeaseSets chiffrés, car :

1. Les clients ont besoin de la **clé publique non aveuglée** pour dériver la clé publique aveuglée
2. Les clients ont besoin des **types de signature** (non aveuglée et aveuglée) pour une dérivation correcte des clés
3. Le hachage seul ne fournit pas ces informations

**Solution :** Un nouveau format base32 qui inclut les types de clé publique et de signature.

### Spécification du format d'adresse

**Structure décodée (35 octets):**

```
┌─────────────────────────────────────────────────────┐
│ Byte 0   │ Byte 1  │ Byte 2  │ Bytes 3-34          │
│ Flags    │ Unblind │ Blinded │ Public Key          │
│ (XOR)    │ SigType │ SigType │ (32 bytes)          │
│          │ (XOR)   │ (XOR)   │                     │
└─────────────────────────────────────────────────────┘
```
**Les 3 premiers octets (XOR avec la somme de contrôle):**

Les 3 premiers octets contiennent des métadonnées combinées par XOR (ou exclusif) avec des portions d'une somme de contrôle CRC-32 :

```python
# Data structure before XOR
flags = 0x00           # 1 byte (reserved for future use)
unblinded_sigtype = 0x07 or 0x0b  # 1 byte (7 or 11)
blinded_sigtype = 0x0b  # 1 byte (always 11)

# Compute CRC-32 checksum of public key
checksum = crc32(pubkey)  # 4-byte CRC-32 of bytes 3-34

# XOR first 3 bytes with parts of checksum
data[0] = flags XOR (checksum >> 24) & 0xFF
data[1] = unblinded_sigtype XOR (checksum >> 16) & 0xFF  
data[2] = blinded_sigtype XOR (checksum >> 8) & 0xFF

# Bytes 3-34 contain the unmodified 32-byte public key
data[3:34] = pubkey
```
**Propriétés de la somme de contrôle :** - Utilise le polynôme CRC-32 standard - Taux de faux négatifs : ~1 sur 16 millions - Permet de détecter les erreurs de frappe dans les adresses - Ne peut pas être utilisé pour l'authentification (non sécurisé cryptographiquement)

**Format encodé:**

```
Base32Encode(35 bytes) || ".b32.i2p"
```
**Caractéristiques:** - Nombre total de caractères: 56 (35 octets × 8 bits ÷ 5 bits par caractère) - Suffixe: ".b32.i2p" (identique à la base32 traditionnelle) - Longueur totale: 56 + 8 = 64 caractères (sans le terminateur nul)

**Encodage Base32:** - Alphabet: `abcdefghijklmnopqrstuvwxyz234567` (standard RFC 4648) - 5 bits inutilisés à la fin DOIVENT être à 0 - Insensible à la casse (par convention en minuscules)

### Génération d'adresses

```python
import struct
from zlib import crc32
import base64

def generate_encrypted_b32_address(pubkey, unblinded_sigtype, blinded_sigtype):
    """
    Generate base32 address for encrypted LeaseSet.
    
    Args:
        pubkey: 32-byte public key (bytes)
        unblinded_sigtype: Unblinded signature type (7 or 11)
        blinded_sigtype: Blinded signature type (always 11)
    
    Returns:
        String address ending in .b32.i2p
    """
    # Verify inputs
    assert len(pubkey) == 32, "Public key must be 32 bytes"
    assert unblinded_sigtype in [7, 11], "Unblinded sigtype must be 7 or 11"
    assert blinded_sigtype == 11, "Blinded sigtype must be 11"
    
    # Compute CRC-32 of public key
    checksum = crc32(pubkey) & 0xFFFFFFFF  # Ensure 32-bit unsigned
    
    # Prepare metadata bytes
    flags = 0x00
    
    # XOR metadata with checksum parts
    byte0 = flags ^ ((checksum >> 24) & 0xFF)
    byte1 = unblinded_sigtype ^ ((checksum >> 16) & 0xFF)
    byte2 = blinded_sigtype ^ ((checksum >> 8) & 0xFF)
    
    # Construct 35-byte data
    data = bytes([byte0, byte1, byte2]) + pubkey
    
    # Base32 encode (standard alphabet)
    # Python's base64 module uses uppercase by default
    b32 = base64.b32encode(data).decode('ascii').lower().rstrip('=')
    
    # Construct full address
    address = b32 + ".b32.i2p"
    
    return address
```
### Analyse syntaxique des adresses

```python
import struct
from zlib import crc32
import base64

def parse_encrypted_b32_address(address):
    """
    Parse base32 address for encrypted LeaseSet.
    
    Args:
        address: String address ending in .b32.i2p
    
    Returns:
        Tuple of (pubkey, unblinded_sigtype, blinded_sigtype)
    
    Raises:
        ValueError: If address is invalid or checksum fails
    """
    # Remove suffix
    if not address.endswith('.b32.i2p'):
        raise ValueError("Invalid address suffix")
    
    b32 = address[:-8]  # Remove ".b32.i2p"
    
    # Verify length (56 characters for 35 bytes)
    if len(b32) != 56:
        raise ValueError(f"Invalid length: {len(b32)} (expected 56)")
    
    # Base32 decode
    # Add padding if needed
    padding_needed = (8 - (len(b32) % 8)) % 8
    b32_padded = b32.upper() + '=' * padding_needed
    
    try:
        data = base64.b32decode(b32_padded)
    except Exception as e:
        raise ValueError(f"Invalid base32 encoding: {e}")
    
    # Verify decoded length
    if len(data) != 35:
        raise ValueError(f"Invalid decoded length: {len(data)} (expected 35)")
    
    # Extract public key
    pubkey = data[3:35]
    
    # Compute CRC-32 for verification
    checksum = crc32(pubkey) & 0xFFFFFFFF
    
    # Un-XOR metadata bytes
    flags = data[0] ^ ((checksum >> 24) & 0xFF)
    unblinded_sigtype = data[1] ^ ((checksum >> 16) & 0xFF)
    blinded_sigtype = data[2] ^ ((checksum >> 8) & 0xFF)
    
    # Verify expected values
    if flags != 0x00:
        raise ValueError(f"Invalid flags: {flags:#x} (expected 0x00)")
    
    if unblinded_sigtype not in [7, 11]:
        raise ValueError(f"Invalid unblinded sigtype: {unblinded_sigtype} (expected 7 or 11)")
    
    if blinded_sigtype != 11:
        raise ValueError(f"Invalid blinded sigtype: {blinded_sigtype} (expected 11)")
    
    return pubkey, unblinded_sigtype, blinded_sigtype
```
### Comparaison avec le Base32 traditionnel

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Traditional B32</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Encrypted LS2 B32</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Content</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-256 hash of Destination</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Public key + signature types</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Decoded Size</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">35 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Encoded Length</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">52 characters</td><td style="border:1px solid var(--color-border); padding:0.5rem;">56 characters</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Suffix</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">.b32.i2p</td><td style="border:1px solid var(--color-border); padding:0.5rem;">.b32.i2p</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Total Length</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">60 chars</td><td style="border:1px solid var(--color-border); padding:0.5rem;">64 chars</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Checksum</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">None</td><td style="border:1px solid var(--color-border); padding:0.5rem;">CRC-32 (XOR'd into first 3 bytes)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Use Case</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Regular destinations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted LeaseSet destinations</td></tr>
  </tbody>
</table>
### Restrictions d'utilisation

**Incompatibilité avec BitTorrent:**

Les adresses LS2 chiffrées NE PEUVENT PAS être utilisées avec les réponses d’annonce compactes de BitTorrent :

```
Compact announce reply format:
┌────────────────────────────┐
│ 32-byte destination hash   │  ← Only hash, no signature types
│ 2-byte port                │
└────────────────────────────┘
```
**Problème:** Le format compact ne contient que le hachage (32 octets), sans espace pour les types de signature ni les informations de clé publique.

**Solution :** Utilisez des réponses d'annonce complètes ou des trackers basés sur HTTP qui prennent en charge les adresses complètes.

### Intégration du carnet d’adresses

Si un client dispose de la Destination complète (identifiant cryptographique I2P) dans un carnet d’adresses :

1. Stocker la Destination complète (identité I2P) (inclut la clé publique)
2. Prendre en charge la recherche inverse par hachage
3. Lorsqu'un LS2 (LeaseSet version 2) chiffré est rencontré, récupérer la clé publique depuis le carnet d'adresses
4. Pas besoin d'un nouveau format base32 si la Destination complète est déjà connue

**Formats de carnet d’adresses qui prennent en charge LS2 (LeaseSet2, nouvelle version de leaseSet) chiffré:** - hosts.txt avec des chaînes de destination complètes - bases de données SQLite avec colonne de destination - formats JSON/XML avec des données de destination complètes

### Exemples d'implémentation

**Exemple 1 : Générer une adresse**

```python
# Ed25519 destination example
pubkey = bytes.fromhex('a' * 64)  # 32-byte public key
unblinded_type = 7   # Ed25519
blinded_type = 11    # Red25519 (always)

address = generate_encrypted_b32_address(pubkey, unblinded_type, blinded_type)
print(f"Address: {address}")
# Output: 56 base32 characters + .b32.i2p
```
**Exemple 2: Analyser et valider**

```python
address = "abc...xyz.b32.i2p"  # 56 chars + suffix

try:
    pubkey, unblinded, blinded = parse_encrypted_b32_address(address)
    print(f"Public Key: {pubkey.hex()}")
    print(f"Unblinded SigType: {unblinded}")
    print(f"Blinded SigType: {blinded}")
except ValueError as e:
    print(f"Invalid address: {e}")
```
**Exemple 3 : Conversion depuis une Destination (identité publique I2P)**

```python
def destination_to_encrypted_b32(destination):
    """
    Convert full Destination to encrypted LS2 base32 address.
    
    Args:
        destination: I2P Destination object
    
    Returns:
        Base32 address string
    """
    # Extract public key and signature type from destination
    pubkey = destination.signing_public_key  # 32 bytes
    sigtype = destination.sig_type  # 7 or 11
    
    # Blinded type is always 11 (Red25519)
    blinded_type = 11
    
    # Generate address
    return generate_encrypted_b32_address(pubkey, sigtype, blinded_type)
```
### Considérations de sécurité

**Confidentialité:** - L'adresse Base32 révèle la clé publique - C'est intentionnel et requis par le protocole - Ne révèle PAS la clé privée et ne compromet pas la sécurité - Les clés publiques sont, par conception, des informations publiques

**Résistance aux collisions:** - CRC-32 n'offre que 32 bits de résistance aux collisions - Non sécurisé cryptographiquement (à utiliser uniquement pour la détection d'erreurs) - Ne PAS s’appuyer sur la somme de contrôle pour l’authentification - Une vérification complète de la destination reste nécessaire

**Validation d'adresse:** - Toujours valider la somme de contrôle avant utilisation - Rejeter les adresses avec des types de signature invalides - Vérifier que la clé publique est sur la courbe (spécifique à l'implémentation)

**Références:** - [Proposition 149 : B32 pour LS2 chiffré](/proposals/149-b32-encrypted-ls2/) - [Spécification d'adressage B32](/docs/specs/b32-for-encrypted-leasesets/) - [Spécification de nommage I2P](/docs/overview/naming/)

---

## Prise en charge des clés hors ligne

### Aperçu

Les clés hors ligne permettent à la clé de signature principale de rester hors ligne (stockage à froid) tandis qu'une clé de signature éphémère est utilisée pour les opérations quotidiennes. Cela est essentiel pour les services à haute sécurité.

**Exigences spécifiques pour LS2 chiffré:** - Les clés éphémères doivent être générées hors ligne - Les clés privées aveuglées doivent être pré-générées (une par jour) - Les clés, qu’elles soient éphémères ou aveuglées, sont fournies par lots - Aucun format de fichier standardisé n’est encore défini (à faire dans la spécification)

### Structure de la clé hors ligne

**Données de clé éphémère de la couche 0 (lorsque le bit de drapeau 0 = 1) :**

```
┌───────────────────────────────────────────────────┐
│ Expires Timestamp       │ 4 bytes (seconds)       │
│ Transient Sig Type      │ 2 bytes (big endian)    │
│ Transient Signing Pubkey│ Variable (sigtype len)  │
│ Signature (by blinded)  │ 64 bytes (Red25519)     │
└───────────────────────────────────────────────────┘
```
**Portée de la signature:** La signature dans le bloc de clé hors ligne couvre : - Horodatage d’expiration (4 octets) - Type de signature temporaire (2 octets)   - Clé publique de signature temporaire (variable)

Cette signature est vérifiée à l'aide de la **clé publique aveuglée**, prouvant que l'entité détenant la clé privée aveuglée a autorisé cette clé éphémère.

### Processus de génération de clés

**Pour un LeaseSet chiffré avec des clés hors ligne:**

1. **Générer des paires de clés éphémères** (hors ligne, en stockage à froid):
   ```python
   # For each day in future
   for date in future_dates:
       # Generate daily transient keypair
       transient_privkey = generate_red25519_privkey()  # Type 11
       transient_pubkey = derive_public(transient_privkey)

       # Store for later delivery
       keys[date] = (transient_privkey, transient_pubkey)
   ```

2. **Generate daily blinded keypairs** (offline, in cold storage):
   ```python
# Pour chaque jour    for date in future_dates:

       # Derive alpha for this date
       datestring = date.strftime("%Y%m%d")  # "YYYYMMDD"
       alpha = GENERATE_ALPHA(destination, datestring, secret)
       
       # Blind the signing private key
       a = destination_signing_privkey  # Type 7 or 11
       blinded_privkey = BLIND_PRIVKEY(a, alpha)  # Result is type 11
       blinded_pubkey = DERIVE_PUBLIC(blinded_privkey)
       
       # Store for later delivery
       blinded_keys[date] = (blinded_privkey, blinded_pubkey)
   ```

3. **Sign transient keys with blinded keys** (offline):
   ```python
for date in future_dates:

       transient_pubkey = keys[date][1]
       blinded_privkey = blinded_keys[date][0]
       
       # Create signature data
       expires = int((date + timedelta(days=1)).timestamp())
       sig_data = struct.pack('>I', expires)  # 4 bytes
       sig_data += struct.pack('>H', 11)     # Transient type (Red25519)
       sig_data += transient_pubkey          # 32 bytes
       
       # Sign with blinded private key
       signature = RED25519_SIGN(blinded_privkey, sig_data)
       
       # Package for delivery
       offline_sig_blocks[date] = {
           'expires': expires,
           'transient_type': 11,
           'transient_pubkey': transient_pubkey,
           'signature': signature
       }
   ```

4. **Package for delivery to router:**
   ```python
# Pour chaque date    delivery_package[date] = {

       'transient_privkey': keys[date][0],
       'transient_pubkey': keys[date][1],
       'blinded_privkey': blinded_keys[date][0],
       'blinded_pubkey': blinded_keys[date][1],
       'offline_sig_block': offline_sig_blocks[date]
}

   ```

### Router Usage

**Daily Key Loading:**

```python
# À minuit UTC (ou avant publication)

date = datetime.utcnow().date()

# Charger les clés du jour

today_keys = load_delivery_package(date)

transient_privkey = today_keys['transient_privkey'] transient_pubkey = today_keys['transient_pubkey'] blinded_privkey = today_keys['blinded_privkey'] blinded_pubkey = today_keys['blinded_pubkey'] offline_sig_block = today_keys['offline_sig_block']

# Utilisez ces clés pour le LeaseSet (ensemble de baux) chiffré d'aujourd'hui

```

**Publishing Process:**

```python
# 1. Créer un LeaseSet2 interne

inner_ls2 = create_leaseset2(

    destinations, leases, expires, 
    signing_key=transient_privkey  # Use transient key
)

# 2. Chiffrer la couche 2

layer2_ciphertext = encrypt_layer2(inner_ls2, authCookie, subcredential, timestamp)

# 3. Créer la couche 1 avec des données d’autorisation

layer1_plaintext = create_layer1(authorization_data, layer2_ciphertext)

# 4. Chiffrer la couche 1

layer1_ciphertext = encrypt_layer1(layer1_plaintext, subcredential, timestamp)

# 5. Créer la couche 0 avec un bloc de signature hors ligne

layer0 = create_layer0(

    blinded_pubkey,
    timestamp,
    expires,
    flags=0x0001,  # Bit 0 set (offline keys present)
    offline_sig_block=offline_sig_block,
    layer1_ciphertext=layer1_ciphertext
)

# 6. Signer la couche 0 avec une clé privée éphémère

signature = RED25519_SIGN(transient_privkey, layer0)

# 7. Ajouter la signature et publier

encrypted_leaseset = layer0 + signature publish_to_netdb(encrypted_leaseset)

```

### Security Considerations

**Tracking via Offline Signature Block:**

The offline signature block is in plaintext (Layer 0). An adversary scraping floodfills could:
- Track the same encrypted LeaseSet across multiple days
- Correlate encrypted LeaseSets even though blinded keys change daily

**Mitigation:** Generate new transient keys daily (in addition to blinded keys):

```python
# Générez LES DEUX, de nouvelles clés éphémères et de nouvelles clés aveuglées, chaque jour

for date in future_dates:

    # New transient keypair for this day
    transient_privkey = generate_red25519_privkey()
    transient_pubkey = derive_public(transient_privkey)
    
    # New blinded keypair for this day
    alpha = GENERATE_ALPHA(destination, datestring, secret)
    blinded_privkey = BLIND_PRIVKEY(signing_privkey, alpha)
    blinded_pubkey = DERIVE_PUBLIC(blinded_privkey)
    
    # Sign new transient key with new blinded key
    sig = RED25519_SIGN(blinded_privkey, transient_pubkey || metadata)
    
    # Now offline sig block changes daily
```

**Benefits:**
- Prevents tracking across days via offline signature block
- Provides same security as encrypted LS2 without offline keys
- Each day appears completely independent

**Cost:**
- More keys to generate and store
- More complex key management

### File Format (TODO)

**Current Status:** No standardized file format defined for batch key delivery.

**Requirements for Future Format:**

1. **Must support multiple dates:**
   - Batch delivery of 30+ days worth of keys
   - Clear date association for each key set

2. **Must include all necessary data:**
   - Transient private key
   - Transient public key
   - Blinded private key
   - Blinded public key
   - Pre-computed offline signature block
   - Expiration timestamps

3. **Should be tamper-evident:**
   - Checksums or signatures over entire file
   - Integrity verification before loading

4. **Should be encrypted:**
   - Keys are sensitive material
   - Encrypt file with router's key or passphrase

**Proposed Format Example (JSON, encrypted):**

```json
{   "version": 1,   "destination_hash": "base64...",   "keys": [

    {
      "date": "2025-10-15",
      "transient": {
        "type": 11,
        "privkey": "base64...",
        "pubkey": "base64..."
      },
      "blinded": {
        "privkey": "base64...",
        "pubkey": "base64..."
      },
      "offline_sig_block": {
        "expires": 1729123200,
        "signature": "base64..."
      }
    }
],   "signature": "base64..."  // Signature over entire structure }

```

### I2CP Protocol Enhancement (TODO)

**Current Status:** No I2CP protocol enhancement defined for offline keys with encrypted LeaseSet.

**Requirements:**

1. **Key delivery mechanism:**
   - Upload batch of keys from client to router
   - Acknowledgment of successful key loading

2. **Key expiration notification:**
   - Router notifies client when keys running low
   - Client can generate and upload new batch

3. **Key revocation:**
   - Emergency revocation of future keys if compromise suspected

**Proposed I2CP Messages:**

```
UPLOAD_OFFLINE_KEYS   - Lot de matériel de clés chiffré   - Plage de dates couverte

OFFLINE_KEY_STATUS   - Nombre de jours restants   - Date d'expiration de la prochaine clé

REVOKE_OFFLINE_KEYS     - Plage de dates à révoquer   - Nouvelles clés de remplacement (facultatif)

```

### Implementation Status

**Java I2P:**
- ✅ Offline keys for standard LS2: Fully supported (since 0.9.38)
- ⚠️ Offline keys for encrypted LS2: Implemented (since 0.9.40)
- ❌ File format: Not standardized
- ❌ I2CP protocol: Not enhanced

**i2pd (C++):**
- ✅ Offline keys for standard LS2: Fully supported
- ✅ Offline keys for encrypted LS2: Fully supported (since 2.58.0)
- ❌ File format: Not standardized
- ❌ I2CP protocol: Not enhanced

**References:**
- [Offline Signatures Proposal](/proposals/123-new-netdb-entries/)
- [I2CP Specification](/docs/specs/i2cp/)

---

## Security Considerations

### Cryptographic Security

**Algorithm Selection:**

All cryptographic primitives are based on well-studied algorithms:
- **ChaCha20:** Modern stream cipher, constant-time, no timing attacks
- **SHA-256:** NIST-approved hash, 128-bit security level
- **HKDF:** RFC 5869 standard, proven security bounds
- **Ed25519/Red25519:** Curve25519-based, ~128-bit security level
- **X25519:** Diffie-Hellman over Curve25519, ~128-bit security level

**Key Sizes:**
- All symmetric keys: 256 bits (32 bytes)
- All public/private keys: 256 bits (32 bytes)
- All nonces/IVs: 96 bits (12 bytes)
- All signatures: 512 bits (64 bytes)

These sizes provide adequate security margins against current and near-future attacks.

### Forward Secrecy

**Daily Key Rotation:**

Encrypted LeaseSets rotate keys daily (UTC midnight):
- New blinded public/private key pair
- New storage location in DHT
- New encryption keys for both layers

**Benefits:**
- Compromising today's blinded key doesn't reveal yesterday's
- Limits exposure window to 24 hours
- Prevents long-term tracking via DHT

**Enhanced with Ephemeral Keys:**

DH client authorization uses ephemeral keys:
- Server generates new ephemeral DH keypair for each publication
- Compromising ephemeral key only affects that publication
- True forward secrecy even if long-term keys compromised

### Privacy Properties

**Destination Blinding:**

The blinded public key:
- Is unlinkable to the original destination (without knowing the secret)
- Changes daily, preventing long-term correlation
- Cannot be reversed to find the original public key

**Client Membership Privacy:**

Per-client authorization provides:
- **Anonymity:** No way to identify which clients are authorized
- **Untraceability:** Cannot track when specific clients added/revoked
- **Size obfuscation:** Can add dummy entries to hide true count

**DHT Privacy:**

Storage location rotates daily:
```
location = SHA-256(sig_type || blinded_public_key)

```

This prevents:
- Correlation across days via DHT lookups
- Long-term monitoring of service availability
- Traffic analysis of DHT queries

### Threat Model

**Adversary Capabilities:**

1. **Network Adversary:**
   - Can monitor all DHT traffic
   - Can observe encrypted LeaseSet publications
   - Cannot decrypt without proper keys

2. **Floodfill Adversary:**
   - Can store and analyze all encrypted LeaseSets
   - Can track publication patterns over time
   - Cannot decrypt Layer 1 or Layer 2
   - Can see client count (but not identities)

3. **Authorized Client Adversary:**
   - Can decrypt specific encrypted LeaseSets
   - Can access inner LeaseSet2 data
   - Cannot determine other clients' identities
   - Cannot decrypt past LeaseSets (with ephemeral keys)

**Out of Scope:**

- Malicious router implementations
- Compromised router host systems
- Side-channel attacks (timing, power analysis)
- Physical access to keys
- Social engineering attacks

### Attack Scenarios

**1. Offline Keys Tracking Attack:**

**Attack:** Adversary tracks encrypted LeaseSets via unchanging offline signature block.

**Mitigation:** Generate new transient keys daily (in addition to blinded keys).

**Status:** Documented recommendation, implementation-specific.

**2. Client Position Inference Attack:**

**Attack:** If client order is static, clients can infer their position and detect when other clients added/removed.

**Mitigation:** Randomize client order in authorization list for each publication.

**Status:** Documented recommendation in specification.

**3. Client Count Analysis Attack:**

**Attack:** Adversary monitors client count changes over time to infer service popularity or client churn.

**Mitigation:** Add random dummy entries to authorization list.

**Status:** Optional feature, deployment-specific trade-off (size vs. privacy).

**4. PSK Interception Attack:**

**Attack:** Adversary intercepts PSK during out-of-band exchange and can decrypt all future encrypted LeaseSets.

**Mitigation:** Use DH client authorization instead, or ensure secure key exchange (Signal, OTR, PGP).

**Status:** Known limitation of PSK approach, documented in specification.

**5. Timing Correlation Attack:**

**Attack:** Adversary correlates publication times across days to link encrypted LeaseSets.

**Mitigation:** Randomize publication times, use delayed publishing.

**Status:** Implementation-specific, not addressed in core specification.

**6. Long-term Secret Compromise:**

**Attack:** Adversary compromises the blinding secret and can compute all past and future blinded keys.

**Mitigation:** 
- Use optional secret parameter (not empty)
- Rotate secret periodically
- Use different secrets for different services

**Status:** Secret parameter is optional; using it is highly recommended.

### Operational Security

**Key Management:**

1. **Signing Private Key:**
   - Store offline in cold storage
   - Use only for generating blinded keys (batch process)
   - Never expose to online router

2. **Blinded Private Keys:**
   - Generate offline, deliver in batches
   - Rotate daily automatically
   - Delete after use (forward secrecy)

3. **Transient Private Keys (with offline keys):**
   - Generate offline, deliver in batches
   - Can be longer-lived (days/weeks)
   - Rotate regularly for enhanced privacy

4. **Client Authorization Keys:**
   - DH: Client private keys never leave client device
   - PSK: Use unique keys per client, secure exchange
   - Revoke immediately upon client removal

**Secret Management:**

The optional secret parameter in `GENERATE_ALPHA`:
- SHOULD be used for high-security services
- MUST be transmitted securely to authorized clients
- SHOULD be rotated periodically (e.g., monthly)
- CAN be different for different client groups

**Monitoring and Auditing:**

1. **Publication Monitoring:**
   - Verify encrypted LeaseSets published successfully
   - Monitor floodfill acceptance rates
   - Alert on publication failures

2. **Client Access Monitoring:**
   - Log client authorization attempts (without identifying clients)
   - Monitor for unusual patterns
   - Detect potential attacks early

3. **Key Rotation Auditing:**
   - Verify daily key rotation occurs
   - Check blinded key changes daily
   - Ensure old keys are deleted

### Implementation Security

**Constant-Time Operations:**

Implementations MUST use constant-time operations for:
- All scalar arithmetic (mod L operations)
- Private key comparisons
- Signature verification
- DH key agreement

**Memory Security:**

- Zero sensitive key material after use
- Use secure memory allocation for keys
- Prevent keys from being paged to disk
- Clear stack variables containing key material

**Random Number Generation:**

- Use cryptographically secure RNG (CSRNG)
- Properly seed RNG from OS entropy source
- Do not use predictable RNGs for key material
- Verify RNG output quality periodically

**Input Validation:**

- Validate all public keys are on the curve
- Check all signature types are supported
- Verify all lengths before parsing
- Reject malformed encrypted LeaseSets early

**Error Handling:**

- Do not leak information via error messages
- Use constant-time comparison for authentication
- Do not expose timing differences in decryption
- Log security-relevant events properly

### Recommendations

**For Service Operators:**

1. ✅ **Use Red25519 (type 11)** for new destinations
2. ✅ **Use DH client authorization** for high-security services
3. ✅ **Generate new transient keys daily** when using offline keys
4. ✅ **Use the optional secret parameter** in GENERATE_ALPHA
5. ✅ **Randomize client order** in authorization lists
6. ✅ **Monitor publication success** and investigate failures
7. ⚠️ **Consider dummy entries** to hide client count (size trade-off)

**For Client Implementers:**

1. ✅ **Validate blinded public keys** are on prime-order subgroup
2. ✅ **Verify all signatures** before trusting data
3. ✅ **Use constant-time operations** for cryptographic primitives
4. ✅ **Zero key material** immediately after use
5. ✅ **Implement proper error handling** without information leaks
6. ✅ **Support both Ed25519 and Red25519** destination types

**For Network Operators:**

1. ✅ **Accept encrypted LeaseSets** in floodfill routers
2. ✅ **Enforce reasonable size limits** to prevent abuse
3. ✅ **Monitor for anomalous patterns** (extremely large, frequent updates)
4. ⚠️ **Consider rate limiting** encrypted LeaseSet publications

---

## Implementation Notes

### Java I2P Implementation

**Repository:** https://github.com/i2p/i2p.i2p

**Key Classes:**
- `net.i2p.data.LeaseSet2` - LeaseSet2 structure
- `net.i2p.data.EncryptedLeaseSet` - Encrypted LS2 implementation
- `net.i2p.crypto.eddsa.EdDSAEngine` - Ed25519/Red25519 signatures
- `net.i2p.crypto.HKDF` - HKDF implementation
- `net.i2p.crypto.ChaCha20` - ChaCha20 cipher

**Configuration:**

Enable encrypted LeaseSet in `clients.config`:
```properties
# Activer le LeaseSet (descripteur d'accès à une destination I2P) chiffré

i2cp.encryptLeaseSet=true

# Facultatif : activer l’autorisation des clients

i2cp.enableAccessList=true

# Facultatif : utiliser l’autorisation DH (Diffie-Hellman) (par défaut : PSK, clé pré-partagée)

i2cp.accessListType=0

# Facultatif : Blinding secret (secret d’aveuglement, fortement recommandé)

i2cp.blindingSecret=votre-secret-ici

```

**API Usage Example:**

```java
// Créer un LeaseSet chiffré EncryptedLeaseSet els = new EncryptedLeaseSet();

// Définir la destination els.setDestination(destination);

// Activer l'autorisation par client els.setAuthorizationEnabled(true); els.setAuthType(EncryptedLeaseSet.AUTH_DH);

// Ajouter des clients autorisés (clés publiques DH (Diffie-Hellman)) for (byte[] clientPubKey : authorizedClients) {

    els.addClient(clientPubKey);
}

// Définir les paramètres d'aveuglement (blinding) els.setBlindingSecret("your-secret");

// Signer et publier els.sign(signingPrivateKey); netDb.publish(els);

```

### i2pd (C++) Implementation

**Repository:** https://github.com/PurpleI2P/i2pd

**Key Files:**
- `libi2pd/LeaseSet.h/cpp` - LeaseSet implementations
- `libi2pd/Crypto.h/cpp` - Cryptographic primitives
- `libi2pd/Ed25519.h/cpp` - Ed25519/Red25519 signatures
- `libi2pd/ChaCha20.h/cpp` - ChaCha20 cipher

**Configuration:**

Enable in tunnel configuration (`tunnels.conf`):
```ini
[my-hidden-service] type = http host = 127.0.0.1 port = 8080 keys = my-service-keys.dat

# Activer le LeaseSet chiffré

encryptleaseset = true

# Optionnel : Type d’autorisation client (0=DH, 1=PSK)

authtype = 0

# Optionnel: Secret d'aveuglement

secret = your-secret-here

# Facultatif : Clients autorisés (une par ligne, clés publiques encodées en base64)

client.1 = base64-encoded-client-pubkey-1 client.2 = base64-encoded-client-pubkey-2

```

**API Usage Example:**

```cpp
// Créer un LeaseSet chiffré auto encryptedLS = std::make_shared<i2p::data::EncryptedLeaseSet>(

    destination,
    blindingSecret
);

// Activer l'autorisation par client encryptedLS->SetAuthType(i2p::data::AUTH_TYPE_DH);

// Ajouter les clients autorisés for (const auto& clientPubKey : authorizedClients) {

    encryptedLS->AddClient(clientPubKey);
}

// Signer et publier encryptedLS->Sign(signingPrivKey); netdb.Publish(encryptedLS);

```

### Testing and Debugging

**Test Vectors:**

Generate test vectors for implementation verification:

```python
# Vecteur de test 1 : Aveuglement de clé

destination_pubkey = bytes.fromhex('a' * 64) sigtype = 7 blinded_sigtype = 11 date = "20251015" secret = ""

alpha = generate_alpha(destination_pubkey, sigtype, blinded_sigtype, date, secret) print(f"Alpha: {alpha.hex()}")

# Attendu: (vérifier par rapport à l'implémentation de référence)

```

**Unit Tests:**

Key areas to test:
1. HKDF derivation with various inputs
2. ChaCha20 encryption/decryption
3. Red25519 signature generation and verification
4. Key blinding (private and public)
5. Layer 1/2 encryption/decryption
6. Client authorization (DH and PSK)
7. Base32 address generation and parsing

**Integration Tests:**

1. Publish encrypted LeaseSet to test network
2. Retrieve and decrypt from client
3. Verify daily key rotation
4. Test client authorization (add/remove clients)
5. Test offline keys (if supported)

**Common Implementation Errors:**

1. **Incorrect mod L reduction:** Must use proper modular arithmetic
2. **Endianness errors:** Most fields are big-endian, but some crypto uses little-endian
3. **Off-by-one in array slicing:** Verify indices are inclusive/exclusive as needed
4. **Missing constant-time comparisons:** Use constant-time for all sensitive comparisons
5. **Not zeroing key material:** Always zero keys after use

### Performance Considerations

**Computational Costs:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Operation</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Cost</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Key blinding (server)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 scalar mult</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per publication</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Key blinding (client)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 point add + 1 scalar mult</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per retrieval</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Layer 1 encryption</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 HKDF + 1 ChaCha20</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Fast</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Layer 2 encryption</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 HKDF + 1 ChaCha20</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Fast</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DH client auth (server)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">N+1 X25519 ops</td><td style="border:1px solid var(--color-border); padding:0.5rem;">N = number of clients</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DH client auth (client)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 X25519 op</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per retrieval</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">PSK client auth</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0 DH ops</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Only HKDF + ChaCha20</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature (Red25519)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 signature op</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Similar cost to Ed25519</td></tr>
  </tbody>
</table>

**Size Overhead:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Component</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Frequency</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded public key</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Layer 1 encryption overhead</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes (salt)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Layer 2 encryption overhead</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes (salt)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DH auth per client</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per client per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DH ephemeral pubkey</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet (if DH auth)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">PSK auth per client</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per client per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">PSK salt</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet (if PSK auth)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature</td><td style="border:1px solid var(--color-border); padding:0.5rem;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline sig block</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈100 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Per LeaseSet (if offline keys)</td></tr>
  </tbody>
</table>

**Typical Sizes:**

- **No client auth:** ~200 bytes overhead
- **With 10 DH clients:** ~600 bytes overhead
- **With 100 DH clients:** ~4200 bytes overhead

**Optimization Tips:**

1. **Batch key generation:** Generate blinded keys for multiple days in advance
2. **Cache subcredentials:** Compute once per day, reuse for all publications
3. **Reuse ephemeral keys:** Can reuse ephemeral DH key for short period (minutes)
4. **Parallel client encryption:** Encrypt client cookies in parallel
5. **Fast path for no auth:** Skip authorization layer entirely when disabled

### Compatibility

**Backward Compatibility:**

- Ed25519 (type 7) destinations supported for unblinded keys
- Red25519 (type 11) required for blinded keys
- Traditional LeaseSets still fully supported
- Encrypted LeaseSets do not break existing network

**Forward Compatibility:**

- Reserved flag bits for future features
- Extensible authorization scheme (3 bits allow 8 types)
- Version field in various structures

**Interoperability:**

- Java I2P and i2pd fully interoperable since:
  - Java I2P 0.9.40 (May 2019)
  - i2pd 2.58.0 (September 2025)
- Encrypted LeaseSets work across implementations
- Client authorization works across implementations

---

## References

### IETF RFCs

- **[RFC 2104](https://datatracker.ietf.org/doc/html/rfc2104)** - HMAC: Keyed-Hashing for Message Authentication (February 1997)
- **[RFC 5869](https://datatracker.ietf.org/doc/html/rfc5869)** - HMAC-based Extract-and-Expand Key Derivation Function (HKDF) (May 2010)
- **[RFC 7539](https://datatracker.ietf.org/doc/html/rfc7539)** - ChaCha20 and Poly1305 for IETF Protocols (May 2015)
- **[RFC 7748](https://datatracker.ietf.org/doc/html/rfc7748)** - Elliptic Curves for Security (January 2016)

### I2P Specifications

- **[Common Structures Specification](/docs/specs/common-structures/)** - LeaseSet2 and EncryptedLeaseSet structures
- **[Proposal 123: New netDB Entries](/proposals/123-new-netdb-entries/)** - Background and design of LeaseSet2
- **[Proposal 146: Red25519](/proposals/146-red25519/)** - Red25519 signature scheme specification
- **[Proposal 149: B32 for Encrypted LS2](/proposals/149-b32-encrypted-ls2/)** - Base32 addressing for encrypted LeaseSets
- **[Red25519 Specification](/docs/specs/red25519-signature-scheme/)** - Detailed Red25519 implementation
- **[B32 Addressing Specification](/docs/specs/b32-for-encrypted-leasesets/)** - Base32 address format
- **[Network Database Documentation](/docs/specs/common-structures/)** - NetDB usage and operations
- **[I2CP Specification](/docs/specs/i2cp/)** - I2P Client Protocol

### Cryptographic References

- **[Ed25519 Paper](http://cr.yp.to/papers.html#ed25519)** - "High-speed high-security signatures" by Bernstein et al.
- **[ZCash Protocol Specification](https://zips.z.cash/protocol/protocol.pdf)** - Section 5.4.6: RedDSA signature scheme
- **[Tor Rendezvous Specification v3](https://spec.torproject.org/rend-spec)** - Tor's onion service specification (for comparison)

### Security References

- **[Key Blinding Security Discussion](https://lists.torproject.org/pipermail/tor-dev/2013-December/005943.html)** - Tor Project mailing list discussion
- **[Tor Ticket #8106](https://trac.torproject.org/projects/tor/ticket/8106)** - Key blinding implementation discussion
- **[PRNG Security](http://projectbullrun.org/dual-ec/ext-rand.html)** - Random number generator security considerations
- **[Tor PRNG Discussion](https://lists.torproject.org/pipermail/tor-dev/2015-November/009954.html)** - Discussion of PRNG usage in Tor

### Implementation References

- **[Java I2P Repository](https://github.com/i2p/i2p.i2p)** - Official Java implementation
- **[i2pd Repository](https://github.com/PurpleI2P/i2pd)** - C++ implementation
- **[I2P Website](/)** - Official I2P project website
- **[I2P Specifications](/docs/specs/)** - Complete specification index

### Version History

- **[I2P Release Notes](/en/blog)** - Official release announcements
- **[Java I2P Releases](https://github.com/i2p/i2p.i2p/releases)** - GitHub release history
- **[i2pd Releases](https://github.com/PurpleI2P/i2pd/releases)** - GitHub release history

---

## Appendix A: Cryptographic Constants

### Ed25519 / Red25519 Constants

```python
# Point de base Ed25519 (générateur)

B = 2**255 - 19

# Ordre d'Ed25519 (taille du corps scalaire)

L = 2**252 + 27742317777372353535851937790883648493

# Valeurs des types de signature

SIGTYPE_ED25519 = 7    # 0x0007 SIGTYPE_RED25519 = 11  # 0x000b

# Tailles de clés

PRIVKEY_SIZE = 32  # bytes PUBKEY_SIZE = 32   # bytes SIGNATURE_SIZE = 64  # bytes

```

### ChaCha20 Constants

```python
# Paramètres de ChaCha20

CHACHA20_KEY_SIZE = 32   # octets (256 bits) CHACHA20_NONCE_SIZE = 12  # octets (96 bits) CHACHA20_INITIAL_COUNTER = 1  # RFC 7539 autorise 0 ou 1

```

### HKDF Constants

```python
# Paramètres de HKDF (fonction de dérivation de clés basée sur HMAC)

HKDF_HASH = "SHA-256" HKDF_SALT_MAX = 32  # bytes (HashLen)

# Chaînes d'info HKDF (séparation des domaines)

HKDF_INFO_ALPHA = b"i2pblinding1" HKDF_INFO_LAYER1 = b"ELS2_L1K" HKDF_INFO_LAYER2 = b"ELS2_L2K" HKDF_INFO_DH_AUTH = b"ELS2_XCA" HKDF_INFO_PSK_AUTH = b"ELS2PSKA"

```

### Hash Personalization Strings

```python
# Chaînes de personnalisation pour SHA-256

HASH_PERS_ALPHA = b"I2PGenerateAlpha" HASH_PERS_RED25519 = b"I2P_Red25519H(x)" HASH_PERS_CREDENTIAL = b"credential" HASH_PERS_SUBCREDENTIAL = b"subcredential"

```

### Structure Sizes

```python
# Tailles de la couche 0 (externe)

BLINDED_SIGTYPE_SIZE = 2   # octets BLINDED_PUBKEY_SIZE = 32   # octets (pour Red25519) PUBLISHED_TS_SIZE = 4      # octets EXPIRES_SIZE = 2           # octets FLAGS_SIZE = 2             # octets LEN_OUTER_CIPHER_SIZE = 2  # octets SIGNATURE_SIZE = 64        # octets (Red25519)

# Tailles des blocs de clés hors ligne

OFFLINE_EXPIRES_SIZE = 4   # octets OFFLINE_SIGTYPE_SIZE = 2   # octets OFFLINE_SIGNATURE_SIZE = 64  # octets

# Tailles de la couche 1 (intermédiaire)

AUTH_FLAGS_SIZE = 1        # octet EPHEMERAL_PUBKEY_SIZE = 32  # octets (authentification DH) AUTH_SALT_SIZE = 32        # octets (authentification PSK) NUM_CLIENTS_SIZE = 2       # octets CLIENT_ID_SIZE = 8         # octets CLIENT_COOKIE_SIZE = 32    # octets AUTH_CLIENT_ENTRY_SIZE = 40  # octets (CLIENT_ID + CLIENT_COOKIE)

# Surcoût du chiffrement

SALT_SIZE = 32  # octets (ajoutés en tête de chaque couche chiffrée)

# Adresse Base32

B32_ENCRYPTED_DECODED_SIZE = 35  # octets B32_ENCRYPTED_ENCODED_LEN = 56   # caractères B32_SUFFIX = ".b32.i2p"

```

---

## Appendix B: Test Vectors

### Test Vector 1: Alpha Generation

**Input:**
```python
# Clé publique de destination (Ed25519)

A = bytes.fromhex('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa') stA = 0x0007  # Ed25519 stA_prime = 0x000b  # Red25519 date = "20251015" secret = ""  # Secret vide

```

**Computation:**
```python
keydata = A || bytes([0x00, 0x07]) || bytes([0x00, 0x0b])

# keydata = 36 octets

salt = SHA256(b"I2PGenerateAlpha" + keydata) ikm = b"20251015" info = b"i2pblinding1"

seed = HKDF(salt, ikm, info, 64) alpha = LEOS2IP(seed) mod L

```

**Expected Output:**
```
(Vérifier par rapport à l’implémentation de référence) alpha = [valeur hexadécimale de 64 octets]

```

### Test Vector 2: ChaCha20 Encryption

**Input:**
```python
key = bytes([i for i in range(32)])  # 0x00..0x1f nonce = bytes([i for i in range(12)])  # 0x00..0x0b plaintext = b"Hello, I2P!"

```

**Computation:**
```python
ciphertext = ChaCha20_Encrypt(key, nonce, plaintext, counter=1)

```

**Expected Output:**
```
ciphertext = [vérifier par rapport aux vecteurs de test de la RFC 7539]

```

### Test Vector 3: HKDF

**Input:**
```python
salt = bytes(32)  # Tous à zéro ikm = b"test input keying material" info = b"ELS2_L1K" n = 44

```

**Computation:**
```python
keys = HKDF(salt, ikm, info, n)

```

**Expected Output:**
```
keys = [valeur hexadécimale de 44 octets]

```

### Test Vector 4: Base32 Address

**Input:**
```python
pubkey = bytes.fromhex('bbbb' + 'bb' * 30)  # 32 octets unblinded_sigtype = 11  # Red25519 blinded_sigtype = 11    # Red25519

```

**Computation:**
```python
address = generate_encrypted_b32_address(pubkey, unblinded_sigtype, blinded_sigtype)

```

**Expected Output:**
```
address = [56 caractères en base32].b32.i2p

# Vérifiez que la somme de contrôle est valide

```

---

## Appendix C: Glossary

**Alpha (α):** The secret blinding factor used to blind public and private keys. Generated from the destination, date, and optional secret.

**AuthCookie:** A 32-byte random value encrypted for each authorized client, used as input to Layer 2 encryption.

**B (Base Point):** The generator point for the Ed25519 elliptic curve.

**Blinded Key:** A public or private key that has been transformed using the alpha blinding factor. Blinded keys cannot be linked to the original keys without knowing alpha.

**ChaCha20:** A stream cipher providing fast, secure encryption without requiring AES hardware support.

**ClientID:** An 8-byte identifier derived from HKDF output, used to identify authorization entries for clients.

**ClientCookie:** A 32-byte encrypted value containing the authCookie for a specific client.

**Credential:** A 32-byte value derived from the destination's public key and signature types, binding encryption to knowledge of the destination.

**CSRNG:** Cryptographically Secure Random Number Generator. Must provide unpredictable output suitable for key generation.

**DH (Diffie-Hellman):** A cryptographic protocol for securely establishing shared secrets. I2P uses X25519.

**Ed25519:** An elliptic curve signature scheme providing fast signatures with 128-bit security level.

**Ephemeral Key:** A short-lived cryptographic key, typically used once and then discarded.

**Floodfill:** I2P routers that store and serve network database entries, including encrypted LeaseSets.

**HKDF:** HMAC-based Key Derivation Function, used to derive multiple cryptographic keys from a single source.

**L (Order):** The order of the Ed25519 scalar field (approximately 2^252).

**Layer 0 (Outer):** The plaintext portion of an encrypted LeaseSet, containing blinded key and metadata.

**Layer 1 (Middle):** The first encrypted layer, containing client authorization data.

**Layer 2 (Inner):** The innermost encrypted layer, containing the actual LeaseSet2 data.

**LeaseSet2 (LS2):** Second version of I2P's network database entry format, introducing encrypted variants.

**NetDB:** The I2P network database, a distributed hash table storing router and destination information.

**Offline Keys:** A feature allowing the main signing key to remain in cold storage while a transient key handles daily operations.

**PSK (Pre-Shared Key):** A symmetric key shared in advance between two parties, used for PSK client authorization.

**Red25519:** An Ed25519-based signature scheme with key blinding support, based on ZCash RedDSA.

**Salt:** Random data used as input to key derivation functions to ensure unique outputs.

**SigType:** A numeric identifier for signature algorithms (e.g., 7 = Ed25519, 11 = Red25519).

**Subcredential:** A 32-byte value derived from the credential and blinded public key, binding encryption to a specific encrypted LeaseSet.

**Transient Key:** A temporary signing key used with offline keys, with a limited validity period.

**X25519:** An elliptic curve Diffie-Hellman protocol over Curve25519, providing key agreement.

---

## Document Information

**Status:** This document represents the current stable encrypted LeaseSet specification as implemented in I2P since June 2019. The protocol is mature and widely deployed.

**Contributing:** For corrections or improvements to this documentation, please submit issues or pull requests to the I2P specifications repository.

**Support:** For questions about implementing encrypted LeaseSets:
- I2P Forum: https://i2pforum.net/
- IRC: #i2p-dev on OFTC
- Matrix: #i2p-dev:matrix.org

**Acknowledgments:** This specification builds on work by the I2P development team, ZCash cryptography research, and Tor Project's key blinding research.