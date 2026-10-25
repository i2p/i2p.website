---
title: "I2NP-Spezifikation"
description: "I2NP-Nachrichtenformate, Prioritäten und gemeinsame Strukturen für die Router-zu-Router-Kommunikation."
slug: "i2np"
aliases:
  - "/de/spec/i2np"
  - "/de/spec/i2np/"
category: "Protokolle"
lastUpdated: "2026-03"
accurateFor: "0.9.69"
---

## Übersicht

Das I2P Network Protocol (I2NP) ist die Schicht oberhalb der I2P-Transportprotokolle. Es ist ein router-zu-router Protokoll. Es wird für netDb-Lookups und -Antworten, für die Erstellung von tunnels und für verschlüsselte router- und Client-Datennachrichten verwendet. I2NP-Nachrichten können punkt-zu-punkt an einen anderen router gesendet werden oder anonym durch tunnels an diesen router übertragen werden.

## Protokollversionen {#versions}

Alle Router müssen ihre I2NP-Protokollversion im Feld "router.version" in den RouterInfo-Eigenschaften veröffentlichen. Dieses Versionsfeld ist die API-Version, die das Unterstützungsniveau für verschiedene I2NP-Protokollfeatures anzeigt, und ist nicht notwendigerweise die tatsächliche Router-Version.

Wenn alternative (Nicht-Java) router Versionsinformationen über die tatsächliche Router-Implementierung veröffentlichen möchten, müssen sie dies in einer anderen Eigenschaft tun. Andere Versionen als die unten aufgeführten sind erlaubt. Die Unterstützung wird durch einen numerischen Vergleich bestimmt; zum Beispiel impliziert 0.9.13 Unterstützung für 0.9.12-Funktionen. Beachten Sie, dass die "coreVersion"-Eigenschaft nicht mehr in den router-Informationen veröffentlicht wird und niemals zur Bestimmung der I2NP-Protokollversion verwendet wurde.

Eine grundlegende Zusammenfassung der I2NP-Protokollversionen ist wie folgt. Einzelheiten finden Sie weiter unten.

<table style="border-collapse: collapse; width: 100%;">
<thead>
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">API Version</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">Required I2NP Features</th>
</tr>
</thead>
<tbody>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.68</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Tunnel testing required</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">LeaseSet2 service record options (see proposal 167)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.65</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Tunnel build bandwidth parameters (see proposal 168)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.62</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Minimum peers will build tunnels through, as of 0.9.68<br>Minimum floodfill peers will send DSM to, as of 0.9.68</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.59</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Minimum peers will build tunnels through, as of 0.9.63<br>Minimum floodfill peers will send DSM to, as of 0.9.63</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.58</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Minimum peers will build tunnels through, as of 0.9.62<br>ElGamal Routers deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.55</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">SSU2 transport support (if published in router info)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.51</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Short tunnel build messages for ECIES-X25519 routers<br>Minimum peers will build tunnels through, as of 0.9.58<br>Minimum floodfill peers will send DSM to, as of 0.9.58</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.49</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Garlic messages to ECIES-X25519 routers</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.48</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES-X25519 Routers<br>ECIES-X25519 Build Request/Response records</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.46</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">DatabaseLookup flag bit 4 for AEAD reply</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.44</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES-X25519 keys in LeaseSet2</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.40</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">MetaLeaseSet may be sent in a DSM</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.39</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">EncryptedLeaseSet may be sent in a DSM<br>RedDSA_SHA512_Ed25519 signature type supported for destinations and leasesets</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">DSM type bits 3-0 now contain the type; LeaseSet2 may be sent in a DSM</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.36</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">NTCP2 transport support (if published in router info)<br>Minimum peers will build tunnels through, as of 0.9.46</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.28</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">RSA sig types disallowed<br>Minimum floodfill peers will send DSM to, as of 0.9.34</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.18</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">DSM type bits 7-1 ignored</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.16</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">RI key certs / ECDSA and EdDSA sig types<br>Note: RSA sig types also supported as of this version, but currently unused<br>DLM lookup types (DLM flag bits 3-2)<br>Minimum version compatible with vast majority of current network, since routers are now using the EdDSA sig type.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.15</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest/LS key certs w/ EdDSA Ed25519 sig type (if floodfill)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest/LS key certs w/ ECDSA P-256, P-384, and P-521 sig types (if floodfill)<br>Note: RSA sig types also supported as of this version, but currently unused<br>Nonzero expiration allowed in RouterAddress</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Encrypted DSM/DSRM replies supported (DLM flag bit 1) (if floodfill)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Nonzero DLM flag bits 7-1 allowed</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Requires zero expiration in RouterAddress</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Supports up to 16 leases in a DSM LS store (6 previously)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">VTBM and VTBRM message support</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.10</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Floodfill supports encrypted DSM stores</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.9 or lower</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">All messages and features not listed above</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.6.1.10</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">TBM and TBRM messages introduced<br>Minimum version compatible with current network</td>
</tr>
</tbody>
</table>
Beachten Sie, dass es auch transportbezogene Funktionen und Kompatibilitätsprobleme gibt; siehe die NTCP- und SSU-Transport-Dokumentation für Details.

## Allgemeine Strukturen {#structures}

Die folgenden Strukturen sind Elemente mehrerer I2NP-Nachrichten. Sie sind keine vollständigen Nachrichten.

### I2NP Message Header {#struct-I2NPMessageHeader}

#### Beschreibung

Gemeinsamer Header für alle I2NP-Nachrichten, der wichtige Informationen wie eine Prüfsumme, ein Ablaufdatum usw. enthält.

#### Inhalt

Es werden drei verschiedene Formate verwendet, je nach Kontext; ein Standardformat und zwei Kurzformate.

