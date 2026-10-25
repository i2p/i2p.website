---
title: "Proxy SOCKS"
description: "Utiliser le tunnel SOCKS d'I2P en toute sécurité"
slug: "socks"
aliases:
  - "/fr/socks"
  - "/fr/socks/"
lastUpdated: "2024-02"
accurateFor: "0.9.62"
---

## SOCKS et proxys SOCKS {#overview}

Le proxy SOCKS fonctionne depuis la version 0.7.1. SOCKS 4/4a/5 sont pris en charge. Activez SOCKS en créant un tunnel client SOCKS dans i2ptunnel. Les clients partagés et non partagés sont tous deux pris en charge. Il n'y a pas d'outproxy SOCKS, son utilité est donc limitée.

Comme indiqué dans la [FAQ](/docs/overview/faq#socks) :

```
Many applications leak sensitive information that could identify you on the
Internet. I2P only filters connection data, but if the program you intend to
run sends this information as content, I2P has no way to protect your anonymity.
For example, some mail applications will send the IP address of the machine
they are running on to a mail server. There is no way for I2P to filter this,
thus using I2P to 'socksify' existing applications is possible, but extremely
dangerous.
```
Et en citant un email de 2005 :

```
... there is a reason why human and others have both built and abandoned the
SOCKS proxies. Forwarding arbitrary traffic is just plain unsafe, and it
behooves us as developers of anonymity and security software to have the safety
of our end users foremost in our minds.
```
Espérer que nous puissions simplement greffer un client arbitraire sur I2P sans auditer à la fois son comportement et ses protocoles exposés pour la sécurité et l'anonymat est naïf. Pratiquement *toutes* les applications et protocoles violent l'anonymat, à moins qu'ils n'aient été conçus spécifiquement pour cela, et même dans ce cas, la plupart le font aussi. C'est la réalité. Les utilisateurs finaux sont mieux servis par des systèmes conçus pour l'anonymat et la sécurité. Modifier des systèmes existants pour qu'ils fonctionnent dans des environnements anonymes n'est pas une mince affaire, c'est un travail d'un ordre de grandeur supérieur à l'utilisation simple des APIs I2P existantes.

Le proxy SOCKS prend en charge les noms de carnet d'adresses standards, mais pas les destinations Base64. Les hachages Base32 devraient fonctionner depuis la version 0.7. Il prend en charge uniquement les connexions sortantes, c'est-à-dire un client I2PTunnel. La prise en charge UDP est ébauchée mais ne fonctionne pas encore. La sélection d'outproxy par numéro de port est ébauchée.

## Voir aussi {#see-also}

- Les notes pour la Réunion 81 (16 mars 2004) et la Réunion 82 (23 mars 2004).
- [Onioncat](http://www.abenteuerland.at/onioncat/)

## Si vous arrivez à faire fonctionner quelque chose {#working}

Veuillez nous en informer. Et veuillez fournir des avertissements substantiels concernant les risques des proxies SOCKS.
