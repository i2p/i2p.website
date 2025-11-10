---
title: "Opt-in Statistik-Sammlung"
number: "117"
author: "zab"
created: "2015-11-04"
lastupdated: "2015-11-04"
status: "Entwurf"
thread: "http://zzz.i2p/topics/1981"
---

## Überblick

Dieser Vorschlag betrifft ein automatisiertes, optionales Berichtssystem für Netzwerkstatistiken.

## Motivation

Derzeit gibt es mehrere Netzwerkparameter, die durch fundiertes Raten festgelegt wurden. Es wird vermutet, dass einige davon angepasst werden können, um die Gesamtleistung des Netzwerks in Bezug auf Geschwindigkeit, Zuverlässigkeit usw. zu verbessern. Ohne entsprechende Forschung ist eine Änderung jedoch sehr riskant.

## Design

Der Router unterstützt eine umfangreiche Sammlung von Statistiken, die zur Analyse netzwerkweiter Eigenschaften verwendet werden können. Was wir benötigen, ist ein automatisiertes Berichtssystem, das diese Statistiken an einem zentralen Ort sammelt. Natürlich wäre dies opt-in, da es die Anonymität erheblich beeinträchtigt. (Die datenschutzfreundlichen Statistiken werden bereits an stats.i2p gemeldet.) Als grober Anhaltspunkt wird angenommen, dass bei einem Netzwerk von 30.000 Teilnehmern eine Stichprobe von 300 berichtenden Routern ausreichend repräsentativ sein sollte.
