---
title: "Stau-Caps"
number: "162"
author: "dr|z3d, idk, orignal, zzz"
created: "2023-01-24"
lastupdated: "2023-02-01"
status: "Offen"
thread: "http://zzz.i2p/topics/3516"
target: "0.9.59"
toc: true
---

## Übersicht

Fügen Sie Staumelder zu den veröffentlichten Router-Infos (RI) hinzu.




## Motivation

Bandbreiten-"Caps" (Fähigkeiten) zeigen geteilte Bandbreitengrenzen und Erreichbarkeit an, jedoch nicht den Stauzustand.
Ein Stau-Indikator hilft Routern, den Versuch zu vermeiden, über einen überlasteten Router zu bauen,
was zu mehr Stau und einer verringerten Tunnelaufbau-Erfolgsquote führt.



## Design

Definieren Sie neue Caps, um verschiedene Stau- oder Kapazitätsprobleme anzuzeigen.
Diese werden in den obersten RI-Caps sein, nicht in den Adress-Caps.


### Stau-Definition

Stau bedeutet im Allgemeinen, dass es unwahrscheinlich ist, dass der Peer
einen Tunnelbauantrag erhält und akzeptiert.
Wie man Staulevel definiert oder klassifiziert, ist implementierungsspezifisch.

Implementierungen können eines oder mehrere der folgenden Punkte berücksichtigen:

- An oder nahe Bandbreitengrenzen
- An oder nahe maximal beteiligten Tunneln
- An oder nahe maximalen Verbindungen bei einem oder mehreren Transporten
- Über der Schwelle für Warteschlangentiefe, Latenz oder CPU-Auslastung; interne Warteschlangenüberlauf
- Basisplattform/ OS CPU- und Speicherfähigkeiten
- Wahrgenommenes Netzwerkkongestion
- Netzwerkstatus wie Firewall oder symmetrisches NAT oder verborgen oder Proxied
- Konfiguriert, um keine Tunnel zu akzeptieren

Der Stauzustand sollte auf einem Durchschnitt der Bedingungen
über mehrere Minuten basieren, nicht auf einer Momentaufnahme.



## Spezifikation

Aktualisieren Sie [NETDB](/docs/how/network-database/) wie folgt:


```text
D: Mittlerer Stau, oder ein leistungsschwacher Router (z.B. Android, Raspberry Pi)
     Andere Router sollten diese Router in ihrem Profil als mit eingeschränkter
     Tunnelkapazität betrachten.

  E: Hoher Stau, dieser Router ist nahe oder an irgendeinem Limit,
     und lehnt die meisten Tunnelanforderungen ab oder lässt sie fallen.
     Wenn dieses RI in den letzten 15 Minuten veröffentlicht wurde, sollten andere Router
     die Kapazität dieses Routers stark herabsetzen oder einschränken.
     Wenn dieses RI älter als 15 Minuten ist, wie 'D' behandeln.

  G: Dieser Router lehnt vorübergehend oder dauerhaft alle Tunnel ab.
     Versuchen Sie nicht, einen Tunnel über diesen Router zu bauen,
     bis ein neues RI ohne 'G' empfangen wird.
```

Für Konsistenz sollten Implementierungen jedes Stau-Cap
am Ende hinzufügen (nach R oder U).



## Sicherheitsanalyse

Alle veröffentlichten Peer-Informationen können nicht vertraut werden.
Caps können wie alles andere im Router Info gefälscht sein.
Wir verwenden niemals etwas im Router Info, um die wahrgenommene Kapazität eines Routers zu erhöhen.

Die Veröffentlichung von Stau-Indikatoren, die Peers anweisen, diesen Router zu meiden, ist von Natur aus
viel sicherer als permissive oder Kapazitätsindikatoren, die mehr Tunnel verlangen.

Die aktuellen Bandbreitenkapazitätsindikatoren (L-P, X) werden nur verwendet, um
Router mit sehr geringer Bandbreite zu meiden. Das "U" (unerreichbar) Cap hat eine ähnliche Wirkung.

Jeder veröffentlichte Stau-Indikator sollte die gleiche Wirkung haben wie
das Ablehnen oder Fallenlassen eines Tunnelbauantrags, mit ähnlichen Sicherheitseigenschaften.



## Anmerkungen

Peers dürfen 'D'-Router nicht vollständig meiden, sie sollten sie nur herabsetzen.

Es muss darauf geachtet werden, 'E'-Router nicht vollständig zu meiden,
damit, wenn das gesamte Netzwerk unter Stau steht und 'E' veröffentlicht,
nicht alles zusammenbricht.

Router können unterschiedliche Strategien verwenden, welche Arten von Tunneln sie durch 'D'- und 'E'-Router bauen,
zum Beispiel Erkundungs- vs. Client-Tunnel oder hohe vs. niedrige Bandbreiten-Client-Tunnel.

Router sollten wahrscheinlich standardmäßig keinen Stau-Cap bei Start oder Herunterfahren veröffentlichen,
selbst wenn ihr Netzwerkstatus unbekannt ist, um eine Neustarterkennung durch Peers zu verhindern.




## Kompatibilität

Keine Probleme, alle Implementierungen ignorieren unbekannte Caps.


## Migration

Implementierungen können jederzeit Unterstützung hinzufügen, keine Koordination erforderlich.

Vorläufiger Plan:
Veröffentliche Caps in 0.9.58 (April 2023);
auf veröffentlichte Caps in 0.9.59 (Juli 2023) reagieren.



## Verweise

* [NETDB](/docs/how/network-database/)
