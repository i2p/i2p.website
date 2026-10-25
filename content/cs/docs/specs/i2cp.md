---
title: "I2P Client Protocol (I2CP)"
description: "Jak aplikace vyjednávají relace, tunely a LeaseSets s I2P routerem."
slug: "i2cp"
aliases:
  - "/cs/docs/api/i2cp"
  - "/cs/docs/api/i2cp/"
  - "/cs/docs/specs/i2cp-spec"
  - "/cs/docs/specs/i2cp-spec/"
  - "/cs/i2cp_spec"
  - "/cs/i2cp_spec/"
category: "Protokoly"
lastUpdated: "2025-07"
accurateFor: "0.9.67"
---

## Přehled

Toto je specifikace I2P Control Protocol (I2CP), nízkoúrovňového rozhraní mezi klienty a routerem. Java klienti budou používat I2CP klientské API, které implementuje tento protokol.

Neexistují žádné známé implementace klientské knihovny pro I2CP mimo Javu. Navíc aplikace orientované na sockety (streaming) by potřebovaly implementaci streaming protokolu, ale ani pro ten neexistují knihovny mimo Javu. Proto by klienti mimo Javu měli místo toho používat protokol vyšší vrstvy SAM [SAMv3](/docs/api/samv3/), pro který existují knihovny v několika jazycích.

Jedná se o nízkoúrovňový protokol podporovaný jak interně, tak externě Java I2P routerem. Protokol je serializován pouze v případě, že klient a router nejsou ve stejném JVM; jinak jsou I2CP zprávy jako Java objekty předávány přes interní JVM rozhraní. I2CP je také externě podporován C++ routerem i2pd.

Více informací najdete na stránce Přehled I2CP [I2CP](/docs/specs/i2cp/).

## Relace

