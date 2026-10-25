---
title: "SOCKS Proxy"
description: "Sichere Verwendung des I2P SOCKS tunnel"
slug: "socks"
aliases:
  - "/de/socks"
  - "/de/socks/"
lastUpdated: "2024-02"
accurateFor: "0.9.62"
---

## SOCKS und SOCKS-Proxies {#overview}

Der SOCKS-Proxy funktioniert seit Version 0.7.1. SOCKS 4/4a/5 werden unterstützt. Aktivieren Sie SOCKS, indem Sie einen SOCKS-Client-Tunnel in i2ptunnel erstellen. Sowohl shared-clients als auch non-shared werden unterstützt. Es gibt keinen SOCKS-Outproxy, daher ist der Nutzen begrenzt.

Wie es in den [FAQ](/docs/overview/faq#socks) steht:

```
Many applications leak sensitive information that could identify you on the
Internet. I2P only filters connection data, but if the program you intend to
run sends this information as content, I2P has no way to protect your anonymity.
For example, some mail applications will send the IP address of the machine
they are running on to a mail server. There is no way for I2P to filter this,
thus using I2P to 'socksify' existing applications is possible, but extremely
dangerous.
```
Und aus einer E-Mail von 2005 zitiert:

```
... there is a reason why human and others have both built and abandoned the
SOCKS proxies. Forwarding arbitrary traffic is just plain unsafe, and it
behooves us as developers of anonymity and security software to have the safety
of our end users foremost in our minds.
```
Zu hoffen, dass wir einfach einen beliebigen Client auf I2P aufsetzen können, ohne sowohl sein Verhalten als auch die offengelegten Protokolle auf Sicherheit und Anonymität zu prüfen, ist naiv. So gut wie *jede* Anwendung und jedes Protokoll verletzt die Anonymität, es sei denn, es wurde speziell dafür entwickelt, und selbst dann tun das die meisten auch. Das ist die Realität. Endnutzer sind mit Systemen besser bedient, die für Anonymität und Sicherheit entwickelt wurden. Bestehende Systeme zu modifizieren, damit sie in anonymen Umgebungen funktionieren, ist keine Kleinigkeit - es bedeutet Größenordnungen mehr Arbeit als einfach die bestehenden I2P-APIs zu verwenden.

Der SOCKS-Proxy unterstützt Standard-Adressbuchnamen, aber keine Base64-Ziele. Base32-Hashes sollten ab Version 0.7 funktionieren. Er unterstützt nur ausgehende Verbindungen, d.h. einen I2PTunnel Client. UDP-Unterstützung ist vorbereitet, funktioniert aber noch nicht. Die Outproxy-Auswahl nach Portnummer ist vorbereitet.

## Siehe auch {#see-also}

- Die Notizen für Meeting 81 (16. März 2004) und Meeting 82 (23. März 2004).
- [Onioncat](http://www.abenteuerland.at/onioncat/)

## Falls Sie etwas zum Laufen bringen {#working}

Bitte lassen Sie es uns wissen. Und bitte geben Sie deutliche Warnungen über die Risiken von SOCKS-Proxys an.
