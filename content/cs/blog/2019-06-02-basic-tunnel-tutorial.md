---
title: "Základní návod k I2P Tunnels s obrázky"
date: 2019-06-02
author: "idk"
description: "Basic i2ptunnel Setup"
categories: ["tutorial"]
---

Ačkoli je Java I2P router dodáván s předem nakonfigurovaným statickým webovým serverem, jetty, který poskytne uživateli jeho první eepSite, mnozí požadují od svého webového serveru sofistikovanější funkce a raději si vytvoří eepSite pomocí jiného serveru. To je samozřejmě možné a ve skutečnosti je to opravdu snadné, jakmile to jednou uděláte.

Ačkoli je to snadné provést, je několik věcí, které byste měli předtím zvážit. Budete chtít odstranit identifikovatelné prvky ze svého webového serveru, například potenciálně identifikující hlavičky a výchozí chybové stránky, které prozrazují typ serveru/distribuce. Více informací o hrozbách pro anonymitu způsobených nesprávně nakonfigurovanými aplikacemi viz: [Riseup zde](https://riseup.net/en/security/network-security/tor/onionservices-best-practices), [Whonix zde](https://www.whonix.org/wiki/Onion_Services), [tento blogový článek o některých selháních v oblasti opsec (operační bezpečnosti)](https://blog.0day.rocks/securing-a-web-hidden-service-89d935ba1c1d), [a stránku o aplikacích I2P zde](https://geti2p.net/docs/applications/supported). Ačkoli je mnoho těchto informací popsáno pro Tor Onion Services, stejné postupy a zásady platí i pro hostování aplikací přes I2P.

### Krok 1: Otevřete průvodce Tunnel

Přejděte do webového rozhraní I2P na adrese 127.0.0.1:7657 a otevřete [Hidden Services Manager](http://127.0.0.1:7657/i2ptunnelmgr) (odkazuje na localhost). Klikněte na tlačítko "Tunnel Wizard" a začněte.

### Krok dva: Vyberte serverový Tunnel

Průvodce pro tunnel je velmi jednoduchý. Protože nastavujeme http *server*, stačí jen vybrat *server* tunnel.

### Třetí krok: Vyberte HTTP Tunnel

HTTP tunnel je tunnel optimalizovaný pro hostování HTTP služeb. Má aktivované funkce filtrování a omezování rychlosti, které jsou přizpůsobeny právě tomuto účelu. Standardní tunnel může fungovat také, ale pokud zvolíte standardní tunnel, budete se o tyto bezpečnostní funkce muset postarat sami. Podrobnější rozbor konfigurace HTTP Tunnel je k dispozici v dalším tutoriálu.

### Krok čtyři: Zadejte název a popis

Pro svou vlastní orientaci a abyste si snadno zapamatovali a rozlišili, k čemu tunnel používáte, dejte mu výstižnou přezdívku a popis. Pokud se k tomu budete potřebovat vrátit a později provádět další správu, právě podle toho tunnel rozpoznáte ve správci skrytých služeb.

### Krok pět: Nakonfigurujte hostitele a port

V tomto kroku nasměrujete webový server na TCP port, na kterém naslouchá. Jelikož většina webových serverů naslouchá na portu 80 nebo 8080, příklad to odráží. Pokud k izolaci svých webových služeb používáte jiné porty nebo virtuální stroje či kontejnery, možná bude potřeba upravit host (název hostitele), port, nebo obojí.

### Krok šest: Rozhodněte, zda se má spouštět automaticky

Nenapadá mě žádný způsob, jak tento krok dále rozvést.

### Krok sedm: Zkontrolujte svá nastavení

Nakonec se podívejte na nastavení, která jste zvolili. Pokud vám vyhovují, uložte je. Pokud jste nezvolili automatické spuštění tunnel, přejděte do správce skrytých služeb a spusťte jej ručně, až budete chtít svou službu zpřístupnit.

### Dodatek: Možnosti přizpůsobení HTTP serveru

I2P poskytuje podrobný panel pro konfiguraci tunnelu http serveru podle vlastních potřeb. Tento návod dokončím tím, že je všechny projdu. Nakonec.
