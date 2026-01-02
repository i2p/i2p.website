---
title: "Příručka pro odstraňování problémů I2P routeru"
description: "Komplexní průvodce odstraňováním běžných problémů I2P routeru, včetně potíží s konektivitou, výkonem a konfigurací"
slug: "troubleshooting"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

I2P routery nejčastěji selhávají kvůli **problémům s přesměrováním portů**, **nedostatečnému vyhrazení šířky pásma** a **nedostatečnému času pro bootstrap**. Tyto tři faktory představují více než 70 % nahlášených problémů. Router po startu potřebuje alespoň **10-15 minut** k plné integraci do sítě, **minimální šířku pásma 128 KB/sec** (doporučeno 256 KB/sec) a správné **přesměrování portů UDP/TCP** k dosažení stavu neblokovaného firewallem. Noví uživatelé často očekávají okamžité připojení a předčasně restartují, což resetuje průběh integrace a vytváří frustrující smyčku. Tato příručka poskytuje podrobná řešení všech hlavních problémů I2P, které ovlivňují verze 2.10.0 a novější.

Architektura anonymity I2P ze své podstaty vyměňuje rychlost za soukromí prostřednictvím víceskokových šifrovaných tunnelů. Pochopení tohoto základního návrhu pomáhá uživatelům nastavit si realistická očekávání a efektivně řešit potíže, místo aby běžné chování mylně považovali za problémy.

## Router se nespustí nebo se okamžitě zhroutí

Nejčastější potíže při spuštění pramení z **konfliktů portů**, **nekompatibility verzí Javy** nebo **poškozených konfiguračních souborů**. Než budete pátrat po hlubších příčinách, ověřte, zda už neběží jiná instance I2P.

**Zkontrolujte, zda neběží žádné kolidující procesy:**

Linux: `ps aux | grep i2p` nebo `netstat -tulpn | grep 7657`

Windows: Správce úloh → Podrobnosti → najděte java.exe s i2p v příkazovém řádku

macOS: Monitor aktivity → vyhledejte "i2p"

Pokud existuje zombie proces, ukončete ho: `pkill -9 -f i2p` (Linux/Mac) nebo `taskkill /F /IM javaw.exe` (Windows)

**Zkontrolujte kompatibilitu verze Javy:**

I2P 2.10.0+ vyžaduje **minimálně Java 8**, doporučena je Java 11 nebo novější. Ověřte, že vaše instalace zobrazuje "mixed mode" (nikoli "interpreted mode"):

```bash
java -version
```
Mělo by se zobrazit: OpenJDK nebo Oracle Java, verze 8+, "mixed mode"

**Vyhněte se:** GNU GCJ, zastaralým implementacím Javy, pouze interpretovaným režimům

**Běžné konflikty portů** nastávají, když se více služeb přetahuje o výchozí porty I2P. Konzole routeru (7657), I2CP (7654), SAM (7656) a HTTP proxy (4444) musí být volné. Zkontrolujte konflikty: `netstat -ano | findstr "7657 4444 7654"` (Windows) nebo `lsof -i :7657,4444,7654` (Linux/Mac).

**Poškození konfiguračního souboru** se projevuje jako okamžité pády s chybami parsování v logech. Router.config vyžaduje kódování UTF-8 bez BOM, používá `=` jako oddělovač (nikoli `:`) a zakazuje určité speciální znaky. Zálohujte a poté zkontrolujte: `~/.i2p/router.config` (Linux), `%LOCALAPPDATA%\I2P\router.config` (Windows), `~/Library/Application Support/i2p/router.config` (macOS).

Pro resetování konfigurace při zachování identity: Zastavte I2P, zálohujte router.keys a adresář keyData, smažte router.config a restartujte. Router znovu vygeneruje výchozí konfiguraci.

**Příliš nízké přidělení haldy Javy** způsobuje pády s chybou OutOfMemoryError (chyba nedostatku paměti). Upravte wrapper.config a zvyšte `wrapper.java.maxmemory` z výchozích 128 nebo 256 na **minimálně 512** (1024 pro routery s vysokou šířkou pásma). To vyžaduje úplné vypnutí, vyčkání 11 minut a poté restart - kliknutí na "Restart" v konzoli změnu neaplikuje.

## Řešení stavu "Network: Firewalled"

Stav blokovaný firewallem znamená, že router nemůže přijímat přímá příchozí spojení, což nutí spoléhat se na introducers (uzly zprostředkovávající navázání příchozího spojení). I když router v tomto stavu funguje, **výkon se výrazně zhoršuje** a přínos pro síť zůstává minimální. Dosažení stavu bez blokování firewallem vyžaduje správné přesměrování portů.

**Router náhodně vybere port** v rozmezí 9000-31000 pro komunikaci. Svůj port najdete na http://127.0.0.1:7657/confignet - hledejte "UDP Port" a "TCP Port" (obvykle stejné číslo). Pro optimální výkon musíte přesměrovat porty pro **jak UDP, tak TCP**, i když samotné UDP umožňuje základní funkčnost.

**Povolit automatické přesměrování portů přes UPnP** (nejjednodušší metoda):

1. Přejděte na http://127.0.0.1:7657/confignet
2. Zaškrtněte "Enable UPnP"
3. Uložte změny a restartujte router
4. Počkejte 5-10 minut a ověřte, že se stav změní z "Network: Firewalled" na "Network: OK"

UPnP vyžaduje podporu ze strany routeru (která je ve výchozím nastavení povolena u většiny spotřebitelských routerů vyrobených po roce 2010) a správnou konfiguraci sítě.

**Ruční přesměrování portů** (vyžaduje se, pokud selže UPnP):

1. Poznamenejte si svůj port I2P z http://127.0.0.1:7657/confignet (např. 22648)
2. Zjistěte svou místní IP adresu: `ipconfig` (Windows), `ip addr` (Linux), Předvolby systému → Síť (macOS)
3. Otevřete administrační rozhraní routeru (obvykle 192.168.1.1 nebo 192.168.0.1)
4. Přejděte do Port Forwarding (může být v části Advanced, NAT nebo Virtual Servers)
5. Vytvořte dvě pravidla:
   - External Port: [váš port I2P] → Internal IP: [váš počítač] → Internal Port: [stejný] → Protocol: **UDP**
   - External Port: [váš port I2P] → Internal IP: [váš počítač] → Internal Port: [stejný] → Protocol: **TCP**
6. Uložte konfiguraci a případně restartujte router

**Ověřte přesměrování portů** pomocí online testovacích nástrojů po konfiguraci. Pokud zjišťování selže, zkontrolujte nastavení firewallu – jak systémový firewall, tak případný firewall antiviru musí povolit port I2P.

**Alternativa Hidden mode** pro restriktivní sítě, kde není možné přesměrování portů: Povolte na http://127.0.0.1:7657/confignet → zaškrtněte "Hidden mode". Router zůstane za firewallem, ale optimalizuje se pro tento stav tím, že bude výhradně používat SSU introducers (zprostředkovatele SSU). Výkon bude pomalejší, ale funkční.

## Router uvízl ve stavu "Spouštění" nebo "Testování"

Tyto přechodné stavy během počátečního bootstrapu se obvykle vyřeší do **10-15 minut u nových instalací** nebo **3-5 minut u zavedených routers**. Předčasný zásah často problémy zhoršuje.

**"Network: Testing"** označuje, že router ověřuje dosažitelnost prostřednictvím různých typů připojení (přímé, introducers (zprostředkovatelé), více verzí protokolu). To je **normální během prvních 5–10 minut** po spuštění. Router testuje více scénářů, aby určil optimální konfiguraci.

**"Rejecting tunnels: starting up"** se zobrazuje během bootstrapu, když router nemá dostatek informací o peerech. Router nebude přeposílat provoz, dokud nebude dostatečně integrován. Tato zpráva by měla zmizet po 10-20 minutách, jakmile bude v netDb 50+ routers.

**Odchylka hodin znemožňuje testování dosažitelnosti.** I2P vyžaduje, aby systémový čas byl v odchylce **±60 sekund** vůči síťovému času. Rozdíl přesahující 90 sekund způsobí automatické odmítnutí spojení. Synchronizujte systémové hodiny:

Linux: `sudo timedatectl set-ntp true && sudo systemctl restart systemd-timesyncd`

Windows: Ovládací panely → Datum a čas → Internetový čas → Aktualizovat nyní → Povolit automatickou synchronizaci

macOS: Předvolby systému → Datum a čas → Povolte "Nastavit datum a čas automaticky"

