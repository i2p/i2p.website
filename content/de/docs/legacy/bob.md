---
title: "BOB – Basic Open Bridge (grundlegende offene Brücke)"
description: "Veraltete API für die Zielverwaltung (veraltet)"
slug: "bob"
lastUpdated: "2025-05"
layout: "single"
reviewStatus: "needs-review"
---

> **Warnung:** BOB unterstützt nur den veralteten DSA-SHA1-Signaturtyp. Java I2P liefert BOB seit **1.7.0 (2022-02)** nicht mehr mit; es ist nur noch auf Installationen vorhanden, die ursprünglich mit Version 1.6.1 oder älter eingerichtet wurden, sowie auf einigen i2pd-Builds. Neue Anwendungen **müssen** [SAM v3](/docs/api/samv3/) verwenden.

## Sprachanbindungen

- Go – [ccondom](https://bitbucket.org/kallevedin/ccondom)
- Python – [`i2py-bob`](http://git.repo.i2p/w/i2py-bob.git)
- Twisted – [`txi2p`](https://pypi.python.org/pypi/txi2p)
- C++ – [`bobcpp`](https://gitlab.com/rszibele/bobcpp)

## Hinweise zum Protokoll

- `KEYS` bezeichnet eine Base64-Destination (Zieladresse; öffentliche + private Schlüssel).  
- `KEY` ist ein öffentlicher Schlüssel in Base64.  
- Antworten mit `ERROR` haben die Form `ERROR <description>\n`.  
- `OK` zeigt den Abschluss des Befehls an; optionale Daten folgen in derselben Zeile.  
- `DATA`-Zeilen liefern zusätzliche Ausgabe vor einem abschließenden `OK`.

Der Befehl `help` ist die einzige Ausnahme: Er kann keine Ausgabe liefern, um „kein solcher Befehl“ zu signalisieren.

## Verbindungsbanner

BOB verwendet ASCII-Zeilen, die mit einem Zeilenumbruch enden (LF oder CRLF). Beim Verbindungsaufbau gibt es Folgendes aus:

```
BOB <version>
OK
```
Aktuelle Version: `00.00.10`. Frühere Builds verwendeten großgeschriebene Hexadezimalziffern und eine nicht standardkonforme Nummerierung.

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
## Kernbefehle

> Ausführliche Details zu den Befehlen erhalten Sie, indem Sie sich mit `telnet localhost 2827` verbinden und `help` ausführen.

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
## Übersicht der Abkündigungen

- BOB (älteres Bridge-API für I2P) unterstützt weder moderne Signaturtypen noch verschlüsselte LeaseSets noch Transportfunktionen.
- Die API ist eingefroren; es werden keine neuen Befehle mehr hinzugefügt.
- Anwendungen, die weiterhin auf BOB setzen, sollten so bald wie möglich auf SAM v3 migrieren.
