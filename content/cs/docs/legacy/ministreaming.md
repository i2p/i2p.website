---
title: "Ministreamingová knihovna"
description: "Historické poznámky k první TCP-podobné transportní vrstvě I2P"
slug: "ministreaming"
lastUpdated: "2025-02"
accurateFor: "historical"
---

> **Zastaralé:** Knihovna ministreaming předchází současné [streamovací knihovně](/docs/specs/streaming/). Moderní aplikace musí používat plné streamovací API nebo SAM v3. Informace níže jsou ponechány pro vývojáře, kteří provádějí revizi zastaralého zdrojového kódu dodávaného v `ministreaming.jar`.

## Přehled

Ministreaming (minimalistická streamovací vrstva) běží nad [I2CP](/docs/specs/i2cp/) a zajišťuje spolehlivé doručování ve správném pořadí napříč zprávovou vrstvou I2P — podobně jako TCP nad IP. Původně byl vyčleněn z rané aplikace **I2PTunnel** (pod licencí BSD), aby se alternativní transporty mohly vyvíjet nezávisle.

Klíčová návrhová omezení:

- Klasické dvoufázové navazování spojení (SYN/ACK/FIN) převzaté z TCP
- Pevná velikost okna **1** paketu
- Žádná ID pro jednotlivé pakety ani selektivní potvrzování

Tyto volby udržely implementaci malou, ale omezují propustnost—každý paket obvykle čeká téměř dvě RTT, než je odeslán další. U dlouhotrvajících spojení je tato režie přijatelná, ale krátké výměny ve stylu HTTP tím znatelně trpí.

## Vztah ke streamovací knihovně

Aktuální streamovací knihovna rozšiřuje tentýž balíček Java (`net.i2p.client.streaming`). Zastaralé třídy a metody zůstávají v dokumentaci Javadoc, jasně označené, aby vývojáři mohli identifikovat rozhraní API z éry ministreaming (starší streamovací knihovna). Když streamovací knihovna nahradila ministreaming, přidala:

- Efektivnější navazování spojení s menším počtem kol komunikace
- Adaptivní okna zahlcení a logika retransmise
- Lepší výkon přes ztrátové tunnels

## Kdy byl Ministreaming užitečný?

Navzdory svým omezením poskytoval ministreaming (minimalistické streamovací rozhraní) spolehlivý přenos v nejranějších nasazeních. API bylo záměrně malé a odolné vůči budoucím změnám, aby bylo možné zaměňovat alternativní streamovací enginy, aniž by došlo k porušení kompatibility pro volající. Aplikace v jazyce Java jej linkovaly přímo; klienti mimo Javu ke stejné funkcionalitě přistupovali prostřednictvím podpory [SAM](/docs/legacy/sam/) pro streamovací relace.

V současnosti považujte `ministreaming.jar` pouze za kompatibilní vrstvu. Nový vývoj by měl:

1. Použijte plnou streamingovou knihovnu (Java) nebo SAM v3 (styl `STREAM`)  
2. Při modernizaci kódu odstraňte veškeré přetrvávající předpoklady pevné velikosti okna  
3. Upřednostněte větší velikosti okna a optimalizované handshake (navázání spojení) pro zlepšení výkonu u zátěží citlivých na latenci

## Referenční dokumentace

- [Dokumentace knihovny pro streamování](/docs/specs/streaming/)
- [Javadoc knihovny pro streamování](http://idk.i2p/javadoc-i2p/net/i2p/client/streaming/package-summary.html) – včetně zastaralých tříd "ministreaming" (zjednodušené streamování)
- [Specifikace SAMv3](/docs/api/samv3/) – podpora streamování pro aplikace nepsané v Javě

Pokud narazíte na kód, který stále závisí na ministreaming (starší minimalistické streamovací rozhraní), plánujte jej převést na moderní streamovací API — síť a její nástroje očekávají novější chování.
