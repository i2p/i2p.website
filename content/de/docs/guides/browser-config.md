---
title: "Web-Browser-Konfiguration"
description: "Konfigurieren Sie gängige Browser zur Verwendung der HTTP/HTTPS-Proxys von I2P auf Desktop und Android"
slug: "browser-config"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

Diese Anleitung zeigt, wie man gängige Browser so konfiguriert, dass sie Datenverkehr über den integrierten HTTP-Proxy von I2P senden. Sie behandelt Safari, Firefox und Chrome/Chromium-Browser mit detaillierten Schritt-für-Schritt-Anleitungen.

**Wichtige Hinweise**:

- Der Standard-HTTP-Proxy von I2P lauscht auf `127.0.0.1:4444`.
- I2P schützt den Datenverkehr innerhalb des I2P-Netzwerks (.i2p-Seiten).
- Stellen Sie sicher, dass Ihr I2P-router läuft, bevor Sie Ihren Browser konfigurieren.

## Safari (macOS)

Safari verwendet die systemweiten Proxy-Einstellungen unter macOS.

### Step 1: Open Network Settings

1. Öffne **Safari** und gehe zu **Safari → Einstellungen** (oder **Preferences**)
2. Klicke auf den Tab **Erweitert**
3. Im Abschnitt **Proxys** klicke auf **Einstellungen ändern...**

Dadurch werden die Netzwerkeinstellungen deines Mac geöffnet.

![Safari Erweiterte Einstellungen](/images/guides/browser-config/accessi2p_1.png)

### Schritt 1: Netzwerkeinstellungen öffnen

1. Aktivieren Sie in den Netzwerkeinstellungen das Kontrollkästchen für **Web Proxy (HTTP)**
2. Geben Sie Folgendes ein:
   - **Web Proxy Server**: `127.0.0.1`
   - **Port**: `4444`
3. Klicken Sie auf **OK**, um Ihre Einstellungen zu speichern

![Safari Proxy-Konfiguration](/images/guides/browser-config/accessi2p_2.png)

Sie können jetzt `.i2p`-Seiten in Safari durchsuchen!

**Hinweis**: Diese Proxy-Einstellungen wirken sich auf alle Anwendungen aus, die die macOS-Systemproxys verwenden. Erwägen Sie, ein separates Benutzerkonto zu erstellen oder einen anderen Browser exklusiv für I2P zu verwenden, wenn Sie das I2P-Browsing isolieren möchten.

## Firefox (Desktop)

Firefox hat eigene Proxy-Einstellungen unabhängig vom System, was es ideal für dediziertes I2P-Browsing macht.

### Schritt 2: HTTP-Proxy konfigurieren

1. Klicken Sie auf die **Menüschaltfläche** (☰) oben rechts
2. Wählen Sie **Einstellungen**

![Firefox Einstellungen](/images/guides/browser-config/accessi2p_3.png)

### Step 2: Find Proxy Settings

1. Geben Sie im Suchfeld der Einstellungen **"proxy"** ein
2. Scrollen Sie zu **Netzwerkeinstellungen**
3. Klicken Sie auf die Schaltfläche **Einstellungen...**

![Firefox Proxy-Suche](/images/guides/browser-config/accessi2p_4.png)

### Schritt 1: Einstellungen öffnen

1. Wählen Sie **Manuelle Proxy-Konfiguration**
2. Geben Sie Folgendes ein:
   - **HTTP-Proxy**: `127.0.0.1` **Port**: `4444`
3. Lassen Sie **SOCKS-Host** leer (außer Sie benötigen ausdrücklich einen SOCKS-Proxy)
4. Aktivieren Sie **DNS über Proxy auflösen (bei Verwendung von SOCKS)** nur bei Verwendung eines SOCKS-Proxys
5. Klicken Sie auf **OK**, um zu speichern

![Firefox Manuelle Proxy-Konfiguration](/images/guides/browser-config/accessi2p_5.png)

Sie können nun `.i2p`-Sites in Firefox durchsuchen!

**Tipp**: Erwägen Sie die Erstellung eines separaten Firefox-Profils, das ausschließlich für das I2P-Browsing verwendet wird. Dies hält Ihr I2P-Browsing von Ihrem regulären Browsing getrennt. Um ein Profil zu erstellen, geben Sie `about:profiles` in die Firefox-Adressleiste ein.

## Chrome / Chromium (Desktop)

