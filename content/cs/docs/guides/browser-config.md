---
title: "Konfigurace webového prohlížeče"
description: "Nakonfigurujte oblíbené prohlížeče pro použití HTTP/HTTPS proxy I2P na desktopu a Androidu"
slug: "browser-config"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: dokumentace
---

Tento průvodce ukazuje, jak nakonfigurovat běžné prohlížeče pro odesílání provozu přes vestavěnou HTTP proxy I2P. Pokrývá prohlížeče Safari, Firefox a Chrome/Chromium s podrobnými pokyny krok za krokem.

**Důležité poznámky**:

- Výchozí HTTP proxy I2P naslouchá na `127.0.0.1:4444`.
- I2P chrání provoz uvnitř sítě I2P (stránky .i2p).
- Ujistěte se, že váš I2P router běží před konfigurací prohlížeče.

## Safari (macOS)

Safari používá celostystémová nastavení proxy na macOS.

### Step 1: Open Network Settings

1. Otevřete **Safari** a přejděte do **Safari → Nastavení** (nebo **Předvolby**)
2. Klikněte na záložku **Pokročilé**
3. V sekci **Proxy** klikněte na **Změnit nastavení...**

Toto otevře síťová nastavení vašeho Macu.

![Safari Advanced Settings](/images/guides/browser-config/accessi2p_1.png)

### Krok 1: Otevřete nastavení sítě

1. V nastavení sítě zaškrtněte políčko **Web Proxy (HTTP)**
2. Zadejte následující údaje:
   - **Web Proxy Server**: `127.0.0.1`
   - **Port**: `4444`
3. Klikněte na **OK** pro uložení nastavení

![Konfigurace proxy v Safari](/images/guides/browser-config/accessi2p_2.png)

Nyní můžete procházet stránky `.i2p` v Safari!

**Poznámka**: Tato nastavení proxy ovlivní všechny aplikace, které používají systémové proxy macOS. Zvažte vytvoření samostatného uživatelského účtu nebo použití jiného prohlížeče výhradně pro I2P, pokud chcete izolovat procházení I2P.

## Firefox (Desktop)

Firefox má vlastní nastavení proxy nezávislé na systému, což z něj činí ideální volbu pro vyhrazené procházení I2P.

### Krok 2: Konfigurace HTTP Proxy

1. Klikněte na **tlačítko nabídky** (☰) v pravém horním rohu
2. Vyberte **Nastavení**

![Firefox Settings](/images/guides/browser-config/accessi2p_3.png)

### Step 2: Find Proxy Settings

1. Do vyhledávacího pole Nastavení napište **"proxy"**
2. Přejděte na **Nastavení sítě**
3. Klikněte na tlačítko **Nastavení...**

![Firefox Proxy Search](/images/guides/browser-config/accessi2p_4.png)

### Krok 1: Otevřete Nastavení

1. Vyberte **Ruční konfigurace proxy**
2. Zadejte následující:
   - **HTTP Proxy**: `127.0.0.1` **Port**: `4444`
3. Nechte **SOCKS Host** prázdné (pokud specificky nepotřebujete SOCKS proxy)
4. Zaškrtněte **Proxy DNS when using SOCKS** pouze pokud používáte SOCKS proxy
5. Klikněte na **OK** pro uložení

![Ruční konfigurace proxy ve Firefoxu](/images/guides/browser-config/accessi2p_5.png)

Nyní můžete procházet `.i2p` stránky ve Firefoxu!

**Tip**: Zvažte vytvoření samostatného profilu Firefoxu věnovaného prohlížení I2P. Tím udržíte prohlížení I2P oddělené od běžného prohlížení. Pro vytvoření profilu zadejte `about:profiles` do adresního řádku Firefoxu.

## Chrome / Chromium (Desktop)

Chrome a prohlížeče založené na Chromiu (Brave, Edge atd.) obvykle používají systémová nastavení proxy na Windows a macOS. Tento průvodce ukazuje konfiguraci pro Windows.

