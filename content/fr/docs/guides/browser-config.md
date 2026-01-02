---
title: "Configuration du navigateur Web"
description: "Configurer les navigateurs populaires pour utiliser les proxies HTTP/HTTPS d'I2P sur ordinateur de bureau et Android"
slug: "browser-config"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

Ce guide explique comment configurer les navigateurs courants pour envoyer le trafic via le proxy HTTP intégré d'I2P. Il couvre Safari, Firefox et les navigateurs Chrome/Chromium avec des instructions détaillées étape par étape.

**Notes importantes** :

- Le proxy HTTP par défaut d'I2P écoute sur `127.0.0.1:4444`.
- I2P protège le trafic à l'intérieur du réseau I2P (sites .i2p).
- Assurez-vous que votre router I2P est en cours d'exécution avant de configurer votre navigateur.

## Safari (macOS)

Safari utilise les paramètres de proxy à l'échelle du système sur macOS.

### Step 1: Open Network Settings

1. Ouvrez **Safari** et allez dans **Safari → Réglages** (ou **Préférences**)
2. Cliquez sur l'onglet **Avancé**
3. Dans la section **Proxys**, cliquez sur **Modifier les réglages...**

Cela ouvrira les Réglages Réseau système de votre Mac.

![Paramètres avancés de Safari](/images/guides/browser-config/accessi2p_1.png)

### Étape 1 : Ouvrir les paramètres réseau

1. Dans les paramètres réseau, cochez la case **Proxy Web (HTTP)**
2. Entrez les informations suivantes :
   - **Serveur Proxy Web** : `127.0.0.1`
   - **Port** : `4444`
3. Cliquez sur **OK** pour enregistrer vos paramètres

![Configuration du proxy Safari](/images/guides/browser-config/accessi2p_2.png)

Vous pouvez maintenant parcourir les sites `.i2p` dans Safari !

**Note** : Ces paramètres de proxy affecteront toutes les applications qui utilisent les proxys système de macOS. Envisagez de créer un compte utilisateur séparé ou d'utiliser un navigateur différent exclusivement pour I2P si vous souhaitez isoler la navigation I2P.

## Firefox (Desktop)

Firefox possède ses propres paramètres de proxy indépendants du système, ce qui le rend idéal pour une navigation I2P dédiée.

### Étape 2 : Configurer le proxy HTTP

1. Cliquez sur le **bouton de menu** (☰) en haut à droite
2. Sélectionnez **Paramètres**

![Paramètres Firefox](/images/guides/browser-config/accessi2p_3.png)

### Step 2: Find Proxy Settings

1. Dans la boîte de recherche des Paramètres, tapez **"proxy"**
2. Faites défiler jusqu'à **Paramètres réseau**
3. Cliquez sur le bouton **Paramètres...**

![Firefox Proxy Search](/images/guides/browser-config/accessi2p_4.png)

### Étape 1 : Ouvrir les paramètres

1. Sélectionnez **Configuration manuelle du proxy**
2. Saisissez les informations suivantes :
   - **Proxy HTTP** : `127.0.0.1` **Port** : `4444`
