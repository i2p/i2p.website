---
title: "SSU2-Transport"
date: 2022-10-11
author: "zzz"
description: "SSU2-Transport"
categories: ["development"]
---

## Übersicht

I2P verwendet seit 2005 ein zensurresistentes UDP-Transportprotokoll "SSU". In 17 Jahren haben wir wenige, wenn überhaupt, Berichte darüber erhalten, dass SSU blockiert wurde. Nach heutigen Maßstäben in Bezug auf Sicherheit, Blockierungsresistenz und Leistung können wir es besser machen. Viel besser.

Deshalb haben wir zusammen mit dem [i2pd-Projekt](https://i2pd.xyz/) "SSU2" entwickelt und implementiert, ein modernes UDP-Protokoll, das nach den höchsten Standards für Sicherheit und Blockierungsresistenz ausgelegt ist. Dieses Protokoll wird SSU ersetzen.

Wir haben Verschlüsselung nach Industriestandard mit den besten Eigenschaften der UDP-Protokolle WireGuard und QUIC kombiniert, zusammen mit den Zensurresistenzfunktionen unseres TCP-Protokolls "NTCP2". SSU2 könnte eines der sichersten je entwickelten Transportprotokolle sein.

The Java I2P and i2pd teams are finishing the SSU2 transport and we will enable it for all routers in the next release. This completes our decade-long plan to upgrade all the cryptography from the original Java I2P implementation dating back to 2003. SSU2 will replace SSU, our sole remaining use of ElGamal cryptography.

- Signature types and ECDSA signatures (0.9.8, 2013)
- Ed25519 signatures and leasesets (0.9.15, 2014)
- Ed25519 routers (0.9.22, 2015)
- Destination encryption types and X25519 leasesets (0.9.46, 2020)
- Router encryption types and X25519 routers (0.9.49, 2021)

Nach der Umstellung auf SSU2 werden wir alle unsere authentifizierten und verschlüsselten Protokolle auf standardmäßige Handshakes des [Noise Protocol](https://noiseprotocol.org/) überführt haben:

- NTCP2 (0.9.36, 2018)
- ECIES-X25519-Ratchet end-to-end protocol (0.9.46, 2020)
- ECIES-X25519 tunnel build messages (1.5.0, 2021)
- SSU2 (2.0.0, 2022)

Alle I2P Noise-Protokolle verwenden die folgenden Standard-Kryptografie-Algorithmen:

- [X25519](https://en.wikipedia.org/wiki/Curve25519)
- [ChaCha20/Poly1305 AEAD](https://www.rfc-editor.org/rfc/rfc8439.html)
- [SHA-256](https://en.wikipedia.org/wiki/SHA-2)

## Ziele


- Upgrade the asymmetric cryptography to the much faster X25519
- Use standard symmetric authenticated encryption ChaCha20/Poly1305
- Improve the obfuscation and blocking resistance features of SSU
- Improve the resistance to spoofed addresses by adapting strategies from QUIC
- Improved handshake CPU efficiency
- Improved bandwidth efficiency via smaller handshakes and acknowledgements
- Improve the security of the peer test and relay features of SSU
- Improve the handling of peer IP and port changes by adapting the "connection migration" feature of QUIC
- Move away from heuristic code for packet handling to documented, algorithmic processing
- Support a gradual network transition from SSU to SSU2
- Easy extensibility using the block concept from NTCP2

## Entwurf

I2P uses multiple layers of encryption to protect traffic from attackers. The lowest layer is the transport protocol layer, used for point-to-point links between two routers. We currently have two transport protocols: NTCP2, a modern TCP protocol introduced in 2018, and SSU, a UDP protocol developed in 2005.

SSU2 ist, wie frühere I2P-Transportprotokolle, kein Allzweckkanal für Daten. Seine Hauptaufgabe besteht darin, die niedrigstufigen I2NP-Nachrichten von I2P sicher von einem router zum nächsten zu übermitteln. Jede dieser Punkt-zu-Punkt-Verbindungen bildet einen Hop in einem I2P tunnel. Höherstufige I2P-Protokolle laufen über diese Punkt-zu-Punkt-Verbindungen, um garlic messages (Garlic-Nachrichten) Ende-zu-Ende zwischen den I2P-Zielen zu übermitteln.

Die Entwicklung eines UDP-Transports stellt einzigartige und komplexe Herausforderungen dar, die in TCP-Protokollen nicht auftreten. Ein UDP-Protokoll muss Sicherheitsprobleme bewältigen, die durch Adressfälschung verursacht werden, und seine eigene Staukontrolle implementieren. Außerdem müssen alle Nachrichten fragmentiert werden, damit sie in die maximale Paketgröße (MTU) des Netzwerkpfads passen, und vom Empfänger wieder zusammengesetzt werden.

Zunächst stützten wir uns stark auf unsere bisherigen Erfahrungen mit unseren NTCP2-, SSU- und Streaming-Protokollen. Dann überprüften wir sorgfältig und übernahmen in erheblichem Umfang von zwei kürzlich entwickelten UDP-Protokollen:

- QUIC ([RFC 9000](https://www.rfc-editor.org/rfc/rfc9000.html), [RFC 9001](https://www.rfc-editor.org/rfc/rfc9001.html), [RFC 9002](https://www.rfc-editor.org/rfc/rfc9002.html))
- [WireGuard](https://www.wireguard.com/protocol/)

Die Klassifizierung und Blockierung von Protokollen durch gegnerische Angreifer im Datenpfad, etwa staatliche Firewalls, ist kein expliziter Bestandteil des Bedrohungsmodells dieser Protokolle. Für das Bedrohungsmodell von I2P ist dies jedoch ein wichtiger Aspekt, da es unsere Mission ist, gefährdeten Nutzern weltweit ein anonymes und zensurresistentes Kommunikationssystem bereitzustellen. Daher bestand ein großer Teil unserer Entwurfsarbeit darin, die aus NTCP2 und SSU gewonnenen Erkenntnisse mit den von QUIC und WireGuard unterstützten Funktionen und Sicherheitsmechanismen zu kombinieren.

## Leistung

Das I2P-Netzwerk ist eine komplexe Mischung aus unterschiedlichen routers. Es gibt zwei primäre Implementierungen, die weltweit auf Hardware laufen, die von Hochleistungsrechnern in Rechenzentren bis hin zu Raspberry Pis und Android-Smartphones reicht. Routers verwenden sowohl TCP- als auch UDP-Transporte. Obwohl die SSU2-Verbesserungen erheblich sind, erwarten wir nicht, dass sie für den Nutzer spürbar sind, weder lokal noch bei den Ende-zu-Ende-Übertragungsgeschwindigkeiten.

Hier sind einige Highlights der voraussichtlichen Verbesserungen von SSU2 im Vergleich zu SSU:

- 40% reduction in total handshake packet size
- 50% or more reduction in handshake CPU
- 90% or more reduction in ACK overhead
- 50% reduction in packet fragmentation
- 10% reduction in data phase overhead

## Übergangsplan

I2P bemüht sich, die Abwärtskompatibilität aufrechtzuerhalten, sowohl um die Netzwerkstabilität zu gewährleisten als auch um älteren routers zu ermöglichen, weiterhin nützlich und sicher zu bleiben. Es gibt jedoch Grenzen, denn Kompatibilität erhöht die Codekomplexität und den Wartungsaufwand.

Die Projekte Java I2P und i2pd werden in ihren nächsten Releases (2.0.0 und 2.44.0) Ende November 2022 SSU2 standardmäßig aktivieren. Sie haben jedoch unterschiedliche Pläne zum Deaktivieren von SSU. I2pd wird SSU sofort deaktivieren, da SSU2 gegenüber ihrer SSU-Implementierung eine enorme Verbesserung darstellt. Java I2P plant, SSU Mitte 2023 zu deaktivieren, um einen schrittweisen Übergang zu unterstützen und älteren routers Zeit für ein Upgrade zu geben.

## Zusammenfassung

Die Gründer von I2P mussten mehrere Entscheidungen hinsichtlich kryptografischer Algorithmen und Protokolle treffen. Einige dieser Entscheidungen waren besser als andere, aber zwanzig Jahre später sind die meisten in die Jahre gekommen. Natürlich wussten wir, dass das kommen würde, und wir haben das letzte Jahrzehnt damit verbracht, kryptografische Aktualisierungen zu planen und umzusetzen.

SSU2 war das letzte und zugleich komplexeste Protokoll, das wir auf unserem langen Upgrade-Pfad entwickelt haben. UDP hat sehr herausfordernde Rahmenannahmen und ein anspruchsvolles Bedrohungsmodell. Zunächst haben wir drei andere Varianten der Noise-Protokolle entworfen und eingeführt und dadurch Erfahrungen sowie ein tieferes Verständnis der Sicherheits- und Protokolldesign-Fragestellungen gewonnen.

Rechnen Sie damit, dass SSU2 in den für Ende November 2022 geplanten Versionen von i2pd und Java I2P aktiviert wird. Wenn das Update gut verläuft, wird voraussichtlich niemand einen Unterschied bemerken. Die Leistungsgewinne sind zwar erheblich, werden sich für die meisten Nutzer jedoch vermutlich nicht messen lassen.

Wie üblich empfehlen wir, auf die neue Version zu aktualisieren, sobald sie verfügbar ist. Der beste Weg, die Sicherheit aufrechtzuerhalten und dem Netzwerk zu helfen, besteht darin, die neueste Version auszuführen.
