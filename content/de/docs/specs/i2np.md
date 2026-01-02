---
title: "I2P-Netzwerkprotokoll (I2NP)"
description: "Router-zu-Router-Nachrichtenformate, Prioritäten und Größenbeschränkungen innerhalb von I2P."
slug: "i2np"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Übersicht

Das I2P‑Netzwerkprotokoll (I2NP) definiert, wie router Nachrichten austauschen, Transporte auswählen und den Datenverkehr mischen, wobei die Anonymität gewahrt bleibt. Es arbeitet zwischen **I2CP** (Client-API) und den Transportprotokollen (**NTCP2** und **SSU2**).

I2NP ist die Schicht oberhalb der I2P-Transportprotokolle. Es ist ein router-zu-router-Protokoll, das verwendet wird für: - Netzwerkdatenbankabfragen und -antworten - Erstellen von tunnels - Verschlüsselte router- und Client-Datennachrichten

I2NP-Nachrichten können Punkt-zu-Punkt an einen anderen router gesendet werden oder anonym durch tunnels an denselben router.

Router reihen ausgehende Aufgaben anhand lokaler Prioritäten in die Warteschlange ein. Höhere Prioritätswerte werden zuerst verarbeitet. Alles oberhalb der Standardpriorität für tunnel-Daten (400) wird als dringend behandelt.

### Aktuelle Transportprotokolle

I2P verwendet jetzt **NTCP2** (TCP) und **SSU2** (UDP) sowohl für IPv4 als auch für IPv6. Beide Transporte nutzen: - **X25519**-Schlüsselaustausch (Noise-Protokoll-Framework) - **ChaCha20/Poly1305**-authentifizierte Verschlüsselung (AEAD) - **SHA-256**-Hashing

**Veraltete Transportprotokolle entfernt:** - NTCP (ursprüngliches TCP) wurde aus dem Java router mit Version 0.9.50 (Mai 2021) entfernt - SSU v1 (ursprüngliches UDP) wurde aus dem Java router mit Version 2.4.0 (Dezember 2023) entfernt - SSU v1 wurde aus i2pd mit Version 2.44.0 (November 2022) entfernt

Seit 2025 ist das Netzwerk vollständig auf Noise-basierte Transporte umgestellt und bietet keinerlei Unterstützung mehr für Legacy-Transporte.

---

## System zur Versionsnummerierung

**WICHTIG:** I2P verwendet ein doppeltes Versionsschema, das eindeutig verstanden werden muss:

### Release-Versionen (benutzerorientiert)

Dies sind die Versionen, die Nutzer sehen und herunterladen: - 0.9.50 (Mai 2021) - Letzte 0.9.x-Version - **1.5.0** (August 2021) - Erste 1.x-Version - 1.6.0, 1.7.0, 1.8.0, 1.9.0 (von 2021 bis 2022) - **2.0.0** (November 2022) - Erste 2.x-Version - 2.1.0 bis 2.9.0 (von 2023 bis 2025) - **2.10.0** (8. September 2025) - Aktuelle Version

### API-Versionen (Protokollkompatibilität)

Dies sind interne Versionsnummern, die im Feld "router.version" in den RouterInfo-Eigenschaften veröffentlicht werden: - 0.9.50 (Mai 2021) - **0.9.51** (August 2021) - API-Version für Release 1.5.0 - 0.9.52 bis 0.9.66 (fortlaufend über die 2.x-Releases) - **0.9.67** (September 2025) - API-Version für Release 2.10.0

**Wichtiger Hinweis:** Es gab KEINE Releases mit den Versionsnummern 0.9.51 bis 0.9.67. Diese Nummern existieren nur als API-Versionskennungen. I2P sprang von Release 0.9.50 direkt auf 1.5.0.

### Tabelle zur Versionszuordnung

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Release Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">API Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Date</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Features</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.50</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.50</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">May 2021</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Last 0.9.x release, removed NTCP1</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.5.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.51</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">August 2021</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Short tunnel build messages (218 bytes)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.52</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">November 2021</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Various improvements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.7.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.53</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">January 2022</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Performance enhancements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.8.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.54</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">May 2022</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 introduced</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1.9.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.55</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">August 2022</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 improvements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.0.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.56</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">November 2022</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 enabled by default</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.1.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.57</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">January 2023</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Stability improvements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.2.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.58</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">March 2023</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>ElGamal routers deprecated</strong></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.3.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.59</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">May 2023</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Various improvements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.4.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.61</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">December 2023</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Removed SSU1 support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.5.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.62</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">February 2024</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Performance improvements</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.63</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">May 2024</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Network optimizations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.7.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.64</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">October 2024</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Post-quantum preparation work</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.8.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.65</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">February 2025</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Tunnel bandwidth parameters</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.9.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">June 2025</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet service records</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">September 2025</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Post-quantum hybrid cryptography (beta)</td>
    </tr>
  </tbody>
</table>
**Bevorstehend:** Version 2.11.0 (geplant für Dezember 2025) wird Java 17+ voraussetzen und Post-Quanten-Kryptografie standardmäßig aktivieren.

---

## Protokollversionen

Alle router müssen ihre I2NP-Protokollversion im Feld "router.version" in den RouterInfo-Eigenschaften veröffentlichen. Dieses Versionsfeld ist die API-Version, die den Unterstützungsgrad für verschiedene I2NP-Protokollfunktionen angibt, und entspricht nicht notwendigerweise der tatsächlichen Version des routers.

Wenn alternative (nicht-Java) routers Versionsinformationen über die tatsächliche router-Implementierung veröffentlichen möchten, müssen sie dies in einer anderen Eigenschaft tun. Andere als die unten aufgeführten Versionen sind zulässig. Die Unterstützung wird anhand eines numerischen Vergleichs bestimmt; zum Beispiel impliziert 0.9.13 Unterstützung für die Funktionen von 0.9.12.

**Hinweis:** Die Eigenschaft "coreVersion" wird in der router info nicht mehr veröffentlicht und wurde nie zur Bestimmung der I2NP-Protokollversion verwendet.

### Funktionsübersicht nach API-Version

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">API Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Required I2NP Features</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Post-quantum hybrid cryptography (MLKEM ratchet) support (beta), UDP tracker support</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td><td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet2 service record options (see proposal 167)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.65</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Tunnel build bandwidth parameters (see proposal 168)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.59</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimum peers will build tunnels through (as of 0.9.63), minimum floodfill peers will send DSM to (as of 0.9.63)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.58</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimum peers will build tunnels through (as of 0.9.62), <strong>ElGamal routers deprecated</strong></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.55</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SSU2 transport support (if published in router info)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.51</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Short tunnel build messages for ECIES-X25519 routers, minimum peers will build tunnels through (as of 0.9.58), minimum floodfill peers will send DSM to (as of 0.9.58)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.49</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Garlic messages to ECIES-X25519 routers</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.48</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-X25519 routers, ECIES-X25519 build request/response records</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.46</td><td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseLookup flag bit 4 for AEAD reply</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.44</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-X25519 keys in LeaseSet2</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.40</td><td style="border:1px solid var(--color-border); padding:0.5rem;">MetaLeaseSet may be sent in a DSM</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet may be sent in a DSM, RedDSA_SHA512_Ed25519 signature type supported</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td><td style="border:1px solid var(--color-border); padding:0.5rem;">DSM type bits 3-0 now contain the type; LeaseSet2 may be sent in a DSM</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.36</td><td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP2 transport support (if published in router info), minimum peers will build tunnels through (as of 0.9.46)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.28</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA signature types disallowed, minimum floodfill peers will send DSM to (as of 0.9.34)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.18</td><td style="border:1px solid var(--color-border); padding:0.5rem;">DSM type bits 7-1 ignored</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.16</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RI key certs / ECDSA and EdDSA signature types, DLM lookup types (flag bits 3-2), minimum version compatible with the current network</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destination/LeaseSet key certificates with EdDSA Ed25519 signature type (if floodfill)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Destination/LeaseSet key certificates with ECDSA P-256, P-384, and P-521 signature types (if floodfill); non-zero expiration allowed in RouterAddress</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted DSM/DSRM replies supported (DLM flag bit 1) for floodfill routers</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Non-zero DLM flag bits 7-1 allowed</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Requires zero expiration in RouterAddress</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Supports up to 16 leases in a DSM LeaseSet store (previously 6)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">VTBM and VTBRM message support</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Floodfill supports encrypted DSM stores</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">TBM and TBRM messages introduced; minimum version compatible with the current network</td></tr>
  </tbody>
</table>
**Hinweis:** Es gibt außerdem transportbezogene Funktionen und Kompatibilitätsprobleme. Siehe die Transportdokumentation zu NTCP2 und SSU2 für Details.

---

## Nachrichtenkopf

I2NP verwendet eine logische 16-Byte-Headerstruktur, während moderne Transportprotokolle (NTCP2 und SSU2) einen verkürzten 9-Byte-Header verwenden, der redundante Felder für Größe und Prüfsumme weglässt. Die Felder bleiben konzeptionell identisch.

### Vergleich der Header-Formate

**Standardformat (16 Byte):**

Wird im Legacy-NTCP-Transport verwendet sowie wenn I2NP-Nachrichten in andere Nachrichten (TunnelData, TunnelGateway, GarlicClove) eingebettet sind.

```
Bytes 0-15:
+----+----+----+----+----+----+----+----+
|type|      msg_id       |  expiration
+----+----+----+----+----+----+----+----+
                         |  size   |chks|
+----+----+----+----+----+----+----+----+

type :: Integer (1 byte)
        Identifies the message type (see message type table)

msg_id :: Integer (4 bytes)
          Uniquely identifies this message (for some time at least)
          Usually a locally-generated random number, but for outgoing
          tunnel build messages may be derived from the incoming message

expiration :: Date (8 bytes)
              Unix timestamp in milliseconds when this message expires

size :: Integer (2 bytes)
        Length of the payload (0 to ~61.2 KB for tunnel messages)

chks :: Integer (1 byte)
        SHA256 hash of payload truncated to first byte
        Deprecated - NTCP2/SSU2 use ChaCha20/Poly1305 AEAD for integrity
```
**Kurzformat für SSU (veraltet, 5 Bytes):**

```
+----+----+----+----+----+
|type| short_expiration  |
+----+----+----+----+----+

type :: Integer (1 byte)
short_expiration :: Integer (4 bytes, seconds since epoch)
```
**Kurzformat für NTCP2, SSU2 und ECIES-Ratchet Garlic Cloves (Einzelnachrichten innerhalb einer Garlic-Nachricht) (9 Bytes):**

Wird in modernen Transportprotokollen und in ECIES-verschlüsselten garlic messages (I2P-Nachrichtenbündeln) verwendet.

```
+----+----+----+----+----+----+----+----+
|type|      msg_id       | short_expira-
+----+----+----+----+----+----+----+----+
 tion|
+----+

type :: Integer (1 byte)
msg_id :: Integer (4 bytes)
short_expiration :: Integer (4 bytes, seconds since epoch, unsigned)
```
### Details zu Header-Feldern

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Bytes</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Type</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Identifies the message class (0&ndash;255, see message types below)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Unique ID</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Locally unique identifier for matching replies</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Expiration</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8 (standard) / 4 (short)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Timestamp when the message expires. Routers discard expired messages. Short format uses seconds since epoch (unsigned, wraps February 7, 2106)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Payload Length</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Size in bytes (0 to ~61.2 KB for tunnel messages). NTCP2 and SSU2 encode this in their frame headers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Checksum</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated. First byte of SHA-256 hash of the payload. NTCP2/SSU2 use ChaCha20/Poly1305 AEAD for integrity</td>
    </tr>
  </tbody>
