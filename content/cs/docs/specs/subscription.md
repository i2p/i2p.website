---
title: "Příkazy pro kanál odběru adres"
description: "Rozšíření odběrových kanálů s adresami, které umožňuje držitelům názvů hostitelů aktualizovat a spravovat své záznamy"
slug: "subscription"
lastUpdated: "2025-10"
accurateFor: "I2P 2.10.0"
---

## Přehled

Tato specifikace rozšiřuje odběrný kanál adresáře o příkazy, které umožňují jmenným serverům distribuovat aktualizace záznamů od držitelů názvů hostitelů (hostname). Původně navržena v [Návrh 112](/proposals/112-addressbook-subscription-feed-commands/) (září 2014), implementována ve verzi 0.9.26 (červen 2016) a nasazena v celé síti se statusem CLOSED.

Systém zůstal stabilní a beze změn od své počáteční implementace a nadále funguje totožně v I2P 2.10.0 (Router API 0.9.65, září 2025).

## Motivace

Dříve servery pro odběr hosts.txt zasílaly data pouze v jednoduchém formátu hosts.txt:

```
example.i2p=b64destination
```
Tento základní formát způsobil několik problémů:

- Držitelé názvů hostitelů nemohou aktualizovat Destination (I2P cílový identifikátor) spojenou s jejich názvy hostitelů (například kvůli přechodu podpisového klíče na silnější kryptografický typ).
- Držitelé názvů hostitelů se nemohou svých názvů hostitelů libovolně vzdát. Odpovídající soukromé klíče Destination musí předat přímo novému držiteli.
- Neexistuje způsob, jak ověřit, že subdoména je spravována odpovídajícím základním názvem hostitele. To je v současnosti vynucováno pouze jednotlivě některými jmennými servery.

## Návrh

Tato specifikace přidává do formátu hosts.txt řádky s příkazy. Pomocí těchto příkazů mohou jmenné servery rozšířit své služby a poskytovat další funkce. Klienti, kteří tuto specifikaci implementují, mohou o těchto funkcích získávat informace prostřednictvím běžného procesu odběru.

Všechny příkazové řádky musí být podepsány příslušnou Destination (cílovou identitou v I2P). To zajišťuje, že změny jsou prováděny pouze na žádost držitele názvu hostitele.

## Bezpečnostní dopady

Tato specifikace nemá vliv na anonymitu.

Dochází ke zvýšení rizika spojeného se ztrátou kontroly nad Destination key (klíčem k Destination – identitě cílové služby v I2P), protože kdokoli, kdo jej získá, může pomocí těchto příkazů provádět změny u libovolných k němu přiřazených názvů hostitele. To však nepředstavuje větší problém než status quo, kdy někdo, kdo získá Destination, se může vydávat za název hostitele a (částečně) převzít jeho provoz. Zvýšené riziko je vyváženo tím, že držitelům názvů hostitele dává možnost změnit Destination přiřazenou k názvu hostitele v případě, že se domnívají, že Destination byla kompromitována. To je v současném systému nemožné.

## Specifikace

### Nové typy řádků

Existují dva nové typy řádků:

1. **Příkazy Add a Change:**

```
example.i2p=b64destination#!key1=val1#key2=val2...
```
2. **Odstranit příkazy:**

```
#!key1=val1#key2=val2...
```
#### Pořadí

Kanál nemusí být nutně seřazený ani úplný. Například příkaz change se může objevit na řádku před příkazem add, nebo i bez příkazu add.

Klíče mohou být v libovolném pořadí. Duplicitní klíče nejsou povoleny. Všechny klíče i hodnoty rozlišují velká a malá písmena.

### Obecné klíče

**Povinné u všech příkazů:**

**sig** : Podpis v Base64, s použitím podpisového klíče destination (cílová adresa)

**Odkazy na druhý název hostitele a/nebo destinaci:**

**oldname** : Druhý název hostitele (nový nebo změněný)

**olddest** : Druhá destinace v Base64 (nová nebo změněná)

**oldsig** : Druhý podpis v kódování Base64, s použitím podpisového klíče z olddest

**Další běžné klíče:**

**akce** : Příkaz

**name** : Název hostitele, uveden pouze pokud mu nepředchází `example.i2p=b64dest`

**dest** : Base64 Destination (cílová adresa v I2P), je přítomná pouze v případě, že jí nepředchází `example.i2p=b64dest`

**date** : V sekundách od epochy

**expires** : V sekundách od epochy

### Příkazy

Všechny příkazy kromě příkazu "Add" musí obsahovat dvojici klíč/hodnota `action=command`.

Pro kompatibilitu se staršími klienty je většině příkazů předřazeno `example.i2p=b64dest`, jak je uvedeno níže. U změn jde vždy o nové hodnoty. Případné staré hodnoty jsou zahrnuty v sekci klíč/hodnota.

Uvedené klíče jsou povinné. Všechny příkazy mohou obsahovat další položky klíč/hodnota, které zde nejsou definovány.

