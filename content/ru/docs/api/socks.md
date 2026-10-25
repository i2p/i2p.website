---
title: "SOCKS прокси"
description: "Безопасное использование SOCKS tunnel I2P"
slug: "socks"
aliases:
  - "/ru/socks"
  - "/ru/socks/"
lastUpdated: "2024-02"
accurateFor: "0.9.62"
---

## SOCKS и SOCKS прокси {#overview}

SOCKS прокси работает начиная с версии 0.7.1. Поддерживаются SOCKS 4/4a/5. Включите SOCKS, создав клиентский tunnel SOCKS в i2ptunnel. Поддерживаются как shared-clients, так и non-shared. SOCKS outproxy отсутствует, поэтому функциональность ограничена.

Как сказано в [FAQ](/docs/overview/faq#socks):

```
Many applications leak sensitive information that could identify you on the
Internet. I2P only filters connection data, but if the program you intend to
run sends this information as content, I2P has no way to protect your anonymity.
For example, some mail applications will send the IP address of the machine
they are running on to a mail server. There is no way for I2P to filter this,
thus using I2P to 'socksify' existing applications is possible, but extremely
dangerous.
```
И цитируя из письма 2005 года:

```
... there is a reason why human and others have both built and abandoned the
SOCKS proxies. Forwarding arbitrary traffic is just plain unsafe, and it
behooves us as developers of anonymity and security software to have the safety
of our end users foremost in our minds.
```
Надеяться, что мы можем просто прикрутить произвольный клиент поверх I2P без аудита как его поведения, так и используемых им протоколов на предмет безопасности и анонимности — наивно. Практически *каждое* приложение и протокол нарушает анонимность, если только он не был специально разработан для неё, и даже тогда большинство из них тоже нарушают. Такова реальность. Конечным пользователям лучше подходят системы, изначально спроектированные для анонимности и безопасности. Модификация существующих систем для работы в анонимных средах — задача не из простых, на порядки более трудоёмкая, чем простое использование существующих I2P API.

SOCKS прокси поддерживает стандартные имена адресной книги, но не поддерживает Base64 назначения. Base32 хеши должны работать начиная с версии 0.7. Поддерживает только исходящие соединения, то есть работает как I2PTunnel клиент. Поддержка UDP заглушена, но пока не работает. Выбор outproxy по номеру порта заглушен.

## См. также {#see-also}

- Заметки для Встречи 81 (16 марта 2004 г.) и Встречи 82 (23 марта 2004 г.).
- [Onioncat](http://www.abenteuerland.at/onioncat/)

## Если вам удалось что-то заставить работать {#working}

Пожалуйста, сообщите нам. И, пожалуйста, предоставьте существенные предупреждения о рисках socks прокси.
