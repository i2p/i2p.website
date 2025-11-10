---
title: "Hallo Git, auf Wiedersehen Monotone"
date: 2020-12-10
author: "idk"
description: "Hallo git, auf Wiedersehen mtn"
categories: ["Status"]
---

## Hallo Git, auf Wiedersehen Monotone

### The I2P Git Migration is nearly concluded

Seit über einem Jahrzehnt hat sich I2P auf den altehrwürdigen Monotone-Dienst verlassen, um seine Anforderungen an die Versionsverwaltung zu erfüllen, doch in den vergangenen Jahren ist der Großteil der Welt zum inzwischen universellen Versionskontrollsystem Git übergegangen. Im selben Zeitraum ist das I2P-Netzwerk schneller und zuverlässiger geworden, und es wurden praktikable Workarounds für die fehlende Wiederaufnehmbarkeit von Git entwickelt.

Heute ist ein bedeutender Tag für I2P, denn wir haben den alten mtn i2p.i2p-Branch abgeschaltet und die Entwicklung der Kern-Java-I2P-Bibliotheken offiziell von Monotone auf Git umgestellt.

Während unsere Verwendung von mtn in der Vergangenheit infrage gestellt wurde und es nicht immer eine beliebte Wahl war, möchte ich diesen Moment nutzen, um – vielleicht als das allerletzte Projekt, das Monotone verwendet – den Monotone-Entwicklern, aktuellen und ehemaligen, wo immer sie auch sind, für die von ihnen geschaffene Software zu danken.

## GPG Signing

Check-ins in die Repositories des I2P-Projekts erfordern, dass Sie die GPG-Signierung für Ihre Git-Commits konfigurieren, einschließlich Merge Requests und Pull Requests. Bitte konfigurieren Sie Ihren Git-Client für die GPG-Signierung, bevor Sie einen Fork von i2p.i2p erstellen und irgendetwas einchecken.

## GPG-Signierung

Das offizielle Repository ist dasjenige, das unter https://i2pgit.org/i2p-hackers/i2p.i2p und unter https://git.idk.i2p/i2p-hackers/i2p.i2p gehostet wird, aber es gibt ein "Mirror" bei Github unter https://github.com/i2p/i2p.i2p.

Da wir jetzt Git verwenden, können wir Repositories von unserer eigenen selbstgehosteten Gitlab-Instanz zu Github und wieder zurück synchronisieren. Das bedeutet, dass es möglich ist, auf Gitlab einen Merge Request zu erstellen und einzureichen und dass, wenn er zusammengeführt wird, das Ergebnis mit Github synchronisiert wird, und dass ein Pull Request auf Github, wenn er zusammengeführt wird, auf Gitlab erscheint.

This means that it's possible to submit code to us through our Gitlab instance or through Github depending on what you prefer, however, more of the I2P developers are regularly monitoring Gitlab than Github. MR's to Gitlab are more likely to be merged sooner than PR's to Github.

## Offizielle Repositorys und Gitlab/Github-Synchronisierung

Herzlichen Glückwunsch und vielen Dank an alle, die bei der Git-Migration geholfen haben, insbesondere zzz, eche|on, nextloop und die Betreiber unserer Website-Spiegel! Auch wenn einige von uns Monotone vermissen werden, ist es zu einem Hindernis für neue und bestehende Mitwirkende an der I2P-Entwicklung geworden, und wir freuen uns darauf, uns der Welt der Entwickler anzuschließen, die Git zur Verwaltung ihrer verteilten Projekte verwenden.
