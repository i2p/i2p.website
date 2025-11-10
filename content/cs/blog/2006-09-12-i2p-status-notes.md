---
title: "Stavové poznámky I2P k 2006-09-12"
date: 2006-09-12
author: "jr"
description: "Vydání 0.6.1.25 s vylepšeními stability sítě, optimalizacemi I2PSnarku a rozsáhlým přepracováním Syndie s offline distribuovanými fóry"
categories: ["status"]
---

Ahoj všichni, tady jsou naše *ehm* týdenní poznámky ke stavu

* Index:

1) 0.6.1.25 a stav sítě 2) I2PSnark 3) Syndie (co/proč/kdy) 4) Syndie otázky ke kryptografii 5) ???

* 1) 0.6.1.25 and net status

Před pár dny jsme vydali verzi 0.6.1.25, která zahrnuje spoustu oprav chyb nasbíraných za poslední měsíc, stejně jako práci zzz na I2PSnark a práci Complication na tom, aby byl náš kód pro synchronizaci času o něco robustnější. V tuto chvíli se zdá, že síť je poměrně stabilní, i když IRC bylo v posledních několika dnech trochu problematické (z důvodů nesouvisejících s I2P). Přibližně polovina sítě je zřejmě již aktualizována na nejnovější vydání; úspěšnost při sestavování tunnel se příliš nezměnila, i když celková propustnost se zdá být vyšší (pravděpodobně kvůli nárůstu počtu lidí používajících I2PSnark).

* 2) I2PSnark

Aktualizace zzz pro I2PSnark zahrnovaly optimalizace protokolu i změny webového rozhraní, jak je popsáno v záznamu historie [1]. Od vydání 0.6.1.25 došlo také k několika menším aktualizacím I2PSnarku a možná nám zzz může během dnešní večerní schůzky poskytnout přehled aktuálního stavu.

[1] <http://dev.i2p.net/cgi-bin/cvsweb.cgi/i2p/history.txt?rev=HEAD>

* 3) Syndie

Jak jistě víte, věnoval jsem svůj čas přepracování Syndie, i když "revamp" možná není to správné slovo. Možná můžete považovat to, co je nyní nasazeno, za "důkaz konceptu", protože nová Syndie byla od základu přepracována a znovu implementována, i když mnoho konceptů zůstává. Když se níže odkazuji na Syndie, mám na mysli novou Syndii.

* 3.1) What is Syndie

Syndie je na té nejzákladnější úrovni systém pro provozování offline distribuovaných fór. Ačkoli jeho struktura vede k velkému počtu různých konfigurací, většinu potřeb pokryje výběr jedné z možností v každém z následujících tří kritérií:
  - Typy fór:
    - Jeden autor (typický blog)
    - Více autorů (víceautorský blog)**
    - Otevřené (diskusní skupiny; lze však zavést omezení tak, aby pouze
      autorizovaní** uživatelé mohli zakládat nová vlákna, zatímco kdokoli může komentovat
      tato nová vlákna)
  - Viditelnost:
    - Kdokoli může číst cokoli
    - Příspěvky mohou číst pouze autorizované* osoby, ale některá metadata jsou zveřejněna
    - Příspěvky mohou číst pouze autorizované* osoby, případně dokonce i vědět, kdo přispívá
    - Příspěvky mohou číst pouze autorizované* osoby a nikdo neví, kdo je
      přispívá
  - Komentáře/odpovědi:
    - Kdokoli může komentovat nebo posílat soukromé odpovědi autorovi/vlastníkovi
      fóra
    - Komentovat mohou pouze autorizované** osoby a kdokoli může posílat soukromé
      odpovědi
    - Nikdo nemůže komentovat, ale kdokoli může posílat soukromé odpovědi
    - Nikdo nemůže komentovat a nikdo nemůže posílat soukromé odpovědi

 * reading is authorized by giving people the symmetric key or passphrase
   to decrypt the post.  Alternately, the post may include a publicly
   visible prompt, where the correct answer serves to generate the
   correct decryption key.

** zveřejňování, aktualizace a/nebo komentování je autorizováno tím, že těmto    uživatelům jsou poskytnuty asymetrické soukromé klíče k podepisování příspěvků, přičemž    odpovídající veřejný klíč je v metadatech fóra uveden jako    oprávněný zveřejňovat, spravovat nebo komentovat na fóru.  Případně mohou být    veřejné podpisové klíče jednotlivých oprávněných uživatelů uvedeny    v metadatech.