Po opravě odchylky systémového času úplně restartujte I2P pro správnou integraci.

**Nedostatečné přidělení šířky pásma** brání úspěšnému testování. Router potřebuje dostatečnou kapacitu pro sestavení testovacích tunnels. Nastavte na http://127.0.0.1:7657/config:

- **Minimální použitelné:** Příchozí 96 KB/sec, Odchozí 64 KB/sec
- **Doporučený standard:** Příchozí 256 KB/sec, Odchozí 128 KB/sec  
- **Optimální výkon:** Příchozí 512+ KB/sec, Odchozí 256+ KB/sec
- **Procento sdílení:** 80% (umožňuje, aby router přispíval šířkou pásma do sítě)

Nižší šířka pásma může sice fungovat, ale prodlužuje dobu integrace z minut na hodiny.

**Poškozená netDb** v důsledku nesprávného vypnutí nebo chyb disku způsobuje neustálé testovací smyčky. Router nemůže dokončit testování bez platných dat o uzlech:

```bash
# Stop I2P completely
i2prouter stop    # or systemctl stop i2p

# Delete corrupted database (safe - will reseed automatically)
rm -rf ~/.i2p/netDb/*

# Restart and allow 10-15 minutes for reseed
i2prouter start
```
Windows: Odstraňte obsah `%APPDATA%\I2P\netDb\` nebo `%LOCALAPPDATA%\I2P\netDb\`

**Firewall blokující reseed (počáteční získávání peerů)** znemožňuje získání počátečních peerů. Během bootstrapu I2P načítá informace o routeru z HTTPS reseed serverů. Firewally v korporátních sítích nebo u ISP mohou tato spojení blokovat. Nastavte reseed proxy na adrese http://127.0.0.1:7657/configreseed, pokud se nacházíte v restriktivní síti.

## Nízké rychlosti, vypršení časových limitů a selhání při vytváření tunnelů

Architektura I2P přirozeně vede k **3-10x pomalejším rychlostem než clearnet (běžný otevřený internet)** kvůli vícehopovému šifrování, režii paketů a nepředvídatelnosti tras. Při sestavení tunnelu se prochází více routerů, z nichž každý přidává latenci. Pochopení toho pomáhá předejít záměně normálního chování za problémy.

**Typická očekávání ohledně výkonu:**

- Prohlížení .i2p webů: zpočátku se stránky načítají 10-30 sekund, rychlejší, jakmile jsou tunnel vytvořeny
- Torrentování přes I2PSnark: 10-100 KB/s na torrent podle počtu seederů a podmínek sítě  
- Stahování velkých souborů: vyžaduje trpělivost - soubory v řádu megabajtů mohou trvat minuty, v řádu gigabajtů hodiny
- První připojení je nejpomalejší: budování tunnel trvá 30-90 sekund; následující připojení používají existující tunnels

**Míra úspěšnosti sestavování tunnelů** naznačuje zdraví sítě. Zkontrolujte na http://127.0.0.1:7657/tunnels:

- **Nad 60%:** Normální, zdravý provoz
- **40-60%:** Hraniční, zvažte navýšení šířky pásma nebo snížení zátěže
- **Pod 40%:** Problematické - naznačuje nedostatečnou šířku pásma, síťové problémy nebo špatný výběr peerů

**Zvyšte přidělení šířky pásma** jako první krok optimalizace. Většina problémů s pomalým výkonem pramení z nedostatku šířky pásma. Na adrese http://127.0.0.1:7657/config limity navyšujte postupně a sledujte grafy na http://127.0.0.1:7657/graphs.

**Pro DSL/Kabel (1-10 Mbps připojení):** - Příchozí: 400 KB/sec - Odchozí: 200 KB/sec - Sdílení: 80% - Paměť: 384 MB (upravte wrapper.config)

**Pro vysokorychlostní (10-100+ Mbps připojení):** - Příchozí: 1500 KB/sec   - Odchozí: 1000 KB/sec - Sdílení: 80-100% - Paměť: 512-1024 MB - Zvažte: Zvyšte počet participating tunnels (účastnické tunely) na 2000-5000 na adrese http://127.0.0.1:7657/configadvanced

**Optimalizujte konfiguraci tunnel** pro lepší výkon. Otevřete konkrétní nastavení tunnel na http://127.0.0.1:7657/i2ptunnel a upravte každý tunnel:

- **Počet Tunnel:** Zvyšte z 2 na 3-4 (více dostupných cest)
- **Počet záloh:** Nastavte na 1-2 (rychlé přepnutí při selhání tunnel)
- **Délka Tunnel:** Výchozí 3 skoky poskytují dobrou rovnováhu; snížení na 2 zlepší rychlost, ale sníží anonymitu

**Nativní kryptografická knihovna (jbigi)** poskytuje 5-10x lepší výkon než šifrování implementované čistě v Javě. Ověřte, že je načtená, na http://127.0.0.1:7657/logs - hledejte "jbigi loaded successfully" nebo "Using native CPUID implementation". Pokud chybí:

Linux: Obvykle automaticky detekováno a načteno z ~/.i2p/jbigi-*.so Windows: Zkontrolujte jbigi.dll v instalačním adresáři I2P Pokud chybí: Nainstalujte nástroje pro sestavení a zkompilujte ze zdrojového kódu, nebo stáhněte předkompilované binární soubory z oficiálních repozitářů

**Nechte router běžet nepřetržitě.** Každý restart resetuje integraci do sítě a vyžaduje 30-60 minut na znovuvybudování sítě tunnel a vztahů s peery. Stabilní routery s vysokou dobou provozu jsou při stavbě tunnel vybírány přednostně, což vytváří pozitivní zpětnou vazbu pro výkon.

## Vysoké využití procesoru a paměti

Nadměrné využití prostředků obvykle naznačuje **nedostatečné přidělení paměti**, **chybějící nativní kryptografické knihovny** nebo **nadměrné zapojení do účasti v síti**. Dobře nakonfigurovaný router by měl během aktivního používání využívat 10-30% CPU a udržovat stabilní využití paměti pod 80% přiděleného heapu.

**Problémy s pamětí se projevují následovně:** - Paměťové grafy s „plochým vrcholem“ (držené na maximu) - Častá garbage collection (odklízení paměti) (pilovitý průběh se strmými poklesy) - OutOfMemoryError v logech - Router při zátěži přestává reagovat - Automatické vypnutí kvůli vyčerpání prostředků

**Zvyšte alokaci haldy Javy** v wrapper.config (vyžaduje úplné vypnutí):

```bash
# Linux: ~/.i2p/wrapper.config
# Windows: %APPDATA%\I2P\wrapper.config  
# Find and modify:
wrapper.java.maxmemory=512

