---
title: "Adresářové příkazy pro odběrový kanál"
number: "112"
author: "zzz"
created: "2014-09-15"
lastupdated: "2020-07-16"
status: "Uzavřený"
thread: "http://zzz.i2p/topics/1704"
target: "0.9.26"
implementedin: "0.9.26"
---

## Poznámka
Nasazení v síti dokončeno.
Viz [SPEC](/docs/specs/subscription/) pro oficiální specifikaci.

## Přehled

Tento návrh se týká rozšíření odběrového kanálu adres o příkazy, aby bylo
umožněno jmenným serverům vysílat aktualizace záznamů od držitelů hostname.
Implementováno ve verzi 0.9.26.

## Motivace

V současnosti servery pro odběr hosts.txt jednoduše posílají data ve formátu
hosts.txt, který je následující:

    example.i2p=b64destination

Existuje několik problémů s tímto:

- Držitelé hostnamů nemohou aktualizovat Cílové místo (Destination) spojené s
  jejich hostnamy (aby například aktualizovali podpisový klíč na silnější typ).
- Držitelé hostnamů nemohou libovolně vzdát svých hostnamů; musí předat
  odpovídající soukromé klíče Cílového místa přímo novému držiteli.
- Neexistuje způsob, jak ověřit, že subdoména je řízena odpovídajícím základním
  jménem hostitele; to je aktuálně vymáháno individuálně některými jmennými
  servery.

## Návrh

Tento návrh přidává několik příkazových řádků do formátu hosts.txt. Prostřednictvím
těchto příkazů mohou jmenné servery rozšířit své služby na poskytování řady
dalších funkcí. Klienti, kteří implementují tento návrh, budou schopni poslouchat
tyto funkce prostřednictvím běžného odběrového procesu.

Všechny příkazové řádky musí být podepsány odpovídajícím Cílovým místem. To
zajistí, že změny budou prováděny pouze na žádost držitele hostnamu.

## Důsledky pro bezpečnost

Tento návrh nemá žádné důsledky pro anonymitu.

Zvýší se však riziko spojené se ztrátou kontroly nad klíčem Cílového místa, neboť
ten, kdo jej získá, může pomocí těchto příkazů provádět změny u jakýchkoliv
přidružených hostnamů. Ale toto není o nic větší problém než současný stav, kde
ten, kdo získá Cílové místo, může zneužít hostname a (částečně) převzít jeho
trafik. Zvýšené riziko je také vyváženo tím, že držitelé hostnamů mají možnost
změnit Cílové místo spojené s hostnamem, pokud uvěří, že bylo kompromitováno;
to je s aktuálním systémem nemožné.

## Specifikace

### Nové typy řádků

Tento návrh přidává dva nové typy řádků:

1. Příkazy pro přidání a změnu:

     example.i2p=b64destination#!key1=val1#key2=val2 ...

2. Příkazy pro odstranění:

     #!key1=val1#key2=val2 ...

#### Pořadí
Kanál nemusí být nutně v pořadí nebo kompletní. Například příkaz změny
může být na řádku před příkazem přidání, nebo bez příkazu přidání.

Klíče mohou být v libovolném pořadí. Dvojité položky klíčů nejsou povoleny. Všechny
klíče a hodnoty jsou citlivé na velikost písmen.

### Společné klíče

Požadováno ve všech příkazech:

sig
  B64 podpis, použitý podpisový klíč z cílového místa

Reference ke druhému hostname a/nebo cílovému místu:

oldname
  Druhé hostname (nové nebo změněné)
olddest
  Druhé b64 cílové místo (nové nebo změněné)
oldsig
  Druhý b64 podpis, využívající podpisový klíč z nolddest

Další společné klíče:

action
  Příkaz
name
  Hostname, přítomen pouze pokud není předcházena example.i2p=b64dest
dest
  B64 cílové místo, přítomen pouze pokud není předcházena example.i2p=b64dest
date
  V sekundách od epochy
expires
  V sekundách od epochy

### Příkazy

Všechny příkazy kromě příkazu "Přidat" musí obsahovat klíč/hodnotu "action=command".

Pro kompatibilitu s staršími klienty jsou většina příkazů předcházena example.i2p=b64dest,
jak je uvedeno níže. Pro změny jsou to vždy nové hodnoty. Jakékoliv staré
hodnoty jsou zahrnuty v části klíč/hodnota.

Uvedené klíče jsou povinné. Všechny příkazy mohou obsahovat další klíč/hodnota položky
nejsou zde definovány.

#### Přidat hostname
Předcházena example.i2p=b64dest
  ANO, to je nové jméno hostitele a cílové místo.
action
  NENÍ zahrnuto, je to implicitní.
sig
  podpis

Příklad:

  ```text
  example.i2p=b64dest#!sig=b64sig
  ```

#### Změna hostname
Předcházena example.i2p=b64dest
  ANO, to je nové jméno hostitele a staré cílové místo.
action
  changename
oldname
  staré hostname, bude nahrazeno
sig
  podpis

Příklad:

  ```text
  example.i2p=b64dest#!action=changename#oldname=oldhostname#sig=b64sig
  ```

#### Změna cílového místa
Předcházena example.i2p=b64dest
  ANO, to je staré jméno hostitele a nové cílové místo.
action
  changedest