### Krok 2: Najděte nastavení proxy

1. Klikněte na **menu tří teček** (⋮) v pravém horním rohu
2. Vyberte **Nastavení**

![Nastavení Chrome](/images/guides/browser-config/accessi2p_6.png)

### Krok 3: Konfigurace manuálního proxy

1. Do vyhledávacího pole Nastavení napište **"proxy"**
2. Klikněte na **Otevřít nastavení proxy serveru počítače**

![Chrome Proxy Search](/images/guides/browser-config/accessi2p_7.png)

### Step 3: Open Manual Proxy Setup

Toto otevře nastavení sítě a internetu ve Windows.

1. Posuňte se dolů na **Ruční nastavení proxy**
2. Klikněte na **Nastavit**

![Windows Proxy Setup](/images/guides/browser-config/accessi2p_8.png)

### Krok 1: Otevřete nastavení prohlížeče Chrome

1. Přepněte **Použít proxy server** na **Zapnuto**
2. Zadejte následující:
   - **IP adresa proxy**: `127.0.0.1`
   - **Port**: `4444`
3. Volitelně přidejte výjimky do **"Nepoužívat proxy server pro adresy začínající"** (např. `localhost;127.*`)
4. Klikněte na **Uložit**

![Konfigurace proxy v Chrome](/images/guides/browser-config/accessi2p_9.png)

Nyní můžete prohlížet `.i2p` stránky v Chromu!

**Poznámka**: Tato nastavení ovlivňují všechny prohlížeče založené na Chromiu a některé další aplikace ve Windows. Chcete-li tomu zabránit, zvažte použití Firefoxu s vyhrazeným I2P profilem.

### Krok 2: Otevřete nastavení proxy

Na Linuxu můžete spustit Chrome/Chromium s proxy příznaky, abyste se vyhnuli změně systémových nastavení:

```bash
chromium \
  --proxy-server="http=127.0.0.1:4444 \
  --proxy-bypass-list="<-loopback>"
```
Nebo vytvořte spouštěcí skript pro plochu:

```bash
#!/bin/bash
chromium --proxy-server="http=127.0.0.1:4444" --user-data-dir="$HOME/.config/chromium-i2p"
```
Příznak `--user-data-dir` vytváří samostatný profil Chrome pro procházení I2P.

## Firefox (Desktop)

Moderní buildy Firefoxu "Fenix" ve výchozím nastavení omezují about:config a rozšíření. IceRaven je fork Firefoxu, který umožňuje kurátorovanou sadu rozšíření a zjednodušuje nastavení proxy.

Konfigurace založená na rozšíření (IceRaven):

1) Pokud již používáte IceRaven, zvažte nejprve vymazání historie prohlížení (Menu → Historie → Smazat historii). 2) Otevřete Menu → Doplňky → Správce doplňků. 3) Nainstalujte rozšíření „I2P Proxy for Android and Other Systems". 4) Prohlížeč nyní bude směrovat provoz přes I2P.

Toto rozšíření funguje také v prohlížečích založených na Firefox před verzí Fenix, pokud je nainstalováno z [AMO](https://addons.mozilla.org/en-US/android/addon/i2p-proxy/).

Povolení podpory širokého spektra rozšíření ve Firefox Nightly vyžaduje samostatný proces [zdokumentovaný Mozillou](https://blog.mozilla.org/addons/2020/09/29/expanded-extension-support-in-firefox-for-android-nightly/).

## Internet Explorer / Windows System Proxy

Na Windows se dialogové okno systémového proxy vztahuje na IE a může být použito prohlížeči založenými na Chromiu, když dědí systémová nastavení.

1) Otevřete „Nastavení sítě a internetu" → „Proxy". 2) Povolte „Použít proxy server pro vaši síť LAN". 3) Nastavte adresu `127.0.0.1`, port `4444` pro HTTP. 4) Volitelně zaškrtněte „Obejít proxy server pro místní adresy".
