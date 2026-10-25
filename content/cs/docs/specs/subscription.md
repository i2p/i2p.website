---
title: "Příkazy pro odběr kanálů adresáře"
description: "Specifikace pro rozšíření kanálu předplatného adres o příkazy umožňující jmenným serverům vysílat aktualizace záznamů od držitelů hostitelských jmen."
slug: "subscription"
aliases:
  - "/cs/docs/specs/subscription-spec"
  - "/cs/docs/specs/subscription-spec/"
category: "Formáty"
lastUpdated: "2021-01"
accurateFor: "0.9.49"
---

## Přehled

Tato specifikace rozšiřuje feed odběru adres o příkazy, aby umožnila jmenným serverům vysílat aktualizace záznamů od držitelů názvů hostitelů. Implementováno ve verzi 0.9.26, původně navrženo v návrhu 112.

## Motivace

Dříve servery pro odběr hosts.txt posílaly data pouze ve formátu hosts.txt, který vypadá následovně:

```
example.i2p=b64destination
```
S tím je několik problémů:

- Držitelé hostnames nemohou aktualizovat Destination asociovanou s jejich hostnames (například za účelem upgradu podpisového klíče na silnější typ).
- Držitelé hostnames nemohou libovolně vzdát svých hostnames; musí předat odpovídající soukromé klíče Destination přímo novému držiteli.
- Neexistuje způsob, jak autentifikovat, že subdoména je kontrolována odpovídajícím základním hostname; to je v současnosti vynucováno pouze individuálně některými name servery.

## Design

Tato specifikace přidává řadu příkazových řádků do formátu hosts.txt. Pomocí těchto příkazů mohou name servery rozšířit své služby o řadu dodatečných funkcí. Klienti, kteří implementují tuto specifikaci, budou schopni naslouchat těmto funkcím prostřednictvím běžného procesu odběru.

Všechny příkazové řádky musí být podepsány odpovídající Destination. To zajišťuje, že změny jsou prováděny pouze na žádost držitele názvu hostitele.

## Bezpečnostní důsledky

Tato specifikace neovlivňuje anonymitu.

Existuje zvýšené riziko spojené se ztrátou kontroly nad klíčem Destination, protože někdo, kdo jej získá, může použít tyto příkazy k provádění změn u jakýchkoli přidružených hostnames. Ale to není větší problém než současný stav, kdy někdo, kdo získá Destination, může předstírat hostname a (částečně) převzít jeho provoz. Zvýšené riziko je také vyváženo tím, že držitelům hostname dává možnost změnit Destination přidružený k hostname, v případě že se domnívají, že Destination byl kompromitován; to je s aktuálním systémem nemožné.

## Specifikace

### Nové typy řádků

Existují dva nové typy řádků:

1. Příkazy Add a Change:

   ```
   example.i2p=b64destination#!key1=val1#key2=val2 ...
   ```
2. Příkazy pro odebrání:

   ```
   #!key1=val1#key2=val2 ...
   ```
#### Řazení

Feed nemusí být nutně v pořadí nebo úplný. Například příkaz změny může být na řádku před příkazem přidání, nebo bez příkazu přidání.

Klíče mohou být v libovolném pořadí. Duplicitní klíče nejsou povoleny. Všechny klíče a hodnoty rozlišují velikost písmen.

### Běžné klíče

Vyžadováno ve všech příkazech:

**sig** : B64 podpis, používající podepisovací klíč z cíle

Odkazy na druhý hostname a/nebo cíl:

**oldname** : Druhý hostname (nový nebo změněný)

**olddest** : Druhá b64 destinace (nová nebo změněná)

**oldsig** : Druhý b64 podpis, používající podpisový klíč z olddest

Další běžné klíče:

**action** : Příkaz

**name** : Název hostitele, přítomen pouze pokud mu nepředchází `example.i2p=b64dest`

**dest** : B64 cíl, přítomen pouze pokud nepředchází `example.i2p=b64dest`

**date** : V sekundách od epochy

**expires** : V sekundách od epochy

### Příkazy

Všechny příkazy kromě příkazu "Add" musí obsahovat klíč/hodnotu `action=command`.

Z důvodu kompatibility se staršími klienty je většina příkazů předcházena `example.i2p=b64dest`, jak je uvedeno níže. U změn se jedná vždy o nové hodnoty. Jakékoli staré hodnoty jsou zahrnuty v sekci klíč/hodnota.

Uvedené klíče jsou povinné. Všechny příkazy mohou obsahovat další položky klíč/hodnota, které zde nejsou definovány.

#### Přidat název hostitele

**Předchází example.i2p=b64dest** : ANO, toto je nový název hostitele a cílová adresa.

**action** : NENÍ zahrnuto, je to implicitní.

**sig** : podpis

Příklad:

```
example.i2p=b64dest#!sig=b64sig
```
#### Změnit název hostitele

**Předchází example.i2p=b64dest** : ANO, toto je nový název hostitele a starý cíl.

**action** : changename

**oldname** : starý název hostitele, který má být nahrazen

**sig** : podpis

Příklad:

```
example.i2p=b64dest#!action=changename#oldname=oldhostname#sig=b64sig
```
#### Změnit cíl

