---
title: "SSU (Secure Semireliable UDP)"
description: "Původní specifikace transportního protokolu UDP (zastaralá, nahrazena SSU2)"
slug: "ssu"
aliases:
  - "/cs/docs/transport/ssu"
  - "/cs/docs/transport/ssu/"
  - "/cs/docs/transports/ssu"
  - "/cs/docs/transports/ssu/"
  - "/cs/docs/specs/ssu-spec"
  - "/cs/docs/specs/ssu-spec/"
category: "Transporty"
lastUpdated: "2024-01"
accurateFor: "0.9.61"
---

## Přehled

ZASTARALÉ - SSU byl nahrazen SSU2. Podpora SSU byla odstraněna z i2pd ve verzi 2.44.0 (API 0.9.56) v 11/2022. Podpora SSU byla odstraněna z Java I2P ve verzi 2.4.0 (API 0.9.61) v 12/2023.

Další informace najdete v [přehledu SSU](/docs/transport/ssu/).

## DH výměna klíčů {#dh}

Počáteční 2048bitová DH výměna klíčů je popsána na [stránce SSU klíčů](/docs/transport/ssu/#keys). Tato výměna používá stejné sdílené prvočíslo jako to, které se používá pro I2P [ElGamal šifrování](/docs/specs/cryptography/#elgamal).

## Záhlaví zprávy {#header}

Všechny UDP datagramy začínají 16bytovým MAC (Message Authentication Code) a 16bytovým IV (Initialization Vector), následovanými payload proměnné velikosti zašifrovanou odpovídajícím klíčem. Používaný MAC je HMAC-MD5, zkrácený na 16 bytů, zatímco klíč je plný 32bytový AES256 klíč. Specifická konstrukce MAC je prvních 16 bytů z:

```
HMAC-MD5(encryptedPayload + IV + (payloadLength ^ protocolVersion ^ ((netid - 2) << 8)), macKey)
```
kde '+' znamená připojení a '^' znamená exkluzivní nebo.

IV je generováno náhodně pro každý paket. encryptedPayload je šifrovaná verze zprávy začínající flag bytem (encrypt-then-MAC). payloadLength použitý v MAC je 2bytové unsigned integer, big endian. Všimněte si, že protocolVersion je 0, takže exclusive-or je no-op. macKey je buď introduction key nebo je konstruován z vyměněného DH klíče (viz podrobnosti níže), jak je specifikováno pro každou zprávu níže.

**VAROVÁNÍ** - HMAC-MD5-128 používaný zde není standardní, viz [podrobnosti o HMAC](/docs/specs/cryptography/#udp) pro více informací.

Samotný payload (tedy zpráva začínající flag bytem) je šifrován pomocí AES256/CBC s IV a sessionKey, s ochranou proti replay útokům řešenou v jejím těle, jak je vysvětleno níže.

ProtocolVersion je 2bajtové nepředznamenované celé číslo, big endian, a je aktuálně nastaveno na 0. Peeři používající jinou verzi protokolu nebudou schopni komunikovat s tímto peerem, ačkoli dřívější verze nepoužívající tento příznak ano.

Exkluzivní OR z ((netid - 2) << 8) se používá k rychlé identifikaci připojení mezi sítěmi. Netid je 2bajtové nepodepsané celé číslo, big endian, a je aktuálně nastaveno na 2. Od verze 0.9.42. Více informací naleznete v návrhu 147. Jelikož je aktuální síťové ID 2, jedná se o no-op pro současnou síť a je zpětně kompatibilní. Jakákoliv připojení z testovacích sítí by měla mít jiné ID a HMAC selže.

### Specifikace HMAC

- Vnitřní výplň: 0x36...
- Vnější výplň: 0x5C...
- Klíč: 32 bytů
- Funkce hash digest: MD5, 16 bytů
- Velikost bloku: 64 bytů
- Velikost MAC: 16 bytů
- Příklady implementací v C:
  - hmac.h v [i2pd](https://github.com/PurpleI2P/i2pd)
  - I2PHMAC.cpp v [i2pcpp](http://git.repo.i2p/w/i2pcpp.git)
- Příklad implementace v Javě:
  - I2PHMac.java v [I2P](https://github.com/i2p/i2p.i2p)

### Podrobnosti klíče relace

32bajtový klíč relace se vytváří následovně:

1. Vezměte vyměněný DH klíč, reprezentovaný jako pozitivní pole bajtů
   BigInteger s minimální délkou (two's complement big-endian)
2. Pokud je nejvýznamnější bit 1 (tj. array[0] & 0x80 != 0),
   připojte na začátek bajt 0x00, jako v Java BigInteger.toByteArray()
   reprezentaci
3. Pokud je pole bajtů větší nebo rovno 32 bajtům, použijte
   prvních (nejvýznamnějších) 32 bajtů
4. Pokud je pole bajtů menší než 32 bajtů, připojte bajty 0x00 pro rozšíření
   na 32 bajtů. *Velmi nepravděpodobné - Viz poznámka níže.*

### Detaily MAC klíče

32-bajtový MAC klíč se vytváří následovně:

1. Vezměte vyměněné DH key byte pole, předřazené 0x00 bytem pokud
   je to nutné, z kroku 2 v Session Key Details výše.
2. Pokud je toto byte pole větší nebo rovno 64 bytům, MAC key
   jsou byty 33-64 z tohoto byte pole.
3. Pokud je toto byte pole menší než 64 bytů, MAC key je SHA-256
   Hash tohoto byte pole. *Od vydání 0.9.8. Viz poznámka níže.*

#### Důležitá poznámka

Kód před vydáním 0.9.8 byl porušený a nesprávně zpracovával pole bajtů DH klíčů mezi 32 a 63 bajty (kroky 3 a 4 výše) a připojení selhalo. Jelikož tyto případy nikdy nefungovaly, byly pro vydání 0.9.8 předefinovány jak je popsáno výše, a případ 0-32 bajtů byl také předefinován. Vzhledem k tomu, že nominální vyměňovaný DH klíč má 256 bajtů, jsou šance, že minimální reprezentace bude menší než 64 bajtů, zanedbatelně malé.

### Formát hlavičky

Uvnitř AES šifrované datové části se nachází minimální společná struktura pro různé zprávy - jednobajtový příznak a čtyřbajtové časové razítko odeslání (sekundy od unix epoch).

Formát hlavičky je:

```
Header: 37+ bytes
  Encryption starts with the flag byte.
  +----+----+----+----+----+----+----+----+
  |                  MAC                  |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |                   IV                  |
  +                                       +
  |                                       |
  +----+----+----+----+----+----+----+----+
  |flag|        time       |              |
  +----+----+----+----+----+              +
  | keying material (optional)            |
  +                                       +
  |                                       |
  ~                                       ~
  |                                       |
  +                        +----+----+----+
  |                        |#opt|         |
  +----+----+----+----+----+----+         +
  | #opt extended option bytes (optional) |
  ~                                       ~
  ~                                       ~
  +----+----+----+----+----+----+----+----+
```
Bajt příznaku obsahuje následující bitová pole:

```
Bit order: 76543210 (bit 7 is MSB)

  bits 7-4: payload type
     bit 3: If 1, rekey data is included. Always 0, unimplemented
     bit 2: If 1, extended options are included. Always 0 before release
            0.9.24.
  bits 1-0: reserved, set to 0 for compatibility with future uses
```
Bez rekeying a rozšířených možností má hlavička velikost 37 bajtů.

### Obnova klíčů {#rekey}

Pokud je nastaven příznak rekey, za časovým razítkem následuje 64 bajtů klíčového materiálu.

Při rekeying se prvních 32 bajtů klíčového materiálu podává do SHA256 pro vytvoření nového MAC klíče a dalších 32 bajtů se podává do SHA256 pro vytvoření nového session klíče, přičemž klíče se nepoužívají okamžitě. Druhá strana by měla také odpovědět s nastaveným rekey příznakem a stejným klíčovým materiálem. Jakmile obě strany odeslaly a přijaly tyto hodnoty, nové klíče by se měly začít používat a předchozí klíče zahodit. Může být užitečné ponechat staré klíče krátce k dispozici pro řešení ztráty a přeřazování paketů.

POZNÁMKA: Rekeying je v současnosti neimplementován.

### Rozšířené možnosti {#extend}

Pokud je nastaven příznak rozšířených možností, připojí se jednobajtová hodnota velikosti možností, následovaná odpovídajícím počtem bajtů rozšířených možností. Rozšířené možnosti vždy byly součástí specifikace, ale nebyly implementovány až do vydání 0.9.24. Pokud jsou přítomny, formát možností je specifický pro typ zprávy. Viz dokumentace zpráv níže, zda jsou pro danou zprávu očekávány rozšířené možnosti a jaký je specifikovaný formát. Zatímco Java routery vždy rozpoznaly příznak a délku možností, jiné implementace ne. Proto neposílejte rozšířené možnosti routerům starším než vydání 0.9.24.

## Výplň

Všechny zprávy obsahují 0 nebo více bajtů výplně. Každá zpráva musí být doplněna na 16bajtovou hranici, jak vyžaduje [šifrovací vrstva AES256](/docs/specs/cryptography/#AES).

Do vydání 0.9.7 byly zprávy zarovnávány pouze na nejbližší 16bajtovou hranici a zprávy, které nebyly násobkem 16 bajtů, mohly být potenciálně neplatné.

Od verze 0.9.7 mohou být zprávy vyplněny na libovolnou délku, pokud je dodržena aktuální MTU. Jakékoli dodatečné 1-15 výplňových bajtů za posledním blokem 16 bajtů nelze zašifrovat ani dešifrovat a budou ignorovány. Nicméně celá délka a všechny výplně jsou zahrnuty do výpočtu MAC.

Od verze 0.9.8 nejsou přenášené zprávy nutně násobkem 16 bajtů. Zpráva SessionConfirmed je výjimkou, viz níže.

## Klíče

Podpisy ve zprávách SessionCreated a SessionConfirmed jsou generovány pomocí [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) z [RouterIdentity](/docs/specs/common-structures/#routeridentity), která je distribuována out-of-band publikováním v síťové databázi, a přidruženého [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey).

Do verze 0.9.15 byl algoritmus podpisu vždy DSA s 40bajtovým podpisem.

Od vydání 0.9.16 může být algoritmus podpisu specifikován pomocí [KeyCertificate](/docs/specs/common-structures/#key-certificates) v Bobově [RouterIdentity](/docs/specs/common-structures/#routeridentity).

Jak úvodní klíče, tak klíče relace jsou 32 bajtů a jsou definovány specifikací Common structures [SessionKey](/docs/specs/common-structures/#sessionkey). Klíč použitý pro MAC a šifrování je specifikován pro každou zprávu níže.

Úvodní klíče jsou dodávány prostřednictvím externího kanálu (síťové databáze), kde byly tradičně identické s router Hash až do verze 0.9.47, ale od verze 0.9.48 mohou být náhodné.

## Poznámky

### IPv6

Specifikace protokolu umožňuje jak 4-bajtové IPv4, tak 16-bajtové IPv6 adresy. SSU-over-IPv6 je podporováno od verze 0.9.8. Podrobnosti o podpoře IPv6 naleznete v dokumentaci jednotlivých zpráv níže.

### Časové značky {#time}

Zatímco většina I2P používá 8-bajtové [Date](/docs/specs/common-structures/#date) časové značky s rozlišením na milisekundy, SSU používá 4-bajtové nepředznamenné celé číslo časových značek s rozlišením na sekundu. Protože jsou tyto hodnoty nepředznamenné, nebudou se přetáčet až do února 2106.

## Zprávy

Je definováno 10 zpráv (typy payloadu):

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Message</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Notes</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#sessionrequest">SessionRequest</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#sessioncreated">SessionCreated</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#sessionconfirmed">SessionConfirmed</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#relayrequest">RelayRequest</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#relayresponse">RelayResponse</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#relayintro">RelayIntro</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#data">Data</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#peertest">PeerTest</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">8</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#sessiondestroyed">SessionDestroyed</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Implemented as of 0.8.9</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">n/a</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#holepunch">HolePunch</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
</table>
### SessionRequest (typ 0) {#sessionrequest}

Toto je první zpráva odeslaná k navázání relace.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice to Bob</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">256 byte X, to begin the DH agreement; 1 byte IP address size; that many bytes representation of Bob's IP address; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey, as retrieved from the network database</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey, as retrieved from the network database</td>
</tr>
</table>
Formát zprávy:

```
+----+----+----+----+----+----+----+----+
|         X, as calculated from DH      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
|size| that many byte IP address (4-16) |
+----+----+----+----+----+----+----+----+
| arbitrary amount of uninterpreted data|
~                .  .  .                ~
```
Typická velikost včetně hlavičky v současné implementaci: 304 (IPv4) nebo 320 (IPv6) bajtů (před non-mod-16 paddingem)

#### Rozšířené možnosti

Poznámka: Implementováno ve verzi 0.9.24.

- Minimální délka: 3 (byte délky volby + 2 byty)
- Délka volby: minimálně 2
- 2 byty příznaků:

```
Bit order: 15...76543210 (bit 15 is MSB)

      bit 0: 1 for Alice to request a relay tag from Bob in the
             SessionCreated response, 0 if Alice does not need a relay tag.
             Note that "1" is the default if no extended options are present
  bits 15-1: unused, set to 0 for compatibility with future uses
```
#### Poznámky

- IPv4 a IPv6 adresy jsou podporovány.
- Neinterpretovaná data by mohla být v budoucnu využita pro výzvy.

### SessionCreated (typ 1) {#sessioncreated}

Toto je odpověď na [SessionRequest](#sessionrequest).

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob to Alice</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">256 byte Y, to complete the DH agreement; 1 byte IP address size; that many bytes representation of Alice's IP address; 2 byte Alice's port number; 4 byte relay (introduction) tag which Alice can publish (else 0x00000000); 4 byte timestamp (seconds from the epoch) for use in the DSA signature; Bob's <a href="/docs/specs/common-structures/#signature">Signature</a> of the critical exchanged data (X + Y + Alice's IP + Alice's port + Bob's IP + Bob's port + Alice's new relay tag + Bob's signed on time), encrypted with another layer of encryption using the negotiated sessionKey. The IV is reused here. See notes for length information.; 0-15 bytes of padding of the signature, using random data, to a multiple of 16 bytes, so that the signature + padding may be encrypted with an additional layer of encryption using the negotiated session key as part of the DSA block.; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey, with an additional layer of encryption over the 40 byte signature and the following 8 bytes padding.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey</td>
</tr>
</table>
Formát zprávy:

```
+----+----+----+----+----+----+----+----+
|         Y, as calculated from DH      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
|size| that many byte IP address (4-16) |
+----+----+----+----+----+----+----+----+
| Port (A)| public relay tag  |  signed
+----+----+----+----+----+----+----+----+
  on time |                             |
+----+----+                             +
|                                       |
+                                       +
|             signature                 |
+                                       +
|                                       |
+                                       +
|                                       |
+         +----+----+----+----+----+----+
|         |   (0-15 bytes of padding) 
+----+----+----+----+----+----+----+----+
          |                             |
+----+----+                             +
|           arbitrary amount            |
~        of uninterpreted data          ~
~                .  .  .                ~
```
Typická velikost včetně hlavičky v současné implementaci: 368 bajtů (IPv4 nebo IPv6) (před doplněním na non-mod-16)

#### Poznámky

- Jsou podporovány IPv4 a IPv6 adresy.
- Pokud je relay tag nenulový, Bob nabízí, že bude působit jako introducer pro
  Alici. Alice může následně publikovat Bobovu adresu a relay tag v
  síťové databázi.
- Pro podpis musí Bob použít svůj externí port, protože to je to, co Alice použije
  k ověření. Pokud Bobův NAT/firewall namapoval jeho interní port na
  jiný externí port a Bob si toho není vědom, ověření Alicí
  selže.
- Podrobnosti o podpisech najdete v sekci [Klíče](#keys) výše. Alice už má
  Bobův veřejný podepisovací klíč ze síťové databáze.
- Do vydání 0.9.15 byl podpis vždy 40bajtový DSA podpis a
  padding byl vždy 8 bajtů. Od vydání 0.9.16 jsou typ podpisu a
  délka odvozeny z typu [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) v Bobově
  [RouterIdentity](/docs/specs/common-structures/#routeridentity). Padding je podle potřeby na násobky 16 bajtů.
- Toto je jediná zpráva, která používá odesílatelův intro klíč. Všechny ostatní používají
  příjemcův intro klíč nebo zavedený session klíč.
- Čas podpisu se zdá být nepoužíván nebo neověřován v současné
  implementaci.
- Neinterpretovaná data by mohla být v budoucnu případně použita pro výzvy.
- Rozšířené možnosti v hlavičce: Neočekávané, nedefinované.

### SessionConfirmed (typ 2) {#sessionconfirmed}

Toto je odpověď na zprávu [SessionCreated](#sessioncreated) a poslední krok při vytváření relace. Může být vyžadováno více zpráv SessionConfirmed, pokud musí být Router Identity fragmentována.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice to Bob</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 byte identity fragment info (bits 7-4: current identity fragment # 0-14; bits 3-0: total identity fragments (F) 1-15); 2 byte size of the current identity fragment; that many byte fragment of Alice's <a href="/docs/specs/common-structures/#routeridentity">RouterIdentity</a>; After the last identity fragment only: 4 byte signed-on time; N bytes padding, currently uninterpreted; After the last identity fragment only: The remaining bytes contain Alice's <a href="/docs/specs/common-structures/#signature">Signature</a> of the critical exchanged data (X + Y + Alice's IP + Alice's port + Bob's IP + Bob's port + Alice's new relay tag + Alice's signed on time). See notes for length information.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob sessionKey, as generated from the DH exchange</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob MAC Key, as generated from the DH exchange</td>
</tr>
</table>
**Fragment 0 až F-2** (pouze pokud F > 1; momentálně nepoužito, viz poznámky níže):

```
+----+----+----+----+----+----+----+----+
|info| cursize |                        |
+----+----+----+                        +
|      fragment of Alice's full         |
~            Router Identity            ~
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
| arbitrary amount of uninterpreted data|
~                .  .  .                ~
```
**Fragment F-1 (poslední nebo jediný fragment):**

```
+----+----+----+----+----+----+----+----+
|info| cursize |                        |
+----+----+----+                        +
|     last fragment of Alice's full     |
~            Router Identity            ~
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
|  signed on time   |                   |
+----+----+----+----+                   +
|  arbitrary amount of uninterpreted    |
~      data, until the signature at     ~
~       end of the current packet       ~
|  Packet length must be mult. of 16    |
+----+----+----+----+----+----+----+----+
+                                       +
|                                       |
+                                       +
|             signature                 |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
```
Typická velikost včetně záhlaví v současné implementaci: 512 bajtů (s Ed25519 podpisem) nebo 480 bajtů (s DSA-SHA1 podpisem) (před non-mod-16 padding)

#### Poznámky

- V současné implementaci je maximální velikost fragmentu 512 bajtů. Toto by mělo být rozšířeno tak, aby delší podpisy fungovaly bez fragmentace. Současná implementace nesprávně zpracovává podpisy rozdělené mezi dva fragmenty.
- Typická [RouterIdentity](/docs/specs/common-structures/#routeridentity) má 387 bajtů, takže fragmentace nikdy není nutná. Pokud nová kryptografie rozšíří velikost RouterIdentity, schéma fragmentace musí být pečlivě otestováno.
- Neexistuje mechanismus pro vyžádání nebo opětovné doručení chybějících fragmentů.
- Pole celkových fragmentů F musí být nastaveno identicky ve všech fragmentech.
- Pro podrobnosti o DSA podpisech viz sekce [Keys](#keys) výše.
- Čas podepsání se zdá být nepoužívaný nebo neověřený v současné implementaci.
- Protože podpis je na konci, výplň v posledním nebo jediném paketu musí doplnit celkový paket na násobek 16 bajtů, jinak se podpis nedešifruje správně. Toto se liší od všech ostatních typů zpráv, kde je výplň na konci.
- Do verze 0.9.15 byl podpis vždy 40bajtový DSA podpis. Od verze 0.9.16 jsou typ a délka podpisu odvozeny z typu [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) v Alice [RouterIdentity](/docs/specs/common-structures/#routeridentity). Výplň je podle potřeby na násobek 16 bajtů.
- Rozšířené možnosti v hlavičce: Neočekávané, nedefinované.

### SessionDestroyed (typ 8) {#sessiondestroyed}

Zpráva SessionDestroyed byla implementována (pouze příjem) ve verzi 0.8.1 a je odesílána od verze 0.8.9.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice to Bob or Bob to Alice</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">none</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob sessionKey</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob MAC Key</td>
</tr>
</table>
Tato zpráva neobsahuje žádná data. Typická velikost včetně hlavičky v současné implementaci: 48 bajtů (před non-mod-16 paddingem)

#### Poznámky

- Destroy zprávy přijaté s intro klíčem odesílatele nebo příjemce budou
  ignorovány.
- Rozšířené možnosti v hlavičce: Neočekávané, nedefinované.

### RelayRequest (typ 3) {#relayrequest}

Toto je první zpráva odeslaná od Alice k Bobovi s žádostí o představení Charliemu.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice to Bob</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4 byte relay (introduction) tag, nonzero, as received by Alice in the SessionCreated message from Bob; 1 byte IP address size; that many byte representation of Alice's IP address; 2 byte port number (of Alice); 1 byte challenge size; that many bytes to be relayed to Charlie in the intro; Alice's 32-byte introduction key (so Bob can reply with Charlie's info); 4 byte nonce of Alice's relay request; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey, as retrieved from the network database (or Alice/Bob sessionKey, if established)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob's introKey, as retrieved from the network database (or Alice/Bob MAC Key, if established)</td>
</tr>
</table>
Formát zprávy:

```
+----+----+----+----+----+----+----+----+
|      relay tag    |size| Alice IP addr
+----+----+----+----+----+----+----+----+
     | Port (A)|size| challenge bytes   |
+----+----+----+----+                   +
|      to be delivered to Charlie       |
+----+----+----+----+----+----+----+----+
| Alice's intro key                     |
+                                       +
|                                       |
+                                       +
|                                       |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|       nonce       |                   |
+----+----+----+----+                   +
| arbitrary amount of uninterpreted data|
~                .  .  .                ~
```
Typická velikost včetně hlavičky v současné implementaci: 96 bajtů (bez Alice IP) nebo 112 bajtů (se 4-bajtovou Alice IP) (před non-mod-16 paddingem)

#### Poznámky

- IP adresa je zahrnuta pouze tehdy, pokud se liší od zdrojové adresy a portu paketu.
- Tato zpráva může být odeslána přes IPv4 nebo IPv6.
  Pokud je zpráva přes IPv6 pro IPv4 introduction,
  nebo (od vydání 0.9.50) přes IPv4 pro IPv6 introduction,
  Alice musí zahrnout svou introduction adresu a port.
  Toto je podporováno od vydání 0.9.50.
- Pokud Alice zahrne svou adresu/port, Bob může provést dodatečnou validaci
  před pokračováním.
  - Před vydáním 0.9.24 Java I2P odmítal jakoukoli adresu nebo port, který se
    lišil od připojení.
- Challenge není implementována, velikost challenge je vždy nula
- Relaying pro IPv6 je podporováno od vydání 0.9.50.
- Před vydáním 0.9.12 byl vždy použit Bob's intro key. Od vydání
  0.9.12 je použit session key, pokud existuje navázaná session mezi
  Alice a Bobem. V praxi musí existovat navázaná session, protože Alice
  získá nonce (introduction tag) pouze ze zprávy o vytvoření session,
  a Bob označí introduction tag jako neplatný, jakmile je session zničena.
- Rozšířené možnosti v hlavičce: Neočekávány, nedefinovány.

### RelayResponse (typ 4) {#relayresponse}

Toto je odpověď na [RelayRequest](#relayrequest) a je poslána od Boba k Alici.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob to Alice</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 byte IP address size; that many byte representation of Charlie's IP address; 2 byte Charlie's port number; 1 byte IP address size; that many byte representation of Alice's IP address; 2 byte Alice's port number; 4 byte nonce sent by Alice; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice's introKey, as received in the Relay Request (or Alice/Bob sessionKey, if established)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice's introKey, as received in the Relay Request (or Alice/Bob MAC Key, if established)</td>
</tr>
</table>
Formát zprávy:

```
+----+----+----+----+----+----+----+----+
|size|    Charlie IP     | Port (C)|size|
+----+----+----+----+----+----+----+----+
|    Alice IP       | Port (A)|  nonce
+----+----+----+----+----+----+----+----+
          |   arbitrary amount of       |
+----+----+                             +
|          uninterpreted data           |
~                .  .  .                ~
```
Typická velikost včetně hlavičky v současné implementaci: 64 (Alice IPv4) nebo 80 (Alice IPv6) bajtů (před non-mod-16 paddingem)

#### Poznámky

- Tato zpráva může být odeslána přes IPv4 nebo IPv6.
- IP adresa/port Alice jsou zdánlivá IP/port, na kterých Bob obdržel
  RelayRequest (nemusí nutně být IP, kterou Alice zahrnula do RelayRequest),
  a mohou být IPv4 nebo IPv6. Alice je aktuálně při příjmu ignoruje.
- IP adresa Charlie může být IPv4, nebo od vydání 0.9.50 IPv6,
  protože to je adresa, na kterou Alice
  odešle SessionRequest po Hole Punch.
- Relaying pro IPv6 je podporováno od vydání 0.9.50.
- Před vydáním 0.9.12 byl vždy používán intro key Alice. Od vydání
  0.9.12 se používá session key, pokud existuje navázané spojení mezi
  Alice a Bobem.
- Rozšířené možnosti v hlavičce: Neočekávané, nedefinované.

### RelayIntro (typ 5) {#relayintro}

Toto je představení pro Alice, které je zasláno od Boba k Charliemu.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob to Charlie</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 byte IP address size; that many byte representation of Alice's IP address; 2 byte port number (of Alice); 1 byte challenge size; that many bytes relayed from Alice; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob/Charlie sessionKey</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bob/Charlie MAC Key</td>
</tr>
</table>
Formát zprávy:

```
+----+----+----+----+----+----+----+----+
|size|     Alice IP      | Port (A)|size|
+----+----+----+----+----+----+----+----+
|      that many bytes of challenge     |
+                                       +
|        data relayed from Alice        |
+----+----+----+----+----+----+----+----+
| arbitrary amount of uninterpreted data|
~                .  .  .                ~
```
Typická velikost včetně hlavičky v současné implementaci: 48 bajtů (před non-mod-16 padding)

#### Poznámky

- Pro IPv4 je Alice IP adresa vždy 4 bajty, protože Alice se pokouší připojit k Charlie přes IPv4.
  Od verze 0.9.50 je podporováno IPv6 a Alice IP adresa může mít 16 bajtů.
- Pro IPv4 musí být tato zpráva odeslána přes navázané IPv4 spojení,
  protože to je jediný způsob, jak Bob zná Charlie IPv4 adresu, aby ji mohl vrátit Alice v RelayResponse.
  Od verze 0.9.50 je podporováno IPv6 a tato zpráva může být odeslána přes navázané IPv6 spojení.
- Od verze 0.9.50 musí jakákoli SSU adresa publikovaná s introducery obsahovat "4" nebo "6" v možnosti "caps".
- Challenge není implementováno, velikost challenge je vždy nula
- Rozšířené možnosti v hlavičce: Neočekávané, nedefinované.

### Data (typ 6) {#data}

Tato zpráva se používá pro přenos dat a potvrzení.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Any</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob sessionKey</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Alice/Bob MAC Key</td>
</tr>
</table>
**Data:** 1 byte příznaky (viz níže); pokud jsou zahrnuty explicitní ACK: 1 byte počet ACK, tolik 4 byte MessageIds plně potvrzených; pokud jsou zahrnuty ACK bitfields: 1 byte počet ACK bitfields, tolik 4 byte MessageIds + 1 nebo více bytů ACK bitfield (viz poznámky); Pokud jsou zahrnuty rozšířená data: 1 byte velikost dat, tolik bytů rozšířených dat (aktuálně neinterpretováno); 1 byte počet fragmentů (může být nula); Pokud nenulový, tolik fragmentů zpráv.

```
Flags byte:
  Bit order: 76543210 (bit 7 is MSB)
  bit 7: explicit ACKs included
  bit 6: ACK bitfields included
  bit 5: reserved
  bit 4: explicit congestion notification (ECN)
  bit 3: request previous ACKs
  bit 2: want reply
  bit 1: extended data included (unused, never set)
  bit 0: reserved
```
Každý fragment obsahuje: - 4 bytový messageId - 3 bytovou informaci o fragmentu:   - bity 23-17: číslo fragmentu 0 - 127   - bit 16: isLast (1 = true)   - bity 15-14: nepoužité, nastavené na 0 pro kompatibilitu s budoucím použitím   - bity 13-0: velikost fragmentu 0 - 16383 - tolik bytů dat fragmentu

Formát zprávy:

```
+----+----+----+----+----+----+----+----+
|flag| (additional headers, determined  |
+----+                                  +
~ by the flags, such as ACKs or         ~
| bitfields                             |
+----+----+----+----+----+----+----+----+
|#frg|     messageId     |   frag info  |
+----+----+----+----+----+----+----+----+
| that many bytes of fragment data      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
|     messageId     |   frag info  |    |
+----+----+----+----+----+----+----+    +
| that many bytes of fragment data      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
|     messageId     |   frag info  |    |
+----+----+----+----+----+----+----+    +
| that many bytes of fragment data      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
| arbitrary amount of uninterpreted data|
~                .  .  .                ~
```
#### Poznámky k ACK Bitfield

Bitové pole používá 7 nízkých bitů každého bajtu, přičemž vysoký bit specifikuje, zda za ním následuje další bajt bitového pole (1 = ano, 0 = aktuální bajt bitového pole je poslední). Tato sekvence 7bitových polí reprezentuje, zda byl fragment přijat - pokud je bit 1, fragment byl přijat. Pro objasnění, za předpokladu, že byly přijaty fragmenty 0, 2, 5 a 9, bajty bitového pole by byly následující:

```
byte 0:
   Bit order: 76543210 (bit 7 is MSB)
   bit 7: 1 (further bitfield bytes follow)
   bit 6: 0 (fragment 6 not received)
   bit 5: 1 (fragment 5 received)
   bit 4: 0 (fragment 4 not received)
   bit 3: 0 (fragment 3 not received)
   bit 2: 1 (fragment 2 received)
   bit 1: 0 (fragment 1 not received)
   bit 0: 1 (fragment 0 received)
byte 1:
   Bit order: 76543210 (bit 7 is MSB)
   bit 7: 0 (no further bitfield bytes)
   bit 6: 0 (fragment 13 not received)
   bit 5: 0 (fragment 12 not received)
   bit 4: 0 (fragment 11 not received)
   bit 3: 0 (fragment 10 not received)
   bit 2: 1 (fragment 9 received)
   bit 1: 0 (fragment 8 not received)
   bit 0: 0 (fragment 7 not received)
```
#### Poznámky

- Současná implementace přidává omezený počet duplicitních potvrzení pro
  zprávy dříve potvrzené, pokud je k dispozici místo.
- Pokud je počet fragmentů nula, jedná se o zprávu pouze s potvrzením nebo keepalive zprávu.
- Funkce ECN není implementována a bit není nikdy nastaven.
- V současné implementaci je bit want reply nastaven, když je počet
  fragmentů větší než nula, a není nastaven, když nejsou žádné fragmenty.
- Extended data není implementováno a nikdy není přítomno.
- Příjem více fragmentů je podporován ve všech vydáních. Přenos více
  fragmentů je implementován ve vydání 0.9.16.
- Jak je v současnosti implementováno, maximum fragmentů je 64 (maximální číslo fragmentu = 63).
- Jak je v současnosti implementováno, maximální velikost fragmentu je samozřejmě menší než MTU.
- Dávejte pozor, abyste nepřekročili maximální MTU, i když je velký počet
  ACK k odeslání.
- Protokol umožňuje fragmenty nulové délky, ale není důvod je posílat.
- V SSU data používají krátkou 5-bajtovou I2NP hlavičku následovanou payload
  I2NP zprávy místo standardní 16-bajtové I2NP hlavičky. Krátká I2NP
  hlavička se skládá pouze z jednobajtového I2NP typu a 4-bajtové expirace v
  sekundách. I2NP message ID je použito jako message ID pro fragment. I2NP
  velikost je sestavena z velikostí fragmentů. I2NP kontrolní součet není
  vyžadován, protože integrita UDP zprávy je zajištěna dešifrováním.
- Message ID nejsou pořadová čísla a nejsou po sobě následující. SSU nezaručuje
  dodání ve správném pořadí. Zatímco používáme I2NP message ID jako SSU
  message ID, z pohledu SSU protokolu jsou to náhodná čísla. Ve skutečnosti,
  protože router používá jediný Bloom filtr pro všechny peery, message ID
  musí být skutečným náhodným číslem.
- Protože neexistují pořadová čísla, neexistuje způsob, jak si být jistý, že bylo ACK
  přijato. Současná implementace rutinně posílá velké množství
  duplicitních ACK. Duplicitní ACK by neměly být brány jako známka
  přetížení.
- Poznámky k ACK Bitfield: Příjemce datového paketu neví, kolik
  fragmentů je ve zprávě, pokud nepřijal poslední fragment.
  Proto počet bitfield bajtů odeslaných v odpovědi může být menší nebo větší
  než počet fragmentů dělený 7. Například pokud nejvyšší
  fragment, který příjemce viděl, má číslo 4, je třeba odeslat pouze jeden bajt,
  i když celkem může být 13 fragmentů. Až 10 bajtů (tj. (64 / 7)
  + 1) může být zahrnuto pro každé potvrzené message ID.
- Extended options v hlavičce: Neočekávané, nedefinované.

### PeerTest (typ 7) {#peertest}

Viz [SSU Peer Testing](/docs/transport/ssu/#peerTesting) pro podrobnosti. Poznámka: IPv6 peer testing je podporováno od vydání 0.9.27.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Peer:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Any</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Data:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4 byte nonce; 1 byte IP address size (may be zero); that many byte representation of Alice's IP address, if size > 0; 2 byte Alice's port number; Alice's or Charlie's 32-byte introduction key; N bytes, currently uninterpreted</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>Crypto Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">See notes below</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><strong>MAC Key used:</strong></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">See notes below</td>
</tr>
</table>
Použitý kryptografický klíč (uvedeno v pořadí výskytu): 1. Při odeslání od Alice k Bobovi: Alice/Bob sessionKey 2. Při odeslání od Boba k Charliemu: Bob/Charlie sessionKey 3. Při odeslání od Charlieho k Bobovi: Bob/Charlie sessionKey 4. Při odeslání od Boba k Alice: Alice/Bob sessionKey (nebo pro Boba před verzí 0.9.52, Alicein introKey) 5. Při odeslání od Charlieho k Alice: Alicein introKey, jak byl přijat ve zprávě PeerTest od Boba 6. Při odeslání od Alice k Charliemu: Charlieho introKey, jak byl přijat ve zprávě PeerTest od Charlieho

Použitý MAC klíč (uvedeny v pořadí výskytu): 1. Při odesílání od Alice k Bobovi: Alice/Bob MAC klíč 2. Při odesílání od Boba k Charliemu: Bob/Charlie MAC klíč 3. Při odesílání od Charlieho k Bobovi: Bob/Charlie MAC klíč 4. Při odesílání od Boba k Alici: Alice's introKey, jak byl přijat ve zprávě PeerTest od Alice 5. Při odesílání od Charlieho k Alici: Alice's introKey, jak byl přijat ve zprávě PeerTest od Boba 6. Při odesílání od Alice k Charliemu: Charlie's introKey, jak byl přijat ve zprávě PeerTest od Charlieho

Formát zprávy:

```
+----+----+----+----+----+----+----+----+
|    test nonce     |size| Alice IP addr
+----+----+----+----+----+----+----+----+
     | Port (A)|                        |
+----+----+----+                        +
| Alice or Charlie's                    |
+ introduction key (Alice's is sent to  +
| Bob and Charlie, while Charlie's is   |
+ sent to Alice)                        +
|                                       |
+              +----+----+----+----+----+
|              | arbitrary amount of    |
+----+----+----+                        |
| uninterpreted data                    |
~                .  .  .                ~
```
Typická velikost včetně hlavičky v současné implementaci: 80 bajtů (před non-mod-16 paddingem)

#### Poznámky

- Když odesílá Alice, velikost IP adresy je 0, IP adresa není přítomna a port
  je 0, protože Bob a Charlie data nepoužívají; cílem je zjistit
  Alicinu skutečnou IP adresu/port a říct to Alici; Bob a Charlie se nestarají o to, co
  si Alice myslí, že je její adresa.
- Když odesílá Bob nebo Charlie, IP a port jsou přítomny a IP adresa má
  4 nebo 16 bytů. Testování IPv6 je podporováno od verze 0.9.27.
- Když odesílá Charlie Alici, IP a port jsou následující:
  Poprvé (zpráva 5): Alicina požadovaná IP a port jak byly přijaty ve zprávě 2.
  Podruhé (zpráva 7): Alicina skutečná IP a port, ze kterých byla zpráva 6 přijata.
- Poznámky k IPv6: Do verze 0.9.26 je podporováno pouze testování IPv4 adres. Proto
  veškerá komunikace Alice-Bob a Alice-Charlie musí probíhat přes IPv4. Komunikace Bob-Charlie
  však může probíhat přes IPv4 nebo IPv6. Alicina adresa, když je
  specifikována ve zprávě PeerTest, musí mít 4 byty.
  Od verze 0.9.27 je podporováno testování IPv6 adres
  a komunikace Alice-Bob a Alice-Charlie může probíhat přes IPv6,
  pokud Bob a Charlie indikují podporu pomocí schopnosti 'B' ve své publikované IPv6 adrese.
  Podrobnosti viz Návrh 126.
- Alice odesílá požadavek Bobovi pomocí existující relace přes transport (IPv4 nebo IPv6), který chce testovat.
  Když Bob přijme požadavek od Alice přes IPv4, Bob musí vybrat Charlieho, který inzeruje IPv4 adresu.
  Když Bob přijme požadavek od Alice přes IPv6, Bob musí vybrat Charlieho, který inzeruje IPv6 adresu.
  Skutečná komunikace Bob-Charlie může probíhat přes IPv4 nebo IPv6 (tj. nezávisle na typu Aliciny adresy).
- Peer musí udržovat tabulku aktivních stavů testů (nonce). Po přijetí
  zprávy PeerTest vyhledá nonce v tabulce. Pokud je nalezen, jedná se o
  existující test a znáte svou roli (Alice, Bob nebo Charlie). Jinak, pokud
  IP není přítomna a port je 0, jedná se o nový test a jste Bob.
  Jinak se jedná o nový test a jste Charlie.
- Od verze 0.9.15 musí mít Alice navázanou relaci s Bobem a použít
  klíč relace.
- Před API verzí 0.9.52 v některých implementacích Bob odpovídal Alici pomocí
  Alicina intro klíče místo klíče relace Alice/Bob, i když
  Alice a Bob měli navázanou relaci (od 0.9.15).
  Od API verze 0.9.52 Bob bude správně používat klíč relace ve všech
  implementacích a Alice by měla odmítnout zprávu přijatou od Boba
  s Aliciným intro klíčem, pokud má Bob API verzi 0.9.52 nebo vyšší.
- Rozšířené možnosti v hlavičce: Neočekávané, nedefinované.

### HolePunch {#holepunch}

HolePunch je jednoduše UDP paket bez dat. Je neautentizovaný a nešifrovaný. Neobsahuje SSU hlavičku, takže nemá číslo typu zprávy. Je odeslán od Charlieho k Alici jako součást sekvence Introduction.

## Ukázkové datagramy {#sampledatagrams}

### Minimální datová zpráva

- žádné fragmenty, žádné ACK, žádné NACK, atd.
- Velikost: 39 bajtů

```
+----+----+----+----+----+----+----+----+
|                  MAC                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                   IV                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag|        time       |flag|#frg|    |
+----+----+----+----+----+----+----+    +
|  padding to fit a full AES256 block   |
+----+----+----+----+----+----+----+----+
```
### Minimální datová zpráva s datovou částí

- Velikost: 46+fragmentSize bytů

```
+----+----+----+----+----+----+----+----+
|                  MAC                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|                   IV                  |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|flag|        time       |flag|#frg|
+----+----+----+----+----+----+----+----+
  messageId    |   frag info  |         |
----+----+----+----+----+----+         +
| that many bytes of fragment data      |
~                .  .  .                ~
|                                       |
+----+----+----+----+----+----+----+----+
```
## Reference

- [AES šifrování](/docs/specs/cryptography/#AES)
- [Specifikace běžných struktur](/docs/specs/common-structures/)
- [Datum](/docs/specs/common-structures/#date)
- [ElGamal šifrování](/docs/specs/cryptography/#elgamal)
- [Podrobnosti HMAC](/docs/specs/cryptography/#udp)
- [I2P zdrojový kód](https://github.com/i2p/i2p.i2p)
- [i2pd zdrojový kód](https://github.com/PurpleI2P/i2pd)
- [KeyCertificate](/docs/specs/common-structures/#key-certificates)
- [RouterIdentity](/docs/specs/common-structures/#routeridentity)
- [SessionKey](/docs/specs/common-structures/#sessionkey)
- [Podpis](/docs/specs/common-structures/#signature)
- [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey)
- [SigningPublicKey](/docs/specs/common-structures/#signingpublickey)
- [Přehled SSU](/docs/transport/ssu/)
- [SSU klíče](/docs/transport/ssu/#keys)
- [SSU testování peerů](/docs/transport/ssu/#peerTesting)
