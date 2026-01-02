---
title: "v3dgsend"
description: "CLI-Dienstprogramm zum Senden von I2P-Datagrammen über SAM v3"
slug: "v3dgsend"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

> Status: Dies ist eine prägnante Referenz für das `v3dgsend`-Dienstprogramm. Es ergänzt die Dokumentation zur [Datagram API](/docs/api/datagrams/) und [SAM v3](/docs/api/samv3/).

## Übersicht

`v3dgsend` ist ein Befehlszeilen-Hilfswerkzeug zum Senden von I2P-Datagrammen über das SAMv3-Interface. Es ist nützlich zum Testen der Datagramm-Zustellung, zum Prototyping von Diensten und zur Überprüfung des End-to-End-Verhaltens, ohne einen vollständigen Client schreiben zu müssen.

Typische Anwendungsfälle sind:

- Smoke-Testing der Datagramm-Erreichbarkeit zu einem Destination
- Validierung der Firewall- und Adressbuch-Konfiguration
- Experimentieren mit rohen vs. signierten (beantwortbaren) Datagrammen

## Verwendung

Die grundlegende Aufrufweise variiert je nach Plattform und Paketierung. Gängige Optionen sind:

- Destination: base64 Destination oder `.i2p`-Name
- Protocol: raw (PROTOCOL 18) oder signed (PROTOCOL 17)
- Payload: Inline-String oder Dateieingabe

Beziehen Sie sich auf die Paketierung Ihrer Distribution oder die `--help`-Ausgabe für die exakten Flags.

## Siehe auch

- [Datagram API](/docs/api/datagrams/)
- [SAM v3](/docs/api/samv3/)
- [Streaming Library](/docs/api/streaming/) (Alternative zu Datagrams)
