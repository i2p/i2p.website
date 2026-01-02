---
title: "Structures communes"
description: "Types de données partagés et formats de sérialisation utilisés dans l’ensemble des spécifications I2P"
slug: "common-structures"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Vue d'ensemble

Ce document spécifie les structures de données fondamentales utilisées dans l’ensemble des protocoles I2P, y compris [I2NP](/docs/specs/i2np/), [I2CP](/docs/specs/i2cp/), [SSU2](/docs/specs/ssu2/), [NTCP2](/docs/specs/ntcp2/), et d’autres. Ces structures communes garantissent l’interopérabilité entre les différentes implémentations I2P et les couches de protocole.

### Principaux changements depuis la 0.9.58

- ElGamal et DSA-SHA1 déconseillés pour les identités du router (utiliser X25519 + EdDSA)
- Prise en charge post-quantique de ML-KEM en test bêta (opt-in, activation facultative, à partir de la 2.10.0)
- Options des enregistrements de service normalisées ([Proposition 167](/proposals/167-service-records/), implémentées depuis 0.9.66)
- Spécifications de bourrage compressible finalisées ([Proposition 161](/fr/proposals/161-ri-dest-padding/), implémentées depuis 0.9.57)

---

## Spécifications des types communs

### Entier

**Description:** Représente un entier non négatif au format d’octets réseau big-endian (gros-boutiste).

**Contenu:** 1 à 8 octets représentant un entier non signé.

**Utilisation :** Longueurs de champ, décomptes, identifiants de type et valeurs numériques dans l'ensemble des protocoles I2P.

---

### Date

**Description:** Horodatage représentant le nombre de millisecondes écoulées depuis l'époque Unix (1er janvier 1970 00:00:00 GMT).

**Contenu :** Entier sur 8 octets (long non signé)

**Valeurs spéciales :** - `0` = Date non définie ou nulle - Valeur maximale : `0xFFFFFFFFFFFFFFFF` (année 584,942,417,355)

**Notes d’implémentation:** - Toujours le fuseau horaire UTC/GMT - Précision à la milliseconde requise - Utilisé pour l’expiration du lease (bail de tunnel), la publication de RouterInfo et la validation de l’horodatage

---

### Chaîne

**Description :** Chaîne encodée en UTF-8 avec un préfixe de longueur.

**Format :**

```
+----+----+----+----+----+----+
|len | UTF-8 encoded data...   |
+----+----+----+----+----+----+

len :: Integer (1 byte)
       Value: 0-255 (string length in bytes, NOT characters)

data :: UTF-8 encoded bytes
        Length: 0-255 bytes
```
**Contraintes:** - Longueur maximale: 255 octets (et non des caractères - les séquences UTF-8 à plusieurs octets comptent comme plusieurs octets) - La longueur peut être zéro (chaîne vide) - Le terminateur nul n'est PAS inclus - La chaîne n'est PAS terminée par un caractère nul

**Important:** Les séquences UTF-8 peuvent utiliser plusieurs octets par caractère. Une chaîne de 100 caractères peut dépasser la limite de 255 octets si elle utilise des caractères encodés sur plusieurs octets.

---

## Structures de clés cryptographiques

### Clé publique

**Description:** Clé publique pour le chiffrement asymétrique. Le type et la taille de la clé dépendent du contexte ou sont spécifiés dans un Key Certificate (certificat de clé).

**Type par défaut:** ElGamal (déprécié pour les identités de Router à partir de la version 0.9.58)

**Types pris en charge :**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destinations only (unused field)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated for RIs</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">132</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Recommended</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">800</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1184</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1568</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512_CT</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">768</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768_CT</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1088</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024_CT</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1568</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
  </tbody>
</table>
**Exigences d’implémentation:**

