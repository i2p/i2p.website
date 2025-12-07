---
title: "BOB – Basic Open Bridge"
description: "Deprecated API for destination management (deprecated)"
slug: "bob"
lastUpdated: "2025-05"
layout: "single"
reviewStatus: "needs-review"
---

> **Warning:** BOB only supports the legacy DSA-SHA1 signature type. Java I2P stopped shipping BOB in **1.7.0 (2022-02)**; it remains only on installations that started with 1.6.1 or earlier and on some i2pd builds. New applications **must** use [SAM v3](/docs/api/samv3/).

## Language Bindings

- Go – [ccondom](https://bitbucket.org/kallevedin/ccondom)
- Python – [`i2py-bob`](http://git.repo.i2p/w/i2py-bob.git)
- Twisted – [`txi2p`](https://pypi.python.org/pypi/txi2p)
- C++ – [`bobcpp`](https://gitlab.com/rszibele/bobcpp)

## Protocol Notes

- `KEYS` denotes a base64 destination (public + private keys).  
- `KEY` is a base64 public key.  
- `ERROR` responses have the form `ERROR <description>\n`.  
- `OK` indicates command completion; optional data follows on the same line.  
- `DATA` lines stream additional output before a final `OK`.

The `help` command is the only exception: it may return nothing to signal “no such command”.

## Connection Banner

BOB uses newline-terminated ASCII lines (LF or CRLF). On connect it emits:

```
BOB <version>
OK
```

Current version: `00.00.10`. Earlier builds used uppercase hex digits and non-standard numbering.

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

## Core Commands

> For complete command details, connect with `telnet localhost 2827` and run `help`.

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

## Deprecation Summary

- BOB has no support for modern signature types, encrypted LeaseSets, or transport features.
- The API is frozen; no new commands will be added.
- Applications still relying on BOB should migrate to SAM v3 as soon as possible.
