---
title: "I2P Mail (Anonyme E-Mail über I2P)"
description: "Eine Übersicht über E-Mail-Systeme im I2P-Netzwerk — Geschichte, Optionen und aktueller Status"
slug: "i2p-mail"
lastUpdated: "2025-10"
---

## Einleitung

I2P bietet privates E-Mail-ähnliches Messaging durch den **Postman's Mail.i2p-Dienst** in Kombination mit **SusiMail**, einem integrierten Webmail-Client. Dieses System ermöglicht es Benutzern, E-Mails sowohl innerhalb des I2P-Netzwerks als auch zum/vom regulären Internet (Clearnet) über eine Gateway-Brücke zu senden und zu empfangen.

---

## Postman / Mail.i2p + SusiMail

### What it is

- **Mail.i2p** ist ein gehosteter E-Mail-Anbieter innerhalb von I2P, betrieben von "Postman"
- **SusiMail** ist der Webmail-Client, der in die I2P-Router-Konsole integriert ist. Er wurde entwickelt, um das Leaken von Metadaten (z. B. Hostname) an externe SMTP-Server zu verhindern.
- Durch dieses Setup können I2P-Nutzer Nachrichten sowohl innerhalb von I2P als auch zum/vom Clearnet (z. B. Gmail) über die Postman-Bridge senden und empfangen.

### How Addressing Works

I2P-E-Mail verwendet ein duales Adresssystem:

- **Innerhalb des I2P-Netzwerks**: `username@mail.i2p` (z. B. `idk@mail.i2p`)
- **Vom Clearnet aus**: `username@i2pmail.org` (z. B. `idk@i2pmail.org`)

Das `i2pmail.org`-Gateway ermöglicht es normalen Internet-Nutzern, E-Mails an I2P-Adressen zu senden, und I2P-Nutzern, E-Mails an Clearnet-Adressen zu senden. Internet-E-Mails werden über das Gateway geleitet, bevor sie durch I2P an Ihren SusiMail-Posteingang weitergeleitet werden.

**Clearnet-Sendequote**: 20 E-Mails pro Tag beim Versenden an reguläre Internetadressen.

### Was es ist

**So registrieren Sie sich für ein mail.i2p-Konto:**

1. Stellen Sie sicher, dass Ihr I2P-Router läuft
2. Besuchen Sie **[http://hq.postman.i2p](http://hq.postman.i2p)** innerhalb von I2P
3. Folgen Sie dem Registrierungsprozess
4. Greifen Sie auf Ihre E-Mails über **SusiMail** in der Router-Konsole zu

> **Hinweis**: `hq.postman.i2p` ist eine I2P-Netzwerkadresse (eepsite) und kann nur bei bestehender Verbindung zu I2P aufgerufen werden. Für weitere Informationen zur E-Mail-Einrichtung, Sicherheit und Nutzung besuchen Sie Postman HQ.

### Wie Adressierung funktioniert

- Automatisches Entfernen identifizierender Header (`User-Agent:`, `X-Mailer:`) zum Schutz der Privatsphäre
- Metadaten-Bereinigung zur Verhinderung von Lecks an externe SMTP-Server
- Ende-zu-Ende-Verschlüsselung für interne I2P-zu-I2P-E-Mails

### Erste Schritte

- Interoperabilität mit "normalem" E-Mail (SMTP/POP) über die Postman-Bridge
- Einfache Benutzererfahrung (Webmail integriert in die Router-Konsole)
- Integration in die I2P-Kernverteilung (SusiMail wird mit Java I2P ausgeliefert)
- Entfernung von Headern zum Schutz der Privatsphäre

### Datenschutzfunktionen

- Die Brücke zu externer E-Mail erfordert Vertrauen in die Postman-Infrastruktur
- Clearnet-Brücke reduziert die Privatsphäre im Vergleich zu rein interner I2P-Kommunikation
- Abhängig von der Verfügbarkeit und Sicherheit des Postman-Mailservers

---


## Technical Details

**SMTP-Dienst**: `localhost:7659` (bereitgestellt von Postman) **POP3-Dienst**: `localhost:7660` **Webmail-Zugriff**: In die Router-Konsole integriert unter `http://127.0.0.1:7657/susimail/`

> **Wichtig**: SusiMail dient nur zum Lesen und Versenden von E-Mails. Kontoerstellung und -verwaltung müssen unter **hq.postman.i2p** durchgeführt werden.

---

## Best Practices

- **Ändern Sie Ihr Passwort** nach der Registrierung Ihres mail.i2p-Kontos
- **Nutzen Sie I2P-zu-I2P E-Mail** wann immer möglich für maximale Privatsphäre (keine Clearnet-Brücke)
- **Beachten Sie das Limit von 20/Tag** beim Versenden an Clearnet-Adressen
- **Verstehen Sie die Kompromisse**: Clearnet-Brücken bieten Komfort, reduzieren aber die Anonymität im Vergleich zu rein internen I2P-Kommunikationen
- **Halten Sie I2P aktuell**, um von Sicherheitsverbesserungen in SusiMail zu profitieren