3. Laissez **Hôte SOCKS** vide (sauf si vous avez spécifiquement besoin d'un proxy SOCKS)
4. Cochez **Proxy DNS lors de l'utilisation de SOCKS** uniquement si vous utilisez un proxy SOCKS
5. Cliquez sur **OK** pour enregistrer

![Configuration manuelle du proxy dans Firefox](/images/guides/browser-config/accessi2p_5.png)

Vous pouvez maintenant naviguer sur les sites `.i2p` dans Firefox !

**Astuce** : Envisagez de créer un profil Firefox distinct dédié à la navigation I2P. Cela permet de garder votre navigation I2P isolée de votre navigation habituelle. Pour créer un profil, tapez `about:profiles` dans la barre d'adresse de Firefox.

## Chrome / Chromium (Desktop)

Chrome et les navigateurs basés sur Chromium (Brave, Edge, etc.) utilisent généralement les paramètres proxy du système sur Windows et macOS. Ce guide présente la configuration Windows.

### Étape 2 : Trouver les paramètres du proxy

1. Cliquez sur le **menu trois points** (⋮) en haut à droite
2. Sélectionnez **Paramètres**

![Paramètres Chrome](/images/guides/browser-config/accessi2p_6.png)

### Étape 3 : Configurer le proxy manuellement

1. Dans la zone de recherche des Paramètres, tapez **"proxy"**
2. Cliquez sur **Ouvrir les paramètres de proxy de votre ordinateur**

![Chrome Proxy Search](/images/guides/browser-config/accessi2p_7.png)

### Step 3: Open Manual Proxy Setup

Cela ouvrira les paramètres Réseau et Internet de Windows.

1. Faites défiler vers le bas jusqu'à **Configuration manuelle du proxy**
2. Cliquez sur **Configurer**

![Configuration du proxy Windows](/images/guides/browser-config/accessi2p_8.png)

### Étape 1 : Ouvrir les paramètres de Chrome

1. Basculez **Utiliser un serveur proxy** sur **Activé**
2. Entrez ce qui suit :
   - **Adresse IP du proxy** : `127.0.0.1`
   - **Port** : `4444`
3. Facultativement, ajoutez des exceptions dans **« Ne pas utiliser le serveur proxy pour les adresses commençant par »** (par ex., `localhost;127.*`)
4. Cliquez sur **Enregistrer**

![Configuration du proxy Chrome](/images/guides/browser-config/accessi2p_9.png)

Vous pouvez maintenant naviguer sur les sites `.i2p` dans Chrome !

**Remarque** : Ces paramètres affectent tous les navigateurs basés sur Chromium et certaines autres applications sur Windows. Pour éviter cela, envisagez d'utiliser Firefox avec un profil I2P dédié à la place.

### Étape 2 : Ouvrir les paramètres du proxy

Sous Linux, vous pouvez lancer Chrome/Chromium avec des paramètres de proxy pour éviter de modifier les paramètres système :

```bash
chromium \
  --proxy-server="http=127.0.0.1:4444 \
  --proxy-bypass-list="<-loopback>"
```
Ou créez un script de lanceur de bureau :

```bash
#!/bin/bash
chromium --proxy-server="http=127.0.0.1:4444" --user-data-dir="$HOME/.config/chromium-i2p"
```
Le flag `--user-data-dir` crée un profil Chrome distinct pour la navigation I2P.

## Firefox (Bureau)

Les versions modernes de Firefox "Fenix" limitent about:config et les extensions par défaut. IceRaven est un fork de Firefox qui active un ensemble sélectionné d'extensions, simplifiant ainsi la configuration du proxy.

Configuration basée sur les extensions (IceRaven) :

1) Si vous utilisez déjà IceRaven, envisagez d'effacer l'historique de navigation en premier (Menu → Historique → Supprimer l'historique). 2) Ouvrez Menu → Modules complémentaires → Gestionnaire de modules complémentaires. 3) Installez l'extension « I2P Proxy for Android and Other Systems ». 4) Le navigateur utilisera désormais I2P comme proxy.

Cette extension fonctionne également sur les navigateurs basés sur Firefox pré-Fenix si elle est installée depuis [AMO](https://addons.mozilla.org/en-US/android/addon/i2p-proxy/).

L'activation d'une prise en charge étendue des extensions dans Firefox Nightly nécessite un processus distinct [documenté par Mozilla](https://blog.mozilla.org/addons/2020/09/29/expanded-extension-support-in-firefox-for-android-nightly/).

## Internet Explorer / Windows System Proxy

Sur Windows, la boîte de dialogue du proxy système s'applique à IE et peut être utilisée par les navigateurs basés sur Chromium lorsqu'ils héritent des paramètres système.

1) Ouvrez « Paramètres réseau et Internet » → « Proxy ». 2) Activez « Utiliser un serveur proxy pour votre réseau local ». 3) Définissez l'adresse `127.0.0.1`, port `4444` pour HTTP. 4) Cochez éventuellement « Ne pas utiliser de serveur proxy pour les adresses locales ».
