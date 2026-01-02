---
title: "Format du paquet de plugin"
description: "Règles d'empaquetage .xpi2p / .su3 pour les plugins I2P"
slug: "plugin"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

## Vue d'ensemble

Les plugins I2P sont des archives signées qui étendent les fonctionnalités du router. Ils sont fournis sous forme de fichiers `.xpi2p` ou `.su3`, s’installent dans `~/.i2p/plugins/<name>/` (ou `%APPDIR%\I2P\plugins\<name>\` sous Windows) et s’exécutent avec des permissions complètes du router, sans bac à sable.

### Types de plugins pris en charge

- Applications web de la console
- Nouveaux eepsites avec cgi-bin, applications web
- Thèmes de la console
- Traductions de la console
- Programmes Java (dans le même processus ou JVM séparée)
- Scripts shell et binaires natifs

### Modèle de sécurité

**CRITIQUE:** Les plugins s'exécutent dans la même JVM avec des permissions identiques à celles du router I2P. Ils ont un accès sans restriction à : - Système de fichiers (lecture et écriture) - API du router et état interne - Connexions réseau - Exécution de programmes externes

Les plugins doivent être traités comme du code entièrement approuvé. Les utilisateurs doivent vérifier les sources et les signatures des plugins avant l’installation.

---

## Formats de fichiers

### Format SU3 (fortement recommandé)

**Statut:** Actif, format préféré depuis I2P 0.9.15 (septembre 2014)

Le format `.su3` offre : - **clés de signature RSA-4096** (contre DSA-1024 dans xpi2p) - Signature stockée dans l'en-tête du fichier - Nombre magique : `I2Psu3` - Meilleure compatibilité avec les versions futures

**Structure:**

```
[SU3 Header with RSA-4096 signature]
[ZIP Archive]
  ├── plugin.config (required)
  ├── console/
  ├── lib/
  ├── webapps/
  └── [other plugin files]
```
### Format XPI2P (hérité, déprécié)

**Statut:** Pris en charge pour des raisons de rétrocompatibilité, non recommandé pour les nouveaux plugins

Le format `.xpi2p` utilise d’anciennes signatures cryptographiques : - **Signatures DSA-1024** (obsolètes selon NIST-800-57) - Signature DSA de 40 octets ajoutée en tête du ZIP - Nécessite le champ `key` dans plugin.config

**Structure:**

```
[40-byte DSA signature]
[16-byte version string (UTF-8, zero-padded)]
[ZIP Archive]
```
**Chemin de migration :** Lors de la migration de xpi2p vers su3, fournissez à la fois `updateURL` et `updateURL.su3` pendant la transition. Les routers modernes (0.9.15+) donnent automatiquement la priorité à SU3.

---

## Structure de l’archive et plugin.config

### Fichiers requis

**plugin.config** - Fichier de configuration I2P standard avec des paires clé-valeur

### Propriétés requises

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Property</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Format</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>name</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Installation directory name, must match for updates</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Alphanumeric, no spaces</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>signer</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Developer contact information</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>user@mail.i2p</code> format recommended</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>version</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Plugin version for update comparison</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Max 16 bytes, parsed by VersionComparator</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>key</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA public key (172 B64 chars ending with '=')</td><td style="border:1px solid var(--color-border); padding:0.5rem;"><strong>Omit for SU3 format</strong></td></tr>
  </tbody>
</table>
**Exemples de formats de version :** - `1.2.3` - `1.2.3-4` - `2.0.0-beta.1`

Séparateurs valides : `.` (point), `-` (tiret), `_` (tiret bas)

### Propriétés de métadonnées facultatives

#### Afficher les informations

- `date` - Date de publication (horodatage long Java)
- `author` - Nom du développeur (`user@mail.i2p` recommandé)
- `description` - Description en anglais
- `description_xx` - Description localisée (xx = code de langue)
- `websiteURL` - Page d'accueil du plugin (`http://foo.i2p/`)
- `license` - Identifiant de licence (par exemple, "Apache-2.0", "GPL-3.0")

#### Mettre à jour la configuration

- `updateURL` - Emplacement de mise à jour XPI2P (hérité)
- `updateURL.su3` - Emplacement de mise à jour SU3 (recommandé)
- `min-i2p-version` - Version minimale d'I2P requise
- `max-i2p-version` - Version maximale d'I2P compatible
- `min-java-version` - Version minimale de Java (par ex., `1.7`, `17`)
- `min-jetty-version` - Version minimale de Jetty (utilisez `6` pour Jetty 6+)
- `max-jetty-version` - Version maximale de Jetty (utilisez `5.99999` pour Jetty 5)

#### Comportement d'installation

- `dont-start-at-install` - Par défaut `false`. Si `true`, nécessite un démarrage manuel
- `router-restart-required` - Par défaut `false`. Indique à l’utilisateur qu’un redémarrage est nécessaire après la mise à jour
- `update-only` - Par défaut `false`. Échoue si le plug-in n’est pas déjà installé
- `install-only` - Par défaut `false`. Échoue si le plug-in existe déjà
- `min-installed-version` - Version minimale requise pour la mise à jour
- `max-installed-version` - Version maximale pouvant être mise à jour
- `disableStop` - Par défaut `false`. Masque le bouton d’arrêt si `true`

#### Intégration à la console

- `consoleLinkName` - Texte du lien de la barre de résumé de la console
- `consoleLinkName_xx` - Texte de lien localisé (xx = code de langue)
- `consoleLinkURL` - Destination du lien (par ex. `/appname/index.jsp`)
- `consoleLinkTooltip` - Texte de l’info-bulle (pris en charge depuis 0.7.12-6)
- `consoleLinkTooltip_xx` - Info-bulle localisée
- `console-icon` - Chemin vers une icône 32x32 (pris en charge depuis 0.9.20)
- `icon-code` - PNG 32x32 encodé en Base64 pour les plugins sans ressources web (depuis 0.9.25)

#### Exigences de plateforme (affichage uniquement)

- `required-platform-OS` - Exigence du système d’exploitation (non imposée)
- `other-requirements` - Exigences supplémentaires (p. ex., "Python 3.8+")

#### Gestion des dépendances (non implémentée)

- `depends` - Dépendances du plugin, séparées par des virgules
- `depends-version` - Exigences de version pour les dépendances
- `langs` - Contenu du pack de langue
- `type` - Type de plugin (app/theme/locale/webapp)

### Substitution de variables dans l’URL de mise à jour

**Statut de la fonctionnalité :** Disponible depuis I2P 1.7.0 (0.9.53)

Les deux `updateURL` et `updateURL.su3` prennent en charge des variables spécifiques à la plateforme :

**Variables:** - `$OS` - Système d'exploitation: `windows`, `linux`, `mac` - `$ARCH` - Architecture: `386`, `amd64`, `arm64`

**Exemple:**

```properties
updateURL.su3=http://foo.i2p/downloads/foo-$OS-$ARCH.su3
```
**Résultat sur Windows AMD64 :**

```
http://foo.i2p/downloads/foo-windows-amd64.su3
```
Cela permet d'utiliser des fichiers plugin.config uniques pour les compilations spécifiques à la plateforme.

---

## Structure des répertoires

### Disposition standard

```
plugins/
└── pluginname/
    ├── plugin.config (required)
    ├── console/
    │   ├── locale/          # Translation JARs
    │   ├── themes/          # Console themes
    │   ├── webapps/         # Web applications
    │   └── webapps.config   # Webapp configuration
    ├── eepsite/
    │   ├── cgi-bin/
    │   ├── docroot/
    │   ├── logs/
    │   ├── webapps/
    │   └── jetty.xml
    ├── lib/
    │   └── *.jar            # Plugin libraries
    └── clients.config       # Client startup configuration
```
### Objectifs du répertoire

**console/locale/** - Fichiers JAR contenant des Resource bundles (fichiers de ressources) pour les traductions de base d'I2P - Les traductions spécifiques aux plugins doivent se trouver dans `console/webapps/*.war` ou `lib/*.jar`

**console/themes/** - Chaque sous-répertoire contient un thème de console complet - Ajouté automatiquement au chemin de recherche des thèmes

**console/webapps/** - fichiers `.war` pour l'intégration à la console - Démarrés automatiquement sauf s'ils sont désactivés dans `webapps.config` - Le nom du WAR n'a pas besoin de correspondre au nom du plugin

**eepsite/** - eepsite complet avec sa propre instance Jetty - Nécessite une configuration `jetty.xml` avec substitution de variables - Voir les exemples de plug-ins zzzot et pebble

**lib/** - Bibliothèques JAR de plug-in - À spécifier dans le classpath via `clients.config` ou `webapps.config`

---

## Configuration de l'application Web

### Format de webapps.config

Fichier de configuration I2P standard régissant le comportement de l'application web.

**Syntaxe:**

```properties
# Disable autostart
webapps.warname.startOnLoad=false

# Add classpath JARs (as of API 0.9.53, works for any warname)
webapps.warname.classpath=$PLUGIN/lib/foo.jar,$I2P/lib/bar.jar
```
**Notes importantes:** - Avant router 0.7.12-9, utilisez `plugin.warname.startOnLoad` pour la compatibilité - Avant l'API 0.9.53, le classpath ne fonctionnait que si le warname (nom du fichier WAR) correspondait au nom du plugin - À partir de la 0.9.53+, le classpath fonctionne pour n'importe quel nom d'application web

### Meilleures pratiques pour les applications web

1. **Implémentation de ServletContextListener**
   - Implémenter `javax.servlet.ServletContextListener` pour le nettoyage
   - Ou surcharger `destroy()` dans la servlet
   - Garantit un arrêt correct lors des mises à jour et de l'arrêt du router

2. **Gestion des bibliothèques**
   - Placez les JARs partagés dans `lib/`, pas à l’intérieur du WAR
   - Référencez-les via le classpath de `webapps.config`
   - Permet d’installer et de mettre à jour les plugins séparément

3. **Évitez les bibliothèques en conflit**
   - N'intégrez jamais Jetty, Tomcat ni des fichiers JAR de servlets
   - N'intégrez jamais des fichiers JAR issus de l'installation standard d'I2P
   - Consultez la section classpath (chemin des classes) pour les bibliothèques standard

4. **Exigences de compilation**
   - N'incluez pas de fichiers source `.java` ou `.jsp`
   - Précompilez toutes les JSP pour éviter les retards au démarrage
   - Ne présumez pas de la disponibilité d’un compilateur Java/JSP

5. **Compatibilité avec l'API Servlet**
   - I2P prend en charge Servlet 3.0 (depuis 0.9.30)
   - **L'analyse des annotations n'est PAS prise en charge** (@WebContent)
   - Doit fournir le descripteur de déploiement `web.xml` traditionnel

6. **Version de Jetty**
   - Version actuelle : Jetty 9 (I2P 0.9.30+)
   - Utilisez `net.i2p.jetty.JettyStart` pour l’abstraction
   - Protège contre les modifications de l’API Jetty

---

## Configuration du client

### Format de clients.config

Définit les clients (services) lancés avec le plugin.

**Client de base:**

```properties
clientApp.0.main=com.example.PluginMain
clientApp.0.name=Example Plugin Service
clientApp.0.delay=30
clientApp.0.args=arg1 arg2 $PLUGIN/config.properties
```
**Client avec Arrêt/Désinstallation:**

```properties
clientApp.0.stopargs=stop
clientApp.0.uninstallargs=uninstall
clientApp.0.classpath=$PLUGIN/lib/plugin.jar,$I2P/lib/i2p.jar
```
### Référence des propriétés

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Property</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>main</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Fully qualified class name implementing ClientApp interface</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>name</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Display name for user interface</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>delay</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Startup delay in seconds (default: 0)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>args</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Space-separated arguments passed to constructor</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>stopargs</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Arguments for shutdown (must handle gracefully)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>uninstallargs</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Arguments called before plugin deletion</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>classpath</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Comma-separated JAR paths</td></tr>
  </tbody>
</table>
### Substitution de variables

Les variables suivantes sont remplacées dans `args`, `stopargs`, `uninstallargs` et `classpath`:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Variable</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Replacement</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$I2P</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2P base installation directory</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$CONFIG</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">I2P configuration directory (typically <code>~/.i2p</code>)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$PLUGIN</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">This plugin's directory (<code>$CONFIG/plugins/name</code>)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$OS</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Operating system: <code>windows</code>, <code>linux</code>, <code>mac</code></td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;"><code>$ARCH</code></td><td style="border:1px solid var(--color-border); padding:0.5rem;">Architecture: <code>386</code>, <code>amd64</code>, <code>arm64</code></td></tr>
  </tbody>
</table>
### Clients gérés vs. non gérés

**Clients gérés (Recommandés depuis la version 0.9.4):** - Instanciés par ClientAppManager (gestionnaire d’applications client) - Assurent le suivi des références et de l’état - Gestion du cycle de vie facilitée - Meilleure gestion de la mémoire

**Clients non gérés :** - Démarrés par le router, pas de suivi d'état - Doivent gérer proprement plusieurs appels start/stop - Utiliser un état statique ou des fichiers PID pour la coordination - Appelés à l'arrêt du router (à partir de la version 0.7.12-3)

### ShellService (depuis la version 0.9.53 / 1.7.0)

Solution généralisée pour exécuter des programmes externes avec suivi automatique de l’état.

**Fonctionnalités:** - Gère le cycle de vie des processus - Communique avec ClientAppManager - Gestion automatique du PID - Prise en charge multiplateforme

**Utilisation:**

```properties
clientApp.0.main=net.i2p.apps.ShellService
clientApp.0.args=$PLUGIN/bin/myservice.sh
```
Pour les scripts spécifiques à la plateforme:

```properties
clientApp.0.args=$PLUGIN/bin/myservice-$OS.$ARCH
```
**Alternative (ancienne):** Écrire un wrapper Java (adaptateur) qui vérifie le type de système d’exploitation (OS), et appeler `ShellCommand` avec le fichier `.bat` ou `.sh` approprié.

---

## Procédure d’installation

### Processus d’installation de l’utilisateur

1. L’utilisateur colle l’URL du plugin dans la page de configuration des plugins de la Console du Router (`/configplugins`)
2. Le Router télécharge le fichier du plugin
3. Vérification de la signature (échoue si la clé est inconnue et que le mode strict est activé)
4. Vérification de l’intégrité du ZIP
5. Extraction et analyse de `plugin.config`
6. Vérification de la compatibilité des versions (`min-i2p-version`, `min-java-version`, etc.)
7. Détection d’un conflit de nom de l’application web
8. Arrêt du plugin existant en cas de mise à jour
9. Validation du répertoire (doit se trouver sous `plugins/`)
10. Extraction de tous les fichiers vers le répertoire du plugin
11. Mise à jour de `plugins.config`
12. Démarrage du plugin (sauf si `dont-start-at-install=true`)

### Sécurité et confiance

**Gestion des clés:** - Modèle de confiance « First-key-seen » (première clé vue) pour les nouveaux signataires - Seules les clés jrandom et zzz sont pré-intégrées - À partir de 0.9.14.1, les clés inconnues sont rejetées par défaut - Une propriété avancée peut outrepasser ce comportement pour le développement

**Restrictions d'installation :** - Les archives doivent être extraites uniquement dans le répertoire du plugin - Le programme d'installation refuse les chemins en dehors de `plugins/` - Les plugins peuvent accéder à des fichiers ailleurs après l'installation - Pas de sandboxing ni d'isolation des privilèges

---

## Mécanisme de mise à jour

### Processus de vérification des mises à jour

1. Router lit `updateURL.su3` (préféré) ou `updateURL` depuis plugin.config
2. Requête HTTP HEAD ou GET partielle pour récupérer les octets 41-56
3. Extraire la chaîne de version depuis le fichier distant
4. Comparer avec la version installée en utilisant VersionComparator
5. Si plus récente, demander à l'utilisateur ou télécharger automatiquement (selon les paramètres)
6. Arrêter le plugin
7. Installer la mise à jour
8. Démarrer le plugin (à moins que la préférence de l'utilisateur n'ait changé)

### Comparaison des versions

Versions analysées en composants séparés par des points/tirets/underscores (tirets bas): - `1.2.3` < `1.2.4` - `1.2.3` < `1.2.3-1` - `2.0.0` > `1.9.9`

**Longueur maximale:** 16 octets (doit correspondre à l’en-tête SUD/SU3)

### Meilleures pratiques de mise à jour

1. Toujours incrémenter la version pour chaque publication
2. Tester le parcours de mise à jour depuis la version précédente
3. Prendre en compte `router-restart-required` pour les changements majeurs
4. Fournir à la fois `updateURL` et `updateURL.su3` pendant la migration
5. Utiliser un suffixe de numéro de build pour les tests (`1.2.3-456`)

---

## Classpath et bibliothèques standard

### Toujours disponible dans le classpath

Les fichiers JAR suivants de `$I2P/lib` sont toujours dans le classpath pour I2P 0.9.30+:

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">JAR</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Plugin Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2p.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Core API</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Required for all plugins</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>mstreaming.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Streaming API</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Most plugins need</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>streaming.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Streaming implementation</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Most plugins need</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>i2ptunnel.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">I2PTunnel</td><td style="border:1px solid var(--color-border); padding:0.6rem;">HTTP/server plugins</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>router.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Router internals</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Rarely needed, avoid if possible</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>javax.servlet.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Servlet 3.1, JSP 2.3 API</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Plugins with servlets/JSPs</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>jasper-runtime.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Jasper compiler/runtime</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Plugins with JSPs</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>commons-el.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">EL 3.0 API</td><td style="border:1px solid var(--color-border); padding:0.6rem;">JSPs using expression language</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>jetty-i2p.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Jetty utilities</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Plugins starting Jetty</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>org.mortbay.jetty.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Jetty 9 base</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Custom Jetty instances</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>sam.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">SAM API</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Rarely needed</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>addressbook.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Subscription/blockfile</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Use NamingService instead</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>routerconsole.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Console libraries</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Not public API, avoid</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>jbigi.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Native crypto</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Plugins should not need</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>systray.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">URL launcher</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Rarely needed</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>wrapper.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Service wrapper</td><td style="border:1px solid var(--color-border); padding:0.6rem;">Plugins should not need</td></tr>
  </tbody>
</table>
### Remarques particulières

**commons-logging.jar:** - Vide depuis 0.9.30 - Avant 0.9.30: Apache Tomcat JULI - Avant 0.9.24: Commons Logging + JULI - Avant 0.9: Commons Logging uniquement

**jasper-compiler.jar:** - Vide depuis Jetty 6 (0.9)

**systray4j.jar:** - Retiré dans la version 0.9.26

### Non présent dans le Classpath (doit être spécifié)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">JAR</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contents</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>jstl.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Standard Taglib</td><td style="border:1px solid var(--color-border); padding:0.6rem;">JSP tag libraries</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.6rem;"><code>standard.jar</code></td><td style="border:1px solid var(--color-border); padding:0.6rem;">Standard Taglib</td><td style="border:1px solid var(--color-border); padding:0.6rem;">JSP tag libraries</td></tr>
  </tbody>
</table>
### Spécification du classpath (chemin de classes Java)

**Dans clients.config :**

```properties
clientApp.0.classpath=$PLUGIN/lib/mylib.jar,$I2P/lib/i2p.jar
```
**Dans webapps.config:**

```properties
webapps.mywebapp.classpath=$PLUGIN/lib/mylib.jar,$I2P/lib/jstl.jar
```
**Important:** À partir de la 0.7.13-3, les classpath sont spécifiques à chaque thread, et non à l’échelle de la JVM. Spécifiez le classpath complet pour chaque client.

---

## Exigences relatives à la version de Java

### Exigences actuelles (octobre 2025)

**I2P 2.10.0 et versions antérieures:** - Minimum: Java 7 (requis depuis 0.9.24, janvier 2016) - Recommandé: Java 8 ou supérieur

**I2P 2.11.0 et ultérieures (À VENIR):** - **Minimum : Java 17+** (annoncé dans les notes de version 2.9.0) - Avertissement sur deux versions consécutives (2.9.0 → 2.10.0 → 2.11.0)

### Stratégie de compatibilité des plugins

**Pour une compatibilité maximale (jusqu'à I2P 2.10.x):**

```xml
<javac source="1.7" target="1.7" />
```
```properties
min-java-version=1.7
```
**Pour les fonctionnalités de Java 8+ :**

```xml
<javac source="1.8" target="1.8" />
```
```properties
min-java-version=1.8
```
**Pour les fonctionnalités de Java 11+ :**

```xml
<javac source="11" target="11" />
```
```properties
min-java-version=11
```
**Préparation pour 2.11.0+:**

```xml
<javac source="17" target="17" />
```
```properties
min-java-version=17
min-i2p-version=2.11.0
```
### Meilleures pratiques de compilation

**Lors de la compilation avec un JDK plus récent pour une cible plus ancienne:**

```xml
<javac source="1.7" target="1.7" 
       bootclasspath="${java7.home}/jre/lib/rt.jar"
       includeantruntime="false" />
```
Cela empêche d'utiliser des API non disponibles dans la version cible de Java.

---

## Compression Pack200 - OBSOLÈTE

### Mise à jour critique : n'utilisez pas Pack200

**Statut:** DÉPRÉCIÉ ET SUPPRIMÉ

La spécification d’origine recommandait vivement la compression Pack200 pour une réduction de taille de 60 à 65 %. **Cela n’est plus valable.**

**Chronologie:** - **JEP 336:** Pack200 déprécié en Java 11 (septembre 2018) - **JEP 367:** Pack200 supprimé en Java 14 (mars 2020)

**La spécification officielle des mises à jour I2P indique :** > "Les fichiers JAR et WAR dans l'archive ZIP ne sont plus compressés avec pack200 comme documenté ci-dessus pour les fichiers 'su2', parce que les environnements d'exécution Java récents ne le prennent plus en charge."

**Que faire :**

1. **Retirez pack200 des processus de compilation immédiatement**
2. **Utilisez la compression ZIP standard**
3. **Envisagez des alternatives :**
   - ProGuard/R8 pour la réduction du code
   - UPX pour les binaires natifs
   - Algorithmes de compression modernes (zstd, brotli) si un décompresseur personnalisé est fourni

**Pour les plugins existants:** - Anciens routers (0.7.11-5 jusqu'à Java 10) peuvent encore décompresser pack200 (format de compression Java) - Nouveaux routers (Java 11+) ne peuvent pas décompresser pack200 - Republiez les plugins sans compression pack200

---

## Clés de signature et sécurité

### Génération de clés (format SU3)

Utilisez le script `makeplugin.sh` du dépôt i2p.scripts :

```bash
# Generate new signing key
./makeplugin.sh keygen

# Keys stored in ~/.i2p-plugin-keys/
```
**Détails clés:** - Algorithme: RSA_SHA512_4096 - Format: certificat X.509 - Stockage: format de keystore Java (magasin de clés)

### Signature des plugins

```bash
# Create signed su3 file
./makeplugin.sh sign myplugin.zip myplugin.su3 keyname

# Verify signature
./makeplugin.sh verify myplugin.su3
```
### Bonnes pratiques de gestion des clés

1. **Générez une fois, protégez pour toujours**
   - Les Routers rejettent les noms de clé dupliqués avec des clés différentes
   - Les Routers rejettent les clés dupliquées avec des noms de clé différents
   - Mises à jour rejetées en cas de non-correspondance clé/nom

2. **Stockage sécurisé**
   - Sauvegardez le magasin de clés en toute sécurité
   - Utilisez une phrase de passe robuste
   - Ne validez jamais dans le système de gestion de versions

3. **Rotation des clés**
   - Non pris en charge par l'architecture actuelle
   - Planifier l'utilisation des clés à long terme
   - Envisager des schémas multisignatures pour le développement en équipe

### Signature DSA héritée (XPI2P)

**Statut :** Fonctionnel mais obsolète

Signatures DSA-1024 utilisées par le format xpi2p: - signature de 40 octets - clé publique de 172 caractères en base64 - NIST-800-57 recommande (L=2048, N=224) au minimum - I2P utilise des paramètres plus faibles (L=1024, N=160)

**Recommandation :** Utilisez plutôt SU3 avec RSA-4096.

---

## Directives de développement des plugins

### Bonnes pratiques essentielles

1. **Documentation**
   - Fournir un README clair avec des instructions d’installation
   - Documenter les options de configuration et les valeurs par défaut
   - Inclure un journal des modifications avec chaque version
   - Préciser les versions d’I2P/Java requises

2. **Optimisation de la taille**
   - Inclure uniquement les fichiers nécessaires
   - Ne jamais inclure les fichiers JAR du router
   - Séparer les paquets d’installation et de mise à jour (bibliothèques dans lib/)
   - ~~Utiliser la compression Pack200~~ **OBSOLÈTE - Utiliser un ZIP standard**

3. **Configuration**
   - Ne jamais modifier `plugin.config` pendant l'exécution
   - Utiliser un fichier de configuration distinct pour les paramètres d'exécution
   - Documenter les paramètres nécessaires du router (ports SAM, tunnels, etc.)
   - Respecter la configuration existante de l'utilisateur

4. **Utilisation des ressources**
   - Éviter une consommation de bande passante agressive par défaut
   - Mettre en œuvre des limites raisonnables d'utilisation du CPU
   - Libérer les ressources lors de l'arrêt
   - Utiliser des threads daemon (threads de démon) le cas échéant

5. **Tests**
   - Tester l’installation/la mise à niveau/la désinstallation sur toutes les plateformes
   - Tester les mises à jour depuis la version précédente
   - Vérifier l’arrêt/le redémarrage de l’application web pendant les mises à jour
   - Tester avec la version minimale d’I2P prise en charge

6. **Système de fichiers**
   - N'écrivez jamais dans `$I2P` (peut être en lecture seule)
   - Écrivez les données d'exécution dans `$PLUGIN` ou `$CONFIG`
   - Utilisez `I2PAppContext` pour la découverte des répertoires
   - Ne présumez pas de l'emplacement de `$CWD`

7. **Compatibilité**
   - Ne dupliquez pas les classes I2P standard
   - Étendez les classes si nécessaire, ne les remplacez pas
   - Vérifiez `min-i2p-version`, `min-jetty-version` dans plugin.config
   - Testez avec des versions I2P plus anciennes si vous les prenez en charge

8. **Gestion de l'arrêt**
   - Configurer correctement les `stopargs` dans clients.config
   - Enregistrer les hooks d'arrêt: `I2PAppContext.addShutdownTask()`
   - Gérer proprement plusieurs appels de démarrage/arrêt
   - Mettre tous les threads en mode démon

9. **Sécurité**
   - Validez toutes les entrées externes
   - N'appelez jamais `System.exit()`
   - Respectez la vie privée des utilisateurs
   - Suivez les bonnes pratiques de codage sécurisé

10. **Licences**
    - Spécifier clairement la licence du plug-in
    - Respecter les licences des bibliothèques intégrées
    - Inclure les mentions d’attribution requises
    - Fournir l’accès au code source si requis

### Considérations avancées

**Gestion des fuseaux horaires:** - Router définit le fuseau horaire de la JVM sur UTC - Fuseau horaire réel de l'utilisateur : propriété `I2PAppContext` `i2p.systemTimeZone`

**Découverte de l'annuaire:**

```java
// Plugin directory
String pluginDir = I2PAppContext.getGlobalContext()
    .getAppDir().getAbsolutePath() + "/plugins/" + pluginName;

// Or use $PLUGIN variable in clients.config args
```
**Numérotation des versions:** - Utiliser le versionnage sémantique (major.minor.patch) - Ajouter un numéro de build pour les tests (1.2.3-456) - Veiller à une progression strictement croissante des mises à jour

**Accès aux classes du router :** - Évitez généralement les dépendances à `router.jar` - Utilisez plutôt les API publiques dans `i2p.jar` - De futures versions d'I2P pourraient restreindre l'accès aux classes du router

**Prévention des crashs de la JVM (historique):** - Corrigé dans 0.7.13-3 - Utiliser correctement les chargeurs de classes - Éviter de mettre à jour des JAR dans un plugin en cours d'exécution - Concevoir pour permettre un redémarrage lors de la mise à jour si nécessaire

---

## Greffons pour Eepsite

### Aperçu

Les plugins peuvent fournir des eepsites complets avec leurs propres instances Jetty (serveur web Java) et I2PTunnel.

### Architecture

**N'essayez pas de :** - Installer dans une eepsite (site hébergé sur I2P) existante - Fusionner avec l'eepsite par défaut du router - Supposer la disponibilité d'une seule eepsite

**Au lieu de:** - Démarrer une nouvelle instance I2PTunnel (via l'interface en ligne de commande) - Démarrer une nouvelle instance Jetty - Configurer les deux dans `clients.config`

### Structure d'exemple

```
plugins/myeepsite/
├── plugin.config
├── clients.config          # Starts Jetty + I2PTunnel
├── eepsite/
│   ├── jetty.xml          # Requires variable substitution
│   ├── docroot/
│   ├── webapps/
│   └── logs/
└── lib/
    └── [dependencies]
```
### Substitution de variables dans jetty.xml

Utilisez la variable `$PLUGIN` pour les chemins:

```xml
<Set name="resourceBase">$PLUGIN/eepsite/docroot</Set>
```
Router effectue une substitution lors du démarrage du plug-in.

### Exemples

Implémentations de référence : - **zzzot plugin** - Tracker de torrents - **pebble plugin** - Plateforme de blog

Tous deux sont disponibles sur la page des plugins de zzz (interne à I2P).

---

## Intégration à la console

### Liens de la barre de synthèse

Ajouter un lien cliquable à la barre récapitulative de la console du router :

```properties
consoleLinkName=My Plugin
consoleLinkURL=/myplugin/
consoleLinkTooltip=Open My Plugin Interface
```
Versions localisées :

```properties
consoleLinkName_de=Mein Plugin
consoleLinkTooltip_de=Öffne Mein Plugin Schnittstelle
```
### Icônes de la console

**Fichier image (depuis 0.9.20):**

```properties
console-icon=/myicon.png
```
Chemin relatif à `consoleLinkURL` si spécifié (depuis la version 0.9.53), sinon relatif au nom de l’application web.

**Icône intégrée (depuis 0.9.25) :**

```properties
icon-code=iVBORw0KGgoAAAANSUhEUgAAA...Base64EncodedPNG...
```
Générer avec:

```bash
base64 -w 0 icon-32x32.png
```
Ou Java:

```bash
java -cp i2p.jar net.i2p.data.Base64 encode icon.png
```
Exigences: - 32x32 pixels - format PNG - encodé en Base64 (sans sauts de ligne)

---

## Internationalisation

### Ensembles de traduction

**Pour les traductions de base d'I2P :** - Placez les JAR dans `console/locale/` - Doivent contenir des resource bundles (fichiers de ressources) pour les applications I2P existantes - Nommage : `messages_xx.properties` (xx = code de langue)

**Pour les traductions spécifiques aux plugins :** - Inclure dans `console/webapps/*.war` - Ou inclure dans `lib/*.jar` - Utiliser la méthode standard ResourceBundle de Java

### Chaînes localisées dans plugin.config

```properties
description=My awesome plugin
description_de=Mein tolles Plugin
description_fr=Mon plugin génial
description_es=Mi plugin increíble
```
Champs pris en charge: - `description_xx` - `consoleLinkName_xx` - `consoleLinkTooltip_xx`

### Traduction du thème de la console

Les thèmes dans `console/themes/` sont automatiquement ajoutés au chemin de recherche des thèmes.

---

## Plugins spécifiques à la plateforme

### Approche par paquets séparés

Utilisez des noms de plugins différents pour chaque plateforme:

```properties
# Windows package
name=myplugin-windows

# Linux package  
name=myplugin-linux

# macOS package
name=myplugin-mac
```
### Approche de substitution de variables

Un seul plugin.config avec des variables de plateforme :

```properties
name=myplugin
updateURL.su3=http://myplugin.i2p/downloads/myplugin-$OS-$ARCH.su3
```
Dans clients.config:

```properties
clientApp.0.main=net.i2p.apps.ShellService
clientApp.0.args=$PLUGIN/bin/myapp-$OS-$ARCH
```
### Détection du système d’exploitation à l’exécution

Approche en Java pour l’exécution conditionnelle :

```java
String os = System.getProperty("os.name").toLowerCase();
if (os.contains("win")) {
    // Windows-specific code
} else if (os.contains("nix") || os.contains("nux")) {
    // Linux-specific code
} else if (os.contains("mac")) {
    // macOS-specific code
}
```
---

## Dépannage

### Problèmes courants

**Le plugin ne démarre pas :** 1. Vérifiez la compatibilité de la version I2P (`min-i2p-version`) 2. Vérifiez la version de Java (`min-java-version`) 3. Vérifiez les journaux du router pour détecter des erreurs 4. Vérifiez que tous les fichiers JAR requis sont dans le classpath (chemin de classes Java)

**Application Web inaccessible :** 1. Confirmez que `webapps.config` ne la désactive pas 2. Vérifiez la compatibilité de la version de Jetty (`min-jetty-version`) 3. Vérifiez que `web.xml` est présent (la recherche d’annotations n’est pas prise en charge) 4. Vérifiez qu’il n’y a pas de conflit de noms d’applications Web

**Échec de la mise à jour :** 1. Vérifiez que le numéro de version a été incrémenté 2. Vérifiez que la signature correspond à la clé de signature 3. Assurez-vous que le nom du plugin correspond à la version installée 4. Passez en revue les paramètres `update-only`/`install-only`

**Impossible d'arrêter le programme externe :** 1. Utilisez ShellService pour une gestion automatique du cycle de vie 2. Implémentez une gestion correcte de `stopargs` 3. Vérifiez le nettoyage du fichier PID 4. Vérifiez la terminaison du processus

### Journalisation de débogage

Activer la journalisation de débogage sur le router :

```
logger.record.net.i2p.router.web.ConfigPluginsHandler=DEBUG
```
Consultez les journaux:

```
~/.i2p/logs/log-router-0.txt
```
---

## Informations de référence

### Spécifications officielles

- [Spécification des plugins](/docs/specs/plugin/)
- [Format de configuration](/docs/specs/configuration/)
- [Spécification des mises à jour](/docs/specs/updates/)
- [Cryptographie](/docs/specs/cryptography/)

### Historique des versions d’I2P

**Version actuelle:** - **I2P 2.10.0** (8 septembre 2025)

**Versions majeures depuis 0.9.53:** - 2.10.0 (sept. 2025) - annonce Java 17+ - 2.9.0 (juin 2025) - avertissement Java 17+ - 2.8.0 (oct. 2024) - tests de cryptographie post-quantique - 2.6.0 (mai 2024) - blocage d'I2P-over-Tor - 2.4.0 (déc. 2023) - améliorations de la sécurité de NetDB - 2.2.0 (mars 2023) - contrôle de congestion - 2.1.0 (janv. 2023) - améliorations du réseau - 2.0.0 (nov. 2022) - protocole de transport SSU2 - 1.7.0/0.9.53 (févr. 2022) - ShellService, substitution de variables - 0.9.15 (sept. 2014) - format SU3 introduit

**Numérotation des versions:** - série 0.9.x: Jusqu'à la version 0.9.53 - série 2.x: À partir de la version 2.0.0 (introduction de SSU2, nouvelle version du transport SSU)

### Ressources pour les développeurs

**Code source:** - Dépôt principal: https://i2pgit.org/I2P_Developers/i2p.i2p - Miroir GitHub: https://github.com/i2p/i2p.i2p

**Exemples de plugins:** - zzzot (tracker BitTorrent) - pebble (plateforme de blog) - i2p-bote (messagerie sans serveur) - orchid (client Tor) - seedless (échange de pairs)

**Outils de compilation:** - makeplugin.sh - Génération et signature de clés - Disponible dans le dépôt i2p.scripts - Automatise la création et la vérification des fichiers su3 (format de mise à jour signé)

### Assistance communautaire

**Forums:** - [Forum I2P](https://i2pforum.net/) - [zzz.i2p](http://zzz.i2p/) (interne à I2P)

**IRC/Chat:** - #i2p-dev sur OFTC - I2P IRC au sein du réseau

---

## Annexe A : Exemple complet de plugin.config

```properties
# Required fields
name=example-plugin
signer=developer@mail.i2p
version=1.2.3

# Update configuration
updateURL.su3=http://example.i2p/plugins/example-$OS-$ARCH.su3
min-i2p-version=2.0.0
min-java-version=17

# Display information
date=1698796800000
author=Example Developer <developer@mail.i2p>
websiteURL=http://example.i2p/
license=Apache-2.0

description=An example I2P plugin demonstrating best practices
description_de=Ein Beispiel-I2P-Plugin zur Demonstration bewährter Praktiken
description_es=Un plugin I2P de ejemplo que demuestra las mejores prácticas

# Console integration
consoleLinkName=Example Plugin
consoleLinkName_de=Beispiel-Plugin
consoleLinkURL=/example/
consoleLinkTooltip=Open the Example Plugin control panel
consoleLinkTooltip_de=Öffne das Beispiel-Plugin-Kontrollfeld
console-icon=/icon.png

# Installation behavior
dont-start-at-install=false
router-restart-required=false

# Platform requirements (informational)
required-platform-OS=All platforms supported
other-requirements=Requires 512MB free disk space
```
---

## Annexe B : Exemple complet de clients.config

```properties
# Main service client (managed)
clientApp.0.main=com.example.plugin.MainService
clientApp.0.name=Example Plugin Main Service
clientApp.0.delay=30
clientApp.0.args=$PLUGIN/config.properties --port=7656
clientApp.0.stopargs=shutdown
clientApp.0.uninstallargs=cleanup
clientApp.0.classpath=$PLUGIN/lib/example.jar,$I2P/lib/i2p.jar,$I2P/lib/mstreaming.jar

# External program via ShellService
clientApp.1.main=net.i2p.apps.ShellService
clientApp.1.name=Example Native Helper
clientApp.1.delay=35
clientApp.1.args=$PLUGIN/bin/helper-$OS-$ARCH --config $PLUGIN/helper.conf
clientApp.1.classpath=$I2P/lib/i2p.jar

# Jetty eepsite
clientApp.2.main=net.i2p.jetty.JettyStart
clientApp.2.name=Example Eepsite
clientApp.2.delay=40
clientApp.2.args=$PLUGIN/eepsite/jetty.xml
clientApp.2.stopargs=$PLUGIN/eepsite/jetty.xml stop
clientApp.2.classpath=$PLUGIN/lib/example-web.jar,$I2P/lib/i2p.jar

# I2PTunnel for eepsite
clientApp.3.main=net.i2p.i2ptunnel.TunnelControllerGroup
clientApp.3.name=Example Eepsite Tunnel
clientApp.3.delay=45
clientApp.3.args=$PLUGIN/eepsite/i2ptunnel.config
```
---

## Annexe C : Exemple complet de webapps.config

```properties
# Disable autostart for admin webapp
webapps.example-admin.startOnLoad=false

# Main webapp with classpath
webapps.example.startOnLoad=true
webapps.example.classpath=$PLUGIN/lib/example-core.jar,$PLUGIN/lib/commons-utils.jar,$I2P/lib/jstl.jar,$I2P/lib/standard.jar

# Legacy support (pre-0.7.12-9)
plugin.example.startOnLoad=true
```
---

## Annexe D : Liste de contrôle de migration (de 0.9.53 à 2.10.0)

### Modifications requises

- [ ] **Supprimer la compression Pack200 du processus de build**
  - Supprimer les tâches pack200 des scripts Ant/Maven/Gradle
  - Republier les plug-ins existants sans pack200

- [ ] **Revoir les exigences de version de Java**
  - Envisager d'exiger Java 11+ pour les nouvelles fonctionnalités
  - Prévoir l'exigence de Java 17+ pour I2P 2.11.0
  - Mettre à jour `min-java-version` dans plugin.config

- [ ] **Mettre à jour la documentation**
  - Supprimer les références à Pack200
  - Mettre à jour les exigences de version de Java
  - Mettre à jour les références de version d'I2P (0.9.x → 2.x)

### Modifications recommandées

- [ ] **Renforcer les signatures cryptographiques**
  - Migrer de XPI2P vers SU3 si ce n'est pas déjà fait
  - Utiliser des clés RSA-4096 pour les nouveaux plugins

- [ ] **Tirer parti des nouvelles fonctionnalités (si vous utilisez 0.9.53+)**
  - Utilisez les variables `$OS` / `$ARCH` pour des mises à jour spécifiques à la plateforme
  - Utilisez ShellService pour les programmes externes
  - Utilisez le classpath amélioré des applications web (fonctionne pour n'importe quel nom de WAR)

- [ ] **Tester la compatibilité**
  - Tester sur I2P 2.10.0
  - Vérifier avec Java 8, 11, 17
  - Tester sur Windows, Linux, macOS

### Améliorations facultatives

- [ ] Implémenter un ServletContextListener approprié (écouteur de contexte Servlet)
- [ ] Ajouter des descriptions localisées
- [ ] Fournir une icône pour la console
- [ ] Améliorer la gestion de l'arrêt
- [ ] Ajouter une journalisation complète
- [ ] Écrire des tests automatisés