</table>
### Hinweise zur Implementierung

- Bei Übertragung über SSU (veraltet) waren nur Typ und eine 4-Byte-Ablaufzeit enthalten
- Bei Übertragung über NTCP2 oder SSU2 wird das 9-Byte-Kurzformat verwendet
- Der standardmäßige 16-Byte-Header ist für I2NP-Nachrichten erforderlich, die in anderen Nachrichten enthalten sind (Data, TunnelData, TunnelGateway, GarlicClove)
- Seit Version 0.8.12 ist die Prüfsummenprüfung an einigen Stellen im Protokollstapel aus Effizienzgründen deaktiviert, die Erzeugung von Prüfsummen ist jedoch aus Kompatibilitätsgründen weiterhin erforderlich
- Die kurze Ablaufzeit ist vorzeichenlos und überläuft am 7. Februar 2106. Nach diesem Datum muss ein Offset hinzugefügt werden, um die korrekte Zeit zu erhalten
- Zur Kompatibilität mit älteren Versionen sind Prüfsummen stets zu erzeugen, auch wenn sie möglicherweise nicht verifiziert werden

---

## Größenbeschränkungen

Tunnel-Nachrichten fragmentieren I2NP-Payloads (Nutzlasten) in Stücke fester Größe: - **Erstes Fragment:** ungefähr 956 Bytes - **Nachfolgende Fragmente:** jeweils ungefähr 996 Bytes - **Maximale Anzahl Fragmente:** 64 (nummeriert 0-63) - **Maximale Payload:** ungefähr 61.200 Bytes (61,2 KB)

**Berechnung:** 956 + (63 × 996) = 63.704 Bytes theoretisches Maximum, mit praktischem Limit von etwa 61.200 Bytes aufgrund von Overhead.

### Historischer Kontext

Ältere Transportprotokolle hatten strengere Grenzwerte für die Frame-Größe: - NTCP: 16 KB große Frames - SSU: ungefähr 32 KB große Frames

NTCP2 unterstützt ungefähr 65-KB-Frames, aber die tunnel-Fragmentierungsgrenze gilt weiterhin.

### Überlegungen zu Anwendungsdaten

Garlic messages (Garlic-Nachrichten) können LeaseSets, Session Tags (Sitzungs-Tags) oder verschlüsselte LeaseSet2-Varianten bündeln, was den verfügbaren Platz für Nutzdaten verringert.

**Empfehlung:** Datagramme sollten ≤ 10 KB groß sein, um eine zuverlässige Übermittlung zu gewährleisten. Nachrichten, die sich dem 61-KB-Limit nähern, können Folgendes aufweisen: - Erhöhte Latenz aufgrund der Reassemblierung fragmentierter Daten - Höhere Wahrscheinlichkeit eines Zustellfehlers - Größere Anfälligkeit für Traffic-Analyse (Verkehrsanalyse)

### Technische Details zur Fragmentierung

Jede tunnel-Nachricht ist genau 1.024 Bytes (1 KB) groß und enthält: - 4-Byte tunnel-ID - 16-Byte Initialisierungsvektor (IV) - 1.004 Bytes verschlüsselter Daten

Innerhalb der verschlüsselten Daten transportieren tunnel-Nachrichten fragmentierte I2NP-Nachrichten mit Fragment-Headern, die Folgendes angeben: - Fragmentnummer (0-63) - Ob dies das erste oder ein Folgefragment ist - Gesamt-Nachrichten-ID zur Wiederzusammensetzung

Das erste Fragment enthält den vollständigen I2NP-Nachrichten-Header (16 Byte), wodurch ungefähr 956 Byte für die Nutzlast verbleiben. Nachfolgende Fragmente enthalten den Nachrichten-Header nicht, sodass pro Fragment ungefähr 996 Byte Nutzlast möglich sind.

---

## Übliche Nachrichtentypen

Routers verwenden den Nachrichtentyp und die Priorität, um ausgehende Aufgaben zu planen. Höhere Prioritätswerte werden zuerst verarbeitet. Die unten aufgeführten Werte entsprechen den aktuellen Standardwerten von Java I2P (Stand API-Version 0.9.67).

**Hinweis:** Die Prioritäten sind implementierungsabhängig. Verbindliche Prioritätswerte finden Sie in der Dokumentation der Klasse `OutNetMessage` im Java-I2P-Quellcode.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Message</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Priority</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Typical Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>DatabaseStore</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">460</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Varies (LeaseSet ≈ 898&nbsp;B, RouterInfo ≈ 2&ndash;4&nbsp;KB compressed)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Publishes RouterInfo or LeaseSet objects. Supports LeaseSet2, EncryptedLeaseSet, and MetaLeaseSet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>DatabaseLookup</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">500</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Queries the network database for RouterInfo or LeaseSet entries</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>DatabaseSearchReply</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">300</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">≈161&nbsp;B (5 hashes)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Returns candidate floodfill router hashes (typically 3&ndash;16 hashes, recommended maximum 16)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>DeliveryStatus</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Varies</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">12&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Receipts for tunnel tests or acknowledgements inside GarlicMessages</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>GarlicMessage</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">100 (local)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bundles multiple message cloves (e.g., DataMessage, LeaseSets). Supports ElGamal/AES (deprecated) and ECIES-X25519-AEAD-Ratchet encryption</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>TunnelData</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">18</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">400</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1,028&nbsp;B (fixed)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Encrypted tunnel message exchanged between hops. Contains a 4-byte tunnel ID, 16-byte IV, and 1,004 bytes of encrypted data</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>TunnelGateway</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">19</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">300&ndash;400</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Varies</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Encapsulates messages at the tunnel gateway before fragmentation</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>DataMessage</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">425</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">4&ndash;62&nbsp;KB</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Carries end-to-end garlic payloads (application traffic)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>TunnelBuild</strong> <em>(deprecated)</em></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">21</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">500</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">4,224&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Requests tunnel participation from routers (8 × 528-byte records). Replaced by VariableTunnelBuild for ECIES</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>TunnelBuildReply</strong> <em>(deprecated)</em></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">22</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">300</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">4,224&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Replies to TunnelBuild with accept/reject status per hop</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>VariableTunnelBuild</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">23</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">500</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1,057&ndash;4,225&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Variable-length tunnel build for ElGamal or ECIES-X25519 routers (1&ndash;8 records, API 0.9.12+)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>VariableTunnelBuildReply</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">24</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">300</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">1,057&ndash;4,225&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Replies to VariableTunnelBuild</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>ShortTunnelBuild</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">25</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">500</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">873&ndash;1,745&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Short tunnel build messages for ECIES-X25519 routers only (1&ndash;8 × 218-byte records, API 0.9.51+)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>OutboundTunnelBuildReply</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">26</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">300</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">873&ndash;1,745&nbsp;B</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Sent from outbound endpoint to originator for ECIES-X25519 routers (API 0.9.51+)</td>
    </tr>
  </tbody>
</table>
**Reservierte Nachrichtentypen:** - Typ 0: Reserviert - Typen 4-9: Für zukünftige Verwendung reserviert - Typen 12-17: Für zukünftige Verwendung reserviert - Typen 224-254: Für experimentelle Nachrichten reserviert - Typ 255: Für zukünftige Erweiterungen reserviert

### Hinweise zu Nachrichtentypen

- Nachrichten der Steuerungsebene (DatabaseLookup, TunnelBuild, etc.) laufen typischerweise über **exploratory tunnels** (Erkundungs-Tunnel), nicht über client tunnels (Client-Tunnel), wodurch eine unabhängige Priorisierung möglich ist
- Prioritätswerte sind ungefähre Angaben und können je nach Implementierung variieren
- TunnelBuild (21) und TunnelBuildReply (22) sind veraltet, werden aber weiterhin implementiert, um die Kompatibilität mit sehr langen tunnels (>8 Hops) zu gewährleisten
- Die Standard-Priorität für Daten in tunnels beträgt 400; alles darüber wird als dringend behandelt
- Die typische Länge von tunnels im heutigen Netzwerk beträgt 3-4 Hops, daher verwenden die meisten tunnel builds (Tunnelaufbauten) ShortTunnelBuild (218-Byte-Datensätze) oder VariableTunnelBuild (528-Byte-Datensätze)

---

## Verschlüsselung und Nachrichtenkapselung

Routers verkapseln häufig I2NP-Nachrichten vor der Übertragung und erzeugen dadurch mehrere Verschlüsselungsschichten. Eine DeliveryStatus-Nachricht kann sein: 1. In einer GarlicMessage verpackt (verschlüsselt) 2. In einer DataMessage 3. In einer TunnelData-Nachricht (erneut verschlüsselt)

Jeder Hop entschlüsselt nur seine eigene Schicht; der endgültige Empfänger legt die innerste Nutzlast offen.

### Verschlüsselungsalgorithmen

**Veraltet (wird schrittweise ausgemustert):** - ElGamal/AES + SessionTags (Sitzungs-Tags) - ElGamal-2048 für asymmetrische Verschlüsselung - AES-256 für symmetrische Verschlüsselung - 32-Byte SessionTags

**Aktuell (Standard seit API 0.9.48):** - ECIES-X25519 + ChaCha20/Poly1305 AEAD mit Ratcheting-Vorwärtsgeheimnis - Noise-Protokoll-Framework (Noise_IK_25519_ChaChaPoly_SHA256 für Ziele) - 8-Byte Session-Tags (reduziert von 32 Byte) - Signal-Double-Ratchet-Algorithmus für Vorwärtsgeheimnis - Eingeführt in API-Version 0.9.46 (2020) - Seit API-Version 0.9.58 (2023) für alle routers obligatorisch

**Zukunft (Beta seit 2.10.0):** - Post-Quanten-Hybridkryptografie unter Verwendung von MLKEM (ML-KEM-768), kombiniert mit X25519 - Hybride Ratchet (Schlüssel-Update-Mechanismus), die klassischen und Post-Quanten-Schlüsselaustausch kombiniert - Abwärtskompatibel mit ECIES-X25519 - Wird zum Standard in Release 2.11.0 (Dezember 2025)

### ElGamal Router Abkündigung

**KRITISCH:** ElGamal routers wurden ab API-Version 0.9.58 (Release 2.2.0, März 2023) als veraltet markiert. Da die für Abfragen empfohlene minimale floodfill-Version nun 0.9.58 ist, müssen Implementierungen für ElGamal floodfill routers keine Verschlüsselung implementieren.

**Allerdings:** ElGamal destinations (Ziele) werden aus Gründen der Abwärtskompatibilität weiterhin unterstützt. Clients, die ElGamal-Verschlüsselung verwenden, können weiterhin über ECIES routers kommunizieren.

### Details zum ECIES-X25519-AEAD-Ratchet

Dies ist Krypto-Typ 4 in der Kryptografie-Spezifikation von I2P. Er bietet:

