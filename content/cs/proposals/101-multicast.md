---
title: "Multicast"
number: "101"
author: "zzz"
created: "2008-12-08"
lastupdated: "2009-03-25"
status: "Mrtvý"
thread: "http://zzz.i2p/topics/172"
---

## Přehled

Základní myšlenka: Odeslat jednu kopii přes váš odchozí tunel, odchozí koncový bod distribuuje ke všem vstupním branám. Konec-konec šifrování vyloučeno.


## Návrh

- Nový typ multicast tunelové zprávy (typ doručení = 0x03)
- Odchozí koncový bod multicast distribuce
- Nový typ I2NP Multicast Zprávy?
- Nový typ I2CP Multicast SendMessageMessage Zprávy
- Nešifrovat router-router v OutNetMessageOneShotJob (česnek?)

Aplikace:

- RTSP Proxy?

Streamr:

- Nastavit MTU? Nebo to udělat jen v aplikaci?
- Přijem a přenos na požádání
