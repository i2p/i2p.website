---
title: "SOCKS Proxy"
description: "Bezpečné používání SOCKS tunnel v I2P"
slug: "socks"
aliases:
  - "/cs/socks"
  - "/cs/socks/"
lastUpdated: "2024-02"
accurateFor: "0.9.62"
---

## SOCKS a SOCKS Proxy {#overview}

SOCKS proxy funguje od verze 0.7.1. Podporovány jsou SOCKS 4/4a/5. SOCKS povolíte vytvořením SOCKS klientského tunelu v i2ptunnel. Podporováni jsou jak shared-clients, tak non-shared klienti. Neexistuje žádný SOCKS outproxy, takže je jeho použití omezené.

Jak je uvedeno v [FAQ](/docs/overview/faq#socks):

```
Many applications leak sensitive information that could identify you on the
Internet. I2P only filters connection data, but if the program you intend to
run sends this information as content, I2P has no way to protect your anonymity.
For example, some mail applications will send the IP address of the machine
they are running on to a mail server. There is no way for I2P to filter this,
thus using I2P to 'socksify' existing applications is possible, but extremely
dangerous.
```
A citace z emailu z roku 2005:

```
... there is a reason why human and others have both built and abandoned the
SOCKS proxies. Forwarding arbitrary traffic is just plain unsafe, and it
behooves us as developers of anonymity and security software to have the safety
of our end users foremost in our minds.
```
Doufat, že můžeme jednoduše připojit libovolného klienta na I2P bez kontroly jak jeho chování, tak jeho vystavených protokolů z hlediska bezpečnosti a anonymity, je naivní. Prakticky *každá* aplikace a protokol porušuje anonymitu, pokud nebyl speciálně pro ni navržen, a i tak většina z nich to také dělá. To je realita. Koncoví uživatelé jsou lépe obslouženi systémy navrženými pro anonymitu a bezpečnost. Upravování existujících systémů pro práci v anonymních prostředích není malý úkol, je to o řády větší množství práce než jednoduché použití stávajících I2P API.

SOCKS proxy podporuje standardní názvy z adresáře, ale ne Base64 destinace. Base32 hashe by měly fungovat od verze 0.7. Podporuje pouze odchozí připojení, tj. I2PTunnel klienta. UDP podpora je připravena, ale zatím nefunkční. Výběr outproxy podle čísla portu je připraven.

## Viz také {#see-also}

- Poznámky ze schůzky 81 (16. března 2004) a schůzky 82 (23. března 2004).
- [Onioncat](http://www.abenteuerland.at/onioncat/)

## Pokud se vám něco podaří zprovoznit {#working}

Dejte nám prosím vědět. A prosím poskytněte důkladná upozornění o rizicích socks proxy.
