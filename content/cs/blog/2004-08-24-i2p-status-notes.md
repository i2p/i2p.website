---
title: "Poznámky o stavu I2P k 2004-08-24"
date: 2004-08-24
author: "jr"
description: "Týdenní aktualizace stavu I2P zahrnující vydání 0.3.4.3, nové funkce router konzole, pokrok ve verzi 0.4 a různá vylepšení"
categories: ["status"]
---

Ahoj všem, dnes máme spoustu aktualizací.

## Rejstřík

1. 0.3.4.3 status
   1.1) timestamper
   1.2) new router console authentication
2. 0.4 status
   2.1) service & systray integration
   2.2) jbigi & jcpuid
   2.3) i2paddresshelper
3. AMOC vs. restricted routes
4. stasher
5. pages of note
6. ???

## 1) 0.3.4.3 stav

Vydání 0.3.4.3 vyšlo minulý pátek a od té doby jde vše docela dobře. Vyskytly se některé problémy s nově zavedeným kódem pro testování tunnelů a výběr peerů, ale po několika úpravách od vydání je to poměrně solidní. Nevím, jestli je IRC server už na nové revizi, takže se obecně musíme spoléhat na testování pomocí eepsites(I2P Sites) a http outproxies (squid.i2p a www1.squid.i2p). Velké (>5MB) přenosy souborů ve vydání 0.3.4.3 stále nejsou dostatečně spolehlivé, ale podle mých testů změny od té doby věci dále zlepšily.

Síť také roste – dnes jsme dosáhli 45 současně připojených uživatelů a už několik dní se stabilně držíme v rozmezí 38–44 uživatelů (w00t)! To je pro tuto chvíli zdravé číslo a sleduji celkovou aktivitu sítě, abych měl pod kontrolou případná rizika. Při přechodu na verzi 0.4 budeme chtít postupně zvýšit uživatelskou základnu až někam k hranici 100 routerů a ještě nějakou dobu testovat, než porosteme dál. Alespoň to je můj cíl z pohledu vývojáře.

### 1.1) timestamper

Jedna z naprosto skvělých věcí, které se změnily s vydáním verze 0.3.4.3 a kterou jsem úplně zapomněl zmínit, byla aktualizace kódu SNTP. Díky štědrosti Adama Buckleyho, který souhlasil s uvolněním svého SNTP kódu pod licencí BSD, jsme sloučili starou aplikaci Timestamper do jádra I2P SDK a plně ji integrovali s našimi interními hodinami. To znamená tři věci: 1. můžete smazat timestamper.jar (kód je teď v i2p.jar) 2. můžete odstranit související řádky clientApp z vaší konfigurace 3. můžete aktualizovat svou konfiguraci tak, aby používala nové možnosti synchronizace času

Nové možnosti v router.config jsou jednoduché a výchozí hodnoty by měly postačovat (zvlášť když je většina z vás nevědomky používá :).

Chcete-li nastavit seznam serverů SNTP, které se mají dotazovat:

```
time.sntpServerList=pool.ntp.org,pool.ntp.org,pool.ntp.org
```
Chcete-li zakázat synchronizaci času (pouze pokud jste NTP guru a víte, že hodiny vašeho operačního systému jsou *vždy* přesné - samotné spuštění "windows time" NENÍ dostačující):

```
time.disabled=true
```
Už nepotřebujete mít 'timestamper password', protože je vše přímo integrováno do kódu (ach, ty radosti BSD vs GPL :)

### 1.2) new router console authentication

Toto je relevantní pouze pro ty z vás, kteří provozují novou konzoli routeru, ale pokud ji necháváte naslouchat na veřejném rozhraní, možná budete chtít využít integrované základní HTTP autentizace. Ano, základní HTTP autentizace je absurdně slabá – neochrání vás před nikým, kdo odposlouchává provoz ve vaší síti nebo se dovnitř dostane hrubou silou, ale udrží mimo náhodné zvědavce. Každopádně, chcete-li ji použít, jednoduše přidejte řádek

```
consolePassword=blah
```
do vašeho router.config. Bohužel budete muset restartovat router, protože tento parametr je do Jetty předán pouze jednou (při startu).

## 2) 0.4 status

Na verzi 0.4 děláme velký pokrok a doufáme, že během příštího týdne zveřejníme několik předběžných verzí. Pořád ještě dolaďujeme některé detaily, takže zatím nemáme připravený propracovaný postup aktualizace. Tato verze bude zpětně kompatibilní, takže by aktualizace neměla být příliš nepříjemná. Každopádně sledujte novinky a hned poznáte, až bude vše připravené.

### 1.1) generátor časových razítek

Hypercubus dělá velký pokrok při integraci instalátoru, aplikace do oznamovací oblasti a části kódu pro správu služby. V zásadě pro vydání 0.4 budou mít všichni uživatelé Windows automaticky malou ikonu v oznamovací oblasti (Iggy!), přičemž ji budou moci přes webovou konzoli zakázat (a/nebo znovu povolit). Kromě toho budeme přibalovat JavaService wrapper, který nám umožní řadu užitečných věcí, jako například spouštět I2P při startu systému (nebo ne), automaticky restartovat za určitých podmínek, provést tvrdý restart JVM na vyžádání, generovat výpisy zásobníku a mnoho dalších užitečných funkcí.

