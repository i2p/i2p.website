---
title: "Bidirektionale Tunnel"
number: "119"
author: "original"
created: "2016-01-07"
lastupdated: "2016-01-07"
status: "Needs-Research"
thread: "http://zzz.i2p/topics/2041"
---

## Übersicht

Dieser Vorschlag betrifft die Implementierung von bidirektionalen Tunneln in I2P.

## Motivation

i2pd wird vorerst bidirektionale Tunnel einführen, die nur über andere i2pd-Router aufgebaut werden. Für das Netzwerk erscheinen sie als gewöhnliche Eingangs- und Ausgangstunnel.

## Design

### Ziele

1. Reduzierung des Netzwerk- und CPU-Verbrauchs durch Verringerung der Anzahl von TunnelBuild-Nachrichten
2. Möglichkeit, sofort zu wissen, ob ein Teilnehmer weggegangen ist
3. Genauere Profilierung und Statistiken
4. Nutzung anderer Darknets als Zwischenpeers

### Tunnelmodifikationen

TunnelBuild
```````````
Tunnel werden auf die gleiche Weise wie Eingangstunnel gebaut. Eine Antwortnachricht ist nicht erforderlich. Es gibt einen speziellen Teilnehmertyp, der als "Eingang" bezeichnet wird und durch eine Flagge markiert, sowohl als IBGW als auch als OBEP dient. Die Nachricht hat dasselbe Format wie VaribaleTunnelBuild, aber ClearText enthält verschiedene Felder::

    in_tunnel_id
    out_tunnel_id
    in_next_tunnel_id
    out_next_tunnel_id
    in_next_ident
    out_next_ident
    layer_key, iv_key

Es wird auch ein Feld enthalten, das erwähnt, zu welchem Darknet der nächste Peer gehört, sowie einige zusätzliche Informationen, falls es sich nicht um I2P handelt.

TunnelTermination
`````````````````
Wenn ein Peer weggehen möchte, erstellt er TunnelTermination-Nachrichten, verschlüsselt sie mit dem Layer-Key und sendet sie in "In"-Richtung. Wenn ein Teilnehmer eine solche Nachricht erhält, verschlüsselt er sie erneut mit seinem Layer-Key und sendet sie an den nächsten Peer. Sobald eine Nachricht den Tunnelbesitzer erreicht, beginnt dieser, Peer für Peer zu entschlüsseln, bis er die unverschlüsselte Nachricht erhält. Er findet heraus, welcher Peer weggegangen ist, und beendet den Tunnel.
