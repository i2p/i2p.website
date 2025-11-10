---
title: "Transport SSU2"
date: 2022-10-11
author: "zzz"
description: "Transport SSU2"
categories: ["development"]
API_Translate: pravda
---

## Přehled

I2P has used a censorship-resistant UDP transport protocol "SSU" since 2005. We've had few, if any, reports of SSU being blocked in 17 years. However, by today's standards of security, blocking resistance, and performance, we can do better. Much better.

Proto jsme společně s [projektem i2pd](https://i2pd.xyz/) vytvořili a implementovali "SSU2", moderní protokol UDP navržený podle nejvyšších standardů bezpečnosti a odolnosti vůči blokování. Tento protokol nahradí SSU.

Zkombinovali jsme šifrování podle průmyslových standardů s nejlepšími vlastnostmi UDP protokolů WireGuard a QUIC, společně s prvky zajišťujícími odolnost vůči cenzuře našeho TCP protokolu "NTCP2". SSU2 může být jedním z nejbezpečnějších transportních protokolů, které kdy byly navrženy.

Týmy Java I2P a i2pd dokončují transport SSU2 a v příštím vydání jej povolíme pro všechny routers. Tím završujeme náš desetiletý plán na aktualizaci veškeré kryptografie pocházející z původní implementace Java I2P z roku 2003. SSU2 nahradí SSU, naše jediné zbývající použití ElGamalovy kryptografie.

- Signature types and ECDSA signatures (0.9.8, 2013)
- Ed25519 signatures and leasesets (0.9.15, 2014)
- Ed25519 routers (0.9.22, 2015)
- Destination encryption types and X25519 leasesets (0.9.46, 2020)
- Router encryption types and X25519 routers (0.9.49, 2021)

Po přechodu na SSU2 budeme mít všechny naše autentizované a šifrované protokoly převedené na standardní [Noise Protocol](https://noiseprotocol.org/) handshaky:

- NTCP2 (0.9.36, 2018)
- ECIES-X25519-Ratchet end-to-end protocol (0.9.46, 2020)
- ECIES-X25519 tunnel build messages (1.5.0, 2021)
- SSU2 (2.0.0, 2022)

Všechny protokoly I2P Noise používají následující standardní kryptografické algoritmy:

- [X25519](https://en.wikipedia.org/wiki/Curve25519)
- [ChaCha20/Poly1305 AEAD](https://www.rfc-editor.org/rfc/rfc8439.html)
- [SHA-256](https://en.wikipedia.org/wiki/SHA-2)

## Cíle

- Upgrade the asymmetric cryptography to the much faster X25519
- Use standard symmetric authenticated encryption ChaCha20/Poly1305
- Improve the obfuscation and blocking resistance features of SSU
- Improve the resistance to spoofed addresses by adapting strategies from QUIC
- Improved handshake CPU efficiency
- Improved bandwidth efficiency via smaller handshakes and acknowledgements
- Improve the security of the peer test and relay features of SSU
- Improve the handling of peer IP and port changes by adapting the "connection migration" feature of QUIC
- Move away from heuristic code for packet handling to documented, algorithmic processing
- Support a gradual network transition from SSU to SSU2
- Easy extensibility using the block concept from NTCP2

## Návrh

I2P používá více vrstev šifrování k ochraně provozu před útočníky. Nejnižší vrstvou je vrstva transportního protokolu, používaná pro spojení bod–bod mezi dvěma routers. V současnosti máme dva transportní protokoly: NTCP2, moderní protokol TCP zavedený v roce 2018, a SSU, protokol UDP vyvinutý v roce 2005.

SSU2, stejně jako předchozí transportní protokoly I2P, není obecným přenosovým kanálem pro data. Jeho primárním úkolem je bezpečně doručovat nízkoúrovňové zprávy I2NP z jednoho routeru do dalšího. Každé z těchto bod‑bodových spojení představuje jeden skok v I2P tunnel. Vyšší vrstvy protokolů I2P běží nad těmito bod‑bodovými spojeními a zajišťují end‑to‑end doručení garlic messages (tzv. „garlic“ zprávy) mezi I2P destinations (cíle).

Návrh UDP transportu přináší jedinečné a složité výzvy, které se u protokolů TCP nevyskytují. Protokol UDP musí řešit bezpečnostní problémy způsobené podvrhováním adres a musí implementovat vlastní řízení zahlcení. Kromě toho musí být všechny zprávy fragmentovány tak, aby se vešly do maximální velikosti paketu (MTU) na síťové cestě a příjemcem znovu sestaveny.

Nejprve jsme ve značné míře vycházeli z našich předchozích zkušeností s NTCP2, SSU a streamovacími protokoly. Poté jsme pečlivě prostudovali a výrazně čerpali ze dvou nedávno vyvinutých protokolů UDP:

- QUIC ([RFC 9000](https://www.rfc-editor.org/rfc/rfc9000.html), [RFC 9001](https://www.rfc-editor.org/rfc/rfc9001.html), [RFC 9002](https://www.rfc-editor.org/rfc/rfc9002.html))
- [WireGuard](https://www.wireguard.com/protocol/)

Klasifikace protokolů a jejich blokování ze strany nepřátelských on-path útočníků (v trase), jako jsou firewally na úrovni státu, není explicitní součástí modelu hrozeb těchto protokolů. Pro I2P je to však důležitá součást modelu hrozeb, protože naším posláním je poskytovat anonymní a vůči cenzuře odolný komunikační systém ohroženým uživatelům po celém světě. Proto velká část naší práce na návrhu spočívala v kombinaci poznatků získaných z NTCP2 a SSU s funkcemi a bezpečnostními mechanismy podporovanými v QUIC a WireGuard.

## Výkon

Síť I2P je komplexní mix rozmanitých routerů. Existují dvě hlavní implementace, které běží po celém světě na hardware od výkonných počítačů v datových centrech až po Raspberry Pi a telefony s Androidem. Routery používají jak TCP, tak UDP transporty. Ačkoli jsou vylepšení v SSU2 významná, nepředpokládáme, že budou pro uživatele patrná, a to ani lokálně, ani v end-to-end rychlostech přenosu.

Zde je několik nejdůležitějších bodů odhadovaných vylepšení pro SSU2 oproti SSU:

- 40% reduction in total handshake packet size
- 50% or more reduction in handshake CPU
- 90% or more reduction in ACK overhead
- 50% reduction in packet fragmentation
- 10% reduction in data phase overhead

## Přechodový plán

I2P se snaží zachovat zpětnou kompatibilitu, jednak kvůli stabilitě sítě, jednak proto, aby starší routery mohly i nadále být užitečné a bezpečné. Existují však určité limity, protože kompatibilita zvyšuje složitost kódu a nároky na údržbu.

Projekty Java I2P a i2pd ve svých příštích vydáních (2.0.0 a 2.44.0) na konci listopadu 2022 oba ve výchozím nastavení povolí SSU2. Mají však odlišné plány ohledně zakázání SSU. I2pd zakáže SSU okamžitě, protože SSU2 je oproti jejich implementaci SSU výrazným zlepšením. Java I2P plánuje zakázat SSU v polovině roku 2023, aby podpořila postupný přechod a dala starším routers čas na aktualizaci.

## Souhrn

Uveďte POUZE překlad, nic jiného:

Zakladatelé I2P museli učinit několik rozhodnutí ohledně kryptografických algoritmů a protokolů. Některá z těchto rozhodnutí byla lepší než jiná, ale po dvaceti letech je na většině z nich znát jejich stáří. Samozřejmě jsme věděli, že k tomu dojde, a poslední desetiletí jsme věnovali plánování a implementaci kryptografických modernizací.

SSU2 byl posledním a nejsložitějším protokolem, který jsme v rámci naší dlouhé cesty modernizace vyvíjeli. UDP přináší velmi náročnou sadu předpokladů a model hrozeb. Nejprve jsme navrhli a nasadili tři další varianty protokolů Noise a získali tak zkušenosti a hlubší porozumění otázkám bezpečnosti a návrhu protokolů.

Očekávejte, že SSU2 bude povoleno ve vydáních i2pd a Java I2P plánovaných na konec listopadu 2022. Pokud aktualizace proběhne dobře, nikdo si nevšimne žádné změny. Výkonnostní přínosy, ač významné, pravděpodobně nebudou pro většinu uživatelů měřitelné.

Jako obvykle doporučujeme, abyste aktualizovali na nové vydání, jakmile bude k dispozici. Nejlepším způsobem, jak udržovat bezpečnost a pomoci síti, je provozovat nejnovější vydání.
