---
title: "Síťový protokol I2P (I2NP)"
description: "Formáty zpráv mezi routery, priority a limity velikosti v rámci I2P."
slug: "i2np"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Přehled

Síťový protokol I2P (I2NP) definuje, jak routers vyměňují zprávy, volí transportní protokoly a mísí provoz při zachování anonymity. Funguje mezi **I2CP** (klientské API) a transportními protokoly (**NTCP2** a **SSU2**).

I2NP je vrstva nad transportními protokoly I2P. Je to protokol router-to-router (komunikace přímo mezi routery) používaný pro: - Vyhledávání v síťové databázi a odpovědi - Vytváření tunnelů - Šifrované datové zprávy routeru a klienta

Zprávy I2NP lze posílat bod-bod na jiný router nebo anonymně přes tunnels na tentýž router.

Routers řadí odchozí úlohy do fronty podle lokálních priorit. Vyšší čísla priority se zpracovávají dříve. Cokoli nad standardní prioritu dat pro tunnel (400) se považuje za naléhavé.

### Současné transportní protokoly

I2P nyní používá **NTCP2** (TCP) a **SSU2** (UDP) pro IPv4 i IPv6. Oba transporty používají: - **X25519** pro výměnu klíčů (rámec protokolu Noise) - **ChaCha20/Poly1305** pro autentizované šifrování s přidruženými daty (AEAD) - **SHA-256** pro hashování

**Zastaralé transporty odstraněny:** - NTCP (původní TCP) byl odstraněn z Java routeru ve verzi 0.9.50 (květen 2021) - SSU v1 (původní UDP) byl odstraněn z Java routeru ve verzi 2.4.0 (prosinec 2023) - SSU v1 byl odstraněn z i2pd ve verzi 2.44.0 (listopad 2022)

Od roku 2025 síť zcela přešla na transportní protokoly založené na Noise (sada kryptografických handshake protokolů) bez jakékoli podpory starších transportů.

---

## Systém číslování verzí

**DŮLEŽITÉ:** I2P používá dvojí systém verzování, kterému je nutné jasně rozumět:

### Verze vydání (určené pro uživatele)

Toto jsou verze, které uživatelé vidí a stahují: - 0.9.50 (květen 2021) - Poslední vydání řady 0.9.x - **1.5.0** (srpen 2021) - První vydání řady 1.x - 1.6.0, 1.7.0, 1.8.0, 1.9.0 (v letech 2021-2022) - **2.0.0** (listopad 2022) - První vydání řady 2.x - 2.1.0 až 2.9.0 (v letech 2023-2025) - **2.10.0** (8. září 2025) - Aktuální vydání

### Verze API (kompatibilita protokolů)

Toto jsou interní čísla verzí zveřejněná v poli "router.version" ve vlastnostech RouterInfo: - 0.9.50 (květen 2021) - **0.9.51** (srpen 2021) - Verze API pro vydání 1.5.0 - 0.9.52 až 0.9.66 (pokračuje napříč vydáními 2.x) - **0.9.67** (září 2025) - Verze API pro vydání 2.10.0

**Klíčový bod:** Nevyšla ŽÁDNÁ vydání s označením 0.9.51 až 0.9.67. Tato čísla existují pouze jako identifikátory verzí API. I2P přeskočilo z vydání 0.9.50 přímo na 1.5.0.

### Tabulka mapování verzí

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
**Nadcházející:** Verze 2.11.0 (plánováno na prosinec 2025) bude vyžadovat Javu 17+ a ve výchozím nastavení povolí postkvantovou kryptografii.

---

## Verze protokolů

Všechny routery musí uvádět svou verzi protokolu I2NP v poli "router.version" ve vlastnostech RouterInfo (informační záznam o routeru). Tato verze je verzí API, která udává úroveň podpory různých funkcí protokolu I2NP, a nemusí nutně odpovídat skutečné verzi routeru.

Pokud alternativní (non-Java) routers chtějí zveřejnit jakékoli informace o verzi samotné implementace routeru, musejí tak učinit v jiné vlastnosti. Jsou povoleny i jiné verze než ty uvedené níže. Podpora bude určena číselným porovnáním; například 0.9.13 implikuje podporu funkcí verze 0.9.12.

**Poznámka:** Vlastnost "coreVersion" se již v informacích o routeru nezveřejňuje a nikdy se nepoužívala k určení verze protokolu I2NP.

### Přehled funkcí podle verze API

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
**Poznámka:** Existují také funkce související s transportem a problémy s kompatibilitou. Podrobnosti viz dokumentaci k transportům NTCP2 a SSU2.

---

## Hlavička zprávy

I2NP používá logickou strukturu hlavičky o velikosti 16 bajtů, zatímco moderní transporty (NTCP2 a SSU2) používají zkrácenou 9bajtovou hlavičku, která vynechává redundantní pole velikosti a kontrolního součtu. Pole zůstávají koncepčně shodná.

### Srovnání formátu hlavičky

**Standardní formát (16 bajtů):**

Používá se v zastaralém transportu NTCP a když jsou zprávy I2NP vnořeny do jiných zpráv (TunnelData, TunnelGateway, GarlicClove).

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
**Krátký formát pro SSU (zastaralý, 5 bajtů):**

```
+----+----+----+----+----+
|type| short_expiration  |
+----+----+----+----+----+

type :: Integer (1 byte)
short_expiration :: Integer (4 bytes, seconds since epoch)
```
**Krátký formát pro NTCP2, SSU2 a ECIES-Ratchet (postupný klíčový mechanismus ECIES) Garlic Cloves (podsložky zprávy v garlic encryption) (9 bajtů):**

Používá se v moderních transportech a v garlic messages (garlicových zprávách) šifrovaných pomocí ECIES.

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
### Podrobnosti o polích hlavičky

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
### Poznámky k implementaci

- Při přenosu přes SSU (zastaralé) byly zahrnuty pouze typ a 4bajtová doba platnosti
- Při přenosu přes NTCP2 nebo SSU2 se používá 9bajtový krátký formát
- Pro zprávy I2NP obsažené v jiných zprávách (Data, TunnelData, TunnelGateway, GarlicClove) je vyžadována standardní 16bajtová hlavička
- Od verze 0.8.12 je na některých místech v zásobníku protokolů z důvodu efektivity ověřování kontrolního součtu vypnuto, ale generování kontrolního součtu je kvůli kompatibilitě stále vyžadováno
- Krátká doba platnosti je bez znaménka a 7. února 2106 dojde k přetočení. Po tomto datu je nutné přičíst offset (posun), aby se získal správný čas
- Pro kompatibilitu se staršími verzemi vždy generujte kontrolní součty, i když nemusí být ověřovány

---

## Omezení velikosti

Zprávy tunnel fragmentují užitečná data I2NP na části pevné velikosti:
- **První fragment:** přibližně 956 bajtů
- **Následující fragmenty:** přibližně 996 bajtů každý
- **Maximální počet fragmentů:** 64 (očíslované 0–63)
- **Maximální velikost užitečných dat:** přibližně 61 200 bajtů (61,2 KB)

**Výpočet:** 956 + (63 × 996) = 63,704 bajtů jako teoretické maximum, s praktickým limitem kolem 61,200 bajtů kvůli režii.