# Recommendations by usage:
# Light browsing only: 256
# Standard use (browsing + light torrenting): 512
# Heavy use (multiple applications, active torrenting): 768-1024
# Floodfill or very high bandwidth: 1024-2048
```
**Kritické:** Po úpravě wrapper.config musíte **zcela vypnout** (ne restartovat), počkejte 11 minut na korektní ukončení a poté spusťte načisto. Tlačítko "Restart" v Router console nenačte znovu nastavení wrapperu.

**Optimalizace CPU vyžaduje nativní kryptografickou knihovnu.** Operace s BigInteger v čisté Javě spotřebují 10–20× více CPU než nativní implementace. Ověřte stav jbigi na http://127.0.0.1:7657/logs během spouštění. Bez jbigi CPU vyskočí na 50–100 % během budování tunnel a šifrovacích operací.

**Snižte zátěž participujících tunnel** pokud je router přetížen:

1. Přejděte na http://127.0.0.1:7657/configadvanced
2. Nastavte `router.maxParticipatingTunnels=1000` (výchozí 8000)
3. Snižte procento sdílení na http://127.0.0.1:7657/config z 80% na 50%
4. Vypněte režim floodfill, pokud je povolen: `router.floodfillParticipant=false`

**Omezte šířku pásma I2PSnark a počet současně běžících torrentů.** Torrentování spotřebovává značné prostředky. Na adrese http://127.0.0.1:7657/i2psnark:

- Omezte počet aktivních torrentů na maximálně 3–5
- Nastavte "Up BW Limit" a "Down BW Limit" na rozumné hodnoty (každý 50–100 KB/sec)
- Zastavte torrenty, když je zrovna nepotřebujete
- Vyhněte se seedování desítek torrentů najednou

**Sledujte využití prostředků** pomocí vestavěných grafů na http://127.0.0.1:7657/graphs. Paměť by měla vykazovat rezervu, ne plochý strop. Špičky CPU během vytváření tunnel jsou normální; dlouhodobě vysoké využití CPU naznačuje problémy s konfigurací.

**Pro systémy s výrazně omezenými prostředky** (Raspberry Pi, starší hardware) zvažte **i2pd** (implementace v C++) jako alternativu. i2pd vyžaduje ~130 MB RAM oproti 350+ MB u Java I2P a při podobné zátěži používá ~7% CPU oproti 70%. Mějte na paměti, že i2pd nemá vestavěné aplikace a vyžaduje externí nástroje.

## Problémy s torrenty v I2PSnarku

Integrace I2PSnark s architekturou I2P router vyžaduje pochopení, že **torrentování závisí zcela na zdraví router tunnel**. Torrenty se nespustí, dokud router nedosáhne dostatečné integrace s 10+ aktivními peery a funkčními tunnels.

**Torrenty zaseknuté na 0 % obvykle naznačují:**

1. **Router není plně integrován:** Po spuštění I2P počkejte 10-15 minut, než se objeví aktivita torrentů
2. **DHT je vypnuté:** Povolte na http://127.0.0.1:7657/i2psnark → Configuration → zaškrtněte "Enable DHT" (ve výchozím nastavení povoleno od verze 0.9.2)
3. **Neplatné nebo nefunkční trackery:** Torrenty v I2P vyžadují trackery specifické pro I2P - trackery z clearnet (veřejný internet) nebudou fungovat
4. **Nedostatečná konfigurace tunnel:** Zvyšte počet tunnel v I2PSnark Configuration → sekci Tunnels

**Nakonfigurujte I2PSnark tunnels pro lepší výkon:**

- Příchozí tunnels: 3-5 (výchozí 2 pro Java I2P, 5 pro i2pd)
- Odchozí tunnels: 3-5  
- Délka tunnels: 3 skoky (snižte na 2 pro vyšší rychlost, nižší anonymita)
- Počet tunnels: 3 (zajišťuje stabilní výkon)

**Nezbytné I2P torrentové trackery** k zahrnutí: - tracker2.postman.i2p (primární, nejspolehlivější) - w7tpbzncbcocrqtwwm3nezhnnsw4ozadvi2hmvzdhrqzfxfum7wa.b32.i2p/a

Odstraňte všechny clearnet trackery (non-.i2p; veřejný internet) - nepřinášejí žádný užitek a vedou k pokusům o připojení, které končí vypršením časového limitu.

**Chyby "Torrent not registered"** nastávají, když selže komunikace s trackerem. Klikněte pravým tlačítkem na torrent → "Start" vynutí opětovné ohlášení u trackeru. Pokud to přetrvává, ověřte dostupnost trackeru návštěvou http://tracker2.postman.i2p v prohlížeči nakonfigurovaném pro I2P. Mrtvé trackery nahraďte funkčními alternativami.

**Žádní vrstevníci (peers) se nepřipojují** přestože tracker funguje, naznačuje, že: - Router za firewallem (zlepší se s přesměrováním portů, ale není vyžadováno) - Nedostatečná šířka pásma (zvyšte na 256+ KB/sec)   - Roj je příliš malý (některé torrenty mají 1-2 seedeři; je třeba trpělivost) - DHT je vypnuté (povolte pro vyhledávání vrstevníků bez trackeru)

**Povolte DHT a PEX (Peer Exchange – výměna peerů)** v nastavení I2PSnark. DHT umožňuje nalézat peery bez závislosti na trackeru. PEX zjišťuje peery prostřednictvím již připojených peerů, což urychluje objevování roje.

**Poškození stažených souborů** se díky vestavěné kontrole integrity v I2PSnarku vyskytuje jen zřídka. Pokud je zjištěno:

1. Klikněte pravým tlačítkem na torrent → "Zkontrolovat" vynutí opětovné přepočítání hashů všech částí
2. Smažte poškozená data torrentu (ponechá soubor .torrent)  
3. Klikněte pravým tlačítkem → "Spustit" pro opětovné stažení s ověřováním částí
4. Zkontrolujte disk na chyby, pokud poškození přetrvává: `chkdsk` (Windows), `fsck` (Linux)

**Nefunkční sledovaná složka** vyžaduje správné nastavení:

1. Konfigurace I2PSnark → "Sledovaný adresář": Nastavte absolutní cestu (např. `/home/user/torrents/watch`)
2. Ujistěte se, že proces I2P má oprávnění ke čtení: `chmod 755 /path/to/watch`
3. Umístěte soubory .torrent do sledovaného adresáře - I2PSnark je automaticky přidá
4. Nastavte "Automatické spuštění": Zaškrtněte, mají-li se torrenty spouštět ihned po přidání

**Optimalizace výkonu pro torrentování:**

- Omezte současně aktivní torrenty: maximálně 3-5 pro standardní připojení
- Upřednostněte důležité stahování: Dočasně zastavte torrenty s nízkou prioritou
- Zvyšte přidělení šířky pásma pro router: Více šířky pásma = lepší výkon torrentů
- Buďte trpěliví: torrentování v I2P je ze své podstaty pomalejší než BitTorrent na clearnetu (veřejném internetu)
- Seedujte po dokončení stahování: Síť prosperuje díky reciprocitě

## Git přes I2P konfigurace a odstraňování problémů

Operace Gitu přes I2P vyžadují buď **konfiguraci SOCKS proxy**, nebo **dedicated I2P tunnels** pro přístup přes SSH/HTTP. Návrh Gitu předpokládá spojení s nízkou latencí, což činí architekturu I2P s vysokou latencí náročnou.

**Nakonfigurujte Git tak, aby používal I2P SOCKS proxy:**

Upravte ~/.ssh/config (vytvořte, pokud neexistuje):

```
Host *.i2p
    ProxyCommand nc -X 5 -x 127.0.0.1:4447 %h %p
    ServerAliveInterval 60
    ServerAliveCountMax 3
    Compression yes
