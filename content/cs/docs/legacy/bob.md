---
title: "BOB – Basic Open Bridge (základní otevřený most)"
description: "Zastaralé API pro správu destinací (zastaralé)"
slug: "bob"
lastUpdated: "2025-05"
layout: "single"
reviewStatus: "needs-review"
---

> **Upozornění:** BOB (rozhraní Basic Open Bridge pro I2P) podporuje pouze zastaralý typ podpisu DSA-SHA1. Projekt Java I2P přestal dodávat BOB ve verzi **1.7.0 (2022-02)**; zůstává pouze na instalacích, které začínaly na verzi 1.6.1 nebo starší, a na některých sestaveních i2pd. Nové aplikace **musí** používat [SAM v3](/docs/api/samv3/).

## Jazykové vazby

- Go – [ccondom](https://bitbucket.org/kallevedin/ccondom)
- Python – [`i2py-bob`](http://git.repo.i2p/w/i2py-bob.git)
- Twisted – [`txi2p`](https://pypi.python.org/pypi/txi2p)
- C++ – [`bobcpp`](https://gitlab.com/rszibele/bobcpp)

## Poznámky k protokolu

- `KEYS` označuje destinaci v base64 (veřejné + soukromé klíče).  
- `KEY` je veřejný klíč v base64.  
- `ERROR` odpovědi mají tvar `ERROR <description>\n`.  
- `OK` značí dokončení příkazu; volitelná data následují na stejném řádku.  
- `DATA` řádky průběžně posílají dodatečný výstup před závěrečným `OK`.

Příkaz `help` je jedinou výjimkou: může nevrátit žádný výstup, aby signalizoval, že „takový příkaz neexistuje“.

## Banner při připojení

BOB používá řádky ASCII ukončené znakem nového řádku (LF nebo CRLF). Po navázání spojení odešle:

```
BOB <version>
OK
```
Aktuální verze: `00.00.10`. Starší sestavení používala hexadecimální číslice psané velkými písmeny a nestandardní číslování.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">BOB Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Router Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Notes</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">00.00.10</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.8</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Latest defined version</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">00.00.00 – 00.00.0F</td><td style="border:1px solid var(--color-border); padding:0.5rem;">—</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Development builds</td></tr>
  </tbody>
</table>
## Základní příkazy

> Pro úplné podrobnosti o příkazech se připojte pomocí `telnet localhost 2827` a spusťte `help`.

```
COMMAND     OPERAND                               RETURNS
help        [command]                             NOTHING | OK <info>
clear                                             ERROR | OK
getdest                                           ERROR | OK <KEY>
getkeys                                           ERROR | OK <KEYS>
getnick     <tunnelname>                          ERROR | OK
inhost      <hostname | IP>                       ERROR | OK
inport      <port>                                ERROR | OK
list                                              ERROR | DATA... + OK
lookup      <hostname>                            ERROR | OK <KEY>
nick        <friendlyname>                        ERROR | OK
outhost     <hostname | IP>                       ERROR | OK
outport     <port>                                ERROR | OK
quit                                              ERROR | OK
setkey      <base64 destination>                  ERROR | OK
start                                             ERROR | OK
status                                            ERROR | DATA... + OK
stop                                              ERROR | OK
```
## Přehled zastarání

- BOB nepodporuje moderní typy podpisů, šifrované LeaseSets ani funkce transportní vrstvy.
- Rozhraní API je zmrazené; žádné nové příkazy nebudou přidány.
- Aplikace, které se stále spoléhají na BOB, by měly co nejdříve migrovat na SAM v3.