olddest
  staré cílové místo, bude nahrazeno
oldsig
  podpis využívající olddest
sig
  podpis

Příklad:

  ```text
  example.i2p=b64dest#!action=changedest#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
  ```

#### Přidat alias hostname
Předcházena example.i2p=b64dest
  ANO, to je nové (alias) jméno hostitele a staré cílové místo.
action
  addname
oldname
  staré hostname
sig
  podpis

Příklad:

  ```text
  example.i2p=b64dest#!action=addname#oldname=oldhostname#sig=b64sig
  ```

#### Přidat alias cílového místa
(Používá se pro upgrade krypta)

Předcházena example.i2p=b64dest
  ANO, to je staré jméno hostitele a nové (alternativní) cílové místo.
action
  adddest
olddest
  staré cílové místo
oldsig
  podpis využívající olddest
sig
  podpis využívající dest

Příklad:

  ```text
  example.i2p=b64dest#!action=adddest#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
  ```

#### Přidat subdoménu
Předcházena subdomain.example.i2p=b64dest
  ANO, to je nové jméno hostitele subdomény a cílové místo.
action
  addsubdomain
oldname
  vyšší úroveň hostname (example.i2p)
olddest
  vyšší úroveň cílového místa (for example.i2p)
oldsig
  podpis využívající olddest
sig
  podpis využívající dest

Příklad:

  ```text
  subdomain.example.i2p=b64dest#!action=addsubdomain#oldname=example.i2p#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
  ```

#### Aktualizovat metadata
Předcházena example.i2p=b64dest
  ANO, to je staré jméno hostitele a cílové místo.
action
  update
sig
  podpis

(přidat jakékoliv aktualizované klíče zde)

Příklad:

  ```text
  example.i2p=b64dest#!action=update#k1=v1#k2=v2#sig=b64sig
  ```

#### Odstranit hostname
Předcházena example.i2p=b64dest
  NE, jsou specifikována v možnostech
action
  remove
name
  hostname
dest
  cílové místo
sig
  podpis

Příklad:

  ```text
  #!action=removeall#name=example.i2p#dest=b64destsig=b64sig
  ```

#### Odstranit vše s tímto cílovým místem
Předcházena example.i2p=b64dest
  NE, jsou specifikována v možnostech
action
  removeall
name
  staré hostname, pouze informativní
dest
  staré cílové místo, vše s tímto cílovým místem je odstraněno
sig
  podpis

Příklad:

  ```text
  #!action=removeall#name=example.i2p#dest=b64destsig=b64sig
  ```

### Podpisy

Všechny příkazy musí obsahovat klíč/hodnotu podpisu "sig=b64podpis", kde
podpis pro ostatní data používá podpisový klíč cílového místa.

Pro příkazy obsahující staré a nové cílové místo musí být zahrnut také
oldsig=b64podpis, a buď oldname, olddest, nebo obojí.

V příkazu Přidat nebo Změnit je veřejný klíč pro ověření ve
Cílovém místě, které má být přidáno nebo změněno.

V některých příkazech pro přidání nebo úpravu může být uvedeno další cílové místo,
například při přidávání aliasu nebo změně cílů nebo hostnamu. V tomto případě
musí být zahrnut druhý podpis a oba by měly být ověřeny. Druhý podpis je
"vnitřní" podpis a je podepsán a ověřen jako první (s vyloučením "vnějšího"
podpisu). Klient by měl podniknout jakékoliv další kroky nezbytné k ověření a
přijetí změn.

oldsig je vždy "vnitřní" podpis. Podepište a ověřte bez přítomnosti klíčů 'oldsig' nebo
'sig'. sig je vždy "vnější" podpis. Podepište a ověřte s klíčem 'oldsig'
přítomným, ale nikoli klíčem 'sig'.

#### Vstupy pro podpisy
Pro generování byte streamu k vytvoření nebo ověření podpisu serializujte
následujícím způsobem:

- Odstraňte klíč "sig"
- Pokud ověřujete pomocí oldsig, odstraňte také klíč "oldsig"
- Pouze pro příkazy Přidat nebo Změnit,
  výstup example.i2p=b64dest
- Pokud zůstávají nějaké klíče, výstup "#!"
- Seřaďte možnosti podle UTF-8 klíče, selžte, pokud jsou přítomné duplicitní klíče
- Pro každý klíč/hodnotu, výstup klíč=hodnota, následuje (pokud není poslední klíč/hodnota) 
  '#'

Poznámky

- Nevypisovat nový řádek
- Výstupní kódování je UTF-8
- Všechny kódování cílových míst a podpisů je v Base 64 s použitím I2P abecedy
- Klíče a hodnoty jsou citlivé na velikost písmen
- Hostnames musí být malými písmeny

## Kompatibilita

Všechny nové řádky ve formátu hosts.txt jsou implementovány pomocí úvodních
znaků komentáře, tedy všechny starší verze I2P budou nové příkazy
interpretovat jako komentáře.

Když se I2P routery aktualizují na novou specifikaci, nebudou znovu
interpretovat staré komentáře, ale začnou poslouchat nové příkazy v
následných načítáních jejich odběrových kanálů. Proto je důležité, aby
jmenné servery uchovaly příkazy nějakým způsobem, nebo umožnily podporu
etag, aby routery mohly načíst všechny minulé příkazy.