Jednotlivé příspěvky mohou obsahovat mnoho různých prvků:  - Libovolný počet stránek, s out of band data (oddělená data mimo hlavní kanál) pro každou stránku, která určují typ obsahu, jazyk atd.  Lze použít libovolné formátování, protože je na klientské aplikaci, aby obsah bezpečně vykreslila - prostý text musí být podporován a klienti, kteří mohou, by měli podporovat HTML.  - Libovolný počet příloh (opět s out of band data popisujícími přílohu)  - Malý avatar pro příspěvek (pokud není uveden, použije se autorův výchozí avatar)  - Sadu odkazů na jiné příspěvky, fóra, archivy, adresy URL atd. (která mohou zahrnovat klíče potřebné k publikování, správě nebo čtení odkazovaných fór)

Celkově vzato Syndie funguje na *obsahové vrstvě* - jednotlivé příspěvky jsou obsaženy v šifrovaných ZIP souborech a účast ve fóru znamená jednoduše sdílet tyto soubory. Nezávisí na tom, jak jsou soubory přenášeny (přes I2P, Tor, Freenet, gnutella, bittorrent, RSS, usenet, email), ale jednoduché nástroje pro agregaci a distribuci budou součástí standardního vydání Syndie.

Interakce s obsahem Syndie bude probíhat několika způsoby. Nejprve je k dispozici skriptovatelné textové rozhraní, které umožňuje základní obsluhu z příkazové řádky i interaktivní čtení z fór, zápis do fór, správu a synchronizaci fór. Například následuje jednoduchý skript pro vytvoření nového příspěvku "zpráva dne" -

login     menu post     create --channel 0000000000000000000000000000000000000000     addpage --in /etc/motd --content-type text/plain     addattachment --in ~/webcam.png --content-type image/png     listauthkeys --authorizedOnly true     authenticate 0     authorize 0     set --subject "Today's MOTD"     set --publicTags motd     execute     exit

Stačí to přesměrovat přes rouru (pipe) do spustitelného souboru syndie a je hotovo: cat motd-script | ./syndie > syndie.log

Kromě toho probíhají práce na grafickém rozhraní Syndie, které zahrnuje bezpečné vykreslování prostého textu a HTML stránek (samozřejmě s podporou transparentní integrace s funkcemi Syndie).

Aplikace založené na starém kódu "sucker" projektu Syndie umožní scraping (automatickou extrakci obsahu) a přepisování běžných webových stránek a webů tak, aby mohly být použity jako jedno- nebo vícestránkové příspěvky Syndie, včetně obrázků a dalších zdrojů jako příloh.

Do budoucna jsou plánovány zásuvné moduly pro firefox/mozilla, které budou umět detekovat a importovat soubory ve formátu Syndie a odkazy Syndie, stejně jako upozornit lokální Syndie GUI, že konkrétní fórum, téma, štítek, autor nebo výsledek vyhledávání má být přiveden do popředí.

Samozřejmě, jelikož je Syndie ve svém jádru obsahová vrstva s definovaným formátem souborů a kryptografickými algoritmy, budou se časem pravděpodobně objevovat další aplikace nebo alternativní implementace.

* 3.2) Why does Syndie matter?

V posledních několika měsících jsem od několika lidí slyšel otázku, proč pracuji na nástroji pro fóra/blogy - jak to souvisí se zajištěním silné anonymity?

Odpověď: *všechno*.

Stručně shrnuto:  - Návrh Syndie jako klientské aplikace citlivé na anonymitu se pečlivě
    vyhýbá složitým problémům citlivosti dat, jimž se téměř žádná
    aplikace navržená bez ohledu na anonymitu nevyhne.  - Tím, že pracuje na vrstvě obsahu, Syndie není závislá na
    výkonu ani spolehlivosti distribuovaných sítí jako I2P, Tor nebo
    Freenet, ačkoli je může využít tam, kde je to vhodné.  - Tímto způsobem může plně fungovat s malými, ad-hoc mechanismy pro
    distribuci obsahu - mechanismy, které by pro silné protivníky nemusely
    stát za námahu je zmařit (protože 'payoff' z dopadení jen několika
    desítek lidí pravděpodobně převýší náklady na zahájení
    útoků)  - Z toho plyne, že Syndie bude užitečná i tehdy, když ji nebude
    používat pár milionů lidí - malé, navzájem nesouvisející skupiny lidí
    by si měly zřídit své vlastní soukromé distribuční schéma Syndie, aniž
    by to vyžadovalo jakoukoli interakci s jinými skupinami nebo dokonce
    povědomí jiných skupin o jejich existenci.  - Protože se Syndie nespoléhá na interakci v reálném čase, může dokonce
    využít anonymizační systémy a techniky s vysokou latencí, aby se
    vyhnula útokům, jimž jsou všechny systémy s nízkou latencí
    zranitelné (například pasivní intersekční útoky, pasivní i aktivní
    časovací útoky a aktivní maskovací útoky).

