---
title: "Záznamy služeb v LS2"
number: "167"
author: "zzz, orignal, eyedeekay"
created: "2024-06-22"
lastupdated: "2025-04-03"
status: "Zavřeno"
thread: "http://zzz.i2p/topics/3641"
target: "0.9.66"
toc: true
---

## Stav
Schváleno při druhém přezkumu 2025-04-01; specifikace jsou aktualizovány; ještě není implementováno.


## Přehled

I2P postrádá centralizovaný DNS systém.
Avšak, adresář společně se systémem hostnames b32 umožňuje
routeru vyhledat plné destinace a získat lease sety, které obsahují
seznamy bran a klíčů, takže klienti mohou připojit k té destinaci.

Lease sety jsou tedy v určitém smyslu jako záznamy DNS. Momentálně však chybí možnost zjistit,
zda daný host podporuje nějaké služby, buď na té destinaci nebo na jiné,
podobně jako DNS SRV záznamy [SRV](https://en.wikipedia.org/wiki/SRV_record) [RFC2782](https://datatracker.ietf.org/doc/html/rfc2782).

První aplikací pro toto může být peer-to-peer email.
Další možné aplikace: DNS, GNS, klíčové servery, certifikační autority, časové servery,
bittorrent, kryptoměny, jiné peer-to-peer aplikace.


## Související návrhy a alternativy

### Seznamy služeb

Návrh LS2 č. 123 [Prop123](/en/proposals/123-new-netdb-entries/) definoval 'záznamy služeb', které indikují, že destinace
participuje v globální službě. Floodfill servery by agregovaly tyto záznamy
do globálních 'seznamů služeb'.
To nebylo nikdy implementováno kvůli komplexnosti, nedostatku autentizace,
bezpečnostním obavám a obavám ze spamu.

Tento návrh se liší v tom, že poskytuje vyhledávání služby pro konkrétní destinaci,
ne globální pool destinací pro nějakou globální službu.

### GNS

GNS [GNS](http://zzz.i2p/topcs/1545) navrhuje, aby každý provozoval svůj vlastní DNS server.
Tento návrh je komplementární, protože bychom mohli použít záznamy služeb ke specifikaci,
že GNS (nebo DNS) je podporováno, se standardním názvem služby "domain" na portu 53.

### Dot well-known

V [DOTWELLKNOWN](http://i2pforum.i2p/viewtopic.php?p=3102) je navrhováno, že služby by měly být vyhledány prostřednictvím HTTP požadavku na
/.well-known/i2pmail.key. To vyžaduje, aby každá služba měla spojenou
webovou stránku pro hostování klíče. Většina uživatelů neprovozuje webové stránky.

Jedním z řešení je, že bychom mohli předpokládat, že služba pro b32 adresu je ve skutečnosti
provozována na té b32 adrese. Takže při hledání služby pro example.i2p se vyžaduje
HTTP dotaz na http://example.i2p/.well-known/i2pmail.key, ale
služba pro aaa...aaa.b32.i2p tento dotaz nevyžaduje, může se připojit přímo.

Ale je zde dvojznačnost, protože example.i2p může být také adresována jeho b32.

### MX záznamy

SRV záznamy jsou jednoduše obecnou verzí MX záznamů pro jakoukoli službu.
"_smtp._tcp" je "MX" záznam.
MX záznamy nejsou potřeba, pokud máme SRV záznamy, a samotné MX záznamy
neposkytují obecný záznam pro jakoukoli službu.


## Návrh

Záznamy služeb jsou umístěny v sekci možností v LS2 [LS2](/en/docs/spec/common-structures/).
Sekce možností LS2 je momentálně nevyužitá.
Nepodporováno pro LS1.
To je podobné návrhu šířky pásma tunelu [Prop168](/en/proposals/168-tunnel-bandwidth/),
který definuje možnosti pro záznamy sestavení tunelu.

Aby bylo možné vyhledat adresu služby pro konkrétní hostname nebo b32, router získá
leaseset a vyhledá v něm záznam služby v rámci vlastností.

Služba může být hostována na stejné destinaci jako samotný LS, nebo může odkazovat
na jiný hostname/b32.

Pokud je cílová destinace pro službu odlišná, i cílový LS musí
obsahovat záznam služby, který na sebe ukazuje, čímž indikuje, že podporuje službu.

Návrh nevyžaduje zvláštní podporu nebo cachování nebo jakékoliv změny ve floodfills.
Pouze vydavatel leasesetu a klient hledající záznam služby
musí tyto změny podporovat.

Jsou navržena malá rozšíření I2CP a SAM pro usnadnění získání
záznamů služby klienty.



## Specifikace

### Specifikace možností LS2

Možnosti LS2 MUSÍ být seřazeny podle klíče, takže podpis je invariantní.

Definováno následujícím způsobem:

- serviceoption := optionkey optionvalue
- optionkey := _service._proto
- service := Symbolický název požadované služby. Musí být malými písmeny. Příklad: "smtp".
  Povoleny jsou znaky [a-z0-9-] a nesmí začínat nebo končit znakem '-'.
  Standardní identifikátory z [REGISTRY](http://www.dns-sd.org/ServiceTypes.html) nebo Linux /etc/services musí být použity, pokud jsou tam definovány.
- proto := Transportní protokol požadované služby. Musí být malými písmeny, buď "tcp" nebo "udp".
  "tcp" znamená streaming a "udp" znamená odpovídající datagramy.
  Ukazatele protokolu pro surové datagramy a datagram2 mohou být definovány později.
  Povoleny jsou znaky [a-z0-9-] a nesmí začínat nebo končit znakem '-'.
- optionvalue := self | srvrecord[,srvrecord]*
- self := "0" ttl port [appoptions]
- srvrecord := "1" ttl priority weight port target [appoptions]
- ttl := čas života, celé číslo v sekundách. Kládlý kladný. Příklad: "86400".
  Minimum 86400 (jednoho dne) je doporučeno, viz sekce Doporučení níže pro další podrobnosti.
- priority := Priorita cílového hostitele, nižší hodnota znamená více preferovaný. Nezáporné celé číslo. Příklad: "0"
  Užitené pouze pokud existuje více než jeden záznam, ale požadováno i pokud je pouze jeden záznam.
- weight := Relativní váha pro záznamy se stejnou prioritou. Vyšší hodnota znamená větší šanci na vybrání. Nezáporné celé číslo. Příklad: "0"
  Užitečné pouze pokud existuje více než jeden záznam, ale požadováno i pokud je pouze jeden záznam.
- port := I2CP port, na kterém je služba nalezena. Nezáporné celé číslo. Příklad: "25"
  Port 0 je podporován, ale nedoporučuje se.
- target := Hostname nebo b32 destinace poskytující služby. Platný hostname jako v [NAMING](/en/docs/naming/). Musí být malými písmeny.
  Příklad: "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.b32.i2p" nebo "example.i2p".
  b32 je doporučeno, pokud hostname není "dobře známé", tj. v oficiálních nebo výchozích adresářích.
- appoptions := libovolný text specifický pro aplikaci, nesmí obsahovat " " nebo ",". Kódování je UTF-8.

### Příklady


V LS2 pro aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.b32.i2p, ukazující na jeden SMTP server:

    "_smtp._tcp" "1 86400 0 0 25 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p"

V LS2 pro aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.b32.i2p, ukazující na dva SMTP servery:

    "_smtp._tcp" "1 86400 0 0 25 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p,86400 1 0 25 cccccccccccccccccccccccccccccccccccccccccccc.b32.i2p"

V LS2 pro bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p, ukazující na sebe jako SMTP server:

    "_smtp._tcp" "0 999999 25"

Možný formát pro přesměrování emailu (viz níže):

    "_smtp._tcp" "1 86400 0 0 25 smtp.postman.i2p example@mail.i2p"


### Limity


Formát datové struktury Mapping používaný pro možnosti LS2 omezuje klíče a hodnoty na maximálně 255 bajtů (ne znaků).
U b32 cíle je optionvalue asi 67 bajtů, takže se vejdou pouze 3 záznamy.
Možná jen jeden nebo dva s dlouhým polem appoptions, nebo až čtyři nebo pět s krátkým hostname.
To by mělo být dostačující; více záznamů by mělo být vzácné.


### Rozdíly oproti [RFC2782](https://datatracker.ietf.org/doc/html/rfc2782)


- Žádné koncové tečky
- Žádné jméno po proto
- Povinně malá písmena
- V textovém formátu s čárkami oddělenými záznamy, nikoliv binárním DNS formátu
- Různé typy indikátorů záznamů
- Další pole appoptions


### Poznámky


Není povoleno žádné zástupné znakování jako hvězdička, hvězdička._tcp nebo _tcp.
Každá podporovaná služba musí mít svůj vlastní záznam.



### Registr názvů služeb

Nestandardní identifikátory, které nejsou uvedeny v [REGISTRY](http://www.dns-sd.org/ServiceTypes.html) nebo Linux /etc/services
mohou být požadovány a přidány do specifikace obecných struktur [LS2](/en/docs/spec/common-structures/).

Formáty appoptions specifické pro služby mohou být také tam přidány.


### Specifikace I2CP

Protokol [I2CP](/en/docs/spec/i2cp/) musí být rozšířen, aby podporoval vyhledávání služeb.
Další MessageStatusMessage a/nebo HostReplyMessage chybové kódy související s vyhledáváním služeb
jsou vyžadovány.
Aby bylo vyhledávací zařízení obecné, nejen specifické pro záznamy služby,
návrh je podporovat získání všech možností LS2.

Implementace: Rozšíření HostLookupMessage pro přidání požadavku na
LS2 možnosti pro hash, hostname a destinaci (typy požadavku 2-4).
Rozšíření HostReplyMessage pro přidání možností mapování, pokud je požadováno.
Rozšíření HostReplyMessage s dalšími chybovými kódy.

Možnosti mapování mohou být kešovány nebo negativně kešovány na krátkou dobu na straně klienta nebo routeru,
závislé na implementaci. Doporučená maximální doba je jedna hodina, pokud není TTL záznamu služby kratší.
Záznamy služeb mohou být kešovány až do TTL specifikovaného aplikací, klientem nebo routerem.

Rozšíření specifikace následovně:

### Konfigurační možnosti

Přidat následující do [I2CP-OPTIONS]

i2cp.leaseSetOption.nnn

Možnosti, které mají být umístěny v leasesetu. K dispozici pouze pro LS2.
nnn začíná číslem 0. Hodnota možnosti obsahuje "key=value".
(nezahrnovat uvozovky)

Příklad:

    i2cp.leaseSetOption.0=_smtp._tcp=1 86400 0 0 25 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p


### HostLookup Message


- Typ vyhledávání 2: Vyhledání pomocí hashe, požadavek na mapování možností
- Typ vyhledávání 3: Vyhledání pomocí hostname, požadavek na mapování možností
- Typ vyhledávání 4: Vyhledání pomocí destinace, požadavek na mapování možností

Pro typ vyhledávání 4, item 5 je Destinace.



### HostReply Message


Pro typy vyhledávání 2-4, router musí získat leaseset,
i když je vyhledávací klíč v adresáři.

Pokud je úspěšné, HostReply bude obsahovat možnosti mapování
z leasesetu a zahrne je jako položku 5 po destinaci.
Pokud v mapování nejsou žádné možnosti nebo byl leaseset verze 1,
stále bude zahrnuto jako prázdné mapování (dva bajty: 0 0).
Všechny možnosti z leasesetu budou zahrnuty, nejen možnosti záznamů služeb.
Například možnosti pro parametry definované v budoucnosti mohou být přítomny.

Při selhání vyhledání leasesetu, odpověď bude obsahovat nový chybový kód 6 (selhání vyhledání leasesetu)
a nebude obsahovat mapování.
Když je vrácen chybový kód 6, pole Destination může nebo nemusí být přítomné.
Bude přítomné, pokud bylo úspěšné vyhledání hostname v adresáři,
nebo pokud bylo předchozí vyhledání úspěšné a výsledek byl kešován,
nebo pokud byla Destinace přítomna ve vyhledávací zprávě (typ vyhledávání 4).

Pokud není typ vyhledávání podporován,
odpověď bude obsahovat nový chybový kód 7 (typ vyhledávání nepodporován).



### Specifikace SAM

Protokol [SAMv3](/en/docs/api/samv3/) musí být rozšířen, aby podporoval vyhledávání služeb.

Rozšíření NAMING LOOKUP následujícím způsobem:

NAMING LOOKUP NAME=example.i2p OPTIONS=true požaduje mapování možností v odpovědi.

NAME může být plná destinace base64 pokud je OPTIONS=true.

Pokud bylo vyhledání destinace úspěšné a možnosti byly přítomny v leasesetu,
pak v odpovědi, po destinaci,
bude jedna nebo více možností ve formě OPTION:key=value.
Každá možnost bude mít samostatný prefix OPTION:.
Všechny možnosti z leasesetu budou zahrnuty, nejen možnosti záznamů služeb.
Například možnosti pro parametry definované v budoucnosti mohou být přítomny.
Příklad:

    NAMING REPLY RESULT=OK NAME=example.i2p VALUE=base64dest OPTION:_smtp._tcp="1 86400 0 0 25 bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb.b32.i2p"

Klíče obsahující '=', a klíče nebo hodnoty obsahující novou řádku,
jsou považovány za neplatné a pár klíč/hodnota bude odstraněn z odpovědi.

Pokud nejsou nalezeny žádné možnosti v leasesetu, nebo pokud byl leaseset verze 1,
odpověď nebude zahrnovat žádné možnosti.

Pokud OPTIONS=true bylo v vyhledávání a leaseset není nalezen, bude vrácená nová hodnota výsledku LEASESET_NOT_FOUND.


## Alternativa Naming Lookup

Byl zvažován alternativní návrh, jak podporovat vyhledávání služeb
jako plného hostname, například _smtp._tcp.example.i2p,
aktualizací [NAMING](/en/docs/naming/) pro specifikaci zpracování hostname začínajících '_'.
To bylo odmítnuto ze dvou důvodů:

- Změny I2CP a SAM by byly stále nezbytné pro průchod TTL a informací o portu k klientovi.
- Nebylo by to obecné zařízení, které by mohlo být použito pro získání dalších LS2
  možností, které by mohly být v budoucnu definovány.


## Doporučení

Servery by měly specifikovat TTL alespoň 86400 a standardní port pro aplikaci.



## Pokročilé funkce

### Rekurzivní vyhledávání

Může být žádoucí podporovat rekurzivní vyhledávání, kde každý následující leaseset
je kontrolován pro záznam služby ukazující na jiný leaseset, ve stylu DNS.
To pravděpodobně není nutné, alespoň v počáteční implementaci.

TODO



### Pole specifická pro aplikaci

Může být žádoucí mít v záznamu služby data specifická pro aplikaci.
Například operátor example.i2p by mohl chtít naznačit, že email by měl
být přesměrován na example@mail.i2p. Část "example@" by musela být v samostatném poli
záznamu služby nebo odstraněna z cíle.

I když operátor provozuje svou vlastní emailovou službu, může chtít naznačit, že
email by měl být poslán na example@example.i2p. Většina I2P služeb je provozována jednou osobou.
Takže samostatné pole může být i tady užitečné.

TODO jak to udělat obecně


### Změny nutné pro Email

Mimo rozsah tohoto návrhu. Viz [DOTWELLKNOWN](http://i2pforum.i2p/viewtopic.php?p=3102) pro diskusi.


## Poznámky k implementaci

Kešování záznamů služeb až do TTL může být provedeno routerem nebo aplikací,
závislé na implementaci. Zda kešovat trvale je také závislé na implementaci.

Vyhledávání musí také vyhledat cílový leaseset a ověřit, že obsahuje "self" záznam
před vrácením cílové destinace klientovi.


## Analýza bezpečnosti

Jelikož je leaseset podepsán, jakékoliv záznamy služeb v něm jsou autentizovány podpisovým klíčem destinace.

Záznamy služeb jsou veřejné a viditelné pro floodfill servery, pokud není leaseset šifrován.
Každý router požadující leaseset bude moci vidět záznamy služeb.

SRV záznam jiný než "self" (tj. ten, který ukazuje na jiný hostname/b32 cíl)
nevyžaduje souhlas cílového hostname/b32.
Není jasné, zda by přesměrování služby na libovolnou destinaci mohlo usnadnit některý
druh útoku, nebo jaký by mohl být účel takového útoku.
Avšak tento návrh zmírňuje takový útok vyžadováním, aby cílový
také zveřejnil "self" SRV záznam. Implementátoři musí zkontrolovat "self" záznam
v leasesetu cíle.


## Kompatibilita

LS2: Žádné problémy. Všechny známé implementace momentálně ignorují pole možností v LS2,
a správně přeskočí ne-prázdné pole možností.
To bylo ověřeno při testování jak Java I2P, tak i2pd během vývoje LS2.
LS2 bylo implementováno v 0.9.38 v roce 2016 a je dobře podporováno všemi implementacemi routeru.
Návrh nevyžaduje zvláštní podporu nebo cachování nebo jakékoliv změny ve floodfills.

Naming: '_' není platný znak v i2p hostnamech.

I2CP: Typy vyhledávání 2-4 by neměly být zasílány routerům pod minimální verzí API
ve které je to podporováno (TBD).

SAM: Java SAM server ignoruje další klíče/hodnoty jako OPTIONS=true.
i2pd by měl také, k ověření.
SAM klienti nebudou dostávat další hodnoty v odpovědi, pokud nejsou požadovány s OPTIONS=true.
Žádné zvýšení verze by nemělo být nutné.


