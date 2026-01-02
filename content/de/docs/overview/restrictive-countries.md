---
title: "Länder mit strikten/restriktiven Internetrichtlinien"
description: "Wie sich I2P in Jurisdiktionen mit Einschränkungen für Routing- oder Anonymitätstools verhält (Hidden Mode und Strict List)"
slug: "restrictive-countries"
lastUpdated: "2024-07"
accurateFor: "2.10.0"
type: docs
reviewStatus: "needs-review"
---

Diese Implementierung von I2P (die Java-Implementierung, die auf dieser Seite verteilt wird) enthält eine "Strict Countries List", die verwendet wird, um das Routerverhalten in Regionen anzupassen, in denen die Teilnahme am Routing für andere möglicherweise gesetzlich eingeschränkt ist. Obwohl uns keine Rechtsordnungen bekannt sind, die die Nutzung von I2P verbieten, haben mehrere umfassende Verbote für das Weiterleiten von Datenverkehr. Router, die sich offenbar in "strict" Ländern befinden, werden automatisch in den Hidden-Modus versetzt.

Das Projekt bezieht sich bei diesen Entscheidungen auf Forschungsergebnisse von Bürgerrechts- und digitalen Rechtsorganisationen. Insbesondere fließen laufende Untersuchungen von Freedom House in unsere Entscheidungen ein. Die allgemeine Richtlinie besteht darin, Länder mit einem Civil Liberties (CL)-Wert von 16 oder weniger oder einem Internet Freedom-Wert von 39 oder weniger (nicht frei) einzubeziehen.

## Zusammenfassung des Hidden-Modus

Wenn ein Router in den Hidden-Modus versetzt wird, ändern sich drei wesentliche Aspekte seines Verhaltens:

- Es veröffentlicht keine RouterInfo in der netDb.
- Es akzeptiert keine participating tunnels.
- Es lehnt direkte Verbindungen zu Routern im selben Land ab.

Diese Schutzmaßnahmen erschweren es, Router zuverlässig zu erfassen, und verringern das Risiko, lokale Verbote bezüglich der Weiterleitung von Datenverkehr für andere zu verletzen.

## Liste strenger Länder (Stand: 2024)

```
/* Afghanistan */ "AF",
/* Azerbaijan */ "AZ",
/* Bahrain */ "BH",
/* Belarus */ "BY",
/* Brunei */ "BN",
/* Burundi */ "BI",
/* Cameroon */ "CM",
/* Central African Republic */ "CF",
/* Chad */ "TD",
/* China */ "CN",
/* Cuba */ "CU",
/* Democratic Republic of the Congo */ "CD",
/* Egypt */ "EG",
/* Equatorial Guinea */ "GQ",
/* Eritrea */ "ER",
/* Ethiopia */ "ET",
/* Iran */ "IR",
/* Iraq */ "IQ",
/* Kazakhstan */ "KZ",
/* Laos */ "LA",
/* Libya */ "LY",
/* Myanmar */ "MM",
/* North Korea */ "KP",
/* Palestinian Territories */ "PS",
/* Pakistan */ "PK",
/* Rwanda */ "RW",
/* Saudi Arabia */ "SA",
/* Somalia */ "SO",
/* South Sudan */ "SS",
/* Sudan */ "SD",
/* Eswatini (Swaziland) */ "SZ",
/* Syria */ "SY",
/* Tajikistan */ "TJ",
/* Thailand */ "TH",
/* Turkey */ "TR",
/* Turkmenistan */ "TM",
/* Venezuela */ "VE",
/* United Arab Emirates */ "AE",
/* Uzbekistan */ "UZ",
/* Vietnam */ "VN",
/* Western Sahara */ "EH",
/* Yemen */ "YE"
```
Wenn Sie der Meinung sind, dass ein Land zur strikten Liste hinzugefügt oder daraus entfernt werden sollte, eröffnen Sie bitte ein Issue: https://i2pgit.org/i2p/i2p.i2p/

Referenz: Freedom House – https://freedomhouse.org/
