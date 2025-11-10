---
title: "Neue I2P Routers"
date: 2025-10-16
author: "idk"
categories: ["community"]
description: "Mehrere neue Implementierungen des I2P router entstehen, darunter emissary in Rust und go-i2p in Go, die neue Möglichkeiten für Einbettung und Netzwerkdiversität bringen."
API_Translate: wahr
---

Es ist eine spannende Zeit für die I2P-Entwicklung, unsere Community wächst und es tauchen jetzt mehrere neue, voll funktionsfähige I2P router-Prototypen auf! Wir freuen uns sehr über diese Entwicklung und darauf, die Neuigkeiten mit Ihnen zu teilen.

## Wie hilft das dem Netzwerk?

Das Implementieren von I2P routers hilft uns nachzuweisen, dass unsere Spezifikationsdokumente zur Entwicklung neuer I2P routers verwendet werden können, öffnet den Code für neue Analysetools und verbessert insgesamt die Sicherheit und Interoperabilität des Netzwerks. Mehrere I2P routers bedeuten, dass potenzielle Fehler nicht einheitlich sind; ein Angriff auf einen router funktioniert möglicherweise nicht auf einem anderen router, wodurch ein Monokulturproblem vermieden wird. Die vielleicht spannendste Perspektive auf lange Sicht ist jedoch die Einbettung.

## Was ist Einbettung?

Im Kontext von I2P ist Einbettung eine Möglichkeit, einen I2P router direkt in eine andere App einzubinden, ohne einen eigenständigen router zu benötigen, der im Hintergrund läuft. Auf diese Weise können wir I2P einfacher nutzbar machen, was das Wachstum des Netzwerks erleichtert, indem die Software zugänglicher wird. Sowohl Java als auch C++ sind außerhalb ihrer eigenen Ökosysteme schwer zu verwenden; bei C++ sind fragile, handgeschriebene C-Bindings (Anbindungen) erforderlich, und im Fall von Java besteht die Schwierigkeit darin, von einer Nicht-JVM-Anwendung mit einer JVM-Anwendung zu kommunizieren.

Obwohl diese Situation in vielerlei Hinsicht ganz normal ist, bin ich der Meinung, dass sie verbessert werden kann, um I2P zugänglicher zu machen. Andere Sprachen bieten elegantere Lösungen für diese Probleme. Natürlich sollten wir stets die bestehenden Richtlinien für die Java- und C++-routers beachten und anwenden.

## Gesandter erscheint aus der Dunkelheit

Völlig unabhängig von unserem Team hat ein Entwickler namens altonen eine in Rust geschriebene Implementierung von I2P namens emissary entwickelt. Obwohl es noch recht neu ist und wir mit Rust nicht vertraut sind, hat dieses faszinierende Projekt großes Potenzial. Herzlichen Glückwunsch an altonen zur Entwicklung von emissary, wir sind sehr beeindruckt.

### Why Rust?

Der Hauptgrund, Rust zu verwenden, ist im Grunde derselbe wie der Grund, Java oder Go zu verwenden. Rust ist eine kompilierte Programmiersprache mit Speicherverwaltung und einer großen, äußerst engagierten Community. Rust bietet außerdem fortgeschrittene Funktionen zur Erstellung von Bindings für die Programmiersprache C, die möglicherweise leichter zu warten sind als in anderen Sprachen, während sie dennoch Rusts starke Speichersicherheitsmerkmale übernehmen.

### Do you want to get involved with emissary?

