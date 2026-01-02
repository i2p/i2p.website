---
title: "Git sur I2P"
description: "Connexion des clients Git aux services hébergés sur I2P tels que i2pgit.org"
slug: "git"
lastUpdated: "2025-02"
accurateFor: "2.5.0"
reviewStatus: "needs-review"
---

Cloner et pousser des dépôts au sein d'I2P utilise les mêmes commandes Git que vous connaissez déjà—votre client se connecte simplement via des tunnels I2P au lieu de TCP/IP. Ce guide explique comment configurer un compte, configurer les tunnels et gérer les connexions lentes.

> **Démarrage rapide :** L'accès en lecture seule fonctionne via le proxy HTTP : `http_proxy=http://127.0.0.1:4444 git clone http://example.i2p/project.git`. Suivez les étapes ci-dessous pour l'accès SSH en lecture/écriture.

## 1. Créer un compte

Choisissez un service Git I2P et inscrivez-vous :

- À l'intérieur d'I2P : `http://git.idk.i2p`
- Miroir Clearnet : `https://i2pgit.org`

L'inscription peut nécessiter une approbation manuelle ; consultez la page d'accueil pour obtenir des instructions. Une fois approuvé, créez une bifurcation (fork) ou créez un dépôt afin d'avoir quelque chose pour tester.

## 2. Configurer un client I2PTunnel (SSH)

1. Ouvrez la console du routeur → **I2PTunnel** et ajoutez un nouveau tunnel **Client**.
2. Entrez la destination du service (Base32 ou Base64). Pour `git.idk.i2p`, vous trouverez les destinations HTTP et SSH sur la page d'accueil du projet.
3. Choisissez un port local (par exemple `localhost:7442`).
4. Activez le démarrage automatique si vous prévoyez d'utiliser le tunnel fréquemment.

L'interface utilisateur confirmera le nouveau tunnel et affichera son état. Lorsqu'il est en cours d'exécution, les clients SSH peuvent se connecter à `127.0.0.1` sur le port choisi.

## 3. Cloner via SSH

Utilisez le port du tunnel avec `GIT_SSH_COMMAND` ou une stanza de configuration SSH :

```bash
GIT_SSH_COMMAND="ssh -p 7442" \
    git clone git@127.0.0.1:your-project/example.git
```
Si la première tentative échoue (les tunnels peuvent être lents), essayez un clone superficiel :

```bash
GIT_SSH_COMMAND="ssh -p 7442" \
    git clone --depth 1 git@127.0.0.1:your-project/example.git
cd example
git fetch --unshallow
```
Configurer Git pour récupérer toutes les branches :

```bash
git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"
git fetch origin
```
### Conseils de performance

- Ajoutez un ou deux tunnels de secours dans l'éditeur de tunnels pour améliorer la résilience.
- Pour les tests ou les dépôts à faible risque, vous pouvez réduire la longueur du tunnel à 1 saut, mais soyez conscient du compromis sur l'anonymat.
- Conservez `GIT_SSH_COMMAND` dans votre environnement ou ajoutez une entrée dans `~/.ssh/config` :

```sshconfig
Host git.i2p
    HostName 127.0.0.1
    Port 7442
    User git
```
Ensuite, clonez en utilisant `git clone git@git.i2p:namespace/project.git`.

## 4. Suggestions de flux de travail

Adoptez un flux de travail de fork et branches courant sur GitLab/GitHub :

1. Définir un dépôt distant upstream : `git remote add upstream git@git.i2p:I2P_Developers/i2p.i2p`
2. Maintenir votre `master` synchronisé : `git pull upstream master`
3. Créer des branches de fonctionnalité pour les modifications : `git checkout -b feature/new-thing`
4. Pousser les branches vers votre fork : `git push origin feature/new-thing`
5. Soumettre une demande de fusion, puis effectuer un fast-forward du master de votre fork depuis upstream.

## 5. Rappels de confidentialité

- Git stocke les horodatages de commit dans votre fuseau horaire local. Pour forcer les horodatages UTC :

```bash
git config --global alias.utccommit '!git commit --date="$(date --utc +%Y-%m-%dT%H:%M:%S%z)"'
```
Utilisez `git utccommit` au lieu de `git commit` lorsque la confidentialité est importante.

- Évitez d'incorporer des URL clearnet ou des adresses IP dans les messages de commit ou les métadonnées du dépôt si l'anonymat est une préoccupation.

## 6. Dépannage

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Symptom</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Fix</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>connection closed</code> during clone</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Retry with <code>--depth 1</code>, add backup tunnels, or increase tunnel quantities.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>ssh: connect to host 127.0.0.1 port …: Connection refused</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Ensure the I2PTunnel client is running and SAM is enabled.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Slow performance</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Lower tunnel length, increase bandwidth limits, or schedule large fetches during off-peak hours.</td>
    </tr>
  </tbody>
</table>
Pour les scénarios avancés (mise en miroir de dépôts externes, distribution de bundles), consultez les guides associés : [Flux de travail avec les bundles Git](/docs/applications/git-bundle/) et [Héberger GitLab sur I2P](/docs/guides/gitlab/).
