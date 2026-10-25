---
title: "Указатель технической документации"
description: "Указатель технической документации I2P"
slug: "overview"
lastUpdated: "2025-06"
accurateFor: "0.9.67"
aliases:
  - "/ru/docs/develop/overview"
  - "/ru/docs/develop/overview/"
---


## Обзор {#overview}

- [Техническое введение](/docs/overview/intro)
- [Менее техническое введение](/docs/overview/intro/)
- [Модель угроз и анализ](/docs/overview/threat-model)
- [Сравнение с другими анонимными сетями](/docs/overview/comparison)
- [Схема стека протоколов](/docs/development/protocol-stack)
- [Статьи об I2P](/papers/)
- [Презентации, статьи, руководства, видео и интервью](/about/media/)
- [Обзор проекта Invisible Internet Project (I2P) — 28 августа 2003 г. (PDF)](/docs/historical/i2p_philosophy.pdf)


## Темы прикладного уровня {#applications}

- [Обзор и руководство по разработке приложений](/docs/development/applications)
- [Именование и адресная книга](/docs/overview/naming)
- [Команды ленты подписки адресной книги](/docs/specs/subscription)
- [Обзор плагинов](/docs/guides/plugins)
- [Спецификация плагинов](/docs/specs/plugin)
- [Управляемые клиенты](/docs/applications/managed-clients)
- [Встраивание маршрутизатора в ваше приложение](/docs/applications/embedding)
- [Bittorrent через I2P](/docs/applications/bittorrent)
- [API плагина I2PControl](/docs/api/i2pcontrol)
- [Формат hostsdb.blockfile](/docs/specs/blockfile)
- [Формат файла конфигурации](/docs/specs/configuration)


## API и протоколы прикладного уровня {#api}

- [I2PTunnel](/docs/api/i2ptunnel)
- [Конфигурация I2PTunnel](/docs/specs/configuration)
- [SOCKS прокси](/docs/api/socks)
- [Протокол SAMv3](/docs/api/samv3)
- [Протокол SAM](/docs/legacy/sam) (Устаревший)
- [Протокол SAMv2](/docs/legacy/samv2) (Устаревший)
- [Протокол BOB](/docs/legacy/bob) (Устаревший)


## API и протоколы сквозной передачи {#transport-api}

- [Обзор потокового протокола](/docs/api/streaming)
- [Спецификация потокового протокола](/docs/specs/streaming)
- [Датаграммы](/docs/api/datagrams)
- [Спецификация датаграмм](/docs/specs/datagrams)


## API и протокол интерфейса клиент-маршрутизатор {#i2cp}

- [Обзор I2CP](/docs/specs/i2cp)
- [Спецификация I2CP](/docs/specs/i2cp)
- [Спецификация общих структур данных](/docs/specs/common-structures)


## Сквозное шифрование {#encryption}

- [Шифрование ECIES-X25519-AEAD-Ratchet для пунктов назначения](/docs/specs/ecies)
- [Гибридное шифрование ECIES-X25519](/docs/specs/ecies-hybrid)
- [Шифрование ECIES-X25519 для маршрутизаторов](/docs/specs/ecies-routers)
- [Шифрование ElGamal/AES+SessionTag](/docs/specs/elgamal-aes)
- [Детали криптографии ElGamal и AES](/docs/specs/cryptography)


## Сетевая база данных {#netdb}

- [Обзор сетевой базы данных, детали и анализ угроз](/docs/overview/network-database)
- [Криптографические хэши](/docs/specs/cryptography#hashes)
- [Криптографические подписи](/docs/specs/cryptography#signatures)
- [Подписи Red25519](/docs/specs/red25519)
- [Спецификация reseed маршрутизатора](/docs/misc/reseed)
- [Адреса Base32 для зашифрованных наборов аренды](/docs/specs/b32encrypted)


## Протокол сообщений маршрутизатора {#i2np}

- [Обзор I2NP](/docs/specs/i2np)
- [Спецификация I2NP](/docs/specs/i2np)
- [Спецификация общих структур данных](/docs/specs/common-structures)
- [Спецификация зашифрованного набора аренды](/docs/specs/encryptedleaseset)


## Туннели {#tunnels}

- [Профилирование и выбор пиров](/docs/overview/peer-selection)
- [Обзор маршрутизации туннелей](/docs/overview/tunnel-routing)
- [Чесночная маршрутизация и терминология](/docs/overview/garlic-routing)
- [Построение и шифрование туннелей](/docs/specs/tunnel-creation)
- [ElGamal/AES для шифрования запросов на построение](/docs/specs/elgamal-tunnel-creation)
- [Детали криптографии ElGamal и AES](/docs/specs/cryptography)
- [Спецификация построения туннелей (ElGamal)](/docs/specs/tunnel-creation)
- [Спецификация построения туннелей (ECIES-X25519)](/docs/specs/tunnel-creation-ecies)
- [Спецификация низкоуровневых сообщений туннеля](/docs/specs/tunnel-message)
- [Однонаправленные туннели](/docs/legacy/unidirectional)
- [Профилирование и выбор пиров в анонимной сети I2P — 2009 (PDF)](/docs/historical/I2P-PET-CON-2009.1.pdf)


## Транспортный уровень {#transports}

- [Обзор транспортного уровня](/docs/overview/transport)
- [Спецификация NTCP2](/docs/specs/ntcp2)
- [Спецификация SSU2](/docs/specs/ssu2)
- [NTCP (Устаревший)](/docs/legacy/ntcp)
- [Обзор SSU (Устаревший)](/docs/legacy/ssu-overview)


## Другие темы маршрутизатора {#router}

- [Обновления программного обеспечения маршрутизатора](/docs/specs/updates)
- [Спецификация reseed маршрутизатора](/docs/misc/reseed)
- [Производительность](/docs/overview/performance)
- [Формат файла конфигурации](/docs/specs/configuration)
- [Формат файла GeoIP](/docs/legacy/geoip)
- [Порты, используемые I2P](/docs/overview/ports)


## Руководства и ресурсы для разработчиков {#develop}

- [Руководство для новых разработчиков](/docs/development/new-developers)
- [Руководство для новых переводчиков](/docs/development/new-translators)
- [Рекомендации для разработчиков](/docs/development/dev-guidelines)
- [Предложения](/proposals/)
- [Встраивание маршрутизатора в ваше приложение](/docs/applications/embedding)
- [Как настроить сервер reseed](/docs/guides/reseed-server)
- [Порты, используемые I2P](/docs/overview/ports)
- [Дорожная карта проекта](/get-involved/roadmap/)
- [Старые документы invisiblenet I2P — 2003](/docs/historical/)
