---
title: "API 2 I2PControl"
number: "118"
author: "hottuna"
created: "2016-01-23"
lastupdated: "2018-03-22"
status: "Zamítnuto"
thread: "http://zzz.i2p/topics/2030"
toc: true
---

## Přehled

Tento návrh popisuje API2 pro I2PControl.

Tento návrh byl zamítnut a nebude implementován, protože narušuje zpětnou kompatibilitu.
Podrobnosti naleznete v odkazu na diskuzní vlákno.

### Pozor vývojáři!

Všechny parametry RPC budou nyní psány malými písmeny. To *přeruší* zpětnou
kompatibilitu s implementacemi API1. Důvodem je poskytování
uživatelům >=API2 co nejjednodušší a nejkoherentnější možné API.


## Specifikace API 2

```json
{
    "id": "id",
    "method": "method_name",
    "params": {
      "token": "auth_token",
      "method_param": "method_parameter_value",
    },
    "jsonrpc": "2.0"
  }

  {
    "id": "id",
    "result": "result_value",
    "jsonrpc": "2.0"
  }
```

### Parametry

**`"id"`**

Číslo id nebo požadavek. Používá se k identifikaci, která odpověď byla vyvolána jakým požadavkem.

**`"method_name"`**

Název RPC, který je vyvolán.

**`"auth_token"`**

Autentizační token relace. Je potřeba ho dodat s každým RPC, kromě volání 'authenticate'.

**`"method_parameter_value"`**

Parametr metody. Používá se k nabídce různých variant metody. Jako 'get', 'set' a podobné varianty.

**`"result_value"`**

Hodnota, kterou RPC vrací. Její typ a obsah záleží na metodě a konkrétní metodě.


### Předpony

Pojmenovací schéma RPC je podobné jako v CSS, s předponami specifickými pro různé implementace API (i2p, kovri, i2pd):

```text
XXX.YYY.ZZZ
i2p.XXX.YYY.ZZZ
i2pd.XXX.YYY.ZZZ
kovri.XXX.YYY.ZZZ
```

Celkovým záměrem u předpon specifických pro prodejce je umožnit určitý pohyb
a umožnit implementacím inovovat, aniž by musely čekat, až všechny ostatní
implementace doženou. Pokud je RPC implementováno všemi implementacemi, jeho
mnohočetné předpony mohou být odstraněny a může být zahrnuto jako základní RPC v
další verzi API.


### Průvodce čtením metod

* **rpc.method**

   * *parameter* [typ parametru]:  [null], [number], [string], [boolean],
     [array] nebo [object]. [object] je mapa {key:value}.
  * Vrací:

```text
"return_value" [string] // Toto je hodnota vrácená voláním RPC
```


### Metody

* **authenticate** - Za předpokladu, že je poskytnuto správné heslo, tato metoda vám poskytne token pro další přístup a seznam podporovaných úrovní API.

  * *password* [string]:  Heslo pro tuto implementaci i2pcontrol

    Vrací:
```text
    [object]
    {
      "token" : [string], // Token, který má být dodán se všemi ostatními metodami RPC
      "api" : [[int],[int], ...]  // Seznam podporovaných úrovní API.
    }
```


* **control.** - Ovládání i2p

  * **control.reseed** - Spustit opětovné nasazování

    * [nil]: Není potřeba žádný parametr

    Vrací:
```text
      [nil]
```

  * **control.restart** - Restartovat instanci i2p

    * [nil]: Není potřeba žádný parametr

    Vrací:
```text
      [nil]
```

  * **control.restart.graceful** - Jemně restartovat instanci i2p

    * [nil]: Není potřeba žádný parametr

    Vrací:
```text
      [nil]
```

  * **control.shutdown** - Vypnout instanci i2p

    * [nil]: Není potřeba žádný parametr

    Vrací:
```text
      [nil]
```

  * **control.shutdown.graceful** - Jemně vypnout instanci i2p

    * [nil]: Není potřeba žádný parametr

    Vrací:
```text
      [nil]
```

  * **control.update.find** - **BLOKOVÁNÍ** Vyhledat podepsané aktualizace

    * [nil]: Není potřeba žádný parametr

    Vrací:
