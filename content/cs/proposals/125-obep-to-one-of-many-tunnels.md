---
title: "Dodání OBEP do 1-z-N nebo N-z-N tunelů"
number: "125"
author: "zzz, str4d"
created: "2016-03-10"
lastupdated: "2017-04-07"
status: "Otevřeno"
thread: "http://zzz.i2p/topics/2099"
toc: true
---

## Přehled

Tento návrh pokrývá dvě zlepšení pro zlepšení výkonu sítě:

- Delegovat výběr IBGW OSBEP tím, že mu poskytneme seznam
  alternativ namísto jedné možnosti.

- Umožnit směrování vícesměrových paketů na OSBEP.


## Motivace

V případě přímého připojení je cílem snížit přetížení připojení tím,
že OSBEP poskytne flexibilitu v tom, jak se připojuje k IBGW. Schopnost specifikovat
více tunelů nám také umožňuje implementovat vícesměrové vysílání na OSBEP (tím,
že zprávu doručíme do všech specifikovaných tunelů).

Alternativou k delegační části tohoto návrhu by bylo odeslat přes
haš [LeaseSet](http://localhost:63465/docs/specs/common-structures/#leaseset), podobně jako stávající schopnost specifikovat haš cílové
[RouterIdentity](http://localhost:63465/docs/specs/common-structures/#common-structure-specification). To by mělo za následek menší zprávu a potenciálně
novější LeaseSet. Nicméně:

1. To by nutilo OSBEP provést vyhledávání

2. LeaseSet nemusí být publikován do floodfillu, takže vyhledávání by selhalo.

3. LeaseSet může být zašifrován, takže OSBEP nemůže získat lease.

4. Specifikace LeaseSetu odhaluje OSBEP [Destination](/docs/specs/common-structures/#destination) zprávy,
   kterou by jinak mohli objevit pouze procházením všech LeaseSetů v síti a
   hledáním odpovídajícího Lease.


## Návrh

Odesílatel (OBGW) by umístil některé (všechny?) z cílových [Leases](http://localhost:63465/docs/specs/common-structures/#lease)
do doručovacích pokynů [TUNNEL-DELIVERY](/docs/specs/i2np/#tunnel-message-delivery-instructions) namísto výběru pouze jednoho.

OSBEP by vybral jeden z těchto tunelů pro doručení. OSBEP by vybral, pokud
je dostupný, ten, ke kterému je již připojen, nebo o kterém již ví. To by
způsobilo, že cesta OBEP-IBGW by byla rychlejší a spolehlivější a snížila by
celková síťová připojení.

Máme jeden nevyužitý typ doručení (0x03) a dva zbývající bity (0 a 1) ve
stavu pro [TUNNEL-DELIVERY](/docs/specs/i2np/#tunnel-message-delivery-instructions), které můžeme využít k implementaci těchto funkcí.


## Bezpečnostní důsledky

Tento návrh nemění množství informací unikajících o cílové destinaci OBGW nebo
jejich pohledu na NetDB:

- Protivník, který kontroluje OBEP a sbírá LeaseSety z NetDB, již může
  určit, zda je zpráva odesílána na konkrétní destinaci, hledáním páru
  [TunnelId](http://localhost:63465/docs/specs/common-structures/#tunnelid) / [RouterIdentity](http://localhost:63465/docs/specs/common-structures/#common-structure-specification). V nejhorším případě by přítomnost více
  Lease v TMDI mohla zrychlit hledání shody v databázi protivníka.

- Protivník, který provozuje škodlivou destinaci, již může získat informace
  o pohledu připojující oběti na NetDB, publikováním LeaseSetů, které
  obsahují různé příchozí tunely na různé floodfille, a pozorováním, kterými
  tunely se OBGW připojuje. Z jejich pohledu je výběr tunelu, který OBEP
  použije, funkčně totožný s výběrem, který provádí OBGW.

Vícesměrová vlajka odhaluje fakt, že OBGW provádí vícesměrové vysílání na OBEPs.
To vytváří obchod mezi výkonem a soukromím, který by měl být zvážen při
implementaci vyšších protokolů. Jako volitelná vlajka, uživatelé mohou udělat
vhodné rozhodnutí pro svou aplikaci. Mohou být výhody, kdyby toto bylo výchozí
chování pro kompatibilní aplikace, protože široké používání různými aplikacemi
by snížilo únik informací o tom, z které konkrétní aplikace je zpráva.


## Specifikace

Pokyny pro doručení prvního fragmentu [TUNNEL-DELIVERY](/docs/specs/i2np/#tunnel-message-delivery-instructions) by byly upraveny
následovně:

```
+----+----+----+----+----+----+----+----+
|flag|  ID tunelu (volitelný)  |              |
+----+----+----+----+----+              +
|                                       |
+                                       +
|         Na Hash (volitelný)            |
+                                       +
|                                       |
+                        +----+----+----+
|                        |dly | Zpráva  
+----+----+----+----+----+----+----+----+
 ID (volitelný) |rozšířené možnosti (volitelný)|cnt | (o)
+----+----+----+----+----+----+----+----+
 ID tunelu N   |                        |
+----+----+----+                        +
|                                       |
+                                       +
|         Na Hash N (volitelný)          |
+                                       +
|                                       |
+              +----+----+----+----+----+
|              | ID tunelu N+1 (o) |    |
+----+----+----+----+----+----+    +
|                                       |
+                                       +
|         Na Hash N+1 (volitelný)        |
+                                       +
|                                       |
+                                  +----+
|                                  | roz
+----+----+----+----+----+----+----+----+
     |
+----+

vlajka ::
       1 byte
       Pořadí bitů: 76543210
       bity 6-5: typ doručení
                 0x03 = TUNELE
       bit 0: vícesměrové? Pokud 0, doručit do jednoho z tunelů
                         Pokud 1, doručit do všech tunelů
                         Nastavit na 0 pro kompatibilitu s budoucími použitími,
                         pokud typ doručení není TUNELE

Počet ::
       1 byte
       Volitelné, přítomné pokud je typ doručení TUNELE
       2-255 - Počet následujících párů id/hash

ID tunelu :: `TunnelId`
Na Hash ::
       36 byte každý
       Volitelný, přítomný pokud je typ doručení TUNELE
       páry id/hash

Celková délka: Typická délka je:
       75 byte pro doručení se dvěma TUNELE (nerozdělená tunelová zpráva);
       79 byte pro doručení se dvěma TUNELE (první fragment)

Zbytek doručovacích pokynů nezměněn
```


## Kompatibilita

Jedinými partnery, kteří potřebují rozumět nové specifikaci, jsou OBGWs
a OBEPs. Proto můžeme tuto změnu učinit kompatibilní se stávající sítí tím,
že její použití bude podmíněno cílovou verzí I2P [VERSIONS](/docs/specs/i2np/#protocol-versions):

* OBGWs musí vybrat kompatibilní OBEPs při budování výstupních tunelů,
  na základě verze I2P inzerované v jejich [RouterInfo](http://localhost:63465/docs/specs/common-structures/#routerinfo).

* Partneři, kteří inzerují cílovou verzi, musí podporovat parsování nových
  vlajek a nesmí odmítat pokyny jako neplatné.