**Wichtige Merkmale:** - Vorwärtsgeheimhaltung durch ratcheting (stufenweise Schlüsselaktualisierung; neue Schlüssel für jede Nachricht) - Reduzierter Speicherbedarf für Session-Tags (8 Byte statt 32 Byte) - Mehrere Session-Typen (Neue Session, bestehende Session, einmalig) - Basiert auf dem Noise-Protokoll Noise_IK_25519_ChaChaPoly_SHA256 - Integriert mit dem Double Ratchet-Algorithmus von Signal

**Kryptographische Primitive:** - X25519 für den Diffie-Hellman-Schlüsselaustausch - ChaCha20 zur Stream-Verschlüsselung - Poly1305 zur Nachrichtenauthentifizierung (AEAD) - SHA-256 zum Hashing - HKDF zur Schlüsselableitung

**Sitzungsverwaltung:** - Neue Sitzung: Anfängliche Verbindung über den statischen Schlüssel der Destination (Ziel) - Bestehende Sitzung: Nachfolgende Nachrichten mithilfe von Session Tags (Sitzungs-Tags) - Einmalsitzung: Sitzungen mit nur einer Nachricht für geringeren Overhead

Siehe [ECIES Specification](/docs/specs/ecies/) und [Proposal 144](/proposals/144-ecies-x25519-aead-ratchet/) für vollständige technische Details.

---

## Gemeinsame Strukturen

Die folgenden Strukturen sind Bestandteile mehrerer I2NP-Nachrichten. Sie sind keine vollständigen Nachrichten.

### BuildRequestRecord (Aufbauanforderungs-Datensatz) (ElGamal)

**VERALTET.** Wird im aktuellen Netzwerk nur verwendet, wenn ein tunnel einen ElGamal router enthält. Siehe [ECIES Tunnel-Erstellung](/docs/specs/implementation/) für das moderne Format.

**Zweck:** Ein Datensatz in einer Gruppe mehrerer Datensätze, um die Erstellung eines Hops im tunnel anzufordern.

**Format:**

Mit ElGamal und AES verschlüsselt (insgesamt 528 Bytes):

```
+----+----+----+----+----+----+----+----+
| encrypted data (528 bytes)            |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
```
ElGamal-verschlüsselte Struktur (528 Bytes):

```
+----+----+----+----+----+----+----+----+
| toPeer (16 bytes)                     |
+----+----+----+----+----+----+----+----+
| ElGamal encrypted data (512 bytes)    |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

toPeer :: First 16 bytes of SHA-256 hash of peer's RouterIdentity

encrypted_data :: ElGamal-2048 encrypted (bytes 1-256 and 258-513
                  of the 514-byte ElGamal block, with padding bytes
                  at positions 0 and 257 removed)
```
Klartextstruktur (222 Byte vor der Verschlüsselung):

```
+----+----+----+----+----+----+----+----+
| receive_tunnel (4) | our_ident (32)   |
+----+----+----+----+                   +
|                                       |
+                   +----+----+----+----+
|                   | next_tunnel (4)   |
+----+----+----+----+----+----+----+----+
| next_ident (32 bytes)                 |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| layer_key (32 bytes)                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| iv_key (32 bytes)                     |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| reply_key (32 bytes)                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| reply_iv (16 bytes)                   |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag| request_time (4) | send_msg_id  |
+----+----+----+----+----+----+----+----+
     (4)                | padding (29)  |
+----+----+----+----+----+              +
|                                       |
+                             +----+----+
|                             |
+----+----+----+----+----+----+

receive_tunnel :: TunnelId (4 bytes, nonzero)
our_ident :: Hash (32 bytes)
next_tunnel :: TunnelId (4 bytes, nonzero)
next_ident :: Hash (32 bytes)
layer_key :: SessionKey (32 bytes)
iv_key :: SessionKey (32 bytes)
reply_key :: SessionKey (32 bytes)
reply_iv :: 16 bytes
flag :: Integer (1 byte)
request_time :: Integer (4 bytes, hours since epoch = time / 3600)
send_message_id :: Integer (4 bytes)
padding :: 29 bytes random data
```
**Hinweise:** - Die ElGamal-2048-Verschlüsselung erzeugt einen 514-Byte-Block, aber die beiden Padding-Bytes (Auffüll-Bytes) (an den Positionen 0 und 257) werden entfernt, wodurch 512 Bytes verbleiben - Siehe [Spezifikation zur Tunnel-Erstellung](/docs/specs/implementation/) für Details zu den Feldern - Quellcode: `net.i2p.data.i2np.BuildRequestRecord` - Konstante: `EncryptedBuildRecord.RECORD_SIZE = 528`

### BuildRequestRecord (ECIES-X25519 Long)

Für ECIES-X25519 routers, eingeführt in API-Version 0.9.48. Verwendet 528 Bytes zur Abwärtskompatibilität mit gemischten tunnels.

**Format:**

```
+----+----+----+----+----+----+----+----+
| toPeer (16 bytes)                     |
+----+----+----+----+----+----+----+----+
| ephemeral_key (32 bytes)              |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| ChaCha20 encrypted data (464 bytes)   |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Poly1305 MAC (16 bytes)               |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

toPeer :: First 16 bytes of SHA-256 hash of peer's RouterIdentity
ephemeral_key :: X25519 ephemeral public key (32 bytes)
encrypted_data :: ChaCha20 encrypted (464 bytes)
mac :: Poly1305 message authentication code (16 bytes)
```
**Gesamtgröße:** 528 Bytes (identisch mit ElGamal zur Kompatibilität)

Siehe [ECIES Tunnel Creation](/docs/specs/implementation/) für die Klartextstruktur und Details zur Verschlüsselung.

### BuildRequestRecord (Datensatz für Aufbauanforderung) (ECIES-X25519 Short)

Nur für ECIES-X25519 Router, ab API-Version 0.9.51 (Release 1.5.0). Dies ist das aktuelle Standardformat.

**Format:**

```
+----+----+----+----+----+----+----+----+
| toPeer (16 bytes)                     |
+----+----+----+----+----+----+----+----+
| ephemeral_key (32 bytes)              |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| ChaCha20 encrypted data (154 bytes)   |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Poly1305 MAC (16 bytes)               |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

toPeer :: First 16 bytes of SHA-256 hash of peer's RouterIdentity
ephemeral_key :: X25519 ephemeral public key (32 bytes)
encrypted_data :: ChaCha20 encrypted (154 bytes)
mac :: Poly1305 message authentication code (16 bytes)
```
**Gesamtgröße:** 218 Bytes (59 % Reduktion gegenüber 528 Bytes)

**Wesentlicher Unterschied:** Kurzdatensätze leiten ALLE Schlüssel über HKDF (Schlüsselableitungsfunktion) ab, statt sie explizit im Datensatz aufzuführen. Dazu gehören: - Layer-Schlüssel (für tunnel-Verschlüsselung) - IV-Schlüssel (für tunnel-Verschlüsselung) - Antwort-Schlüssel (für Build-Antwort) - Antwort-IVs (für Build-Antwort)

Alle Schlüssel werden mithilfe des HKDF-Mechanismus des Noise-Protokolls auf Basis des gemeinsamen Geheimnisses aus dem X25519-Schlüsselaustausch abgeleitet.

**Vorteile:** - 4 kurze Datensätze passen in eine tunnel-Nachricht (873 Bytes) - 3 Nachrichten für den tunnel-Aufbau statt separater Nachrichten für jeden Datensatz - Reduzierter Bandbreitenbedarf und geringere Latenz - Gleiche Sicherheitseigenschaften wie das Langformat

Siehe [Proposal 157](/proposals/157-new-tbm/) für die Begründung und [ECIES Tunnel Creation](/docs/specs/implementation/) (ECIES: Elliptic Curve Integrated Encryption Scheme, Verschlüsselungsschema mit elliptischen Kurven) für die vollständige Spezifikation.

**Quellcode:** - `net.i2p.data.i2np.ShortEncryptedBuildRecord` - Konstante: `ShortEncryptedBuildRecord.RECORD_SIZE = 218`

### BuildResponseRecord (ElGamal)

**VERALTET.** Wird nur verwendet, wenn der tunnel einen ElGamal router enthält.

**Zweck:** Ein Eintrag in einer Sammlung mehrerer Einträge mit Antworten auf eine Aufbauanfrage.

**Format:**

Verschlüsselt (528 Bytes, gleiche Größe wie BuildRequestRecord):

```
bytes 0-527 :: AES-encrypted record
```
Unverschlüsselte Struktur:

```
+----+----+----+----+----+----+----+----+
| SHA-256 hash (32 bytes)               |
+                                       +
|        (hash of bytes 32-527)         |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| random data (495 bytes)               |
~                                       ~
|                                  |ret |
+----+----+----+----+----+----+----+----+

bytes 0-31 :: SHA-256 hash of bytes 32-527
bytes 32-526 :: Random data (could be used for congestion info)
byte 527 :: Reply code (0 = accept, 30 = reject)
```
**Antwortcodes:** - `0` - Annehmen - `30` - Ablehnen (Bandbreitenlimit überschritten)

Siehe [Spezifikation zur Tunnel-Erstellung](/docs/specs/implementation/) für Details zum Antwortfeld.

### BuildResponseRecord (ECIES-X25519)

Für ECIES-X25519 (ECIES mit Curve25519) routers, API-Version 0.9.48+. Gleiche Größe wie die entsprechende Anfrage (528 für lang, 218 für kurz).

**Format:**

Ausführliches Format (528 Bytes):

```
+----+----+----+----+----+----+----+----+
| ChaCha20 encrypted data (512 bytes)   |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Poly1305 MAC (16 bytes)               |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
Kurzformat (218 Bytes):

```
+----+----+----+----+----+----+----+----+
| ChaCha20 encrypted data (202 bytes)   |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Poly1305 MAC (16 bytes)               |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
**Klartextstruktur (beide Formate):**

Enthält eine Mapping-Struktur (I2Ps Schlüssel-Wert-Format) mit: - Antwortstatuscode (erforderlich) - Parameter für verfügbare Bandbreite ("b") (optional, hinzugefügt in API 0.9.65) - Weitere optionale Parameter für zukünftige Erweiterungen

**Antwort-Statuscodes:** - `0` - Erfolg - `30` - Abgelehnt: Bandbreite überschritten

Siehe [ECIES Tunnel-Erstellung](/docs/specs/implementation/) für die vollständige Spezifikation.

### GarlicClove (ElGamal/AES)

**WARNUNG:** Dies ist das Format, das für garlic cloves (einzelne Teilnachrichten im Garlic-Verfahren) innerhalb von ElGamal-verschlüsselten garlic messages verwendet wird. Das Format für ECIES-AEAD-X25519-Ratchet garlic messages und garlic cloves unterscheidet sich erheblich. Siehe [ECIES Specification](/docs/specs/ecies/) für das moderne Format.

**Veraltet für routers (API 0.9.58+), für Ziele weiterhin unterstützt.**

**Format:**

Unverschlüsselt:

```
+----+----+----+----+----+----+----+----+
| Delivery Instructions (variable)      |
~                                       ~
+----+----+----+----+----+----+----+----+
| I2NP Message (variable)               |
~                                       ~
+----+----+----+----+----+----+----+----+
| Clove ID (4)  | Expiration (8)   |Cert|
+----+----+----+----+----+----+----+----+
                                    (3) |
+----+----+----+----+----+----+----+----+

Delivery Instructions :: Variable length (typically 1, 33, or 37 bytes)
I2NP Message :: Any I2NP message
Clove ID :: 4-byte Integer (random, checked for duplicates)
Expiration :: Date (8 bytes)
Certificate :: Always NULL (3 bytes total, all zeroes)
```
**Hinweise:** - Cloves (Teilnachrichten) werden niemals fragmentiert - Wenn das erste Bit des Delivery Instructions-Flag-Bytes 0 ist, ist der clove nicht verschlüsselt - Wenn das erste Bit 1 ist, ist der clove verschlüsselt (nicht implementierte Funktion) - Die maximale Länge ist eine Funktion der gesamten clove-Längen und der maximalen GarlicMessage-Länge (Nachrichtentyp in I2NP) - Das Zertifikat könnte möglicherweise für HashCash verwendet werden, um für das Routing zu „bezahlen“ (zukünftige Möglichkeit) - In der Praxis verwendete Nachrichten: DataMessage, DeliveryStatusMessage, DatabaseStoreMessage - GarlicMessage kann GarlicMessage enthalten (verschachtelt), wird in der Praxis jedoch nicht verwendet

Siehe [Garlic Routing](/docs/overview/garlic-routing/) (eine in I2P verwendete Routing-Technik) für eine konzeptionelle Übersicht.

### GarlicClove (Einzelelement einer Garlic-Nachricht) (ECIES-X25519-AEAD-Ratchet)

Für ECIES-X25519 routers und Ziele, API-Version 0.9.46+. Dies ist das aktuelle Standardformat.

**KRITISCHER UNTERSCHIED:** ECIES garlic verwendet eine völlig andere Struktur, die auf Noise-Protokoll-Blöcken basiert, statt auf expliziten clove-Strukturen (clove = Teilnachricht innerhalb einer garlic-Nachricht in I2P).

**Format:**

ECIES-Garlic-Nachrichten enthalten eine Reihe von Blöcken:

```
Block structure:
+----+----+----+----+----+----+----+----+
|type| length    | data ...
+----+----+----+----+----+-//-

type :: 1 byte block type
length :: 2 bytes block length
data :: variable length data
```
**Blocktypen:** - `0` - Garlic Clove Block (enthält eine I2NP-Nachricht) - `1` - DateTime Block (Zeitstempel) - `2` - Options Block (Übermittlungsoptionen) - `3` - Padding Block - `254` - Termination Block (nicht implementiert)

**Garlic Clove Block (Typ 0):**

```
+----+----+----+----+----+----+----+----+
|  0 | length    | Delivery Instructions |
+----+----+----+----+                    +
~                                       ~
+----+----+----+----+----+----+----+----+
| I2NP Message                          |
~                                       ~
+----+----+----+----+----+----+----+----+
| Clove ID (4)  | Expiration (4)        |
+----+----+----+----+----+----+----+----+
```
**Wesentliche Unterschiede zum ElGamal-Format:** - Verwendet eine 4-Byte-Ablaufzeit (Sekunden seit der Unix-Epoche) statt eines 8-Byte-Datums - Kein Zertifikat-Feld - Eingebettet in eine Blockstruktur mit Typ und Länge - Gesamte Nachricht mit ChaCha20/Poly1305 AEAD verschlüsselt - Sitzungsverwaltung über ratcheting (Schlüssel-Ratchet-Verfahren)

Ausführliche Informationen zum Noise-Protokoll-Framework und zu den Blockstrukturen finden Sie in der [ECIES-Spezifikation](/docs/specs/ecies/).

### Zustellungsanweisungen für Garlic Clove (Einzelnachricht in der garlic encryption)

Dieses Format wird sowohl für ElGamal- als auch für ECIES garlic cloves (Teilnachrichten im Rahmen der garlic encryption) verwendet. Es legt fest, wie die enthaltene Nachricht zugestellt wird.

**KRITISCHE WARNUNG:** Diese Spezifikation gilt AUSSCHLIESSLICH für "Delivery Instructions" (Zustellanweisungen) innerhalb von "Garlic Cloves" (Einzelelementen einer Garlic-Nachricht). "Delivery Instructions" werden auch innerhalb von Tunnel-Nachrichten verwendet, wo das Format deutlich anders ist. Siehe die [Spezifikation für Tunnel-Nachrichten](/docs/specs/implementation/) für Delivery Instructions in Tunnel-Nachrichten. Verwechseln Sie diese beiden Formate NICHT.

**Format:**

Sitzungsschlüssel und Verzögerung werden nicht verwendet und sind nie vorhanden, daher sind die drei möglichen Längen:
- 1 Byte (LOCAL)
- 33 Bytes (ROUTER und DESTINATION)
- 37 Bytes (TUNNEL)

```
+----+----+----+----+----+----+----+----+
|flag|                                  |
+----+                                  +
|       Session Key (optional, 32)     |
+                                       +
|                                       |
+    +----+----+----+----+--------------+
|    |                                  |
+----+                                  +
|       To Hash (optional, 32)         |
+                                       +
|                                       |
+    +----+----+----+----+--------------+
|    | Tunnel ID (4, opt)| Delay (4, opt)|
+----+----+----+----+----+----+----+----+

flag :: 1 byte
        Bit order: 76543210
        bit 7: encrypted? (Unimplemented, always 0)
               If 1, a 32-byte encryption session key follows
        bits 6-5: delivery type
               0x0 = LOCAL (0)
               0x1 = DESTINATION (1)
               0x2 = ROUTER (2)
               0x3 = TUNNEL (3)
        bit 4: delay included? (Not fully implemented, always 0)
               If 1, four delay bytes are included
        bits 3-0: reserved, set to 0 for compatibility

Session Key :: 32 bytes (Optional, unimplemented)
               Present if encrypt flag bit is set

To Hash :: 32 bytes (Optional)
           Present if delivery type is DESTINATION, ROUTER, or TUNNEL
           - DESTINATION: SHA256 hash of the destination
           - ROUTER: SHA256 hash of the router identity
           - TUNNEL: SHA256 hash of the gateway router identity

Tunnel ID :: 4 bytes (Optional)
             Present if delivery type is TUNNEL
             The destination tunnel ID (nonzero)

Delay :: 4 bytes (Optional, unimplemented)
         Present if delay included flag is set
         Specifies delay in seconds
```
**Typische Längen:** - LOKALE Zustellung: 1 Byte (nur Flag) - ROUTER / ZIEL Zustellung: 33 Byte (Flag + Hash) - TUNNEL Zustellung: 37 Byte (Flag + Hash + tunnel ID)

**Beschreibungen der Zustelltypen:**

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Value</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LOCAL</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deliver to the local router (this router)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DESTINATION</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deliver to a destination (client) identified by hash</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ROUTER</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deliver to another router identified by hash</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">TUNNEL</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deliver to a tunnel gateway router</td>
    </tr>
  </tbody>
</table>
**Hinweise zur Implementierung:** - Die Verschlüsselung mit Sitzungsschlüssel ist nicht implementiert und das Flag-Bit ist immer 0 - Die Verzögerung ist nicht vollständig implementiert und das Flag-Bit ist immer 0 - Für TUNNEL-Zustellung identifiziert der Hash den Gateway router und die tunnel ID gibt an, welcher eingehende tunnel - Für DESTINATION (Ziel-Identität)-Zustellung ist der Hash der SHA-256-Hash des öffentlichen Schlüssels der destination - Für ROUTER-Zustellung ist der Hash der SHA-256-Hash der Identität des router

---

## I2NP-Nachrichten

Vollständige Nachrichtenspezifikationen für alle I2NP-Nachrichtentypen.

### Zusammenfassung der Nachrichtentypen

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Message</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseStore</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseLookup</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DatabaseSearchReply</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DeliveryStatus</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Garlic</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelData</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">18</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelGateway</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">19</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">Data</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelBuild</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">21</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelBuildReply</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">22</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.6.1.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">VariableTunnelBuild</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">23</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">VariableTunnelBuildReply</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">24</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ShortTunnelBuild</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">25</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.51</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">OutboundTunnelBuildReply</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">26</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.51</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Active</td></tr>
  </tbody>
</table>
**Reserviert:** - Typ 0: Reserviert - Typen 4-9: Für zukünftige Verwendung reserviert - Typen 12-17: Für zukünftige Verwendung reserviert - Typen 224-254: Für experimentelle Nachrichten reserviert - Typ 255: Für zukünftige Erweiterungen reserviert

---

### DatabaseStore (Typ 1)

**Zweck:** Eine unaufgeforderte Datenbankspeicherung oder die Antwort auf eine erfolgreiche DatabaseLookup-Nachricht (Nachrichtentyp zur Datenbanksuche).

**Inhalt:** Ein nicht komprimiertes LeaseSet, LeaseSet2, MetaLeaseSet oder EncryptedLeaseSet, oder eine komprimierte RouterInfo.

**Format mit Antwort-Token:**

```
+----+----+----+----+----+----+----+----+
| SHA256 Hash as key (32 bytes)        |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|type| reply token (4)   | reply_tunnelId
+----+----+----+----+----+----+----+----+
     (4)               | reply gateway  |
+----+----+----+----+----+              +
|       SHA256 hash (32 bytes)          |
+                                       +
|                                       |
+                                  +----+
|                                  |
+----+----+----+----+----+----+----+
| data ...
+----+-//

key :: 32 bytes
       SHA256 hash (the "real" hash, not routing key)

type :: 1 byte
        Type identifier
        bit 0:
            0 = RouterInfo
            1 = LeaseSet or variants
        bits 3-1: (as of 0.9.38)
            0: RouterInfo or LeaseSet (types 0 or 1)
            1: LeaseSet2 (type 3)
            2: EncryptedLeaseSet (type 5)
            3: MetaLeaseSet (type 7)
            4-7: Unsupported, invalid
        bits 7-4:
            Reserved, set to 0

reply token :: 4 bytes
               If greater than zero, a DeliveryStatusMessage is
               requested with the Message ID set to the reply token
               A floodfill router is also expected to flood the data
               to the closest floodfill peers

reply_tunnelId :: 4 bytes (only if reply token > 0)
                  TunnelId of the inbound gateway of the tunnel
                  for the response
                  If 0, reply is sent directly to reply gateway

reply gateway :: 32 bytes (only if reply token > 0)
                 SHA256 hash of the RouterInfo
                 If reply_tunnelId is nonzero: inbound gateway router
                 If reply_tunnelId is zero: router to send reply to

data :: Variable length
        If type == 0: 2-byte Integer length + gzip-compressed RouterInfo
        If type == 1: Uncompressed LeaseSet
        If type == 3: Uncompressed LeaseSet2
        If type == 5: Uncompressed EncryptedLeaseSet
        If type == 7: Uncompressed MetaLeaseSet
```
**Format mit Antwort-Token == 0:**