**Předchází příklad.i2p=b64dest** : ANO, toto je starý název hostitele a nová destinace.

**action** : changedest

**olddest** : starý cíl, který má být nahrazen

**oldsig** : podpis používající olddest

**sig** : podpis

Příklad:

```
example.i2p=b64dest#!action=changedest#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
```
#### Přidat alias hostname

**Předchází example.i2p=b64dest** : ANO, toto je nový (alias) název hostitele a starý cíl.

**action** : addname

**oldname** : původní hostname

**sig** : podpis

Příklad:

```
example.i2p=b64dest#!action=addname#oldname=oldhostname#sig=b64sig
```
#### Přidat alias destinace

(Používá se pro upgrade kryptografie)

**Předchází example.i2p=b64dest** : ANO, toto je starý název hostitele a nová (alternativní) destinace.

**action** : adddest

**olddest** : starý cíl

**oldsig** : podpis používající olddest

**sig** : podpis pomocí dest

Příklad:

```
example.i2p=b64dest#!action=adddest#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
```
#### Přidat subdoménu

**Předchází subdomain.example.i2p=b64dest** : ANO, toto je nový název subdomény hostitele a cíl.

**action** : addsubdomain

**oldname** : hostname vyšší úrovně (example.i2p)

**olddest** : cíl vyšší úrovně (například example.i2p)

**oldsig** : podpis používající olddest

**sig** : podpis používající dest

Příklad:

```
subdomain.example.i2p=b64dest#!action=addsubdomain#oldname=example.i2p#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
```
#### Aktualizovat metadata

**Předchází příklad.i2p=b64dest** : ANO, toto je starý název hostitele a cíl.

**action** : update

**sig** : podpis

(zde přidejte všechny aktualizované klíče)

Příklad:

```
example.i2p=b64dest#!action=update#k1=v1#k2=v2#sig=b64sig
```
#### Odebrat hostname

**Předcházeno example.i2p=b64dest** : NE, tyto jsou specifikovány v možnostech

**action** : remove

**name** : název hostitele

**dest** : cíl

**sig** : podpis

Příklad:

```
#!action=remove#name=example.i2p#dest=b64dest#sig=b64sig
```
#### Odstranit vše s touto destinací

**Předchází example.i2p=b64dest** : NE, tyto jsou specifikovány v možnostech

**action** : removeall

**name** : starý název hostitele, pouze informativní

**dest** : stará dest, všechny s touto dest jsou odstraněny

**sig** : podpis

Příklad:

```
#!action=removeall#name=example.i2p#dest=b64dest#sig=b64sig
```
### Podpisy

Všechny příkazy musí obsahovat podpisový klíč/hodnotu `sig=b64signature`, kde podpis je pro ostatní data, používající podpisový klíč cílové destinace.

Pro příkazy zahrnující staré i nové cílové místo musí být také uvedeno `oldsig=b64signature` a buď oldname, olddest, nebo obojí.

V příkazu Add nebo Change je veřejný klíč pro ověření obsažen v Destination, které má být přidáno nebo změněno.

V některých příkazech pro přidání nebo úpravu může být odkazována další destination, například při přidávání aliasu nebo změně destination či názvu hostitele. V takovém případě musí být zahrnuta druhá signatura a obě by měly být ověřeny. Druhá signatura je "vnitřní" signatura a je podepsána a ověřena jako první (vyjma "vnější" signatury). Klient by měl podniknout veškeré další kroky nutné k ověření a přijetí změn.

oldsig je vždy "vnitřní" podpis. Podepisujte a ověřujte bez přítomnosti klíčů 'oldsig' nebo 'sig'. sig je vždy "vnější" podpis. Podepisujte a ověřujte s přítomným klíčem 'oldsig', ale bez klíče 'sig'.

#### Vstup pro podpisy

Pro generování bajtového proudu k vytvoření nebo ověření podpisu, serializujte následovně:

- Odeberte klíč "sig"
- Pokud ověřujete pomocí oldsig, odeberte také klíč "oldsig"
- Pouze pro příkazy Add nebo Change vypište `example.i2p=b64dest`
- Pokud zůstávají nějaké klíče, vypište `#!`
- Seřaďte možnosti podle UTF-8 klíče, selžete při duplicitních klíčích
- Pro každý klíč/hodnotu vypište `key=value`, následovaný (pokud to není poslední klíč/hodnota) znakem `#`

Poznámky:

- Nevypisuj nový řádek
- Výstupní kódování je UTF-8
- Všechno kódování destinací a podpisů je v Base 64 s použitím I2P abecedy
- Klíče a hodnoty rozlišují velká a malá písmena
- Názvy hostů musí být malými písmeny

## Kompatibilita

Všechny nové řádky ve formátu hosts.txt jsou implementovány pomocí úvodních komentářových znaků, takže všechny starší verze I2P budou nové příkazy interpretovat jako komentáře.

Když se I2P routery aktualizují na novou specifikaci, nebudou znovu interpretovat staré komentáře, ale začnou naslouchat novým příkazům v následných stahováních jejich odběrových feedů. Proto je důležité, aby name servery nějakým způsobem zachovávaly příkazové záznamy, nebo aby povolily podporu etagů, aby routery mohly stáhnout všechny minulé příkazy.