```
Tím se směrují všechna připojení SSH na hosty .i2p přes SOCKS proxy I2P (port 4447). Nastavení ServerAlive udržují spojení i při latenci I2P.

Pro operace gitu přes HTTP/HTTPS nakonfigurujte git globálně:

```bash
git config --global http.proxy socks5h://127.0.0.1:4447
git config --global https.proxy socks5h://127.0.0.1:4447
```
Poznámka: `socks5h` provádí rozlišení DNS přes proxy - zásadní pro domény .i2p.

**Vytvořte vyhrazený I2P tunnel pro Git SSH (spolehlivější než SOCKS):**

1. Přejděte na http://127.0.0.1:7657/i2ptunnel
2. "Nový klientský tunnel" → "Standard"
3. Nakonfigurujte:
   - Název: Git-SSH  
   - Typ: Klient
   - Port: 2222 (lokální port pro přístup ke Gitu)
   - Cíl: [your-git-server].i2p:22
   - Automatické spuštění: Zapnuto
   - Počet tunnelů: 3-4 (vyšší pro spolehlivost)
4. Uložte a spusťte tunnel
5. Nastavte SSH tak, aby používalo tunnel: `ssh -p 2222 git@127.0.0.1`

**Chyby autentizace SSH** přes I2P obvykle pramení z:

- Klíč není přidán do ssh-agentu: `ssh-add ~/.ssh/id_rsa`
- Nesprávná oprávnění souboru s klíčem: `chmod 600 ~/.ssh/id_rsa`
- Tunnel neběží: Ověřte na http://127.0.0.1:7657/i2ptunnel, že je stav zelený
- Git server vyžaduje konkrétní typ klíče: Vygenerujte klíč ed25519, pokud RSA selže

**Vypršení časového limitu u operací Git** souvisí s charakteristikami latence I2P:

- Zvyšte časový limit Gitu: `git config --global http.postBuffer 524288000` (vyrovnávací paměť 500 MB)
- Zvyšte limit nízké rychlosti: `git config --global http.lowSpeedLimit 1000` a `git config --global http.lowSpeedTime 600` (čeká 10 minut)
- Pro počáteční klonování použijte shallow clone (mělký klon): `git clone --depth 1 [url]` (stáhne pouze poslední commit, rychlejší)
- Klonujte v obdobích nižší aktivity: Přetížení sítě ovlivňuje výkon I2P

**Pomalé operace git clone/fetch** vyplývají z architektury I2P. Repozitář o velikosti 100MB může přes I2P trvat 30-60 minut, zatímco na clearnetu (veřejném internetu) jen sekundy. Strategie:

- Použijte mělké klony: `--depth 1` výrazně snižuje počáteční objem přenesených dat
- Načítejte postupně: Místo úplného klonování načítejte konkrétní větve: `git fetch origin branch:branch`
- Zvažte rsync přes I2P: U velmi velkých repozitářů může rsync dosahovat lepšího výkonu
- Zvyšte počet tunnel (tunelů): Vyšší počet poskytne lepší propustnost při dlouhotrvajících velkých přenosech

**Chyby "Connection refused"** naznačují nesprávné nastavení tunnelu:

1. Ověřte, že I2P router běží: Zkontrolujte http://127.0.0.1:7657
2. Potvrďte, že tunnel je aktivní a zelený na http://127.0.0.1:7657/i2ptunnel
3. Otestujte tunnel: `nc -zv 127.0.0.1 2222` (mělo by se připojit, pokud tunnel funguje)
4. Zkontrolujte, zda je cíl dostupný: Otevřete v prohlížeči HTTP rozhraní cíle, pokud je k dispozici
5. Zkontrolujte logy tunnelu na http://127.0.0.1:7657/logs kvůli konkrétním chybám

**Osvědčené postupy pro Git přes I2P:**

- Udržujte I2P router v nepřetržitém provozu pro stabilní přístup k Git repozitářům
- Používejte klíče SSH místo ověřování heslem (méně interaktivních výzev)
- Nakonfigurujte trvalé tunnels namísto dočasných připojení SOCKS
- Zvažte hostování vlastního I2P git serveru pro lepší kontrolu
- Zdokumentujte své .i2p git koncové body pro spolupracovníky

## Přístup k eepsites a překlad domén .i2p

Nejčastějším důvodem, proč uživatelé nemohou přistupovat ke stránkám .i2p, je **nesprávná konfigurace proxy v prohlížeči**. Stránky I2P existují pouze v rámci sítě I2P a vyžadují směrování přes HTTP proxy I2P.

**Přesně nakonfigurujte nastavení proxy v prohlížeči:**

**Firefox (doporučeno pro I2P):**

1. Menu → Nastavení → Síťová nastavení → tlačítko Nastavení
2. Vyberte "Ruční nastavení proxy"
3. HTTP proxy: **127.0.0.1** Port: **4444**
4. SSL proxy: **127.0.0.1** Port: **4444**  
5. SOCKS proxy: **127.0.0.1** Port: **4447** (volitelné, pro aplikace SOCKS)
6. Zaškrtněte "Proxy DNS při použití SOCKS v5"
7. OK pro uložení

**Zásadní nastavení about:config ve Firefoxu:**

Přejděte na `about:config` a upravte:

- `media.peerconnection.ice.proxy_only` = **true** (zabraňuje únikům IP přes WebRTC)
- `keyword.enabled` = **false** (zabraňuje přesměrování adres .i2p na vyhledávače)
- `network.proxy.socks_remote_dns` = **true** (DNS přes proxy)

**Omezení pro Chrome/Chromium:**

Chrome používá systémová nastavení proxy, nikoli nastavení specifická pro aplikaci. Ve Windows: Nastavení → vyhledejte "proxy" → "Otevřít nastavení proxy vašeho počítače" → Nastavte HTTP: 127.0.0.1:4444 a HTTPS: 127.0.0.1:4445.

Lepší postup: Použijte rozšíření FoxyProxy nebo Proxy SwitchyOmega pro selektivní směrování domén .i2p.

**"Website Not Found In Address Book" chyby** znamenají, že routeru chybí kryptografická adresa domény .i2p. I2P používá místní adresáře místo centralizovaného DNS. Řešení:

**Metoda 1: Použijte jump služby** (nejjednodušší pro nové stránky):

Přejděte na http://stats.i2p a vyhledejte daný web. Klikněte na odkaz addresshelper: `http://example.i2p/?i2paddresshelper=base64destination`. Váš prohlížeč zobrazí „Save to addressbook?“ – potvrďte pro přidání.

**Metoda 2: Aktualizujte odběry adresáře:**