### Historický kontext

Starší transporty měly přísnější limity velikosti rámců: - NTCP: rámce o velikosti 16 KB - SSU: rámce o velikosti přibližně 32 KB

NTCP2 podporuje rámce o velikosti přibližně 65 KB, ale limit fragmentace pro tunnel stále platí.

### Úvahy týkající se dat aplikací

Garlic messages (typ zpráv používaný v rámci garlic encryption) mohou zahrnovat LeaseSets, značky relace, nebo šifrované varianty LeaseSet2, čímž se snižuje prostor pro užitečná data.

**Doporučení:** Datagramy by měly zůstat ≤ 10 KB pro zajištění spolehlivého doručení. Zprávy blížící se limitu 61 KB mohou zaznamenat: - Zvýšenou latenci kvůli opětovnému sestavení fragmentů - Vyšší pravděpodobnost selhání doručení - Větší vystavení analýze provozu

### Technické podrobnosti fragmentace

Každá zpráva tunnelu má přesně 1,024 bajtů (1 KB) a obsahuje: - 4bajtové tunnel ID - 16bajtový inicializační vektor (IV) - 1,004 bajtů šifrovaných dat

V rámci šifrovaných dat zprávy tunnelu přenášejí fragmentované zprávy I2NP s hlavičkami fragmentů, které uvádějí:
- Číslo fragmentu (0-63)
- Zda se jedná o první, nebo navazující fragment
- ID celé zprávy pro opětovné sestavení

První fragment obsahuje úplnou hlavičku zprávy I2NP (16 bajtů), takže pro užitečná data zbývá přibližně 956 bajtů. Následující fragmenty hlavičku zprávy neobsahují, což umožňuje přibližně 996 bajtů užitečných dat na fragment.

---

## Běžné typy zpráv

Routers používají typ zprávy a prioritu k plánování odchozí práce. Vyšší hodnoty priority jsou zpracovány jako první. Hodnoty níže odpovídají aktuálním výchozím hodnotám Java I2P (k verzi API 0.9.67).

**Poznámka:** Priority závisejí na implementaci. Pro závazné hodnoty priorit nahlédněte do dokumentace třídy `OutNetMessage` ve zdrojovém kódu Java I2P.

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
**Vyhrazené typy zpráv:** - Typ 0: Vyhrazeno - Typy 4-9: Vyhrazeno pro budoucí použití - Typy 12-17: Vyhrazeno pro budoucí použití - Typy 224-254: Vyhrazeno pro experimentální zprávy - Typ 255: Vyhrazeno pro budoucí rozšíření

### Poznámky k typům zpráv

- Zprávy řídicí roviny (DatabaseLookup, TunnelBuild apod.) obvykle putují přes **průzkumné tunnels** (virtuální okruhy v I2P), nikoli klientské tunnels, což umožňuje nezávislé určování priority
- Hodnoty priorit jsou přibližné a mohou se lišit podle implementace
- TunnelBuild (21) a TunnelBuildReply (22) jsou zastaralé, ale stále implementované kvůli kompatibilitě s velmi dlouhými tunnels (>8 skoků)
- Standardní priorita dat pro tunnel je 400; cokoli nad tímto je považováno za naléhavé
- Typická délka tunnel v dnešní síti je 3–4 skoky, takže většina sestavení tunnel používá ShortTunnelBuild (záznamy o velikosti 218 bajtů) nebo VariableTunnelBuild (záznamy o velikosti 528 bajtů)

---

## Šifrování a zapouzdřování zpráv

Routers často zapouzdřují zprávy I2NP před přenosem, čímž vytvářejí více vrstev šifrování. Zpráva DeliveryStatus může být: 1. Vložená do GarlicMessage (zašifrovaná) 2. Uvnitř DataMessage 3. Uvnitř zprávy TunnelData (znovu zašifrovaná)

Každý skok dešifruje pouze svou vrstvu; koncový cíl odhalí nejvnitřnější užitečná data.

### Šifrovací algoritmy

**Zastaralé (postupně vyřazováno):** - ElGamal/AES + SessionTags (značky relace) - ElGamal-2048 pro asymetrické šifrování - AES-256 pro symetrické šifrování - 32bajtové session tags

**Aktuální (standard od API 0.9.48):** - ECIES-X25519 + ChaCha20/Poly1305 AEAD s ratcheting forward secrecy (průběžně obnovované dopředné utajení) - rámec protokolu Noise (Noise_IK_25519_ChaChaPoly_SHA256 pro destinace) - 8bajtové značky relace (zmenšeno z 32 bajtů) - algoritmus Signal Double Ratchet pro dopředné utajení - Zavedeno ve verzi API 0.9.46 (2020) - Povinné pro všechny routers od verze API 0.9.58 (2023)

**Budoucnost (Beta od verze 2.10.0):** - Postkvantová hybridní kryptografie používající MLKEM (ML-KEM-768) v kombinaci s X25519 - Hybridní ratchet (kryptografický krokovací mechanismus) kombinující klasické i postkvantové vyjednávání klíče - Zpětně kompatibilní s ECIES-X25519 - Stane se výchozí ve vydání 2.11.0 (prosinec 2025)

### Označení ElGamal routeru za zastaralý

**KRITICKÉ:** ElGamal routery byly označeny jako zastaralé od verze API 0.9.58 (vydání 2.2.0, březen 2023). Jelikož doporučená minimální verze floodfill pro dotazování je nyní 0.9.58, implementace nemusejí implementovat šifrování pro ElGamal floodfill routery.

**Nicméně:** Cíle ElGamal jsou stále podporovány kvůli zpětné kompatibilitě. Klienti používající šifrování ElGamal mohou nadále komunikovat prostřednictvím ECIES routers.

### Podrobnosti o ECIES-X25519-AEAD-Ratchet (kryptografický mechanismus)

Toto je crypto type 4 (typ kryptografie číslo 4) v kryptografické specifikaci I2P. Poskytuje:

**Klíčové vlastnosti:** - Dopředné utajení pomocí ratcheting (nové klíče pro každou zprávu) - Snížené nároky na ukládání značek relací (8 bajtů vs. 32 bajtů) - Více typů relací (New Session, Existing Session, One-Time) - Založeno na protokolu Noise Noise_IK_25519_ChaChaPoly_SHA256 - Integrované s algoritmem Double Ratchet od Signalu

**Kryptografická primitiva:** - X25519 pro dohodu o klíči Diffie-Hellman - ChaCha20 pro proudové šifrování - Poly1305 pro autentizaci zpráv (AEAD, autentizované šifrování s přidruženými daty) - SHA-256 pro hašování - HKDF pro odvozování klíčů

**Správa relací:** - Nová relace: Počáteční spojení s použitím statického klíče cíle - Stávající relace: Následné zprávy s využitím značek relace - Jednorázová relace: Relace s jedinou zprávou pro nižší režii

Viz [Specifikace ECIES](/docs/specs/ecies/) a [Návrh 144](/proposals/144-ecies-x25519-aead-ratchet/) pro úplné technické podrobnosti.

---

## Společné struktury

Následující struktury jsou součástí více zpráv I2NP. Nejedná se o úplné zprávy.

### BuildRequestRecord (záznam požadavku na sestavení) (ElGamal)