### 1.2) nová autentizace konzole routeru

Jednou z velkých novinek ve vydání 0.4 bude přepracování kódu jbigi, které sloučí úpravy, které Iakin provedl pro Freenet, stejně jako jeho novou nativní knihovnu "jcpuid". Knihovna jcpuid funguje pouze na architekturách x86 a ve spojení s novým kódem jbigi určí, který 'správný' jbigi se má načíst. Proto budeme dodávat jediný jbigi.jar, který budou mít všichni, a z něj vybereme pro aktuální stroj ten 'správný'. Uživatelé samozřejmě budou moci i nadále sestavit vlastní nativní jbigi a přebít tak to, co jcpuid požaduje (jednoduše jej sestavte a zkopírujte do instalačního adresáře I2P, nebo jej pojmenujte "jbigi" a umístěte do souboru .jar ve vašem classpath). Kvůli těmto aktualizacím však *není* zpětně kompatibilní - při aktualizaci musíte buď znovu sestavit své vlastní jbigi, nebo odstranit existující nativní knihovnu (aby nový kód jcpuid mohl vybrat tu správnou).

### 2.3) i2paddresshelper

oOo dal dohromady opravdu skvělý pomocný nástroj, který lidem umožní procházet eepsites(I2P Sites) bez toho, aby museli aktualizovat svůj hosts.txt. Byl zapsán do CVS a bude nasazen v příštím vydání, ale lidé možná budou chtít podle toho upravit odkazy (cervantes aktualizoval [i2p] bbcode na forum.i2p, aby jej podporoval odkazem "Try it [i2p]").

V zásadě stačí vytvořit odkaz na eepsite(I2P Site) s libovolným názvem, jaký chcete, a pak k němu připojit speciální parametr URL určující cílovou adresu:

```
http://wowthisiscool.i2p/?i2paddresshelper=FpCkYW5pw...
```
Na pozadí je to docela bezpečné - nemůžete podvrhnout cizí adresu a název není trvale uložen v hosts.txt, ale umožní vám zobrazit obrázky / atd. odkazované z eepsites(I2P Sites), které byste se starým trikem `http://i2p/base64/` nemohli. Pokud chcete mít vždy možnost používat "wowthisiscool.i2p" k přístupu na ten web, budete samozřejmě pořád muset přidat záznam do svého hosts.txt (dokud nebude nasazen adresář MyI2P, tj. ;)

## 3) AMOC vs. restricted routes

Mule dává dohromady pár nápadů a pobízí mě, abych některé věci vysvětlil, a přitom se mu docela daří mě přimět, abych znovu přehodnotil celý koncept AMOC. Konkrétně, pokud upustíme od jednoho z omezení, která jsem na naši transportní vrstvu kladl — toho, jež nám umožňovalo předpokládat obousměrnost — možná se obejdeme bez celého AMOC transportu a místo toho implementujeme základní provoz omezených tras (položíme tím základy pro pokročilejší techniky omezených tras, jako jsou trusted peers (důvěryhodné peer uzly) a víceskokové router tunnels na později).

Pokud se vydáme touto cestou, znamenalo by to, že lidé by se mohli bez jakékoli konfigurace účastnit sítě i za firewally, NATy apod., a zároveň by to nabízelo některé vlastnosti anonymity restricted route (s omezenou trasou). To by zase pravděpodobně vedlo k velké revizi našeho plánu vývoje, ale pokud to dokážeme udělat bezpečně, ušetřilo by nám to hromadu času a změna by za to rozhodně stála.

Nicméně to nechceme uspěchat a předtím, než se k tomuto postupu zavážeme, budeme muset pečlivě přezkoumat důsledky pro anonymitu a bezpečnost. Uděláme to poté, co bude verze 0.4 vydána a poběží hladce, takže není důvod spěchat.

## 2) 0.4 stav

Proslýchá se, že aum dělá slušný pokrok - nevím, jestli bude na schůzce s aktualizací, ale dnes ráno nám na #i2p zanechal krátkou zprávu:

```
<aum> hi all, can't talk long, just a quick stasher update - work is
      continuing on implementing freenet keytypes, and freenet FCP
      compatibility - work in progress, should have a test build
      ready to try out by the end of the week
```
Hurá.

## 5) pages of note

Jen bych chtěl upozornit na dva nové zdroje, které by si uživatelé I2P mohli chtít prohlédnout – DrWoo připravil stránku se spoustou informací pro lidi, kteří chtějí procházet web anonymně, a Luckypunk zveřejnil návod popisující své zkušenosti s některými JVM na FreeBSD. Hypercubus také zveřejnil dokumentaci k testování dosud nevydané integrace služby a systray (oznamovací oblast).

## 6) ???

Ok, to je zatím všechno, co mám na srdci - zaskoč dnes večer na schůzku ve 21:00 GMT, pokud chceš otevřít ještě něco dalšího.

=jr