1. Přejděte na http://127.0.0.1:7657/dns (SusiDNS)
2. Klikněte na záložku "Subscriptions"  
3. Ověřte aktivní odběry (výchozí: http://i2p-projekt.i2p/hosts.txt)
4. Přidejte doporučené odběry:
   - http://stats.i2p/cgi-bin/newhosts.txt
   - http://notbob.i2p/hosts.txt
   - http://reg.i2p/export/hosts.txt
5. Klikněte na "Update Now" pro vynucení okamžité aktualizace odběrů
6. Počkejte 5-10 minut na zpracování

**Metoda 3: Použijte adresy base32** (vždy funguje, pokud je stránka online):

Každý .i2p web má adresu Base32: 52 náhodných znaků následovaných .b32.i2p (např. `ukeu3k5oycgaauneqgtnvselmt4yemvoilkln7jpvamvfx7dnkdq.b32.i2p`). Adresy Base32 obcházejí adresář - router provádí přímé kryptografické vyhledání.

**Běžné chyby v konfiguraci prohlížeče:**

- Pokus o HTTPS na webech pouze s HTTP: Většina .i2p webů používá pouze HTTP - pokus o `https://example.i2p` selže
- Zapomenutí prefixu `http://`: Prohlížeč může místo připojení vyhledávat - vždy použijte `http://example.i2p`
- WebRTC zapnuté: Může prozradit skutečnou IP adresu - zakažte ho v nastavení Firefoxu nebo pomocí rozšíření
- DNS není přes proxy: Clearnet (veřejný internet) DNS neumí přeložit .i2p - je nutné posílat DNS dotazy přes proxy
- Špatný port proxy: 4444 pro HTTP (ne 4445, který je HTTPS outproxy do clearnetu)

**Router není plně integrován** znemožňuje přístup na jakékoli weby. Ověřte, že je integrace dostatečná:

1. Zkontrolujte, že http://127.0.0.1:7657 zobrazuje "Network: OK" nebo "Network: Firewalled" (ne "Network: Testing")
2. Active peers zobrazuje minimálně 10 (optimálně 50+)  
3. Žádná zpráva "Rejecting tunnels: starting up"
4. Počkejte plných 10-15 minut po spuštění routeru, než budete očekávat přístup k .i2p

**Konfigurace IRC a e-mailového klienta** se řídí podobnými vzory nastavení proxy:

**IRC:** Klienti se připojují k **127.0.0.1:6668** (IRC proxy tunnel v I2P). Vypněte v IRC klientu nastavení proxy - připojení na localhost:6668 už je vedeno přes I2P.

**E-mail (Postman):**  - SMTP: **127.0.0.1:7659** - POP3: **127.0.0.1:7660**   - Bez SSL/TLS (šifrování zajišťuje I2P tunnel) - Přihlašovací údaje z registrace účtu na postman.i2p

Všechny tyto tunnels musí na http://127.0.0.1:7657/i2ptunnel zobrazovat stav "running" (zelený).

## Selhání instalace a problémy s balíčky

Instalace z balíčků (Debian, Ubuntu, Arch) občas selhávají kvůli **změnám v repozitářích**, **vypršení platnosti klíče GPG** nebo **konfliktům závislostí**. Oficiální repozitáře se v novějších verzích změnily z deb.i2p2.de/deb.i2p2.no (ukončená podpora) na **deb.i2p.net**.

**Aktualizujte repozitář Debian/Ubuntu na aktuální stav:**

```bash
# Remove old repository entries
sudo rm /etc/apt/sources.list.d/i2p.list

# Add current repository
echo "deb [signed-by=/usr/share/keyrings/i2p-archive-keyring.gpg] https://deb.i2p.net/ $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/i2p.list

# Download and install current signing key
curl -o i2p-archive-keyring.gpg https://geti2p.net/_static/i2p-archive-keyring.gpg
sudo cp i2p-archive-keyring.gpg /usr/share/keyrings/

# Update and install
sudo apt update
sudo apt install i2p i2p-keyring
```
**Selhání ověřování podpisů GPG** nastávají, když klíče repozitáře vyprší nebo se změní:

```bash
# Error: "The following signatures were invalid"
# Solution: Install current keyring package
sudo apt install i2p-keyring

# Manual key import if package unavailable
wget https://geti2p.net/_static/i2p-debian-repo.key.asc
sudo apt-key add i2p-debian-repo.key.asc
```
**Služba se po instalaci balíčku nespustí** – nejčastěji je to způsobeno problémy s profilem AppArmor na Debianu/Ubuntu:

```bash
# Check service status
sudo systemctl status i2p.service

# Common error: "Failed at step APPARMOR spawning"
# Solution: Reconfigure without AppArmor
sudo dpkg-reconfigure -plow i2p
# Select "No" for AppArmor when prompted

# Alternative: Set profile to complain mode
sudo aa-complain /usr/sbin/wrapper

# Check logs for specific errors  
sudo journalctl -xe -u i2p.service
```
**Problémy s oprávněními** u I2P nainstalovaného z balíčku:

```bash
# Fix ownership (package install uses 'i2psvc' user)
sudo chown -R i2psvc:i2psvc /var/lib/i2p /var/log/i2p /run/i2p
sudo chmod 750 /var/log/i2p /var/lib/i2p

# Set file descriptor limits (add to /etc/security/limits.conf)
i2psvc soft nofile 4096  
i2psvc hard nofile 8192
```
**Problémy s kompatibilitou Javy:**

I2P 2.10.0 vyžaduje **minimálně Javu 8**. Starší systémy mohou mít Javu 7 nebo starší:

```bash
# Check Java version
java -version

# Install appropriate Java (Debian/Ubuntu)
sudo apt install openjdk-11-jre-headless

# Set default Java if multiple versions installed
sudo update-alternatives --config java
```
**Chyby konfigurace Wrapperu (nástroj pro spouštění služeb)** zabraňují spuštění služby:

Umístění Wrapper.config se liší podle metody instalace: - Uživatelská instalace: `~/.i2p/wrapper.config` - Instalace z balíčku: `/etc/i2p/wrapper.config` nebo `/var/lib/i2p/wrapper.config`

Časté problémy s wrapper.config:

- Nesprávné cesty: `wrapper.java.command` musí ukazovat na platnou instalaci Javy
- Nedostatečná paměť: `wrapper.java.maxmemory` je nastaveno příliš nízko (zvyšte na 512+)
- Nesprávné umístění pidfile (soubor PID): `wrapper.pidfile` musí ukazovat na zapisovatelné umístění
- Chybí binární soubor wrapperu: Na některých platformách chybí předkompilovaný wrapper (použijte záložní variantu runplain.sh)

**Selhání aktualizací a poškozené aktualizace:**

Aktualizace konzole routeru mohou občas uprostřed stahování selhat kvůli výpadkům sítě. Postup ruční aktualizace:

1. Stáhněte si i2pupdate_X.X.X.zip z https://geti2p.net/en/download
2. Ověřte, že kontrolní součet SHA256 odpovídá zveřejněné hodnotě hash
3. Zkopírujte do instalačního adresáře I2P jako `i2pupdate.zip`
4. Restartujte router - automaticky detekuje a rozbalí aktualizaci
5. Počkejte 5-10 minut na instalaci aktualizace
6. Ověřte novou verzi na http://127.0.0.1:7657

**Migrace z velmi starých verzí** (před 0.9.47) na aktuální verze může selhat kvůli nekompatibilním podpisovým klíčům nebo odebraným funkcím. Jsou nutné postupné aktualizace:

- Verze starší než 0.9.9: Nelze ověřit aktuální podpisy - je nutná ruční aktualizace
- Verze na Javě 6/7: Před aktualizací I2P na 2.x je nutné nejprve aktualizovat Javu
- Velké skoky mezi hlavními verzemi: Nejprve aktualizujte na mezilehlou verzi (doporučený mezikrok 0.9.47)

**Kdy použít instalátor vs. balíček:**

- **Balíčky (apt/yum):** Nejlepší pro servery, automatické bezpečnostní aktualizace, systémová integrace, správa systemd
- **Instalátor (.jar):** Nejlepší pro instalaci na úrovni uživatele, Windows, macOS, vlastní instalace, dostupnost nejnovější verze

## Poškození konfiguračního souboru a jeho obnova

Trvalé uložení konfigurace I2P se opírá o několik zásadních souborů. Poškození obvykle vzniká v důsledku **nesprávného vypnutí**, **chyb disku** nebo **chyb při ručních úpravách**. Pochopení účelu jednotlivých souborů umožňuje cílenou opravu namísto úplné přeinstalace.

**Kritické soubory a jejich účely:**

- **router.keys** (516+ bajtů): Kryptografická identita routeru - ztráta tohoto souboru vytvoří novou identitu
- **router.info** (automaticky generováno): Publikované informace o routeru - bezpečné smazat, znovu se vygeneruje  
- **router.config** (text): Hlavní konfigurace - šířka pásma, síťová nastavení, předvolby
- **i2ptunnel.config** (text): Definice tunnelů - client/server tunnely, klíče, destinace
- **netDb/** (adresář): Databáze peerů - informace o routerech účastníků sítě
- **peerProfiles/** (adresář): Statistiky výkonu peerů - ovlivňují výběr tunnelů
- **keyData/** (adresář): Klíče destinací pro eepsites a služby - ztráta změní adresy
- **addressbook/** (adresář): Místní mapování názvů hostitelů .i2p

**Kompletní postup zálohování** před provedením změn:

```bash
# Stop I2P first
i2prouter stop  # or: systemctl stop i2p

# Backup directory
BACKUP_DIR=~/i2p-backup-$(date +%Y%m%d-%H%M)
mkdir -p $BACKUP_DIR

# Copy critical files
cp -r ~/.i2p/router.keys $BACKUP_DIR/
cp -r ~/.i2p/*.config $BACKUP_DIR/
cp -r ~/.i2p/keyData $BACKUP_DIR/
cp -r ~/.i2p/addressbook $BACKUP_DIR/
cp -r ~/.i2p/eepsite $BACKUP_DIR/  # if hosting sites

# Optional but recommended
tar -czf $BACKUP_DIR.tar.gz $BACKUP_DIR
```
**Příznaky poškození Router.config:**

- Router se nespustí; v logech jsou chyby parsování
- Nastavení se po restartu neuchovají
- Objevují se neočekávané výchozí hodnoty  
- Zkomolené znaky při zobrazení souboru

**Oprava poškozeného router.config:**

1. Zálohujte stávající: `cp router.config router.config.broken`
2. Zkontrolujte kódování souboru: Musí být UTF-8 bez BOM
3. Ověřte syntaxi: Klíče používají oddělovač `=` (ne `:`), žádné koncové mezery u klíčů, `#` pouze pro komentáře
4. Časté chyby: Znaky mimo ASCII v hodnotách, problémy s konci řádků (CRLF vs LF)
5. Pokud nelze opravit: Smažte router.config - router vygeneruje výchozí router.config a zachová identitu

**Zásadní nastavení v router.config, která je třeba zachovat:**

```properties
i2np.bandwidth.inboundKBytesPerSecond=512
i2np.bandwidth.outboundKBytesPerSecond=256
router.updatePolicy=notify
routerconsole.lang=en
router.hiddenMode=false
```
**Ztracený nebo neplatný router.keys** vytvoří novou identitu routeru. To je přijatelné, ledaže:

- Provozování floodfill (ztrácí status floodfill)
- Hostování eepsites s publikovanou adresou (ztrácí kontinuitu)  
- Vybudovaná reputace v síti

Obnova bez zálohy není možná – vygenerujte novou: smažte router.keys, restartujte I2P; vytvoří se nová identita.

**Zásadní rozdíl:** router.keys (identita) vs keyData/* (služby). Ztráta souboru router.keys změní identitu routeru. Ztráta souboru keyData/mysite-keys.dat změní .i2p adresu vašeho eepsite - katastrofální, pokud je adresa zveřejněna.

**Zálohujte klíče pro eepsite/službu samostatně:**

```bash
# Identify your service keys
ls -la ~/.i2p/keyData/

# Backup with descriptive names  
cp ~/.i2p/keyData/myservice-keys.dat ~/backups/myservice-keys-$(date +%Y%m%d).dat

# Store securely (encrypted if sensitive)
gpg -c ~/backups/myservice-keys-*.dat
```
**Poškození NetDb (síťová databáze) a peerProfiles (profily peerů):**

Příznaky: Žádné aktivní protějšky, nelze sestavit tunnels, "Zjištěno poškození databáze" v logech

Bezpečná oprava (vše se automaticky reseeduje (znovu získá počáteční seznam uzlů)/znovu sestaví):

```bash
i2prouter stop
rm -rf ~/.i2p/netDb/*
rm -rf ~/.i2p/peerProfiles/*
i2prouter start
# Wait 10-15 minutes for reseed and integration
```
Tyto adresáře obsahují pouze informace o síti uložené v mezipaměti - jejich smazání vynutí nový bootstrap (počáteční inicializační proces), ale nezpůsobí ztrátu žádných kritických dat.

**Strategie prevence:**

1. **Vždy provádějte korektní ukončení:** Použijte `i2prouter stop` nebo tlačítko „Shutdown“ v router konzoli - nikdy proces neukončujte násilně
2. **Automatické zálohy:** Cron úloha s týdenní zálohou ~/.i2p na samostatný disk
3. **Monitorování stavu disku:** Průběžně kontrolujte stav SMART - selhávající disky poškozují data
4. **Dostatečné místo na disku:** Udržujte alespoň 1+ GB volného místa - plné disky způsobují poškození dat
5. **UPS doporučena:** Výpadky napájení během zápisu poškozují soubory
6. **Verzování kritických konfigurací:** Git repozitář pro router.config, i2ptunnel.config umožňuje návrat k předchozím verzím

**Na oprávněních souborů záleží:**

```bash
# Correct permissions (user install)
chmod 600 ~/.i2p/router.keys
chmod 600 ~/.i2p/*.config  
chmod 700 ~/.i2p/keyData
chmod 755 ~/.i2p

# Never run as root - creates permission problems
```
## Vysvětlení běžných chybových hlášení

Logování v I2P poskytuje konkrétní chybová hlášení, která přesně identifikují problémy. Porozumění těmto hlášením urychluje odstraňování problémů.

**"No tunnels available"** se zobrazí, když router nesestavil dostatek tunnels pro provoz. To je **normální během prvních 5-10 minut** po spuštění. Pokud přetrvává déle než 15 minut:

1. Ověřte, že Active Peers > 10 na http://127.0.0.1:7657
2. Zkontrolujte, že přidělení šířky pásma je dostatečné (128+ KB/sec minimum)
3. Prozkoumejte míru úspěšnosti tunnelů na http://127.0.0.1:7657/tunnels (měla by být >40%)
4. Zkontrolujte protokoly kvůli důvodům odmítnutí při sestavování tunnelů

**"Clock skew detected"** nebo **"NTCP2 disconnect code 7"** znamená, že systémový čas se liší od síťového konsenzu o více než 90 sekund. I2P vyžaduje přesnost ±60 sekund. Připojení k routerům s odchýleným časem jsou automaticky odmítána.

Opravit okamžitě:

```bash
# Linux  
sudo timedatectl set-ntp true
sudo systemctl restart systemd-timesyncd
date  # Verify correct time

# Windows
# Control Panel → Date and Time → Internet Time → Update now

# Verify after sync
http://127.0.0.1:7657/logs  # Should no longer show clock skew warnings
```
**"Build timeout"** nebo **"Tunnel build timeout exceeded"** znamená, že budování tunnelu skrze řetězec peerů nebylo dokončeno v rámci časového okna pro timeout (obvykle 60 sekund). Příčiny:

- **Pomalé uzly:** Router vybral nereagující účastníky pro tunnel
- **Přetížení sítě:** Síť I2P je silně vytížená
- **Nedostatečná šířka pásma:** Vaše limity šířky pásma brání včasnému sestavení tunnel
- **Přetížený router:** Příliš mnoho zapojených tunnel spotřebovává prostředky

Řešení: Zvyšte šířku pásma, snižte počet participujících tunnels (`router.maxParticipatingTunnels` na http://127.0.0.1:7657/configadvanced), povolte přesměrování portů pro lepší výběr peerů.

**"Router is shutting down"** nebo **"Graceful shutdown in progress"** se může zobrazit během běžného ukončení nebo obnovy po pádu. Řízené ukončení (graceful shutdown) může trvat až 10 minut, protože router uzavírá tunnels, informuje protějšky a trvale ukládá stav.

Pokud zůstane ve stavu vypínání déle než 11 minut, vynutit ukončení:

```bash
# Linux  
kill -9 $(pgrep -f i2p)

# Windows
taskkill /F /IM javaw.exe
```
**"java.lang.OutOfMemoryError: Java heap space"** signalizuje vyčerpání paměťové haldy. Okamžitá řešení:

1. Upravte wrapper.config: `wrapper.java.maxmemory=512` (nebo vyšší)
2. **Je vyžadováno úplné vypnutí** - restart změnu neuplatní
3. Počkejte 11 minut na úplné vypnutí  
4. Spusťte router načisto
5. Ověřte přidělení paměti na http://127.0.0.1:7657/graphs - měla by být vidět rezerva

**Související chyby paměti:**

- **"GC overhead limit exceeded":** Tráví se příliš mnoho času v garbage collection (uvolňování paměti) - zvyšte velikost haldy
- **"Metaspace":** Metaspace (prostor pro metadata tříd v Javě) je vyčerpán - přidejte `wrapper.java.additional.X=-XX:MaxMetaspaceSize=256M`

**Specifické pro Windows:** Kaspersky Antivirus omezuje paměťovou haldu Javy na 512MB bez ohledu na nastavení v wrapper.config - odinstalujte ho nebo přidejte I2P do výjimek.

**"Connection timeout"** nebo **"I2CP Error - port 7654"**, když se aplikace pokoušejí připojit k routeru:

1. Ověřte, že router běží: http://127.0.0.1:7657 by měl být dostupný
2. Zkontrolujte port I2CP: `netstat -an | grep 7654` by měl zobrazit LISTENING
3. Ujistěte se, že firewall na localhostu povoluje: `sudo ufw allow from 127.0.0.1`  
4. Ověřte, že aplikace používá správný port (I2CP=7654, SAM=7656)

**"Certificate validation failed"** nebo **"RouterInfo corrupt"** během reseedu (počátečního bootstrapu sítě):

Kořenové příčiny: odchylka systémových hodin (nejprve opravte), poškozená netDb, neplatné certifikáty pro reseed (počáteční naplnění netDb z veřejných bootstrap serverů)

```bash
# After fixing clock:
i2prouter stop
rm -rf ~/.i2p/netDb/*  # Delete corrupted database
i2prouter start  # Auto-reseeds with fresh data
```
**"Database corruption detected"** značí poškození dat na úrovni disku v netDb nebo peerProfiles:

```bash
# Safe fix - all will rebuild
i2prouter stop  
rm -rf ~/.i2p/netDb/* ~/.i2p/peerProfiles/*
i2prouter start
```
Zkontrolujte stav disku pomocí nástrojů SMART - opakované poškození dat naznačuje selhávající úložiště.

## Výzvy specifické pro platformu

Různé operační systémy představují při nasazení I2P specifické výzvy související s oprávněními, bezpečnostními zásadami a systémovou integrací.

### Problémy s oprávněními a službami v Linuxu

I2P nainstalované z balíčku běží jako systémový uživatel **i2psvc** (Debian/Ubuntu) nebo **i2p** (ostatní distribuce) a vyžaduje specifická oprávnění:

```bash
# Fix package install permissions  
sudo chown -R i2psvc:i2psvc /var/lib/i2p /var/log/i2p /run/i2p
sudo chmod 750 /var/log/i2p /var/lib/i2p
sudo chmod 644 /var/lib/i2p/*.config

# User install permissions (should be your user)
chown -R $USER:$USER ~/.i2p
chmod 700 ~/.i2p
chmod 600 ~/.i2p/router.keys ~/.i2p/*.config
```
**Limity deskriptorů souborů** ovlivňují kapacitu routeru pro spojení. Výchozí limity (1024) jsou nedostatečné pro routery s vysokou propustností:

```bash
# Check current limits
ulimit -n

# Temporary increase  
ulimit -n 4096

# Permanent fix: Edit /etc/security/limits.conf
i2psvc soft nofile 4096
i2psvc hard nofile 8192

# Systemd override
sudo mkdir -p /etc/systemd/system/i2p.service.d/
sudo nano /etc/systemd/system/i2p.service.d/override.conf

# Add:
[Service]
LimitNOFILE=8192

sudo systemctl daemon-reload
sudo systemctl restart i2p
```
**Konflikty AppArmor** běžné na Debianu/Ubuntu zabraňují spuštění služby:

```bash
# Error: "Failed at step APPARMOR spawning /usr/sbin/wrapper"
# Cause: AppArmor profile missing or misconfigured

# Solution 1: Disable AppArmor for I2P
sudo aa-complain /usr/sbin/wrapper

# Solution 2: Reconfigure package without AppArmor
sudo dpkg-reconfigure -plow i2p  
# Select "No" when asked about AppArmor

# Solution 3: LXC/Proxmox containers - disable AppArmor in container config
lxc.apparmor.profile: unconfined
```
**Problémy se SELinuxem** na RHEL/CentOS/Fedora:

```bash
# Temporary: Set permissive mode
sudo setenforce 0

# Permanent: Generate custom policy
sudo ausearch -c 'java' --raw | audit2allow -M i2p_policy
sudo semodule -i i2p_policy.pp

# Or disable SELinux for I2P process (less secure)
sudo semanage permissive -a i2p_t
```
**Řešení problémů se službou SystemD:**

```bash
# Detailed service status
sudo systemctl status i2p.service -l

# Full logs  
sudo journalctl -xe -u i2p.service

# Follow logs live
sudo journalctl -f -u i2p.service

# Restart with logging
sudo systemctl restart i2p.service && sudo journalctl -f -u i2p.service
```
### Rušení brány firewall systému Windows a antiviru

Windows Defender a antivirové produkty třetích stran často vyhodnocují I2P jako hrozbu kvůli vzorcům síťového chování. Správné nastavení brání zbytečným blokacím při zachování bezpečnosti.

**Nakonfigurujte bránu firewall systému Windows Defender:**

```powershell
# Run PowerShell as Administrator

# Find Java path (adjust for your Java installation)
$javaPath = "C:\Program Files\Eclipse Adoptium\jdk-11.0.16.101-hotspot\bin\javaw.exe"

# Create inbound rules
New-NetFirewallRule -DisplayName "I2P Java" -Direction Inbound -Program $javaPath -Action Allow
New-NetFirewallRule -DisplayName "I2P UDP" -Direction Inbound -Protocol UDP -LocalPort 22648 -Action Allow  
New-NetFirewallRule -DisplayName "I2P TCP" -Direction Inbound -Protocol TCP -LocalPort 22648 -Action Allow

# Add exclusions to Windows Defender
Add-MpPreference -ExclusionPath "C:\Program Files\i2p"
Add-MpPreference -ExclusionPath "$env:APPDATA\I2P"
Add-MpPreference -ExclusionPath "$env:LOCALAPPDATA\I2P"
Add-MpPreference -ExclusionProcess "javaw.exe"
```
Nahraďte port 22648 svým skutečným I2P portem z http://127.0.0.1:7657/confignet.

**Specifický problém s Kaspersky Antivirus:** „Application Control“ od Kaspersky omezuje haldu paměti Javy na 512 MB bez ohledu na nastavení v wrapper.config. To způsobuje OutOfMemoryError na routers s vysokou propustností.

Řešení: 1. Přidejte I2P do vyloučení v Kaspersky: Nastavení → Další → Hrozby a vyloučení → Spravovat vyloučení 2. Nebo odinstalujte Kaspersky (doporučeno pro provoz I2P)

**Obecná doporučení pro antivirový software třetích stran:**

- Přidat instalační adresář I2P do výjimek  
- Přidat %APPDATA%\I2P a %LOCALAPPDATA%\I2P do výjimek
- Vyloučit javaw.exe z analýzy chování
- Vypnout funkce "Network Attack Protection", které mohou narušovat protokoly I2P

### Gatekeeper v macOS blokuje instalaci

macOS Gatekeeper (bezpečnostní mechanismus macOS) brání spouštění nepodepsaných aplikací. Instalátory I2P nejsou podepsané pomocí Apple Developer ID, což vyvolává bezpečnostní varování.

**Obejít Gatekeeper pro instalační program I2P:**

```bash
# Method 1: Remove quarantine attribute
xattr -d com.apple.quarantine ~/Downloads/i2pinstall_*.jar
java -jar ~/Downloads/i2pinstall_*.jar

# Method 2: Use System Settings (macOS 13+)
# Try to open installer → macOS blocks it
# System Settings → Privacy & Security → scroll down
# Click "Open Anyway" next to I2P warning
# Confirm in dialog

# Method 3: Control-click installer
# Control-click (right-click) i2pinstall_*.jar
# Select "Open" from menu → "Open" again in dialog
# Bypasses Gatekeeper for this specific file
```
**Po instalaci spuštění** může stále vyvolávat varování:

```bash
# If I2P won't start due to Gatekeeper:
xattr -dr com.apple.quarantine ~/i2p/
```
**Nikdy natrvalo nevypínejte Gatekeeper** - bezpečnostní riziko pro ostatní aplikace. Používejte pouze výjimky pro jednotlivé soubory.

**Konfigurace firewallu v macOS:**

1. Předvolby systému → Zabezpečení a soukromí → Firewall → Možnosti firewallu
2. Klikněte na "+" pro přidání aplikace  
3. Přejděte k instalaci Javy (např. `/Library/Java/JavaVirtualMachines/jdk-11.jdk/Contents/Home/bin/java`)
4. Přidejte ji a nastavte na "Povolit příchozí připojení"

### Problémy s aplikací I2P pro Android

Omezení verzí Androidu a limity prostředků vytvářejí jedinečné výzvy.

**Minimální požadavky:** - Android 5.0+ (úroveň API 21+) je vyžadován pro aktuální verze - 512MB RAM minimálně, 1GB+ doporučeno   - 100MB úložiště pro aplikaci + data routeru - Omezení aplikací na pozadí musí být pro I2P vypnutá

**Aplikace se okamžitě zhroutí:**

1. **Zkontrolujte verzi Androidu:** Nastavení → O telefonu → Verze systému Android (musí být 5.0+)
2. **Odinstalujte všechny verze I2P:** Instalujte pouze jednu variantu:
   - net.i2p.android (Google Play)
   - net.i2p.android.router (F-Droid)  
   Současná instalace více variant vede ke konfliktům
3. **Vymažte data aplikace:** Nastavení → Aplikace → I2P → Úložiště → Vymazat data
4. **Znovu nainstalujte z čistého stavu**

**Optimalizace baterie ukončuje router:**

Android agresivně ukončuje aplikace na pozadí, aby šetřil baterii. I2P potřebuje výjimku:

1. Nastavení → Baterie → Optimalizace baterie (nebo Využití baterie aplikace)
2. Najděte I2P → Neoptimalizovat (nebo Povolit aktivitu na pozadí)
3. Nastavení → Aplikace → I2P → Baterie → Povolit aktivitu na pozadí + Odstranit omezení

**Problémy s připojením na mobilu:**

- **Bootstrap (počáteční zavedení) vyžaduje WiFi:** Počáteční reseed stahuje značné množství dat - použijte WiFi, ne mobilní data
- **Změny sítě:** I2P nezvládá přepínání sítí bez problémů - po přechodu mezi WiFi a mobilní sítí aplikaci restartujte
- **Šířka pásma pro mobil:** Nastavte konzervativně na 64-128 KB/sec, abyste předešli vyčerpání mobilních dat

**Optimalizace výkonu pro mobilní zařízení:**

1. Aplikace I2P → Menu → Nastavení → Šířka pásma
2. Nastavte vhodné limity: 64 KB/s příchozí, 32 KB/s odchozí pro mobilní data
3. Snižte počet participating tunnels (tunnels, kterými prochází cizí provoz): Nastavení → Pokročilé → Max participating tunnels: 100-200
4. Povolte "Stop I2P when screen off" pro úsporu baterie

**Torrentování na Androidu:**

- Omezte na maximálně 2-3 současně aktivní torrenty
- Snižte agresivitu DHT (distribuovaná hašovací tabulka)  
- Pro torrentování používejte pouze WiFi
- Smířte se s nižšími rychlostmi na mobilním hardwaru

## Problémy s reseedem a bootstrapem

Nové instalace I2P vyžadují **reseeding** (počáteční načtení informací o uzlech) - získání počátečních informací o uzlech z veřejných serverů HTTPS pro připojení k síti. Problémy s reseedingem mohou uvěznit uživatele s nulovým počtem uzlů a bez přístupu k síti.

**"No active peers" po čerstvé instalaci** obvykle znamená selhání reseed (počáteční získání seznamu uzlů). Příznaky:

- Známí peerové: 0 nebo zůstává pod 5
- "Network: Testing" přetrvává déle než 15 minut
- Logy ukazují "Reseed failed" (reseed = bootstrap sítě, počáteční stažení dat netDb z reseed serverů) nebo chyby připojení k reseed serverům

**Proč reseed selhává:**

1. **Firewall blokuje HTTPS:** Korporátní/ISP firewally blokují spojení k reseed serverům (servery pro počáteční načtení seznamu uzlů; port 443)
2. **Chyby certifikátů SSL:** Systému chybí aktuální kořenové certifikáty
3. **Požadavek na proxy:** Síť vyžaduje proxy HTTP/SOCKS pro externí připojení
4. **Časová odchylka:** Ověření certifikátů SSL selže, pokud je systémový čas nesprávný
5. **Geografická cenzura:** Některé země/ISP blokují známé reseed servery

**Vynutit ruční reseed (opětovné stažení počátečních uzlů):**

1. Otevřete http://127.0.0.1:7657/configreseed
2. Klikněte na "Save changes and reseed now"  
3. Sledujte http://127.0.0.1:7657/logs a hledejte "Reseed got XX router infos"
4. Počkejte 5-10 minut na zpracování
5. Zkontrolujte http://127.0.0.1:7657 - počet známých peerů by se měl zvýšit na 50+

**Nakonfigurujte reseed proxy** pro restriktivní sítě:

http://127.0.0.1:7657/configreseed → Konfigurace proxy:

- HTTP proxy: [proxy-server]:[port]
- Nebo SOCKS5: [socks-server]:[port]  
- Povolit "Use proxy for reseed only"
- Přihlašovací údaje, pokud je to vyžadováno
- Uložit a vynutit reseed (získání počátečních uzlů)

**Alternativa: Tor proxy pro reseed (získání počátečních dat o síti):**

Pokud běží Tor Browser nebo démon Toru:

- Typ proxy: SOCKS5
- Hostitel: 127.0.0.1
- Port: 9050 (výchozí port SOCKS pro Tor)
- Povolit a provést reseed (obnovení počátečních uzlů sítě)

**Ruční reseed (obnovení počátečních uzlů) prostřednictvím souboru su3** (krajní možnost):

Když selže veškerý automatický reseed (počáteční načtení netDb), získejte reseed soubor mimo běžné kanály:

1. Stáhněte i2pseeds.su3 z důvěryhodného zdroje při neomezeném připojení k internetu (https://reseed.i2p.rocks/i2pseeds.su3, https://reseed-fr.i2pd.xyz/i2pseeds.su3)
2. Zcela ukončete I2P
3. Zkopírujte i2pseeds.su3 do adresáře ~/.i2p/  
4. Spusťte I2P - soubor se automaticky rozbalí a zpracuje
5. Smažte i2pseeds.su3 po zpracování
6. Ověřte, že počet peerů na http://127.0.0.1:7657 roste

**Chyby certifikátu SSL během reseed (počátečního zavedení do sítě):**

```
Error: "Reseed: Certificate verification failed"  
Cause: System root certificates outdated or missing
```
Řešení:

```bash
# Linux - update certificates
sudo apt install ca-certificates
sudo update-ca-certificates

# Windows - install KB updates for root certificate trust
# Or install .NET Framework (includes certificate updates)

# macOS - update system
# Software Update includes certificate trust updates
```
**Zaseknuto na 0 známých peerů po více než 30 minutách:**

Označuje úplné selhání reseedu (počáteční stažení informací o uzlech). Postup odstraňování problémů:

1. **Ověřte, že systémový čas je přesný** (nejčastější problém - opravte jako PRVNÍ)
2. **Otestujte připojení přes HTTPS:** Zkuste v prohlížeči otevřít https://reseed.i2p.rocks - pokud selže, jde o problém se sítí
3. **Zkontrolujte logy I2P** na http://127.0.0.1:7657/logs kvůli konkrétním chybám reseed (stažení počátečních dat sítě)
4. **Vyzkoušejte jinou reseed URL:** http://127.0.0.1:7657/configreseed → přidejte vlastní reseed URL: https://reseed-fr.i2pd.xyz/
5. **Použijte ruční metodu se souborem su3** pokud selhaly všechny automatizované pokusy

**Reseed servery jsou občas nedostupné:** I2P obsahuje několik natvrdo definovaných reseed serverů. Pokud jeden selže, router automaticky zkusí ostatní. Úplné selhání všech reseed serverů je velmi vzácné, ale možné.

**Aktuálně aktivní reseed servery** (stav k říjnu 2025):

- https://reseed.i2p.rocks/
- https://reseed-fr.i2pd.xyz/
- https://i2p.novg.net/
- https://i2p-projekt.de/

Přidejte je jako vlastní adresy URL, pokud máte problémy s výchozími.

**Pro uživatele v přísně cenzurovaných regionech:**

Zvažte použití mostů Snowflake/Meek přes Tor pro počáteční reseed (počáteční stažení seedů), poté přepněte na přímé I2P po integraci. Nebo získejte i2pseeds.su3 prostřednictvím steganografie, e-mailem nebo přes USB z místa mimo cenzurní zónu.

## Kdy vyhledat další pomoc

Tento průvodce pokrývá drtivou většinu problémů souvisejících s I2P, ale některé vyžadují pozornost vývojářů nebo odborné znalosti komunity.

**Obraťte se na komunitu I2P o pomoc, když:**

- Router opakovaně padá i po provedení všech kroků pro řešení problémů
- Úniky paměti způsobující trvalý růst nad rámec alokované haldy
- Míra úspěšnosti Tunnel zůstává pod 20 % navzdory odpovídajícímu nastavení  
- Nové chyby v logech, které tato příručka nezahrnuje
- Zjištěné bezpečnostní zranitelnosti
- Požadavky na nové funkce nebo návrhy na vylepšení

**Než požádáte o pomoc, shromážděte diagnostické informace:**

1. Verze I2P: http://127.0.0.1:7657 (např. "2.10.0")
2. Verze Javy: výstup `java -version`
3. Operační systém a verze
4. Stav routeru: Stav sítě, Počet aktivních peerů, Participující tunnels
5. Konfigurace šířky pásma: příchozí/odchozí limity
6. Stav přesměrování portů: za firewallem nebo OK
7. Relevantní výpisy z logu: posledních 50 řádků zobrazujících chyby z http://127.0.0.1:7657/logs

**Oficiální kanály podpory:**

- **Fórum:** https://i2pforum.net (clearnet) nebo http://i2pforum.i2p (v rámci I2P)
- **IRC:** #i2p na Irc2P (irc.postman.i2p přes I2P) nebo irc.freenode.net (clearnet)
- **Reddit:** https://reddit.com/r/i2p pro komunitní diskusi
- **Sledovač chyb:** https://i2pgit.org/i2p-hackers/i2p.i2p/-/issues pro potvrzené chyby
- **E-mailová konference:** i2p-dev@lists.i2p-projekt.de pro dotazy k vývoji

**Realistická očekávání jsou důležitá.** I2P je z podstaty svého návrhu pomalejší než clearnet (běžný internet mimo I2P) - víceskokové šifrované 'tunnel' propojení vytváří inherentní latenci. Funkční I2P router s načítáním stránek trvajícím 30 sekund a rychlostí torrentu 50 KB/sec **funguje správně**, není rozbitý. Uživatelé očekávající rychlosti clearnetu budou zklamaní bez ohledu na optimalizaci konfigurace.

## Závěr

Většina problémů v I2P pramení ze tří kategorií: nedostatek trpělivosti během bootstrapu (počáteční inicializace; vyžaduje 10–15 minut), nedostatečné přidělení prostředků (minimálně 512 MB RAM, 256 KB/sec šířky pásma) nebo chybně nastavené přesměrování portů. Pochopení distribuované architektury I2P a na anonymitu zaměřeného designu pomáhá uživatelům rozlišit očekávané chování od skutečných problémů.

Stav „Firewalled“ routeru, ačkoli není ideální, nebrání používání I2P - pouze omezuje přínos do sítě a mírně zhoršuje výkon. Noví uživatelé by měli upřednostnit **stabilitu před optimalizací**: nechte router běžet nepřetržitě několik dní, než začnete upravovat pokročilá nastavení, protože integrace se s dobou provozu přirozeně zlepšuje.

Při odstraňování problémů vždy nejprve ověřte základní věci: správný systémový čas, dostatečnou šířku pásma, router běžící nepřetržitě a alespoň 10 aktivních uzlů. Většinu problémů vyřešíte tím, že se zaměříte na tyto základy, nikoli úpravami málo srozumitelných konfiguračních parametrů. I2P odměňuje trpělivost a nepřetržitý provoz lepším výkonem, protože si router v průběhu dnů a týdnů provozu buduje reputaci a optimalizuje výběr uzlů.
