---
title: "Index der technischen Dokumentation"
description: "Index zur technischen Dokumentation von I2P"
slug: "overview"
lastUpdated: "2025-06"
accurateFor: "0.9.67"
aliases:
  - "/de/docs/develop/overview"
  - "/de/docs/develop/overview/"
---


## Übersicht {#overview}

- [Technische Einführung](/docs/overview/intro)
- [Eine weniger technische Einführung](/docs/overview/intro/)
- [Bedrohungsmodell und Analyse](/docs/overview/threat-model)
- [Vergleiche mit anderen anonymen Netzwerken](/docs/overview/comparison)
- [Protokollstapel-Diagramm](/docs/development/protocol-stack)
- [Veröffentlichungen über I2P](/papers/)
- [Präsentationen, Artikel, Tutorials, Videos und Interviews](/about/media/)
- [Invisible Internet Project (I2P) Projektübersicht - 28. August 2003 (PDF)](/docs/historical/i2p_philosophy.pdf)


## Anwendungsschicht-Themen {#applications}

- [Übersicht und Leitfaden zur Anwendungsentwicklung](/docs/development/applications)
- [Benennung und Adressbuch](/docs/overview/naming)
- [Adressbuch-Abonnement-Feed-Befehle](/docs/specs/subscription)
- [Plugin-Übersicht](/docs/guides/plugins)
- [Plugin-Spezifikation](/docs/specs/plugin)
- [Verwaltete Clients](/docs/applications/managed-clients)
- [Einbetten des Routers in Ihre Anwendung](/docs/applications/embedding)
- [Bittorrent über I2P](/docs/applications/bittorrent)
- [I2PControl Plugin API](/docs/api/i2pcontrol)
- [hostsdb.blockfile Format](/docs/specs/blockfile)
- [Konfigurationsdatei-Format](/docs/specs/configuration)


## Anwendungsschicht-API und Protokolle {#api}

- [I2PTunnel](/docs/api/i2ptunnel)
- [I2PTunnel Konfiguration](/docs/specs/configuration)
- [SOCKS Proxy](/docs/api/socks)
- [SAMv3 Protokoll](/docs/api/samv3)
- [SAM Protokoll](/docs/legacy/sam) (Veraltet)
- [SAMv2 Protokoll](/docs/legacy/samv2) (Veraltet)
- [BOB Protokoll](/docs/legacy/bob) (Veraltet)


## Ende-zu-Ende Transport-API und Protokolle {#transport-api}

- [Streaming-Protokoll Übersicht](/docs/api/streaming)
- [Streaming-Protokoll Spezifikation](/docs/specs/streaming)
- [Datagramme](/docs/api/datagrams)
- [Datagramm-Spezifikation](/docs/specs/datagrams)


## Client-zu-Router Schnittstellen-API und Protokoll {#i2cp}

- [I2CP Übersicht](/docs/specs/i2cp)
- [I2CP Spezifikation](/docs/specs/i2cp)
- [Gemeinsame Datenstrukturen Spezifikation](/docs/specs/common-structures)


## Ende-zu-Ende Verschlüsselung {#encryption}

- [ECIES-X25519-AEAD-Ratchet Verschlüsselung für Ziele](/docs/specs/ecies)
- [Hybride ECIES-X25519 Verschlüsselung](/docs/specs/ecies-hybrid)
- [ECIES-X25519 Verschlüsselung für Router](/docs/specs/ecies-routers)
- [ElGamal/AES+SessionTag Verschlüsselung](/docs/specs/elgamal-aes)
- [ElGamal und AES Kryptographie-Details](/docs/specs/cryptography)


## Netzwerk-Datenbank {#netdb}

- [Netzwerk-Datenbank Übersicht, Details und Bedrohungsanalyse](/docs/overview/network-database)
- [Kryptographische Hashes](/docs/specs/cryptography#hashes)
- [Kryptographische Signaturen](/docs/specs/cryptography#signatures)
- [Red25519 Signaturen](/docs/specs/red25519)
- [Router Reseed Spezifikation](/docs/misc/reseed)
- [Base32 Adressen für verschlüsselte Leasesets](/docs/specs/b32encrypted)


## Router-Nachrichtenprotokoll {#i2np}

- [I2NP Übersicht](/docs/specs/i2np)
- [I2NP Spezifikation](/docs/specs/i2np)
- [Gemeinsame Datenstrukturen Spezifikation](/docs/specs/common-structures)
- [Verschlüsseltes Leaseset Spezifikation](/docs/specs/encryptedleaseset)


## Tunnel {#tunnels}

- [Peer-Profiling und -Auswahl](/docs/overview/peer-selection)
- [Tunnel-Routing Übersicht](/docs/overview/tunnel-routing)
- [Garlic-Routing und Terminologie](/docs/overview/garlic-routing)
- [Tunnelbau und Verschlüsselung](/docs/specs/tunnel-creation)
- [ElGamal/AES für Bauanfrage-Verschlüsselung](/docs/specs/elgamal-tunnel-creation)
- [ElGamal und AES Kryptographie-Details](/docs/specs/cryptography)
- [Tunnelbau-Spezifikation (ElGamal)](/docs/specs/tunnel-creation)
- [Tunnelbau-Spezifikation (ECIES-X25519)](/docs/specs/tunnel-creation-ecies)
- [Low-Level Tunnel-Nachrichtenspezifikation](/docs/specs/tunnel-message)
- [Unidirektionale Tunnel](/docs/legacy/unidirectional)
- [Peer-Profiling und -Auswahl im anonymen I2P-Netzwerk - 2009 (PDF)](/docs/historical/I2P-PET-CON-2009.1.pdf)


## Transportschicht {#transports}

- [Transportschicht Übersicht](/docs/overview/transport)
- [NTCP2 Spezifikation](/docs/specs/ntcp2)
- [SSU2 Spezifikation](/docs/specs/ssu2)
- [NTCP (Veraltet)](/docs/legacy/ntcp)
- [SSU Übersicht (Veraltet)](/docs/legacy/ssu-overview)


## Weitere Router-Themen {#router}

- [Router-Software-Updates](/docs/specs/updates)
- [Router Reseed Spezifikation](/docs/misc/reseed)
- [Leistung](/docs/overview/performance)
- [Konfigurationsdatei-Format](/docs/specs/configuration)
- [GeoIP Datei-Format](/docs/legacy/geoip)
- [Von I2P verwendete Ports](/docs/overview/ports)


## Entwickler-Leitfäden und Ressourcen {#develop}

- [Leitfaden für neue Entwickler](/docs/development/new-developers)
- [Leitfaden für neue Übersetzer](/docs/development/new-translators)
- [Entwickler-Richtlinien](/docs/development/dev-guidelines)
- [Vorschläge](/proposals/)
- [Einbetten des Routers in Ihre Anwendung](/docs/applications/embedding)
- [So richten Sie einen Reseed-Server ein](/docs/guides/reseed-server)
- [Von I2P verwendete Ports](/docs/overview/ports)
- [Projekt-Roadmap](/get-involved/roadmap/)
- [Alte invisiblenet I2P Dokumente - 2003](/docs/historical/)
