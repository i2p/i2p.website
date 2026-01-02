---
title: "Installation d'I2P sur Debian et Ubuntu"
description: "Guide complet pour installer I2P sur Debian, Ubuntu et leurs dérivés en utilisant les dépôts officiels"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

Le projet I2P maintient des paquets officiels pour Debian, Ubuntu et leurs distributions dérivées. Ce guide fournit des instructions complètes pour installer I2P en utilisant nos dépôts officiels.

---


## 🚀 Bêta : Installation Automatique (Expérimental)

**Pour les utilisateurs avancés qui souhaitent une installation automatisée rapide :**

Cette commande unique détectera automatiquement votre distribution et installera I2P. **À utiliser avec précaution** - examinez le [script d'installation](https://i2p.net/installlinux.sh) avant de l'exécuter.

```bash
curl -fsSL https://i2p.net/installlinux.sh | sudo bash
```
**Ce que cela fait :** - Détecte votre distribution Linux (Ubuntu/Debian) - Ajoute le dépôt I2P approprié - Installe les clés GPG et les paquets requis - Installe I2P automatiquement

⚠️ **Ceci est une fonctionnalité bêta.** Si vous préférez l'installation manuelle ou souhaitez comprendre chaque étape, utilisez les méthodes d'installation manuelle ci-dessous.

---

IMPORTANT :  NE posez PAS de questions, ne fournissez PAS d'explications et n'ajoutez AUCUN commentaire. Même si le texte n'est qu'un titre ou semble incomplet, traduisez-le tel quel.

## Plateformes supportées

Les paquets Debian sont compatibles avec :

- **Ubuntu** 18.04 (Bionic) et versions ultérieures
- **Linux Mint** 19 (Tara) et versions ultérieures
- **Debian** Buster (10) et versions ultérieures
- **Knoppix**
- Autres distributions basées sur Debian (LMDE, ParrotOS, Kali Linux, etc.)

**Architectures supportées** : amd64, i386, armhf, arm64, powerpc, ppc64el, s390x

Les paquets I2P peuvent fonctionner sur d'autres systèmes basés sur Debian qui ne sont pas explicitement listés ci-dessus. Si vous rencontrez des problèmes, veuillez [les signaler sur notre GitLab](https://i2pgit.org/I2P_Developers/i2p.i2p/).

## Méthodes d'installation

Choisissez la méthode d'installation qui correspond à votre distribution :

- **Option 1** : [Ubuntu et dérivés](#ubuntu-installation) (Linux Mint, elementary OS, Pop!_OS, etc.)
- **Option 2** : [Debian et distributions basées sur Debian](#debian-installation) (incluant LMDE, Kali, ParrotOS)

---

IMPORTANT :  NE posez PAS de questions, ne fournissez PAS d'explications et n'ajoutez AUCUN commentaire. Même si le texte n'est qu'un titre ou semble incomplet, traduisez-le tel quel.

## Installation sur Ubuntu

Ubuntu et ses dérivés officiels (Linux Mint, elementary OS, Trisquel, etc.) peuvent utiliser le PPA I2P (Personal Package Archive) pour une installation facile et des mises à jour automatiques.

### Method 1: Command Line Installation (Recommended)

C'est la méthode la plus rapide et la plus fiable pour installer I2P sur les systèmes basés sur Ubuntu.

**Étape 1 : Ajouter le PPA I2P**

Ouvrez un terminal et exécutez :

```bash
sudo apt-add-repository ppa:i2p-maintainers/i2p
```
Cette commande ajoute le PPA I2P à `/etc/apt/sources.list.d/` et importe automatiquement la clé GPG qui signe le dépôt. La signature GPG garantit que les paquets n'ont pas été modifiés depuis leur construction.

**Étape 2 : Mettre à jour la liste des paquets**

Actualisez la base de données des paquets de votre système pour inclure le nouveau PPA :

```bash
sudo apt-get update
```
Cela récupère les dernières informations sur les paquets depuis tous les dépôts activés, y compris le PPA I2P que vous venez d'ajouter.

**Étape 3 : Installer I2P**

Installez maintenant I2P :

```bash
sudo apt-get install i2p
```
C'est tout ! Passez à la section [Configuration post-installation](#post-installation-configuration) pour apprendre comment démarrer et configurer I2P.

### Method 2: Using the Software Center GUI

Si vous préférez une interface graphique, vous pouvez ajouter le PPA en utilisant la Logithèque Ubuntu.

**Étape 1 : Ouvrir Logiciels et mises à jour**

Lancez « Logiciels et mises à jour » depuis votre menu d'applications.

![Menu du Centre de Logiciels](/images/guides/debian/software-center-menu.png)

**Étape 2 : Accéder à Autres logiciels**

Sélectionnez l'onglet « Autres logiciels » et cliquez sur le bouton « Ajouter » en bas pour configurer un nouveau PPA.

![Onglet Autres logiciels](/images/guides/debian/software-center-addother.png)

**Étape 3 : Ajouter le PPA I2P**

Dans la boîte de dialogue PPA, saisissez :

```
ppa:i2p-maintainers/i2p
```
![Boîte de dialogue Ajouter un PPA](/images/guides/debian/software-center-ppatool.png)

**Étape 4 : Recharger les informations du dépôt**

Cliquez sur le bouton « Recharger » pour télécharger les informations mises à jour du dépôt.

![Bouton Actualiser](/images/guides/debian/software-center-reload.png)

**Étape 5 : Installer I2P**

Ouvrez l'application « Logiciels » depuis votre menu d'applications, recherchez « i2p », et cliquez sur Installer.

![Application logicielle](/images/guides/debian/software-center-software.png)

Une fois l'installation terminée, procédez à la [Configuration Post-Installation](#post-installation-configuration).

---

IMPORTANT :  NE posez PAS de questions, ne fournissez PAS d'explications et n'ajoutez AUCUN commentaire. Même si le texte n'est qu'un titre ou semble incomplet, traduisez-le tel quel.

## Debian Installation

Debian et ses distributions dérivées (LMDE, Kali Linux, ParrotOS, Knoppix, etc.) doivent utiliser le dépôt Debian officiel I2P à `deb.i2p.net`.

### Important Notice

**Nos anciens dépôts à `deb.i2p2.de` et `deb.i2p2.no` ne sont plus maintenus.** Si vous utilisez ces dépôts obsolètes, veuillez suivre les instructions ci-dessous pour migrer vers le nouveau dépôt à `deb.i2p.net`.

### Prerequisites

Toutes les étapes ci-dessous nécessitent un accès root. Soit passez à l'utilisateur root avec `su`, soit préfixez chaque commande avec `sudo`.

### Méthode 1 : Installation en ligne de commande (Recommandée)

**Étape 1 : Installer les paquets requis**

Assurez-vous d'avoir les outils nécessaires installés :

```bash
sudo apt-get update
sudo apt-get install apt-transport-https lsb-release curl
```
Ces packages permettent un accès sécurisé aux dépôts HTTPS, la détection de la distribution et le téléchargement de fichiers.

**Étape 2 : Ajouter le dépôt I2P**

La commande que vous utilisez dépend de votre version de Debian. Tout d'abord, déterminez quelle version vous utilisez :

```bash
cat /etc/debian_version
```
Recoupez cette information avec les [informations de version Debian](https://wiki.debian.org/LTS/) pour identifier le nom de code de votre distribution (par exemple, Bookworm, Bullseye, Buster).

**Pour Debian Bullseye (11) ou plus récent :**

```bash
echo "deb [signed-by=/usr/share/keyrings/i2p-archive-keyring.gpg] https://deb.i2p.net/ $(lsb_release -sc) main" \
  | sudo tee /etc/apt/sources.list.d/i2p.list
```
**Pour les dérivés de Debian (LMDE, Kali, ParrotOS, etc.) sur Bullseye-équivalent ou plus récent :**

```bash
echo "deb [signed-by=/usr/share/keyrings/i2p-archive-keyring.gpg] https://deb.i2p.net/ $(dpkg --status tzdata | grep Provides | cut -f2 -d'-') main" \
  | sudo tee /etc/apt/sources.list.d/i2p.list
```
**Pour Debian Buster (10) ou antérieure :**

```bash
echo "deb https://deb.i2p.net/ $(lsb_release -sc) main" \
  | sudo tee /etc/apt/sources.list.d/i2p.list
```
**Pour les dérivés Debian sur Buster-équivalent ou plus ancien :**

```bash
echo "deb https://deb.i2p.net/ $(dpkg --status tzdata | grep Provides | cut -f2 -d'-') main" \
  | sudo tee /etc/apt/sources.list.d/i2p.list
```
**Étape 3 : Télécharger la clé de signature du dépôt**

```bash
curl -o i2p-archive-keyring.gpg https://geti2p.net/_static/i2p-archive-keyring.gpg
```
**Étape 4 : Vérifier l'empreinte de la clé**

Avant de faire confiance à la clé, vérifiez que son empreinte correspond à la clé de signature officielle d'I2P :

```bash
gpg --keyid-format long --import --import-options show-only --with-fingerprint i2p-archive-keyring.gpg
```
**Vérifiez que la sortie affiche cette empreinte :**

```
7840 E761 0F28 B904 7535  49D7 67EC E560 5BCF 1346
```
⚠️ **Ne continuez pas si l'empreinte ne correspond pas.** Cela pourrait indiquer un téléchargement compromis.

**Étape 5 : Installer la clé du dépôt**

Copiez le trousseau de clés vérifié dans le répertoire des trousseaux de clés système :

```bash
sudo cp i2p-archive-keyring.gpg /usr/share/keyrings
```
**Pour Debian Buster ou versions antérieures uniquement**, vous devez également créer un lien symbolique :

```bash
sudo ln -sf /usr/share/keyrings/i2p-archive-keyring.gpg /etc/apt/trusted.gpg.d/i2p-archive-keyring.gpg
```
**Étape 6 : Mettre à jour les listes de paquets**

Actualisez la base de données des paquets de votre système pour inclure le dépôt I2P :

```bash
sudo apt-get update
```
**Étape 7 : Installer I2P**

Installez à la fois le routeur I2P et le paquet keyring (qui garantit que vous recevrez les futures mises à jour de clés) :

```bash
sudo apt-get install i2p i2p-keyring
```
Parfait ! I2P est maintenant installé. Continuez vers la section [Configuration post-installation](#post-installation-configuration).

---


## Post-Installation Configuration

Après avoir installé I2P, vous devrez démarrer le router et effectuer quelques configurations initiales.

### Méthode 2 : Utilisation de l'interface graphique du centre de logiciels

Les paquets I2P fournissent trois façons d'exécuter le routeur I2P :

#### Option 1: On-Demand (Basic)

Démarrez I2P manuellement lorsque nécessaire en utilisant le script `i2prouter` :

```bash
i2prouter start
```
**Important** : N'utilisez **pas** `sudo` et n'exécutez pas ceci en tant que root ! I2P doit s'exécuter avec votre utilisateur normal.

Pour arrêter I2P :

```bash
i2prouter stop
```
#### Option 2: On-Demand (Without Java Service Wrapper)

Si vous êtes sur un système non-x86 ou si le Java Service Wrapper ne fonctionne pas sur votre plateforme, utilisez :

```bash
i2prouter-nowrapper
```
Encore une fois, n'utilisez **pas** `sudo` et n'exécutez pas en tant que root.

#### Option 3: System Service (Recommended)

Pour une expérience optimale, configurez I2P pour démarrer automatiquement au démarrage de votre système, même avant la connexion :

```bash
sudo dpkg-reconfigure i2p
```
Cela ouvre une boîte de dialogue de configuration. Sélectionnez « Oui » pour activer I2P en tant que service système.

**Il s'agit de la méthode recommandée** car : - I2P démarre automatiquement au démarrage - Votre routeur maintient une meilleure intégration réseau - Vous contribuez à la stabilité du réseau - I2P est disponible immédiatement lorsque vous en avez besoin

### Initial Router Configuration

Après avoir démarré I2P pour la première fois, l'intégration au réseau prendra plusieurs minutes. En attendant, configurez ces paramètres essentiels :

#### 1. Configure NAT/Firewall

Pour des performances optimales et une participation au réseau, transférez les ports I2P à travers votre NAT/pare-feu :

1. Ouvrez la [Console du routeur I2P](http://127.0.0.1:7657/)
2. Accédez à la [page de configuration réseau](http://127.0.0.1:7657/confignet)
3. Notez les numéros de port listés (généralement des ports aléatoires entre 9000 et 31000)
4. Redirigez ces ports UDP et TCP dans votre routeur/pare-feu

Si vous avez besoin d'aide pour la redirection de ports, [portforward.com](https://portforward.com) propose des guides spécifiques à chaque routeur.

#### 2. Adjust Bandwidth Settings

Les paramètres de bande passante par défaut sont conservateurs. Ajustez-les en fonction de votre connexion internet :

1. Visitez la [page de configuration](http://127.0.0.1:7657/config.jsp)
2. Trouvez la section des paramètres de bande passante
3. Les valeurs par défaut sont 96 Ko/s en téléchargement / 40 Ko/s en envoi
4. Augmentez ces valeurs si vous avez une connexion internet plus rapide (par exemple, 250 Ko/s en téléchargement / 100 Ko/s en envoi pour une connexion haut débit classique)

**Note** : Définir des limites plus élevées aide le réseau et améliore vos propres performances.

#### 3. Configure Your Browser

Pour accéder aux sites I2P (eepsites) et services, configurez votre navigateur pour utiliser le proxy HTTP d'I2P :

Consultez notre [Guide de Configuration du Navigateur](/docs/guides/browser-config) pour des instructions détaillées de configuration pour Firefox, Chrome et d'autres navigateurs.

---

## Installation Debian

### Avis Important

- Assurez-vous de ne pas exécuter I2P en tant que root : `ps aux | grep i2p`
- Vérifiez les journaux : `tail -f ~/.i2p/wrapper.log`
- Vérifiez que Java est installé : `java -version`

### Prérequis

Si vous recevez des erreurs de clé GPG pendant l'installation :

1. Retéléchargez et vérifiez l'empreinte de la clé (Étape 3-4 ci-dessus)
2. Assurez-vous que le fichier de trousseau de clés dispose des permissions correctes : `sudo chmod 644 /usr/share/keyrings/i2p-archive-keyring.gpg`

### Étapes d'installation

Si I2P ne reçoit pas les mises à jour :

1. Vérifiez que le dépôt est configuré : `cat /etc/apt/sources.list.d/i2p.list`
2. Mettez à jour les listes de paquets : `sudo apt-get update`
3. Vérifiez les mises à jour d'I2P : `sudo apt-get upgrade`

### Migrating from old repositories

Si vous utilisez les anciens dépôts `deb.i2p2.de` ou `deb.i2p2.no` :

1. Supprimer l'ancien dépôt : `sudo rm /etc/apt/sources.list.d/i2p.list`
2. Suivre les étapes d'[Installation Debian](#debian-installation) ci-dessus
3. Mettre à jour : `sudo apt-get update && sudo apt-get install i2p i2p-keyring`

---

## Next Steps

Maintenant qu'I2P est installé et en cours d'exécution :

- [Configurez votre navigateur](/docs/guides/browser-config) pour accéder aux sites I2P
- Explorez la [console du router I2P](http://127.0.0.1:7657/) pour surveiller votre router
- Découvrez les [applications I2P](/docs/applications/) que vous pouvez utiliser
- Lisez comment [I2P fonctionne](/docs/overview/tech-intro) pour comprendre le réseau

Bienvenue sur l'Internet Invisible !
