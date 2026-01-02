---
title: "Tunnel-Bandbreitenparameter"
number: "168"
author: "zzz"
created: "2024-07-31"
lastupdated: "2024-12-10"
status: "Geschlossen"
thread: "http://zzz.i2p/topics/3652"
target: "0.9.65"
toc: true
---

## HINWEIS

Dieser Vorschlag wurde genehmigt und ist nun in der
[Tunnel Creation ECIES specification](/docs/specs/implementation/#tunnel-creation-ecies) ab API 0.9.65 enthalten.
Es gibt noch keine bekannten Implementierungen; Implementierungsdaten / API-Versionen sind noch festzulegen.


## Überblick

Da wir die Leistung des Netzwerks in den letzten Jahren mit neuen Protokollen, Verschlüsselungsarten und Verbesserungen der Staukontrolle erhöht haben, werden schnellere Anwendungen wie Video-Streaming möglich.
Diese Anwendungen erfordern hohe Bandbreite an jedem Knotenpunkt in ihren Client-Tunneln.

Teilnehmende Router haben jedoch keine Informationen darüber, wie viel Bandbreite ein Tunnel verwenden wird, wenn sie eine Tunnelaufbaunachricht erhalten.
Sie können einen Tunnel nur akzeptieren oder ablehnen, basierend auf der aktuellen Gesamtbandbreite, die von allen teilnehmenden Tunneln genutzt wird, und dem Gesamtbandbreitenlimit für teilnehmende Tunnel.

Anfragende Router haben ebenfalls keine Informationen darüber, wie viel Bandbreite an jedem Knotenpunkt verfügbar ist.

Außerdem haben Router derzeit keine Möglichkeit, eingehenden Verkehr auf einem Tunnel zu begrenzen.
Dies wäre während Überlastungen oder DDoS-Angriffen auf einen Dienst sehr nützlich.

Dieser Vorschlag adressiert diese Probleme durch Hinzufügen von Bandbreitenparametern zu den Tunnelaufbauanforderungs- und Antwortnachrichten.


## Design

Fügen Sie Bandbreitenparameter zu den Datensätzen in ECIES-Tunnelaufbaunachrichten (siehe [Tunnel Creation ECIES specification](/docs/specs/implementation/#tunnel-creation-ecies)) im Mapping-Feld für Tunnelaufbauoptionen hinzu. Verwenden Sie kurze Parameternamen, da der verfügbare Platz für das Optionsfeld begrenzt ist.
Tunnelaufbaunachrichten haben eine feste Größe, sodass die Nachrichten dadurch nicht größer werden.


## Spezifikation

Aktualisieren Sie die [ECIES-Tunnelaufbaunachrichtenspezifikation](/docs/specs/implementation/#tunnel-creation-ecies)
wie folgt:

Für sowohl lange als auch kurze ECIES-Aufbau-Datensätze:

### Aufbauanfrage-Optionen

Die folgenden drei Optionen können im Mapping-Feld für Tunnelaufbauoptionen des Datensatzes festgelegt werden:
Ein anfragender Router kann eine, alle oder keine davon einschließen.

- m := minimale Bandbreite, die für diesen Tunnel erforderlich ist (KBps positive Ganzzahl als Zeichenkette)
- r := angeforderte Bandbreite für diesen Tunnel (KBps positive Ganzzahl als Zeichenkette)
- l := Bandbreitengrenze für diesen Tunnel; nur an IBGW gesendet (KBps positive Ganzzahl als Zeichenkette)

Einschränkung: m <= r <= l

Der teilnehmende Router sollte den Tunnel ablehnen, wenn "m" angegeben ist und er nicht mindestens so viel Bandbreite bereitstellen kann.

Anfrageoptionen werden an jeden Teilnehmer im entsprechenden verschlüsselten Aufbauanfrage-Datensatz gesendet und sind für andere Teilnehmer nicht sichtbar.


### Aufbauantwortoption

Die folgende Option kann im Mapping-Feld für Tunnelaufbauantwortoptionen des Datensatzes festgelegt werden,
wenn die Antwort ANGENOMMEN ist:

- b := verfügbare Bandbreite für diesen Tunnel (KBps positive Ganzzahl als Zeichenkette)

Der teilnehmende Router sollte dies einbeziehen, wenn entweder "m" oder "r" in der Aufbaunachricht angegeben war. Der Wert sollte mindestens dem angegebenen "m"-Wert entsprechen, aber kann weniger oder mehr als der angegebene "r"-Wert sein.

Der teilnehmende Router sollte versuchen, mindestens so viel Bandbreite für den Tunnel zu reservieren und bereitzustellen, dies ist jedoch nicht garantiert.
Router können Bedingungen in 10 Minuten nicht vorhersagen, und
teilnehmender Verkehr hat geringere Priorität als der eigene Verkehr und die Tunnel eines Routers.

Router können bei Bedarf auch verfügbare Bandbreite überzuteilen, und das ist wahrscheinlich wünschenswert, da andere Knoten im Tunnel ihn ablehnen könnten.

Aus diesen Gründen sollte die Antwort des teilnehmenden Routers
als Zusicherung nach bestem Bemühen, aber nicht als Garantie behandelt werden.

Antwortoptionen werden an den anfragenden Router im entsprechenden verschlüsselten Aufbauantwort-Datensatz gesendet und sind für andere Teilnehmer nicht sichtbar.


## Implementierungsnotizen

Bandbreitenparameter sind wie bei den teilnehmenden Routern auf Tunnelschicht zu sehen,
d. h. die Anzahl der festen 1-KB-Tunnelnachrichten pro Sekunde.
Transport-Overhead (NTCP2 oder SSU2) ist nicht enthalten.

Diese Bandbreite kann viel mehr oder weniger sein als die Bandbreite, die beim Client gesehen wird.
Tunnelnachrichten enthalten erheblichen Overhead, einschließlich Overhead von höheren Schichten
einschließlich Ratchet und Streaming. Unregelmäßige kleine Nachrichten wie Streaming-Acks
werden jeweils auf 1 KB erweitert.
Jedoch kann die gzip-Kompression auf der I2CP-Schicht die Bandbreite erheblich reduzieren.

Die einfachste Implementierung beim anfragenden Router besteht darin, die durchschnittlichen, minimalen und/oder maximalen Bandbreiten der aktuellen Tunnel im Pool zu verwenden, um die Werte zu berechnen, die in der Anfrage angegeben werden sollen.
Komplexere Algorithmen sind möglich und liegen im Ermessen des Implementierers.

Es sind derzeit keine I2CP- oder SAM-Optionen definiert, mit denen der Client dem Router mitteilen kann, welche Bandbreite erforderlich ist, und hier werden keine neuen Optionen vorgeschlagen.
Optionen können bei Bedarf später definiert werden.

Implementierungen können verfügbare Bandbreite oder andere Daten, Algorithmen, lokale Richtlinien oder lokale Konfiguration verwenden, um den in der Aufbauantwort zurückgegebenen Bandbreitenwert zu berechnen. Nicht durch diesen Vorschlag spezifiziert.

Dieser Vorschlag erfordert, dass eingehende Gateways bei Anforderung durch die "l"-Option eine Drosselung pro Tunnel implementieren.
Es erfordert nicht, dass andere teilnehmende Knoten irgendeine Art von Drosselung pro Tunnel oder globaler Drosselung implementieren, oder einen bestimmten Algorithmus oder eine Implementierung spezifizieren, falls vorhanden.

Dieser Vorschlag erfordert auch nicht, dass Client-Router den Verkehr auf den von der teilnehmenden Station zurückgegebenen "b"-Wert drosseln, und je nach Anwendung
ist das möglicherweise nicht möglich, insbesondere für eingehende Tunnel.

Dieser Vorschlag betrifft nur Tunnel, die vom Ursprungsrouter erstellt wurden. Es ist keine Methode definiert, um Bandbreite für "entferntere" Tunnel anzufordern oder zuzuweisen, die vom Besitzer des anderen Endes einer End-to-End-Verbindung erstellt wurden.


## Sicherheitsanalyse

Client-Fingerprinting oder -Korrelation kann basierend auf Anfragen möglich sein.
Der Client (Ursprungs-) Router möchte möglicherweise die "m"- und "r"-Werte randomisieren, anstatt denselben Wert an jeden Knoten zu senden; oder eine begrenzte Anzahl von Werten senden, die Bandbreiten-"Buckets" darstellen, oder eine Kombination aus beidem.

Überallokation DDoS: Während es möglicherweise jetzt möglich ist, einen Router anzugreifen, indem man eine große Anzahl von Tunneln durch ihn hindurchbaut und nutzt, macht dieser Vorschlag es arguably wesentlich einfacher, indem man einfach einen oder mehrere Tunnel mit großen Bandbreitenanfragen anfordert.

Implementierungen können und sollten eine oder mehrere der folgenden Strategien
verwenden, um dieses Risiko zu mindern:

- Überallokation der verfügbaren Bandbreite
- Begrenzung der Zuteilung pro Tunnel auf einen Prozentsatz der verfügbaren Bandbreite
- Begrenzung der Erhöhungsgeschwindigkeit der zugeteilten Bandbreite
- Begrenzung der Erhöhungsgeschwindigkeit der genutzten Bandbreite
- Begrenzung der zugeteilten Bandbreite für einen Tunnel, wenn sie nicht früh in der Lebensdauer eines Tunnels genutzt wird (use it or lose it)
- Nachverfolgung der durchschnittlichen Bandbreite pro Tunnel
- Nachverfolgung der angeforderten vs. tatsächlich genutzten Bandbreite pro Tunnel


## Kompatibilität

Keine Probleme. Alle bekannten Implementierungen ignorieren derzeit das Mapping-Feld in Aufbaunachrichten und überspringen korrekt ein nicht leeres Optionsfeld.


## Migration

Implementierungen können jederzeit Unterstützung hinzufügen, es ist keine Koordination erforderlich.

Da derzeit keine API-Version definiert ist, in der Unterstützung für diesen Vorschlag erforderlich ist,
sollten Router auf eine "b" Antwort prüfen, um die Unterstützung zu bestätigen.


