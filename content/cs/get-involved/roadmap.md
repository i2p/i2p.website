---
title: "Plán rozvoje I2P"
description: "Aktuální plány vývoje a historické milníky pro síť I2P"
---

<div style="background: var(--color-bg-secondary); border-left: 4px solid var(--color-primary); padding: 1.5rem; margin-bottom: 2rem; border-radius: var(--radius-md);">

**I2P sleduje model inkrementálního vývoje** s vydáním přibližně každých 13 týdnů. Tento plán pokrývá vydání pro desktopové a Android aplikace Java v jedné stabilní cestě vydání.

**Poslední aktualizace:** srpen 2025

</div>

## 🎯 Připravovaná vydání

<div style="border-left: 3px solid var(--color-accent); padding-left: 1.5rem; margin-bottom: 2rem;">

### Verze 2.11.0
<div style="display: inline-block; background: var(--color-accent); color: white; padding: 0.25rem 0.75rem; border-radius: var(--radius-md); font-size: 0.875rem; margin-bottom: 1rem;">
Cíl: začátek prosince 2025
</div>

- Hybridní PQ MLKEM Ratchet, povolit jako výchozí (návrh 169)
- Jetty 12, požadováno Java 17+
- Pokračování prací na PQ (transporty) (návrh 169)
- Podpora vyhledávání I2CP pro parametry servisních záznamů LS (návrh 167)
- Omezení dle tunelu
- Podsystém statistik přátelský k Prometheus
- Podpora SAM pro Datagram 2/3

</div>

---

## 📦 Nedávná vydání

### Vydání 2025

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-success);">

**Verze 2.10.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— Vydáno 8. září 2025</span>

- Podpora UDP trackeru ve i2psnark (návrh 160)
- Parametry servisního záznamu LS I2CP (částečně) (návrh 167)
- Asynchronní API vyhledávání I2CP
- Hybridní PQ MLKEM Ratchet Beta (návrh 169)
- Pokračování prací na PQ (transporty) (návrh 169)
- Parametry šířky pásma pro stavbu tunelů (návrh 168) Část 2 (zpracování)
- Pokračování prací na omezení dle tunelu
- Odstranění nepoužívaného kódu pro transport ElGamal
- Odstranění starého kódu "aktivního škrcení" SSU2
- Odstranění staré podpory protokolování statistik
- Úklid podsystému statistik/grafů
- Vylepšení a opravy skrytého režimu

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-success);">

**Verze 2.9.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— Vydáno 2. června 2025</span>

- Mapa Netdb
- Implementace Datagram2, Datagram3 (návrh 163)
- Začátek práce na parametru servisního záznamu LS (návrh 167)
- Začátek práce na PQ (návrh 169)
- Pokračování prací na omezení dle tunelu
- Parametry šířky pásma pro stavbu tunelů (návrh 168) Část 1 (odesílání)
- Používání /dev/random jako výchozí PRNG na Linuxu
- Odstranění redundantního kódu LS
- Zobrazení changelogu v HTML
- Snížení využití vláken HTTP serveru
- Oprava automatické registrace do floodfill
- Aktualizace Wrapperu na 3.5.60

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-success);">

**Verze 2.8.2** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— Vydáno 29. března 2025</span>

- Oprava chyby poškození SHA256

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-success);">

**Verze 2.8.1** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— Vydáno 17. března 2025</span>

- Oprava chyby instalátoru na Java 21+
- Oprava chyby "loopback"
- Oprava testů tunelů pro odchozí klientské tunely
- Oprava instalace na cesty obsahující mezery
- Aktualizace zastaralého Docker kontejneru a knihoven kontejneru
- Oznámení konzole
- Třídění podle nejnovějšího v SusiDNS
- Použití SHA256 fondu v Noise
- Opravy a vylepšení tmavého tématu konzole
- Podpora .i2p.alt

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-success);">

**Verze 2.8.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— Vydáno 3. února 2025</span>

- Zlepšení publikování RouterInfa
- Zlepšení efektivity ACK SSU2
- Zlepšení manipulace duplicitních zpráv SSU2
- Rychlejší / variabilní vypršení časových limitů vyhledávání
- Vylepšení expirace LS
- Změna kapacity NAT symetrického
- Prosazování POST ve více formulářích
- Opravy tmavého tématu SusiDNS
- Úklid testů šířky pásma
- Nový překlad do čínštiny Gan
- Přidání kurdské volby UI
- Nová stavba Jammy
- Izpack 5.2.3
- rrd4j 3.10

</div>

<div style="margin: 3rem 0; padding: 1rem 0; border-top: 2px solid var(--color-border); border-bottom: 2px solid var(--color-border);">
  <h3 style="margin: 0; color: var(--color-primary);">📅 Vydání 2024</h3>
</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**Verze 2.7.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— Říjen 8, 2024</span>

- Snížení spotřeby vláken serveru HTTP i2ptunnel
- Obecné UDP tunely v I2PTunnel
- Proxy prohlížeč v I2PTunnel
- Migrace webu
- Oprava žlutých tunelů
- Konzole /netdb refaktoring

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**Verze 2.6.1** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— Srpen 6, 2024</span>

- Oprava problémů s velikostí iframe v konzoli
- Převod grafů na SVG
- Balíčkový překladový report

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**Verze 2.6.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— Červenec 19, 2024</span>

