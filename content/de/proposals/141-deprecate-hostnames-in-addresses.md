---
title: "Veraltet Hostnamen in Router-Adressen"
number: "141"
author: "zzz"
created: "2017-08-03"
lastupdated: "2018-03-17"
status: "Geschlossen"
thread: "http://zzz.i2p/topics/2363"
target: "0.9.32"
implementedin: "0.9.32"
toc: true
---

## Übersicht

Ab der Version 0.9.32 wird die NetDB-Spezifikation aktualisiert, um Hostnamen in Router-Infos, genauer gesagt in den einzelnen Router-Adressen, zu veralten. In allen I2P-Implementierungen sollten veröffentlichende Router, die mit Hostnamen konfiguriert sind, Hostnamen vor der Veröffentlichung durch IPs ersetzen, und andere Router sollten Adressen mit Hostnamen ignorieren. Router sollten keine DNS-Lookups für veröffentlichte Hostnamen durchführen.

## Motivation

Hostnamen wurden seit Beginn von I2P in Router-Adressen erlaubt. Allerdings veröffentlichen nur sehr wenige Router Hostnamen, da es sowohl einen öffentlichen Hostnamen (den nur wenige Benutzer haben) als auch eine manuelle Konfiguration erfordert (was nur wenige Benutzer tun). In einer kürzlich durchgeführten Stichprobe veröffentlichten 0,7 % der Router einen Hostnamen.