**ZASTARALÉ.** Používá se v současné síti pouze tehdy, když tunnel obsahuje ElGamal router. Viz [ECIES Tunnel Creation](/docs/specs/implementation/) pro moderní formát.

**Účel:** Jeden záznam v sadě více záznamů k vyžádání vytvoření jednoho skoku v rámci tunnel.

**Formát:**

Zašifrováno pomocí ElGamal a AES (celkem 528 bajtů):

```
+----+----+----+----+----+----+----+----+
| encrypted data (528 bytes)            |
~                                       ~
|                                       |
+----+----+----+----+----+----+----+----+
```
ElGamalem šifrovaná struktura (528 bajtů):

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
Struktura otevřeného textu (222 bajtů před šifrováním):

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
**Poznámky:** - Šifrování ElGamal-2048 vytváří 514bajtový blok, ale dva vycpávkové bajty (na pozicích 0 a 257) jsou odstraněny, takže výsledkem je 512 bajtů - Viz [Specifikace vytváření Tunnelu](/docs/specs/implementation/) pro podrobnosti o polích - Zdrojový kód: `net.i2p.data.i2np.BuildRequestRecord` - Konstanta: `EncryptedBuildRecord.RECORD_SIZE = 528`

### BuildRequestRecord (ECIES-X25519 dlouhý)

Pro ECIES-X25519 routers, uvedené ve verzi API 0.9.48. Používá 528 bajtů pro zpětnou kompatibilitu se smíšenými tunnels.

**Formát:**

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
**Celková velikost:** 528 bajtů (stejná jako u ElGamalu kvůli kompatibilitě)

Viz [ECIES Tunnel Creation](/docs/specs/implementation/) pro podrobnosti o struktuře nešifrovaných dat a šifrování.

### BuildRequestRecord (ECIES-X25519 Short) (záznam požadavku na sestavení)

Pouze pro ECIES-X25519 routers, od verze API 0.9.51 (vydání 1.5.0). Toto je aktuální standardní formát.

**Formát:**

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
**Celková velikost:** 218 bajtů (snížení o 59 % oproti 528 bajtům)

**Klíčový rozdíl:** Krátké záznamy odvozují VŠECHNY klíče pomocí HKDF (funkce pro odvozování klíčů), místo aby je do záznamu explicitně zahrnovaly. To zahrnuje: - Klíče vrstvy (pro šifrování tunnelu) - IV klíče (pro šifrování tunnelu) - Reply klíče (pro build reply) - Reply IVs (pro build reply)

Všechny klíče jsou odvozeny pomocí mechanismu HKDF protokolu Noise na základě sdíleného tajemství z výměny klíčů X25519.

**Výhody:** - 4 krátké záznamy se vejdou do jedné zprávy pro tunnel (873 bajtů) - 3 zprávové tunnel builds (sestavení tunnelu) místo samostatných zpráv pro každý záznam - Snížené nároky na šířku pásma a latenci - Stejné bezpečnostní vlastnosti jako dlouhý formát

Viz [Návrh 157](/proposals/157-new-tbm/) pro odůvodnění a [ECIES Tunnel Creation](/docs/specs/implementation/) pro úplnou specifikaci.

**Zdrojový kód:** - `net.i2p.data.i2np.ShortEncryptedBuildRecord` - Konstanta: `ShortEncryptedBuildRecord.RECORD_SIZE = 218`

### BuildResponseRecord (ElGamal) (záznam odpovědi pro sestavení)

**ZASTARALÉ.** Používá se pouze, pokud tunnel obsahuje ElGamal router.

**Účel:** Jeden záznam v sadě více záznamů obsahujících odpovědi na požadavek na sestavení.

**Formát:**

Šifrované (528 bajtů, stejná velikost jako BuildRequestRecord (záznam požadavku na sestavení tunnelu)):

```
bytes 0-527 :: AES-encrypted record
```
Nešifrovaná struktura:

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
**Kódy odpovědí:** - `0` - Přijmout - `30` - Odmítnout (kvůli překročení šířky pásma)

Viz [Tunnel Creation Specification](/docs/specs/implementation/) pro podrobnosti o poli odpovědi.

### BuildResponseRecord (záznam odpovědi na sestavení) (ECIES-X25519)

Pro ECIES-X25519 routers, verze API 0.9.48+. Stejná velikost jako u odpovídajícího požadavku (528 pro dlouhý, 218 pro krátký).

**Formát:**

Dlouhý formát (528 bajtů):

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
Krátký formát (218 bajtů):

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
**Struktura otevřeného textu (pro oba formáty):**

Obsahuje mapovací strukturu (formát klíč–hodnota I2P) s: - Kód stavu odpovědi (povinný) - Parametr dostupné šířky pásma ("b") (volitelný, přidán v API 0.9.65) - Další volitelné parametry pro budoucí rozšíření

**Stavové kódy odpovědi:** - `0` - Úspěch - `30` - Odmítnuto: překročen limit šířky pásma

Viz [ECIES Tunnel Creation](/docs/specs/implementation/) pro úplnou specifikaci.

### GarlicClove (vnitřní část zprávy v rámci garlic encryption, ElGamal/AES)

**UPOZORNĚNÍ:** Toto je formát používaný pro garlic cloves (části garlic zpráv) uvnitř ElGamalem šifrovaných garlic messages. Formát pro ECIES-AEAD-X25519-Ratchet garlic messages a garlic cloves je výrazně odlišný. Moderní formát viz [Specifikace ECIES](/docs/specs/ecies/).

**Zastaralé pro routers (API 0.9.58+), stále podporováno pro cíle.**

**Formát:**

Nešifrované:

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
**Poznámky:** - Cloves (podzpráva v garlic routingu) se nikdy nefragmentují - Když je první bit bajtu příznaků Delivery Instructions 0, clove není šifrován - Když je první bit 1, clove je šifrován (neimplementovaná funkce) - Maximální délka je funkcí součtu délek všech clove a maximální délky GarlicMessage - Certifikát by bylo možné použít s HashCash k "placení" za směrování (možná budoucí funkcionalita) - V praxi používané zprávy: DataMessage, DeliveryStatusMessage, DatabaseStoreMessage - GarlicMessage může obsahovat GarlicMessage (vnořený garlic), ale to se v praxi nepoužívá

Pro koncepční přehled viz [Garlic Routing](/docs/overview/garlic-routing/) (způsob směrování v I2P).

### GarlicClove (ECIES-X25519-AEAD-Ratchet)

Pro ECIES-X25519 routers a destinace, verze API 0.9.46+. Toto je aktuální standardní formát.

**ZÁSADNÍ ROZDÍL:** ECIES garlic používá zcela odlišnou strukturu založenou na blocích protokolu Noise, nikoli na explicitních strukturách clove (podzprávy v rámci garlic v I2P).

**Formát:**

ECIES garlic messages (zprávy typu garlic) obsahují sérii bloků:

```
Block structure:
+----+----+----+----+----+----+----+----+
|type| length    | data ...
+----+----+----+----+----+-//-

type :: 1 byte block type
length :: 2 bytes block length
data :: variable length data
```
**Typy bloků:** - `0` - Garlic Clove Block (blok „stroužku“ v rámci garlic encryption; obsahuje zprávu I2NP) - `1` - Blok data a času (časové razítko) - `2` - Blok možností (parametry doručení) - `3` - Vycpávkový blok - `254` - Ukončovací blok (neimplementováno)