1. **X25519 (Type 4) - Standard actuel:**
   - Utilisé pour le chiffrement ECIES-X25519-AEAD-Ratchet
   - Obligatoire pour les identités de router depuis la version 0.9.48
   - Encodage en little-endian (ordre des octets du moins significatif au plus)
   - Voir [ECIES](/docs/specs/ecies/) et [ECIES-ROUTERS](/docs/specs/ecies/#routers)

2. **ElGamal (Type 0) - Ancien:**
   - Déprécié pour les Identités de Router depuis 0.9.58
   - Toujours valide pour les Destinations (champ inutilisé depuis 0.6/2005)
   - Utilise des nombres premiers fixes définis dans [la spécification ElGamal](/docs/specs/cryptography/)
   - Prise en charge maintenue pour la rétrocompatibilité

3. **MLKEM (post-quantique) - Bêta:**
   - L'approche hybride combine ML-KEM avec X25519
   - NON activée par défaut dans la version 2.10.0
   - Nécessite une activation manuelle via Hidden Service Manager (gestionnaire de service caché)
   - Voir [ECIES-HYBRID](/docs/specs/ecies/#hybrid) et [Proposal 169](/proposals/169-pq-crypto/)
   - Les codes de type et les spécifications sont susceptibles d'être modifiés

**JavaDoc:** [PublicKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/PublicKey.html)

---

### PrivateKey

**Description:** Clé privée pour le déchiffrement asymétrique, correspondant aux types PublicKey.

**Stockage:** Type et longueur inférés du contexte ou stockés séparément dans des structures de données/fichiers de clés.

**Types pris en charge:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destinations only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated for RIs</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">48</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">66</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">See Proposal 145</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Recommended</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024_X25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mixed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Hybrid PQ, LeaseSets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1632</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM768</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2400</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MLKEM1024</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3168</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Handshakes only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td></tr>
  </tbody>
</table>
**Notes de sécurité :** - Les clés privées DOIVENT être générées à l'aide de générateurs de nombres aléatoires cryptographiquement sûrs - Les clés privées X25519 utilisent le "scalar clamping" (ajustement du scalaire) tel que défini dans la RFC 7748 - Les données de clé DOIVENT être effacées de manière sécurisée de la mémoire lorsqu'elles ne sont plus nécessaires

**JavaDoc:** [PrivateKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/PrivateKey.html)

---

### Clé de session

**Description :** Clé symétrique pour le chiffrement et le déchiffrement AES-256 dans le tunnel et la garlic encryption d'I2P.

**Contenu :** 32 octets (256 bits)

**Utilisation:** - Chiffrement au niveau du tunnel (AES-256/CBC avec IV) - Chiffrement des messages (garlic encryption) - Chiffrement de session de bout en bout

**Génération:** DOIT utiliser un générateur de nombres aléatoires cryptographiquement sécurisé.

**JavaDoc:** [SessionKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SessionKey.html)

---

### SigningPublicKey

**Description:** Clé publique pour la vérification de la signature. Type et longueur spécifiés dans le certificat de clé de la Destination ou déduits du contexte.

**Type par défaut:** DSA_SHA1 (déprécié depuis la 0.9.58)

**Types pris en charge:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA_SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">128</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA256_P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Older Destinations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA384_P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA512_P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">132</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA256_2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA384_3072</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA512_4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Recommended for SU3</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Recommended</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519ph</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.25</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RedDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted leasesets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specialized</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved (GOST)</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">9</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Proposal 134</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved (GOST)</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">128</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Proposal 134</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved (MLDSA)</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12-20</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBD</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Proposal 169</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Experimental</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">65280-65534</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Testing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Never production</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">65535</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Future expansion</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td></tr>
  </tbody>
</table>
**Exigences d'implémentation:**

1. **EdDSA_SHA512_Ed25519 (Type 7) - Standard actuel :**
   - Valeur par défaut pour toutes les nouvelles Router Identities et destinations depuis fin 2015
   - Utilise la courbe Ed25519 avec hachage SHA-512
   - Clés publiques de 32 octets, signatures de 64 octets
   - Encodage little-endian (ordre des octets où l'octet le moins significatif vient en premier), contrairement à la plupart des autres types
   - Performances et sécurité élevées

2. **RedDSA_SHA512_Ed25519 (Type 11) - Spécialisé :**
   - Utilisé UNIQUEMENT pour les leasesets chiffrés et le blinding (aveuglement)
   - Jamais utilisé pour les Router Identities ni les destinations standard
   - Principales différences par rapport à EdDSA :
     - Clés privées via réduction modulaire (pas de clamping (ajustement par masquage de bits))
     - Les signatures incluent 80 octets de données aléatoires
     - Utilise directement les clés publiques (et non des hachages de clés privées)
   - Voir [Spécification Red25519](//docs/specs/red25519-signature-scheme/

3. **DSA_SHA1 (Type 0) - Ancien:**
   - Déprécié pour les Router Identities (identités du router) à partir de la 0.9.58
   - Déconseillé pour les nouvelles Destinations
   - DSA 1024 bits avec SHA-1 (faiblesses connues)
   - Prise en charge maintenue uniquement pour compatibilité

4. **Clés à plusieurs éléments :**
   - Lorsqu’elles sont composées de deux éléments (p. ex., points ECDSA X,Y)
   - Chaque élément est complété par des zéros en tête jusqu’à length/2
   - Exemple : clé ECDSA de 64 octets = X de 32 octets + Y de 32 octets

**JavaDoc:** [SigningPublicKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SigningPublicKey.html)

---

### SigningPrivateKey

**Description:** Clé privée utilisée pour créer des signatures, correspondant aux types SigningPublicKey (clé publique de signature).

**Stockage :** Type et longueur spécifiés lors de la création.

**Types pris en charge:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA_SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA256_P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Older Destinations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA384_P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">48</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA512_P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">66</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA256_2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA384_3072</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">768</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA512_4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1024</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Recommended for SU3</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Recommended</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519ph</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.25</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RedDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted leasesets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specialized</td></tr>
  </tbody>
</table>
**Exigences de sécurité:** - Générer à partir d'une source d'aléa cryptographiquement sûre - Protéger avec des contrôles d'accès appropriés - Effacer de la mémoire de manière sécurisée une fois terminé - Pour EdDSA: graine de 32 octets hachée avec SHA-512, les 32 premiers octets deviennent le scalaire (clampé) - Pour RedDSA: génération de clé différente (réduction modulaire au lieu de clampage)

**JavaDoc:** [SigningPrivateKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SigningPrivateKey.html) (clé privée de signature)

---

### Signature

**Description:** Signature cryptographique des données, utilisant l’algorithme de signature correspondant au type SigningPrivateKey.

**Type et longueur:** Déduits du type de clé utilisé pour la signature.

**Types pris en charge:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Endianness</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA_SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">40</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA256_P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Older Destinations</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA384_P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_SHA512_P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">132</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA256_2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA384_3072</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_SHA512_4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current for SU3</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current standard</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Recommended</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA_SHA512_Ed25519ph</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.25</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline signing only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Rare</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RedDSA_SHA512_Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Little</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted leasesets only</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specialized</td></tr>
  </tbody>
</table>
**Notes de format :** - Les signatures à éléments multiples (p. ex., valeurs R et S d’ECDSA) sont complétées, pour chaque élément, à longueur/2, en les préfixant de zéros - EdDSA et RedDSA utilisent un encodage en little-endian - Tous les autres types utilisent un encodage en big-endian

**Vérification :** - Utiliser la SigningPublicKey (clé publique de signature) correspondante - Suivre les spécifications de l’algorithme de signature pour le type de clé - Vérifier que la longueur de la signature correspond à la longueur attendue pour ce type de clé

**JavaDoc:** [Signature](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Signature.html)

---

### Hachage

**Description:** Hachage SHA-256 des données, utilisé partout dans I2P pour la vérification de l’intégrité et l’identification.

**Contenu:** 32 octets (256 bits)

**Utilisation :** - Hachages de Router Identity (clés de la base de données réseau) - Hachages de Destination (clés de la base de données réseau) - Identification de la passerelle de Tunnel dans les Leases - Vérification de l'intégrité des données - Génération de Tunnel ID

**Algorithme :** SHA-256 tel que défini dans la norme FIPS 180-4

**JavaDoc:** [Hash](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Hash.html)

---

### Session Tag (étiquette de session)

**Description:** Nombre aléatoire utilisé pour l'identification de session et le tag-based encryption (chiffrement basé sur des tags).

**Important:** La taille de Session Tag (étiquette de session) varie selon le type de chiffrement: - **ElGamal/AES+SessionTag:** 32 octets (ancien) - **ECIES-X25519:** 8 octets (standard actuel)

**Norme actuelle (ECIES):**

```
Contents: 8 bytes
Usage: Ratchet-based encryption for Destinations and Routers
```
Voir [ECIES](/docs/specs/ecies/) et [ECIES-ROUTERS](/docs/specs/ecies/#routers) pour des spécifications détaillées.

**Ancien (ElGamal/AES):**

```
Contents: 32 bytes
Usage: Deprecated encryption scheme
```
**Génération:** DOIT utiliser un générateur de nombres aléatoires cryptographiquement sûr.

**JavaDoc:** [SessionTag](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SessionTag.html)

---

### TunnelId

**Description:** Identifiant unique de la position d’un router dans un tunnel. Chaque saut dans un tunnel possède son propre TunnelId (identifiant de tunnel).

**Format :**

```
Contents: 4-byte Integer (unsigned 32-bit)
Range: Generally > 0 (zero reserved for special cases)
```
**Utilisation :** - Identifie les connexions de tunnel entrantes/sortantes à chaque router - TunnelId (identifiant de tunnel) différent à chaque saut dans la chaîne du tunnel - Utilisé dans les structures Lease (éléments du LeaseSet) pour identifier les tunnels passerelle

**Valeurs spéciales:** - `0` = Réservé à des usages particuliers du protocole (à éviter en fonctionnement normal) - Les TunnelIds (identifiants de tunnel) sont localement significatifs pour chaque router

**JavaDoc:** [TunnelId](http://docs.i2p-projekt.de/javadoc/net/i2p/data/TunnelId.html)

---

## Spécifications des certificats

### Certificat

**Description :** Conteneur pour des reçus, des preuves de travail ou des métadonnées cryptographiques, utilisés dans l’ensemble d’I2P.

**Format:**

```
+----+----+----+----+----+----+-//
|type| length  | payload
+----+----+----+----+----+----+-//

type :: Integer (1 byte)
        Values: 0-5 (see types below)

length :: Integer (2 bytes, big-endian)
          Size of payload in bytes

payload :: data
           length -> $length bytes
```
**Taille totale :** 3 octets minimum (NULL certificate, certificat nul), jusqu’à 65538 octets maximum

### Types de certificats

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Payload Length</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Total Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">NULL</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Default/empty certificate</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">HASHCASH</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused (was for proof-of-work)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">HIDDEN</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused (hidden routers don't advertise)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SIGNED</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 or 72</td><td style="border:1px solid var(--color-border); padding:0.5rem;">43 or 75</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused (DSA signature ± destination hash)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MULTIPLE</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused (multiple certificates)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">KEY</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4+</td><td style="border:1px solid var(--color-border); padding:0.5rem;">7+</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Current</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specifies key types (see below)</td></tr>
  </tbody>
</table>
### Certificat de clé (Type 5)

**Introduction:** Version 0.9.12 (décembre 2013)

**Objectif:** Spécifie des types de clés autres que le type par défaut et stocke les données de clé excédentaires au-delà de la structure KeysAndCert standard de 384 octets.

**Structure de la charge utile :**

```
+----+----+----+----+----+----+----+----+-//
|SPKtype|CPKtype| Excess SPK data     |
+----+----+----+----+----+----+----+----+-//
              | Excess CPK data...    |
+----+----+----+----+----+----+----+----+

SPKtype :: Signing Public Key Type (2 bytes)
           See SigningPublicKey table above

CPKtype :: Crypto Public Key Type (2 bytes)
           See PublicKey table above

Excess SPK data :: Signing key bytes beyond 128 bytes
                   Length: 0 to 65531 bytes

Excess CPK data :: Crypto key bytes beyond 256 bytes
                   Length: 0 to remaining space
```
**Remarques importantes pour l'implémentation:**

1. **Ordre des types de clés:**
   - **AVERTISSEMENT:** Le type de clé de signature vient AVANT le type de clé de chiffrement
   - C'est contre-intuitif, mais cela est conservé pour des raisons de compatibilité
   - Ordre: SPKtype, CPKtype (et non CPKtype, SPKtype)

2. **Agencement des données de clés dans KeysAndCert (structure combinant les clés et le certificat):**
   ```
   [Crypto Public Key (partial/complete)]
   [Padding (if total key lengths < 384)]
   [Signing Public Key (partial/complete)]
   [Certificate Header (3 bytes)]
   [Key Certificate (4+ bytes)]
   [Excess Signing Key Data]
   [Excess Crypto Key Data]
   ```

3. **Calcul des données de clé excédentaires:**
   - Si Crypto Key > 256 octets: Excess = (Crypto Length - 256)
   - Si Signing Key > 128 octets: Excess = (Signing Length - 128)
   - Padding = max(0, 384 - Crypto Length - Signing Length)

**Exemples (Clé cryptographique ElGamal):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Signing Key Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Total SPK Length</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Padding</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Excess in Cert</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Total Structure Size</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA_SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">128</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 7 = 394</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">64</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 7 = 394</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 7 = 394</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA_P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">132</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 11 = 398</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">128</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 135 = 522</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA_4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">512</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">384</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 391 = 778</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">96</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 + 7 = 394</td></tr>
  </tbody>
</table>
**Exigences relatives à l'identité du Router:** - Certificat NULL utilisé jusqu'à la version 0.9.15 - Certificat de clé requis pour les types de clés non par défaut depuis la version 0.9.16 - Clés de chiffrement X25519 prises en charge depuis la version 0.9.48

**Exigences relatives à la Destination:** - certificat NULL OU Certificat de clé (au besoin) - Certificat de clé requis pour les types de clé de signature non par défaut depuis la 0.9.12 - Champ de clé publique cryptographique inutilisé depuis la 0.6 (2005), mais doit toujours être présent

**Avertissements importants:**

1. **Certificat NULL vs KEY:**
   - Un certificat KEY avec les types (0,0) spécifiant ElGamal+DSA_SHA1 est autorisé mais déconseillé
   - Utilisez toujours le certificat NULL pour ElGamal+DSA_SHA1 (représentation canonique)
   - Un certificat KEY avec (0,0) est plus long de 4 octets et peut entraîner des problèmes de compatibilité
   - Certaines implémentations peuvent ne pas gérer correctement les certificats KEY (0,0)

2. **Validation des données excédentaires :**
   - Les implémentations DOIVENT vérifier que la longueur du certificat correspond à la longueur attendue pour les types de clés
   - Rejeter les certificats contenant des données excédentaires qui ne correspondent pas aux types de clés
   - Interdire la présence de données parasites à la suite d’une structure de certificat valide

**JavaDoc:** [Certificat](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Certificate.html)

---

### Mappage

**Description:** Collection de propriétés clé-valeur utilisée pour la configuration et les métadonnées.

**Format:**

```
+----+----+----+----+----+----+----+----+
|  size   | key_string (len + data)| =  |
+----+----+----+----+----+----+----+----+
| val_string (len + data)     | ;  | ...
+----+----+----+----+----+----+----+

size :: Integer (2 bytes, big-endian)
        Total number of bytes that follow (not including size field)
        Range: 0 to 65535

key_string :: String
              Format: 1-byte length + UTF-8 data
              Length: 0-255 bytes

= :: Single byte (0x3D, '=' character)

val_string :: String
              Format: 1-byte length + UTF-8 data
              Length: 0-255 bytes

; :: Single byte (0x3B, ';' character)

[Repeat key_string = val_string ; for additional entries]
```
**Limites de taille:** - Longueur de la clé : 0-255 octets (+ 1 octet de longueur) - Longueur de la valeur : 0-255 octets (+ 1 octet de longueur) - Taille totale du mappage : 0-65535 octets (+ 2 octets du champ de taille) - Taille maximale de la structure : 65537 octets

**Exigence critique de tri:**

Lorsque des mappages apparaissent dans des **structures signées** (RouterInfo, RouterAddress, Destination properties, I2CP SessionConfig), les entrées DOIVENT être triées par clé pour garantir l'invariance de la signature:

1. **Méthode de tri:** Ordre lexicographique utilisant les valeurs des points de code Unicode (équivalent à Java String.compareTo())
2. **Sensibilité à la casse:** Les clés et les valeurs sont généralement sensibles à la casse (selon l'application)
3. **Clés en double:** NON autorisées dans les structures signées (provoquera un échec de vérification de la signature)
4. **Encodage des caractères:** Comparaison au niveau des octets en UTF-8

**Pourquoi le tri est important :** - Les signatures sont calculées sur la représentation en octets - Des ordres de clés différents produisent des signatures différentes - Les mappages non signés ne nécessitent pas de tri mais devraient suivre la même convention

**Notes d'implémentation:**

1. **Redondance d'encodage:**
   - Les délimiteurs `=` et `;` ET les octets de longueur de chaîne sont présents
   - C’est inefficace, mais maintenu pour des raisons de compatibilité
   - Les octets de longueur font autorité; les délimiteurs sont requis mais redondants

2. **Prise en charge des caractères :**
   - Malgré la documentation, `=` et `;` SONT pris en charge dans les chaînes (les octets de longueur gèrent cela)
   - L’encodage UTF-8 prend en charge la totalité d’Unicode
   - **Avertissement :** I2CP utilise UTF-8, mais I2NP, historiquement, ne gérait pas correctement UTF-8
   - Utilisez l’ASCII pour les mappages I2NP lorsque possible pour une compatibilité maximale

3. **Contextes particuliers:**
   - **RouterInfo/RouterAddress:** DOIT être trié, sans doublons
   - **I2CP SessionConfig:** DOIT être trié, sans doublons  
   - **Mappages d’application:** Tri recommandé mais pas toujours obligatoire

**Exemple (options de RouterInfo):**

```
Mapping size: 45 bytes
Sorted entries:
  caps=L       (capabilities)
  netId=2      (network ID)
  router.version=0.9.67
```
**JavaDoc :** [DataHelper](http://docs.i2p-projekt.de/javadoc/net/i2p/data/DataHelper.html)

---

## Spécification des structures communes

### Clés et certificats

**Description:** Structure fondamentale combinant une clé de chiffrement, une clé de signature et un certificat. Utilisée à la fois comme RouterIdentity et Destination.

**Structure :**

```
+----+----+----+----+----+----+----+----+
| public_key                            |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| padding (optional)                    |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signing_key                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| certificate                           |
+----+----+----+-//

public_key :: PublicKey (partial or full)
              Default: 256 bytes (ElGamal)
              Other sizes: As specified in Key Certificate

padding :: Random data
           Length: 0 bytes or as needed
           CONSTRAINT: public_key + padding + signing_key = 384 bytes

signing_key :: SigningPublicKey (partial or full)
               Default: 128 bytes (DSA_SHA1)
               Other sizes: As specified in Key Certificate

certificate :: Certificate
               Minimum: 3 bytes (NULL certificate)
               Common: 7 bytes (Key Certificate with default keys)

TOTAL LENGTH: 387+ bytes (never assume exactly 387!)
```
**Alignement des clés:** - **Clé publique de chiffrement:** Alignée au début (octet 0) - **Bourrage:** Au milieu (si nécessaire) - **Clé publique de signature:** Alignée à la fin (octet 256 à octet 383) - **Certificat:** Commence à l’octet 384

**Calcul de la taille:**

```
Total size = 384 + 3 + key_certificate_length

For NULL certificate (ElGamal + DSA_SHA1):
  Total = 384 + 3 = 387 bytes

For Key Certificate (EdDSA + X25519):
  Total = 384 + 3 + 4 = 391 bytes

For larger keys (e.g., RSA_4096):
  Total = 384 + 3 + 4 + excess_key_data_length
```
### Directives de génération de bourrage ([Proposition 161](/fr/proposals/161-ri-dest-padding/))

**Version de l'implémentation:** 0.9.57 (janvier 2023, sortie 2.1.0)

**Contexte:** - Pour les clés autres que ElGamal+DSA, un bourrage est présent dans la structure fixe de 384 octets - Pour les Destinations, le champ de clé publique de 256 octets n’est plus utilisé depuis la version 0.6 (2005) - Le bourrage doit être généré de manière à être compressible tout en restant sécurisé

**Prérequis :**

1. **Données aléatoires minimales :**
   - Utilisez au moins 32 octets de données aléatoires cryptographiquement sécurisées
   - Cela fournit une entropie suffisante pour la sécurité

2. **Stratégie de compression:**
   - Répéter les 32 octets dans tout le champ de bourrage/clé publique
   - Des protocoles comme I2NP Database Store, Streaming SYN, SSU2 handshake utilisent la compression
   - Importantes économies de bande passante sans compromettre la sécurité

3. **Exemples:**

**Identité du router (X25519 + EdDSA):**

```
Structure:
- 32 bytes X25519 public key
- 320 bytes padding (10 copies of 32-byte random data)
- 32 bytes EdDSA public key
- 7 bytes Key Certificate

Compression savings: ~288 bytes when compressed
```
**Destination (ElGamal-unused + EdDSA):**

```
Structure:
- 256 bytes unused ElGamal field (11 copies of 32-byte random data, truncated to 256)
- 96 bytes padding (3 copies of 32-byte random data)
- 32 bytes EdDSA public key  
- 7 bytes Key Certificate

Compression savings: ~320 bytes when compressed
```
4. **Pourquoi cela fonctionne :**
   - Le hachage SHA-256 de la structure complète inclut toujours toute l'entropie
   - La distribution DHT (table de hachage distribuée) de la base de données réseau ne dépend que du hachage
   - La clé de signature (32 octets EdDSA/X25519) fournit 256 bits d'entropie
   - 32 octets supplémentaires de données aléatoires répétées = 512 bits d'entropie au total
   - Plus que suffisant pour la solidité cryptographique

5. **Notes d’implémentation :**
   - DOIT stocker et transmettre la structure complète de 387+ octets
   - Hachage SHA-256 calculé sur la structure complète non compressée
   - Compression appliquée à la couche protocolaire (I2NP, Streaming, SSU2)
   - Rétrocompatible avec toutes les versions depuis la version 0.6 (2005)

**JavaDoc :** [KeysAndCert](http://docs.i2p-projekt.de/javadoc/net/i2p/data/KeysAndCert.html)

---

### RouterIdentity (identité du router)

**Description:** Identifie de manière unique un router dans le réseau I2P. Structure identique à KeysAndCert.

**Format:** Voir la structure KeysAndCert ci-dessus

**Exigences actuelles (à partir de la version 0.9.58):**

1. **Types de clés obligatoires:**
   - **Chiffrement:** X25519 (type 4, 32 octets)
   - **Signature:** EdDSA_SHA512_Ed25519 (type 7, 32 octets)
   - **Certificat:** Certificat de clé (type 5)

2. **Types de clés dépréciés:**
   - ElGamal (type 0) déprécié pour les Router Identities (identités de router) à partir de la version 0.9.58
   - DSA_SHA1 (type 0) déprécié pour les Router Identities à partir de la version 0.9.58
   - Ces types ne doivent PAS être utilisés pour de nouveaux routers

3. **Taille typique:**
   - X25519 + EdDSA avec certificat de clé = 391 octets
   - 32 octets de clé publique X25519
   - remplissage de 320 octets (compressible selon la [Proposition 161](/fr/proposals/161-ri-dest-padding/))
   - 32 octets de clé publique EdDSA
   - certificat de 7 octets (en-tête de 3 octets + 4 octets pour les types de clés)

**Évolution historique:** - Avant 0.9.16: toujours un NULL certificate (certificat NULL) (ElGamal + DSA_SHA1) - 0.9.16-0.9.47: prise en charge du Key Certificate (certificat de clé) ajoutée - 0.9.48+: clés de chiffrement X25519 prises en charge - 0.9.58+: ElGamal et DSA_SHA1 dépréciés

**Clé de la base de données réseau:** - RouterInfo (informations du router) indexé par le hachage SHA-256 de la RouterIdentity (identité du router) complète - Hachage calculé sur la structure complète de 391+ octets (y compris le bourrage)

**Voir aussi :** - Recommandations pour la génération du bourrage ([Proposition 161](/fr/proposals/161-ri-dest-padding/)) - Spécification du certificat de clé ci-dessus

**JavaDoc :** [RouterIdentity](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterIdentity.html)

---

### Destination

**Description:** Identifiant de point de terminaison pour la remise sécurisée de messages. Structurellement identique à KeysAndCert (clés et certificat), mais avec une sémantique d'utilisation différente.

**Format:** Voir la structure KeysAndCert ci-dessus

**Différence critique par rapport à RouterIdentity:** - **Le champ de clé publique est INUTILISÉ et peut contenir des données aléatoires** - Ce champ est inutilisé depuis la version 0.6 (2005) - Servait à l’origine à l’ancien chiffrement I2CP-to-I2CP (désactivé) - Actuellement utilisé uniquement comme IV (vecteur d’initiation) pour le chiffrement LeaseSet déprécié

**Recommandations actuelles :**

1. **Clé de signature:**
   - **Recommandé:** EdDSA_SHA512_Ed25519 (type 7, 32 octets)
   - Alternative: types ECDSA pour la compatibilité avec les anciennes versions
   - À éviter: DSA_SHA1 (obsolète, déconseillé)

2. **Clé de chiffrement :**
   - Le champ est inutilisé mais doit être présent
   - **Recommandé :** Remplir avec des données aléatoires conformément à [Proposal 161](/fr/proposals/161-ri-dest-padding/) (compressibles)
   - Taille : toujours 256 octets (emplacement ElGamal, même s’il n’est pas utilisé pour ElGamal)

3. **Certificat:**
   - Certificat NULL pour ElGamal + DSA_SHA1 (ancien format uniquement)
   - Certificat de clé pour tous les autres types de clés de signature

**Destination moderne typique:**

```
Structure:
- 256 bytes unused field (random data, compressible)
- 96 bytes padding (random data, compressible)
- 32 bytes EdDSA signing public key
- 7 bytes Key Certificate

Total: 391 bytes
Compression savings: ~320 bytes
```
**Clé de chiffrement en vigueur :** - La clé de chiffrement de la Destination se trouve dans le **LeaseSet**, et non dans la Destination - Le LeaseSet contient la/les clé(s) publique(s) de chiffrement actuelle(s) - Voir la spécification LeaseSet2 pour la gestion des clés de chiffrement

**Clé de la base de données réseau:** - LeaseSet indexé par le hachage SHA-256 de la Destination complète - Hachage calculé sur l'intégralité de la structure de 387+ octets

**JavaDoc :** [Destination](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Destination.html)

---

## Structures de la base de données du réseau

### Bail

**Description:** Autorise un tunnel spécifique à recevoir des messages pour une Destination. Fait partie du format LeaseSet original (type 1).

**Format:**

```
+----+----+----+----+----+----+----+----+
| tunnel_gw                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|     tunnel_id     |      end_date
+----+----+----+----+----+----+----+----+
                    |
+----+----+----+----+

tunnel_gw :: Hash (32 bytes)
             SHA-256 hash of the gateway RouterIdentity

tunnel_id :: TunnelId (4 bytes)
             Tunnel identifier at the gateway router

end_date :: Date (8 bytes)
            Expiration timestamp in milliseconds since epoch
```
**Taille totale :** 44 octets

**Utilisation:** - Utilisé uniquement dans le LeaseSet original (type 1, obsolète) - Pour LeaseSet2 et les variantes ultérieures, utilisez plutôt Lease2

**JavaDoc:** [Lease](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Lease.html)

---

### LeaseSet (Type 1)

**Description:** Format LeaseSet d’origine. Contient des tunnels autorisés et des clés pour une Destination (identité de service I2P). Stocké dans la base de données réseau. **Statut: Déprécié** (utilisez LeaseSet2 à la place).

**Structure:**

```
+----+----+----+----+----+----+----+----+
| destination                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| encryption_key                        |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signing_key                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| num| Lease 0                          |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Lease 1                               |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Lease ($num-1)                        |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

destination :: Destination
               Length: 387+ bytes

encryption_key :: PublicKey (256 bytes, ElGamal)
                  Used for end-to-end ElGamal/AES+SessionTag encryption
                  Generated anew at each router startup (not persistent)

signing_key :: SigningPublicKey (128+ bytes)
               Same type as Destination signing key
               Used for LeaseSet revocation (unimplemented)
               Generated anew at each router startup (not persistent)

num :: Integer (1 byte)
       Number of Leases to follow
       Range: 0-16

leases :: Array of Lease structures
          Length: $num × 44 bytes
          Each Lease is 44 bytes

signature :: Signature (40+ bytes)
             Length determined by Destination signing key type
             Signed by Destination's SigningPrivateKey
```
**Stockage de base de données:** - **Type de base de données:** 1 - **Clé:** hachage SHA-256 de la destination - **Valeur:** structure complète de LeaseSet

**Notes importantes:**

1. **Clé publique de chiffrement de la Destination non utilisée :**
   - Le champ de clé publique de chiffrement dans la Destination n'est pas utilisé
   - La clé de chiffrement dans le LeaseSet (structure de baux I2P) est la clé de chiffrement réelle

2. **Clés temporaires :**
   - `encryption_key` est temporaire (régénérée au démarrage du router)
   - `signing_key` est temporaire (régénérée au démarrage du router)
   - Aucune des deux clés n'est persistante d'un redémarrage à l'autre

3. **Révocation (non implémentée):**
   - `signing_key` était prévu pour la révocation du LeaseSet
   - Le mécanisme de révocation n'a jamais été implémenté
   - Un LeaseSet à zéro lease (entrée de tunnel temporaire) était prévu pour la révocation mais n'est pas utilisé

4. **Versionnage/Horodatage:**
   - LeaseSet n’a pas de champ d’horodatage `published` explicite
   - La version est l’expiration la plus imminente de tous les leases (autorisations temporaires de tunnels entrants)
   - Un nouveau LeaseSet doit avoir une expiration de lease plus imminente pour être accepté

5. **Publication de l'expiration des baux:**
   - Pré-0.9.7: Tous les baux publiés avec la même date d'expiration (la plus proche)
   - 0.9.7+: Publication des dates d'expiration individuelles réelles des baux
   - Ceci est un détail d'implémentation, qui ne fait pas partie de la spécification

6. **Zéro bail :**
   - Un LeaseSet avec zéro bail est techniquement autorisé
   - Prévu pour la révocation (non implémenté)
   - Inutilisé en pratique
   - Les variantes de LeaseSet2 requièrent au moins un bail

**Dépréciation :** LeaseSet type 1 est déprécié. Les nouvelles implémentations devraient utiliser **LeaseSet2 (type 3)** qui offre : - Champ d’horodatage de publication (meilleure gestion des versions) - Prise en charge de plusieurs clés de chiffrement - Capacité de signature hors ligne - Expirations de lease (période de bail I2P) sur 4 octets (contre 8 octets) - Options plus flexibles

**JavaDoc:** [LeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/LeaseSet.html)

---

## Variantes de LeaseSet

### Lease2 (terme technique I2P)

**Description :** Format de lease (enregistrement d’accès I2P) amélioré avec expiration sur 4 octets. Utilisé dans LeaseSet2 (type 3) et MetaLeaseSet (type 7).

**Introduction :** Version 0.9.38 (voir [Proposition 123](/proposals/123-new-netdb-entries/))

**Format:**

```
+----+----+----+----+----+----+----+----+
| tunnel_gw                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|     tunnel_id     |      end_date     |
+----+----+----+----+----+----+----+----+

tunnel_gw :: Hash (32 bytes)
             SHA-256 hash of gateway RouterIdentity

tunnel_id :: TunnelId (4 bytes)
             Tunnel identifier at gateway

end_date :: 4-byte timestamp (seconds since epoch)
            Rolls over in year 2106
```
**Taille totale :** 40 octets (4 octets de moins que le Lease d'origine)

**Comparaison avec le Lease (entrée d'un leaseSet indiquant un tunnel de destination et son expiration) d'origine:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1pxsolid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Lease (Type&nbsp;1)</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Lease2 (Type&nbsp;3+)</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Size</td><td style="border:1px solid var(--color-border); padding:0.5rem;">44 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Expiration Size</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes (ms)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes (seconds)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Precision</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Millisecond</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Second</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Rollover</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Year&nbsp;292,277,026,596</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Year&nbsp;2106</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Used In</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet (deprecated)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2, MetaLeaseSet</td></tr>
  </tbody>
</table>
**JavaDoc:** [Lease2](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Lease2.html)

---

### Signature hors ligne

**Description:** Structure facultative pour des clés éphémères pré-signées, permettant la publication du LeaseSet sans accès en ligne à la clé de signature privée de la Destination.

**Introduction :** Version 0.9.38 (voir [Proposition 123](/proposals/123-new-netdb-entries/))

**Format :**

```
+----+----+----+----+----+----+----+----+
|     expires       | sigtype |         |
+----+----+----+----+----+----+         +
|       transient_public_key            |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|           signature                   |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

expires :: 4-byte timestamp (seconds since epoch)
           Expiration of transient key validity
           Rolls over in year 2106

sigtype :: 2-byte signature type
           Type of transient_public_key (see SigningPublicKey types)

transient_public_key :: SigningPublicKey
                        Length determined by sigtype
                        Temporary signing key for LeaseSet

signature :: Signature
             Length determined by Destination's signing key type
             Signature of (expires || sigtype || transient_public_key)
             Signed by Destination's permanent SigningPrivateKey
```
**Objectif:** - Permet la génération de LeaseSet hors ligne - Protège la clé maîtresse de la Destination (identité I2P) contre une exposition en ligne - La clé éphémère peut être révoquée en publiant un nouveau LeaseSet sans la signature hors ligne

**Scénarios d'utilisation :**

1. **Destinations hautement sécurisées:**
   - Clé de signature maîtresse stockée hors ligne (HSM [module matériel de sécurité], stockage à froid)
   - Clés éphémères générées hors ligne pour des durées limitées
   - La compromission d'une clé éphémère n'expose pas la clé de signature maîtresse

2. **Publication de LeaseSet chiffré:**
   - EncryptedLeaseSet peut inclure une signature hors ligne
   - Une clé publique aveuglée + une signature hors ligne offrent une sécurité supplémentaire

**Considérations de sécurité:**

1. **Gestion de l’expiration:**
   - Définissez une durée d’expiration raisonnable (de quelques jours à quelques semaines, pas des années)
   - Générez de nouvelles clés éphémères avant l’expiration
   - Une expiration plus courte = une meilleure sécurité, mais davantage de maintenance

2. **Génération de clés:**
   - Générer des clés éphémères hors ligne dans un environnement sécurisé
   - Signer hors ligne avec la clé maîtresse
   - Transférer uniquement la clé éphémère signée + la signature vers le router en ligne

3. **Révocation:**
   - Publier un nouveau LeaseSet sans signature hors ligne pour le révoquer implicitement
   - Ou publier un nouveau LeaseSet avec une clé éphémère différente

**Vérification de la signature:**

```
Data to sign: expires (4 bytes) || sigtype (2 bytes) || transient_public_key

Verification:
1. Extract Destination from LeaseSet
2. Get Destination's SigningPublicKey
3. Verify signature over (expires || sigtype || transient_public_key)
4. Check that current time < expires
5. If valid, use transient_public_key to verify LeaseSet signature
```
**Notes d'implémentation:** - La taille totale varie selon le sigtype (type de signature) et le type de clé de signature de Destination - Taille minimale : 4 + 2 + 32 (clé EdDSA) + 64 (signature EdDSA) = 102 octets - Taille maximale pratique : ~600 octets (clé éphémère RSA-4096 + signature RSA-4096)

**Compatible avec :** - LeaseSet2 (type 3) - EncryptedLeaseSet (type 5) - MetaLeaseSet (type 7)

**Voir aussi :** [Proposition 123](/proposals/123-new-netdb-entries/) pour le protocole de signature hors ligne détaillé.

---

### LeaseSet2Header (en-tête de LeaseSet2)

**Description:** Structure d'en-tête commune pour LeaseSet2 (format de leaseSet de nouvelle génération) (type 3) et MetaLeaseSet (variante « meta » de leaseSet) (type 7).

**Introduction:** Version 0.9.38 (voir [Proposition 123](/proposals/123-new-netdb-entries/))

**Format:**

```
+----+----+----+----+----+----+----+----+
| destination                           |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|     published     | expires |  flags  |
+----+----+----+----+----+----+----+----+
| offline_signature (optional)          |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

destination :: Destination
               Length: 387+ bytes

published :: 4-byte timestamp (seconds since epoch)
             Publication time of this LeaseSet
             Rolls over in year 2106

expires :: 2-byte offset (seconds)
           Offset from published timestamp
           Maximum: 65535 seconds (18.2 hours)

flags :: 2 bytes (bit flags)
         See flag definitions below

offline_signature :: OfflineSignature (optional)
                     Present only if flags bit 0 is set
                     Variable length
```
**Taille totale minimale:** 395 octets (sans signature hors ligne)

**Définitions des indicateurs (ordre des bits: 15 14 ... 3 2 1 0):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Bit</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Offline Keys</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0 = No offline keys, 1 = Offline signature present</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unpublished</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0 = Standard published, 1 = Unpublished (client-side only)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0 = Standard, 1 = Will be blinded when published</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3-15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Must be 0 for compatibility</td></tr>
  </tbody>
</table>
**Détails du drapeau:**

**Bit 0 - Clés hors ligne:** - `0`: Aucune signature hors ligne, utiliser la clé de signature de la Destination (identifiant public I2P) pour vérifier la signature du LeaseSet - `1`: La structure OfflineSignature (structure de signature hors ligne) suit le champ des indicateurs (flags)

**Bit 1 - Non publié:** - `0`: LeaseSet (ensemble de baux) standard publié, doit être propagé aux floodfills - `1`: LeaseSet non publié (côté client uniquement)   - NE DOIT PAS être propagé, publié, ni envoyé en réponse aux requêtes   - S'il est expiré, NE PAS interroger netdb pour un remplacement (sauf si le bit 2 est également défini)   - Utilisé pour des tunnels locaux ou des tests

**Bit 2 - Aveuglé (depuis 0.9.42):** - `0`: LeaseSet standard - `1`: Ce LeaseSet non chiffré sera aveuglé et chiffré lors de sa publication   - La version publiée sera EncryptedLeaseSet (type 5)   - S'il a expiré, interroger l'**emplacement aveuglé** dans netdb pour en obtenir un de remplacement   - Il faut aussi mettre le bit 1 à 1 (non publié + aveuglé)   - Utilisé pour les services cachés chiffrés

**Limites d'expiration:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">LeaseSet Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Maximum Expires Value</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Maximum Actual Time</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2 (type 3)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈660 seconds</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈11 minutes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MetaLeaseSet (type 7)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">65,535 seconds</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈18.2 hours</td></tr>
  </tbody>
</table>
**Exigences relatives à l’horodatage de publication :**

LeaseSet (type 1) ne comportait pas de champ published, ce qui nécessitait de rechercher, pour le versionnage, la date d'expiration de lease (entrée de tunnel à durée limitée) la plus proche. LeaseSet2 ajoute un horodatage `published` explicite avec une résolution d'une seconde.

**Note critique d'implémentation :** - Routers DOIVENT limiter le débit de publication des LeaseSet à **un rythme bien inférieur à une fois par seconde** par Destination (adresse I2P) - Si la publication est plus rapide, s'assurer que chaque nouveau LeaseSet possède un horodatage `published` au moins 1 seconde plus tard - Les Floodfills rejettent le LeaseSet si l'horodatage `published` n'est pas plus récent que la version actuelle - Intervalle minimal recommandé : 10-60 secondes entre les publications

**Exemples de calculs:**

**LeaseSet2 (11 minutes maximum):**

```
published = 1704067200 (2024-01-01 00:00:00 UTC)
expires = 660 (seconds)
Actual expiration = 1704067200 + 660 = 1704067860 (2024-01-01 00:11:00 UTC)
```
**MetaLeaseSet (maximum 18,2 heures):**

```
published = 1704067200 (2024-01-01 00:00:00 UTC)
expires = 65535 (seconds)
Actual expiration = 1704067200 + 65535 = 1704132735 (2024-01-01 18:12:15 UTC)
```
**Versionnage:** - LeaseSet est considéré comme « plus récent » si l’horodatage `published` est supérieur - Floodfills stockent et diffusent uniquement la version la plus récente - Attention lorsque le plus ancien Lease (composant d’un LeaseSet dans I2P) correspond au plus ancien Lease du LeaseSet précédent

---

### LeaseSet2 (Type 3)

**Description:** Format LeaseSet moderne avec plusieurs clés de chiffrement, des signatures hors ligne et des enregistrements de service. Norme actuelle pour les services cachés I2P.

**Introduction :** Version 0.9.38 (voir [Proposition 123](/proposals/123-new-netdb-entries/))

**Structure :**

```
+----+----+----+----+----+----+----+----+
|         ls2_header                    |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|          options                      |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|numk| keytype0| keylen0 |              |
+----+----+----+----+----+              +
|          encryption_key_0             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| keytypen| keylenn |                   |
+----+----+----+----+                   +
|          encryption_key_n             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| num| Lease2 0                         |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Lease2($num-1)                        |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

ls2header :: LeaseSet2Header
             Length: 395+ bytes (varies with offline signature)

options :: Mapping
           Key-value pairs for service records and metadata
           Length: 2+ bytes (size field + data)

numk :: Integer (1 byte)
        Number of encryption keys
        Range: 1 to (implementation-defined maximum, typically 8)

keytype :: 2-byte encryption type
           See PublicKey type table

keylen :: 2-byte key length
          Must match keytype specification

encryption_key :: PublicKey
                  Length: keylen bytes
                  Type: keytype

[Repeat keytype/keylen/encryption_key for each key]

num :: Integer (1 byte)
       Number of Lease2s
       Range: 1-16 (at least one required)

leases :: Array of Lease2 structures
          Length: $num × 40 bytes

signature :: Signature
             Length determined by signing key type
             Signed over entire structure including database type prefix
```
**Stockage de base de données:** - **Type de base de données:** 3 - **Clé:** hachage SHA-256 de la Destination - **Valeur:** Structure LeaseSet2 complète

**Calcul de la signature :**

```
Data to sign: database_type (1 byte, value=3) || complete LeaseSet2 data

Verification:
1. Prepend database type byte (0x03) to LeaseSet2 data
2. If offline signature present:
   - Verify offline signature against Destination key
   - Verify LeaseSet2 signature against transient key
3. Else:
   - Verify LeaseSet2 signature against Destination key
```
### Ordre de préférence des clés de chiffrement

**Pour un LeaseSet publié (serveur):** - Les clés sont listées par ordre de préférence du serveur (les plus préférées en premier) - Les clients prenant en charge plusieurs types DEVRAIENT respecter la préférence du serveur - Sélectionner le premier type pris en charge dans la liste - En général, les types de clés avec un numéro plus élevé (plus récents) sont plus sûrs/efficaces - Ordre recommandé : lister les clés dans l'ordre inverse du code de type (les plus récents d'abord)

**Exemple de préférence du serveur:**

```
numk = 2
Key 0: X25519 (type 4, 32 bytes)         [Most preferred]
Key 1: ElGamal (type 0, 256 bytes)       [Legacy compatibility]
```
**Pour un LeaseSet (client) non publié:** - L'ordre des clés importe peu en pratique (les connexions vers les clients sont rarement tentées) - Suivez la même convention par cohérence

**Sélection de la clé du client:** - Respecter la préférence du serveur (sélectionner le premier type pris en charge) - Ou utiliser une préférence définie par l’implémentation - Ou déterminer une préférence combinée en fonction des capacités des deux côtés

### Mappage des options

**Exigences:** - Les options DOIVENT être triées par clé (ordre lexicographique, ordre des octets UTF-8) - Le tri garantit l'invariance de la signature - Les clés en double NE sont PAS autorisées

**Format standard ([Proposition 167](/proposals/167-service-records/)):**

À partir de l’API 0.9.66 (juin 2025, version 2.9.0), les options de service record (enregistrement de service) suivent un format standardisé. Voir [Proposition 167](/proposals/167-service-records/) pour la spécification complète.

**Format de l'option d'enregistrement de service:**

```
Key: _service._proto
Value: record_type ttl [priority weight] port target [appoptions]

service :: Symbolic name of service (lowercase, [a-z0-9-])
           Examples: smtp, http, irc, mumble
           Use standard identifiers from IANA Service Name Registry
           or Linux /etc/services when available

proto :: Transport protocol (lowercase, [a-z0-9-])
         "tcp" = streaming protocol
         "udp" = repliable datagrams
         Protocol indicators for raw datagrams may be defined later

record_type :: "0" (self-reference) or "1" (SRV record)

ttl :: Time to live in seconds (positive integer)
       Recommended minimum: 86400 (one day)
       Prevents frequent re-queries

For record_type = 0 (self-reference):
  port :: I2CP port number (non-negative integer)
  appoptions :: Optional application-specific data (no spaces or commas)

For record_type = 1 (SRV record):
  priority :: Lower value = more preferred (non-negative integer)
  weight :: Relative weight for same priority, higher = more likely (non-negative)
  port :: I2CP port number (non-negative integer)
  target :: Hostname or b32 of destination (lowercase)
            Format: "example.i2p" or "aaaaa...aaaa.b32.i2p"
            Recommend b32 unless hostname is "well known"
  appoptions :: Optional application-specific data (no spaces or commas)
```
**Exemples d'enregistrements de service :**

**1. Serveur SMTP auto-référencé :**

```
Destination: aaaa...aaaa.b32.i2p (this LeaseSet)
Option: "_smtp._tcp" = "0 999999 25"

Meaning: This destination provides SMTP service on I2CP port 25
```
**2. Serveur SMTP externe unique:**

```
Destination: aaaa...aaaa.b32.i2p (this LeaseSet)
Option: "_smtp._tcp" = "1 86400 0 0 25 bbbb...bbbb.b32.i2p"

Meaning: SMTP service provided by bbbb...bbbb on port 25
         TTL = 1 day, single server (priority=0, weight=0)
```
**3. Plusieurs serveurs SMTP (répartition de charge):**

```
Destination: aaaa...aaaa.b32.i2p (this LeaseSet)
Option: "_smtp._tcp" = "1 86400 0 0 25 bbbb...bbbb.b32.i2p,1 86400 1 0 25 cccc...cccc.b32.i2p"

Meaning: Two SMTP servers
         bbbb...bbbb (priority=0, preferred)
         cccc...cccc (priority=1, backup)
```
**4. Service HTTP avec options de l'application:**

```
Option: "_http._tcp" = "0 86400 80 tls=1.3;cert=ed25519"

Meaning: HTTP on port 80 with TLS 1.3 and EdDSA certificates
```
**Recommandations TTL :** - Minimum : 86400 secondes (1 jour) - Un TTL plus long réduit la charge des requêtes netdb - Équilibre entre la réduction des requêtes et la propagation des mises à jour du service - Pour les services stables : 604800 (7 jours) ou plus

**Notes d'implémentation:**

1. **Clés de chiffrement (à partir de la version 0.9.44):**
   - ElGamal (type 0, 256 octets): Compatibilité avec les anciennes versions
   - X25519 (type 4, 32 octets): Standard actuel
   - Variantes MLKEM (Module-Lattice Key Encapsulation Mechanism, mécanisme d’encapsulation de clés à treillis modulaires): Post-quantique (bêta, non finalisées)

2. **Validation de la longueur de clé:**
   - Les Floodfills et les clients DOIVENT pouvoir analyser des types de clé inconnus
   - Utilisez le champ keylen pour ignorer les clés inconnues
   - Ne faites pas échouer l'analyse si le type de clé est inconnu

3. **Horodatage de publication :**
   - Voir les notes de LeaseSet2Header concernant la limitation du débit
   - Incrément minimal d’une seconde entre les publications
   - Recommandé : 10 à 60 secondes entre les publications

4. **Migration du type de chiffrement:**
   - La prise en charge de plusieurs clés permet une migration progressive
   - Répertoriez les anciennes et les nouvelles clés pendant la période de transition
   - Supprimez l'ancienne clé après une période suffisante de mise à niveau des clients

**JavaDoc:** [LeaseSet2](http://docs.i2p-projekt.de/javadoc/net/i2p/data/LeaseSet2.html)

---

### MetaLease (terme technique I2P sans équivalent établi)

**Description:** Structure de Lease pour MetaLeaseSet pouvant référencer d'autres LeaseSets plutôt que des tunnels. Utilisée pour l'équilibrage de charge et la redondance.

**Introduction:** Version 0.9.38, mise en service prévue pour 0.9.40 (voir [Proposition 123](/proposals/123-new-netdb-entries/))

**Format :**

```
+----+----+----+----+----+----+----+----+
| tunnel_gw                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|    flags     |cost|      end_date     |
+----+----+----+----+----+----+----+----+

tunnel_gw :: Hash (32 bytes)
             SHA-256 hash of:
             - Gateway RouterIdentity (for type 1), OR
             - Another MetaLeaseSet destination (for type 3/5/7)

flags :: 3 bytes
         Bit order: 23 22 ... 3 2 1 0
         Bits 3-0: Entry type (see table below)
         Bits 23-4: Reserved (must be 0)

cost :: 1 byte (0-255)
        Lower value = higher priority
        Used for load balancing

end_date :: 4-byte timestamp (seconds since epoch)
            Expiration time
            Rolls over in year 2106
```
**Taille totale:** 40 octets

**Type d'entrée (bits de drapeau 3-0):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Unknown</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unknown/invalid entry</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Points to LeaseSet (type 1, deprecated)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Points to LeaseSet2 (type 3)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Points to EncryptedLeaseSet (type 5)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">MetaLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align-center?">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Points to another MetaLeaseSet (type 7)</td></tr>
  </tbody>
</table>
**Scénarios d'utilisation :**

1. **Équilibrage de charge:**
   - MetaLeaseSet (collection méta de LeaseSet) avec plusieurs entrées MetaLease (entrées méta)
   - Chaque entrée pointe vers un LeaseSet2 différent
   - Les clients sélectionnent en fonction du champ de coût

2. **Redondance:**
   - Plusieurs entrées pointant vers des LeaseSets de secours
   - Repli si le LeaseSet principal est indisponible

3. **Migration du service:**
   - MetaLeaseSet pointe vers un nouveau LeaseSet
   - Permet une transition fluide entre les destinations

**Utilisation du champ Cost :** - Coût plus faible = priorité plus élevée - Coût 0 = priorité la plus élevée - Coût 255 = priorité la plus basse - Les clients DEVRAIENT préférer les entrées à coût plus faible - Les entrées de coût égal peuvent faire l'objet d'un équilibrage de charge aléatoire

**Comparaison avec Lease2 :**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Lease2</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">MetaLease</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Size</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Tunnel ID</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Replaced by flags (3 bytes) + cost (1 byte)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Points To</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Specific tunnel</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet or MetaLeaseSet</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Usage</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Direct tunnel reference</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Indirection/load balancing</td></tr>
  </tbody>
</table>
**JavaDoc:** [MetaLease](http://docs.i2p-projekt.de/javadoc/net/i2p/data/MetaLease.html)

---

### MetaLeaseSet (Type 7)

**Description:** Variante de LeaseSet qui contient des entrées MetaLease (entrées « méta »), fournissant une indirection vers d'autres LeaseSets. Utilisée pour la répartition de charge, la redondance et la migration de services.

**Introduction:** Défini en 0.9.38, prévu fonctionnel en 0.9.40 (voir [Proposition 123](/proposals/123-new-netdb-entries/))

**Statut:** Spécification complète. L'état du déploiement en production doit être vérifié avec les versions actuelles d'I2P.

**Structure:**

```
+----+----+----+----+----+----+----+----+
|         ls2_header                    |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|          options                      |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| num| MetaLease 0                      |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| MetaLease($num-1)                     |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|numr|                                  |
+----+                                  +
|          revocation_0                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|          revocation_n                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

ls2header :: LeaseSet2Header
             Length: 395+ bytes

options :: Mapping
           Length: 2+ bytes (size + data)
           MUST be sorted by key

num :: Integer (1 byte)
       Number of MetaLease entries
       Range: 1 to (implementation-defined, recommend 1-16)

metaleases :: Array of MetaLease structures
              Length: $num × 40 bytes

numr :: Integer (1 byte)
        Number of revocation hashes
        Range: 0 to (implementation-defined, recommend 0-16)

revocations :: Array of Hash structures
               Length: $numr × 32 bytes
               SHA-256 hashes of revoked LeaseSet Destinations
```
**Stockage de base de données:** - **Type de base de données:** 7 - **Clé:** hachage SHA-256 de Destination - **Valeur:** structure MetaLeaseSet complète

**Calcul de la signature :**

```
Data to sign: database_type (1 byte, value=7) || complete MetaLeaseSet data

Verification:
1. Prepend database type byte (0x07) to MetaLeaseSet data
2. If offline signature present in header:
   - Verify offline signature against Destination key
   - Verify MetaLeaseSet signature against transient key
3. Else:
   - Verify MetaLeaseSet signature against Destination key
```
**Scénarios d'utilisation:**

**1. Équilibrage de charge:**

```
MetaLeaseSet for primary.i2p:
  MetaLease 0: cost=0, points to server1.i2p LeaseSet2
  MetaLease 1: cost=0, points to server2.i2p LeaseSet2
  MetaLease 2: cost=0, points to server3.i2p LeaseSet2

Clients randomly select among equal-cost entries
```
**2. Basculement:**

```
MetaLeaseSet for service.i2p:
  MetaLease 0: cost=0, points to primary.i2p LeaseSet2
  MetaLease 1: cost=100, points to backup.i2p LeaseSet2

Clients prefer cost=0 (primary), fall back to cost=100 (backup)
```
**3. Migration du service:**

```
MetaLeaseSet for old-domain.i2p:
  MetaLease 0: cost=0, points to new-domain.i2p LeaseSet2

Transparently redirects clients from old to new destination
```
**4. Architecture multi-tiers:**

```
MetaLeaseSet for service.i2p:
  MetaLease 0: cost=0, points to region1-meta.i2p (another MetaLeaseSet)
  MetaLease 1: cost=0, points to region2-meta.i2p (another MetaLeaseSet)

Each region MetaLeaseSet points to regional servers
Allows hierarchical load balancing
```
**Liste de révocation :**

La liste de révocation permet à MetaLeaseSet de révoquer explicitement des LeaseSets publiés précédemment :

- **Objectif:** Marquer des Destinations spécifiques comme n'étant plus valides
- **Contenu:** Hachages SHA-256 des structures Destination révoquées
- **Utilisation:** Les clients NE DOIVENT PAS utiliser des LeaseSets dont le hachage de la Destination figure dans la liste de révocation
- **Valeur typique:** Vide (numr=0) dans la plupart des déploiements

**Exemple de révocation :**

```
Service migrates from dest-v1.i2p to dest-v2.i2p:
  MetaLease 0: points to dest-v2.i2p
  Revocations: [hash(dest-v1.i2p)]

Clients will use v2 and ignore v1 even if cached
```
**Gestion de l'expiration:**

MetaLeaseSet utilise LeaseSet2Header avec un expires maximal de 65535 secondes (~18,2 heures):

- Beaucoup plus long que LeaseSet2 (max. ~11 minutes)
- Adapté à une indirection relativement statique
- Les LeaseSets référencés peuvent avoir une expiration plus courte
- Les clients doivent vérifier l’expiration à la fois de MetaLeaseSet ET des LeaseSets référencés

**Correspondance des options:**

- Utiliser le même format que les options de LeaseSet2
- Peut inclure des enregistrements de service ([Proposal 167](/proposals/167-service-records/))
- DOIT être trié par clé
- Les enregistrements de service décrivent généralement le service final, pas la structure d’indirection

**Notes d’implémentation côté client :**

1. **Processus de résolution:**
   ```
   1. Query netdb for MetaLeaseSet using SHA-256(Destination)
   2. Parse MetaLeaseSet, extract MetaLease entries
   3. Sort entries by cost (lower = better)
   4. For each entry in cost order:
      a. Extract LeaseSet hash from tunnel_gw field
      b. Determine entry type from flags
      c. Query netdb for referenced LeaseSet (may be another MetaLeaseSet)
      d. Check revocation list
      e. Check expiration
      f. If valid, use the LeaseSet; else try next entry
   ```

2. **Mise en cache:**
   - Mettre en cache à la fois MetaLeaseSet (structure méta référençant des LeaseSets) et les LeaseSets référencés
   - Vérifier l’expiration des deux niveaux
   - Surveiller les mises à jour de la publication du MetaLeaseSet

3. **Basculement:**
   - Si l'entrée préférée échoue, essayer l'option au coût immédiatement supérieur
   - Envisager de marquer les entrées défaillantes comme temporairement indisponibles
   - Revérifier périodiquement pour détecter un rétablissement

**Statut de l’implémentation :**

[Proposition 123](/proposals/123-new-netdb-entries/) indique que certaines parties restent "en cours de développement." Les implémenteurs devraient: - Vérifier l'état de préparation à la mise en production dans la version I2P cible - Tester la prise en charge de MetaLeaseSet (type de leaseSet I2P) avant le déploiement - Vérifier l'existence de spécifications mises à jour dans les versions plus récentes d'I2P

**JavaDoc:** [MetaLeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/MetaLeaseSet.html)

---

### EncryptedLeaseSet (Type 5)

**Description :** LeaseSet chiffré et aveuglé pour une confidentialité renforcée. Seules la clé publique aveuglée et les métadonnées sont visibles ; les leases (références temporaires vers des tunnels) et les clés de chiffrement sont chiffrés.

**Introduction:** Défini en 0.9.38, fonctionnel en 0.9.39 (voir [Proposition 123](/proposals/123-new-netdb-entries/))

**Structure :**

```
+----+----+----+----+----+----+----+----+
| sigtype |                             |
+----+----+                             +
|        blinded_public_key             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|     published     | expires |  flags  |
+----+----+----+----+----+----+----+----+
| offline_signature (optional)          |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|  len    |                             |
+----+----+                             +
|         encrypted_data                |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| signature                             |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

sigtype :: 2-byte signature type
           Type of blinded_public_key
           MUST be RedDSA_SHA512_Ed25519 (type 11)

blinded_public_key :: SigningPublicKey (32 bytes for RedDSA)
                      Blinded version of Destination signing key
                      Used to verify signature on EncryptedLeaseSet

published :: 4-byte timestamp (seconds since epoch)
             Publication time
             Rolls over in year 2106

expires :: 2-byte offset (seconds)
           Offset from published
           Maximum: 65535 seconds (18.2 hours)
           Practical maximum for LeaseSet data: ~660 seconds (~11 min)

flags :: 2 bytes
         Bit 0: Offline signature present (0=no, 1=yes)
         Bit 1: Unpublished (0=published, 1=client-side only)
         Bits 15-2: Reserved (must be 0)

offline_signature :: OfflineSignature (optional)
                     Present only if flags bit 0 = 1
                     Variable length

len :: 2-byte integer
       Length of encrypted_data
       Range: 1 to 65535

encrypted_data :: Encrypted payload
                  Length: len bytes
                  Contains encrypted LeaseSet2 or MetaLeaseSet

signature :: Signature (64 bytes for RedDSA)
             Length determined by sigtype
             Signed by blinded_public_key or transient key
```
**Stockage de la base de données :** - **Type de base de données :** 5 - **Clé :** hachage SHA-256 de la **Destination aveuglée** (et non la Destination d'origine) - **Valeur :** structure EncryptedLeaseSet complète

**Différences essentielles par rapport à LeaseSet2:**

1. **N'utilise PAS la structure LeaseSet2Header** (présente des champs similaires mais une disposition différente)
2. **Clé publique aveuglée** au lieu de la Destination (identifiant d'adresse I2P) complète
3. **Charge utile chiffrée** au lieu de baux et de clés en clair
4. **La clé de base de données est le hachage de la Destination aveuglée**, pas de la Destination d'origine

**Calcul de la signature:**

```
Data to sign: database_type (1 byte, value=5) || complete EncryptedLeaseSet data

Verification:
1. Prepend database type byte (0x05) to EncryptedLeaseSet data
2. If offline signature present (flags bit 0 = 1):
   - Verify offline signature against blinded public key
   - Verify EncryptedLeaseSet signature against transient key
3. Else:
   - Verify EncryptedLeaseSet signature against blinded public key
```
**Exigence relative au type de signature :**

**DOIT utiliser RedDSA_SHA512_Ed25519 (type 11) :** - Clés publiques aveuglées de 32 octets - Signatures de 64 octets - Requis pour les propriétés de sécurité de l’aveuglement - Voir [Spécification Red25519](//docs/specs/red25519-signature-scheme/

**Principales différences par rapport à EdDSA :** - Clés privées par réduction modulaire (pas de clamping, ajustement des bits de la clé privée) - Les signatures incluent 80 octets de données aléatoires - Utilise les clés publiques directement (pas de hachages) - Permet une opération d'aveuglement sécurisée

**Aveuglement et chiffrement:**

Voir la [spécification EncryptedLeaseSet](/docs/specs/encryptedleaseset/) pour des détails complets :

**1. Aveuglement de clé:**

```
Blinding process (daily rotation):
  secret = HKDF(original_signing_private_key, date_string, "i2pblinding1")
  alpha = SHA-256(secret) mod L (where L is Ed25519 group order)
  blinded_private_key = alpha * original_private_key
  blinded_public_key = alpha * original_public_key
```
**2. Emplacement de la base de données :**

```
Client publishes to:
  Key = SHA-256(blinded_destination)
  
Where blinded_destination uses:
  - Blinded public key (signing key)
  - Same unused public key field (random)
  - Same certificate structure
```
**3. Couches de chiffrement (à trois couches):**

**Couche 1 - Couche d’authentification (accès client):** - Chiffrement : chiffre en flux ChaCha20 - Dérivation de clé : HKDF avec des secrets propres à chaque client - Les clients authentifiés peuvent déchiffrer la couche externe

**Couche 2 - Couche de chiffrement:** - Chiffrement: ChaCha20 - Clé: dérivée de DH (Diffie-Hellman) entre le client et le serveur - Contient le LeaseSet2 ou MetaLeaseSet effectif

**Couche 3 - LeaseSet interne:** - LeaseSet2 ou MetaLeaseSet complet - Inclut tous les tunnels, les clés de chiffrement, les options - Accessible uniquement après un déchiffrement réussi

**Dérivation de clé de chiffrement:**

```
Client has: ephemeral_client_private_key
Server has: ephemeral_server_public_key (in encrypted_data)

Shared secret = X25519(client_private, server_public)
Encryption key = HKDF(shared_secret, context_info, "i2pblinding2")
```
**Processus de découverte:**

**Pour les clients autorisés :**

```
1. Client knows original Destination
2. Client computes current blinded Destination (based on current date)
3. Client computes database key: SHA-256(blinded_destination)
4. Client queries netdb for EncryptedLeaseSet using blinded key
5. Client decrypts layer 1 using authorization credentials
6. Client decrypts layer 2 using DH shared secret
7. Client extracts inner LeaseSet2/MetaLeaseSet
8. Client uses tunnels from inner LeaseSet for communication
```
**Pour les clients non autorisés :** - Ne peuvent pas déchiffrer même s'ils trouvent l'EncryptedLeaseSet - Ne peuvent pas déterminer la Destination d'origine à partir de la version aveuglée - Ne peuvent pas relier les EncryptedLeaseSets entre différentes périodes d'aveuglement (rotation quotidienne)

**Délais d'expiration:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Content Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Maximum Expires</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet (outer)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">65,535 sec (≈18.2 hr)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Full 2-byte expires field</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Inner LeaseSet2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈660 sec (≈11 min)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Actual lease data practical maximum</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Inner MetaLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">65,535 sec (≈18.2 hr)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Indirection can be longer-lived</td></tr>
  </tbody>
</table>
**Horodatage de publication:**

Mêmes exigences que pour LeaseSet2Header : - Doit s'incrémenter d'au moins 1 seconde entre les publications - Les floodfills rejettent s'il n'est pas plus récent que la version actuelle - Recommandé : 10-60 secondes entre les publications

**Signatures hors ligne avec des LeaseSets chiffrés:**

Considérations particulières lors de l'utilisation des signatures hors ligne: - La clé publique aveuglée est renouvelée quotidiennement - La signature hors ligne doit être régénérée quotidiennement avec la nouvelle clé aveuglée - OU utiliser la signature hors ligne sur le LeaseSet interne, pas sur l'EncryptedLeaseSet (LeaseSet chiffré) externe - Voir les notes de [Proposal 123](/proposals/123-new-netdb-entries/)

**Notes d'implémentation:**

1. **Autorisation des clients:**
   - Plusieurs clients peuvent être autorisés avec des clés différentes
   - Chaque client autorisé possède des identifiants de déchiffrement uniques
   - Révoquer un client en modifiant les clés d'autorisation

2. **Rotation quotidienne des clés:**
   - Les clés blinded (masquées) changent à minuit UTC
   - Les clients doivent recalculer la Destination blinded chaque jour
   - Les anciens EncryptedLeaseSets deviennent introuvables après la rotation

3. **Propriétés de confidentialité:**
   - Les Floodfills ne peuvent pas déterminer la destination d'origine
   - Les clients non autorisés ne peuvent pas accéder au service
   - Différentes périodes de blinding (périodes de masquage cryptographique) ne peuvent pas être liées
   - Aucune métadonnée en clair au-delà des dates d'expiration

4. **Performances:**
   - Les clients doivent effectuer un calcul d’aveuglement quotidien
   - Le chiffrement en trois couches ajoute une surcharge de calcul
   - Envisager la mise en cache du LeaseSet interne déchiffré

**Considérations de sécurité :**

1. **Gestion des clés d’autorisation :**
   - Distribuer en toute sécurité les identifiants d’autorisation des clients
   - Utiliser des identifiants uniques par client pour une révocation granulaire
   - Renouveler périodiquement les clés d’autorisation

2. **Synchronisation de l’horloge:**
   - L’aveuglement quotidien dépend de dates UTC synchronisées
   - Un décalage de l’horloge peut provoquer des échecs de recherche
   - Envisagez de prendre en charge l’aveuglement du jour précédent/suivant pour plus de tolérance

3. **Fuite de métadonnées:**
   - Les champs Published et expires sont en clair
   - L'analyse des motifs pourrait révéler des caractéristiques du service
   - Rendez aléatoires les intervalles de publication si cela vous préoccupe

**JavaDoc:** [EncryptedLeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/EncryptedLeaseSet.html)

---

## Structures du Router (nœud I2P)

### RouterAddress (adresse du router)

**Description:** Définit les informations de connexion pour un router via un protocole de transport spécifique.

**Format:**

```
+----+----+----+----+----+----+----+----+
|cost|           expiration
+----+----+----+----+----+----+----+----+
     |        transport_style           |
+----+----+----+----+-//-+----+----+----+
|                                       |
+                                       +
|               options                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

cost :: Integer (1 byte)
        Relative cost, 0=free, 255=expensive
        Typical values:
          5-6: SSU2
          10-11: NTCP2

expiration :: Date (8 bytes)
              MUST BE ALL ZEROS (see critical note below)

transport_style :: String (1-256 bytes)
                   Transport protocol name
                   Current values: "SSU2", "NTCP2"
                   Legacy: "SSU", "NTCP" (removed)

options :: Mapping
           Transport-specific configuration
           Common options: "host", "port"
           Transport-specific options vary
```
**CRITIQUE - Champ d'expiration:**

⚠️ **Le champ d'expiration DOIT être défini entièrement à zéro (8 octets nuls).**

- **Raison:** Depuis la version 0.9.3, une expiration non nulle entraîne un échec de la vérification de la signature
- **Historique:** L'expiration n'était à l'origine pas utilisée, toujours null
- **Statut actuel:** Le champ a de nouveau été reconnu à partir de la version 0.9.12, mais doit attendre une mise à niveau du réseau
- **Implémentation:** Toujours défini à 0x0000000000000000

Toute valeur d'expiration non nulle fera échouer la validation de la signature de RouterInfo (informations du router).

### Protocoles de transport

**Protocoles actuels (à la version 2.10.0):**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Introduced</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Removed</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>SSU2</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.54 (May 2022)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Default since 0.9.56</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>NTCP2</strong></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.36 (Aug 2018)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.50 (May 2021)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Use NTCP2</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2.4.0 (Dec 2023)</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Use SSU2</td></tr>
  </tbody>
</table>
**Valeurs de style de transport :** - `"SSU2"`: Transport actuel basé sur UDP - `"NTCP2"`: Transport actuel basé sur TCP - `"NTCP"`: Ancien, supprimé (ne pas utiliser) - `"SSU"`: Ancien, supprimé (ne pas utiliser)

### Options communes

Tous les transports incluent généralement:

```
"host" = IPv4 or IPv6 address or hostname
"port" = Port number (1-65535)
```
### Options spécifiques à SSU2

Voir la [spécification SSU2](/docs/specs/ssu2/) pour tous les détails.

**Options obligatoires:**

```
"host" = IP address (IPv4 or IPv6)
"port" = UDP port number
"s" = Static X25519 public key (Base64, 44 characters = 32 bytes)
"i" = Introduction key X25519 (Base64, 44 characters = 32 bytes)
"v" = "2" (protocol version)
```
**Options facultatives :**

```
"caps" = Capability string (e.g., "B" for bandwidth tier)
"ihost0", "ihost1", ... = Introducer IP addresses
"iport0", "iport1", ... = Introducer ports  
"ikey0", "ikey1", ... = Introducer static keys (Base64, 44 chars)
"itag0", "itag1", ... = Introducer relay tags
"iexp0", "iexp1", ... = Introducer expiration timestamps
"mtu" = Maximum transmission unit (default 1500, min 1280)
"mtu6" = IPv6 MTU (if different from IPv4)
```
**Exemple de SSU2 RouterAddress (adresse du router):**

```
cost: 5
expiration: 0x0000000000000000
transport_style: "SSU2"
options:
  host=198.51.100.42
  port=12345
  s=SGVsbG8gV29ybGQhIFRoaXMgaXMgYSBzYW1wbGUga2V5IQ==
  i=QW5vdGhlciBTYW1wbGUgS2V5IGZvciBJbnRyb2R1Y3Rpb24=
  v=2
  caps=BC
  mtu=1472
```
### Options spécifiques à NTCP2

Voir la [spécification NTCP2](/docs/specs/ntcp2/) pour tous les détails.

**Options requises :**

```
"host" = IP address (IPv4 or IPv6)
"port" = TCP port number
"s" = Static X25519 public key (Base64, 44 characters = 32 bytes)
"i" = Initialization vector (Base64, 24 characters = 16 bytes)
"v" = "2" (protocol version)
```
**Options facultatives (depuis 0.9.50):**

```
"caps" = Capability string
```
**Exemple de NTCP2 RouterAddress (adresse du router) :**

```
cost: 10
expiration: 0x0000000000000000
transport_style: "NTCP2"
options:
  host=198.51.100.42
  port=23456
  s=SGVsbG8gV29ybGQhIFRoaXMgaXMgYSBzYW1wbGUga2V5IQ==
  i=U2FtcGxlIElWIGhlcmU=
  v=2
```
### Notes d'implémentation

1. **Valeurs de coût:**
   - UDP (SSU2) généralement à coût plus faible (5-6) grâce à son efficacité
   - TCP (NTCP2) généralement à coût plus élevé (10-11) en raison de la surcharge
   - Coût plus faible = transport préféré

2. **Adresses multiples :**
   - Les routers peuvent publier plusieurs entrées RouterAddress
   - Transports différents (SSU2 et NTCP2)
   - Différentes versions IP (IPv4 et IPv6)
   - Les clients sélectionnent en fonction du coût et des capacités

3. **Nom d'hôte vs IP :**
   - Les adresses IP sont à privilégier pour les performances
   - Les noms d'hôte sont pris en charge mais ajoutent une surcharge de résolution DNS
   - Envisagez d'utiliser des adresses IP pour les RouterInfos (descripteurs de routeur I2P) publiés

4. **Encodage Base64:**
   - Toutes les clés et les données binaires sont encodées en Base64
   - Base64 standard (RFC 4648)
   - Pas de remplissage ni de caractères non standard

**JavaDoc:** [RouterAddress](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterAddress.html)

---

### RouterInfo

**Description:** Ensemble complet d’informations publiées sur un router, stocké dans la base de données réseau (netDb). Il comprend l’identité, les adresses et les capacités.

**Format:**

```
+----+----+----+----+----+----+----+----+
| router_ident                          |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| published                             |
+----+----+----+----+----+----+----+----+
|size| RouterAddress 0                  |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| RouterAddress 1                       |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| RouterAddress ($size-1)               |
+                                       +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+-//-+----+----+----+
|psiz| options                          |
+----+----+----+----+-//-+----+----+----+
| signature                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

router_ident :: RouterIdentity
                Length: 387+ bytes (typically 391 for X25519+EdDSA)

published :: Date (8 bytes)
             Publication timestamp (milliseconds since epoch)

size :: Integer (1 byte)
        Number of RouterAddress entries
        Range: 0-255

addresses :: Array of RouterAddress
             Variable length
             Each RouterAddress has variable size

peer_size :: Integer (1 byte)
             Number of peer hashes (ALWAYS 0)
             Historical, unused feature

options :: Mapping
           Router capabilities and metadata
           MUST be sorted by key

signature :: Signature
             Length determined by router_ident signing key type
             Typically 64 bytes (EdDSA)
             Signed by router_ident's SigningPrivateKey
```
**Stockage de la base de données:** - **Type de base de données:** 0 - **Clé:** hachage SHA-256 de RouterIdentity (identité du router) - **Valeur:** structure RouterInfo (informations du router) complète

**Horodatage de publication:** - Date sur 8 octets (millisecondes depuis l'époque Unix) - Utilisé pour la gestion des versions de RouterInfo - Les Routers publient périodiquement un nouveau RouterInfo - Les Floodfills conservent la version la plus récente en se basant sur l'horodatage de publication

**Tri des adresses:** - **Historique:** Des routers très anciens exigeaient que les adresses soient triées selon le SHA-256 de leurs données - **Actuel:** Le tri n'est PAS requis, cela ne vaut pas la peine de l'implémenter pour des raisons de compatibilité - Les adresses peuvent être dans n'importe quel ordre

**Champ de taille des pairs (historique):** - **Toujours 0** dans I2P moderne - Était destiné aux routes restreintes (non implémenté) - S'il était implémenté, il serait suivi d'autant de Router Hashes (hachages du router) - Certaines anciennes implémentations pouvaient exiger une liste de pairs triée

**Mappage des options :**

Les options DOIVENT être triées par clé. Les options standard comprennent :

**Options de capacités:**

```
"caps" = Capability string
         Common values:
           f = Floodfill (network database)
           L or M or N or O = Bandwidth tier (L=lowest, O=highest)
           R = Reachable
           U = Unreachable/firewalled
           Example: "fLRU" = Floodfill, Low bandwidth, Reachable, Unreachable
```
**Options réseau:**

```
"netId" = Network ID (default "2" for main I2P network)
          Different values for test networks

"router.version" = I2P version string
                   Example: "0.9.67" or "2.10.0"
```
**Options statistiques:**

```
"stat_uptime" = Uptime in milliseconds
"coreVersion" = Core I2P version
"router.version" = Full router version string
```
Voir la [documentation RouterInfo de la base de données du réseau (informations sur le router)](/docs/specs/common-structures/#routerInfo) pour la liste complète des options standard.

**Calcul de la signature:**

```
Data to sign: Complete RouterInfo structure from router_ident through options

Verification:
1. Extract RouterIdentity from RouterInfo
2. Get SigningPublicKey from RouterIdentity (type determines algorithm)
3. Verify signature over all data preceding signature field
4. Signature must match signing key type and length
```
**RouterInfo moderne typique (enregistrement d'informations du router) :**

```
RouterIdentity: 391 bytes (X25519+EdDSA with Key Certificate)
Published: 8 bytes
Size: 1 byte (typically 1-4 addresses)
RouterAddress × N: Variable (typically 200-500 bytes each)
Peer Size: 1 byte (value=0)
Options: Variable (typically 50-200 bytes)
Signature: 64 bytes (EdDSA)

Total: ~1000-2500 bytes typical
```
**Notes d’implémentation:**

1. **Plusieurs adresses:**
   - Les routers publient généralement 1 à 4 adresses
   - Variantes IPv4 et IPv6
   - Transports SSU2 et/ou NTCP2
   - Chaque adresse est indépendante

2. **Versionnage:**
   - Un RouterInfo (fiche d’information du router) plus récent a un horodatage `published` plus tardif
   - Les routers republient toutes les ~2 heures ou lorsque les adresses changent
   - Les floodfills stockent et diffusent uniquement la version la plus récente

3. **Validation:**
   - Vérifier la signature avant d'accepter RouterInfo
   - Vérifier que le champ d'expiration est entièrement à zéro dans chaque RouterAddress
   - Valider que le mappage des options est trié par clé
   - Vérifier que les types de certificats et de clés sont connus/pris en charge

4. **Base de données réseau:**
   - Les floodfills stockent des RouterInfo indexés par Hash(RouterIdentity)
   - Conservés pendant ~2 jours après la dernière publication
   - Les routers interrogent les floodfills pour découvrir d'autres routers

**JavaDoc:** [RouterInfo](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterInfo.html)

---

## Notes d'implémentation

### Ordre des octets (Endianness)

**Par défaut: Big-Endian (ordre des octets du réseau)**

La plupart des structures I2P utilisent l’ordre des octets big-endian: - Tous les types d’entiers (1-8 octets) - Horodatages de date - TunnelId - Préfixe de longueur de chaîne - Types et longueurs de certificat - Codes de type de clé - Champs de taille de mappage

**Exception : Little-Endian (ordre d'octets où l'octet le moins significatif est stocké en premier)**

Les types de clés suivants utilisent l'encodage **little-endian** : - **X25519** clés de chiffrement (type 4) - **EdDSA_SHA512_Ed25519** clés de signature (type 7) - **EdDSA_SHA512_Ed25519ph** clés de signature (type 8) - **RedDSA_SHA512_Ed25519** clés de signature (type 11)

**Implémentation:**

```java
// Big-endian (most structures)
int value = ((bytes[0] & 0xFF) << 24) | 
            ((bytes[1] & 0xFF) << 16) |
            ((bytes[2] & 0xFF) << 8) | 
            (bytes[3] & 0xFF);

// Little-endian (X25519, EdDSA, RedDSA)
int value = (bytes[0] & 0xFF) | 
            ((bytes[1] & 0xFF) << 8) |
            ((bytes[2] & 0xFF) << 16) | 
            ((bytes[3] & 0xFF) << 24);
```
### Versionnage des structures

**Ne partez jamais du principe que les tailles sont fixes :**

De nombreuses structures ont une longueur variable: - RouterIdentity (identité du router I2P): 387+ octets (pas toujours 387) - Destination (identifiant de destination I2P): 387+ octets (pas toujours 387) - LeaseSet2 (version 2 de LeaseSet): Varie considérablement - Certificate (structure de certificat): 3+ octets

**Toujours lire les champs de taille :** - Longueur du certificat aux octets 1-2 - Taille du mappage au début - KeysAndCert est toujours calculé comme 384 + 3 + certificate_length

**Vérifier la présence de données superflues:** - Interdire les données parasites après des structures valides - Vérifier que les longueurs des certificats correspondent aux types de clés - Imposer les longueurs exactement attendues pour les types à taille fixe

### Recommandations actuelles (octobre 2025)

**Pour les nouvelles identités de Router:**

```
Encryption: X25519 (type 4, 32 bytes)
Signing: EdDSA_SHA512_Ed25519 (type 7, 32 bytes)
Certificate: Key Certificate (type 5)
Total Size: 391 bytes
Padding: Compressible per [Proposal 161](/fr/proposals/161-ri-dest-padding/)
```
**Pour de nouvelles destinations :**

```
Unused Public Key Field: 256 bytes random (compressible)
Signing: EdDSA_SHA512_Ed25519 (type 7, 32 bytes)
Certificate: Key Certificate (type 5)
Total Size: 391 bytes
Padding: Compressible per [Proposal 161](/fr/proposals/161-ri-dest-padding/)
```
**Pour les nouveaux LeaseSets:**

```
Type: LeaseSet2 (type 3)
Encryption Keys: X25519 (type 4, 32 bytes)
Leases: At least 1, typically 3-5
Options: Include service records per [Proposal 167](/proposals/167-service-records/)
Signature: EdDSA (64 bytes)
```
**Pour les services chiffrés:**

```
Type: EncryptedLeaseSet (type 5)
Blinding: RedDSA_SHA512_Ed25519 (type 11)
Inner LeaseSet: LeaseSet2 (type 3)
Rotation: Daily blinding key rotation
Authorization: Per-client encryption keys
```
### Fonctionnalités obsolètes - Ne pas utiliser

**Chiffrement déprécié:** - ElGamal (type 0) pour Router Identities (déprécié depuis 0.9.58) - chiffrement ElGamal/AES+SessionTag (utilisez ECIES-X25519)

**Signatures dépréciées:** - DSA_SHA1 (type 0) pour les Identités de Router (déprécié depuis 0.9.58) - variantes ECDSA (types 1-3) pour les nouvelles implémentations - variantes RSA (types 4-6) sauf pour les fichiers SU3

**Formats réseau obsolètes :** - LeaseSet (ensemble de baux dans I2P) type 1 (utiliser LeaseSet2) - Lease (44 octets, utiliser Lease2) - Format d'expiration de Lease d'origine

**Transports obsolètes:** - NTCP (supprimé en 0.9.50) - SSU (supprimé en 2.4.0)

**Certificats obsolètes:** - HASHCASH (type 1) - HIDDEN (type 2) - SIGNED (type 3) - MULTIPLE (type 4)

### Considérations de sécurité

**Génération de clés:** - Toujours utiliser des générateurs de nombres aléatoires cryptographiquement sûrs - Ne jamais réutiliser des clés dans des contextes différents - Protéger les clés privées avec des contrôles d'accès appropriés - Effacer en toute sécurité le matériau de clé de la mémoire une fois l'opération terminée

**Vérification des signatures:** - Toujours vérifier les signatures avant de faire confiance aux données - Vérifier que la longueur de la signature correspond au type de clé - S'assurer que les données signées contiennent les champs attendus - Pour les mappages triés, vérifier l'ordre de tri avant de signer/vérifier

**Validation des horodatages:** - Vérifier que les horodatages de publication sont raisonnables (pas dans un futur lointain) - Valider que les dates d’expiration des leases (entrée de tunnel dans un leaseSet) ne sont pas échues - Prendre en compte la tolérance au décalage d’horloge (±30 secondes typique)

**Base de données réseau:** - Valider toutes les structures avant leur stockage - Imposer des limites de taille pour prévenir les attaques par déni de service (DoS) - Limiter la fréquence des requêtes et des publications - Vérifier que les clés de la base de données correspondent aux hachages des structures

### Notes de compatibilité

**Rétrocompatibilité:** - ElGamal et DSA_SHA1 toujours pris en charge pour les routers historiques - Les types de clés dépréciés restent fonctionnels mais sont déconseillés - Bourrage compressible ([Proposal 161](/fr/proposals/161-ri-dest-padding/)) rétrocompatible jusqu'à la version 0.6

**Compatibilité ascendante :** - Les types de clés inconnus peuvent être analysés à l'aide des champs de longueur - Les types de certificats inconnus peuvent être ignorés à l'aide du champ de longueur - Les types de signatures inconnus doivent être gérés de manière robuste - Les implémenteurs ne doivent pas échouer en présence de fonctionnalités optionnelles inconnues

**Stratégies de migration:** - Prendre en charge à la fois les anciens et les nouveaux types de clés pendant la transition - LeaseSet2 (LeaseSet de 2e génération) peut répertorier plusieurs clés de chiffrement - Les signatures hors ligne permettent une rotation sécurisée des clés - MetaLeaseSet (format de LeaseSet pour la migration) permet une migration transparente du service

### Tests et validation

**Validation de la structure:** - Vérifier que tous les champs de longueur se situent dans les plages attendues - Vérifier que les structures à longueur variable sont analysées correctement - Valider que la vérification des signatures réussit - Tester avec des structures de taille minimale et maximale

**Cas limites :** - Chaînes de longueur nulle - Mappages vides - Nombre minimal et maximal de leases (entrées de tunnel I2P) - Certificat avec une charge utile de longueur nulle - Structures très volumineuses (proches des tailles maximales)

**Interopérabilité:** - Tester par rapport à l'implémentation Java officielle d'I2P - Vérifier la compatibilité avec i2pd - Tester avec divers contenus de la base de données réseau (netDb) - Valider à l'aide de vecteurs de test réputés corrects

---

## Références

### Spécifications

- [Protocole I2NP](/docs/specs/i2np/)
- [Protocole I2CP](/docs/specs/i2cp/)
- [Transport SSU2](/docs/specs/ssu2/)
- [Transport NTCP2](/docs/specs/ntcp2/)
- [Protocole de tunnel](/docs/specs/implementation/)
- [Protocole de datagrammes](/docs/api/datagrams/)

### Cryptographie

- [Vue d’ensemble de la cryptographie](/docs/specs/cryptography/)
- [Chiffrement ElGamal/AES](/docs/legacy/elgamal-aes/)
- [Chiffrement ECIES-X25519](/docs/specs/ecies/)
- [ECIES pour les routers](/docs/specs/ecies/#routers)
- [ECIES hybride (post-quantique)](/docs/specs/ecies/#hybrid)
- [Signatures Red25519](/docs/specs/red25519-signature-scheme/)
- [LeaseSet chiffré](/docs/specs/encryptedleaseset/)

### Propositions

- [Proposition 123: Nouvelles entrées netDB](/proposals/123-new-netdb-entries/)
- [Proposition 134: Types de signature GOST](/proposals/134-gost/)
- [Proposition 136: Types de signature expérimentaux](/proposals/136-experimental-sigtypes/)
- [Proposition 145: ECIES-P256](/proposals/145-ecies/)
- [Proposition 156: ECIES Routers](/proposals/156-ecies-routers/)
- [Proposition 161: Génération du bourrage](/fr/proposals/161-ri-dest-padding/)
- [Proposition 167: Enregistrements de service](/proposals/167-service-records/)
- [Proposition 169: Cryptographie post-quantique](/proposals/169-pq-crypto/)
- [Index de toutes les propositions](/proposals/)

### Base de données réseau

- [Aperçu de la base de données réseau](/docs/specs/common-structures/)
- [Options standard de RouterInfo](/docs/specs/common-structures/#routerInfo)

### Référence de l'API JavaDoc

- [Package de données cœur](http://docs.i2p-projekt.de/javadoc/net/i2p/data/)
- [PublicKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/PublicKey.html)
- [PrivateKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/PrivateKey.html)
- [SessionKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SessionKey.html)
- [SigningPublicKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SigningPublicKey.html)
- [SigningPrivateKey](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SigningPrivateKey.html)
- [Signature](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Signature.html)
- [Hash](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Hash.html)
- [SessionTag](http://docs.i2p-projekt.de/javadoc/net/i2p/data/SessionTag.html)
- [TunnelId](http://docs.i2p-projekt.de/javadoc/net/i2p/data/TunnelId.html)
- [Certificate](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Certificate.html)
- [DataHelper](http://docs.i2p-projekt.de/javadoc/net/i2p/data/DataHelper.html)
- [KeysAndCert](http://docs.i2p-projekt.de/javadoc/net/i2p/data/KeysAndCert.html)
- [RouterIdentity](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterIdentity.html)
- [Destination](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Destination.html)
- [Lease](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Lease.html)
- [LeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/LeaseSet.html)
- [Lease2](http://docs.i2p-projekt.de/javadoc/net/i2p/data/Lease2.html)
- [LeaseSet2](http://docs.i2p-projekt.de/javadoc/net/i2p/data/LeaseSet2.html)
- [MetaLease](http://docs.i2p-projekt.de/javadoc/net/i2p/data/MetaLease.html)
- [MetaLeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/MetaLeaseSet.html)
- [EncryptedLeaseSet](http://docs.i2p-projekt.de/javadoc/net/i2p/data/EncryptedLeaseSet.html)
- [RouterAddress](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterAddress.html)
- [RouterInfo](http://docs.i2p-projekt.de/javadoc/net/i2p/data/router/RouterInfo.html)

### Normes externes

- **RFC 7748 (X25519):** Courbes elliptiques pour la sécurité
- **RFC 7539 (ChaCha20):** ChaCha20 et Poly1305 pour les protocoles de l'IETF
- **RFC 4648 (Base64):** Les encodages de données Base16, Base32 et Base64
- **FIPS 180-4 (SHA-256):** Norme de hachage sécurisé
- **FIPS 204 (ML-DSA):** Norme de signature numérique basée sur des réseaux modulaires (module-lattice)
- [Registre des services de l'IANA](http://www.dns-sd.org/ServiceTypes.html)

### Ressources de la communauté

- [Site Web I2P](/)
- [Forum I2P](https://i2pforum.net)
- [GitLab d'I2P](https://i2pgit.org/I2P_Developers/i2p.i2p)
- [Miroir GitHub d'I2P](https://github.com/i2p/i2p.i2p)
- [Index de la documentation technique](/docs/)

### Informations sur la version

- [Annonce de la version 2.10.0 d’I2P](/fr/blog/2025/09/08/i2p-2.10.0-release/)
- [Historique des versions](https://github.com/i2p/i2p.i2p/blob/master/history.txt)
- [Journal des modifications](https://github.com/i2p/i2p.i2p/blob/master/debian/changelog)

---

## Annexe : tableaux de référence rapide

### Référence rapide des types de clés

**Standard actuel (recommandé pour toutes les nouvelles implémentations):** - **Chiffrement:** X25519 (type 4, 32 octets, little-endian (ordre des octets du moins significatif au plus significatif)) - **Signature:** EdDSA_SHA512_Ed25519 (type 7, 32 octets, little-endian)

**Ancien (pris en charge mais obsolète):** - **Chiffrement:** ElGamal (type 0, 256 octets, big-endian (ordre des octets du plus significatif au moins significatif)) - **Signature:** DSA_SHA1 (type 0, 20 octets pour la clé privée / 128 octets pour la clé publique, big-endian)

**Spécialisé:** - **Signature (LeaseSet chiffré):** RedDSA_SHA512_Ed25519 (type 11, 32 octets, little-endian (ordre petit-boutiste))

**Post-quantique (bêta, non finalisé):** - **Chiffrement hybride:** variantes MLKEM_X25519 (types 5-7) - **Chiffrement post-quantique pur:** variantes MLKEM (pas encore de codes de type attribués)

### Référence rapide des tailles de structures

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Structure</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Minimum Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Typical Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Maximum Size</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Integer</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Date</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">8 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">String</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1 byte</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td><td style="border:1px solid var(--color-border); padding:0.5rem;">256 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SessionKey</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Hash</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">32 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelId</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Certificate</td><td style="border:1px solid var(--color-border); padding:0.5rem;">3 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">7 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">65,538 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">KeysAndCert</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">391 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterIdentity</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">391 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Destination</td><td style="border:1px solid var(--color-border); padding:0.5rem;">387 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">391 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Lease</td><td style="border:1px solid var(--color-border); padding:0.5rem;">44 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">44 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">44 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Lease2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1200 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈2000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈500 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈800 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈2000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈600 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈3000+ bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterAddress</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈150 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈300 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈600 bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1000 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈1500 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">≈3000+ bytes</td></tr>
  </tbody>
</table>
### Référence rapide des types de base de données

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Structure</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RouterInfo</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Stored under Hash(RouterIdentity)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Use LeaseSet2 instead</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Stored under Hash(Destination)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Stored under Hash(Blinded Destination)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">MetaLeaseSet</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Defined</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Verify production status</td></tr>
  </tbody>
</table>
### Référence rapide du protocole de transport

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Protocol</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Port Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">UDP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.54</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Default since 0.9.56</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TCP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.36</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">UDP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1pxsolid var(--color-border); padding:0.5rem;">Removed in 2.4.0</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TCP</td><td style="border:1px solid var(--color-border); padding:0.5rem;">-</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Removed in 0.9.50</td></tr>
  </tbody>
</table>
### Référence rapide des jalons de version

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">API</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Date</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Changes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.6.x</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2005</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destination encryption disabled</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Dec 2013</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Key Certificates introduced</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Sep 2015</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA support added</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.16</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.16</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Nov 2015</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Router Key Certificates</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.36</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.36</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Aug 2018</td><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP2 introduced</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Nov 2018</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2, X25519 for Destinations</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Dec 2018</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet working</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.48</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.48</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Jul 2020</td><td style="border:1px solid var(--color-border); padding:0.5rem;">X25519 for Router Identities</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.50</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.50</td><td style="border:1px solid var(--color-border); padding:0.5rem;">May 2021</td><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP removed</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.54</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.54</td><td style="border:1px solid var(--color-border); padding:0.5rem;">May 2022</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 testing</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.57</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.57</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Jan 2023</td><td style="border:1px solid var(--color-border); padding:0.5rem;">[Proposal 161](/fr/proposals/161-ri-dest-padding/) padding (release 2.1.0)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.58</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.58</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Mar 2023</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal/DSA deprecated for RIs (2.2.0)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.66</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.66</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Jun 2025</td><td style="border:1px solid var(--color-border); padding:0.5rem;">[Proposal 167](/proposals/167-service-records/) service records (2.9.0)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Sep 2025</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ML-KEM beta support (2.10.0)</td></tr>
  </tbody>
</table>
---
