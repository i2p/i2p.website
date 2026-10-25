---
title: "Specifikace I2NP"
description: "Formáty zpráv, priority a běžné struktury I2P Network Protocol (I2NP) pro komunikaci mezi routery."
slug: "i2np"
aliases:
  - "/cs/spec/i2np"
  - "/cs/spec/i2np/"
  - "/cs/i2np_spec"
  - "/cs/i2np_spec/"
category: "Protokoly"
lastUpdated: "2026-03"
accurateFor: "0.9.69"
---

## Přehled

I2P Network Protocol (I2NP) je vrstva nad I2P transportními protokoly. Jedná se o protokol router-to-router. Používá se pro vyhledávání a odpovědi v síťové databázi, pro vytváření tunelů a pro šifrované zprávy s daty routerů a klientů. I2NP zprávy mohou být zasílány point-to-point jinému routeru, nebo zasílány anonymně přes tunely tomuto routeru.

## Verze protokolu {#versions}

Všechny routery musí publikovat svou verzi I2NP protokolu v poli "router.version" ve vlastnostech RouterInfo. Toto pole verze je verze API, která označuje úroveň podpory pro různé funkce I2NP protokolu, a nemusí nutně odpovídat skutečné verzi routeru.

Pokud chtějí alternativní (ne-Java) routery publikovat jakékoli informace o verzi o skutečné implementaci routeru, musí tak učinit v jiné vlastnosti. Verze jiné než ty uvedené níže jsou povoleny. Podpora bude určena prostřednictvím číselného porovnání; například 0.9.13 implikuje podporu pro funkce 0.9.12. Všimněte si, že vlastnost "coreVersion" se již nepublikuje v informacích routeru a nikdy nebyla použita pro určení verze I2NP protokolu.

Základní přehled verzí I2NP protokolu je následující. Pro podrobnosti viz níže.

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
Všimněte si, že existují také funkce a problémy kompatibility související s přenosem; podrobnosti najdete v dokumentaci transportů NTCP a SSU.

## Běžné struktury {#structures}

Následující struktury jsou elementy více I2NP zpráv. Nejsou to kompletní zprávy.

### I2NP Message Header {#struct-I2NPMessageHeader}

#### Popis

Společná hlavička pro všechny I2NP zprávy, která obsahuje důležité informace jako kontrolní součet, datum vypršení platnosti atd.

#### Obsah

Používají se tři samostatné formáty v závislosti na kontextu; jeden standardní formát a dva krátké formáty.

