---
title: "Poznámky ke stavu I2P k 2004-09-28"
date: 2004-09-28
author: "jr"
description: "Týdenní přehled stavu I2P zahrnující implementaci nového transportního protokolu, autodetekci IP adresy a postup prací na vydání 0.4.1"
categories: ["status"]
---

Ahoj všichni, je čas na týdenní aktualizaci

## Rejstřík:

1. New transport
2. 0.4.1 status
3. ???

## 1) Nový transport

Vydání 0.4.1 trvá déle, než se očekávalo, ale nový transportní protokol a implementace jsou připraveny se vším, co bylo plánováno - detekce IP adresy, nízkonákladové navázání spojení a snazší rozhraní, které pomůže s laděním, když spojení selhávají. Tohoto bylo dosaženo úplným zahozením starého transportního protokolu a implementací nového, i když máme pořád stejné buzzwordy (2048bit DH + STS, AES256/CBC/PKCS#5). Pokud si chcete protokol projít, je v dokumentaci. Nová implementace je také mnohem čistší, protože stará verze byla jen hromadou aktualizací nashromážděných během posledního roku.

Každopádně, v novém kódu pro detekci IP je několik věcí, které stojí za zmínku. Nejdůležitější je, že je zcela volitelný – pokud na konfigurační stránce (nebo přímo v router.config) zadáte IP adresu, bude tuto adresu vždy používat, ať se děje cokoli. Pokud však toto pole necháte prázdné, váš router nechá prvního peera, s nímž se spojí, aby mu sdělil, jaká je jeho IP adresa, na které pak začne naslouchat (poté, co ji přidá do svého RouterInfo a uloží do síťové databáze). No, to není tak úplně pravda – pokud jste IP adresu výslovně nenastavili, bude věřit komukoli, kdo mu řekne, na jaké IP adrese je dosažitelný, kdykoli peer nemá žádná spojení. Takže pokud se vaše internetové připojení restartuje a třeba vám přidělí novou adresu z DHCP, váš router uvěří prvnímu peeru, kterého dokáže zastihnout.

Ano, to znamená, že už není potřeba používat dyndns. Samozřejmě ho můžete dál používat, ale není to nutné.

Nicméně to nevyřeší vše, co potřebujete - pokud máte NAT nebo firewall, znát svou externí IP adresu je jen polovina úspěchu - stále ještě musíte otevřít příchozí port. Ale je to začátek.

(mimochodem, pro lidi provozující své vlastní soukromé sítě I2P nebo simulátory, existuje nová dvojice příznaků k nastavení i2np.tcp.allowLocal a i2np.tcp.tagFile)

## 2) 0.4.1 stav

Kromě položek v plánu pro 0.4.1 bych tam chtěl dostat ještě pár dalších věcí – jak opravy chyb, tak aktualizace nástrojů pro monitorování sítě. Momentálně dohledávám problémy s nadměrným memory churn (nadměrné alokace a uvolňování paměti) a chci prověřit několik hypotéz ohledně občasných problémů se spolehlivostí v síti, ale brzy budeme připraveni verzi vydat, možná už ve čtvrtek. Bohužel nebude zpětně kompatibilní, takže to může být trochu hrbolaté, ale díky novému procesu aktualizace a tolerantnější implementaci transportu by to nemělo být tak zlé jako u předchozích aktualizací, které nebyly zpětně kompatibilní.

## 3) ???

Jo, poslední dva týdny jsme měli krátké aktualizace, ale je to proto, že jsme v zákopech a soustředíme se na implementaci, ne na různé návrhy na vyšší úrovni. Mohl bych vám povědět o datech z profilování nebo o connection tag cache (vyrovnávací paměť značek připojení) s kapacitou 10 000 pro nový transport, ale to není tak zajímavé. Každopádně možná máte ještě nějaké věci k probrání, tak přijďte dnes večer na schůzku a pusťte se do toho naplno.

=jr
