---
title: "Ihr I2P-Netzwerk beschleunigen"
date: 2019-07-27
author: "mhatta"
description: "Ihr I2P‑Netzwerk beschleunigen"
categories: ["tutorial"]
---

*Dieser Beitrag wurde direkt aus Material adaptiert, das ursprünglich für mhattas* [Medium-Blog](https://medium.com/@mhatta/speeding-up-your-i2p-network-c08ec9de225d) *.* *Er verdient die Anerkennung für den ursprünglichen Beitrag (OP). Es wurde an einigen Stellen aktualisiert, wo* *auf alte Versionen von I2P als aktuell verwiesen wurde, und einer leichten* *Überarbeitung unterzogen. -idk*

Direkt nach dem Start wird I2P oft als ein wenig langsam wahrgenommen. Das stimmt, und wir wissen alle, warum: Von Natur aus fügt [garlic routing](https://en.wikipedia.org/wiki/Garlic_routing) der vertrauten Nutzung des Internets zusätzlichen Overhead hinzu, um Ihre Privatsphäre zu ermöglichen; das bedeutet jedoch, dass Ihre Daten bei vielen oder den meisten I2P-Diensten standardmäßig 12 Hops durchlaufen müssen.

![Analyse von Tools für die Online-Anonymität](https://www.researchgate.net/publication/289531182_An_analysis_of_tools_for_online_anonymity)

Außerdem wurde I2P, anders als Tor, in erster Linie als geschlossenes Netzwerk konzipiert. Sie können problemlos [eepsites](https://medium.com/@mhatta/how-to-set-up-untraceable-websites-eepsites-on-i2p-1fe26069271d) oder andere Ressourcen innerhalb von I2P aufrufen, aber der Zugriff auf [Clearnet](https://en.wikipedia.org/wiki/Clearnet_(networking))‑Websites über I2P ist nicht vorgesehen. Es gibt einige wenige I2P-"outproxies" (Proxy-Server für den Zugriff auf das Clearnet), ähnlich den Exit-Knoten von [Tor](https://en.wikipedia.org/wiki/Tor_(anonymity_network)), um auf das Clearnet zuzugreifen, aber die meisten davon sind sehr langsam, da der Weg ins Clearnet faktisch *ein weiterer* Hop in der bereits aus sechs Hops hinein und sechs Hops hinaus bestehenden Verbindung ist.

Bis vor einigen Versionen war dieses Problem noch schwieriger zu bewältigen, da viele I2P router-Nutzer Schwierigkeiten hatten, die Bandbreiteneinstellungen für ihre routers zu konfigurieren. Wenn alle, die es können, sich die Zeit nehmen, ihre Bandbreiteneinstellungen korrekt einzustellen, verbessern sie nicht nur Ihre Verbindung, sondern auch das I2P-Netzwerk als Ganzes.

## Anpassen der Bandbreitenbegrenzungen

Da I2P ein Peer-to-Peer-Netzwerk ist, müssen Sie einen Teil Ihrer Netzwerkbandbreite mit anderen Peers teilen. Sie können festlegen, wie viel, in "I2P Bandwidth Configuration" ("Configure Bandwidth"-Schaltfläche im Abschnitt "Applications and Configuration" der I2P Router Console, oder http://localhost:7657/config).

![I2P-Bandbreitenkonfiguration](https://geti2p.net/images/blog/bandwidthmenu.png)

Wenn Sie ein Limit für die freigegebene Bandbreite von 48 KBps sehen, was sehr niedrig ist, dann haben Sie Ihre freigegebene Bandbreite möglicherweise nicht von der Voreinstellung aus angepasst. Wie der ursprüngliche Autor des Materials, auf dem dieser Blogbeitrag basiert, anmerkte, hat I2P ein standardmäßiges Limit für die freigegebene Bandbreite, das sehr niedrig ist, bis Sie es anpassen, um Probleme mit Ihrer Verbindung zu vermeiden.

Da jedoch viele Nutzer möglicherweise nicht genau wissen, welche Bandbreiteneinstellungen sie anpassen sollten, führte die [I2P 0.9.38 release](https://geti2p.net/en/download) einen Assistenten für die Erstinstallation ein. Er enthält einen Bandbreitentest, der automatisch (dank M-Labs [NDT](https://www.measurementlab.net/tests/ndt/)) die Bandbreite ermittelt und die Bandbreiteneinstellungen von I2P entsprechend anpasst.

Wenn Sie den Assistenten erneut ausführen möchten, zum Beispiel nach einem Wechsel Ihres Internetdienstanbieters oder weil Sie I2P vor Version 0.9.38 installiert haben, können Sie ihn über den Link 'Setup' auf der Seite 'Help & FAQ' erneut starten oder den Assistenten einfach direkt unter http://localhost:7657/welcome aufrufen.

![Kannst du „Setup“ finden?](https://geti2p.net/images/blog/sidemenu.png)

Die Verwendung des Assistenten ist unkompliziert; klicken Sie einfach immer wieder auf "Next". Manchmal sind die von M-Lab ausgewählten Messserver nicht erreichbar, und der Test schlägt fehl. In einem solchen Fall klicken Sie auf "Previous" (verwenden Sie nicht die "back"-Schaltfläche Ihres Webbrowsers), dann versuchen Sie es erneut.

![Ergebnisse des Bandbreitentests](https://geti2p.net/images/blog/bwresults.png)

## I2P dauerhaft betreiben

Selbst nachdem Sie die Bandbreite angepasst haben, kann Ihre Verbindung dennoch langsam sein. Wie gesagt, I2P ist ein P2P‑Netzwerk. Es dauert eine Weile, bis Ihr I2P router von anderen Peers entdeckt und in das I2P‑Netzwerk integriert wird. Wenn Ihr router nicht lange genug online ist, um gut integriert zu werden, oder wenn Sie zu oft nicht ordnungsgemäß herunterfahren, bleibt das Netzwerk relativ langsam. Andererseits gilt: Je länger Sie Ihren I2P router ununterbrochen laufen lassen, desto schneller und stabiler wird Ihre Verbindung, und mehr von Ihrem Bandbreitenanteil wird im Netzwerk genutzt.

Allerdings können viele Menschen ihren I2P router möglicherweise nicht durchgängig in Betrieb halten. In einem solchen Fall können Sie den I2P router dennoch auf einem entfernten Server wie einem VPS betreiben und dann SSH-Portweiterleitung verwenden.
