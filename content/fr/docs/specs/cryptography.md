---
title: "Cryptographie de bas niveau"
description: "Résumé des primitives cryptographiques symétriques, asymétriques et de signature utilisées au sein d'I2P"
slug: "cryptography"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
reviewStatus: "needs-review"
---


## Instantané de l'évolution

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Functional Area</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Legacy Primitive</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Current / Planned Primitive</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Migration Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Transport key exchange</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Diffie–Hellman over 2048-bit prime (NTCP / SSU)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519 (NTCP2 / SSU2)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Completed (NTCP2 and SSU2 fully deployed)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">End-to-end encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ElGamal/AES+SessionTags</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECIES-X25519-AEAD-Ratchet</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Completed (2.4.0+)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Symmetric cipher</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES-256/CBC + HMAC-MD5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20/Poly1305 (AEAD)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Active (tunnel layer remains AES-256)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default signatures</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DSA-SHA1 (1024-bit)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA/RedDSA on Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fully migrated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Experimental / future</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">—</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Hybrid post-quantum encryption (opt-in)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">In testing (2.10.0)</td>
    </tr>
  </tbody>
  
</table>
## Chiffrement asymétrique

### X25519 (algorithme d’échange de clés Diffie-Hellman à courbe elliptique)

- Utilisé pour NTCP2, ECIES-X25519-AEAD-Ratchet, SSU2 et la création de tunnel basée sur X25519.  
- Fournit des clés compactes, des opérations en temps constant et la confidentialité persistante via le cadre du protocole Noise.  
- Offre une sécurité de 128 bits avec des clés de 32 octets et un échange de clés efficace.

### ElGamal (ancien)

- Conservé pour des raisons de compatibilité ascendante avec d’anciens routers.  
- Fonctionne sur le nombre premier du groupe Oakley 14 à 2048 bits (RFC 3526) avec le générateur 2.  
- Chiffre les clés de session AES ainsi que les IV dans des textes chiffrés de 514 octets.  
- N’offre ni chiffrement authentifié ni confidentialité persistante ; tous les points de terminaison modernes ont migré vers ECIES.

## Chiffrement symétrique

### ChaCha20/Poly1305 (algorithme de chiffrement authentifié combinant ChaCha20 pour le chiffrement et Poly1305 pour l'authentification)

- Primitive de chiffrement authentifié par défaut dans NTCP2, SSU2 et ECIES.  
- Fournit une sécurité AEAD et de hautes performances sans prise en charge matérielle AES.  
- Implémenté conformément à la RFC 7539 (clé 256 bits, nonce 96 bits, tag 128 bits).

### AES‑256/CBC (ancien)

- Toujours utilisé pour le chiffrement de la couche de tunnel, où sa structure de chiffrement par blocs s’aligne bien sur le modèle de chiffrement en couches d’I2P.  
- Utilise le remplissage PKCS#5 et des transformations de l’IV (vecteur d’initialisation) à chaque saut.  
- Prévu pour un examen à long terme, mais reste solide sur le plan cryptographique.

## Signatures

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Signature Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage Notes</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DSA‑SHA1 (1024‑bit)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Original default; still accepted for legacy Destinations.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA‑SHA256/384/512</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Used during 2014–2015 transition.</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA‑SHA512‑Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default for Router and Destination identities (since 0.9.15).</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RedDSA‑SHA512‑Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Used for encrypted LeaseSet signatures (0.9.39+).</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Specialized</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA‑SHA512‑4096</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For out‑of‑band signing (su3 updates, reseeds, plugins).</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Application‑layer</td>
    </tr>
  </tbody>
</table>
## Hachage et dérivation de clés

