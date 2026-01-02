---
title: "Vkládání I2P do vaší aplikace"
description: "Aktualizované praktické pokyny pro odpovědné začlenění I2P routeru do vaší aplikace"
slug: "embedding"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

Začlenění I2P do vaší aplikace je účinný způsob, jak přilákat uživatele—ale pouze pokud je router nakonfigurován odpovědně.

## 1. Koordinace s týmy routerů

- Kontaktujte správce **Java I2P** a **i2pd** před začleněním do balíčku. Mohou zkontrolovat vaše výchozí nastavení a upozornit na problémy s kompatibilitou.
- Vyberte implementaci routeru, která odpovídá vašemu zásobníku:
  - **Java/Scala** → Java I2P
  - **C/C++** → i2pd
  - **Ostatní jazyky** → začleňte router do balíčku a integrujte pomocí [SAM v3](/docs/api/samv3/) nebo [I2CP](/docs/specs/i2cp/)
- Ověřte podmínky redistribuce pro binární soubory routeru a závislosti (Java runtime, ICU, atd.).

## 2. Doporučená výchozí konfigurace

Snažte se „přispívat více, než spotřebováváte." Moderní výchozí nastavení upřednostňuje zdraví a stabilitu sítě.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Setting</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended Default (2025)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Bandwidth share</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">80% for participating tunnels </td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Tunnel quantities</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2pd: 3 inbound / 3 outbound; Java I2P: 2 inbound / 2 outbound. </td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature &amp; encryption</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Use Ed25519 (<code>SIGNATURE_TYPE=7</code>) and advertise ECIES-X25519 + ElGamal (<code>i2cp.leaseSetEncType=4,0</code>).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Client protocols</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Use SAM v3 or I2CP.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">API listeners</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Bind SAM/I2CP to <code>127.0.0.1</code> only. Disable if not needed.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UI toggles</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Expose bandwidth controls, logs, and an opt-in checkbox for participating tunnels.</td>
    </tr>
  </tbody>
</table>
### Zúčastněné tunely zůstávají nezbytné

**Nedeaktivujte** tunely pro účast.

1. Routery, které nepřenášejí provoz, fungují sami hůře.
2. Síť závisí na dobrovolném sdílení kapacity.
3. Krycí provoz (přenášený provoz) zlepšuje anonymitu.

**Oficiální minima:** - Sdílená šířka pásma: ≥ 12 KB/s   - Automatické zapojení jako floodfill: ≥ 128 KB/s   - Doporučeno: 2 příchozí / 2 odchozí tunnely (výchozí nastavení Java I2P)

## 3. Perzistence a Reseeding

Adresáře s trvalým stavem (`netDb/`, profily, certifikáty) musí být zachovány mezi spuštěními.

Bez perzistence budou vaši uživatelé spouštět reseedy při každém startu—což zhoršuje výkon a zvyšuje zátěž na reseed servery.

Pokud není perzistence možná (např. kontejnery nebo dočasné instalace):

1. Zahrňte **1 000–2 000 router infos** do instalátoru.  
2. Provozujte jeden nebo více vlastních reseed serverů pro odlehčení veřejným serverům.

Konfigurační proměnné: - Základní adresář: `i2p.dir.base` - Konfigurační adresář: `i2p.dir.config` - Zahrnuje `certificates/` pro reseed (obnovení dat sítě).

## 4. Bezpečnost a odhalení

- Ponechte konzoli routeru (`127.0.0.1:7657`) pouze pro lokální přístup.
- Pokud zpřístupňujete UI externě, použijte HTTPS.
- Zakažte externí SAM/I2CP, pokud není vyžadováno.
- Zkontrolujte zahrnuté pluginy—dodávejte pouze ty, které vaše aplikace podporuje.
- Vždy zahrňte autentizaci pro vzdálený přístup ke konzoli.

**Bezpečnostní funkce zavedené od verze 2.5.0:** - Izolace NetDB mezi aplikacemi (2.4.0+)   - Zmírnění DoS a Tor bloklisty (2.5.1)   - Odolnost NTCP2 proti skenování (2.9.0)   - Vylepšení výběru floodfill routerů (2.6.0+)

## 5. Podporovaná API (2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">API</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SAM v3 (3.3)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Active</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Recommended bridge for non-Java apps.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2CP</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Active</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stable protocol core, used internally by Java I2P.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2PControl</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Active</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">JSON-RPC API; plugin maintained.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>BOB</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">⚠️ Deprecated</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Removed from Java I2P since 1.7.0; use SAM v3 instead.</td>
    </tr>
  </tbody>
</table>
Veškerá oficiální dokumentace se nachází v `/docs/api/` — stará cesta `/spec/samv3/` **neexistuje**.

## 6. Síťové připojení a porty

Typické výchozí porty: - 4444 – HTTP proxy   - 4445 – HTTPS proxy   - 7654 – I2CP   - 7656 – SAM Bridge   - 7657 – Konzole routeru   - 7658 – Lokální I2P stránka   - 6668 – IRC proxy   - 9000–31000 – Náhodný port routeru (UDP/TCP příchozí)

Routery si při prvním spuštění vyberou náhodný příchozí port. Přesměrování portů zlepšuje výkon, ale UPnP to může zvládnout automaticky.

## 7. Moderní změny (2024–2025)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Change</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Status</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Details</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SSU1 Transport</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Removed</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SSU2 is now the exclusive UDP transport.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2P-over-Tor</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Blocked</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Since 2.6.0 (July 2024).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Datagram2/3</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Added</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Authenticated, repliable datagram formats (2.9.0).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>LeaseSet service records</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Added</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Enables service discovery (Proposal 167).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Tunnel build parameters</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Improved</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Adaptive congestion handling (2.9.0+).</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Post-quantum crypto</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Introduced (beta)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">ML-KEM hybrid ratchet, opt-in from 2.10.0.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Java 17 requirement</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Announced</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Becomes mandatory in 2.11.0 (early 2026).</td>
    </tr>
  </tbody>
</table>
## 8. Uživatelská zkušenost a testování

- Komunikovat, co I2P dělá a proč je šířka pásma sdílena.
- Poskytnout diagnostiku routeru (šířka pásma, tunnely, stav reseedu).
- Testovat balíčky na Windows, macOS a Linuxu (včetně verzí pro nízkou RAM).
- Ověřit interoperabilitu s peery **Java I2P** i **i2pd**.
- Testovat obnovu po výpadcích sítě a nekorektních ukončeních.

## 9. Komunitní zdroje

- Fórum: [i2pforum.net](https://i2pforum.net) nebo `http://i2pforum.i2p` uvnitř I2P.  
- Kód: [i2pgit.org/I2P_Developers/i2p.i2p](https://i2pgit.org/I2P_Developers/i2p.i2p).  
- IRC (síť Irc2P): `#i2p-dev`, `#i2pd`.  
  - `#i2papps` neověřeno; možná neexistuje.  
  - Upřesněte, která síť (Irc2P vs ilita.i2p) hostuje váš kanál.

Zodpovědné začlenění znamená vyvážení uživatelského komfortu, výkonu a přínosu pro síť. Používejte tato výchozí nastavení, zůstaňte synchronizováni s vývojáři routeru a testujte pod reálným zatížením před vydáním.