Standardní 16 bajtový formát obsahuje 1 bajt [Integer](/docs/specs/common-structures/#integer) specifikující typ této zprávy, následovaný 4 bajtovým [Integer](/docs/specs/common-structures/#integer) specifikujícím message-id. Poté následuje datum vypršení [Date](/docs/specs/common-structures/#date), následované 2 bajtovým [Integer](/docs/specs/common-structures/#integer) specifikujícím délku užitečného obsahu zprávy, následovaný [Hash](/docs/specs/common-structures/#hash), který je zkrácen na první bajt. Poté následují skutečná data zprávy.

Krátké formáty používají 4bajtové vypršení v sekundách místo 8bajtového vypršení v milisekundách. Krátké formáty neobsahují kontrolní součet ani velikost, ty jsou poskytovány enkapsulacemi v závislosti na kontextu.

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
#### Poznámky

- Při přenosu přes [SSU](/docs/transports/ssu/) se nepoužívá 16bytová standardní hlavička. Zahrnuje se pouze 1bytový typ a 4bytová doba vypršení v sekundách. ID zprávy a velikost jsou začleněny do formátu datového paketu SSU. Kontrolní součet není vyžadován, protože chyby jsou zachyceny při dešifrování.

- Při přenosu přes [NTCP2](/docs/specs/ntcp2/) nebo [SSU2](/docs/specs/ssu2/) se 16-bajtová standardní hlavička nepoužívá. Je zahrnuta pouze 1-bajtová hodnota typu, 4-bajtové ID zprávy a 4-bajtová doba vypršení v sekundách. Velikost je zahrnuta ve formátech datových paketů NTCP2 a SSU2. Kontrolní součet není vyžadován, protože chyby jsou zachyceny při dešifrování.

- Standardní hlavička je také vyžadována pro I2NP zprávy obsažené v jiných zprávách a strukturách (Data, TunnelData, TunnelGateway a GarlicClove). Od vydání 0.8.12 je pro snížení režie ověřování kontrolních součtů zakázáno na některých místech v protokolovém zásobníku. Pro kompatibilitu se staršími verzemi je však stále vyžadováno generování kontrolních součtů. Je to téma pro budoucí výzkum k určení bodů v protokolovém zásobníku, kde je známa verze vzdáleného routeru a generování kontrolních součtů může být zakázáno.

- Krátká doba vypršení je bez znaménka a přeteče 7. února 2106. Od tohoto data musí být přidán offset pro získání správného času.

- Implementace mohou odmítnout zprávy s vypršením platnosti příliš daleko v budoucnosti. Doporučené maximální vypršení platnosti je 60 sekund v budoucnosti.

### BuildRequestRecord {#struct-BuildRequestRecord}

ZASTARALÉ, používá se v současné síti pouze když tunel obsahuje ElGamal router. Viz [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

#### Popis

Jeden záznam v sadě více záznamů pro požadavek vytvoření jednoho skoku v tunnel. Pro více podrobností viz [přehled tunnel](/docs/specs/tunnel-implementation/) a [specifikace vytváření ElGamal tunnel](/docs/specs/tunnel-creation/).

Pro ECIES-X25519 BuildRequestRecords viz [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

#### Obsah (ElGamal)

[TunnelId](/docs/specs/common-structures/#tunnelid) pro příjem zpráv, následovaný [Hash](/docs/specs/common-structures/#hash) naší [RouterIdentity](/docs/specs/common-structures/#routeridentity). Poté následuje [TunnelId](/docs/specs/common-structures/#tunnelid) a [Hash](/docs/specs/common-structures/#hash) [RouterIdentity](/docs/specs/common-structures/#routeridentity) dalšího routeru.

ElGamal a AES šifrované:

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
ElGamal šifrované:

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
Nešifrovaný text:

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
#### Poznámky

- V 512-bajtovém šifrovaném záznamu obsahují ElGamal data bajty 1-256 a 258-513 ze 514-bajtového ElGamal šifrovaného bloku [CRYPTO-ELG](/docs/specs/cryptography/#elgamal). Dva padding bajty z bloku (nulové bajty na pozicích 0 a 257) jsou odstraněny.

- Podrobnosti o obsahu polí naleznete ve [specifikaci vytváření tunelů](/docs/specs/tunnel-creation/).

### BuildResponseRecord {#struct-BuildResponseRecord}

ZASTARALÉ, používá se v současné síti pouze když tunel obsahuje ElGamal router. Viz [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

#### Popis

Jeden záznam v sadě více záznamů s odpověďmi na požadavek o sestavení. Pro více podrobností viz [přehled tunelů](/docs/specs/tunnel-implementation/) a [specifikace vytváření tunelů ElGamal](/docs/specs/tunnel-creation/).

Pro ECIES-X25519 BuildResponseRecords viz [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

#### Obsah (ElGamal)

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
#### Poznámky

- Pole náhodných dat by v budoucnu mohlo být použito k vrácení informací o přetížení nebo konektivitě peerů zpět žadateli.

- Viz [specifikace vytváření tunelů](/docs/specs/tunnel-creation/) pro podrobnosti o poli odpovědi.

### ShortBuildRequestRecord {#struct-ShortBuildRequestRecord}

Pouze pro ECIES-X25519 routery, od verze API 0.9.51. 218 bajtů při šifrování. Viz [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

### ShortBuildResponseRecord {#struct-ShortBuildResponseRecord}

Pouze pro ECIES-X25519 routery, od verze API 0.9.51. 218 bajtů při šifrování. Viz [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

### GarlicClove {#struct-GarlicClove}

Varování: Toto je formát používaný pro garlic cloves uvnitř ElGamal-šifrovaných garlic zpráv [CRYPTO-ELG](/docs/specs/cryptography/#elgamal). Formát pro ECIES-AEAD-X25519-Ratchet garlic zprávy a garlic cloves je výrazně odlišný; specifikaci najdete v [ECIES](/docs/specs/ecies/).

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
#### Poznámky

- Cloves nejsou nikdy fragmentovány. Při použití v Garlic Clove první bit flag bytu Delivery Instructions specifikuje šifrování. Pokud je tento bit 0, clove není šifrován. Pokud je 1, clove je šifrován a 32 bajtový Session Key následuje bezprostředně za flag bytem. Šifrování clove není plně implementováno.

- Viz také [specifikaci garlic routing](/docs/overview/garlic-routing/).

- Maximální délka je funkcí celkové délky všech částí (cloves) a maximální délky GarlicMessage.

- V budoucnu by certifikát mohl být případně použit pro HashCash k "placení" za směrování.

- Zpráva může být jakákoli I2NP zpráva (včetně GarlicMessage, ačkoli ta se v praxi nepoužívá). Zprávy používané v praxi jsou DataMessage, DeliveryStatusMessage a DatabaseStoreMessage.

- Clove ID je obecně nastaveno na náhodné číslo při přenosu a je kontrolováno na duplicity při příjmu (stejný prostor ID zpráv jako Message ID na nejvyšší úrovni)

### Pokyny pro doručení Garlic Clove {#struct-GarlicCloveDeliveryInstructions}

Toto je formát používaný jak pro ElGamal-šifrované [CRYPTO-ELG](/docs/specs/cryptography/#elgamal), tak pro ECIES-AEAD-X25519-Ratchet šifrované [ECIES](/docs/specs/ecies/) garlic cloves.

Tato specifikace je pouze pro Delivery Instructions uvnitř Garlic Cloves. Všimněte si, že "Delivery Instructions" se také používají uvnitř Tunnel Messages, kde je formát výrazně odlišný. Podrobnosti najdete v [dokumentaci Tunnel Message](/docs/legacy/tunnel-message/#tunnel-message-delivery-instructions). NEPOUŽÍVEJTE následující specifikaci pro Tunnel Message Delivery Instructions!

Session key a delay se nepoužívají a nikdy nejsou přítomny, takže tři možné délky jsou 1 (LOCAL), 33 (ROUTER a DESTINATION) a 37 (TUNNEL) bajtů.

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
## Zprávy

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

#### Popis

Nevyžádané uložení databáze, nebo odpověď na úspěšnou zprávu [DatabaseLookup](#msg-DatabaseLookup)

#### Obsah

Nekomprimovaný LeaseSet, LeaseSet2, MetaLeaseSet nebo EncryptedLeaseset, nebo komprimovaný RouterInfo

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
#### Poznámky

- Z bezpečnostních důvodů jsou pole odpovědi ignorována, pokud je zpráva přijata prostřednictvím tunnelu.

- Klíč je "skutečný" hash RouterIdentity nebo Destination, NIKOLI routing klíč.

- Typy 3, 5 a 7 jsou od verze 0.9.38. Více informací naleznete v návrhu 123. Tyto typy by měly být odesílány pouze routerům s verzí 0.9.38 nebo vyšší.

- Jako optimalizace ke snížení počtu spojení, pokud je typ LeaseSet, je zahrnut reply token, reply tunnel ID je nenulové a dvojice reply gateway/tunnelID je nalezena v LeaseSet jako lease, příjemce může přesměrovat odpověď na jakýkoli jiný lease v LeaseSet.

- Pro skrytí OS routeru a implementace, shodujte se s implementací gzip Java routeru nastavením času modifikace na 0 a OS bajtu na 0xFF, a nastavte XFL na 0x02 (maximální komprese, nejpomalejší algoritmus). Viz RFC 1952. Prvních 10 bajtů komprimovaných informací o routeru bude (hex): 1F 8B 08 00 00 00 00 00 02 FF

### DatabaseLookup {#msg-DatabaseLookup}

#### Popis

Požadavek na vyhledání položky v databázi sítě. Odpovědí je buď [DatabaseStore](#msg-DatabaseStore) nebo [DatabaseSearchReply](#msg-DatabaseSearchReply).

#### Obsah

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
#### Šifrování odpovědi

POZNÁMKA: ElGamal routery jsou od API 0.9.58 zastaralé. Jelikož doporučená minimální verze floodfill pro dotazování je nyní 0.9.58, implementace nemusí implementovat šifrování pro ElGamal floodfill routery. ElGamal destinace jsou stále podporovány.

Flag bit 4 se používá v kombinaci s bitem 1 k určení režimu šifrování odpovědi. Flag bit 4 smí být nastaven pouze při odesílání na routery s verzí 0.9.46 nebo vyšší. Podrobnosti viz návrhy 154 a 156.

V tabulce níže "DH n/a" znamená, že odpověď není šifrována. "DH no" znamená, že klíče odpovědi jsou zahrnuty v požadavku. "DH yes" znamená, že klíče odpovědi jsou odvozeny z DH operace.

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
#### Bez šifrování

reply_key, tags a reply_tags nejsou přítomny.

#### ElG to ElG

Podporováno od verze 0.9.7. Zastaralé od verze 0.9.58. ElG destinace posílá vyhledávání do ElG routeru.

Generování klíče žadatele:

```
reply_key :: CSRNG(32) 32 bytes random data
reply_tags :: Each is CSRNG(32) 32 bytes random data
```
Formát zprávy:

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
#### ECIES na ElG

Podporováno od verze 0.9.46. Zastaralé od verze 0.9.58. ECIES cíl odesílá vyhledávání do ElG routeru. Pole reply_key a reply_tags jsou předefinována pro ECIES-šifrovanou odpověď.

Generování klíče žadatele:

```
reply_key :: CSRNG(32) 32 bytes random data
reply_tags :: Each is CSRNG(8) 8 bytes random data
```
Formát zprávy: Předefinovat pole reply_key a reply_tags následovně:

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
Odpověď je zpráva ECIES Existing Session, jak je definována v [ECIES](/docs/specs/ecies/).

#### Formát odpovědi

Toto je stávající zpráva relace, stejná jako v [ECIES](/docs/specs/ecies/), zkopírovaná níže pro referenci.

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
Parametry AEAD:

```
tag :: 8 byte reply_tag

k :: 32 byte session key
   The reply_key.

n :: 0

ad :: The 8 byte reply_tag

payload :: Plaintext data, the DSM or DSRM.

ciphertext = ENCRYPT(k, n, payload, ad)
```
#### ECIES na ECIES (0.9.49)

ECIES cíl nebo router odesílá vyhledávání do ECIES routeru. Podporováno od verze 0.9.49.

ECIES routery byly představeny ve verzi 0.9.48, viz [Návrh 156](/proposals/156/). ECIES destinace a routery mohou používat stejný formát jako v sekci "ECIES to ElG" výše, s reply klíči zahrnutými v požadavku. Šifrování lookup zprávy je specifikováno v [ECIES-ROUTERS](/docs/specs/ecies-routers/). Žadatel je anonymní.

#### ECIES na ECIES (budoucí)

Tato možnost ještě není plně definována. Viz [Návrh 156](/proposals/156/).

#### Poznámky

- Před verzí 0.9.16 mohl klíč být pro RouterInfo nebo LeaseSet, protože jsou ve stejném prostoru klíčů a neexistoval žádný příznak pro vyžádání pouze konkrétního typu dat.

- Příznak šifrování, klíč odpovědi a značky odpovědi od vydání 0.9.7.

- Šifrované odpovědi jsou užitečné pouze tehdy, když je odpověď odesílána přes tunnel.

- Počet zahrnutých tagů by mohl být větší než jeden, pokud jsou implementovány alternativní strategie vyhledávání DHT (například rekurzivní vyhledávání).

- Vyhledávací klíč a vyloučené klíče jsou "skutečné" hashe, NIKOLI směrovací klíče.

- Typy 3, 5 a 7 mohou být vráceny od vydání 0.9.38. Více informací najdete v návrhu 123.

- Poznámky k průzkumovému vyhledávání: Průzkumové vyhledávání je definováno tak, aby vrátilo seznam non-floodfill hashů blízkých ke klíči. Nicméně viz důležité poznámky pro DatabaseSearchReply ohledně variant implementace. Navíc tato specifikace nikdy jasně neuvedla, zda by příjemce měl vyhledat vyhledávací klíč pro RI a vrátit DatabaseStore místo DSRM, pokud je přítomen. Java toto vyhledávání provádí; i2pd ne. Proto se nedoporučuje používat průzkumové vyhledávání pro dříve přijaté hashe.

### DatabaseSearchReply {#msg-DatabaseSearchReply}

#### Popis

Odpověď na neúspěšnou zprávu [DatabaseLookup](#msg-DatabaseLookup)

#### Obsah

Seznam router hashů nejblíže k požadovanému klíči

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
#### Poznámky

- Hash 'from' není ověřen a nelze mu důvěřovat.

- Vrácené hashe peerů nejsou nutně blíže ke klíči než router, který je dotazován. U odpovědí na běžné vyhledávání to usnadňuje objevování nových floodfillů a "zpětné" vyhledávání (dále-od-klíče) pro robustnost.

- Klíč pro exploration lookup je obvykle generován náhodně. Proto mohou být peer_hashes jiných než floodfill uzlů v odpovědi vybrány pomocí optimalizovaného algoritmu, například poskytováním uzlů, které jsou blízko klíče, ale nemusí být nutně nejbližší v celé lokální síťové databázi, aby se předešlo neefektivnímu třídění nebo prohledávání celé lokální databáze. Další strategie jako ukládání do mezipaměti mohou být také vhodné. Toto závisí na implementaci.

- Typický počet vrácených hashů: 3

- Doporučený maximální počet hashů k vrácení: 16

- Vyhledávací klíč, hashe peerů a from hash jsou "skutečné" hashe, NIKOLIV routing klíče.

### DeliveryStatus {#msg-DeliveryStatus}

#### Popis

Jednoduché potvrzení zprávy. Obvykle vytvořeno původcem zprávy a zabaleno do Garlic Message spolu se samotnou zprávou, aby bylo vráceno cílem.

Tato zpráva se používá také pro testování tunelů, kdy odesílatel pošle zprávu výstupním tunelem do vstupního tunelu a zpět k sobě. I v tomto případě je obvykle zabalena pomocí garlic encryption. Testování tunelů je vyžadováno od verze API 0.9.68 z roku 2026-02, protože směrovače mají povoleno odmítat zapojené tunely, které po prvních dvou minutách nepřijaly žádný provoz.

#### Obsah

ID doručené zprávy a čas jejího vytvoření nebo přijetí.

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
#### Poznámky

- Zdá se, že časové razítko je vždy nastaveno tvůrcem na aktuální čas. Existuje však několik použití tohoto v kódu a v budoucnu může být přidáno více.

- Tato zpráva se také používá jako potvrzení navázané relace v SSU [SSU-ED](/docs/transports/ssu/#establishDirect). V tomto případě je ID zprávy nastaveno na náhodné číslo a "čas příchodu" je nastaven na aktuální celé síťové ID, které je 2 (tj. 0x0000000000000002).

### Garlic {#msg-Garlic}

Upozornění: Toto je formát používaný pro ElGamal-šifrované garlic zprávy [CRYPTO-ELG](/docs/specs/cryptography/#elgamal). Formát pro ECIES-AEAD-X25519-Ratchet garlic zprávy a garlic cloves je výrazně odlišný; viz [ECIES](/docs/specs/ecies/) pro specifikaci.

#### Popis

Používá se k zabalení více šifrovaných zpráv I2NP

#### Obsah

Po dešifrování série [Garlic Cloves](#struct-GarlicClove) a dalších dat, známých také jako Clove Set.

Šifrované:

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
Dešifrovaná data, známá také jako Clove Set:

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
#### Poznámky

- Když nejsou šifrována, data obsahují jeden nebo více [Garlic Cloves](#struct-GarlicClove).

- AES šifrovaný blok je doplněn na minimálně 128 bajtů; s 32-bajtovým Session Tag je minimální velikost šifrované zprávy 160 bajtů; se 4 bajty délky je minimální velikost Garlic Message 164 bajtů.

- Skutečná maximální délka je menší než 64 KB; viz [I2NP](/docs/protocol/i2np/).

- Viz také [specifikaci ElGamal/AES](/docs/specs/elgamal-aes/).

- Viz také [specifikace garlic routing](/docs/overview/garlic-routing/).

- Minimální velikost 128 bajtů pro AES šifrovaný blok není aktuálně konfigurovatelná, nicméně minimální velikost DataMessage v GarlicClove v GarlicMessage včetně režie je tak či tak 128 bajtů. Konfigurovatelná možnost pro zvýšení minimální velikosti může být přidána v budoucnu.

- ID zprávy je obvykle nastaveno na náhodné číslo při odesílání a zdá se, že je při příjmu ignorováno.

- V budoucnu by certifikát mohl být případně použit pro HashCash k "placení" za směrování.

### TunnelData {#msg-TunnelData}

#### Popis

Zpráva odeslaná z brány nebo účastníka tunelu dalšímu účastníkovi nebo koncovému bodu. Data mají pevnou délku a obsahují fragmentované, seskupené, doplněné a šifrované zprávy I2NP.

#### Obsah

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
#### Poznámky

- ID I2NP zprávy pro tuto zprávu je nastaveno na nové náhodné číslo při každém skoku.

- Viz také [Specifikace Tunnel Message](/docs/legacy/tunnel-message/)

### TunnelGateway {#msg-TunnelGateway}

#### Popis

Zabalení jiné zprávy I2NP, která má být odeslána do tunelu na vstupní bráně tunelu.

#### Obsah

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
#### Poznámky

- Datová část je I2NP zpráva se standardní 16-bajtovou hlavičkou.

### Data {#msg-Data}

#### Popis

Používá se u Garlic zpráv a Garlic cloves pro zabalení libovolných dat.

#### Obsah

Celé číslo udávající délku, následované neprůhlednými daty.

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
#### Poznámky

- Tato zpráva neobsahuje žádné směrovací informace a nikdy nebude odeslána "nebalená". Používá se pouze uvnitř zpráv `Garlic`.

### TunnelBuild {#msg-TunnelBuild}

ZASTARALÉ, použijte [VariableTunnelBuild](#msg-VariableTunnelBuild)

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
#### Poznámky

- Od verze 0.9.48 může také obsahovat ECIES-X25519 BuildRequestRecords, viz [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

- Viz také [specifikace vytváření tunelů](/docs/specs/tunnel-creation/).

- ID I2NP zprávy pro tuto zprávu musí být nastaveno podle specifikace vytváření tunelu.

- Ačkoli je tato zpráva v dnešní síti zřídka vidět, protože byla nahrazena zprávou `VariableTunnelBuild`, může být stále použita pro velmi dlouhé tunnely a nebyla označena jako zastaralá. Routery ji musí implementovat.

### TunnelBuildReply {#msg-TunnelBuildReply}

ZASTARALÉ, použijte [VariableTunnelBuildReply](#msg-VariableTunnelBuildReply)

```
Same format as TunnelBuildMessage, with BuildResponseRecords
```
#### Poznámky

- Od verze 0.9.48 může také obsahovat ECIES-X25519 BuildResponseRecords, viz [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

- Viz také [specifikace vytváření tunnelů](/docs/specs/tunnel-creation/).

- ID I2NP zprávy pro tuto zprávu musí být nastaveno podle specifikace vytváření tunnelu.

- Zatímco tato zpráva je v dnešní síti zřídka viděna, jelikož byla nahrazena zprávou `VariableTunnelBuildReply`, může být stále používána pro velmi dlouhé tunnely a nebyla označena jako zastaralá. Routery ji musí implementovat.

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
#### Poznámky

- Od verze 0.9.48 může také obsahovat ECIES-X25519 BuildRequestRecords, viz [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

- Tato zpráva byla zavedena ve verzi routeru 0.7.12 a nemusí být odeslána účastníkům tunelu starším než tato verze.

- Viz také [specifikace vytváření tunelu](/docs/specs/tunnel-creation/).

- ID I2NP zprávy pro tuto zprávu musí být nastaveno podle specifikace vytváření tunelu.

- Typický počet záznamů v dnešní síti je 4, celková velikost 2113.

### VariableTunnelBuildReply {#msg-VariableTunnelBuildReply}

```
+----+----+----+----+----+----+----+----+
| num| BuildResponseRecords...
+----+----+----+----+----+----+----+----+

Same format as VariableTunnelBuildMessage, with BuildResponseRecords.
```
#### Poznámky

- Od verze 0.9.48 může také obsahovat ECIES-X25519 BuildResponseRecords, viz [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

- Tato zpráva byla zavedena ve verzi routeru 0.7.12 a nemusí být odeslána účastníkům tunelu ve starších verzích.

- Viz také [specifikace vytváření tunelů](/docs/specs/tunnel-creation/).

- ID I2NP zprávy pro tuto zprávu musí být nastaveno podle specifikace pro vytváření tunelů.

- Typický počet záznamů v dnešní síti je 4, pro celkovou velikost 2113.

### ShortTunnelBuild {#msg-ShortTunnelBuild}

#### Popis

Počínaje verzí API 0.9.51, pouze pro směrovače ECIES-X25519.

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
#### Poznámky

- Od verze 0.9.51. Viz [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

- Tato zpráva byla představena ve verzi routeru 0.9.51 a nemusí být odeslána účastníkům tunelu s dřívější verzí.

- Typický počet záznamů v dnešní síti je 4, pro celkovou velikost 873.

### OutboundTunnelBuildReply {#msg-OutboundTunnelBuildReply}

#### Popis

Odesláno z odchozího koncového bodu nového tunelu původci. Od verze API 0.9.51 pouze pro směrovače ECIES-X25519.

```
+----+----+----+----+----+----+----+----+
| num| ShortBuildResponseRecords...
+----+----+----+----+----+----+----+----+

Same format as ShortTunnelBuildMessage, with ShortBuildResponseRecords.
```
#### Poznámky

- Od verze 0.9.51. Viz [ECIES Tunnel Creation](/docs/specs/tunnel-creation-ecies/).

- Typický počet záznamů v dnešní síti je 4, celková velikost je 873.

## Reference

- **[CRYPTO-ELG]** [Kryptografie - ElGamal](/docs/specs/cryptography/#elgamal)
- **[Date]** [Běžné struktury - Datum](/docs/specs/common-structures/#date)
- **[ECIES]** [Specifikace ECIES](/docs/specs/ecies/)
- **[ECIES-ROUTERS]** [Specifikace ECIES routerů](/docs/specs/ecies-routers/)
- **[ElG-AES]** [ElGamal/AES](/docs/specs/elgamal-aes/)
- **[GARLICSPEC]** [Garlic Routing](/docs/overview/garlic-routing/)
- **[Hash]** [Běžné struktury - Hash](/docs/specs/common-structures/#hash)
- **[I2NP]** [I2NP Protocol](/docs/protocol/i2np/)
- **[Integer]** [Běžné struktury - Integer](/docs/specs/common-structures/#integer)
- **[NTCP2]** [Specifikace NTCP2](/docs/specs/ntcp2/)
- **[Prop156]** [Návrh 156](/proposals/156/)
- **[Prop157]** [Návrh 157](/proposals/157/)
- **[RouterIdentity]** [Běžné struktury - RouterIdentity](/docs/specs/common-structures/#routeridentity)
- **[SSU]** [SSU Transport](/docs/transports/ssu/)
- **[SSU-ED]** [SSU Transport - Establish Direct](/docs/transports/ssu/#establishDirect)
- **[SSU2]** [Specifikace SSU2](/docs/specs/ssu2/)
- **[TMDI]** [Instrukce pro doručování tunelových zpráv](/docs/legacy/tunnel-message/#tunnel-message-delivery-instructions)
- **[TUNNEL-CREATION]** [Specifikace vytváření tunelů](/docs/specs/tunnel-creation/)
- **[TUNNEL-CREATION-ECIES]** [Vytváření ECIES tunelů](/docs/specs/tunnel-creation-ecies/)
- **[TUNNEL-IMPL]** [Implementace tunelů](/docs/specs/tunnel-implementation/)
- **[TUNNEL-MSG]** [Specifikace tunelových zpráv](/docs/legacy/tunnel-message/)
- **[TunnelId]** [Běžné struktury - TunnelId](/docs/specs/common-structures/#tunnelid)