#### Přidat název hostitele

**Předcházeno řetězcem example.i2p=b64dest** : ANO, toto je nový název hostitele a cíl.

**akce** : NENÍ zahrnuta, je implicitní.

**sig** : podpis

Příklad:

```
example.i2p=b64dest#!sig=b64sig
```
#### Změnit název hostitele

**Předchází example.i2p=b64dest** : ANO, jde o nový název hostitele a starou destinaci.

**action** : changename

**oldname** : starý název hostitele, který má být nahrazen

**sig** : podpis

Příklad:

```
example.i2p=b64dest#!action=changename#oldname=oldhostname#sig=b64sig
```
#### Změnit cíl

**Předchází example.i2p=b64dest** : ANO, toto je starý název hostitele a nový destination (cílový identifikátor).

**akce** : changedest

**olddest** : původní destinace, která má být nahrazena

**oldsig** : podpis pomocí olddest

**sig** : podpis

Příklad:

```
example.i2p=b64dest#!action=changedest#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
```
#### Přidat alias hostitele

**Předchází example.i2p=b64dest** : ANO, toto je nový (alias) název hostitele a stará destinace.

**akce** : addname

**oldname** : původní název hostitele

**sig** : podpis

Příklad:

```
example.i2p=b64dest#!action=addname#oldname=oldhostname#sig=b64sig
```
#### Přidat alias cíle

(Použito pro kryptografickou aktualizaci)

**Uvedeno ve tvaru example.i2p=b64dest** : ANO, toto je starý název hostitele a nová (alternativní) cílová adresa.

**action** : adddest

**olddest** : předchozí destinace

**oldsig** : podpis vytvořený pomocí olddest

**sig** : podpis pomocí dest

Příklad:

```
example.i2p=b64dest#!action=adddest#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
```
#### Přidat subdoménu

**Uvozeno subdomain.example.i2p=b64dest** : ANO, toto je nový název subdomény a destinace.

**akce** : addsubdomain

**oldname** : název hostitele vyšší úrovně (example.i2p)

**olddest** : nadřazený cíl (například example.i2p)

**oldsig** : podpis s použitím olddest

**sig** : podpis s použitím dest

Příklad:

```
subdomain.example.i2p=b64dest#!action=addsubdomain#oldname=example.i2p#olddest=oldb64dest#oldsig=b64sig#sig=b64sig
```
#### Aktualizovat metadata

**Předcházeno řetězcem example.i2p=b64dest** : ANO, toto je původní název hostitele a destination (cílový identifikátor).

**akce** : aktualizace

**sig** : podpis

(zde přidejte všechny aktualizované klíče)

Příklad:

```
example.i2p=b64dest#!action=update#k1=v1#k2=v2#sig=b64sig
```
#### Odstranit název hostitele

**Předcházeno řetězcem example.i2p=b64dest** : NE, to se uvádí v možnostech

**akce** : odstranit

**name** : název hostitele

**dest** : cíl

**sig** : podpis

Příklad:

```
#!action=remove#name=example.i2p#dest=b64dest#sig=b64sig
```
#### Odstranit vše s touto destinací

**S předponou example.i2p=b64dest** : NE, tyto se zadávají v parametrech

**akce** : removeall

**dest** : cíl

**sig** : podpis

Příklad:

```
#!action=removeall#dest=b64dest#sig=b64sig
```
### Podpisy

Všechny příkazy musí být podepsány odpovídající Destination (cílovou identitou v I2P). Příkazy se dvěma cíli mohou vyžadovat dva podpisy.

`oldsig` je vždy "vnitřní" podpis. Podepisujte a ověřujte bez přítomnosti klíčů `oldsig` a `sig`. `sig` je vždy "vnější" podpis. Podepisujte a ověřujte s přítomným klíčem `oldsig`, ale bez klíče `sig`.

#### Vstup pro podpisy

Chcete‑li vygenerovat bajtový proud pro vytvoření nebo ověření podpisu, serializujte následovně:

1. Odstraňte klíč `sig`
2. Pokud ověřujete pomocí `oldsig`, odstraňte také klíč `oldsig`
3. Pouze pro příkazy Add nebo Change vypište `example.i2p=b64dest`
4. Pokud nějaké klíče zbývají, vypište `#!`
5. Seřaďte volby podle klíče v UTF-8, pokud se vyskytnou duplicitní klíče, skončete chybou
6. Pro každý pár klíč/hodnota vypište `key=value`, následovaný (pokud nejde o poslední pár klíč/hodnota) znakem `#`

**Poznámky**

- Nevypisujte znak nového řádku
- Kódování výstupu je UTF-8
- Veškeré kódování destination (cílové identity) a podpisu je v Base 64 s použitím abecedy I2P
- Klíče a hodnoty rozlišují velká a malá písmena
- Názvy hostitelů musí být psány malými písmeny

#### Aktuální typy podpisů

