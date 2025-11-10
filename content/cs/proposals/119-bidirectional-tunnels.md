---
title: "Obousměrné tunely"
number: "119"
author: "orignal"
created: "2016-01-07"
lastupdated: "2016-01-07"
status: "Needs-Research"
thread: "http://zzz.i2p/topics/2041"
---

## Přehled

Tento návrh se týká implementace obousměrných tunelů v I2P.


## Motivace

i2pd hodlá zavést obousměrné tunely, které budou prozatím budovány pouze přes jiné směrovače i2pd. Pro síť se budou jevit jako běžné vstupní a výstupní tunely.


## Návrh

### Cíle

1. Snížit využití sítě a CPU snížením počtu zpráv TunnelBuild
2. Schopnost okamžitě zjistit, zda účastník odešel.
3. Přesnější profilování a statistiky
4. Použití jiných darknetů jako mezilehlých peerů


### Úpravy tunelů

TunnelBuild
```````````
Tunely jsou budovány stejným způsobem jako vstupní tunely. Není vyžadována žádná odpověď. Existuje speciální typ účastníka nazývaný "entrance" označený vlajkou, který slouží jako IBGW a OBEP současně. Zpráva má stejný formát jako VaribaleTunnelBuild, ale ClearText obsahuje různá pole::

    in_tunnel_id
    out_tunnel_id
    in_next_tunnel_id
    out_next_tunnel_id
    in_next_ident
    out_next_ident
    layer_key, iv_key

Bude také obsahovat pole zmiňující, k jakému darknetu patří další peer, a nějaké dodatečné informace, pokud to není I2P.

TunnelTermination
`````````````````
Pokud chce peer odejít, vytvoří zprávy TunnelTermination, zašifruje je s pomocí klíče vrstvy a odešle ve směru "in". Pokud účastník obdrží takovou zprávu, znovu ji zašifruje svým klíčem vrstvy a odešle dalšímu peerovi. Jakmile zpráva dosáhne majitele tunelu, začne ji dešifrovat peer po peeru, dokud se nedostane k nezašifrované zprávě. Zjistí, který peer odešel, a ukončí tunel.
