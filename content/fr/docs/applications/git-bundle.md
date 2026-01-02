---
title: "Git Bundles pour I2P"
description: "Récupération et distribution de dépôts volumineux avec git bundle et BitTorrent"
slug: "git-bundle"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

Lorsque les conditions réseau rendent `git clone` peu fiable, vous pouvez distribuer des dépôts sous forme de **git bundles** via BitTorrent ou tout autre moyen de transfert de fichiers. Un bundle est un fichier unique contenant l'intégralité de l'historique du dépôt. Une fois téléchargé, vous récupérez les données localement depuis celui-ci, puis vous rebasculez vers le dépôt distant en amont.

## 1. Avant de commencer

Générer un bundle nécessite un clone Git **complet**. Les clones superficiels créés avec `--depth 1` produiront silencieusement des bundles défectueux qui semblent fonctionner mais échouent lorsque d'autres tentent de les utiliser. Récupérez toujours depuis une source fiable (GitHub à [github.com/i2p/i2p.i2p](https://github.com/i2p/i2p.i2p), l'instance Gitea I2P à [i2pgit.org](https://i2pgit.org), ou `git.idk.i2p` via I2P) et exécutez `git fetch --unshallow` si nécessaire pour convertir tout clone superficiel en clone complet avant de créer des bundles.

Si vous ne faites que consommer un bundle existant, téléchargez-le simplement. Aucune préparation spéciale n'est requise.

## 2. Télécharger un Bundle

### Obtaining the Bundle File

Téléchargez le fichier bundle via BitTorrent en utilisant I2PSnark (le client torrent intégré dans I2P) ou d'autres clients compatibles I2P comme BiglyBT avec le plugin I2P.

**Important** : I2PSnark fonctionne uniquement avec les torrents spécifiquement créés pour le réseau I2P. Les torrents clearnet standards ne sont pas compatibles car I2P utilise des Destinations (adresses de 387+ octets) au lieu d'adresses IP et de ports.

L'emplacement du fichier bundle dépend de votre type d'installation I2P :

- **Installations utilisateur/manuelles** (installées avec l'installateur Java) : `~/.i2p/i2psnark/`
- **Installations système/daemon** (installées via apt-get ou gestionnaire de paquets) : `/var/lib/i2p/i2p-config/i2psnark/`

Les utilisateurs de BiglyBT trouveront les fichiers téléchargés dans leur répertoire de téléchargements configuré.

### Cloning from the Bundle

**Méthode standard** (fonctionne dans la plupart des cas) :

```bash
git clone ~/.i2p/i2psnark/i2p.i2p.bundle
```
Si vous rencontrez des erreurs `fatal: multiple updates for ref` (un problème connu dans Git 2.21.0 et versions ultérieures lorsque la configuration globale de Git contient des refspecs de récupération conflictuelles), utilisez l'approche d'initialisation manuelle :

```bash
mkdir i2p.i2p && cd i2p.i2p
git init
git fetch ~/.i2p/i2psnark/i2p.i2p.bundle
```
Alternativement, vous pouvez utiliser le drapeau `--update-head-ok` :

```bash
git fetch --update-head-ok ~/.i2p/i2psnark/i2p.i2p.bundle '*:*'
```
### Obtention du fichier bundle

Après avoir cloné à partir du bundle, pointez votre clone vers le dépôt distant en direct afin que les futures récupérations passent par I2P ou le clearnet :

```bash
git remote set-url origin git@127.0.0.1:I2P_Developers/i2p.i2p
```
Ou pour l'accès clearnet :

```bash
git remote set-url origin https://github.com/i2p/i2p.i2p
```
Pour l'accès SSH via I2P, vous devez configurer un tunnel client SSH dans la console de votre routeur I2P (généralement le port 7670) pointant vers `g6u4vqiuy6bdc3dbu6a7gmi3ip45sqwgtbgrr6uupqaaqfyztrka.b32.i2p`. Si vous utilisez un port non standard :

```bash
GIT_SSH_COMMAND="ssh -p 7670" git clone git@127.0.0.1:I2P_Developers/i2p.i2p
```
## 3. Creating a Bundle

### Clonage depuis le Bundle

Assurez-vous que votre dépôt est entièrement à jour avec un **clone complet** (pas superficiel) :

```bash
git fetch --all
```
Si vous avez un clone superficiel, convertissez-le d'abord :

```bash
git fetch --unshallow
```
### Passage au Remote en Direct

**Utilisation de la cible de compilation Ant** (recommandé pour l'arborescence source d'I2P) :

```bash
ant git-bundle
```
Cela crée à la fois `i2p.i2p.bundle` (le fichier bundle) et `i2p.i2p.bundle.torrent` (les métadonnées BitTorrent).

**Utiliser git bundle directement** :

```bash
git bundle create i2p.i2p.bundle --all
```
Pour des bundles plus sélectifs :

```bash
git bundle create i2p.i2p.bundle --branches --tags
```
### Verifying Your Bundle

Toujours vérifier le bundle avant de le distribuer :

```bash
git bundle verify i2p.i2p.bundle
```
Cela confirme que le bundle est valide et affiche tous les commits prérequis nécessaires.

### Prérequis

Copiez le bundle et ses métadonnées torrent dans votre répertoire I2PSnark :

**Pour les installations utilisateur** :

```bash
cp i2p.i2p.bundle* ~/.i2p/i2psnark/
```
**Pour les installations système** :

```bash
cp i2p.i2p.bundle* /var/lib/i2p/i2p-config/i2psnark/
```
I2PSnark détecte et charge automatiquement les fichiers .torrent en quelques secondes. Accédez à l'interface web à l'adresse [http://127.0.0.1:7657/i2psnark](http://127.0.0.1:7657/i2psnark) pour commencer à partager.

## 4. Creating Incremental Bundles

Pour les mises à jour périodiques, créez des bundles incrémentaux contenant uniquement les nouveaux commits depuis le dernier bundle :

```bash
git tag lastBundleTag
git bundle create update.bundle lastBundleTag..master
```
Les utilisateurs peuvent récupérer depuis le bundle incrémental s'ils possèdent déjà le dépôt de base :

```bash
git fetch /path/to/update.bundle
```
Vérifiez toujours que les bundles incrémentaux affichent les commits prérequis attendus :

```bash
git bundle verify update.bundle
```
## 5. Updating After the Initial Clone

Une fois que vous avez un dépôt fonctionnel à partir du bundle, traitez-le comme n'importe quel autre clone Git :

```bash
git remote add upstream git@127.0.0.1:I2P_Developers/i2p.i2p
git fetch upstream
git merge upstream/master
```
Ou pour des flux de travail plus simples :

```bash
git fetch origin
git pull origin master
```
## 3. Créer un bundle

- **Distribution résiliente** : Les grands dépôts peuvent être partagés via BitTorrent, qui gère automatiquement les nouvelles tentatives, la vérification des morceaux et la reprise.
- **Amorçage pair-à-pair** : Les nouveaux contributeurs peuvent amorcer leur clone depuis des pairs proches sur le réseau I2P, puis récupérer les modifications incrémentales directement depuis les hôtes Git.
- **Charge serveur réduite** : Les miroirs peuvent publier des bundles périodiques pour réduire la pression sur les hôtes Git actifs, particulièrement utile pour les grands dépôts ou les conditions réseau lentes.
- **Transport hors ligne** : Les bundles fonctionnent sur n'importe quel transport de fichiers (clés USB, transferts directs, sneakernet), pas uniquement BitTorrent.

Les bundles ne remplacent pas les remotes actifs. Ils fournissent simplement une méthode de bootstrap plus résiliente pour les clones initiaux ou les mises à jour majeures.

## 7. Troubleshooting

### Génération du Bundle

**Problème** : La création du bundle réussit mais les autres ne peuvent pas cloner à partir du bundle.

**Cause** : Votre clone source est superficiel (créé avec `--depth`).

**Solution** : Convertir en clone complet avant de créer des bundles :

```bash
git fetch --unshallow
```
### Vérification de votre bundle

**Problème** : `fatal: multiple updates for ref` lors du clonage depuis un bundle.

**Cause** : Git 2.21.0+ entre en conflit avec les refspecs de récupération globaux dans `~/.gitconfig`.

**Solutions** : 1. Utilisez l'initialisation manuelle : `mkdir repo && cd repo && git init && git fetch /path/to/bundle` 2. Utilisez le flag `--update-head-ok` : `git fetch --update-head-ok /path/to/bundle '*:*'` 3. Supprimez la configuration conflictuelle : `git config --global --unset remote.origin.fetch`

### Distribuer via I2PSnark

**Problème** : `git bundle verify` signale des prérequis manquants.

**Cause** : Bundle incrémental ou clone source incomplet.

**Solution** : Soit récupérer les commits prérequis, soit utiliser d'abord le bundle de base, puis appliquer les mises à jour incrémentales.
