---
title: "SOCKS Proxy"
description: "Bezpečné používání SOCKS tunelu I2P (aktualizováno pro verzi 2.10.0)"
slug: "socks"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

> **Upozornění:** SOCKS tunel přeposílá datové části aplikací bez jejich sanitizace. Mnoho protokolů prozrazuje IP adresy, názvy hostitelů nebo jiné identifikátory. SOCKS používejte pouze se softwarem, který jste prověřili z hlediska anonymity.

---

## 1. Přehled

I2P poskytuje podporu proxy **SOCKS 4, 4a a 5** pro odchozí spojení prostřednictvím **I2PTunnel klienta**. Umožňuje standardním aplikacím přístup k I2P destinacím, ale **nemůže přistupovat na clearnet**. Neexistuje žádný **SOCKS outproxy** a veškerý provoz zůstává v rámci sítě I2P.

### Shrnutí implementace

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Parameter</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Java I2P</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">i2pd</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Default Port</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">User-defined</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>127.0.0.1:4447</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported SOCKS Versions</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4, 4a, 5</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4, 4a, 5</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UDP Mode</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stubbed (non-functional)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stubbed (non-functional)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Persistent Keys</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅ Since 0.9.9</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">✅</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Shared Client Tunnels</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Outproxy Support</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">❌ None</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">❌ None</td>
    </tr>
  </tbody>
</table>
**Podporované typy adres:** - `.i2p` hostitelská jména (záznamy v adresáři) - Base32 hashe (`.b32.i2p`) - Bez podpory Base64 nebo běžného internetu

---

## 2. Bezpečnostní rizika a omezení

### Únik na aplikační vrstvě

SOCKS pracuje pod aplikační vrstvou a nemůže sanitizovat protokoly. Mnoho klientů (např. prohlížeče, IRC, e-mail) zahrnuje metadata, která odhalují vaši IP adresu, název hostitele nebo podrobnosti o systému.

Běžné úniky zahrnují: - IP adresy v hlavičkách e-mailů nebo IRC CTCP odpovědích   - Skutečná jména/uživatelská jména v protokolových datech   - Řetězce user-agent s otisky OS   - Externí DNS dotazy   - WebRTC a telemetrii prohlížeče

**I2P nemůže zabránit těmto únikům**—dochází k nim nad vrstvou tunelů. SOCKS používejte pouze pro **auditované klienty** navržené pro anonymitu.

### Sdílená identita tunelu

Pokud několik aplikací sdílí SOCKS tunel, sdílejí stejnou identitu I2P destinace. To umožňuje korelaci nebo otisk prstu napříč různými službami.

**Zmírnění:** Použijte **nesdílené tunnely** pro každou aplikaci a povolte **trvalé klíče** pro udržení konzistentních kryptografických identit napříč restarty.

### Režim UDP není implementován

Podpora UDP v SOCKS5 není implementována. Protokol inzeruje schopnost UDP, ale volání jsou ignorována. Používejte pouze klienty podporující TCP.

### Bez Outproxy záměrně

Na rozdíl od Toru, I2P **nenabízí** SOCKS outproxy pro přístup k běžnému internetu. Pokusy o připojení k externím IP adresám selžou nebo prozradí identitu. Pokud je potřeba outproxy, použijte HTTP nebo HTTPS proxy.

---

## 3. Historický kontext

Vývojáři již dlouho nedoporučují SOCKS pro anonymní použití. Z interních vývojářských diskusí a z roku 2004 [Meeting 81](/cs/blog/2004/03/16/i2p-dev-meeting-march-16-2004/) a [Meeting 82](/cs/blog/2004/03/23/i2p-dev-meeting-march-23-2004/):

> "Přeposílání libovolného provozu je nebezpečné a jako vývojářům softwaru pro anonymitu nám přísluší mít bezpečnost našich koncových uživatelů na prvním místě."

Podpora SOCKS byla zahrnuta kvůli kompatibilitě, ale nedoporučuje se pro produkční prostředí. Téměř každá internetová aplikace prozrazuje citlivá metadata nevhodná pro anonymní směrování.

---

## 4. Konfigurace

### Java I2P

