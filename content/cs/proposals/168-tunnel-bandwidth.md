---
title: "Parametry šířky pásma tunelu"
number: "168"
author: "zzz"
created: "2024-07-31"
lastupdated: "2024-12-10"
status: "Closed"
thread: "http://zzz.i2p/topics/3652"
target: "0.9.65"
toc: true
---

## POZNÁMKA

Tento návrh byl schválen a je nyní součástí
[Tunnel Creation ECIES specification](/docs/specs/implementation/#tunnel-creation-ecies) od API 0.9.65.
Zatím nejsou známy žádné implementace; data implementace / verze API jsou TBD.


## Přehled

Jak jsme během posledních několika let zvýšili výkon sítě s novými protokoly,
typy šifrování a vylepšeními řízení přetížení,
rychlejší aplikace jako streamování videa se stávají možnými.
Tyto aplikace vyžadují vysokou šířku pásma na každém kroku ve svých tunelích klienta.

Účastnické routery však nemají žádné informace o tom, kolik
šířky pásma tunel použije, když obdrží požadavek na vytvoření tunelu.
Mohou pouze přijmout nebo odmítnout tunel na základě aktuálního celkového
využití šířky pásma všemi účastnickými tunely a celkového limitu šířky pásma pro účastnické tunely.

Žádající routery také nemají žádné informace o tom, kolik
šířky pásma je k dispozici na každém kroku.

Rovněž, routery v současné době nemají žádný způsob, jak omezit příchozí provoz na tunelu.
To by bylo velmi užitečné během přetížení nebo DDoS útoku na službu.

Tento návrh řeší tyto problémy přidáním parametrů šířky pásma do
požadavků a odpovědí na vytvoření tunelu.


## Návrh

Přidat parametry šířky pásma do záznamů v ECIES zprávách o vytvoření tunelu (viz [Tunnel Creation ECIES specification](/docs/specs/implementation/#tunnel-creation-ecies))
v poli mapování možností vytvoření tunelu. Použít krátké názvy parametrů, protože prostor
pro pole možností je omezený.
Zprávy o vytvoření tunelu mají pevnou velikost, takže toto nezvětšuje
velikost zpráv.


## Specifikace

Aktualizujte [specifikaci zprávy o vytvoření tunelu ECIES](/docs/specs/implementation/#tunnel-creation-ecies)
takto:

Pro dlouhé i krátké záznamy vytvoření ECIES:

### Možnosti žádosti o vytvoření

Následující tři možnosti mohou být nastaveny v poli mapování možností vytvoření tunelu záznamu:
Žádající router může zahrnout kteroukoliv, všechny, nebo žádnou.

- m := minimální šířka pásma požadovaná pro tento tunel (KBps kladné celé číslo jako řetězec)
- r := požadovaná šířka pásma pro tento tunel (KBps kladné celé číslo jako řetězec)
- l := limit šířky pásma pro tento tunel; posílá se pouze k IBGW (KBps kladné celé číslo jako řetězec)

Omezení: m <= r <= l

Účastnický router by měl odmítnout tunel, pokud je specifikováno "m" a nemůže
poskytnout alespoň takovou šířku pásma.

Možnosti žádosti jsou poslány každému účastníkovi v odpovídajícím šifrovaném záznamu žádosti o vytvoření,
a nejsou viditelné pro ostatní účastníky.


### Možnost odpovědi na vytvoření

Následující možnost může být nastavena v poli mapování možností odpovědi na vytvoření záznamu,
když je odpověď PŘIJATA:

- b := dostupná šířka pásma pro tento tunel (KBps kladné celé číslo jako řetězec)

Účastnický router by měl tuto možnost zahrnout, pokud bylo specifikováno "m" nebo "r"
v žádosti o vytvoření. Hodnota by měla být alespoň taková jako hodnota "m", pokud je specifikována,
ale může být menší nebo větší než hodnota "r", pokud je specifikována.

Účastnický router by se měl pokusit rezervovat a poskytnout alespoň
takovouto šířku pásma pro tunel, nicméně to není zaručeno.
Routery nemohou předpovídat podmínky 10 minut do budoucnosti, a
účastnický provoz má nižší prioritu než vlastní provoz routeru a tunely.

Routery také mohou přidělit více dostupné šířky pásma, pokud je to nutné, a toto je
pravděpodobně žádoucí, protože jiné kroky v tunelu by jej mohly odmítnout.

Z těchto důvodů by odpověď účastnického routeru měla být považována
za závazek na základě nejlepšího úsilí, nikoliv záruku.

Možnosti odpovědi jsou poslány žádajícímu routeru v odpovídajícím šifrovaném záznamu odpovědi na vytvoření,
a nejsou viditelné pro ostatní účastníky.


## Poznámky k implementaci

Parametry šířky pásma jsou jako viditelné na účastnických routerech na vrstvě tunelu,
tj. počet zpráv tunelu pevné velikosti 1 KB za sekundu.
Přenosová režie (NTCP2 nebo SSU2) není zahrnuta.

Tato šířka pásma může být mnohem větší nebo menší než šířka pásma viděná na straně klienta.
Zprávy tunelu obsahují podstatnou režii, včetně režie vyšších vrstev,
včetně ratchet a streamování. Občasné malé zprávy jako potvrzení streaming budou
rozšířeny na 1 KB každá.
Nicméně, gzip komprese na vrstvě I2CP může podstatně snížit šířku pásma.

Nejjednodušší implementace na žádajícím routeru je použití
průměrné, minimální, a/nebo maximální šířky pásma aktuálních tunelů v poolu
k výpočtu hodnot pro žádost.
Komplexnější algoritmy jsou možné a jsou na implementátorovi.

Nejsou definovány žádné aktuální možnosti I2CP nebo SAM pro klienta, aby sdělil
routeru, jaká šířka pásma je vyžadována, a zde nejsou navrhovány žádné nové možnosti.
Možnosti mohou být definovány později, pokud to bude nutné.

Implementace mohou využít dostupnou šířku pásma nebo jakákoliv jiná data, algoritmus, místní politiku,
nebo místní konfiguraci k výpočtu hodnoty šířky pásma vrácené v
odpovědi na vytvoření. Není specifikováno tímto návrhem.

Tento návrh vyžaduje, aby vstupní brány implementovaly omezení šířky pásma pro jednotlivé tunely,
pokud je požadováno pomocí možnosti "l".
Nezavazuje ostatní účastnické kroky implementovat omezení šířky pásma pro jednotlivé tunely nebo globální
omezení jakéhokoli typu, nebo specifikovat konkrétní algoritmus nebo implementaci, pokud vůbec nějakou.

Tento návrh také nevyžaduje, aby klientské routery omezovaly provoz
na hodnotu "b" vrácenou účastnickým krokem, a v závislosti na aplikaci
to nemusí být možné, zejména pro příchozí tunely.

Tento návrh se týká pouze tunelů vytvořených iniciátorem. Není definována žádná
metoda pro požadování nebo přidělení šířky pásma pro tunely "vzdáleného konce" vytvořené
vlastníkem druhého konce end-to-end spojení.


## Bezpečnostní analýza

Otisky klienta nebo korelace mohou být možné na základě žádostí.
Klientský (iniciátorský) router může chtít náhodně generovat hodnoty "m" a "r" místo odesílání
stejné hodnoty na každý krok; nebo odesílat omezenou sadu hodnot, které představují "bucket" šířky pásma,
nebo nějakou kombinaci obojího.

DDoS s nadměrnou alokací: I když může být nyní možné provést DDoS útok na router vytvořením a
použitím velkého počtu tunelů přes něj, tento návrh to pravděpodobně usnadňuje,
jednoduše požadováním jednoho nebo více tunelů s velkými požadavky na šířku pásma.

Implementace mohou a měly by použít jednu nebo více z následujících strategií
k minimalizaci tohoto rizika:

- Nad alokaci dostupné šířky pásma
- Omezení alokace šířky pásma na tunel na určité procento dostupné šířky pásma
- Omezení rychlosti nárůstu v přidělené šířce pásma
- Omezení rychlosti nárůstu ve využité šířce pásma
- Omezení přidělené šířky pásma pro tunel, pokud není využita brzy v životnosti tunelu (použít, jinak ztratíš)
- Sledování průměrné šířky pásma na tunel
- Sledování požadované vs. skutečně využité šířky pásma na tunel


## Kompatibilita

Žádné problémy. Všechny známé implementace v současné době ignorují pole mapování ve zprávách o vytvoření,
a správně přeskočí pole možností, které není prázdné.


## Migrace

Implementace mohou podporu přidat kdykoliv, není potřeba koordinace.

Protože v současné době není definována žádná verze API, kde je podpora tohoto návrhu vyžadována,
routery by měly zkontrolovat odpověď "b", aby si potvrdily podporu.


