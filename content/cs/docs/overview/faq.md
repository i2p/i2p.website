---
title: "Často kladené otázky"
description: "Komplexní I2P FAQ: pomoc s routerem, konfigurace, reseedy, soukromí/bezpečnost, výkon a řešení problémů"
slug: "faq"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

## Nápověda pro I2P Router

### Na jakých systémech poběží I2P? {#systems}

I2P je napsáno v programovacím jazyce Java. Bylo testováno na Windows, Linux, FreeBSD a OSX. K dispozici je také verze pro Android.

Pokud jde o využití paměti, I2P je ve výchozím nastavení nakonfigurováno tak, aby používalo 128 MB RAM. To je dostačující pro procházení webu a používání IRC. Jiné aktivity však mohou vyžadovat větší přidělení paměti. Například pokud chce někdo provozovat router s vysokou šířkou pásma, účastnit se I2P torrentů nebo provozovat skryté služby s vysokým provozem, je potřeba vyšší množství paměti.

Pokud jde o využití CPU, I2P bylo testováno na skromných systémech, jako je řada jednodeskových počítačů Raspberry Pi. Protože I2P intenzivně využívá kryptografické techniky, výkonnější CPU bude lépe zvládat zátěž generovanou I2P i úkoly související se zbytkem systému (tj. operační systém, GUI, další procesy např. prohlížení webu).

Doporučuje se použít Sun/Oracle Java nebo OpenJDK.

### Je pro používání I2P vyžadována instalace Javy? {#java}

Ano, Java je vyžadována pro používání I2P Core. Do našich jednoduchých instalátorů pro Windows, Mac OSX a Linux zahrnujeme Javu. Pokud používáte aplikaci I2P pro Android, budete ve většině případů potřebovat také Java runtime jako Dalvik nebo ART.

### Co je "I2P Site" a jak nakonfiguruji svůj prohlížeč, abych je mohl používat? {#I2P-Site}

I2P Site je běžná webová stránka s tím rozdílem, že je hostována uvnitř I2P. I2P sites mají adresy, které vypadají jako běžné internetové adresy, končící na ".i2p" v lidsky čitelné, nekryptografické podobě pro usnadnění lidem. Samotné připojení k I2P Site vyžaduje kryptografii, což znamená, že adresy I2P Site jsou také dlouhé "Base64" Destinations a kratší "B32" adresy. Možná budete muset provést dodatečnou konfiguraci pro správné procházení. Procházení I2P Sites vyžaduje aktivaci HTTP Proxy ve vaší instalaci I2P a následnou konfiguraci prohlížeče pro její použití. Pro více informací prozkoumejte sekci "Prohlížeče" níže nebo průvodce "Konfigurace prohlížeče".

### Co znamenají čísla Aktivní x/y v konzoli routeru? {#active}

Na stránce Peers ve vaší konzoli routeru můžete vidět dvě čísla - Active x/y. První číslo je počet peerů, kterým jste odeslali nebo od kterých jste obdrželi zprávu v posledních několika minutách. Druhé číslo je počet peerů viděných nedávno, toto číslo bude vždy větší nebo rovno prvnímu číslu.

### Můj router má velmi málo aktivních peerů, je to v pořádku? {#peers}

Ano, to může být normální, zejména když byl router právě spuštěn. Nové routery potřebují čas na spuštění a připojení ke zbytku sítě. Pro zlepšení integrace do sítě, doby provozu a výkonu zkontrolujte tato nastavení:

