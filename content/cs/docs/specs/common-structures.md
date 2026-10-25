---
title: "Specifikace běžných struktur"
description: "Datové typy společné pro všechny I2P protokoly"
slug: "common-structures"
aliases:
  - "/cs/common_structures_spec"
  - "/cs/common_structures_spec/"
category: "Design"
lastUpdated: "2026-10"
accurateFor: "0.9.71"
---

Tento dokument popisuje některé datové typy společné všem I2P protokolům, jako je [I2NP](/docs/specs/i2np/), [I2CP](/docs/specs/i2cp/), [SSU](/docs/legacy/ssu/), atd.

## Specifikace běžného typu

### Celé číslo

#### Popis

Představuje nezáporné celé číslo.

#### Obsah

1 až 8 bajtů v síťovém pořadí bajtů (big endian) reprezentujících neznaménkové celé číslo.

### Datum

#### Popis

Počet milisekund od půlnoci 1. ledna 1970 v časovém pásmu GMT. Pokud je číslo 0, datum je nedefinované nebo null.

#### Obsah

8 bajtový [Integer](#integer)

### Řetězec

#### Popis

Představuje řetězec kódovaný v UTF-8.

#### Obsah

1 nebo více bajtů, kde první bajt je počet bajtů (ne znaků!) v řetězci a zbývajících 0-255 bajtů je pole znaků kódované v UTF-8 bez ukončení nulovým znakem. Limit délky je 255 bajtů (ne znaků). Délka může být 0.

### PublicKey

#### Popis

Tato struktura se používá v ElGamal nebo jiném asymetrickém šifrování a představuje pouze exponent, nikoli prvočísla, která jsou konstantní a definována ve specifikaci kryptografie [ELGAMAL](/docs/specs/cryptography/#elgamal-legacy). Jiná schémata šifrování jsou v procesu definování, viz tabulka níže.

#### Obsah

Typ a délka klíče jsou odvozeny z kontextu nebo specifikovány v Key Certificate cíle nebo RouterInfo, nebo v polích v [LeaseSet2](#leaseset2) či jiné datové struktuře. Výchozím typem je ElGamal. Od verze 0.9.38 mohou být podporovány další typy v závislosti na kontextu. Klíče jsou ve formátu big-endian, pokud není uvedeno jinak.

Klíče X25519 jsou podporovány v Destinations a LeaseSet2 od vydání 0.9.44. Klíče X25519 jsou podporovány v RouterIdentities od vydání 0.9.48.

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

#### Popis

Tato struktura se používá v ElGamal nebo jiných asymetrických šifrováních, představuje pouze exponent, nikoli prvočísla, která jsou konstantní a definovaná ve specifikaci kryptografie [ELGAMAL](/docs/specs/cryptography/#elgamal-legacy). Další šifrovací schémata jsou v procesu definování, viz tabulka níže.

#### Obsah

Typ a délka klíče jsou odvozeny z kontextu nebo jsou uloženy samostatně v datové struktuře nebo v souboru soukromého klíče. Výchozím typem je ElGamal. Od verze 0.9.38 mohou být podporovány další typy, v závislosti na kontextu. Klíče jsou ve formátu big-endian, pokud není uvedeno jinak.

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

#### Popis

Tato struktura se používá pro symetrické šifrování a dešifrování AES256.

#### Obsah

32 bajtů

JavaDoc: [net.i2p.data.SessionKey](http://docs.i2p-projekt.de/net/i2p/data/SessionKey.html)

### SigningPublicKey

#### Popis

Tato struktura se používá pro ověřování podpisů.

#### Obsah

Typ a délka klíče jsou odvozeny z kontextu nebo jsou specifikovány v Key Certificate příslušného Destination. Výchozím typem je DSA_SHA1. Od verze 0.9.12 mohou být podporovány i další typy v závislosti na kontextu.

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
#### Poznámky

* Když je klíč složen ze dvou prvků (například body X,Y), je serializován tak, že se každý prvek doplní na délku/2 s úvodními nulami, pokud je to nutné.

* Všechny typy jsou Big Endian, kromě EdDSA a RedDSA, které jsou ukládány a přenášeny
  ve formátu Little Endian.

JavaDoc: [net.i2p.data.SigningPublicKey](http://docs.i2p-projekt.de/net/i2p/data/SigningPublicKey.html)

### SigningPrivateKey

#### Popis

Tato struktura se používá pro vytváření podpisů.

#### Obsah

Typ a délka klíče jsou specifikovány při vytvoření. Výchozí typ je DSA_SHA1. Od verze 0.9.12 mohou být podporovány další typy v závislosti na kontextu.

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
#### Poznámky

* Když je klíč složen ze dvou prvků (například body X,Y), je serializován tak, že se každý prvek doplní na délku/2 úvodními nulami, pokud je to nutné.

* Všechny typy jsou Big Endian, kromě EdDSA a RedDSA, které jsou uloženy a přenášeny
  ve formátu Little Endian.

JavaDoc: [net.i2p.data.SigningPrivateKey](http://docs.i2p-projekt.de/net/i2p/data/SigningPrivateKey.html)

### Podpis

#### Popis

Tato struktura představuje podpis nějakých dat.

#### Obsah

Typ a délka podpisu se odvozují z typu použitého klíče. Výchozím typem je DSA_SHA1. Od verze 0.9.12 mohou být podporovány i jiné typy, v závislosti na kontextu.

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
#### Poznámky

* Když je podpis složen ze dvou prvků (například hodnoty R,S), je serializován tak, že každý prvek je doplněn na délku/2 úvodními nulami, pokud je to nutné.

* Všechny typy jsou Big Endian, kromě EdDSA a RedDSA, které jsou uloženy a přenášeny
  ve formátu Little Endian.

JavaDoc: [net.i2p.data.Signature](http://docs.i2p-projekt.de/net/i2p/data/Signature.html)

### Hash

#### Popis

Představuje SHA256 hash některých dat.

#### Obsah

32 bajtů

JavaDoc: [net.i2p.data.Hash](http://docs.i2p-projekt.de/net/i2p/data/Hash.html)

### Značka relace

Poznámka: Session Tags pro ECIES-X25519 destinace (ratchet) a ECIES-X25519 routery mají 8 bajtů. Viz [ECIES](/docs/specs/ecies/) a [ECIES-ROUTERS](/docs/specs/ecies-routers/).

#### Popis

Náhodné číslo

#### Obsah

32 bajtů

JavaDoc: [net.i2p.data.SessionTag](http://docs.i2p-projekt.de/net/i2p/data/SessionTag.html)

### TunnelId

#### Popis

Definuje identifikátor, který je jedinečný pro každý router v tunnelu. Tunnel ID je obecně větší než nula; nepoužívejte hodnotu nula kromě zvláštních případů.

#### Obsah

4 bajtové [Integer](#integer)

JavaDoc: [net.i2p.data.TunnelId](http://docs.i2p-projekt.de/net/i2p/data/TunnelId.html)

### Certifikát

#### Popis

Certifikát je kontejner pro různé doklady nebo důkazy prací používané v síti I2P.

#### Obsah

1 byte [Integer](#integer) specifikující typ certifikátu, následovaný 2 byte [Integer](#integer) specifikujícím velikost dat certifikátu, poté tolik bytů.

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
#### Poznámky

* Pro [Router Identities](#routeridentity) je Certificate vždy NULL až do verze
  0.9.15. Od verze 0.9.16 se používá Key Certificate pro specifikaci
  typů klíčů. Od verze 0.9.48 jsou povoleny typy veřejných šifrovacích klíčů X25519. Viz níže.

* Pro [Garlic Cloves](/docs/specs/i2np/#struct-garlicclove) je Certificate vždy NULL, žádné jiné nejsou v současnosti
  implementovány.

* Pro [Garlic Messages](/docs/specs/i2np/#msg-garlic) je Certificate vždy NULL, žádné jiné nejsou v současnosti implementovány.

* Pro [Destinations](#destination) může být Certificate nenulový. Od verze 0.9.12 může být Key Certificate použit k určení typu veřejného podepisovacího klíče. Viz níže.

* Implementátorům se doporučuje zakázat nadbytečná data v certifikátech.
  Měla by být vynucena odpovídající délka pro každý typ certifikátu.

#### Typy certifikátů

Jsou definovány následující typy certifikátů:

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
#### Klíčové certifikáty

Klíčové certifikáty byly zavedeny ve verzi 0.9.12. Před touto verzí byly všechny PublicKeys 256-bajtové ElGamal klíče a všechny SigningPublicKeys byly 128-bajtové DSA-SHA1 klíče. Klíčový certifikát poskytuje mechanismus k označení typu PublicKey a SigningPublicKey v Destination nebo RouterIdentity a k zabalení jakýchkoli klíčových dat přesahujících standardní délky.

Udržováním přesně 384 bajtů před certifikátem a umístěním jakýchkoli přebytečných klíčových dat do certifikátu zachováváme kompatibilitu pro jakýkoli software, který parsuje Destinations a Router Identities.

Obsah certifikátu klíče obsahuje:

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
Varování: Pořadí typů klíčů je opačné, než byste mohli očekávat; typ podpisového veřejného klíče je první.

Definované typy veřejných klíčů pro podepisování jsou:

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
Definované typy kryptografických veřejných klíčů jsou:

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
Když Key Certificate není přítomen, předchozích 384 bytů v Destination nebo RouterIdentity je definováno jako 256-bytový ElGamal PublicKey následovaný 128-bytovým DSA-SHA1 SigningPublicKey. Když je Key Certificate přítomen, předchozích 384 bytů je redefinováno následovně:

* Kompletní nebo první část kryptografického veřejného klíče

* Náhodné vyplnění, pokud je celková délka obou klíčů menší než 384 bajtů

* Úplná nebo první část veřejného klíče pro podepisování

Crypto Public Key je zarovnán na začátku a Signing Public Key je zarovnán na konci. Padding (pokud existuje) je uprostřed. Délky a hranice počátečních klíčových dat, paddingu a přebytečných klíčových dat v certifikátech nejsou explicitně specifikovány, ale jsou odvozeny z délek specifikovaných typů klíčů. Pokud celková délka Crypto a Signing Public Keys překročí 384 bajtů, zbytek bude obsažen v Key Certificate. Pokud délka Crypto Public Key není 256 bajtů, metoda pro určení hranice mezi dvěma klíči bude specifikována v budoucí revizi tohoto dokumentu.

Příklady rozložení používající ElGamal Crypto Public Key a uvedený typ Signing Public Key:

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

#### Poznámky

* Implementátoři jsou upozorněni, aby zakázali nadměrná data v Key Certificates.
  Měla by být vynucována odpovídající délka pro každý typ certifikátu.

* KEY certifikát s typy 0,0 (ElGamal,DSA_SHA1) je povolen, ale nedoporučuje se.
  Není dobře otestován a může způsobovat problémy v některých implementacích.
  Použijte NULL certifikát v kanonické reprezentaci
  (ElGamal,DSA_SHA1) Destination nebo RouterIdentity, což bude o 4 bajty kratší
  než použití KEY certifikátu.

### Mapování

#### Popis

Sada mapování klíč/hodnota nebo vlastností

#### Obsah

2-bajtové celé číslo velikosti následované řadou párů String=String;.

VAROVÁNÍ: Většina použití Mapping je v podepsaných strukturách, kde musí být položky Mapping seřazeny podle klíče, aby byl podpis neměnný. Neseřazení podle klíče bude mít za následek selhání podpisu!

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
#### Poznámky

* Kódování není optimální - potřebujeme buď znaky '=' a ';', nebo délky řetězců, ale ne oboje

#### Popis

* Některá dokumentace uvádí, že řetězce nesmí obsahovat '=' nebo ';', ale toto kódování je podporuje

* Řetězce jsou definovány jako UTF-8, ale v současné implementaci I2CP používá UTF-8, zatímco I2NP ne. Například UTF-8 řetězce v mapování možností RouterInfo ve zprávě I2NP Database Store budou poškozeny.

* Kódování umožňuje duplicitní klíče, avšak při jakémkoli použití, kde je mapování podepsané, mohou duplicity způsobit selhání podpisu.

* Mapování obsažená v I2NP zprávách (např. v RouterAddress nebo RouterInfo)
  musí být seřazena podle klíče, aby byl podpis neměnný. Duplicitní klíče
  nejsou povoleny.

* Mapování obsažená v [I2CP SessionConfig](/docs/specs/i2cp/#struct-sessionconfig) musí být seřazena podle klíče, aby byl podpis neměnný. Duplicitní klíče nejsou povoleny.

* Metoda řazení je definována stejně jako v Java String.compareTo(), používající Unicode hodnotu znaků.

* Ačkoli to závisí na aplikaci, klíče a hodnoty jsou obecně citlivé na velikost písmen.

* Limity délky řetězců klíče a hodnoty jsou 255 bajtů (ne znaků) každý, plus
  bajt délky. Bajt délky může být 0.

* Celkový limit délky je 65535 bajtů, plus 2bajtové pole velikosti, nebo celkem 65537.

* Router Identity s typem šifrování X25519 a typem podpisu Ed25519
  bude obsahovat 10 kopií (320 bajtů) náhodných dat, což při kompresi ušetří přibližně 288 bajtů.

JavaDoc: [net.i2p.data.DataHelper](http://docs.i2p-projekt.de/net/i2p/data/DataHelper.html)

## Specifikace společné struktury

### KeysAndCert

#### Obsah

Veřejný klíč pro šifrování, veřejný klíč pro podepisování a certifikát, používané buď jako RouterIdentity nebo Destination.

#### Směrnice pro generování výplně

[PublicKey](#publickey) následovaný [SigningPublicKey](#signingpublickey) a poté [Certificate](#certificate).

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
#### Poznámky

Tyto pokyny byly navrženy v Návrhu 161 a implementovány v API verzi 0.9.57. Tyto pokyny jsou zpětně kompatibilní se všemi verzemi od 0.6 (2005). Pro kontext a další informace viz Návrh 161.

Pro jakoukoliv aktuálně používanou kombinaci typů klíčů jinou než ElGamal + DSA-SHA1 bude přítomno vyplnění. Navíc pro cíle je 256-bytové pole veřejného klíče nepoužívané od verze 0.6 (2005).

Implementátoři by měli generovat náhodná data pro veřejné klíče Destination a padding pro identitu Destination a router tak, aby byla kompresibilní v různých I2P protokolech a zároveň zůstala bezpečná, a aby Base 64 reprezentace nevypadaly jako poškozené nebo nebezpečné. Toto poskytuje většinu výhod odstranění padding polí bez jakýchkoli rušivých změn protokolu.

Přísně vzato, samotný 32-bytový veřejný klíč pro podepisování (jak v Destinations, tak v Router Identities) a 32-bytový veřejný klíč pro šifrování (pouze v Router Identities) je náhodné číslo, které poskytuje veškerou entropii potřebnou k tomu, aby SHA-256 hashe těchto struktur byly kryptograficky silné a náhodně distribuované v netDb DHT.

Pro maximální opatrnost však doporučujeme použít minimálně 32 bajtů náhodných dat v poli veřejného klíče ElG a ve výplni. Navíc, pokud by všechna pole byla nulová, Base 64 destinace by obsahovaly dlouhé sekvence znaků AAAA, což by mohlo vyvolat poplach nebo zmatení u uživatelů.

Opakujte 32 bajtů náhodných dat podle potřeby tak, aby byla celá struktura KeysAndCert vysoce kompresibilní v I2P protokolech jako je I2NP Database Store Message, Streaming SYN, SSU2 handshake a repliable Datagrams.

Příklady:

* Destination s typem podpisu Ed25519
  bude obsahovat 11 kopií (352 bajtů) náhodných dat, což při kompresi ušetří přibližně 320 bajtů.

* Nepředpokládejte, že mají vždy 387 bajtů! Mají 387 bajtů plus délku certifikátu specifikovanou na bajtech 385-386, která může být nenulová.

Implementace musí samozřejmě ukládat celou strukturu o velikosti 387+ bytů, protože SHA-256 hash struktury pokrývá celý obsah.

#### Popis

* Od vydání 0.9.12, pokud je certifikát Key Certificate, hranice polí klíčů se mohou lišit. Podrobnosti najdete v sekci Key Certificate výše.

* Kryptografický veřejný klíč je zarovnán na začátku a podepisující veřejný klíč je zarovnán na konci. Výplň (pokud existuje) je uprostřed.

* Certifikát pro RouterIdentity byl vždy NULL až do vydání 0.9.12.

JavaDoc: [net.i2p.data.KeysAndCert](http://docs.i2p-projekt.de/net/i2p/data/KeysAndCert.html)

### RouterIdentity

#### Obsah

Definuje způsob, jak jednoznačně identifikovat konkrétní router

#### Poznámky

Identické s KeysAndCert.

Viz [KeysAndCert](#keysandcert) pro pokyny k generování náhodných dat pro pole padding.

#### Popis

* Nepředpokládejte, že tyto jsou vždy 387 bajtů! Jsou to 387 bajtů plus délka certifikátu specifikovaná na bajtech 385-386, která může být nenulová.

* Od verze 0.9.12, pokud je certifikát Key Certificate, hranice polí klíčů se mohou lišit. Podrobnosti najdete v sekci Key Certificate výše.

* Kryptografický veřejný klíč je zarovnán na začátku a podepisovací veřejný klíč je zarovnán na konci. Výplň (pokud existuje) je uprostřed.

* RouterIdentity s certifikátem klíče a veřejným klíčem ECIES_X25519
  jsou podporovány od verze 0.9.48.
  Před tím byly všechny RouterIdentity typu ElGamal.

* Veřejný klíč destinace byl použit pro staré i2cp-to-i2cp šifrování, které bylo zakázáno ve verzi 0.6 (2005), v současnosti je nepoužíván kromě IV pro LeaseSet šifrování, které je zastaralé. Místo toho se používá veřejný klíč v LeaseSet.

JavaDoc: [net.i2p.data.router.RouterIdentity](http://docs.i2p-projekt.de/net/i2p/data/router/RouterIdentity.html)

### Cíl

#### Obsah

Destination definuje konkrétní koncový bod, kam mohou být zprávy směrovány pro bezpečné doručení.

#### Poznámky

Identické s [KeysAndCert](#keysandcert), s výjimkou toho, že veřejný klíč se nikdy nepoužívá a může obsahovat náhodná data namísto platného ElGamal veřejného klíče.

Viz [KeysAndCert](#keysandcert) pro pokyny k generování náhodných dat pro pole veřejného klíče a výplně.

#### Popis

* Nepředpokládejte, že mají vždy 387 bajtů! Mají 387 bajtů plus délku certifikátu specifikovanou na bajtech 385-386, která může být nenulová.

* Od vydání 0.9.12, pokud je certifikát Key Certificate, hranice polí klíčů se mohou lišit. Podrobnosti najdete v sekci Key Certificate výše.

* Crypto Public Key je zarovnán na začátku a Signing Public Key je zarovnán na konci. Výplň (pokud existuje) je uprostřed.

* Veřejný klíč cíle byl použit pro staré I2CP-to-I2CP šifrování, které bylo zakázáno ve verzi 0.6, v současnosti se nepoužívá.

JavaDoc: [net.i2p.data.Destination](http://docs.i2p-projekt.de/net/i2p/data/Destination.html)

### Lease

#### Obsah

ZASTARALÉ. Použijte LeaseSet2 a Lease2.

Definuje autorizaci konkrétního tunelu pro příjem zpráv určených pro [cíl](#destination).

#### Popis

SHA256 [hash](#hash) [RouterIdentity](#routeridentity) brány, poté [TunnelId](#tunnelid) a nakonec koncové [Datum](#date).

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
JavaDoc: [net.i2p.data.Lease](http://docs.i2p-projekt.de/net/i2p/data/Lease.html)

### LeaseSet

#### Obsah

ZASTARALÉ. Použijte LeaseSet2 a Lease2.

Obsahuje všechny aktuálně autorizované [Leases](#lease) pro konkrétní [Destination](#destination), [PublicKey](#publickey), na který lze šifrovat garlic zprávy, a dále [SigningPublicKey](#signingpublickey), který lze použít k odvolání této konkrétní verze struktury. LeaseSet je jednou ze dvou struktur uložených v síťové databázi (druhou je [RouterInfo](#routerinfo)) a je indexován pod SHA256 obsaženého [Destination](#destination).

#### Poznámky

[Destination](#destination), následovaná [PublicKey](#publickey) pro šifrování, poté [SigningPublicKey](#signingpublickey), který lze použít k odvolání této verze LeaseSet, pak 1 byte [Integer](#integer) specifikující kolik struktur [Lease](#lease) je v sadě, následované skutečnými strukturami [Lease](#lease) a nakonec [Signature](#signature) předchozích bytů podepsaná [SigningPrivateKey](#signingprivatekey) [Destination](#destination).

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
#### Popis

* Šifrovací klíč se používá pro end-to-end ElGamal/AES+SessionTag šifrování
  [ELGAMAL-AES](/docs/specs/elgamal-aes/). V současnosti se generuje znovu při každém spuštění routeru, není
  trvalý.

* Podpis může být ověřen pomocí veřejného podepisovacího klíče cíle.

* LeaseSet s nulou Lease je povolen, ale nepoužívá se.
  Byl určen pro revokaci LeaseSet, což není implementováno.
  Všechny varianty LeaseSet2 vyžadují alespoň jeden Lease.

* signing_key je v současnosti nepoužíván. Byl zamýšlen pro zrušení LeaseSet,
  které není implementováno. V současnosti se generuje znovu při každém spuštění routeru,
  není perzistentní. Typ signing key je vždy stejný jako
  typ signing key cíle.

* Nejdřívější vypršení všech Lease je považováno za časovou značku nebo verzi LeaseSet. Routery obecně nepřijmou uložení LeaseSet, pokud není "novější" než současný. Buďte opatrní při publikování nového LeaseSet, kde nejstarší Lease je stejný jako nejstarší Lease v předchozím LeaseSet. Publikující router by v takovém případě měl obecně zvýšit vypršení nejstaršího Lease alespoň o 1 ms.

* Před verzí 0.9.7, když byl zahrnut ve zprávě DatabaseStore odeslané původním routerem, router nastavil všechna vypršení publikovaných leaseů na stejnou hodnotu, tu nejčasnějšího lease. Od verze 0.9.7 router publikuje skutečné vypršení lease pro každý lease. Toto je implementační detail a není součástí specifikace struktur.

* Celková velikost: 40 bajtů

JavaDoc: [net.i2p.data.LeaseSet](http://docs.i2p-projekt.de/net/i2p/data/LeaseSet.html)

### Lease2

#### Obsah

Definuje autorizaci pro konkrétní tunnel přijímat zprávy zaměřené na [Destination](#destination). Stejné jako [Lease](#lease), ale se 4-bytovým end_date. Používá se v [LeaseSet2](#leaseset2). Podporováno od verze 0.9.38; pro více informací viz návrh 123.

#### Poznámky

SHA256 [hash](#hash) [RouterIdentity](#routeridentity) brány, poté [TunnelId](#tunnelid) a nakonec 4 bajty určující koncové datum.

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
#### Popis

* Tato sekce může a měla by být vygenerována offline.

JavaDoc: [net.i2p.data.Lease2](http://docs.i2p-projekt.de/net/i2p/data/Lease2.html)

### OfflineSignature

#### Obsah

Toto je volitelná část [LeaseSet2Header](#leaseset2header). Používá se také ve streamování a I2CP. Podporováno od verze 0.9.38; více informací viz návrh 123.

#### Poznámky

Obsahuje expiraci, sigtype a přechodný [SigningPublicKey](#signingpublickey) a [Signature](#signature).

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
#### Popis

* **Flags** (2 bajty):
  * Bit 0: Pokud je nastaven, jsou přítomny offline klíče (viz [OfflineSignature](#offlinesignature))
  * Bit 1: Pokud je nastaven, jedná se o nepublikovaný leaseset
  * Bit 2: Pokud je nastaven, jedná se o zaslepený leaseset
  * Bity 15-3: Rezervováno, nastaveno na 0

### LeaseSet2Header

#### Obsah

Toto je společná část [LeaseSet2](#leaseset2) a [MetaLeaseSet](#metaleaseset). Podporováno od verze 0.9.38; více informací viz návrh 123.

#### Poznámky

Obsahuje [Destination](#destination), dvě časová razítka a volitelný [OfflineSignature](#offlinesignature).

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
#### Popis

* Celková velikost: minimálně 395 bajtů

* Maximální skutečný čas vypršení je přibližně 660 (11 minut) pro
  [LeaseSet2](#leaseset2) a 65535 (plných 18,2 hodiny) pro [MetaLeaseSet](#metaleaseset).

* [LeaseSet](#leaseset) (1) neměl pole 'published', takže verzování vyžadovalo
  hledání nejstaršího lease. LeaseSet2 přidává pole 'published'
  s rozlišením jedné sekundy. Routery by měly omezovat rychlost odesílání
  nových leaseset do floodfill na rychlost mnohem pomalejší než jednou za sekundu (na destinaci).
  Pokud to není implementováno, pak kód musí zajistit, že každý nový leaseset
  má čas 'published' nejméně o sekundu pozdější než předchozí, jinak
  floodfill neuloží ani nezaplavní nový leaseset.

- serviceoption := optionkey optionvalue
- optionkey := _service._proto
- service := Symbolické jméno požadované služby. Musí být psané malými písmeny. Příklad: "smtp".
  Povolené znaky jsou [a-z0-9-] a nesmí začínat nebo končit znakem '-'.
  Musí být použity standardní identifikátory z [REGISTRY](http://www.dns-sd.org/ServiceTypes.html) nebo Linux /etc/services, pokud jsou tam definovány.
- proto := Transportní protokol požadované služby. Musí být psán malými písmeny, buď "tcp" nebo "udp".
  "tcp" znamená streamování a "udp" znamená odpověditelné datagramy.
  Indikátory protokolů pro surové datagramy a datagram2 mohou být definovány později.
  Povolené znaky jsou [a-z0-9-] a nesmí začínat nebo končit znakem '-'.
- optionvalue := self | srvrecord[,srvrecord]*
- self := "0" ttl port [appoptions]
- srvrecord := "1" ttl priority weight port target [appoptions]
- ttl := doba života, celočíselné sekundy. Kladné číslo. Příklad: "86400".
  Doporučuje se minimum 86400 (jeden den), podrobnosti viz sekce Doporučení níže.
- priority := Priorita cílového hostitele, nižší hodnota znamená vyšší preference. Nezáporné číslo. Příklad: "0"
  Užitečné pouze při více než jednom záznamu, ale vyžadované i při jediném záznamu.
- weight := Relativní váha pro záznamy se stejnou prioritou. Vyšší hodnota znamená větší šanci výběru. Nezáporné číslo. Příklad: "0"
  Užitečné pouze při více než jednom záznamu, ale vyžadované i při jediném záznamu.
- port := I2CP port, na kterém má být služba nalezena. Nezáporné číslo. Příklad: "25"
  Port 0 je podporován, ale není doporučen.
- target := Hostname nebo b32 cíle poskytujícího službu. Platný hostname podle [NAMING](/docs/overview/naming/). Musí být psán malými písmeny.
  Příklad: "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.b32.i2p" nebo "example.i2p".
  b32 je doporučeno, pokud hostname není "dobře známý", tj. v oficiálních nebo výchozích adresářích.
- appoptions := libovolný text specifický pro aplikaci, nesmí obsahovat " " nebo ",". Kódování je UTF-8.

### LeaseSet2

#### Obsah

Obsaženo ve zprávě I2NP DatabaseStore typu 3. Podporováno od verze 0.9.38; více informací viz návrh 123.

Obsahuje všechny aktuálně autorizované [Lease2](#lease2) pro konkrétní [Destination](#destination) a [PublicKey](#publickey), kterým mohou být garlic zprávy šifrovány. LeaseSet je jedna ze dvou struktur uložených v síťové databázi (druhou je [RouterInfo](#routerinfo)) a je klíčována pod SHA256 obsaženého [Destination](#destination).

#### Preference šifrovacího klíče

[LeaseSet2Header](#leaseset2header), následovaný volbami, poté jedním nebo více [PublicKey](#publickey) pro šifrování, [Integer](#integer) udávající počet struktur [Lease2](#lease2) v sadě, následovanými skutečnými strukturami [Lease2](#lease2) a nakonec [Signature](#signature) předchozích bajtů podepsanou [SigningPrivateKey](#signingprivatekey) [Destination](#destination) nebo přechodným klíčem.

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
#### Možnosti

Pro publikované (serverové) leaseSety jsou šifrovací klíče seřazeny podle preference serveru, s nejpreferovanějším jako prvním. Pokud klienti podporují více než jeden typ šifrování, doporučuje se, aby respektovali preferenci serveru a vybrali první podporovaný typ jako šifrovací metodu pro připojení k serveru. Obecně jsou novější (s vyšším číslem) typy klíčů bezpečnější nebo efektivnější a jsou preferované, takže klíče by měly být uvedeny v opačném pořadí podle typu klíče.

Klienti však mohou v závislosti na implementaci vybírat podle svých preferencí nebo použít nějakou metodu k určení „kombinované“ preference. To může být užitečné jako konfigurační možnost nebo pro účely ladění.

Pořadí klíčů v nepublikovaných (klientských) leaseStech v podstatě nezáleží, protože spojení obvykle nebudou pokoušena k nepublikovaným klientům. Pokud se toto pořadí nepoužívá k určení kombinované preference, jak je popsáno výše.

#### Poznámky

Od API 0.9.66 je definován standardní formát pro možnosti záznamu služby. Podrobnosti viz návrh 167. Možnosti jiné než záznamy služeb, používající jiný formát, mohou být definovány v budoucnu.

Volby LS2 MUSÍ být seřazeny podle klíče, takže podpis je neměnný.

Možnosti záznamu služby jsou definovány následovně:

* Veřejný klíč cílového uzlu byl používán pro staré I2CP-to-I2CP šifrování, které bylo zakázáno ve verzi 0.6, v současnosti se nepoužívá.

Příklady:

V LS2 pro aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.b32.i2p, odkazující na jeden SMTP server:

"_smtp._tcp" "1 86400 0 0 25 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p"

V LS2 pro aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.b32.i2p, který odkazuje na dva servery SMTP:

"_smtp._tcp" "1 86400 0 0 25 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p,86400 1 0 25 cccccccccccccccccccccccccccccccccccccccccccc.b32.i2p"

V LS2 pro bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p, který odkazuje sám na sebe jako na SMTP server:

"_smtp._tcp" "0 999999 25"

#### Popis

* Šifrovací klíče se používají pro end-to-end ElGamal/AES+SessionTag šifrování
  [ELGAMAL-AES](/docs/specs/elgamal-aes/) (typ 0) nebo jiná end-to-end šifrovací schémata.
  Viz [ECIES](/docs/specs/ecies/) a návrhy 145 a 156.
  Mohou být generovány znovu při každém spuštění routeru
  nebo mohou být trvalé.
  X25519 (typ 4, viz [ECIES](/docs/specs/ecies/)) je podporováno od verze 0.9.44.

* Podpis je nad daty výše, PŘEDŘAZENÝMI jedním bytem
  obsahujícím typ DatabaseStore (3).

* Podpis může být ověřen pomocí veřejného klíče pro podepisování destinace, nebo přechodného veřejného klíče pro podepisování, pokud je offline podpis zahrnut v hlavičce leaseset2.

* Délka klíče je poskytována pro každý klíč, takže floodfill a klienti mohou analyzovat strukturu i v případě, že nejsou všechny typy šifrování známé nebo podporované.

* Viz poznámka k poli 'published' v [LeaseSet2Header](#leaseset2header)

* Mapování možností, pokud je velikost větší než jedna, musí být seřazeno podle klíče, aby byl podpis neměnný.

* Celková velikost: 40 bytů

JavaDoc: [net.i2p.data.LeaseSet2](http://docs.i2p-projekt.de/net/i2p/data/LeaseSet2.html)

### MetaLease

#### Obsah

PŘEDBĚŽNÉ. Plně podporováno není.

Definuje autorizaci pro konkrétní tunnel pro přijímání zpráv cílených na [Destination](#destination). Stejné jako [Lease2](#lease2), ale s příznaky a cenou namísto tunnel id. Používá [MetaLeaseSet](#metaleaseset). Obsaženo v I2NP DatabaseStore zprávě typu 7. Podporováno od verze 0.9.38; viz návrh 123 pro více informací.

#### Poznámky

SHA256 [hash](#hash) [RouterIdentity](#routeridentity) brány, poté příznaky a cena a nakonec 4bytové datum ukončení.

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
#### Popis

* Veřejný klíč destinace byl používán pro staré I2CP-to-I2CP šifrování, které bylo zakázáno ve verzi 0.6, v současnosti se nepoužívá.

JavaDoc: [net.i2p.data.MetaLease](http://docs.i2p-projekt.de/net/i2p/data/MetaLease.html)

### MetaLeaseSet

#### Obsah

PŘEDBĚŽNÉ. Plně podporováno není.

Obsaženo ve zprávě I2NP DatabaseStore typu 7. Definováno od verze 0.9.38; více informací viz návrh 123.

Obsahuje všechny aktuálně autorizované [MetaLease](#metalease) pro konkrétní [Destination](#destination) a [PublicKey](#publickey), na který lze šifrovat garlic zprávy. LeaseSet je jednou ze dvou struktur uložených v síťové databázi (druhou je [RouterInfo](#routerinfo)) a je indexován pomocí SHA256 obsaženého [Destination](#destination).

#### Poznámky

[LeaseSet2Header](#leaseset2header), následovaný možnostmi, [Integer](#integer) udávající počet struktur [Lease2](#lease2) v sadě, následovanými skutečnými strukturami [Lease2](#lease2) a nakonec [Signature](#signature) předchozích bajtů podepsaných [SigningPrivateKey](#signingprivatekey) [Destination](#destination) nebo přechodným klíčem.

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
#### Popis

* Podpis je nad výše uvedenými daty, PŘEDŘAZENÝMI s jediným bajtem
  obsahujícím typ DatabaseStore (7).

* Podpis může být ověřen pomocí veřejného klíče pro podepisování cíle, nebo přechodného veřejného klíče pro podepisování, pokud je v hlavičce leaseset2 zahrnut offline podpis.

* Viz poznámka k poli 'published' v [LeaseSet2Header](#leaseset2header)

* Veřejný klíč cíle byl používán pro staré I2CP-to-I2CP šifrování, které bylo zakázáno ve verzi 0.6, v současnosti se nepoužívá.

JavaDoc: [net.i2p.data.MetaLeaseSet](http://docs.i2p-projekt.de/net/i2p/data/MetaLeaseSet.html)

### EncryptedLeaseSet

#### Obsah

Obsaženo ve zprávě I2NP DatabaseStore typu 5. Definováno od verze 0.9.38; funguje od verze 0.9.39; více informací viz návrh 123.

Ve volném textu jsou viditelné pouze zaslepený klíč a doba platnosti. Skutečná sada nájemních smluv je šifrována.

#### Poznámky

Dvoubajtový typ podpisu, zveřejněný [SigningPrivateKey](#signingprivatekey) s časem zveřejnění, expirací a příznaky. Poté dvoubajtová délka následovaná šifrovanými daty. Nakonec [Signature](#signature) předchozích bajtů podepsaná zoslepeným [SigningPrivateKey](#signingprivatekey) nebo přechodným klíčem.

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
#### Popis

* Podpis je nad výše uvedenými daty, PŘEDPOJENÝMI s jediným bajtem
  obsahujícím typ DatabaseStore (5).

* Podpis může být ověřen pomocí veřejného klíče pro podepisování cíle, nebo přechodného veřejného klíče pro podepisování, pokud je offline podpis zahrnut v hlavičce leaseset2.

* Blinding a šifrování jsou specifikovány v [EncryptedLeaseSet](/docs/specs/encryptedleaseset/)

* Tato struktura nepoužívá [LeaseSet2Header](#leaseset2header).

* Maximální skutečný čas vypršení je přibližně 660 (11 minut), pokud
  se nejedná o zašifrovaný [MetaLeaseSet](#metaleaseset).

* Viz návrh 123 pro poznámky k používání offline podpisů
  s šifrovanými leaseSety.

* Viz poznámka k poli 'published' v [LeaseSet2Header](#leaseset2header)
  (stejný problém, i když zde nepoužíváme formát LeaseSet2Header)

* Cena je typicky 5 nebo 6 pro SSU a 10 nebo 11 pro NTCP.

* Expiration (vypršení platnosti) se v současnosti nepoužívá, vždy null (všechny nuly). Od vydání 0.9.3 se předpokládá nulové expiration a neukládá se, takže jakékoliv nenulové expiration způsobí selhání ověření podpisu RouterInfo. Implementace expiration (nebo jiné použití těchto bajtů) bude změna nekompatibilní zpětně. Routery MUSÍ nastavit toto pole na všechny nuly. Od vydání 0.9.12 je nenulové pole expiration opět rozpoznáváno, nicméně musíme počkat několik vydání, než toto pole použijeme, dokud ho nebude rozpoznávat naprostá většina sítě.

JavaDoc: [net.i2p.data.EncryptedLeaseSet](http://docs.i2p-projekt.de/net/i2p/data/EncryptedLeaseSet.html)

### RouterAddress

#### Obsah

Tato struktura definuje prostředky pro kontaktování směrovače prostřednictvím přenosového protokolu.

#### Poznámky

1 bajt [Integer](#integer) definující relativní náklady na použití adresy, kde 0 znamená zdarma a 255 drahé, následované [Date](#date) vypršením platnosti, po kterém by se adresa neměla používat, nebo pokud je hodnota null, adresa nikdy nevyprší. Dále následuje [String](#string) definující transportní protokol, který tato adresa směrovače používá. Nakonec je zde [Mapping](#mapping) obsahující všechny transportně specifické volby potřebné k navázání spojení, jako je IP adresa, číslo portu, e-mailová adresa, URL atd.

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
#### Popis

* Následující možnosti, ačkoli nejsou vyžadovány, jsou standardní a očekává se, že budou přítomny ve většině router adres: "host" (IPv4 nebo IPv6 adresa nebo název hostitele) a "port".

* Hodnota peer_size [Integer](#integer) může být následována seznamem tolika router hashů.
  Toto se v současnosti nepoužívá. Bylo určeno pro formu omezených tras,
  která není implementována.
  Některé implementace mohou vyžadovat, aby byl seznam seřazen, takže signatura je invariantní.
  Je třeba toto prozkoumat před povolením této funkce.

* Podpis může být ověřen pomocí veřejného podpisového klíče router_ident.

* Viz stránku síťové databáze [NETDB-ROUTERINFO](/docs/overview/network-database/#routerinfo) pro standardní možnosti, které
  se očekávají ve všech router infos.

JavaDoc: [net.i2p.data.router.RouterAddress](http://docs.i2p-projekt.de/net/i2p/data/router/RouterAddress.html)

### RouterInfo

#### Obsah

Definuje všechna data, která chce router publikovat, aby je mohla síť vidět. [RouterInfo](#routerinfo) je jedna ze dvou struktur uložených v síťové databázi (druhou je [LeaseSet](#leaseset)) a je indexována pod SHA256 hash obsaženého [RouterIdentity](#routeridentity).

#### Poznámky

[RouterIdentity](#routeridentity) následované [Date](#date), kdy byl záznam publikován

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
#### Poznámky

* Velmi staré routery vyžadovaly, aby byly adresy seřazeny podle SHA256 jejich dat,
  takže podpis je invariantní.
  To už není vyžadováno a nestojí za implementaci kvůli zpětné kompatibilitě.

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

* Podpis může být ověřen pomocí veřejného klíče pro podepisování z router_ident.

* Viz stránka databáze sítě [NETDB-ROUTERINFO](/docs/overview/network-database/#routerinfo) pro standardní možnosti, které
  se očekávají v informacích všech routerů.

* Velmi staré směrovače vyžadovaly, aby byly adresy seřazeny podle SHA256 jejich dat,
  aby byl podpis neměnný.
  Tento požadavek již není nutný a pro zpětnou kompatibilitu není implementace jeho hodna úsilí.

JavaDoc: [net.i2p.data.router.RouterInfo](http://docs.i2p-projekt.de/net/i2p/data/router/RouterInfo.html)

### Instrukce pro doručení

Pokyny pro doručení tunelové zprávy jsou definovány ve specifikaci tunelové zprávy [TUNNEL-DELIVERY](/docs/specs/tunnel-message/#struct-tunnelmessagedeliveryinstructions).

Instrukce pro doručování Garlic zpráv jsou definovány ve specifikaci I2NP zpráv [GARLIC-DELIVERY](/docs/specs/i2np/#garlic-clove-delivery-instructions).

## Reference

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
