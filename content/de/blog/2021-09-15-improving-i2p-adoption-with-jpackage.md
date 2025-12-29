---
title: "Verbesserung der I2P-Verbreitung und des Onboardings mit Jpackage, I2P-Zero"
date: 2021-09-15
slug: "improving-i2p-adoption-and-onboarding-using-jpackage-i2p-zero"
author: "idk"
description: "Vielseitige und neu entstehende Möglichkeiten, I2P in Ihre Anwendung zu installieren und einzubetten"
categories: ["general"]
API_Translate: wahr
---

Die meiste Zeit seiner Existenz war I2P eine Anwendung, die mit Hilfe einer bereits auf der Plattform installierten Java Virtual Machine (JVM; Java‑virtuelle Maschine) läuft. Das war zwar schon immer die übliche Art, Java‑Anwendungen zu verteilen, führt für viele jedoch zu einem komplizierten Installationsvorgang. Komplizierter wird es dadurch, dass die „richtige Antwort“ darauf, wie man I2P auf einer bestimmten Plattform leicht installierbar macht, nicht unbedingt dieselbe ist wie auf einer anderen Plattform. So lässt sich I2P auf Debian‑ und Ubuntu‑basierten Betriebssystemen mit Standardwerkzeugen recht einfach installieren, weil wir die benötigten Java‑Komponenten in unserem Paket einfach als "Required" deklarieren können; unter Windows oder OSX gibt es jedoch kein entsprechendes System, das es uns ermöglicht sicherzustellen, dass eine kompatible Java‑Version installiert ist.

Die naheliegende Lösung wäre, die Java-Installation selbst zu verwalten, aber das war früher an sich ein Problem und lag außerhalb des Zuständigkeitsbereichs von I2P. In neueren Java-Versionen ist jedoch ein neuer Satz von Optionen aufgetaucht, der das Potenzial hat, dieses Problem für viele Java-Software zu lösen. Dieses spannende Werkzeug heißt **"Jpackage."**

## I2P-Zero und I2P-Installation ohne Abhängigkeiten

Der erste sehr erfolgreiche Versuch, ein abhängigkeitsfreies I2P-Paket zu erstellen, war I2P-Zero, das ursprünglich vom Monero-Projekt für die Verwendung mit der Monero-Kryptowährung geschaffen wurde. Dieses Projekt hat uns sehr begeistert, weil es erfolgreich einen universellen I2P router entwickelt hat, der sich leicht mit einer I2P-Anwendung bündeln ließ. Insbesondere auf Reddit äußern viele ihre Vorliebe für die einfache Einrichtung eines I2P-Zero router.

Das hat uns wirklich gezeigt, dass ein I2P-Paket ohne Abhängigkeiten, das sich mit modernen Java-Tools leicht installieren ließ, möglich ist, aber der Anwendungsfall von I2P-Zero war ein wenig anders als unserer. Es eignet sich am besten für eingebettete Anwendungen, die einen I2P router benötigen, den sie über seinen praktischen Steuerport auf Port "8051" leicht bedienen können. Unser nächster Schritt wäre, die Technologie an die Allzweck-I2P-Anwendung anzupassen.

## Änderungen der Anwendungssicherheit in OSX betreffen den I2P-IzPack-Installer

Das Problem wurde in neueren Versionen von Mac OSX dringlicher, in denen es nicht mehr ohne Weiteres möglich ist, den "Classic"-Installer zu verwenden, der im .jar-Format vorliegt. Dies liegt daran, dass die Anwendung nicht von Apple "notarisiert" ist und als Sicherheitsrisiko gilt. **Allerdings**, Jpackage kann eine .dmg-Datei erzeugen, die von Apple notarisiert werden kann, wodurch unser Problem bequem gelöst wird.

Das neue I2P-.dmg-Installationsprogramm, erstellt von Zlatinb, macht die Installation von I2P unter OSX so einfach wie nie zuvor: Es erfordert nicht länger, dass Nutzer Java selbst installieren, und verwendet die standardmäßigen OSX-Installationswerkzeuge in der vorgesehenen Weise. Das neue .dmg-Installationsprogramm macht das Einrichten von I2P auf Mac OSX einfacher als je zuvor.

Lade das [dmg](https://geti2p.net/en/download/mac) herunter

## Das I2P der Zukunft ist einfach zu installieren

Eines der Dinge, die ich von Nutzern am häufigsten höre, ist, dass I2P, wenn es Verbreitung finden will, für Menschen einfach zu benutzen sein muss. Viele von ihnen wünschen sich eine "Tor-Browser-ähnliche" Benutzererfahrung, um viele bekannte Redditors zu zitieren oder zu paraphrasieren. Die Installation sollte keine komplizierten und fehleranfälligen "Post-Installation"-Schritte erfordern. Viele neue Nutzer sind nicht darauf vorbereitet, sich umfassend und vollständig mit ihrer Browserkonfiguration auseinanderzusetzen. Um dieses Problem anzugehen, haben wir das I2P Profile Bundle erstellt, das Firefox so konfiguriert hat, dass es für I2P automatisch "einfach funktioniert". Im Laufe der Weiterentwicklung hat es Sicherheitsfunktionen hinzugefügt und die Integration mit I2P selbst verbessert. In seiner neuesten Version bündelt es **auch** einen vollständigen, Jpackage-basierten I2P Router. Das I2P Firefox Profile ist jetzt eine vollwertige Distribution von I2P für Windows, wobei die einzige verbleibende Abhängigkeit Firefox selbst ist. Dies sollte ein beispielloses Maß an Komfort für I2P-Nutzer unter Windows bieten.

Laden Sie das [Installationsprogramm](https://geti2p.net/en/download#windows) herunter
