---
title: "Průvodce konfigurací Routerové konzole"
description: "Komplexní průvodce pochopením a konfigurací konzole I2P routeru"
slug: "router-console-config"
lastUpdated: "2025-11"
accurateFor: "2.10.0"
type: dokumentace
---

Tento průvodce poskytuje přehled konzoly I2P routeru a jeho konfiguračních stránek. Každá sekce vysvětluje, co daná stránka dělá a k čemu je určena, což vám pomůže pochopit, jak monitorovat a konfigurovat váš I2P router.

## Přístup ke konzoli routeru

I2P Router Console je centrální rozbočovač pro správu a monitorování vašeho I2P routeru. Ve výchozím nastavení je přístupná na [I2P Router Console](http://127.0.0.1:7657/home), jakmile je váš I2P router spuštěný.

![Router Console Home](/images/router-console-home.png)

Domovská stránka zobrazuje několik klíčových sekcí:

- **Aplikace** - Rychlý přístup k vestavěným I2P aplikacím jako Email, Torrenty, Správce skrytých služeb a Webový server
- **Komunitní stránky I2P** - Odkazy na důležité komunitní zdroje včetně fór, dokumentace a webových stránek projektu
- **Konfigurace a nápověda** - Nástroje pro konfiguraci nastavení šířky pásma, správu pluginů a přístup ke zdrojům nápovědy
- **Síťové informace a informace pro vývojáře** - Přístup ke grafům, záznamům, technické dokumentaci a statistikám sítě

## Adresář

**URL:** [Address Book](http://127.0.0.1:7657/dns)

![Router Console Address Book](/images/router-console-address-book.png)

Adresář I2P funguje podobně jako DNS na clearnetu a umožňuje vám spravovat lidsky čitelná jména pro I2P destinace (eepsites). Zde můžete prohlížet a přidávat I2P adresy do svého osobního adresáře.

Systém adresáře funguje prostřednictvím několika vrstev:

- **Místní záznamy** - Vaše osobní adresáře, které jsou uloženy pouze na vašem routeru
  - **Místní adresář** - Hostitele, které ručně přidáváte nebo ukládáte pro vlastní použití
  - **Soukromý adresář** - Adresy, které nechcete sdílet s ostatními; nikdy nejsou veřejně distribuovány

- **Předplatné** - Vzdálené zdroje adresáře (jako `http://i2p-projekt.i2p/hosts.txt`), které automaticky aktualizují adresář vašeho routeru o známé I2P stránky

- **Adresář routeru** - Sloučený výsledek vašich lokálních záznamů a odběrů, prohledávatelný všemi I2P aplikacemi na vašem routeru

- **Publikovaný adresář** - Volitelné veřejné sdílení vašeho adresáře, který mohou ostatní používat jako zdroj předplatného (užitečné, pokud provozujete I2P stránku)

Adresář pravidelně kontroluje vaše odběry a slučuje obsah do adresáře vašeho routeru, čímž udržuje váš soubor hosts.txt aktuální se sítí I2P.

## Konfigurace

**URL:** [Pokročilá konfigurace](http://127.0.0.1:7657/configadvanced)

Sekce Konfigurace poskytuje přístup ke všem nastavením routeru prostřednictvím několika specializovaných záložek.

### Advanced

![Router Console Advanced Configuration](/images/router-console-config-advanced.png)

Stránka Pokročilá konfigurace poskytuje přístup k nízkoúrovňovým nastavením routeru, která obvykle nejsou potřebná pro běžný provoz. **Většina uživatelů by neměla tato nastavení měnit, pokud nerozumí konkrétní možnosti konfigurace a jejímu dopadu na chování routeru.**

Klíčové vlastnosti:

- **Konfigurace Floodfill** - Určuje, zda se váš router účastní jako floodfill peer, který pomáhá síti tím, že ukládá a distribuuje informace ze síťové databáze (netDb). Může to využívat více systémových prostředků, ale posiluje to síť I2P.

- **Pokročilá konfigurace I2P** - Přímý přístup k souboru `router.config`, zobrazující všechny pokročilé konfigurační parametry včetně:
  - Limitů šířky pásma a nastavení shluků
  - Nastavení transportu (NTCP2, SSU2, UDP porty a klíče)
  - Identifikace routeru a informace o verzi
  - Předvoleb konzole a nastavení aktualizací

Většina pokročilých konfiguračních možností není zobrazena v uživatelském rozhraní, protože jsou jen zřídka potřeba. Pro povolení úprav těchto nastavení musíte ručně přidat `routerconsole.advanced=true` do souboru `router.config`.

**Upozornění:** Nesprávná úprava pokročilých nastavení může negativně ovlivnit výkon vašeho routeru nebo jeho konektivitu. Měňte tato nastavení pouze tehdy, pokud víte, co děláte.

### Bandwidth

**URL:** [Konfigurace šířky pásma](http://127.0.0.1:7657/config)

![Konfigurace šířky pásma konzole routeru](/images/router-console-config-bandwidth.png)

Stránka konfigurace šířky pásma umožňuje řídit, kolik šířky pásma váš router přispívá do sítě I2P. I2P funguje nejlépe, když nakonfigurujete své rychlosti tak, aby odpovídaly rychlosti vašeho internetového připojení.

**Klíčová nastavení:**

- **KBps In** - Maximální šířka příchozího pásma, kterou váš router přijme (rychlost stahování)
- **KBps Out** - Maximální šířka odchozího pásma, kterou váš router využije (rychlost odesílání)
- **Share** - Procento vaší odchozí šířky pásma věnované participující komunikaci (pomoc při směrování komunikace pro ostatní)

**Důležité poznámky:**

- Všechny hodnoty jsou v **bajtech za sekundu** (KBps), nikoliv v bitech za sekundu
- Čím více šířky pásma zpřístupníte, tím více pomáháte síti a zlepšujete vlastní anonymitu
- Vaše množství sdílení pro odesílání (KBps Out) určuje váš celkový příspěvek k síti
- Pokud si nejste jisti rychlostí vaší sítě, použijte **Bandwidth Test** k jejímu změření
- Vyšší sdílená šířka pásma zlepšuje jak vaši anonymitu, tak pomáhá posílit síť I2P

Stránka konfigurace zobrazuje odhadovaný měsíční přenos dat na základě vašeho nastavení, což vám pomůže naplánovat alokaci šířky pásma podle limitů vašeho internetového tarifu.

### Client Configuration

**URL:** [Konfigurace klienta](http://127.0.0.1:7657/configclients)

![Konfigurace klientů v konzoli routeru](/images/router-console-config-clients.png)

Stránka Konfigurace klienta umožňuje ovládat, které aplikace a služby I2P se spustí při startu. Zde můžete povolit nebo zakázat vestavěné klienty I2P bez jejich odinstalace.

**Důležité upozornění:** Při změně nastavení zde buďte opatrní. Konzole routeru a aplikační tunely jsou vyžadovány pro většinu použití I2P. Pouze pokročilí uživatelé by měli měnit tato nastavení.

**Dostupní klienti:**

- **Aplikační tunely** - Systém I2PTunnel, který spravuje klientské a serverové tunely (HTTP proxy, IRC atd.)
- **Konzole I2P routeru** - Webové administrační rozhraní, které právě používáte
- **I2P webserver (eepsite)** - Vestavěný Jetty webserver pro hostování vlastní I2P webové stránky
- **Otevřít konzoli routeru ve webovém prohlížeči při spuštění** - Automaticky spustí váš prohlížeč na domovské stránce konzole
- **SAM application bridge** - API most pro připojení aplikací třetích stran k I2P

Každý klient zobrazuje: - **Spustit při startu?** - Zaškrtávací políčko pro povolení/zakázání automatického spuštění - **Ovládání** - Tlačítka Start/Stop pro okamžité ovládání - **Třída a argumenty** - Technické detaily o tom, jak je klient spouštěn

Změny nastavení „Spustit při startu?" vyžadují restart routeru, aby se projevily. Všechny úpravy jsou uloženy do `/var/lib/i2p/i2p-config/clients.config.d/`.

### Pokročilé

**URL:** [Konfigurace I2CP](http://127.0.0.1:7657/configi2cp)

![Router Console I2CP Konfigurace](/images/router-console-config-i2cp.png)

Stránka konfigurace I2CP (I2P Client Protocol) umožňuje nastavit, jak se externí aplikace připojují k vašemu I2P routeru. I2CP je protokol, který aplikace používají ke komunikaci s routerem za účelem vytváření tunelů a odesílání/přijímání dat přes I2P.

**Důležité:** Výchozí nastavení bude fungovat pro většinu uživatelů. Jakékoliv změny provedené zde musí být také nakonfigurovány v externí klientské aplikaci. Mnoho klientů nepodporuje SSL ani autorizaci. **Všechny změny vyžadují restart, aby se projevily.**

**Možnosti konfigurace:**

- **Konfigurace externího I2CP rozhraní**
  - **Povoleno bez SSL** - Standardní I2CP přístup (výchozí a nejkompatibilnější)
  - **Povoleno s vyžadovaným SSL** - Pouze šifrovaná I2CP připojení
  - **Zakázáno** - Blokuje připojení externích klientů přes I2CP

- **I2CP rozhraní** - Síťové rozhraní, na kterém se má naslouchat (výchozí: 127.0.0.1 pouze pro localhost)
- **I2CP port** - Číslo portu pro I2CP připojení (výchozí: 7654)

- **Autorizace**
  - **Vyžadovat uživatelské jméno a heslo** - Povolit autentizaci pro I2CP připojení
  - **Uživatelské jméno** - Nastavit požadované uživatelské jméno pro přístup k I2CP
  - **Heslo** - Nastavit požadované heslo pro přístup k I2CP

**Bezpečnostní upozornění:** Pokud provozujete aplikace pouze na stejném počítači jako váš I2P router, ponechte rozhraní nastavené na `127.0.0.1`, abyste zabránili vzdálenému přístupu. Tato nastavení měňte pouze v případě, že potřebujete umožnit I2P aplikacím z jiných zařízení připojení k vašemu routeru.

### Šířka pásma

**URL:** [Konfigurace sítě](http://127.0.0.1:7657/confignet)

![Router Console konfigurace sítě](/images/router-console-config-network.png)

Stránka Konfigurace sítě umožňuje nastavit, jak se váš I2P router připojuje k internetu, včetně detekce IP adresy, preferencí IPv4/IPv6 a nastavení portů pro UDP i TCP transporty.

**Externě Dostupná IP Adresa:**

- **Použít všechny metody automatické detekce** - Automaticky detekuje vaši veřejnou IP pomocí více metod (doporučeno)
- **Zakázat detekci IP adresy pomocí UPnP** - Zabrání použití UPnP k zjištění vaší IP
- **Ignorovat IP adresu lokálního rozhraní** - Nepoužívat IP adresu vaší lokální sítě
- **Použít pouze detekci IP adresy SSU** - Používat pouze transport SSU2 pro detekci IP
- **Skrytý režim - nepublikovat IP** - Zabrání účasti na síťovém provozu (snižuje anonymitu)
- **Zadat hostname nebo IP** - Manuálně nastavit vaši veřejnou IP nebo hostname

**Konfigurace IPv4:**

- **Zakázat příchozí spojení (za firewallem)** - Zaškrtněte tuto možnost, pokud jste za firewallem, domácí sítí, ISP, DS-Lite nebo carrier-grade NAT, který blokuje příchozí spojení

**Konfigurace IPv6:**

- **Upřednostnit IPv4 před IPv6** - Upřednostňuje IPv4 připojení
- **Upřednostnit IPv6 před IPv4** - Upřednostňuje IPv6 připojení (výchozí pro sítě s dual-stack)
- **Povolit IPv6** - Umožňuje IPv6 připojení
- **Zakázat IPv6** - Zakáže veškerou IPv6 konektivitu
- **Používat pouze IPv6 (zakázat IPv4)** - Experimentální režim pouze s IPv6
- **Zakázat příchozí spojení (Firewalled)** - Zkontrolujte, zda je vaše IPv6 za firewallem

**Akce při změně IP adresy:**

- **Režim notebooku** - Experimentální funkce, která mění identitu routeru a UDP port při změně vaší IP adresy pro zvýšenou anonymitu

**Konfigurace UDP:**

- **Specify Port** - Nastavte specifický UDP port pro SSU2 transport (musí být otevřený ve vašem firewallu)
- **Completely disable** - Vyberte pouze pokud jste za firewallem, který blokuje veškerý odchozí UDP provoz

**Konfigurace TCP:**

- **Zadat port** - Nastavit konkrétní TCP port pro NTCP2 transport (musí být otevřen ve vašem firewallu)
- **Použít stejný port nakonfigurovaný pro UDP** - Zjednodušuje konfiguraci použitím jednoho portu pro oba transporty
- **Použít automaticky detekovanou IP adresu** - Automaticky detekuje vaši veřejnou IP (zobrazuje "currently unknown", pokud ještě nebyla detekována nebo je za firewallem)
- **Vždy použít automaticky detekovanou IP adresu (Není za firewallem)** - Nejlepší pro routery s přímým přístupem k internetu
- **Zakázat příchozí spojení (Za firewallem)** - Zaškrtněte, pokud jsou TCP spojení blokována vaším firewallem
- **Zcela zakázat** - Vyberte pouze v případě, že jste za firewallem, který omezuje nebo blokuje odchozí TCP
- **Zadat hostname nebo IP** - Ručně nakonfigurovat vaši externě dostupnou adresu

**Důležité:** Změny nastavení sítě mohou vyžadovat restart routeru, aby se plně projevily. Správná konfigurace přesměrování portů výrazně zlepšuje výkon vašeho routeru a pomáhá síti I2P.

### Konfigurace klienta

**URL:** [Konfigurace peerů](http://127.0.0.1:7657/configpeer)

![Router Console Peer Configuration](/images/router-console-config-peer.png)

Stránka Konfigurace peerů poskytuje ruční ovládací prvky pro správu jednotlivých peerů v síti I2P. Jedná se o pokročilou funkci, která se obvykle používá pouze pro řešení problémů s problematickými peery.

**Manuální ovládání peerů:**

- **Router Hash** - Zadejte 44znakový base64 router hash peera, kterého chcete spravovat

**Manuální zablokování / odblokování peera:**

Zablokování peer mu zabrání účastnit se jakýchkoliv tunnelů, které vytvoříte. Tato akce: - Zabrání použití peer ve vašich klientských nebo exploratorních tunnelech - Nabývá účinnosti okamžitě bez nutnosti restartu - Trvá, dokud peer ručně neodblokujete nebo nerestartujete svůj router - **Zablokovat peer do restartu** - Dočasně zablokuje peer - **Odblokovat peer** - Odstraní blokaci dříve zablokovaného peer

**Upravit bonusy profilu:**

Bonusy profilů ovlivňují způsob, jakým jsou vybíráni peeři pro účast v tunelech. Bonusy mohou být kladné nebo záporné: - **Rychlí peeři** - Používáni pro klientské tunely vyžadující vysokou rychlost - **Peeři s vysokou kapacitou** - Používáni pro některé exploratory tunely vyžadující spolehlivé směrování - Aktuální bonusy jsou zobrazeny na stránce profilů

**Konfigurace:** - **Rychlost** - Upravit bonus rychlosti pro tento peer (0 = neutrální) - **Kapacita** - Upravit bonus kapacity pro tento peer (0 = neutrální) - **Upravit bonusy peera** - Použít nastavení bonusů

**Případy použití:** - Zakázat peer, který konzistentně způsobuje problémy s připojením - Dočasně vyloučit peer, u kterého máte podezření, že je škodlivý - Upravit bonusy pro snížení priority podprůměrných peerů - Ladit problémy s budováním tunelů vyloučením konkrétních peerů

**Poznámka:** Většina uživatelů tuto funkci nikdy nebude potřebovat. I2P router automaticky spravuje výběr peerů a jejich profilování na základě metrik výkonu.

### Konfigurace I2CP

**URL:** [Konfigurace reseed](http://127.0.0.1:7657/configreseed)

![Router Console Reseed Configuration](/images/router-console-config-reseed.png)

Stránka Konfigurace reseedu vám umožňuje ručně provést reseed vašeho routeru, pokud automatický reseed selže. Reseeding je bootstrapovací proces používaný k nalezení dalších routerů při první instalaci I2P nebo když váš router má příliš málo zbývajících odkazů na routery.

**Kdy použít manuální reseed:**

1. Pokud reseed selhal, měli byste nejprve zkontrolovat své síťové připojení
2. Pokud firewall blokuje vaše připojení k reseed hostitelům, můžete mít přístup k proxy:
   - Proxy může být vzdálená veřejná proxy, nebo může běžet na vašem počítači (localhost)
   - Pro použití proxy nakonfigurujte typ, hostitele a port v sekci Konfigurace Reseedingu
   - Pokud používáte Tor Browser, proveďte reseed přes něj nakonfigurováním SOCKS 5, localhost, port 9150
   - Pokud používáte Tor z příkazové řádky, proveďte reseed přes něj nakonfigurováním SOCKS 5, localhost, port 9050
   - Pokud máte nějaké uzly (peers), ale potřebujete více, můžete zkusit možnost I2P Outproxy. Nechte hostitele a port prázdné. Toto nebude fungovat pro počáteční reseed, když nemáte vůbec žádné uzly
   - Poté klikněte na "Uložit změny a provést reseed nyní"
   - Výchozí nastavení bude fungovat pro většinu uživatelů. Změňte je pouze pokud HTTPS je blokováno restriktivním firewallem a reseed selhal

3. Pokud znáte a důvěřujete někomu, kdo provozuje I2P, požádejte jej, aby vám poslal soubor reseed vygenerovaný pomocí této stránky v jejich router console. Poté použijte tuto stránku k provedení reseed pomocí souboru, který jste obdrželi. Nejprve vyberte soubor níže. Poté klikněte na "Reseed from file"

4. Pokud znáte a důvěřujete někomu, kdo publikuje reseed soubory, požádejte jej o URL. Poté použijte tuto stránku k reseedování pomocí získané URL adresy. Nejprve zadejte URL níže. Pak klikněte na "Reseed from URL"

5. Viz [FAQ](/docs/overview/faq/) pro návod na manuální reseed

**Manuální možnosti reseedu:**

- **Reseed z URL** - Zadejte URL adresu zip nebo su3 souboru z důvěryhodného zdroje a klikněte na "Reseed from URL"
  - Formát su3 je preferován, protože bude ověřen jako podepsaný důvěryhodným zdrojem
  - Formát zip není podepsaný; použijte zip soubor pouze ze zdroje, kterému důvěřujete

- **Reseed ze souboru** - Procházejte a vyberte lokální zip nebo su3 soubor, poté klikněte na "Reseed from file"
  - Reseed soubory můžete najít na [checki2p.com/reseed](https://checki2p.com/reseed)

- **Vytvořit Reseed soubor** - Vygeneruje nový reseed zip soubor, který můžete sdílet s ostatními pro ruční reseed
  - Tento soubor nikdy nebude obsahovat identitu ani IP adresu vašeho vlastního routeru

**Konfigurace reseedingu:**

Výchozí nastavení budou fungovat pro většinu uživatelů. Změňte je pouze v případě, že HTTPS je blokováno restriktivním firewallem a reseed selhal.

- **URL adresy pro reseed** - Seznam HTTPS URL adres k reseed serverům (výchozí seznam je vestavěný a pravidelně aktualizovaný)
- **Konfigurace proxy** - Nastavení HTTP/HTTPS/SOCKS proxy, pokud potřebujete přistupovat k reseed serverům přes proxy
- **Obnovit seznam URL** - Obnovení výchozího seznamu reseed serverů

**Důležité:** Ruční reseed by měl být nutný pouze ve vzácných případech, kdy automatický reseed opakovaně selže. Většina uživatelů nikdy nebude potřebovat používat tuto stránku.

### Konfigurace sítě

**URL:** [Konfigurace rodiny routerů](http://127.0.0.1:7657/configfamily)

![Konfigurace rodiny routerů v konzoli routeru](/images/router-console-config-family.png)

Stránka Konfigurace rodiny routerů umožňuje spravovat rodiny routerů. Routery ve stejné rodině sdílejí rodinný klíč, který je identifikuje jako provozované stejnou osobou nebo organizací. To zabraňuje tomu, aby byly vybrány více routerů, které ovládáte, pro stejný tunnel, což by snížilo anonymitu.

**Co je Router Family?**

Když provozujete více I2P routerů, měli byste je nakonfigurovat jako součást stejné rodiny. To zajistí: - Vaše routery nebudou použity společně ve stejné tunnel cestě - Ostatní uživatelé si zachovají správnou anonymitu, když jejich tunnely používají vaše routery - Síť může správně distribuovat účast v tunnelech

**Aktuální rodina:**

Stránka zobrazuje aktuální název rodiny vašeho routeru. Pokud nejste součástí rodiny, bude toto pole prázdné.

**Exportovat rodinný klíč:**

- **Exportujte tajný rodinný klíč pro import do dalších routerů, které ovládáte**
- Klikněte na "Export Family Key" pro stažení souboru s rodinným klíčem
- Importujte tento klíč na svých dalších routerech, abyste je přidali do stejné rodiny

**Opustit rodinu routerů:**

- **Již nebýt členem rodiny**
- Klikněte na „Opustit rodinu" pro odebrání tohoto routeru z jeho současné rodiny
- Tuto akci nelze vrátit zpět bez opětovného importu klíče rodiny

**Důležité aspekty:**

- **Vyžadována veřejná registrace:** Aby byla vaše rodina rozpoznána v celé síti, musí být váš rodinný klíč přidán do kódové základny I2P vývojovým týmem. Tím je zajištěno, že všechny routery v síti o vaší rodině vědí.
- **Kontaktujte tým I2P** pro registraci vašeho rodinného klíče, pokud provozujete více veřejných routerů
- Většina uživatelů provozujících pouze jeden router tuto funkci nikdy nebude potřebovat
- Konfigurace rodiny se primárně používá provozovateli více veřejných routerů nebo poskytovateli infrastruktury

**Případy použití:**

- Provozování více I2P routerů pro redundanci
- Provozování infrastruktury jako reseed servery nebo outproxy na více strojích
- Správa sítě I2P routerů pro organizaci

### Konfigurace peerů

**URL:** [Konfigurace tunelu](http://127.0.0.1:7657/configtunnels)

![Konfigurace tunelů v konzoli routeru](/images/router-console-config-tunnels.png)

Stránka Konfigurace tunelů umožňuje upravit výchozí nastavení tunelů jak pro exploratory tunnels (používané pro komunikaci routeru), tak pro client tunnels (používané aplikacemi). **Výchozí nastavení vyhovuje většině uživatelů a mělo by být měněno pouze tehdy, pokud rozumíte kompromisům.**

**Důležitá upozornění:**

⚠️ **Kompromis mezi anonymitou a výkonem:** Existuje základní kompromis mezi anonymitou a výkonem. Tunnely delší než 3 hopy (například 2 hopy + 0-2 hopy, 3 hopy + 0-1 hopy, 3 hopy + 0-2 hopy), nebo vysoké množství + záložní množství, mohou výrazně snížit výkon nebo spolehlivost. Může dojít k vysokému využití CPU a/nebo velké šířce odchozího pásma. Tato nastavení měňte opatrně a upravte je, pokud budete mít problémy.

⚠️ **Trvalost:** Změny nastavení průzkumných tunnelů jsou uloženy v souboru router.config. Změny klientských tunnelů jsou dočasné a nejsou ukládány. Pro trvalé změny klientských tunnelů viz [stránka I2PTunnel](/docs/api/i2ptunnel).

**Průzkumné tunely:**

Explorační tunely jsou využívány vaším routerem ke komunikaci se síťovou databází a k účasti v síti I2P.

Možnosti konfigurace pro Inbound i Outbound: - **Length** - Počet hopů v tunelu (výchozí: 2-3 hopy) - **Randomization** - Náhodná odchylka v délce tunelu (výchozí: 0-1 hopů) - **Quantity** - Počet aktivních tunelů (výchozí: 2 tunely) - **Backup quantity** - Počet záložních tunelů připravených k aktivaci (výchozí: 0 tunelů)

**Klientské tunely pro I2P webserver:**

Tato nastavení řídí tunely pro vestavěný I2P webserver (eepsite).

⚠️ **VAROVÁNÍ ANONYMITY** - Nastavení zahrnuje 1-hop tunely. ⚠️ **VAROVÁNÍ VÝKONU** - Nastavení zahrnuje vysoké množství tunelů.

Možnosti konfigurace pro Inbound i Outbound: - **Length** - Délka tunelu (výchozí: 1 hop pro webserver) - **Randomization** - Náhodná odchylka v délce tunelu - **Quantity** - Počet aktivních tunelů - **Backup quantity** - Počet záložních tunelů

**Klientské tunely pro sdílené klienty:**

Tato nastavení se vztahují na sdílené klientské aplikace (HTTP proxy, IRC atd.).

Možnosti konfigurace pro Inbound i Outbound: - **Length** - Délka tunelu (výchozí: 3 skoky) - **Randomization** - Náhodná odchylka v délce tunelu - **Quantity** - Počet aktivních tunelů - **Backup quantity** - Počet záložních tunelů

**Porozumění parametrům tunelů:**

- **Délka:** Delší tunely poskytují vyšší anonymitu, ale snižují výkon a spolehlivost
- **Randomizace:** Přidává nepředvídatelnost do cest tunelů, čímž zlepšuje zabezpečení
- **Množství:** Více tunelů zlepšuje spolehlivost a distribuci zátěže, ale zvyšuje spotřebu zdrojů
- **Záložní množství:** Předem vytvořené tunely připravené k nahrazení selhavších tunelů, zlepšující odolnost

**Osvědčené postupy:**

- Ponechte výchozí nastavení, pokud nemáte specifické potřeby
- Zvyšte délku tunelu pouze v případě, že je anonymita kritická a můžete akceptovat pomalejší výkon
- Zvyšte počet/zálohy pouze v případě, že dochází k častým selháním tunelů
- Sledujte výkon routeru po provedení změn
- Klikněte na "Save changes" pro aplikaci úprav

### Konfigurace Reseed

**URL:** [Konfigurace uživatelského rozhraní](http://127.0.0.1:7657/configui)

![Konfigurace UI konzole routeru](/images/router-console-config-ui.png)

Stránka Konfigurace UI vám umožňuje přizpůsobit vzhled a přístupnost vaší konzole routeru, včetně výběru tématu, jazykových předvoleb a ochrany heslem.

**Téma konzole routeru:**

Vyberte si mezi tmavým a světlým tématem pro rozhraní konzole routeru:
- **Tmavý** - Tmavý režim (šetrnější k očím při slabém osvětlení)
- **Světlý** - Světlý režim (tradiční vzhled)

Další možnosti motivu: - **Nastavit motiv univerzálně pro všechny aplikace** - Použít zvolený motiv pro všechny I2P aplikace, nejen pro konzoli routeru - **Vynutit použití mobilní konzole** - Používat rozhraní optimalizované pro mobilní zařízení i v prohlížečích na počítači - **Integrovat aplikace Email a Torrent do konzole** - Začlenit Susimail a I2PSnark přímo do rozhraní konzole místo jejich otevírání v samostatných záložkách

**Jazyk konzole routeru:**

Vyberte si preferovaný jazyk pro rozhraní konzole routeru z rozbalovací nabídky. I2P podporuje mnoho jazyků včetně angličtiny, němčiny, francouzštiny, španělštiny, ruštiny, čínštiny, japonštiny a dalších.

**Příspěvky k překladům jsou vítány:** Pokud si všimnete neúplných nebo nesprávných překladů, můžete pomoci vylepšit I2P tím, že přispějete do překladatelského projektu. Kontaktujte vývojáře v #i2p-dev na IRC nebo zkontrolujte zprávu o stavu překladu (odkaz na stránce).

**Heslo pro Router Console:**

Přidejte autentizaci pomocí uživatelského jména a hesla pro ochranu přístupu ke konzoli vašeho routeru:

- **Uživatelské jméno** - Zadejte uživatelské jméno pro přístup ke konzoli
- **Heslo** - Zadejte heslo pro přístup ke konzoli
- **Přidat uživatele** - Vytvořit nového uživatele se zadanými přihlašovacími údaji
- **Smazat vybrané** - Odstranit existující uživatelské účty

**Proč přidat heslo?**

- Zabraňuje neoprávněnému místnímu přístupu ke konzoli vašeho routeru
- Nezbytné, pokud váš počítač používá více osob
- Doporučeno, pokud je konzole vašeho routeru přístupná v místní síti
- Chrání vaši I2P konfiguraci a nastavení soukromí před neoprávněnými změnami

**Bezpečnostní upozornění:** Ochrana heslem ovlivňuje pouze přístup k webovému rozhraní konzole routeru na adrese [I2P Router Console](http://127.0.0.1:7657). Nešifruje provoz I2P ani nebrání aplikacím v použití I2P. Pokud jste jediným uživatelem svého počítače a konzole routeru naslouchá pouze na localhost (výchozí nastavení), heslo nemusí být nutné.

### Konfigurace rodiny routerů

**URL:** [Konfigurace WebApp](http://127.0.0.1:7657/configwebapps)

![Konfigurace WebApp Router Console](/images/router-console-config-webapps.png)

Stránka Konfigurace webových aplikací umožňuje spravovat Java webové aplikace, které běží ve vašem I2P routeru. Tyto aplikace jsou spouštěny klientem webConsole a běží ve stejném JVM jako router, poskytující integrovanou funkcionalitu přístupnou prostřednictvím konzole routeru.

**Co jsou WebApps?**

WebApps jsou aplikace založené na Javě, které mohou být: - **Kompletní aplikace** (např. I2PSnark pro torrenty) - **Front-endy k dalším klientům**, které musí být samostatně povoleny (např. Susidns, I2PTunnel) - **Webové aplikace bez webového rozhraní** (např. adresář kontaktů)

**Důležité poznámky:**

- Webová aplikace může být zcela zakázána, nebo může být pouze zakázáno její spuštění při startu
- Odstranění war souboru z adresáře webapps zakáže webovou aplikaci úplně
- War soubor a adresář webové aplikace se však znovu objeví, když aktualizujete svůj router na novější verzi
- **Pro trvalé zakázání webové aplikace:** Zakažte ji zde, což je preferovaná metoda

**Dostupné WebAplikace:**

| WebApp | Description |
|--------|-------------|
| **i2psnark** | Torrents - Built-in BitTorrent client for I2P |
| **i2ptunnel** | Hidden Services Manager - Configure client and server tunnels |
| **imagegen** | Identification Image Generator - Creates unique identicons |
| **jsonrpc** | jsonrpc.war - JSON-RPC API interface (disabled by default) |
| **routerconsole** | I2P Router Console - The main administrative interface |
| **susidns** | Address Book - Manage I2P addresses and subscriptions |
| **susimail** | Email - Web-based email client for I2P |
**Ovládání:**

Pro každou webovou aplikaci: - **Spustit při startu?** - Zaškrtávací políčko pro povolení/zakázání automatického spuštění - **Ovládání** - Tlačítka Start/Stop pro okamžité ovládání   - **Stop** - Zastaví aktuálně běžící webovou aplikaci   - **Start** - Spustí zastavenou webovou aplikaci

**Tlačítka konfigurace:**

- **Zrušit** - Zahodit změny a vrátit se na předchozí stránku
- **Uložit konfiguraci WebApp** - Uložit změny a aplikovat je

**Případy použití:**

- Zastavte I2PSnark, pokud nepoužíváte torrenty, abyste ušetřili zdroje
- Zakažte jsonrpc, pokud nepotřebujete API přístup
- Zastavte Susimail, pokud používáte externí emailového klienta
- Dočasně zastavte webapps pro uvolnění paměti nebo řešení problémů

**Tip pro výkon:** Vypnutí nepoužívaných webových aplikací může snížit spotřebu paměti a zlepšit výkon routeru, zejména na systémech s nízkými prostředky.

## Help

**URL:** [Nápověda](http://127.0.0.1:7657/help)

Stránka Nápověda poskytuje komplexní dokumentaci a zdroje, které vám pomohou pochopit a efektivně používat I2P. Slouží jako centrální rozcestník pro řešení problémů, učení a získávání podpory.

**Co zde naleznete:**

- **Rychlý průvodce** - Základní informace pro nové uživatele začínající s I2P
- **Často kladené otázky (FAQ)** - Odpovědi na běžné dotazy týkající se instalace, konfigurace a používání I2P
- **Řešení problémů** - Řešení běžných problémů a potíží s připojením
- **Technická dokumentace** - Podrobné informace o protokolech I2P, architektuře a specifikacích
- **Průvodce aplikacemi** - Návody pro používání aplikací I2P jako torrenty, e-mail a skryté služby
- **Informace o síti** - Pochopení fungování I2P a toho, co ji činí bezpečnou
- **Zdroje podpory** - Odkazy na fóra, IRC kanály a komunitní podporu

**Získání pomoci:**

Pokud máte problémy s I2P: 1. Zkontrolujte FAQ pro běžné otázky a odpovědi 2. Projděte si sekci řešení problémů pro váš konkrétní problém 3. Navštivte I2P fórum na [i2pforum.i2p](http://i2pforum.i2p) nebo [i2pforum.net](https://i2pforum.net) 4. Připojte se na IRC kanál #i2p pro podporu komunity v reálném čase 5. Prohledejte dokumentaci pro podrobné technické informace

**Tip:** Nápověda je vždy dostupná z postranního panelu konzole routeru, takže můžete snadno najít pomoc, kdykoli ji potřebujete.

## Performance Graphs

**URL:** [Grafy výkonu](http://127.0.0.1:7657/graphs)

![Grafy výkonu konzole routeru](/images/router-console-graphs.png)

Stránka Grafy výkonu poskytuje vizuální monitoring v reálném čase výkonu vašeho I2P routeru a síťové aktivity. Tyto grafy vám pomáhají pochopit využití šířky pásma, připojení k peerům, spotřebu paměti a celkové zdraví routeru.

**Dostupné grafy:**

- **Využití šířky pásma**
  - **Rychlost odesílání na nízké úrovni (bajty/s)** - Rychlost odchozího provozu
  - **Rychlost přijímání na nízké úrovni (bajty/s)** - Rychlost příchozího provozu
  - Zobrazuje aktuální, průměrné a maximální využití šířky pásma
  - Pomáhá sledovat, zda se blížíte k nakonfigurovaným limitům šířky pásma

- **Aktivní protějšky**
  - **router.activePeers průměrováno za 60 sec** - Počet protějšků, se kterými aktivně komunikujete
  - Ukazuje stav vašeho síťového připojení
  - Více aktivních protějšků obecně znamená lepší budování tunelů a účast v síti

- **Využití paměti routeru**
  - **router.memoryUsed průměr za 60 sec** - spotřeba paměti JVM
  - Zobrazuje aktuální, průměrné a maximální využití paměti v MB
  - Užitečné pro identifikaci úniků paměti nebo určení, zda je třeba zvýšit velikost Java heap

**Konfigurace zobrazení grafu:**

Přizpůsobte způsob zobrazení a aktualizace grafů:

- **Velikost grafu** - Nastavte šířku (výchozí: 400 pixelů) a výšku (výchozí: 100 pixelů)
- **Zobrazované období** - Časový rozsah k zobrazení (výchozí: 60 minut)
- **Interval obnovení** - Jak často se grafy aktualizují (výchozí: 5 minut)
- **Typ grafu** - Vyberte mezi zobrazením průměrů nebo událostí
- **Skrýt legendu** - Odebere legendu z grafů pro ušetření místa
- **UTC** - Použije UTC čas místo lokálního času v grafech
- **Persistence** - Ukládá data grafů na disk pro historickou analýzu

**Pokročilé možnosti:**

Klikněte na **[Select Stats]** pro výběr statistik k zobrazení v grafu: - Metriky tunelů (úspěšnost vytváření, počet tunelů atd.) - Statistiky síťové databáze - Statistiky transportu (NTCP2, SSU2) - Výkon klientských tunelů - A mnoho dalších podrobných metrik

**Případy použití:**

- Sledujte šířku pásma, abyste zajistili, že nepřekračujete nastavené limity
- Ověřte konektivitu s peery při řešení problémů se sítí
- Sledujte využití paměti pro optimalizaci nastavení Java heap
- Identifikujte výkonnostní vzory v průběhu času
- Diagnostikujte problémy s budováním tunnelů korelací grafů

**Tip:** Klikněte na „Uložit nastavení a překreslit grafy" po provedení změn pro aplikaci vaší konfigurace. Grafy se automaticky obnoví na základě vašeho nastavení obnovovacího zpoždění.
