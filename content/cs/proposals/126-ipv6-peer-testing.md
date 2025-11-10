---
title: "Testování IPv6 Peer"
number: "126"
author: "zzz"
created: "2016-05-02"
lastupdated: "2018-03-19"
status: "Closed"
thread: "http://zzz.i2p/topics/2119"
target: "0.9.27"
implementedin: "0.9.27"
---

## Přehled

Tento dokument navrhuje implementaci SSU Peer Testování pro IPv6.
Implementováno v 0.9.27.


## Motivace

Nemůžeme spolehlivě určit a sledovat, zda je naše IPv6 adresa za firewallem.

Když jsme před lety přidali podporu IPv6, předpokládali jsme, že IPv6 nikdy není za firewallem.

Nedávno, v 0.9.20 (květen 2015), jsme interně rozdělili status dostupnosti v4/v6 (ticket #1458).
Viz tento ticket pro rozsáhlé informace a odkazy.

Pokud máte jak v4, tak v6 za firewallem, můžete jednoduše vynutit stav za firewallem v sekci konfigurace TCP na /confignet.

Nemáme peer testování pro v6. To je zakázáno ve specifikaci SSU.
Pokud nemůžeme pravidelně testovat dosažitelnost v6, nemůžeme rozumně přecházet mezi dosažitelným a nedosažitelným stavem v6.
Zůstává nám hádat, že jsme dosažitelní, pokud dostaneme příchozí spojení,
a hádat, že nejsme dosažitelní, pokud jsme delší dobu nedostali žádné příchozí spojení.
Problém je, že jakmile prohlásíme nedosažitelnost, nepublikujeme naši v6 IP,
a pak nedostaneme žádné další (po expiraci RI v netdb všech).

## Návrh

Implementovat Peer Testování pro IPv6
odstraněním předchozích omezení, že peer testování bylo povoleno pouze pro IPv4.
Testovací zpráva peeru už má pole pro délku IP.


## Specifikace

V sekci Schopnosti přehledu SSU proveďte následující doplnění:

Do verze 0.9.26 nebylo peer testování podporováno pro IPv6 adresy a
schopnost 'B', pokud byla přítomna pro IPv6 adresu, musela být ignorována.
Od verze 0.9.27 je peer testování podporováno pro IPv6 adresy a
přítomnost nebo nepřítomnost schopnosti 'B' v IPv6 adrese
naznačuje skutečnou podporu (nebo její nedostatek).

V sekcích Peer Testování přehledu SSU a specifikace SSU proveďte následující změny:

Poznámky k IPv6:
Do vydání 0.9.26 je podporováno pouze testování IPv4 adres.
Proto veškerá komunikace Alice-Bob a Alice-Charlie musí probíhat přes IPv4.
Komunikace Bob-Charlie však může probíhat přes IPv4 nebo IPv6.
Adresa Alice, když je specifikována ve zprávě PeerTest, musí být 4 byty.
Od vydání 0.9.27 je podporováno testování IPv6 adres a komunikace Alice-Bob a Alice-Charlie může probíhat přes IPv6,
pokud Bob a Charlie naznačují podporu schopností 'B' ve své publikované IPv6 adrese.

Alice pošle požadavek Bobovi pomocí existujícího spojení přes transport (IPv4 nebo IPv6), který chce testovat.
Když Bob obdrží požadavek od Alice přes IPv4, Bob musí vybrat Charlieho, který inzeruje adresu IPv4.
Když Bob obdrží požadavek od Alice přes IPv6, Bob musí vybrat Charlieho, který inzeruje adresu IPv6.
Skutečná komunikace Bob-Charlie může probíhat přes IPv4 nebo IPv6 (tj. nezávisle na typu adresy Alice).

## Migrace

Routery mohou buď:

1) Nezvýšit svou verzi na 0.9.27 nebo vyšší

2) Odstranit schopnost 'B' z jakýchkoli publikovaných IPv6 SSU adres

3) Implementovat IPv6 peer testování