Celkově vzato mám za to, že Syndie je pro hlavní poslání I2P (poskytovat silnou anonymitu těm, kdo ji potřebují) ještě důležitější než samotný router. Není to všespásné ani konečné řešení, ale je to klíčový krok.

* 3.3) When can we use Syndie?

Ačkoli už bylo dokončeno mnoho práce (včetně téměř celého textového rozhraní a značné části GUI), stále zbývá co udělat. První vydání Syndie bude obsahovat následující základní funkcionalitu:

 - Scriptable text interface, packaged up as a typical java application,
   or buildable with a modern GCJ
 - Support for all forum types, replies, comments, etc.
 - Manual syndication, transferring .snd files.
 - HTTP syndication, including simple CGI scripts to operate archives,
   controllable through the text interface.
 - Specs for the file formats, encryption algorithms, and database
   schema.

Kritériem, které použiji pro vydání, bude "plně funkční". Průměrný uživatel se nebude patlat s aplikací s textovým rozhraním, ale doufám, že nějací geekové ano.

Následující vydání vylepší schopnosti Syndie v několika oblastech:  - Uživatelské rozhraní:   - GUI založené na SWT   - Zásuvné moduly pro webový prohlížeč   - Textové uživatelské rozhraní pro web scraping (stahuje a přepisuje stránky)   - Čtecí rozhraní IMAP/POP3/NNTP  - Podpora obsahu   - Prostý text   - HTML (bezpečné vykreslování v rámci GUI, nikoli v prohlížeči)   - BBCode (?)  - Syndikace   - Feedspace, Feedtree a další nástroje pro synchronizaci s nízkou latencí   - Freenet (ukládání souborů .snd na CHK@s a archivů odkazujících     na soubory .snd na SSK@s a USK@s)   - E-mail (odesílání přes SMTP/mixmaster/mixminion, čtení přes     procmail/etc)   - Usenet (odesílání přes NNTP nebo remailery, čtení přes (proxy)     NNTP)  - Fulltextové vyhledávání s integrací Lucene  - Rozšíření HSQLDB pro plné šifrování databáze  - Další heuristiky pro správu archivů

Kdy co vyjde, závisí na tom, kdy jsou věci udělány.

* 4) Open questions for Syndie

V tuto chvíli je Syndie implementováno s použitím standardních kryptografických primitiv I2P - SHA256, AES256/CBC, ElGamal2048, DSA. Ten poslední však vybočuje z řady, protože používá 1024bitové veřejné klíče a spoléhá na (rychle slábnoucí) SHA1. Jeden podnět, který jsem slyšel z praxe, je rozšíření DSA o SHA256, a přestože je to proveditelné (byť dosud nestandardizované), nabízí to pouze 1024bitové veřejné klíče.

Protože Syndie zatím nebyl nasazen naostro a nemusíme se obávat zpětné kompatibility, máme tu výhodu, že můžeme libovolně měnit kryptografické primitivy. Jedna z úvah je zvolit podpisy ElGamal2048 nebo RSA2048 místo DSA, zatímco další úvaha směřuje k ECC (kryptografie na eliptických křivkách) s podpisy ECDSA a asymetrickým šifrováním ECIES, případně na bezpečnostních úrovních 256 bitů nebo 521 bitů (což odpovídá 128bitovým a 256bitovým velikostem symetrických klíčů, resp.).

Pokud jde o patentové problémy týkající se ECC, zdají se být relevantní pouze pro určité optimalizace (komprese bodů) a algoritmy, které nepotřebujeme (EC MQV). Co se týče podpory v Javě, mnoho toho k dispozici není, i když bouncycastle lib zřejmě má nějaký kód. Nicméně pravděpodobně by také nebyl velký problém přidat malé wrappery (obalové vrstvy) do libtomcrypt, openssl nebo crypto++, podobně jako jsme to udělali pro libGMP (a získali jsme tak jbigi).

Co si o tom myslíte?

* 5) ???

Je toho nahoře hodně ke vstřebání, a proto (na doporučení cervantese) posílám tyto statusové poznámky takhle brzy. Pokud máte nějaké připomínky, dotazy, obavy nebo návrhy, přijďte dnes večer ve 20:00 UTC na #i2p na irc.freenode.net/irc.postman.i2p/irc.freshcoffee.i2p na naše *ehm* týdenní setkání!

=jr
