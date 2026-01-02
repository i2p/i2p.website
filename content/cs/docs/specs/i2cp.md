---
title: "Klientský protokol I2P (I2CP)"
description: "Jak aplikace vyjednávají relace, tunnels a LeaseSets s I2P routerem."
slug: "i2cp"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Přehled

I2CP je nízkoúrovňový řídicí protokol mezi I2P routerem a libovolným klientským procesem. Definuje přísné oddělení odpovědností:

- **Router**: Spravuje směrování, kryptografii, životní cykly pro tunnel a operace síťové databáze
- **Klient**: Volí parametry anonymity, konfiguruje tunnels a odesílá/přijímá zprávy

Veškerá komunikace probíhá přes jediný TCP socket (volitelně obalený protokolem TLS), což umožňuje asynchronní, plně duplexní provoz.

**Verze protokolu**: I2CP používá bajt verze protokolu `0x2A` (42 v desítkové soustavě), který je odesílán při počátečním navázání spojení. Tento bajt verze zůstal stabilní od vzniku protokolu.

**Aktuální stav**: Tato specifikace je platná pro verzi routeru 0.9.67 (verzi API 0.9.67), vydanou 2025-09.

## Kontext implementace

### Implementace v Javě

Referenční implementace je v Java I2P: - Klientské SDK: `i2p.jar` balíček - Implementace routeru: `router.jar` balíček - [Javadocs](http://docs.i2p-projekt.de/javadoc/)

Když klient a router běží ve stejné JVM, zprávy I2CP se předávají jako objekty jazyka Java bez serializace. Externí klienti používají serializovaný protokol přes TCP.

### Implementace v C++

i2pd (C++ I2P router) také externě implementuje I2CP pro klientská připojení.

### Klienti nepsaní v Javě

Neexistují **žádné známé implementace mimo Javu** úplné klientské knihovny I2CP. Aplikace, které nejsou v Javě, by měly místo toho používat protokoly vyšší úrovně:

- **SAM (Simple Anonymous Messaging) v3**: Soketové rozhraní s knihovnami v různých jazycích
- **BOB (Basic Open Bridge)**: Jednodušší alternativa k SAM

Tyto protokoly vyšší úrovně interně řeší složitost I2CP a také poskytují streamovací knihovnu (pro spojení podobná TCP) a datagramovou knihovnu (pro spojení podobná UDP).

## Navázání spojení

### 1. TCP spojení

Připojte se k portu I2CP routeru: - Výchozí: `127.0.0.1:7654` - Lze konfigurovat v nastavení routeru - Volitelná obalovací vrstva TLS (důrazně doporučeno pro vzdálená připojení)

### 2. Protokolový handshake

**Krok 1**: Odešlete bajt verze protokolu `0x2A`

**Krok 2**: Synchronizace hodin

```
Client → Router: GetDateMessage
Router → Client: SetDateMessage
```
Router vrací své aktuální časové razítko a řetězec verze I2CP API (od 0.8.7).

**Krok 3**: Ověření (pokud je povoleno)

Od verze 0.9.11 lze autentizaci zahrnout do GetDateMessage prostřednictvím Mapping (mapování) obsahujícího: - `i2cp.username` - `i2cp.password`

Od verze 0.9.16, pokud je ověřování povoleno, **musí** být dokončeno prostřednictvím GetDateMessage (zpráva GetDate) dříve, než budou odeslány jakékoli jiné zprávy.

**Krok 4**: Vytvoření relace

```
Client → Router: CreateSessionMessage (contains SessionConfig)
Router → Client: SessionStatusMessage (status=Created)
```
**Krok 5**: Signál připravenosti pro tunnel

```
Router → Client: RequestVariableLeaseSetMessage
```
Tato zpráva indikuje, že byly vytvořeny příchozí tunnels. Router to NEODEŠLE, dokud nebude existovat alespoň jeden příchozí a jeden odchozí tunnel.

**Krok 6**: Publikace leaseSet

```
Client → Router: CreateLeaseSet2Message
```
V tomto okamžiku je relace plně funkční pro odesílání a přijímání zpráv.

## Vzory toků zpráv

### Odchozí zpráva (klient odesílá na vzdálený cíl)

**S nastavením i2cp.messageReliability=none**:

```
Client → Router: SendMessageMessage (nonce=0)
[No acknowledgments]
```
**Při nastavení i2cp.messageReliability=BestEffort (nejlepší snaha)**:

```
Client → Router: SendMessageMessage (nonce>0)
Router → Client: MessageStatusMessage (status=Accepted)
Router → Client: MessageStatusMessage (status=Success or Failure)
```
### Příchozí zpráva (Router doručuje klientovi)

**S i2cp.fastReceive=true** (výchozí od verze 0.9.4):

```
Router → Client: MessagePayloadMessage
[No acknowledgment required]
```
**Při i2cp.fastReceive=false** (ZASTARALÉ):

```
Router → Client: MessageStatusMessage (status=Available)
Client → Router: ReceiveMessageBeginMessage
Router → Client: MessagePayloadMessage
Client → Router: ReceiveMessageEndMessage
```
Moderní klienti by měli vždy používat rychlý režim příjmu.

## Společné datové struktury

### Hlavička zprávy I2CP

Všechny zprávy I2CP používají tuto společnou hlavičku:

```
+----+----+----+----+----+----+----+----+
| Body Length (4 bytes)                 |
+----+----+----+----+----+----+----+----+
|Type|  Message Body (variable)        |
+----+----+----+----+----+----+----+----+
```
- **Délka těla**: 4bajtové celé číslo, pouze délka těla zprávy (nezahrnuje hlavičku)
- **Typ**: 1bajtové celé číslo, identifikátor typu zprávy
- **Tělo zprávy**: 0+ bajtů, formát se liší podle typu zprávy

**Limit velikosti zprávy**: Přibližně 64 KB maximálně.

### ID relace

2bajtové celé číslo, které jedinečně identifikuje relaci na routeru.

**Speciální hodnota**: `0xFFFF` označuje "žádná relace" (používá se pro vyhledávání názvů hostitelů bez navázané relace).

### ID zprávy

4bajtové celé číslo generované routerem k jednoznačné identifikaci zprávy v rámci relace.

**Důležité**: ID zpráv **nejsou** globálně jedinečná, pouze jedinečná v rámci relace. Jsou také odlišná od nonce (jednorázová hodnota) generované klientem.

### Formát užitečných dat

Užitečná data zprávy jsou komprimována gzipem se standardním 10bajtovým záhlavím gzip: - Začíná: `0x1F 0x8B 0x08` (RFC 1952) - Od verze 0.7.1: Nevyužité části záhlaví gzip obsahují informace o protokolu, from-port a to-port - To umožňuje streamování a datagramy na stejné Destination (cílový identifikátor v I2P)

**Řízení komprese**: Nastavte `i2cp.gzip=false` pro vypnutí komprese (nastaví úroveň komprese gzip na 0). Hlavička gzip je stále zahrnuta, ale s minimální režií komprese.

### Struktura SessionConfig

Určuje konfiguraci klientské relace:

```
+----------------------------------+
| Destination                      |
+----------------------------------+
| Mapping (configuration options)  |
+----------------------------------+
| Creation Date                    |
+----------------------------------+
| Signature                        |
+----------------------------------+
```
**Kritické požadavky**: 1. **Mapping musí být seřazen podle klíče** pro ověření podpisu 2. **Creation Date** musí být v rozmezí ±30 sekund od aktuálního času routeru 3. **Signature** je vytvořen pomocí SigningPrivateKey (soukromého podepisovacího klíče) objektu Destination (cílové identity)

**Offline podpisy** (od verze 0.9.38):

Pokud používáte offline podepisování, musí mapování obsahovat: - `i2cp.leaseSetOfflineExpiration` - `i2cp.leaseSetTransientPublicKey` - `i2cp.leaseSetOfflineSignature`

Signature se poté vygeneruje dočasným SigningPrivateKey (soukromým klíčem pro podepisování).

## Možnosti konfigurace jádra

### Konfigurace tunnelu

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Default</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>inbound.length</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Number of hops for inbound tunnels</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.length</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Number of hops for outbound tunnels</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>inbound.lengthVariance</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Random variance in hop count (since 0.7.6)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.lengthVariance</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Random variance in hop count (since 0.7.6)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>inbound.quantity</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Number of concurrent inbound tunnels</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.quantity</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Number of concurrent outbound tunnels</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>inbound.backupQuantity</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Standby inbound tunnels (hot spares)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.backupQuantity</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Standby outbound tunnels (hot spares)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>inbound.allowZeroHop</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">true</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Allow 0-hop tunnels (disable for full anonymity)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.allowZeroHop</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">true</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Allow 0-hop tunnels (disable for full anonymity)</td>
    </tr>
  </tbody>
</table>
**Poznámky**: - Hodnoty pro `quantity` > 6 vyžadují peery běžící na verzi 0.9.0+ a výrazně zvyšují nároky na zdroje - Nastavte `backupQuantity` na 1-2 pro služby s vysokou dostupností - tunnels s nulovým počtem skoků obětují anonymitu ve prospěch latence, ale jsou užitečné pro testování

### Zpracování zpráv

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Default</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>clientMessageTimeout</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">60000&nbsp;ms</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy timeout for message delivery</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.messageReliability</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">BestEffort</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>None</code>, <code>BestEffort</code>, or <code>Guaranteed</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.fastReceive</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">true</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Skip ReceiveMessageBegin/End handshake (default since 0.9.4)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.gzip</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">true</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Enable gzip compression of message payloads</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>outbound.priority</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Priority for outbound scheduling (-25 to +25)</td>
    </tr>
  </tbody>
</table>
**Spolehlivost zpráv**: - `None`: Žádná potvrzení od routeru (výchozí nastavení streamovací knihovny od verze 0.8.1) - `BestEffort`: Router posílá informaci o přijetí + oznámení o úspěchu/neúspěchu - `Guaranteed`: Neimplementováno (aktuálně se chová jako BestEffort)

**Přebití pro jednotlivé zprávy** (od verze 0.9.14): - V relaci s `messageReliability=none`, nastavení nenulového nonce vyžádá potvrzení o doručení pro danou zprávu - Nastavení nonce=0 v relaci `BestEffort` vypne oznámení pro tuto zprávu

### Konfigurace LeaseSet (záznam s parametry doručování cílové služby v I2P)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Default</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.dontPublishLeaseSet</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">false</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Disable automatic LeaseSet publication (for client-only destinations)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetType</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet variant: 1 = standard, 3 = LS2, 5 = encrypted, 7 = meta</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetEncType</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Comma-separated encryption type codes (see below)</td>
    </tr>
  </tbody>
</table>
### Zastaralé značky relace ElGamal/AES

Tyto možnosti platí pouze pro zastaralé šifrování ElGamal:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Default</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>crypto.lowTagThreshold</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">30</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Minimum session tags before replenishing</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>crypto.tagsToSend</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">40</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Number of tags to send in a batch</td>
    </tr>
  </tbody>
</table>
**Poznámka**: klienti ECIES-X25519 používají odlišný ráčnový mechanismus a tato nastavení ignorují.

## Typy šifrování

I2CP podporuje více end-to-end šifrovacích schémat prostřednictvím volby `i2cp.leaseSetEncType`. Lze zadat více typů (oddělených čárkou) pro podporu jak moderních, tak i starších peerů.

### Podporované typy šifrování

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Algorithm</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ElGamal/AES+SessionTags</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">2048-bit ElGamal</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Legacy</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1-3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">-</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unused</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-X25519-AEAD-Ratchet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32-byte X25519</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.46</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current Standard</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-X25519-AEAD-Ratchet + ML-KEM-768 hybrid</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32&nbsp;+&nbsp;PQ</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECIES-X25519-AEAD-Ratchet + ML-KEM-1024 hybrid</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32&nbsp;+&nbsp;PQ</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.67</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Beta</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved (likely ML-KEM-512 hybrid)</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">32&nbsp;+&nbsp;PQ</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Future</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Planned</td>
    </tr>
  </tbody>
</table>
**Doporučená konfigurace**:

```
i2cp.leaseSetEncType=4,0
```
Toto poskytuje X25519 (preferované; eliptická výměna klíčů na křivce Curve25519) se záložní variantou ElGamal (asymetrické šifrování) pro kompatibilitu.

### Podrobnosti o typech šifrování

**Typ 0 - ElGamal/AES+SessionTags**: - 2048bitové veřejné klíče ElGamal (256 bajtů) - Symetrické šifrování AES-256 - 32bajtové session tags (dočasné značky relace) odesílané v dávkách - Vysoká režie CPU, šířky pásma a paměti - Postupně vyřazováno napříč sítí

**Typ 4 - ECIES-X25519-AEAD-Ratchet**: - Výměna klíčů X25519 (32bajtové klíče) - ChaCha20/Poly1305 AEAD - Dvojitý ratchet ve stylu Signal - 8bajtové session tags (značky relace) (oproti 32bajtovým u ElGamalu) - Tagy generované pomocí synchronizovaného PRNG (pseudonáhodný generátor) (nejsou posílány předem) - ~92% snížení režie oproti ElGamalu - Standard pro moderní I2P (většina routers to používá)

**Typy 5-6 - postkvantový hybrid**: - Kombinuje X25519 s ML-KEM (NIST FIPS 203) - Poskytuje zabezpečení odolné vůči kvantovým počítačům - ML-KEM-768 pro vyvážený poměr zabezpečení/výkonu - ML-KEM-1024 pro maximální zabezpečení - Větší velikosti zpráv kvůli postkvantovému (PQ) klíčovému materiálu - Podpora v síti je stále zaváděna

### Migrační strategie

Síť I2P aktivně přechází z ElGamal (typ 0) na X25519 (typ 4): - NTCP → NTCP2 (dokončeno) - SSU → SSU2 (dokončeno) - ElGamal tunnels → X25519 tunnels (dokončeno) - ElGamal end-to-end (mezi koncovými body) → ECIES-X25519 (z větší části dokončeno)

## LeaseSet2 a pokročilé funkce

### Možnosti LeaseSet2 (od 0.9.38)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Option</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetType</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Specifies LeaseSet variant (1, 3, 5, 7)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetEncType</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Encryption types supported (comma-separated)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetAuthType</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.41</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Per-client authentication: 0 = none, 1 = DH, 2 = PSK</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetPrivKey</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.41</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">X25519 private key for decrypting LS2 with auth</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetSecret</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Base64 secret for blinded addresses</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetTransientPublicKey</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.38</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Transient signing key for offline signatures</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetPrivateKey</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.18</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Persistent LeaseSet encryption keys (type:key pairs)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetOption.nnn</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Service records (proposal 167)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetClient.dh.nnn</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.41</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DH client auth material (indexed from 0)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>i2cp.leaseSetClient.psk.nnn</code></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.41</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">PSK client auth material (indexed from 0)</td>
    </tr>
  </tbody>
</table>
### Zaslepené adresy

Od verze 0.9.39 mohou destinace používat "blinded" (zaslepené) adresy (formát b33), které se pravidelně mění: - Vyžaduje `i2cp.leaseSetSecret` pro ochranu heslem - Volitelné ověřování pro jednotlivé klienty - Podrobnosti viz návrhy 123 a 149

### Záznamy služeb (od verze 0.9.66)

LeaseSet2 podporuje možnosti záznamu služby (návrh 167):

```
i2cp.leaseSetOption.0=_smtp._tcp=1 86400 0 0 25 mail.example.b32.i2p
```
Formát vychází ze stylu záznamu DNS SRV, ale je přizpůsoben pro I2P.

## Více relací (od verze 0.9.21)

Jedno připojení I2CP může udržovat více relací:

**Primární relace**: První relace vytvořená v rámci spojení **Podrelace**: Další relace sdílející tunnel pool primární relace

### Vlastnosti podrelace

1. **Sdílené Tunnels**: Použijte stejné pooly příchozích/odchozích tunnels jako primární relace
2. **Sdílené šifrovací klíče**: Musí používat totožné LeaseSet šifrovací klíče
3. **Odlišné podpisové klíče**: Musí používat odlišné podpisové klíče Destination (identifikátor služby v I2P)
4. **Bez záruky anonymity**: Jednoznačně propojeno s primární relací (stejný router, stejné tunnels)

### Případ použití Subsession (podrelace)

Povolit komunikaci s destinacemi používajícími různé typy podpisů: - Hlavní: podpis EdDSA (moderní) - Subsession (podřízená relace): podpis DSA (zpětná kompatibilita)

### Životní cyklus podrelace

**Vytvoření**:

```
Client → Router: CreateSessionMessage
Router → Client: SessionStatusMessage (unique Session ID)
Router → Client: RequestVariableLeaseSetMessage (separate for each destination)
Client → Router: CreateLeaseSet2Message (separate for each destination)
```
**Zrušení**: - Zrušení podrelace: Ponechá primární relaci nedotčenou - Zrušení primární relace: Zruší všechny podrelace a uzavře spojení - DisconnectMessage (zpráva pro odpojení): Zruší všechny relace

### Zpracování ID relace

Většina zpráv I2CP obsahuje pole Session ID. Výjimky: - DestLookup / DestReply (zastaralé, použijte HostLookup / HostReply) - GetBandwidthLimits / BandwidthLimits (odpověď není specifická pro relaci)

**Důležité**: Klienti by současně neměli mít více nevyřízených zpráv CreateSession, protože odpovědi nelze jednoznačně spárovat s požadavky.

## Katalog zpráv

### Přehled typů zpráv

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Direction</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">CreateSession</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ReconfigureSession</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DestroySession</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">CreateLeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SendMessage</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ReceiveMessageBegin</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ReceiveMessageEnd</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">GetBandwidthLimits</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SessionStatus</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">21</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">RequestLeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">22</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">MessageStatus</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">23</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">BandwidthLimits</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">29</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ReportAbuse</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bidirectional</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unused</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">30</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Disconnect</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bidirectional</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">31</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">MessagePayload</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">32</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">GetDate</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">33</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SetDate</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">34</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DestLookup</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">35</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DestReply</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Deprecated</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">36</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SendMessageExpires</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.7.1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">37</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">RequestVariableLeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">38</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">HostLookup</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.11</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">39</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">HostReply</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">R → C</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.11</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">41</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">CreateLeaseSet2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.39</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">42</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">BlindingInfo</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">C → R</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.43</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Current</td>
    </tr>
  </tbody>
</table>
**Legenda**: C = Klient, R = Router

### Podrobnosti o klíčové zprávě

#### CreateSessionMessage (Typ 1)

**Účel**: Zahájit novou relaci I2CP

**Obsah**: struktura SessionConfig

**Odpověď**: SessionStatusMessage (status=Created nebo Invalid)

**Požadavky**: - Datum v SessionConfig musí být v rozmezí ±30 sekund od času routeru - Mapování musí být seřazeno podle klíče pro ověření podpisu - Destination (identifikátor cíle v I2P) nesmí již mít aktivní relaci

#### RequestVariableLeaseSetMessage (Typ 37)

**Účel**: Router vyžaduje autorizaci klienta pro příchozí tunnels

**Obsah**: - ID relace - Počet Lease (záznamů o vstupních tunelech) - Pole struktur Lease (každá s vlastním časem vypršení platnosti)

**Odpověď**: CreateLeaseSet2Message

**Význam**: Toto je signál, že relace je v provozu. Router toto odešle až poté, co: 1. je sestaven alespoň jeden inbound tunnel 2. je sestaven alespoň jeden outbound tunnel

**Doporučení pro časový limit**: Klienti by měli relaci ukončit, pokud tato zpráva není přijata během 5+ minut od vytvoření relace.

#### CreateLeaseSet2Message (Typ 41)

**Účel**: Klient publikuje LeaseSet do síťové databáze

**Obsah**: - ID relace - bajt typu LeaseSet (1, 3, 5 nebo 7) - LeaseSet nebo LeaseSet2 nebo EncryptedLeaseSet nebo MetaLeaseSet - Počet soukromých klíčů - Seznam soukromých klíčů (jeden pro každý veřejný klíč v LeaseSet, ve stejném pořadí)

**Soukromé klíče**: Nezbytné pro dešifrování příchozích garlic messages (I2P zprávy typu „garlic“). Formát:

```
Encryption type (2 bytes)
Key length (2 bytes)
Private key data (variable)
```
**Poznámka**: Nahrazuje zastaralou zprávu CreateLeaseSetMessage (typ 4), která nepodporuje: - varianty LeaseSet2 - šifrování jiné než ElGamal - více typů šifrování - šifrované LeaseSets - offline podpisové klíče

#### SendMessageExpiresMessage (Typ 36)

**Účel**: Odeslat zprávu na cílovou adresu s nastavením expirace a pokročilými možnostmi

**Obsah**: - ID relace - Cíl - Užitečná data (komprimovaná gzipem) - Nonce (jednorázová hodnota) (4 bajty) - Příznaky (2 bajty) - viz níže - Datum vypršení (6 bajtů, zkráceno z 8)

**Pole příznaků** (2 bajty, pořadí bitů 15...0):

**Bity 15-11**: Nepoužité, musí být 0

**Bity 10-9**: Přebití spolehlivosti zprávy (nepoužito, místo toho použijte nonce (jednorázovou hodnotu))

**Bit 8**: Nezahrnovat LeaseSet - 0: Router může zahrnout LeaseSet do garlic (I2P technika seskupování zpráv) - 1: Nezahrnovat LeaseSet

**Bity 7-4**: Nízký práh tagů (pouze pro ElGamal, u ECIES se ignoruje)

```
0000 = Use session settings
0001 = 2 tags
0010 = 3 tags
...
1111 = 192 tags
```
**Bity 3-0**: Tagy k odeslání v případě potřeby (pouze ElGamal, ignorováno pro ECIES)

```
0000 = Use session settings
0001 = 2 tags
0010 = 4 tags
...
1111 = 160 tags
```
#### MessageStatusMessage (Typ 22)

**Účel**: Informovat klienta o stavu doručení zprávy

**Obsah**: - ID relace - ID zprávy (generované routerem) - Kód stavu (1 bajt) - Velikost (4 bajty, relevantní pouze pro status=0) - Nonce (4 bajty, odpovídá nonce klienta pro SendMessage)

**Stavové kódy** (Odchozí zprávy):

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Meaning</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Result</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Accepted</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Router accepted message</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Success</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Best Effort Success</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Probable delivery</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Success</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Guaranteed Success</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Probable delivery</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Success</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Local Success</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Delivered to local client</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Success</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Best Effort Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Probable failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Guaranteed Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Generic failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Local Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Local delivery failed</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">8</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Router Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Router shutdown/error</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">9</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Network Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No network connectivity</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">10</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Session</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Invalid/closed session</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">11</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Message</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Invalid payload</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">12</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Options</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Invalid options/expiration</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">13</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Overflow Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Queue/buffer full</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">14</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Message Expired</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Expired before send</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">15</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Local LeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Local LeaseSet problem</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">16</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No Local Tunnels</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No tunnels available</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">17</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Unsupported Encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Incompatible encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">18</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Invalid remote destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">19</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Bad Leaseset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Invalid remote LeaseSet</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">20</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Expired Leaseset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Remote LeaseSet expired</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">21</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">No Leaseset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Remote LeaseSet not found</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">22</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Meta Leaseset</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Cannot send to meta LS</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">23</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Loopback Denied</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Same source and destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
    </tr>
  </tbody>
</table>
**Kódy úspěchu**: 1, 2, 4, 6 **Kódy selhání**: Všechny ostatní

**Kód stavu 0** (ZASTARALÉ): Dostupná zpráva (příchozí, rychlý příjem deaktivován)

#### HostLookupMessage (Typ 38)

**Účel**: Vyhledání destination (I2P adresa) podle názvu hostitele nebo hashe (nahrazuje DestLookup)

**Obsah**: - ID relace (nebo 0xFFFF, pokud není relace) - ID požadavku (4 bajty) - Časový limit v milisekundách (4 bajty, min. doporučeno: 10000) - Typ požadavku (1 bajt) - Vyhledávací klíč (Hash, řetězec názvu hostitele, nebo Destination (cílový identifikátor v I2P))

**Typy požadavků**:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Lookup Key</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Returns</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Since</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Hash</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Hostname String</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">Original</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Hash</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination + Options</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Hostname String</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination + Options</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Destination + Options</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0.9.66</td>
    </tr>
  </tbody>
</table>
Typy 2-4 vracejí možnosti LeaseSet (návrh 167), pokud jsou k dispozici.

**Odpověď**: HostReplyMessage (zpráva s odpovědí hostitele)

#### HostReplyMessage (Typ 39)

**Účel**: Odpověď na HostLookupMessage (zpráva pro vyhledání hostitele)

**Obsah**: - ID relace - ID požadavku - Kód výsledku (1 bajt) - Destination (identita cíle v I2P) (přítomno při úspěchu, někdy i u specifických selhání) - Mapování (pouze pro typy vyhledávání 2-4, může být prázdné)

**Kódy výsledků**:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Name</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Meaning</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Success</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Lookup succeeded</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Generic failure</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Lookup Password Required</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded address requires password</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Private Key Required</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded address requires private key</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Password and Key Required</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Blinded address requires both</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet Decryption Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Cannot decrypt LeaseSet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet Lookup Failure</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">LeaseSet not found in netdb</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Lookup Type Unsupported</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Router doesn't support this type</td>
    </tr>
  </tbody>
</table>
#### BlindingInfoMessage (zpráva s informacemi o zaslepení) (Typ 42)

**Účel**: Informovat router o požadavcích na autentizaci pro blinded destination (oslepenou destinaci) (od verze 0.9.43)

**Obsah**: - ID relace - Příznaky (1 bajt) - Typ koncového bodu (1 bajt): 0=Hash, 1=hostname, 2=Destination, 3=SigType+Key - Typ zaslepeného podpisu (2 bajty) - Vypršení platnosti (4 bajty, sekundy od epochy) - Data koncového bodu (liší se podle typu) - Soukromý klíč (32 bajtů, pouze pokud je v příznacích nastaven bit 0) - Heslo pro vyhledávání (String, pouze pokud je v příznacích nastaven bit 4)

**Příznaky** (pořadí bitů 76543210):

- **Bit 0**: 0=pro všechny, 1=pro jednotlivé klienty
- **Bity 3-1**: Autentizační schéma (pokud bit 0=1): 000=DH, 001=PSK
- **Bit 4**: 1=vyžadován secret (tajemství)
- **Bity 7-5**: Nepoužito, nastavte na 0

**Žádná odpověď**: Router zpracovává tiše

**Případ použití**: Před odesláním na blinded destination (zaslepená destinace) (b33 address - adresa b33) musí klient buď: 1. vyhledat b33 pomocí HostLookup, NEBO 2. odeslat zprávu BlindingInfo

Pokud cíl vyžaduje autentizaci, BlindingInfo je povinné.

#### ReconfigureSessionMessage (Typ 2)

**Účel**: Aktualizovat konfiguraci relace po vytvoření

**Obsah**: - ID relace - SessionConfig (stačí pouze změněné volby)

**Odpověď**: SessionStatusMessage (status=Updated nebo Invalid)

**Poznámky**: - Router sloučí novou konfiguraci se stávající konfigurací - Možnosti tunnelu (`inbound.*`, `outbound.*`) se vždy uplatní - Některé možnosti mohou být po vytvoření relace neměnné - Datum musí být v rámci ±30 sekund od času routeru - Mapování musí být seřazeno podle klíče

#### DestroySessionMessage (Typ 3)

**Účel**: Ukončit relaci

**Obsah**: ID relace

**Očekávaná odpověď**: SessionStatusMessage (status=Destroyed)

**Skutečné chování** (Java I2P až do verze 0.9.66 včetně): - Router nikdy neodesílá SessionStatus(Destroyed) - Pokud nezůstane žádná relace: Odešle DisconnectMessage - Pokud zůstanou subsessions (podrelace): Žádná odpověď

**Důležité**: Chování Java I2P se odchyluje od specifikace. Implementace by měly být obezřetné při ukončování jednotlivých subsessions (podrelací).

#### DisconnectMessage (typ 30)

**Účel**: Oznámit, že spojení bude brzy ukončeno

**Obsah**: text důvodu

**Důsledek**: Všechny relace na spojení jsou ukončeny, socket se uzavře

**Implementace**: Převážně router → klient v Java I2P

## Historie verzí protokolu

### Detekce verze

Verze protokolu I2CP se vyměňuje ve zprávách Get/SetDate (od verze 0.8.7). U starších routerů nejsou informace o verzi k dispozici.

**Řetězec verze**: Udává verzi API „core“, nikoli nutně verzi routeru.

### Časová osa funkcí

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Features</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.67</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">PQ Hybrid ML-KEM (enc types 5-7) in LeaseSet</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.66</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Host lookup/reply extensions (proposal 167), service records</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.62</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">MessageStatus loopback error code</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.46</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">X25519 (enc type 4) in LeaseSet, ECIES end-to-end</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.43</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">BlindingInfo message, extended HostReply failure codes</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.41</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">EncryptedLeaseSet options, Meta LS error code</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.39</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">CreateLeaseSet2 message, RedDSA Ed25519 support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.38</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Preliminary LS2 support (format changed in 0.9.39)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.21</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Multiple sessions on single connection</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.20</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Additional SetDate messages for clock shifts</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.16</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Authentication required before other messages (when enabled)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.15</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA Ed25519 signature type</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.14</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Per-message reliability override with nonzero nonce</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.12</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA P-256/384/521 signature types, RSA support</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.11</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">HostLookup/HostReply messages, auth in GetDate</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.7</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">RequestVariableLeaseSet message</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.5</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Additional MessageStatus codes</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.4</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Fast receive mode default, nonce=0 allowed</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9.2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SendMessageExpires flag tag bits</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.9</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">16 leases per LeaseSet (up from 6)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.8.7</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Version strings in Get/SetDate</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.8.4</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SendMessageExpires flag bits</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.8.3</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DestLookup in standard session, concurrent lookups</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.8.1</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><code>messageReliability=none</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.7.2</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">GetBandwidthLimits, BandwidthLimits</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.7.1</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">SendMessageExpires, ReconfigureSession, ports in gzip header</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.7</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">DestLookup, DestReply</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>0.6.5-</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">Original protocol features</td>
    </tr>
  </tbody>
</table>
## Bezpečnostní hlediska

### Autentizace

**Výchozí**: Ověřování není vyžadováno **Volitelné**: Ověřování pomocí uživatelského jména a hesla (od 0.9.11) **Povinné**: Pokud je povoleno, ověřování se musí dokončit před ostatními zprávami (od 0.9.16)

**Vzdálená připojení**: Vždy používejte TLS (`i2cp.SSL=true`) k ochraně přihlašovacích údajů a soukromých klíčů.

### Časová odchylka

SessionConfig Date musí být v rozmezí ±30 sekund od času routeru, jinak bude relace odmítnuta. K synchronizaci použijte Get/SetDate.

### Zacházení se soukromými klíči

CreateLeaseSet2Message obsahuje soukromé klíče pro dešifrování příchozích zpráv. Tyto klíče musí být:
- Bezpečně přenášeny (TLS pro vzdálená připojení)
- Bezpečně ukládány routerem
- Vyměněny v případě kompromitace

### Vypršení platnosti zprávy

Vždy používejte SendMessageExpires (nikoli SendMessage) k nastavení explicitního vypršení platnosti. To:
- Zabrání tomu, aby byly zprávy zařazeny do fronty na neurčito
- Snižuje spotřebu prostředků
- Zvyšuje spolehlivost

### Správa značek relace

**ElGamal** (zastaralé): - Tagy musí být přenášeny po dávkách - Ztracené tagy způsobují selhání dešifrování - Vysoká paměťová režie

**ECIES-X25519** (aktuální): - Tagy generované synchronizovaným PRNG - Není nutný žádný předběžný přenos - Odolné vůči ztrátám zpráv - Výrazně nižší režie

## Osvědčené postupy

### Pro vývojáře klientských aplikací

1. **Použijte režim rychlého příjmu**: Vždy nastavte `i2cp.fastReceive=true` (nebo se spolehněte na výchozí nastavení)

2. **Upřednostněte ECIES-X25519**: Nastavte `i2cp.leaseSetEncType=4,0` pro nejlepší výkon při zachování kompatibility

3. **Nastavte explicitní expiraci**: Použijte SendMessageExpires, nikoli SendMessage

4. **Zacházejte se Subsessions (podrelacemi) opatrně**: Mějte na paměti, že subsessions neposkytují žádnou anonymitu mezi cíli

5. **Časový limit pro vytvoření relace**: Ukončit relaci, pokud není do 5 minut přijat RequestVariableLeaseSet

6. **Seřaďte konfigurační mapování**: Vždy seřaďte klíče mapování před podepsáním SessionConfig (konfigurace relace)

7. **Používejte vhodný počet Tunnel**: Nenastavujte `quantity` > 6, pokud to není nutné

8. **Zvažte SAM/BOB pro prostředí mimo Javu**: Implementujte raději SAM než přímo I2CP

### Pro vývojáře routeru

1. **Ověřit datumy**: Vynutit časové okno ±30 sekund u datumů v SessionConfig

2. **Omezení velikosti zprávy**: Vynutit maximální velikost zprávy ~64 KB

3. **Podpora více relací**: Implementovat podporu subsession (podrelace) podle specifikace 0.9.21

4. **Odešlete RequestVariableLeaseSet neprodleně**: Teprve poté, co existují jak příchozí, tak odchozí tunnels

5. **Ošetřete zastaralé zprávy**: Přijímejte, ale nedoporučujte používání ReceiveMessageBegin/End

6. **Podporujte ECIES-X25519**: Upřednostněte šifrování typu 4 pro nová nasazení

## Ladění a odstraňování problémů

### Časté problémy

**Relace odmítnuta (neplatná)**: - Zkontrolujte odchylku hodin (musí být v rozmezí ±30 sekund) - Ověřte, že mapování je seřazeno podle klíče - Ujistěte se, že Destinace není již používána

**No RequestVariableLeaseSet**: - Router může vytvářet tunnels (počkejte až 5 minut) - Zkontrolujte problémy s připojením k síti - Ověřte, že je k dispozici dostatečný počet připojení k uzlům

**Selhání doručení zpráv**: - Zkontrolujte kódy MessageStatus (stavové kódy zpráv) pro konkrétní důvod selhání - Ověřte, že vzdálený LeaseSet je zveřejněn a aktuální - Zajistěte kompatibilní typy šifrování

**Problémy s podrelacemi**: - Ověřte, že primární relace byla vytvořena jako první - Potvrďte, že šifrovací klíče jsou stejné - Zkontrolujte, zda jsou podpisové klíče odlišné

### Diagnostické zprávy

**GetBandwidthLimits**: Zjištění kapacity routeru **HostLookup**: Test rozlišení názvů a dostupnosti LeaseSetu (záznam o dostupnosti cíle v I2P) **MessageStatus**: Sledování doručování zpráv end-to-end

## Související specifikace

- **Společné struktury**: /docs/specs/common-structures/
- **I2NP (síťový protokol)**: /docs/specs/i2np/
- **ECIES-X25519**: /docs/specs/ecies/
- **Vytváření Tunnel**: /docs/specs/implementation/
- **Streamovací knihovna**: /docs/specs/streaming/
- **Datagramová knihovna**: /docs/api/datagrams/
- **SAM v3**: /docs/api/samv3/

## Citované návrhy

- [Návrh 123](/proposals/123-new-netdb-entries/): Šifrované LeaseSets a autentizace
- [Návrh 144](/proposals/144-ecies-x25519-aead-ratchet/): ECIES-X25519-AEAD-Ratchet
- [Návrh 149](/proposals/149-b32-encrypted-ls2/): Zaslepený formát adresy (b33)
- [Návrh 152](/proposals/152-ecies-tunnels/): Vytváření X25519 tunnelů
- [Návrh 154](/proposals/154-ecies-lookups/): Vyhledávání v databázi z ECIES destinací
- [Návrh 156](/proposals/156-ecies-routers/): Migrace routerů na ECIES-X25519
- [Návrh 161](/cs/proposals/161-ri-dest-padding/): Komprese paddingu destinace
- [Návrh 167](/proposals/167-service-records/): Záznamy služeb LeaseSet
- [Návrh 169](/proposals/169-pq-crypto/): Postkvantová hybridní kryptografie (ML-KEM)

## Referenční dokumentace Javadoc

- [Balíček I2CP](http://docs.i2p-projekt.de/javadoc/net/i2p/data/i2cp/package-summary.html)
- [MessageStatusMessage](http://docs.i2p-projekt.de/javadoc/net/i2p/data/i2cp/MessageStatusMessage.html)
- [Klientské API](http://docs.i2p-projekt.de/javadoc/net/i2p/client/package-summary.html)

## Shrnutí zastarání

### Zastaralé zprávy (nepoužívat)

- **CreateLeaseSetMessage** (typ 4): Použijte CreateLeaseSet2Message
- **RequestLeaseSetMessage** (typ 21): Použijte RequestVariableLeaseSetMessage
- **ReceiveMessageBeginMessage** (typ 6): Použijte rychlý režim příjmu
- **ReceiveMessageEndMessage** (typ 7): Použijte rychlý režim příjmu
- **DestLookupMessage** (typ 34): Použijte HostLookupMessage
- **DestReplyMessage** (typ 35): Použijte HostReplyMessage
- **ReportAbuseMessage** (typ 29): Nikdy nebylo implementováno

### Zastaralé volby

- Šifrování ElGamalem (typ 0): Přejděte na ECIES-X25519 (typ 4)
- Podpisy DSA: Přejděte na EdDSA nebo ECDSA
- `i2cp.fastReceive=false`: Vždy používejte režim rychlého příjmu
