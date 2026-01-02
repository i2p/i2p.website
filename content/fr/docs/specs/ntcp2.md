---
title: "Transport NTCP2"
description: "Transport TCP basé sur Noise (cadre de protocoles) pour les liens de router à router"
slug: "ntcp2"
lastUpdated: "2025-10"
accurateFor: "0.9.66"
type: docs
---

## Aperçu

NTCP2 remplace l’ancien transport NTCP par un handshake basé sur Noise (framework de protocoles cryptographiques) qui résiste au fingerprinting du trafic, chiffre les champs de longueur et prend en charge des suites cryptographiques modernes. Les routers peuvent exécuter NTCP2 aux côtés de SSU2, les deux protocoles de transport obligatoires du réseau I2P. NTCP (version 1) a été déprécié dans la 0.9.40 (mai 2019) et entièrement supprimé dans la 0.9.50 (mai 2021).

## Cadre de protocoles Noise

NTCP2 utilise le Noise Protocol Framework (cadre de protocoles cryptographiques) [Revision 33, 2017-10-04](https://noiseprotocol.org/noise.html) avec des extensions spécifiques à I2P :

- **Schéma**: `Noise_XK_25519_ChaChaPoly_SHA256`
- **Identifiant étendu**: `Noise_XKaesobfse+hs2+hs3_25519_ChaChaPoly_SHA256` (pour l'initialisation du KDF, fonction de dérivation de clé)
- **Fonction DH**: X25519 (RFC 7748) - clés de 32 octets, encodage little-endian
- **Chiffrement**: AEAD_CHACHA20_POLY1305 (RFC 7539/RFC 8439)
  - Nonce de 12 octets: 4 premiers octets à zéro, 8 derniers octets servent de compteur (little-endian)
  - Valeur maximale du nonce: 2^64 - 2 (la connexion doit se terminer avant d'atteindre 2^64 - 1)
- **Fonction de hachage**: SHA-256 (sortie de 32 octets)
- **MAC**: Poly1305 (tag d'authentification de 16 octets)

### Extensions spécifiques à I2P

1. **Obfuscation par AES**: Clés éphémères chiffrées avec AES-256-CBC en utilisant le hachage du router de Bob et un IV publié (vecteur d'initialisation)
2. **Bourrage aléatoire**: Bourrage en clair dans les messages 1-2 (authentifiés), bourrage AEAD (Authenticated Encryption with Associated Data) dans les messages 3+ (chiffrés)
3. **Obfuscation de la longueur par SipHash-2-4**: Longueurs de trame sur deux octets XORées (OU exclusif) avec la sortie de SipHash
4. **Structure des trames**: Trames préfixées par la longueur pour la phase de données (compatibilité avec le streaming TCP)
5. **Charges utiles basées sur des blocs**: Format de données structuré avec des blocs typés

## Flux de négociation

```
Alice (Initiator)             Bob (Responder)
SessionRequest  ──────────────────────►
                ◄────────────────────── SessionCreated
SessionConfirmed ──────────────────────►
```
### Poignée de main en trois messages

1. **SessionRequest** - la clé éphémère obfusquée d'Alice, options, indications de bourrage
2. **SessionCreated** - la clé éphémère obfusquée de Bob, options chiffrées, bourrage
3. **SessionConfirmed** - la clé statique chiffrée d'Alice et RouterInfo (deux trames AEAD)

### Schémas de messages Noise

```
XK(s, rs):           Authentication   Confidentiality
  <- s               (Bob's static key known in advance)
  -> e, es                  0                2
  <- e, ee                  2                1
  -> s, se                  2                5
  <-                        2                5
```
**Niveaux d’authentification:** - 0: Aucune authentification (n’importe qui aurait pu l’envoyer) - 2: Authentification de l’expéditeur résistante aux attaques de key-compromise impersonation (KCI, usurpation en cas de compromission de clé)

**Niveaux de confidentialité:** - 1: Destinataire éphémère (confidentialité persistante, aucune authentification du destinataire) - 2: Destinataire connu, confidentialité persistante uniquement en cas de compromission de l'expéditeur - 5: Confidentialité persistante forte (DH éphémère-éphémère + éphémère-statique)

## Spécifications des messages

### Notation des clés

- `RH_A` = Hachage du Router d’Alice (32 octets, SHA-256)
- `RH_B` = Hachage du Router de Bob (32 octets, SHA-256)
- `||` = opérateur de concaténation
- `byte(n)` = Un octet unique de valeur n
- Tous les entiers multi-octets sont en **big-endian** sauf indication contraire
- Les clés X25519 sont en **little-endian** (32 octets)

### Chiffrement authentifié (ChaCha20-Poly1305)

**Fonction de chiffrement :**

```
AEAD_ChaCha20_Poly1305(key, nonce, associatedData, plaintext)
  → (ciphertext || MAC)
```
**Paramètres:** - `key`: clé de chiffrement de 32 octets issue d'une KDF (fonction de dérivation de clé) - `nonce`: 12 octets (4 octets nuls + compteur sur 8 octets, little-endian (ordre des octets du moins significatif au plus significatif)) - `associatedData`: hachage de 32 octets pendant la phase de handshake (établissement de session); longueur nulle pendant la phase de données - `plaintext`: Données à chiffrer (0+ octets)

**Sortie:** - Texte chiffré: Même longueur que le texte en clair - MAC: 16 octets (tag d'authentification Poly1305)

**Gestion du nonce (nombre à usage unique):** - Le compteur commence à 0 pour chaque instance de chiffrement - S'incrémente à chaque opération AEAD dans cette direction - Compteurs séparés pour Alice→Bob et Bob→Alice dans la phase de données - La connexion doit être interrompue avant que le compteur n'atteigne 2^64 - 1

## Message 1 : SessionRequest (requête de session)

Alice initie une connexion vers Bob.

**Opérations Noise**: `e, es` (génération et échange de clés éphémères)

### Format brut

```
+----+----+----+----+----+----+----+----+
|                                       |
+    AES-256-CBC Encrypted X (32B)      +
|    Key: RH_B, IV: Bob's published IV  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+    ChaChaPoly Frame (48 bytes)        +
|    Plaintext: 32B (X + options)       |
+    k from KDF-1, n=0, ad=h            +
|                                       |
+----+----+----+----+----+----+----+----+
|    Cleartext Padding (optional)       |
+    Length specified in options         +
|    0 to 65535 - 80 bytes              |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
**Contraintes de taille :** - Minimum : 80 octets (32 AES + 48 AEAD) - Maximum : 65535 octets au total - **Cas particulier** : 287 octets max lors de la connexion à des adresses "NTCP" (détection de la version)

### Contenu déchiffré

```
+----+----+----+----+----+----+----+----+
|                                       |
+    X (Alice ephemeral public key)     +
|    32 bytes, X25519, little-endian    |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|           Options Block               |
+             (16 bytes)                +
|                                       |
+----+----+----+----+----+----+----+----+
|    Cleartext Padding (optional)       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
### Bloc d’options (16 octets, big-endian (ordre des octets gros-boutiste))

```
+----+----+----+----+----+----+----+----+
| id | ver|  padLen | m3p2len | Rsvd(0) |
+----+----+----+----+----+----+----+----+
|        tsA        |   Reserved (0)    |
+----+----+----+----+----+----+----+----+

id      : 1 byte  - Network ID (2 for mainnet, 16-254 for testnets)
ver     : 1 byte  - Protocol version (currently 2)
padLen  : 2 bytes - Padding length in this message (0-65455)
m3p2len : 2 bytes - Length of SessionConfirmed part 2 frame
Rsvd    : 2 bytes - Reserved, set to 0
tsA     : 4 bytes - Unix timestamp (seconds since epoch)
Reserved: 4 bytes - Reserved, set to 0
```
**Champs critiques:** - **Network ID** (depuis la version 0.9.42): Rejet rapide des connexions entre réseaux - **m3p2len**: Taille exacte du message 3 partie 2 (doit correspondre lors de l’envoi)

### Fonction de dérivation de clé (KDF-1)

**Initialiser le protocole :**

```
protocol_name = "Noise_XKaesobfse+hs2+hs3_25519_ChaChaPoly_SHA256"
h = SHA256(protocol_name)
ck = h  // Chaining key initialized to hash
```
**Opérations de MixHash :**

```
h = SHA256(h)                    // Null prologue
h = SHA256(h || rs)              // Bob's static key (known)
h = SHA256(h || e.pubkey)        // Alice's ephemeral key X
// h is now the associated data for message 1 AEAD
```
**Opération MixKey (es pattern — schéma « es »):**

```
dh_result = X25519(Alice.ephemeral_private, Bob.static_public)
temp_key = HMAC-SHA256(ck, dh_result)
ck = HMAC-SHA256(temp_key, byte(0x01))
k = HMAC-SHA256(temp_key, ck || byte(0x02))
// k is the cipher key for message 1
// ck is retained for message 2 KDF
```
### Notes d'implémentation

1. **Obfuscation par AES**: Utilisée uniquement pour la résistance au DPI (inspection approfondie des paquets) ; toute personne disposant du hachage du router de Bob et de l’IV (vecteur d’initialisation) peut déchiffrer X
2. **Prévention du rejeu**: Bob doit mettre en cache les valeurs X (ou leurs équivalents chiffrés) pendant au moins 2*D secondes (D = écart d’horloge maximal)
3. **Validation de l’horodatage**: Bob doit rejeter les connexions avec |tsA - current_time| > D (typiquement D = 60 secondes)
4. **Validation de la courbe**: Bob doit vérifier que X est un point X25519 valide
5. **Rejet rapide**: Bob peut vérifier que X[31] & 0x80 == 0 avant déchiffrement (les clés X25519 valides ont le bit de poids fort (MSB) à 0)
6. **Gestion des erreurs**: En cas d’échec, Bob ferme avec un TCP RST après un délai aléatoire et la lecture d’un nombre aléatoire d’octets
7. **Mise en tampon**: Alice doit vider l’intégralité du message (y compris le remplissage) en une seule fois pour des raisons d’efficacité

## Message 2 : SessionCreated

Bob répond à Alice.

**Opérations Noise** (cadre de protocoles cryptographiques) : `e, ee` (DH éphémère-éphémère)

### Format brut

```
+----+----+----+----+----+----+----+----+
|                                       |
+    AES-256-CBC Encrypted Y (32B)      +
|    Key: RH_B, IV: AES state from msg1 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+    ChaChaPoly Frame (48 bytes)        +
|    Plaintext: 32B (Y + options)       |
+    k from KDF-2, n=0, ad=h            +
|                                       |
+----+----+----+----+----+----+----+----+
|    Cleartext Padding (optional)       |
+    Length specified in options         +
|    0 to 65535 - 80 bytes              |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
### Contenu déchiffré

```
+----+----+----+----+----+----+----+----+
|                                       |
+    Y (Bob ephemeral public key)       +
|    32 bytes, X25519, little-endian    |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|           Options Block               |
+             (16 bytes)                +
|                                       |
+----+----+----+----+----+----+----+----+
|    Cleartext Padding (optional)       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
### Bloc d’options (16 octets, big-endian)

```
+----+----+----+----+----+----+----+----+
| Rsvd(0) | padLen  |   Reserved (0)    |
+----+----+----+----+----+----+----+----+
|        tsB        |   Reserved (0)    |
+----+----+----+----+----+----+----+----+

Rsvd    : 2 bytes - Reserved, set to 0
padLen  : 2 bytes - Padding length in this message
Reserved: 10 bytes - Reserved, set to 0
tsB     : 4 bytes - Unix timestamp (seconds since epoch)
```
### Fonction de dérivation de clés (KDF-2)

**Opérations de MixHash:**

```
h = SHA256(h || encrypted_payload_msg1)  // 32-byte ciphertext
if (msg1_padding_length > 0):
    h = SHA256(h || padding_from_msg1)
h = SHA256(h || e.pubkey)                // Bob's ephemeral key Y
// h is now the associated data for message 2 AEAD
```
**Opération MixKey (schéma ee):**

```
dh_result = X25519(Bob.ephemeral_private, Alice.ephemeral_public)
temp_key = HMAC-SHA256(ck, dh_result)
ck = HMAC-SHA256(temp_key, byte(0x01))
k = HMAC-SHA256(temp_key, ck || byte(0x02))
// k is the cipher key for message 2
// ck is retained for message 3 KDF
```
**Nettoyage de la mémoire:**

```
// Overwrite ephemeral keys after ee DH
Alice.ephemeral_public = zeros(32)
Alice.ephemeral_private = zeros(32)  // Bob side
Bob.received_ephemeral = zeros(32)    // Bob side
```
### Notes d'implémentation

1. **Chaînage AES**: Le chiffrement de Y utilise l’état AES-CBC du message 1 (non réinitialisé)
2. **Prévention des rejouements**: Alice doit mettre en cache les valeurs Y pendant au moins 2*D secondes
3. **Validation de l’horodatage**: Alice doit rejeter |tsB - current_time| > D
4. **Validation de la courbe**: Alice doit vérifier que Y est un point X25519 valide
5. **Gestion des erreurs**: Alice ferme avec un TCP RST en cas d’échec
6. **Mise en tampon**: Bob doit vider l’intégralité du message en une seule fois

## Message 3 : SessionConfirmed

Alice confirme la session et envoie RouterInfo (informations du router).

**Opérations Noise**: `s, se` (révélation de clé statique et DH statique-éphémère)

### Structure en deux parties

Message 3 se compose de **deux trames AEAD (chiffrement authentifié avec des données associées) distinctes**:

1. **Partie 1**: Trame fixe de 48 octets avec la clé statique chiffrée d'Alice
2. **Partie 2**: Trame de longueur variable avec RouterInfo, des options et du bourrage

### Format brut

```
+----+----+----+----+----+----+----+----+
|    ChaChaPoly Frame 1 (48 bytes)      |
+    Plaintext: Alice static key (32B)  +
|    k from KDF-2, n=1, ad=h            |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+    ChaChaPoly Frame 2 (variable)      +
|    Length specified in msg1.m3p2len   |
+    k from KDF-3, n=0, ad=h            +
|    Plaintext: RouterInfo + padding    |
+                                       +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
**Contraintes de taille:** - Partie 1: Exactement 48 octets (32 texte en clair + 16 MAC) - Partie 2: Longueur spécifiée dans le message 1 (champ m3p2len) - Maximum total: 65535 octets (partie 1 max 48, donc partie 2 max 65487)

### Contenu déchiffré

**Partie 1:**

```
+----+----+----+----+----+----+----+----+
|                                       |
+    S (Alice static public key)        +
|    32 bytes, X25519, little-endian    |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
**Partie 2 :**

```
+----+----+----+----+----+----+----+----+
|    Block: RouterInfo (required)       |
+    Type=2, contains Alice's RI         +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
|    Block: Options (optional)          |
+    Type=1, padding parameters          +
|                                       |
+----+----+----+----+----+----+----+----+
|    Block: Padding (optional)          |
+    Type=254, random data               +
|    MUST be last block if present      |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+
```
### Fonction de dérivation de clé (KDF-3)

**Partie 1 (modèle s):**

```
h = SHA256(h || encrypted_payload_msg2)  // 32-byte ciphertext
if (msg2_padding_length > 0):
    h = SHA256(h || padding_from_msg2)

// Encrypt static key with message 2 cipher key
ciphertext = AEAD_ChaCha20_Poly1305(k_msg2, n=1, h, Alice.static_public)
h = SHA256(h || ciphertext)  // 48 bytes (32 + 16)
// h is now the associated data for message 3 part 2
```
**Partie 2 (se pattern):**

```
dh_result = X25519(Alice.static_private, Bob.ephemeral_public)
temp_key = HMAC-SHA256(ck, dh_result)
ck = HMAC-SHA256(temp_key, byte(0x01))
k = HMAC-SHA256(temp_key, ck || byte(0x02))
// k is the cipher key for message 3 part 2
// ck is retained for data phase KDF

ciphertext = AEAD_ChaCha20_Poly1305(k, n=0, h, payload)
h = SHA256(h || ciphertext)
// h is retained for SipHash KDF
```
**Nettoyage de la mémoire:**

```
// Overwrite Bob's ephemeral key after se DH
Alice.received_ephemeral = zeros(32)  // Alice side
Bob.ephemeral_public = zeros(32)       // Bob side
Bob.ephemeral_private = zeros(32)      // Bob side
```
### Notes de mise en œuvre

1. **Validation de RouterInfo (métadonnées du router)**: Bob doit vérifier la signature, l’horodatage et la cohérence des clés
2. **Correspondance des clés**: Bob doit vérifier que la clé statique d’Alice dans la partie 1 correspond à la clé dans RouterInfo
3. **Emplacement de la clé statique**: Rechercher un paramètre "s" correspondant dans le RouterAddress (adresse du router) NTCP ou NTCP2
4. **Ordre des blocs**: RouterInfo doit être en premier, Options en second (si présentes), Padding en dernier (si présent)
5. **Planification de la longueur**: Alice doit s’assurer que m3p2len dans le message 1 correspond exactement à la longueur de la partie 2
6. **Mise en tampon**: Alice doit envoyer les deux parties ensemble en un seul envoi TCP
7. **Chaînage facultatif**: Alice peut ajouter immédiatement une trame de phase de données pour plus d’efficacité

## Phase de données

Après l’achèvement de la négociation, tous les messages utilisent des trames AEAD (chiffrement authentifié avec données associées) à longueur variable avec des champs de longueur obfusqués.

### Fonction de dérivation de clés (phase de données)

**Fonction Split (Noise):**

```
// Generate transmit and receive keys
zerolen = ""  // Zero-length byte array
temp_key = HMAC-SHA256(ck, zerolen)

// Alice transmits to Bob
k_ab = HMAC-SHA256(temp_key, byte(0x01))

// Bob transmits to Alice  
k_ba = HMAC-SHA256(temp_key, k_ab || byte(0x02))

// Cleanup
ck = zeros(32)
temp_key = zeros(32)
```
**Dérivation de clé SipHash:**

```
// Generate additional symmetric key for SipHash
ask_master = HMAC-SHA256(temp_key, "ask" || byte(0x01))

// "siphash" is 7 bytes US-ASCII
temp_key2 = HMAC-SHA256(ask_master, h || "siphash")
sip_master = HMAC-SHA256(temp_key2, byte(0x01))

// Alice to Bob SipHash keys
temp_key3 = HMAC-SHA256(sip_master, zerolen)
sipkeys_ab = HMAC-SHA256(temp_key3, byte(0x01))
sipk1_ab = sipkeys_ab[0:7]   // 8 bytes, little-endian
sipk2_ab = sipkeys_ab[8:15]  // 8 bytes, little-endian
sipiv_ab = sipkeys_ab[16:23] // 8 bytes, IV

// Bob to Alice SipHash keys
sipkeys_ba = HMAC-SHA256(temp_key3, sipkeys_ab || byte(0x02))
sipk1_ba = sipkeys_ba[0:7]   // 8 bytes, little-endian
sipk2_ba = sipkeys_ba[8:15]  // 8 bytes, little-endian
sipiv_ba = sipkeys_ba[16:23] // 8 bytes, IV
```
### Structure de trame

```
+----+----+----+----+----+----+----+----+
|Obfs Len |                             |
+----+----+    ChaChaPoly Frame         +
|    Encrypted Block Data               |
+    k_ab (Alice→Bob) or k_ba (Bob→Alice)|
|    Nonce starts at 0, increments      |
+    No associated data (empty string)  +
|                                       |
~           .   .   .                   ~
|                                       |
+----+----+----+----+----+----+----+----+
|    Poly1305 MAC (16 bytes)            |
+----+----+----+----+----+----+----+----+
```
**Contraintes de trame:** - Minimum: 18 octets (2 longueur obfusquée + 0 texte en clair + 16 MAC) - Maximum: 65537 octets (2 longueur obfusquée + 65535 trame) - Recommandé: Quelques Ko par trame (minimiser la latence côté récepteur)

### Obfuscation de la longueur avec SipHash

**Objectif** : Empêcher l’identification par DPI des limites de trame

**Algorithme :**

```
// Initialization (per direction)
IV[0] = sipiv  // From KDF

// For each frame:
IV[n] = SipHash-2-4(sipk1, sipk2, IV[n-1])
Mask[n] = IV[n][0:1]  // First 2 bytes of IV
ObfuscatedLength = ActualLength XOR Mask[n]

// Send 2-byte ObfuscatedLength, then ActualLength bytes
```
**Décodage:**

```
// Receiver maintains identical IV chain
IV[n] = SipHash-2-4(sipk1, sipk2, IV[n-1])
Mask[n] = IV[n][0:1]
ActualLength = ObfuscatedLength XOR Mask[n]
// Read ActualLength bytes (includes 16-byte MAC)
```
**Notes :** - Chaînes d'IV (vecteur d'initialisation) séparées pour chaque direction (Alice→Bob et Bob→Alice) - Si SipHash renvoie uint64, utiliser les 2 octets de poids faible comme masque - Convertir uint64 en l'IV suivant sous forme d'octets little-endian

### Format de bloc

Chaque trame contient zéro ou plusieurs blocs :

```
+----+----+----+----+----+----+----+----+
|Type| Length  |       Data              |
+----+----+----+                        +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type  : 1 byte  - Block type identifier
Length: 2 bytes - Big-endian, data size (0-65516)
Data  : Variable length payload
```
**Limites de taille:** - Trame maximale : 65535 octets (y compris le MAC) - Espace maximal d'un bloc : 65519 octets (trame - MAC de 16 octets) - Taille maximale d'un bloc : 65519 octets (en-tête de 3 octets + 65516 octets de données)

### Types de blocs

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">DateTime</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Time synchronization (4-byte timestamp)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Options</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Padding parameters, dummy traffic</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo delivery/flooding</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2NP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2NP message with shortened header</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Termination</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Explicit connection close</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">224-253</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental features</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">254</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Padding</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Random padding (must be last)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">255</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Future extensions</td></tr>
  </tbody>
</table>
**Règles d’ordonnancement des blocs:** - **Message 3 partie 2**: RouterInfo (informations du router), Options (facultatif), Padding (facultatif) - AUCUN autre type - **Phase de données**: N'importe quel ordre sauf:   - Padding DOIT être le dernier bloc si présent   - Termination DOIT être le dernier bloc (sauf Padding) si présent - Plusieurs blocs I2NP autorisés par trame - Plusieurs blocs Padding NON autorisés par trame

### Type de bloc 0 : DateTime

Synchronisation de l'heure pour la détection du décalage d'horloge.

```
+----+----+----+----+----+----+----+
| 0  |    4    |     timestamp     |
+----+----+----+----+----+----+----+

Type     : 0
Length   : 4 (big-endian)
Timestamp: 4 bytes, Unix seconds (big-endian)
```
**Implémentation**: Arrondir à la seconde la plus proche pour éviter l'accumulation du biais d'horloge.

### Type de bloc 1 : Options

Paramètres de bourrage et de mise en forme du trafic.

```
+----+----+----+----+----+----+----+----+
| 1  |  size   |tmin|tmax|rmin|rmax|tdmy|
+----+----+----+----+----+----+----+----+
|tdmy|  rdmy   |  tdelay |  rdelay |    |
+----+----+----+----+----+----+----+    +
|         more_options (TBD)            |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type  : 1
Length: 12+ bytes (big-endian)
```
**Taux de bourrage** (nombre en virgule fixe 4.4, valeur/16.0): - `tmin`: Taux de bourrage minimal en émission (0.0 - 15.9375) - `tmax`: Taux de bourrage maximal en émission (0.0 - 15.9375) - `rmin`: Taux de bourrage minimal en réception (0.0 - 15.9375) - `rmax`: Taux de bourrage maximal en réception (0.0 - 15.9375)

**Exemples :** - 0x00 = 0 % de bourrage - 0x01 = 6,25 % de bourrage - 0x10 = 100 % de bourrage (rapport 1:1) - 0x80 = 800 % de bourrage (rapport 8:1)

**Trafic factice:** - `tdmy`: Maximum prêt à envoyer (2 octets, débit moyen en octets/s) - `rdmy`: Montant demandé en réception (2 octets, débit moyen en octets/s)

**Insertion de délai:** - `tdelay`: Maximum disposé à insérer (2 octets, moyenne en millisecondes) - `rdelay`: Délai demandé (2 octets, moyenne en millisecondes)

**Directives:** - Les valeurs minimales indiquent la résistance souhaitée à l'analyse de trafic - Les valeurs maximales indiquent les contraintes de bande passante - L'expéditeur doit respecter la valeur maximale du destinataire - L'expéditeur peut respecter la valeur minimale du destinataire dans les limites des contraintes - Aucun mécanisme de contrainte; les implémentations peuvent varier

### Type de bloc 2 : RouterInfo (informations du router)

Acheminement des RouterInfo (métadonnées d'un Router) pour le peuplement et l’inondation de la netDb.

```
+----+----+----+----+----+----+----+----+
| 2  |  size   |flg |    RouterInfo     |
+----+----+----+----+                   +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type : 2
Length: Flag (1 byte) + RouterInfo size
Flag : Bit 0 = flood request (1) or local store (0)
       Bits 1-7 = Reserved, set to 0
```
**Utilisation:**

**Dans le message 3 partie 2** (handshake): - Alice envoie son RouterInfo à Bob - Flood bit (bit d'inondation) généralement à 0 (stockage local) - RouterInfo n'est PAS compressé avec gzip

**En phase de données:** - L'une ou l'autre des parties peut envoyer son RouterInfo mis à jour - Flood bit = 1: Demande de distribution via floodfill (si le destinataire est floodfill) - Flood bit = 0: Stockage local netdb uniquement

**Exigences de validation:** 1. Vérifier que le type de signature est pris en charge 2. Vérifier la signature du RouterInfo 3. Vérifier que l'horodatage est dans des limites acceptables 4. Pour le handshake: Vérifier que la clé statique correspond au paramètre "s" de l'adresse NTCP2 5. Pour la phase de données: Vérifier que le hachage du router correspond au pair de la session 6. Ne diffuser que les RouterInfos avec des adresses publiées

**Remarques:** - Pas de mécanisme d'ACK (accusé de réception) (utilisez I2NP DatabaseStore avec un jeton de réponse si nécessaire) - Peut contenir des RouterInfos de tiers (usage de floodfill) - PAS compressé en gzip (contrairement à I2NP DatabaseStore)

### Type de bloc 3: Message I2NP

Message I2NP à en-tête raccourci de 9 octets.

```
+----+----+----+----+----+----+----+----+
| 3  |  size   |type|    msg_id         |
+----+----+----+----+----+----+----+----+
|   expiration  |     I2NP payload      |
+----+----+----+                        +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type      : 3
Length    : 9 + payload_size (big-endian)
Type      : 1 byte, I2NP message type
Msg_ID    : 4 bytes, big-endian, I2NP message ID
Expiration: 4 bytes, big-endian, Unix timestamp (seconds)
Payload   : I2NP message body (length = size - 9)
```
**Différences par rapport à NTCP1:** - Expiration : 4 octets (secondes) contre 8 octets (millisecondes) - Longueur : Omise (déductible de la longueur du bloc) - Somme de contrôle : Omise (AEAD assure l'intégrité) - En-tête : 9 octets contre 16 octets (réduction de 44 %)

**Fragmentation:** - Les messages I2NP NE DOIVENT PAS être fragmentés sur plusieurs blocs - Les messages I2NP NE DOIVENT PAS être fragmentés sur plusieurs trames - Plusieurs blocs I2NP sont autorisés par trame

### Type de bloc 4: Terminaison

Fermeture explicite de la connexion avec un code de motif.

```
+----+----+----+----+----+----+----+----+
| 4  |  size   |  valid_frames_recv    |
+----+----+----+----+----+----+----+----+
| (continued) |rsn |   additional_data   |
+----+----+----+----+                   +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type            : 4
Length          : 9+ bytes (big-endian)
Valid_Frames_Recv: 8 bytes, big-endian (receive nonce value)
                  0 if error in handshake phase
Reason          : 1 byte (see table below)
Additional_Data : Optional (format unspecified, for debugging)
```
**Codes motif:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Reason</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Phase</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Normal close / unspecified</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Termination received</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Idle timeout</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Router shutdown</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data phase AEAD failure</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Incompatible options</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Incompatible signature type</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Clock skew</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Padding violation</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">9</td><td style="border:1px solid var(--color-border); padding:0.5rem;">AEAD framing error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Payload format error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Message 1 error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Message 2 error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">13</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Message 3 error</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">14</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Intra-frame read timeout</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo signature verification fail</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">16</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Static key parameter mismatch</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshake</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">17</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Banned</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td></tr>
  </tbody>
</table>
**Règles:** - La terminaison DOIT être le dernier bloc qui n’est pas de remplissage dans la trame - Un seul bloc de terminaison par trame au maximum - L’émetteur devrait fermer la connexion après l’envoi - Le récepteur devrait fermer la connexion après la réception

**Gestion des erreurs :** - Erreurs de handshake : se terminent généralement par un TCP RST (pas de bloc de terminaison) - Erreurs AEAD (chiffrement authentifié avec données associées) pendant la phase de données : délai d'expiration aléatoire + lecture aléatoire, puis envoi d'une terminaison - Voir la section "AEAD Error Handling" pour les procédures de sécurité

### Type de bloc 254 : Bourrage

Bourrage aléatoire pour résister à l'analyse de trafic.

```
+----+----+----+----+----+----+----+----+
|254 |  size   |     random_data       |
+----+----+----+                        +
|                                       |
~           .   .   .                   ~
+----+----+----+----+----+----+----+----+

Type: 254
Length: 0-65516 bytes (big-endian)
Data: Cryptographically random bytes
```
**Règles :** - Le bloc de bourrage DOIT être le dernier bloc de la trame s'il est présent - Un bourrage de longueur nulle est autorisé - Un seul bloc de bourrage par trame - Les trames composées uniquement de bourrage sont autorisées - Devrait respecter les paramètres négociés du Options block (bloc d'options)

**Bourrage dans les messages 1-2:** - Hors de la trame AEAD (chiffrement authentifié avec données associées) (texte en clair) - Inclus dans la chaîne de hachage du message suivant (authentifié) - La falsification est détectée lorsque l'AEAD du message suivant échoue

**Bourrage dans Message 3+ et la phase de données:** - Dans la trame AEAD (chiffrée et authentifiée) - Utilisé pour la mise en forme du trafic et l'obfuscation de la taille

## Gestion des erreurs de l’AEAD (chiffrement authentifié avec données associées)

**Exigences de sécurité critiques :**

### Phase de négociation (Messages 1 à 3)

**Taille de message connue :** - Les tailles de messages sont prédéterminées ou spécifiées à l'avance - Un échec d'authentification AEAD est sans ambiguïté

**Réponse de Bob à l'échec du Message 1:** 1. Définir un délai d'expiration aléatoire (plage dépendante de l'implémentation, suggéré 100-500ms) 2. Lire un nombre aléatoire d'octets (plage dépendante de l'implémentation, suggéré 1KB-64KB) 3. Fermer la connexion avec TCP RST (aucune réponse) 4. Bloquer temporairement l'adresse IP source 5. Suivre les échecs répétés en vue de bannissements à long terme

**Réponse d'Alice à l'échec du message 2:** 1. Fermer la connexion immédiatement avec TCP RST 2. Ne pas répondre à Bob

**Réponse de Bob à l'échec du message 3:** 1. Fermer immédiatement la connexion avec un TCP RST 2. Aucune réponse à Alice

### Phase de données

**Taille du message obfusquée:** - Le champ de longueur est obfusqué par SipHash - Une longueur invalide ou un échec AEAD (chiffrement authentifié avec données associées) peut indiquer:   - Sondage par un attaquant   - Corruption des données réseau   - IV SipHash désynchronisé   - Pair malveillant

**Réponse à une erreur AEAD ou de longueur:** 1. Définir un délai d'expiration aléatoire (recommandé : 100-500 ms) 2. Lire un nombre aléatoire d'octets (recommandé : 1 Ko-64 Ko) 3. Envoyer un bloc de terminaison avec le code de raison 4 (échec AEAD) ou 9 (erreur de trame) 4. Fermer la connexion

**Prévention d'un oracle de déchiffrement:** - Ne jamais révéler le type d'erreur au pair avant l'expiration d'un délai d'attente aléatoire - Ne jamais omettre la validation de la longueur avant la vérification AEAD - Traiter une longueur invalide de la même manière qu'un échec AEAD - Utiliser un chemin de gestion des erreurs identique pour les deux erreurs

**Considérations d’implémentation:** - Certaines implémentations peuvent continuer après des erreurs AEAD si elles sont peu fréquentes - Mettre fin après des erreurs répétées (seuil suggéré: 3 à 5 erreurs par heure) - Équilibrer la reprise après erreur et la sécurité

## RouterInfo (fiche d'information du router) publié

### Format d'adresse du router

La prise en charge de NTCP2 est annoncée via des entrées RouterAddress (adresse du router) publiées avec des options spécifiques.

**Style de transport:** - `"NTCP2"` - NTCP2 uniquement sur ce port - `"NTCP"` - NTCP et NTCP2 tous deux sur ce port (détection automatique)   - **Remarque**: la prise en charge de NTCP (v1) a été supprimée dans la version 0.9.50 (mai 2021)   - Le style "NTCP" est désormais obsolète ; utilisez "NTCP2"

### Options requises

**Toutes les adresses NTCP2 publiées:**

1. **`host`** - Adresse IP (IPv4 ou IPv6) ou nom d'hôte
   - Format: notation IP standard ou nom de domaine
   - Peut être omis pour les routers uniquement sortants ou cachés

2. **`port`** - Numéro de port TCP
   - Format : entier, 1-65535
   - Peut être omis pour les routers uniquement sortants ou cachés

3. **`s`** - Clé publique statique (X25519, algorithme de courbe elliptique)
   - Format: encodé en Base64, 44 caractères
   - Encodage: alphabet Base64 d'I2P
   - Source: clé publique X25519 de 32 octets, little-endian (octet de poids faible en premier)

4. **`i`** - Vecteur d'initialisation pour AES
   - Format: Encodé en Base64, 24 caractères
   - Encodage: alphabet Base64 d'I2P
   - Source: IV de 16 octets, big-endian

5. **`v`** - Version du protocole
   - Format: entier ou entiers séparés par des virgules
   - Actuel: `"2"`
   - Futur: `"2,3"` (doit être en ordre numérique)

**Options facultatives:**

6. **`caps`** - Capacités (depuis la version 0.9.50)
   - Format: chaîne de caractères indiquant les capacités
   - Valeurs:
     - `"4"` - capacité sortante IPv4
     - `"6"` - capacité sortante IPv6
     - `"46"` - IPv4 et IPv6 (ordre recommandé)
   - Pas nécessaire si `host` est publié
   - Utile pour les routers cachés/derrière un pare-feu

7. **`cost`** - Priorité de l'adresse
   - Format: entier, 0-255
   - Valeurs plus faibles = priorité plus élevée
   - Suggéré: 5-10 pour les adresses normales
   - Suggéré: 14 pour les adresses non publiées

### Exemples d'entrées RouterAddress

**Adresse IPv4 publiée:**

```
<Address cost="5">
  <transport_style>NTCP2</transport_style>
  <options>
    <host>192.0.2.1</host>
    <port>8887</port>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <i>MDEyMzQ1Njc4OUFCQ0RFRg==</i>
    <v>2</v>
  </options>
</Address>
```
**Router masqué (sortant uniquement):**

```
<Address cost="14">
  <transport_style>NTCP2</transport_style>
  <options>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <v>2</v>
    <caps>4</caps>
  </options>
</Address>
```
**Router à double pile:**

```
<!-- IPv4 Address -->
<Address cost="5">
  <transport_style>NTCP2</transport_style>
  <options>
    <host>192.0.2.1</host>
    <port>8887</port>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <i>MDEyMzQ1Njc4OUFCQ0RFRg==</i>
    <v>2</v>
  </options>
</Address>

<!-- IPv6 Address (same keys, same port) -->
<Address cost="5">
  <transport_style>NTCP2</transport_style>
  <options>
    <host>2001:db8::1</host>
    <port>8887</port>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <i>MDEyMzQ1Njc4OUFCQ0RFRg==</i>
    <v>2</v>
  </options>
</Address>
```
**Règles importantes:** - Plusieurs adresses NTCP2 avec le **même port** DOIVENT utiliser des valeurs `s`, `i` et `v` **identiques** - Des ports différents peuvent utiliser des clés différentes - Les routers à double pile devraient publier des adresses IPv4 et IPv6 séparées

### Adresse NTCP2 non publiée

**Pour les routers sortants uniquement :**

Si un router n'accepte pas les connexions NTCP2 entrantes mais établit des connexions sortantes, il DOIT tout de même publier une RouterAddress (adresse du routeur) avec:

```xml
<Address cost="14">
  <transport_style>NTCP2</transport_style>
  <options>
    <s>9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=</s>
    <v>2</v>
  </options>
</Address>
```
**Objectif:** - Permet à Bob de valider la clé statique d'Alice pendant la négociation - Nécessaire à la vérification de RouterInfo du message 3 partie 2 - Aucun `i`, `host` ni `port` requis (sortant uniquement)

**Alternative:** - Ajouter `s` et `v` à l'adresse "NTCP" ou SSU déjà publiée

### Rotation de la clé publique et de l'IV (vecteur d'initialisation)

**Politique de sécurité critique :**

**Règles générales :** 1. **Ne jamais effectuer une rotation pendant que le router est en cours d’exécution** 2. **Conserver de manière persistante la clé et l’IV (vecteur d’initialisation)** entre les redémarrages 3. **Suivre le temps d’arrêt précédent** pour déterminer l’éligibilité à la rotation

**Temps d'arrêt minimal avant la rotation:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Router Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Min Downtime</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Reason</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Published NTCP2 address</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>1 month</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Many routers cache RouterInfo</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Published SSU only (no NTCP2)</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>1 day</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Moderate caching</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">No published addresses (hidden)</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>2 hours</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimal impact</td></tr>
  </tbody>
</table>
**Déclencheurs supplémentaires:** - Changement d'adresse IP locale: Peut entraîner une rotation indépendamment du temps d'arrêt - Router "rekey" (nouveau Router Hash): Générer de nouvelles clés

**Justification:** - Empêche d'exposer les heures de redémarrage via des changements de clés - Permet aux RouterInfos mis en cache d'expirer naturellement - Maintient la stabilité du réseau - Réduit les tentatives de connexion échouées

**Implémentation:** 1. Stocker de manière persistante la clé, le vecteur d'initialisation (IV) et l'horodatage du dernier arrêt 2. Au démarrage, calculer downtime = current_time - last_shutdown 3. Si downtime > minimum pour le type de router, peut procéder à une rotation 4. Si l'IP a changé ou en cas de renouvellement des clés, peut procéder à une rotation 5. Sinon, réutiliser la clé et l'IV précédents

**Rotation de l'IV:** - Soumise aux mêmes règles que la rotation de clé - Présente uniquement dans les adresses publiées (pas dans les routers cachés) - Recommandé de changer l'IV chaque fois que la clé change

## Détection de version

**Contexte:** Lorsque `transportStyle="NTCP"` (ancien), Bob prend en charge à la fois NTCP v1 et v2 sur le même port et doit détecter automatiquement la version du protocole.

**Algorithme de détection:**

```
1. Wait for at least 64 bytes (minimum NTCP2 message 1 size)

2. If received ≥ 288 bytes:
   → Connection is NTCP version 1 (NTCP1 message 1 is 288 bytes)

3. If received < 288 bytes:
   
   Option A (conservative, pre-NTCP2 majority):
   a. Wait additional short time (e.g., 100-500ms)
   b. If total received ≥ 288 bytes → NTCP1
   c. Otherwise → Attempt NTCP2 decode
   
   Option B (aggressive, post-NTCP2 majority):
   a. Attempt NTCP2 decode immediately:
      - Decrypt first 32 bytes (X key) with AES-256-CBC
      - Verify valid X25519 point (X[31] & 0x80 == 0)
      - Verify AEAD frame
   b. If decode succeeds → NTCP2
   c. If decode fails → Wait for more data or NTCP1
```
**Vérification rapide du MSB (bit de poids fort) :** - Avant le déchiffrement AES, vérifiez : `encrypted_X[31] & 0x80 == 0` - Les clés X25519 valides ont le bit de poids fort à zéro - Un échec indique probablement NTCP1 (ou une attaque) - Implémentez une résistance au sondage (temporisation aléatoire + lecture) en cas d'échec

**Exigences d'implémentation:**

1. **Responsabilité d'Alice :**
   - Lors de la connexion à une adresse "NTCP", limiter le message 1 à 287 octets maximum
   - Mettre en mémoire tampon et vider l'intégralité du message 1 en une seule fois
   - Augmente la probabilité d'une livraison en un seul paquet TCP

2. **Responsabilités de Bob :**
   - Mettre en mémoire tampon les données reçues avant de déterminer la version
   - Implémenter une gestion correcte des délais d’expiration
   - Utiliser TCP_NODELAY pour une détection rapide de la version
   - Mettre en mémoire tampon puis vider l’intégralité du message 2 en une seule fois après détection de la version

**Considérations de sécurité :** - Attaques par segmentation : Bob doit être résistant à la segmentation TCP - Attaques de sondage : mettre en œuvre des délais aléatoires et des lectures d’octets en cas d’échec - Prévention du déni de service (DoS) : limiter les connexions en attente simultanées - Délais d’expiration de lecture : à la fois par lecture et au total ("slowloris" protection)

## Directives sur le décalage d’horloge

**Champs d'horodatage:** - Message 1: `tsA` (horodatage d'Alice) - Message 2: `tsB` (horodatage de Bob) - Message 3+: Blocs DateTime (date/heure) optionnels

**Décalage maximal (D):** - Typique : **±60 secondes** - Configurable selon l’implémentation - Un décalage > D est généralement fatal

### Traitement par Bob (Message 1)

```
1. Receive tsA from Alice
2. skew = tsA - current_time
3. If |skew| > D:
   a. Still send message 2 (allows Alice to calculate skew)
   b. Include tsB in message 2
   c. Do NOT initiate handshake completion
   d. Optionally: Temporary ban Alice's IP
   e. After message 2 sent, close connection

4. If |skew| ≤ D:
   a. Continue handshake normally
```
**Justification:** L'envoi du message 2, même en cas de décalage d'horloge, permet à Alice de diagnostiquer des problèmes d'horloge.

### Traitement par Alice (Message 2)

```
1. Receive tsB from Bob
2. RTT = (current_time_now - tsA_sent)
3. adjusted_skew = (tsB - current_time_now) - (RTT / 2)
4. If |adjusted_skew| > D:
   a. Close connection immediately
   b. If local clock suspect: Adjust clock or use external time source
   c. If Bob's clock suspect: Temporary ban Bob
   d. Log for operator review
5. If |adjusted_skew| ≤ D:
   a. Continue handshake normally
   b. Optionally: Track skew for time synchronization
```
**Ajustement du RTT (Round-Trip Time, temps aller-retour):** - Soustraire la moitié du RTT du décalage calculé - Tient compte du délai de propagation sur le réseau - Estimation du décalage plus précise

### Traitement par Bob (Message 3)

```
1. If message 3 received (unlikely if skew exceeded in message 1)
2. Recalculate skew = tsA_received - current_time
3. If |adjusted_skew| > D:
   a. Send termination block (reason code 7: clock skew)
   b. Close connection
   c. Ban Alice for period (e.g., 1-24 hours)
```
### Synchronisation de l'heure

**Blocs DateTime (phase de données):** - Envoyer périodiquement un bloc DateTime (type 0) - Le récepteur peut l'utiliser pour l'ajustement de l'horloge - Arrondir l'horodatage à la seconde la plus proche (pour éviter un biais)

**Sources de temps externes:** - NTP (Network Time Protocol) - Synchronisation de l'horloge système - Temps de consensus du réseau I2P

**Stratégies d’ajustement de l’horloge:** - Si l’horloge locale est incorrecte : ajuster l’heure du système ou utiliser un décalage - Si les horloges des pairs sont constamment incorrectes : signaler un problème côté pair - Suivre les statistiques de dérive d’horloge pour la surveillance de la santé du réseau

## Propriétés de sécurité

### Confidentialité persistante

**Réalisé grâce à :** - Échange de clés Diffie-Hellman éphémère (X25519) - Trois opérations DH : es, ee, se (schéma Noise XK) - Clés éphémères détruites après l'achèvement de la négociation (handshake)

**Progression de la confidentialité :** - Message 1 : Niveau 2 (confidentialité persistante en cas de compromission de l'expéditeur) - Message 2 : Niveau 1 (destinataire éphémère) - Message 3+ : Niveau 5 (forte confidentialité persistante)

**Perfect Forward Secrecy (confidentialité persistante):** - La compromission de clés statiques à long terme ne révèle PAS les anciennes clés de session - Chaque session utilise des clés éphémères uniques - Les clés privées éphémères ne sont jamais réutilisées - Nettoyage de la mémoire après la négociation de clés

**Limitations :** - Message 1 vulnérable si la clé statique de Bob est compromise (mais confidentialité persistante en cas de compromission d'Alice) - Des attaques par rejeu sont possibles pour le message 1 (atténuées par un horodatage et un cache anti-rejeu)

### Authentification

**Authentification mutuelle :** - Alice authentifiée par une clé statique dans le message 3 - Bob authentifié par la possession de la clé privée statique (implicite suite à un échange initial réussi)

**Résistance à la Key Compromise Impersonation (usurpation d'identité après compromission de clé, KCI):** - Niveau d'authentification 2 (résistant aux attaques KCI) - L'attaquant ne peut pas usurper l'identité d'Alice même avec la clé privée statique d'Alice (sans la clé éphémère d'Alice) - L'attaquant ne peut pas usurper l'identité de Bob même avec la clé privée statique de Bob (sans la clé éphémère de Bob)

**Vérification de la clé statique:** - Alice connaît à l'avance la clé statique de Bob (à partir de RouterInfo) - Bob vérifie que la clé statique d'Alice correspond à RouterInfo dans le message 3 - Empêche les attaques de type « man-in-the-middle »

### Résistance à l'analyse du trafic

**Contre-mesures DPI (inspection profonde des paquets):** 1. **Obfuscation AES:** Clés éphémères chiffrées, aspect aléatoire 2. **Obfuscation de la longueur avec SipHash:** Les longueurs de trame ne sont pas en clair 3. **Bourrage aléatoire:** Tailles de message variables, aucun motif fixe 4. **Trames chiffrées:** Toute la charge utile est chiffrée avec ChaCha20

**Prévention des attaques par rejeu :** - Validation de l'horodatage (±60 secondes) - Cache anti-rejeu des clés éphémères (durée de vie 2*D) - Les incréments de nonce (nombre utilisé une seule fois) empêchent le rejeu de paquets au sein de la session

**Résistance au sondage:** - Temporisations aléatoires en cas d'échecs AEAD (chiffrement authentifié avec données associées) - Lectures d'octets aléatoires avant la fermeture de la connexion - Aucune réponse en cas d'échecs du handshake (établissement de la connexion) - Mise sur liste noire des IP en cas d'échecs répétés

**Directives de bourrage:** - Messages 1-2: Bourrage en clair (authentifié) - Message 3+: Bourrage chiffré à l'intérieur des trames AEAD - Paramètres de bourrage négociés (Options block) - Trames uniquement de bourrage autorisées

### Atténuation des attaques par déni de service

**Limites de connexion:** - Nombre maximal de connexions actives (dépendant de l’implémentation) - Nombre maximal de handshakes (initialisation de connexion) en attente (p. ex., 100-1000) - Limites de connexion par IP (p. ex., 3-10 simultanées)

**Protection des ressources:** - Limitation du débit des opérations DH (coûteuses) - Temporisations de lecture par socket et totales - Protection "Slowloris" (limites de temps totales) - Mise en liste noire des IP en cas d'abus

**Rejet rapide:** - Non-correspondance de l'ID de réseau → fermeture immédiate - Point X25519 invalide → vérification rapide du bit de poids fort (MSB) avant déchiffrement - Horodatage hors limites → fermeture sans calcul - Échec de l'AEAD → aucune réponse, délai aléatoire

**Résistance au sondage:** - Temporisation aléatoire: 100-500ms (dépend de l’implémentation) - Lecture aléatoire: 1KB-64KB (dépend de l’implémentation) - Aucune information d’erreur transmise à l’attaquant - Fermeture avec TCP RST (sans handshake FIN)

### Sécurité cryptographique

**Algorithmes:** - **X25519**: sécurité de 128 bits, DH à courbe elliptique (Curve25519) - **ChaCha20**: chiffrement en flux à clé de 256 bits - **Poly1305**: MAC sécurisé au sens de la théorie de l'information - **SHA-256**: résistance aux collisions de 128 bits, résistance aux préimages de 256 bits - **HMAC-SHA256**: PRF (fonction pseudo-aléatoire) pour la dérivation de clés

**Tailles des clés:** - Clés statiques: 32 octets (256 bits) - Clés éphémères: 32 octets (256 bits) - Clés de chiffrement: 32 octets (256 bits) - MAC: 16 octets (128 bits)

**Problèmes connus:** - La réutilisation du nonce (valeur aléatoire à usage unique) ChaCha20 est catastrophique (empêchée par l'incrément du compteur) - X25519 présente des problèmes liés aux petits sous-groupes (atténués par la validation de la courbe) - SHA-256 est théoriquement vulnérable à l’extension de longueur (non exploitable dans HMAC)

**Aucune vulnérabilité connue (à ce jour, octobre 2025):** - Noise Protocol Framework largement analysé - ChaCha20-Poly1305 déployé dans TLS 1.3 - X25519 standard des protocoles modernes - Aucune attaque pratique connue contre la construction

## Références

### Spécifications principales

- **[Spécification NTCP2](/docs/specs/ntcp2/)** - Spécification officielle d’I2P
- **[Proposition 111](/proposals/111-ntcp-2/)** - Document de conception original avec justification
- **[Noise Protocol Framework](https://noiseprotocol.org/noise.html)** (cadre de protocoles Noise) - Révision 33 (2017-10-04)

### Normes cryptographiques

- **[RFC 7748](https://www.rfc-editor.org/rfc/rfc7748)** - Courbes elliptiques pour la sécurité (X25519)
- **[RFC 7539](https://www.rfc-editor.org/rfc/rfc7539)** - ChaCha20 et Poly1305 pour les protocoles de l'IETF
- **[RFC 8439](https://www.rfc-editor.org/rfc/rfc8439)** - ChaCha20-Poly1305 (rend obsolète la RFC 7539)
- **[RFC 2104](https://www.rfc-editor.org/rfc/rfc2104)** - HMAC : hachage à clé pour l'authentification des messages
- **[SipHash](https://www.131002.net/siphash/)** - SipHash-2-4 pour les applications de fonctions de hachage

### Spécifications I2P connexes

- **[Spécification I2NP](/docs/specs/i2np/)** - Format des messages du protocole réseau I2P
- **[Structures communes](/docs/specs/common-structures/)** - Formats de RouterInfo et RouterAddress
- **[Transport SSU](/docs/legacy/ssu/)** - Transport UDP (d'origine, maintenant SSU2)
- **[Proposition 147](/proposals/147-transport-network-id-check/)** - Vérification de l'ID de réseau de transport (0.9.42)

### Références d’implémentation

- **[I2P Java](https://github.com/i2p/i2p.i2p)** - Implémentation de référence (Java)
- **[i2pd](https://github.com/PurpleI2P/i2pd)** - Implémentation en C++
- **[Notes de version I2P](/blog/)** - Historique des versions et mises à jour

### Contexte historique

- **[Station-To-Station Protocol (STS)](https://en.wikipedia.org/wiki/Station-to-Station_protocol)** - Source d'inspiration pour le Noise framework (cadre de protocoles cryptographiques)
- **[obfs4](https://gitlab.com/yawning/obfs4)** - Pluggable transport (mécanisme de transport modulaire) (précédent d'obfuscation de longueur par SipHash)

## Directives d’implémentation

### Exigences obligatoires

**À des fins de conformité :**

1. **Implémenter le handshake complet:**
   - Prendre en charge les trois messages avec des chaînes de KDF correctes
   - Valider tous les tags AEAD
   - Vérifier que les points X25519 sont valides

2. **Implémenter la phase de données:**
   - Obfuscation de la longueur avec SipHash (dans les deux sens)
   - Tous les types de blocs : 0 (DateTime), 1 (Options), 2 (RouterInfo), 3 (I2NP), 4 (Termination), 254 (Padding)
   - Gestion correcte des nonces (nombre utilisé une seule fois) (compteurs séparés)

3. **Fonctionnalités de sécurité:**
   - Prévention des attaques par rejeu (mise en cache des clés éphémères pendant 2*D)
   - Validation des horodatages (±60 secondes par défaut)
   - Remplissage aléatoire dans les messages 1-2
   - Gestion des erreurs AEAD avec délais d'attente aléatoires

4. **Publication de RouterInfo:**
   - Publier la clé statique ("s"), l’IV (vecteur d'initialisation) ("i") et la version ("v")
   - Effectuer la rotation des clés conformément à la politique
   - Prendre en charge le champ des capacités ("caps") pour les routers cachés

5. **Compatibilité réseau:**
   - Prendre en charge le champ d'ID réseau (actuellement 2 pour le réseau principal)
   - Interopérer avec les implémentations Java et i2pd existantes
   - Gérer IPv4 et IPv6

### Pratiques recommandées

**Optimisation des performances:**

1. **Stratégie de mise en tampon :**
   - Émettre chaque message en une seule fois (messages 1, 2, 3)
   - Utiliser TCP_NODELAY pour les messages de handshake (phase d'initialisation de la connexion)
   - Regrouper plusieurs blocs de données dans une seule trame
   - Limiter la taille des trames à quelques Ko (minimiser la latence côté récepteur)

2. **Gestion des connexions:**
   - Réutiliser les connexions lorsque c'est possible
   - Mettre en place un pool de connexions
   - Surveiller la santé des connexions (DateTime blocks)

3. **Gestion de la mémoire :**
   - Mettre à zéro les données sensibles après utilisation (clés éphémères, résultats DH)
   - Limiter les handshakes (échanges d'initialisation) simultanés (prévention des attaques DoS)
   - Utiliser des pools de mémoire pour les allocations fréquentes

**Renforcement de la sécurité :**

1. **Résistance au sondage:**
   - Temporisations aléatoires: 100-500ms
   - Lectures d'octets aléatoires: 1KB-64KB
   - Mise sur liste noire des adresses IP en cas d'échecs répétés
   - Aucun détail d'erreur communiqué aux pairs

2. **Limites de ressources :**
   - Nombre maximal de connexions par IP : 3-10
   - Nombre maximal de handshakes (négociation initiale) en attente : 100-1000
   - Délais d'expiration de lecture : 30-60 secondes par opération
   - Délai d'expiration total de connexion : 5 minutes pour le handshake

3. **Gestion des clés:**
   - Stockage persistant de la clé statique et de l’IV (vecteur d’initialisation)
   - Génération aléatoire sécurisée (RNG cryptographique)
   - Appliquer strictement les politiques de rotation
   - Ne jamais réutiliser les clés éphémères

**Surveillance et diagnostics:**

1. **Métriques:**
   - Taux de réussite/échec du handshake (établissement de connexion)
   - Taux d'erreur AEAD (chiffrement authentifié avec données associées)
   - Distribution du décalage d'horloge
   - Statistiques de durée de connexion

2. **Journalisation:**
   - Consigner les échecs de handshake (négociation initiale) avec des codes de cause
   - Consigner les événements de décalage d'horloge
   - Consigner les adresses IP bannies
   - Ne jamais consigner de key material (informations sensibles de clé)

3. **Tests:**
   - Tests unitaires des chaînes de KDF (fonction de dérivation de clé)
   - Tests d'intégration avec d'autres implémentations
   - Fuzzing (tests par données aléatoires) pour le traitement des paquets
   - Tests de charge pour la résistance aux attaques par déni de service (DoS)

### Pièges courants

**Erreurs critiques à éviter :**

1. **Réutilisation du nonce (nombre utilisé une seule fois):**
   - Ne jamais réinitialiser le compteur de nonce en cours de session
   - Utiliser des compteurs distincts pour chaque direction
   - Terminer avant d'atteindre 2^64 - 1

2. **Rotation des clés :**
   - Ne jamais effectuer une rotation des clés pendant que le router est en cours d'exécution
   - Ne jamais réutiliser des clés éphémères entre les sessions
   - Respecter les règles de temps d'arrêt minimal

3. **Gestion des horodatages:**
   - Ne jamais accepter des horodatages expirés
   - Toujours ajuster en fonction du RTT lors du calcul du décalage
   - Arrondir les horodatages DateTime à la seconde près

4. **Erreurs AEAD (chiffrement authentifié avec données associées):**
   - Ne jamais révéler le type d’erreur à un attaquant
   - Toujours utiliser une temporisation aléatoire avant de fermer
   - Traiter une longueur non valide comme un échec AEAD

5. **Bourrage:**
   - Ne jamais envoyer de bourrage en dehors des limites négociées
   - Toujours placer le bloc de bourrage en dernier
   - Ne jamais inclure plusieurs blocs de bourrage par trame

6. **RouterInfo:**
   - Toujours vérifier que la clé statique correspond au RouterInfo
   - Ne jamais flood (diffuser massivement) des RouterInfos sans adresses publiées
   - Toujours valider les signatures

### Méthodologie de test

**Tests unitaires:**

1. **Primitives cryptographiques:**
   - Vecteurs de test pour X25519, ChaCha20, Poly1305, SHA-256
   - Vecteurs de test pour HMAC-SHA256
   - Vecteurs de test pour SipHash-2-4

2. **Chaînes KDF:**
   - Tests à réponse connue pour les trois messages
   - Vérifier la propagation de la clé de chaînage
   - Tester la génération de l'IV (vecteur d'initialisation) SipHash

3. **Analyse des messages:**
   - Décodage de messages valides
   - Rejet des messages invalides
   - Cas limites (vide, taille maximale)

**Tests d'intégration:**

1. **Handshake (négociation initiale):**
   - Échange en trois messages réussi
   - Rejet en cas de décalage d'horloge
   - Détection d'attaque par rejeu
   - Rejet de clé invalide

2. **Phase de données:**
   - Transfert de messages I2NP
   - Échange de RouterInfo
   - Gestion du bourrage (padding)
   - Messages de terminaison

3. **Interopérabilité:**
   - Tester avec Java I2P
   - Tester avec i2pd
   - Tester IPv4 et IPv6
   - Tester les routers publiés et cachés

**Tests de sécurité:**

1. **Tests négatifs :**
   - Étiquettes AEAD non valides
   - Messages rejoués
   - Attaques par décalage d’horloge
   - Trames mal formées

2. **Tests de DoS:**
   - Inondation de connexions
   - Attaques Slowloris
   - Épuisement du CPU (DH (Diffie-Hellman) excessif)
   - Épuisement de la mémoire

3. **Fuzzing (tests aléatoires):**
   - Messages de handshake aléatoires
   - Trames aléatoires pour la phase de données
   - Types et tailles de blocs aléatoires
   - Valeurs cryptographiques invalides

### Migration depuis NTCP

**Pour la prise en charge NTCP héritée (désormais supprimée):**

NTCP (version 1) a été supprimé dans I2P 0.9.50 (mai 2021). Toutes les implémentations actuelles doivent prendre en charge NTCP2. Notes historiques :

1. **Période de transition (2018-2021):**
   - 0.9.36: NTCP2 introduit (désactivé par défaut)
   - 0.9.37: NTCP2 activé par défaut
   - 0.9.40: NTCP déprécié
   - 0.9.50: NTCP supprimé

2. **Détection de version:**
   - Le transportStyle "NTCP" indiquait que les deux versions étaient prises en charge
   - Le transportStyle "NTCP2" indiquait uniquement NTCP2
   - Détection automatique via la taille du message (287 vs 288 octets)

3. **État actuel:**
   - Tous les routers doivent prendre en charge NTCP2
   - Le transportStyle "NTCP" est obsolète
   - Utiliser exclusivement le transportStyle "NTCP2"

## Annexe A : Noise XK Pattern (schéma de poignée de main XK du framework Noise)

**Modèle Noise XK standard:**

```
XK(s, rs):
  <- s
  ...
  -> e, es
  <- e, ee
  -> s, se
```
**Interprétation:**

- `<-` : Message du répondeur (Bob) à l'initiateur (Alice)
- `->` : Message de l'initiateur (Alice) au répondeur (Bob)
- `s` : Clé statique (clé d'identité à long terme)
- `rs` : Clé statique distante (clé statique du pair, connue à l'avance)
- `e` : Clé éphémère (spécifique à la session, générée à la demande)
- `es` : DH éphémère–statique (éphémère d'Alice × statique de Bob)
- `ee` : DH éphémère–éphémère (éphémère d'Alice × éphémère de Bob)
- `se` : DH statique–éphémère (statique d'Alice × éphémère de Bob)

**Séquence d'accord de clés:**

1. **Pré-message:** Alice connaît la clé publique statique de Bob (provenant de RouterInfo)
2. **Message 1:** Alice envoie une clé éphémère, effectue es DH (échange Diffie-Hellman éphémère-statique)
3. **Message 2:** Bob envoie une clé éphémère, effectue ee DH
4. **Message 3:** Alice révèle sa clé statique, effectue se DH

**Propriétés de sécurité:**

- Alice authentifiée : Oui (par le message 3)
- Bob authentifié : Oui (par la possession de la clé privée statique)
- Confidentialité persistante : Oui (clés éphémères détruites)
- Résistance KCI (Key Compromise Impersonation, usurpation par compromission de clé) : Oui (niveau d'authentification 2)

## Annexe B : Encodage Base64

**Alphabet Base64 d'I2P:**

```
ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-~
```
**Différences par rapport au Base64 standard:** - Caractères 62-63: `-~` au lieu de `+/` - Remplissage: identique (`=`) ou omis selon le contexte

**Utilisation dans NTCP2:** - Clé statique ("s"): 32 octets → 44 caractères (sans remplissage) - IV ("i"): 16 octets → 24 caractères (sans remplissage)

**Exemple d'encodage :**

```python
# 32-byte static key (hex): 
# f4489e1bb0597b39ca6cbf5ad9f5f1f09043e02d96cb9aa6a63742b3462429aa

# I2P Base64 encoded:
# 9EjeG7BZeznKbL9a2fXx8JBDPgLZbLmKbqY3QrNGJCo=
```
## Annexe C: Analyse des captures de paquets

**Identification du trafic NTCP2:**

1. **Établissement de la connexion TCP:**
   - Séquence TCP standard SYN, SYN-ACK, ACK
   - Port de destination généralement 8887 ou similaire

2. **Message 1 (SessionRequest — demande de session):**
   - Premières données applicatives envoyées par Alice
   - 80-65535 octets (généralement quelques centaines)
   - Semble aléatoire (clé éphémère chiffrée en AES)
   - 287 octets max si connexion à une adresse "NTCP"

3. **Message 2 (SessionCreated):**
   - Réponse de Bob
   - 80-65535 octets (généralement quelques centaines)
   - Semble également aléatoire

4. **Message 3 (SessionConfirmed — confirmation de session):**
   - Provenant d’Alice
   - 48 octets + variable (taille de RouterInfo + bourrage)
   - En général 1-4 Ko

5. **Phase de données:**
   - Trames de longueur variable
   - Champ de longueur obfusqué (semble aléatoire)
   - Charge utile chiffrée
   - Le bourrage rend la taille imprévisible

**Évasion du DPI:** - Pas d'en-têtes en clair - Pas de motifs fixes - Champs de longueur obfusqués - Le remplissage aléatoire met en échec les heuristiques fondées sur la taille

**Comparaison avec NTCP :** - Le message 1 NTCP fait toujours 288 octets (identifiable) - La taille du message 1 NTCP2 varie (non identifiable) - NTCP présentait des schémas reconnaissables - NTCP2 est conçu pour résister à l’inspection approfondie des paquets (DPI)

## Annexe D : Historique des versions

**Principaux jalons:**

- **0.9.36** (23 août 2018): NTCP2 introduit, désactivé par défaut
- **0.9.37** (4 octobre 2018): NTCP2 activé par défaut
- **0.9.40** (20 mai 2019): NTCP déprécié
- **0.9.42** (27 août 2019): Champ Network ID ajouté (Proposition 147)
- **0.9.50** (17 mai 2021): NTCP supprimé, prise en charge des capacités ajoutée
- **2.10.0** (9 septembre 2025): Dernière version stable

**Stabilité du protocole :** - Aucune modification non rétrocompatible depuis la 0.9.50 - Améliorations continues de la résistance aux attaques de sondage - Accent sur les performances et la fiabilité - Cryptographie post-quantique en développement (désactivée par défaut)

**Statut actuel des transports :** - NTCP2: Transport TCP obligatoire - SSU2: Transport UDP obligatoire - NTCP (v1): Supprimé - SSU (v1): Supprimé
