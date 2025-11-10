---
title: "Stavové poznámky I2P k 2004-09-14"
date: 2004-09-14
author: "jr"
description: "Týdenní aktualizace stavu I2P zahrnující vydání 0.4.0.1, aktualizace modelu hrozeb, vylepšení webu, změny v roadmapě (plánu vývoje) a potřeby vývoje klientských aplikací"
categories: ["status"]
---

Ahoj všichni, zase nadešel ten čas v týdnu

## Rejstřík:

1. 0.4.0.1
2. Threat model updates
3. Website updates
4. Roadmap
5. Client apps
6. ???

## 1) 0.4.0.1

Od vydání 0.4.0.1 minulou středu se na síti daří docela dobře – více než dvě třetiny sítě se aktualizovaly a na síti průběžně udržujeme mezi 60 a 80 routers. Délky připojení k IRC se liší, ale poslední dobou jsou běžná 4–12hodinová spojení. Objevily se ale nějaké zprávy o podivnostech při spouštění na OS/X, nicméně věřím, že i v tomto směru se dělají pokroky.

## 2) Aktualizace modelu hrozeb

Jak bylo zmíněno v odpovědi na Toniho příspěvek, došlo k poměrně zásadnímu přepracování modelu hrozeb. Hlavní rozdíl spočívá v tom, že namísto starého způsobu řešení hrozeb ad hoc jsem se snažil řídit některými taxonomiemi popsanými v odborné literatuře. Největším problémem pro mě bylo najít způsoby, jak začlenit skutečné techniky, které lidé mohou použít, do nabízených schémat – často jediný útok spadal do několika různých kategorií. Proto nejsem příliš spokojen s tím, jak jsou na té stránce informace podány, ale je to lepší než to bylo předtím.

## 3) Aktualizace webu

Díky pomoci Curiosity jsme začali s několika aktualizacemi webu – tu nejviditelnější uvidíte přímo na domovské stránce. To by mělo pomoci lidem, kteří na I2P narazí a chtějí hned vědět, co to sakra je ta I2P, místo aby se museli pracně probírat různými stránkami. Každopádně, pokrok, stále vpřed :)

## 4) Plán vývoje

Když už mluvíme o pokroku, konečně jsem dal dohromady přepracovaný plán vývoje na základě toho, co podle mě potřebujeme implementovat, a toho, co je nutné splnit, abychom vyhověli potřebám uživatele. Hlavní změny oproti starému plánu vývoje jsou:

- Drop AMOC altogether, replaced with UDP (however, we'll support TCP for those who can't use UDP *cough*mihi*cough*)
- Kept all of the restricted route operation to the 2.0 release, rather than bring in partial restricted routes earlier. I believe we'll be able to meet the needs of many users without restricted routes, though of course with them many more users will be able to join us. Walk before run, as they say.
- Pulled the streaming lib in to the 0.4.3 release, as we don't want to go 1.0 with the ~4KBps per stream limit. The bounty on this is still of course valid, but if no one claims it before 0.4.2 is done, I'll start working on it.
- TCP revamp moved to 0.4.1 to address some of our uglier issues (high CPU usage when connecting to people, the whole mess with "target changed identities", adding autodetection of IP address)

Ostatní položky naplánované pro různá vydání 0.4.* již byly implementovány. Nicméně je tu ještě jedna věc, která byla z roadmapy vyřazena...

## 5) Klientské aplikace

Potřebujeme klientské aplikace. Aplikace, které jsou poutavé, bezpečné, škálovatelné a anonymní. I2P samo o sobě toho moc neumí; pouze umožňuje, aby spolu dva koncové body komunikovaly anonymně. I2PTunnel sice nabízí zatraceně univerzální nástroj, ale takové nástroje ve skutečnosti osloví jen technické nadšence mezi námi. Potřebujeme víc než to – něco, co lidem umožní dělat to, co skutečně chtějí, a pomůže jim to dělat lépe. Potřebujeme důvod, aby lidé používali I2P i z jiných důvodů než jen proto, že je bezpečnější.

Dosud jsem propagoval MyI2P jako řešení této potřeby - distribuovaný systém pro blogování nabízející rozhraní ve stylu LiveJournalu. Nedávno jsem na e-mailové konferenci probíral některé funkce MyI2P. Nicméně jsem to vyřadil z roadmapy (plánu vývoje), protože je to na mě prostě příliš práce, abych to zvládl a zároveň věnoval základní síti I2P pozornost, kterou potřebuje (už teď jsme kapacitně na hraně).

