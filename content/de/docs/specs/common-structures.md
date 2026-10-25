---
title: "Spezifikation gemeinsamer Strukturen"
description: "Datentypen, die allen I2P-Protokollen gemeinsam sind"
slug: "common-structures"
category: "Design"
lastUpdated: "2026-10"
accurateFor: "0.9.71"
---

Dieses Dokument beschreibt einige Datentypen, die allen I2P-Protokollen gemeinsam sind, wie [I2NP](/docs/specs/i2np/), [I2CP](/docs/specs/i2cp/), [SSU](/docs/legacy/ssu/), etc.

## Allgemeine Typspezifikation

### Ganzzahl

#### Beschreibung

Stellt eine nicht-negative ganze Zahl dar.

#### Inhalt

1 bis 8 Bytes in Netzwerk-Byte-Reihenfolge (Big Endian), die eine vorzeichenlose Ganzzahl darstellen.

### Datum

#### Beschreibung

Die Anzahl der Millisekunden seit Mitternacht des 1. Januar 1970 in der GMT-Zeitzone. Wenn die Zahl 0 ist, ist das Datum undefiniert oder null.

#### Inhaltsverzeichnis

8 Byte [Integer](#integer)

### Zeichenkette

#### Beschreibung

Stellt eine UTF-8-kodierte Zeichenkette dar.

#### Inhalt

1 oder mehr Bytes, wobei das erste Byte die Anzahl der Bytes (nicht Zeichen!) in der Zeichenkette angibt und die verbleibenden 0-255 Bytes das nicht null-terminierte UTF-8 kodierte Zeichen-Array sind. Das Längenlimit beträgt 255 Bytes (nicht Zeichen). Die Länge kann 0 sein.

### PublicKey

#### Beschreibung

Diese Struktur wird in ElGamal oder anderen asymmetrischen Verschlüsselungsverfahren verwendet und repräsentiert nur den Exponenten, nicht die Primzahlen, die konstant sind und in der Kryptographie-Spezifikation [ELGAMAL](/docs/specs/cryptography/#elgamal-legacy) definiert werden. Andere Verschlüsselungsverfahren befinden sich derzeit in der Definition, siehe die Tabelle unten.

#### Inhalt

Schlüsseltyp und -länge werden aus dem Kontext abgeleitet oder sind im Key Certificate einer Destination oder RouterInfo oder in den Feldern eines [LeaseSet2](#leaseset2) oder einer anderen Datenstruktur angegeben. Der Standardtyp ist ElGamal. Ab Version 0.9.38 können je nach Kontext andere Typen unterstützt werden. Schlüssel sind big-endian, sofern nicht anders angegeben.

X25519-Schlüssel werden in Destinations und LeaseSet2 ab Version 0.9.44 unterstützt. X25519-Schlüssel werden in RouterIdentities ab Version 0.9.48 unterstützt.

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

#### Beschreibung

Diese Struktur wird bei ElGamal oder anderen asymmetrischen Entschlüsselungsverfahren verwendet und repräsentiert nur den Exponenten, nicht die Primzahlen, die konstant sind und in der Kryptografie-Spezifikation [ELGAMAL](/docs/specs/cryptography/#elgamal-legacy) definiert werden. Andere Verschlüsselungsverfahren sind derzeit in der Entwicklung, siehe die Tabelle unten.

#### Inhaltsverzeichnis

Schlüsseltyp und -länge werden aus dem Kontext abgeleitet oder separat in einer Datenstruktur oder einer privaten Schlüsseldatei gespeichert. Der Standardtyp ist ElGamal. Ab Version 0.9.38 können je nach Kontext auch andere Typen unterstützt werden. Schlüssel sind big-endian, sofern nicht anders angegeben.

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

#### Beschreibung

Diese Struktur wird für symmetrische AES256-Verschlüsselung und -Entschlüsselung verwendet.

#### Inhaltsverzeichnis

32 Bytes

JavaDoc: [net.i2p.data.SessionKey](http://docs.i2p-projekt.de/net/i2p/data/SessionKey.html)

### SigningPublicKey

#### Beschreibung

Diese Struktur wird zur Verifizierung von Signaturen verwendet.

#### Inhalt

Schlüsseltyp und -länge werden aus dem Kontext abgeleitet oder sind im Key Certificate einer Destination angegeben. Der Standardtyp ist DSA_SHA1. Ab Release 0.9.12 können je nach Kontext auch andere Typen unterstützt werden.

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
#### Hinweise

* Wenn ein Schlüssel aus zwei Elementen besteht (zum Beispiel Punkte X,Y), wird er serialisiert, indem jedes Element auf Länge/2 mit führenden Nullen aufgefüllt wird, falls erforderlich.

* Alle Typen sind Big Endian, außer EdDSA und RedDSA, die in einem Little Endian Format gespeichert und übertragen werden.

JavaDoc: [net.i2p.data.SigningPublicKey](http://docs.i2p-projekt.de/net/i2p/data/SigningPublicKey.html)

### SigningPrivateKey

#### Beschreibung

Diese Struktur wird zum Erstellen von Signaturen verwendet.

#### Inhaltsverzeichnis

Schlüsseltyp und -länge werden bei der Erstellung festgelegt. Der Standardtyp ist DSA_SHA1. Ab Release 0.9.12 können je nach Kontext andere Typen unterstützt werden.

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
#### Notizen

* Wenn ein Schlüssel aus zwei Elementen besteht (zum Beispiel Punkte X,Y), wird er serialisiert, indem jedes Element auf Länge/2 mit führenden Nullen aufgefüllt wird, falls erforderlich.

* Alle Typen sind Big Endian, außer EdDSA und RedDSA, die in einem Little Endian Format gespeichert und übertragen werden.

JavaDoc: [net.i2p.data.SigningPrivateKey](http://docs.i2p-projekt.de/net/i2p/data/SigningPrivateKey.html)

### Signatur

#### Beschreibung

Diese Struktur stellt die Signatur einiger Daten dar.

#### Inhaltsverzeichnis

Signaturtyp und -länge werden vom verwendeten Schlüsseltyp abgeleitet. Der Standardtyp ist DSA_SHA1. Ab Version 0.9.12 können je nach Kontext auch andere Typen unterstützt werden.

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
#### Notizen

* Wenn eine Signatur aus zwei Elementen besteht (zum Beispiel Werte R,S), wird sie serialisiert, indem jedes Element auf length/2 mit führenden Nullen aufgefüllt wird, falls nötig.

* Alle Typen sind Big Endian, außer EdDSA und RedDSA, die in einem Little Endian Format gespeichert und übertragen werden.

JavaDoc: [net.i2p.data.Signature](http://docs.i2p-projekt.de/net/i2p/data/Signature.html)

### Hash

#### Beschreibung

Repräsentiert den SHA256-Hashwert von bestimmten Daten.

#### Inhalt

32 Bytes

JavaDoc: [net.i2p.data.Hash](http://docs.i2p-projekt.de/net/i2p/data/Hash.html)

### Session Tag

Hinweis: Session Tags für ECIES-X25519 Ziele (ratchet) und ECIES-X25519 router sind 8 Bytes. Siehe [ECIES](/docs/specs/ecies/) und [ECIES-ROUTERS](/docs/specs/ecies-routers/).

#### Beschreibung

Eine Zufallszahl

#### Inhalt

32 Bytes

JavaDoc: [net.i2p.data.SessionTag](http://docs.i2p-projekt.de/net/i2p/data/SessionTag.html)

### TunnelId

#### Beschreibung

Definiert eine Kennung, die für jeden Router in einem Tunnel eindeutig ist. Eine Tunnel ID ist im Allgemeinen größer als null; verwenden Sie den Wert null nur in besonderen Fällen.

#### Inhalt

4 Byte [Integer](#integer)

JavaDoc: [net.i2p.data.TunnelId](http://docs.i2p-projekt.de/net/i2p/data/TunnelId.html)

### Zertifikat

#### Beschreibung

Ein Zertifikat ist ein Container für verschiedene Belege oder Arbeitsnachweise, die im gesamten I2P-Netzwerk verwendet werden.

#### Inhaltsverzeichnis

1 Byte [Integer](#integer), das den Zertifikatstyp angibt, gefolgt von einem 2 Byte [Integer](#integer), das die Größe der Zertifikatsdaten angibt, dann entsprechend viele Bytes.

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
#### Hinweise

* Für [Router Identities](#routeridentity) ist das Certificate bis Version
  0.9.15 immer NULL. Ab 0.9.16 wird ein Key Certificate verwendet, um die
  Schlüsseltypen zu spezifizieren. Ab 0.9.48 sind X25519-Verschlüsselungs-
  öffentliche Schlüsseltypen erlaubt. Siehe unten.

* Für [Garlic Cloves](/docs/specs/i2np/#struct-garlicclove) ist das Zertifikat immer NULL, keine anderen sind derzeit
  implementiert.

* Für [Garlic Messages](/docs/specs/i2np/#msg-garlic) ist das Zertifikat immer NULL, andere sind derzeit nicht implementiert.

* Für [Destinations](#destination) kann das Zertifikat nicht-NULL sein. Seit Version 0.9.12 kann ein Key Certificate verwendet werden, um den Typ des öffentlichen Signaturschlüssels zu spezifizieren. Siehe unten.

* Implementierer werden davor gewarnt, überschüssige Daten in Zertifikaten zuzulassen.
  Die angemessene Länge für jeden Zertifikatstyp sollte durchgesetzt werden.

#### Zertifikatstypen

Die folgenden Zertifikattypen sind definiert:

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
#### Schlüsselzertifikate

Key-Zertifikate wurden in Release 0.9.12 eingeführt. Vor diesem Release waren alle PublicKeys 256-Byte ElGamal-Schlüssel und alle SigningPublicKeys 128-Byte DSA-SHA1-Schlüssel. Ein Key-Zertifikat stellt einen Mechanismus bereit, um den Typ des PublicKey und SigningPublicKey in der Destination oder RouterIdentity anzugeben und um beliebige Schlüsseldaten zu verpacken, die die Standardlängen überschreiten.

Durch die Beibehaltung von exakt 384 Bytes vor dem Zertifikat und die Platzierung zusätzlicher Schlüsseldaten innerhalb des Zertifikats wahren wir die Kompatibilität für jede Software, die Destinations und Router Identities analysiert.

Die Schlüsselzertifikat-Nutzdaten enthalten:

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
Warnung: Die Reihenfolge der Schlüsseltypen ist das Gegenteil von dem, was Sie erwarten könnten; der Signing Public Key Type steht an erster Stelle.

Die definierten Signing Public Key-Typen sind:

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
Die definierten Crypto Public Key-Typen sind:

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
Wenn kein Key Certificate vorhanden ist, werden die vorhergehenden 384 Bytes in der Destination oder RouterIdentity als der 256-Byte ElGamal PublicKey gefolgt vom 128-Byte DSA-SHA1 SigningPublicKey definiert. Wenn ein Key Certificate vorhanden ist, werden die vorhergehenden 384 Bytes wie folgt neu definiert:

* Vollständiger oder erster Teil des kryptografischen öffentlichen Schlüssels

* Zufällige Auffüllung, wenn die Gesamtlänge der beiden Schlüssel weniger als 384 Bytes beträgt

* Vollständiger oder erster Teil des Signing Public Key

Der Crypto Public Key ist am Anfang ausgerichtet und der Signing Public Key ist am Ende ausgerichtet. Das Padding (falls vorhanden) befindet sich in der Mitte. Die Längen und Grenzen der ursprünglichen Schlüsseldaten, des Paddings und der überschüssigen Schlüsseldatenabschnitte in den Zertifikaten sind nicht explizit spezifiziert, sondern werden aus den Längen der angegebenen Schlüsseltypen abgeleitet. Wenn die Gesamtlängen des Crypto und Signing Public Keys 384 Bytes überschreiten, wird der Rest im Key Certificate enthalten sein. Wenn die Crypto Public Key Länge nicht 256 Bytes beträgt, soll die Methode zur Bestimmung der Grenze zwischen den beiden Schlüsseln in einer zukünftigen Überarbeitung dieses Dokuments spezifiziert werden.

Beispiel-Layouts mit einem ElGamal Crypto Public Key und dem angegebenen Signing Public Key-Typ:

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

#### Notizen

* Implementierer werden darauf hingewiesen, überschüssige Daten in Key Certificates zu verbieten.
  Die angemessene Länge für jeden Zertifikatstyp sollte durchgesetzt werden.

* Ein KEY-Zertifikat mit den Typen 0,0 (ElGamal,DSA_SHA1) ist erlaubt, wird aber nicht empfohlen.
  Es ist nicht gut getestet und kann in manchen Implementierungen zu Problemen führen.
  Verwenden Sie ein NULL-Zertifikat in der kanonischen Darstellung einer
  (ElGamal,DSA_SHA1) Destination oder RouterIdentity, das 4 Bytes kürzer sein wird
  als die Verwendung eines KEY-Zertifikats.

### Zuordnung

#### Beschreibung

Eine Sammlung von Schlüssel-/Wert-Zuordnungen oder Eigenschaften

#### Inhalt

Ein 2-Byte-Größen-Integer gefolgt von einer Reihe von String=String; Paaren.

WARNUNG: Die meisten Verwendungen von Mapping erfolgen in signierten Strukturen, bei denen die Mapping-Einträge nach Schlüssel sortiert werden müssen, damit die Signatur unveränderlich ist. Eine fehlende Sortierung nach Schlüssel führt zu Signaturfehlern!

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
#### Hinweise

* Die Kodierung ist nicht optimal - wir benötigen entweder die '=' und ';' Zeichen, oder die String-Längen, aber nicht beides

#### Beschreibung

* Einige Dokumentation besagt, dass die Zeichenketten möglicherweise nicht '=' oder ';' enthalten dürfen, aber diese Kodierung unterstützt sie

* Strings sind als UTF-8 definiert, aber in der aktuellen Implementierung verwendet I2CP UTF-8, während I2NP dies nicht tut. Zum Beispiel werden UTF-8-Strings in einer RouterInfo-Optionen-Zuordnung in einer I2NP Database Store Message beschädigt.

* Die Kodierung erlaubt doppelte Schlüssel, jedoch kann bei jeder Verwendung, bei der das Mapping signiert ist, das Vorhandensein von Duplikaten zu einem Signaturversagen führen.

* Zuordnungen in I2NP-Nachrichten (z.B. in einer RouterAddress oder RouterInfo) müssen nach Schlüssel sortiert sein, damit die Signatur unveränderlich ist. Doppelte Schlüssel sind nicht erlaubt.

* Zuordnungen, die in einer [I2CP SessionConfig](/docs/specs/i2cp/#struct-sessionconfig) enthalten sind, müssen nach Schlüssel sortiert sein, damit
  die Signatur unveränderlich ist. Doppelte Schlüssel sind nicht erlaubt.

* Die Sortiermethode ist wie in Java String.compareTo() definiert und verwendet die Unicode-Werte der Zeichen.

* Obwohl es anwendungsabhängig ist, sind Schlüssel und Werte im Allgemeinen case-sensitive.

* Die Längenbegrenzungen für Schlüssel- und Wert-Strings betragen jeweils 255 Bytes (nicht Zeichen), plus das Längen-Byte. Das Längen-Byte kann 0 sein.

* Die Gesamtlängenbegrenzung beträgt 65535 Bytes, plus das 2-Byte-Größenfeld, oder insgesamt 65537.

* Eine Router Identity mit X25519-Verschlüsselungstyp und Ed25519-Signaturtyp
  wird 10 Kopien (320 Bytes) der Zufallsdaten enthalten, was eine Einsparung von etwa 288 Bytes bei der Komprimierung ergibt.

JavaDoc: [net.i2p.data.DataHelper](http://docs.i2p-projekt.de/net/i2p/data/DataHelper.html)

## Spezifikation der gemeinsamen Struktur

### KeysAndCert

#### Inhaltsverzeichnis

Ein Verschlüsselungs-Public-Key, ein Signatur-Public-Key und ein Zertifikat, verwendet entweder als RouterIdentity oder als Destination.

#### Richtlinien zur Padding-Generierung

Ein [PublicKey](#publickey) gefolgt von einem [SigningPublicKey](#signingpublickey) und dann einem [Certificate](#certificate).

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
#### Notizen

Diese Richtlinien wurden in Proposal 161 vorgeschlagen und in API-Version 0.9.57 implementiert. Diese Richtlinien sind rückwärtskompatibel mit allen Versionen seit 0.6 (2005). Siehe Proposal 161 für Hintergrundinformationen und weitere Details.

Für jede derzeit verwendete Kombination von Schlüsseltypen außer ElGamal + DSA-SHA1 wird Padding vorhanden sein. Zusätzlich ist bei Zielen das 256-Byte öffentliche Schlüsselfeld seit Version 0.6 (2005) ungenutzt.

Implementierer sollten die Zufallsdaten für öffentliche Destination-Schlüssel sowie für Destination- und Router-Identity-Padding so generieren, dass sie in verschiedenen I2P-Protokollen komprimierbar sind, während sie dennoch sicher bleiben und ohne dass Base-64-Darstellungen beschädigt oder unsicher erscheinen. Dies bietet die meisten Vorteile der Entfernung der Padding-Felder ohne störende Protokolländerungen.

Streng genommen ist der 32-Byte signing public key allein (sowohl in Destinations als auch in Router Identities) und der 32-Byte encryption public key (nur in Router Identities) eine Zufallszahl, die die gesamte Entropie liefert, die erforderlich ist, damit die SHA-256-Hashes dieser Strukturen kryptographisch stark und zufällig in der netDb DHT verteilt sind.

Aus Vorsichtsgründen empfehlen wir jedoch, mindestens 32 Bytes zufällige Daten im ElG Public Key-Feld und Padding zu verwenden. Zusätzlich würden Base 64-Zieladressen bei ausschließlich Null-Feldern lange Folgen von AAAA-Zeichen enthalten, was bei Benutzern Besorgnis oder Verwirrung auslösen könnte.

Wiederhole die 32 Bytes zufälliger Daten nach Bedarf, damit die vollständige KeysAndCert-Struktur in I2P-Protokollen wie I2NP Database Store Message, Streaming SYN, SSU2 handshake und beantwortbaren Datagrammen hochkomprimierbar ist.

Beispiele:

* Eine Destination mit Ed25519-Signaturtyp
  wird 11 Kopien (352 Bytes) der Zufallsdaten enthalten, was eine Ersparnis von etwa 320 Bytes bei der Komprimierung bedeutet.

* Gehen Sie nicht davon aus, dass diese immer 387 Bytes groß sind! Sie sind 387 Bytes plus der Zertifikatslänge, die in den Bytes 385-386 angegeben ist, welche ungleich null sein kann.

Implementierungen müssen natürlich die vollständige 387+ Byte-Struktur speichern, da der SHA-256-Hash der Struktur den gesamten Inhalt abdeckt.

#### Beschreibung

* Ab Release 0.9.12 können sich die Grenzen der Schlüsselfelder variieren, wenn es sich bei dem Zertifikat um ein Key Certificate handelt. Siehe den Abschnitt Key Certificate oben für Details.

* Der Crypto Public Key ist am Anfang ausgerichtet und der Signing Public Key ist am Ende ausgerichtet. Das Padding (falls vorhanden) befindet sich in der Mitte.

* Das Zertifikat für eine RouterIdentity war bis zur Version 0.9.12 immer NULL.

JavaDoc: [net.i2p.data.KeysAndCert](http://docs.i2p-projekt.de/net/i2p/data/KeysAndCert.html)

### RouterIdentity

#### Inhalt

Definiert die Art und Weise, einen bestimmten router eindeutig zu identifizieren

#### Notizen

Identisch mit KeysAndCert.

Siehe [KeysAndCert](#keysandcert) für Richtlinien zur Generierung der Zufallsdaten für das Padding-Feld.

#### Beschreibung

* Gehen Sie nicht davon aus, dass diese immer 387 Bytes haben! Sie sind 387 Bytes plus die Zertifikatslänge, die bei Bytes 385-386 angegeben ist, welche ungleich null sein kann.

* Ab Release 0.9.12 können die Grenzen der Schlüsselfelder variieren, wenn das Zertifikat ein Key Certificate ist. Siehe den Abschnitt Key Certificate oben für Details.

* Der Crypto Public Key ist am Anfang ausgerichtet und der Signing Public Key ist am Ende ausgerichtet. Das Padding (falls vorhanden) befindet sich in der Mitte.

* RouterIdentities mit einem Schlüsselzertifikat und einem ECIES_X25519 öffentlichen Schlüssel
  werden ab Release 0.9.48 unterstützt.
  Davor waren alle RouterIdentities ElGamal.

* Der öffentliche Schlüssel des Ziels wurde für die alte i2cp-zu-i2cp-Verschlüsselung verwendet, die in Version 0.6 (2005) deaktiviert wurde. Er wird derzeit nicht verwendet, außer für den IV für die LeaseSet-Verschlüsselung, welche veraltet ist. Stattdessen wird der öffentliche Schlüssel im LeaseSet verwendet.

JavaDoc: [net.i2p.data.router.RouterIdentity](http://docs.i2p-projekt.de/net/i2p/data/router/RouterIdentity.html)

### Ziel

#### Inhalt

Eine Destination definiert einen bestimmten Endpunkt, an den Nachrichten für eine sichere Zustellung gerichtet werden können.

#### Notizen

Identisch zu [KeysAndCert](#keysandcert), außer dass der öffentliche Schlüssel niemals verwendet wird und möglicherweise Zufallsdaten anstelle eines gültigen ElGamal Public Key enthält.

Siehe [KeysAndCert](#keysandcert) für Richtlinien zur Generierung der Zufallsdaten für die Felder des öffentlichen Schlüssels und der Auffüllung.

#### Beschreibung

* Gehen Sie nicht davon aus, dass diese immer 387 Bytes sind! Sie sind 387 Bytes plus die Zertifikatslänge, die bei den Bytes 385-386 angegeben ist, welche ungleich null sein kann.

* Ab Release 0.9.12 können sich die Grenzen der Schlüsselfelder variieren, wenn das Zertifikat ein Key Certificate ist. Siehe den Abschnitt Key Certificate oben für Details.

* Der Crypto Public Key ist am Anfang ausgerichtet und der Signing Public Key ist am Ende ausgerichtet. Das Padding (falls vorhanden) befindet sich in der Mitte.

* Der öffentliche Schlüssel des Ziels wurde für die alte I2CP-zu-I2CP-Verschlüsselung verwendet, die in Version 0.6 deaktiviert wurde und derzeit nicht genutzt wird.

JavaDoc: [net.i2p.data.Destination](http://docs.i2p-projekt.de/net/i2p/data/Destination.html)

### Lease

#### Inhaltsverzeichnis

VERALTET. Verwenden Sie LeaseSet2 und Lease2.

Definiert die Autorisierung für einen bestimmten Tunnel, Nachrichten zu empfangen, die ein [Ziel](#destination) adressieren.

#### Beschreibung

SHA256-[Hash](#hash) der [RouterIdentity](#routeridentity) des Gateway-Routers, danach die [TunnelId](#tunnelid) und schließlich ein End-[Datum](#date).

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

#### Inhalt

VERALTET. Verwenden Sie LeaseSet2 und Lease2.

Enthält alle derzeit autorisierten [Leases](#lease) für ein bestimmtes [Destination](#destination), den [PublicKey](#publickey), an den verschlüsselte Garlic-Nachrichten gesendet werden können, sowie den [SigningPublicKey](#signingpublickey), der verwendet werden kann, um diese bestimmte Version der Struktur zurückzuziehen. Der LeaseSet ist eine der beiden Strukturen, die in der Netzwerkdatenbank gespeichert werden (die andere ist [RouterInfo](#routerinfo)), und wird unter dem SHA256-Hash des enthaltenen [Destination](#destination) indiziert.

#### Hinweise

[Destination](#destination), gefolgt von einem [PublicKey](#publickey) für die Verschlüsselung, dann einem [SigningPublicKey](#signingpublickey), der verwendet werden kann, um diese Version des LeaseSet zu widerrufen, dann einem 1 Byte [Integer](#integer), der angibt, wie viele [Lease](#lease)-Strukturen in der Menge enthalten sind, gefolgt von den tatsächlichen [Lease](#lease)-Strukturen und schließlich einer [Signature](#signature) der vorherigen Bytes, die mit dem [SigningPrivateKey](#signingprivatekey) der [Destination](#destination) signiert wurde.

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
#### Beschreibung

* Der Verschlüsselungsschlüssel wird für Ende-zu-Ende ElGamal/AES+SessionTag-Verschlüsselung verwendet
  [ELGAMAL-AES](/docs/specs/elgamal-aes/). Er wird derzeit bei jedem router-Start neu generiert und ist
  nicht persistent.

* Die Signatur kann mit dem öffentlichen Signaturschlüssel des Ziels verifiziert werden.

* Ein LeaseSet mit null Leases ist erlaubt, wird aber nicht verwendet.
  Es war für LeaseSet-Widerruf gedacht, was nicht implementiert ist.
  Alle LeaseSet2-Varianten erfordern mindestens ein Lease.

* Der signing_key wird derzeit nicht verwendet. Er war für LeaseSet-Widerruf vorgesehen, was nicht implementiert ist. Er wird derzeit bei jedem router-Start neu generiert und ist nicht persistent. Der signing key-Typ ist immer derselbe wie der signing key-Typ des Ziels.

* Der früheste Ablaufzeitpunkt aller Leases wird als Zeitstempel oder Version des LeaseSet behandelt. Router werden im Allgemeinen keine Speicherung eines LeaseSet akzeptieren, es sei denn, es ist "neuer" als das aktuelle. Seien Sie vorsichtig beim Veröffentlichen eines neuen LeaseSet, bei dem der älteste Lease derselbe ist wie der älteste Lease im vorherigen LeaseSet. Der veröffentlichende Router sollte in diesem Fall im Allgemeinen den Ablaufzeitpunkt des ältesten Lease um mindestens 1 ms erhöhen.

* Vor Version 0.9.7 setzte der router, wenn er in einer DatabaseStore Message vom ursprünglichen router enthalten war, alle Ablaufzeiten der veröffentlichten leases auf denselben Wert, nämlich den des frühesten lease. Ab Version 0.9.7 veröffentlicht der router die tatsächliche lease-Ablaufzeit für jeden lease. Dies ist ein Implementierungsdetail und nicht Teil der Strukturspezifikation.

* Gesamtgröße: 40 bytes

JavaDoc: [net.i2p.data.LeaseSet](http://docs.i2p-projekt.de/net/i2p/data/LeaseSet.html)

### Lease2

#### Inhalt

Definiert die Autorisierung für einen bestimmten tunnel, Nachrichten zu empfangen, die auf ein [Destination](#destination) abzielen. Identisch mit [Lease](#lease), jedoch mit einem 4-Byte end_date. Wird von [LeaseSet2](#leaseset2) verwendet. Unterstützt ab 0.9.38; siehe Vorschlag 123 für weitere Informationen.

#### Notizen

SHA256-[Hash](#hash) der [RouterIdentity](#routeridentity) des Gateway-Routers, dann die [TunnelId](#tunnelid) und schließlich ein 4-Byte-langes Enddatum.

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
#### Beschreibung

* Dieser Abschnitt kann und sollte offline generiert werden.

JavaDoc: [net.i2p.data.Lease2](http://docs.i2p-projekt.de/net/i2p/data/Lease2.html)

### OfflineSignature

#### Inhalt

Dies ist ein optionaler Teil des [LeaseSet2Header](#leaseset2header). Wird ebenfalls in Streaming und I2CP verwendet. Unterstützt ab 0.9.38; weitere Informationen finden sich in Vorschlag 123.

#### Notizen

Enthält ein Ablaufdatum, einen sigtype und einen temporären [SigningPublicKey](#signingpublickey), sowie eine [Signature](#signature).

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
#### Beschreibung

* **Flags** (2 Bytes):
  * Bit 0: Wenn gesetzt, sind Offline-Schlüssel vorhanden (siehe [OfflineSignature](#offlinesignature))
  * Bit 1: Wenn gesetzt, ist dies ein unveröffentlichtes leaseSet
  * Bit 2: Wenn gesetzt, ist dies ein verblendetes leaseSet
  * Bits 15-3: Reserviert, auf 0 setzen

### LeaseSet2Header

#### Inhalt

Dies ist der gemeinsame Teil des [LeaseSet2](#leaseset2) und des [MetaLeaseSet](#metaleaseset). Unterstützt ab 0.9.38; weitere Informationen finden Sie in Vorschlag 123.

#### Hinweise

Enthält das [Destination](#destination), zwei Zeitstempel und eine optionale [OfflineSignature](#offlinesignature).

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
#### Beschreibung

* Gesamtgröße: mindestens 395 Bytes

* Die maximale tatsächliche Ablaufzeit beträgt etwa 660 (11 Minuten) für
  [LeaseSet2](#leaseset2) und 65535 (die vollen 18,2 Stunden) für [MetaLeaseSet](#metaleaseset).

* [LeaseSet](#leaseset) (1) hatte kein 'published'-Feld, daher erforderte die Versionierung
  eine Suche nach dem frühesten Lease. LeaseSet2 fügt ein 'published'-Feld
  mit einer Auflösung von einer Sekunde hinzu. Router sollten das Senden
  neuer leaseSets an floodfills auf eine Rate begrenzen, die viel langsamer ist als einmal pro Sekunde (pro Ziel).
  Wenn dies nicht implementiert wird, muss der Code sicherstellen, dass jedes neue leaseSet
  eine 'published'-Zeit hat, die mindestens eine Sekunde später liegt als das vorherige, andernfalls
  werden floodfills das neue leaseSet nicht speichern oder weiterleiten.

- serviceoption := optionkey optionvalue
- optionkey := _service._proto
- service := Der symbolische Name des gewünschten Dienstes. Muss kleingeschrieben sein. Beispiel: "smtp".
  Erlaubte Zeichen sind [a-z0-9-] und dürfen nicht mit einem '-' beginnen oder enden.
  Standard-Kennungen aus der [REGISTRY](http://www.dns-sd.org/ServiceTypes.html) oder Linux /etc/services müssen verwendet werden, falls dort definiert.
- proto := Das Transportprotokoll des gewünschten Dienstes. Muss kleingeschrieben sein, entweder "tcp" oder "udp".
  "tcp" bedeutet Streaming und "udp" bedeutet antwortfähige Datagramme.
  Protokollindikatoren für rohe Datagramme und datagram2 können später definiert werden.
  Erlaubte Zeichen sind [a-z0-9-] und dürfen nicht mit einem '-' beginnen oder enden.
- optionvalue := self | srvrecord[,srvrecord]*
- self := "0" ttl port [appoptions]
- srvrecord := "1" ttl priority weight port target [appoptions]
- ttl := Lebensdauer, Integer-Sekunden. Positive Ganzzahl. Beispiel: "86400".
  Ein Minimum von 86400 (ein Tag) wird empfohlen, siehe Empfehlungsabschnitt unten für Details.
- priority := Die Priorität des Ziel-Hosts, niedrigerer Wert bedeutet bevorzugt. Nicht-negative Ganzzahl. Beispiel: "0"
  Nur nützlich bei mehr als einem Datensatz, aber erforderlich auch bei nur einem Datensatz.
- weight := Ein relatives Gewicht für Datensätze mit derselben Priorität. Höherer Wert bedeutet größere Chance ausgewählt zu werden. Nicht-negative Ganzzahl. Beispiel: "0"
  Nur nützlich bei mehr als einem Datensatz, aber erforderlich auch bei nur einem Datensatz.
- port := Der I2CP-Port, auf dem der Dienst zu finden ist. Nicht-negative Ganzzahl. Beispiel: "25"
  Port 0 wird unterstützt, aber nicht empfohlen.
- target := Der Hostname oder b32 des Ziels, das den Dienst bereitstellt. Ein gültiger Hostname wie in [NAMING](/docs/overview/naming/). Muss kleingeschrieben sein.
  Beispiel: "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.b32.i2p" oder "example.i2p".
  b32 wird empfohlen, es sei denn der Hostname ist "wohlbekannt", d.h. in offiziellen oder Standard-Adressbüchern.
- appoptions := beliebiger Text spezifisch für die Anwendung, darf keine " " oder "," enthalten. Kodierung ist UTF-8.

### LeaseSet2

#### Inhalt

Enthalten in einer I2NP-DatabaseStore-Nachricht vom Typ 3. Unterstützt ab 0.9.38; siehe Vorschlag 123 für weitere Informationen.

Enthält alle aktuell autorisierten [Lease2](#lease2) für ein bestimmtes [Destination](#destination) und den [PublicKey](#publickey), mit dem garlic messages verschlüsselt werden können. Ein LeaseSet ist eine der beiden Strukturen, die in der Netzwerkdatenbank gespeichert werden (die andere ist [RouterInfo](#routerinfo)), und wird unter dem SHA256 des enthaltenen [Destination](#destination) als Schlüssel gespeichert.

#### Verschlüsselungsschlüssel-Präferenz

[LeaseSet2Header](#leaseset2header), gefolgt von Optionen, dann ein oder mehrere [PublicKey](#publickey) für die Verschlüsselung, eine [Integer](#integer)-Angabe, wie viele [Lease2](#lease2)-Strukturen in dem Set enthalten sind, gefolgt von den eigentlichen [Lease2](#lease2)-Strukturen und schließlich einer [Signature](#signature) der vorherigen Bytes, signiert mit dem [SigningPrivateKey](#signingprivatekey) des [Destination](#destination) oder dem transienten Schlüssel.

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
#### Optionen

Für veröffentlichte (Server) leaseSets sind die Verschlüsselungsschlüssel in der Reihenfolge der Server-Präferenz angeordnet, wobei der bevorzugteste zuerst steht. Wenn Clients mehr als einen Verschlüsselungstyp unterstützen, wird empfohlen, dass sie die Server-Präferenz respektieren und den ersten unterstützten Typ als Verschlüsselungsmethode für die Verbindung zum Server auswählen. Im Allgemeinen sind die neueren (höher nummerierten) Schlüsseltypen sicherer oder effizienter und werden bevorzugt, daher sollten die Schlüssel in umgekehrter Reihenfolge des Schlüsseltyps aufgelistet werden.

Clients können jedoch abhängig von der Implementierung stattdessen basierend auf ihren Präferenzen auswählen oder eine Methode verwenden, um die „kombinierte“ Präferenz zu bestimmen. Dies kann als Konfigurationsoption oder für Debugging-Zwecke nützlich sein.

Die Reihenfolge der Schlüssel in unveröffentlichten (Client) leaseSets spielt praktisch keine Rolle, da normalerweise keine Verbindungsversuche zu unveröffentlichten Clients unternommen werden. Es sei denn, diese Reihenfolge wird verwendet, um eine kombinierte Präferenz zu bestimmen, wie oben beschrieben.

#### Notizen

Ab API 0.9.66 ist ein Standardformat für Optionen von Dienstekontaktdaten definiert. Details finden Sie in Vorschlag 167. Optionen, die keine Dienstekontaktdaten sind und ein anderes Format verwenden, können in Zukunft definiert werden.

LS2-Optionen MÜSSEN nach Schlüssel sortiert sein, damit die Signatur unveränderlich ist.

Die Optionen für den Dienst-Datensatz sind wie folgt definiert:

* Der öffentliche Schlüssel des Ziels wurde für die alte I2CP-zu-I2CP-Verschlüsselung verwendet, die in Version 0.6 deaktiviert wurde und derzeit nicht verwendet wird.

Beispiele:

In LS2 für aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.b32.i2p, verweist auf einen SMTP-Server:

"_smtp._tcp" "1 86400 0 0 25 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p"

In LS2 für aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.b32.i2p, mit Verweis auf zwei SMTP-Server:

"_smtp._tcp" "1 86400 0 0 25 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p,86400 1 0 25 cccccccccccccccccccccccccccccccccccccccccccc.b32.i2p"

In LS2 für bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p, das auf sich selbst als SMTP-Server verweist:

"_smtp._tcp" "0 999999 25"

#### Beschreibung

* Die Verschlüsselungsschlüssel werden für Ende-zu-Ende ElGamal/AES+SessionTag-Verschlüsselung
  [ELGAMAL-AES](/docs/specs/elgamal-aes/) (Typ 0) oder andere Ende-zu-Ende-Verschlüsselungsverfahren verwendet.
  Siehe [ECIES](/docs/specs/ecies/) und Vorschläge 145 und 156.
  Sie können bei jedem router-Start neu generiert werden
  oder sie können persistent sein.
  X25519 (Typ 4, siehe [ECIES](/docs/specs/ecies/)) wird ab Version 0.9.44 unterstützt.

* Die Signatur erstreckt sich über die obigen Daten, VORANGESTELLT mit dem einzelnen Byte, das den DatabaseStore-Typ (3) enthält.

* Die Signatur kann mit dem öffentlichen Signaturschlüssel des Ziels oder dem temporären öffentlichen Signaturschlüssel verifiziert werden, falls eine Offline-Signatur im leaseset2-Header enthalten ist.

* Die Schlüssellänge wird für jeden Schlüssel angegeben, damit floodfills und Clients die Struktur parsen können, auch wenn nicht alle Verschlüsselungstypen bekannt oder unterstützt sind.

* Siehe Hinweis zum 'published' Feld in [LeaseSet2Header](#leaseset2header)

* Das Options-Mapping muss, wenn die Größe größer als eins ist, nach Schlüssel sortiert werden, damit die Signatur unveränderlich ist.

* Gesamtgröße: 40 Bytes

JavaDoc: [net.i2p.data.LeaseSet2](http://docs.i2p-projekt.de/net/i2p/data/LeaseSet2.html)

### MetaLease

#### Inhaltsverzeichnis

VORLÄUFIG. Nicht vollständig unterstützt.

Definiert die Berechtigung für einen bestimmten tunnel, Nachrichten zu empfangen, die auf ein [Destination](#destination) abzielen. Identisch mit [Lease2](#lease2), jedoch mit Flags und Kosten anstelle einer tunnel-ID. Wird von [MetaLeaseSet](#metaleaseset) verwendet. Enthalten in einer I2NP DatabaseStore-Nachricht vom Typ 7. Unterstützt ab Version 0.9.38; siehe Vorschlag 123 für weitere Informationen.

#### Notizen

SHA256-[Hash](#hash) der [RouterIdentity](#routeridentity) des Gateway-Routers, danach Flags und Kosten und schließlich ein 4-Byte-langes Enddatum.

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
#### Beschreibung

* Der öffentliche Schlüssel des Ziels wurde für die alte I2CP-zu-I2CP-Verschlüsselung verwendet, die in Version 0.6 deaktiviert wurde; er wird derzeit nicht verwendet.

JavaDoc: [net.i2p.data.MetaLease](http://docs.i2p-projekt.de/net/i2p/data/MetaLease.html)

### MetaLeaseSet

#### Inhalt

VORLÄUFIG. Nicht vollständig unterstützt.

Enthalten in einer I2NP-DatabaseStore-Nachricht vom Typ 7. Definiert ab 0.9.38; siehe Vorschlag 123 für weitere Informationen.

Enthält alle derzeit autorisierten [MetaLease](#metalease) für ein bestimmtes [Destination](#destination) sowie den [PublicKey](#publickey), mit dem Garlic-Nachrichten verschlüsselt werden können. Ein LeaseSet ist eine der beiden Strukturen, die in der Netzwerkdatenbank gespeichert werden (die andere ist [RouterInfo](#routerinfo)), und wird unter dem SHA256-Hash des enthaltenen [Destination](#destination) indiziert.

#### Hinweise

[LeaseSet2Header](#leaseset2header), gefolgt von Optionen, einer [Integer](#integer)-Angabe, die festlegt, wie viele [Lease2](#lease2)-Strukturen im Set enthalten sind, dann die eigentlichen [Lease2](#lease2)-Strukturen und schließlich eine [Signatur](#signature) der vorherigen Bytes, signiert mit dem [SigningPrivateKey](#signingprivatekey) des [Destination](#destination) oder dem transienten Schlüssel.

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
#### Beschreibung

* Die Signatur erstreckt sich über die obigen Daten, VORANGESTELLT mit dem einzelnen Byte, das den DatabaseStore-Typ (7) enthält.

* Die Signatur kann mit dem öffentlichen Signaturschlüssel des Ziels oder dem temporären öffentlichen Signaturschlüssel verifiziert werden, falls eine Offline-Signatur im leaseset2-Header enthalten ist.

* Siehe Hinweis zum 'published'-Feld in [LeaseSet2Header](#leaseset2header)

* Der öffentliche Schlüssel des Ziels wurde für die alte I2CP-zu-I2CP-Verschlüsselung verwendet, die in Version 0.6 deaktiviert wurde und derzeit nicht genutzt wird.

JavaDoc: [net.i2p.data.MetaLeaseSet](http://docs.i2p-projekt.de/net/i2p/data/MetaLeaseSet.html)

### EncryptedLeaseSet

#### Inhaltsverzeichnis

Enthalten in einer I2NP DatabaseStore-Nachricht vom Typ 5. Definiert ab 0.9.38; funktionsfähig ab 0.9.39; siehe Vorschlag 123 für weitere Informationen.

Nur der verblendete Schlüssel und das Ablaufdatum sind im Klartext sichtbar. Der eigentliche LeaseSet ist verschlüsselt.

#### Notizen

Ein zweibytiges Signaturtyp-Feld, der blinde [SigningPrivateKey](#signingprivatekey), Veröffentlichungszeit, Ablaufzeit und Flags. Danach eine zweibytige Länge, gefolgt von verschlüsselten Daten. Abschließend eine [Signature](#signature) der vorhergehenden Bytes, signiert mit dem blinden [SigningPrivateKey](#signingprivatekey) oder dem transienten Schlüssel.

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
#### Beschreibung

* Die Signatur bezieht sich auf die obigen Daten, VORANGESTELLT mit dem einzelnen Byte, das den DatabaseStore-Typ (5) enthält.

* Die Signatur kann mit dem öffentlichen Signaturschlüssel des Ziels oder dem temporären öffentlichen Signaturschlüssel verifiziert werden, falls eine Offline-Signatur im leaseset2-Header enthalten ist.

* Blinding und Verschlüsselung sind in [EncryptedLeaseSet](/docs/specs/encryptedleaseset/) spezifiziert

* Diese Struktur verwendet nicht den [LeaseSet2Header](#leaseset2header).

* Die maximale tatsächliche Ablaufzeit beträgt etwa 660 (11 Minuten), es sei denn,
  es handelt sich um ein verschlüsseltes [MetaLeaseSet](#metaleaseset).

* Siehe Vorschlag 123 für Hinweise zur Verwendung von Offline-Signaturen mit verschlüsselten leaseSets.

* Siehe Hinweis zum 'published'-Feld in [LeaseSet2Header](#leaseset2header)
  (gleiches Problem, obwohl wir das LeaseSet2Header-Format hier nicht verwenden)

* Die Kosten betragen typischerweise 5 oder 6 für SSU und 10 oder 11 für NTCP.

* Expiration wird derzeit nicht verwendet, immer null (alle Nullen). Ab Release 0.9.3 wird angenommen, dass die Expiration null ist und nicht gespeichert wird, sodass jede Expiration ungleich null bei der RouterInfo-Signaturverifikation fehlschlagen wird. Die Implementierung einer Expiration (oder einer anderen Verwendung für diese Bytes) wird eine rückwärts-inkompatible Änderung sein. Router MÜSSEN dieses Feld auf alle Nullen setzen. Ab Release 0.9.12 wird ein Expiration-Feld ungleich null wieder erkannt, jedoch müssen wir mehrere Releases abwarten, um dieses Feld zu verwenden, bis die große Mehrheit des Netzwerks es erkennt.

JavaDoc: [net.i2p.data.EncryptedLeaseSet](http://docs.i2p-projekt.de/net/i2p/data/EncryptedLeaseSet.html)

### RouterAddress

#### Inhalt

Diese Struktur definiert die Mittel, um einen Router über ein Transportprotokoll zu kontaktieren.

#### Hinweise

1 Byte [Integer](#integer), das die relative Nutzungskosten der Adresse definiert, wobei 0 kostenlos und 255 teuer bedeutet, gefolgt von dem Ablauf-[Datum](#date), nach dem die Adresse nicht mehr verwendet werden sollte; falls null, läuft die Adresse niemals ab. Danach folgt ein [String](#string), der das Transportprotokoll angibt, das diese Routeradresse verwendet. Abschließend folgt eine [Zuordnung](#mapping), die alle transportprotokollspezifischen Optionen enthält, die für den Verbindungsaufbau erforderlich sind, wie z. B. IP-Adresse, Portnummer, E-Mail-Adresse, URL usw.

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
#### Beschreibung

* Die folgenden Optionen sind zwar nicht erforderlich, aber standardmäßig vorhanden und werden in den meisten router-Adressen erwartet: "host" (eine IPv4- oder IPv6-Adresse oder ein Hostname) und "port".

* Die peer_size [Integer](#integer) kann von einer Liste mit entsprechend vielen router-Hashes gefolgt werden.
  Dies wird derzeit nicht verwendet. Es war für eine Form von eingeschränkten Routen gedacht,
  die nicht implementiert ist.
  Bestimmte Implementierungen könnten erfordern, dass die Liste sortiert ist, damit die Signatur unveränderlich ist.
  Dies muss erforscht werden, bevor diese Funktion aktiviert wird.

* Die Signatur kann mit dem öffentlichen Signaturschlüssel der
  router_ident verifiziert werden.

* Siehe die Netzwerkdatenbank-Seite [NETDB-ROUTERINFO](/docs/overview/network-database/#routerinfo) für Standardoptionen, die
  in allen router infos vorhanden sein sollten.

JavaDoc: [net.i2p.data.router.RouterAddress](http://docs.i2p-projekt.de/net/i2p/data/router/RouterAddress.html)

### RouterInfo

#### Inhaltsverzeichnis

Definiert alle Daten, die ein router im Netzwerk veröffentlichen möchte. Die [RouterInfo](#routerinfo) ist eine von zwei Strukturen, die in der netDb gespeichert werden (die andere ist [LeaseSet](#leaseset)), und wird unter dem SHA256-Hash der enthaltenen [RouterIdentity](#routeridentity) indiziert.

#### Notizen

[RouterIdentity](#routeridentity), gefolgt vom [Datum](#datum), wann der Eintrag veröffentlicht wurde

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
#### Hinweise

* Sehr alte router verlangten, dass die Adressen nach dem SHA256 ihrer Daten sortiert werden,
  damit die Signatur unveränderlich ist.
  Dies ist nicht mehr erforderlich und nicht wert, für Rückwärtskompatibilität implementiert zu werden.

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

* Die Signatur kann mit dem öffentlichen Signierschlüssel der router_ident verifiziert werden.

* Siehe die Netzwerkdatenbank-Seite [NETDB-ROUTERINFO](/docs/overview/network-database/#routerinfo) für Standardoptionen, die in allen Router-Infos vorhanden sein sollten.

* Sehr alte Router erforderten, dass die Adressen nach dem SHA256 ihrer Daten sortiert waren, damit die Signatur invariant ist. Dies ist nicht mehr erforderlich und lohnt sich nicht für die Rückwärtskompatibilität.

JavaDoc: [net.i2p.data.router.RouterInfo](http://docs.i2p-projekt.de/net/i2p/data/router/RouterInfo.html)

### Zustellungsanweisungen

Die Anweisungen für die Tunnelnachrichtenübermittlung sind in der Tunnelnachrichtenspezifikation [TUNNEL-DELIVERY](/docs/specs/tunnel-message/#struct-tunnelmessagedeliveryinstructions) definiert.

Garlic Message Delivery Instructions sind in der I2NP Message Specification [GARLIC-DELIVERY](/docs/specs/i2np/#garlic-clove-delivery-instructions) definiert.

## Referenzen

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
