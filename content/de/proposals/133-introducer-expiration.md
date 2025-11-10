---
title: "Introducer-Verfall"
number: "133"
author: "zzz"
created: "2017-02-05"
lastupdated: "2017-08-09"
status: "Geschlossen"
thread: "http://zzz.i2p/topics/2230"
target: "0.9.30"
implementedin: "0.9.30"
---

## Übersicht

Dieser Vorschlag bezieht sich auf die Verbesserung der Erfolgsrate bei Einführungen. Siehe
[TRAC-TICKET]_.


## Motivation

Einführer verfallen nach einer bestimmten Zeit, aber diese Info wird nicht in der
[RouterInfo]_ veröffentlicht. Router müssen derzeit Heuristiken verwenden, um zu schätzen, wann ein
Einführer nicht mehr gültig ist.


## Design

In einer SSU [RouterAddress]_, die Einführer enthält, kann der Herausgeber optional
Ablaufzeiten für jeden Einführer angeben.


## Spezifikation

.. raw:: html

  {% highlight lang='dataspec' %}
iexp{X}={nnnnnnnnnn}

  X :: Die Einführer-Nummer (0-2)

  nnnnnnnnnn :: Die Zeit in Sekunden (nicht ms) seit der Epoche.
{% endhighlight %}

Hinweise
`````
* Jeder Ablauf muss größer sein als das Veröffentlichungsdatum der [RouterInfo]_
  und weniger als 6 Stunden nach dem Veröffentlichungsdatum der RouterInfo.

* Herausgeber von Routern und Einführern sollten versuchen, den Einführer bis zum Ablauf gültig zu halten,
  können dies jedoch nicht garantieren.

* Router sollten einen veröffentlichten Einführer nach dessen Ablauf nicht mehr verwenden.

* Die Einführerabläufe befinden sich in der [RouterAddress]_ Zuordnung.
  Sie sind nicht das (derzeit ungenutzte) 8-Byte-Ablauf-Feld in der [RouterAddress]_.

Beispiel: ``iexp0=1486309470``


## Migration

Keine Probleme. Die Implementierung ist optional.
Abwärtskompatibilität ist sichergestellt, da ältere Router unbekannte Parameter ignorieren.



## Referenzen

.. [RouterAddress]
    {{ ctags_url('RouterAddress') }}

.. [RouterInfo]
    {{ ctags_url('RouterInfo') }}

.. [TRAC-TICKET]
    http://{{ i2pconv('trac.i2p2.i2p') }}/ticket/1352
