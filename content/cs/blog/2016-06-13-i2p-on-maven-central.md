---
title: "I2P na Maven Centralu"
date: 2016-06-13
author: "str4d"
description: "Klientské knihovny I2P jsou nyní k dispozici na Maven Central!"
categories: ["summer-dev"]
---

Jsme téměř v polovině měsíce API v rámci Summer Dev a dosahujeme velkého pokroku na několika frontách. S potěšením oznamuji, že první z nich je dokončen: klientské knihovny I2P jsou nyní k dispozici na Maven Central!

To by mělo vývojářům v jazyce Java výrazně zjednodušit používání I2P v jejich aplikacích. Místo aby museli získávat knihovny z aktuální instalace, mohou jednoduše přidat I2P do svých závislostí. Aktualizace na nové verze bude podobně mnohem snazší.

## Jak je používat

Existují dvě knihovny, které byste měli znát:

- `net.i2p:i2p` - The core I2P APIs; you can use these to send individual datagrams.
- `net.i2p.client:streaming` - A TCP-like set of sockets for communicating over I2P.

Přidejte jednu nebo obě tyto položky do závislostí vašeho projektu a můžete začít!

### Gradle

```
compile 'net.i2p:i2p:0.9.26'
compile 'net.i2p.client:streaming:0.9.26'
```
### Gradle

```xml
<dependency>
    <groupId>net.i2p</groupId>
    <artifactId>i2p</artifactId>
    <version>0.9.26</version>
</dependency>
<dependency>
    <groupId>net.i2p.client</groupId>
    <artifactId>streaming</artifactId>
    <version>0.9.26</version>
</dependency>
```
Pro ostatní systémy sestavení viz stránky Maven Central pro knihovny core a streaming.

Vývojáři pro Android by měli používat I2P Android client library, která obsahuje stejné knihovny spolu s pomocnými nástroji specifickými pro Android. Brzy ji aktualizuji tak, aby závisela na nových knihovnách I2P, aby multiplatformní aplikace mohly pracovat nativně buď s I2P Android, nebo s desktopovým I2P.

## Get hacking!

Podívejte se na naši příručku pro vývoj aplikací, která vám pomůže začít s těmito knihovnami. Můžete si o nich s námi také popovídat na IRC v kanálu #i2p-dev. A pokud je začnete používat, dejte nám vědět, na čem pracujete, s hashtagem #I2PSummer na Twitteru!
