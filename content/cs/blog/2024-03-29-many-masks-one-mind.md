---
title: "Mnoho masek, jedna mysl: Zabezpečení NetDB"
date: 2024-03-29
author: "idk"
description: "Mnoho masek, jedna mysl: Zabezpečení NetDB"
categories: ["development"]
API_Translate: pravda
---

Poznámka autora: útoky zmíněné v tomto článku nejsou možné proti aktuálním verzím I2P.

Jako samoorganizující se peer-to-peer síť se I2P spoléhá na routery účastnící se sítě, že budou mít způsob, jak sdílet informace o tom, co se v síti nachází, a jak k tomu přistupovat. Routery I2P toho dosahují pomocí NetDB, DHT založené na Kademlii, ale upravené pro I2P. NetDB musí sdílet dva hlavní typy záznamů, "RouterInfos" (informace o routerech), které uzly použijí pro přímou komunikaci s jinými routery, a "LeaseSets", které jiné uzly použijí ke komunikaci s klienty I2P prostřednictvím anonymních tunnelů. Routery si často navzájem předávají záznamy NetDB, buď tak, že posílají informace routeru nebo klientovi, nebo tak, že informace od routeru či klienta vyžadují. To znamená, že záznamy mohou přicházet přímo či nepřímo, anonymně či neanonymně, v závislosti na potřebách sítě a schopnostech klienta. Jako anonymizační síť však musí zároveň zajistit, aby bylo nemožné vyžádat si neanonymně informace, které byly odeslány anonymně. Stejně tak musí být nemožné vyžádat si anonymně informace, které byly odeslány neanonymně. Pokud by byla možná kterákoliv z těchto situací, bylo by možné provést linkovací útok, který útočníkovi umožní určit, zda klienti a routery sdílejí společný pohled na NetDB. Pokud lze spolehlivě určit, že tyto dva cíle sdílejí společný pohled na NetDB, je velmi pravděpodobné, že jsou na stejném routeru, což výrazně oslabuje anonymitu cíle. Protože anonymizačních sítí je jen velmi málo a I2P je jediná, kde se směrovací tabulka sdílí prostřednictvím činnosti DHT, je tato třída útoků prakticky jedinečná pro I2P a její vyřešení je důležité pro úspěch I2P.

Zvažte následující scénář: Existuje I2P router, který hostuje I2P klienta. Router publikuje RouterInfo a I2P klient publikuje svůj LeaseSet. Protože jsou oba publikovány v NetDB, mohou ostatní I2P routery dotazovat NetDB, aby zjistily, jak s nimi komunikovat. To je normální a zásadní pro fungování překryvné sítě (overlay network) typu, který I2P implementuje. Útočník provozuje I2P router a dotazuje NetDB na cílový RouterInfo a cílový LeaseSet. Poté vytvoří nový LeaseSet, který je jedinečný a případně i falešný, a pošle jej přes tunnel k LeaseSetu klienta, na kterého útok cílí. Klient zpracuje zkonstruovaný LeaseSet a přidá jej do své vlastní NetDB. Útočník pak požádá o zkonstruovaný LeaseSet zpět přímo od routeru, s použitím RouterInfo, které získal z NetDB. Pokud se zkonstruovaný LeaseSet vrátí jako odpověď, může útočník usoudit, že cílový klient a cílový router sdílejí společný pohled na NetDB.

To je jednoduchý příklad třídy deanonymizačních útoků na NetDB, která spoléhá na přidání záznamu do NetDB jiné osoby pod jednou identitou a následné vyžádání téhož zpět pod jinou identitou. V tomto případě jsou dotčenými identitami identita "router" a identita "klienta". Nicméně v některých návrzích je také možné propojení klient–klient, které je méně škodlivé. Navrhnout obranu proti této třídě útoků vyžaduje, aby měl router možnost určit, zda je či není bezpečné sdělit určitou informaci potenciální identitě.

Jak bychom o tomto problému měli přemýšlet? O co tu ve skutečnosti jde, je propojitelnost různých "identit" v síti. Možnost propojení vzniká proto, že všechny tyto identity sdílejí společnou datovou strukturu, která si "pamatuje", s kým komunikovala a kdo komunikoval s ní. Také si "pamatuje", jak k této komunikaci došlo.

Na chvíli si představme, že jsme útočník. Představte si, že se snažíte odhalit totožnost mistra převleků. Určitě víte, že jste už viděli jeho skutečnou tvář, a také víte, že pravidelně komunikujete s jedním z jeho převleků. Jak byste postupovali, abyste zjistili, že identita v převleku a skutečná identita patří téže osobě? Tomu, kdo je v převleku, bych mohl sdělit tajemství. Pokud osoba bez převleku zareaguje použitím tajné informace, pak mohu usoudit, že osoba bez převleku to tajemství zná. Za předpokladu, že osoba v převleku tajemství nikomu dalšímu nesdělila, mohu tedy předpokládat, že osoba bez převleku a osoba v převleku jsou ve skutečnosti tatáž osoba. Ať už mistr převleků nosí kolik chce masek, má jen jednu mysl.

Aby bylo možné úspěšně chránit identity klientů I2P, musí být I2P schopné fungovat jako lepší mistr maskování než ten popsaný výše. Musí být schopné "pamatovat si" několik důležitých informací o tom, jak se podílelo na NetDB, a na základě těchto detailů odpovídajícím způsobem reagovat. Musí si umět vybavit:

- Whether a NetDB Entry was received directly, or received down a client tunnel
- Whether a NetDB Entry was sent by a peer in response to our lookup, or sent unsolicited
- Which NetDB Entry was received down Which client Tunnel
- Multiple versions of the same entry for different client tunnels

Z hlediska struktury je nejlépe pochopitelným a nejspolehlivějším způsobem, jak tento vzor řešit, použít "Sub-DBs." Sub-DB's jsou miniatury NetDB's, které pomáhají NetDB organizovat záznamy, aniž by ztratila přehled. Každý klient dostane Sub-DB pro vlastní použití a samotný router má plnohodnotnou NetDB. Pomocí Sub-DB's dáváme našemu mistrovi převleků kartotéku tajemství uspořádanou podle toho, kdo se s ním o ta tajemství podělil. Když je požadavek poslán klientovi, hledají se pouze záznamy, které byly klientovi předány, a když je požadavek poslán na router, použije se pouze NetDB pro celý router. Tímto způsobem nejen vyřešíme nejjednodušší formu útoku, ale také oslabíme účinnost celé této třídy útoků.
