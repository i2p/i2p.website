---
title: "Spécification du chiffrement ECIES-X25519-AEAD-Ratchet"
description: "Schéma de chiffrement intégré à courbes elliptiques pour I2P (X25519 + AEAD)"
slug: "ecies"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
toc: true
---

## Vue d'ensemble

### Objectif

ECIES-X25519-AEAD-Ratchet est le protocole moderne de chiffrement de bout en bout d’I2P, remplaçant l’ancien système ElGamal/AES+SessionTags. Il offre la confidentialité persistante (PFS), un chiffrement authentifié et des améliorations significatives en matière de performances et de sécurité.

### Améliorations clés par rapport à ElGamal/AES+SessionTags

- **Clés plus petites** : Clés de 32 octets contre clés publiques ElGamal de 256 octets (réduction de 87,5 %)
- **Confidentialité persistante** : Obtenue via DH ratcheting (mécanisme de cliquet Diffie-Hellman) (non disponible dans l'ancien protocole)
- **Cryptographie moderne** : X25519 DH, ChaCha20-Poly1305 AEAD, SHA-256
- **Chiffrement authentifié** : Authentification intégrée via la construction AEAD (chiffrement authentifié avec données associées)
- **Protocole bidirectionnel** : Sessions entrantes/sortantes appariées, par opposition à l'ancien protocole unidirectionnel
- **Étiquettes efficaces** : Étiquettes de session de 8 octets contre étiquettes de 32 octets (réduction de 75 %)
- **Obfuscation du trafic** : L'encodage Elligator2 rend les handshakes (négociation initiale) indiscernables du trafic aléatoire

### Statut du déploiement

- **Publication initiale**: Version 0.9.46 (25 mai 2020)
- **Déploiement sur le réseau**: Achevé en 2020
- **État actuel**: Mature, largement déployé (plus de 5 ans en production)
- **Prise en charge du router**: Version 0.9.46 ou supérieure requise
- **Exigences de Floodfill**: Adoption proche de 100 % pour les recherches chiffrées

### État de l’implémentation

**Entièrement implémentés:** - messages New Session (NS) avec liaison - messages New Session Reply (NSR) - messages Existing Session (ES) - mécanisme de ratchet (à cliquet) DH - mécanismes à cliquet pour l’étiquette de session et la clé symétrique - blocs DateTime, NextKey, ACK, ACK Request, Garlic Clove (élément « gousse » du schéma garlic d’I2P), et de bourrage

**Non implémenté (à compter de la version 0.9.50) :** - Bloc MessageNumbers (type 6) - Bloc d’options (type 5) - Bloc de terminaison (type 4) - Réponses automatiques au niveau du protocole - Zero static key mode (mode à clé statique nulle) - Sessions de multidiffusion

**Remarque**: L'état d'implémentation pour les versions 1.5.0 à 2.10.0 (2021-2025) nécessite une vérification, certaines fonctionnalités ayant peut-être été ajoutées.

---

## Fondements du protocole

### Cadre de protocoles Noise

ECIES-X25519-AEAD-Ratchet est fondé sur le [Noise Protocol Framework](https://noiseprotocol.org/) (révision 34, 2018-07-11), en particulier le modèle de poignée de main **IK** (Interactif, clé statique distante connue) avec des extensions spécifiques à I2P.

### Identifiant du protocole Noise

```
Noise_IKelg2+hs2_25519_ChaChaPoly_SHA256
```
**Composants de l’identifiant:** - `Noise` - Cadre de base - `IK` - Modèle de poignée de main interactive avec clé statique distante connue - `elg2` - Encodage Elligator2 pour des clés éphémères (extension I2P) - `+hs2` - MixHash appelée avant le deuxième message pour y intégrer le tag (extension I2P) - `25519` - Fonction Diffie-Hellman X25519 - `ChaChaPoly` - Chiffrement AEAD ChaCha20-Poly1305 - `SHA256` - Fonction de hachage SHA-256

### Schéma de handshake Noise

**Notation du schéma IK:**

```
<- s                    (Bob's static key known to Alice)
...
-> e, es, s, ss         (Alice sends ephemeral, DH es, static key, DH ss)
<- e, ee, se            (Bob sends ephemeral, DH ee, DH se)
```
**Sens des jetons:** - `e` - Transmission de clé éphémère - `s` - Transmission de clé statique - `es` - DH entre la clé éphémère d'Alice et la clé statique de Bob - `ss` - DH entre la clé statique d'Alice et la clé statique de Bob - `ee` - DH entre la clé éphémère d'Alice et la clé éphémère de Bob - `se` - DH entre la clé statique de Bob et la clé éphémère d'Alice

### Propriétés de sécurité de Noise

En termes de Noise (cadre de protocoles cryptographiques), l’IK pattern (motif IK) fournit :

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Message</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Authentication Level</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Confidentiality Level</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Message&nbsp;1 (NS)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;1 (sender auth, KCI vulnerable)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;2 (weak forward secrecy)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Message&nbsp;2 (NSR)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;2 (mutual auth)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;4 (weak forward secrecy)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Transport (ES)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;2 (mutual auth)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Level&nbsp;5 (strong forward secrecy)</td>
    </tr>
  </tbody>
</table>
**Niveaux d'authentification:** - **Niveau 1**: La charge utile est authentifiée comme appartenant au propriétaire de la clé statique de l'expéditeur, mais vulnérable à l'usurpation d'identité par compromission de clé (KCI) - **Niveau 2**: Résistant aux attaques KCI après NSR

**Niveaux de confidentialité :** - **Niveau 2** : Confidentialité persistante si la clé statique de l’expéditeur est ultérieurement compromise - **Niveau 4** : Confidentialité persistante si la clé éphémère de l’expéditeur est ultérieurement compromise - **Niveau 5** : Confidentialité persistante parfaite après la suppression des deux clés éphémères

### Différences entre IK et XK

Le schéma IK diffère du schéma XK utilisé dans NTCP2 et SSU2 :

1. **Quatre opérations DH**: IK utilise 4 opérations DH (es, ss, ee, se) contre 3 pour XK
2. **Authentification immédiate**: Alice est authentifiée dès le premier message (Niveau d’authentification 1)
3. **Confidentialité persistante plus rapide**: Confidentialité persistante complète (niveau 5) atteinte après le deuxième message (1-RTT)
4. **Compromis**: La charge utile du premier message n’est pas protégée par la confidentialité persistante (contrairement à XK où toutes les charges utiles le sont)

**Résumé**: IK permet la livraison en un seul aller-retour (1-RTT) de la réponse de Bob avec une confidentialité persistante complète, au prix d'une requête initiale dépourvue de confidentialité persistante.

### Concepts du Double Ratchet (algorithme à double cliquet) de Signal

ECIES (schéma de chiffrement intégré à courbe elliptique) intègre des concepts issus de l’[algorithme Double Ratchet de Signal](https://signal.org/docs/specifications/doubleratchet/) :

- **Cliquet DH**: Assure la confidentialité persistante en échangeant périodiquement de nouvelles clés DH
- **Cliquet à clé symétrique**: Dérive de nouvelles clés de session pour chaque message
- **Session Tag Ratchet**: Génère de manière déterministe des session tags (étiquettes de session) à usage unique

**Principales différences par rapport à Signal:** - **Ratcheting (mécanisme de mise à jour progressive des clés) moins fréquent**: I2P effectue le ratcheting uniquement lorsque nécessaire (proche de l’épuisement des étiquettes ou selon la politique) - **Session Tags (étiquettes de session) au lieu du chiffrement d’en-tête**: Utilise des étiquettes déterministes plutôt que des en-têtes chiffrés - **ACK explicites (accusés de réception)**: Utilise des blocs d’ACK dans le même canal plutôt que de se reposer uniquement sur le trafic retour - **Ratchets séparés pour les étiquettes et les clés**: Plus efficace pour le récepteur (peut différer le calcul de la clé)

### Extensions d'I2P pour Noise (protocole)

1. **Encodage Elligator2**: Clés éphémères encodées pour être indiscernables de données aléatoires
2. **Étiquette préfixée au NSR**: Étiquette de session ajoutée avant le message NSR pour corrélation
3. **Format de charge utile défini**: Structure de charge utile par blocs pour tous les types de messages
4. **Encapsulation I2NP**: Tous les messages sont encapsulés dans des en-têtes I2NP Garlic Message
5. **Phase de données séparée**: Les messages de transport (ES) divergent de la phase de données standard de Noise (cadre cryptographique)

---

## Primitives cryptographiques

### X25519 Diffie-Hellman

**Spécification**: [RFC 7748](https://tools.ietf.org/html/rfc7748)

**Caractéristiques principales:** - **Taille de la clé privée**: 32 octets - **Taille de la clé publique**: 32 octets - **Taille du secret partagé**: 32 octets - **Ordre des octets**: Little-endian (poids faible en premier) - **Courbe**: Curve25519

**Opérations:**

### X25519 GENERATE_PRIVATE()

Génère une clé privée aléatoire de 32 octets :

```
privkey = CSRNG(32)
```
### X25519 DERIVE_PUBLIC(privkey)

Dérive la clé publique correspondante:

```
pubkey = curve25519_scalarmult_base(privkey)
```
Renvoie une clé publique de 32 octets en little-endian (octet le moins significatif en premier).

### X25519 DH(privkey, pubkey)

Effectue un échange de clés Diffie-Hellman :

```
sharedSecret = curve25519_scalarmult(privkey, pubkey)
```
Renvoie un secret partagé de 32 octets.

**Note de sécurité**: Les implémenteurs doivent vérifier que le secret partagé n’est pas entièrement composé de zéros (clé faible). Le cas échéant, rejeter et interrompre le handshake (établissement de session).

### ChaCha20-Poly1305 AEAD (chiffrement authentifié avec données associées)

**Spécification**: [RFC 7539](https://tools.ietf.org/html/rfc7539) section 2.8

**Paramètres:** - **Taille de clé**: 32 octets (256 bits) - **Taille du nonce (nombre utilisé une fois)**: 12 octets (96 bits) - **Taille du MAC**: 16 octets (128 bits) - **Taille de bloc**: 64 octets (interne)

**Format du Nonce (valeur aléatoire à usage unique):**

```
Byte 0-3:   0x00 0x00 0x00 0x00  (always zero)
Byte 4-11:  Little-endian counter (message number N)
```
**Construction AEAD (chiffrement authentifié avec données associées):**

L'AEAD (chiffrement authentifié avec des données associées) combine le chiffrement en flux ChaCha20 avec le MAC Poly1305 :

1. Générer le flux de clés ChaCha20 à partir de la clé et du nonce (valeur unique)
2. Chiffrer le texte en clair via XOR avec le flux de clés
3. Calculer le MAC Poly1305 sur (données associées || texte chiffré)
4. Ajouter à la fin du texte chiffré un MAC de 16 octets

### ChaCha20-Poly1305 ENCRYPT(k, n, plaintext, ad)

Chiffre le texte en clair avec authentification:

```python
# Inputs
k = 32-byte cipher key
n = 12-byte nonce (first 4 bytes zero, last 8 bytes = message number)
plaintext = data to encrypt (0 to 65519 bytes)
ad = associated data (optional, used in MAC calculation)

# Output
ciphertext = chacha20_encrypt(k, n, plaintext)
mac = poly1305(ad || ciphertext, poly1305_key_gen(k, n))
return ciphertext || mac  # Total length = len(plaintext) + 16
```
**Propriétés:** - Le texte chiffré a la même longueur que le texte en clair (chiffrement par flot) - La sortie est de plaintext_length + 16 octets (inclut le MAC) - L’ensemble de la sortie est indiscernable de données aléatoires si la clé est secrète - Le MAC authentifie à la fois les données associées et le texte chiffré

### ChaCha20-Poly1305 DECRYPT(k, n, ciphertext, ad)

Déchiffre et vérifie l'authentification :

```python
# Split ciphertext and MAC
ct_without_mac = ciphertext[0:-16]
received_mac = ciphertext[-16:]

# Verify MAC
expected_mac = poly1305(ad || ct_without_mac, poly1305_key_gen(k, n))
if not constant_time_compare(received_mac, expected_mac):
    raise AuthenticationError("MAC verification failed")

# Decrypt
plaintext = chacha20_decrypt(k, n, ct_without_mac)
return plaintext
```
**Exigences de sécurité critiques:** - Nonces (nombre arbitraire utilisé une seule fois) DOIVENT être uniques pour chaque message avec la même clé - Nonces NE DOIVENT PAS être réutilisés (défaillance catastrophique en cas de réutilisation) - La vérification du MAC (code d’authentification de message) DOIT utiliser une comparaison en temps constant pour empêcher les attaques par temporisation - Une vérification du MAC échouée DOIT entraîner un rejet complet du message (aucun déchiffrement partiel)

### Fonction de hachage SHA-256

**Spécification**: NIST FIPS 180-4

**Propriétés:** - **Taille de sortie**: 32 octets (256 bits) - **Taille de bloc**: 64 octets (512 bits) - **Niveau de sécurité**: 128 bits (résistance aux collisions)

**Opérations :**

### SHA-256 de H(p, d)

Hachage SHA-256 avec chaîne de personnalisation :

```
H(p, d) := SHA256(p || d)
```
Où `||` désigne la concaténation, `p` est une chaîne de personnalisation, `d` représente les données.

### SHA-256 MixHash(d)

Met à jour le hachage cumulatif avec de nouvelles données :

```
h = SHA256(h || d)
```
Utilisé tout au long du handshake Noise pour maintenir le hachage de la transcription.

### Dérivation de clé HKDF

**Spécification**: [RFC 5869](https://tools.ietf.org/html/rfc5869)

**Description**: Fonction de dérivation de clé basée sur HMAC utilisant SHA-256

**Paramètres:** - **Fonction de hachage**: HMAC-SHA256 - **Longueur du sel**: Jusqu'à 32 octets (taille de sortie SHA-256) - **Longueur de sortie**: Variable (jusqu'à 255 * 32 octets)

**Fonction HKDF:**

```python
def HKDF(salt, ikm, info, length):
    """
    Args:
        salt: Salt value (32 bytes max for SHA-256)
        ikm: Input key material (any length)
        info: Context-specific info string
        length: Desired output length in bytes
    
    Returns:
        output: Derived key material (length bytes)
    """
    # Extract phase
    prk = HMAC-SHA256(salt, ikm)
    
    # Expand phase
    n = ceil(length / 32)
    t = b''
    okm = b''
    for i in range(1, n + 1):
        t = HMAC-SHA256(prk, t || info || byte(i))
        okm = okm || t
    
    return okm[0:length]
```
**Modèles d'utilisation courants:**

```python
# Generate two keys (64 bytes total)
keydata = HKDF(chainKey, sharedSecret, "KDFDHRatchetStep", 64)
nextRootKey = keydata[0:31]
chainKey = keydata[32:63]

# Generate session tag (8 bytes)
tagdata = HKDF(chainKey, CONSTANT, "SessionTagKeyGen", 64)
nextChainKey = tagdata[0:31]
sessionTag = tagdata[32:39]

# Generate symmetric key (32 bytes)
keydata = HKDF(chainKey, ZEROLEN, "SymmetricRatchet", 64)
nextChainKey = keydata[0:31]
sessionKey = keydata[32:63]
```
**Chaînes d'information utilisées dans ECIES:** - `"KDFDHRatchetStep"` - Dérivation de clés du cliquet DH - `"TagAndKeyGenKeys"` - Initialisation des clés des chaînes de tags et de clés - `"STInitialization"` - Initialisation du cliquet des tags de session - `"SessionTagKeyGen"` - Génération des tags de session - `"SymmetricRatchet"` - Génération de clés symétriques - `"XDHRatchetTagSet"` - Clé de tagset (ensemble de tags) du cliquet DH - `"SessionReplyTags"` - Génération du tagset NSR (New Session Reply, réponse de nouvelle session) - `"AttachPayloadKDF"` - Dérivation de la clé de charge utile NSR

### Encodage Elligator2

**Objectif**: Encoder des clés publiques X25519 de façon qu'elles soient indiscernables de chaînes aléatoires uniformes de 32 octets.

**Spécification**: [Article Elligator2](https://elligator.cr.yp.to/elligator-20130828.pdf)

**Problème**: Les clés publiques X25519 standard présentent une structure reconnaissable. Un observateur peut identifier les messages de handshake (établissement de connexion) en détectant ces clés, même si le contenu est chiffré.

**Solution**: Elligator2 fournit une correspondance bijective entre environ 50 % des clés publiques X25519 valides et des chaînes de 254 bits d'apparence aléatoire.

**Génération de clés avec Elligator2 (technique de mappage des points de courbe elliptique vers des octets à distribution uniforme) :**

### Elligator2 GENERATE_PRIVATE_ELG2()

Génère une clé privée qui correspond à une clé publique encodable au format Elligator2 :

```python
while True:
    privkey = CSRNG(32)
    pubkey = DERIVE_PUBLIC(privkey)
    
    # Test if public key is Elligator2-encodable
    try:
        encoded = ENCODE_ELG2(pubkey)
        # Success - this key pair is suitable
        return privkey
    except NotEncodableError:
        # Try again with new random key
        continue
```
**Important**: Environ 50 % des clés privées générées aléatoirement produiront des clés publiques non encodables. Celles-ci doivent être écartées et une nouvelle génération doit être tentée.

**Optimisation des performances**: Générez des clés à l'avance dans un fil d'exécution en arrière-plan pour maintenir une réserve de paires de clés adéquates, afin d'éviter les retards lors du handshake (phase de négociation initiale).

### Elligator2 ENCODE_ELG2(pubkey)

Encode une clé publique en 32 octets d'apparence aléatoire :

```python
def ENCODE_ELG2(pubkey):
    """
    Encodes X25519 public key using Elligator2.
    
    Args:
        pubkey: 32-byte X25519 public key (little-endian)
    
    Returns:
        encoded: 32-byte encoded key indistinguishable from random
    
    Raises:
        NotEncodableError: If pubkey cannot be encoded
    """
    # Perform Elligator2 representative calculation
    # Returns 254-bit value (31.75 bytes)
    encodedKey = elligator2_encode(pubkey)
    
    # Add 2 random bits to MSB to make full 32 bytes
    randomByte = CSRNG(1)
    encodedKey[31] |= (randomByte & 0xc0)
    
    return encodedKey
```
**Détails d'encodage:** - Elligator2 produit 254 bits (pas les 256 complets) - Les 2 bits de poids fort de l'octet 31 sont du remplissage aléatoire - Le résultat est uniformément réparti dans l'espace de 32 octets - Encode avec succès environ 50 % des clés publiques X25519 valides

### Elligator2 DECODE_ELG2(encodedKey)

Se décode pour obtenir la clé publique d’origine:

```python
def DECODE_ELG2(encodedKey):
    """
    Decodes Elligator2-encoded key back to X25519 public key.
    
    Args:
        encodedKey: 32-byte encoded key
    
    Returns:
        pubkey: 32-byte X25519 public key (little-endian)
    """
    # Mask out 2 random padding bits from MSB
    encodedKey[31] &= 0x3f
    
    # Perform Elligator2 representative inversion
    pubkey = elligator2_decode(encodedKey)
    
    return pubkey
```
**Propriétés de sécurité:** - Les clés encodées sont computationnellement indiscernables d'octets aléatoires - Aucun test statistique ne peut détecter de manière fiable des clés encodées avec Elligator2 (méthode de mappage cryptographique) - Le décodage est déterministe (la même clé encodée produit toujours la même clé publique) - L'encodage est bijectif pour ~50 % des clés du sous-ensemble encodable

**Notes d’implémentation:** - Stocker les clés encodées lors de la phase de génération pour éviter de les réencoder pendant le handshake - Les clés inadaptées issues de la génération Elligator2 (mécanisme de camouflage de clés sur courbe elliptique) peuvent être utilisées pour NTCP2 (qui ne requiert pas Elligator2) - La génération de clés en arrière-plan est essentielle pour les performances - Le temps moyen de génération double en raison d’un taux de rejet de 50 %

---

## Formats des messages

### Aperçu

ECIES (schéma de chiffrement intégré sur courbe elliptique) définit trois types de messages :

1. **Nouvelle session (NS)**: Message de poignée de main initial d'Alice à Bob
2. **Réponse de nouvelle session (NSR)**: Réponse de poignée de main de Bob à Alice
3. **Session existante (ES)**: Tous les messages ultérieurs dans les deux sens

Tous les messages sont encapsulés au format I2NP Garlic Message, avec des couches de chiffrement supplémentaires.

### Conteneur I2NP de Garlic Message (message composite « garlic »)

Tous les messages ECIES sont encapsulés dans des en-têtes I2NP Garlic Message standard :

```
+----+----+----+----+----+----+----+----+
|type|      msg_id       |  expiration   |
+----+----+----+----+----+----+----+----+
                         |  size   |chks|
+----+----+----+----+----+----+----+----+
|      length       |                   |
+----+----+----+----+                   +
|          encrypted data               |
~                                       ~
```
**Champs:** - `type`: 0x26 (Garlic Message, message 'garlic' d'I2P) - `msg_id`: identifiant de message I2NP de 4 octets - `expiration`: horodatage Unix de 8 octets (millisecondes) - `size`: taille de la charge utile de 2 octets - `chks`: somme de contrôle sur 1 octet - `length`: longueur des données chiffrées sur 4 octets - `encrypted data`: charge utile chiffrée ECIES

**Objectif**: Fournit l’identification et le routage des messages au niveau de la couche I2NP. Le champ `length` permet aux récepteurs de connaître la taille totale de la charge utile chiffrée.

### Message de nouvelle session (NS)

Le message « New Session » initie une nouvelle session d’Alice vers Bob. Il se décline en trois variantes :

1. **Avec liaison** (1b): Inclut la clé statique d’Alice pour une communication bidirectionnelle
2. **Sans liaison** (1c): Omet la clé statique pour une communication unidirectionnelle
3. **À usage unique** (1d): Mode à message unique sans établissement de session

### Message NS avec liaison (Type 1b)

**Cas d’utilisation**: Diffusion en continu, datagrammes pouvant recevoir une réponse, tout protocole nécessitant des réponses

**Longueur totale** : 96 + payload_length octets

**Format**:

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|   New Session Ephemeral Public Key    |
+             32 bytes                  +
|     Encoded with Elligator2           |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+         Static Key Section            +
|       ChaCha20 encrypted data         |
+            32 bytes                   +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+    (MAC) for Static Key Section       +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~          Variable length              ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
```
**Détails du champ:**

**Clé publique éphémère** (32 octets, en clair): - La clé publique X25519 à usage unique d'Alice - Encodée avec Elligator2 (indiscernable d'une donnée aléatoire) - Générée pour chaque message NS (jamais réutilisée) - Format little-endian

**Section de clé statique** (32 octets chiffrés, 48 octets avec MAC): - Contient la clé publique statique X25519 d'Alice (32 octets) - Chiffrée avec ChaCha20 - Authentifiée avec un MAC Poly1305 (16 octets) - Utilisée par Bob pour lier la session à la destination d'Alice

**Section de charge utile** (chiffrée de longueur variable, +16 octets de MAC): - Contient des garlic cloves (sous-blocs de message de garlic encryption) et d'autres blocs - Doit inclure un bloc DateTime comme premier bloc - Inclut généralement des blocs Garlic Clove contenant des données applicatives - Peut inclure un bloc NextKey pour un ratchet immédiat (mécanisme de rotation de clés) - Chiffré avec ChaCha20 - Authentifié avec un MAC Poly1305 (16 octets)

**Propriétés de sécurité:** - La clé éphémère fournit une composante de confidentialité persistante - La clé statique authentifie Alice (liaison à la destination) - Les deux sections ont des MAC distincts pour la séparation des domaines - Le handshake complet effectue 2 opérations DH (es, ss)

### Message NS sans liaison (Type 1c)

**Cas d'utilisation**: Datagrammes bruts où aucune réponse n'est attendue ni souhaitée

**Longueur totale**: 96 + payload_length octets

**Format** :

```
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|   New Session Ephemeral Public Key    |
+             32 bytes                  +
|     Encoded with Elligator2           |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                                       |
+           Flags Section               +
|       ChaCha20 encrypted data         |
+            32 bytes                   +
|           All zeros                   |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for above section       +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~          Variable length              ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
```
**Différence principale**: La section des drapeaux contient 32 octets à zéro au lieu d'une clé statique.

**Détection**: Bob détermine le type de message en déchiffrant la section de 32 octets et en vérifiant si tous les octets sont à zéro: - Tous à zéro → Session non liée (type 1c) - Non nuls → Session liée avec clé statique (type 1b)

**Propriétés:** - L'absence de clé statique signifie qu'il n'y a pas de liaison à la destination d'Alice - Bob ne peut pas envoyer de réponses (aucune destination connue) - N'effectue qu'1 opération DH (Diffie-Hellman) - Suit le Noise "N" pattern (modèle "N" du protocole Noise) plutôt que "IK" - Plus efficace lorsque les réponses ne sont jamais nécessaires

**Section des drapeaux** (réservée pour une utilisation future): Actuellement tous à zéro. Peut être utilisée pour la négociation de fonctionnalités dans de futures versions.

### Message NS à usage unique (Type 1d)

**Cas d'utilisation**: Message anonyme unique sans session ni réponse attendue

**Longueur totale**: 96 + payload_length octets

**Format**: Identique à NS sans liaison (type 1c)

**Distinction**:  - Le type 1c peut envoyer plusieurs messages dans la même session (des messages ES suivent) - Le type 1d envoie exactement un seul message sans établissement de session - En pratique, les implémentations peuvent les traiter de manière identique initialement

**Propriétés :** - Anonymat maximal (aucune clé statique, aucune session) - Aucun état de session conservé par aucune des parties - Suit le modèle "N" de Noise - Une seule opération DH (Diffie-Hellman)

### Message de réponse de nouvelle session (NSR)

Bob envoie un ou plusieurs messages NSR en réponse au message NS d'Alice. Le NSR achève le Noise IK handshake (échange d'initialisation sécurisé) et établit une session bidirectionnelle.

**Longueur totale**: 72 + payload_length octets

**Format**:

```
+----+----+----+----+----+----+----+----+
|       Session Tag   8 bytes           |
+----+----+----+----+----+----+----+----+
|                                       |
+        Ephemeral Public Key           +
|                                       |
+            32 bytes                   +
|     Encoded with Elligator2           |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+  (MAC) for Key Section (empty)        +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~          Variable length              ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+         (MAC) for Payload Section     +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
```
**Détails du champ:**

**Étiquette de session** (8 octets, en clair): - Générée à partir du jeu de tags NSR (voir les sections KDF) - Associe cette réponse au message NS d’Alice - Permet à Alice d’identifier à quel NS cette NSR répond - Utilisation unique (jamais réutilisée)

**Clé publique éphémère** (32 octets, en clair): - Clé publique X25519 à usage unique de Bob - Encodée avec Elligator2 - Générée spécifiquement pour chaque message NSR - Doit être différente pour chaque NSR envoyé

**MAC de la section de clé** (16 octets): - Authentifie des données vides (ZEROLEN) - Fait partie du protocole Noise IK (se pattern (static-ephemeral, statique-éphémère)) - Utilise la transcription de hachage comme données associées - Essentiel pour lier NSR à NS

**Section de charge utile** (longueur variable): - Contient des garlic cloves (unités de message « garlic ») et des blocs - Inclut généralement des réponses de la couche applicative - Peut être vide (ACK-only NSR, NSR ne contenant qu’un ACK) - Taille maximale : 65519 octets (65535 - MAC de 16 octets)

**Plusieurs messages NSR:**

Bob peut envoyer plusieurs messages NSR en réponse à un NS : - Chaque NSR possède une clé éphémère unique - Chaque NSR possède une étiquette de session unique - Alice utilise le premier NSR reçu pour terminer le handshake (établissement de session) - Les autres NSR servent de redondance (en cas de perte de paquets)

**Synchronisation critique :** - Alice doit recevoir un NSR avant d'envoyer des messages ES - Bob doit recevoir un message ES avant d'envoyer des messages ES - NSR établit des clés de session bidirectionnelles via l'opération split()

**Propriétés de sécurité :** - Achève le handshake IK de Noise - Effectue 2 opérations DH supplémentaires (ee, se) - Total de 4 opérations DH sur NS+NSR - Assure une authentification mutuelle (Niveau 2) - Fournit une confidentialité persistante (PFS) faible (Niveau 4) pour la charge utile NSR

### Message de session existante (ES)

Tous les messages après la poignée de main NS/NSR utilisent le format Existing Session (session existante). Les messages ES sont utilisés dans les deux sens par Alice et Bob.

**Longueur totale**: 8 + payload_length + 16 octets (minimum 24 octets)

**Format**:

```
+----+----+----+----+----+----+----+----+
|       Session Tag   8 bytes           |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~          Variable length              ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+              (MAC)                    +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+
```
**Détails des champs:**

**Session Tag** (étiquette de session) (8 octets, en clair): - Généré à partir du jeu de tags sortant actuel - Identifie la session et le numéro du message - Le récepteur recherche le tag pour trouver la clé de session et le nonce (nombre utilisé une seule fois) - Usage unique (chaque tag utilisé exactement une fois) - Format: les 8 premiers octets de la sortie HKDF

**Section de charge utile** (longueur variable): - Contient des garlic cloves (« gousses » dans la terminologie I2P) et des blocs - Aucun bloc obligatoire (peut être vide) - Blocs courants : Garlic Clove, NextKey, ACK, ACK Request, Padding - Taille maximale : 65519 octets (65535 - MAC de 16 octets)

**MAC** (16 octets): - Tag d'authentification Poly1305 - Calculé sur l'ensemble de la charge utile - Données associées : le tag de session de 8 octets - Doit être vérifié correctement, sinon le message est rejeté

**Processus de recherche d'étiquettes:**

1. Le récepteur extrait un tag de 8 octets
2. Recherche le tag dans tous les tagsets (ensembles de tags) entrants actuels
3. Récupère la clé de session associée et le numéro de message N
4. Construit le nonce : `[0x00, 0x00, 0x00, 0x00, N (8 bytes little-endian)]`
5. Déchiffre la charge utile en utilisant l’AEAD avec le tag comme données associées
6. Retire le tag du tagset (usage unique)
7. Traite les blocs déchiffrés

**Étiquette de session introuvable :**

Si le tag (étiquette) n'est trouvé dans aucun tagset (ensemble de tags): - Peut être un message NS (session Noise) → tenter le déchiffrement NS - Peut être un message NSR (réponse de session Noise) → tenter le déchiffrement NSR - Peut être un ES hors séquence (session existante) → attendre brièvement une mise à jour du tagset - Peut être une attaque par rejeu → rejeter - Peut être des données corrompues → rejeter

**Charge utile vide:**

Les messages ES peuvent avoir des charges utiles vides (0 octet) : - Sert d'accusé de réception explicite (ACK) lorsqu'une requête d'ACK a été reçue - Fournit une réponse au niveau du protocole sans données d'application - Consomme tout de même une étiquette de session - Utile lorsque la couche supérieure n'a pas de données immédiates à envoyer

**Propriétés de sécurité :** - Confidentialité persistante totale (niveau 5) après réception de NSR - Chiffrement authentifié via AEAD (chiffrement authentifié avec données associées) - Le Tag (étiquette) agit comme des données associées supplémentaires - Maximum 65535 messages par tagset (ensemble de tags) avant qu'un ratchet (mécanisme de cliquet cryptographique) ne soit requis

---

## Fonctions de dérivation de clés

Cette section documente toutes les opérations de KDF utilisées dans ECIES, en présentant les dérivations cryptographiques complètes.

### Notation et constantes

**Constantes:** - `ZEROLEN` - Tableau d'octets de longueur zéro (chaîne vide) - `||` - Opérateur de concaténation

**Variables :** - `h` - Hachage cumulatif du transcript (historique des échanges) (32 octets) - `chainKey` - Clé de chaînage pour HKDF (32 octets) - `k` - Clé de chiffrement symétrique (32 octets) - `n` - Nonce (valeur à usage unique) / numéro de message

**Clés:** - `ask` / `apk` - clé privée/publique statique d'Alice - `aesk` / `aepk` - clé privée/publique éphémère d'Alice - `bsk` / `bpk` - clé privée/publique statique de Bob - `besk` / `bepk` - clé privée/publique éphémère de Bob

### Fonctions de dérivation de clés (KDF) pour les messages NS

### KDF 1: Clé de chaîne initiale

Effectué une seule fois lors de l'initialisation du protocole (peut être précalculé):

```python
# Protocol name (40 bytes, ASCII, no null termination)
protocol_name = "Noise_IKelg2+hs2_25519_ChaChaPoly_SHA256"

# Initialize hash
h = SHA256(protocol_name)

# Initialize chaining key
chainKey = h

# MixHash with empty prologue
h = SHA256(h)

# State: chainKey and h initialized
# Can be precalculated for all outbound sessions
```
**Résultat:** - `chainKey` = Clé de chaînage initiale pour toutes les fonctions de dérivation de clé (KDF) ultérieures - `h` = Transcription de hachage initiale

### KDF 2: Mélange avec la clé statique de Bob

Bob exécute ceci une fois (peut être précalculé pour toutes les sessions entrantes):

```python
# Bob's static keys (published in LeaseSet)
bsk = GENERATE_PRIVATE()
bpk = DERIVE_PUBLIC(bsk)

# Mix Bob's public key into hash
h = SHA256(h || bpk)

# State: h updated with Bob's identity
# Can be precalculated by Bob for all inbound sessions
```
### KDF 3 : Génération de la clé éphémère d'Alice

Alice génère de nouvelles clés pour chaque message NS :

```python
# Generate ephemeral key pair suitable for Elligator2
aesk = GENERATE_PRIVATE_ELG2()
aepk = DERIVE_PUBLIC(aesk)

# Mix ephemeral public key into hash
h = SHA256(h || aepk)

# Elligator2 encode for transmission
elg2_aepk = ENCODE_ELG2(aepk)

# State: h updated with Alice's ephemeral key
# Send elg2_aepk as first 32 bytes of NS message
```
### KDF 4 : Section de clé statique NS (DH)

Dérive des clés pour chiffrer la clé statique d'Alice :

```python
# Perform first DH (ephemeral-static)
sharedSecret = DH(aesk, bpk)  # Alice computes
# Equivalent: sharedSecret = DH(bsk, aepk)  # Bob computes

# Derive cipher key from shared secret
keydata = HKDF(chainKey, sharedSecret, "", 64)
chainKey = keydata[0:31]
k = keydata[32:63]

# AEAD encryption parameters
nonce = 0
associated_data = h  # Current hash transcript

# Encrypt static key section
if binding_requested:
    plaintext = apk  # Alice's static public key (32 bytes)
else:
    plaintext = bytes(32)  # All zeros for unbound

ciphertext = ENCRYPT(k, nonce, plaintext, associated_data)
# ciphertext = 32 bytes encrypted + 16 bytes MAC = 48 bytes

# Mix ciphertext into hash
h = SHA256(h || ciphertext)

# State: Static key section encrypted, h updated
# Send ciphertext (48 bytes) as next part of NS message
```
### KDF 5: Section de charge utile NS (ss DH, liée uniquement)

Pour les sessions liées, effectuez un second échange de clés Diffie-Hellman (DH) pour le chiffrement de la charge utile :

```python
if binding_requested:
    # Alice's static keys
    ask = GENERATE_PRIVATE()  # Alice's long-term key
    apk = DERIVE_PUBLIC(ask)
    
    # Perform second DH (static-static)
    sharedSecret = DH(ask, bpk)  # Alice computes
    # Equivalent: sharedSecret = DH(bsk, apk)  # Bob computes
    
    # Derive cipher key
    keydata = HKDF(chainKey, sharedSecret, "", 64)
    chainKey = keydata[0:31]
    k = keydata[32:63]
    
    nonce = 0
    associated_data = h
else:
    # Unbound: reuse keys from static key section
    # chainKey and k unchanged
    nonce = 1  # Increment nonce (reusing same key)
    associated_data = h

# Encrypt payload
payload = build_payload()  # DateTime + Garlic Cloves + etc.
ciphertext = ENCRYPT(k, nonce, payload, associated_data)

# Mix ciphertext into hash
h = SHA256(h || ciphertext)

# State: Payload encrypted, h contains complete NS transcript
# Save chainKey and h for NSR processing
# Send ciphertext as final part of NS message
```
**Notes importantes :**

1. **Lié vs Non lié**: 
   - Lié effectue 2 opérations DH (es + ss)
   - Non lié effectue 1 opération DH (es uniquement)
   - Non lié incrémente le nonce (nombre utilisé une seule fois) au lieu de dériver une nouvelle clé

2. **Sécurité contre la réutilisation des clés**:
   - Des nonces différents (0 vs 1) empêchent la réutilisation de la paire clé/nonce
   - Des données associées différentes (h est différent) assurent une séparation des domaines

3. **Transcription de hachage**:
   - `h` contient maintenant : protocol_name, prologue vide, bpk, aepk, static_key_ciphertext, payload_ciphertext
   - Cette transcription lie toutes les parties du message NS entre elles

### KDF (fonction de dérivation de clés) du jeu d’étiquettes de réponse NSR

Bob génère des tags pour les messages NSR (un type de message spécifique) :

```python
# Chain key from NS payload section
# chainKey = final chainKey from NS KDF

# Generate tagset key
tagsetKey = HKDF(chainKey, ZEROLEN, "SessionReplyTags", 32)

# Initialize NSR tagset (see DH_INITIALIZE below)
tagset_nsr = DH_INITIALIZE(chainKey, tagsetKey)

# Get tag for this NSR
tagsetEntry = tagset_nsr.GET_NEXT_ENTRY()
tag = tagsetEntry.SESSION_TAG  # 8 bytes

# State: tag available for NSR message
# Send tag as first 8 bytes of NSR
```
### Fonctions de dérivation de clés pour les messages NSR

### KDF 6: Génération de clés éphémères NSR

Bob génère une nouvelle clé éphémère pour chaque NSR :

```python
# Mix tag into hash (I2P extension to Noise)
h = SHA256(h || tag)

# Generate ephemeral key pair
besk = GENERATE_PRIVATE_ELG2()
bepk = DERIVE_PUBLIC(besk)

# Mix ephemeral public key into hash
h = SHA256(h || bepk)

# Elligator2 encode for transmission
elg2_bepk = ENCODE_ELG2(bepk)

# State: h updated with tag and Bob's ephemeral key
# Send elg2_bepk as bytes 9-40 of NSR message
```
### KDF 7 : Section de clés NSR (ee et se DH)

Dérive des clés pour la section de clés NSR:

```python
# Perform third DH (ephemeral-ephemeral)
sharedSecret_ee = DH(aesk, bepk)  # Alice computes
# Equivalent: sharedSecret_ee = DH(besk, aepk)  # Bob computes

# Mix ee into chain
keydata = HKDF(chainKey, sharedSecret_ee, "", 32)
chainKey = keydata[0:31]

# Perform fourth DH (static-ephemeral)
sharedSecret_se = DH(ask, bepk)  # Alice computes
# Equivalent: sharedSecret_se = DH(besk, apk)  # Bob computes

# Derive cipher key from se
keydata = HKDF(chainKey, sharedSecret_se, "", 64)
chainKey = keydata[0:31]
k = keydata[32:63]

# AEAD encryption of empty data (key section has no payload)
nonce = 0
associated_data = h
ciphertext = ENCRYPT(k, nonce, ZEROLEN, associated_data)
# ciphertext = 16 bytes (MAC only, no plaintext)

# Mix ciphertext into hash
h = SHA256(h || ciphertext)

# State: Key section encrypted, chainKey contains all 4 DH results
# Send ciphertext (16 bytes MAC) as bytes 41-56 of NSR
```
**Critique**: Cela termine le Noise IK handshake (échange initial du protocole Noise IK). `chainKey` contient désormais les contributions des 4 opérations DH (es, ss, ee, se).

### KDF 8: Section de charge utile NSR

Dérive des clés pour le chiffrement de la charge utile NSR :

```python
# Split chainKey into bidirectional keys
keydata = HKDF(chainKey, ZEROLEN, "", 64)
k_ab = keydata[0:31]   # Alice → Bob key
k_ba = keydata[32:63]  # Bob → Alice key

# Initialize ES tagsets for both directions
tagset_ab = DH_INITIALIZE(chainKey, k_ab)  # Alice → Bob
tagset_ba = DH_INITIALIZE(chainKey, k_ba)  # Bob → Alice

# Derive NSR payload key (Bob → Alice)
k_nsr = HKDF(k_ba, ZEROLEN, "AttachPayloadKDF", 32)

# Encrypt NSR payload
nonce = 0
associated_data = h  # Binds payload to entire NSR
payload = build_payload()  # Usually application reply
ciphertext = ENCRYPT(k_nsr, nonce, payload, associated_data)

# State: Bidirectional ES sessions established
# tagset_ab and tagset_ba ready for ES messages
# Send ciphertext as bytes 57+ of NSR message
```
**Notes importantes :**

1. **Opération de séparation**: 
   - Crée des clés indépendantes pour chaque direction
   - Empêche la réutilisation des clés entre Alice→Bob et Bob→Alice

2. **Liaison de la charge utile NSR**:
   - Utilise `h` comme données associées pour lier la charge utile au handshake (poignée de main)
   - Une KDF distincte ("AttachPayloadKDF") assure la séparation des domaines

3. **Préparation ES**:
   - Après NSR, les deux parties peuvent envoyer des messages ES
   - Alice doit recevoir NSR avant d'envoyer ES
   - Bob doit recevoir ES avant d'envoyer ES

### Fonctions de dérivation de clés pour les messages ES

Les messages ES utilisent des clés de session générées à l'avance issues de tagsets (ensembles de tags):

```python
# Sender gets next tag and key
tagsetEntry = outbound_tagset.GET_NEXT_ENTRY()
tag = tagsetEntry.SESSION_TAG     # 8 bytes
k = tagsetEntry.SESSION_KEY       # 32 bytes
N = tagsetEntry.INDEX             # Message number

# Construct nonce (12 bytes)
nonce = [0x00, 0x00, 0x00, 0x00] + little_endian_8_bytes(N)

# AEAD encryption
associated_data = tag  # Tag is associated data
payload = build_payload()
ciphertext = ENCRYPT(k, nonce, payload, associated_data)

# Send: tag || ciphertext (8 + len(ciphertext) bytes)
```
**Processus de réception :**

```python
# Extract tag
tag = message[0:8]

# Look up tag in inbound tagsets
tagsetEntry = inbound_tagset.GET_SESSION_KEY(tag)
if tagsetEntry is None:
    # Not an ES message, try NS/NSR decryption
    return try_handshake_decryption(message)

k = tagsetEntry.SESSION_KEY
N = tagsetEntry.INDEX

# Construct nonce
nonce = [0x00, 0x00, 0x00, 0x00] + little_endian_8_bytes(N)

# AEAD decryption
associated_data = tag
ciphertext = message[8:]
try:
    payload = DECRYPT(k, nonce, ciphertext, associated_data)
except AuthenticationError:
    # MAC verification failed, reject message
    return reject_message()

# Process payload blocks
process_payload(payload)

# Remove tag from tagset (one-time use)
inbound_tagset.remove(tag)
```
### Fonction DH_INITIALIZE

Crée un ensemble d'étiquettes pour un seul sens:

```python
def DH_INITIALIZE(rootKey, k):
    """
    Initializes a tagset with session tag and symmetric key ratchets.
    
    Args:
        rootKey: Chain key from previous DH ratchet (32 bytes)
        k: Key material from split() or DH ratchet (32 bytes)
    
    Returns:
        tagset: Initialized tagset object
    """
    # Derive next root key and chain key
    keydata = HKDF(rootKey, k, "KDFDHRatchetStep", 64)
    nextRootKey = keydata[0:31]
    chainKey_tagset = keydata[32:63]
    
    # Derive separate chain keys for tags and keys
    keydata = HKDF(chainKey_tagset, ZEROLEN, "TagAndKeyGenKeys", 64)
    sessTag_ck = keydata[0:31]   # Session tag chain key
    symmKey_ck = keydata[32:63]  # Symmetric key chain key
    
    # Create tagset object
    tagset = Tagset()
    tagset.nextRootKey = nextRootKey
    tagset.sessTag_chainKey = sessTag_ck
    tagset.symmKey_chainKey = symmKey_ck
    tagset.lastIndex = -1
    
    return tagset
```
**Contextes d’utilisation :**

1. **NSR Tagset (ensemble d’étiquettes)**: `DH_INITIALIZE(chainKey_from_NS, tagsetKey_NSR)`
2. **ES Tagsets**: `DH_INITIALIZE(chainKey_from_NSR, k_ab or k_ba)`
3. **Tagsets à cliquet**: `DH_INITIALIZE(nextRootKey_from_previous, tagsetKey_from_DH)`

---

## Mécanismes à cliquet

ECIES utilise trois mécanismes à cliquet synchronisés pour assurer la confidentialité persistante et une gestion des sessions efficace.

### Vue d’ensemble de Ratchet (mécanisme d’actualisation des clés cryptographiques)

**Trois types de Ratchet (mécanisme à cliquet cryptographique):**

1. **DH Ratchet** (mécanisme à cliquet Diffie-Hellman): Effectue des échanges de clés Diffie-Hellman pour générer de nouvelles clés racine
2. **Session Tag Ratchet** (mécanisme à cliquet pour les étiquettes de session): Dérive de manière déterministe des étiquettes de session à usage unique
3. **Symmetric Key Ratchet** (mécanisme à cliquet pour les clés symétriques): Dérive des clés de session pour le chiffrement des messages

**Relation:**

```
DH Ratchet (periodic)
    ↓
Creates new tagset
    ↓
Session Tag Ratchet (per message) ← synchronized → Symmetric Key Ratchet (per message)
    ↓                                                      ↓
Session Tags (8 bytes each)                      Session Keys (32 bytes each)
```
**Propriétés clés:**

- **Émetteur**: Génère des tags et des clés à la demande (aucun stockage nécessaire)
- **Récepteur**: Pré-génère des tags pour la fenêtre d’anticipation (stockage requis)
- **Synchronisation**: L’index de tag détermine l’index de clé (N_tag = N_key)
- **Confidentialité persistante**: Obtenue via un DH ratchet (mécanisme à cliquet Diffie-Hellman)
- **Efficacité**: Le récepteur peut différer le calcul de la clé jusqu’à réception du tag

### Cliquet Diffie-Hellman

Le DH ratchet (mécanisme à cliquet Diffie-Hellman) assure la confidentialité persistante en échangeant périodiquement de nouvelles clés éphémères.

### Fréquence du cliquet Diffie-Hellman

**Conditions requises du ratchet (mécanisme à cliquet cryptographique):** - Ensemble de tags approchant l’épuisement (le tag 65535 est le maximum) - Politiques propres à l’implémentation:   - Seuil basé sur le nombre de messages (par exemple, tous les 4096 messages)   - Seuil temporel (par exemple, toutes les 10 minutes)   - Seuil de volume de données (par exemple, tous les 100 Mo)

**Ratchet (mécanisme de cliquet cryptographique) initial recommandé**: Aux environs du numéro de tag 4096 pour éviter d'atteindre la limite

**Valeurs maximales:** - **ID maximum de l’ensemble de tags**: 65535 - **ID maximum de clé**: 32767 - **Nombre maximal de messages par ensemble de tags**: 65535 - **Volume de données maximal théorique par session**: ~6.9 TB (64K ensembles de tags × 64K messages × 1730 octets en moyenne)

### Identifiants de tags et de clés du DH Ratchet (mécanisme à cliquet Diffie-Hellman)

**Ensemble de tags initial** (après le handshake): - ID de l'ensemble de tags: 0 - Aucun bloc NextKey n'a encore été envoyé - Aucun ID de clé n'a été attribué

**Après le premier Ratchet (mécanisme de cliquet cryptographique)**: - ID de l'ensemble de tags: 1 = (1 + ID de la clé d'Alice + ID de la clé de Bob) = (1 + 0 + 0) - Alice envoie NextKey avec l'ID de clé 0 - Bob répond avec NextKey avec l'ID de clé 0

**Subsequent Tag Sets (jeux de tags ultérieurs)**: - Tag set ID = 1 + ID de la clé de l'expéditeur + ID de la clé du destinataire - Exemple : Tag set 5 = (1 + sender_key_2 + receiver_key_2)

**Tableau de progression des ensembles de balises:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Tag Set ID</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Sender Key ID</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Receiver Key ID</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">n/a</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">n/a</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Initial tag set (post-NSR)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">First ratchet (both generate new keys)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Sender generates new key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Receiver generates new key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Sender generates new key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Receiver generates new key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">...</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">...</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">...</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Pattern repeats</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">65534</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32767 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32766</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Second-to-last tag set</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">65535</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32767</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32767 *</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Final tag set</td>
    </tr>
  </tbody>
</table>
\* = Nouvelle clé générée par ce ratchet (mécanisme à cliquet)

**Règles de l'ID de clé:** - Les ID sont séquentiels à partir de 0 - Les ID sont incrémentés uniquement lorsqu'une nouvelle clé est générée - L'ID de clé maximal est 32767 (15 bits) - Après l'ID de clé 32767, une nouvelle session est requise

### Flux des messages du DH Ratchet (mécanisme de cliquet Diffie-Hellman)

**Rôles:** - **Émetteur de tags (étiquettes)**: Possède l'ensemble de tags sortants, envoie des messages - **Récepteur de tags**: Possède l'ensemble de tags entrants, reçoit des messages

**Schéma:** L'expéditeur des tags initie le ratchet (mécanisme à cliquet cryptographique) lorsque l'ensemble de tags est presque épuisé.

**Diagramme de flux des messages :**

```
Tag Sender                         Tag Receiver

       ... using tag set #0 ...

(Tag set #0 approaching exhaustion)
(Generate new key #0)

NextKey forward, request reverse, with key #0  -------->
(Repeat until NextKey ACK received)
                                   (Generate new key #0)
                                   (Perform DH: sender_key_0 × receiver_key_0)
                                   (Create inbound tag set #1)

        <---------------           NextKey reverse, with key #0
                                   (Repeat until tag from tag set #1 received)

(Receive NextKey with key #0)
(Perform DH: sender_key_0 × receiver_key_0)
(Create outbound tag set #1)


       ... using tag set #1 ...


(Tag set #1 approaching exhaustion)
(Generate new key #1)

NextKey forward, with key #1        -------->
(Repeat until NextKey ACK received)
                                   (Reuse existing key #0)
                                   (Perform DH: sender_key_1 × receiver_key_0)
                                   (Create inbound tag set #2)

        <--------------            NextKey reverse, id 0 (ACK)
                                   (Repeat until tag from tag set #2 received)

(Receive NextKey with id 0)
(Perform DH: sender_key_1 × receiver_key_0)
(Create outbound tag set #2)


       ... using tag set #2 ...


(Tag set #2 approaching exhaustion)
(Reuse existing key #1)

NextKey forward, request reverse, id 1  -------->
(Repeat until NextKey received)
                                   (Generate new key #1)
                                   (Perform DH: sender_key_1 × receiver_key_1)
                                   (Create inbound tag set #3)

        <--------------            NextKey reverse, with key #1

(Receive NextKey with key #1)
(Perform DH: sender_key_1 × receiver_key_1)
(Create outbound tag set #3)


       ... using tag set #3 ...

       (Pattern repeats: even-numbered tag sets
        use forward key, odd-numbered use reverse key)
```
**Schémas de ratchet (mécanisme à cliquet):**

**Création de Tag Sets (ensembles d’étiquettes) numérotés pairs** (2, 4, 6, ...): 1. L’émetteur génère une nouvelle clé 2. L’émetteur envoie un NextKey block (bloc NextKey) avec la nouvelle clé 3. Le récepteur envoie un NextKey block avec l’ancien identifiant de clé (ACK, accusé de réception) 4. Les deux effectuent un DH (Diffie-Hellman) avec (nouvelle clé de l’émetteur × ancienne clé du récepteur)

**Création de Tag Sets (ensembles de tags) à nombre impair** (3, 5, 7, ...): 1. L’émetteur demande la reverse key (clé de retour) (envoie NextKey avec l’indicateur de requête) 2. Le récepteur génère une nouvelle clé 3. Le récepteur envoie un bloc NextKey avec la nouvelle clé 4. Les deux réalisent un Diffie-Hellman (DH) avec (ancienne clé de l’émetteur × nouvelle clé du récepteur)

### Format du bloc NextKey

Voir la section Payload Format pour une spécification détaillée du bloc NextKey.

**Éléments clés:** - **Octet de drapeaux**:   - Bit 0: Clé présente (1) ou ID uniquement (0)   - Bit 1: Clé retour (1) ou clé aller (0)   - Bit 2: Demander la clé retour (1) ou aucune demande (0) - **ID de clé**: 2 octets, big-endian (0-32767) - **Clé publique**: 32 octets X25519 (si le bit 0 = 1)

**Exemples de blocs NextKey:**

```python
# Sender initiates ratchet with new key (key ID 0, tag set 1)
NextKey(flags=0x01, key_id=0, pubkey=sender_key_0)

# Receiver replies with new key (key ID 0, tag set 1)
NextKey(flags=0x03, key_id=0, pubkey=receiver_key_0)

# Sender ratchets again with new key (key ID 1, tag set 2)
NextKey(flags=0x01, key_id=1, pubkey=sender_key_1)

# Receiver ACKs with old key ID (tag set 2)
NextKey(flags=0x02, key_id=0)

# Sender requests reverse key (tag set 3)
NextKey(flags=0x04, key_id=1)

# Receiver sends new reverse key (key ID 1, tag set 3)
NextKey(flags=0x03, key_id=1, pubkey=receiver_key_1)
```
### Fonction de dérivation de clés (KDF) du ratchet DH (mécanisme à cliquet)

Lorsque de nouvelles clés sont échangées:

```python
# Tag sender generates or reuses key
if generating_new:
    sender_sk = GENERATE_PRIVATE()
    sender_pk = DERIVE_PUBLIC(sender_sk)
else:
    # Reuse existing key pair
    sender_pk = existing_sender_pk

# Tag receiver generates or reuses key
if generating_new:
    receiver_sk = GENERATE_PRIVATE()
    receiver_pk = DERIVE_PUBLIC(receiver_sk)
else:
    # Reuse existing key pair
    receiver_pk = existing_receiver_pk

# Both parties perform DH
sharedSecret = DH(sender_sk, receiver_pk)

# Derive tagset key
tagsetKey = HKDF(sharedSecret, ZEROLEN, "XDHRatchetTagSet", 32)

# Get next root key from previous tagset
rootKey = previous_tagset.nextRootKey

# Initialize new tagset
new_tagset = DH_INITIALIZE(rootKey, tagsetKey)

# Tag sender: outbound tagset
# Tag receiver: inbound tagset
```
**Synchronisation critique:**

**Tag Sender (émetteur de tags):** - Crée immédiatement un nouvel ensemble de tags sortants - Commence immédiatement à utiliser les nouveaux tags - Supprime l’ancien ensemble de tags sortants

**Récepteur de tags:** - Crée un nouvel ensemble de tags entrants - Conserve l'ancien ensemble de tags entrants pendant la période de grâce (3 minutes) - Accepte des tags provenant à la fois de l'ancien et du nouvel ensemble de tags pendant la période de grâce - Supprime l'ancien ensemble de tags entrants après la période de grâce

### Gestion de l'état du DH Ratchet (mécanisme à cliquet Diffie-Hellman)

**État de l'expéditeur:** - Ensemble de tags sortants actuel - Identifiant de l'ensemble de tags et identifiants des clés - Prochaine clé racine (pour le prochain ratchet (mécanisme de cliquet cryptographique)) - Nombre de messages dans l'ensemble de tags actuel

**État du récepteur:** - Ensemble(s) d’étiquettes entrantes actuel(s) (il peut y en avoir deux pendant la période de grâce) - Numéros des messages précédents (PN) pour la détection des écarts - Fenêtre d’anticipation d’étiquettes pré-générées - Prochaine clé racine (pour le prochain ratchet, mécanisme de cliquet cryptographique)

**Règles de transition d'état :**

1. **Avant le premier Ratchet (mécanisme de chiffrement à cliquet)**:
   - Utilisation de l'ensemble de tags 0 (provenant de NSR)
   - Aucun identifiant de clé attribué

2. **Initialisation du Ratchet (mécanisme de cliquet cryptographique)**:
   - Générer une nouvelle clé (si l'expéditeur génère pour cette itération)
   - Envoyer le bloc NextKey dans le message ES
   - Attendre la réponse NextKey avant de créer un nouvel ensemble de tags sortants

3. **Réception d'une requête de ratchet (mécanisme à cliquet cryptographique)**:
   - Générer une nouvelle clé (si c'est au récepteur de générer à ce tour)
   - Effectuer un DH (Diffie-Hellman) avec la clé reçue
   - Créer un nouvel ensemble de tags entrants
   - Envoyer une réponse NextKey
   - Conserver l'ancien ensemble de tags entrants pendant une période de grâce

4. **Finalisation du Ratchet (mécanisme de cliquet cryptographique)**:
   - Recevoir la réponse NextKey
   - Effectuer l'échange DH
   - Créer un nouvel ensemble de tags sortants
   - Commencer à utiliser les nouveaux tags

### Mécanisme à cliquet des étiquettes de session

Le session tag ratchet (mécanisme à cliquet des étiquettes de session) génère de manière déterministe des étiquettes de session à usage unique de 8 octets.

### Objectif du cliquet des étiquettes de session

- Remplace la transmission explicite des étiquettes (ElGamal envoyait des étiquettes de 32 octets)
- Permet au récepteur de pré-générer des étiquettes pour une fenêtre d’anticipation
- L’expéditeur les génère à la demande (aucun stockage requis)
- Se synchronise avec le ratchet de clé symétrique (mécanisme à cliquet) via un index

### Formule du cliquet pour Session Tag (étiquette de session)

**Initialisation:**

```python
# From DH_INITIALIZE
sessTag_ck = initial_chain_key  # 32 bytes

# Initialize session tag ratchet
keydata = HKDF(sessTag_ck, ZEROLEN, "STInitialization", 64)
sessTag_chainKey = keydata[0:31]    # First chain key
SESSTAG_CONSTANT = keydata[32:63]   # Constant for all tags in this tagset
```
**Génération de l'étiquette (pour l'étiquette N):**

```python
# Generate tag N
keydata = HKDF(sessTag_chainKey_(N-1), SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
sessTag_chainKey_N = keydata[0:31]  # Chain key for next tag
tag_N = keydata[32:39]              # Session tag (8 bytes)

# Chain continues for each tag
# tag_0, tag_1, tag_2, ..., tag_65535
```
**Séquence complète :**

```python
# Tag 0
keydata_0 = HKDF(sessTag_chainKey, SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
sessTag_chainKey_0 = keydata_0[0:31]
tag_0 = keydata_0[32:39]

# Tag 1
keydata_1 = HKDF(sessTag_chainKey_0, SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
sessTag_chainKey_1 = keydata_1[0:31]
tag_1 = keydata_1[32:39]

# Tag N
keydata_N = HKDF(sessTag_chainKey_(N-1), SESSTAG_CONSTANT, "SessionTagKeyGen", 64)
sessTag_chainKey_N = keydata_N[0:31]
tag_N = keydata_N[32:39]
```
### Implémentation côté expéditeur du Session Tag Ratchet (mécanisme de cliquet pour les étiquettes de session)

```python
class OutboundTagset:
    def __init__(self, sessTag_ck):
        # Initialize
        keydata = HKDF(sessTag_ck, ZEROLEN, "STInitialization", 64)
        self.chainKey = keydata[0:31]
        self.constant = keydata[32:63]
        self.index = -1
    
    def get_next_tag(self):
        # Increment index
        self.index += 1
        
        if self.index > 65535:
            raise TagsetExhausted("Ratchet required")
        
        # Generate tag
        keydata = HKDF(self.chainKey, self.constant, "SessionTagKeyGen", 64)
        self.chainKey = keydata[0:31]
        tag = keydata[32:39]
        
        return (tag, self.index)
```
**Processus d’envoi:** 1. Appeler `get_next_tag()` pour chaque message 2. Utiliser le tag renvoyé dans le message ES 3. Stocker l’index N pour un suivi éventuel des ACK (accusé de réception) 4. Aucun stockage de tag n’est requis (généré à la demande)

### Implémentation du récepteur de Session Tag Ratchet (mécanisme à cliquet des étiquettes de session)

```python
class InboundTagset:
    def __init__(self, sessTag_ck, look_ahead=32):
        # Initialize
        keydata = HKDF(sessTag_ck, ZEROLEN, "STInitialization", 64)
        self.chainKey = keydata[0:31]
        self.constant = keydata[32:63]
        self.index = -1
        self.look_ahead = look_ahead
        self.tags = {}  # Dictionary: tag -> index
        
        # Pre-generate initial tags
        self.extend(look_ahead)
    
    def extend(self, count):
        """Generate 'count' more tags"""
        for _ in range(count):
            self.index += 1
            
            if self.index > 65535:
                return  # Cannot exceed maximum
            
            # Generate tag
            keydata = HKDF(self.chainKey, self.constant, "SessionTagKeyGen", 64)
            self.chainKey = keydata[0:31]
            tag = keydata[32:39]
            
            # Store tag
            self.tags[tag] = self.index
    
    def lookup_tag(self, tag):
        """Look up tag and return index"""
        if tag in self.tags:
            index = self.tags[tag]
            # Remove tag (one-time use)
            del self.tags[tag]
            return index
        return None
    
    def check_and_extend(self):
        """Extend if tag count is low"""
        current_count = len(self.tags)
        if current_count < self.look_ahead // 2:
            # Extend to restore window
            self.extend(self.look_ahead - current_count)
```
**Processus de réception:** 1. Pré-générer des étiquettes pour la fenêtre d’anticipation (p. ex., 32 étiquettes) 2. Stocker les étiquettes dans une table de hachage ou un dictionnaire 3. À l’arrivée d’un message, rechercher l’étiquette pour obtenir l’index N 4. Retirer l’étiquette du stockage (usage unique) 5. Étendre la fenêtre si le nombre d’étiquettes tombe en dessous du seuil

### Stratégie d’anticipation des tags de session

**Objectif**: Équilibrer l'utilisation de la mémoire et la gestion des messages arrivant dans le désordre

**Tailles d'anticipation recommandées:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Tagset Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Initial Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Maximum Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR tagset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Short-lived</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ES tagset 0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">24</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">160</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Initial ES tagset</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ES tagset 1+</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">160</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">160</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Ratcheted tagsets</td>
    </tr>
  </tbody>
</table>
**Anticipation adaptative:**

```python
# Dynamic look-ahead based on highest tag received
look_ahead = min(tsmax, tsmin + N // 4)

# Example:
# tsmin = 24, tsmax = 160
# N = 0:   look_ahead = min(160, 24 + 0/4) = 24
# N = 100: look_ahead = min(160, 24 + 100/4) = 49
# N = 500: look_ahead = min(160, 24 + 500/4) = 149
# N = 544: look_ahead = min(160, 24 + 544/4) = 160
```
**Élagage arrière:**

```python
# Trim tags far behind highest received
trim_behind = look_ahead // 2

# If highest received tag is N=100, trim tags below N=50
```
**Calcul de la mémoire :**

```python
# Per tag: 8 bytes (tag) + 2 bytes (index) + overhead ≈ 16 bytes
# Look-ahead of 160 tags ≈ 2.5 KB per inbound tagset

# With multiple sessions:
# 100 inbound sessions × 2.5 KB = 250 KB total
```
### Traitement des Session Tag (étiquettes de session) hors séquence

**Scénario**: Les messages arrivent dans le désordre

```
Expected: tag_5, tag_6, tag_7, tag_8
Received: tag_5, tag_7, tag_6, tag_8
```
**Comportement du récepteur:**

1. Recevoir tag_5:
   - Recherche: trouvé à l'index 5
   - Traiter le message
   - Supprimer tag_5
   - Plus haut reçu: 5

2. Recevoir tag_7 (hors séquence):
   - Recherche: trouvé à l'index 7
   - Traiter le message
   - Supprimer tag_7
   - Reçu le plus élevé: 7
   - Remarque: tag_6 toujours en stockage (pas encore reçu)

3. Réception de tag_6 (retardé):
   - Recherche: trouvé à l'index 6
   - Traiter le message
   - Supprimer tag_6
   - Maximum reçu: 7 (inchangé)

4. Recevoir tag_8:
   - Rechercher: trouvé à l'index 8
   - Traiter le message
   - Supprimer tag_8
   - Plus élevé reçu: 8

**Gestion de la fenêtre:** - Suivre le plus grand indice reçu - Maintenir une liste des indices manquants (lacunes) - Étendre la fenêtre en fonction du plus grand indice - Optionnel : supprimer les anciennes lacunes après expiration du délai

### Cliquet à clé symétrique

Le cliquet symétrique génère des clés de chiffrement de 32 octets synchronisées avec les étiquettes de session.

### Objectif du cliquet à clé symétrique

- Fournit une clé de chiffrement unique pour chaque message
- Synchronisé avec session tag ratchet (mécanisme de progression cryptographique des étiquettes de session; même index)
- L’expéditeur peut générer à la demande
- Le destinataire peut différer la génération jusqu’à réception de l’étiquette

### Formule du ratchet à clé symétrique (mécanisme à cliquet)

**Initialisation:**

```python
# From DH_INITIALIZE
symmKey_ck = initial_chain_key  # 32 bytes

# No additional initialization needed
# Unlike session tag ratchet, no constant is derived
```
**Génération de la clé (pour la clé N):**

```python
# Generate key N
SYMMKEY_CONSTANT = ZEROLEN  # Empty string
keydata = HKDF(symmKey_chainKey_(N-1), SYMMKEY_CONSTANT, "SymmetricRatchet", 64)
symmKey_chainKey_N = keydata[0:31]  # Chain key for next key
key_N = keydata[32:63]              # Session key (32 bytes)
```
**Séquence complète:**

```python
# Key 0
keydata_0 = HKDF(symmKey_ck, ZEROLEN, "SymmetricRatchet", 64)
symmKey_chainKey_0 = keydata_0[0:31]
key_0 = keydata_0[32:63]

# Key 1
keydata_1 = HKDF(symmKey_chainKey_0, ZEROLEN, "SymmetricRatchet", 64)
symmKey_chainKey_1 = keydata_1[0:31]
key_1 = keydata_1[32:63]

# Key N
keydata_N = HKDF(symmKey_chainKey_(N-1), ZEROLEN, "SymmetricRatchet", 64)
symmKey_chainKey_N = keydata_N[0:31]
key_N = keydata_N[32:63]
```
### Implémentation côté expéditeur du cliquet à clé symétrique

```python
class OutboundKeyRatchet:
    def __init__(self, symmKey_ck):
        self.chainKey = symmKey_ck
        self.index = -1
    
    def get_key(self, index):
        """Generate key for specific index"""
        # Fast-forward to desired index if needed
        while self.index < index:
            self.index += 1
            keydata = HKDF(self.chainKey, ZEROLEN, "SymmetricRatchet", 64)
            self.chainKey = keydata[0:31]
            if self.index == index:
                return keydata[32:63]
        
        # Should not reach here if called correctly
        raise ValueError("Key already generated")
```
**Processus de l'expéditeur:** 1. Récupérer l'étiquette suivante et son indice N 2. Générer une clé pour l'indice N 3. Utiliser la clé pour chiffrer le message 4. Aucun stockage de clé n'est requis

### Implémentation du récepteur du Symmetric Key Ratchet (cliquet symétrique)

**Stratégie 1: Génération différée (recommandée)**

```python
class InboundKeyRatchet:
    def __init__(self, symmKey_ck):
        self.chainKey = symmKey_ck
        self.index = -1
        self.cache = {}  # Optional: cache recently used keys
    
    def get_key(self, index):
        """Generate key for specific index"""
        # Check cache first (optional optimization)
        if index in self.cache:
            key = self.cache[index]
            del self.cache[index]
            return key
        
        # Fast-forward to desired index
        while self.index < index:
            self.index += 1
            keydata = HKDF(self.chainKey, ZEROLEN, "SymmetricRatchet", 64)
            self.chainKey = keydata[0:31]
            
            if self.index == index:
                return keydata[32:63]
        
        raise ValueError("Index already passed")
```
**Processus de génération différée:** 1. Recevoir un message ES avec un tag 2. Rechercher le tag pour obtenir l'index N 3. Générer les clés 0 à N (si elles n'ont pas déjà été générées) 4. Utiliser la clé N pour déchiffrer le message 5. La clé de chaîne est maintenant positionnée à l'index N

**Avantages :** - Utilisation mémoire minimale - Clés générées uniquement au besoin - Implémentation simple

**Inconvénients:** - Doit générer toutes les clés de 0 à N lors de la première utilisation - Ne peut pas gérer les messages reçus dans le désordre sans mise en cache

**Stratégie 2 : Pré-génération avec fenêtre de balises (alternative)**

```python
class InboundKeyRatchet:
    def __init__(self, symmKey_ck):
        self.chainKey = symmKey_ck
        self.index = -1
        self.keys = {}  # Dictionary: index -> key
    
    def extend(self, count):
        """Pre-generate 'count' more keys"""
        for _ in range(count):
            self.index += 1
            keydata = HKDF(self.chainKey, ZEROLEN, "SymmetricRatchet", 64)
            self.chainKey = keydata[0:31]
            key = keydata[32:63]
            self.keys[self.index] = key
    
    def get_key(self, index):
        """Retrieve pre-generated key"""
        if index in self.keys:
            key = self.keys[index]
            del self.keys[index]
            return key
        return None
```
**Processus de pré-génération:** 1. Pré-générer des clés correspondant à la fenêtre de tags (par exemple, 32 clés) 2. Stocker les clés indexées par numéro de message 3. À la réception d’un tag, rechercher la clé correspondante 4. Étendre la fenêtre au fur et à mesure que les tags sont utilisés

**Avantages :** - Gère naturellement les messages hors séquence - Récupération rapide des clés (aucun délai de génération)

**Inconvénients :** - Consommation mémoire plus élevée (32 octets par clé contre 8 octets par étiquette) - Les clés doivent rester synchronisées avec les étiquettes

**Comparaison de la mémoire:**

```python
# Look-ahead of 160:
# Tags only:  160 × 16 bytes = 2.5 KB
# Tags+Keys:  160 × (16 + 32) bytes = 7.5 KB
# 
# For 100 sessions:
# Tags only:  250 KB
# Tags+Keys:  750 KB
```
### Synchronisation du Ratchet symétrique (cliquet cryptographique) avec les Session Tags (étiquettes de session)

**Exigence critique**: L'index du tag de session DOIT être égal à l'index de la clé symétrique

```python
# Sender
tag, index = outbound_tagset.get_next_tag()
key = outbound_keyratchet.get_key(index)  # Same index
nonce = construct_nonce(index)
ciphertext = ENCRYPT(key, nonce, payload, tag)

# Receiver
index = inbound_tagset.lookup_tag(tag)
key = inbound_keyratchet.get_key(index)  # Same index
nonce = construct_nonce(index)
plaintext = DECRYPT(key, nonce, ciphertext, tag)
```
**Modes de défaillance:**

Si la synchronisation est rompue : - Mauvaise clé utilisée pour le déchiffrement - Échec de la vérification du MAC - Message rejeté

**Prévention:** - Toujours utiliser le même indice pour le tag et la clé - Ne jamais sauter des indices dans l’un ou l’autre ratchet (mécanisme à cliquet) - Traiter avec prudence les messages hors séquence

### Construction du nonce pour le Ratchet (mécanisme à cliquet) symétrique

Le nonce (nombre utilisé une seule fois) est dérivé du numéro de message :

```python
def construct_nonce(index):
    """
    Construct 12-byte nonce for ChaCha20-Poly1305
    
    Args:
        index: Message number (0-65535)
    
    Returns:
        nonce: 12-byte nonce
    """
    # First 4 bytes are always zero
    nonce = bytearray(12)
    nonce[0:4] = b'\x00\x00\x00\x00'
    
    # Last 8 bytes are little-endian message number
    nonce[4:12] = index.to_bytes(8, byteorder='little')
    
    return bytes(nonce)
```
**Exemples:**

```python
index = 0:     nonce = 0x00000000 0000000000000000
index = 1:     nonce = 0x00000000 0100000000000000
index = 255:   nonce = 0x00000000 FF00000000000000
index = 256:   nonce = 0x00000000 0001000000000000
index = 65535: nonce = 0x00000000 FFFF000000000000
```
**Propriétés importantes:** - Les nonces (nombre aléatoire à usage unique) sont uniques pour chaque message dans un tagset (ensemble de tags) - Les nonces ne se répètent jamais (les tags à usage unique le garantissent) - Un compteur sur 8 octets permet 2^64 messages (nous n'en utilisons que 2^16) - Le format du nonce correspond à la construction basée sur un compteur de la RFC 7539

---

## Gestion des sessions

### Contexte de session

Toutes les sessions entrantes et sortantes doivent appartenir à un contexte spécifique:

1. **Contexte du router**: Sessions pour le router lui-même
2. **Contexte de destination**: Sessions pour une destination locale spécifique (application cliente)

**Règle critique**: Les sessions NE DOIVENT PAS être partagées entre les contextes afin d'empêcher les attaques par corrélation.

**Implémentation:**

```python
class SessionKeyManager:
    """Context for managing sessions (router or destination)"""
    def __init__(self, context_id):
        self.context_id = context_id
        self.inbound_sessions = {}   # far_end_dest -> [sessions]
        self.outbound_sessions = {}  # far_end_dest -> session
        self.static_keypair = generate_keypair()  # Context's identity
    
    def get_outbound_session(self, destination):
        """Get or create outbound session to destination"""
        if destination not in self.outbound_sessions:
            self.outbound_sessions[destination] = create_outbound_session(destination)
        return self.outbound_sessions[destination]
    
    def add_inbound_session(self, session, destination=None):
        """Add inbound session, optionally bound to destination"""
        if destination:
            if destination not in self.inbound_sessions:
                self.inbound_sessions[destination] = []
            self.inbound_sessions[destination].append(session)
        else:
            # Unbound session
            self.inbound_sessions[None].append(session)
```
**Implémentation Java d'I2P:**

Dans Java I2P, la classe `SessionKeyManager` fournit cette fonctionnalité : - Un `SessionKeyManager` par router - Un `SessionKeyManager` par destination locale - Gestion distincte des sessions ECIES et ElGamal dans chaque contexte

### Liaison de session

**Binding** (association) associe une session à une destination distante spécifique.

### Sessions liées

**Caractéristiques:** - Inclut la clé statique de l'expéditeur dans le message NS - Le destinataire peut identifier la destination de l'expéditeur - Permet une communication bidirectionnelle - Une seule session sortante par destination - Peut avoir plusieurs sessions entrantes (pendant les transitions)

**Cas d’utilisation:** - Connexions en streaming (de type TCP) - Datagrammes répondables - Tout protocole nécessitant un modèle requête/réponse

**Processus de liaison:**

```python
# Alice creates bound outbound session
outbound_session = OutboundSession(
    destination=bob_destination,
    static_key=alice_static_key,
    bound=True
)

# Alice sends NS with static key
ns_message = build_ns_message(
    ephemeral_key=alice_ephemeral_key,
    static_key=alice_static_key,  # Included for binding
    payload=data
)

# Bob receives NS
bob_receives_ns(ns_message)
# Bob extracts Alice's static key
alice_static_key = decrypt_static_key_section(ns_message)

# Bob looks up Alice's destination (from bundled LeaseSet)
alice_destination = lookup_destination_by_static_key(alice_static_key)

# Bob creates bound inbound session
inbound_session = InboundSession(
    destination=alice_destination,
    bound=True
)

# Bob pairs with outbound session
outbound_session = OutboundSession(
    destination=alice_destination,
    bound=True
)
```
**Avantages:** 1. **DH éphémère-éphémère**: La réponse utilise un DH ee (confidentialité persistante totale) 2. **Continuité de session**: Les ratchets (mécanismes de cliquet cryptographiques) maintiennent la liaison avec la même destination 3. **Sécurité**: Empêche le détournement de session (authentification par clé statique) 4. **Efficacité**: Une seule session par destination (aucune duplication)

### Sessions non liées

**Caractéristiques:** - Aucune clé statique dans le NS message (message NS) (la section des indicateurs ne contient que des zéros) - Le destinataire ne peut pas identifier l'expéditeur - Communication unidirectionnelle uniquement - Plusieurs sessions vers la même destination autorisées

**Cas d'utilisation:** - Datagrammes bruts (envoi sans acquittement) - Publication anonyme - Messagerie de type diffusion

**Propriétés:** - Plus anonyme (pas d'identification de l'expéditeur) - Plus efficace (1 DH contre 2 DH lors du handshake (négociation initiale)) - Aucune réponse possible (le destinataire ne sait pas où répondre) - Pas de session ratcheting (mécanisme de renouvellement progressif des clés de session; utilisation unique ou limitée)

### Appariement de session

**L'appairage** relie une session entrante à une session sortante pour une communication bidirectionnelle.

### Création de sessions appariées

**Point de vue d'Alice (initiatrice):**

```python
# Create outbound session to Bob
outbound_session = create_outbound_session(bob_destination)

# Create paired inbound session
inbound_session = create_inbound_session(
    paired_with=outbound_session,
    bound_to=bob_destination
)

# Link them
outbound_session.paired_inbound = inbound_session
inbound_session.paired_outbound = outbound_session

# Send NS message
send_ns_message(outbound_session, payload)
```
**Point de vue de Bob (répondant):**

```python
# Receive NS message
ns_message = receive_ns_message()

# Create inbound session
inbound_session = create_inbound_session_from_ns(ns_message)

# If NS contains static key (bound):
if ns_message.has_static_key():
    alice_destination = extract_destination(ns_message)
    inbound_session.bind_to(alice_destination)
    
    # Create paired outbound session
    outbound_session = create_outbound_session(alice_destination)
    
    # Link them
    outbound_session.paired_inbound = inbound_session
    inbound_session.paired_outbound = outbound_session

# Send NSR
send_nsr_message(inbound_session, outbound_session, payload)
```
### Avantages de l'appairage de session

1. **Accusés de réception in-band (ACKs)**: Peuvent accuser réception des messages sans clove (sous-message encapsulé) séparé
2. **Ratcheting (mécanisme de cliquet cryptographique) efficace**: Les deux directions avancent de concert sur le même ratchet
3. **Contrôle de flux**: Peut mettre en œuvre une contre-pression entre des sessions appariées
4. **Cohérence de l’état**: Plus facile de maintenir un état synchronisé

### Règles d'appariement des sessions

- La session sortante peut être non appariée (NS non lié)
- La session entrante pour un NS lié doit être appariée
- L'appariement a lieu lors de la création de la session, pas après
- Les sessions appariées ont la même liaison de destination
- Les Ratchets (cliquets) se produisent indépendamment mais sont coordonnés

### Cycle de vie de la session

### Cycle de vie de la session : phase de création

**Création de session sortante (Alice):**

```python
def create_outbound_session(destination, bound=True):
    session = OutboundSession()
    session.destination = destination
    session.bound = bound
    session.state = SessionState.NEW
    session.created_time = now()
    
    # Generate keys for NS message
    session.ephemeral_keypair = generate_elg2_keypair()
    if bound:
        session.static_key = context.static_keypair.public_key
    
    # Will be populated after NSR received
    session.outbound_tagset = None
    session.inbound_tagset = None
    
    return session
```
**Création d'une session entrante (Bob) :**

```python
def create_inbound_session_from_ns(ns_message):
    session = InboundSession()
    session.state = SessionState.ESTABLISHED
    session.created_time = now()
    
    # Extract from NS
    session.remote_ephemeral_key = ns_message.ephemeral_key
    session.remote_static_key = ns_message.static_key
    
    if session.remote_static_key:
        session.bound = True
        session.destination = lookup_destination(session.remote_static_key)
    else:
        session.bound = False
        session.destination = None
    
    # Generate keys for NSR
    session.ephemeral_keypair = generate_elg2_keypair()
    
    # Create tagsets from KDF
    session.inbound_tagset = create_tagset_from_nsr()
    session.outbound_tagset = create_tagset_from_nsr()
    
    return session
```
### Cycle de vie de la session : phase active

**Transitions d'état:**

```
NEW (outbound only)
  ↓
  NS sent
  ↓
PENDING_REPLY (outbound only)
  ↓
  NSR received
  ↓
ESTABLISHED
  ↓
  ES messages exchanged
  ↓
ESTABLISHED (ongoing)
  ↓
  (optional) RATCHETING
  ↓
ESTABLISHED
```
**Maintien actif de la session:**

```python
def maintain_active_session(session):
    # Update last activity time
    session.last_activity = now()
    
    # Check for ratchet needed
    if session.outbound_tagset.needs_ratchet():
        initiate_ratchet(session)
    
    # Check for incoming ratchet
    if received_nextkey_block():
        process_ratchet(session)
    
    # Trim old tags from inbound tagset
    session.inbound_tagset.expire_old_tags()
    
    # Check session health
    if session.idle_time() > SESSION_TIMEOUT:
        mark_session_idle(session)
```
### Cycle de vie de la session : phase d’expiration

**Valeurs du délai d'expiration de session :**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Session Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Sender Timeout</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Receiver Timeout</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR tagset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">N/A</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Short-lived</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ES tagset 0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Initial</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ES tagset 1+</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Ratcheted</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Old tagset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">N/A</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3 minutes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">After ratchet</td>
    </tr>
  </tbody>
</table>
**Logique d’expiration :**

```python
def check_session_expiration():
    for session in active_sessions:
        # Outbound session expiration (sender)
        if session.is_outbound():
            if session.idle_time() > 8 * 60:  # 8 minutes
                expire_outbound_session(session)
        
        # Inbound session expiration (receiver)
        else:
            if session.idle_time() > 10 * 60:  # 10 minutes
                expire_inbound_session(session)
    
    # Old tagsets (after ratchet)
    for tagset in old_tagsets:
        if tagset.age() > 3 * 60:  # 3 minutes
            delete_tagset(tagset)
```
**Règle critique**: Les sessions sortantes DOIVENT expirer avant les sessions entrantes pour éviter toute désynchronisation.

**Arrêt en douceur:**

```python
def terminate_session(session, reason=0):
    # Send Termination block (if implemented)
    send_termination_block(session, reason)
    
    # Mark session for deletion
    session.state = SessionState.TERMINATED
    
    # Keep session briefly for final messages
    schedule_deletion(session, delay=30)  # 30 seconds
    
    # Notify paired session
    if session.paired_session:
        session.paired_session.mark_remote_terminated()
```
### Plusieurs messages NS

**Scénario**: Le message NS d'Alice est perdu ou la réponse NSR est perdue.

**Comportement d'Alice :**

```python
class OutboundSession:
    def __init__(self):
        self.ns_messages_sent = []
        self.ns_timer = None
        self.max_ns_attempts = 5
    
    def send_ns_message(self, payload):
        # Generate new ephemeral key for each NS
        ephemeral_key = generate_elg2_keypair()
        
        ns_message = build_ns_message(
            ephemeral_key=ephemeral_key,
            static_key=self.static_key,
            payload=payload
        )
        
        # Store state for this NS
        ns_state = {
            'ephemeral_key': ephemeral_key,
            'chainkey': compute_chainkey(ns_message),
            'hash': compute_hash(ns_message),
            'tagset': derive_nsr_tagset(ns_message),
            'sent_time': now()
        }
        self.ns_messages_sent.append(ns_state)
        
        # Send message
        send_message(ns_message)
        
        # Set timer for retry
        if not self.ns_timer:
            self.ns_timer = set_timer(1.0, self.on_ns_timeout)
    
    def on_ns_timeout(self):
        if len(self.ns_messages_sent) >= self.max_ns_attempts:
            # Give up
            fail_session("No NSR received after {self.max_ns_attempts} attempts")
            return
        
        # Retry with new NS message
        send_ns_message(self.payload)
    
    def on_nsr_received(self, nsr_message):
        # Cancel timer
        cancel_timer(self.ns_timer)
        
        # Find which NS this NSR responds to
        tag = nsr_message.tag
        for ns_state in self.ns_messages_sent:
            if tag in ns_state['tagset']:
                # This NSR corresponds to this NS
                self.active_ns_state = ns_state
                break
        
        # Process NSR and complete handshake
        complete_handshake(nsr_message, self.active_ns_state)
        
        # Discard other NS states
        self.ns_messages_sent = []
```
**Propriétés importantes :**

1. **Clés éphémères uniques**: Chaque NS utilise une clé éphémère différente
2. **Négociations indépendantes**: Chaque NS crée un état de négociation distinct
3. **Corrélation NSR**: L'étiquette NSR identifie le NS auquel elle répond
4. **Nettoyage de l'état**: Les états de NS inutilisés sont supprimés après une NSR réussie

**Prévention des attaques :**

Pour éviter l'épuisement des ressources :

```python
# Limit NS sending rate
max_ns_rate = 5 per 10 seconds per destination

# Limit total NS attempts
max_ns_attempts = 5

# Limit total pending NS states
max_pending_ns = 10 per context
```
### Plusieurs messages NSR

**Scénario** : Bob envoie plusieurs NSRs (terme technique; par exemple, des données de réponse découpées en plusieurs messages).

**Comportement de Bob :**

```python
class InboundSession:
    def send_nsr_replies(self, payload_chunks):
        # One NS received, multiple NSRs to send
        for chunk in payload_chunks:
            # Generate new ephemeral key for each NSR
            ephemeral_key = generate_elg2_keypair()
            
            # Get next tag from NSR tagset
            tag = self.nsr_tagset.get_next_tag()
            
            nsr_message = build_nsr_message(
                tag=tag,
                ephemeral_key=ephemeral_key,
                payload=chunk
            )
            
            send_message(nsr_message)
        
        # Wait for ES message from Alice
        self.state = SessionState.AWAITING_ES
```
**Comportement d'Alice:**

```python
class OutboundSession:
    def on_nsr_received(self, nsr_message):
        if self.state == SessionState.PENDING_REPLY:
            # First NSR received
            complete_handshake(nsr_message)
            self.state = SessionState.ESTABLISHED
            
            # Create ES sessions
            self.es_outbound_tagset = derive_es_outbound_tagset()
            self.es_inbound_tagset = derive_es_inbound_tagset()
            
            # Send ES message (ACK)
            send_es_message(empty_payload)
        
        elif self.state == SessionState.ESTABLISHED:
            # Additional NSR received
            # Decrypt and process payload
            payload = decrypt_nsr_payload(nsr_message)
            process_payload(payload)
            
            # These NSRs are from other NS attempts, ignore handshake
```
**Nettoyage de Bob:**

```python
class InboundSession:
    def on_es_received(self, es_message):
        # First ES received from Alice
        # This confirms which NSR Alice used
        
        # Clean up other handshake states
        for other_ns_state in self.pending_ns_states:
            if other_ns_state != self.active_ns_state:
                delete_ns_state(other_ns_state)
        
        # Delete unused NSR tagsets
        for tagset in self.nsr_tagsets:
            if tagset != self.active_nsr_tagset:
                delete_tagset(tagset)
        
        self.state = SessionState.ESTABLISHED
```
**Propriétés importantes :**

1. **Plusieurs NSR autorisées**: Bob peut envoyer plusieurs NSR par NS
2. **Clés éphémères différentes**: Chaque NSR doit utiliser une clé éphémère unique
3. **Même tagset (jeu de tags) pour les NSR**: Toutes les NSR pour un même NS utilisent le même tagset
4. **Le premier ES l'emporte**: Le premier ES d'Alice détermine quelle NSR a réussi
5. **Nettoyage après ES**: Bob supprime les états inutilisés après réception de l'ES

### Automate à états de session

**Diagramme d'états complet:**

```
                    Outbound Session                    Inbound Session

                         NEW
                          |
                     send NS
                          |
                   PENDING_REPLY -------------------- receive NS ---> ESTABLISHED
                          |                                                |
                   receive NSR                                        send NSR
                          |                                                |
                    ESTABLISHED <---------- receive ES ------------- AWAITING_ES
                          |                     |                          |
                    ┌─────┴─────┐               |                    receive ES
                    |           |               |                          |
              send ES      receive ES           |                    ESTABLISHED
                    |           |               |                          |
                    └─────┬─────┘               |                ┌─────────┴─────────┐
                          |                     |                |                   |
                          |                     |          send ES              receive ES
                          |                     |                |                   |
                          |                     |                └─────────┬─────────┘
                          |                     |                          |
                          └─────────────────────┴──────────────────────────┘
                                              ACTIVE
                                                |
                                         idle timeout
                                                |
                                             EXPIRED
```
**Descriptions des états :**

- **NEW**: Session sortante créée, aucun NS envoyé pour l’instant
- **PENDING_REPLY**: NS envoyé, en attente du NSR
- **AWAITING_ES**: NSR envoyé, en attente du premier ES d’Alice
- **ESTABLISHED**: Négociation initiale (handshake) terminée, peut envoyer/recevoir des ES
- **ACTIVE**: Échange activement des messages ES
- **RATCHETING**: DH ratchet (mécanisme à cliquet Diffie-Hellman) en cours (sous-ensemble de ACTIVE)
- **EXPIRED**: Session expirée, en attente de suppression
- **TERMINATED**: Session explicitement terminée

---

## Format de la charge utile

La section de charge utile de tous les messages ECIES (schéma de chiffrement intégré à courbe elliptique) (NS, NSR, ES) utilise un format basé sur des blocs similaire à NTCP2.

### Structure des blocs

**Format général :**

```
+----+----+----+----+----+----+----+----+
|blk |  size   |       data             |
+----+----+----+                        +
|                                       |
~               ...                     ~
|                                       |
+----+----+----+----+----+----+----+----+
|blk |  size   |       data             |
+----+----+----+                        +
|                                       |
~               ...                     ~
|                                       |
+----+----+----+----+----+----+----+----+
```
**Champs :**

- `blk`: 1 octet - Numéro de type de bloc
- `size`: 2 octets - Taille Big-endian du champ de données (0-65516)
- `data`: Longueur variable - Données spécifiques au bloc

**Contraintes:**

- Trame ChaChaPoly maximale : 65535 octets
- MAC Poly1305 (code d'authentification de message) : 16 octets
- Taille totale maximale des blocs : 65519 octets (65535 - 16)
- Taille maximale d’un bloc unique : 65519 octets (en incluant un en-tête de 3 octets)
- Taille maximale des données d’un bloc unique : 65516 octets

### Types de blocs

**Types de blocs définis :**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DateTime</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">7 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Required in NS</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1-3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Future use</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Termination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">9+ bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unimplemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Session termination</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Options</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">21+ bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unimplemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Session options</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">MessageNumbers</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">5 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unimplemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">PN value</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NextKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">3 or 35 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DH ratchet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ACK</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">4+ bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Message acknowledgment</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">9</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ACK Request</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">3 bytes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Request ACK</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Future use</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Garlic Clove</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Variable</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Application data</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12-223</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Future use</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">224-253</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Variable</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Testing features</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">254</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Padding</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Variable</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implemented</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Traffic shaping</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">255</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Future extension</td>
    </tr>
  </tbody>
</table>
**Gestion des blocs inconnus:**

Les implémentations DOIVENT ignorer les blocs dont le numéro de type est inconnu et les traiter comme du remplissage. Cela assure la compatibilité ascendante.

### Règles d'ordonnancement des blocs

### Ordre des messages NS

**Obligatoire:** - Le bloc DateTime DOIT être le premier

**Autorisés :** - Garlic Clove (sous-message « gousse d'ail ») (type 11) - Options (type 5) - si implémenté - Bourrage (type 254)

**Interdits:** - NextKey, ACK, ACK Request, Termination, MessageNumbers

**Exemple de charge utile NS valide :**

```
DateTime (0) | Garlic Clove (11) | Garlic Clove (11) | Padding (254)
```
### Ordre des messages NSR

**Requis:** - Aucun (la charge utile peut être vide)

**Autorisé :** - Garlic Clove (sous-unité de garlic encryption, type 11) - Options (type 5) - si implémenté - Bourrage (type 254)

**Interdits:** - DateTime, NextKey, ACK, ACK Request, Termination, MessageNumbers

**Exemple de charge utile NSR valide :**

```
Garlic Clove (11) | Garlic Clove (11) | Padding (254)
```
ou

```
(empty - ACK only)
```
### Ordonnancement des messages ES

**Obligatoire:** - Aucun (la charge utile peut être vide)

**Autorisés (dans n'importe quel ordre) :** - Garlic Clove (sous-message 'clove') (type 11) - NextKey (type 7) - ACK (type 8) - ACK Request (type 9) - Termination (type 4) - si implémenté - MessageNumbers (type 6) - si implémenté - Options (type 5) - si implémenté - Padding (type 254)

**Règles spéciales :** - Termination DOIT être le dernier bloc (sauf Padding) - Padding DOIT être le dernier bloc - Plusieurs Garlic Cloves autorisés (gousses/sous-messages) - Jusqu'à 2 blocs NextKey autorisés (aller et retour) - Plusieurs blocs Padding NON autorisés

**Exemples de charges utiles ES valides :**

```
Garlic Clove (11) | ACK (8) | Padding (254)
```
```
NextKey (7) | Garlic Clove (11) | Garlic Clove (11)
```
```
NextKey (7) forward | NextKey (7) reverse | Garlic Clove (11)
```
```
ACK Request (9) | Garlic Clove (11) | Termination (4) | Padding (254)
```
### Bloc DateTime (Type 0)

**Objectif**: Horodatage pour la prévention des attaques par rejeu et la validation du décalage d'horloge

**Taille**: 7 octets (en-tête de 3 octets + 4 octets de données)

**Format :**

```
+----+----+----+----+----+----+----+
| 0  |    4    |     timestamp     |
+----+----+----+----+----+----+----+
```
**Champs:**

- `blk`: 0
- `size`: 4 (big-endian, octets de poids fort en premier)
- `timestamp`: 4 octets - horodatage Unix en secondes (non signé, big-endian)

**Format d'horodatage :**

```python
timestamp = int(time.time())  # Seconds since 1970-01-01 00:00:00 UTC
# Wraps around in year 2106 (4-byte unsigned maximum)
```
**Règles de validation :**

```python
MAX_CLOCK_SKEW_PAST = 5 * 60      # 5 minutes
MAX_CLOCK_SKEW_FUTURE = 2 * 60    # 2 minutes

def validate_datetime(timestamp):
    now = int(time.time())
    age = now - timestamp
    
    if age < -MAX_CLOCK_SKEW_FUTURE:
        return False  # Too far in future
    
    if age > MAX_CLOCK_SKEW_PAST:
        return False  # Too old
    
    return True
```
**Prévention du rejeu:**

```python
class ReplayFilter:
    def __init__(self, duration=5*60):
        self.duration = duration  # 5 minutes
        self.seen_messages = BloomFilter(size=100000, false_positive_rate=0.001)
        self.cleanup_timer = RepeatTimer(60, self.cleanup)
    
    def check_replay(self, ephemeral_key, timestamp):
        # Check timestamp validity
        if not validate_datetime(timestamp):
            return False
        
        # Check if ephemeral key seen recently
        if ephemeral_key in self.seen_messages:
            return False  # Replay attack
        
        # Add to seen messages
        self.seen_messages.add(ephemeral_key)
        return True
    
    def cleanup(self):
        # Expire old entries (Bloom filter automatically ages out)
        pass
```
**Notes d'implémentation:**

1. **Messages NS**: DateTime DOIT être le premier bloc
2. **Messages NSR/ES**: DateTime généralement non inclus
3. **Fenêtre de rejeu**: 5 minutes sont le minimum recommandé
4. **Filtre de Bloom**: Recommandé pour une détection efficace des rejeux
5. **Dérive d'horloge**: Tolérer 5 minutes dans le passé, 2 minutes dans le futur

### Garlic Clove Block (bloc « clove » dans un message Garlic) (Type 11)

**Objectif**: Encapsule les messages I2NP pour l'acheminement

**Format :**

```
+----+----+----+----+----+----+----+----+
| 11 |  size   |                        |
+----+----+----+                        +
|      Delivery Instructions            |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|type|  Message_ID       | Expiration  |
+----+----+----+----+----+----+----+----+
     |      I2NP Message body           |
+----+                                  +
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
```
**Champs :**

- `blk`: 11
- `size`: Taille totale du clove (sous-message d'un message 'garlic', variable)
- `Delivery Instructions`: Comme indiqué dans la spécification I2NP
- `type`: Type de message I2NP (1 octet)
- `Message_ID`: ID de message I2NP (4 octets)
- `Expiration`: Horodatage Unix en secondes (4 octets)
- `I2NP Message body`: Données de message de longueur variable

**Formats des instructions d'acheminement:**

**Livraison locale** (1 octet) :

```
+----+
|0x00|
+----+
```
**Remise à la destination** (33 octets):

```
+----+----+----+----+----+----+----+----+
|0x01|                                  |
+----+        Destination Hash         +
|              32 bytes                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
**Remise au Router** (33 octets):

```
+----+----+----+----+----+----+----+----+
|0x02|                                  |
+----+         Router Hash              +
|              32 bytes                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
**Acheminement via Tunnel** (37 octets):

```
+----+----+----+----+----+----+----+----+
|0x03|         Tunnel ID                |
+----+----+----+----+----+              +
|           Router Hash                 |
+              32 bytes                 +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
**En-tête de message I2NP** (9 octets au total) :

```
+----+----+----+----+----+----+----+----+
|type|      msg_id       |  expiration   |
+----+----+----+----+----+----+----+----+
     |                                   |
```
- `type`: type de message I2NP (Database Store, Database Lookup, Data, etc.)
- `msg_id`: identifiant de message sur 4 octets
- `expiration`: horodatage Unix sur 4 octets (secondes)

**Principales différences par rapport au format ElGamal Clove :**

1. **Pas de certificat**: Champ Certificate omis (non utilisé avec ElGamal)
2. **Pas d'ID de Clove (sous-message encapsulé)**: ID de Clove omis (valait toujours 0)
3. **Pas d'expiration de Clove**: Utilise à la place l'expiration du message I2NP
4. **En-tête compact**: En-tête I2NP de 9 octets, contre le format ElGamal plus volumineux
5. **Chaque Clove est un bloc distinct**: Pas de structure CloveSet (ensemble de Clove)

**Plusieurs Cloves (sous-messages dans un message garlic):**

```python
# Multiple Garlic Cloves in one message
payload = [
    build_datetime_block(),
    build_garlic_clove(i2np_message_1),
    build_garlic_clove(i2np_message_2),
    build_garlic_clove(i2np_message_3),
    build_padding_block()
]
```
**Types de messages I2NP courants dans les Cloves (gousses) :**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseStore</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Publishing LeaseSet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseLookup</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Requesting LeaseSet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DeliveryStatus</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ACK (legacy, avoid in ECIES)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Streaming data</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">21</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Garlic</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Nested garlic messages</td>
    </tr>
  </tbody>
</table>
**Traitement des Cloves (sous-messages encapsulés):**

```python
def process_garlic_clove(clove_data):
    # Parse delivery instructions
    delivery_type = clove_data[0]
    
    if delivery_type == 0x00:
        # Local delivery
        offset = 1
    elif delivery_type == 0x01:
        # Destination delivery
        dest_hash = clove_data[1:33]
        offset = 33
    elif delivery_type == 0x02:
        # Router delivery
        router_hash = clove_data[1:33]
        offset = 33
    elif delivery_type == 0x03:
        # Tunnel delivery
        tunnel_id = struct.unpack('>I', clove_data[1:5])[0]
        router_hash = clove_data[5:37]
        offset = 37
    
    # Parse I2NP header
    i2np_type = clove_data[offset]
    msg_id = struct.unpack('>I', clove_data[offset+1:offset+5])[0]
    expiration = struct.unpack('>I', clove_data[offset+5:offset+9])[0]
    
    # Extract I2NP body
    i2np_body = clove_data[offset+9:]
    
    # Process message
    process_i2np_message(i2np_type, msg_id, expiration, i2np_body)
```
### Bloc NextKey (Type 7)

**Objectif**: échange de clés DH ratchet (mécanisme à cliquet Diffie-Hellman)

**Format (clé présente - 38 octets):**

```
+----+----+----+----+----+----+----+----+
| 7  |   35    |flag|  key ID |         |
+----+----+----+----+----+----+         +
|                                       |
+     Next DH Ratchet Public Key        +
|              32 bytes                 |
+                                       +
|                                       |
+                             +----+----+
|                             |
+----+----+----+----+----+----+
```
**Format (ID de clé uniquement - 6 octets):**

```
+----+----+----+----+----+----+
| 7  |    3    |flag|  key ID |
+----+----+----+----+----+----+
```
**Champs :**

- `blk`: 7
- `size`: 3 (ID uniquement) ou 35 (avec clé)
- `flag`: 1 octet - Bits de drapeau
- `key ID`: 2 octets - Identifiant de clé Big-endian (ordre des octets du poids fort en premier) (0-32767)
- `Public Key`: 32 octets - clé publique X25519 (little-endian, ordre des octets du poids faible en premier), si le bit 0 du drapeau = 1

**Bits de drapeau:**

```
Bit 7 6 5 4 3 2 1 0
    | | | | | | | |
    | | | | | | | +-- Bit 0: Key present (1) or ID only (0)
    | | | | | | +---- Bit 1: Reverse key (1) or forward key (0)
    | | | | | +------ Bit 2: Request reverse key (1) or no request (0)
    | | | | |
    +-+-+-+-+-------- Bits 3-7: Reserved (set to 0)
```
**Exemples de flags (indicateurs) :**

```python
# Forward key present
flags = 0x01  # Binary: 00000001

# Reverse key present
flags = 0x03  # Binary: 00000011

# Forward key ID only (ACK)
flags = 0x00  # Binary: 00000000

# Reverse key ID only (ACK)
flags = 0x02  # Binary: 00000010

# Forward key ID with reverse request
flags = 0x04  # Binary: 00000100
```
**Règles pour les ID de clé:**

- Les ID sont séquentiels : 0, 1, 2, ..., 32767
- L'ID ne s'incrémente que lorsqu'une nouvelle clé est générée
- Le même ID est utilisé pour plusieurs messages jusqu'au prochain ratchet (mécanisme de renouvellement de clés)
- L'ID maximal est 32767 (il faut démarrer une nouvelle session après)

**Exemples d'utilisation :**

```python
# Initiating ratchet (sender generates new key)
nextkey = NextKeyBlock(
    flags=0x01,           # Key present, forward
    key_id=0,
    public_key=sender_new_pk
)

# Replying to ratchet (receiver generates new key)
nextkey = NextKeyBlock(
    flags=0x03,           # Key present, reverse
    key_id=0,
    public_key=receiver_new_pk
)

# Acknowledging ratchet (no new key from sender)
nextkey = NextKeyBlock(
    flags=0x02,           # ID only, reverse
    key_id=0
)

# Requesting reverse ratchet
nextkey = NextKeyBlock(
    flags=0x04,           # Request reverse, forward ID
    key_id=1
)
```
**Logique de traitement :**

```python
def process_nextkey_block(block):
    flags = block.flags
    key_id = block.key_id
    
    key_present = (flags & 0x01) != 0
    is_reverse = (flags & 0x02) != 0
    request_reverse = (flags & 0x04) != 0
    
    if key_present:
        public_key = block.public_key
        
        if is_reverse:
            # Reverse key received
            perform_dh_ratchet(receiver_key=public_key, key_id=key_id)
            # Sender should ACK with own key ID
        else:
            # Forward key received
            perform_dh_ratchet(sender_key=public_key, key_id=key_id)
            # Receiver should reply with reverse key
            send_reverse_key(generate_new_key())
    
    else:
        # Key ID only (ACK)
        if is_reverse:
            # Reverse key ACK
            confirm_reverse_ratchet(key_id)
        else:
            # Forward key ACK
            confirm_forward_ratchet(key_id)
    
    if request_reverse:
        # Sender requests receiver to generate new key
        send_reverse_key(generate_new_key())
```
**Plusieurs blocs NextKey :**

Un seul message ES peut contenir jusqu'à 2 blocs NextKey lorsque les deux directions appliquent le mécanisme de ratchet (mécanisme à cliquet) simultanément:

```python
# Both directions ratcheting
payload = [
    NextKeyBlock(flags=0x01, key_id=2, public_key=forward_key),  # Forward
    NextKeyBlock(flags=0x03, key_id=1, public_key=reverse_key),  # Reverse
    build_garlic_clove(data)
]
```
### Bloc ACK (Type 8)

**Objectif**: Accuser réception des messages reçus en bande

**Format (ACK unique - 7 octets):**

```
+----+----+----+----+----+----+----+
| 8  |    4    |tagsetid |   N     |
+----+----+----+----+----+----+----+
```
**Format (accusés de réception multiples):**

```
+----+----+----+----+----+----+----+----+
| 8  |  size   |tagsetid |   N     |    |
+----+----+----+----+----+----+----+    +
|            more ACKs                  |
~               ...                     ~
|                                       |
+----+----+----+----+----+----+----+----+
```
**Champs:**

- `blk`: 8
- `size`: 4 * nombre d'ACK (acquittements) (minimum 4)
- Pour chaque ACK:
  - `tagsetid`: 2 octets - ID de l'ensemble de tags en Big-endian (octets de poids fort en premier) (0-65535)
  - `N`: 2 octets - numéro de message en Big-endian (0-65535)

**Détermination de l'ID de l'ensemble d'étiquettes :**

```python
# Tag set 0 (initial, after NSR)
tagset_id = 0

# After first ratchet (tag set 1)
# Both Alice and Bob sent key ID 0
tagset_id = 1 + 0 + 0 = 1

# After second ratchet (tag set 2)
# Alice sent key ID 1, Bob still using key ID 0
tagset_id = 1 + 1 + 0 = 2

# After third ratchet (tag set 3)
# Alice still using key ID 1, Bob sent key ID 1
tagset_id = 1 + 1 + 1 = 3
```
**Exemple d'un accusé de réception (ACK) unique:**

```python
# ACK message from tag set 5, message number 127
ack_block = ACKBlock(
    tagset_id=5,
    message_number=127
)

# Wire format (7 bytes):
# 08 00 04 00 05 00 7F
# |  |  |  |  |  |  |
# |  |  |  |  |  |  +-- N (127)
# |  |  |  |  +--------- N high byte
# |  |  |  +------------ tagset_id (5)
# |  |  +--------------- tagset_id high byte
# |  +------------------ size (4)
# +--------------------- type (8)
```
**Exemple d’ACK multiples:**

```python
# ACK three messages
ack_block = ACKBlock([
    (tagset_id=3, N=42),
    (tagset_id=3, N=43),
    (tagset_id=4, N=0)
])

# Wire format (15 bytes):
# 08 00 0C 00 03 00 2A 00 03 00 2B 00 04 00 00
#                (ts=3, N=42) (ts=3, N=43) (ts=4, N=0)
```
**Traitement:**

```python
def process_ack_block(block):
    num_acks = block.size // 4
    
    for i in range(num_acks):
        offset = i * 4
        tagset_id = struct.unpack('>H', block.data[offset:offset+2])[0]
        message_num = struct.unpack('>H', block.data[offset+2:offset+4])[0]
        
        # Mark message as acknowledged
        mark_acked(tagset_id, message_num)
        
        # May trigger retransmission timeout cancellation
        cancel_retransmit_timer(tagset_id, message_num)
```
**Quand envoyer des ACK :**

1. **Demande explicite d’accusé de réception (ACK)**: Toujours répondre au bloc de demande d’ACK
2. **Livraison du LeaseSet**: Lorsque l’expéditeur inclut un LeaseSet dans le message
3. **Établissement de session**: Peut envoyer un accusé de réception pour NS/NSR (bien que le protocole préfère un accusé de réception implicite via ES)
4. **Confirmation du Ratchet (mécanisme de cliquet cryptographique)**: Peut accuser réception de NextKey
5. **Couche applicative**: Selon les exigences du protocole de couche supérieure (p. ex., Streaming)

**Temporisation des ACK:**

```python
class ACKManager:
    def __init__(self):
        self.pending_acks = []
        self.ack_timer = None
    
    def request_ack(self, tagset_id, message_num):
        self.pending_acks.append((tagset_id, message_num))
        
        if not self.ack_timer:
            # Delay ACK briefly to allow higher layer to respond
            self.ack_timer = set_timer(0.1, self.send_acks)  # 100ms
    
    def send_acks(self):
        if self.pending_acks and not has_outbound_data():
            # No higher layer data, send explicit ACK
            send_es_message(build_ack_block(self.pending_acks))
        
        # Otherwise, ACK will piggyback on next ES message
        self.pending_acks = []
        self.ack_timer = None
```
### Bloc de demande d'ACK (accusé de réception) (Type 9)

**Objectif**: Demander un accusé de réception in-band (dans le même canal) du message en cours

**Format :**

```
+----+----+----+----+
| 9  |    1    |flg |
+----+----+----+----+
```
**Champs:**

- `blk`: 9
- `size`: 1
- `flg`: 1 octet - Drapeaux (tous les bits actuellement inutilisés, positionnés à 0)

**Utilisation:**

```python
# Request ACK for this message
payload = [
    build_ack_request_block(),
    build_garlic_clove(important_data)
]
```
**Réponse du récepteur:**

Lorsqu'une ACK Request (requête d'accusé de réception) est reçue:

1. **Avec données immédiates**: Inclure un bloc ACK dans la réponse immédiate
2. **Sans données immédiates**: Démarrer un minuteur (p. ex., 100ms) et envoyer un ES vide avec ACK si le minuteur expire
3. **Tag Set ID**: Utiliser l'ID de tagset (ensemble de balises) entrant actuel
4. **Numéro de message**: Utiliser le numéro de message associé au tag de session reçu

**Traitement :**

```python
def process_ack_request(message):
    # Extract message identification
    tagset_id = message.tagset_id
    message_num = message.message_num
    
    # Schedule ACK
    schedule_ack(tagset_id, message_num)
    
    # If no data to send immediately, start timer
    if not has_pending_data():
        set_timer(0.1, lambda: send_ack_only(tagset_id, message_num))
```
**Quand utiliser une requête d’ACK :**

1. **Messages critiques**: Messages qui doivent être accusés de réception
2. **Transmission d'un LeaseSet**: Lors de l'inclusion d'un LeaseSet
3. **Session Ratchet (mécanisme de ratchet de session)**: Après l'envoi du bloc NextKey
4. **Fin de transmission**: Lorsque l'expéditeur n'a plus de données à envoyer mais souhaite une confirmation

**Quand NE PAS l'utiliser :**

1. **Protocole de streaming**: La couche de streaming gère les ACK (accusés de réception)
2. **Messages à haute fréquence**: Éviter une requête d’ACK pour chaque message (surcharge)
3. **Datagrammes peu importants**: Les datagrammes bruts n’ont généralement pas besoin d’ACK

### Bloc de terminaison (Type 4)

**Statut**: NON IMPLÉMENTÉ

**Objectif**: Terminer la session proprement

**Format :**

```
+----+----+----+----+----+----+----+----+
| 4  |  size   | rsn|     addl data     |
+----+----+----+----+                   +
~               ...                     ~
+----+----+----+----+----+----+----+----+
```
**Champs:**

- `blk`: 4
- `size`: 1 octet ou plus
- `rsn`: 1 octet - Code de motif
- `addl data`: Données supplémentaires facultatives (le format dépend du motif)

**Codes de cause :**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Meaning</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Additional Data</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Normal close / unspecified</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">None</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Termination received</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">None</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Idle timeout</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">None (implementation-specific)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Resource exhaustion</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">None (implementation-specific)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4+</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Implementation-specific</td>
    </tr>
  </tbody>
</table>
**Utilisation (lorsque cela sera implémenté) :**

```python
# Normal session close
termination = TerminationBlock(
    reason=0,
    additional_data=b''
)

# Session termination due to received termination
termination = TerminationBlock(
    reason=1,
    additional_data=b''
)
```
**Règles:**

- DOIT être le dernier bloc sauf Padding (remplissage)
- Padding (remplissage) DOIT suivre Termination (terminaison) si présent
- Interdit dans les messages NS ou NSR
- Autorisé uniquement dans les messages ES

### Bloc d'options (Type 5)

**Statut**: NON IMPLÉMENTÉ

**Objectif**: Négocier les paramètres de session

**Format:**

```
+----+----+----+----+----+----+----+----+
| 5  |  size   |ver |flg |STL |STimeout |
+----+----+----+----+----+----+----+----+
|  SOTW   |  RITW   |tmin|tmax|rmin|rmax|
+----+----+----+----+----+----+----+----+
|  tdmy   |  rdmy   |  tdelay |  rdelay |
+----+----+----+----+----+----+----+----+
|              more_options             |
~               ...                     ~
|                                       |
+----+----+----+----+----+----+----+----+
```
**Champs:**

- `blk`: 5
- `size`: 21 octets ou plus
- `ver`: 1 octet - Version du protocole (doit être 0)
- `flg`: 1 octet - Drapeaux (tous les bits actuellement inutilisés)
- `STL`: 1 octet - Longueur du tag de session (doit être 8)
- `STimeout`: 2 octets - Délai d'inactivité de session en secondes (big-endian, octet de poids fort en premier)
- `SOTW`: 2 octets - Fenêtre de tags sortants de l'émetteur (big-endian)
- `RITW`: 2 octets - Fenêtre de tags entrants du récepteur (big-endian)
- `tmin`, `tmax`, `rmin`, `rmax`: 1 octet chacun - Paramètres de bourrage (format à virgule fixe 4.4)
- `tdmy`: 2 octets - Trafic factice maximum que l'on est disposé à envoyer (octets/s, big-endian)
- `rdmy`: 2 octets - Trafic factice demandé (octets/s, big-endian)
- `tdelay`: 2 octets - Délai intra-message maximal que l'on est disposé à insérer (msec, big-endian)
- `rdelay`: 2 octets - Délai intra-message demandé (msec, big-endian)
- `more_options`: Variable - Extensions futures

**Paramètres de bourrage (4.4 à virgule fixe):**

```python
def encode_padding_ratio(ratio):
    """
    Encode padding ratio as 4.4 fixed-point
    
    ratio: 0.0 to 15.9375
    returns: 0x00 to 0xFF
    """
    return int(ratio * 16)

def decode_padding_ratio(encoded):
    """
    Decode 4.4 fixed-point to ratio
    
    encoded: 0x00 to 0xFF
    returns: 0.0 to 15.9375
    """
    return encoded / 16.0

# Examples:
# 0x00 = 0.0 (no padding)
# 0x01 = 0.0625 (6.25% padding)
# 0x10 = 1.0 (100% padding - double traffic)
# 0x80 = 8.0 (800% padding - 9x traffic)
# 0xFF = 15.9375 (1593.75% padding)
```
**Négociation de la fenêtre de tags:**

```python
# SOTW: Sender's recommendation for receiver's inbound window
# RITW: Sender's declaration of own inbound window

# Receiver calculates actual inbound window:
inbound_window = calculate_window(
    sender_suggestion=SOTW,
    own_constraints=MAX_INBOUND_TAGS,
    own_resources=available_memory()
)

# Sender uses:
# - RITW to know how far ahead receiver will accept
# - Own SOTW to hint optimal window size
```
**Valeurs par défaut (lorsque les options ne sont pas négociées):**

```python
DEFAULT_OPTIONS = {
    'version': 0,
    'session_tag_length': 8,
    'session_timeout': 600,  # 10 minutes
    'sender_outbound_tag_window': 160,
    'receiver_inbound_tag_window': 160,
    'tmin': 0x00,  # No minimum padding
    'tmax': 0x10,  # Up to 100% padding
    'rmin': 0x00,  # No minimum requested
    'rmax': 0x10,  # Up to 100% requested
    'tdmy': 0,     # No dummy traffic
    'rdmy': 0,     # No dummy traffic requested
    'tdelay': 0,   # No delay
    'rdelay': 0    # No delay requested
}
```
### MessageNumbers Block (bloc des numéros de message) (Type 6)

**Statut**: NON IMPLÉMENTÉ

**Objectif**: Indiquer le dernier message envoyé dans le jeu de balises précédent (permet la détection des écarts)

**Format :**

```
+----+----+----+----+----+
| 6  |    2    |  PN    |
+----+----+----+----+----+
```
**Champs :**

- `blk`: 6
- `size`: 2
- `PN`: 2 octets - Numéro du dernier message de l'ensemble d'étiquettes précédent (big-endian, 0-65535)

**Définition de PN (numéro précédent):**

PN est l’indice du dernier tag (étiquette) envoyé dans l’ensemble de tags précédent.

**Utilisation (lorsque ce sera mis en œuvre):**

```python
# After ratcheting to new tag set
# Old tag set: sent messages 0-4095
# New tag set: sending first message

payload = [
    MessageNumbersBlock(PN=4095),
    build_garlic_clove(data)
]
```
**Avantages pour le récepteur:**

```python
def process_message_numbers(pn_value):
    # Receiver can now:
    
    # 1. Determine if any messages were skipped
    highest_received_in_old_tagset = 4090
    if pn_value > highest_received_in_old_tagset:
        missing_count = pn_value - highest_received_in_old_tagset
        # 5 messages were never received
    
    # 2. Delete tags higher than PN from old tagset
    for tag_index in range(pn_value + 1, MAX_TAG_INDEX):
        delete_tag(old_tagset, tag_index)
    
    # 3. Expire tags ≤ PN after grace period (e.g., 2 minutes)
    schedule_deletion(old_tagset, delay=120)
```
**Règles :**

- NE DOIT PAS être envoyé dans l’ensemble de tags 0 (aucun ensemble de tags précédent)
- Envoyé uniquement dans les messages ES
- Envoyé uniquement dans le(s) premier(s) message(s) d’un nouvel ensemble de tags
- La valeur PN est du point de vue de l’expéditeur (dernier tag envoyé par l’expéditeur)

**Relation avec Signal :**

Dans Signal Double Ratchet, PN se trouve dans l’en-tête du message. Dans ECIES, il est dans la charge utile chiffrée et est facultatif.

### Bloc de bourrage (Type 254)

**Objectif**: Résistance à l'analyse de trafic et obfuscation de la taille des messages

**Format :**

```
+----+----+----+----+----+----+----+----+
|254 |  size   |      padding           |
+----+----+----+                        +
|                                       |
~               ...                     ~
|                                       |
+----+----+----+----+----+----+----+----+
```
**Champs :**

- `blk`: 254
- `size`: 0-65516 octets (big-endian)
- `padding`: Données aléatoires ou nulles

**Règles :**

- DOIT être le dernier bloc du message
- Plusieurs blocs de bourrage NON autorisés
- Peut être de longueur nulle (en-tête de 3 octets uniquement)
- Les données de bourrage peuvent être des zéros ou des octets aléatoires

**Bourrage par défaut :**

```python
DEFAULT_PADDING_MIN = 0
DEFAULT_PADDING_MAX = 15

def generate_default_padding():
    size = random.randint(DEFAULT_PADDING_MIN, DEFAULT_PADDING_MAX)
    data = random.bytes(size)  # or zeros
    return PaddingBlock(size, data)
```
**Stratégies de résistance à l'analyse de trafic:**

**Stratégie 1: Taille aléatoire (par défaut)**

```python
# Add 0-15 bytes random padding to each message
padding_size = random.randint(0, 15)
padding_block = PaddingBlock(padding_size, random.bytes(padding_size))
```
**Stratégie 2 : Arrondir à un multiple**

```python
# Round total message size to next multiple of 64
target_size = ((message_size + 63) // 64) * 64
padding_size = target_size - message_size - 3  # -3 for block header
padding_block = PaddingBlock(padding_size, random.bytes(padding_size))
```
**Stratégie 3 : taille fixe des messages**

```python
# Always send 1KB messages
TARGET_MESSAGE_SIZE = 1024
padding_size = TARGET_MESSAGE_SIZE - message_size - 3
padding_block = PaddingBlock(padding_size, random.bytes(padding_size))
```
**Stratégie 4: Bourrage négocié (bloc d’options)**

```python
# Calculate padding based on negotiated parameters
# tmin, tmax from Options block
min_padding = int(payload_size * tmin_ratio)
max_padding = int(payload_size * tmax_ratio)
padding_size = random.randint(min_padding, max_padding)
padding_block = PaddingBlock(padding_size, random.bytes(padding_size))
```
**Messages uniquement de bourrage:**

Des messages peuvent ne contenir que du bourrage (aucune donnée applicative):

```python
# Dummy traffic message
payload = [
    PaddingBlock(random.randint(100, 500), random.bytes(...))
]
```
**Notes d'implémentation:**

1. **Bourrage de zéros**: Acceptable (sera chiffré par ChaCha20)
2. **Bourrage aléatoire**: N'apporte aucune sécurité supplémentaire après chiffrement mais consomme davantage d'entropie
3. **Performances**: La génération de bourrage aléatoire peut être coûteuse ; envisagez d'utiliser des zéros
4. **Mémoire**: Les blocs de bourrage volumineux consomment de la bande passante ; soyez prudent avec la taille maximale

---

## Guide d'implémentation

### Prérequis

**Bibliothèques cryptographiques :**

- **X25519**: libsodium, NaCl, ou Bouncy Castle
- **ChaCha20-Poly1305**: libsodium, OpenSSL 1.1.0+, ou Bouncy Castle
- **SHA-256**: OpenSSL, Bouncy Castle, ou prise en charge native du langage
- **Elligator2**: Prise en charge limitée au niveau des bibliothèques ; peut nécessiter une implémentation personnalisée

**Implémentation d’Elligator2 (technique de masquage pour courbes elliptiques):**

Elligator2 (méthode permettant de représenter des points de courbe elliptique comme des données indiscernables d'un flux aléatoire) n'est pas largement implémenté. Options:

1. **OBFS4** : Le transport enfichable obfs4 de Tor inclut une implémentation d’Elligator2 (technique cryptographique de dissimulation sur courbe elliptique)
2. **Implémentation personnalisée** : Basée sur l’[article Elligator2](https://elligator.cr.yp.to/elligator-20130828.pdf)
3. **kleshni/Elligator** : Implémentation de référence sur GitHub

**Remarque Java I2P :** Java I2P utilise la bibliothèque net.i2p.crypto.eddsa avec des ajouts personnalisés pour Elligator2 (technique de mappage elliptique permettant de rendre les clés publiques indiscernables de données aléatoires).

### Ordre d'implémentation recommandé

**Phase 1: Cryptographie de base** 1. Génération et échange de clés DH X25519 2. Chiffrement/déchiffrement AEAD ChaCha20-Poly1305 3. Hachage SHA-256 et MixHash 4. Dérivation de clés HKDF 5. Encodage/décodage Elligator2 (peut utiliser des vecteurs de test au départ)

**Phase 2: Formats de messages** 1. message NS (non lié) - format le plus simple 2. message NS (lié) - ajoute une clé statique 3. message NSR 4. message ES 5. Analyse et génération de blocs

**Phase 3 : Gestion des sessions** 1. Création et stockage des sessions 2. Gestion de l'ensemble des tags (émetteur et récepteur) 3. Ratchet (mécanisme de cliquet cryptographique) des tags de session 4. Ratchet des clés symétriques 5. Recherche des tags et gestion de la fenêtre

**Phase 4 : DH Ratcheting (mécanisme à cliquet Diffie-Hellman)** 1. Gestion du bloc NextKey 2. Fonction de dérivation de clé du DH ratchet 3. Création d'un ensemble de tags après le ratchet 4. Gestion de plusieurs ensembles de tags

**Phase 5: Logique du protocole** 1. Machine à états NS/NSR/ES 2. Prévention du rejeu (DateTime, filtre de Bloom) 3. Logique de retransmission (NS/NSR multiples) 4. Gestion des ACK (acquittements)

**Phase 6: Intégration** 1. Traitement des Garlic Clove d’I2NP (élément d’un message garlic) 2. Regroupement de LeaseSet 3. Intégration du protocole de streaming 4. Intégration du protocole de datagrammes

### Implémentation de l'émetteur

**Cycle de vie de la session sortante:**

```python
class OutboundSession:
    def __init__(self, destination, bound=True):
        self.destination = destination
        self.bound = bound
        self.state = SessionState.NEW
        
        # Keys for NS message
        self.ephemeral_keypair = generate_elg2_keypair()
        if bound:
            self.static_key = context.static_keypair
        
        # Will be populated after NSR
        self.outbound_tagset = None
        self.outbound_keyratchet = None
        self.inbound_tagset = None
        self.inbound_keyratchet = None
        
        # Timing
        self.created_time = now()
        self.last_activity = now()
        
        # Retransmission
        self.ns_attempts = []
        self.ns_timer = None
    
    def send_initial_message(self, payload):
        """Send NS message"""
        # Build NS message
        ns_message = self.build_ns_message(payload)
        
        # Send
        send_to_network(self.destination, ns_message)
        
        # Track for retransmission
        self.ns_attempts.append({
            'message': ns_message,
            'time': now(),
            'ephemeral_key': self.ephemeral_keypair,
            'kdf_state': self.save_kdf_state()
        })
        
        # Start timer
        self.ns_timer = set_timer(1.0, self.on_ns_timeout)
        self.state = SessionState.PENDING_REPLY
    
    def build_ns_message(self, payload):
        """Construct NS message"""
        # KDF initialization
        chainKey, h = self.initialize_kdf()
        
        # Ephemeral key section
        elg2_ephemeral = ENCODE_ELG2(self.ephemeral_keypair.public_key)
        h = SHA256(h || self.destination.static_key)
        h = SHA256(h || self.ephemeral_keypair.public_key)
        
        # es DH
        es_shared = DH(self.ephemeral_keypair.private_key, 
                       self.destination.static_key)
        keydata = HKDF(chainKey, es_shared, "", 64)
        chainKey = keydata[0:31]
        k_static = keydata[32:63]
        
        # Encrypt static key section
        if self.bound:
            static_section = self.static_key.public_key
        else:
            static_section = bytes(32)
        
        static_ciphertext = ENCRYPT(k_static, 0, static_section, h)
        h = SHA256(h || static_ciphertext)
        
        # ss DH (if bound)
        if self.bound:
            ss_shared = DH(self.static_key.private_key, 
                          self.destination.static_key)
            keydata = HKDF(chainKey, ss_shared, "", 64)
            chainKey = keydata[0:31]
            k_payload = keydata[32:63]
            nonce = 0
        else:
            k_payload = k_static
            nonce = 1
        
        # Build payload blocks
        payload_data = self.build_ns_payload(payload)
        
        # Encrypt payload
        payload_ciphertext = ENCRYPT(k_payload, nonce, payload_data, h)
        h = SHA256(h || payload_ciphertext)
        
        # Save KDF state for NSR processing
        self.ns_chainkey = chainKey
        self.ns_hash = h
        
        # Assemble message
        return elg2_ephemeral + static_ciphertext + payload_ciphertext
    
    def build_ns_payload(self, application_data):
        """Build NS payload blocks"""
        blocks = []
        
        # DateTime block (required, first)
        blocks.append(build_datetime_block())
        
        # Garlic Clove(s) with application data
        blocks.append(build_garlic_clove(application_data))
        
        # Optionally bundle LeaseSet
        if should_send_leaseset():
            blocks.append(build_garlic_clove(build_leaseset_store()))
        
        # Padding
        blocks.append(build_padding_block(random.randint(0, 15)))
        
        return encode_blocks(blocks)
    
    def on_nsr_received(self, nsr_message):
        """Process NSR and establish ES session"""
        # Cancel retransmission timer
        cancel_timer(self.ns_timer)
        
        # Parse NSR
        tag = nsr_message[0:8]
        elg2_bob_ephemeral = nsr_message[8:40]
        key_section_mac = nsr_message[40:56]
        payload_ciphertext = nsr_message[56:]
        
        # Find corresponding NS attempt
        ns_state = self.find_ns_by_tag(tag)
        if not ns_state:
            raise ValueError("NSR tag doesn't match any NS")
        
        # Restore KDF state
        chainKey = ns_state['chainkey']
        h = ns_state['hash']
        
        # Decode Bob's ephemeral key
        bob_ephemeral = DECODE_ELG2(elg2_bob_ephemeral)
        
        # Mix tag and Bob's ephemeral into hash
        h = SHA256(h || tag)
        h = SHA256(h || bob_ephemeral)
        
        # ee DH
        ee_shared = DH(self.ephemeral_keypair.private_key, bob_ephemeral)
        keydata = HKDF(chainKey, ee_shared, "", 32)
        chainKey = keydata[0:31]
        
        # se DH
        se_shared = DH(self.static_key.private_key, bob_ephemeral)
        keydata = HKDF(chainKey, se_shared, "", 64)
        chainKey = keydata[0:31]
        k_key_section = keydata[32:63]
        
        # Verify key section MAC
        try:
            DECRYPT(k_key_section, 0, key_section_mac, h)
        except AuthenticationError:
            raise ValueError("NSR key section MAC verification failed")
        
        h = SHA256(h || key_section_mac)
        
        # Split for bidirectional ES
        keydata = HKDF(chainKey, ZEROLEN, "", 64)
        k_ab = keydata[0:31]  # Alice → Bob
        k_ba = keydata[32:63]  # Bob → Alice
        
        # Initialize ES tagsets
        self.outbound_tagset = DH_INITIALIZE(chainKey, k_ab)
        self.inbound_tagset = DH_INITIALIZE(chainKey, k_ba)
        
        # Decrypt NSR payload
        k_nsr = HKDF(k_ba, ZEROLEN, "AttachPayloadKDF", 32)
        try:
            payload = DECRYPT(k_nsr, 0, payload_ciphertext, h)
        except AuthenticationError:
            raise ValueError("NSR payload MAC verification failed")
        
        # Process NSR payload blocks
        self.process_payload_blocks(payload)
        
        # Session established
        self.state = SessionState.ESTABLISHED
        self.last_activity = now()
        
        # Send ES message (implicit ACK)
        self.send_es_ack()
    
    def send_es_message(self, payload):
        """Send ES message"""
        if self.state != SessionState.ESTABLISHED:
            raise ValueError("Session not established")
        
        # Get next tag and key
        tag, index = self.outbound_tagset.get_next_tag()
        key = self.outbound_keyratchet.get_key(index)
        
        # Construct nonce
        nonce = construct_nonce(index)
        
        # Build payload blocks
        payload_data = self.build_es_payload(payload)
        
        # AEAD encryption
        ciphertext = ENCRYPT(key, nonce, payload_data, tag)
        
        # Assemble message
        es_message = tag + ciphertext
        
        # Send
        send_to_network(self.destination, es_message)
        
        # Update activity
        self.last_activity = now()
        
        # Check if ratchet needed
        if self.outbound_tagset.should_ratchet():
            self.initiate_ratchet()
```
### Implémentation du récepteur

**Cycle de vie d'une session entrante:**

```python
class InboundSession:
    def __init__(self):
        self.state = None
        self.bound = False
        self.destination = None
        
        # Keys
        self.remote_ephemeral_key = None
        self.remote_static_key = None
        self.ephemeral_keypair = None
        
        # Tagsets
        self.inbound_tagset = None
        self.outbound_tagset = None
        
        # Timing
        self.created_time = None
        self.last_activity = None
        
        # Paired session
        self.paired_outbound = None
    
    @staticmethod
    def try_decrypt_ns(message):
        """Attempt to decrypt as NS message"""
        # Parse NS structure
        elg2_ephemeral = message[0:32]
        static_ciphertext = message[32:80]  # 32 + 16
        payload_ciphertext = message[80:]
        
        # Decode ephemeral key
        try:
            alice_ephemeral = DECODE_ELG2(elg2_ephemeral)
        except:
            return None  # Not a valid Elligator2 encoding
        
        # Check replay
        if is_replay(alice_ephemeral):
            return None
        
        # KDF initialization
        chainKey, h = initialize_kdf()
        
        # Mix keys
        h = SHA256(h || context.static_keypair.public_key)
        h = SHA256(h || alice_ephemeral)
        
        # es DH
        es_shared = DH(context.static_keypair.private_key, alice_ephemeral)
        keydata = HKDF(chainKey, es_shared, "", 64)
        chainKey = keydata[0:31]
        k_static = keydata[32:63]
        
        # Decrypt static key section
        try:
            static_data = DECRYPT(k_static, 0, static_ciphertext, h)
        except AuthenticationError:
            return None  # Not a valid NS message
        
        h = SHA256(h || static_ciphertext)
        
        # Check if bound or unbound
        if static_data == bytes(32):
            # Unbound
            alice_static_key = None
            k_payload = k_static
            nonce = 1
        else:
            # Bound - perform ss DH
            alice_static_key = static_data
            ss_shared = DH(context.static_keypair.private_key, alice_static_key)
            keydata = HKDF(chainKey, ss_shared, "", 64)
            chainKey = keydata[0:31]
            k_payload = keydata[32:63]
            nonce = 0
        
        # Decrypt payload
        try:
            payload = DECRYPT(k_payload, nonce, payload_ciphertext, h)
        except AuthenticationError:
            return None
        
        h = SHA256(h || payload_ciphertext)
        
        # Create session
        session = InboundSession()
        session.state = SessionState.ESTABLISHED
        session.created_time = now()
        session.last_activity = now()
        session.remote_ephemeral_key = alice_ephemeral
        session.remote_static_key = alice_static_key
        session.bound = (alice_static_key is not None)
        session.ns_chainkey = chainKey
        session.ns_hash = h
        
        # Extract destination if bound
        if session.bound:
            session.destination = extract_destination_from_payload(payload)
        
        # Process payload
        session.process_payload_blocks(payload)
        
        return session
    
    def send_nsr_reply(self, reply_payload):
        """Send NSR message"""
        # Generate NSR tagset
        tagsetKey = HKDF(self.ns_chainkey, ZEROLEN, "SessionReplyTags", 32)
        nsr_tagset = DH_INITIALIZE(self.ns_chainkey, tagsetKey)
        
        # Get tag
        tag, _ = nsr_tagset.get_next_tag()
        
        # Mix tag into hash
        h = SHA256(self.ns_hash || tag)
        
        # Generate ephemeral key
        self.ephemeral_keypair = generate_elg2_keypair()
        bob_ephemeral = self.ephemeral_keypair.public_key
        elg2_bob_ephemeral = ENCODE_ELG2(bob_ephemeral)
        
        # Mix ephemeral key
        h = SHA256(h || bob_ephemeral)
        
        chainKey = self.ns_chainkey
        
        # ee DH
        ee_shared = DH(self.ephemeral_keypair.private_key, 
                      self.remote_ephemeral_key)
        keydata = HKDF(chainKey, ee_shared, "", 32)
        chainKey = keydata[0:31]
        
        # se DH
        se_shared = DH(context.static_keypair.private_key, 
                      self.remote_ephemeral_key)
        keydata = HKDF(chainKey, se_shared, "", 64)
        chainKey = keydata[0:31]
        k_key_section = keydata[32:63]
        
        # Encrypt key section (empty)
        key_section_ciphertext = ENCRYPT(k_key_section, 0, ZEROLEN, h)
        h = SHA256(h || key_section_ciphertext)
        
        # Split for bidirectional ES
        keydata = HKDF(chainKey, ZEROLEN, "", 64)
        k_ab = keydata[0:31]  # Alice → Bob
        k_ba = keydata[32:63]  # Bob → Alice
        
        # Initialize ES tagsets
        self.inbound_tagset = DH_INITIALIZE(chainKey, k_ab)
        self.outbound_tagset = DH_INITIALIZE(chainKey, k_ba)
        
        # Build reply payload
        payload_data = build_payload_blocks(reply_payload)
        
        # Encrypt payload
        k_nsr = HKDF(k_ba, ZEROLEN, "AttachPayloadKDF", 32)
        payload_ciphertext = ENCRYPT(k_nsr, 0, payload_data, h)
        
        # Assemble NSR
        nsr_message = tag + elg2_bob_ephemeral + key_section_ciphertext + payload_ciphertext
        
        # Send
        send_to_network(self.destination, nsr_message)
        
        # Wait for ES
        self.state = SessionState.AWAITING_ES
        self.last_activity = now()
    
    def on_es_received(self, es_message):
        """Process first ES message"""
        if self.state == SessionState.AWAITING_ES:
            # First ES received, confirms session
            self.state = SessionState.ESTABLISHED
        
        # Process ES message
        self.process_es_message(es_message)
    
    def process_es_message(self, es_message):
        """Decrypt and process ES message"""
        # Extract tag
        tag = es_message[0:8]
        ciphertext = es_message[8:]
        
        # Look up tag
        index = self.inbound_tagset.lookup_tag(tag)
        if index is None:
            raise ValueError("Tag not found")
        
        # Get key
        key = self.inbound_keyratchet.get_key(index)
        
        # Construct nonce
        nonce = construct_nonce(index)
        
        # Decrypt
        try:
            payload = DECRYPT(key, nonce, ciphertext, tag)
        except AuthenticationError:
            raise ValueError("ES MAC verification failed")
        
        # Process blocks
        self.process_payload_blocks(payload)
        
        # Update activity
        self.last_activity = now()
```
### Classification des messages

**Distinction des types de messages:**

```python
def classify_message(message):
    """Determine message type"""
    
    # Minimum lengths
    if len(message) < 24:
        return None  # Too short
    
    # Check for session tag (8 bytes)
    tag = message[0:8]
    
    # Try ES decryption first (most common)
    session = lookup_session_by_tag(tag)
    if session:
        return ('ES', session)
    
    # Try NSR decryption (tag + Elligator2 key)
    if len(message) >= 72:
        # Check if bytes 8-40 are valid Elligator2
        try:
            nsr_ephemeral = DECODE_ELG2(message[8:40])
            nsr_session = find_pending_nsr_by_tag(tag)
            if nsr_session:
                return ('NSR', nsr_session)
        except:
            pass
    
    # Try NS decryption (starts with Elligator2 key)
    if len(message) >= 96:
        try:
            ns_ephemeral = DECODE_ELG2(message[0:32])
            ns_session = InboundSession.try_decrypt_ns(message)
            if ns_session:
                return ('NS', ns_session)
        except:
            pass
    
    # Check ElGamal/AES (for dual-key compatibility)
    if len(message) >= 514:
        if (len(message) - 2) % 16 == 0:
            # Might be ElGamal NS
            return ('ELGAMAL_NS', None)
        elif len(message) % 16 == 0:
            # Might be ElGamal ES
            return ('ELGAMAL_ES', None)
    
    return None  # Unknown message type
```
### Meilleures pratiques de gestion des sessions

**Stockage de session :**

```python
class SessionKeyManager:
    def __init__(self):
        # Outbound sessions (one per destination)
        self.outbound_sessions = {}  # destination -> OutboundSession
        
        # Inbound sessions (multiple per destination during transition)
        self.inbound_sessions = []  # [InboundSession]
        
        # Session tag lookup (fast path for ES messages)
        self.tag_to_session = {}  # tag -> InboundSession
        
        # Limits
        self.max_inbound_sessions = 1000
        self.max_tags_per_session = 160
    
    def get_outbound_session(self, destination):
        """Get or create outbound session"""
        if destination not in self.outbound_sessions:
            session = OutboundSession(destination)
            self.outbound_sessions[destination] = session
        return self.outbound_sessions[destination]
    
    def add_inbound_session(self, session):
        """Add new inbound session"""
        # Check limits
        if len(self.inbound_sessions) >= self.max_inbound_sessions:
            self.expire_oldest_session()
        
        self.inbound_sessions.append(session)
        
        # Add tags to lookup table
        self.register_session_tags(session)
    
    def register_session_tags(self, session):
        """Register session's tags in lookup table"""
        for tag in session.inbound_tagset.get_all_tags():
            self.tag_to_session[tag] = session
    
    def lookup_tag(self, tag):
        """Fast tag lookup"""
        return self.tag_to_session.get(tag)
    
    def expire_sessions(self):
        """Periodic session expiration"""
        now_time = now()
        
        # Expire outbound sessions
        for dest, session in list(self.outbound_sessions.items()):
            if session.idle_time(now_time) > 8 * 60:
                del self.outbound_sessions[dest]
        
        # Expire inbound sessions
        expired = []
        for session in self.inbound_sessions:
            if session.idle_time(now_time) > 10 * 60:
                expired.append(session)
        
        for session in expired:
            self.remove_inbound_session(session)
    
    def remove_inbound_session(self, session):
        """Remove inbound session and clean up tags"""
        self.inbound_sessions.remove(session)
        
        # Remove tags from lookup
        for tag in session.inbound_tagset.get_all_tags():
            if tag in self.tag_to_session:
                del self.tag_to_session[tag]
```
**Gestion de la mémoire:**

```python
class TagMemoryManager:
    def __init__(self, max_memory_kb=10240):  # 10 MB default
        self.max_memory = max_memory_kb * 1024
        self.current_memory = 0
        self.max_tags_per_session = 160
        self.min_tags_per_session = 32
    
    def calculate_tag_memory(self, session):
        """Calculate memory used by session tags"""
        tag_count = len(session.inbound_tagset.tags)
        # Each tag: 8 bytes (tag) + 2 bytes (index) + 32 bytes (key, optional)
        # + overhead
        bytes_per_tag = 16 if session.defer_keys else 48
        return tag_count * bytes_per_tag
    
    def check_pressure(self):
        """Check if under memory pressure"""
        return self.current_memory > (self.max_memory * 0.9)
    
    def handle_pressure(self):
        """Reduce memory usage when under pressure"""
        if not self.check_pressure():
            return
        
        # Strategy 1: Reduce look-ahead windows
        for session in all_sessions:
            if session.look_ahead > self.min_tags_per_session:
                session.reduce_look_ahead(self.min_tags_per_session)
        
        # Strategy 2: Trim old tags aggressively
        for session in all_sessions:
            session.inbound_tagset.trim_behind(aggressive=True)
        
        # Strategy 3: Refuse new ratchets
        for session in all_sessions:
            if session.outbound_tagset.should_ratchet():
                session.defer_ratchet = True
        
        # Strategy 4: Expire idle sessions early
        expire_idle_sessions(threshold=5*60)  # 5 min instead of 10
```
### Stratégies de test

**Tests unitaires:**

```python
def test_x25519_dh():
    """Test X25519 key exchange"""
    alice_sk = GENERATE_PRIVATE()
    alice_pk = DERIVE_PUBLIC(alice_sk)
    
    bob_sk = GENERATE_PRIVATE()
    bob_pk = DERIVE_PUBLIC(bob_sk)
    
    # Both sides compute same shared secret
    alice_shared = DH(alice_sk, bob_pk)
    bob_shared = DH(bob_sk, alice_pk)
    
    assert alice_shared == bob_shared

def test_elligator2_encode_decode():
    """Test Elligator2 roundtrip"""
    sk = GENERATE_PRIVATE_ELG2()
    pk = DERIVE_PUBLIC(sk)
    
    encoded = ENCODE_ELG2(pk)
    decoded = DECODE_ELG2(encoded)
    
    assert decoded == pk

def test_chacha_poly_encrypt_decrypt():
    """Test ChaCha20-Poly1305 AEAD"""
    key = CSRNG(32)
    nonce = construct_nonce(42)
    plaintext = b"Hello, I2P!"
    ad = b"associated_data"
    
    ciphertext = ENCRYPT(key, nonce, plaintext, ad)
    decrypted = DECRYPT(key, nonce, ciphertext, ad)
    
    assert decrypted == plaintext

def test_session_tag_ratchet():
    """Test session tag generation"""
    sessTag_ck = CSRNG(32)
    tagset = SessionTagRatchet(sessTag_ck)
    
    # Generate 100 tags
    tags = [tagset.get_next_tag() for _ in range(100)]
    
    # All tags should be unique
    assert len(set(tags)) == 100
    
    # Each tag should be 8 bytes
    for tag in tags:
        assert len(tag) == 8
```
**Tests d'intégration:**

```python
def test_ns_nsr_handshake():
    """Test NS/NSR handshake"""
    # Alice creates outbound session
    alice_session = OutboundSession(bob_destination, bound=True)
    
    # Alice sends NS
    ns_message = alice_session.build_ns_message(b"Hello Bob")
    
    # Bob receives NS
    bob_session = InboundSession.try_decrypt_ns(ns_message)
    assert bob_session is not None
    assert bob_session.bound == True
    
    # Bob sends NSR
    nsr_message = bob_session.build_nsr_message(b"Hello Alice")
    
    # Alice receives NSR
    alice_session.on_nsr_received(nsr_message)
    assert alice_session.state == SessionState.ESTABLISHED
    
    # Both should have matching ES tagsets
    # (Cannot directly compare, but can test by sending ES messages)

def test_es_bidirectional():
    """Test ES messages in both directions"""
    # (After NS/NSR handshake)
    
    # Alice sends ES to Bob
    es_alice_to_bob = alice_session.send_es_message(b"Data from Alice")
    
    # Bob receives ES
    bob_session.process_es_message(es_alice_to_bob)
    
    # Bob sends ES to Alice
    es_bob_to_alice = bob_session.send_es_message(b"Data from Bob")
    
    # Alice receives ES
    alice_session.process_es_message(es_bob_to_alice)

def test_dh_ratchet():
    """Test DH ratchet"""
    # (After established session)
    
    # Alice initiates ratchet
    alice_session.initiate_ratchet()
    nextkey_alice = build_nextkey_block(
        flags=0x01,
        key_id=0,
        public_key=alice_new_key
    )
    
    # Send to Bob
    bob_session.process_nextkey_block(nextkey_alice)
    
    # Bob replies
    nextkey_bob = build_nextkey_block(
        flags=0x03,
        key_id=0,
        public_key=bob_new_key
    )
    
    # Send to Alice
    alice_session.process_nextkey_block(nextkey_bob)
    
    # Both should now be using new tagsets
    assert alice_session.outbound_tagset.id == 1
    assert bob_session.inbound_tagset.id == 1
```
**Vecteurs de test :**

Implémenter les vecteurs de test issus de la spécification :

1. **Noise IK Handshake**: Utiliser des vecteurs de test Noise standard
2. **HKDF**: Utiliser les vecteurs de test de la RFC 5869
3. **ChaCha20-Poly1305**: Utiliser les vecteurs de test de la RFC 7539
4. **Elligator2**: Utiliser les vecteurs de test de l'article Elligator2 ou d'OBFS4

**Tests d'interopérabilité:**

1. **Java I2P**: Tester par rapport à l'implémentation de référence Java I2P
2. **i2pd**: Tester par rapport à l'implémentation i2pd en C++
3. **Captures de paquets**: Utiliser le dissecteur Wireshark (s'il est disponible) pour vérifier les formats des messages
4. **Inter-implémentation**: Créer un test harness (infrastructure de test) capable d'envoyer/recevoir entre les implémentations

### Considérations relatives aux performances

**Génération de clés :**

La génération de clés Elligator2 (méthode de représentation uniforme de points de courbe elliptique) est coûteuse (taux de rejet de 50 %) :

```python
class KeyPool:
    """Pre-generate keys in background thread"""
    def __init__(self, pool_size=10):
        self.pool = Queue(maxsize=pool_size)
        self.generator_thread = Thread(target=self.generate_keys, daemon=True)
        self.generator_thread.start()
    
    def generate_keys(self):
        while True:
            if not self.pool.full():
                keypair = generate_elg2_keypair()
                # Also compute encoded form
                encoded = ENCODE_ELG2(keypair.public_key)
                self.pool.put((keypair, encoded))
            else:
                sleep(0.1)
    
    def get_keypair(self):
        try:
            return self.pool.get(timeout=1.0)
        except Empty:
            # Pool exhausted, generate inline
            return generate_elg2_keypair()
```
**Recherche de tags:**

Utilisez des tables de hachage pour une recherche d’étiquettes en O(1):

```python
class FastTagLookup:
    def __init__(self):
        self.tag_to_session = {}  # Python dict is hash table
    
    def add_tag(self, tag, session, index):
        # 8-byte tag as bytes is hashable
        self.tag_to_session[tag] = (session, index)
    
    def lookup_tag(self, tag):
        return self.tag_to_session.get(tag)
```
**Optimisation de la mémoire :**

Différer la génération de clés symétriques :

```python
class DeferredKeyRatchet:
    """Only generate keys when needed"""
    def __init__(self, symmKey_ck):
        self.chainKey = symmKey_ck
        self.index = -1
        self.cache = LRUCache(maxsize=32)  # Cache recent keys
    
    def get_key(self, index):
        # Check cache first
        if index in self.cache:
            return self.cache[index]
        
        # Generate keys up to index
        while self.index < index:
            self.index += 1
            keydata = HKDF(self.chainKey, ZEROLEN, "SymmetricRatchet", 64)
            self.chainKey = keydata[0:31]
            
            if self.index == index:
                key = keydata[32:63]
                self.cache[index] = key
                return key
```
**Traitement par lots:**

Traiter plusieurs messages par lot:

```python
def process_message_batch(messages):
    """Process multiple messages efficiently"""
    results = []
    
    # Group by type
    ns_messages = []
    nsr_messages = []
    es_messages = []
    
    for msg in messages:
        msg_type = classify_message(msg)
        if msg_type[0] == 'NS':
            ns_messages.append(msg)
        elif msg_type[0] == 'NSR':
            nsr_messages.append(msg)
        elif msg_type[0] == 'ES':
            es_messages.append(msg)
    
    # Process in batches
    # ES messages are most common, process first
    for msg in es_messages:
        results.append(process_es_message(msg))
    
    for msg in nsr_messages:
        results.append(process_nsr_message(msg))
    
    for msg in ns_messages:
        results.append(process_ns_message(msg))
    
    return results
```
---

## Considérations de sécurité

### Modèle de menaces

**Capacités de l’adversaire:**

1. **Observateur passif**: Peut observer tout le trafic réseau
2. **Attaquant actif**: Peut injecter, modifier, rejeter, rejouer des messages
3. **Nœud compromis**: Peut compromettre un router ou une destination
4. **Analyse du trafic**: Peut effectuer une analyse statistique des schémas de trafic

**Objectifs de sécurité :**

1. **Confidentialité**: Contenu des messages caché aux observateurs
2. **Authentification**: Identité de l'expéditeur vérifiée (pour les sessions liées)
3. **Confidentialité persistante**: Les messages passés restent secrets même si les clés sont compromises
4. **Protection contre la relecture**: Impossible de rejouer d'anciens messages
5. **Obfuscation du trafic**: Les handshakes (échanges initiaux) sont indiscernables de données aléatoires

### Hypothèses cryptographiques

**Hypothèses de difficulté :**

1. **X25519 CDH**: Le problème Diffie-Hellman computationnel est difficile sur Curve25519
2. **ChaCha20 PRF**: ChaCha20 est une fonction pseudo-aléatoire
3. **Poly1305 MAC**: Poly1305 est inforgeable sous attaque par message choisi
4. **SHA-256 CR**: SHA-256 est résistant aux collisions
5. **HKDF Security**: HKDF extrait et étend des clés uniformément distribuées

**Niveaux de sécurité:**

- **X25519**: sécurité de ~128 bits (ordre de la courbe 2^252)
- **ChaCha20**: clés de 256 bits, sécurité de 256 bits
- **Poly1305**: sécurité de 128 bits (probabilité de collision)
- **SHA-256**: résistance aux collisions de 128 bits, résistance aux préimages de 256 bits

### Gestion des clés

**Génération de clés:**

```python
# CRITICAL: Use cryptographically secure RNG
def CSRNG(length):
    # GOOD: os.urandom, secrets.token_bytes (Python)
    # GOOD: /dev/urandom (Linux)
    # GOOD: BCryptGenRandom (Windows)
    # BAD: random.random(), Math.random() (NOT cryptographically secure)
    return os.urandom(length)

# CRITICAL: Validate keys
def validate_x25519_key(pubkey):
    # Check for weak keys (all zeros, small order points)
    if pubkey == bytes(32):
        raise WeakKeyError("All-zero public key")
    
    # Perform DH to check for weak shared secrets
    test_shared = DH(test_private_key, pubkey)
    if test_shared == bytes(32):
        raise WeakKeyError("Results in zero shared secret")
```
**Stockage des clés :**

```python
# CRITICAL: Protect private keys
class SecureKeyStorage:
    def __init__(self):
        # Store in memory with protection
        self.keys = {}
        
        # Option 1: Memory locking (prevent swapping to disk)
        # mlock(self.keys)
        
        # Option 2: Encrypted storage
        # self.encryption_key = derive_from_password()
    
    def store_key(self, key_id, private_key):
        # Option: Encrypt before storage
        # encrypted = encrypt(private_key, self.encryption_key)
        # self.keys[key_id] = encrypted
        self.keys[key_id] = private_key
    
    def delete_key(self, key_id):
        # Securely wipe memory
        if key_id in self.keys:
            key = self.keys[key_id]
            # Overwrite with zeros before deletion
            for i in range(len(key)):
                key[i] = 0
            del self.keys[key_id]
```
**Rotation des clés:**

```python
# CRITICAL: Rotate keys regularly
class KeyRotationPolicy:
    def __init__(self):
        self.max_messages_per_tagset = 4096  # Ratchet before 65535
        self.max_tagset_age = 10 * 60       # 10 minutes
        self.max_session_age = 60 * 60      # 1 hour
    
    def should_ratchet(self, tagset):
        return (tagset.messages_sent >= self.max_messages_per_tagset or
                tagset.age() >= self.max_tagset_age)
    
    def should_replace_session(self, session):
        return session.age() >= self.max_session_age
```
### Mesures d'atténuation des attaques

### Mesures d’atténuation des attaques par rejeu

**Validation de la date et de l'heure:**

```python
MAX_CLOCK_SKEW_PAST = 5 * 60
MAX_CLOCK_SKEW_FUTURE = 2 * 60

def validate_datetime(timestamp):
    now = int(time.time())
    age = now - timestamp
    
    if age < -MAX_CLOCK_SKEW_FUTURE:
        raise ReplayError("Timestamp too far in future")
    
    if age > MAX_CLOCK_SKEW_PAST:
        raise ReplayError("Timestamp too old")
    
    return True
```
**Filtre de Bloom pour les messages NS:**

```python
class ReplayFilter:
    def __init__(self, capacity=100000, error_rate=0.001, duration=5*60):
        self.bloom = BloomFilter(capacity=capacity, error_rate=error_rate)
        self.duration = duration
        self.entries = []  # (timestamp, ephemeral_key)
    
    def check_replay(self, ephemeral_key, timestamp):
        # Validate timestamp
        if not validate_datetime(timestamp):
            return False
        
        # Check Bloom filter
        if ephemeral_key in self.bloom:
            # Potential replay (or false positive)
            # Check exact match in entries
            for ts, key in self.entries:
                if key == ephemeral_key:
                    return False  # Definite replay
        
        # Add to filter
        self.bloom.add(ephemeral_key)
        self.entries.append((timestamp, ephemeral_key))
        
        # Expire old entries
        self.expire_old_entries()
        
        return True
    
    def expire_old_entries(self):
        now = int(time.time())
        self.entries = [(ts, key) for ts, key in self.entries
                       if now - ts < self.duration]
```
**Session Tag (étiquette de session) à usage unique:**

```python
def process_session_tag(tag):
    # Look up tag
    entry = tagset.lookup_tag(tag)
    if entry is None:
        raise ValueError("Invalid session tag")
    
    # CRITICAL: Remove tag immediately (one-time use)
    tagset.remove_tag(tag)
    
    # Use associated key
    return entry.key, entry.index
```
### Mesures d'atténuation contre l'usurpation d'identité en cas de compromission de clé (KCI)

**Problème**: l'authentification des messages NS est vulnérable à KCI (Key Compromise Impersonation - usurpation après compromission de clé) (Niveau d'authentification 1)

**Atténuation**:

1. Passez à NSR (niveau d'authentification 2) le plus rapidement possible
2. Ne faites pas confiance à la charge utile NS pour les opérations critiques pour la sécurité
3. Attendez la confirmation NSR avant d'effectuer des actions irréversibles

```python
def process_ns_message(ns_message):
    # NS authenticated at Level 1 (KCI vulnerable)
    # Do NOT perform security-critical operations yet
    
    # Extract sender's static key
    sender_key = ns_message.static_key
    
    # Mark session as pending Level 2 authentication
    session.auth_level = 1
    session.sender_key = sender_key
    
    # Send NSR
    send_nsr_reply(session)

def process_first_es_message(es_message):
    # Now we have Level 2 authentication (KCI resistant)
    session.auth_level = 2
    
    # Safe to perform security-critical operations
    process_security_critical_operation(es_message)
```
### Mesures d'atténuation des attaques par déni de service

**Protection contre les inondations NS:**

```python
class NSFloodProtection:
    def __init__(self):
        self.ns_count = defaultdict(int)  # source -> count
        self.ns_timestamps = defaultdict(list)  # source -> [timestamps]
        
        self.max_ns_per_source = 5
        self.rate_window = 10  # seconds
        self.max_concurrent_ns = 100
    
    def check_ns_allowed(self, source):
        # Global limit
        total_pending = sum(self.ns_count.values())
        if total_pending >= self.max_concurrent_ns:
            return False
        
        # Per-source rate limit
        now = time.time()
        timestamps = self.ns_timestamps[source]
        
        # Remove old timestamps
        timestamps = [ts for ts in timestamps if now - ts < self.rate_window]
        self.ns_timestamps[source] = timestamps
        
        # Check rate
        if len(timestamps) >= self.max_ns_per_source:
            return False
        
        # Allow NS
        timestamps.append(now)
        self.ns_count[source] += 1
        return True
    
    def on_session_established(self, source):
        # Decrease pending count
        if self.ns_count[source] > 0:
            self.ns_count[source] -= 1
```
**Limites de stockage des étiquettes:**

```python
class TagStorageLimit:
    def __init__(self, max_tags=1000000):
        self.max_tags = max_tags
        self.current_tags = 0
    
    def can_create_session(self, look_ahead):
        if self.current_tags + look_ahead > self.max_tags:
            return False
        return True
    
    def add_tags(self, count):
        self.current_tags += count
    
    def remove_tags(self, count):
        self.current_tags -= count
```
**Gestion adaptative des ressources:**

```python
class AdaptiveResourceManager:
    def __init__(self):
        self.load_level = 0  # 0 = low, 1 = medium, 2 = high, 3 = critical
    
    def adjust_parameters(self):
        if self.load_level == 0:
            # Normal operation
            return {
                'max_look_ahead': 160,
                'max_sessions': 1000,
                'session_timeout': 10 * 60
            }
        
        elif self.load_level == 1:
            # Moderate load
            return {
                'max_look_ahead': 80,
                'max_sessions': 800,
                'session_timeout': 8 * 60
            }
        
        elif self.load_level == 2:
            # High load
            return {
                'max_look_ahead': 32,
                'max_sessions': 500,
                'session_timeout': 5 * 60
            }
        
        else:  # load_level == 3
            # Critical load
            return {
                'max_look_ahead': 16,
                'max_sessions': 200,
                'session_timeout': 3 * 60
            }
```
### Résistance à l'analyse de trafic

**Encodage Elligator2:**

Garantit que les messages de poignée de main (handshake) sont indiscernables de données aléatoires :

```python
# NS and NSR start with Elligator2-encoded ephemeral keys
# Observer cannot distinguish from random 32-byte string
```
**Stratégies de remplissage:**

```python
# Resist message size fingerprinting
def add_padding(payload, strategy='random'):
    if strategy == 'random':
        # Random padding 0-15 bytes
        size = random.randint(0, 15)
    
    elif strategy == 'round':
        # Round to next 64-byte boundary
        target = ((len(payload) + 63) // 64) * 64
        size = target - len(payload) - 3  # -3 for block header
    
    elif strategy == 'fixed':
        # Always 1KB messages
        size = 1024 - len(payload) - 3
    
    return build_padding_block(size)
```
**Attaques par temporisation:**

```python
# CRITICAL: Use constant-time operations
def constant_time_compare(a, b):
    """Constant-time byte string comparison"""
    if len(a) != len(b):
        return False
    
    result = 0
    for x, y in zip(a, b):
        result |= x ^ y
    
    return result == 0

# CRITICAL: Constant-time MAC verification
def verify_mac(computed_mac, received_mac):
    if not constant_time_compare(computed_mac, received_mac):
        # Always take same time regardless of where comparison fails
        raise AuthenticationError("MAC verification failed")
```
### Écueils d’implémentation

**Erreurs courantes:**

1. **Réutilisation du nonce (valeur unique)**: NE JAMAIS réutiliser les paires (key, nonce)
   ```python
   # BAD: Reusing nonce with same key
   ciphertext1 = ENCRYPT(key, nonce, plaintext1, ad1)
   ciphertext2 = ENCRYPT(key, nonce, plaintext2, ad2)  # CATASTROPHIC

# BON: nonce (valeur unique non répétée) pour chaque message    ciphertext1 = ENCRYPT(key, nonce1, plaintext1, ad1)    ciphertext2 = ENCRYPT(key, nonce2, plaintext2, ad2)

   ```

2. **Ephemeral Key Reuse**: Generate fresh ephemeral key for each NS/NSR
   ```python
# MAUVAIS : Réutilisation d'une clé éphémère    ephemeral_key = generate_elg2_keypair()    send_ns_message(ephemeral_key)    send_ns_message(ephemeral_key)  # MAUVAIS

# BON : Nouvelle clé pour chaque message    send_ns_message(generate_elg2_keypair())    send_ns_message(generate_elg2_keypair())

   ```

3. **Weak RNG**: Use cryptographically secure random number generator
   ```python
# MAUVAIS : Générateur de nombres aléatoires non cryptographique    import random    key = bytes([random.randint(0, 255) for _ in range(32)])  # NON SÉCURISÉ

# BON : Générateur de nombres aléatoires cryptographiquement sûr    import os    key = os.urandom(32)

   ```

4. **Timing Attacks**: Use constant-time comparisons
   ```python
# MAUVAIS: comparaison avec sortie anticipée    if computed_mac == received_mac:  # Fuite temporelle

       pass
   
# BON: Comparaison en temps constant    if constant_time_compare(computed_mac, received_mac):

       pass
   ```

5. **Incomplete MAC Verification**: Always verify before using data
   ```python
# MAUVAIS: Déchiffrement avant vérification    plaintext = chacha20_decrypt(key, nonce, ciphertext)    mac_ok = verify_mac(mac, plaintext)  # TROP TARD    if not mac_ok:

       return error
   
# BON: AEAD vérifie avant de déchiffrer    try:

       plaintext = DECRYPT(key, nonce, ciphertext, ad)  # Verifies MAC first
except AuthenticationError:

       return error
   ```

6. **Key Deletion**: Securely wipe keys from memory
   ```python
# MAUVAIS: Suppression simple    del private_key  # Toujours en mémoire

# CORRECT: Écraser avant suppression    for i in range(len(private_key)):

       private_key[i] = 0
del private_key

   ```

### Security Audits

**Recommended Audits:**

1. **Cryptographic Review**: Expert review of KDF chains and DH operations
2. **Implementation Audit**: Code review for timing attacks, key management, RNG usage
3. **Protocol Analysis**: Formal verification of handshake security properties
4. **Side-Channel Analysis**: Timing, power, and cache attacks
5. **Fuzzing**: Random input testing for parser robustness

**Test Cases:**

```python
# Cas de test critiques pour la sécurité

def test_nonce_uniqueness():

    """Ensure nonces are never reused"""
    nonces = set()
    for i in range(10000):
        nonce = construct_nonce(i)
        assert nonce not in nonces
        nonces.add(nonce)

def test_key_isolation():

    """Ensure sessions don't share keys"""
    session1 = create_session(destination1)
    session2 = create_session(destination2)
    
    assert session1.key != session2.key

def test_replay_prevention():

    """Ensure replay attacks are detected"""
    ns_message = create_ns_message()
    
    # First delivery succeeds
    assert process_ns_message(ns_message) == True
    
    # Replay fails
    assert process_ns_message(ns_message) == False

def test_mac_verification():

    """Ensure MAC verification is enforced"""
    key = CSRNG(32)
    nonce = construct_nonce(0)
    plaintext = b"test"
    ad = b"test_ad"
    
    ciphertext = ENCRYPT(key, nonce, plaintext, ad)
    
    # Correct MAC verifies
    assert DECRYPT(key, nonce, ciphertext, ad) == plaintext
    
    # Corrupted MAC fails
    corrupted = ciphertext[:-1] + bytes([ciphertext[-1] ^ 0xFF])
    with pytest.raises(AuthenticationError):
        DECRYPT(key, nonce, corrupted, ad)
```

---

## Configuration and Deployment

### I2CP Configuration

**Enable ECIES Encryption:**

```properties
# ECIES (schéma de chiffrement intégré à courbes elliptiques) uniquement (recommandé pour les nouveaux déploiements)

i2cp.leaseSetEncType=4

# À deux clés (ECIES + ElGamal pour la compatibilité)

i2cp.leaseSetEncType=4,0

# ElGamal uniquement (ancien, déconseillé)

i2cp.leaseSetEncType=0

```

**LeaseSet Type:**

```properties
# LS2 standard (leaseSet version 2, le plus courant)

i2cp.leaseSetType=3

# LS2 chiffré (destinations aveuglées)

i2cp.leaseSetType=5

# Méta LS2 (abréviation de leaseSet version 2) (plusieurs destinations)

i2cp.leaseSetType=7

```

**Additional Options:**

```properties
# Clé statique pour ECIES (schéma de chiffrement intégré à courbes elliptiques) (optionnelle, générée automatiquement si elle n'est pas spécifiée)

# Clé publique X25519 de 32 octets, encodée en base64

i2cp.leaseSetPrivateKey=<base64-encoded-key>

# Type de signature (pour LeaseSet)

i2cp.leaseSetSigningPrivateKey=<base64-encoded-key> i2cp.leaseSetSigningType=7  # Ed25519

```

### Java I2P Configuration

**router.config:**

```properties
# ECIES entre routers

i2p.router.useECIES=true

```

**Build Properties:**

```java
// Pour les clients I2CP (Java) Properties props = new Properties(); props.setProperty("i2cp.leaseSetEncType", "4"); props.setProperty("i2cp.leaseSetType", "3");

I2PSession session = i2pClient.createSession(props);

```

### i2pd Configuration

**i2pd.conf:**

```ini
[limites]

# Limite de mémoire des sessions ECIES (schéma de chiffrement intégré sur courbes elliptiques)

ecies.memory = 128M

[ecies]

# Activer ECIES (schéma de chiffrement intégré sur courbes elliptiques)

enabled = true

# ECIES uniquement ou à double clé

compatibility = true  # true = à double clé, false = ECIES uniquement

```

**Tunnels Configuration:**

```ini
[my-service] type = http host = 127.0.0.1 port = 8080 keys = my-service-keys.dat

# ECIES (schéma de chiffrement intégré à courbe elliptique) uniquement

ecies = true

```

### Compatibility Matrix

**Router Version Support:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">ECIES Support</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">LS2 Support</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Dual-Key</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">&lt; 0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">❌ No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">❌ No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">N/A</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy only</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.38-0.9.45</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">❌ No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">N/A</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LS2 only</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.46-0.9.50</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Initial ECIES</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.5.0+</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.0.0+</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">✅ Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
  </tbody>
</table>

**Destination Compatibility:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Destination Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Can Connect To</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-only</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-only, Dual-key</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Requires 0.9.46+ routers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Dual-key</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Maximum compatibility</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal-only</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal-only, Dual-key</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy</td>
    </tr>
  </tbody>
</table>

**FloodFill Requirements:**

- **ECIES-only destinations**: Require majority of floodfills on 0.9.46+ for encrypted lookups
- **Dual-key destinations**: Work with any floodfill version
- **Current status**: Near 100% floodfill adoption as of 2025

### Migration Guide

**Migrating from ElGamal to ECIES:**

**Step 1: Enable Dual-Key Mode**

```properties
# Ajouter ECIES (schéma de chiffrement intégré à courbe elliptique) tout en conservant ElGamal (cryptosystème de chiffrement asymétrique)

i2cp.leaseSetEncType=4,0

```

**Step 2: Monitor Connections**

```bash
# Vérifiez les types de connexion

i2prouter.exe status

# ou

http://127.0.0.1:7657/peers

```

**Step 3: Switch to ECIES-Only (after testing)**

```properties
# Supprimer ElGamal

i2cp.leaseSetEncType=4

```

**Step 4: Restart Application**

```bash
# Redémarrer l'I2P router ou l'application

systemctl restart i2p

# ou

i2prouter.exe restart

```

**Rollback Plan:**

```properties
# Revenir à ElGamal uniquement en cas de problèmes

i2cp.leaseSetEncType=0

```

### Performance Tuning

**Session Limits:**

```properties
# Nombre maximal de sessions entrantes

i2p.router.maxInboundSessions=1000

# Nombre maximal de sessions sortantes

i2p.router.maxOutboundSessions=1000

# Délai d’expiration de la session (secondes)

i2p.router.sessionTimeout=600

```

**Memory Limits:**

```properties
# Limite de stockage des étiquettes (Ko)

i2p.ecies.maxTagMemory=10240  # 10 Mo

# Fenêtre d'anticipation

i2p.ecies.tagLookAhead=160 i2p.ecies.tagLookAheadMin=32

```

**Ratchet Policy:**

```properties
# Messages avant le ratchet

i2p.ecies.ratchetThreshold=4096

# Délai avant déclenchement du cliquet (secondes)

i2p.ecies.ratchetTimeout=600  # 10 minutes

```

### Monitoring and Debugging

**Logging:**

```properties
# Activer la journalisation de débogage pour ECIES (schéma de chiffrement intégré à courbes elliptiques)

logger.i2p.router.transport.ecies=DEBUG

```

**Metrics:**

Monitor these metrics:

1. **NS Success Rate**: Percentage of NS messages receiving NSR
2. **Session Establishment Time**: Time from NS to first ES
3. **Tag Storage Usage**: Current memory usage for tags
4. **Ratchet Frequency**: How often sessions ratchet
5. **Session Lifetime**: Average session duration

**Common Issues:**

1. **NS Timeout**: No NSR received
   - Check destination is online
   - Check floodfill availability
   - Verify LeaseSet published correctly

2. **High Memory Usage**: Too many tags stored
   - Reduce look-ahead window
   - Decrease session timeout
   - Implement aggressive expiration

3. **Frequent Ratchets**: Sessions ratcheting too often
   - Increase ratchet threshold
   - Check for retransmissions

4. **Session Failures**: ES messages failing to decrypt
   - Verify tag synchronization
   - Check for replay attacks
   - Validate nonce construction

---

## References

### Specifications

1. **ECIES Proposal**: [Proposal 144](/proposals/144-ecies-x25519-aead-ratchet/)
2. **I2NP**: [I2NP Specification](/docs/specs/i2np/)
3. **Common Structures**: [Common Structures Specification](/docs/specs/common-structures/)
4. **NTCP2**: [NTCP2 Specification](/docs/specs/ntcp2/)
5. **SSU2**: [SSU2 Specification](/docs/specs/ssu2/)
6. **I2CP**: [I2CP Specification](/docs/specs/i2cp/)
7. **ElGamal/AES+SessionTags**: [ElGamal/AES Specification](/docs/legacy/elgamal-aes/)

### Cryptographic Standards

1. **Noise Protocol Framework**: [Noise Specification](https://noiseprotocol.org/noise.html) (Revision 34, 2018-07-11)
2. **Signal Double Ratchet**: [Signal Specification](https://signal.org/docs/specifications/doubleratchet/)
3. **RFC 7748**: [Elliptic Curves for Security (X25519)](https://tools.ietf.org/html/rfc7748)
4. **RFC 7539**: [ChaCha20 and Poly1305 for IETF Protocols](https://tools.ietf.org/html/rfc7539)
5. **RFC 5869**: [HKDF (HMAC-based Key Derivation Function)](https://tools.ietf.org/html/rfc5869)
6. **RFC 2104**: [HMAC: Keyed-Hashing for Message Authentication](https://tools.ietf.org/html/rfc2104)
7. **Elligator2**: [Elligator Paper](https://elligator.cr.yp.to/elligator-20130828.pdf)

### Implementation Resources

1. **Java I2P**: [i2p.i2p Repository](https://github.com/i2p/i2p.i2p)
2. **i2pd (C++)**: [i2pd Repository](https://github.com/PurpleI2P/i2pd)
3. **OBFS4 (Elligator2)**: [obfs4proxy Repository](https://gitlab.com/yawning/obfs4)

### Additional Information

1. **I2P Website**: [/](/)
2. **I2P Forum**: [https://i2pforum.net](https://i2pforum.net)
3. **I2P Wiki**: [https://wiki.i2p-projekt.de](https://wiki.i2p-projekt.de)

---

## Appendix A: KDF Summary

**All KDF Operations in ECIES:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Operation</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Input</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Info String</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Output</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NS Initial ChainKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">protocol_name</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">(none - SHA256)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">h, chainKey</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NS Static Key Section</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, es_shared</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">""</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, k</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NS Payload Section (bound)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, ss_shared</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">""</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, k</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR Tagset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"SessionReplyTags"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">tagsetKey</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR ee DH</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, ee_shared</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">""</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR se DH</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, se_shared</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">""</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, k</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR Split</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">""</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">k_ab, k_ba</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NSR Payload</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">k_ba</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"AttachPayloadKDF"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">k_nsr</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DH Initialize</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">rootKey, k</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"KDFDHRatchetStep"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">nextRootKey, chainKey</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Tag and Key Chain Keys</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"TagAndKeyGenKeys"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">sessTag_ck, symmKey_ck</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Session Tag Init</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">sessTag_ck</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"STInitialization"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, CONSTANT</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Session Tag Gen</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, CONSTANT</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"SessionTagKeyGen"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, tag</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Symmetric Key Gen</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"SymmetricRatchet"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">chainKey, key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DH Ratchet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">sharedSecret</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">"XDHRatchetTagSet"</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">tagsetKey</td>
    </tr>
  </tbody>
</table>

---

## Appendix B: Message Size Calculator

**Calculate message sizes for capacity planning:**

```python
def calculate_ns_size(payload_size, bound=True):

    """Calculate New Session message size"""
    ephemeral_key = 32
    static_section = 32 + 16  # encrypted + MAC
    payload_encrypted = payload_size + 16  # + MAC
    
    return ephemeral_key + static_section + payload_encrypted

def calculate_nsr_size(payload_size):

    """Calculate New Session Reply message size"""
    tag = 8
    ephemeral_key = 32
    key_section_mac = 16
    payload_encrypted = payload_size + 16  # + MAC
    
    return tag + ephemeral_key + key_section_mac + payload_encrypted

def calculate_es_size(payload_size):

    """Calculate Existing Session message size"""
    tag = 8
    payload_encrypted = payload_size + 16  # + MAC
    
    return tag + payload_encrypted

# Exemples

print("NS (bound, charge utile de 1 Ko) :", calculate_ns_size(1024, bound=True), "octets")

# Sortie: 1120 octets

print("NSR (1KB payload):", calculate_nsr_size(1024), "bytes")

# Sortie : 1096 octets

print("ES (1 Ko de charge utile) :", calculate_es_size(1024), "octets")

# Sortie : 1048 octets

```

---

## Appendix C: Glossary

**AEAD**: Authenticated Encryption with Associated Data - encryption mode that provides both confidentiality and authenticity

**Authentication Level**: Noise protocol security property indicating strength of sender identity verification

**Binding**: Association of a session with a specific far-end destination

**ChaCha20**: Stream cipher designed by Daniel J. Bernstein

**ChainKey**: Cryptographic key used in HKDF chains to derive subsequent keys

**Confidentiality Level**: Noise protocol security property indicating strength of forward secrecy

**DH**: Diffie-Hellman key agreement protocol

**Elligator2**: Encoding technique to make elliptic curve points indistinguishable from random

**Ephemeral Key**: Short-lived key used only for a single handshake

**ES**: Existing Session message (used after handshake completion)

**Forward Secrecy**: Property ensuring past communications remain secure if keys are compromised

**Garlic Clove**: I2NP message container for end-to-end delivery

**HKDF**: HMAC-based Key Derivation Function

**IK Pattern**: Noise handshake pattern where initiator sends static key immediately

**KCI**: Key Compromise Impersonation attack

**KDF**: Key Derivation Function - cryptographic function for generating keys from other keys

**LeaseSet**: I2P structure containing a destination's public keys and tunnel information

**LS2**: LeaseSet version 2 with encryption type support

**MAC**: Message Authentication Code - cryptographic checksum proving authenticity

**MixHash**: Noise protocol function for maintaining running hash transcript

**NS**: New Session message (initiates new session)

**NSR**: New Session Reply message (response to NS)

**Nonce**: Number used once - ensures unique encryption even with same key

**Pairing**: Linking an inbound session with an outbound session for bidirectional communication

**Poly1305**: Message authentication code designed by Daniel J. Bernstein

**Ratchet**: Cryptographic mechanism for deriving sequential keys

**Session Tag**: 8-byte one-time identifier for existing session messages

**Static Key**: Long-term key associated with a destination's identity

**Tag Set**: Collection of session tags derived from a common root

**X25519**: Elliptic curve Diffie-Hellman key agreement using Curve25519

---