---
title: "Specifikace aktualizace softwaru"
description: "Bezpečný mechanismus podepsaných aktualizací a struktura kanálu pro I2P routers"
slug: "updates"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## Přehled

Router automaticky kontroluje aktualizace průběžným dotazováním podepsaného kanálu novinek distribuovaného prostřednictvím sítě I2P. Když je oznámena novější verze, router stáhne kryptograficky podepsaný aktualizační archiv (`.su3`) a připraví jej k instalaci. Tento systém zajišťuje **ověřenou, vůči manipulaci odolnou** a **vícekanálovou** distribuci oficiálních vydání.

Od verze I2P 2.10.0 používá systém aktualizací: - **RSA-4096 / SHA-512** podpisy - **kontejnerový formát SU3** (nahrazující zastaralé SUD/SU2) - **Redundantní zrcadla:** HTTP v síti, clearnet HTTPS (veřejný internet) a BitTorrent

---

## 1. Kanál novinek

Routery každých několik hodin pravidelně načítají podepsaný kanál Atom, aby zjistily nové verze a bezpečnostní upozornění.   Kanál je podepsaný a distribuován jako soubor `.su3`, který může obsahovat:

- `<i2p:version>` — nové číslo verze  
- `<i2p:minVersion>` — minimální podporovaná verze routeru  
- `<i2p:minJavaVersion>` — požadované minimální běhové prostředí Java  
- `<i2p:update>` — uvádí více zrcadel ke stažení (I2P, HTTPS, torrent)  
- `<i2p:revocations>` — data o revokaci certifikátů  
- `<i2p:blocklist>` — blokovací seznamy na úrovni sítě pro kompromitované uzly

### Distribuce kanálu

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Channel</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2P HTTP (eepsite)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Primary update source</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Private, resilient</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Clearnet HTTPS</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fallback mirror</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Public fallback</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>BitTorrent magnet</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Distributed channel</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Reduces mirror load</td>
    </tr>
  </tbody>
</table>
Routers dávají přednost I2P kanálu, ale v případě potřeby se mohou uchýlit k distribuci přes clearnet (veřejný internet) nebo k torrentové distribuci.

---

## 2. Formáty souborů

### SU3 (aktuální standard)

Zavedeno ve verzi 0.9.9, SU3 nahradilo starší formáty SUD a SU2. Každý soubor obsahuje hlavičku, užitečná data a koncový podpis.

**Struktura hlavičky** <table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">   <thead>

    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
    </tr>
</thead>   <tbody>

    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Magic</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>"I2Psu3"</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Format Version</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>0</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature Type</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">e.g., <code>0x000B</code> (RSA-SHA512-4096)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature Length</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>512 bytes</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Version String</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Router version</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signer ID</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Certificate name</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Content Type</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1 = router update, 3 = reseed, 4 = news feed</td>
    </tr>
</tbody> </table>

**Kroky ověření podpisu** 1. Parsujte hlavičku a identifikujte algoritmus podpisu.   2. Ověřte hash a podpis pomocí uloženého certifikátu podepisujícího.   3. Potvrďte, že certifikát podepisujícího není revokován.   4. Porovnejte vložený řetězec verze s metadaty užitečných dat.

Routers jsou dodávány s důvěryhodnými certifikáty podepisovatelů (aktuálně **zzz** a **str4d**) a odmítají jakékoli nepodepsané nebo odvolané zdroje.

### SU2 (Zastaralé)

- Používala se přípona `.su2` u JAR souborů komprimovaných pomocí Pack200.  
- Odstraněno poté, co Java 14 označila Pack200 za zastaralý (JEP 367).  
- Deaktivováno v I2P 0.9.48+; nyní plně nahrazeno kompresí ZIP.

### SUD (zastaralé)

- Raný formát ZIP podepsaný DSA-SHA1 (pre-0.9.9).  
- Chybí ID podepisujícího i hlavička, omezená integrita.  
- Nahrazen kvůli slabé kryptografii a chybějícímu vynucování verzí.

---

## 3. Pracovní postup aktualizace

### 3.1 Ověření hlavičky

Routers načítají pouze **hlavičku SU3**, aby ověřily řetězec verze před stažením celých souborů.   To zabraňuje plýtvání šířkou pásma na neaktuálních zrcadlech nebo zastaralých verzích.