**Garlic Clove Block (blok stroužku v garlic encryption) (typ 0):**

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
**Klíčové rozdíly oproti formátu ElGamal:** - Používá 4bajtové vypršení platnosti (sekundy od epochy) místo 8bajtového Date - Bez pole certificate - Zabalené do blokové struktury s typem a délkou - Celá zpráva šifrovaná pomocí ChaCha20/Poly1305 AEAD - Správa relace pomocí ratcheting (postupné posouvání klíčů)

Pro úplné podrobnosti o rámci protokolu Noise a strukturách bloků viz [specifikaci ECIES](/docs/specs/ecies/).

### Instrukce pro doručení Garlic Clove (podzpráva v rámci garlic encryption)

Tento formát se používá pro garlic cloves (stroužky) u ElGamal i ECIES. Určuje, jak doručit obsaženou zprávu.

**KRITICKÉ VAROVÁNÍ:** Tato specifikace je určena POUZE pro Pokyny k doručení uvnitř Garlic Cloves (v I2P: jednotlivé vnořené části tzv. garlicové zprávy). "Pokyny k doručení" se používají také uvnitř zpráv Tunnel, kde je formát výrazně odlišný. Viz [Specifikace zprávy Tunnel](/docs/specs/implementation/) pro pokyny k doručení týkající se Tunnel. NEZAMĚŇUJTE tyto dva formáty.

**Formát:**

Klíč relace a zpoždění se nepoužívají a nikdy nejsou přítomny, takže tři možné délky jsou: - 1 bajt (LOCAL) - 33 bajtů (ROUTER a DESTINATION) - 37 bajtů (TUNNEL)

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
**Typické délky:** - LOKÁLNÍ doručení: 1 bajt (pouze příznak) - ROUTER / DESTINATION doručení: 33 bajtů (příznak + hash) - TUNNEL doručení: 37 bajtů (příznak + hash + tunnel ID)

**Popisy typů doručení:**

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
**Poznámky k implementaci:** - Šifrování klíče relace není implementováno a příznakový bit je vždy 0 - Zpoždění není plně implementováno a příznakový bit je vždy 0 - U doručení TUNNEL hash identifikuje vstupní router a tunnel ID určuje, který příchozí tunnel - U doručení DESTINATION je hash SHA-256 veřejného klíče cíle - U doručení ROUTER je hash SHA-256 identity routeru

---

## Zprávy I2NP

Úplné specifikace zpráv pro všechny typy zpráv I2NP.

### Přehled typů zpráv

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
**Vyhrazeno:** - Typ 0: Vyhrazeno - Typy 4-9: Vyhrazeno pro budoucí použití - Typy 12-17: Vyhrazeno pro budoucí použití - Typy 224-254: Vyhrazeno pro experimentální zprávy - Typ 255: Vyhrazeno pro budoucí rozšíření

---

### DatabaseStore (uložení do databáze; Typ 1)

**Účel:** Nevyžádané uložení do databáze nebo odpověď na úspěšnou zprávu DatabaseLookup.

**Obsah:** Nekomprimovaný LeaseSet, LeaseSet2, MetaLeaseSet nebo EncryptedLeaseSet, případně komprimovaný RouterInfo.

**Formát s reply token (token pro odpověď):**

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
**Formát s tokenem odpovědi == 0:**

```
+----+----+----+----+----+----+----+----+
| SHA256 Hash as key (32 bytes)        |
+                                       +
|                                       |
+----+----+----+----+----+----+----+----+
|type|         0         | data ...
+----+----+----+----+----+-//
```
**Poznámky:** - Z bezpečnostních důvodů se pole pro odpověď ignorují, pokud je zpráva přijata přes tunnel - Klíč je „skutečný“ hash RouterIdentity nebo Destination, NE směrovací klíč - Typy 3, 5 a 7 (varianty LeaseSet2) byly přidány ve verzi 0.9.38 (API 0.9.38). Podrobnosti viz [Návrh 123](/proposals/123-new-netdb-entries/) - Tyto typy by se měly posílat pouze routerům s verzí API 0.9.38 nebo vyšší - Jako optimalizaci ke snížení počtu spojení, pokud je typ LeaseSet, je přiložen odpovědní token, reply tunnel ID je nenulové a dvojice reply gateway/tunnelID je v LeaseSetu nalezena jako lease (záznam v LeaseSetu), může příjemce přesměrovat odpověď na libovolný jiný lease v daném LeaseSetu - **Formát RouterInfo gzip:** Aby se skryl OS routeru a implementace, slaďte se s implementací Java routeru nastavením času změny na 0 a bajtu OS na 0xFF a nastavte XFL na 0x02 (maximální komprese, nejpomalejší algoritmus) dle RFC 1952. Prvních 10 bajtů: `1F 8B 08 00 00 00 00 00 02 FF`

**Zdrojový kód:** - `net.i2p.data.i2np.DatabaseStoreMessage` - `net.i2p.data.RouterInfo` (pro strukturu RouterInfo) - `net.i2p.data.LeaseSet` (pro strukturu LeaseSet)

---

### DatabaseLookup (vyhledávání v databázi) (Typ 2)

**Účel:** Požadavek na vyhledání položky v síťové databázi (netDb). Odpovědí je buď DatabaseStore, nebo DatabaseSearchReply.

**Formát:**

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
**Režimy šifrování odpovědí:**

**POZNÁMKA:** ElGamal routery jsou od API 0.9.58 označeny jako zastaralé. Jelikož je nyní doporučená minimální verze floodfill pro dotazování 0.9.58, implementace nemusejí implementovat šifrování pro ElGamal floodfill routery. ElGamal destinace jsou stále podporovány.

Příznakový bit 4 (ECIESFlag) se používá v kombinaci s bitem 1 (encryptionFlag) k určení režimu šifrování odpovědi:

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
**Bez šifrování (příznaky 0,0):**

reply_key, tags a reply_tags nejsou k dispozici.

**ElG na ElG (příznaky 0,1) - ZASTARALÉ:**

Podporováno od verze 0.9.7, zastaralé od verze 0.9.58.

```
reply_key :: 32 byte SessionKey (big-endian)
             CSRNG(32) random data

tags :: 1 byte Integer (1-32, typically 1)
        Number of reply tags that follow

reply_tags :: One or more 32-byte SessionTags
              Each is CSRNG(32) random data
```
**ECIES na ElG (příznaky 1,0) - ZASTARALÉ:**

Podporováno od verze 0.9.46, zastaralé od verze 0.9.58.

```
reply_key :: 32 byte ECIES SessionKey (big-endian)
             CSRNG(32) random data

tags :: 1 byte Integer (required value: 1)
        Number of reply tags that follow

reply_tags :: One 8-byte ECIES SessionTag
              CSRNG(8) random data
```
Odpověď je zpráva ECIES Existing Session (zpráva pro existující relaci), jak je definována ve [Specifikaci ECIES](/docs/specs/ecies/):

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
**ECIES (šifrovací schéma založené na eliptických křivkách) na ECIES (příznaky 1,0) - AKTUÁLNÍ STANDARD:**

