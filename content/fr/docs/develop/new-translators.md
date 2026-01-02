---
title: "Guide du nouveau traducteur"
description: "Comment contribuer des traductions pour le site Web I2P et la console du routeur en utilisant Transifex ou des méthodes manuelles"
slug: "new-translators"
lastUpdated: "2025-10"
type: docs
---

Vous souhaitez aider à rendre I2P accessible à plus de personnes dans le monde ? La traduction est l'une des contributions les plus précieuses que vous puissiez apporter au projet. Ce guide vous expliquera comment traduire la console du routeur.

## Méthodes de traduction

Il existe deux façons de contribuer aux traductions :

### Méthode 1 : Transifex (Recommandée)

**C'est la façon la plus simple de traduire I2P.** Transifex fournit une interface web qui rend la traduction simple et accessible.

1. Inscrivez-vous sur [Transifex](https://www.transifex.com/otf/I2P/)
2. Demandez à rejoindre l'équipe de traduction I2P
3. Commencez à traduire directement dans votre navigateur

Aucune connaissance technique requise - il suffit de s'inscrire et de commencer à traduire !

### Méthode 2 : Traduction manuelle

Pour les traducteurs qui préfèrent travailler avec git et des fichiers locaux, ou pour les langues qui ne sont pas encore configurées sur Transifex.

**Exigences :** - Familiarité avec le contrôle de version git - Éditeur de texte ou outil de traduction (POEdit recommandé) - Outils en ligne de commande : git, gettext

**Configuration :** 1. Rejoignez [#i2p-dev sur IRC](/contact/#irc) et présentez-vous 2. Mettez à jour le statut de traduction sur le wiki (demandez l'accès sur IRC) 3. Clonez le dépôt approprié (voir les sections ci-dessous)

---

## Traduction de la Console du Routeur

La console du routeur est l'interface web que vous voyez lorsque vous exécutez I2P. La traduire aide les utilisateurs qui ne sont pas à l'aise avec l'anglais.

### Utiliser Transifex (recommandé)

1. Accédez à [I2P sur Transifex](https://www.transifex.com/otf/I2P/)
2. Sélectionnez le projet de la console du router
3. Choisissez votre langue
4. Commencez à traduire

### Traduction manuelle de la console du routeur

**Prérequis :** - Identiques à ceux de la traduction de site web (git, gettext) - Clé GPG (pour l'accès aux commits) - Accord de développeur signé

**Cloner le dépôt principal I2P :**

```bash
git clone https://i2pgit.org/I2P_Developers/i2p.i2p.git
cd i2p.i2p
```
**Fichiers à traduire :**

La console du routeur contient environ 15 fichiers qui nécessitent une traduction :

1. **Fichiers d'interface principaux :**
   - `apps/routerconsole/locale/messages_*.po` - Messages principaux de la console
   - `apps/routerconsole/locale-news/messages_*.po` - Messages d'actualités

2. **Fichiers proxy :**
   - `apps/i2ptunnel/locale/messages_*.po` - Interface de configuration de tunnel

3. **Locales des applications :**
   - `apps/susidns/locale/messages_*.po` - Interface du carnet d'adresses
   - `apps/susimail/locale/messages_*.po` - Interface de messagerie électronique
   - Autres répertoires de locales spécifiques aux applications

4. **Fichiers de documentation :**
   - `installer/resources/readme/readme_*.html` - Fichier readme d'installation
   - Fichiers d'aide dans diverses applications

**Flux de travail de traduction :**

```bash
# Update .po files from source
ant extractMessages

# Edit .po files with POEdit or text editor
poedit apps/routerconsole/locale/messages_es.po

# Build and test
ant updaters
# Install the update and check translations in the console
```
**Soumettez votre travail :** - Créez une demande de fusion sur [GitLab](https://i2pgit.org/I2P_Developers/i2p.i2p) - Ou partagez des fichiers avec l'équipe de développement sur IRC

---

## Outils de traduction

### POEdit (Hautement recommandé)

[POEdit](https://poedit.net/) est un éditeur spécialisé pour les fichiers de traduction .po.

**Fonctionnalités :** - Interface visuelle pour le travail de traduction - Affiche le contexte de traduction - Validation automatique - Disponible pour Windows, macOS et Linux

### Éditeurs de texte

Vous pouvez également utiliser n'importe quel éditeur de texte : - VS Code (avec des extensions i18n) - Sublime Text - vim/emacs (pour les utilisateurs de terminal)

### Contrôles de qualité

Avant de soumettre : 1. **Vérifiez le formatage :** Assurez-vous que les espaces réservés comme `%s` et `{0}` restent inchangés 2. **Testez vos traductions :** Installez et exécutez I2P pour voir comment elles s'affichent 3. **Cohérence :** Maintenez une terminologie cohérente dans tous les fichiers 4. **Longueur :** Certaines chaînes ont des contraintes d'espace dans l'interface utilisateur

---

## Conseils pour les traducteurs

### Directives générales

- **Restez cohérent :** Utilisez les mêmes traductions pour les termes courants tout au long du document
- **Conservez la mise en forme :** Préservez les balises HTML, les espaces réservés (`%s`, `{0}`) et les sauts de ligne
- **Le contexte compte :** Lisez attentivement la source anglaise pour comprendre le contexte
- **Posez des questions :** Utilisez IRC ou les forums si quelque chose n'est pas clair

### Termes courants I2P

Certains termes doivent rester en anglais ou être translittérés avec soin :

- **I2P** - Keep as is
- **eepsite** - Site web I2P (peut nécessiter une explication dans votre langue)
- **tunnel** - Chemin de connexion (éviter la terminologie Tor comme "circuit")
- **netDb** - Base de données réseau
- **floodfill** - Type de router
- **destination** - Point de terminaison d'adresse I2P

### Tester vos traductions

1. Compilez I2P avec vos traductions
2. Changez la langue dans les paramètres de la console du routeur
3. Parcourez toutes les pages pour vérifier :
   - Le texte s'adapte aux éléments de l'interface
   - Aucun caractère mal affiché (problèmes d'encodage)
   - Les traductions ont du sens dans le contexte

---

## Foire aux questions

### Pourquoi le processus de traduction est-il si complexe ?

Le processus utilise le contrôle de version (git) et des outils de traduction standards (fichiers .po) car :

1. **Responsabilité :** Suivre qui a modifié quoi et quand
2. **Qualité :** Examiner les modifications avant leur mise en ligne
3. **Cohérence :** Maintenir un formatage et une structure de fichiers appropriés
4. **Évolutivité :** Gérer efficacement les traductions dans plusieurs langues
5. **Collaboration :** Plusieurs traducteurs peuvent travailler sur la même langue

### Ai-je besoin de compétences en programmation ?

**Non !** Si vous utilisez Transifex, vous avez seulement besoin de : - Maîtrise de l'anglais et de votre langue cible - Un navigateur web - Compétences informatiques de base

Pour une traduction manuelle, vous aurez besoin de connaissances de base en ligne de commande, mais aucune programmation n'est requise.

### Combien de temps cela prend-il ?

- **Console du routeur :** Environ 15-20 heures pour tous les fichiers
- **Maintenance :** Quelques heures par mois pour mettre à jour les nouvelles chaînes

### Plusieurs personnes peuvent-elles travailler sur une seule langue ?

Oui ! La coordination est essentielle : - Utilisez Transifex pour une coordination automatique - Pour le travail manuel, communiquez sur le canal IRC #i2p-dev - Divisez le travail par sections ou fichiers

### Que faire si ma langue n'est pas répertoriée ?

Demandez-le sur Transifex ou contactez l'équipe sur IRC. L'équipe de développement peut configurer une nouvelle langue rapidement.

### Comment puis-je tester mes traductions avant de les soumettre ?

- Compiler I2P depuis les sources avec vos traductions
- Installer et exécuter localement
- Changer la langue dans les paramètres de la console

---

## Obtenir de l'aide

### Support IRC

Rejoignez [#i2p-dev sur IRC](/contact/#irc) pour : - Aide technique avec les outils de traduction - Questions sur la terminologie I2P - Coordination avec les autres traducteurs - Support direct des développeurs

### Forums

- Discussions sur la traduction dans les [Forums I2P](http://i2pforum.net/)
- Inside I2P : Forum de traduction sur zzz.i2p (nécessite un routeur I2P)

### Documentation

- [Documentation Transifex](https://docs.transifex.com/)
- [Documentation POEdit](https://poedit.net/support)
- [Manuel gettext](https://www.gnu.org/software/gettext/manual/)

---

## Reconnaissance

Tous les traducteurs sont crédités dans : - La console du routeur I2P (page À propos) - La page des crédits du site web - L'historique des commits Git - Les annonces de version

Votre travail aide directement des personnes du monde entier à utiliser I2P de manière sûre et privée. Merci de votre contribution !

---

## Prochaines étapes

Prêt à commencer la traduction ?

1. **Choisissez votre méthode :**
   - Démarrage rapide : [Inscrivez-vous sur Transifex](https://www.transifex.com/otf/I2P/)
   - Approche manuelle : Rejoignez [#i2p-dev sur IRC](/contact/#irc)

2. **Commencez petit :** Traduisez quelques chaînes pour vous familiariser avec le processus

3. **Demandez de l'aide :** N'hésitez pas à contacter sur IRC ou les forums

**Merci de contribuer à rendre I2P accessible à tous !**
