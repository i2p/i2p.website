---
title: "Web Browser Configuration"
description: "Configure popular browsers to use I2P’s HTTP/HTTPS proxies on desktop and Android"
slug: "browser-config"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
aliases:
type: docs
---

This guide shows how to configure common browsers to send traffic through I2P's built‑in HTTP proxy. It covers Safari, Firefox, and Chrome/Chromium browsers with detailed step-by-step instructions.

**Important Notes**:

- I2P's default HTTP proxy listens on `127.0.0.1:4444`.
- I2P protects traffic inside the I2P network (.i2p sites). 
- Make sure your I2P router is running before configuring your browser.

## Safari (macOS)

Safari uses the system-wide proxy settings on macOS.

### Step 1: Open Network Settings

1. Open **Safari** and go to **Safari → Settings** (or **Preferences**)
2. Click on the **Advanced** tab
3. In the **Proxies** section, click **Change Settings...**

This will open your Mac's System Network Settings.

![Safari Advanced Settings](/images/guides/browser-config/accessi2p_1.png)

### Step 2: Configure HTTP Proxy

1. In the Network settings, check the box for **Web Proxy (HTTP)**
2. Enter the following:
   - **Web Proxy Server**: `127.0.0.1`
   - **Port**: `4444`
3. Click **OK** to save your settings

![Safari Proxy Configuration](/images/guides/browser-config/accessi2p_2.png)

You can now browse `.i2p` sites in Safari!

**Note**: These proxy settings will affect all applications that use macOS system proxies. Consider creating a separate user account or using a different browser exclusively for I2P if you want to isolate I2P browsing.

## Firefox (Desktop)

Firefox has its own proxy settings independent of the system, making it ideal for dedicated I2P browsing.

### Step 1: Open Settings

1. Click the **menu button** (☰) in the top right
2. Select **Settings**

![Firefox Settings](/images/guides/browser-config/accessi2p_3.png)

### Step 2: Find Proxy Settings

1. In the Settings search box, type **"proxy"**
2. Scroll to **Network Settings**
3. Click the **Settings...** button

![Firefox Proxy Search](/images/guides/browser-config/accessi2p_4.png)

### Step 3: Configure Manual Proxy

1. Select **Manual proxy configuration**
2. Enter the following:
   - **HTTP Proxy**: `127.0.0.1` **Port**: `4444`
3. Leave **SOCKS Host** empty (unless you specifically need SOCKS proxy)
4. Check **Proxy DNS when using SOCKS** only if using SOCKS proxy
5. Click **OK** to save

![Firefox Manual Proxy Configuration](/images/guides/browser-config/accessi2p_5.png)

You can now browse `.i2p` sites in Firefox!

**Tip**: Consider creating a separate Firefox profile dedicated to I2P browsing. This keeps your I2P browsing isolated from regular browsing. To create a profile, type `about:profiles` in the Firefox address bar.

## Chrome / Chromium (Desktop)

Chrome and Chromium-based browsers (Brave, Edge, etc.) typically use system proxy settings on Windows and macOS. This guide shows the Windows configuration.

### Step 1: Open Chrome Settings

1. Click the **three dots menu** (⋮) in the top right
2. Select **Settings**

![Chrome Settings](/images/guides/browser-config/accessi2p_6.png)

### Step 2: Open Proxy Settings

1. In the Settings search box, type **"proxy"**
2. Click **Open your computer's proxy settings**

![Chrome Proxy Search](/images/guides/browser-config/accessi2p_7.png)

### Step 3: Open Manual Proxy Setup

This will open Windows Network & Internet settings.

1. Scroll down to **Manual proxy setup**
2. Click **Set up**

![Windows Proxy Setup](/images/guides/browser-config/accessi2p_8.png)

### Step 4: Configure Proxy Server

1. Toggle **Use a proxy server** to **On**
2. Enter the following:
   - **Proxy IP address**: `127.0.0.1`
   - **Port**: `4444`
3. Optionally, add exceptions in **"Don't use the proxy server for addresses beginning with"** (e.g., `localhost;127.*`)
4. Click **Save**

![Chrome Proxy Configuration](/images/guides/browser-config/accessi2p_9.png)

You can now browse `.i2p` sites in Chrome!

**Note**: These settings affect all Chromium-based browsers and some other applications on Windows. To avoid this, consider using Firefox with a dedicated I2P profile instead.

### Linux: Chrome with Command-Line Flags

On Linux, you can launch Chrome/Chromium with proxy flags to avoid changing system settings:

```bash
chromium \
  --proxy-server="http=127.0.0.1:4444 \
  --proxy-bypass-list="<-loopback>"
```

Or create a desktop launcher script:

```bash
#!/bin/bash
chromium --proxy-server="http=127.0.0.1:4444" --user-data-dir="$HOME/.config/chromium-i2p"
```

The `--user-data-dir` flag creates a separate Chrome profile for I2P browsing.

## Firefox‑based Android (IceRaven and others)

Modern “Fenix” Firefox builds limit about:config and extensions by default. IceRaven is a Firefox fork that enables a curated set of extensions, making proxy setup simple.

Extension‑based configuration (IceRaven):

1) If you already use IceRaven, consider clearing browsing history first (Menu → History → Delete History).
2) Open Menu → Add‑Ons → Add‑Ons Manager.
3) Install the extension “I2P Proxy for Android and Other Systems”.
4) The browser will now proxy through I2P.

This extension also works on pre‑Fenix Firefox‑based browsers if installed from AMO:
https://addons.mozilla.org/en-US/android/addon/i2p-proxy/

Enabling wide extension support in Firefox Nightly requires a separate process documented by Mozilla:
https://blog.mozilla.org/addons/2020/09/29/expanded-extension-support-in-firefox-for-android-nightly/

## Internet Explorer / Windows System Proxy

On Windows, the system proxy dialog applies to IE and can be used by Chromium‑based browsers when they inherit system settings.

1) Open “Network and Internet Settings” → “Proxy”.
2) Enable “Use a proxy server for your LAN”.
3) Set address `127.0.0.1`, port `4444` for HTTP..
4) Optionally check “Bypass proxy server for local addresses”.