Chrome und Chromium-basierte Browser (Brave, Edge, etc.) verwenden unter Windows und macOS in der Regel die System-Proxy-Einstellungen. Diese Anleitung zeigt die Windows-Konfiguration.

### Schritt 2: Proxy-Einstellungen finden

1. Klicken Sie auf das **Dreipunkt-Menü** (⋮) oben rechts
2. Wählen Sie **Einstellungen**

![Chrome-Einstellungen](/images/guides/browser-config/accessi2p_6.png)

### Schritt 3: Manuellen Proxy konfigurieren

1. Geben Sie im Suchfeld der Einstellungen **"proxy"** ein
2. Klicken Sie auf **Proxy-Einstellungen Ihres Computers öffnen**

![Chrome Proxy-Suche](/images/guides/browser-config/accessi2p_7.png)

### Step 3: Open Manual Proxy Setup

Dies öffnet die Windows Netzwerk- & Interneteinstellungen.

1. Scrolle nach unten zu **Manuelle Proxy-Einrichtung**
2. Klicke auf **Einrichten**

![Windows Proxy Setup](/images/guides/browser-config/accessi2p_8.png)

### Schritt 1: Chrome-Einstellungen öffnen

1. Schalten Sie **Proxyserver verwenden** auf **Ein**
2. Geben Sie Folgendes ein:
   - **Proxy-IP-Adresse**: `127.0.0.1`
   - **Port**: `4444`
3. Optional können Sie Ausnahmen unter **"Proxyserver nicht für Adressen verwenden, die beginnen mit"** hinzufügen (z. B. `localhost;127.*`)
4. Klicken Sie auf **Speichern**

![Chrome Proxy-Konfiguration](/images/guides/browser-config/accessi2p_9.png)

Sie können jetzt `.i2p`-Seiten in Chrome durchsuchen!

**Hinweis**: Diese Einstellungen wirken sich auf alle Chromium-basierten Browser und einige andere Anwendungen unter Windows aus. Um dies zu vermeiden, sollten Sie stattdessen Firefox mit einem dedizierten I2P-Profil verwenden.

### Schritt 2: Proxy-Einstellungen öffnen

Unter Linux können Sie Chrome/Chromium mit Proxy-Flags starten, um Änderungen an den Systemeinstellungen zu vermeiden:

```bash
chromium \
  --proxy-server="http=127.0.0.1:4444 \
  --proxy-bypass-list="<-loopback>"
```
Oder erstellen Sie ein Desktop-Starter-Skript:

```bash
#!/bin/bash
chromium --proxy-server="http=127.0.0.1:4444" --user-data-dir="$HOME/.config/chromium-i2p"
```
Das `--user-data-dir`-Flag erstellt ein separates Chrome-Profil für das I2P-Browsing.

## Firefox (Desktop)

Moderne "Fenix" Firefox-Builds beschränken about:config und Erweiterungen standardmäßig. IceRaven ist ein Firefox-Fork, der eine kuratierte Auswahl an Erweiterungen aktiviert und die Proxy-Einrichtung vereinfacht.

Erweiterungsbasierte Konfiguration (IceRaven):

1) Wenn Sie IceRaven bereits verwenden, sollten Sie zunächst den Browserverlauf löschen (Menü → Verlauf → Verlauf löschen). 2) Öffnen Sie Menü → Add‑Ons → Add‑Ons-Manager. 3) Installieren Sie die Erweiterung „I2P Proxy for Android and Other Systems". 4) Der Browser wird nun über I2P als Proxy kommunizieren.

Diese Erweiterung funktioniert auch auf Pre-Fenix Firefox-basierten Browsern, wenn sie von [AMO](https://addons.mozilla.org/en-US/android/addon/i2p-proxy/) installiert wird.

Die Aktivierung der erweiterten Extension-Unterstützung in Firefox Nightly erfordert einen separaten Prozess, der [von Mozilla dokumentiert wurde](https://blog.mozilla.org/addons/2020/09/29/expanded-extension-support-in-firefox-for-android-nightly/).

## Internet Explorer / Windows System Proxy

Unter Windows gilt der System-Proxy-Dialog für den IE und kann von Chromium-basierten Browsern verwendet werden, wenn diese die Systemeinstellungen übernehmen.

1) Öffne „Netzwerk- und Interneteinstellungen" → „Proxy". 2) Aktiviere „Proxyserver für LAN verwenden". 3) Setze die Adresse `127.0.0.1`, Port `4444` für HTTP. 4) Optional aktiviere „Proxyserver für lokale Adressen umgehen".