ECIES destinace nebo router odešle požadavek na vyhledání k ECIES routeru. Podporováno od verze 0.9.49.

Stejný formát jako "ECIES to ElG" výše. Šifrování vyhledávací zprávy je specifikováno v [ECIES Routers](/docs/specs/ecies/#routers). Žadatel je anonymní.

**ECIES (integrované šifrování na eliptických křivkách) na ECIES s DH (výměna klíčů Diffie–Hellman) (příznaky 1,1) - BUDOUCNOST:**

Zatím není plně definováno. Viz [Návrh 156](/proposals/156-ecies-routers/).

**Poznámky:** - Před verzí 0.9.16 mohl klíč patřit k RouterInfo nebo LeaseSet (stejný prostor klíčů, bez příznaku k rozlišení) - Šifrované odpovědi jsou užitečné pouze tehdy, když odpověď jde přes tunnel - Počet zahrnutých tagů může být více než jeden, pokud jsou implementovány alternativní strategie vyhledávání v DHT (distribuovaná hašovací tabulka) - Vyhledávací klíč a vylučovací klíče jsou "skutečné" hashe, NIKOLI směrovací klíče - Typy 3, 5 a 7 (varianty LeaseSet2) mohou být od verze 0.9.38 vráceny. Viz [Návrh 123](/proposals/123-new-netdb-entries/) - **Poznámky k průzkumnému vyhledávání:** Průzkumné vyhledávání je definováno tak, že vrací seznam ne-floodfill hashů blízkých danému klíči. Implementace se však liší: Java skutečně vyhledá hledaný klíč pro RI (RouterInfo) a vrátí DatabaseStore (záznam v netDb), pokud existuje; i2pd nikoli. Proto se nedoporučuje používat průzkumné vyhledávání pro dříve přijaté hashe

**Zdrojový kód:** - `net.i2p.data.i2np.DatabaseLookupMessage` - Šifrování: `net.i2p.crypto.SessionKeyManager`

---

### DatabaseSearchReply (Typ 3)

**Účel:** Odpověď na neúspěšnou zprávu DatabaseLookup (dotaz do databáze).

**Obsah:** Seznam router hashů nejbližších k požadovanému klíči.

**Formát:**

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

**Zdrojový kód:** - `net.i2p.data.i2np.DatabaseSearchReplyMessage`

---

### DeliveryStatus (stav doručení, typ 10)

**Účel:** Jednoduché potvrzení přijetí zprávy. Toto potvrzení obvykle vytváří odesílatel zprávy a spolu se samotnou zprávou je zabaleno do Garlic Message (speciální typ zprávy v I2P), aby je příjemce vrátil.

**Obsah:** ID doručené zprávy a čas vytvoření nebo přijetí.

**Formát:**

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
**Poznámky:** - Časové razítko je vždy nastaveno tvůrcem na aktuální čas. V kódu však existuje několik použití a v budoucnu mohou přibýt další - Tato zpráva se také používá jako potvrzení o navázání relace v SSU. V tomto případě je ID zprávy nastaveno na náhodné číslo a "arrival time" je nastaven na aktuální síťové ID platné pro celou síť, které je 2 (tj., `0x0000000000000002`) - DeliveryStatus (zpráva potvrzení doručení) se obvykle zapouzdřuje do GarlicMessage a posílá se přes tunnel, aby poskytla potvrzení bez odhalení odesílatele - Používá se pro testování tunnel k měření latence a spolehlivosti

**Zdrojový kód:** - `net.i2p.data.i2np.DeliveryStatusMessage` - Použito v: `net.i2p.router.tunnel.InboundEndpointProcessor` pro testování tunnelu

---

### GarlicMessage (Typ 11)

**UPOZORNĚNÍ:** Toto je formát používaný pro garlic messages (zprávy typu garlic) šifrované pomocí ElGamalu. Formát pro ECIES-AEAD-X25519-Ratchet garlic messages je výrazně odlišný. Podívejte se na [ECIES Specification](/docs/specs/ecies/) pro moderní formát.

**Účel:** Slouží k zapouzdření více šifrovaných zpráv I2NP.

**Obsah:** Po dešifrování se jedná o sérii Garlic Cloves (jednotlivé části garlic zprávy) a doplňkových dat, která se také nazývá Clove Set (sada těchto částí).

**Šifrovaný formát:**

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
**Dešifrovaná data (Clove Set – sada dílčích zpráv):**

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

**Pro formát ECIES-X25519-AEAD-Ratchet (aktuální standard pro routers):**

Viz [Specifikaci ECIES](/docs/specs/ecies/) a [Návrh 144](/proposals/144-ecies-x25519-aead-ratchet/).

**Zdrojový kód:** - `net.i2p.data.i2np.GarlicMessage` - Šifrování: `net.i2p.crypto.elgamal.ElGamalAESEngine` (zastaralé) - Moderní šifrování: `net.i2p.crypto.ECIES` balíčky

---

### TunnelData (Typ 18)

**Účel:** Zpráva odeslaná ze vstupní brány nebo účastníka tunnelu k dalšímu účastníkovi nebo koncovému bodu. Data mají pevnou délku a obsahují zprávy I2NP, které jsou fragmentované, sdružované do dávek, doplněné vycpávkou a šifrované.

**Formát:**

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
**Struktura užitečných dat (1024 bajtů):**

```
Bytes 0-15: Initialization Vector (IV) for AES encryption
Bytes 16-1023: Encrypted tunnel message data (1008 bytes)
```
**Poznámky:** - ID zprávy I2NP pro TunnelData je na každém skoku nastaveno na nové náhodné číslo - Formát zprávy tunnel (uvnitř šifrovaných dat) je specifikován v [Specifikaci zprávy tunnel](/docs/specs/implementation/) - Každý skok dešifruje jednu vrstvu pomocí AES-256 v režimu CBC - IV se na každém skoku aktualizuje pomocí dešifrovaných dat - Celková velikost je přesně 1,028 bajtů (4 tunnelId + 1024 data) - Toto je základní jednotka provozu v tunnel - Zprávy TunnelData přenášejí fragmentované zprávy I2NP (GarlicMessage, DatabaseStore atd.)

**Zdrojový kód:** - `net.i2p.data.i2np.TunnelDataMessage` - Konstanta: `TunnelDataMessage.DATA_LENGTH = 1024` - Zpracování: `net.i2p.router.tunnel.InboundGatewayProcessor`

---

### TunnelGateway (Typ 19)

**Účel:** Zapouzdřuje další zprávu I2NP, která má být odeslána do tunnelu na jeho vstupní bráně.

**Formát:**

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
**Poznámky:** - Užitečná data jsou zpráva I2NP se standardní 16bajtovou hlavičkou - Používá se k vkládání zpráv do tunnels z místního routeru - Brána podle potřeby fragmentuje vloženou zprávu - Po fragmentaci jsou fragmenty zapouzdřeny do zpráv TunnelData - TunnelGateway se nikdy neposílá po síti; jde o interní typ zprávy používaný před zpracováním tunnelu

**Zdrojový kód:** - `net.i2p.data.i2np.TunnelGatewayMessage` - Zpracování: `net.i2p.router.tunnel.OutboundGatewayProcessor`

---

### DataMessage (typ 20)

**Účel:** Používá se v Garlic Messages (struktura zpráv v I2P) a Garlic Cloves (vložené podzprávy v rámci Garlic Messages) k zapouzdření libovolných dat (typicky end-to-end šifrovaných aplikačních dat).

**Formát:**

```
+----+----+----+----+----+----+-//-+
| length (4)            | data...    |
+----+----+----+----+----+----+-//-+

length :: 4 bytes
          Length of the payload

data :: $length bytes
        Actual payload of this message
```
**Poznámky:** - Tato zpráva neobsahuje žádné směrovací informace a nikdy nebude odeslána "neobalená" - Používá se pouze uvnitř Garlic messages (garlic zprávy) - Typicky obsahuje end-to-end šifrovaná aplikační data (HTTP, IRC, email atd.) - Data jsou obvykle šifrována pomocí ElGamal/AES nebo ECIES - Maximální praktická délka je přibližně 61,2 KB kvůli omezením fragmentace zpráv v tunnelu

**Zdrojový kód:** - `net.i2p.data.i2np.DataMessage`

---

### TunnelBuild (typ 21)

**ZASTARALÉ.** Použijte VariableTunnelBuild (typ 23) nebo ShortTunnelBuild (typ 25).

**Účel:** Požadavek na sestavení tunnelu pevné délky pro 8 skoků.

**Formát:**

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

**Zdrojový kód:** - `net.i2p.data.i2np.TunnelBuildMessage` - Konstanta: `TunnelBuildMessageBase.MAX_RECORD_COUNT = 8`

---

### TunnelBuildReply (Typ 22)

**ZASTARALÉ.** Použijte VariableTunnelBuildReply (typ 24) nebo OutboundTunnelBuildReply (typ 26).

**Účel:** Odpověď pro sestavení tunnelu s pevnou délkou pro 8 skoků.

**Formát:**

Stejný formát jako u TunnelBuildMessage, s BuildResponseRecords namísto BuildRequestRecords.

```
Total size: 8 × 528 = 4,224 bytes
```
**Poznámky:** - Od verze 0.9.48 může obsahovat ECIES-X25519 BuildResponseRecords (záznamy odpovědí pro sestavení pomocí ECIES-X25519). Viz [Vytváření ECIES tunnelu](/docs/specs/implementation/) - Podrobnosti viz [Specifikace vytváření tunnelu](/docs/specs/implementation/) - ID zprávy I2NP pro tuto zprávu musí být nastaveno podle specifikace vytváření tunnelu - Ačkoli se v dnešní síti vyskytuje zřídka (nahrazeno VariableTunnelBuildReply), může být stále použito pro velmi dlouhé tunnely a nebylo formálně označeno jako zastaralé - Routers to stále musí implementovat kvůli kompatibilitě

**Zdrojový kód:** - `net.i2p.data.i2np.TunnelBuildReplyMessage`

---

### VariableTunnelBuild (Typ 23)

**Účel:** Sestavení tunnelu s proměnnou délkou pro 1-8 skoků. Podporuje jak routery ElGamal, tak ECIES-X25519.

**Formát:**

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
**Poznámky:** - Od verze 0.9.48 může obsahovat ECIES-X25519 (schéma ECIES s křivkou X25519) BuildRequestRecords (záznamy požadavku na sestavení). Viz [Vytváření ECIES tunnelů](/docs/specs/implementation/) - Zavedeno ve verzi routeru 0.7.12 (2009) - Nemá být posíláno účastníkům tunnelu s verzí starší než 0.7.12 - Podrobnosti viz [Specifikace vytváření tunnelů](/docs/specs/implementation/) - ID zprávy I2NP musí být nastaveno podle specifikace vytváření tunnelu - **Obvyklý počet záznamů:** 4 (pro 4-hopový tunnel) - **Obvyklá celková velikost:** 1 + (4 × 528) = 2,113 bajtů - Toto je standardní zpráva pro sestavení tunnelu pro ElGamal routery - ECIES routery obvykle místo toho používají ShortTunnelBuild (zpráva pro krátkou výstavbu tunnelu; typ 25)

**Zdrojový kód:** - `net.i2p.data.i2np.VariableTunnelBuildMessage`

---

### VariableTunnelBuildReply (Typ 24)

**Účel:** Odpověď na sestavení tunnel s proměnnou délkou pro 1-8 skoků. Podporuje jak ElGamal, tak ECIES-X25519 routers.

**Formát:**

Stejný formát jako VariableTunnelBuildMessage, s BuildResponseRecords namísto BuildRequestRecords.

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
**Poznámky:** - Od verze 0.9.48 může obsahovat ECIES-X25519 BuildResponseRecords. Viz [Vytváření tunnelu ECIES](/docs/specs/implementation/) - Zavedeno ve verzi routeru 0.7.12 (2009) - Nesmí být odesíláno účastníkům tunnelu s verzí starší než 0.7.12 - Podrobnosti viz [Specifikace vytváření tunnelu](/docs/specs/implementation/) - ID zprávy I2NP musí být nastaveno podle specifikace vytváření tunnelu - **Typický počet záznamů:** 4 - **Typická celková velikost:** 2,113 bajtů

**Zdrojový kód:** - `net.i2p.data.i2np.VariableTunnelBuildReplyMessage`

---

### ShortTunnelBuild (Typ 25)

**Účel:** Krátké zprávy pro sestavení tunnelů pouze pro ECIES-X25519 routers. Zavedeno ve verzi API 0.9.51 (vydání 1.5.0, srpen 2021). Toto je aktuální standard pro ECIES sestavování tunnelů.

**Formát:**

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
**Poznámky:** - Zavedeno ve verzi routeru 0.9.51 (vydání 1.5.0, srpen 2021) - Nesmí být odesíláno účastníkům tunnelu dříve než od verze API 0.9.51 - Viz [Vytváření ECIES Tunnel](/docs/specs/implementation/) pro úplnou specifikaci - Viz [Návrh 157](/proposals/157-new-tbm/) pro zdůvodnění - **Typický počet záznamů:** 4 - **Typická celková velikost:** 1 + (4 × 218) = 873 bajtů - **Úspora šířky pásma:** o 59% menší než VariableTunnelBuild (873 vs 2,113 bajtů) - **Výkonnostní přínos:** 4 krátké záznamy se vejdou do jedné tunnel zprávy; VariableTunnelBuild vyžaduje 3 tunnel zprávy - Toto je nyní standardní formát sestavení tunnelu pro čisté ECIES-X25519 tunnely - Záznamy odvozují klíče pomocí HKDF místo jejich explicitního zahrnutí

**Zdrojový kód:** - `net.i2p.data.i2np.ShortTunnelBuildMessage` - Konstanta: `ShortEncryptedBuildRecord.RECORD_SIZE = 218`

---

### OutboundTunnelBuildReply (Typ 26)

**Účel:** Odesláno z výstupního koncového bodu nového tunnel iniciátorovi. Pouze pro ECIES-X25519 routers. Zavedeno v API verzi 0.9.51 (vydání 1.5.0, srpen 2021).

**Formát:**

Stejný formát jako ShortTunnelBuildMessage, s ShortBuildResponseRecords namísto ShortBuildRequestRecords.

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
**Poznámky:** - Zavedeno ve verzi router 0.9.51 (vydání 1.5.0, srpen 2021) - Viz [ECIES Tunnel Creation](/docs/specs/implementation/) pro úplnou specifikaci - **Typický počet záznamů:** 4 - **Typická celková velikost:** 873 bajtů - Tato odpověď je odeslána z odchozího koncového bodu (OBEP) zpět k tvůrci tunnel přes nově vytvořený odchozí tunnel - Poskytuje potvrzení, že všechny skoky přijaly sestavení tunnel

**Zdrojový kód:** - `net.i2p.data.i2np.OutboundTunnelBuildReplyMessage`

---

## Reference

### Oficiální specifikace

- **[Specifikace I2NP](/docs/specs/i2np/)** - Kompletní specifikace formátu zpráv I2NP
- **[Společné struktury](/docs/specs/common-structures/)** - Datové typy a struktury používané napříč I2P
- **[Vytváření tunnel](/docs/specs/implementation/)** - Vytváření tunnel pomocí ElGamal (zastaralé)
- **[Vytváření tunnel ECIES](/docs/specs/implementation/)** - Vytváření tunnel s ECIES-X25519 (aktuální)
- **[Zpráva pro tunnel](/docs/specs/implementation/)** - Formát zprávy pro tunnel a pokyny k doručení
- **[Specifikace NTCP2](/docs/specs/ntcp2/)** - Transportní protokol TCP
- **[Specifikace SSU2](/docs/specs/ssu2/)** - Transportní protokol UDP
- **[Specifikace ECIES](/docs/specs/ecies/)** - Šifrování ECIES-X25519-AEAD-Ratchet (krokovací mechanismus)
- **[Specifikace kryptografie](/docs/specs/cryptography/)** - Nízkoúrovňová kryptografická primitiva
- **[Specifikace I2CP](/docs/specs/i2cp/)** - Specifikace klientského protokolu
- **[Specifikace datagramů](/docs/api/datagrams/)** - Formáty Datagram2 a Datagram3

### Návrhy

- **[Návrh 123](/proposals/123-new-netdb-entries/)** - Nové záznamy netDB (LeaseSet2, EncryptedLeaseSet, MetaLeaseSet)
- **[Návrh 144](/proposals/144-ecies-x25519-aead-ratchet/)** - Šifrování ECIES-X25519-AEAD-Ratchet
- **[Návrh 154](/proposals/154-ecies-lookups/)** - Šifrované vyhledávání v databázi
- **[Návrh 156](/proposals/156-ecies-routers/)** - ECIES routery
- **[Návrh 157](/proposals/157-new-tbm/)** - Menší zprávy pro sestavení tunnel (krátký formát)
- **[Návrh 159](/proposals/159-ssu2/)** - Transport SSU2
- **[Návrh 161](/cs/proposals/161-ri-dest-padding/)** - Komprimovatelná výplň
- **[Návrh 163](/proposals/163-datagram2/)** - Datagram2 a Datagram3
- **[Návrh 167](/proposals/167-service-records/)** - Parametry záznamu služby LeaseSet
- **[Návrh 168](/proposals/168-tunnel-bandwidth/)** - Parametry šířky pásma pro sestavení tunnel
- **[Návrh 169](/proposals/169-pq-crypto/)** - Postkvantová hybridní kryptografie

### Dokumentace

- **[Garlic Routing](/docs/overview/garlic-routing/)** - Vrstvené seskupování zpráv
- **[ElGamal/AES](/docs/legacy/elgamal-aes/)** - Zastaralé šifrovací schéma
- **[Implementace tunnelu](/docs/specs/implementation/)** - Fragmentace a zpracování
- **[Síťová databáze](/docs/specs/common-structures/)** - Distribuovaná hašovací tabulka
- **[Transport NTCP2](/docs/specs/ntcp2/)** - Specifikace transportu TCP
- **[Transport SSU2](/docs/specs/ssu2/)** - Specifikace transportu UDP
- **[Technický úvod](/docs/overview/tech-intro/)** - Přehled architektury I2P

### Zdrojový kód

- **[Repozitář Java I2P](https://i2pgit.org/I2P_Developers/i2p.i2p)** - Oficiální implementace v jazyce Java
- **[Zrcadlo na GitHubu](https://github.com/i2p/i2p.i2p)** - GitHubové zrcadlo Java I2P
- **[Repozitář i2pd](https://github.com/PurpleI2P/i2pd)** - Implementace v C++

### Klíčová umístění zdrojového kódu

**Java I2P (i2pgit.org/I2P_Developers/i2p.i2p):** - `core/java/src/net/i2p/data/i2np/` - implementace zpráv I2NP - `core/java/src/net/i2p/crypto/` - kryptografické implementace - `router/java/src/net/i2p/router/tunnel/` - zpracování tunnelu - `router/java/src/net/i2p/router/transport/` - implementace transportu

**Konstanty a hodnoty:** - `I2NPMessage.MAX_SIZE = 65536` - Maximální velikost zprávy I2NP - `I2NPMessageImpl.HEADER_LENGTH = 16` - Standardní velikost hlavičky - `TunnelDataMessage.DATA_LENGTH = 1024` - Užitečná data zprávy Tunnel - `EncryptedBuildRecord.RECORD_SIZE = 528` - Dlouhý záznam sestavení - `ShortEncryptedBuildRecord.RECORD_SIZE = 218` - Krátký záznam sestavení - `TunnelBuildMessageBase.MAX_RECORD_COUNT = 8` - Max. počet záznamů na jedno sestavení

---

## Příloha A: Statistiky sítě a aktuální stav

### Složení sítě (stav k říjnu 2025)

- **Celkový počet routers:** Přibližně 60,000-70,000 (liší se)
- **Floodfill routers:** Přibližně 500-700 aktivních
- **Typy šifrování:**
  - ECIES-X25519: >95% routerů
  - ElGamal: <5% routerů (zastaralé, pouze pro zpětnou kompatibilitu)
- **Rozšíření transportů:**
  - SSU2: >60% jako primární transport
  - NTCP2: ~40% jako primární transport
  - Zastaralé transporty (SSU1, NTCP): 0% (odstraněno)
- **Typy podpisů:**
  - EdDSA (Ed25519): drtivá většina
  - ECDSA: malé procento
  - RSA: nepovoleno (odstraněno)

### Minimální požadavky na router

- **Verze API:** 0.9.16+ (pro kompatibilitu EdDSA se sítí)
- **Doporučené minimum:** API 0.9.51+ (sestavení krátkých tunnelů ECIES)
- **Aktuální minimum pro floodfills (uzly udržující netDb):** API 0.9.58+ (zastarání routerů ElGamal)
- **Nadcházející požadavek:** Java 17+ (od vydání 2.11.0, prosinec 2025)

### Požadavky na šířku pásma

- **Minimální:** 128 KBytes/sec (příznak N nebo vyšší) pro floodfill
- **Doporučeno:** 256 KBytes/sec (příznak O) nebo vyšší
- **Požadavky floodfill:**
  - Minimálně 128 KB/sec šířky pásma
  - Stabilní doba běhu (>95% doporučeno)
  - Nízká latence (<500ms k peerům)
  - Splnit testy kondice (doba ve frontě, zpoždění úloh)

### Statistiky tunnelů

- **Typická délka tunnelu:** 3-4 skoky
- **Maximální délka tunnelu:** 8 skoků (teoretická, zřídka používaná)
- **Typická životnost tunnelu:** 10 minut
- **Úspěšnost sestavení tunnelu:** >85% u dobře propojených routerů
- **Formát zprávy pro sestavení tunnelu:**
  - ECIES routery: ShortTunnelBuild (záznamy o velikosti 218 bajtů)
  - Smíšené tunnely: VariableTunnelBuild (záznamy o velikosti 528 bajtů)

### Metriky výkonu

- **Doba sestavení tunnelu:** 1-3 sekundy (typicky)
- **End-to-end latence:** 0.5-2 sekundy (typicky, celkem 6-8 skoků)
- **Propustnost:** Omezená šířkou pásma tunnelu (typicky 10-50 KB/sec na tunnel)
- **Maximální velikost datagramu:** 10 KB doporučeno (teoretické maximum 61.2 KB)

---

## Příloha B: Zastaralé a odstraněné funkce

### Zcela odstraněno (již není podporováno)

- **NTCP transport** - Odstraněno ve verzi 0.9.50 (květen 2021)
- **SSU v1 transport** - Odstraněno z Java I2P ve verzi 2.4.0 (prosinec 2023)
- **SSU v1 transport** - Odstraněno z i2pd ve verzi 2.44.0 (listopad 2022)
- **Typy podpisů RSA** - Nepovoleno od API 0.9.28

### Zastaralé (podporováno, ale nedoporučuje se)

- **ElGamal routers** - Zastaralé od API 0.9.58 (březen 2023)
  - ElGamal destinace jsou nadále podporovány kvůli zpětné kompatibilitě
  - Nové routers by měly používat výhradně ECIES-X25519
- **TunnelBuild (typ 21)** - Zastaralé ve prospěch VariableTunnelBuild a ShortTunnelBuild
  - Stále implementováno pro velmi dlouhé tunnels (>8 skoků)
- **TunnelBuildReply (typ 22)** - Zastaralé ve prospěch VariableTunnelBuildReply a OutboundTunnelBuildReply
- **Šifrování ElGamal/AES** - Zastaralé ve prospěch ECIES-X25519-AEAD-Ratchet
  - Stále používáno pro starší destinace
- **Dlouhé ECIES BuildRequestRecords (528 bajtů)** - Zastaralé ve prospěch krátkého formátu (218 bajtů)
  - Stále používáno pro smíšené tunnels s ElGamal skoky

### Časová osa podpory starších verzí

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

## Příloha C: Budoucí vývoj

### Postkvantová kryptografie

**Stav:** Beta od vydání 2.10.0 (září 2025), stane se výchozí ve vydání 2.11.0 (prosinec 2025)

**Implementace:** - Hybridní přístup kombinující klasické X25519 a postkvantové MLKEM (ML-KEM-768) - Zpětně kompatibilní se stávající infrastrukturou ECIES-X25519 - Používá Signal Double Ratchet (mechanismus postupné výměny klíčů) s klasickým i postkvantovým klíčovým materiálem - Podrobnosti viz [Návrh 169](/proposals/169-pq-crypto/)

**Migrační postup:** 1. Verze 2.10.0 (září 2025): K dispozici jako volitelná beta 2. Verze 2.11.0 (prosinec 2025): Povoleno ve výchozím nastavení 3. Budoucí verze: Nakonec povinné

### Plánované funkce

- **Vylepšení pro IPv6** - Lepší podpora IPv6 a přechodové mechanismy
- **Omezování na úrovni tunnel** - Jemně odstupňované řízení šířky pásma pro každý tunnel
- **Vylepšené metriky** - Lepší monitoring výkonu a diagnostika
- **Optimalizace protokolů** - Snížená režie a vyšší efektivita
- **Vylepšený výběr floodfill** - Lepší distribuce síťové databáze

### Výzkumné oblasti

- **Optimalizace délky tunnelu** - Dynamická délka tunnelu na základě modelu hrozeb
- **Pokročilý padding (výplň dat)** - Vylepšení odolnosti proti analýze provozu
- **Nová šifrovací schémata** - Příprava na hrozby kvantového výpočetnictví
- **Řízení zahlcení** - Lepší zvládání zátěže sítě
- **Podpora mobilních zařízení** - Optimalizace pro mobilní zařízení a sítě

---

## Příloha D: Pokyny k implementaci

### Pro nové implementace

**Minimální požadavky:** 1. Podporovat funkce API ve verzi 0.9.51+ 2. Implementovat šifrování ECIES-X25519-AEAD-Ratchet 3. Podporovat transporty NTCP2 a SSU2 4. Implementovat zprávy ShortTunnelBuild (záznamy o velikosti 218 bajtů) 5. Podporovat varianty LeaseSet2 (typy 3, 5, 7) 6. Používat podpisy EdDSA (Ed25519)

**Doporučeno:** 1. Podporovat postkvantovou hybridní kryptografii (od verze 2.11.0) 2. Implementovat parametry šířky pásma pro každý tunnel 3. Podporovat formáty Datagram2 a Datagram3 4. Implementovat možnosti záznamu služby v LeaseSets 5. Dodržovat oficiální specifikace na /docs/specs/

**Není vyžadováno:** 1. Podpora routeru ElGamal (zastaralé) 2. Podpora staršího transportu (SSU1, NTCP) 3. Dlouhé ECIES BuildRequestRecords (528 bajtů pro čisté ECIES tunnels) 4. Zprávy TunnelBuild/TunnelBuildReply (použijte varianty Variable nebo Short)

### Testování a validace

**Soulad s protokolem:** 1. Otestujte interoperabilitu s oficiální Java I2P router 2. Otestujte interoperabilitu s i2pd C++ router 3. Ověřte formáty zpráv podle specifikací 4. Otestujte cykly sestavení/zrušení tunnel 5. Ověřte šifrování/dešifrování pomocí testovacích vektorů

**Testování výkonu:** 1. Změřte míru úspěšnosti sestavování tunnel (měla by být >85%) 2. Testujte s různými délkami tunnel (2-8 hopů) 3. Ověřte správnou fragmentaci a znovusestavení 4. Testujte pod zátěží (více současných tunnel) 5. Změřte end-to-end latenci

**Testování zabezpečení:** 1. Ověřit implementaci šifrování (použít testovací vektory) 2. Otestovat prevenci útoků typu replay 3. Ověřit zpracování vypršení platnosti zpráv 4. Testovat proti nesprávně formátovaným zprávám 5. Ověřit správnou generaci náhodných čísel

### Častá úskalí implementace

1. **Matoucí formáty pokynů k doručení** - garlic clove (jednotlivá část v garlic zprávě) vs tunnel message
2. **Nesprávné odvozování klíčů** - použití HKDF pro krátké záznamy sestavení
3. **Zpracování ID zprávy** - Není správně nastavováno pro tunnel builds
4. **Problémy s fragmentací** - Nerespektování praktického limitu 61,2 KB
5. **Chyby endianness (pořadí bajtů)** - Java používá big-endian pro všechna celá čísla
6. **Zpracování expirace** - Krátký formát se přetočí 7. února 2106
7. **Generování kontrolního součtu** - Pořád vyžadováno, i když se neověřuje