### 3.2 Úplné stažení

Po ověření hlavičky router stáhne celý soubor `.su3` z: - Zrcadel eepsite uvnitř sítě (preferováno)   - Zrcadel na clearnetu (veřejný internet) přes HTTPS (záložní)   - BitTorrentu (volitelná distribuce s asistencí peerů)

Stahování používají standardní HTTP klienty I2PTunnel, s opakováním pokusů, obsluhou časových limitů a přepínáním na zrcadla.

### 3.3 Ověření podpisu

Každý stažený soubor prochází: - **Kontrola podpisu:** ověření RSA-4096/SHA512   - **Shoda verzí:** kontrola shody verze hlavičky a datové části   - **Zabránění snížení verze:** zajišťuje, že aktualizace je novější než nainstalovaná verze

Neplatné nebo neodpovídající soubory jsou okamžitě zahazovány.

### 3.4 Příprava instalace

Po ověření: 1. Rozbalte obsah ZIPu do dočasného adresáře   2. Odstraňte soubory uvedené v `deletelist.txt`   3. Nahraďte nativní knihovny, pokud je součástí `lib/jbigi.jar`   4. Zkopírujte certifikáty podepisovatele do `~/.i2p/certificates/`   5. Uložte aktualizaci jako `i2pupdate.zip`, aby se použila při příštím restartu

Aktualizace se nainstaluje automaticky při příštím spuštění nebo když je ručně vyvolána možnost „Nainstalovat aktualizaci nyní“.

---

## 4. Správa souborů

### deletelist.txt

Seznam v prostém textu zastaralých souborů, které je třeba odstranit před rozbalením nového obsahu.

**Pravidla:** - Jedna cesta na řádek (pouze relativní cesty) - Řádky začínající znakem `#` se ignorují - `..` a absolutní cesty jsou odmítnuty

### Nativní knihovny

Aby se předešlo zastaralým nebo neodpovídajícím nativním binárním souborům: - Pokud existuje `lib/jbigi.jar`, staré soubory `.so` nebo `.dll` jsou odstraněny   - Zajišťuje, že knihovny specifické pro danou platformu jsou znovu rozbaleny

---

## 5. Správa certifikátů

Routers mohou přijímat **nové certifikáty podepisovatele** prostřednictvím aktualizací nebo revokací v kanálu novinek.

- Nové soubory `.crt` jsou zkopírovány do adresáře s certifikáty.  
- Odvolané certifikáty jsou před dalšími ověřeními smazány.  
- Podporuje rotaci klíčů bez nutnosti ručního zásahu uživatele.

Všechny aktualizace jsou podepisovány offline pomocí **air-gapped signing systems** (systémy pro podepisování fyzicky izolované od sítě).   Soukromé klíče nejsou nikdy ukládány na sestavovacích serverech.

---

## 6. Pokyny pro vývojáře

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Topic</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Details</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Signing</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Use RSA-4096 (SHA-512) via <code>apps/jetty/news</code> SU3 tooling.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Mirror Policy</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P eepsite preferred, clearnet HTTPS fallback, torrent optional.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Testing</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Validate updates from prior releases, across all OS platforms.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Version Enforcement</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>minVersion</code> prevents incompatible upgrades.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Certificate Rotation</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Distribute new certs in updates and revocation lists.</td>
    </tr>
  </tbody>
</table>
Budoucí vydání se zaměří na integraci postkvantových podpisů (viz Proposal 169) a na reprodukovatelná sestavení.

---

## 7. Přehled zabezpečení

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Threat</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Mitigation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Tampering</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Cryptographic signature (RSA-4096/SHA512)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Key Compromise</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Feed-based certificate revocation</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Downgrade Attack</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Version comparison enforcement</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Mirror Hijack</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Signature verification, multiple mirrors</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>DoS</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Fallback to alternate mirrors/torrents</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>MITM</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HTTPS transport + signature-level integrity</td>
    </tr>
  </tbody>
</table>
---

## 8. Verzování

- Router: **2.10.0 (API 0.9.67)**  
- Sémantické verzování s `Major.Minor.Patch`.  
- Vynucování minimální verze brání nebezpečným aktualizacím.  
- Podporované verze Javy: **Java 8–17**. Budoucí verze 2.11.0+ bude vyžadovat Javu 17+.

---
