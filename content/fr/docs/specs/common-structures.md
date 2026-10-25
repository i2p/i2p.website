---
title: "Spécification des structures communes"
description: "Types de données communs à tous les protocoles I2P"
slug: "common-structures"
aliases:
  - "/fr/common_structures_spec"
  - "/fr/common_structures_spec/"
category: "Conception"
lastUpdated: "2026-10"
accurateFor: "0.9.71"
---

Ce document décrit certains types de données communs à tous les protocoles I2P, comme [I2NP](/docs/specs/i2np/), [I2CP](/docs/specs/i2cp/), [SSU](/docs/legacy/ssu/), etc.

## Spécification de type commun

### Entier

#### Description

Représente un entier non négatif.

#### Sommaire

1 à 8 octets en ordre d'octets réseau (big endian) représentant un entier non signé.

### Date

#### Description

Le nombre de millisecondes écoulées depuis minuit le 1er janvier 1970 dans le fuseau horaire GMT. Si le nombre est 0, la date est indéfinie ou nulle.

#### Sommaire

8 byte [Integer](#integer)

### Chaîne de caractères

#### Description

Représente une chaîne de caractères encodée en UTF-8.

#### Sommaire

1 ou plusieurs octets où le premier octet est le nombre d'octets (pas de caractères !) dans la chaîne et les 0-255 octets restants sont le tableau de caractères encodé en UTF-8 non terminé par null. La limite de longueur est de 255 octets (pas de caractères). La longueur peut être 0.

### PublicKey

#### Description

Cette structure est utilisée dans ElGamal ou d'autres chiffrements asymétriques, représentant seulement l'exposant, pas les nombres premiers, qui sont constants et définis dans la spécification cryptographique [ELGAMAL](/docs/specs/cryptography/#elgamal-legacy). D'autres schémas de chiffrement sont en cours de définition, voir le tableau ci-dessous.

#### Sommaire

Le type et la longueur de la clé sont déduits du contexte ou sont spécifiés dans le certificat de clé d'une destination ou d'un RouterInfo, ou dans les champs d'un [LeaseSet2](#leaseset2) ou d'une autre structure de données. Le type par défaut est ElGamal. À partir de la version 0.9.38, d'autres types peuvent être pris en charge, selon le contexte. Les clés sont en big-endian sauf indication contraire.

Les clés X25519 sont prises en charge dans les Destinations et LeaseSet2 depuis la version 0.9.44. Les clés X25519 sont prises en charge dans les RouterIdentities depuis la version 0.9.48.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ElGamal</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated for Router Identities as of 0.9.58; use for Destinations, as the public key field is unused there; discouraged for leasesets</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TBD</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see proposal 145</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">96</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TBD</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see proposal 145</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P521</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">132</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TBD</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see proposal 145</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Little-endian. See <a href="/docs/specs/ecies/">ECIES</a> and <a href="/docs/specs/ecies-routers/">ECIES-ROUTERS</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for Leasesets only, not for RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for Leasesets only, not for RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for Leasesets only, not for RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">800</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for handshakes only, not for Leasesets, RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1184</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for handshakes only, not for Leasesets, RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1568</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for handshakes only, not for Leasesets, RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_CT</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">768</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for handshakes only, not for Leasesets, RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_CT</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1088</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for handshakes only, not for Leasesets, RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_CT</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1568</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for handshakes only, not for Leasesets, RIs or Destinations</td>
    </tr>
  </tbody>
</table>
JavaDoc: [net.i2p.data.PublicKey](http://docs.i2p-projekt.de/net/i2p/data/PublicKey.html)

### PrivateKey

#### Description

Cette structure est utilisée dans ElGamal ou d'autres décryptages asymétriques, représentant seulement l'exposant, pas les nombres premiers qui sont constants et définis dans la spécification cryptographique [ELGAMAL](/docs/specs/cryptography/#elgamal-legacy). D'autres schémas de chiffrement sont en cours de définition, voir le tableau ci-dessous.

#### Sommaire

Le type et la longueur de clé sont déduits du contexte ou stockés séparément dans une structure de données ou un fichier de clé privée. Le type par défaut est ElGamal. Depuis la version 0.9.38, d'autres types peuvent être pris en charge, selon le contexte. Les clés sont en big-endian sauf indication contraire.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ElGamal</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated for Router Identities as of 0.9.58; use for Destinations, as the public key field is unused there; discouraged for leasesets</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TBD</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see proposal 145</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">48</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TBD</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see proposal 145</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P521</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">66</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TBD</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see proposal 145</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Little-endian. See <a href="/docs/specs/ecies/">ECIES</a> and <a href="/docs/specs/ecies-routers/">ECIES-ROUTERS</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for Leasesets only, not for RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for Leasesets only, not for RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for Leasesets only, not for RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1632</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for handshakes only, not for Leasesets, RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2400</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for handshakes only, not for Leasesets, RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3168</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for handshakes only, not for Leasesets, RIs or Destinations</td>
    </tr>
  </tbody>
</table>
JavaDoc: [net.i2p.data.PrivateKey](http://docs.i2p-projekt.de/net/i2p/data/PrivateKey.html)

### SessionKey

#### Description

Cette structure est utilisée pour le chiffrement et déchiffrement symétrique AES256.

#### Sommaire

32 octets

JavaDoc: [net.i2p.data.SessionKey](http://docs.i2p-projekt.de/net/i2p/data/SessionKey.html)

### SigningPublicKey

#### Description

Cette structure est utilisée pour vérifier les signatures.

#### Sommaire

Le type et la longueur de clé sont déduits du contexte ou sont spécifiés dans le certificat de clé d'une destination. Le type par défaut est DSA_SHA1. À partir de la version 0.9.12, d'autres types peuvent être pris en charge, selon le contexte.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DSA_SHA1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated for Router Identities as of 09.58; discouraged for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA256_P256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Older Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA384_P384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">96</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Rarely used for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA512_P521</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">132</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Rarely used for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA256_2048</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA384_3072</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA512_4096</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">512</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA_SHA512_Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Recent Router Identities and Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA_SHA512_Ed25519ph</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.25</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RedDSA_SHA512_Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.39</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For Destinations and encrypted leasesets only, never used for Router Identities</td>
    </tr>
  </tbody>
</table>
#### Notes

* Quand une clé est composée de deux éléments (par exemple les points X,Y), elle est
  sérialisée en complétant chaque élément à longueur/2 avec des zéros en tête si
  nécessaire.

* Tous les types sont en Big Endian, excepté pour EdDSA et RedDSA, qui sont stockés et transmis
  dans un format Little Endian.

JavaDoc: [net.i2p.data.SigningPublicKey](http://docs.i2p-projekt.de/net/i2p/data/SigningPublicKey.html)

### SigningPrivateKey

#### Description

Cette structure est utilisée pour créer des signatures.

#### Sommaire

Le type et la longueur de clé sont spécifiés lors de la création. Le type par défaut est DSA_SHA1. À partir de la version 0.9.12, d'autres types peuvent être pris en charge, selon le contexte.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DSA_SHA1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated for Router Identities as of 09.58; discouraged for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA256_P256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Older Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA384_P384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">48</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Rarely used for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA512_P521</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">66</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Rarely used for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA256_2048</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">512</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA384_3072</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">768</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA512_4096</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1024</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA_SHA512_Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Recent Router Identities and Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA_SHA512_Ed25519ph</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.25</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RedDSA_SHA512_Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.39</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For Destinations and encrypted leasesets only, never used for Router Identities</td>
    </tr>
  </tbody>
</table>
#### Notes

* Lorsqu'une clé est composée de deux éléments (par exemple les points X,Y), elle est sérialisée en complétant chaque élément à longueur/2 avec des zéros de tête si nécessaire.

* Tous les types sont en Big Endian, à l'exception d'EdDSA et RedDSA, qui sont stockés et transmis dans un format Little Endian.

JavaDoc: [net.i2p.data.SigningPrivateKey](http://docs.i2p-projekt.de/net/i2p/data/SigningPrivateKey.html)

### Signature

#### Description

Cette structure représente la signature de certaines données.

#### Sommaire

Le type et la longueur de signature sont déduits du type de clé utilisé. Le type par défaut est DSA_SHA1. Depuis la version 0.9.12, d'autres types peuvent être pris en charge, selon le contexte.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Length (bytes)</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DSA_SHA1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">40</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated for Router Identities as of 09.58; discouraged for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA256_P256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Older Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA384_P384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">96</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Rarely used for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA512_P521</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">132</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Rarely used for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA256_2048</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA384_3072</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA512_4096</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">512</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA_SHA512_Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Recent Router Identities and Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA_SHA512_Ed25519ph</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.25</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Offline signing, never used for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RedDSA_SHA512_Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.39</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For Destinations and encrypted leasesets only, never used for Router Identities</td>
    </tr>
  </tbody>
</table>
#### Notes

* Lorsqu'une signature est composée de deux éléments (par exemple les valeurs R,S), elle est sérialisée en complétant chaque élément à longueur/2 avec des zéros en tête si nécessaire.

* Tous les types sont en Big Endian, à l'exception d'EdDSA et RedDSA, qui sont stockés et transmis dans un format Little Endian.

JavaDoc: [net.i2p.data.Signature](http://docs.i2p-projekt.de/net/i2p/data/Signature.html)

### Hachage

#### Description

Représente le SHA256 de certaines données.

#### Sommaire

32 octets

JavaDoc: [net.i2p.data.Hash](http://docs.i2p-projekt.de/net/i2p/data/Hash.html)

### Étiquette de session

Note : Les Session Tags pour les destinations ECIES-X25519 (ratchet) et les routers ECIES-X25519 font 8 octets. Voir [ECIES](/docs/specs/ecies/) et [ECIES-ROUTERS](/docs/specs/ecies-routers/).

#### Description

Un nombre aléatoire

#### Table des matières

32 octets

JavaDoc: [net.i2p.data.SessionTag](http://docs.i2p-projekt.de/net/i2p/data/SessionTag.html)

### TunnelId

#### Description

Définit un identifiant unique pour chaque router dans un tunnel. Un Tunnel ID est généralement supérieur à zéro ; n'utilisez pas une valeur de zéro sauf dans des cas particuliers.

#### Sommaire

Entier [Integer](#integer) de 4 octets

JavaDoc: [net.i2p.data.TunnelId](http://docs.i2p-projekt.de/net/i2p/data/TunnelId.html)

### Certificat

#### Description

Un certificat est un conteneur pour diverses preuves de réception ou preuves de travail utilisées dans le réseau I2P.

#### Sommaire

1 octet [Integer](#integer) spécifiant le type de certificat, suivi d'un [Integer](#integer) de 2 octets spécifiant la taille de la charge utile du certificat, puis ce nombre d'octets.

```
+----+----+----+----+----+-/
|type| length  | payload
+----+----+----+----+----+-/

type :: Integer
        length -> 1 byte

length :: Integer
          length -> 2 bytes

payload :: data
           length -> $length bytes
```
#### Notes

* Pour les [Identités de Router](#routeridentity), le Certificat est toujours NULL jusqu'à la version
  0.9.15. À partir de la version 0.9.16, un Certificat de Clé est utilisé pour spécifier les
  types de clés. À partir de la version 0.9.48, les types de clés publiques de chiffrement X25519
  sont autorisés. Voir ci-dessous.

* Pour les [Garlic Cloves](/docs/specs/i2np/#struct-garlicclove), le Certificate est toujours NULL, aucun autre n'est actuellement implémenté.

* Pour les [Garlic Messages](/docs/specs/i2np/#msg-garlic), le Certificat est toujours NULL, aucun autre n'est actuellement implémenté.

* Pour les [Destinations](#destination), le Certificate peut être non-NULL. Depuis la version 0.9.12, un Key Certificate peut être utilisé pour spécifier le type de clé publique de signature. Voir ci-dessous.

* Les implémenteurs sont avertis d'interdire les données excédentaires dans les Certificats.
  La longueur appropriée pour chaque type de certificat doit être appliquée.

#### Types de certificats

Les types de certificats suivants sont définis :

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Payload Length</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Total Length</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Null</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HashCash</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">varies</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">varies</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated, unused. Payload contains an ASCII colon-separated hashcash string.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Hidden</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated, unused. Hidden routers generally do not announce that they are hidden.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signed</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">40 or 72</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">43 or 75</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated, unused. Payload contains a 40-byte DSA signature, optionally followed by the 32-byte Hash of the signing Destination.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Multiple</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">varies</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">varies</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated, unused. Payload contains multiple certificates.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Key</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7+</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Since 0.9.12. See below for details.</td>
    </tr>
  </tbody>
</table>
#### Certificats de Clés

Les certificats de clé ont été introduits dans la version 0.9.12. Avant cette version, toutes les PublicKeys étaient des clés ElGamal de 256 octets, et toutes les SigningPublicKeys étaient des clés DSA-SHA1 de 128 octets. Un certificat de clé fournit un mécanisme pour indiquer le type de la PublicKey et de la SigningPublicKey dans la Destination ou RouterIdentity, et pour empaqueter toutes les données de clé dépassant les longueurs standard.

En maintenant exactement 384 octets avant le certificat, et en plaçant toutes les données de clé excédentaires à l'intérieur du certificat, nous maintenons la compatibilité pour tout logiciel qui analyse les Destinations et les Router Identities.

Le payload du certificat de clé contient :

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Data</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Length</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signing Public Key Type (<a href="#integer">Integer</a>)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Crypto Public Key Type (<a href="#integer">Integer</a>)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Excess Signing Public Key Data</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0+</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Excess Crypto Public Key Data</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0+</td>
    </tr>
  </tbody>
</table>
Attention : L'ordre des types de clés est l'inverse de ce à quoi vous pourriez vous attendre ; le Type de Clé Publique de Signature vient en premier.

Les types de clés publiques de signature définis sont :

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Total Public Key Length</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DSA_SHA1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated for Router Identities as of 0.9.58; discouraged for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA256_P256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Older Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA384_P384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">96</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Rarely if ever used for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA512_P521</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">132</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Rarely if ever used for Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA256_2048</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Offline only; never used in Key Certificates for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA384_3072</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated Offline only; never used in Key Certificates for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA512_4096</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">512</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Offline only; never used in Key Certificates for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA_SHA512_Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Recent Router Identities and Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA_SHA512_Ed25519ph</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">8</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.25</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Offline only; never used in Key Certificates for Router Identities or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (GOST)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">9</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/134-gost/">Prop134</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (GOST)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">10</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/134-gost/">Prop134</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RedDSA_SHA512_Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">11</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.39</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For Destinations and encrypted leasesets only; never used for Router Identities</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (MLDSA)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">12</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/169-pq-crypto/">Prop169</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (MLDSA)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">13</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/169-pq-crypto/">Prop169</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (MLDSA)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">14</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/169-pq-crypto/">Prop169</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (MLDSA)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">15</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/169-pq-crypto/">Prop169</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (MLDSA)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">16</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/169-pq-crypto/">Prop169</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (MLDSA)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">17</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/169-pq-crypto/">Prop169</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (MLDSA)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">18</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/169-pq-crypto/">Prop169</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (MLDSA)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">19</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/169-pq-crypto/">Prop169</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (MLDSA)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/169-pq-crypto/">Prop169</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">65280-65534</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved for experimental use</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">65535</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved for future expansion</td>
    </tr>
  </tbody>
</table>
Les types de clés publiques cryptographiques définis sont :

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Type Code</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Total Public Key Length</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ElGamal</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated for Router Identities as of 0.9.58; use for Destinations, as the public key field is unused there</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see proposal 145</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">96</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see proposal 145</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">P521</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">132</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see proposal 145</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies/">ECIES</a> and proposal 156</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM512_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for Leasesets only, not for RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM768_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for Leasesets only, not for RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">MLKEM1024_X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">See <a href="/docs/specs/ecies-hybrid/">ECIES-HYBRID</a>, for Leasesets only, not for RIs or Destinations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved (NONE)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">255</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved, see <a href="/proposals/169-pq-crypto/">Prop169</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">65280-65534</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved for experimental use</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">65535</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reserved for future expansion</td>
    </tr>
  </tbody>
</table>
Lorsqu'un certificat de clé n'est pas présent, les 384 octets précédents dans la destination ou l'identité de routeur sont définis comme la clé publique ElGamal de 256 octets suivie de la clé publique de signature DSA-SHA1 de 128 octets. Lorsqu'un certificat de clé est présent, les 384 octets précédents sont redéfinis comme suit :

* Clé publique cryptographique complète ou première portion

* Remplissage aléatoire si les longueurs totales des deux clés sont inférieures à 384 octets

* Clé publique de signature complète ou première partie

La clé publique cryptographique est alignée au début et la clé publique de signature est alignée à la fin. Le remplissage (le cas échéant) se trouve au milieu. Les longueurs et les limites des données de clé initiales, du remplissage et des portions de données de clé excédentaires dans les certificats ne sont pas explicitement spécifiées, mais sont dérivées des longueurs des types de clés spécifiés. Si les longueurs totales des clés publiques cryptographiques et de signature dépassent 384 octets, le reste sera contenu dans le certificat de clé. Si la longueur de la clé publique cryptographique n'est pas de 256 octets, la méthode pour déterminer la limite entre les deux clés doit être spécifiée dans une révision future de ce document.

Exemples de structures utilisant une clé publique de cryptographie ElGamal et le type de clé publique de signature indiqué :

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Signing Key Type</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Padding Length</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Excess Signing Key Data in Cert</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">DSA_SHA1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA256_P256</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">64</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA384_P384</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ECDSA_SHA512_P521</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA256_2048</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">128</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA384_3072</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">256</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">RSA_SHA512_4096</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">384</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA_SHA512_Ed25519</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">96</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">EdDSA_SHA512_Ed25519ph</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">96</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0</td>
    </tr>
  </tbody>
</table>
JavaDoc: [net.i2p.data.Certificate](http://docs.i2p-projekt.de/net/i2p/data/Certificate.html)

#### Notes

* Les implémenteurs sont avertis d'interdire les données excédentaires dans les certificats de clé.
  La longueur appropriée pour chaque type de certificat doit être appliquée.

* Un certificat KEY avec les types 0,0 (ElGamal,DSA_SHA1) est autorisé mais déconseillé.
  Il n'est pas bien testé et peut causer des problèmes dans certaines implémentations.
  Utilisez un certificat NULL dans la représentation canonique d'une
  Destination ou RouterIdentity (ElGamal,DSA_SHA1), qui sera 4 octets plus court
  qu'en utilisant un certificat KEY.

### Mappage

#### Description

Un ensemble de correspondances clé/valeur ou de propriétés

#### Sommaire

Un entier de taille 2 octets suivi d'une série de paires String=String;.

AVERTISSEMENT : La plupart des utilisations de Mapping se trouvent dans des structures signées, où les entrées Mapping doivent être triées par clé, afin que la signature soit immuable. L'échec du tri par clé entraînera des échecs de signature !

```bytefield
size       | 4 | red    | Integer, 2 bytes
key_string | 4 | blue   | String (len + data)
val_string | 8 | green  | String (len + data)
;          | 8 | yellow | :: A single byte containing ';'
```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
|  size   | key_string (len + data)| =  |
+----+----+----+----+----+----+----+----+
| val_string (len + data)     | ;  | ...
+----+----+----+----+----+----+----+
```
</details>
#### Notes

* L'encodage n'est pas optimal - nous avons besoin soit des caractères '=' et ';', soit des longueurs de chaîne, mais pas des deux

#### Description

* Certaines documentations indiquent que les chaînes ne peuvent pas inclure '=' ou ';' mais cet encodage les prend en charge

* Les chaînes sont définies comme étant UTF-8 mais dans l'implémentation actuelle, I2CP utilise UTF-8 mais pas I2NP. Par exemple, les chaînes UTF-8 dans un mappage d'options RouterInfo dans un message I2NP Database Store seront corrompues.

* L'encodage autorise les clés dupliquées, cependant dans tout usage où le mappage est signé, les doublons peuvent provoquer un échec de signature.

* Les mappings contenus dans les messages I2NP (par exemple dans une RouterAddress ou RouterInfo)
  doivent être triés par clé afin que la signature soit invariante. Les clés
  dupliquées ne sont pas autorisées.

* Les mappages contenus dans un [I2CP SessionConfig](/docs/specs/i2cp/#struct-sessionconfig) doivent être triés par clé afin que
  la signature soit invariante. Les clés dupliquées ne sont pas autorisées.

* La méthode de tri est définie comme dans Java String.compareTo(), en utilisant la valeur Unicode des caractères.

* Bien que cela dépende de l'application, les clés et valeurs sont généralement sensibles à la casse.

* Les limites de longueur des chaînes de clé et de valeur sont de 255 octets (pas de caractères) chacune, plus l'octet de longueur. L'octet de longueur peut être 0.

* La limite de longueur totale est de 65535 octets, plus le champ de taille de 2 octets, soit 65537 au total.

* Une Router Identity avec un type de chiffrement X25519 et un type de signature Ed25519 contiendra 10 copies (320 octets) de données aléatoires, pour une économie d'environ 288 octets une fois compressée.

JavaDoc: [net.i2p.data.DataHelper](http://docs.i2p-projekt.de/net/i2p/data/DataHelper.html)

## Spécification de structure commune

### KeysAndCert

#### Sommaire

Une clé publique de chiffrement, une clé publique de signature, et un certificat, utilisés soit comme RouterIdentity soit comme Destination.

#### Directives de génération de padding

Une [PublicKey](#publickey) suivie d'une [SigningPublicKey](#signingpublickey) puis d'un [Certificate](#certificate).

```bytefield
public_key          | 8 | blue   | PublicKey (partial or full), 256 bytes or as specified in key cert

padding (optional)  | 8 | yellow | random data, pub + pad + sig == 384 bytes

signing_key         | 8 | green  | SigningPublicKey (partial or full), 128 bytes or as specified

certificate         | 3 | purple | Certificate, >= 3 bytes
= total length: 387+ bytes
```
<details class="content-section">
<summary>View original ASCII diagram</summary>

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
+----+----+----+-/

public_key :: `PublicKey` (partial or full)
              length -> 256 bytes or as specified in key certificate

padding :: random data
           length -> 0 bytes or as specified in key certificate
           public_key length + padding length + signing_key length == 384 bytes

signing__key :: `SigningPublicKey` (partial or full)
                length -> 128 bytes or as specified in key certificate

certificate :: `Certificate`
               length -> >= 3 bytes

total length: 387+ bytes
```

</details>
#### Notes

Ces directives ont été proposées dans la Proposition 161 et implémentées dans la version d'API 0.9.57. Ces directives sont rétrocompatibles avec toutes les versions depuis la 0.6 (2005). Voir la Proposition 161 pour le contexte et des informations supplémentaires.

Pour toute combinaison actuellement utilisée de types de clés autre qu'ElGamal + DSA-SHA1, un remplissage sera présent. De plus, pour les destinations, le champ de clé publique de 256 octets n'est plus utilisé depuis la version 0.6 (2005).

Les implémenteurs devraient générer les données aléatoires pour les clés publiques de Destination, et le rembourrage des identités de Destination et de router, de manière à ce qu'elles soient compressibles dans divers protocoles I2P tout en restant sécurisées, et sans que les représentations Base 64 apparaissent comme corrompues ou non sécurisées. Cela offre la plupart des avantages de la suppression des champs de rembourrage sans aucun changement de protocole perturbateur.

Strictement parlant, la clé publique de signature de 32 octets seule (dans les Destinations et les Router Identities) et la clé publique de chiffrement de 32 octets (dans les Router Identities uniquement) est un nombre aléatoire qui fournit toute l'entropie nécessaire pour que les hachages SHA-256 de ces structures soient cryptographiquement robustes et distribués de manière aléatoire dans la DHT de la base de données réseau.

Cependant, par excès de prudence, nous recommandons d'utiliser un minimum de 32 octets de données aléatoires dans le champ de clé publique ElG et le padding. De plus, si les champs étaient tous à zéro, les destinations Base 64 contiendraient de longues séquences de caractères AAAA, ce qui pourrait alarmer ou confondre les utilisateurs.

Répétez les 32 octets de données aléatoires autant que nécessaire pour que la structure KeysAndCert complète soit hautement compressible dans les protocoles I2P tels que I2NP Database Store Message, Streaming SYN, handshake SSU2, et Datagrams avec réponse.

Exemples :

* Une Destination avec un type de signature Ed25519
  contiendra 11 copies (352 octets) des données aléatoires, pour une économie d'environ 320 octets une fois compressée.

* N'assumez pas que ceux-ci font toujours 387 octets ! Ils font 387 octets plus la longueur du certificat spécifiée aux octets 385-386, qui peut être non nulle.

Les implémentations doivent, bien entendu, stocker la structure complète de 387+ octets car le hachage SHA-256 de la structure couvre l'intégralité du contenu.

#### Description

* À partir de la version 0.9.12, si le certificat est un Key Certificate, les limites des champs de clé peuvent varier. Voir la section Key Certificate ci-dessus pour plus de détails.

* La clé publique cryptographique est alignée au début et la clé publique de signature est alignée à la fin. Le rembourrage (s'il y en a un) se trouve au milieu.

* Le certificat pour une RouterIdentity était toujours NULL jusqu'à la version 0.9.12.

JavaDoc: [net.i2p.data.KeysAndCert](http://docs.i2p-projekt.de/net/i2p/data/KeysAndCert.html)

### RouterIdentity

#### Sommaire

Définit la façon d'identifier de manière unique un router particulier

#### Notes

Identique à KeysAndCert.

Voir [KeysAndCert](#keysandcert) pour les directives sur la génération de données aléatoires pour le champ de remplissage.

#### Description

* Ne supposez pas que ceux-ci font toujours 387 octets ! Ils font 387 octets plus la longueur du certificat spécifiée aux octets 385-386, qui peut être non nulle.

* À partir de la version 0.9.12, si le certificat est un Key Certificate, les limites des champs de clé peuvent varier. Voir la section Key Certificate ci-dessus pour plus de détails.

* La clé publique crypto est alignée au début et la clé publique de signature est alignée à la fin. Le remplissage (le cas échéant) se trouve au milieu.

* Les RouterIdentities avec un certificat de clé et une clé publique ECIES_X25519
  sont pris en charge depuis la version 0.9.48.
  Avant cela, toutes les RouterIdentities étaient ElGamal.

* La clé publique de la destination était utilisée pour l'ancien chiffrement i2cp-to-i2cp
  qui a été désactivé dans la version 0.6 (2005), elle n'est actuellement pas utilisée sauf
  pour l'IV du chiffrement LeaseSet, qui est obsolète. La clé publique dans
  le LeaseSet est utilisée à la place.

JavaDoc: [net.i2p.data.router.RouterIdentity](http://docs.i2p-projekt.de/net/i2p/data/router/RouterIdentity.html)

### Destination

#### Sommaire

Une Destination définit un point de terminaison particulier vers lequel les messages peuvent être dirigés pour une livraison sécurisée.

#### Notes

Identique à [KeysAndCert](#keysandcert), sauf que la clé publique n'est jamais utilisée et peut contenir des données aléatoires au lieu d'une clé publique ElGamal valide.

Voir [KeysAndCert](#keysandcert) pour les directives sur la génération des données aléatoires pour la clé publique et les champs de remplissage.

#### Description

* Ne supposez pas que ceux-ci font toujours 387 octets ! Ils font 387 octets plus la longueur du certificat spécifiée aux octets 385-386, qui peut être non nulle.

* À partir de la version 0.9.12, si le certificat est un Key Certificate, les limites des champs de clé peuvent varier. Voir la section Key Certificate ci-dessus pour plus de détails.

* La clé publique cryptographique est alignée au début et la clé publique de signature est alignée à la fin. Le remplissage (s'il y en a un) est au milieu.

* La clé publique de la destination était utilisée pour l'ancien chiffrement I2CP vers I2CP qui a été désactivé dans la version 0.6, elle n'est actuellement pas utilisée.

JavaDoc: [net.i2p.data.Destination](http://docs.i2p-projekt.de/net/i2p/data/Destination.html)

### Lease

#### Sommaire

OBSOLÈTE. Utilisez LeaseSet2 et Lease2.

Définit l'autorisation pour un tunnel particulier de recevoir des messages destinés à une [Destination](#destination).

#### Description

SHA256 du [Hash](#hash) du [RouterIdentity](#routeridentity) du routeur passerelle, puis le [TunnelId](#tunnelid), et enfin une [Date](#date) de fin.

```bytefield
tunnel_gw   | 8 | blue   | Hash of the RouterIdentity of the tunnel gateway, 32 bytes

tunnel_id   | 4 | green  | TunnelId, 4 bytes
end_date    | 4 | yellow | Date, 8 bytes

= Total size 44 bytes
```
<details class="content-section">
<summary>View original ASCII diagram</summary>

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

tunnel_gw :: Hash of the `RouterIdentity` of the tunnel gateway
             length -> 32 bytes

tunnel_id :: `TunnelId`
             length -> 4 bytes

end_date :: `Date`
            length -> 8 bytes
```

</details>
JavaDoc : [net.i2p.data.Lease](http://docs.i2p-projekt.de/net/i2p/data/Lease.html)

### LeaseSet

#### Sommaire

OBSOLÈTE. Utilisez LeaseSet2 et Lease2.

Contient tous les [Leases](#lease) actuellement autorisés pour un [Destination](#destination) particulier, la [PublicKey](#publickey) permettant de chiffrer les messages au format garlic, puis la [SigningPublicKey](#signingpublickey) qui peut être utilisée pour révoquer cette version spécifique de la structure. Le LeaseSet est l'une des deux structures stockées dans la base de données du réseau (l'autre étant [RouterInfo](#routerinfo)), et est indexé selon le hachage SHA256 du [Destination](#destination) qu'il contient.

#### Notes

[Destination](#destination), suivie d'une [PublicKey](#publickey) pour le chiffrement, puis d'une [SigningPublicKey](#signingpublickey) qui peut être utilisée pour révoquer cette version du LeaseSet, puis d'un [Integer](#integer) de 1 octet spécifiant combien de structures [Lease](#lease) sont dans l'ensemble, suivi des structures [Lease](#lease) actuelles et enfin d'une [Signature](#signature) des octets précédents signée par la [SigningPrivateKey](#signingprivatekey) de la [Destination](#destination).

```bytefield
destination     | 8 | blue   | Destination, >= 387+ bytes
encryption_key  | 8 | green  | PublicKey, 256 bytes
signing_key     | 8 | cyan   | SigningPublicKey, 128 bytes or as specified in destination's key cert
num             | 1 | red    | Integer, 1 byte, number of leases (0-16)
Lease 0         | 7 | yellow | Lease, 44 bytes
Lease 1         | 8 | yellow | Lease, 44 bytes
Lease ($num-1)  | 8 | yellow | Lease, 44 bytes
signature       | 8 | purple | Signature, 40 bytes or as specified in destination's key cert

```
<details class="content-section">
<summary>View original ASCII diagram</summary>

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

destination :: `Destination`
               length -> >= 387+ bytes

encryption_key :: `PublicKey`
                  length -> 256 bytes

signing_key :: `SigningPublicKey`
               length -> 128 bytes or as specified in destination's key
                         certificate

num :: `Integer`
       length -> 1 byte
       Number of leases to follow
       value: 0 <= num <= 16

leases :: [`Lease`]
          length -> $num*44 bytes

signature :: `Signature`
             length -> 40 bytes or as specified in destination's key
                       certificate
```

</details>
#### Description

* La clé de chiffrement est utilisée pour le chiffrement de bout en bout ElGamal/AES+SessionTag
  [ELGAMAL-AES](/docs/specs/elgamal-aes/). Elle est actuellement générée à nouveau à chaque démarrage du router, elle n'est
  pas persistante.

* La signature peut être vérifiée en utilisant la clé publique de signature de la destination.

* Un LeaseSet avec zéro Leases est autorisé mais n'est pas utilisé.
  Il était destiné à la révocation de LeaseSet, qui n'est pas implémentée.
  Toutes les variantes de LeaseSet2 nécessitent au moins un Lease.

* La signing_key est actuellement inutilisée. Elle était destinée à la révocation de leaseSet, qui n'est pas implémentée. Elle est actuellement générée à nouveau à chaque démarrage du router, elle n'est pas persistante. Le type de clé de signature est toujours le même que le type de clé de signature de la destination.

* L'expiration la plus précoce de tous les Leases est traitée comme l'horodatage ou la version du LeaseSet. Les routeurs n'accepteront généralement pas le stockage d'un LeaseSet à moins qu'il ne soit "plus récent" que l'actuel. Soyez prudent lors de la publication d'un nouveau LeaseSet où le Lease le plus ancien est le même que le Lease le plus ancien dans le LeaseSet précédent. Le routeur de publication devrait généralement incrémenter l'expiration du Lease le plus ancien d'au moins 1 ms dans ce cas.

* Avant la version 0.9.7, lorsqu'inclus dans un message DatabaseStore envoyé par le router d'origine, le router définissait toutes les expirations des leases publiés à la même valeur, celle du lease le plus ancien. À partir de la version 0.9.7, le router publie l'expiration réelle du lease pour chaque lease. Il s'agit d'un détail d'implémentation et non d'une partie de la spécification des structures.

* Taille totale : 40 octets

JavaDoc : [net.i2p.data.LeaseSet](http://docs.i2p-projekt.de/net/i2p/data/LeaseSet.html)

### Lease2

#### Sommaire

Définit l'autorisation pour un tunnel particulier de recevoir des messages ciblant une [Destination](#destination). Identique à [Lease](#lease) mais avec un end_date de 4 octets. Utilisé par [LeaseSet2](#leaseset2). Pris en charge depuis la version 0.9.38 ; voir la proposition 123 pour plus d'informations.

#### Notes

Le hachage SHA256 [Hash](#hash) du [RouterIdentity](#routeridentity) du routeur passerelle, suivi du [TunnelId](#tunnelid), puis d'une date de fin sur 4 octets.

```bytefield
tunnel_gw   | 8 | blue   | Hash of the RouterIdentity of the tunnel gateway, 32 bytes

tunnel_id   | 4 | green  | TunnelId, 4 bytes
end_date    | 4 | yellow | 4 byte date, seconds since epoch, rolls over in 2106
```
<details class="content-section">
<summary>View original ASCII diagram</summary>

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

tunnel_gw :: Hash of the `RouterIdentity` of the tunnel gateway
             length -> 32 bytes

tunnel_id :: `TunnelId`
             length -> 4 bytes

end_date :: 4 byte date
            length -> 4 bytes
            Seconds since the epoch, rolls over in 2106.
```

</details>
#### Description

* Cette section peut, et devrait, être générée hors ligne.

JavaDoc: [net.i2p.data.Lease2](http://docs.i2p-projekt.de/net/i2p/data/Lease2.html)

### OfflineSignature

#### Sommaire

Il s'agit d'une partie facultative de l'élément [LeaseSet2Header](#leaseset2header). Également utilisé dans le streaming et I2CP. Pris en charge depuis la version 0.9.38 ; voir la proposition 123 pour plus d'informations.

#### Notes

Contient une expiration, un sigtype et une [SigningPublicKey](#signingpublickey) transitoire, et une [Signature](#signature).

```bytefield
expires              | 4 | yellow | 4 byte date, seconds since epoch, rolls over in 2106
sigtype              | 2 | cyan   | 2 byte type of the transient_public_key
_ | 2
transient_public_key | 8 | green  | SigningPublicKey, as inferred from sigtype

signature            | 8 | purple | Signature, as inferred from sigtype of the Destination's key

```
<details class="content-section">
<summary>View original ASCII diagram</summary>

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

expires :: 4 byte date
           length -> 4 bytes
           Seconds since the epoch, rolls over in 2106.

sigtype :: 2 byte type of the transient_public_key
           length -> 2 bytes

transient_public_key :: `SigningPublicKey`
                        length -> As inferred from the sigtype

signature :: `Signature`
             length -> As inferred from the sigtype of the signing public key
                       in the `Destination` that preceded this offline signature.
             Signature of expires timestamp, transient sig type, and public key,
             by the destination public key.
```

</details>
#### Description

* **Flags** (2 octets) :
  * Bit 0 : Si défini, les clés hors ligne sont présentes (voir [OfflineSignature](#offlinesignature))
  * Bit 1 : Si défini, il s'agit d'un leaseSet non publié
  * Bit 2 : Si défini, il s'agit d'un leaseSet aveugle
  * Bits 15-3 : Réservés, définis à 0

### LeaseSet2Header

#### Sommaire

Ceci est la partie commune du [LeaseSet2](#leaseset2) et du [MetaLeaseSet](#metaleaseset). Pris en charge depuis la version 0.9.38 ; voir la proposition 123 pour plus d'informations.

#### Notes

Contient la [Destination](#destination), deux horodatages, et une [OfflineSignature](#offlinesignature) optionnelle.

```bytefield
destination          | 8 | blue   | Destination, >= 387+ bytes

published            | 4 | yellow | 4 byte date, seconds since epoch, rolls over in 2106
expires              | 2 | cyan   | 2 byte time, offset from published in seconds, 18.2 hours max
flags                | 2 | red
offline_signature    | 8 | purple | OfflineSignature, varies, optional (present if flags bit 0 set

```
<details class="content-section">
<summary>View original ASCII diagram</summary>

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

destination :: `Destination`
               length -> >= 387+ bytes

published :: 4 byte date
             length -> 4 bytes
             Seconds since the epoch, rolls over in 2106.

expires :: 2 byte time
           length -> 2 bytes
           Offset from published timestamp in seconds, 18.2 hours max

flags :: 2 bytes
  Bit order: 15 14 ... 3 2 1 0
  Bit 0: If 0, no offline keys; if 1, offline keys
  Bit 1: If 0, a standard published leaseset.
         If 1, an unpublished leaseset.
  Bit 2: If 0, a standard published leaseset.
         If 1, this unencrypted leaseset will be blinded and encrypted when published.
  Bits 15-3: set to 0 for compatibility with future uses

offline_signature :: `OfflineSignature`
                     length -> varies
                     Optional, only present if bit 0 is set in the flags.
```

</details>
#### Description

* Taille totale : 395 octets minimum

* Le temps d'expiration réel maximum est d'environ 660 (11 minutes) pour
  [LeaseSet2](#leaseset2) et 65535 (les 18,2 heures complètes) pour [MetaLeaseSet](#metaleaseset).

* [LeaseSet](#leaseset) (1) n'avait pas de champ 'published', donc le versioning nécessitait
  une recherche du lease le plus ancien. LeaseSet2 ajoute un champ 'published'
  avec une résolution d'une seconde. Les routers devraient limiter le débit d'envoi
  de nouveaux leasesets vers les floodfills à un taux beaucoup plus lent qu'une fois par seconde (par destination).
  Si cela n'est pas implémenté, alors le code doit s'assurer que chaque nouveau leaseset
  a un temps 'published' d'au moins une seconde plus tard que le précédent, sinon
  les floodfills ne stockeront pas ou ne diffuseront pas le nouveau leaseset.

- serviceoption := optionkey optionvalue
- optionkey := _service._proto
- service := Le nom symbolique du service désiré. Doit être en minuscules. Exemple : "smtp".
  Les caractères autorisés sont [a-z0-9-] et ne doivent pas commencer ou finir par un '-'.
  Les identifiants standards du [REGISTRY](http://www.dns-sd.org/ServiceTypes.html) ou de Linux /etc/services doivent être utilisés s'ils y sont définis.
- proto := Le protocole de transport du service désiré. Doit être en minuscules, soit "tcp" soit "udp".
  "tcp" signifie streaming et "udp" signifie datagrammes avec réponse possible.
  Les indicateurs de protocole pour les datagrammes bruts et datagram2 pourront être définis ultérieurement.
  Les caractères autorisés sont [a-z0-9-] et ne doivent pas commencer ou finir par un '-'.
- optionvalue := self | srvrecord[,srvrecord]*
- self := "0" ttl port [appoptions]
- srvrecord := "1" ttl priority weight port target [appoptions]
- ttl := durée de vie, en secondes entières. Entier positif. Exemple : "86400".
  Un minimum de 86400 (un jour) est recommandé, voir la section Recommandations ci-dessous pour plus de détails.
- priority := La priorité de l'hôte cible, une valeur plus faible signifie plus préféré. Entier non négatif. Exemple : "0"
  Utile seulement s'il y a plus d'un enregistrement, mais requis même s'il n'y a qu'un seul enregistrement.
- weight := Un poids relatif pour les enregistrements avec la même priorité. Une valeur plus élevée signifie plus de chances d'être sélectionné. Entier non négatif. Exemple : "0"
  Utile seulement s'il y a plus d'un enregistrement, mais requis même s'il n'y a qu'un seul enregistrement.
- port := Le port I2CP sur lequel le service doit être trouvé. Entier non négatif. Exemple : "25"
  Le port 0 est supporté mais non recommandé.
- target := Le nom d'hôte ou b32 de la destination fournissant le service. Un nom d'hôte valide comme dans [NAMING](/docs/overview/naming/). Doit être en minuscules.
  Exemple : "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.b32.i2p" ou "example.i2p".
  Le b32 est recommandé sauf si le nom d'hôte est "bien connu", c'est-à-dire dans les carnets d'adresses officiels ou par défaut.
- appoptions := texte arbitraire spécifique à l'application, ne doit pas contenir " " ou ",". L'encodage est UTF-8.

### LeaseSet2

#### Sommaire

Contenu dans un message I2NP de type DatabaseStore 3. Pris en charge depuis la version 0.9.38 ; voir la proposition 123 pour plus d'informations.

Contient tous les [Lease2](#lease2) actuellement autorisés pour une [Destination](#destination) particulière, et la [PublicKey](#publickey) avec laquelle les messages garlic peuvent être chiffrés. Un LeaseSet est l'une des deux structures stockées dans la base de données réseau (l'autre étant [RouterInfo](#routerinfo)), et est indexé sous le SHA256 de la [Destination](#destination) contenue.

#### Préférence de clé de chiffrement

[LeaseSet2Header](#leaseset2header), suivi par des options, puis une ou plusieurs [PublicKey](#publickey) pour le chiffrement, un [Integer](#integer) indiquant le nombre de structures [Lease2](#lease2) présentes dans l'ensemble, suivi des structures [Lease2](#lease2) elles-mêmes, et enfin une [Signature](#signature) des octets précédents signée par la [SigningPrivateKey](#signingprivatekey) du [Destination](#destination) ou par la clé transitoire.

```bytefield
ls2_header       | 8 | blue   | LeaseSet2Header, varies
options          | 8 | gray   | Mapping, varies, 2 bytes minimum
numk             | 2 | red    | Integer, 1 byte, number of encryption keys (1 <= numk <= max TBD)
keytype0         | 3 | cyan   | Encryption type of PublicKey, 2 bytes
keylen0          | 3 | cyan   | Length of PublicKey, 2 bytes
encryption_key_0 | 8 | green  | PublicKey, keylen bytes
keytypen         | 4 | cyan   | Encryption type of PublicKey, 2 bytes
keylenn          | 4 | cyan   | Length of PublicKey, 2 bytes
encryption_key_n | 8 | green  | PublicKey, keylen bytes
num              | 1 | red    | Integer, 1 byte, number of Lease2s (0-16)
Lease2 0         | 7 | yellow | Lease2, 40 bytes
Lease2 ($num-1)  | 8 | yellow | Lease2, 40 bytes
signature        | 8 | purple | Signature, 40 bytes or as specified in destination's key cert
```
<details class="content-section">
<summary>View original ASCII diagram</summary>

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

ls2header :: `LeaseSet2Header`
             length -> varies

options :: `Mapping`
           length -> varies, 2 bytes minimum

numk :: `Integer`
        length -> 1 byte
        Number of key types, key lengths, and `PublicKey`s to follow
        value: 1 <= numk <= max TBD

keytype :: The encryption type of the `PublicKey` to follow.
           length -> 2 bytes

keylen :: The length of the `PublicKey` to follow.
          Must match the specified length of the encryption type.
          length -> 2 bytes

encryption_key :: `PublicKey`
                  length -> keylen bytes

num :: `Integer`
       length -> 1 byte
       Number of `Lease2`s to follow
       value: 0 <= num <= 16

leases :: [`Lease2`]
          length -> $num*40 bytes

signature :: `Signature`
             length -> 40 bytes or as specified in destination's key
                       certificate, or by the sigtype of the transient public key,
                       if present in the header
```

</details>
#### Options

Pour les leasesets publiés (serveur), les clés de chiffrement sont classées par ordre de préférence du serveur, la plus préférée en premier. Si les clients prennent en charge plus d'un type de chiffrement, il est recommandé qu'ils respectent la préférence du serveur et sélectionnent le premier type pris en charge comme méthode de chiffrement à utiliser pour se connecter au serveur. En général, les types de clés plus récents (numérotés plus haut) sont plus sécurisés ou efficaces et sont préférés, donc les clés devraient être listées dans l'ordre inverse du type de clé.

Cependant, les clients peuvent, selon l'implémentation, choisir en fonction de leurs préférences ou utiliser une méthode pour déterminer la préférence « combinée ». Cela peut être utile comme option de configuration ou à des fins de débogage.

L'ordre des clés dans les leasesets non publiés (client) n'a effectivement pas d'importance, car les connexions ne seront généralement pas tentées vers des clients non publiés. À moins que cet ordre ne soit utilisé pour déterminer une préférence combinée, comme décrit ci-dessus.

#### Notes

À compter de l'API 0.9.66, un format standard pour les options des enregistrements de service est défini. Voir la proposition 167 pour plus de détails. Des options autres que les enregistrements de service, utilisant un format différent, pourraient être définies à l'avenir.

Les options LS2 DOIVENT être triées par clé, afin que la signature soit invariante.

Les options d'enregistrement de service sont définies comme suit :

* La clé publique de la destination était utilisée pour l'ancien chiffrement I2CP-vers-I2CP qui a été désactivé dans la version 0.6, elle n'est actuellement pas utilisée.

Exemples :

Dans LS2 pour aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.b32.i2p, pointant vers un serveur SMTP :

"_smtp._tcp" "1 86400 0 0 25 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p"

Dans LS2 pour aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.b32.i2p, pointant vers deux serveurs SMTP :

"_smtp._tcp" "1 86400 0 0 25 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p,86400 1 0 25 cccccccccccccccccccccccccccccccccccccccccccc.b32.i2p"

Dans LS2 pour bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p, pointant vers lui-même en tant que serveur SMTP :

"_smtp._tcp" "0 999999 25"

#### Description

* Les clés de chiffrement sont utilisées pour le chiffrement de bout en bout ElGamal/AES+SessionTag
  [ELGAMAL-AES](/docs/specs/elgamal-aes/) (type 0) ou d'autres schémas de chiffrement de bout en bout.
  Voir [ECIES](/docs/specs/ecies/) et les propositions 145 et 156.
  Elles peuvent être générées à nouveau à chaque démarrage du router
  ou elles peuvent être persistantes.
  X25519 (type 4, voir [ECIES](/docs/specs/ecies/)) est pris en charge depuis la version 0.9.44.

* La signature porte sur les données ci-dessus, PRÉCÉDÉES par l'octet unique
  contenant le type DatabaseStore (3).

* La signature peut être vérifiée en utilisant la clé publique de signature de la destination, ou la clé publique de signature transitoire, si une signature hors ligne est incluse dans l'en-tête du leaseset2.

* La longueur de clé est fournie pour chaque clé, afin que les floodfills et les clients puissent analyser la structure même si tous les types de chiffrement ne sont pas connus ou pris en charge.

* Voir la note sur le champ 'published' dans [LeaseSet2Header](#leaseset2header)

* Le mappage des options, si la taille est supérieure à un, doit être trié par clé, afin que la signature soit invariante.

* Taille totale : 40 octets

JavaDoc : [net.i2p.data.LeaseSet2](http://docs.i2p-projekt.de/net/i2p/data/LeaseSet2.html)

### MetaLease

#### Contenu

PRÉLIMINAIRE. Prise en charge pas encore complète.

Définit l'autorisation pour un tunnel particulier de recevoir des messages ciblant une [Destination](#destination). Identique à [Lease2](#lease2) mais avec des drapeaux et un coût au lieu d'un identifiant de tunnel. Utilisé par [MetaLeaseSet](#metaleaseset). Contenu dans un message I2NP DatabaseStore de type 7. Pris en charge à partir de la version 0.9.38 ; voir la proposition 123 pour plus d'informations.

#### Notes

SHA256 du [Hash](#hash) du [RouterIdentity](#routeridentity) du routeur passerelle, puis les indicateurs et le coût, et enfin une date de fin sur 4 octets.

```bytefield
tunnel_gw | 8 | blue   | Hash of the RouterIdentity of the tunnel gateway, 32 bytes
flags     | 3 | red    | 3 bytes
cost      | 1 | green  | 1 byte
end_date  | 4 | yellow | 4 bytes, seconds since epoch
```
<details class="content-section">
<summary>View original ASCII diagram</summary>

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

tunnel_gw :: Hash of the `RouterIdentity` of the tunnel gateway,
             or the hash of another `MetaLeaseSet`.
             length -> 32 bytes

flags :: 3 bytes of flags
         Bit order: 23 22 ... 3 2 1 0
         Bits 3-0: Type of the entry.
         If 0, unknown.
         If 1, a `LeaseSet`.
         If 3, a `LeaseSet2`.
         If 5, a `MetaLeaseSet`.
         Bits 23-4: set to 0 for compatibility with future uses
         length -> 3 bytes

cost :: 1 byte, 0-255. Lower value is higher priority.
        length -> 1 byte

end_date :: 4 byte date
            length -> 4 bytes
            Seconds since the epoch, rolls over in 2106.

```
</details>
#### Description

* La clé publique de la destination était utilisée pour l'ancien chiffrement I2CP vers I2CP qui a été désactivé dans la version 0.6, elle n'est actuellement pas utilisée.

JavaDoc : [net.i2p.data.MetaLease](http://docs.i2p-projekt.de/net/i2p/data/MetaLease.html)

### MetaLeaseSet

#### Sommaire

PRÉLIMINAIRE. Prise en charge pas encore complète.

Contenu dans un message I2NP de type DatabaseStore 7. Défini depuis la version 0.9.38 ; voir la proposition 123 pour plus d'informations.

Contient tous les [MetaLease](#metalease) actuellement autorisés pour un [Destination](#destination) donné, ainsi que la [PublicKey](#publickey) permettant de chiffrer les messages au moyen du chiffrement garlic. Un LeaseSet est l'une des deux structures stockées dans la base de données du réseau (l'autre étant [RouterInfo](#routerinfo)) et est indexé selon le hachage SHA256 du [Destination](#destination) qu'il contient.

#### Notes

[LeaseSet2Header](#leaseset2header), suivi par des options, un [Integer](#integer) indiquant le nombre de structures [Lease2](#lease2) présentes dans l'ensemble, puis les structures [Lease2](#lease2) elles-mêmes, et enfin une [Signature](#signature) des octets précédents signée par la [SigningPrivateKey](#signingprivatekey) de la [Destination](#destination) ou par la clé transitoire.

```bytefield
ls2_header       | 8 | blue   | LeaseSet2Header, varies
options          | 8 | green  | Mapping, varies, 2 bytes minimum
num              | 1 | red    | Integer, 1 byte
MetaLease 0      | 7 | yellow | 40 bytes
MetaLease ($num-1) | 8 | yellow | 40 bytes
numr             | 1 | red    | Integer, 1 byte
revocation_0     | 8 | cyan   | Hash, 32 bytes
revocation_n     | 8 | cyan   | Hash, 32 bytes
signature        | 8 | purple | Signature, 40+ bytes
```
<details class="content-section">
<summary>View original ASCII diagram</summary>

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

ls2header :: `LeaseSet2Header`
             length -> varies

options :: `Mapping`
           length -> varies, 2 bytes minimum

num :: `Integer`
        length -> 1 byte
        Number of `MetaLease`s to follow
        value: 1 <= num <= max TBD

leases :: `MetaLease`s
          length -> $numr*40 bytes

numr :: `Integer`
        length -> 1 byte
        Number of `Hash`es to follow
        value: 0 <= numr <= max TBD

revocations :: [`Hash`]
               length -> $numr*32 bytes

signature :: `Signature`
             length -> 40 bytes or as specified in destination's key
                       certificate, or by the sigtype of the transient public key,
                       if present in the header

```
</details>
#### Description

* La signature porte sur les données ci-dessus, PRÉCÉDÉES par l'octet unique
  contenant le type DatabaseStore (7).

* La signature peut être vérifiée en utilisant la clé publique de signature de la destination, ou la clé publique de signature transitoire, si une signature hors ligne est incluse dans l'en-tête du leaseset2.

* Voir la note sur le champ 'published' dans [LeaseSet2Header](#leaseset2header)

* La clé publique de la destination était utilisée pour l'ancien chiffrement I2CP-vers-I2CP qui a été désactivé dans la version 0.6, elle n'est actuellement pas utilisée.

JavaDoc: [net.i2p.data.MetaLeaseSet](http://docs.i2p-projekt.de/net/i2p/data/MetaLeaseSet.html)

### EncryptedLeaseSet

#### Sommaire

Contenu dans un message I2NP de type DatabaseStore 5. Défini à partir de la version 0.9.38 ; fonctionnel à partir de la version 0.9.39 ; voir la proposition 123 pour plus d'informations.

Seule la clé masquée et la date d'expiration sont visibles en texte clair. Le jeu de baux réel est chiffré.

#### Notes

Un type de signature sur deux octets, la [SigningPrivateKey](#signingprivatekey) masquée, l'horodatage de publication, la date d'expiration et les indicateurs. Puis, une longueur sur deux octets suivie de données chiffrées. Enfin, une [Signature](#signature) des octets précédents signée par la [SigningPrivateKey](#signingprivatekey) masquée ou par la clé transitoire.

```bytefield
sigtype            | 2 | red    | 2 bytes
blinded_public_key | 8 | blue   | SigningPublicKey, varies
published          | 4 | green  | 4 bytes, seconds since epoch
expires            | 2 | yellow | 2 bytes
flags              | 2 | red    | 2 bytes
offline_signature  | 8 | orange | OfflineSignature, optional, varies
len                | 2 | gray   | Integer, 2 bytes
encrypted_data     | 8 | cyan   | Encrypted data, len bytes
signature          | 8 | purple | Signature, varies
```
<details class="content-section">
<summary>View original ASCII diagram</summary>

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
```
</details>
#### Description

* La signature porte sur les données ci-dessus, PRÉCÉDÉES du byte unique contenant le type DatabaseStore (5).

* La signature peut être vérifiée en utilisant la clé publique de signature de la
  destination, ou la clé publique de signature transitoire, si une signature hors ligne
  est incluse dans l'en-tête du leaseset2.

* L'aveuglement et le chiffrement sont spécifiés dans [EncryptedLeaseSet](/docs/specs/encryptedleaseset/)

* Cette structure n'utilise pas le [LeaseSet2Header](#leaseset2header).

* Le temps d'expiration réel maximum est d'environ 660 (11 minutes), sauf
  s'il s'agit d'un [MetaLeaseSet](#metaleaseset) chiffré.

* Voir la proposition 123 pour des notes sur l'utilisation de signatures hors ligne avec des leaseSets chiffrés.

* Voir la note sur le champ 'published' dans [LeaseSet2Header](#leaseset2header)
  (même problème, même si nous n'utilisons pas le format LeaseSet2Header ici)

* Le coût est typiquement de 5 ou 6 pour SSU, et de 10 ou 11 pour NTCP.

* L'expiration n'est actuellement pas utilisée, toujours nulle (tous des zéros). Depuis la version 0.9.3, l'expiration est supposée être zéro et n'est pas stockée, donc toute expiration non-nulle échouera lors de la vérification de signature du RouterInfo. L'implémentation de l'expiration (ou un autre usage pour ces octets) sera un changement incompatible avec les versions antérieures. Les routers DOIVENT définir ce champ à tous zéros. Depuis la version 0.9.12, un champ d'expiration non-nul est à nouveau reconnu, cependant nous devons attendre plusieurs versions pour utiliser ce champ, jusqu'à ce que la grande majorité du réseau le reconnaisse.

JavaDoc: [net.i2p.data.EncryptedLeaseSet](http://docs.i2p-projekt.de/net/i2p/data/EncryptedLeaseSet.html)

### RouterAddress

#### Sommaire

Cette structure définit les moyens de contacter un routeur via un protocole de transport.

#### Notes

1 octet [Integer](#integer) définissant le coût relatif d'utilisation de l'adresse, où 0 signifie gratuit et 255 coûteux, suivi de la [Date](#date) d'expiration après laquelle l'adresse ne devrait plus être utilisée, ou, si nulle, l'adresse n'expire jamais. Suit ensuite une [String](#string) définissant le protocole de transport utilisé par cette adresse de routeur. Enfin, un [Mapping](#mapping) contient toutes les options spécifiques au transport nécessaires pour établir la connexion, telles que l'adresse IP, le numéro de port, l'adresse e-mail, l'URL, etc.

```bytefield
cost            | 1 | green  | Integer, 1 byte
expiration      | 7 | yellow | Date, 8 bytes
transport_style | 8 | blue   | String, 1-256 bytes
options         | 8 | purple | Mapping
```
<details class="content-section">
<summary>View original ASCII diagram</summary>

```
+----+----+----+----+----+----+----+----+
|cost|           expiration
+----+----+----+----+----+----+----+----+
     |        transport_style           |
+----+----+----+----+-/-+----+----+----+
|                                       |
+                                       +
|               options                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
```
</details>
#### Description

* Les options suivantes, bien qu'elles ne soient pas obligatoires, sont standard et doivent normalement être présentes dans la plupart des adresses de router : "host" (une adresse IPv4 ou IPv6 ou un nom d'hôte) et "port".

* Le peer_size [Integer](#integer) peut être suivi d'une liste contenant autant de hachages de router.
  Ceci n'est actuellement pas utilisé. Cela était destiné à une forme de routes restreintes,
  qui n'est pas implémentée.
  Certaines implémentations peuvent nécessiter que la liste soit triée afin que la signature soit invariante.
  À rechercher avant d'activer cette fonctionnalité.

* La signature peut être vérifiée en utilisant la clé publique de signature du
  router_ident.

* Voir la page de base de données réseau [NETDB-ROUTERINFO](/docs/overview/network-database/#routerinfo) pour les options standard qui
  sont censées être présentes dans tous les router infos.

JavaDoc : [net.i2p.data.router.RouterAddress](http://docs.i2p-projekt.de/net/i2p/data/router/RouterAddress.html)

### RouterInfo

#### Sommaire

Définit toutes les données qu'un router souhaite publier pour que le réseau puisse les voir. Le [RouterInfo](#routerinfo) est l'une des deux structures stockées dans la base de données réseau (l'autre étant [LeaseSet](#leaseset)), et est indexé sous le SHA256 de l'[RouterIdentity](#routeridentity) contenue.

#### Notes

[RouterIdentity](#routeridentity) suivi par la [Date](#date) à laquelle l'entrée a été publiée

```bytefield
router_ident           | 8 | blue   | RouterIdentity, >= 387+ bytes
published              | 8 | green  | Date, 8 bytes
size                   | 1 | red    | Integer, 1 byte
RouterAddress 0        | 7 | yellow | varies
RouterAddress 1        | 8 | yellow | varies
RouterAddress ($size-1)| 8 | yellow | varies
psiz                   | 1 | red    | Integer, 1 byte
options                | 7 | purple | Mapping
signature              | 8 | cyan   | Signature, 40+ bytes
```
<details class="content-section">
<summary>View original ASCII diagram</summary>

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
+----+----+----+----+-/-+----+----+----+
|psiz| options                          |
+----+----+----+----+-/-+----+----+----+
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
```
</details>
#### Notes

* Les très anciens routers exigeaient que les adresses soient triées par le SHA256 de leurs données
  afin que la signature soit invariante.
  Ceci n'est plus requis, et ne vaut pas la peine d'être implémenté pour la rétrocompatibilité.

- [ECIES](/docs/specs/ecies/)
- [ECIES-HYBRID](/docs/specs/ecies-hybrid/)
- [ECIES-ROUTERS](/docs/specs/ecies-routers/)
- [ELGAMAL](/docs/specs/cryptography/#elgamal-legacy)
- [ELGAMAL-AES](/docs/specs/elgamal-aes/)
- [GARLIC-DELIVERY](/docs/specs/i2np/#garlic-clove-delivery-instructions)
- [I2CP](/docs/specs/i2cp/)
- [I2NP](/docs/specs/i2np/)
- [NAMING](/docs/overview/naming/)
- [NETDB-ROUTERINFO](/docs/overview/network-database/#routerinfo)
- [Prop134](/proposals/134-gost/)
- [Prop169](/proposals/169-pq-crypto/)
- [REGISTRY](http://www.dns-sd.org/ServiceTypes.html)
- [SSU](/docs/legacy/ssu/)
- [TUNNEL-DELIVERY](/docs/specs/tunnel-message/#struct-tunnelmessagedeliveryinstructions)

* La signature peut être vérifiée à l'aide de la clé publique de signature de router_ident.

* Voir la page de la base de données réseau [NETDB-ROUTERINFO](/docs/overview/network-database/#routerinfo) pour les options standard qui
  doivent être présentes dans toutes les informations de routeur.

* Les routeurs très anciens exigeaient que les adresses soient triées selon le hachage SHA256 de leurs données afin que la signature reste invariante.  
Cela n'est plus nécessaire, et il n'est pas utile de l'implémenter pour assurer la compatibilité ascendante.

JavaDoc : [net.i2p.data.router.RouterInfo](http://docs.i2p-projekt.de/net/i2p/data/router/RouterInfo.html)

### Instructions de livraison

Les instructions de livraison des messages de tunnel sont définies dans la spécification du message de tunnel [TUNNEL-DELIVERY](/docs/specs/tunnel-message/#struct-tunnelmessagedeliveryinstructions).

Les instructions de livraison des messages garlic sont définies dans la spécification des messages I2NP [GARLIC-DELIVERY](/docs/specs/i2np/#garlic-clove-delivery-instructions).

## Références

- [ECIES](/docs/specs/ecies/)
- [ECIES-HYBRID](/docs/specs/ecies-hybrid/)
- [ECIES-ROUTERS](/docs/specs/ecies-routers/)
- [ELGAMAL](/docs/specs/cryptography/#elgamal-legacy)
- [ELGAMAL-AES](/docs/specs/elgamal-aes/)
- [GARLIC-DELIVERY](/docs/specs/i2np/#garlic-clove-delivery-instructions)
- [I2CP](/docs/specs/i2cp/)
- [I2NP](/docs/specs/i2np/)
- [NOMMAGE](/docs/overview/naming/)
- [NETDB-ROUTERINFO](/docs/overview/network-database/#routerinfo)
- [Prop134](/proposals/134-gost/)
- [Prop169](/proposals/169-pq-crypto/)
- [REGISTRY](http://www.dns-sd.org/ServiceTypes.html)
- [SSU](/docs/legacy/ssu/)
- [TUNNEL-DELIVERY](/docs/specs/tunnel-message/#struct-tunnelmessagedeliveryinstructions)