Protokol byl navržen pro zpracování více "sessions" (relací), každá s 2-bytovým ID session, přes jediné TCP spojení, nicméně více sessions nebylo implementováno až do verze 0.9.21. Viz [sekce multisession níže](#multisession). Nepokoušejte se používat více sessions na jediném I2CP spojení s routery staršími než verze 0.9.21.

Zdá se také, že existují některá ustanovení pro jediného klienta, aby komunikoval s více routery přes samostatná připojení. Toto je také netestované a pravděpodobně neužitečné.

Neexistuje způsob, jak udržet relaci po odpojení nebo ji obnovit na jiném I2CP připojení. Když je socket uzavřen, relace je zničena.

## Příklady sekvencí zpráv

Poznámka: Příklady níže neukazují Protocol Byte (0x2a), který musí být odeslán z klienta do routeru při prvním připojení. Více informací o inicializaci připojení najdete na stránce I2CP Overview [I2CP](/docs/specs/i2cp/).

### Standardní ustanovení relace

```
  Client                                           Router

                           --------------------->  Get Date Message
        Set Date Message  <---------------------
                           --------------------->  Create Session Message
  Session Status Message  <---------------------
Request LeaseSet Message  <---------------------
                           --------------------->  Create LeaseSet Message

```
### Získat limity šířky pásma (jednoduchá relace)

```
  Client                                           Router

                           --------------------->  Get Bandwidth Limits Message
Bandwidth Limits Message  <---------------------

```
### Vyhledání cíle (jednoduchá relace)

```
  Client                                           Router

                           --------------------->  Dest Lookup Message
      Dest Reply Message  <---------------------

```
### Odchozí zpráva

Existující relace, s i2cp.messageReliability=none

```
  Client                                           Router

                           --------------------->  Send Message Message

```
Existující relace s i2cp.messageReliability=none a nenulovým nonce

```
  Client                                           Router

                           --------------------->  Send Message Message
  Message Status Message  <---------------------
  (succeeded)

```
Existující relace, s i2cp.messageReliability=BestEffort

```
  Client                                           Router

                           --------------------->  Send Message Message
  Message Status Message  <---------------------
  (accepted)
  Message Status Message  <---------------------
  (succeeded)

```
### Příchozí zpráva

Existující relace, s i2cp.fastReceive=true (od verze 0.9.4)

```
  Client                                           Router

 Message Payload Message  <---------------------

```
Existující relace, s i2cp.fastReceive=false (ZASTARALÉ)

```
  Client                                           Router

  Message Status Message  <---------------------
  (available)
                           --------------------->  Receive Message Begin Message
 Message Payload Message  <---------------------
                           --------------------->  Receive Message End Message

```
### Poznámky k více relacím {#multisession}

Více relací na jednom I2CP připojení je podporováno od verze routeru 0.9.21. První relace, která je vytvořena, je "primární relace". Další relace jsou "podrelace". Podrelace se používají k podpoře více destinací sdílejících společnou sadu tunelů. Počáteční aplikace je pro primární relaci použít ECDSA podpisové klíče, zatímco podrelace používá DSA podpisové klíče pro komunikaci se starými eepsites.

Subsessions sdílejí stejné fondy příchozích a odchozích tunelů jako primární relace. Subsessions musí používat stejné šifrovací klíče jako primární relace. To platí jak pro šifrovací klíče leaseSet, tak pro (nepoužívané) šifrovací klíče Destination. Subsessions musí používat různé podepisovací klíče v destinaci, takže hash destinace se liší od primární relace. Protože subsessions používají stejné šifrovací klíče a tunely jako primární relace, je všem zřejmé, že Destinations běží na stejném routeru, takže obvyklé záruky anonymity proti korelaci neplatí.

Subsessions jsou vytvořeny odesláním zprávy CreateSession a přijetím odpovědní zprávy SessionStatus, jako obvykle. Subsessions musí být vytvořeny až po vytvoření primární session. Odpověď SessionStatus bude při úspěchu obsahovat jedinečné Session ID, odlišné od ID primární session. Zatímco zprávy CreateSession by měly být zpracovány v pořadí, neexistuje spolehlivý způsob, jak korelovat zprávu CreateSession s odpovědí, takže klient by neměl mít současně více nevyřízených zpráv CreateSession. Možnosti SessionConfig pro subsession nemusí být respektovány tam, kde se liší od primární session. Zejména, protože subsessions používají stejný tunnel pool jako primární session, možnosti tunnel mohou být ignorovány.

Router pošle klientovi samostatné zprávy RequestVariableLeaseSet pro každou Destination a klient musí odpovědět zprávou CreateLeaseSet pro každou z nich. Leases pro tyto dvě Destinations nebudou nutně identické, i když jsou vybrány ze stejného tunnel poolu.

Subsession může být zničena pomocí zprávy DestroySession jako obvykle. Toto nezničí primární session ani nezastaví I2CP spojení. Zničení primární session však zničí všechny subsessions a zastaví I2CP spojení. Zpráva Disconnect ničí všechny sessions.

Poznamenejte si, že většina, ale ne všechny, I2CP zprávy obsahují Session ID. Pro ty, které ho neobsahují, mohou klienti potřebovat dodatečnou logiku pro správné zpracování odpovědí routeru. DestLookup a DestReply neobsahují Session ID; použijte místo toho novější HostLookup a HostReply. GetBandwidthLimts a BandwidthLimits neobsahují session ID, nicméně odpověď není specifická pro session.

### Poznámky k verzi {#notes}

Počáteční bajt verze protokolu (0x2a) odesílaný klientem se pravděpodobně nezmění. Před vydáním verze 0.8.7 nebyly informace o verzi routeru dostupné klientovi, což bránilo novým klientům ve spolupráci se starými routery. Od vydání verze 0.8.7 se řetězce verzí protokolu obou stran vyměňují ve zprávách Get/Set Date Messages. Do budoucna mohou klienti tyto informace použít ke správné komunikaci se starými routery. Klienti a routery by neměly odesílat zprávy, které druhá strana nepodporuje, protože obecně odpojují relaci po obdržení nepodporované zprávy.

Vyměněné informace o verzi jsou "základní" verze API nebo verze I2CP protokolu a nemusí nutně odpovídat verzi routeru.

Základní shrnutí verzí I2CP protokolu je následující. Podrobnosti viz níže.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Version</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Required I2CP Features</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.67</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">PQ Hybrid ML-KEM (enc types 5-7) supported in LS</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Host lookup/reply extensions (see proposal 167)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.62</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">MessageStatus message Loopback error code</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.46</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">X25519 (enc type 4) supported in LS</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.43</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">BlindingInfo message supported; Additional HostReply message failure codes</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">EncryptedLeaseSet options; MessageStatus message Meta LS error code</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.39</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">CreateLeaseSet2 message and options supported; Dest/LS key certs w/ RedDSA Ed25519 sig type supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Preliminary CreateLeaseSet2 message supported (abandoned)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.21</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Multiple sessions on a single I2CP connection supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.20</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Additional SetDate messages may be sent to the client at any time</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.16</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Authentication, if enabled, is required via GetDate before all other messages</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.15</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest/LS key certs w/ EdDSA Ed25519 sig type supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.14</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Per-message override of messageReliability=none with nonzero nonce</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest/LS key certs w/ ECDSA P-256, P-384, and P-521 sig types supported; RSA sig types also supported but currently unused</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Host Lookup and Host Reply messages supported; Authentication mapping in Get Date message supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Request Variable Lease Set message supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Additional Message Status codes defined</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Send Message nonce=0 allowed; Fast receive mode is the default</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Send Message Expires flag tag bits supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Supports up to 16 leases in a lease set (6 previously)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Get Date and Set Date version strings included. If not present, the client or router is version 0.8.6 or older.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Send Message Expires flag bits supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest Lookup and Get Bandwidth messages supported in standard session; Concurrent Dest Lookup messages supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.messageReliability=none supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Get Bandwidth Limits and Bandwidth Limits messages supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Send Message Expires message supported; Reconfigure Session message supported; Ports and protocol numbers in gzip header</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest Lookup and Dest Reply messages supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.6.5 or lower</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">All messages and features not listed above</td>
</tr>
</table>
## Běžné struktury {#structures}

### Hlavička I2CP zprávy {#struct-I2CPMessageHeader}

#### Popis

Společná hlavička pro všechny I2CP zprávy, obsahující délku zprávy a typ zprávy.

#### Obsah

1.  4 bajtový [Integer](/docs/specs/common-structures/#integer) specifikující délku
    těla zprávy
2.  1 bajtový [Integer](/docs/specs/common-structures/#integer) specifikující typ
    zprávy.
3.  Tělo I2CP zprávy, 0 nebo více bajtů

#### Poznámky

Skutečný limit délky zprávy je přibližně 64 KB.

### ID zprávy {#struct-MessageId}

#### Popis

Jednoznačně identifikuje zprávu čekající na konkrétním routeru v daném okamžiku. Toto je vždy generováno routerem a NENÍ totéž jako nonce generovaný klientem.

#### Obsah

1.  4 byte [Integer](/docs/specs/common-structures/#integer)

#### Poznámky

ID zpráv jsou jedinečné pouze v rámci relace; nejsou globálně jedinečné.

### Payload {#struct-Payload}

#### Popis

Tato struktura je obsahem zprávy doručované z jedné Destination do druhé.

#### Obsah

1.  4 bajtový [Integer](/docs/specs/common-structures/#integer) délka
2.  Tolik bajtů

#### Poznámky

Datová část je ve formátu gzip jak je specifikováno na stránce I2CP Overview [I2CP-FORMAT](/docs/specs/i2cp/#format).

Skutečný limit délky zprávy je asi 64 KB.

### Konfigurace relace {#struct-SessionConfig}

#### Popis

Definuje konfigurační možnosti pro konkrétní klientskou relaci.

#### Obsah

1.  [Destination](/docs/specs/common-structures/#destination)
2.  [Mapping](/docs/specs/common-structures/#mapping) možností
3.  Datum vytvoření [Date](/docs/specs/common-structures/#date)
4.  [Signature](/docs/specs/common-structures/#signature) předchozích 3 polí,
    podepsaný pomocí [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey)

#### Poznámky

- Možnosti jsou specifikovány na stránce I2CP Overview
  [I2CP-OPTIONS](/docs/specs/i2cp/#options).
- [Mapping](/docs/specs/common-structures/#mapping) musí být seřazeno podle klíče, aby
  byl podpis v routeru správně validován.
- Datum vytvoření musí být v rozmezí +/- 30 sekund od aktuálního času
  při zpracování routerem, jinak bude konfigurace odmítnuta.

#### Offline podpisy

- Pokud je [Destination](/docs/specs/common-structures/#destination) offline podepsaná,
  [Mapping](/docs/specs/common-structures/#mapping) musí obsahovat tři možnosti
  i2cp.leaseSetOfflineExpiration, i2cp.leaseSetTransientPublicKey a
  i2cp.leaseSetOfflineSignature. 
  [Signature](/docs/specs/common-structures/#signature) je pak generována dočasným
  [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey) a
  je ověřována pomocí [SigningPublicKey](/docs/specs/common-structures/#signingpublickey)
  specifikovaného v i2cp.leaseSetTransientPublicKey. Podrobnosti viz
  [I2CP-OPTIONS](/docs/specs/i2cp/#options).

### Session ID {#struct-SessionId}

#### Popis

Jedinečně identifikuje relaci na konkrétním router v daném okamžiku.

#### Obsah

1.  2 byte [Integer](/docs/specs/common-structures/#integer)

#### Poznámky

Session ID 0xffff se používá k označení "žádné session", například pro vyhledávání názvů hostů.

## Zprávy

Viz také [I2CP Javadocs](http://javadoc.i2p.net/net/i2p/data/i2cp/package-summary.html).

### Typy zpráv {#types}

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Message</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Direction</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Since</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#BandwidthLimitsMessage">BandwidthLimitsMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">23</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.2</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#BlindingInfoMessage">BlindingInfoMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">42</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.43</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#CreateLeaseSetMessage">CreateLeaseSetMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#CreateLeaseSet2Message">CreateLeaseSet2Message</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.39</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#CreateSessionMessage">CreateSessionMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#DestLookupMessage">DestLookupMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">34</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#DestReplyMessage">DestReplyMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">35</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#DestroySessionMessage">DestroySessionMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#DisconnectMessage">DisconnectMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">bidir.</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">30</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#GetBandwidthLimitsMessage">GetBandwidthLimitsMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">8</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.2</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#GetDateMessage">GetDateMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#HostLookupMessage">HostLookupMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.11</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#HostReplyMessage">HostReplyMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">39</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.11</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#MessagePayloadMessage">MessagePayloadMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">31</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#MessageStatusMessage">MessageStatusMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">22</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#ReceiveMessageBeginMessage">ReceiveMessageBeginMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#ReceiveMessageEndMessage">ReceiveMessageEndMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#ReconfigureSessionMessage">ReconfigureSessionMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#ReportAbuseMessage">ReportAbuseMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">bidir.</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">29</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#RequestLeaseSetMessage">RequestLeaseSetMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">21</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#RequestVariableLeaseSetMessage">RequestVariableLeaseSetMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">37</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#SendMessageMessage">SendMessageMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#SendMessageExpiresMessage">SendMessageExpiresMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">36</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#SessionStatusMessage">SessionStatusMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">20</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#SetDateMessage">SetDateMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">33</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
</table>
### BandwidthLimitsMessage {#BandwidthLimitsMessage}

#### Popis

Informuj klienta o omezeních šířky pásma.

Odesláno z Router do Client jako odpověď na [GetBandwidthLimitsMessage](#GetBandwidthLimitsMessage).

#### Obsah

1.  4 byte [Integer](/docs/specs/common-structures/#integer) Limit příchozích dat klienta
    (KBps)
2.  4 byte [Integer](/docs/specs/common-structures/#integer) Limit odchozích dat klienta
    (KBps)
3.  4 byte [Integer](/docs/specs/common-structures/#integer) Limit příchozích dat router
    (KBps)
4.  4 byte [Integer](/docs/specs/common-structures/#integer) Burst limit příchozích dat router
    (KBps)
5.  4 byte [Integer](/docs/specs/common-structures/#integer) Limit odchozích dat router
    (KBps)
6.  4 byte [Integer](/docs/specs/common-structures/#integer) Burst limit odchozích dat router
    (KBps)
7.  4 byte [Integer](/docs/specs/common-structures/#integer) Burst čas router
    (sekundy)
8.  Devět 4-byte [Integer](/docs/specs/common-structures/#integer) (nedefinováno)

#### Poznámky

Limity klienta mohou být jediné nastavené hodnoty a mohou představovat skutečné limity routeru, nebo procento z limitů routeru, nebo být specifické pro konkrétního klienta, což závisí na implementaci. Všechny hodnoty označené jako limity routeru mohou být 0, což závisí na implementaci. Od vydání 0.7.2.

### BlindingInfoMessage {#BlindingInfoMessage}

#### Popis

Informuje router, že Destination je blinded (zastíněná), s volitelným heslem pro vyhledávání a volitelným soukromým klíčem pro dešifrování. Podrobnosti naleznete v návrzích 123 a 149.

Router potřebuje vědět, zda je cíl zaslepený. Pokud je zaslepený a používá tajné nebo per-client ověřování, potřebuje mít také tyto informace.

Host Lookup nové b32 adresy formátu ("b33") říká routeru, že adresa je zaslepená, ale neexistuje mechanismus pro předání tajného nebo soukromého klíče routeru ve zprávě Host Lookup. Ačkoli bychom mohli rozšířit zprávu Host Lookup o tyto informace, je čistší definovat novou zprávu.

Tato zpráva poskytuje programový způsob, jak může klient informovat router. Jinak by uživatel musel manuálně konfigurovat každou destinaci.

#### Použití

Před tím, než klient odešle zprávu do blinded destination (skryté cílové adresy), musí buď vyhledat "b33" ve zprávě Host Lookup, nebo odeslat zprávu Blinding Info. Pokud blinded destination vyžaduje tajný klíč nebo autentifikaci podle klienta, musí klient odeslat zprávu Blinding Info.

Router neposílá odpověď na tuto zprávu. Odesílá se z klienta do routeru.

#### Obsah

1.  [Session ID](#struct-sessionid)
2.  1 byte [Integer](/docs/specs/common-structures/#integer) Flags

> - Pořadí bitů: 76543210 > - Bit 0: 0 pro všechny, 1 pro jednotlivé klienty > - Bity 3-1: Schéma autentifikace, pokud je bit 0 nastaven na 1 pro >   jednotlivé klienty, jinak 000 >   - 000: DH autentifikace klienta (nebo žádná autentifikace jednotlivých klientů) >   - 001: PSK autentifikace klienta > - Bit 4: 1 pokud je vyžadováno tajemství, 0 pokud není vyžadováno tajemství > - Bity 7-5: Nepoužívané, nastavte na 0 pro budoucí kompatibilitu

3.  1 byte [Integer](/docs/specs/common-structures/#integer) Typ koncového bodu

> - Typ 0 je [Hash](/docs/specs/common-structures/#hash) > - Typ 1 je hostname [String](/docs/specs/common-structures/#string) > - Typ 2 je [Destination](/docs/specs/common-structures/#destination) > - Typ 3 je Sig Type a >   [SigningPublicKey](/docs/specs/common-structures/#signingpublickey)

4.  2 byte [Integer](/docs/specs/common-structures/#integer) Blinded Signature Type
5.  4 byte [Integer](/docs/specs/common-structures/#integer) Expiration Sekundy od
    epochy
6.  Endpoint: Data podle specifikace, jeden z

> - Typ 0: 32 bytový [Hash](/docs/specs/common-structures/#hash) > > - Typ 1: název hostitele [String](/docs/specs/common-structures/#string) > > - Typ 2: binární [Destination](/docs/specs/common-structures/#destination) > >  > >  - Typ 3: 2 bytový [Integer](/docs/specs/common-structures/#integer) typ podpisu, následovaný > >  -   [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) (délka podle >       typu podpisu)

7.  [PrivateKey](/docs/specs/common-structures/#privatekey) Dešifrovací klíč Přítomen pouze
    pokud je flag bit 0 nastaven na 1. 32-bajtový ECIES_X25519 privátní klíč,
    little-endian
8.  [String](/docs/specs/common-structures/#string) Heslo pro vyhledávání Přítomen pouze pokud
    je flag bit 4 nastaven na 1.

#### Poznámky

- Od verze 0.9.43.
- Typ koncového bodu Hash pravděpodobně není užitečný, pokud router nemůže provést zpětné vyhledání v adresáři pro získání Destination.
- Typ koncového bodu hostname pravděpodobně není užitečný, pokud router nemůže provést vyhledání v adresáři pro získání Destination.

### CreateLeaseSetMessage {#CreateLeaseSetMessage}

ZASTARALÉ. Nelze použít pro LeaseSet2, offline klíče, jiné typy šifrování než ElGamal, více typů šifrování nebo šifrované LeaseSets. Použijte CreateLeaseSet2Message se všemi routery verze 0.9.39 nebo vyšší.

#### Popis

Tato zpráva je odeslána v odpovědi na [RequestLeaseSetMessage](#RequestLeaseSetMessage) nebo [RequestVariableLeaseSetMessage](#RequestVariableLeaseSetMessage) a obsahuje všechny struktury [Lease](/docs/specs/common-structures/#lease), které by měly být publikovány do I2NP Network Database.

Odesláno z klienta do routeru.

#### Obsah

1.  [Session ID](#struct-sessionid)
2.  DSA [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey) nebo 20
    bajtů ignorováno
3.  [PrivateKey](/docs/specs/common-structures/#privatekey)
4.  [LeaseSet](/docs/specs/common-structures/#leaseset)

#### Poznámky

SigningPrivateKey odpovídá [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) z LeaseSet pouze tehdy, pokud je typ podpisového klíče DSA. Toto slouží pro odvolání LeaseSet, které není implementováno a pravděpodobně nikdy implementováno nebude. Pokud typ podpisového klíče není DSA, toto pole obsahuje 20 bytů náhodných dat. Délka tohoto pole je vždy 20 bytů, nikdy se nerovná délce ne-DSA podpisového soukromého klíče.

PrivateKey odpovídá [PublicKey](/docs/specs/common-structures/#publickey) z LeaseSet. PrivateKey je nezbytný pro dešifrování zpráv směrovaných pomocí garlic encryption.

Odvolání není implementováno. Připojení k více routerům není implementováno v žádné klientské knihovně.

### CreateLeaseSet2Message {#CreateLeaseSet2Message}

#### Popis

Tato zpráva je odeslána jako odpověď na [RequestLeaseSetMessage](#RequestLeaseSetMessage) nebo [RequestVariableLeaseSetMessage](#RequestVariableLeaseSetMessage) a obsahuje všechny struktury [Lease](/docs/specs/common-structures/#lease), které by měly být publikovány do I2NP Network Database.

Odesláno z klienta do routeru. Od verze 0.9.39. Autentizace per-klient pro EncryptedLeaseSet je podporována od verze 0.9.41. MetaLeaseSet zatím není podporován přes I2CP. Viz návrh 123 pro více informací.

#### Obsah

1.  [Session ID](#struct-sessionid)
2.  Jeden bajt typu lease set, který následuje.

> - Typ 1 je [LeaseSet](/docs/specs/common-structures/#leaseset) (zastaralý) > - Typ 3 je [LeaseSet2](/docs/specs/common-structures/#leaseset2) > - Typ 5 je [EncryptedLeaseSet](/docs/specs/common-structures/#leaseset2) > - Typ 7 je [MetaLeaseSet](/docs/specs/common-structures/#leaseset2)

3.  [LeaseSet](/docs/specs/common-structures/#leaseset) nebo
    [LeaseSet2](/docs/specs/common-structures/#leaseset2) nebo
    [EncryptedLeaseSet](/docs/specs/common-structures/#leaseset2) nebo
    [MetaLeaseSet](/docs/specs/common-structures/#leaseset2)
4.  Jeden byte číslo privátních klíčů následujících.
5.  Seznam [PrivateKey](/docs/specs/common-structures/#privatekey). Jeden pro každý veřejný
    klíč v lease setu, ve stejném pořadí. (Není přítomno pro Meta LS2)

> - Typ šifrování (2 bajtový [Integer](/docs/specs/common-structures/#integer)) > - Délka šifrovacího klíče (2 bajtový [Integer](/docs/specs/common-structures/#integer)) > - Šifrovací [PrivateKey](/docs/specs/common-structures/#privatekey) (počet bajtů >   specifikovaný)

#### Poznámky

PrivateKeys odpovídají každému z [PublicKey](/docs/specs/common-structures/#publickey) z LeaseSet. PrivateKeys jsou nezbytné pro dešifrování zpráv směrovaných pomocí garlic encryption.

Více informací o šifrovaných leaseSetech naleznete v návrhu 123.

Obsah a formát pro MetaLeaseSet jsou předběžné a mohou se změnit. Neexistuje žádný protokol specifikovaný pro správu více routerů. Více informací naleznete v návrhu 123.

Soukromý klíč pro podepisování, dříve definovaný pro zrušení a nepoužitý, není v LS2 přítomen.

Předběžná verze s typem zprávy 40 byla v 0.9.38, ale formát byl změněn. Typ 40 je opuštěn a není podporován. Typ 41 není platný do verze 0.9.39.

### CreateSessionMessage {#CreateSessionMessage}

#### Popis

Tato zpráva je odeslána z klienta pro zahájení relace, kde relace je definována jako připojení jednoho Destination k síti, do kterého budou doručeny všechny zprávy pro tento Destination a přes které budou odesílány všechny zprávy, které tento Destination posílá jakémukoliv jinému Destination.

Odesláno z klienta do routeru. Router odpovídá zprávou [SessionStatusMessage](#SessionStatusMessage).

#### Obsah

1.  [Konfigurace relace](#struct-sessionconfig)

#### Poznámky

- Toto je druhá zpráva odeslaná klientem. Dříve klient
  odeslal [GetDateMessage](#GetDateMessage) a obdržel
  odpověď [SetDateMessage](#SetDateMessage).
- Pokud je Datum v Session Config příliš vzdálené (více než +/- 30
  sekund) od aktuálního času routeru, bude session odmítnuta.
- Pokud již existuje session na routeru pro tuto Destination,
  bude session odmítnuta.
- [Mapping](/docs/specs/common-structures/#mapping) v Session Config musí být
  seřazen podle klíče, aby mohl být podpis správně ověřen v
  routeru.

### DestLookupMessage {#DestLookupMessage}

#### Popis

Odesláno z Klienta do Routeru. Router odpovídá zprávou [DestReplyMessage](#DestReplyMessage).

#### Obsah

1.  SHA-256 [Hash](/docs/specs/common-structures/#hash)

#### Poznámky

Od verze 0.7.

Od verze 0.8.3 jsou podporovány vícenásobné probíhající vyhledávání a vyhledávání je podporováno jak v I2PSimpleSession, tak ve standardních relacích.

[HostLookupMessage](#HostLookupMessage) je preferována od verze 0.9.11.

### DestReplyMessage {#DestReplyMessage}

#### Popis

Odesláno z routeru klientovi jako odpověď na [DestLookupMessage](#DestLookupMessage).

#### Obsah

1.  [Destination](/docs/specs/common-structures/#destination) při úspěchu, nebo
    [Hash](/docs/specs/common-structures/#hash) při selhání

#### Poznámky

Od verze 0.7.

Od verze 0.8.3 je požadovaný Hash vrácen, pokud vyhledávání selhalo, takže klient může mít více vyhledávání probíhajících současně a korelovat odpovědi s vyhledáváními. Pro korelaci odpovědi Destination s požadavkem vezměte Hash Destination. Před verzí 0.8.3 byla odpověď při selhání prázdná.

### DestroySessionMessage {#DestroySessionMessage}

#### Popis

Tato zpráva je odeslána z klienta pro zrušení relace.

Odesláno z klienta na router. Router by měl odpovědět zprávou [SessionStatusMessage](#SessionStatusMessage) (Destroyed). Viz však důležité poznámky níže.

#### Obsah

1.  [ID relace](#struct-sessionid)

#### Poznámky

Router by v tomto okamžiku měl uvolnit všechny prostředky související se session.

Až do API 0.9.66 se Java I2P router a klientské knihovny podstatně odchylují od této specifikace. Router nikdy neodesílá odpověď SessionStatus(Destroyed). Pokud nezůstaly žádné relace, odešle [DisconnectMessage](#DisconnectMessage). Pokud existují podrelace nebo zůstává primární relace, neodpovídá.

Java klientská knihovna reaguje na zprávu SessionStatus zrušením všech relací a opětovným připojením.

Rušení jednotlivých podsezení na připojení s více sezeními nemusí být plně otestováno nebo funkční v různých implementacích routerů a klientů. Postupujte opatrně.

Implementace by měly zacházet s příkazem destroy pro primární relaci jako s příkazem destroy pro všechny podrelace, ale umožnit destroy pro jednu podrelaci a udržet spojení otevřené, Java I2P to však nyní nedělá. Pokud bude chování Java I2P v následujících verzích změněno, bude to zde zdokumentováno.

### DisconnectMessage {#DisconnectMessage}

#### Popis

Oznámí druhé straně, že existují problémy a současné spojení bude ukončeno. Tím se ukončí všechny relace na tomto spojení. Socket bude brzy uzavřen. Odesíláno buď z routeru ke klientovi nebo z klienta k routeru.

#### Obsah

1.  Důvod [String](/docs/specs/common-structures/#string)

#### Poznámky

Implementováno pouze ve směru router-to-client, alespoň v Java I2P.

### GetBandwidthLimitsMessage {#GetBandwidthLimitsMessage}

#### Popis

Požádejte router, aby sdělil, jaké jsou jeho aktuální omezení šířky pásma.

Odesláno z Klienta do Routeru. Router odpovídá s [BandwidthLimitsMessage](#BandwidthLimitsMessage).

#### Obsah

*Žádné*

#### Poznámky

Od verze 0.7.2.

Od verze 0.8.3 je podporováno jak v I2PSimpleSession, tak ve standardních relacích.

### GetDateMessage {#GetDateMessage}

#### Popis

Odesláno z klienta do routeru. Router odpoví zprávou [SetDateMessage](#SetDateMessage).

#### Obsah

1.  Verze I2CP API [String](/docs/specs/common-structures/#string)
2.  Ověřování [Mapping](/docs/specs/common-structures/#mapping) (volitelné, od
    vydání 0.9.11)

#### Poznámky

- Obecně první zpráva odeslaná klientem po odeslání
  bajtu verze protokolu.
- Řetězec verze je zahrnut od vydání 0.8.7. To je užitečné
  pouze pokud klient a router nejsou ve stejném JVM. Pokud není
  přítomen, klient je verze 0.8.6 nebo starší.
- Od vydání 0.9.11 může být zahrnuto autentifikační
  [Mapping](/docs/specs/common-structures/#mapping) s klíči
  i2cp.username a i2cp.password. Mapping nemusí být seřazeno, protože
  tato zpráva není podepsaná. Před verzí 0.9.10 včetně
  je autentifikace zahrnuta v [Session Config](#struct-sessionconfig)
  Mapping a žádná autentifikace není vynucována pro
  [GetDateMessage](#GetDateMessage),
  [GetBandwidthLimitsMessage](#GetBandwidthLimitsMessage) nebo
  [DestLookupMessage](#DestLookupMessage). Pokud je povolena, je od vydání 0.9.16 vyžadována autentifikace
  prostřednictvím [GetDateMessage](#GetDateMessage) před jakýmikoli jinými
  zprávami. To je užitečné pouze mimo kontext routeru. Jedná se o nekompatibilní změnu, ale ovlivní pouze relace
  mimo kontext routeru s autentifikací, což by mělo být vzácné.

### HostLookupMessage {#HostLookupMessage}

#### Popis

Odesláno z klienta do routeru. Router odpovídá zprávou [HostReplyMessage](#HostReplyMessage).

Toto nahrazuje [DestLookupMessage](#DestLookupMessage) a přidává ID požadavku, timeout a podporu pro vyhledávání názvů hostitelů. Jelikož také podporuje Hash vyhledávání, může být použito pro všechna vyhledávání, pokud to router podporuje. Pro vyhledávání názvů hostitelů bude router dotazovat naming service svého kontextu. To je užitečné pouze pokud je klient mimo kontext routeru. Uvnitř kontextu routeru by měl klient dotazovat naming service přímo, což je mnohem efektivnější.

#### Obsah

1.  [Session ID](#struct-sessionid)
2.  4 byte [Integer](/docs/specs/common-structures/#integer) ID požadavku
3.  4 byte [Integer](/docs/specs/common-structures/#integer) timeout (ms)
4.  1 byte [Integer](/docs/specs/common-structures/#integer) typ požadavku
5.  SHA-256 [Hash](/docs/specs/common-structures/#hash) nebo název hostitele
    [String](/docs/specs/common-structures/#string) nebo
    [Destination](/docs/specs/common-structures/#destination)

Typy požadavků:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Lookup key (item 5)</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">As of</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Hash</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">host name String</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Hash</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">host name String</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Destination</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
</tr>
</table>
Typy 2-4 požadují, aby bylo mapování možností z LeaseSet vráceno ve zprávě HostReply. Viz návrh 167.

#### Poznámky

- Od vydání 0.9.11. Pro starší routery použijte [DestLookupMessage](#DestLookupMessage).
- ID relace a ID požadavku budou vráceny v [HostReplyMessage](#HostReplyMessage). Pokud neexistuje relace, použijte pro ID relace hodnotu 0xFFFF.
- Timeout je užitečný pro vyhledávání Hash. Doporučené minimum je 10 000 (10 sekund). V budoucnu může být také užitečné pro vzdálené vyhledávání v názvových službách. Hodnota nemusí být respektována pro vyhledávání místních názvů hostitelů, které by mělo být rychlé.
- Vyhledávání názvu hostitele v Base 32 je podporováno, ale je preferováno jej nejprve převést na Hash.

### HostReplyMessage {#HostReplyMessage}

#### Popis

Odesláno z router do klienta v reakci na [HostLookupMessage](#HostLookupMessage).

#### Obsah

1.  [Session ID](#struct-sessionid)
2.  4 byte [Integer](/docs/specs/common-structures/#integer) ID požadavku
3.  1 byte [Integer](/docs/specs/common-structures/#integer) kód výsledku

> - 0: Úspěch > - 1: Neúspěch > - 2: Vyžadováno heslo pro vyhledávání (od verze 0.9.43) > - 3: Vyžadován privátní klíč (od verze 0.9.43) > - 4: Vyžadováno heslo pro vyhledávání a privátní klíč (od verze 0.9.43) > - 5: Neúspěšné dešifrování leaseSetu (od verze 0.9.43) > - 6: Neúspěšné vyhledávání leaseSetu (od verze 0.9.66) > - 7: Nepodporovaný typ vyhledávání (od verze 0.9.66)

4.  [Destination](/docs/specs/common-structures/#destination), přítomen pouze pokud je kód výsledku nula, s výjimkou případů kdy může být také vrácen pro typy vyhledávání 2-4. Viz níže.
5.  [Mapping](/docs/specs/common-structures/#mapping), přítomen pouze pokud je kód výsledku nula, vrácen pouze pro typy vyhledávání 2-4. Od verze 0.9.66. Viz níže.

#### Odpovědi pro typy vyhledávání 2-4

Proposal 167 definuje další typy vyhledávání, které vrací všechny možnosti z leaseset, pokud jsou k dispozici. Pro typy vyhledávání 2-4 musí router načíst leaseset, i když je vyhledávací klíč v adresáři.

Pokud je operace úspěšná, HostReply bude obsahovat options Mapping z leaseset a zahrne jej jako položku 5 po destination. Pokud v Mapping nejsou žádné options, nebo byl leaseset verze 1, bude stále zahrnut jako prázdný Mapping (dva bajty: 0 0). Všechny options z leaseset budou zahrnuty, nejen options pro service record. Například mohou být přítomny options pro parametry definované v budoucnu. Vrácený Mapping může nebo nemusí být seřazen, závisí na implementaci.

Při selhání vyhledání leaseset bude odpověď obsahovat nový kód chyby 6 (Selhání vyhledání leaseset) a nebude zahrnovat mapování. Když je vrácen kód chyby 6, pole Destination může nebo nemusí být přítomno. Bude přítomno, pokud bylo vyhledání hostname v adresáři úspěšné, nebo pokud bylo předchozí vyhledání úspěšné a výsledek byl uložen do cache, nebo pokud bylo Destination přítomno ve vyhledávací zprávě (typ vyhledání 4).

Pokud typ vyhledávání není podporován, odpověď bude obsahovat nový kód chyby 7 (typ vyhledávání není podporován).

#### Poznámky

- Od vydání 0.9.11. Viz poznámky k [HostLookupMessage](#HostLookupMessage).
- ID relace a ID požadavku jsou ty z [HostLookupMessage](#HostLookupMessage).
- Kód výsledku je 0 pro úspěch, 1-255 pro neúspěch. 1 označuje obecný neúspěch. Od verze 0.9.43 byly definovány dodatečné kódy neúspěchu 2-5 pro podporu rozšířených chyb pro vyhledávání "b33". Viz návrhy 123 a 149 pro další informace. Od verze 0.9.66 byly definovány dodatečné kódy neúspěchu 6-7 pro podporu rozšířených chyb pro vyhledávání typu 2-4. Viz návrh 167 pro další informace.

### MessagePayloadMessage {#MessagePayloadMessage}

#### Popis

Doručit užitečná data zprávy klientovi.

Odesláno z routeru klientovi. Pokud je i2cp.fastReceive=true, což není výchozí nastavení, klient odpovídá zprávou [ReceiveMessageEndMessage](#ReceiveMessageEndMessage).

#### Obsah

1.  [ID relace](#struct-sessionid)
2.  [ID zprávy](#struct-messageid)
3.  [Užitečné zatížení](#struct-payload)

#### Poznámky

### MessageStatusMessage {#MessageStatusMessage}

#### Popis

Oznámit klientovi stav doručení příchozí nebo odchozí zprávy. Odesláno z Router do klienta. Pokud tato zpráva indikuje, že je k dispozici příchozí zpráva, klient odpovídá pomocí [ReceiveMessageBeginMessage](#ReceiveMessageBeginMessage). Pro odchozí zprávu je toto odpověď na [SendMessageMessage](#SendMessageMessage) nebo [SendMessageExpiresMessage](#SendMessageExpiresMessage).

#### Obsah

1.  [Session ID](#struct-sessionid)
2.  [Message ID](#struct-messageid) generované routerem
3.  1 byte [Integer](/docs/specs/common-structures/#integer) status
4.  4 byte [Integer](/docs/specs/common-structures/#integer) velikost
5.  4 byte [Integer](/docs/specs/common-structures/#integer) nonce dříve generované
    klientem

#### Poznámky

Do verze 0.9.4 jsou známé hodnoty stavu 0 pro zpráva je k dispozici, 1 pro přijato, 2 pro best effort uspěšné, 3 pro best effort neúspěšné, 4 pro garantované uspěšné, 5 pro garantované neúspěšné. Celé číslo size specifikuje velikost dostupné zprávy a je relevantní pouze pro stav = 0. I když garantované doručení není implementováno (best effort je jediná služba), současná implementace routeru používá kódy garantovaného stavu, nikoli kódy best effort.

Od verze routeru 0.9.5 jsou definovány další stavové kódy, avšak nemusí být nutně implementovány. Podrobnosti najdete v [MessageStatusMessage Javadocs](http://javadoc.i2p.net/net/i2p/data/i2cp/MessageStatusMessage.html). Pro odchozí zprávy kódy 1, 2, 4 a 6 označují úspěch; všechny ostatní jsou selhání. Vrácené kódy selhání se mohou lišit a jsou specifické pro danou implementaci.

Všechny stavové kódy:

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Status Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">As Of Release</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Name</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Description</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Available</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">DEPRECATED. For incoming messages only. All other status codes below are for outgoing messages. The included size is the size in bytes of the available message. This is unused in "fast receive" mode, which is the default as of release 0.9.4.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Accepted</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Outgoing message accepted by the local router for delivery. The included nonce matches the nonce in the <a href="#SendMessageMessage">SendMessageMessage</a>, and the included Message ID will be used for subsequent success or failure notification.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Best Effort Success</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Probable success (unused)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Best Effort Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Probable failure</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Guaranteed Success</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Probable success</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Guaranteed Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Generic failure, specific cause unknown. May not really be a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local Success</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local delivery successful. The destination was another client on the same router.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local delivery failure. The destination was another client on the same router.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">8</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Router Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The local router is not ready, has shut down, or has major problems. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">9</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Network Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The local computer apparently has no network connectivity at all. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">10</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Session</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The I2CP session is invalid or closed. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Message</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The message payload is invalid or zero-length or too big. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Options</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Something is invalid in the message options, or the expiration is in the past or too far in the future. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">13</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Overflow Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Some queue or buffer in the router is full and the message was dropped. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">14</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Message Expired</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The message expired before it could be sent. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">15</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Local Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The client has not yet signed a <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a>, or the local keys are invalid, or it has expired, or it does not have any tunnels in it. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">No Local Tunnels</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local problems. No outbound tunnel to send through, or no inbound tunnel if a reply is required. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">17</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Unsupported Encryption</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The certs or options in the <a href="/docs/specs/common-structures/#destination">Destination</a> or its <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a> indicate that it uses an encryption format that we don't support, so we can't talk to it. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">18</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Destination</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Something is wrong with the far-end <a href="/docs/specs/common-structures/#destination">Destination</a>. Bad format, unsupported options, certificates, etc. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">19</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">We got the far-end <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a> but something strange is wrong with it. Unsupported options or certificates, no tunnels, etc. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">20</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Expired Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">We got the far-end <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a> but it's expired and we can't get a new one. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">21</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">No Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Could not find the far-end <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a>. This is a common failure, equivalent to a DNS lookup failure. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">22</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Meta Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The far-end destination's lease set was a meta lease set, and cannot be sent to. The client should request the meta lease set's contents with a HostLookupMessage, and select one of the hashes contained within to look up and send to. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">23</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.62</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Loopback Denied</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The message was attempted to be sent from and to the same destination or session. This is a guaranteed failure.</td>
</tr>
</table>
Když status = 1 (přijato), nonce odpovídá nonce v [SendMessageMessage](#SendMessageMessage) a zahrnuté Message ID bude použito pro následné oznámení o úspěchu nebo selhání. V opačném případě může být nonce ignorováno.

### ReceiveMessageBeginMessage {#ReceiveMessageBeginMessage}

ZASTARALÉ. Není podporováno i2pd.

#### Popis

Požádejte router o doručení zprávy, o které byl předem informován. Odesílá se z klienta do routeru. Router odpovídá zprávou [MessagePayloadMessage](#MessagePayloadMessage).

#### Obsah

1.  [ID relace](#struct-sessionid)
2.  [ID zprávy](#struct-messageid)

#### Poznámky

[ReceiveMessageBeginMessage](#ReceiveMessageBeginMessage) se odesílá jako odpověď na [MessageStatusMessage](#MessageStatusMessage) oznamující, že je k dispozici nová zpráva k vyzvednutí. Pokud je id zprávy uvedené v [ReceiveMessageBeginMessage](#ReceiveMessageBeginMessage) neplatné nebo nesprávné, router může jednoduše neodpovědět, nebo může poslat zpět [DisconnectMessage](#DisconnectMessage).

Toto se nepoužívá v režimu "rychlého přijímání", který je výchozí od verze 0.9.4.

### ReceiveMessageEndMessage {#ReceiveMessageEndMessage}

ZASTARALÉ. Není podporováno i2pd.

#### Popis

Řekněte routeru, že doručení zprávy bylo úspěšně dokončeno a že router může zprávu zahodit.

Odesláno z klienta do routeru.

#### Obsah

1.  [ID relace](#struct-sessionid)
2.  [ID zprávy](#struct-messageid)

#### Poznámky

[ReceiveMessageEndMessage](#ReceiveMessageEndMessage) se odesílá poté, co [MessagePayloadMessage](#MessagePayloadMessage) kompletně doručí payload zprávy.

Toto se nepoužívá v režimu "rychlého příjmu", který je výchozí od verze 0.9.4.

### ReconfigureSessionMessage {#ReconfigureSessionMessage}

#### Popis

Odesláno z klienta do routeru pro aktualizaci konfigurace relace. Router odpovídá [SessionStatusMessage](#SessionStatusMessage).

#### Obsah

1.  [ID relace](#struct-sessionid)
2.  [Konfigurace relace](#struct-sessionconfig)

#### Poznámky

- Od verze 0.7.1.
- Pokud je datum v Session Config příliš vzdálené (více než +/- 30
  sekund) od aktuálního času routeru, bude relace
  odmítnuta.
- [Mapping](/docs/specs/common-structures/#mapping) v Session Config musí být
  seřazen podle klíče, aby byla signatura správně validována v
  routeru.
- Některé možnosti konfigurace lze nastavit pouze v
  [CreateSessionMessage](#CreateSessionMessage) a změny zde nebudou
  routerem rozpoznány. Změny možností tunelu inbound.\*
  a outbound.\* jsou vždy rozpoznány.
- Obecně by router měl sloučit aktualizovanou konfiguraci s
  aktuální konfigurací, takže aktualizovaná konfigurace musí obsahovat pouze nové nebo
  změněné možnosti. Kvůli sloučení však možnosti nelze tímto způsobem
  odstranit; musí být explicitně nastaveny na požadovanou
  výchozí hodnotu.

### ReportAbuseMessage {#ReportAbuseMessage}

ZASTARALÉ, NEPOUŽÍVANÉ, NEPODPOROVANÉ

#### Popis

Informovat druhou stranu (client nebo router), že je pod útokem, potenciálně s odkazem na konkrétní MessageId. Pokud je router pod útokem, client se může rozhodnout migrovat na jiný router, a pokud je client pod útokem, router může znovu vybudovat své routery nebo zařadit na černou listinu některé z peerů, které mu poslaly zprávy s útokem.

Odesláno buď z routeru klientovi nebo z klienta routeru.

#### Obsah

1.  [Session ID](#struct-sessionid)
2.  1 byte [Integer](/docs/specs/common-structures/#integer) závažnost zneužití (0 je minimálně škodlivé, 255 je extrémně škodlivé)
3.  Důvod [String](/docs/specs/common-structures/#string)
4.  [Message ID](#struct-messageid)

#### Poznámky

Nepoužíváno. Není plně implementováno. Router i klient mohou generovat [ReportAbuseMessage](#ReportAbuseMessage), ale ani jeden nemá handler pro zprávu při jejím přijetí.

### RequestLeaseSetMessage {#RequestLeaseSetMessage}

ZASTARALÉ. Není podporováno i2pd. Neposílá se Java I2P klientům verze 0.9.7 nebo vyšší (2013-07). Použijte RequestVariableLeaseSetMessage.

#### Popis

Požadavek, aby klient autorizoval zahrnutí konkrétní sady příchozích tunnelů. Odesílá se z routeru klientovi. Klient odpovídá zprávou [CreateLeaseSetMessage](#CreateLeaseSetMessage).

První z těchto zpráv odeslaných v relaci je signál pro klienta, že tunely jsou vybudovány a připraveny pro provoz. Router nesmí odeslat první z těchto zpráv, dokud nebude vybudován alespoň jeden příchozí A jeden odchozí tunnel. Klienti by měli vypršet časový limit a zničit relaci, pokud první z těchto zpráv není přijata po určité době (doporučeno: 5 minut nebo více).

#### Obsah

1.  [Session ID](#struct-sessionid)
2.  1 byte [Integer](/docs/specs/common-structures/#integer) počet tunelů
3.  Tolik párů:
    1.  [Hash](/docs/specs/common-structures/#hash)
    2.  [TunnelId](/docs/specs/common-structures/#tunnelid)
4.  Koncové [Date](/docs/specs/common-structures/#date)

#### Poznámky

Toto požaduje [LeaseSet](/docs/specs/common-structures/#leaseset) se všemi [Lease](/docs/specs/common-structures/#lease) záznamy nastavenými tak, aby vypršely ve stejnou dobu. Pro klientské verze 0.9.7 nebo vyšší se používá [RequestVariableLeaseSetMessage](#RequestVariableLeaseSetMessage).

### RequestVariableLeaseSetMessage {#RequestVariableLeaseSetMessage}

#### Popis

Požadavek, aby klient autorizoval zahrnutí konkrétní sady příchozích tunnelů.

Odesláno z routeru klientovi. Klient odpovídá zprávou [CreateLeaseSetMessage](#CreateLeaseSetMessage) nebo [CreateLeaseSet2Message](#CreateLeaseSet2Message).

První z těchto zpráv odeslaných v rámci relace je signálem pro klienta, že tunnely jsou postavené a připravené pro provoz. Router nesmí odeslat první z těchto zpráv, dokud není postaven alespoň jeden příchozí A jeden odchozí tunnel. Klienti by měli relaci ukončit kvůli vypršení času a zničit ji, pokud první z těchto zpráv není přijata po určité době (doporučeno: 5 minut nebo více).

#### Obsah

1.  [Session ID](#struct-sessionid)
2.  1 byte [Integer](/docs/specs/common-structures/#integer) počet tunnelů
3.  Tolik [Lease](/docs/specs/common-structures/#lease) záznamů

#### Poznámky

Toto vyžaduje [LeaseSet](/docs/specs/common-structures/#leaseset) s individuálním časem vypršení pro každý [Lease](/docs/specs/common-structures/#lease).

Od vydání 0.9.7. Pro klienty před tímto vydáním použijte [RequestLeaseSetMessage](#RequestLeaseSetMessage).

### SendMessageMessage {#SendMessageMessage}

#### Popis

Takto klient odesílá zprávu (payload) na [Destination](/docs/specs/common-structures/#destination). Router použije výchozí dobu platnosti.

Odesláno z klienta do routeru. Router odpovídá zprávou [MessageStatusMessage](#MessageStatusMessage).

#### Obsah

1.  [Session ID](#struct-sessionid)
2.  [Destination](/docs/specs/common-structures/#destination)
3.  [Payload](#struct-payload)
4.  4 byte [Integer](/docs/specs/common-structures/#integer) nonce

#### Poznámky

Jakmile [SendMessageMessage](#SendMessageMessage) dorazí kompletně neporušená, router by měl vrátit [MessageStatusMessage](#MessageStatusMessage) oznamující, že byla přijata k doručení. Tato zpráva bude obsahovat stejný nonce poslaný zde. Později, na základě záruk doručení konfigurace relace, může router dodatečně poslat zpět další [MessageStatusMessage](#MessageStatusMessage) aktualizující stav.

Od vydání 0.8.1 router neposílá ani [MessageStatusMessage](#MessageStatusMessage), pokud i2cp.messageReliability=none.

Před vydáním verze 0.9.4 nebyla hodnota nonce 0 povolena. Od vydání verze 0.9.4 je hodnota nonce 0 povolena a říká routeru, že by neměl posílat [MessageStatusMessage](#MessageStatusMessage), tj. chová se, jako kdyby i2cp.messageReliability=none pouze pro tuto zprávu.

Před vydáním verze 0.9.14 nebylo možné přepsat session s i2cp.messageReliability=none na základě jednotlivých zpráv. Od verze 0.9.14 může v session s i2cp.messageReliability=none klient vyžádat doručení [MessageStatusMessage](#MessageStatusMessage) s úspěchem nebo neúspěchem doručení nastavením nonce na nenulovou hodnotu. Router neodešle "přijatou" [MessageStatusMessage](#MessageStatusMessage), ale později odešle klientovi [MessageStatusMessage](#MessageStatusMessage) se stejným nonce a hodnotou úspěchu nebo neúspěchu.

### SendMessageExpiresMessage {#SendMessageExpiresMessage}

#### Popis

Odesíláno z klienta do routeru. Stejné jako [SendMessageMessage](#SendMessageMessage), kromě toho, že obsahuje expiraci a možnosti.

#### Obsah

1.  [Session ID](#struct-sessionid)
2.  [Destination](/docs/specs/common-structures/#destination)
3.  [Payload](#struct-payload)
4.  4 byte [Integer](/docs/specs/common-structures/#integer) nonce
5.  2 bajty příznaků (možnosti)
6.  Expiration [Date](/docs/specs/common-structures/#date) zkrácený z 8 bajtů na 6
    bajtů

#### Poznámky

Od verze 0.7.1.

V režimu "best effort", jakmile SendMessageExpiresMessage dorazí kompletně neporušená, router by měl vrátit MessageStatusMessage oznamující, že byla přijata k doručení. Tato zpráva bude obsahovat stejný nonce zaslaný zde. Později, na základě záruk doručení konfigurace relace, může router dodatečně zaslat další MessageStatusMessage aktualizující stav.

Od verze 0.8.1 router neposílá žádnou Message Status Message, pokud i2cp.messageReliability=none.

Před verzí 0.9.4 nebyla povolena nonce hodnota 0. Od verze 0.9.4 je nonce hodnota 0 povolena a říká routeru, že nemá odeslat žádnou Message Status Message, tedy se chová, jako by bylo nastaveno i2cp.messageReliability=none pouze pro tuto zprávu.

Před verzí 0.9.14 nemohla být relace s i2cp.messageReliability=none přepsána pro jednotlivé zprávy. Od verze 0.9.14 může v relaci s i2cp.messageReliability=none klient požádat o doručení Message Status Message s informací o úspěchu nebo neúspěchu doručení nastavením nonce na nenulovou hodnotu. Router neodešle "accepted" Message Status Message, ale později odešle klientovi Message Status Message se stejným nonce a hodnotou úspěchu nebo neúspěchu.

#### Pole příznaků

Od verze 0.8.4 jsou horní dva byty Date předefinovány tak, aby obsahovaly příznaky. Příznaky musí být výchozně nastaveny na všechny nuly kvůli zpětné kompatibilitě. Date nezasáhne do pole příznaků až do roku 10889. Příznaky mohou být použity aplikací k poskytnutí návodů routeru ohledně toho, zda má být s touto zprávou doručen LeaseSet a/nebo ElGamal/AES Session Tags. Nastavení významně ovlivní množství protokolové režie a spolehlivost doručování zpráv. Jednotlivé bity příznaků jsou definovány následovně od verze 0.9.2. Definice se mohou změnit. Pro vytvoření příznaků použijte třídu SendMessageOptions.

Pořadí bitů: 15...0

Bity 15-11

:   Nepoužíváno, musí být nula

Bity 10-9

:   Přepsání spolehlivosti zpráv (Neimplementováno, bude odstraněno).

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Field value</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Description</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">00</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Use session setting i2cp.messageReliability (default)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">01</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Use "best effort" message reliability for this message, overriding the session setting. The router will send one or more MessageStatusMessages in response. Unused. Use a nonzero nonce value to override a session setting of "none".</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">10</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Use "guaranteed" message reliability for this message, overriding the session setting. The router will send one or more MessageStatusMessages in response. Unused. Use a nonzero nonce value to override a session setting of "none".</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Unused. Use a nonce value of 0 to force "none" and override a session setting of "best effort" or "guaranteed".</td>
</tr>
</table>
Bit 8

:   Pokud 1, nezahrnuj leaseSet do garlic encryption s touto zprávou. Pokud

    0, the router may bundle a lease set at its discretion.

Bity 7-4

:   Nízký práh tagů. Pokud je k dispozici méně tagů než tento počet,

    send more. This is advisory and does not force tags to be delivered.
    For ElGamal only. Ignored for ECIES-Ratchet.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Field value</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Tag threshold</th>
</tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0000</td><td style="border: 1px solid var(--color-border); padding: 8px;">Use session key manager settings</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0001</td><td style="border: 1px solid var(--color-border); padding: 8px;">2</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0010</td><td style="border: 1px solid var(--color-border); padding: 8px;">3</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0011</td><td style="border: 1px solid var(--color-border); padding: 8px;">6</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0100</td><td style="border: 1px solid var(--color-border); padding: 8px;">9</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0101</td><td style="border: 1px solid var(--color-border); padding: 8px;">14</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0110</td><td style="border: 1px solid var(--color-border); padding: 8px;">20</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0111</td><td style="border: 1px solid var(--color-border); padding: 8px;">27</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1000</td><td style="border: 1px solid var(--color-border); padding: 8px;">35</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1001</td><td style="border: 1px solid var(--color-border); padding: 8px;">45</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1010</td><td style="border: 1px solid var(--color-border); padding: 8px;">57</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1011</td><td style="border: 1px solid var(--color-border); padding: 8px;">72</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1100</td><td style="border: 1px solid var(--color-border); padding: 8px;">92</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1101</td><td style="border: 1px solid var(--color-border); padding: 8px;">117</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1110</td><td style="border: 1px solid var(--color-border); padding: 8px;">147</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1111</td><td style="border: 1px solid var(--color-border); padding: 8px;">192</td></tr>
</table>
Bity 3-0

:   Počet tagů k odeslání, pokud je to požadováno. Toto je pouze doporučující a není

    force tags to be delivered. For ElGamal only. Ignored for
    ECIES-Ratchet.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Field value</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Tags to send</th>
</tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0000</td><td style="border: 1px solid var(--color-border); padding: 8px;">Use session key manager settings</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0001</td><td style="border: 1px solid var(--color-border); padding: 8px;">2</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0010</td><td style="border: 1px solid var(--color-border); padding: 8px;">4</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0011</td><td style="border: 1px solid var(--color-border); padding: 8px;">6</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0100</td><td style="border: 1px solid var(--color-border); padding: 8px;">8</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0101</td><td style="border: 1px solid var(--color-border); padding: 8px;">12</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0110</td><td style="border: 1px solid var(--color-border); padding: 8px;">16</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0111</td><td style="border: 1px solid var(--color-border); padding: 8px;">24</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1000</td><td style="border: 1px solid var(--color-border); padding: 8px;">32</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1001</td><td style="border: 1px solid var(--color-border); padding: 8px;">40</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1010</td><td style="border: 1px solid var(--color-border); padding: 8px;">51</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1011</td><td style="border: 1px solid var(--color-border); padding: 8px;">64</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1100</td><td style="border: 1px solid var(--color-border); padding: 8px;">80</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1101</td><td style="border: 1px solid var(--color-border); padding: 8px;">100</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1110</td><td style="border: 1px solid var(--color-border); padding: 8px;">125</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1111</td><td style="border: 1px solid var(--color-border); padding: 8px;">160</td></tr>
</table>
### SessionStatusMessage {#SessionStatusMessage}

#### Popis

Informovat klienta o stavu jeho relace.

Odesláno z routeru klientovi, jako odpověď na [CreateSessionMessage](#CreateSessionMessage), [ReconfigureSessionMessage](#ReconfigureSessionMessage), nebo [DestroySessionMessage](#DestroySessionMessage). Ve všech případech, včetně odpovědi na [CreateSessionMessage](#CreateSessionMessage), by router měl odpovědět okamžitě (nečekejte na vybudování tunnelů).

#### Obsah

1.  [Session ID](#struct-sessionid)
2.  1 bajt [Integer](/docs/specs/common-structures/#integer) status

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Status</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Since</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Name</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Definition</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Destroyed</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The session with the given ID is terminated. May be a response to a <a href="#DestroySessionMessage">DestroySessionMessage</a>.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Created</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">In response to a <a href="#CreateSessionMessage">CreateSessionMessage</a>, a new session with the given ID is now active.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Updated</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">In response to a <a href="#ReconfigureSessionMessage">ReconfigureSessionMessage</a>, an existing session with the given ID has been reconfigured.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Invalid</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">In response to a <a href="#CreateSessionMessage">CreateSessionMessage</a>, the configuration is invalid. The included session ID should be ignored. In response to a <a href="#ReconfigureSessionMessage">ReconfigureSessionMessage</a>, the new configuration is invalid for the session with the given ID.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Refused</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">In response to a <a href="#CreateSessionMessage">CreateSessionMessage</a>, the router was unable to create the session, perhaps due to limits being exceeded. The included session ID should be ignored.</td>
</tr>
</table>
#### Poznámky

Hodnoty stavu jsou definovány výše. Pokud je stav Created, Session ID je identifikátor, který se má používat po zbytek relace.

### SetDateMessage {#SetDateMessage}

#### Popis

Aktuální datum a čas. Odesíláno z routeru ke klientovi jako součást počátečního handshaku. Od verze 0.9.20 může být také odesíláno kdykoli po handshaku, aby klient byl informován o posunu hodin.

#### Obsah

1.  [Datum](/docs/specs/common-structures/#date)
2.  Verze I2CP API [String](/docs/specs/common-structures/#string)

#### Poznámky

Toto je obecně první zpráva odeslaná routerem. Řetězec verze je zahrnut od vydání 0.8.7. To je užitečné pouze pokud klient a router nejsou ve stejném JVM. Pokud není přítomen, router je verze 0.8.6 nebo starší.

Dodatečné zprávy SetDate nebudou odeslány klientům ve stejném JVM.

## Reference

- [Date](/docs/specs/common-structures/#date)
- [Destination](/docs/specs/common-structures/#destination)
- [EncryptedLeaseSet](/docs/specs/common-structures/#leaseset2)
- [Hash](/docs/specs/common-structures/#hash)
- [Přehled I2CP](/docs/specs/i2cp/)
- [I2CP Javadocs](http://javadoc.i2p.net/net/i2p/data/i2cp/package-summary.html)
- [Integer](/docs/specs/common-structures/#integer)
- [Lease](/docs/specs/common-structures/#lease)
- [LeaseSet](/docs/specs/common-structures/#leaseset)
- [LeaseSet2](/docs/specs/common-structures/#leaseset2)
- [Mapping](/docs/specs/common-structures/#mapping)
- [MetaLeaseSet](/docs/specs/common-structures/#leaseset2)
- [MessageStatusMessage Javadocs](http://javadoc.i2p.net/net/i2p/data/i2cp/MessageStatusMessage.html)
- [PrivateKey](/docs/specs/common-structures/#privatekey)
- [PublicKey](/docs/specs/common-structures/#publickey)
- [RouterIdentity](/docs/specs/common-structures/#routeridentity)
- [SAMv3](/docs/api/samv3/)
- [Signature](/docs/specs/common-structures/#signature)
- [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey)
- [SigningPublicKey](/docs/specs/common-structures/#signingpublickey)
- [String](/docs/specs/common-structures/#string)
- [TunnelId](/docs/specs/common-structures/#tunnelid)
