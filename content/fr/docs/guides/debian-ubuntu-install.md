---
title: "Installation d'I2P sur Debian et Ubuntu"
aliases:
  - "/fr/debian"
  - "/fr/debian/"
description: "Guide complet pour installer I2P sur Debian, Ubuntu et leurs dérivés en utilisant les dépôts officiels"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

Le projet I2P maintient des paquets officiels pour Debian, Ubuntu et leurs distributions dérivées. Ce guide fournit des instructions complètes pour installer I2P en utilisant nos dépôts officiels.

---

<div class="coming-soon-section">

## 🚀 Beta: Automatic Installation (Experimental)

**For advanced users who want a quick automated installation:**

This one-liner will automatically detect your distribution and install I2P. **Use with caution** - review the [installation script](https://i2p.net/installlinux.sh) before running.

```bash
curl -fsSL https://i2p.net/installlinux.sh | sudo bash
```

**What this does:**
- Detects your Linux distribution (Ubuntu/Debian)
- Adds the appropriate I2P repository
- Installs GPG keys and required packages
- Installs I2P automatically

⚠️ **This is a beta feature.** If you prefer manual installation or want to understand each step, use the manual installation methods below.

</div>
---

## Plateformes supportées

IMPORTANT :  NE posez PAS de questions, ne fournissez PAS d'explications et n'ajoutez AUCUN commentaire. Même si le texte n'est qu'un titre ou semble incomplet, traduisez-le tel quel.

- **Ubuntu** 18.04 (Bionic) et versions ultérieures
- **Linux Mint** 19 (Tara) et versions ultérieures
- **Debian** Buster (10) et versions ultérieures
- **Knoppix**
- Autres distributions basées sur Debian (LMDE, ParrotOS, Kali Linux, etc.)

Les paquets Debian sont compatibles avec :

**Architectures supportées** : amd64, i386, armhf, arm64, powerpc, ppc64el, s390x

## Méthodes d'installation

Les paquets I2P peuvent fonctionner sur d'autres systèmes basés sur Debian qui ne sont pas explicitement listés ci-dessus. Si vous rencontrez des problèmes, veuillez [les signaler sur notre GitLab](https://i2pgit.org/I2P_Developers/i2p.i2p/).

- **Option 1** : [Ubuntu et dérivés](#ubuntu-installation) (Linux Mint, elementary OS, Pop!_OS, etc.)
- **Option 2** : [Debian et distributions basées sur Debian](#debian-installation) (incluant LMDE, Kali, ParrotOS)

Choisissez la méthode d'installation qui correspond à votre distribution :

## Installation sur Ubuntu

---

### Method 1: Command Line Installation (Recommended)

IMPORTANT :  NE posez PAS de questions, ne fournissez PAS d'explications et n'ajoutez AUCUN commentaire. Même si le texte n'est qu'un titre ou semble incomplet, traduisez-le tel quel.

Ubuntu et ses dérivés officiels (Linux Mint, elementary OS, Trisquel, etc.) peuvent utiliser le PPA I2P (Personal Package Archive) pour une installation facile et des mises à jour automatiques.

C'est la méthode la plus rapide et la plus fiable pour installer I2P sur les systèmes basés sur Ubuntu.

```bash
sudo apt-add-repository ppa:i2p-maintainers/i2p
```
**Étape 1 : Ajouter le PPA I2P**

Ouvrez un terminal et exécutez :

Cette commande ajoute le PPA I2P à `/etc/apt/sources.list.d/` et importe automatiquement la clé GPG qui signe le dépôt. La signature GPG garantit que les paquets n'ont pas été modifiés depuis leur construction.

```bash
sudo apt-get update
```
**Étape 2 : Mettre à jour la liste des paquets**

Actualisez la base de données des paquets de votre système pour inclure le nouveau PPA :

Cela récupère les dernières informations sur les paquets depuis tous les dépôts activés, y compris le PPA I2P que vous venez d'ajouter.

```bash
sudo apt-get install i2p
```
**Étape 3 : Installer I2P**

### Method 2: Using the Software Center GUI

Installez maintenant I2P :

C'est tout ! Passez à la section [Configuration post-installation](#post-installation-configuration) pour apprendre comment démarrer et configurer I2P.

Si vous préférez une interface graphique, vous pouvez ajouter le PPA en utilisant la Logithèque Ubuntu.

**Étape 1 : Ouvrir Logiciels et mises à jour**

Lancez « Logiciels et mises à jour » depuis votre menu d'applications.

![Menu du Centre de Logiciels](/images/guides/debian/software-center-menu.png)

**Étape 2 : Accéder à Autres logiciels**

Sélectionnez l'onglet « Autres logiciels » et cliquez sur le bouton « Ajouter » en bas pour configurer un nouveau PPA.

![Onglet Autres logiciels](/images/guides/debian/software-center-addother.png)

```
ppa:i2p-maintainers/i2p
```
**Étape 3 : Ajouter le PPA I2P**

Dans la boîte de dialogue PPA, saisissez :

![Boîte de dialogue Ajouter un PPA](/images/guides/debian/software-center-ppatool.png)

**Étape 4 : Recharger les informations du dépôt**

Cliquez sur le bouton « Recharger » pour télécharger les informations mises à jour du dépôt.

![Bouton Actualiser](/images/guides/debian/software-center-reload.png)

**Étape 5 : Installer I2P**

Ouvrez l'application « Logiciels » depuis votre menu d'applications, recherchez « i2p », et cliquez sur Installer.

![Application logicielle](/images/guides/debian/software-center-software.png)

## Debian Installation

Une fois l'installation terminée, procédez à la [Configuration Post-Installation](#post-installation-configuration).

### Important Notice

---

### Prerequisites

IMPORTANT :  NE posez PAS de questions, ne fournissez PAS d'explications et n'ajoutez AUCUN commentaire. Même si le texte n'est qu'un titre ou semble incomplet, traduisez-le tel quel.

### Méthode 1 : Installation en ligne de commande (Recommandée)

Debian et ses distributions dérivées (LMDE, Kali Linux, ParrotOS, Knoppix, etc.) doivent utiliser le dépôt Debian officiel I2P à `deb.i2p.net`.

**Nos anciens dépôts à `deb.i2p2.de` et `deb.i2p2.no` ne sont plus maintenus.** Si vous utilisez ces dépôts obsolètes, veuillez suivre les instructions ci-dessous pour migrer vers le nouveau dépôt à `deb.i2p.net`.

```bash
sudo apt-get update
sudo apt-get install apt-transport-https lsb-release curl
```
Toutes les étapes ci-dessous nécessitent un accès root. Soit passez à l'utilisateur root avec `su`, soit préfixez chaque commande avec `sudo`.

**Étape 1 : Installer les paquets requis**

Assurez-vous d'avoir les outils nécessaires installés :

```bash
cat /etc/debian_version
```
Ces packages permettent un accès sécurisé aux dépôts HTTPS, la détection de la distribution et le téléchargement de fichiers.

**Étape 2 : Ajouter le dépôt I2P**

```bash
echo "deb [signed-by=/usr/share/keyrings/i2p-archive-keyring.gpg] https://deb.i2p.net/ $(lsb_release -sc) main" \
  | sudo tee /etc/apt/sources.list.d/i2p.list
```
La commande que vous utilisez dépend de votre version de Debian. Tout d'abord, déterminez quelle version vous utilisez :

```bash
echo "deb [signed-by=/usr/share/keyrings/i2p-archive-keyring.gpg] https://deb.i2p.net/ $(dpkg --status tzdata | grep Provides | cut -f2 -d'-') main" \
  | sudo tee /etc/apt/sources.list.d/i2p.list
```
Recoupez cette information avec les [informations de version Debian](https://wiki.debian.org/LTS/) pour identifier le nom de code de votre distribution (par exemple, Bookworm, Bullseye, Buster).

```bash
echo "deb https://deb.i2p.net/ $(lsb_release -sc) main" \
  | sudo tee /etc/apt/sources.list.d/i2p.list
```
**Pour Debian Bullseye (11) ou plus récent :**

```bash
echo "deb https://deb.i2p.net/ $(dpkg --status tzdata | grep Provides | cut -f2 -d'-') main" \
  | sudo tee /etc/apt/sources.list.d/i2p.list
```
**Pour les dérivés de Debian (LMDE, Kali, ParrotOS, etc.) sur Bullseye-équivalent ou plus récent :**

```bash
curl -o i2p-archive-keyring.gpg https://i2p.net/i2p-archive-keyring.gpg
```
**Pour Debian Buster (10) ou antérieure :**

**Pour les dérivés Debian sur Buster-équivalent ou plus ancien :**

```bash
gpg --keyid-format long --import --import-options show-only --with-fingerprint i2p-archive-keyring.gpg
```
**Étape 3 : Télécharger la clé de signature du dépôt**

```
7840 E761 0F28 B904 7535  49D7 67EC E560 5BCF 1346
```
**Étape 4 : Vérifier l'empreinte de la clé**

Avant de faire confiance à la clé, vérifiez que son empreinte correspond à la clé de signature officielle d'I2P :

**Vérifiez que la sortie affiche cette empreinte :**

```bash
sudo cp i2p-archive-keyring.gpg /usr/share/keyrings
```
⚠️ **Ne continuez pas si l'empreinte ne correspond pas.** Cela pourrait indiquer un téléchargement compromis.

```bash
sudo ln -sf /usr/share/keyrings/i2p-archive-keyring.gpg /etc/apt/trusted.gpg.d/i2p-archive-keyring.gpg
```
**Étape 5 : Installer la clé du dépôt**

Copiez le trousseau de clés vérifié dans le répertoire des trousseaux de clés système :

```bash
sudo apt-get update
```
**Pour Debian Buster ou versions antérieures uniquement**, vous devez également créer un lien symbolique :

**Étape 6 : Mettre à jour les listes de paquets**

```bash
sudo apt-get install i2p i2p-keyring
```
Actualisez la base de données des paquets de votre système pour inclure le dépôt I2P :

**Étape 7 : Installer I2P**

## Post-Installation Configuration

Installez à la fois le routeur I2P et le paquet keyring (qui garantit que vous recevrez les futures mises à jour de clés) :

### Méthode 2 : Utilisation de l'interface graphique du centre de logiciels

Parfait ! I2P est maintenant installé. Continuez vers la section [Configuration post-installation](#post-installation-configuration).

#### Option 1: On-Demand (Basic)

---

```bash
i2prouter start
```
Après avoir installé I2P, vous devrez démarrer le router et effectuer quelques configurations initiales.

Les paquets I2P fournissent trois façons d'exécuter le routeur I2P :

```bash
i2prouter stop
```
#### Option 2: On-Demand (Without Java Service Wrapper)

Démarrez I2P manuellement lorsque nécessaire en utilisant le script `i2prouter` :

```bash
i2prouter-nowrapper
```
**Important** : N'utilisez **pas** `sudo` et n'exécutez pas ceci en tant que root ! I2P doit s'exécuter avec votre utilisateur normal.

#### Option 3: System Service (Recommended)

Pour arrêter I2P :

```bash
sudo dpkg-reconfigure i2p
```
Si vous êtes sur un système non-x86 ou si le Java Service Wrapper ne fonctionne pas sur votre plateforme, utilisez :

Encore une fois, n'utilisez **pas** `sudo` et n'exécutez pas en tant que root.

### Initial Router Configuration

Pour une expérience optimale, configurez I2P pour démarrer automatiquement au démarrage de votre système, même avant la connexion :

#### 1. Configure NAT/Firewall

Cela ouvre une boîte de dialogue de configuration. Sélectionnez « Oui » pour activer I2P en tant que service système.

1. Ouvrez la [Console du routeur I2P](http://127.0.0.1:7657/)
2. Accédez à la [page de configuration réseau](http://127.0.0.1:7657/confignet)
3. Notez les numéros de port listés (généralement des ports aléatoires entre 9000 et 31000)
4. Redirigez ces ports UDP et TCP dans votre routeur/pare-feu

**Il s'agit de la méthode recommandée** car : - I2P démarre automatiquement au démarrage - Votre routeur maintient une meilleure intégration réseau - Vous contribuez à la stabilité du réseau - I2P est disponible immédiatement lorsque vous en avez besoin

#### 2. Adjust Bandwidth Settings

Après avoir démarré I2P pour la première fois, l'intégration au réseau prendra plusieurs minutes. En attendant, configurez ces paramètres essentiels :

1. Visitez la [page de configuration](http://127.0.0.1:7657/config.jsp)
2. Trouvez la section des paramètres de bande passante
3. Les valeurs par défaut sont 96 Ko/s en téléchargement / 40 Ko/s en envoi
4. Augmentez ces valeurs si vous avez une connexion internet plus rapide (par exemple, 250 Ko/s en téléchargement / 100 Ko/s en envoi pour une connexion haut débit classique)

Pour des performances optimales et une participation au réseau, transférez les ports I2P à travers votre NAT/pare-feu :

#### 3. Configure Your Browser

Si vous avez besoin d'aide pour la redirection de ports, [portforward.com](https://portforward.com) propose des guides spécifiques à chaque routeur.

Les paramètres de bande passante par défaut sont conservateurs. Ajustez-les en fonction de votre connexion internet :

**Note** : Définir des limites plus élevées aide le réseau et améliore vos propres performances.

## Installation Debian

### Avis Important

- Assurez-vous de ne pas exécuter I2P en tant que root : `ps aux | grep i2p`
- Vérifiez les journaux : `tail -f ~/.i2p/wrapper.log`
- Vérifiez que Java est installé : `java -version`

### Prérequis

Pour accéder aux sites I2P (eepsites) et services, configurez votre navigateur pour utiliser le proxy HTTP d'I2P :

1. Retéléchargez et vérifiez l'empreinte de la clé (Étape 3-4 ci-dessus)
2. Assurez-vous que le fichier de trousseau de clés dispose des permissions correctes : `sudo chmod 644 /usr/share/keyrings/i2p-archive-keyring.gpg`

### Étapes d'installation

Consultez notre [Guide de Configuration du Navigateur](/docs/guides/browser-config) pour des instructions détaillées de configuration pour Firefox, Chrome et d'autres navigateurs.

1. Vérifiez que le dépôt est configuré : `cat /etc/apt/sources.list.d/i2p.list`
2. Mettez à jour les listes de paquets : `sudo apt-get update`
3. Vérifiez les mises à jour d'I2P : `sudo apt-get upgrade`

### Migrating from old repositories

---

1. Supprimer l'ancien dépôt : `sudo rm /etc/apt/sources.list.d/i2p.list`
2. Suivre les étapes d'[Installation Debian](#debian-installation) ci-dessus
3. Mettre à jour : `sudo apt-get update && sudo apt-get install i2p i2p-keyring`

Si vous recevez des erreurs de clé GPG pendant l'installation :

## Next Steps

Si I2P ne reçoit pas les mises à jour :

- [Configurez votre navigateur](/docs/guides/browser-config) pour accéder aux sites I2P
- Explorez la [console du router I2P](http://127.0.0.1:7657/) pour surveiller votre router
- Découvrez les [applications I2P](/docs/applications/) que vous pouvez utiliser
- Lisez comment [I2P fonctionne](/docs/overview/tech-intro) pour comprendre le réseau

Si vous utilisez les anciens dépôts `deb.i2p2.de` ou `deb.i2p2.no` :