Der ursprüngliche Zweck von Hostnamen bestand darin, Benutzern mit häufig wechselnden IPs und einem dynamischen DNS-Dienst (wie http://dyn.com/dns/) zu helfen, die Konnektivität nicht zu verlieren, wenn sich ihre IP änderte. Damals war das Netzwerk jedoch klein und das Ablaufdatum der Router-Infos war länger. Außerdem hatte der Java-Code keine funktionierende Logik, um den Router neu zu starten oder die Router-Info erneut zu veröffentlichen, wenn sich die lokale IP änderte.

Außerdem unterstützte I2P anfangs kein IPv6, sodass die Komplikation der Auflösung eines Hostnamens zu einer IPv4- oder IPv6-Adresse nicht existierte.

In Java I2P war es immer eine Herausforderung, einen konfigurierten Hostnamen auf beide veröffentlichten Transports zu übertragen, und die Situation wurde mit IPv6 komplexer. Es ist unklar, ob ein Dual-Stack-Host sowohl einen Hostnamen als auch eine wörtliche IPv6-Adresse veröffentlichen sollte oder nicht. Der Hostname wird für die SSU-Adresse veröffentlicht, jedoch nicht für die NTCP-Adresse.

Kürzlich wurden DNS-Probleme sowohl indirekt als auch direkt durch Forschungen an der Georgia Tech angesprochen. Die Forscher führten eine große Anzahl von Floodfills mit veröffentlichten Hostnamen aus. Das unmittelbare Problem war, dass I2P für eine kleine Anzahl von Benutzern mit möglicherweise fehlerhaftem lokalem DNS vollständig blockierte.

Das größere Problem war DNS im Allgemeinen und wie DNS (entweder aktiv oder passiv) verwendet werden könnte, um das Netzwerk sehr schnell zu enumerieren, insbesondere wenn die veröffentlichenden Router Floodfill sind. Ungültige Hostnamen oder nicht reagierende, langsame oder bösartige DNS-Responder könnten für zusätzliche Angriffe verwendet werden. EDNS0 könnte weitere Aufzählungs- oder Angriffszenarien bieten. DNS könnte auch als Angriffsweg basierend auf der Lookup-Zeit dienen, um Router-zu-Router-Verbindungszeiten aufzudecken, Verbindungsgrafiken zu erstellen, den Datenverkehr zu schätzen und andere Rückschlüsse zu ziehen.

Auch die Georgia Tech Gruppe, angeführt von David Dagon, hat mehrere Bedenken hinsichtlich DNS in datenschutzfokussierten Anwendungen geäußert. DNS-Lookups werden generell von einer Low-Level-Bibliothek durchgeführt, die nicht von der Anwendung gesteuert wird. Diese Bibliotheken wurden nicht speziell für Anonymität entwickelt; bieten möglicherweise keine feinkörnige Kontrolle durch die Anwendung; und ihre Ausgabe kann fingerabdruckbar sein. Java-Bibliotheken können besonders problematisch sein, aber dies ist nicht nur ein Java-Problem. Einige Bibliotheken verwenden DNS ANY-Anfragen, die möglicherweise abgelehnt werden. All dies wird durch die weit verbreitete Präsenz von passiver DNS-Überwachung und -Abfragen, die mehreren Organisationen zur Verfügung stehen, noch besorgniserregender. Alle DNS-Überwachungen und -Angriffe sind aus der Perspektive von I2P-Routern außerhalb des Netzwerks und erfordern wenig bis gar keine I2P-Ressourcen im Netzwerk und keine Modifikation bestehender Implementierungen.

Obwohl wir die möglichen Probleme nicht vollständig durchdacht haben, scheint die Angriffsfläche groß zu sein. Es gibt andere Möglichkeiten, das Netzwerk zu enumerieren und verwandte Daten zu sammeln, aber DNS-Angriffe könnten viel einfacher, schneller und weniger nachweisbar sein.

Router-Implementierungen könnten theoretisch zu einer ausgeklügelten Drittanbieter-DNS-Bibliothek wechseln, aber das wäre ziemlich komplex, wäre eine Wartungslast und liegt weit außerhalb der Kernerfahrungen von I2P-Entwicklern.

Die unmittelbaren Lösungen, die für Java 0.9.31 implementiert wurden, beinhalteten die Behebung des Blockierungsproblems, die Erhöhung der DNS-Cache-Zeiten und die Implementierung eines negativen DNS-Caches. Natürlich reduziert die Erhöhung der Cache-Zeiten den Vorteil, Hostnamen in Routerinfos überhaupt zu haben.

Diese Änderungen sind jedoch nur kurzfristige Milderungen und beheben nicht die oben genannten grundlegenden Probleme. Daher ist die einfachste und vollständigste Lösung, Hostnamen in Router-Infos zu verbieten und somit DNS-Lookups für sie zu eliminieren.


## Design

Für den Code zur Veröffentlichung der Router-Infos haben Implementierer zwei Möglichkeiten: entweder die Konfigurationsoption für Hostnamen zu deaktivieren/entfernen oder konfigurierte Hostnamen zum Veröffentlichungszeitpunkt in IPs umzuwandeln. In jedem Fall sollten Router ihre Informationen sofort erneut veröffentlichen, wenn sich ihre IP ändert.

Für den Code zur Validierung von Router-Infos und Transportverbindungen sollten Implementierer Router-Adressen ignorieren, die Hostnamen enthalten, und die anderen veröffentlichten Adressen mit IPs verwenden, falls vorhanden. Wenn in den Router-Infos keine Adressen mit IPs enthalten sind, sollte der Router keine Verbindung zum veröffentlichten Router herstellen. In keinem Fall sollte ein Router eine DNS-Abfrage eines veröffentlichten Hostnamens durchführen, weder direkt noch über eine zugrunde liegende Bibliothek.

## Spezifikation

Ändern Sie die NTCP- und SSU-Transportspezifikationen, um anzuzeigen, dass der "host" Parameter eine IP und kein Hostname sein muss und dass Router einzelne Router-Adressen ignorieren sollten, die Hostnamen enthalten.

Dies gilt auch für die "ihost0", "ihost1" und "ihost2" Parameter in einer SSU-Adresse. Router sollten Einleitungsadressen ignorieren, die Hostnamen enthalten.


## Anmerkungen

Dieser Vorschlag behandelt nicht Hostnamen für Reseed-Hosts. Während DNS-Lookups für Reseed-Hosts viel seltener sind, könnten sie immer noch ein Problem darstellen. Falls erforderlich, kann dies einfach behoben werden, indem die Hostnamen in der fest kodierten Liste von URLs durch IPs ersetzt werden; es wären keine Spezifikations- oder Codeänderungen erforderlich.

## Migration

Dieser Vorschlag kann sofort umgesetzt werden, ohne eine schrittweise Migration, da sehr wenige Router Hostnamen veröffentlichen und diejenigen, die dies tun, den Hostnamen normalerweise nicht in allen Adressen veröffentlichen.

Router müssen nicht die veröffentlichte Version des Routers überprüfen, bevor sie entscheiden, Hostnamen zu ignorieren, und es besteht kein Bedarf für eine koordinierte Veröffentlichung oder eine gemeinsame Strategie zwischen den verschiedenen Router-Implementierungen.

Für diejenigen Router, die weiterhin Hostnamen veröffentlichen, erhalten sie weniger eingehende Verbindungen und könnten schließlich Schwierigkeiten haben, eingehende Tunnel zu erstellen.

Um die Auswirkungen weiter zu minimieren, könnten Implementierer beginnen, Router-Adressen mit Hostnamen nur für Floodfill-Router oder für Router mit einer veröffentlichten Version kleiner als 0.9.32 zu ignorieren und Hostnamen für alle Router in einer späteren Version zu ignorieren.