```
+----+----+----+----+----+----+----+----+
| SHA256 Hash as key (32 bytes)        |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|type|         0         | data ...
+----+----+----+----+----+-//
```
**Hinweise:** - Aus Sicherheitsgründen werden die Antwortfelder ignoriert, wenn die Nachricht über einen tunnel empfangen wird - Der Schlüssel ist der „echte“ Hash der RouterIdentity oder Destination, NICHT der Routing-Schlüssel - Die Typen 3, 5 und 7 (LeaseSet2-Varianten) wurden in Release 0.9.38 (API 0.9.38) hinzugefügt. Siehe [Proposal 123](/proposals/123-new-netdb-entries/) für Details - Diese Typen sollten nur an router mit API-Version 0.9.38 oder höher gesendet werden - Als Optimierung zur Reduzierung von Verbindungen gilt: Wenn der Typ ein LeaseSet ist, das Antwort-Token enthalten ist, die Antwort-tunnel-ID ungleich Null ist und das Antwort-Gateway/tunnelID-Paar im LeaseSet als Lease gefunden wird, darf der Empfänger die Antwort über jede andere Lease im LeaseSet umleiten - **RouterInfo gzip-Format:** Um das Betriebssystem des router und die Implementierung zu verbergen, sollte die Java-router-Implementierung nachgeahmt werden, indem die Modifikationszeit auf 0 und das OS-Byte auf 0xFF gesetzt und XFL gemäß RFC 1952 auf 0x02 gesetzt wird (maximale Kompression, langsamster Algorithmus). Erste 10 Bytes: `1F 8B 08 00 00 00 00 00 02 FF`

**Quellcode:** - `net.i2p.data.i2np.DatabaseStoreMessage` - `net.i2p.data.RouterInfo` (für die RouterInfo-Struktur) - `net.i2p.data.LeaseSet` (für die LeaseSet-Struktur)

---

### DatabaseLookup (Datenbanksuche) (Typ 2)

**Zweck:** Eine Anfrage, um einen Eintrag in der Netzwerkdatenbank nachzuschlagen. Die Antwort ist entweder ein DatabaseStore (Nachricht zum Speichern in der Datenbank) oder eine DatabaseSearchReply (Antwort auf eine Datenbanksuche).

**Format:**

```
+----+----+----+----+----+----+----+----+
| SHA256 hash as the key (32 bytes)    |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| SHA256 hash of the from router (32)  |
+    or reply tunnel gateway            +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag| reply_tunnelId (4)| size (2)|   |
+----+----+----+----+----+----+----+    +
| SHA256 of key1 to exclude (32 bytes) |
+                                       +
|                                       |
+                                  +----+
|                                  |    |
+----+----+----+----+----+----+----+    +
| SHA256 of key2 to exclude (32)       |
+                                       +
~                                       ~
|                                       |
+                                  +----+
|                                  |    |
+----+----+----+----+----+----+----+    +
|   Session key if reply encryption     |
+       requested (32 bytes)             +
|                                       |
+                                  +----+
|                                  |tags|
+----+----+----+----+----+----+----+----+
|   Session tags if reply encryption    |
+       requested (variable)             +
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

key :: 32 bytes
       SHA256 hash of the object to lookup

from :: 32 bytes
        If deliveryFlag == 0: SHA256 hash of RouterInfo (sender)
        If deliveryFlag == 1: SHA256 hash of reply tunnel gateway

flags :: 1 byte
         Bit order: 76543210
         bit 0: deliveryFlag
             0 = send reply directly
             1 = send reply to some tunnel
         bit 1: encryptionFlag
             Through 0.9.5: must be 0
             As of 0.9.6: ignored
             As of 0.9.7:
                 0 = send unencrypted reply
                 1 = send AES encrypted reply using key and tag
         bits 3-2: lookup type flags
             Through 0.9.5: must be 00
             As of 0.9.6: ignored
             As of 0.9.16:
                 00 = ANY (deprecated, use LS or RI as of 0.9.16)
                 01 = LS lookup (LeaseSet or variants)
                 10 = RI lookup (RouterInfo)
                 11 = exploration lookup (RouterInfo, non-floodfill)
         bit 4: ECIESFlag
             Before 0.9.46: ignored
             As of 0.9.46:
                 0 = send unencrypted or ElGamal reply
                 1 = send ChaCha/Poly encrypted reply using key
         bits 7-5:
             Reserved, set to 0

reply_tunnelId :: 4 bytes (only if deliveryFlag == 1)
                  TunnelId of the tunnel to send reply to (nonzero)

size :: 2 bytes
        Integer (valid range: 0-512)
        Number of peers to exclude from DatabaseSearchReply

excludedPeers :: $size SHA256 hashes of 32 bytes each
                 If lookup fails, exclude these peers from the reply
                 If includes a hash of all zeroes, the request is
                 exploratory (return non-floodfill routers only)

reply_key :: 32 bytes (conditional, see encryption modes below)
reply_tags :: 1 byte count + variable length tags (conditional)
```
**Modi der Antwortverschlüsselung:**

**HINWEIS:** ElGamal routers sind seit API 0.9.58 veraltet. Da die empfohlene minimale floodfill-Version, die abgefragt werden soll, jetzt 0.9.58 ist, müssen Implementierungen keine Verschlüsselung für ElGamal floodfill routers implementieren. ElGamal destinations (Zieladressen) werden weiterhin unterstützt.

Flag-Bit 4 (ECIESFlag) wird in Kombination mit Bit 1 (encryptionFlag) verwendet, um den Antwortverschlüsselungsmodus zu bestimmen:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Flag bits 4,1</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">From</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">To Router</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Reply</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">DH?</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0 0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Any</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">n/a</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No encryption</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0 1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElG</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElG</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">AES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">As of 0.9.7, deprecated 0.9.58</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElG</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">AEAD</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">As of 0.9.46, deprecated 0.9.58</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">AEAD</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">No</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">As of 0.9.49, current standard</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElG</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">AES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">TBD, future</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1 1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">AEAD</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Yes</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">TBD, future</td>
    </tr>
  </tbody>
</table>
**Keine Verschlüsselung (Flags 0,0):**

reply_key, tags und reply_tags sind nicht vorhanden.

**ElG nach ElG (Flags 0,1) - VERALTET:**

Unterstützt seit 0.9.7, seit 0.9.58 als veraltet markiert.

```
reply_key :: 32 byte SessionKey (big-endian)
             CSRNG(32) random data

tags :: 1 byte Integer (1-32, typically 1)
        Number of reply tags that follow

reply_tags :: One or more 32-byte SessionTags
              Each is CSRNG(32) random data
```
**ECIES zu ElG (Flags 1,0) - VERALTET:**

Ab Version 0.9.46 unterstützt, ab Version 0.9.58 als veraltet eingestuft.

```
reply_key :: 32 byte ECIES SessionKey (big-endian)
             CSRNG(32) random data

tags :: 1 byte Integer (required value: 1)
        Number of reply tags that follow

reply_tags :: One 8-byte ECIES SessionTag
              CSRNG(8) random data
```
Die Antwort ist eine ECIES Existing Session message (Nachricht für eine bestehende Sitzung), wie in der [ECIES-Spezifikation](/docs/specs/ecies/) definiert:

```
+----+----+----+----+----+----+----+----+
| Session Tag (8 bytes)                 |
+----+----+----+----+----+----+----+----+
| ChaCha20 encrypted payload            |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Poly1305 MAC (16 bytes)               |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

tag :: 8 byte reply_tag
k :: 32 byte session key (the reply_key)
n :: 0 (nonce)
ad :: The 8 byte reply_tag
payload :: Plaintext data (DSM or DSRM)
ciphertext = ENCRYPT(k, n, payload, ad)
```
**ECIES zu ECIES (Flags 1,0) - AKTUELLER STANDARD:**

Eine ECIES Destination (Ziel) oder ein router sendet ein Lookup (Abfrage) an einen ECIES router. Unterstützt seit 0.9.49.