1. Otevřete [I2PTunnel Manager](http://127.0.0.1:7657/i2ptunnel)  
2. Vytvořte nový klientský tunnel typu **"SOCKS 4/4a/5"**  
3. Nakonfigurujte možnosti:  
   - Lokální port (jakýkoliv dostupný)  
   - Sdílený klient: *vypnout* pro samostatnou identitu pro každou aplikaci  
   - Trvalý klíč: *zapnout* pro snížení korelace klíčů  
4. Spusťte tunnel

### i2pd

i2pd obsahuje podporu SOCKS5, která je ve výchozím nastavení povolena na `127.0.0.1:4447`. Konfigurace v `i2pd.conf` pod sekcí `[SOCKSProxy]` vám umožňuje upravit port, hostitele a parametry tunelu.

---

## 5. Harmonogram vývoje

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Change</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Date</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.7.1</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Initial SOCKS 4/4a/5 support</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2010</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">0.9.9</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Added persistent keying</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2013</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1.7.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">BOB API deprecated and removed</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2022</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.6.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2P-over-Tor blocked to improve network health</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2024</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2.10.0</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Post-quantum hybrid encryption introduced</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2025</td>
    </tr>
  </tbody>
</table>
Samotný modul SOCKS nezaznamenal od roku 2013 žádné zásadní aktualizace protokolu, ale okolní tunnel stack získal vylepšení výkonu a kryptografie.

---

## 6. Doporučené alternativy

Pro jakoukoliv **produkční**, **veřejně přístupnou** nebo **bezpečnostně kritickou** aplikaci používejte místo SOCKS jedno z oficiálních I2P API:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">API</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Recommended For</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>SAM v3 (3.3)</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Simple Anonymous Messaging API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Cross-language apps needing socket-like I/O</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Streaming Library</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TCP-like sockets for Java</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Native Java integrations</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>I2CP</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Low-level router communication</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Custom protocols, router-level integration</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>BOB</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Deprecated (removed 2022)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Legacy only; migrate to SAM</td>
    </tr>
  </tbody>
</table>
Tato API poskytují řádnou izolaci cílů, kontrolu kryptografické identity a lepší výkon směrování.

---

## 7. OnionCat / GarliCat

OnionCat podporuje I2P prostřednictvím svého režimu GarliCat (rozsah IPv6 `fd60:db4d:ddb5::/48`). Stále funkční, ale s omezeným vývojem od roku 2019.

**Upozornění k použití:** - Vyžaduje ruční konfiguraci `.oc.b32.i2p` v SusiDNS   - Potřebuje statické přiřazení IPv6   - Oficiálně není podporováno projektem I2P

Doporučeno pouze pro pokročilá nastavení VPN-over-I2P.

---

## 8. Osvědčené postupy

Pokud musíte použít SOCKS: 1. Vytvořte samostatné tunnely pro každou aplikaci. 2. Vypněte režim sdíleného klienta. 3. Povolte trvalé klíče. 4. Vynuťte SOCKS5 DNS rozlišení. 5. Auditujte chování protokolu kvůli únikům. 6. Vyhněte se clearnet připojením. 7. Monitorujte síťový provoz kvůli únikům.

---

## 9. Technické shrnutí

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Parameter</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Supported SOCKS Versions</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4, 4a, 5</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Transport</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">TCP only</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>UDP Support</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Stubbed (non-functional)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Clearnet Access</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Not supported</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Default Ports</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Java I2P: user-set; i2pd: <code>127.0.0.1:4447</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Persistent Keying</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported since 0.9.9</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><strong>Shared Tunnels</strong></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Supported (discouraged)</td>
    </tr>
  </tbody>
</table>
---

## 10. Závěr

SOCKS proxy v I2P poskytuje základní kompatibilitu s existujícími TCP aplikacemi, ale **není navržen pro silné záruky anonymity**. Měl by být používán pouze v kontrolovaných, auditovaných testovacích prostředích.

> Pro závažná nasazení přejděte na **SAM v3** nebo **Streaming API**. Tato API izolují identity aplikací, používají moderní kryptografii a jsou nadále vyvíjena.

---

### Další zdroje

- [Oficiální dokumentace SOCKS](/docs/api/socks/)  
- [Specifikace SAM v3](/docs/api/samv3/)  
- [Dokumentace Streaming Library](/docs/specs/streaming/)  
- [Reference I2PTunnel](/docs/specs/implementation/)  
- [Dokumentace pro vývojáře I2P](https://i2pgit.org/I2P_Developers/i2p.i2p)  
- [Komunitní fórum](https://i2pforum.net)