- **Sdílení šířky pásma** - Pokud je router nakonfigurován ke sdílení šířky pásma, bude směrovat více provozu pro ostatní routery, což pomáhá integrovat ho se zbytkem sítě a zároveň zlepšuje výkon místního připojení. Lze nakonfigurovat na stránce [http://localhost:7657/config](http://localhost:7657/config).
- **Síťové rozhraní** - Ujistěte se, že na stránce [http://localhost:7657/confignet](http://localhost:7657/confignet) není zadáno žádné rozhraní. To může snížit výkon, pokud váš počítač nemá více domovských připojení s více externími IP adresami.
- **I2NP protokol** - Ujistěte se, že router je nakonfigurován tak, aby očekával připojení na platném protokolu pro operační systém hostitele a prázdném nastavení sítě (Pokročilé). Nevyplňujte IP adresu do pole 'Hostname' na stránce konfigurace sítě. I2NP protokol, který zde vyberete, bude použit pouze v případě, že ještě nemáte dostupnou adresu. Například většina bezdrátových připojení Verizon 4G a 5G ve Spojených státech blokuje UDP a nelze se k nim přes něj dostat. Jiní by používali UDP násilně, i když je pro ně dostupné. Vyberte rozumné nastavení ze seznamu I2NP protokolů.

### Jsem proti určitým typům obsahu. Jak mohu zabránit jejich distribuci, ukládání nebo přístupu k nim? {#badcontent}

Žádný takový obsah není ve výchozím nastavení nainstalován. Protože je však I2P peer-to-peer síť, je možné, že můžete náhodně narazit na zakázaný obsah. Zde je shrnutí, jak vás I2P chrání před nežádoucím zapojením do porušování vašich přesvědčení.

- **Distribuce** - Provoz je interní v rámci sítě I2P, nejste [exit node](#exit) (v naší dokumentaci označovaný jako outproxy).
- **Úložiště** - Síť I2P neprovádí distribuované ukládání obsahu, to musí být specificky nainstalováno a nakonfigurováno uživatelem (například s Tahoe-LAFS). To je funkce jiné anonymní sítě, [Freenet](http://freenetproject.org/). Provozováním I2P routeru neukládáte obsah pro nikoho.
- **Přístup** - Váš router nebude vyžadovat žádný obsah bez vašeho konkrétního pokynu k tomu.

### Je možné zablokovat I2P? {#blocking}

Ano, zdaleka nejjednodušší a nejběžnější způsob je blokování bootstrap serverů, neboli "Reseed" serverů. Úplné blokování veškerého obfuskovaného provozu by také fungovalo (ačkoli by to narušilo mnoho dalších věcí, které nejsou I2P, a většina není ochotna zajít tak daleko). V případě blokování reseed serverů existuje reseed balíček na Github, jeho zablokováním zablokujete také Github. Můžete provést reseed přes proxy (mnoho jich lze najít na internetu, pokud nechcete použít Tor) nebo sdílet reseed balíčky na základě přátelství offline.

### V souboru `wrapper.log` se zobrazuje chyba s textem "`Protocol family unavailable`" při načítání konzole routeru {#protocolfamily}

Tato chyba se často vyskytuje u jakéhokoli síťového java softwaru na některých systémech, které jsou ve výchozím nastavení nakonfigurovány pro použití IPv6. Existuje několik způsobů, jak toto vyřešit:

- Na systémech založených na Linuxu můžete použít `echo 0 > /proc/sys/net/ipv6/bindv6only`
- Vyhledejte následující řádky v `wrapper.config`:
  ```
  #wrapper.java.additional.5=-Djava.net.preferIPv4Stack=true
  #wrapper.java.additional.6=-Djava.net.preferIPv6Addresses=false
  ```
  Pokud tam tyto řádky jsou, odkomentujte je odstraněním "#". Pokud tam řádky nejsou, přidejte je bez "#".

Další možností by bylo odstranit `::1` z `~/.i2p/clients.config`

**VAROVÁNÍ**: Aby se jakékoli změny v `wrapper.config` projevily, musíte zcela zastavit router i wrapper. Kliknutí na *Restart* v konzoli routeru tento soubor NEPŘEČTE znovu! Musíte kliknout na *Shutdown*, počkat 11 minut a poté spustit I2P.

### Většina I2P Sites v rámci I2P nefunguje? {#down}

Pokud vezmete v úvahu každý I2P Site, který kdy byl vytvořen, ano, většina z nich je nedostupná. Lidé i I2P Sites přicházejí a odcházejí. Dobrým způsobem, jak začít v I2P, je podívat se na seznam I2P Sites, které jsou aktuálně v provozu. [identiguy.i2p](http://identiguy.i2p) sleduje aktivní I2P Sites.

### Proč I2P naslouchá na portu 32000? {#port32000}

Tanuki java service wrapper, který používáme, otevírá tento port — vázaný na localhost — aby mohl komunikovat se softwarem běžícím uvnitř JVM. Když je JVM spuštěn, obdrží klíč, aby se mohl připojit k wrapperu. Poté, co JVM naváže své spojení s wrapperem, wrapper odmítne jakákoli další připojení.

Více informací naleznete v [dokumentaci wrapperu](http://wrapper.tanukisoftware.com/doc/english/prop-port.html).

### Jak nakonfiguruji svůj prohlížeč? {#browserproxy}

Konfigurace proxy pro různé prohlížeče je na samostatné stránce se snímky obrazovky. Pokročilejší konfigurace s externími nástroji, jako je rozšíření prohlížeče FoxyProxy nebo proxy server Privoxy, jsou možné, ale mohou do vašeho nastavení vnést bezpečnostní rizika.

### Jak se připojím k IRC v rámci I2P? {#irc}

Tunel k hlavnímu IRC serveru v rámci I2P, Irc2P, je vytvořen při instalaci I2P (viz [konfigurační stránka I2PTunnel](http://localhost:7657/i2ptunnel/index.jsp)) a je automaticky spuštěn při startu I2P routeru. Pro připojení nastavte ve svém IRC klientovi připojení na `localhost 6668`. Uživatelé klientů typu HexChat mohou vytvořit novou síť se serverem `localhost/6668` (nezapomeňte zaškrtnout "Obejít proxy server", pokud máte nakonfigurovaný proxy server). Uživatelé Weechat mohou použít následující příkaz pro přidání nové sítě:

```
/server add irc2p localhost/6668
```
### Jak si mohu nastavit vlastní I2P Site? {#myI2P-Site}

Nejjednodušší metodou je kliknout na odkaz [i2ptunnel](http://127.0.0.1:7657/i2ptunnel/) v konzoli routeru a vytvořit nový 'Server Tunnel'. Dynamický obsah můžete poskytovat nastavením cílové destinace tunelu na port existującího webového serveru, například Tomcat nebo Jetty. Můžete také poskytovat statický obsah. Pro tento účel nastavte cílovou destinaci tunelu na: `0.0.0.0 port 7659` a umístěte obsah do adresáře `~/.i2p/eepsite/docroot/`. (Na systémech jiných než Linux může být umístění jiné. Zkontrolujte konzoli routeru.) Software 'eepsite' je součástí instalačního balíčku I2P a je nastaven tak, aby se automaticky spustil při startu I2P. Výchozí stránka, která se tímto vytvoří, je přístupná na http://127.0.0.1:7658. Váš 'eepsite' je však přístupný i ostatním prostřednictvím vašeho souboru s klíčem eepsite, který se nachází v: `~/.i2p/eepsite/i2p/eepsite.keys`. Pro více informací si přečtěte soubor readme na adrese: `~/.i2p/eepsite/README.txt`.

### Pokud na I2P doma hostím webovou stránku obsahující pouze HTML a CSS, je to nebezpečné? {#hosting}

Záleží na vašem protivníkovi a vašem modelu hrozeb. Pokud se obáváte pouze korporátního porušování „soukromí", běžných zločinců a cenzury, pak to není opravdu nebezpečné. Orgány činné v trestním řízení vás pravděpodobně stejně najdou, pokud budou skutečně chtít. Pouze hostování, když máte spuštěný běžný (internetový) domácí uživatelský prohlížeč, ztíží skutečné zjištění, kdo danou část hostuje. Považujte prosím hostování vaší I2P stránky stejně jako hostování jakékoli jiné služby - je to stejně nebezpečné - nebo bezpečné - jak to sami nakonfigurujete a spravujete.

Poznámka: Již existuje způsob, jak oddělit hostování i2p služby (destination) od i2p routeru. Pokud [rozumíte tomu, jak](/docs/overview/tech-intro#i2pservices) to funguje, můžete jednoduše nastavit samostatný stroj jako server pro webovou stránku (nebo službu), která bude veřejně přístupná, a přesměrovat ji na webserver přes [velmi] zabezpečený SSH tunel nebo použít zabezpečený, sdílený souborový systém.

### Jak I2P nachází webové stránky „.i2p"? {#addresses}

Aplikace I2P Adresář mapuje lidsky čitelná jména na dlouhodobé destinace spojené se službami, což ji činí podobnější souboru hosts nebo seznamu kontaktů než síťové databázi nebo DNS službě. Je také zaměřená na lokální úložiště – neexistuje uznávaný globální jmenný prostor, vy sami rozhodujete, na co se kterákoli daná .i2p doména nakonec mapuje. Střední cestou je něco, čemu se říká "Jump Service" (služba pro přesměrování), která poskytuje lidsky čitelné jméno tím, že vás přesměruje na stránku, kde budete dotázáni: "Dáváte I2P routeru oprávnění nazývat $SITE_CRYPTO_KEY jménem $SITE_NAME.i2p" nebo něco v tom smyslu. Jakmile je záznam v adresáři, můžete si generovat vlastní jump URL adresy, které pomohou sdílet web s ostatními.

### Jak přidám adresy do Adresáře? {#addressbook}

Nemůžete přidat adresu, aniž byste znali alespoň base32 nebo base64 stránky, kterou chcete navštívit. "Hostname" (název hostitele), který je čitelný pro člověka, je pouze alias pro kryptografickou adresu, která odpovídá base32 nebo base64. Bez kryptografické adresy neexistuje způsob, jak přistupovat k I2P Site (I2P stránce), to je záměrné. Distribuce adresy lidem, kteří ji ještě neznají, je obvykle zodpovědností poskytovatele služby Jump. Návštěva neznámé I2P Site spustí použití služby Jump. stats.i2p je nejspolehlivější služba Jump.

Pokud hostujete stránku přes i2ptunnel, zatím nebude mít registraci u jump service. Chcete-li ji dát lokální URL, navštivte konfigurační stránku a klikněte na tlačítko "Add to Local Address Book" (Přidat do místního adresáře). Poté přejděte na http://127.0.0.1:7657/dns, kde najdete addresshelper URL a můžete ji sdílet.

### Jaké porty I2P používá? {#ports}

Porty používané I2P lze rozdělit do 2 sekcí:

1. Porty s přístupem k internetu, které se používají pro komunikaci s ostatními I2P routery
2. Lokální porty pro místní připojení

Ty jsou podrobně popsány níže.

#### 1. Porty otevřené do internetu

Poznámka: Od verze 0.7.8 nové instalace nepoužívají port 8887; při prvním spuštění programu je vybrán náhodný port mezi 9000 a 31000. Vybraný port je zobrazen na [konfigurační stránce](http://127.0.0.1:7657/confignet) routeru.

**ODCHOZÍ**

- UDP z náhodného portu uvedeného na [konfigurační stránce](http://127.0.0.1:7657/confignet) na libovolné vzdálené UDP porty, umožňující odpovědi
- TCP z náhodných vysokých portů na libovolné vzdálené TCP porty
- Odchozí UDP na portu 123, umožňující odpovědi. To je nezbytné pro interní časovou synchronizaci I2P (prostřednictvím SNTP - dotazování na náhodný SNTP host v pool.ntp.org nebo jiný server, který určíte)

**PŘÍCHOZÍ**

- (Volitelné, doporučeno) UDP na port uvedený na [konfigurační stránce](http://127.0.0.1:7657/confignet) z libovolných umístění
- (Volitelné, doporučeno) TCP na port uvedený na [konfigurační stránce](http://127.0.0.1:7657/confignet) z libovolných umístění
- Příchozí TCP může být zakázáno na [konfigurační stránce](http://127.0.0.1:7657/confignet)

#### 2. Lokální I2P porty

Lokální I2P porty ve výchozím nastavení naslouchají pouze lokálním připojením, kromě případů, kde je uvedeno jinak:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">PORT</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">PURPOSE</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">DESCRIPTION</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1900</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UPnP SSDP UDP multicast listener</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Cannot be changed. Binds to all interfaces. May be disabled on <a href="http://127.0.0.1:7657/confignet">confignet</a>.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2827</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">BOB bridge</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">A higher level socket API for clients. Disabled by default. May be enabled/disabled on <a href="http://127.0.0.1:7657/configclients">configclients</a>. May be changed in the bob.config file.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4444</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HTTP proxy</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Configured on <a href="http://127.0.0.1:7657/configclients">configclients</a>, go to the page <a href="http://127.0.0.1:7657/i2ptunnel/">i2ptunnel</a> to start/stop it and on the page <a href="http://127.0.0.1:7657/i2ptunnel/web/0">I2P HTTP Proxy</a> to configure it. Include in your browser's proxy configuration for HTTP</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4445</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HTTPS proxy</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Configured on <a href="http://127.0.0.1:7657/configclients">configclients</a>, go to the page <a href="http://127.0.0.1:7657/i2ptunnel/">i2ptunnel</a> to start/stop it and on the page <a href="http://127.0.0.1:7657/i2ptunnel/web/1">I2P HTTPS Proxy</a> to configure it. Include in your browser's proxy configuration for HTTPS</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6668</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">IRC proxy</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">A tunnel to the inside-the-I2P IRC network. Disabled by default. Configured on the page <a href="http://127.0.0.1:7657/i2ptunnel/web/2">irc.postman.i2p (IRC proxy)</a> and may be enabled/disabled on the page <a href="http://127.0.0.1:7657/i2ptunnel/">i2ptunnel</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7654</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2CP (client protocol) port</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For advanced client usage. Do not expose to an external network.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7656</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SAM bridge</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">A socket API for clients. Disabled by default. May be enabled/disabled on <a href="http://127.0.0.1:7657/configclients">configclients</a> and configured on <a href="http://127.0.0.1:7657/sam">sam</a>.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7657 (or 7658 via SSL)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Router console</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">The router console provides valuable information about your router and the network, in addition to giving you access to configure your router and its associated applications.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7659</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">'eepsite' - an example webserver (Jetty)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Included in the <code>i2pinstall</code> and <code>i2pupdate</code> packages - may be disabled if another webserver is available. May be configured on the page <a href="http://127.0.0.1:7657/i2ptunnel/web/3">eepsite</a> and disabled on the page <a href="http://127.0.0.1:7657/i2ptunnel/">i2ptunnel</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7660</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2PTunnel UDP port for SSH</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Required for Grizzled's/novg's UDP support. Instances disabled by default. May be enabled/disabled and configured to use a different port on the page <a href="http://127.0.0.1:7657/i2ptunnel/">i2ptunnel</a>.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">123</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NTP Port</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Used by <a href="http://127.0.0.1:7657/confignet">NTP Time Sync</a>. May be disabled/changed.</td>
    </tr>
  </tbody>
</table>
### V adresáři mi chybí spousta hostitelů. Jaké jsou dobré odkazy pro odběr? {#subscriptions}

Adresář se nachází na [http://localhost:7657/dns](http://localhost:7657/dns), kde najdete další informace.

**Jaké jsou dobré odkazy na odběr adresáře?**

Můžete zkusit následující:

- [http://stats.i2p/cgi-bin/newhosts.txt](http://stats.i2p/cgi-bin/newhosts.txt)
- [http://identiguy.i2p/hosts.txt](http://identiguy.i2p/hosts.txt)

### Jak mohu přistupovat k webové konzoli z jiných počítačů nebo ji chránit heslem? {#remote_webconsole}

Z bezpečnostních důvodů admin konzole routeru ve výchozím nastavení přijímá připojení pouze na lokálním rozhraní.

Existují dvě metody pro vzdálený přístup ke konzoli:

1. SSH tunel
2. Konfigurace vaší konzole tak, aby byla dostupná na veřejné IP adrese s uživatelským jménem a heslem

Níže jsou uvedeny podrobnosti:

**Metoda 1: SSH tunel**

Pokud používáte unixový operační systém, toto je nejjednodušší metoda pro vzdálený přístup k vaší I2P konzoli. (Poznámka: SSH serverový software je k dispozici i pro systémy se systémem Windows, například [https://github.com/PowerShell/Win32-OpenSSH](https://github.com/PowerShell/Win32-OpenSSH))

Jakmile nakonfigurujete SSH přístup k vašemu systému, příznak '-L' se předává SSH s odpovídajícími argumenty - například:

```
ssh -L 7657:localhost:7657 (System_IP)
```
kde '(System_IP)' je nahrazeno IP adresou vašeho systému. Tento příkaz přesměruje port 7657 (číslo před první dvojtečkou) na port 7657 vzdáleného systému (specifikovaného řetězcem 'localhost' mezi první a druhou dvojtečkou) (číslo za druhou dvojtečkou). Vaše vzdálená konzole I2P bude nyní dostupná na vašem lokálním systému jako 'http://localhost:7657' a bude k dispozici po celou dobu trvání vaší SSH relace.

Pokud chcete spustit SSH relaci bez inicializace shellu na vzdáleném systému, můžete přidat příznak '-N':

```
ssh -NL 7657:localhost:7657 (System_IP)
```
**Metoda 2: Konfigurace vaší konzole tak, aby byla dostupná na veřejné IP adrese s uživatelským jménem a heslem**

1. Otevřete `~/.i2p/clients.config` a nahraďte:
   ```
   clientApp.0.args=7657 ::1,127.0.0.1 ./webapps/
   ```
   za:
   ```
   clientApp.0.args=7657 ::1,127.0.0.1,(System_IP) ./webapps/
   ```
   kde nahradíte (System_IP) veřejnou IP adresou vašeho systému

2. Přejděte na [http://localhost:7657/configui](http://localhost:7657/configui) a v případě potřeby přidejte uživatelské jméno a heslo pro konzoli - Přidání uživatelského jména a hesla je vysoce doporučeno pro zabezpečení vaší I2P konzole proti neoprávněným zásahům, které by mohly vést k deanonymizaci.

3. Přejděte na [http://localhost:7657/index](http://localhost:7657/index) a klikněte na „Graceful restart", což restartuje JVM a znovu načte klientské aplikace

Jakmile se to spustí, měli byste nyní být schopni vzdáleně přistupovat ke své konzoli. Načtěte konzoli routeru na adrese `http://(IP_systému):7657` a budete vyzváni k zadání uživatelského jména a hesla, které jste zadali v kroku 2 výše, pokud váš prohlížeč podporuje automatické ověřovací okno.

POZNÁMKA: V uvedené konfiguraci můžete zadat 0.0.0.0. Toto specifikuje rozhraní, ne síť nebo masku sítě. 0.0.0.0 znamená "navázat se na všechna rozhraní", takže konzole bude dostupná jak na 127.0.0.1:7657, tak i na jakékoli LAN/WAN IP adrese. Buďte opatrní při používání této možnosti, protože konzole bude dostupná na VŠECH adresách nakonfigurovaných ve vašem systému.

### Jak mohu používat aplikace z jiných počítačů? {#remote_i2cp}

Prosím podívejte se na předchozí odpověď pro instrukce k používání přesměrování portů SSH a také se podívejte na tuto stránku ve vaší konzoli: [http://localhost:7657/configi2cp](http://localhost:7657/configi2cp)

### Je možné použít I2P jako SOCKS proxy? {#socks}

SOCKS proxy je funkční od verze 0.7.1. Podporovány jsou SOCKS 4/4a/5. I2P nemá SOCKS outproxy, takže je omezeno pouze na použití v rámci I2P.

Mnoho aplikací prozrazuje citlivé informace, které vás mohou identifikovat na internetu, a to je riziko, kterého byste si měli být vědomi při používání I2P SOCKS proxy. I2P filtruje pouze data spojení, ale pokud program, který hodláte používat, odesílá tyto informace jako obsah, I2P nemá žádnou možnost ochránit vaši anonymitu. Například některé e-mailové aplikace odešlou IP adresu počítače, na kterém běží, na poštovní server. Doporučujeme používat nástroje nebo aplikace specifické pro I2P (jako je [I2PSnark](http://localhost:7657/i2psnark/) pro torrenty), nebo aplikace, o kterých je známo, že jsou bezpečné pro použití s I2P, včetně populárních doplňků dostupných pro [Firefox](https://www.mozilla.org/).

### Jak mohu přistupovat k IRC, BitTorrentu nebo jiným službám na běžném Internetu? {#proxy_other}

Existují služby zvané Outproxy, které propojují I2P a Internet, podobně jako Tor Exit Nodes. Výchozí funkcionalitu outproxy pro HTTP a HTTPS poskytuje `exit.stormycloud.i2p` a provozuje ji StormyCloud Inc. Je nakonfigurována v HTTP Proxy. Navíc, pro ochranu anonymity, I2P ve výchozím nastavení neumožňuje vytvářet anonymní připojení k běžnému Internetu. Pro více informací prosím navštivte stránku [Socks Outproxy](/docs/api/socks#outproxy).

---

## Reseeds

### Můj router běží už několik minut a má nula nebo velmi málo připojení {#reseed}

Nejprve zkontrolujte stránku [http://127.0.0.1:7657/netdb](http://127.0.0.1:7657/netdb) v Router Console – vaši síťovou databázi. Pokud nevidíte ani jeden router uvedený v rámci I2P, ale konzole hlásí, že byste měli být za firewallem, pak se pravděpodobně nemůžete připojit k reseed serverům. Pokud vidíte jiné I2P routery uvedené, zkuste snížit počet maximálních připojení [http://127.0.0.1:7657/config](http://127.0.0.1:7657/config) – možná váš router nezvládá tolik připojení.

### Jak provést ruční reseed? {#manual_reseed}

Za normálních okolností vás I2P připojí k síti automaticky pomocí našich bootstrapových odkazů. Pokud přerušené internetové připojení způsobí selhání bootstrapování ze reseed serverů, jednoduchým způsobem bootstrapování je použití prohlížeče Tor (ve výchozím nastavení otevírá localhost), který funguje velmi dobře s [http://127.0.0.1:7657/configreseed](http://127.0.0.1:7657/configreseed). Je také možné provést reseed I2P routeru ručně.

Při použití prohlížeče Tor k reseedu můžete vybrat více URL najednou a pokračovat. Ačkoli výchozí hodnota, která je 2 (z více url), bude také fungovat, ale bude to pomalé.

---

## Ochrana soukromí a bezpečnost

### Je můj router "výstupní uzel" (outproxy) do běžného internetu? Nechci, aby byl. {#exit}

Ne, váš router se podílí na přenosu end-to-end šifrovaného provozu přes síť i2p ke koncovému bodu náhodného tunelu, obvykle ne k outproxy, ale žádný provoz není předáván mezi vaším routerem a internetem přes transportní vrstvu. Jako koncový uživatel byste neměli provozovat outproxy, pokud nemáte zkušenosti se správou systémů a sítí.

### Je snadné detekovat používání I2P analýzou síťového provozu? {#detection}

Provoz I2P obvykle vypadá jako UDP provoz a o moc víc toho neodhaluje – a právě to, aby toho moc neodhaloval, je cílem. Také podporuje TCP. S určitým úsilím může pasivní analýza provozu klasifikovat provoz jako "I2P", ale doufáme, že pokračující vývoj obfuskace provozu to dále omezí. Dokonce i poměrně jednoduchá vrstva obfuskace protokolu jako obfs4 zabrání cenzorům v blokování I2P (je to cíl, který I2P sleduje).

### Je používání I2P bezpečné? {#safe}

Záleží na vašem osobním modelu hrozeb. Pro většinu lidí je I2P mnohem bezpečnější než nepoužívat žádnou ochranu. Některé jiné sítě (jako Tor, mixminion/mixmaster) jsou pravděpodobně bezpečnější proti určitým protivníkům. Například I2P provoz nepoužívá TLS/SSL, takže nemá problémy s "nejslabším článkem", které má Tor. I2P používalo hodně lidí v Sýrii během "Arabského jara" a v poslední době projekt zaznamenal větší růst v menších jazykových instalacích I2P na Blízkém a Středním východě. Nejdůležitější věc, kterou je třeba zde poznamenat, je, že I2P je technologie a potřebujete návod/průvodce pro zvýšení vašeho soukromí/anonymity na internetu. Také zkontrolujte svůj prohlížeč nebo importujte vyhledávač otisků (fingerprint) pro blokování útoků pomocí otisků s velmi velkou (což znamená: typicky dlouhé chvosty / velmi přesná rozmanitá datová struktura) databází o mnoha environmentálních věcech a nepoužívejte VPN, abyste snížili všechna rizika, která z ní sama plynou, jako je vlastní chování TLS cache a technická konstrukce poskytovatele služeb, který může být hacknut snadněji než vlastní desktopový systém. Možná použití izolovaného Tor V-Browseru s jeho skvělými anti-fingerprint ochranami a celkovou appguard-livetime-protection (ochrana aplikační stráže po dobu života) s povolením pouze pro nezbytnou systémovou komunikaci a poslední záchrannou vm-use (použití virtuálního stroje) s anti-spy disable skripty a live-cd pro odstranění jakéhokoli "téměř trvale možného rizika" a snížení všech rizik pomocí klesající pravděpodobnosti jsou dobrou volbou ve veřejné síti a top individuálním modelu rizik a může to být to nejlepší, co můžete udělat s tímto cílem pro použití i2p.

### V konzoli routeru vidím IP adresy všech ostatních I2P uzlů. Znamená to, že moji IP adresu vidí ostatní? {#netdb_ip}

Ano, pro ostatní I2P uzly, které znají váš router. Používáme to pro připojení ke zbytku I2P sítě. Adresy jsou fyzicky umístěny v objektech "routerInfos (klíč, hodnota)", buď vzdáleně načtených nebo přijatých od partnera. "routerInfos" obsahuje některé informace (některé volitelné oportunisticky přidané), "publikované partnerem", o samotném routeru pro bootstrapping (inicializaci). V tomto objektu nejsou žádné údaje o klientech. Bližší pohled pod kapotu vám řekne, že všichni jsou počítáni s nejnovějším typem vytváření identifikátorů zvaným "SHA-256 Hashes (nízké=Pozitivní hash(-klíč), vysoké=Negativní hash(+klíč))". I2P síť má vlastní databázi dat routerInfos vytvořených během nahrávání a indexování, ale to závisí hluboce na realizaci tabulek klíč/hodnota a topologii sítě a stavu zatížení / stavu šířky pásma a pravděpodobnostech směrování pro uložení v databázových komponentách.

### Je používání outproxy bezpečné? {#proxy_safe}

Záleží na tom, jak definujete "bezpečné". Outproxy servery jsou skvělé, když fungují, ale bohužel jsou provozovány dobrovolně lidmi, kteří mohou ztratit zájem nebo nemusí mít zdroje na jejich nepřetržitou údržbu – prosím mějte na paměti, že se můžete setkat s obdobími, kdy budou služby nedostupné, přerušované nebo nespolehlivé, a my nejsme s touto službou nijak spojeni a nemáme na ni žádný vliv.

Samotné outproxy mohou vidět váš přicházející a odcházející provoz, s výjimkou end-to-end šifrovaných HTTPS/SSL dat, stejně jako váš poskytovatel internetu může vidět provoz přicházející a odcházející z vašeho počítače. Pokud vám váš poskytovatel internetu nevadí, s outproxy to nebude o nic horší.

### A co útoky typu "De-Anonymizing" (odhalení anonymity)? {#deanon}

Pro velmi podrobné vysvětlení si přečtěte více v našich článcích o [Modelu hrozeb](/docs/overview/threat-model). Obecně platí, že deanonymizace není triviální, ale je možná, pokud nejste dostatečně opatrní.

---

## Přístup k Internetu/Výkon

### Nemohu přistupovat k běžným internetovým stránkám přes I2P. {#outproxy}

Proxying na internetové stránky (eepsites, které vedou ven na internet) je poskytováno jako služba uživatelům I2P poskytovateli, kteří neblokují. Tato služba není hlavním zaměřením vývoje I2P a je poskytována dobrovolně. Eepsites, které jsou hostovány na I2P, by měly vždy fungovat bez outproxy. Outproxy jsou pohodlné, ale nejsou záměrně dokonalé ani velkou částí projektu. Mějte na paměti, že nemusí být schopny poskytovat vysoce kvalitní služby, jaké mohou poskytovat jiné služby I2P.

### Nemohu přistupovat k https:// nebo ftp:// stránkám přes I2P. {#https}

Výchozí HTTP proxy podporuje pouze outproxying HTTP a HTTPS.

### Proč můj router využívá příliš mnoho procesoru? {#cpu}

Nejprve se ujistěte, že máte nejnovější verzi všech součástí souvisejících s I2P – starší verze měly v kódu zbytečné sekce, které zatěžovaly procesor. Existuje také [Log výkonu](/docs/overview/performance), který dokumentuje některá vylepšení výkonu I2P v průběhu času.

### Moje aktivní partnery / známé partnery / účastnické tunely / připojení / šířka pásma se dramaticky mění v čase! Je něco špatně? {#vary}

Celková stabilita sítě I2P je předmětem průběžného výzkumu. Značná část tohoto výzkumu se zaměřuje na to, jak drobné změny konfiguračních nastavení mění chování routeru. Jelikož je I2P peer-to-peer síť, akce ostatních uzlů budou mít vliv na výkon vašeho routeru.

### Co zpomaluje stahování, torrenty, procházení webu a vše ostatní na I2P ve srovnání s běžným internetem? {#slow}

I2P má různé ochranné mechanismy, které přidávají další směrování a další vrstvy šifrování. Také směruje provoz přes jiné uzly (tunnels), které mají svou vlastní rychlost a kvalitu, některé jsou pomalé, jiné rychlé. To vše vytváří značnou režii a provoz různou rychlostí v různých směrech. Záměrně všechny tyto věci způsobují, že je I2P pomalejší ve srovnání s přímým připojením na internetu, ale mnohem anonymnější a stále dostatečně rychlé pro většinu účelů.

Níže je uveden příklad s vysvětlením, který pomůže poskytnout určitý kontext k úvahám o latenci a šířce pásma při používání I2P.

Podívejte se na diagram níže. Znázorňuje spojení mezi klientem provádějícím požadavek přes I2P, serverem přijímajícím požadavek přes I2P a následně odpovídajícím zpět také přes I2P. Je zde také znázorněn okruh, kterým požadavek putuje.

Z diagramu vyplývá, že boxy označené 'P', 'Q' a 'R' reprezentují odchozí tunnel pro 'A' a boxy označené 'X', 'Y' a 'Z' reprezentují odchozí tunnel pro 'B'. Podobně boxy označené 'X', 'Y' a 'Z' reprezentují příchozí tunnel pro 'B', zatímco boxy označené 'P_1', 'Q_1' a 'R_1' reprezentují příchozí tunnel pro 'A'. Šipky mezi boxy ukazují směr provozu. Text nad a pod šipkami uvádí příklady šířky pásma mezi párem skoků a také příklady latencí.

Když klient i server používají 3-hop tunnely po celou dobu, celkem 12 dalších I2P routerů se podílí na přeposílání provozu. 6 uzlů přeposílá provoz z klienta na server, který je rozdělen do 3-hop odchozího tunnelu z 'A' ('P', 'Q', 'R') a 3-hop příchozího tunnelu do 'B' ('X', 'Y', 'Z'). Podobně 6 uzlů přeposílá provoz ze serveru zpět na klienta.

Nejprve můžeme zvážit latenci - čas, který trvá, než požadavek od klienta projde sítí I2P, dorazí na server a vrátí se zpět ke klientovi. Sečtením všech latencí vidíme, že:

```
    40 + 100 + 20 + 60 + 80 + 10 + 30 ms        (client to server)
  + 60 + 40 + 80 + 60 + 100 + 20 + 40 ms        (server to client)
  -----------------------------------
  TOTAL:                          740 ms
```
Celková doba odezvy v našem příkladu činí 740 ms - což je rozhodně mnohem více, než by člověk normálně zaznamenal při prohlížení běžných internetových stránek.

Zadruhé můžeme zvážit dostupnou šířku pásma. Ta je určena nejpomalejším spojem mezi uzly od klienta k serveru, stejně jako při přenosu provozu ze serveru ke klientovi. U provozu směřujícího od klienta k serveru vidíme, že dostupná šířka pásma v našem příkladu mezi uzly 'R' a 'X' a také mezi uzly 'X' a 'Y' je 32 KB/s. Navzdory vyšší dostupné šířce pásma mezi ostatními uzly budou tyto uzly působit jako úzké hrdlo a omezí maximální dostupnou šířku pásma pro provoz z 'A' do 'B' na 32 KB/s. Podobně sledování cesty ze serveru ke klientovi ukazuje, že maximální šířka pásma je 64 KB/s - mezi uzly 'Z_1' a 'Y_1', 'Y_1' a 'X_1' a 'Q_1' a 'P_1'.

Doporučujeme zvýšit vaše limity šířky pásma. To pomáhá síti zvýšením množství dostupné šířky pásma, což následně zlepší váš zážitek s I2P. Nastavení šířky pásma najdete na stránce [http://localhost:7657/config](http://localhost:7657/config). Mějte prosím na paměti limity vašeho internetového připojení stanovené vaším poskytovatelem internetu a podle toho upravte své nastavení.

Doporučujeme také nastavit dostatečné množství sdílené šířky pásma - to umožňuje směrování participujících tunelů přes váš I2P router. Povolení participujícího provozu udržuje váš router dobře integrovaný v síti a zlepšuje rychlost přenosu dat.

I2P je průběžně vyvíjený projekt. Implementuje se mnoho vylepšení a oprav, a obecně platí, že používání nejnovější verze pomůže vašemu výkonu. Pokud jste tak ještě neučinili, nainstalujte nejnovější verzi.

### Myslím, že jsem našel chybu, kde ji mohu nahlásit? {#bug}

Můžete nahlásit jakékoli chyby/problémy, se kterými se setkáte, na našem bugtrackeru, který je dostupný jak přes běžný internet, tak přes I2P. Máme diskuzní fórum, které je také dostupné na I2P i běžném internetu. Můžete se také připojit k našemu IRC kanálu: buď přes naši IRC síť IRC2P, nebo na Freenode.

- **Náš Bugtracker:**
  - Mimo soukromý internet: [https://i2pgit.org/I2P_Developers/i2p.i2p/issues](https://i2pgit.org/I2P_Developers/i2p.i2p/issues)
  - Na I2P: [http://git.idk.i2p/I2P_Developers/i2p.i2p/issues](http://git.idk.i2p/I2P_Developers/i2p.i2p/issues)
- **Naše fóra:** [i2pforum.i2p](http://i2pforum.i2p/)
- **Vložení logů:** Můžete vložit jakékoli zajímavé logy do služby pro vkládání textu, jako jsou služby mimo soukromý internet uvedené na [PrivateBin Wiki](https://github.com/PrivateBin/PrivateBin/wiki/PrivateBin-Directory), nebo I2P služby pro vkládání textu, jako je tato [instance PrivateBin](http://paste.crypthost.i2p) nebo tato [služba pro vkládání bez Javascriptu](http://pasta-nojs.i2p) a pokračujte na IRC v #i2p
- **IRC:** Připojte se k #i2p-dev Diskutujte s vývojáři na IRC

Prosím, uveďte relevantní informace ze stránky logů routeru, která je dostupná na: [http://127.0.0.1:7657/logs](http://127.0.0.1:7657/logs). Žádáme vás, abyste sdíleli veškerý text v sekci 'I2P Version and Running Environment' (Verze I2P a běhové prostředí) a také všechny chyby nebo varování zobrazené v různých logech na této stránce.

---

### Mám otázku! {#question}

Skvělé! Najdete nás na IRC:

- na `irc.freenode.net` kanálu `#i2p`
- na `IRC2P` kanálu `#i2p`

nebo zveřejněte na [fóru](http://i2pforum.i2p/) a my to zde zveřejníme (doufejme s odpovědí).
