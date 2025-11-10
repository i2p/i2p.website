---
title: "LeaseSet-Schlüsselpersistenz"
number: "113"
author: "zzz"
created: "2014-12-13"
lastupdated: "2016-12-02"
status: "Closed"
thread: "http://zzz.i2p/topics/1770"
target: "0.9.18"
implementedin: "0.9.18"
---

## Übersicht

Dieses Vorschlag bezieht sich auf die Persistenz zusätzlicher Daten im LeaseSet, die derzeit flüchtig sind. 
In Version 0.9.18 umgesetzt.

## Motivation

In Version 0.9.17 wurde die Persistenz für den netDb-Slicing-Schlüssel hinzugefügt, gespeichert in 
i2ptunnel.config. Dies hilft, einige Angriffe zu verhindern, indem nach einem Neustart derselbe Slice beibehalten wird, und es verhindert auch mögliche Korrelationen mit einem Router-Neustart.

Es gibt zwei weitere Dinge, die sich noch leichter mit einem Router-Neustart korrelieren lassen: 
die Verschlüsselungs- und Signaturschlüssel des LeaseSets. Diese werden derzeit nicht gespeichert.

## Vorgeschlagene Änderungen

Private Schlüssel werden in der i2ptunnel.config gespeichert, als i2cp.leaseSetPrivateKey und i2cp.leaseSetSigningPrivateKey.