Existuje ještě několik dalších aplikací, které jsou velmi slibné. Stasher by poskytl významnou infrastrukturu pro distribuované ukládání dat, ale nejsem si jistý, jak to postupuje. I se Stasherem by však bylo potřeba atraktivní uživatelské rozhraní (ačkoli některé aplikace FCP by s ním možná dokázaly pracovat).

IRC je také výkonný systém, má však svá omezení kvůli serverové architektuře. oOo už ale odvedl nějakou práci na prověření možností implementace transparentního DCC, takže by možná šlo použít IRC pro veřejný chat a DCC pro soukromé přenosy souborů nebo bezserverový chat.

Obecná funkčnost eepsite(I2P Site) je rovněž důležitá, a to, co máme nyní, je zcela neuspokojivé. Jak upozorňuje DrWoo, současné nastavení představuje významná rizika pro anonymitu a, přestože oOo připravil několik záplat filtrujících některé hlavičky, je třeba udělat ještě mnohem více práce, než bude možné považovat eepsites(I2P Sites) za bezpečné. Existuje několik různých přístupů, jak to řešit, všechny mohou fungovat, ale všechny vyžadují práci. Vím, že duck zmínil, že má někoho, kdo na něčem pracuje, ale nevím, jak to postupuje ani zda by to bylo možné přibalit k I2P, aby to mohl používat každý, nebo ne. Duck?

Další dvojicí klientských aplikací, které by mohly pomoci, by byla buď swarming aplikace pro přenos souborů (ala BitTorrent; swarming = současné stahování z více zdrojů) nebo tradičnější aplikace pro sdílení souborů (ala DC/Napster/Gnutella/etc). Domnívám se, že právě tohle chce velké množství lidí, ale každý z těchto systémů má své problémy. Jsou však dobře známé a portování nemusí být velký problém (možná).

Dobře, takže výše uvedené není nic nového - proč jsem to všechno zmínil? Tak, musíme najít způsob, jak zajistit, aby byla implementována atraktivní, bezpečná, škálovatelná a anonymní klientská aplikace, a samo se to zčistajasna nestane. Smířil jsem se s tím, že to sám nezvládnu, takže musíme být proaktivní a najít způsob, jak to dotáhnout do konce.

Abychom toho dosáhli, myslím, že náš systém odměn (bounty) by mohl pomoci, ale jedním z důvodů, proč jsme v tomto ohledu neviděli mnoho aktivity (lidí pracujících na realizaci odměny), je podle mě to, že jsou příliš roztříštění. Abychom dosáhli výsledků, které potřebujeme, myslím, že musíme stanovit priority v tom, co chceme, a soustředit naše úsilí na tu nejvyšší prioritu, 'navýšit odměnu', abychom snad někoho povzbudili, aby se přihlásil a pracoval na té odměně.

Můj osobní názor stále je, že bezpečný a distribuovaný blogovací systém jako MyI2P by byl nejlepší. Místo pouhého anonymního přehazování dat sem a tam nabízí způsob, jak budovat komunity, které jsou životní mízou každého vývojového úsilí. Navíc nabízí relativně vysoký poměr signál/šum, nízkou pravděpodobnost zneužívání společných zdrojů a obecně nízké zatížení sítě. Nenabízí však plnou rozmanitost běžných webů, ale zdá se, že to 1,8 milionu aktivních uživatelů LiveJournalu nevadí.

Kromě toho by mou další prioritou bylo zabezpečení architektury eepsite(I2P Site), které by prohlížečům zajistilo potřebnou bezpečnost a lidem umožnilo provozovat eepsites(I2P Sites) 'ihned po instalaci'.

Přenos souborů a distribuované ukládání dat jsou také neuvěřitelně výkonné, ale nezdají se být tak komunitně zaměřené, jak bychom si pravděpodobně přáli pro první běžnou aplikaci pro koncové uživatele.

Chci, aby všechny uvedené aplikace byly hotové už včera, a k tomu ještě tisíc dalších aplikací, které si ani neumím představit. Chci také světový mír, konec hladu, zničení kapitalismu, osvobození od etatismu, rasismu, sexismu, homofobie, konec bezostyšného ničení životního prostředí a konec všeho toho dalšího zla. Jenže nás není mnoho a dokážeme jen omezené množství věcí. Proto musíme stanovit priority a soustředit své úsilí na to, čeho můžeme dosáhnout, místo abychom jen seděli a byli zahlceni vším, co chceme udělat.

Možná bychom mohli probrat nějaké nápady, co bychom měli dnes večer na schůzce dělat.

## 6) ???

Tak to je pro tuto chvíli všechno, a hele, poznámky ke stavu mám sepsané *před* schůzkou! Takže žádné výmluvy, zastavte se ve 21:00 GMT a zasypte nás všechny svými nápady.

=jr
