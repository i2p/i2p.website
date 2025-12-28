---
title: "BOB – Passerelle ouverte de base"
description: "API dépréciée pour la gestion des destinations (dépréciée)"
slug: "bob"
lastUpdated: "2025-05"
layout: "single"
reviewStatus: "needs-review"
---

> **Avertissement :** BOB ne prend en charge que l’ancien type de signature DSA-SHA1. Java I2P a cessé d’inclure BOB à partir de la **1.7.0 (2022-02)**; il ne subsiste que sur les installations démarrées avec la 1.6.1 ou une version antérieure et sur certaines builds d’i2pd. Les nouvelles applications **doivent** utiliser [SAM v3](/docs/api/samv3/).

## Liaisons de langage

- Go – [ccondom](https://bitbucket.org/kallevedin/ccondom)
- Python – [`i2py-bob`](http://git.repo.i2p/w/i2py-bob.git)
- Twisted – [`txi2p`](https://pypi.python.org/pypi/txi2p)
- C++ – [`bobcpp`](https://gitlab.com/rszibele/bobcpp)

## Notes sur le protocole

- `KEYS` désigne une destination en base64 (clés publiques + privées).  
- `KEY` est une clé publique en base64.  
- Les réponses `ERROR` ont la forme `ERROR <description>\n`.  
- `OK` indique la fin de la commande ; des données facultatives peuvent suivre sur la même ligne.  
- Les lignes `DATA` fournissent une sortie supplémentaire avant un `OK` final.

La commande `help` constitue la seule exception : elle peut ne rien renvoyer pour indiquer « aucune commande de ce type ».

## Bannière de connexion

BOB utilise des lignes ASCII terminées par un saut de ligne (LF ou CRLF). À la connexion, il envoie :

```
BOB <version>
OK
```
Version actuelle : `00.00.10`. Les versions précédentes utilisaient des caractères hexadécimaux en majuscules et une numérotation non standard.

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
## Commandes de base

> Pour obtenir tous les détails sur les commandes, connectez-vous via `telnet localhost 2827` et exécutez `help`.

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
## Résumé des éléments dépréciés

- BOB ne prend pas en charge les types de signatures modernes, les LeaseSets chiffrés, ni les fonctionnalités de transport.
- L'API est figée ; aucune nouvelle commande ne sera ajoutée.
- Les applications qui dépendent encore de BOB devraient migrer vers SAM v3 dès que possible.