Od verze I2P 2.10.0 jsou pro destinace podporovány následující typy podpisů:

- **EdDSA_SHA512_Ed25519** (Typ 7): Nejběžnější pro destinace od verze 0.9.15. Používá veřejný klíč o délce 32 bajtů a podpis o délce 64 bajtů. Toto je doporučený typ podpisu pro nové destinace.
- **RedDSA_SHA512_Ed25519** (Typ 13): Dostupné pouze pro destinace a šifrované leaseSety (sada pronájmů) (od 0.9.39).
- Starší typy (DSA_SHA1, varianty ECDSA): Stále podporované, ale od 0.9.58 označené jako zastaralé pro nové identity routeru.

Poznámka: Postkvantové kryptografické možnosti jsou k dispozici od verze I2P 2.10.0, ale zatím nejsou výchozími typy podpisů.

## Kompatibilita

Všechny nové řádky ve formátu hosts.txt jsou implementovány pomocí počátečních znaků komentáře (`#!`), takže všechny starší verze I2P budou nové příkazy interpretovat jako komentáře a bez problémů je budou ignorovat.

Když se I2P routers aktualizují na novou specifikaci, nebudou znovu interpretovat staré komentáře, ale při následných načteních jejich odběrových kanálů začnou přijímat nové příkazy. Proto je důležité, aby jmenné servery nějakým způsobem trvale uchovávaly záznamy příkazů, nebo aby povolily podporu ETag (HTTP identifikátor entity), aby si routers mohly načíst všechny dřívější příkazy.

## Stav implementace

**Počáteční nasazení:** Verze 0.9.26 (7. června 2016)

**Aktuální stav:** Stabilní a beze změn až do verze I2P 2.10.0 včetně (Router API 0.9.65, září 2025)

**Stav návrhu:** UZAVŘENO (úspěšně nasazeno napříč sítí)

**Umístění implementace:** `apps/addressbook/java/src/net/i2p/addressbook/` v I2P Java routeru

**Klíčové třídy:** - `SubscriptionList.java`: Spravuje zpracování odběrů - `Subscription.java`: Obsluhuje jednotlivé kanály odběrů - `AddressBook.java`: Základní funkcionalita adresáře - `Daemon.java`: Služba adresáře běžící na pozadí

**Výchozí URL odběru:** `http://i2p-projekt.i2p/hosts.txt`

## Podrobnosti o přenosu

Odběry používají HTTP s podporou podmíněného GET:

- **Hlavička ETag:** Podporuje efektivní detekci změn
- **Hlavička Last-Modified:** Sleduje časy aktualizací odběru
- **304 Not Modified:** Servery by měly vracet tento kód, když se obsah nezměnil
- **Content-Length:** Důrazně doporučeno pro všechny odpovědi

I2P router používá standardní chování klienta HTTP se správnou podporou ukládání do mezipaměti.

## Kontext verze

**Poznámka k verzování I2P:** Přibližně od verze 1.5.0 (srpen 2021) přešlo I2P z verzování 0.9.x na sémantické verzování (1.x, 2.x atd.). Interní verze Router API však nadále používá číslování 0.9.x kvůli zpětné kompatibilitě. K říjnu 2025 je aktuálním vydáním I2P 2.10.0 s verzí Router API 0.9.65.

Tento specifikační dokument byl původně napsán pro verzi 0.9.49 (únor 2021) a zůstává plně aktuální i pro současnou verzi 0.9.65 (I2P 2.10.0), protože systém odběru informačních kanálů neprošel od své původní implementace ve verzi 0.9.26 žádnými změnami.

## Reference

- [Návrh 112 (původní)](/proposals/112-addressbook-subscription-feed-commands/)
- [Oficiální specifikace](/docs/specs/subscription/)
- [Dokumentace k pojmenování v I2P](/docs/overview/naming/)
- [Specifikace společných struktur](/docs/specs/common-structures/)
- [Repozitář zdrojových kódů I2P](https://github.com/i2p/i2p.i2p)
- [Gitea repozitář I2P](https://i2pgit.org/I2P_Developers/i2p.i2p)

## Související vývoj

Ačkoli se samotný systém odběrových kanálů nezměnil, následující související novinky v jmenné infrastruktuře I2P by vás mohly zajímat:

- **Rozšířené názvy Base32** (0.9.40+): Podpora pro base32 adresy o délce 56+ znaků pro šifrované leaseSet. Neovlivňuje formát odběrového kanálu.
- **Registrace TLD .i2p.alt** (RFC 9476, koncem roku 2023): Oficiální registrace .i2p.alt u GANA jako alternativní TLD. Budoucí aktualizace routeru mohou odstranit sufix .alt, ale nejsou vyžadovány žádné změny příkazů odběru.
- **Postkvantová kryptografie** (2.10.0+): K dispozici, ale není výchozí. Do budoucna se zvažuje pro podpisové algoritmy v odběrových kanálech.
