---
title: "Výkon"
description: "Výkon I2P sítě: rychlost, připojení a správa zdrojů"
slug: "performance"
aliases:
  - "/cs/about/performance/future"
  - "/cs/about/performance/future/"
  - "/cs/about/performance/history"
  - "/cs/about/performance/history/"
  - "/cs/performance"
  - "/cs/performance/"
  - "/cs/performance-history"
  - "/cs/performance-history/"
  - "/cs/benchmarks"
  - "/cs/benchmarks/"
lastUpdated: "2025-01"
accurateFor: "0.9.65"
---

## Výkon I2P sítě: Rychlost, připojení a správa zdrojů

Síť I2P je plně dynamická. Každý klient je znám ostatním uzlům a testuje lokálně známé uzly z hlediska dostupnosti a kapacity. Do lokální NetDB jsou ukládány pouze dostupné a schopné uzly. Během procesu budování tunelů jsou z tohoto fondu vybírány nejlepší zdroje pro stavbu tunelů. Protože testování probíhá nepřetržitě, fond uzlů se mění. Každý I2P uzel zná jinou část NetDB, což znamená, že každý router má odlišnou sadu I2P uzlů, které lze použít pro tunely. I když mají dva routery stejnou podmnožinu známých uzlů, testy dostupnosti a kapacity pravděpodobně ukáží odlišné výsledky, protože ostatní routery mohou být zatížené právě ve chvíli, kdy jeden router testuje, ale být volné, když testuje druhý router.

To vysvětluje, proč má každý I2P uzel různé uzly pro stavbu tunelů. Protože má každý I2P uzel odlišnou latenci a šířku pásma, tunely (které jsou stavěny přes tyto uzly) mají různé hodnoty latence a šířky pásma. A protože má každý I2P uzel postavené jiné tunely, žádné dva I2P uzly nemají stejné sady tunelů.

Server/klient je známý jako "destination" (cíl) a každý destination má alespoň jeden příchozí a jeden odchozí tunnel. Výchozí nastavení je 3 skoky na tunnel. To dává celkem 12 skoků (tedy 12 různých I2P uzlů) pro úplnou cestu tam a zpět klient-server-klient.

Každý datový balíček je odeslán přes 6 dalších I2P uzlů, než dosáhne serveru:

```
client - hop1 - hop2 - hop3 - hopa1 - hopa2 - hopa3 - server
```
a na zpáteční cestě 6 různých I2P uzlů:

```
server - hopb1 - hopb2 - hopb3 - hopc1 - hopc2 - hopc3 - client
```
Provoz v síti potřebuje potvrzení (ACK) před odesláním nových dat, musí čekat, dokud se ACK nevrátí ze serveru: odeslat data, čekat na ACK, odeslat více dat, čekat na ACK. Jelikož se RTT (doba odezvy) skládá z latence každého jednotlivého I2P uzlu a každého spojení na této cestě tam a zpět, obvykle trvá 1-3 sekundy, než se ACK vrátí ke klientovi. Kvůli návrhu TCP a I2P transportu má datový paket omezenou velikost. Tyto podmínky společně stanovují limit maximální šířky pásma na tunnel 20-50 kbyte/sec. Pokud však POUZE JEDEN skok v tunnel má k dispozici pouze 5 kb/sec šířky pásma, celý tunnel je omezen na 5 kb/sec, nezávisle na latenci a dalších omezeních.

Šifrování, latence a způsob, jakým se tunnel staví, činí jeho výstavbu velmi náročnou z hlediska času procesoru. Proto může mít destinace maximálně 6 IN a 6 OUT tunnelů pro přenos dat. S maximálně 50 kb/sec na tunnel by destinace mohla celkově využívat přibližně 300 kb/sec provozu (ve skutečnosti to může být více při použití kratších tunnelů s nízkou nebo žádnou anonymitou). Používané tunnely se zahodí každých 10 minut a vystaví se nové. Tato změna tunnelů a někdy klienti, kteří se vypnou nebo ztratí připojení k síti, občas rozbijí tunnely a spojení. Příklad tohoto chování lze vidět na IRC2P síti při ztrátě spojení (ping timeout) nebo při používání eepget.

S omezenou sadou cílů a omezenou sadou tunelů na jeden cíl používá jeden I2P uzel pouze omezenou sadu tunelů napříč ostatními I2P uzly. Například pokud je I2P uzel "hop1" v malém příkladu výše, vidíme pouze 1 účastnický tunel pocházející z klienta. Pokud sečteme celou I2P síť, pouze poměrně omezený počet účastnických tunelů by mohl být vybudován s omezeným množstvím celkové šířky pásma. Když se tyto omezené počty rozdělí mezi počet I2P uzlů, je k dispozici pouze zlomek dostupné šířky pásma/kapacity.

Pro zachování anonymity by neměl být jeden router používán celou sítí pro budování tunelů. Pokud jeden router skutečně funguje jako tunnel router pro VŠECHNY I2P uzly, stává se velmi reálným centrálním bodem selhání a také centrálním bodem pro shromažďování IP adres a dat od klientů. Proto síť distribuuje provoz napříč uzly v procesu budování tunelů.

Dalším aspektem výkonu je způsob, jakým I2P zpracovává mesh síť. Každý hop-hop spoj využívá jedno TCP nebo UDP spojení na I2P uzlech. S 1000 spojeními vidí uživatel 1000 TCP spojení. To je poměrně hodně a některé domácí a malé kancelářské routery povolují pouze malý počet spojení. I2P se snaží omezit tato spojení pod 1500 pro každý typ UDP a TCP. To také omezuje množství provozu směrovaného přes I2P uzel.

Pokud je uzel dostupný a má nastavení šířky pásma >128 kB/s sdílené a je dostupný 24/7, měl by být po určité době používán pro účastnický provoz. Pokud se mezitím odpojí, testování I2P uzlu prováděné jinými uzly jim oznámí, že není dostupný. To zablokuje uzel na ostatních uzlech minimálně na 24 hodin. Takže ostatní uzly, které testovaly tento uzel jako nedostupný, nebudou tento uzel používat po dobu 24 hodin pro budování tunelů. Proto je váš provoz nižší po restartu/vypnutí vašeho I2P routeru minimálně po dobu 24 hodin.

Navíc ostatní I2P uzly potřebují znát I2P router, aby ho mohly testovat z hlediska dosažitelnosti a kapacity. Tento proces lze urychlit, když interagujete se sítí, například používáním aplikací nebo návštěvou I2P stránek, což povede k většímu budování tunnelů a tím i k větší aktivitě a dosažitelnosti pro testování uzly v síti.

---

## Zlepšení výkonu

Pro možná budoucí vylepšení výkonu viz [Budoucí vylepšení výkonu](/docs/overview/performance#future).

Pro minulá vylepšení výkonu viz [Historie výkonu](/docs/overview/performance#history).