- Snížení využití paměti netdb
- Odstranění kódu SSU1
- Oprava úniků a zablokování dočasných souborů i2psnark
- Efektivnější PEX v i2psnark
- Obnova JS konzolových grafů
- Vylepšení vykreslování grafů
- Susimail JS vyhledávání
- Efektivnější manipulace se zprávami na OBEP
- Efektivnější lokální vyhledávání destinací I2CP
- Oprava problému s rozsahy proměnných JS

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**Verze 2.5.2** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— Květen 15, 2024</span>

- Oprava HTTP zkracování
- Publikování schopnosti G, pokud je detekován symetrický NAT
- Aktualizace na rrd4j 3.9.1-preview

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**Verze 2.5.1** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— Květen 6, 2024</span>

- Zmírnění DDoS útoků NetDB
- Tor blokovací seznam
- Opravy a vyhledávání Susimail
- Pokračování v odstraňování kódu SSU1
- Aktualizace na Tomcat 9.0.88

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**Verze 2.5.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— Duben 8, 2024</span>

- Vylepšení iframe konzole
- Přepracování omezení šířky pásma i2psnark
- Javascript drag-and-drop pro i2psnark a susimail
- Vylepšení manipulace s chybami SSL i2ptunnel
- Podpora i2ptunnel pro trvalá HTTP spojení
- Začátek odstraňování kódu SSU1
- Vylepšení manipulace požadavků na relé tagů SSU2
- Opravy testů peerů SSU2
- Vylepšení Susimail (načítání, markdown, podpora HTML emailů)
- Úpravy výběru peerů tunelů
- Aktualizace RRD4J na 3.9
- Aktualizace gradlew na 8.5

</div>

<div style="background: var(--color-bg-secondary); padding: 1.5rem; border-radius: var(--radius-md); margin-bottom: 1.5rem; border-left: 4px solid var(--color-primary);">

**Verze 2.4.0** <span style="color: var(--color-text-muted); font-size: 0.9rem;">— Prosinec 18, 2023</span>

- Správa kontextu NetDB/Segregovaná NetDB
- Řešení schopností přetížení snížením priority přetížených routerů
- Oživení knihovny pro pomocníky Androidu
- Vyhledávač místních torrentových souborů i2psnark
- Opravy manipulátorů vyhledávání v NetDB
- Zakázat SSU1
- Zakázat routery publikující v budoucnosti
- Opravy SAM
- Opravy susimail
- Opravy UPnP

</div>

---

### Vydání 2023-2022

<details>
<summary>Klikněte pro zobrazení vydání 2023-2022</summary>

**Verze 2.3.0** — Vydáno 28. června 2023

- Zlepšení výběru peerů tunelů
- Uživatelsky konfigurovatelná expirace blokovacího seznamu
- Omezení rychlých burstů vyhledávání ze stejného zdroje
- Oprava úniku detekční informace o replay
- Opravy NetDB pro multihomed leaseSets
- Opravy NetDB pro leaseSets přijaté jako odpověď před přijetím jako obchod

**Verze 2.2.1** — Vydáno 12. dubna 2023

- Opravy balíčkování

**Verze 2.2.0** — Vydáno 13. března 2023

- Zlepšení výběru peerů tunelů
- Oprava replay streamování

**Verze 2.1.0** — Vydáno 10. ledna 2023

- Opravy SSU2
- Opravy přetížení stavby tunelů
- Opravy testů peerů SSU a detekce symetrického NAT
- Oprava LS2 zašifrovaných leaseSets
- Možnost zakázat SSU 1 (předběžně)
- Komprimovatelné doplnění (návrh 161)
- Nová záložka stavu peerů konzole
- Přidání podpory torsocks do SOCKS proxy a další vylepšení a opravy SOCKS

**Verze 2.0.0** — Vydáno 21. listopadu 2022

- Migrace spojení SSU2
- Okamžité potvrzení SSU2
- Povoleno SSU2 jako výchozí
- Autentizace proxy pomocí SHA-256 v i2ptunnel
- Aktualizovaný proces sestavování Android pomocí moderního AGP
- Podpora automatické konfigurace I2P prohlížeče mezi platformami (Desktop)

**Verze 1.9.0** — Vydáno 22. srpna 2022

- Implementace testování peerů a relé SSU2
- Opravy SSU2
- Vylepšení MTU/PMTU SSU
- Povoleno SSU2 pro malou část routerů
- Přidání detektoru zamykání
- Další opravy importu certifikátů
- Oprava opakování DHT restartu i2psnark po restartu routeru

**Verze 1.8.0** — Vydáno 23. května 2022

- Opravy a vylepšení pro rodinu routeru
- Opravy měkkého restartu
- Opravy a vylepšení výkonu SSU
- Opravy a vylepšení pro i2psnark standalone
- Vyhnutí se penále Sybil pro důvěryhodné rodiny
- Snížení timeoutu odpovědi na stavbu tunelu
- Opravy UPnP
- Odstranění zdroje BOB
- Opravy importu certifikátů
- Tomcat 9.0.62
- Refaktoring pro podporu SSU2 (návrh 159)
- Počáteční implementace základního protokolu SSU2 (návrh 159)
- Vyskakovací okno autorizace SAM pro Android aplikace
- Vylepšení podpory vlastních instalačních adresářů v i2p.firefox

**Verze 1.7.0** — Vydáno 21. února 2022

- Odstranění BOB
- Nový editor torrentů i2psnark
- Opravy a vylepšení pro i2psnark standalone
- Zlepšení spolehlivosti NetDB
- Přidání vyskakovacích zpráv v systray
- Vylepšení výkonu NTCP
