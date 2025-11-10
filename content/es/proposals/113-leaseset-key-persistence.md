---
title: "Persistencia de Claves LeaseSet"
number: "113"
author: "zzz"
created: "2014-12-13"
lastupdated: "2016-12-02"
status: "Cerrado"
thread: "http://zzz.i2p/topics/1770"
target: "0.9.18"
implementedin: "0.9.18"
---

## Visión General

Esta propuesta trata sobre la persistencia de datos adicionales en el LeaseSet que actualmente son efímeros.
Implementado en 0.9.18.

## Motivación

En 0.9.17 se agregó la persistencia para la clave de particionamiento netDb, almacenada en
i2ptunnel.config. Esto ayuda a prevenir algunos ataques al mantener la misma partición
después de reiniciar, y también evita la posible correlación con un reinicio del router.

Hay dos cosas más que son aún más fáciles de correlacionar con el reinicio del router:
las claves de cifrado y firma de leaseset. Estas actualmente no son persistentes.

## Cambios Propuestos

Las claves privadas se almacenan en i2ptunnel.config, como i2cp.leaseSetPrivateKey e i2cp.leaseSetSigningPrivateKey.