emissary wird auf Github von altonen entwickelt. Das Repository finden Sie unter: [altonen/emissary](https://github.com/altonen/emissary). Rust leidet außerdem unter einem Mangel an umfassenden SAMv3-Client-Bibliotheken, die mit gängigen Rust-Netzwerkbibliotheken kompatibel sind; eine SAMv3-Bibliothek zu schreiben, ist ein guter Einstieg.

## go-i2p is getting closer to completion

Seit etwa 3 Jahren arbeite ich an go-i2p und versuche, eine noch junge Bibliothek in einen vollwertigen I2P router in reinem Go, einer weiteren speichersicheren Sprache, zu verwandeln. In den letzten etwa 6 Monaten wurde es drastisch umstrukturiert, um Leistung, Zuverlässigkeit und Wartbarkeit zu verbessern.

### Why Go?

Während Rust und Go viele der gleichen Vorteile haben, ist Go in vielerlei Hinsicht deutlich einfacher zu erlernen. Seit Jahren gibt es ausgezeichnete Bibliotheken und Anwendungen für die Verwendung von I2P in der Programmiersprache Go, einschließlich der vollständigsten Implementierungen der SAMv3.3-Bibliotheken. Doch ohne einen I2P router, den wir automatisch verwalten können(z. B. einen eingebetteten router), stellt dies für Nutzer weiterhin eine Hürde dar. Das Ziel von go-i2p ist es, diese Lücke zu überbrücken und alle Stolpersteine für I2P-Anwendungsentwickler, die in Go arbeiten, zu beseitigen.

### Warum Rust?

go-i2p wird auf Github entwickelt, derzeit hauptsächlich von eyedeekay, und ist für Beiträge aus der Community unter [go-i2p](https://github.com/go-i2p/) offen. Innerhalb dieses Namensraums gibt es viele Projekte, zum Beispiel:

#### Router Libraries

Wir haben diese Bibliotheken entwickelt, um unsere I2P router Bibliotheken zu erstellen. Sie sind auf mehrere, spezialisierte Repositories aufgeteilt, um die Überprüfung zu erleichtern und sie für andere nützlich zu machen, die experimentelle, maßgeschneiderte I2P router bauen möchten.

- [go-i2p the router itself, most active right now](https://github.com/go-i2p/go-i2p)
- [common our core library for I2P datastructures](https://github.com/go-i2p/common)
- [crypto our library for cryptographic operations](https://github.com/go-i2p/crypto)
- [go-noise a library for implementing noise-based connections](https://github.com/go-i2p/go-noise)
- [noise a low-level library for using the Noise framework](https://github.com/go-i2p/noise)
- [su3 a library for manipulating su3 files](https://github.com/go-i2p/su3)

#### Client libraries

- [onramp a very convenient library for using(or combining) I2P and Tor](https://github.com/go-i2p/onramp)
- [go-sam-go an advanced, efficient, and very complete SAMv3 library](https://github.com/go-i2p/go-sam-go)

## If you don't like Go or Rust and are thinking of writing an I2P Router, what should you do?

Nun, es gibt ein ruhendes Projekt, einen [I2P router in C#](https://github.com/PeterZander/i2p-cs) zu schreiben, falls du I2P auf einer XBox ausführen möchtest. Klingt eigentlich ziemlich cool. Wenn das auch nicht dein Ding ist, könntest du es wie altonen machen und einen ganz neuen entwickeln.

### Möchten Sie sich an emissary beteiligen?

Du kannst aus jedem beliebigen Grund einen I2P router entwickeln; es ist ein freies Netzwerk, aber es hilft, zu wissen, warum. Gibt es eine Community, die du stärken möchtest, ein Tool, das deiner Meinung nach gut zu I2P passt, oder eine Strategie, die du ausprobieren möchtest? Definiere dein Ziel, um festzustellen, wo du anfangen musst und wie ein "fertiger" Zustand aussehen wird.

### Decide what language you want to do it in and why

Hier sind einige Gründe, warum Sie sich für eine Sprache entscheiden könnten:

- **C**: No need for binding-generation, supported everywhere, can be called from any language, lingua franca of modern computing
- **Typescript**: Massive community, lots of applications, services, and libraries, works with node and deno, seems like it's everywhere right now
- **D**: It's memory safe and not Rust or Go
- **Vala**: It emits C code for the target platform, combining some of the advantages of memory-safe languages with the flexibility of C
- **Python**: Everybody uses Python

Aber hier sind einige Gründe, warum du diese Sprachen vielleicht nicht wählen würdest:

- **C**: Memory management can be challenging, leading to impactful bugs
- **Typescript**: TypeScript is transpiled to JavaScript, which is interpreted and may impact performance
- **D**: Relatively small community
- **Vala**: Not a lot of underlying infrastructure in Vala, you end up using C versions of most libraries
- **Python**: It's an interpreted language which may impact performance

Es gibt Hunderte von Programmiersprachen, und wir begrüßen gepflegte I2P-Bibliotheken und routers in allen Sprachen. Wägen Sie die Kompromisse klug ab und legen Sie los.

## go-i2p kommt der Fertigstellung näher

Egal, ob du in Rust, Go, Java, C++ oder einer anderen Sprache arbeiten möchtest, melde dich bei uns im Irc2P-Kanal #i2p-dev. Fang dort an, und wir führen dich in router-spezifische Kanäle ein. Außerdem sind wir auf ramble.i2p unter f/i2p, auf reddit unter r/i2p sowie auf GitHub und git.idk.i2p vertreten. Wir freuen uns darauf, bald von dir zu hören.