Dasselbe Format wie oben bei "ECIES to ElG". Die Verschlüsselung der Abfrage-Nachricht ist in [ECIES Routers](/docs/specs/ecies/#routers) spezifiziert. Der Anfragende ist anonym.

**ECIES (integriertes Verschlüsselungsschema mit elliptischen Kurven) zu ECIES mit DH (Diffie-Hellman-Schlüsselaustausch) (flags 1,1) - ZUKUNFT:**

Noch nicht vollständig definiert. Siehe [Proposal 156](/proposals/156-ecies-routers/).


**Quellcode:** - `net.i2p.data.i2np.DatabaseLookupMessage` - Verschlüsselung: `net.i2p.crypto.SessionKeyManager`

---

### DatabaseSearchReply (Antwort auf Datenbanksuche) (Typ 3)

**Zweck:** Die Antwort auf eine fehlgeschlagene DatabaseLookup-Nachricht (Nachricht zur Datenbanksuche).

**Inhalt:** Eine Liste von router-Hashes, die dem angeforderten Schlüssel am nächsten liegen.

**Format:**

```
+----+----+----+----+----+----+----+----+
| SHA256 hash as query key (32 bytes)  |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| num| peer_hashes (variable)           |
+----+                                  +
|                                       |
~                                       ~
|                                       |
+    +----+----+----+----+----+----+----+
|    | from (32 bytes)                  |
+----+                                  +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+----+----+----+
|    |
+----+

key :: 32 bytes
       SHA256 of the object being searched

num :: 1 byte Integer
       Number of peer hashes that follow (0-255)

peer_hashes :: $num SHA256 hashes of 32 bytes each (total $num*32 bytes)
               SHA256 of the RouterIdentity that the sender thinks is
               close to the key

from :: 32 bytes
        SHA256 of the RouterInfo of the router this reply was sent from
```
**Hinweise:** - Der 'from'-Hash ist nicht authentifiziert und nicht vertrauenswürdig - Die zurückgegebenen Peer-Hashes sind nicht notwendigerweise näher am Schlüssel als der abgefragte router. Bei Antworten auf reguläre Abfragen erleichtert dies die Entdeckung neuer floodfills und das „rückwärtsgerichtete“ Suchen (weiter-vom-Schlüssel-entfernt) für mehr Robustheit - Bei Erkundungsabfragen wird der Schlüssel normalerweise zufällig erzeugt. Die nicht-floodfill peer_hashes der Antwort können mithilfe eines optimierten Algorithmus ausgewählt werden (z. B. nahe, aber nicht unbedingt nächstgelegene Peers), um eine ineffiziente Sortierung der gesamten lokalen Datenbank zu vermeiden. Es können auch Caching-Strategien verwendet werden. Dies ist implementierungsabhängig - **Typische Anzahl zurückgegebener Hashes:** 3 - **Empfohlene maximale Anzahl zurückzugebender Hashes:** 16 - Der Lookup-Schlüssel, die Peer-Hashes und der from-Hash sind "echte" Hashes, KEINE Routing-Schlüssel - Wenn num 0 ist, bedeutet dies, dass keine näheren Peers gefunden wurden (Sackgasse)

**Quellcode:** - `net.i2p.data.i2np.DatabaseSearchReplyMessage`

---

### Zustellstatus (Typ 10)

**Zweck:** Eine einfache Nachrichtenbestätigung. Wird im Allgemeinen vom Absender der Nachricht erstellt und zusammen mit der eigentlichen Nachricht in einer Garlic Message (I2P-Nachricht, die mehrere Teilnachrichten bündelt) verpackt, damit sie vom Ziel zurückgesendet wird.

**Inhalt:** Die ID der zugestellten Nachricht und die Erstellungs- oder Ankunftszeit.

**Format:**

```
+----+----+----+----+----+----+----+----+----+----+----+----+
| msg_id (4)            | time_stamp (8)                    |
+----+----+----+----+----+----+----+----+----+----+----+----+

msg_id :: Integer (4 bytes)
          Unique ID of the message we deliver the DeliveryStatus for
          (see I2NP Message Header for details)

time_stamp :: Date (8 bytes)
              Time the message was successfully created or delivered
```
**Hinweise:** - Der Zeitstempel wird vom Ersteller stets auf die aktuelle Zeit gesetzt. Es gibt jedoch mehrere Verwendungen dafür im Code, und in Zukunft könnten weitere hinzukommen - Diese Nachricht wird in SSU auch als Bestätigung einer aufgebauten Sitzung verwendet. In diesem Fall wird die Nachrichten-ID auf eine Zufallszahl gesetzt, und die "Ankunftszeit" wird auf die aktuelle netzwerkweite ID gesetzt, die derzeit 2 ist (d. h., `0x0000000000000002`) - DeliveryStatus wird typischerweise in eine GarlicMessage verpackt und durch einen tunnel gesendet, um eine Bestätigung zu liefern, ohne den Absender offenzulegen - Wird für tunnel-Tests verwendet, um Latenz und Zuverlässigkeit zu messen

**Quellcode:** - `net.i2p.data.i2np.DeliveryStatusMessage` - Verwendet in: `net.i2p.router.tunnel.InboundEndpointProcessor` für tunnel-Tests

---

### GarlicMessage (I2NP-Nachricht; Typ 11)

**WARNUNG:** Dies ist das Format, das für ElGamal-verschlüsselte Garlic-Nachrichten verwendet wird. Das Format für ECIES-AEAD-X25519-Ratchet-Garlic-Nachrichten ist erheblich unterschiedlich. Siehe [ECIES-Spezifikation](/docs/specs/ecies/) für das moderne Format.

**Zweck:** Wird verwendet, um mehrere verschlüsselte I2NP-Nachrichten zu kapseln.

**Inhalt:** Nach der Entschlüsselung enthält es eine Reihe von Garlic Cloves (Einzelelemente einer Garlic-Nachricht) und zusätzliche Daten, auch als Clove Set bezeichnet.

**Verschlüsseltes Format:**

```
+----+----+----+----+----+----+----+----+
| length (4)            | data          |
+----+----+----+----+----+              +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

length :: 4 byte Integer
          Number of bytes that follow (0 to 64 KB)

data :: $length bytes
        ElGamal encrypted data
```
**Entschlüsselte Daten (Clove Set, Menge einzelner Teilnachrichten innerhalb einer gebündelten Nachricht):**

```
+----+----+----+----+----+----+----+----+
| num| clove 1 (variable)               |
+----+                                  +
|                                       |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| clove 2 (variable)                    |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Certificate (3) | Message_ID (4)  |
+----+----+----+----+----+----+----+----+
    Expiration (8)                  |
+----+----+----+----+----+----+----+----+

num :: 1 byte Integer
       Number of GarlicCloves to follow

clove :: GarlicClove (see GarlicClove structure above)

Certificate :: Always NULL (3 bytes total, all zeroes)

Message_ID :: 4 byte Integer

Expiration :: Date (8 bytes)
```

**Für das ECIES-X25519-AEAD-Ratchet-Format (aktueller Standard für routers):**

Siehe [ECIES-Spezifikation](/docs/specs/ecies/) und [Vorschlag 144](/proposals/144-ecies-x25519-aead-ratchet/).

**Quellcode:** - `net.i2p.data.i2np.GarlicMessage` - Verschlüsselung: `net.i2p.crypto.elgamal.ElGamalAESEngine` (veraltet) - Moderne Verschlüsselung: `net.i2p.crypto.ECIES` Pakete

---

### TunnelData (Typ 18)

**Zweck:** Eine Nachricht, die vom Gateway oder einem Teilnehmer eines tunnel an den nächsten Teilnehmer oder Endpunkt gesendet wird. Die Daten haben eine feste Länge und enthalten I2NP-Nachrichten, die fragmentiert, gebündelt, aufgefüllt und verschlüsselt sind.

**Format:**

```
+----+----+----+----+----+----+----+----+
| tunnelID (4)          | data (1024)   |
+----+----+----+----+----+              +
|                                       |
~                                       ~
|                                       |
+                   +----+----+----+----+
|                   |
+----+----+----+----+

tunnelId :: 4 bytes
            TunnelId identifying the tunnel this message is directed at
            Nonzero

data :: 1024 bytes
        Payload data, fixed to 1024 bytes
```
**Aufbau der Nutzdaten (1024 Bytes):**

```
Bytes 0-15: Initialization Vector (IV) for AES encryption
Bytes 16-1023: Encrypted tunnel message data (1008 bytes)
```
**Hinweise:** - Die I2NP-Nachrichten-ID für TunnelData wird bei jedem Hop (Sprung) auf eine neue Zufallszahl gesetzt - Das tunnel-Nachrichtenformat (innerhalb der verschlüsselten Daten) ist in [Spezifikation für tunnel-Nachrichten](/docs/specs/implementation/) definiert - Jeder Hop entschlüsselt eine Schicht mit AES-256 im CBC-Modus - Der IV (Initialisierungsvektor) wird bei jedem Hop anhand der entschlüsselten Daten aktualisiert - Die Gesamtgröße beträgt genau 1,028 Bytes (4 tunnelId + 1024 data) - Dies ist die grundlegende Einheit des tunnel-Verkehrs - TunnelData-Nachrichten transportieren fragmentierte I2NP-Nachrichten (GarlicMessage, DatabaseStore, usw.)

**Quellcode:** - `net.i2p.data.i2np.TunnelDataMessage` - Konstante: `TunnelDataMessage.DATA_LENGTH = 1024` - Verarbeitung: `net.i2p.router.tunnel.InboundGatewayProcessor`

---

### TunnelGateway (Typ 19)

**Zweck:** Kapselt eine weitere I2NP-Nachricht, die am Eingangs-Gateway von einem tunnel in diesen tunnel eingespeist werden soll.

**Format:**

```
+----+----+----+----+----+----+----+-//
| tunnelId (4)          | length (2)| data...
+----+----+----+----+----+----+----+-//

tunnelId :: 4 bytes
            TunnelId identifying the tunnel this message is directed at
            Nonzero

length :: 2 byte Integer
          Length of the payload

data :: $length bytes
        Actual payload of this message
```
**Hinweise:** - Die Nutzlast ist eine I2NP-Nachricht mit einem standardmäßigen 16-Byte-Header - Dient dazu, Nachrichten vom lokalen router in tunnels einzuspeisen - Das Gateway fragmentiert die eingeschlossene Nachricht bei Bedarf - Nach der Fragmentierung werden die Fragmente in TunnelData-Nachrichten verpackt - TunnelGateway wird nie über das Netzwerk gesendet; es ist ein interner Nachrichtentyp, der vor der Verarbeitung im tunnel verwendet wird

**Quellcode:** - `net.i2p.data.i2np.TunnelGatewayMessage` - Verarbeitung: `net.i2p.router.tunnel.OutboundGatewayProcessor`

---

### DataMessage (Typ 20)

**Zweck:** Wird von Garlic Messages (Garlic-Nachrichten) und Garlic Cloves (Teilnachrichten) verwendet, um beliebige Daten zu kapseln (typischerweise Ende-zu-Ende-verschlüsselte Anwendungsdaten).

**Format:**

```
+----+----+----+----+----+----+-//-+
| length (4)            | data...    |
+----+----+----+----+----+----+-//-+

length :: 4 bytes
          Length of the payload

data :: $length bytes
        Actual payload of this message
```
**Hinweise:** - Diese Nachricht enthält keine Routing-Informationen und wird niemals "unverpackt" gesendet - Wird nur innerhalb von Garlic messages (Garlic-Nachrichten) verwendet - Enthält typischerweise Ende-zu-Ende-verschlüsselte Anwendungsdaten (HTTP, IRC, E-Mail usw.) - Die Daten sind üblicherweise eine ElGamal/AES- oder ECIES-verschlüsselte Nutzlast - Die maximal praktikable Länge beträgt aufgrund der Fragmentierungsgrenzen von tunnel-Nachrichten etwa 61,2 KB

**Quellcode:** - `net.i2p.data.i2np.DataMessage`

---

### TunnelBuild (Tunnelaufbau, Typ 21)

**VERALTET.** Verwenden Sie VariableTunnelBuild (variabler Aufbau eines tunnel) (Typ 23) oder ShortTunnelBuild (kurzformatiger Aufbau eines tunnel) (Typ 25).

**Zweck:** Aufbauanfrage für einen tunnel mit fester Länge über 8 Sprünge.

**Format:**

```
+----+----+----+----+----+----+----+----+
| Record 0 (528 bytes)                  |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Record 1 (528 bytes)                  |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Record 7 (528 bytes)                  |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

Just 8 BuildRequestRecords attached together
Record size: 528 bytes
Total size: 8 × 528 = 4,224 bytes
```
**Hinweise:** - Ab 0.9.48 kann es ECIES-X25519 BuildRequestRecords enthalten (BuildRequestRecords nach ECIES-X25519). Siehe [ECIES Tunnel-Erstellung](/docs/specs/implementation/) - Siehe [Spezifikation zur Tunnel-Erstellung](/docs/specs/implementation/) für Details - Die I2NP-Nachrichten-ID für diese Nachricht muss gemäß der Spezifikation zur Tunnel-Erstellung gesetzt werden - Obwohl dies im heutigen Netzwerk selten zu sehen ist (durch VariableTunnelBuild ersetzt), kann es für sehr lange tunnels weiterhin verwendet werden und wurde nicht formell als veraltet markiert - Routers müssen dies aus Kompatibilitätsgründen weiterhin implementieren - Das feste 8-Record-Format ist unflexibel und verschwendet Bandbreite bei kürzeren tunnels

**Quellcode:** - `net.i2p.data.i2np.TunnelBuildMessage` - Konstante: `TunnelBuildMessageBase.MAX_RECORD_COUNT = 8`

---

### TunnelBuildReply (Typ 22)

**Veraltet.** Verwenden Sie VariableTunnelBuildReply (Typ 24) oder OutboundTunnelBuildReply (Typ 26).

**Zweck:** Antwort auf den tunnel-Aufbau mit fester Länge für 8 Sprünge.

**Format:**

Dasselbe Format wie TunnelBuildMessage, mit BuildResponseRecords statt BuildRequestRecords.

```
Total size: 8 × 528 = 4,224 bytes
```
**Hinweise:** - Seit 0.9.48 kann es ECIES-X25519 BuildResponseRecords enthalten. Siehe [ECIES Tunnel Creation](/docs/specs/implementation/) - Siehe [Tunnel Creation Specification](/docs/specs/implementation/) für Details - Die I2NP message ID für diese Nachricht muss gemäß der Tunnel Creation Specification gesetzt werden - Obwohl im heutigen Netzwerk selten anzutreffen (ersetzt durch VariableTunnelBuildReply), kann es für sehr lange tunnel weiterhin verwendet werden und wurde nicht formell als veraltet eingestuft - Routers müssen dies zur Wahrung der Kompatibilität weiterhin implementieren

**Quellcode:** - `net.i2p.data.i2np.TunnelBuildReplyMessage`

---

### VariableTunnelBuild (Typ 23)

**Zweck:** tunnel-Aufbau mit variabler Länge für 1-8 Hops. Unterstützt sowohl ElGamal- als auch ECIES-X25519 routers.

**Format:**

```
+----+----+----+----+----+----+----+----+
| num| BuildRequestRecords (variable)   |
+----+----+----+----+----+----+----+----+

num :: 1 byte Integer
       Valid values: 1-8

BuildRequestRecords :: $num records of 528 bytes each

Record size: 528 bytes
Total size: 1 + ($num × 528) bytes
```
**Hinweise:** - Seit 0.9.48 können ECIES-X25519 BuildRequestRecords enthalten sein. Siehe [ECIES tunnel-Erstellung](/docs/specs/implementation/) - Eingeführt in router-Version 0.7.12 (2009) - Darf nicht an tunnel-Teilnehmer mit Versionen älter als 0.7.12 gesendet werden - Siehe [Spezifikation zur tunnel-Erstellung](/docs/specs/implementation/) für Details - Die I2NP-Message-ID muss gemäß der tunnel-Erstellungsspezifikation gesetzt werden - **Typische Anzahl der Datensätze:** 4 (für einen 4-Hop-tunnel) - **Typische Gesamtgröße:** 1 + (4 × 528) = 2.113 Bytes - Dies ist die Standard-tunnel-Build-Nachricht für ElGamal router - ECIES router verwenden typischerweise stattdessen ShortTunnelBuild (Typ 25)

**Quellcode:** - `net.i2p.data.i2np.VariableTunnelBuildMessage`

---

### VariableTunnelBuildReply (Typ 24)

**Zweck:** tunnel-Build-Antwort mit variabler Länge für 1-8 Sprünge. Unterstützt sowohl ElGamal- als auch ECIES-X25519-routers.

**Format:**

Gleiches Format wie VariableTunnelBuildMessage, mit BuildResponseRecords statt BuildRequestRecords.

```
+----+----+----+----+----+----+----+----+
| num| BuildResponseRecords (variable)  |
+----+----+----+----+----+----+----+----+

num :: 1 byte Integer
       Valid values: 1-8

BuildResponseRecords :: $num records of 528 bytes each

Record size: 528 bytes
Total size: 1 + ($num × 528) bytes
```
**Hinweise:** - Seit 0.9.48 kann es ECIES-X25519 BuildResponseRecords enthalten. Siehe [ECIES Tunnel Creation](/docs/specs/implementation/) - Eingeführt in router-Version 0.7.12 (2009) - Darf nicht an Tunnel-Teilnehmer mit einer Version früher als 0.7.12 gesendet werden - Siehe [Tunnel Creation Specification](/docs/specs/implementation/) für Details - Die I2NP-Nachrichten-ID muss gemäß der Tunnel Creation Specification gesetzt werden - **Typische Anzahl der Datensätze:** 4 - **Typische Gesamtgröße:** 2.113 Bytes

**Quellcode:** - `net.i2p.data.i2np.VariableTunnelBuildReplyMessage`

---

### ShortTunnelBuild (Typ 25)

**Zweck:** Kurze Nachrichten zum tunnel-Aufbau nur für ECIES-X25519 routers. Eingeführt in API-Version 0.9.51 (Release 1.5.0, August 2021). Dies ist der aktuelle Standard für den ECIES-tunnel-Aufbau.

**Format:**

```
+----+----+----+----+----+----+----+----+
| num| ShortBuildRequestRecords (var)   |
+----+----+----+----+----+----+----+----+

num :: 1 byte Integer
       Valid values: 1-8

ShortBuildRequestRecords :: $num records of 218 bytes each

Record size: 218 bytes
Total size: 1 + ($num × 218) bytes
```
**Hinweise:** - Eingeführt in router-Version 0.9.51 (Release 1.5.0, August 2021) - Darf an tunnel-Teilnehmer nicht vor API-Version 0.9.51 gesendet werden - Siehe [ECIES Tunnel-Erstellung](/docs/specs/implementation/) für die vollständige Spezifikation - Siehe [Proposal 157](/proposals/157-new-tbm/) für die Begründung - **Typische Anzahl der Datensätze:** 4 - **Typische Gesamtgröße:** 1 + (4 × 218) = 873 Bytes - **Bandbreitenersparnis:** 59% kleiner als VariableTunnelBuild (873 vs 2,113 Bytes) - **Leistungsvorteil:** 4 kurze Datensätze passen in eine tunnel-Nachricht; VariableTunnelBuild erfordert 3 tunnel-Nachrichten - Dies ist jetzt das Standard-tunnel-Build-Format für reine ECIES-X25519 tunnels - Datensätze leiten Schlüssel mittels HKDF ab, statt sie explizit mitzuliefern

**Quellcode:** - `net.i2p.data.i2np.ShortTunnelBuildMessage` - Konstante: `ShortEncryptedBuildRecord.RECORD_SIZE = 218`

---

### OutboundTunnelBuildReply (Typ 26)

**Zweck:** Vom ausgehenden Endpunkt eines neuen tunnel an den Initiator gesendet. Nur für ECIES-X25519 routers. Eingeführt in API-Version 0.9.51 (Release 1.5.0, August 2021).

**Format:**

Gleiches Format wie ShortTunnelBuildMessage, mit ShortBuildResponseRecords statt ShortBuildRequestRecords.

```
+----+----+----+----+----+----+----+----+
| num| ShortBuildResponseRecords (var)  |
+----+----+----+----+----+----+----+----+

num :: 1 byte Integer
       Valid values: 1-8

ShortBuildResponseRecords :: $num records of 218 bytes each

Record size: 218 bytes
Total size: 1 + ($num × 218) bytes
```
**Hinweise:** - Eingeführt in router Version 0.9.51 (Release 1.5.0, August 2021) - Siehe [ECIES Tunnel-Erstellung](/docs/specs/implementation/) für die vollständige Spezifikation - **Typische Anzahl der Datensätze:** 4 - **Typische Gesamtgröße:** 873 Bytes - Diese Antwort wird vom ausgehenden Endpunkt (OBEP) über den neu erstellten ausgehenden tunnel zurück an den tunnel-Ersteller gesendet - Bestätigt, dass alle Hops den tunnel-Aufbau akzeptiert haben

**Quellcode:** - `net.i2p.data.i2np.OutboundTunnelBuildReplyMessage`

---

## Referenzen

### Offizielle Spezifikationen

- **[I2NP-Spezifikation](/docs/specs/i2np/)** - Vollständige Spezifikation des I2NP-Nachrichtenformats
- **[Gemeinsame Strukturen](/docs/specs/common-structures/)** - Datentypen und -strukturen, die in ganz I2P verwendet werden
- **[Tunnel-Erstellung](/docs/specs/implementation/)** - ElGamal Tunnel-Erstellung (veraltet)
- **[ECIES Tunnel-Erstellung](/docs/specs/implementation/)** - ECIES-X25519 Tunnel-Erstellung (aktuell)
- **[Tunnel-Nachricht](/docs/specs/implementation/)** - Format der Tunnel-Nachricht und Zustellungsanweisungen
- **[NTCP2-Spezifikation](/docs/specs/ntcp2/)** - TCP-Transportprotokoll
- **[SSU2-Spezifikation](/docs/specs/ssu2/)** - UDP-Transportprotokoll
- **[ECIES-Spezifikation](/docs/specs/ecies/)** - ECIES-X25519-AEAD-Ratchet-Verschlüsselung
- **[Kryptografie-Spezifikation](/docs/specs/cryptography/)** - Kryptografische Primitive auf niedriger Ebene
- **[I2CP-Spezifikation](/docs/specs/i2cp/)** - Spezifikation des Client-Protokolls
- **[Datagram-Spezifikation](/docs/api/datagrams/)** - Formate von Datagram2 und Datagram3

### Vorschläge

- **[Proposal 123](/proposals/123-new-netdb-entries/)** - Neue netDB-Einträge (LeaseSet2, EncryptedLeaseSet, MetaLeaseSet)
- **[Proposal 144](/proposals/144-ecies-x25519-aead-ratchet/)** - ECIES-X25519-AEAD-Ratchet-Verschlüsselung
- **[Proposal 154](/proposals/154-ecies-lookups/)** - Verschlüsselte Datenbankabfrage
- **[Proposal 156](/proposals/156-ecies-routers/)** - ECIES-Router
- **[Proposal 157](/proposals/157-new-tbm/)** - Kleinere tunnel-build-Nachrichten (Kurzformat)
- **[Proposal 159](/proposals/159-ssu2/)** - SSU2-Transport
- **[Proposal 161](/de/proposals/161-ri-dest-padding/)** - Komprimierbares Padding
- **[Proposal 163](/proposals/163-datagram2/)** - Datagram2 und Datagram3
- **[Proposal 167](/proposals/167-service-records/)** - Service-Record-Parameter im LeaseSet
- **[Proposal 168](/proposals/168-tunnel-bandwidth/)** - Bandbreitenparameter für tunnel build
- **[Proposal 169](/proposals/169-pq-crypto/)** - Post-Quanten-Hybridkryptografie

### Dokumentation

- **[Garlic Routing](/docs/overview/garlic-routing/)** (mehrschichtiges Routing) - Mehrschichtiges Nachrichtenbündeln
- **[ElGamal/AES](/docs/legacy/elgamal-aes/)** - Veraltetes Verschlüsselungsschema
- **[Tunnel Implementation](/docs/specs/implementation/)** - Fragmentierung und Verarbeitung
- **[Network Database](/docs/specs/common-structures/)** - Verteilte Hash-Tabelle
- **[NTCP2 Transport](/docs/specs/ntcp2/)** - TCP-Transportspezifikation
- **[SSU2 Transport](/docs/specs/ssu2/)** - UDP-Transportspezifikation
- **[Technical Introduction](/docs/overview/tech-intro/)** - Überblick über die I2P-Architektur

### Quellcode

- **[Java-I2P-Repository](https://i2pgit.org/I2P_Developers/i2p.i2p)** - Offizielle Java-Implementierung
- **[GitHub-Spiegel](https://github.com/i2p/i2p.i2p)** - GitHub-Spiegel von Java I2P
- **[i2pd-Repository](https://github.com/PurpleI2P/i2pd)** - C++-Implementierung

### Wichtige Quellcode-Verzeichnisse

**Java I2P (i2pgit.org/I2P_Developers/i2p.i2p):** - `core/java/src/net/i2p/data/i2np/` - I2NP-Nachrichten-Implementierungen - `core/java/src/net/i2p/crypto/` - Kryptografische Implementierungen - `router/java/src/net/i2p/router/tunnel/` - Tunnel-Verarbeitung - `router/java/src/net/i2p/router/transport/` - Transport-Implementierungen

**Konstanten und Werte:** - `I2NPMessage.MAX_SIZE = 65536` - Maximale I2NP-Nachrichtengröße - `I2NPMessageImpl.HEADER_LENGTH = 16` - Standard-Headergröße - `TunnelDataMessage.DATA_LENGTH = 1024` - Nutzlast der Tunnel-Nachricht - `EncryptedBuildRecord.RECORD_SIZE = 528` - Langer Build-Datensatz (Build: Aufbau) - `ShortEncryptedBuildRecord.RECORD_SIZE = 218` - Kurzer Build-Datensatz - `TunnelBuildMessageBase.MAX_RECORD_COUNT = 8` - Max. Datensätze pro Build

---

## Anhang A: Netzwerkstatistiken und aktueller Status

### Netzwerkzusammensetzung (Stand: Oktober 2025)

- **Gesamtzahl der Router:** Ungefähr 60,000-70,000 (variiert)
- **Floodfill-Router:** Ungefähr 500-700 aktiv
- **Verschlüsselungstypen:**
  - ECIES-X25519: >95% der Router
  - ElGamal: <5% der Router (veraltet, nur Legacy (Altbestand))
- **Einsatz der Transportprotokolle:**
  - SSU2: >60% primäres Transportprotokoll
  - NTCP2: ~40% primäres Transportprotokoll
  - Legacy-Transporte (SSU1, NTCP): 0% (entfernt)
- **Signaturtypen:**
  - EdDSA (Ed25519): Überwiegende Mehrheit
  - ECDSA: Kleiner Prozentsatz
  - RSA: Nicht zulässig (entfernt)

### Mindestanforderungen für den Router

- **API-Version:** 0.9.16+ (für EdDSA-Kompatibilität mit dem Netzwerk)
- **Empfohlenes Minimum:** API 0.9.51+ (ECIES Kurz-tunnel-Builds)
- **Aktuelles Minimum für floodfills:** API 0.9.58+ (Abkündigung des ElGamal router)
- **Bevorstehende Voraussetzung:** Java 17+ (ab Version 2.11.0, Dezember 2025)

### Bandbreitenanforderungen

- **Minimum:** 128 KBytes/sec (N-Flag oder höher) für floodfill
- **Empfohlen:** 256 KBytes/sec (O-Flag) oder höher
- **Anforderungen für Floodfill:**
  - Mindestens 128 KB/sec Bandbreite
  - Stabile Betriebszeit (>95% empfohlen)
  - Geringe Latenz (<500ms zu Peers)
  - Health-Checks bestehen (Warteschlangenzeit, Job-Verzögerung)

### Tunnel-Statistiken

- **Typische Tunnel-Länge:** 3-4 Hops
- **Maximale Tunnel-Länge:** 8 Hops (theoretisch, selten verwendet)
- **Typische Tunnel-Lebensdauer:** 10 Minuten
- **Erfolgsrate beim Tunnelaufbau:** >85% für gut vernetzte Router
- **Nachrichtenformat für den Tunnelaufbau:**
  - ECIES Router: ShortTunnelBuild (218-Byte-Datensätze)
  - Gemischte Tunnel: VariableTunnelBuild (528-Byte-Datensätze)

### Leistungsmetriken

- **Tunnel-Aufbauzeit:** 1-3 Sekunden (typisch)
- **Ende-zu-Ende-Latenz:** 0,5-2 Sekunden (typisch, insgesamt 6-8 Hops)
- **Durchsatz:** Begrenzt durch die tunnel-Bandbreite (typischerweise 10-50 KB/sec pro tunnel)
- **Maximale Datagrammgröße:** 10 KB empfohlen (61,2 KB theoretisches Maximum)

---

## Anhang B: Veraltete und entfernte Funktionen

### Vollständig entfernt (nicht mehr unterstützt)

- **NTCP-Transport** - In Release 0.9.50 entfernt (Mai 2021)
- **SSU v1-Transport** - Aus Java I2P in Release 2.4.0 entfernt (Dezember 2023)
- **SSU v1-Transport** - Aus i2pd in Release 2.44.0 entfernt (November 2022)
- **RSA-Signaturtypen** - Seit API 0.9.28 nicht mehr zugelassen

### Veraltet (unterstützt, aber nicht empfohlen)

- **ElGamal routers** - Seit API 0.9.58 (März 2023) veraltet
  - ElGamal-Destinationen weiterhin unterstützt zur Abwärtskompatibilität
  - Neue routers sollten ausschließlich ECIES-X25519 verwenden
- **TunnelBuild (Typ 21)** - Veraltet zugunsten von VariableTunnelBuild und ShortTunnelBuild
  - Weiterhin implementiert für sehr lange tunnels (>8 Hops)
- **TunnelBuildReply (Typ 22)** - Veraltet zugunsten von VariableTunnelBuildReply und OutboundTunnelBuildReply
- **ElGamal/AES-Verschlüsselung** - Veraltet zugunsten von ECIES-X25519-AEAD-Ratchet
  - Wird weiterhin für Legacy-Destinationen verwendet
- **Lange ECIES-BuildRequestRecords (528 Bytes)** - Veraltet zugunsten des kurzen Formats (218 Bytes)
  - Wird weiterhin für gemischte tunnels mit ElGamal-Hops verwendet

### Zeitplan für die Unterstützung älterer Versionen

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Feature</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Introduced</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Deprecated</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Removed</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">NTCP</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2003</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2018 (0.9.36)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2021 (0.9.50)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Replaced by NTCP2</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SSU v1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2004</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2022 (0.9.54)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2023 (Java) / 2022 (i2pd)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Replaced by SSU2</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal routers</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2003</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2023 (0.9.58)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">TBD</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destinations still supported</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">RSA signatures</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2015</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2017</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2017 (0.9.28)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Never widely used</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">TunnelBuild</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2004</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2009 (0.7.12)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Not removed</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Still supported for long tunnels</td>
    </tr>
  </tbody>
</table>
---

## Anhang C: Zukünftige Entwicklungen

### Post-Quanten-Kryptografie

**Status:** Beta seit Release 2.10.0 (September 2025), wird mit 2.11.0 (Dezember 2025) zum Standard

**Implementierung:** - Hybrider Ansatz, der klassisches X25519 und Post-Quanten-MLKEM (ML-KEM-768) kombiniert - Abwärtskompatibel mit der bestehenden ECIES-X25519-Infrastruktur - Verwendet den Signal-Double-Ratchet-Algorithmus mit sowohl klassischem als auch PQ-Schlüsselmaterial (Post-Quanten) - Siehe [Proposal 169](/proposals/169-pq-crypto/) für Details

**Migrationspfad:** 1. Release 2.10.0 (September 2025): Als Beta-Option verfügbar 2. Release 2.11.0 (Dezember 2025): Standardmäßig aktiviert 3. Zukünftige Releases: Schließlich verpflichtend

### Geplante Funktionen

- **IPv6-Verbesserungen** - Bessere IPv6-Unterstützung und Übergangsmechanismen
- **Pro-tunnel-Drosselung** - Fein abgestimmte Bandbreitenkontrolle pro tunnel
- **Erweiterte Metriken** - Verbesserte Leistungsüberwachung und Diagnostik
- **Protokolloptimierungen** - Reduzierter Overhead und verbesserte Effizienz
- **Verbesserte floodfill-Auswahl (Knoten mit spezieller Rolle zur Verteilung der netDb)** - Bessere Verteilung der Netzwerkdatenbank

### Forschungsbereiche

- **Tunnel-Längenoptimierung** - Dynamische Tunnel-Länge basierend auf dem Bedrohungsmodell
- **Erweitertes Padding** - Verbesserungen der Widerstandsfähigkeit gegen Verkehrsanalyse
- **Neue Verschlüsselungsschemata** - Vorbereitung auf Bedrohungen durch Quantencomputing
- **Überlastkontrolle** - Bessere Handhabung der Netzwerklast
- **Mobile Unterstützung** - Optimierungen für mobile Geräte und Netzwerke

---

## Anhang D: Implementierungsrichtlinien

### Für neue Implementierungen

**Mindestanforderungen:** 1. Funktionen der API-Version 0.9.51+ unterstützen 2. ECIES-X25519-AEAD-Ratchet-Verschlüsselung implementieren 3. NTCP2- und SSU2-Transportprotokolle unterstützen 4. ShortTunnelBuild-Nachrichten (218-Byte-Datensätze) implementieren 5. LeaseSet2-Varianten (Typen 3, 5, 7) unterstützen 6. EdDSA-Signaturen verwenden (Ed25519)

**Empfohlen:** 1. Hybride Post-Quanten-Kryptografie unterstützen (ab 2.11.0) 2. Bandbreitenparameter pro tunnel implementieren 3. Datagram2- und Datagram3-Formate unterstützen 4. Service-Record-Optionen in LeaseSets implementieren 5. Den offiziellen Spezifikationen unter /docs/specs/ folgen

**Nicht erforderlich:** 1. Unterstützung für ElGamal router (veraltet) 2. Unterstützung für Legacy-Transporte (SSU1, NTCP) 3. Lange ECIES BuildRequestRecords (Anforderungsdatensätze für den Aufbau) (528 Bytes für reine ECIES tunnels) 4. TunnelBuild/TunnelBuildReply-Nachrichten (verwenden Sie die Varianten Variable oder Short)

### Testen und Validierung

**Protokollkonformität:** 1. Teste die Interoperabilität mit dem offiziellen Java I2P router 2. Teste die Interoperabilität mit dem i2pd C++ router 3. Validiere die Nachrichtenformate anhand der Spezifikationen 4. Teste die tunnel-Aufbau-/Abbauzyklen 5. Verifiziere die Verschlüsselung/Entschlüsselung mit Testvektoren

**Leistungstests:** 1. Erfolgsraten beim tunnel-Aufbau messen (sollten >85 % betragen) 2. Mit verschiedenen tunnel-Längen testen (2-8 Sprünge) 3. Fragmentierung und Reassemblierung validieren 4. Unter Last testen (mehrere gleichzeitige tunnel) 5. End-to-End-Latenz messen

**Sicherheitstests:** 1. Verschlüsselungsimplementierung verifizieren (Testvektoren verwenden) 2. Schutz vor Replay-Angriffen testen 3. Umgang mit Ablaufzeiten von Nachrichten validieren 4. Gegen fehlerhaft formatierte Nachrichten testen 5. Ordnungsgemäße Zufallszahlengenerierung verifizieren

### Häufige Fallstricke bei der Implementierung

1. **Verwirrende Formate der Zustellhinweise** - garlic clove (Teilnachricht beim Garlic-Routing) vs tunnel message
2. **Fehlerhafte Schlüsselableitung** - HKDF-Verwendung für short build records (kurze Build-Datensätze)
3. **Message-ID-Behandlung** - Nicht korrekt gesetzt für tunnel builds
4. **Fragmentierungsprobleme** - Die praktische Grenze von 61,2 KB wird nicht eingehalten
5. **Endianness-Fehler** - Java verwendet Big-Endian für alle Ganzzahlen
6. **Behandlung von Ablaufzeiten** - Das Kurzformat läuft am 7. Februar 2106 über (Überlauf)
7. **Prüfsummenerzeugung** - Weiterhin erforderlich, auch wenn sie nicht verifiziert wird
