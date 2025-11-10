---
title: "I2P-Statushinweise für 2006-08-01"
date: 2006-08-01
author: "jr"
description: "Starke Netzwerkleistung mit hohen I2PSnark-Übertragungsraten, Stabilität des NTCP-Transports und Klarstellungen zur eepsite-Erreichbarkeit"
categories: ["status"]
---

Hallo zusammen, es ist Zeit für ein paar kurze Notizen vor dem Treffen heute Abend. Mir ist klar, dass ihr verschiedene Fragen oder Themen ansprechen möchtet, daher wählen wir ein flexibleres Format als sonst. Es gibt nur ein paar Dinge, die ich zuerst erwähnen möchte.

* Network status

Es scheint, dass das Netzwerk ziemlich gut läuft: Schwärme von recht großen I2PSnark-Übertragungen werden abgeschlossen, und auf einzelnen routers werden durchaus beträchtliche Transferraten erreicht – ich habe 650KBytes/sec und 17,000 teilnehmende tunnels ohne besondere Vorkommnisse gesehen. Routers am unteren Ende des Spektrums scheinen ebenfalls gut zurechtzukommen: Das Browsen von eepsites(I2P Sites) und irc mit 2 hop tunnels kommt im Durchschnitt mit weniger als 1KByte/sec aus.

Es ist allerdings nicht für alle nur eitel Sonnenschein, aber wir arbeiten daran, das Verhalten des router zu aktualisieren, um eine konstantere und besser nutzbare Leistung zu ermöglichen.

* NTCP

Der neue NTCP-Transport ("neu" tcp) funktioniert nach dem Beseitigen der anfänglichen Kinderkrankheiten recht gut. Um eine häufige Frage zu beantworten: Langfristig werden sowohl NTCP als auch SSU im Einsatz sein - wir kehren nicht zu reinem TCP zurück.

* eepsite(I2P Site) reachability

Denkt daran, Leute, dass eepsites(I2P Sites) nur erreichbar sind, wenn die Person, die sie betreibt, sie online hat - wenn sie offline sind, könnt ihr nichts tun, um sie zu erreichen ;) Leider war orion.i2p in den letzten Tagen nicht erreichbar, aber das Netz funktioniert definitiv weiterhin - schaut vielleicht bei inproxy.tino.i2p oder eepsites(I2P Sites).i2p vorbei, wenn ihr das Netzwerk erkunden wollt.

Jedenfalls, es passiert noch eine Menge, aber es wäre etwas verfrüht, das hier zu erwähnen. Natürlich, wenn ihr Fragen oder Bedenken habt, kommt in ein paar Minuten im #i2p zu unserem *hust* wöchentlichen Entwicklertreffen vorbei.

Vielen Dank für Ihre Hilfe, die uns voranbringt! =jr