Das standardmäßige 16-Byte-Format enthält 1 Byte [Integer](/docs/specs/common-structures/#integer), das den Typ dieser Nachricht angibt, gefolgt von einem 4-Byte [Integer](/docs/specs/common-structures/#integer), der die Nachrichten-ID angibt. Danach folgt ein Ablaufdatum [Date](/docs/specs/common-structures/#date), gefolgt von einem 2-Byte [Integer](/docs/specs/common-structures/#integer), der die Länge der Nachrichten-Nutzdaten angibt, gefolgt von einem [Hash](/docs/specs/common-structures/#hash), der auf das erste Byte gekürzt wird. Danach folgen die eigentlichen Nachrichtendaten.

Die kurzen Formate verwenden einen 4-Byte-Ablaufwert in Sekunden anstelle eines 8-Byte-Ablaufwerts in Millisekunden. Die kurzen Formate enthalten keine Prüfsumme oder Größenangabe, diese werden je nach Kontext von den Kapselungen bereitgestellt.

```
Standard (16 bytes):

+----+----+----+----+----+----+----+----+
|type|      msg_id       |  expiration
+----+----+----+----+----+----+----+----+
                         |  size   |chks|
+----+----+----+----+----+----+----+----+

Short (SSU, 5 bytes) (obsolete):

+----+----+----+----+----+
|type| short_expiration  |
+----+----+----+----+----+

Short (NTCP2, SSU2, and ECIES-Ratchet Garlic Cloves, 9 bytes):

+----+----+----+----+----+----+----+----+
|type|      msg_id       | short_expira-
+----+----+----+----+----+----+----+----+
 tion|
+----+

type :: Integer
        length -> 1 byte
        purpose -> identifies the message type (see table below)

msg_id :: Integer
          length -> 4 bytes
          purpose -> uniquely identifies this message (for some time at least)
                     This is usually a locally-generated random number, but
                     for outgoing tunnel build messages it may be derived from
                     the incoming message. See below.

expiration :: Date
              8 bytes
              date this message will expire

short_expiration :: Integer
                    4 bytes
                    date this message will expire (seconds since the epoch)

size :: Integer
        length -> 2 bytes
        purpose -> length of the payload

chks :: Integer
        length -> 1 byte
        purpose -> checksum of the payload
                   SHA256 hash truncated to the first byte

data ::
        length -> $size bytes
        purpose -> actual message contents
```
#### Anmerkungen

- Bei der Übertragung über [SSU](/docs/transports/ssu/) wird der 16-Byte-Standard-Header nicht verwendet. Es sind nur ein 1-Byte-Typ und eine 4-Byte-Ablaufzeit in Sekunden enthalten. Die Nachrichten-ID und Größe sind in das SSU-Datenpaketformat eingebunden. Die Prüfsumme ist nicht erforderlich, da Fehler bei der Entschlüsselung erkannt werden.

- Bei der Übertragung über [NTCP2](/docs/specs/ntcp2/) oder [SSU2](/docs/specs/ssu2/) wird der 16-Byte-Standard-Header nicht verwendet. Es sind nur ein 1-Byte-Typ, eine 4-Byte-Nachrichten-ID und eine 4-Byte-Ablaufzeit in Sekunden enthalten. Die Größe ist in die NTCP2- und SSU2-Datenpaketformate integriert. Die Prüfsumme ist nicht erforderlich, da Fehler bei der Entschlüsselung erkannt werden.

- Der Standard-Header ist auch für I2NP-Nachrichten erforderlich, die in anderen Nachrichten und Strukturen enthalten sind (Data, TunnelData, TunnelGateway und GarlicClove). Ab Version 0.8.12 ist die Prüfsummenverifikation an einigen Stellen im Protokollstapel deaktiviert, um den Overhead zu reduzieren. Jedoch ist aus Kompatibilitätsgründen mit älteren Versionen die Prüfsummengenerierung weiterhin erforderlich. Es ist ein Thema für zukünftige Forschung, Punkte im Protokollstapel zu bestimmen, wo die Version des entfernten routers bekannt ist und die Prüfsummengenerierung deaktiviert werden kann.

- Der kurze Ablaufzeitpunkt ist vorzeichenlos und wird am 7. Februar 2106 überlaufen. Ab diesem Datum muss ein Offset hinzugefügt werden, um die korrekte Zeit zu erhalten.

- Implementierungen können Nachrichten mit Ablaufzeiten ablehnen, die zu weit in der Zukunft liegen. Die empfohlene maximale Ablaufzeit liegt 60s in der Zukunft.

### BuildRequestRecord {#struct-BuildRequestRecord}

VERALTET, wird im aktuellen Netzwerk nur verwendet, wenn ein tunnel einen ElGamal router enthält. Siehe [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

#### Beschreibung

Ein Datensatz in einem Satz von mehreren Datensätzen zur Anforderung der Erstellung eines Hops im tunnel. Für weitere Details siehe die [tunnel-Übersicht](/docs/specs/tunnel-implementation/) und die [ElGamal tunnel-Erstellungsspezifikation](/docs/specs/tunnel-creation/).

Für ECIES-X25519 BuildRequestRecords siehe [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

#### Inhalt (ElGamal)

[TunnelId](/docs/specs/common-structures/#tunnelid) zum Empfangen von Nachrichten, gefolgt vom [Hash](/docs/specs/common-structures/#hash) unserer [RouterIdentity](/docs/specs/common-structures/#routeridentity). Danach folgen die [TunnelId](/docs/specs/common-structures/#tunnelid) und der [Hash](/docs/specs/common-structures/#hash) der [RouterIdentity](/docs/specs/common-structures/#routeridentity) des nächsten routers.

ElGamal und AES verschlüsselt:

```
+----+----+----+----+----+----+----+----+
| encrypted data...                     |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

encrypted_data :: ElGamal and AES encrypted data
                  length -> 528

total length: 528
```
ElGamal verschlüsselt:

```
+----+----+----+----+----+----+----+----+
| toPeer                                |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| encrypted data...                     |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

toPeer :: First 16 bytes of the SHA-256 Hash of the peer's RouterIdentity
          length -> 16 bytes

encrypted_data :: ElGamal-2048 encrypted data (see notes)
                  length -> 512

total length: 528
```
Klartext:

```
+----+----+----+----+----+----+----+----+
| receive_tunnel    | our_ident         |
+----+----+----+----+                   +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+                   +----+----+----+----+
|                   | next_tunnel       |
+----+----+----+----+----+----+----+----+
| next_ident                            |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| layer_key                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| iv_key                                |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| reply_key                             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| reply_iv                              |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag| request_time      | send_msg_id
+----+----+----+----+----+----+----+----+
     |                                  |
+----+                                  +
|         29 bytes padding              |
+                                       +
|                                       |
+                             +----+----+
|                             |
+----+----+----+----+----+----+

receive_tunnel :: TunnelId
                  length -> 4 bytes
                  nonzero

our_ident :: Hash
             length -> 32 bytes

next_tunnel :: TunnelId
               length -> 4 bytes
               nonzero

next_ident :: Hash
              length -> 32 bytes

layer_key :: SessionKey
             length -> 32 bytes

iv_key :: SessionKey
          length -> 32 bytes

reply_key :: SessionKey
             length -> 32 bytes

reply_iv :: data
            length -> 16 bytes

flag :: Integer
        length -> 1 byte

request_time :: Integer
                length -> 4 bytes
                Hours since the epoch, i.e. current time / 3600

send_message_id :: Integer
                   length -> 4 bytes

padding :: Data
           length -> 29 bytes
           source -> random

total length: 222
```
#### Hinweise

- Im 512-Byte verschlüsselten Datensatz enthalten die ElGamal-Daten die Bytes 1-256 und 258-513 des 514-Byte ElGamal-verschlüsselten Blocks [CRYPTO-ELG](/docs/specs/cryptography/#elgamal). Die beiden Padding-Bytes aus dem Block (die Null-Bytes an den Positionen 0 und 257) werden entfernt.

- Siehe die [Spezifikation zur Tunnel-Erstellung](/docs/specs/tunnel-creation/) für Details zu den Feldinhalten.

### BuildResponseRecord {#struct-BuildResponseRecord}

VERALTET, wird im aktuellen Netzwerk nur verwendet, wenn ein tunnel einen ElGamal router enthält. Siehe [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

#### Beschreibung

Ein Datensatz in einem Satz mehrerer Datensätze mit Antworten auf eine Build-Anfrage. Für weitere Details siehe die [tunnel-Übersicht](/docs/specs/tunnel-implementation/) und die [ElGamal tunnel-Erstellungsspezifikation](/docs/specs/tunnel-creation/).

Für ECIES-X25519 BuildResponseRecords, siehe [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

#### Inhalte (ElGamal)

```
Encrypted:

bytes 0-527 :: AES-encrypted record (note: same size as BuildRequestRecord)

Unencrypted:

+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|                                       |
+   SHA-256 Hash of following bytes     +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| random data...                        |
~                                       ~
|                                       |
+                                  +----+
|                                  | ret|
+----+----+----+----+----+----+----+----+

bytes 0-31   :: SHA-256 Hash of bytes 32-527
bytes 32-526 :: random data
byte  527    :: reply

total length: 528
```
#### Notizen

- Das Zufallsdatenfeld könnte in Zukunft dazu verwendet werden, Stau- oder Peer-Konnektivitätsinformationen an den Anfrager zurückzusenden.

- Siehe die [Tunnel-Erstellungsspezifikation](/docs/specs/tunnel-creation/) für Details zum Antwortfeld.

### ShortBuildRequestRecord {#struct-ShortBuildRequestRecord}

Nur für ECIES-X25519 router, ab API-Version 0.9.51. 218 Bytes wenn verschlüsselt. Siehe [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

### ShortBuildResponseRecord {#struct-ShortBuildResponseRecord}

Nur für ECIES-X25519 router, ab API-Version 0.9.51. 218 Bytes wenn verschlüsselt. Siehe [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

### GarlicClove {#struct-GarlicClove}

Warnung: Dies ist das Format, das für garlic cloves innerhalb von ElGamal-verschlüsselten garlic messages verwendet wird [CRYPTO-ELG](/docs/specs/cryptography/#elgamal). Das Format für ECIES-AEAD-X25519-Ratchet garlic messages und garlic cloves ist erheblich anders; siehe [ECIES](/docs/specs/ecies/) für die Spezifikation.

```
Unencrypted:

+----+----+----+----+----+----+----+----+
| Delivery Instructions                 |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| I2NP Message                          |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|    Clove ID       |     Expiration
+----+----+----+----+----+----+----+----+
                    | Certificate  |
+----+----+----+----+----+----+----+

Delivery Instructions :: as defined below
       Length varies but is typically 1, 33, or 37 bytes

I2NP Message :: Any I2NP Message

Clove ID :: 4 byte Integer

Expiration :: Date (8 bytes)

Certificate :: Always NULL in the current implementation (3 bytes total, all zeroes)
```
#### Notizen

- Cloves werden niemals fragmentiert. Bei Verwendung in einem Garlic Clove gibt das erste Bit des Delivery Instructions Flag-Bytes die Verschlüsselung an. Wenn dieses Bit 0 ist, ist der Clove nicht verschlüsselt. Wenn 1, ist der Clove verschlüsselt, und ein 32 Byte Session Key folgt unmittelbar auf das Flag-Byte. Clove-Verschlüsselung ist nicht vollständig implementiert.

- Siehe auch die [Spezifikation für garlic routing](/docs/overview/garlic-routing/).

- Die maximale Länge ist eine Funktion der Gesamtlänge aller Cloves und der maximalen Länge der GarlicMessage.

- In Zukunft könnte das Zertifikat möglicherweise für einen HashCash verwendet werden, um für das Routing zu "bezahlen".

- Die Nachricht kann jede I2NP-Nachricht sein (einschließlich einer GarlicMessage, obwohl dies in der Praxis nicht verwendet wird). Die in der Praxis verwendeten Nachrichten sind DataMessage, DeliveryStatusMessage und DatabaseStoreMessage.

- Die Clove ID wird beim Senden normalerweise auf eine Zufallszahl gesetzt und beim Empfangen auf Duplikate überprüft (derselbe Nachrichten-ID-Bereich wie Message IDs der obersten Ebene)

### Garlic Clove Delivery Instructions {#struct-GarlicCloveDeliveryInstructions}

Dies ist das Format, das sowohl für ElGamal-verschlüsselte [CRYPTO-ELG](/docs/specs/cryptography/#elgamal) als auch für ECIES-AEAD-X25519-Ratchet verschlüsselte [ECIES](/docs/specs/ecies/) garlic cloves verwendet wird.

Diese Spezifikation gilt nur für Delivery Instructions (Zustellungsanweisungen) innerhalb von Garlic Cloves. Beachten Sie, dass "Delivery Instructions" auch innerhalb von Tunnel Messages verwendet werden, wo das Format erheblich anders ist. Siehe die [Tunnel Message Dokumentation](/docs/legacy/tunnel-message/#tunnel-message-delivery-instructions) für Details. Verwenden Sie die folgende Spezifikation NICHT für Tunnel Message Delivery Instructions!

Session-Schlüssel und Verzögerung werden nicht verwendet und sind niemals vorhanden, daher sind die drei möglichen Längen 1 (LOCAL), 33 (ROUTER und DESTINATION) und 37 (TUNNEL) Bytes.

```
+----+----+----+----+----+----+----+----+
|flag|                                  |
+----+                                  +
|                                       |
+       Session Key (optional)          +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+--------------+
|    |                                  |
+----+                                  +
|                                       |
+         To Hash (optional)            +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+--------------+
|    |  Tunnel ID (opt)  |  Delay (opt)
+----+----+----+----+----+----+----+----+
     |
+----+

flag ::
       1 byte
       Bit order: 76543210
       bit 7: encrypted? Unimplemented, always 0
                If 1, a 32-byte encryption session key is included
       bits 6-5: delivery type
                0x0 = LOCAL, 0x01 = DESTINATION, 0x02 = ROUTER, 0x03 = TUNNEL
       bit 4: delay included?  Not fully implemented, always 0
                If 1, four delay bytes are included
       bits 3-0: reserved, set to 0 for compatibility with future uses

Session Key ::
       32 bytes
       Optional, present if encrypt flag bit is set.
       Unimplemented, never set, never present.

To Hash ::
       32 bytes
       Optional, present if delivery type is DESTINATION, ROUTER, or TUNNEL
          If DESTINATION, the SHA256 Hash of the destination
          If ROUTER, the SHA256 Hash of the router
          If TUNNEL, the SHA256 Hash of the gateway router

Tunnel ID :: TunnelId
       4 bytes
       Optional, present if delivery type is TUNNEL
       The destination tunnel ID, nonzero

Delay :: Integer
       4 bytes
       Optional, present if delay included flag is set
       Not fully implemented. Specifies the delay in seconds.

Total length: Typical length is:
       1 byte for LOCAL delivery;
       33 bytes for ROUTER / DESTINATION delivery;
       37 bytes for TUNNEL delivery
```
## Nachrichten

<table style="border-collapse: collapse; width: 100%;">
<thead>
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">Message</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">Since</th>
</tr>
</thead>
<tbody>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-DatabaseStore">DatabaseStore</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-DatabaseLookup">DatabaseLookup</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-DatabaseSearchReply">DatabaseSearchReply</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-DeliveryStatus">DeliveryStatus</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">10</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-Garlic">Garlic</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-TunnelData">TunnelData</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">18</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-TunnelGateway">TunnelGateway</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">19</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-Data">Data</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">20</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-TunnelBuild">TunnelBuild</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">21</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-TunnelBuildReply">TunnelBuildReply</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">22</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-VariableTunnelBuild">VariableTunnelBuild</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">23</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.12</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-VariableTunnelBuildReply">VariableTunnelBuildReply</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">24</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.12</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-ShortTunnelBuild">ShortTunnelBuild</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">25</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.51</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#msg-OutboundTunnelBuildReply">OutboundTunnelBuildReply</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">26</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.51</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Reserved</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Reserved for experimental messages</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">224-254</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">Reserved for future expansion</td>
<td style="border: 1px solid var(--color-border); padding: 8px; text-align: center;">255</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
</tbody>
</table>
### DatabaseStore {#msg-DatabaseStore}

#### Beschreibung

Ein unangeforderter Database Store oder die Antwort auf eine erfolgreiche [DatabaseLookup](#msg-DatabaseLookup) Nachricht

#### Inhaltsverzeichnis

Ein unkomprimiertes LeaseSet, LeaseSet2, MetaLeaseSet oder EncryptedLeaseset, oder eine komprimierte RouterInfo

```
with reply token:
+----+----+----+----+----+----+----+----+
| SHA256 Hash as key                    |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|type| reply token       | reply_tunnelId
+----+----+----+----+----+----+----+----+
     | SHA256 of the gateway RouterInfo |
+----+                                  +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+----+----+----+
|    | data ...
+----+-//

with reply token == 0:
+----+----+----+----+----+----+----+----+
| SHA256 Hash as key                    |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|type|         0         | data ...
+----+----+----+----+----+-//

key ::
    32 bytes
    SHA256 hash

type ::
     1 byte
     type identifier
     bit 0:
             0    RouterInfo
             1    LeaseSet or variants listed below
     bits 3-1:
            Through release 0.9.17, must be 0
            As of release 0.9.18, ignored, reserved for future options, set to 0 for compatibility
            As of release 0.9.38, the remainder of the type identifier:
            0: RouterInfo or LeaseSet (types 0 or 1)
            1: LeaseSet2 (type 3)
            2: EncryptedLeaseSet (type 5)
            3: MetaLeaseSet (type 7)
            4-7: Unsupported, invalid
     bits 7-4:
            Through release 0.9.17, must be 0
            As of release 0.9.18, ignored, reserved for future options, set to 0 for compatibility

reply token ::
            4 bytes
            If greater than zero, a DeliveryStatusMessage
            is requested with the Message ID set to the value of the Reply Token.
            A floodfill router is also expected to flood the data to the closest floodfill peers
            if the token is greater than zero.

reply_tunnelId ::
               4 byte TunnelId
               Only included if reply token > 0
               This is the TunnelId of the inbound gateway of the tunnel the response should be sent to
               If $reply_tunnelId is zero, the reply is sent directy to the reply gateway router.

reply gateway ::
              32 bytes
              Hash of the RouterInfo entry to reach the gateway
              Only included if reply token > 0
              If $reply_tunnelId is nonzero, this is the router hash of the inbound gateway
              of the tunnel the response should be sent to.
              If $reply_tunnelId is zero, this is the router hash the response should be sent to.

data ::
     If type == 0, data is a 2-byte Integer specifying the number of bytes that follow,
                   followed by a gzip-compressed RouterInfo. See note below.
     If type == 1, data is an uncompressed LeaseSet.
     If type == 3, data is an uncompressed LeaseSet2.
     If type == 5, data is an uncompressed EncryptedLeaseSet.
     If type == 7, data is an uncompressed MetaLeaseSet.
```
#### Notizen

- Aus Sicherheitsgründen werden die Antwortfelder ignoriert, wenn die Nachricht über einen tunnel empfangen wird.

- Der Schlüssel ist der "echte" Hash der RouterIdentity oder Destination, NICHT der Routing-Schlüssel.

- Die Typen 3, 5 und 7 sind ab Release 0.9.38 verfügbar. Siehe Vorschlag 123 für weitere Informationen. Diese Typen sollten nur an router mit Release 0.9.38 oder höher gesendet werden.

- Als Optimierung zur Reduzierung von Verbindungen kann der Empfänger, wenn der Typ ein LeaseSet ist, das Antwort-Token enthalten ist, die Antwort-Tunnel-ID ungleich null ist und das Antwort-Gateway/Tunnel-ID-Paar im LeaseSet als Lease gefunden wird, die Antwort zu jedem anderen Lease im LeaseSet umleiten.

- Um das router-Betriebssystem und die Implementierung zu verbergen, sollte die Java-router-Implementierung von gzip nachgeahmt werden, indem die Änderungszeit auf 0 und das OS-Byte auf 0xFF gesetzt wird, und XFL auf 0x02 (maximale Kompression, langsamster Algorithmus) gesetzt wird. Siehe RFC 1952. Die ersten 10 Bytes der komprimierten router-Info werden (hex): 1F 8B 08 00 00 00 00 00 02 FF

### DatabaseLookup {#msg-DatabaseLookup}

#### Beschreibung

Eine Anfrage zum Nachschlagen eines Elements in der Netzwerkdatenbank. Die Antwort ist entweder eine [DatabaseStore](#msg-DatabaseStore) oder eine [DatabaseSearchReply](#msg-DatabaseSearchReply).

#### Inhaltsverzeichnis

```
+----+----+----+----+----+----+----+----+
| SHA256 hash as the key to look up     |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| SHA256 hash of the routerInfo         |
+ who is asking or the gateway to       +
| send the reply to                     |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag| reply_tunnelId    | size    |    |
+----+----+----+----+----+----+----+    +
| SHA256 of key1 to exclude             |
+                                       +
|                                       |
+                                       +
|                                       |
+                                  +----+
|                                  |    |
+----+----+----+----+----+----+----+    +
| SHA256 of key2 to exclude             |
+                                       +
~                                       ~
+                                  +----+
|                                  |    |
+----+----+----+----+----+----+----+    +
|                                       |
+                                       +
|   Session key if reply encryption     |
+   was requested                       +
|                                       |
+                                  +----+
|                                  |tags|
+----+----+----+----+----+----+----+----+
|                                       |
+                                       +
|   Session tags if reply encryption    |
+   was requested                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+

key ::
    32 bytes
    SHA256 hash of the object to lookup

from ::
     32 bytes
     if deliveryFlag == 0, the SHA256 hash of the routerInfo entry this
                           request came from (to which the reply should be
                           sent)
     if deliveryFlag == 1, the SHA256 hash of the reply tunnel gateway (to
                           which the reply should be sent)

flags ::
     1 byte
     bit order: 76543210
     bit 0: deliveryFlag
             0  => send reply directly
             1  => send reply to some tunnel
     bit 1: encryptionFlag
             through release 0.9.5, must be set to 0
             as of release 0.9.6, ignored
             as of release 0.9.7:
             0  => send unencrypted reply
             1  => send AES encrypted reply using enclosed key and tag
     bits 3-2: lookup type flags
             through release 0.9.5, must be set to 00
             as of release 0.9.6, ignored
             as of release 0.9.16:
             00  => ANY lookup, return RouterInfo or LeaseSet or
                    DatabaseSearchReplyMessage. DEPRECATED.
                    Use LS or RI lookup as of 0.9.16.
             01  => LS lookup, return LeaseSet or
                    DatabaseSearchReplyMessage
                    As of release 0.9.38, may also return a
                    LeaseSet2, MetaLeaseSet, or EncryptedLeaseSet.
             10  => RI lookup, return RouterInfo or
                    DatabaseSearchReplyMessage
             11  => exploration lookup, return RouterInfo or
                    DatabaseSearchReplyMessage containing
                    non-floodfill routers only (replaces an
                    excludedPeer of all zeroes)
     bit 4: ECIESFlag
             before release 0.9.46 ignored
             as of release 0.9.46:
             0  => send unencrypted or ElGamal reply
             1  => send ChaCha/Poly encrypted reply using enclosed key
                   (whether tag is enclosed depends on bit 1)
     bits 7-5:
             through release 0.9.5, must be set to 0
             as of release 0.9.6, ignored, set to 0 for compatibility with
             future uses and with older routers

reply_tunnelId ::
               4 byte TunnelID
               only included if deliveryFlag == 1
               tunnelId of the tunnel to send the reply to, nonzero

size ::
     2 byte Integer
     valid range: 0-512
     number of peers to exclude from the DatabaseSearchReplyMessage

excludedPeers ::
              $size SHA256 hashes of 32 bytes each (total $size*32 bytes)
              if the lookup fails, these peers are requested to be excluded
              from the list in the DatabaseSearchReplyMessage.
              if excludedPeers includes a hash of all zeroes, the request is
              exploratory, and the DatabaseSearchReplyMessage is requested
              to list non-floodfill routers only.

reply_key ::
     32 byte key
     see below

tags ::
     1 byte Integer
     valid range: 1-32 (typically 1)
     the number of reply tags that follow
     see below

reply_tags ::
     one or more 8 or 32 byte session tags (typically one)
     see below
```
#### Reply-Verschlüsselung

HINWEIS: ElGamal router sind seit API 0.9.58 veraltet. Da die empfohlene Mindestversion für floodfill-Abfragen nun 0.9.58 ist, müssen Implementierungen keine Verschlüsselung für ElGamal floodfill router implementieren. ElGamal-Ziele werden weiterhin unterstützt.

Flag-Bit 4 wird in Kombination mit Bit 1 verwendet, um den Antwort-Verschlüsselungsmodus zu bestimmen. Flag-Bit 4 darf nur gesetzt werden, wenn an Router mit Version 0.9.46 oder höher gesendet wird. Siehe Vorschläge 154 und 156 für Details.

In der Tabelle unten bedeutet "DH n/a", dass die Antwort nicht verschlüsselt ist. "DH no" bedeutet, dass die Antwortschlüssel in der Anfrage enthalten sind. "DH yes" bedeutet, dass die Antwortschlüssel aus der DH-Operation abgeleitet werden.

<table style="border-collapse: collapse; width: 100%;">
<thead>
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">Flag bits 4,1</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">From</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">To Router</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">Reply</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">DH?</th>
<th style="border: 1px solid var(--color-border); padding: 8px; text-align: left;">notes</th>
</tr>
</thead>
<tbody>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Any</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Any</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">no enc</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">n/a</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">no encryption</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ElG</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ElG</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">no</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">As of 0.9.7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ElG</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AEAD</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">no</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">As of 0.9.46</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AEAD</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">no</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">As of 0.9.49</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ElG</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">yes</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">TBD</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">ECIES</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">AEAD</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">yes</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">TBD</td>
</tr>
</tbody>
</table>
#### Keine Verschlüsselung

reply_key, tags und reply_tags sind nicht vorhanden.

#### ElG zu ElG

Unterstützt seit 0.9.7. Veraltet seit 0.9.58. ElG-Ziel sendet eine Anfrage an einen ElG-Router.

Schlüsselerzeugung für Anforderer:

```
reply_key :: CSRNG(32) 32 bytes random data
reply_tags :: Each is CSRNG(32) 32 bytes random data
```
Nachrichtenformat:

```
reply_key ::
     32 byte SessionKey big-endian
     only included if encryptionFlag == 1 AND ECIESFlag == 0, only as of release 0.9.7

tags ::
     1 byte Integer
     valid range: 1-32 (typically 1)
     the number of reply tags that follow
     only included if encryptionFlag == 1 AND ECIESFlag == 0, only as of release 0.9.7

reply_tags ::
     one or more 32 byte SessionTags (typically one)
     only included if encryptionFlag == 1 AND ECIESFlag == 0, only as of release 0.9.7
```
#### ECIES zu ElG

Unterstützt seit 0.9.46. Veraltet seit 0.9.58. ECIES destination sendet eine Anfrage an einen ElG router. Die reply_key und reply_tags Felder werden für eine ECIES-verschlüsselte Antwort neu definiert.

Erzeugung des Anfragerschlüssels:

```
reply_key :: CSRNG(32) 32 bytes random data
reply_tags :: Each is CSRNG(8) 8 bytes random data
```
Nachrichtenformat: Definiere die Felder reply_key und reply_tags wie folgt neu:

```
reply_key ::
     32 byte ECIES SessionKey big-endian
     only included if encryptionFlag == 0 AND ECIESFlag == 1, only as of release 0.9.46

tags ::
     1 byte Integer
     required value: 1
     the number of reply tags that follow
     only included if encryptionFlag == 0 AND ECIESFlag == 1, only as of release 0.9.46

reply_tags ::
     an 8 byte ECIES SessionTag
     only included if encryptionFlag == 0 AND ECIESFlag == 1, only as of release 0.9.46
```
Die Antwort ist eine ECIES Existing Session Nachricht, wie in [ECIES](/docs/specs/ecies/) definiert.

#### Antwortformat

Dies ist die bestehende Session-Nachricht, identisch mit der in [ECIES](/docs/specs/ecies/), die unten als Referenz kopiert ist.

```
+----+----+----+----+----+----+----+----+
|       Session Tag                     |
+----+----+----+----+----+----+----+----+
|                                       |
+            Payload Section            +
|       ChaCha20 encrypted data         |
~                                       ~
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|  Poly1305 Message Authentication Code |
+              (MAC)                    +
|             16 bytes                  |
+----+----+----+----+----+----+----+----+

Session Tag :: 8 bytes, cleartext

Payload Section encrypted data :: remaining data minus 16 bytes

MAC :: Poly1305 message authentication code, 16 bytes
```
AEAD-Parameter:

```
tag :: 8 byte reply_tag

k :: 32 byte session key
   The reply_key.

n :: 0

ad :: The 8 byte reply_tag

payload :: Plaintext data, the DSM or DSRM.

ciphertext = ENCRYPT(k, n, payload, ad)
```
#### ECIES zu ECIES (0.9.49)

ECIES-Ziel oder -router sendet eine Anfrage an einen ECIES-router. Unterstützt ab Version 0.9.49.

ECIES router wurden in 0.9.48 eingeführt, siehe [Proposal 156](/proposals/156/). ECIES destinations und router können das gleiche Format wie im Abschnitt "ECIES to ElG" oben verwenden, mit reply keys die in der Anfrage enthalten sind. Die Verschlüsselung der lookup-Nachricht ist in [ECIES-ROUTERS](/docs/specs/ecies-routers/) spezifiziert. Der Anfrager ist anonym.

#### ECIES zu ECIES (zukünftig)

Diese Option ist noch nicht vollständig definiert. Siehe [Proposal 156](/proposals/156/).

#### Hinweise

- Vor 0.9.16 konnte der Schlüssel für eine RouterInfo oder ein LeaseSet sein, da sie sich im selben Schlüsselraum befinden und es kein Flag gab, um nur einen bestimmten Datentyp anzufordern.

- Verschlüsselungsflag, Antwortschlüssel und Antwort-Tags ab Version 0.9.7.

- Verschlüsselte Antworten sind nur dann nützlich, wenn die Antwort über einen tunnel erfolgt.

- Die Anzahl der enthaltenen Tags könnte größer als eins sein, wenn alternative DHT-Suchstrategien (zum Beispiel rekursive Suchen) implementiert werden.

- Der Lookup-Schlüssel und die Exclude-Schlüssel sind die "echten" Hashes, NICHT die Routing-Schlüssel.

- Typen 3, 5 und 7 können seit Version 0.9.38 zurückgegeben werden. Siehe Vorschlag 123 für weitere Informationen.

- Hinweise zur explorativen Suche: Eine explorative Suche ist definiert als Rückgabe einer Liste von non-floodfill Hashes, die dem Schlüssel nahestehen. Siehe jedoch wichtige Hinweise zu DatabaseSearchReply für Implementierungsvarianten. Zusätzlich hat diese Spezifikation nie klargestellt, ob der Empfänger den Suchschlüssel für eine RI nachschlagen und stattdessen einen DatabaseStore anstatt eines DSRM zurückgeben sollte, falls vorhanden. Java führt die Suche durch; i2pd nicht. Daher wird nicht empfohlen, eine explorative Suche für zuvor empfangene Hashes zu verwenden.

### DatabaseSearchReply {#msg-DatabaseSearchReply}

#### Beschreibung

Die Antwort auf eine fehlgeschlagene [DatabaseLookup](#msg-DatabaseLookup) Nachricht

#### Inhalt

Eine Liste von router-Hashes, die dem angeforderten Schlüssel am nächsten sind

```
+----+----+----+----+----+----+----+----+
| SHA256 hash as query key              |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
| num| peer_hashes                      |
+----+                                  +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+----+----+----+
|    | from                             |
+----+                                  +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+    +----+----+----+----+----+----+----+
|    |
+----+

key ::
    32 bytes
    SHA256 of the object being searched

num ::
    1 byte Integer
    number of peer hashes that follow, 0-255

peer_hashes ::
          $num SHA256 hashes of 32 bytes each (total $num*32 bytes)
          SHA256 of the RouterIdentity that the other router thinks is close
          to the key

from ::
     32 bytes
     SHA256 of the RouterInfo of the router this reply was sent from
```
#### Notizen

- Der 'from'-Hash ist nicht authentifiziert und kann nicht vertraut werden.

- Die zurückgegebenen Peer-Hashes sind nicht notwendigerweise näher zum Schlüssel als der Router, der abgefragt wird. Für Antworten auf reguläre Lookups erleichtert dies die Entdeckung neuer floodfills und "rückwärts" gerichtete Suche (weiter-vom-Schlüssel-entfernt) für Robustheit.

- Der Schlüssel für eine Erkundungssuche wird normalerweise zufällig generiert. Daher können die Nicht-floodfill peer_hashes der Antwort mit einem optimierten Algorithmus ausgewählt werden, wie z.B. die Bereitstellung von Peers, die dem Schlüssel nahe sind, aber nicht unbedingt die nächstgelegenen in der gesamten lokalen Netzwerkdatenbank, um eine ineffiziente Sortierung oder Suche der gesamten lokalen Datenbank zu vermeiden. Andere Strategien wie Caching können ebenfalls angemessen sein. Dies ist implementierungsabhängig.

- Typische Anzahl der zurückgegebenen Hashes: 3

- Empfohlene maximale Anzahl der zurückzugebenden Hashes: 16

- Der Lookup-Schlüssel, Peer-Hashes und From-Hash sind "echte" Hashes, KEINE Routing-Schlüssel.

### DeliveryStatus {#msg-DeliveryStatus}

#### Beschreibung

Eine einfache Nachrichtenbestätigung. Wird normalerweise vom Nachrichtenabsender erstellt und zusammen mit der Nachricht selbst in eine Garlic Message eingehüllt, um vom Ziel zurückgesendet zu werden.

Diese Nachricht wird auch für die Tunnelprüfung verwendet, bei der der Absender sie über einen Outbound-Tunnel an einen Inbound-Tunnel zurück an sich selbst sendet. Auch hier ist sie in der Regel mit Garlic verschlüsselt. Die Tunnelprüfung ist ab API-Version 0.9.68 vom Jahr 2026-02 erforderlich, da Router es dürfen, an Tunneln teilnehmende Verbindungen zu verwerfen, die nach den ersten zwei Minuten keinen Datenverkehr erhalten haben.

#### Inhalt

Die ID der zugestellten Nachricht sowie die Erstellungs- oder Ankunftszeit.

```
+----+----+----+----+----+----+----+----+----+----+----+----+
| msg_id            |           time_stamp                  |
+----+----+----+----+----+----+----+----+----+----+----+----+

msg_id :: Integer
       4 bytes
       unique ID of the message we deliver the DeliveryStatus for (see
       I2NPMessageHeader for details)

time_stamp :: Date
             8 bytes
             time the message was successfully created or delivered
```
#### Hinweise

- Es scheint, dass der Zeitstempel immer vom Ersteller auf die aktuelle Zeit gesetzt wird. Es gibt jedoch mehrere Verwendungen davon im Code, und weitere könnten in Zukunft hinzugefügt werden.

- Diese Nachricht wird auch als Bestätigung für eine etablierte Sitzung in SSU [SSU-ED](/docs/transports/ssu/#establishDirect) verwendet. In diesem Fall wird die Nachrichten-ID auf eine Zufallszahl gesetzt und die "Ankunftszeit" wird auf die aktuelle netzwerkweite ID gesetzt, welche 2 ist (d.h. 0x0000000000000002).

### Garlic {#msg-Garlic}

Warnung: Dies ist das Format für ElGamal-verschlüsselte Garlic-Nachrichten [CRYPTO-ELG](/docs/specs/cryptography/#elgamal). Das Format für ECIES-AEAD-X25519-Ratchet-Garlic-Nachrichten und Garlic-Cloves unterscheidet sich erheblich; siehe [ECIES](/docs/specs/ecies/) für die Spezifikation.

#### Beschreibung

Wird verwendet, um mehrere verschlüsselte I2NP-Nachrichten zu verpacken

#### Inhaltsverzeichnis

Nach der Entschlüsselung eine Reihe von [Garlic Cloves](#struct-GarlicClove) und zusätzlichen Daten, auch bekannt als Clove Set.

Verschlüsselt:

```
+----+----+----+----+----+----+----+----+
|      length       | data              |
+----+----+----+----+                   +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

length ::
       4 byte Integer
       number of bytes that follow 0 - 64 KB

data ::
     $length bytes
     ElGamal encrypted data
```
Entschlüsselte Daten, auch bekannt als Clove-Set:

```
+----+----+----+----+----+----+----+----+
| num|  clove 1                         |
+----+                                  +
|                                       |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
|         clove 2 ...                   |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Certificate  |   Message_ID      |
+----+----+----+----+----+----+----+----+
          Expiration               |
+----+----+----+----+----+----+----+

num ::
     1 byte Integer number of GarlicCloves to follow

clove ::  a GarlicClove

Certificate :: always NULL in the current implementation (3 bytes total, all zeroes)

Message_ID :: 4 byte Integer

Expiration :: Date (8 bytes)
```
#### Notizen

- Wenn unverschlüsselt, enthalten die Daten eine oder mehrere [Garlic Cloves](#struct-GarlicClove).

- Der AES-verschlüsselte Block wird auf mindestens 128 Bytes aufgefüllt; mit dem 32-Byte Session Tag beträgt die Mindestgröße der verschlüsselten Nachricht 160 Bytes; mit den 4 Längen-Bytes beträgt die Mindestgröße der Garlic Message 164 Bytes.

- Die tatsächliche maximale Länge ist geringer als 64 KB; siehe [I2NP](/docs/protocol/i2np/).

- Siehe auch die [ElGamal/AES-Spezifikation](/docs/specs/elgamal-aes/).

- Siehe auch die [garlic routing Spezifikation](/docs/overview/garlic-routing/).

- Die minimale Größe von 128 Bytes des AES-verschlüsselten Blocks ist derzeit nicht konfigurierbar, jedoch beträgt die minimale Größe einer DataMessage in einer GarlicClove in einer GarlicMessage mit Overhead ohnehin 128 Bytes. Eine konfigurierbare Option zur Erhöhung der minimalen Größe könnte in Zukunft hinzugefügt werden.

- Die Nachrichten-ID wird beim Senden in der Regel auf eine Zufallszahl gesetzt und scheint beim Empfang ignoriert zu werden.

- In Zukunft könnte das Zertifikat möglicherweise für ein HashCash verwendet werden, um für das Routing zu "bezahlen".

### TunnelData {#msg-TunnelData}

#### Beschreibung

Eine Nachricht, die von einem Tunnel-Gateway oder -Teilnehmer an den nächsten Teilnehmer oder Endpunkt gesendet wird. Die Daten haben eine feste Länge und enthalten I2NP-Nachrichten, die fragmentiert, gebündelt, gepadded und verschlüsselt sind.

#### Inhalt

```
+----+----+----+----+----+----+----+----+
|     tunnnelID     | data              |
+----+----+----+----+                   |
|                                       |
~                                       ~
~                                       ~
|                                       |
+                   +----+----+----+----+
|                   |
+----+----+----+----+

tunnelId ::
         4 byte TunnelId
         identifies the tunnel this message is directed at
         nonzero

data ::
     1024 bytes
     payload data.. fixed to 1024 bytes
```
#### Hinweise

- Die I2NP-Nachrichten-ID für diese Nachricht wird bei jedem Hop auf eine neue Zufallszahl gesetzt.

- Siehe auch die [Tunnel Message Specification](/docs/legacy/tunnel-message/)

### TunnelGateway {#msg-TunnelGateway}

#### Beschreibung

Umhüllt eine andere I2NP-Nachricht, um sie über das Eintrittsgateway des Tunnels in einen Tunnel zu senden.

#### Inhalt

```
+----+----+----+----+----+----+----+-//
| tunnelId          | length  | data...
+----+----+----+----+----+----+----+-//

tunnelId ::
         4 byte TunnelId
         identifies the tunnel this message is directed at
         nonzero

length ::
       2 byte Integer
       length of the payload

data ::
     $length bytes
     actual payload of this message
```
#### Notizen

- Die Nutzlast ist eine I2NP-Nachricht mit einem standardmäßigen 16-Byte-Header.

### Data {#msg-Data}

#### Beschreibung

Wird von Garlic Messages und Garlic Cloves verwendet, um beliebige Daten einzuschließen.

#### Inhaltsverzeichnis

Eine Längen-Ganzzahl, gefolgt von undurchsichtigen Daten.

```
+----+----+----+----+----+-//-+
| length            | data... |
+----+----+----+----+----+-//-+

length ::
       4 bytes
       length of the payload

data ::
     $length bytes
     actual payload of this message
```
#### Hinweise

- Diese Nachricht enthält keine Routing-Informationen und wird niemals "unverpackt" gesendet. Sie wird nur innerhalb von `Garlic`-Nachrichten verwendet.

### TunnelBuild {#msg-TunnelBuild}

VERALTET, verwenden Sie [VariableTunnelBuild](#msg-VariableTunnelBuild)

```
+----+----+----+----+----+----+----+----+
| Record 0 ...                          |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Record 1 ...                          |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
| Record 7 ...                          |
~                                       ~
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+

Just 8 BuildRequestRecords attached together
record size: 528 bytes
total size: 8*528 = 4224 bytes
```
#### Hinweise

- Ab Version 0.9.48 können auch ECIES-X25519 BuildRequestRecords enthalten sein, siehe [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

- Siehe auch die [Spezifikation zur tunnel-Erstellung](/docs/specs/tunnel-creation/).

- Die I2NP-Nachrichten-ID für diese Nachricht muss gemäß der tunnel-Erstellungsspezifikation gesetzt werden.

- Obwohl diese Nachricht im heutigen Netzwerk selten zu sehen ist, da sie durch die `VariableTunnelBuild`-Nachricht ersetzt wurde, kann sie noch für sehr lange tunnel verwendet werden und ist nicht veraltet. Router müssen sie implementieren.

### TunnelBuildReply {#msg-TunnelBuildReply}

VERALTET, verwenden Sie [VariableTunnelBuildReply](#msg-VariableTunnelBuildReply)

```
Same format as TunnelBuildMessage, with BuildResponseRecords
```
#### Notizen

- Ab Version 0.9.48 kann es auch ECIES-X25519 BuildResponseRecords enthalten, siehe [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

- Siehe auch die [Spezifikation zur Tunnel-Erstellung](/docs/specs/tunnel-creation/).

- Die I2NP-Nachrichten-ID für diese Nachricht muss gemäß der Tunnel-Erstellungsspezifikation gesetzt werden.

- Obwohl diese Nachricht im heutigen Netzwerk selten zu sehen ist, da sie durch die `VariableTunnelBuildReply`-Nachricht ersetzt wurde, kann sie immer noch für sehr lange tunnel verwendet werden und wurde nicht als veraltet markiert. Router müssen sie implementieren.

### VariableTunnelBuild {#msg-VariableTunnelBuild}

```
+----+----+----+----+----+----+----+----+
| num| BuildRequestRecords...
+----+----+----+----+----+----+----+----+

Same format as TunnelBuildMessage, except for the addition of a $num field
in front and $num number of BuildRequestRecords instead of 8

num ::
       1 byte Integer
       Valid values: 1-8

record size: 528 bytes
total size: 1+$num*528
```
#### Notizen

- Ab Version 0.9.48 kann es auch ECIES-X25519 BuildRequestRecords enthalten, siehe [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

- Diese Nachricht wurde in router Version 0.7.12 eingeführt und wird möglicherweise nicht an tunnel-Teilnehmer gesendet, die eine frühere Version verwenden.

- Siehe auch die [Spezifikation zur Tunnel-Erstellung](/docs/specs/tunnel-creation/).

- Die I2NP-Nachrichten-ID für diese Nachricht muss gemäß der tunnel-Erstellungsspezifikation gesetzt werden.

- Typische Anzahl von Datensätzen im heutigen Netzwerk ist 4, für eine Gesamtgröße von 2113.

### VariableTunnelBuildReply {#msg-VariableTunnelBuildReply}

```
+----+----+----+----+----+----+----+----+
| num| BuildResponseRecords...
+----+----+----+----+----+----+----+----+

Same format as VariableTunnelBuildMessage, with BuildResponseRecords.
```
#### Hinweise

- Ab Version 0.9.48 können auch ECIES-X25519 BuildResponseRecords enthalten sein, siehe [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

- Diese Nachricht wurde in router Version 0.7.12 eingeführt und wird möglicherweise nicht an tunnel-Teilnehmer gesendet, die eine frühere Version verwenden.

- Siehe auch die [tunnel creation Spezifikation](/docs/specs/tunnel-creation/).

- Die I2NP-Nachrichten-ID für diese Nachricht muss gemäß der Tunnel-Erstellungsspezifikation gesetzt werden.

- Typische Anzahl von Datensätzen im heutigen Netzwerk ist 4, für eine Gesamtgröße von 2113.

### ShortTunnelBuild {#msg-ShortTunnelBuild}

#### Beschreibung

Ab API-Version 0.9.51 nur für ECIES-X25519-Router.

```
+----+----+----+----+----+----+----+----+
| num| ShortBuildRequestRecords...
+----+----+----+----+----+----+----+----+

Same format as VariableTunnelBuildMessage,
except that the record size is 218 bytes instead of 528

num ::
       1 byte Integer
       Valid values: 1-8

record size: 218 bytes
total size: 1+$num*218
```
#### Notizen

- Ab Version 0.9.51. Siehe [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

- Diese Nachricht wurde in router Version 0.9.51 eingeführt und wird möglicherweise nicht an tunnel-Teilnehmer gesendet, die eine frühere Version verwenden.

- Die typische Anzahl von Datensätzen im heutigen Netzwerk beträgt 4, für eine Gesamtgröße von 873.

### OutboundTunnelBuildReply {#msg-OutboundTunnelBuildReply}

#### Beschreibung

Gesendet vom Outbound-Endpunkt eines neuen Tunnels an den Initiator. Ab API-Version 0.9.51 nur für ECIES-X25519-Router.

```
+----+----+----+----+----+----+----+----+
| num| ShortBuildResponseRecords...
+----+----+----+----+----+----+----+----+

Same format as ShortTunnelBuildMessage, with ShortBuildResponseRecords.
```
#### Notizen

- Ab 0.9.51. Siehe [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

- Die typische Anzahl von Datensätzen im heutigen Netzwerk beträgt 4, für eine Gesamtgröße von 873.

## Referenzen

- **[CRYPTO-ELG]** [Kryptographie - ElGamal](/docs/specs/cryptography/#elgamal)
- **[Date]** [Gemeinsame Strukturen - Datum](/docs/specs/common-structures/#date)
- **[ECIES]** [ECIES Spezifikation](/docs/specs/ecies/)
- **[ECIES-ROUTERS]** [ECIES Router Spezifikation](/docs/specs/ecies-routers/)
- **[ElG-AES]** [ElGamal/AES](/docs/specs/elgamal-aes/)
- **[GARLICSPEC]** [Garlic Routing](/docs/overview/garlic-routing/)
- **[Hash]** [Gemeinsame Strukturen - Hash](/docs/specs/common-structures/#hash)
- **[I2NP]** [I2NP Protokoll](/docs/protocol/i2np/)
- **[Integer]** [Gemeinsame Strukturen - Integer](/docs/specs/common-structures/#integer)
- **[NTCP2]** [NTCP2 Spezifikation](/docs/specs/ntcp2/)
- **[Prop156]** [Vorschlag 156](/proposals/156/)
- **[Prop157]** [Vorschlag 157](/proposals/157/)
- **[RouterIdentity]** [Gemeinsame Strukturen - RouterIdentity](/docs/specs/common-structures/#routeridentity)
- **[SSU]** [SSU Transport](/docs/transports/ssu/)
- **[SSU-ED]** [SSU Transport - Direkte Verbindung etablieren](/docs/transports/ssu/#establishDirect)
- **[SSU2]** [SSU2 Spezifikation](/docs/specs/ssu2/)
- **[TMDI]** [Tunnel Nachrichten Zustellungsanweisungen](/docs/legacy/tunnel-message/#tunnel-message-delivery-instructions)
- **[TUNNEL-CREATION]** [Tunnel Erstellungs-Spezifikation](/docs/specs/tunnel-creation/)
- **[TUNNEL-CREATION-ECIES]** [ECIES Tunnel Erstellung](/docs/specs/tunnel-creation-ecies/)
- **[TUNNEL-IMPL]** [Tunnel Implementierung](/docs/specs/tunnel-implementation/)
- **[TUNNEL-MSG]** [Tunnel Nachrichten Spezifikation](/docs/legacy/tunnel-message/)
- **[TunnelId]** [Gemeinsame Strukturen - TunnelId](/docs/specs/common-structures/#tunnelid)