- **SHA‑256:** Utilisé pour les clés DHT (table de hachage distribuée), HKDF (fonction de dérivation de clés) et les anciennes signatures.  
- **SHA‑512:** Utilisé par EdDSA/RedDSA (schémas de signature) et pour les dérivations HKDF de Noise (protocole cryptographique).  
- **HKDF‑SHA256:** Dérive les clés de session dans ECIES (schéma de chiffrement à courbe elliptique), NTCP2 et SSU2.  
- Des dérivations SHA‑256 à rotation quotidienne sécurisent les emplacements de stockage de RouterInfo et LeaseSet dans le netDb.

## Résumé de la couche de transport

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Transport</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Key Exchange</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Encryption</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Authentication</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NTCP2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20/Poly1305</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AEAD</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default TCP transport</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SSU2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ChaCha20/Poly1305</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AEAD</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default UDP transport</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SSU (Legacy)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DH‑2048</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">AES‑256/CBC + HMAC‑MD5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Legacy</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Removed (2.4.0)</td>
    </tr>
  </tbody>
</table>
Les deux transports fournissent une confidentialité persistante au niveau de la liaison et une protection contre les attaques par rejeu, en utilisant le Noise_XK handshake pattern (schéma de poignée de main Noise_XK).

## Chiffrement de la couche Tunnel

- Continue d’utiliser AES‑256/CBC pour le chiffrement en couches par saut.  
- Les passerelles sortantes effectuent un déchiffrement AES itératif ; chaque saut ré‑chiffre en utilisant sa clé de couche et sa clé d’IV (vecteur d’initialisation).  
- Le chiffrement à double IV atténue les attaques par corrélation et par confirmation.  
- La migration vers l’AEAD (chiffrement authentifié avec données associées) est à l’étude mais n’est pas actuellement prévue.

## Cryptographie post‑quantique

- I2P 2.10.0 introduit le **chiffrement post‑quantique hybride expérimental**.  
- Activé manuellement via Hidden Service Manager (gestionnaire de services cachés) pour des tests.  
- Combine X25519 avec un KEM (mécanisme d’encapsulation de clés) résistant aux attaques quantiques (mode hybride).  
- Pas activé par défaut; destiné à la recherche et à l’évaluation des performances.

## Cadre d'extensibilité

- Les *identifiants de type* pour le chiffrement et la signature permettent la prise en charge parallèle de plusieurs primitives.  
- Les correspondances actuelles incluent:  
  - **Types de chiffrement:** 0 = ElGamal/AES+SessionTags, 4 = ECIES‑X25519‑AEAD‑Ratchet.  
  - **Types de signature:** 0 = DSA‑SHA1, 7 = EdDSA‑SHA512‑Ed25519, 11 = RedDSA‑SHA512‑Ed25519.  
- Ce cadre permet des mises à niveau futures, y compris des schémas post‑quantiques, sans scissions du réseau.

## Composition cryptographique

- **Couche de transport:** X25519 + ChaCha20/Poly1305 (cadre Noise).  
- **Couche tunnel:** Chiffrement en couches AES‑256/CBC pour l’anonymat.  
- **De bout en bout:** ECIES‑X25519‑AEAD‑Ratchet pour la confidentialité et la confidentialité persistante.  
- **Couche de base de données:** Signatures EdDSA/RedDSA pour l’authenticité.

Ces couches se combinent pour fournir une défense en profondeur : même si l’une d’elles est compromise, les autres préservent la confidentialité et la non‑corrélabilité.

## Résumé

La pile cryptographique d’I2P 2.10.0 s’articule autour de :

- **Curve25519 (X25519)** pour l'échange de clés  
- **ChaCha20/Poly1305** pour le chiffrement symétrique  
- **EdDSA / RedDSA** pour les signatures  
- **SHA‑256 / SHA‑512** pour le hachage et la dérivation de clés  
- **Modes hybrides post‑quantiques expérimentaux** pour la compatibilité future

Les algorithmes hérités ElGamal, AES‑CBC et DSA demeurent pour assurer la compatibilité ascendante, mais ne sont plus utilisés dans les transports actifs ni dans les chemins de chiffrement.