```text
      true [boolean] // Pravda, pokud je k dispozici podepsaná aktualizace
```

  * **control.update.start** - Spustit proces aktualizace

    * [nil]: Není potřeba žádný parametr

    Vrací:
```text
      [nil]
```


* **i2pcontrol.** - Konfigurace i2pcontrol

  * **i2pcontrol.address** - Získat/nastavit IP adresu, na které i2pcontrol naslouchá.

    * *get* [null]: Tento parametr nemusí být nastaven.

    Vrací:
```text
      "0.0.0.0" [string]
```

    * *set* [string]: Toto bude IP adresa jako "0.0.0.0" nebo "192.168.0.1"

    Vrací:
```text
      [nil]
```

  * **i2pcontrol.password** - Změnit heslo i2pcontrol.

    * *set* [string]: Nastavit nové heslo na tento řetězec

    Vrací:
```text
      [nil]
```

  * **i2pcontrol.port** - Získat/nastavit port, na kterém i2pcontrol naslouchá.

    * *get* [null]: Tento parametr nemusí být nastaven.

    Vrací:
```text
      7650 [number]
```

    * *set* [number]: Změnit port, na kterém i2pcontrol naslouchá, na tento port

    Vrací:
```text
      [nil]
```


* **settings.** - Získat/nastavit nastavení instance i2p

  * **settings.advanced** - Pokročilá nastavení

    * *get*  [string]: Získat hodnotu tohoto nastavení

    Vrací:
```text
      "setting-value" [string]
```

    * *getAll* [null]:

    Vrací:
```text
      [object]
      {
        "setting-name" : "setting-value", [string]
        ".." : ".."
      }
```

    * *set* [string]: Nastavit hodnotu tohoto nastavení
    * *setAll* [object] {"setting-name" : "setting-value", ".." : ".." }

    Vrací:
```text
      [nil]
```

  * **settings.bandwidth.in** - Nastavení příchozí šířky pásma
  * **settings.bandwidth.out** - Nastavení odchozí šířky pásma

    * *get* [nil]: Tento parametr nemusí být nastaven.

    Vrací:
```text
      0 [number]
```

    * *set* [number]: Nastavit limit šířky pásma

    Vrací:
```text
     [nil]
```

  * **settings.ntcp.autoip** - Získat nastavení automatické detekce IP pro NTCP

    * *get* [null]: Tento parametr nemusí být nastaven.

    Vrací:
```text
      true [boolean]
```

  * **settings.ntcp.hostname** - Získat hostitel NTCP

    * *get* [null]: Tento parametr nemusí být nastaven.

    Vrací:
```text
      "0.0.0.0" [string]
```

    * *set* [string]: Nastavit nového hostitele

    Vrací:
```text
      [nil]
```

  * **settings.ntcp.port** - NTCP port

    * *get* [null]: Tento parametr nemusí být nastaven.

    Vrací:
```text
      0 [number]
```

    * *set* [number]: Nastavit nový NTCP port.

    Vrací:
```text
      [nil]
```

    * *set* [boolean]: Nastavit automatickou detekci IP pro NTCP

    Vrací:
```text
      [nil]
```

  * **settings.ssu.autoip** - Konfigurace nastavení automatické detekce IP pro SSU

    * *get* [nil]: Tento parametr nemusí být nastaven.

    Vrací:
```text
      true [boolean]
```

  * **settings.ssu.hostname** - Konfigurace hostitele SSU

    * *get* [null]: Tento parametr nemusí být nastaven.

    Vrací:
```text
      "0.0.0.0" [string]
```

    * *set* [string]: Nastavit nového hostitele SSU

    Vrací:
```text
      [nil]
```

  * **settings.ssu.port** - SSU port

    * *get* [null]: Tento parametr nemusí být nastaven.

    Vrací:
```text
      0 [number]
```

    * *set* [number]: Nastavit nový SSU port.

    Vrací:
```text
      [nil]
```

    * *set* [boolean]: Nastavit automatickou detekci IP pro SSU

    Vrací:
```text
      [nil]
```

  * **settings.share** - Získat procentuální podíl šířky pásma

    * *get* [null]: Tento parametr nemusí být nastaven.

    Vrací:
```text
      0 [number] // Procentuální podíl šířky pásma (0-100)
```

    * *set* [number]: Nastavit procentuální podíl šířky pásma (0-100)

    Vrací:
```text
      [nil]
```

  * **settings.upnp** - Povolte nebo zakažte UPNP

    * *get* [nil]: Tento parametr nemusí být nastaven.

    Vrací:
```text
      true [boolean]
```

    * *set* [boolean]: Nastavit automatickou detekci IP pro SSU

    Vrací:
```text
      [nil]
```


* **stats.** - Získat statistiky z instance i2p

  * **stats.advanced** - Tato metoda poskytuje přístup ke všem statistikám vedeným v rámci instance.

    * *get* [string]:  Název pokročilé statistiky, kterou je třeba poskytnout
    * *Optional:* *period* [number]:  Období pro požadovanou statistiku

  * **stats.knownpeers** - Vrátí počet známých peerů
  * **stats.uptime** - Vrátí dobu v ms od doby, kdy byl router spuštěn
  * **stats.bandwidth.in** - Vrátí příchozí šířku pásma (ideálně za poslední sekundu)
  * **stats.bandwidth.in.total** - Vrátí počet přijatých bajtů od posledního restartu
  * **stats.bandwidth.out** - Vrátí odchozí šířku pásma (ideálně za poslední sekundu)'
  * **stats.bandwidth.out.total** - Vrátí počet odeslaných bajtů od posledního restartu'
  * **stats.tunnels.participating** - Vrátí počet tunelů, kterých se aktuálně účastníte
  * **stats.netdb.peers.active** - Vrátí počet peerů, s nimiž jsme nedávno komunikovali
  * **stats.netdb.peers.fast** - Vrátí počet 'rychlých' peerů
  * **stats.netdb.peers.highcapacity** - Vrátí počet peerů s 'vysokou kapacitou'
  * **stats.netdb.peers.known** - Vrátí počet známých peerů

    * *get* [null]: Tento parametr nemusí být nastaven.

    Vrací:
```text
      0.0 [number]
```


* **status.** - Získat stav instance i2p

  * **status.router** - Získat stav routeru

    * *get* [null]: Tento parametr nemusí být nastaven.

    Vrací:
```text
      "status" [string]
```

  * **status.net** - Získat stav routerové sítě

    * *get* [null]: Tento parametr nemusí být nastaven.

    Vrací:
```text
      0 [number]
      /**
       *    0 – OK
       *    1 – TESTING
       *    2 – FIREWALLED
       *    3 – HIDDEN
       *    4 – WARN_FIREWALLED_AND_FAST
       *    5 – WARN_FIREWALLED_AND_FLOODFILL
       *    6 – WARN_FIREWALLED_WITH_INBOUND_TCP
       *    7 – WARN_FIREWALLED_WITH_UDP_DISABLED
       *    8 – ERROR_I2CP
       *    9 – ERROR_CLOCK_SKEW
       *   10 – ERROR_PRIVATE_TCP_ADDRESS
       *   11 – ERROR_SYMMETRIC_NAT
       *   12 – ERROR_UDP_PORT_IN_USE
       *   13 – ERROR_NO_ACTIVE_PEERS_CHECK_CONNECTION_AND_FIREWALL
       *   14 – ERROR_UDP_DISABLED_AND_TCP_UNSET
       */
```

  * **status.isfloodfill** - Je tato instance i2p momentálně floodfill

    * *get* [null]: Tento parametr nemusí být nastaven.

    Vrací:
```text
      true [boolean]
```

  * **status.isreseeding** - Dochází u této instance i2p k opětovnému nasazování

    * *get* [null]: Tento parametr nemusí být nastaven.

    Vrací:
```text
      true [boolean]
```

  * **status.ip** - Veřejná IP zjištěná pro tuto instanci i2p

    * *get* [null]: Tento parametr nemusí být nastaven.

    Vrací:
```text
      "0.0.0.0" [string]
```
