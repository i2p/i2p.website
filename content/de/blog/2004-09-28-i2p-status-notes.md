---
title: "I2P-Statusnotizen für 2004-09-28"
date: 2004-09-28
author: "jr"
description: "Wöchentliches I2P-Status-Update zur Implementierung eines neuen Transportprotokolls, zur automatischen IP-Erkennung und zum Fortschritt des 0.4.1-Releases"
categories: ["status"]
---

Hi zusammen, Zeit fürs wöchentliche Update

## Stichwortverzeichnis:

1. New transport
2. 0.4.1 status
3. ???

## 1) Neuer Transport

Die Veröffentlichung 0.4.1 hat länger gedauert als erwartet, aber das neue Transportprotokoll und die Implementierung sind mit allem Geplanten einsatzbereit – IP-Erkennung, ressourcenschonende Verbindungsaufnahme und eine einfachere Schnittstelle, die beim Debugging hilft, wenn Verbindungen fehlschlagen. Dies wurde erreicht, indem wir das alte Transportprotokoll vollständig verworfen und ein neues implementiert haben, auch wenn wir immer noch mit denselben Buzzwords aufwarten (2048bit DH + STS, AES256/CBC/PKCS#5). Wenn Sie das Protokoll überprüfen möchten, finden Sie es in der Dokumentation. Die neue Implementierung ist außerdem deutlich sauberer, da die alte Version im Grunde nur ein Haufen von im letzten Jahr angesammelten Updates war.

Jedenfalls gibt es im neuen IP-Erkennungscode ein paar Dinge, die erwähnenswert sind. Am wichtigsten: Er ist vollständig optional – wenn Sie auf der Konfigurationsseite (oder in der router.config selbst) eine IP-Adresse angeben, wird diese Adresse unter allen Umständen verwendet. Lassen Sie das Feld jedoch leer, lässt Ihr router den ersten Peer, den er kontaktiert, ihm mitteilen, unter welcher IP-Adresse er erreichbar ist; auf dieser Adresse beginnt er dann zu lauschen (nachdem er diese seiner eigenen RouterInfo hinzugefügt und in die netDb (Netzwerkdatenbank) eingetragen hat). Nun, das stimmt nicht ganz – wenn Sie nicht ausdrücklich eine IP-Adresse festgelegt haben, wird er jedem vertrauen, der ihm mitteilt, unter welcher IP-Adresse er erreichbar ist, sobald der Peer keine Verbindungen hat. Wenn also Ihre Internetverbindung neu startet und Ihnen möglicherweise eine neue DHCP-Adresse zuweist, vertraut Ihr router dem ersten Peer, den er erreichen kann.

Ja, das bedeutet: kein dyndns mehr. Sie können es natürlich weiterhin verwenden, aber es ist nicht notwendig.

Allerdings erledigt das noch nicht alles, was Sie wollen – wenn Sie sich hinter NAT oder einer Firewall befinden, ist das Wissen um Ihre externe IP-Adresse nur die halbe Miete – Sie müssen die Weiterleitung für den eingehenden Port immer noch einrichten. Aber es ist ein Anfang.

(Nebenbei bemerkt, für Personen, die ihre eigenen privaten I2P-Netzwerke oder Simulatoren betreiben, gibt es ein neues Paar von Flags (Schalter), die gesetzt werden sollen, nämlich i2np.tcp.allowLocal und i2np.tcp.tagFile)

## 2) 0.4.1 Status

Über die Punkte auf der Roadmap für 0.4.1 hinaus möchte ich noch ein paar weitere Dinge unterbringen – sowohl Bugfixes als auch Aktualisierungen bei der Netzwerküberwachung. Ich gehe derzeit einigen Problemen mit übermäßigem Memory-Churn (häufigen Allokationen und Freigaben von Speicher) nach, und ich möchte einige Hypothesen zu den gelegentlichen Zuverlässigkeitsproblemen im Netz untersuchen, aber wir werden bald bereit sein, die Veröffentlichung auszurollen, vielleicht am Donnerstag. Sie wird leider nicht rückwärtskompatibel sein, daher wird es etwas holprig, aber mit dem neuen Upgrade-Prozess und der fehlertoleranteren Transport-Implementierung sollte es nicht so schlimm sein wie bei den bisherigen nicht rückwärtskompatiblen Updates.

## 3) ???

Ja, in den letzten zwei Wochen gab es nur kurze Updates, aber das liegt daran, dass wir tief in der Implementierung stecken und uns darauf konzentrieren statt auf verschiedene High‑Level‑Designs. Ich könnte euch von den Profiling‑Daten erzählen oder dem Connection‑Tag‑Cache (Zwischenspeicher für Verbindungstags) mit 10.000 Einträgen für den neuen Transport, aber das ist nicht so interessant. Allerdings habt ihr vielleicht noch ein paar Dinge zu besprechen, also schaut heute Abend beim Meeting vorbei und legt los.

=jr
