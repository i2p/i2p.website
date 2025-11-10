---
title: "GOST Sig Type"
number: "134"
author: "orignal"
created: "2017-02-18"
lastupdated: "2017-03-31"
status: "Open"
thread: "http://zzz.i2p/topics/2239"
---

## Přehled

Podpis eliptické křivky GOST R 34.10 používaný úřady a podniky v Rusku. Podpora by mohla zjednodušit integraci existujících aplikací (obvykle založených na CryptoPro). Hash funkce je GOST R 34.11 o 32 nebo 64 bajtech. V zásadě funguje stejným způsobem jako EcDSA, podpis a velikost veřejného klíče je 64 nebo 128 bajtů.

## Motivace

Kryptografie eliptických křivek nikdy nebyla zcela důvěryhodná a vyvolává mnoho spekulací o možných zadních vrátkách. Proto neexistuje žádný ultimátní typ podpisu, kterému by všichni věřili. Přidání dalšího typu podpisu poskytne lidem více možností, kterým více důvěřují.

## Návrh

GOST R 34.10 používá standardní eliptickou křivku s vlastními sadami parametrů. Matematika stávajících skupin může být znovu použita. Nicméně podepisování a ověřování je odlišné a musí být realizováno. Viz RFC: https://www.rfc-editor.org/rfc/rfc7091.txt GOST R 34.10 má pracovat spolu s hash GOST R 34.11. Použijeme GOST R 34.10-2012 (známý také jako steebog) buď 256 nebo 512 bitů. Viz RFC: https://tools.ietf.org/html/rfc6986

GOST R 34.10 nespecifikuje parametry, nicméně existují dobré sady parametrů používané všemi. GOST R 34.10-2012 s veřejnými klíči 64 bajtů dědí sady parametrů CryptoPro z GOST R 34.10-2001 Viz RFC: https://tools.ietf.org/html/rfc4357

Nicméně novější sady parametrů pro klíče 128 bajtů jsou vytvořeny zvláštní technickou komisí tc26 (tc26.ru). Viz RFC: https://www.rfc-editor.org/rfc/rfc7836.txt

Implementace založená na OpenSSL v i2pd ukazuje, že je rychlejší než P256 a pomalejší než 25519.

## Specifikace

Podporovány jsou pouze GOST R 34.10-2012 a GOST R 34.11-2012. Dva nové typy podpisů: 9 - GOSTR3410_GOSTR3411_256_CRYPTO_PRO_A označuje typ veřejného klíče a podpisu 64 bajtů, velikost hashe 32 bajtů a sadu parametrů CryptoProA (známou také jako CryptoProXchA) 10 - GOSTR3410_GOSTR3411_512_TC26_A označuje typ veřejného klíče a podpisu 128 bajtů, velikost hashe 64 bajtů a sadu parametrů A z TC26.

## Migrace

Tyto typy podpisů jsou určeny pouze pro použití jako volitelný typ podpisu. Není nutná žádná migrace. i2pd to již podporuje.
