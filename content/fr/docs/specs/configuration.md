---
title: "Configuration du Router"
description: "Options et formats de configuration pour les I2P routers et les clients I2P"
slug: "configuration"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

## Aperçu

Ce document fournit une spécification technique exhaustive des fichiers de configuration I2P utilisés par le router et diverses applications. Il couvre les spécifications des formats de fichiers, les définitions des propriétés et les détails d’implémentation vérifiés par rapport au code source d’I2P et à la documentation officielle.

### Portée

- Fichiers et formats de configuration du router
- Configurations des applications clientes
- Configurations de tunnel I2PTunnel
- Spécifications des formats de fichiers et implémentation
- Fonctionnalités spécifiques à une version et dépréciations

### Notes d’implémentation

Les fichiers de configuration sont lus et écrits à l'aide des méthodes `DataHelper.loadProps()` et `storeProps()` de la bibliothèque principale d'I2P. Le format du fichier diffère sensiblement du format sérialisé utilisé dans les protocoles I2P (voir [Spécification des structures communes - Correspondance des types](/docs/specs/common-structures/#type-mapping)).

---

## Format général du fichier de configuration

Les fichiers de configuration I2P suivent un format Java Properties modifié, avec des exceptions et des contraintes spécifiques.

### Spécification du format

Basé sur [Java Properties](http://docs.oracle.com/javase/1.5.0/docs/api/java/util/Properties.html#load%28java.io.InputStream%29) avec les différences essentielles suivantes :

#### Encodage

- **DOIT** utiliser l'encodage UTF-8 (PAS ISO-8859-1 comme dans les propriétés Java standard)
- Implémentation : Utilise les utilitaires `DataHelper.getUTF8()` pour toutes les opérations sur les fichiers

#### Séquences d’échappement

- **AUCUNE** séquence d’échappement n’est reconnue (y compris le caractère de barre oblique inverse `\`)
- La continuation de ligne n’est **PAS** prise en charge
- Les caractères de barre oblique inverse sont traités comme des caractères littéraux

#### Caractères de commentaire

- `#` introduit un commentaire à n'importe quelle position sur une ligne
- `;` introduit un commentaire **uniquement** lorsqu'il est en colonne 1
- `!` n'introduit **PAS** un commentaire (diffère de Java Properties)

#### Séparateurs clé-valeur

- `=` est le **SEUL** séparateur clé-valeur valide
- `:` n'est **PAS** reconnu comme séparateur
- Les caractères d'espacement ne sont **PAS** reconnus comme des séparateurs

#### Gestion des espaces blancs

- Les espaces blancs en début et en fin ne sont **PAS** supprimés pour les clés
- Les espaces blancs en début et en fin **SONT** supprimés pour les valeurs

#### Traitement des lignes

- Les lignes sans `=` sont ignorées (traitées comme des commentaires ou des lignes vides)
- Les valeurs vides (`key=`) sont prises en charge à partir de la version 0.9.10
- Les clés avec des valeurs vides sont stockées et récupérées normalement

#### Restrictions de caractères

**Les clés ne doivent PAS contenir**: - `#` (signe dièse) - `=` (signe égal) - `\n` (caractère de saut de ligne) - Ne peuvent pas commencer par `;` (point-virgule)

**Les valeurs ne doivent PAS contenir**: - `#` (signe dièse/hash) - `\n` (caractère de saut de ligne) - Ne peuvent pas commencer ni se terminer par `\r` (retour chariot) - Ne peuvent pas commencer ni se terminer par des caractères d'espacement (supprimés automatiquement)

### Tri des fichiers

Les fichiers de configuration n'ont pas besoin d'être triés par clé. Cependant, la plupart des applications I2P trient les clés par ordre alphabétique lors de l'écriture des fichiers de configuration afin de faciliter : - Édition manuelle - Opérations diff (comparaison) de contrôle de version - Lisibilité humaine

### Détails d’implémentation

#### Lecture des fichiers de configuration

```java
// Method signature from net.i2p.data.DataHelper
public static Properties loadProps(File file)
```
**Comportement**: - Lit des fichiers encodés en UTF-8 - Applique toutes les règles de format décrites ci-dessus - Valide les restrictions de caractères - Retourne un objet Properties vide si le fichier n'existe pas - Lève une `IOException` en cas d'erreurs de lecture

#### Écriture des fichiers de configuration

```java
// Method signature from net.i2p.data.DataHelper
public static void storeProps(Properties props, File file)
```
**Comportement**: - Écrit des fichiers encodés en UTF-8 - Trie les clés par ordre alphabétique (sauf si OrderedProperties est utilisé) - Définit les permissions du fichier au mode 600 (lecture/écriture utilisateur uniquement) à partir de la version 0.8.1 - Lève `IllegalArgumentException` pour les caractères non valides dans les clés ou les valeurs - Lève `IOException` en cas d'erreurs d'écriture

#### Validation du format

L'implémentation effectue une validation stricte : - Les clés et les valeurs sont vérifiées afin de détecter les caractères interdits - Les entrées invalides provoquent des exceptions lors des opérations d'écriture - La lecture ignore silencieusement les lignes mal formées (lignes sans `=`)

### Exemples de formats

#### Fichier de configuration valide

```properties
# This is a comment
; This is also a comment (column 1 only)
key.with.dots=value with spaces
another_key=value=with=equals
empty.value=
numeric.value=12345
unicode.value=こんにちは
```
#### Exemples de configurations invalides

```properties
# INVALID: Key contains equals sign
invalid=key=value

# INVALID: Key contains hash
invalid#key=value

# INVALID: Value contains newline (implicit)
key=value
continues here

# INVALID: Semicolon comment not in column 1 (treated as key)
 ; not.a.comment=value
```
---

## Configuration de la bibliothèque principale et du router

### Configuration des clients (clients.config)

**Emplacement**: `$I2P_CONFIG_DIR/clients.config` (ancien) ou `$I2P_CONFIG_DIR/clients.config.d/` (moderne)   **Interface de configuration**: console du router à `/configclients`   **Changement de format**: Version 0.9.42 (août 2019)

#### Arborescence des répertoires (Version 0.9.42+)

À partir de la version 0.9.42, le fichier clients.config par défaut est automatiquement scindé en fichiers de configuration individuels :

```
$I2P_CONFIG_DIR/
├── clients.config.d/
│   ├── 00-webConsole.config
│   ├── 01-i2ptunnel.config
│   ├── 02-i2psnark.config
│   ├── 03-susidns.config
│   └── ...
└── clients.config (legacy, auto-migrated)
```
**Comportement de migration**: - Lors de la première exécution après la mise à niveau vers 0.9.42+, le fichier monolithique est scindé automatiquement - Les propriétés des fichiers scindés sont préfixées par `clientApp.0.` - L'ancien format reste pris en charge pour la rétrocompatibilité - Le format scindé permet une paquetisation modulaire et la gestion des plugins

#### Format des propriétés

Les lignes sont de la forme `clientApp.x.prop=val`, où `x` est le numéro de l'application.

**Exigences de numérotation des applications**: - DOIT commencer par 0 - DOIT être consécutive (sans trous) - L'ordre détermine la séquence de démarrage

#### Propriétés obligatoires

##### principal

- **Type**: String (nom de classe entièrement qualifié)
- **Requis**: Oui
- **Description**: Selon le type de client (géré vs non géré), le constructeur ou la méthode `main()` de cette classe sera appelé
- **Exemple**: `clientApp.0.main=net.i2p.router.web.RouterConsoleRunner`

#### Propriétés facultatives

##### nom

- **Type**: Chaîne de caractères
- **Required**: Non
- **Description**: Nom affiché dans la console du router
- **Example**: `clientApp.0.name=Router Console`

##### arguments

- **Type**: Chaîne (séparée par des espaces ou des tabulations)
- **Obligatoire**: Non
- **Description**: Arguments transmis au constructeur de la classe principale ou à la méthode main()
- **Guillemets**: Les arguments contenant des espaces ou des tabulations peuvent être mis entre guillemets avec `'` ou `"`
- **Exemple**: `clientApp.0.args=-d $CONFIG/eepsite`

##### délai

- **Type**: Entier (secondes)
- **Obligatoire**: Non
- **Par défaut**: 120
- **Description**: Nombre de secondes à attendre avant de démarrer le client
- **Surcharges**: Écrasé par `onBoot=true` (fixe le délai à 0)
- **Valeurs spéciales**:
  - `< 0`: Attendre que le router atteigne l'état RUNNING, puis démarrer immédiatement dans un nouveau thread
  - `= 0`: Exécuter immédiatement dans le même thread (les exceptions se propagent vers la console)
  - `> 0`: Démarrer après le délai dans un nouveau thread (les exceptions sont consignées dans les journaux, non propagées)

##### onBoot

- **Type**: Booléen
- **Required**: Non
- **Default**: false
- **Description**: Impose un délai de 0, outrepasse le réglage explicite du délai
- **Use Case**: Démarrer les services critiques immédiatement au démarrage du router

##### startOnLoad

- **Type**: booléen
- **Obligatoire**: Non
- **Valeur par défaut**: true
- **Description**: Indique s'il faut démarrer le client
- **Cas d'utilisation**: Désactiver les clients sans supprimer la configuration

#### Propriétés spécifiques au plugin

Ces propriétés sont utilisées uniquement par les plugins (pas par les clients du noyau):

##### stopargs

- **Type**: Chaîne de caractères (séparée par des espaces ou des tabulations)
- **Description**: Arguments transmis pour arrêter le client
- **Variable Substitution**: Oui (voir ci-dessous)

##### uninstallargs

- **Type**: Chaîne (séparée par des espaces ou des tabulations)
- **Description**: Arguments transmis pour désinstaller le client
- **Variable Substitution**: Oui (voir ci-dessous)

##### classpath (chemin de classes)

- **Type**: String (chemins séparés par des virgules)
- **Description**: Éléments supplémentaires du classpath pour le client
- **Substitution de variables**: Oui (voir ci-dessous)

#### Substitution de variables (plugins uniquement)

Les variables suivantes sont remplacées dans `args`, `stopargs`, `uninstallargs` et `classpath` pour les plugins :

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Variable</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Expands To</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Example</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$I2P</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Base I2P installation directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>/usr/share/i2p</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$CONFIG</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">User configuration directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>~/.i2p</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$PLUGIN</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Plugin directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>~/.i2p/plugins/foo</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$OS</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Operating system name</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>linux</code></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$ARCH</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Architecture name</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>amd64</code></td>
    </tr>
  </tbody>
</table>
**Remarque**: La substitution de variables est effectuée uniquement pour les plugins, pas pour les clients principaux.

#### Types de clients

##### Clients gérés

- Le constructeur est appelé avec les paramètres `RouterContext` et `ClientAppManager`
- Le client doit implémenter l'interface `ClientApp`
- Cycle de vie contrôlé par le router
- Peut être démarré, arrêté et redémarré dynamiquement

##### Clients non gérés

- La méthode `main(String[] args)` est appelée
- S'exécute dans un fil d'exécution séparé
- Le cycle de vie n'est pas géré par le router
- Type de client hérité

#### Exemple de configuration

```properties
# Router Console (core client)
clientApp.0.main=net.i2p.router.web.RouterConsoleRunner
clientApp.0.name=Router Console
clientApp.0.args=-d $CONFIG/eepsite
clientApp.0.delay=0
clientApp.0.onBoot=true
clientApp.0.startOnLoad=true

# I2PTunnel (core client)
clientApp.1.main=net.i2p.i2ptunnel.TunnelControllerGroup
clientApp.1.name=I2PTunnel
clientApp.1.args=
clientApp.1.delay=120
clientApp.1.startOnLoad=true

# Plugin Example
clientApp.2.main=org.example.plugin.PluginMain
clientApp.2.name=Example Plugin
clientApp.2.args=-config $PLUGIN/config.properties
clientApp.2.stopargs=-shutdown
clientApp.2.uninstallargs=-remove $PLUGIN
clientApp.2.classpath=$PLUGIN/lib/plugin.jar,$PLUGIN/lib/dep.jar
clientApp.2.delay=240
clientApp.2.startOnLoad=true
```
---

### Configuration de la journalisation (logger.config)

**Emplacement**: `$I2P_CONFIG_DIR/logger.config`   **Interface de configuration**: Console du router à `/configlogging`

#### Référence des propriétés

##### Configuration du tampon de la console

###### logger.consoleBufferSize

- **Type**: Entier
- **Valeur par défaut**: 20
- **Description**: Nombre maximal de messages de journal à mettre en mémoire tampon dans la console
- **Plage**: 1-1000 recommandé

##### Formatage de la date et de l'heure

###### logger.dateFormat

- **Type**: String (motif SimpleDateFormat)
- **Default**: Selon la locale du système
- **Example**: `HH:mm:ss.SSS`
- **Documentation**: [Java SimpleDateFormat](https://docs.oracle.com/javase/8/docs/api/java/text/SimpleDateFormat.html)

##### Niveaux de journalisation

###### logger.defaultLevel

- **Type**: Énumération
- **Valeur par défaut**: ERROR
- **Valeurs**: `CRIT`, `ERROR`, `WARN`, `INFO`, `DEBUG`
- **Description**: Niveau de journalisation par défaut pour toutes les classes

###### logger.minimumOnScreenLevel

- **Type**: Énumération
- **Par défaut**: CRIT
- **Valeurs**: `CRIT`, `ERROR`, `WARN`, `INFO`, `DEBUG`
- **Description**: Niveau minimal pour les messages affichés à l'écran

###### logger.record.{class}

- **Type**: Énumération
- **Values**: `CRIT`, `ERROR`, `WARN`, `INFO`, `DEBUG`
- **Description**: Surcharge du niveau de journalisation par classe
- **Example**: `logger.record.net.i2p.router.transport.udp=DEBUG`

##### Options d’affichage

###### logger.displayOnScreen

- **Type**: Booléen
- **Par défaut**: true
- **Description**: Indique s’il faut afficher les messages de journal dans la sortie de la console

###### logger.dropDuplicates

- **Type**: Booléen
- **Default**: true
- **Description**: Supprime les messages de journal consécutifs en double

###### logger.dropOnOverflow

- **Type**: Booléen
- **Valeur par défaut**: faux
- **Description**: Abandonner les messages lorsque le tampon est plein (plutôt que de bloquer)

##### Comportement de vidage

###### logger.flushInterval

- **Type**: Entier (secondes)
- **Par défaut**: 29
- **Depuis**: Version 0.9.18
- **Description**: Fréquence à laquelle vider le tampon de journal sur le disque

##### Configuration du format

###### logger.format

- **Type**: Chaîne (séquence de caractères)
- **Description**: Modèle de format de message de journalisation
- **Format Characters**:
  - `d` = date/heure
  - `c` = nom de classe
  - `t` = nom du thread (fil d’exécution)
  - `p` = priorité (niveau de journalisation)
  - `m` = message
- **Example**: `dctpm` produit `[horodatage] [classe] [thread] [niveau] message`

##### Compression (version 0.9.56+)

###### logger.gzip

- **Type**: booléen
- **Par défaut**: false
- **Depuis**: Version 0.9.56
- **Description**: Activer la compression gzip pour les fichiers journaux faisant l'objet d'une rotation

###### logger.minGzipSize

- **Type**: Entier (octets)
- **Valeur par défaut**: 65536
- **Depuis**: Version 0.9.56
- **Description**: Taille de fichier minimale pour déclencher la compression (64 Ko par défaut)

##### Gestion des fichiers

###### logger.logBufferSize

- **Type**: Entier (octets)
- **Valeur par défaut**: 1024
- **Description**: Nombre maximal de messages à mettre en mémoire tampon avant de vider le tampon

###### logger.logFileName

- **Type**: Chaîne (chemin de fichier)
- **Default**: `logs/log-@.txt`
- **Description**: Modèle de nommage du fichier journal (`@` remplacé par le numéro de rotation)

###### logger.logFilenameOverride

- **Type**: Chaîne de caractères (chemin de fichier)
- **Description**: Remplacement du nom du fichier journal (désactive le schéma de rotation)

###### logger.logFileSize

- **Type**: Chaîne de caractères (taille avec unité)
- **Valeur par défaut**: 10M
- **Unités**: K (kilooctets), M (mégaoctets), G (gigaoctets)
- **Exemple**: `50M`, `1G`

###### logger.logRotationLimit

- **Type**: Entier
- **Par défaut**: 2
- **Description**: Numéro maximal de fichier de rotation (log-0.txt à log-N.txt)

#### Exemple de configuration

```properties
# Basic logging configuration
logger.consoleBufferSize=50
logger.dateFormat=yyyy-MM-dd HH:mm:ss.SSS
logger.defaultLevel=WARN
logger.displayOnScreen=true
logger.dropDuplicates=true
logger.dropOnOverflow=false

# Flushing and format
logger.flushInterval=30
logger.format=dctpm

# File management
logger.logBufferSize=2048
logger.logFileName=logs/log-@.txt
logger.logFileSize=25M
logger.logRotationLimit=5

# Compression (0.9.56+)
logger.gzip=true
logger.minGzipSize=131072

# On-screen filtering
logger.minimumOnScreenLevel=ERROR

# Per-class overrides
logger.record.net.i2p.router.transport=INFO
logger.record.net.i2p.router.tunnel=DEBUG
logger.record.net.i2p.crypto=WARN
```
---

### Configuration du plugin

#### Configuration individuelle du plugin (plugins/*/plugin.config)

**Emplacement**: `$I2P_CONFIG_DIR/plugins/{plugin-name}/plugin.config`   **Format**: Format de fichier de configuration I2P standard   **Documentation**: [Spécification du plugin](/docs/specs/plugin/)

##### Propriétés requises

###### nom

- **Type**: Chaîne de caractères
- **Obligatoire**: Oui
- **Description**: Nom d'affichage du plugin
- **Exemple**: `name=I2P Plugin Example`

###### clé

- **Type**: Chaîne (clé publique)
- **Obligatoire**: Oui (à omettre pour les plugins signés SU3)
- **Description**: Clé publique de signature du plugin utilisée pour la vérification
- **Format**: Clé de signature encodée en Base64

###### signataire

- **Type**: Chaîne de caractères
- **Required**: Oui
- **Description**: Identité du signataire du plugin
- **Example**: `signer=user@example.i2p`

###### version

- **Type**: Chaîne (format VersionComparator)
- **Required**: Oui
- **Description**: Version du plugin pour la vérification des mises à jour
- **Format**: Versionnage sémantique ou format comparable personnalisé
- **Example**: `version=1.2.3`

##### Propriétés d’affichage

###### date

- **Type**: Long (type entier 64 bits; horodatage Unix en millisecondes)
- **Description**: Date de publication du plugin

###### auteur

- **Type**: Chaîne de caractères
- **Description**: Nom de l'auteur du plugin

###### websiteURL

- **Type**: Chaîne (URL)
- **Description**: URL du site du plugin

###### updateURL

- **Type** : Chaîne de caractères (URL)
- **Description** : URL de vérification des mises à jour pour le plug-in

###### updateURL.su3

- **Type**: Chaîne (URL)
- **Since**: Version 0.9.15
- **Description**: URL de mise à jour au format SU3 (recommandée)

###### description

- **Type**: String
- **Description**: Description du plugin en anglais

###### description_{language}

- **Type**: Chaîne de caractères
- **Description**: Description localisée du plugin
- **Example**: `description_de=Deutsche Beschreibung`

###### licence

- **Type**: Chaîne de caractères
- **Description**: Identifiant de licence du plugin
- **Exemple**: `license=Apache 2.0`

##### Propriétés d'installation

###### Ne pas démarrer après l’installation

- **Type**: booléen
- **Default**: false
- **Description**: Empêcher le démarrage automatique après l'installation

###### Redémarrage du router requis

- **Type**: Booléen
- **Default**: false
- **Description**: Nécessite un redémarrage du router après l'installation

###### installation seule

- **Type**: booléen
- **Par défaut**: false
- **Description**: Installer une seule fois (aucune mise à jour)

###### mise à jour uniquement

- **Type**: Booléen
- **Default**: false
- **Description**: Mettre à jour uniquement l'installation existante (pas de nouvelle installation)

##### Exemple de configuration de module d'extension

```properties
# Required properties
name=Example I2P Plugin
signer=developer@mail.i2p
version=1.5.0

# Display properties
author=Plugin Developer
websiteURL=http://plugin.example.i2p
updateURL=http://plugin.example.i2p/update.xpi2p
updateURL.su3=http://plugin.example.i2p/update.su3
description=Example plugin demonstrating configuration
description_de=Beispiel-Plugin zur Demonstration der Konfiguration
license=MIT

# Installation behavior
dont-start-at-install=false
router-restart-required=false
```
#### Configuration globale des plugins (plugins.config)

**Emplacement**: `$I2P_CONFIG_DIR/plugins.config`   **Objectif**: activer/désactiver globalement les plugins installés

##### Format des propriétés

```properties
plugin.{name}.startOnLoad=true|false
```
- `{name}`: Nom du plugin indiqué dans plugin.config
- `startOnLoad`: Indique s'il faut démarrer le plugin au démarrage du router

##### Exemple

```properties
plugin.i2psnark.startOnLoad=true
plugin.susimail.startOnLoad=true
plugin.susidns.startOnLoad=true
plugin.i2pbote.startOnLoad=false
```
---

### Configuration des applications Web (webapps.config)

**Emplacement**: `$I2P_CONFIG_DIR/webapps.config`   **Objectif**: Activer/désactiver et configurer des applications web

#### Format des propriétés

##### webapps.{name}.startOnLoad

- **Type**: Booléen
- **Description**: Indique s'il faut démarrer l'application web au lancement du router
- **Format**: `webapps.{name}.startOnLoad=true|false`

##### webapps.{name}.classpath

- **Type**: Chaîne (chemins séparés par des espaces ou des virgules)
- **Description**: Éléments supplémentaires du classpath pour l'application web
- **Format**: `webapps.{name}.classpath=[paths]`

#### Substitution de variables

Les chemins prennent en charge les substitutions de variables suivantes :

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Variable</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Expands To</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Context</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$I2P</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Base I2P directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Core webapps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$CONFIG</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">User config directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">All webapps</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;"><code>$PLUGIN</code></td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Plugin directory</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Plugin webapps</td>
    </tr>
  </tbody>
</table>
#### Résolution du classpath

- **Applications web principales**: Chemins relatifs à `$I2P/lib`
- **Applications web des plugins**: Chemins relatifs à `$CONFIG/plugins/{appname}/lib`

#### Exemple de configuration

```properties
# Router console
webapps.routerconsole.startOnLoad=true
webapps.routerconsole.classpath=routerconsole.jar

# I2PSnark
webapps.i2psnark.startOnLoad=true
webapps.i2psnark.classpath=i2psnark.jar

# SusiDNS
webapps.susidns.startOnLoad=true
webapps.susidns.classpath=susidns.jar

# Plugin webapp example
webapps.exampleplugin.startOnLoad=false
webapps.exampleplugin.classpath=$PLUGIN/lib/webapp.jar,$PLUGIN/lib/deps.jar
```
---

### Configuration du Router (router.config)

**Emplacement**: `$I2P_CONFIG_DIR/router.config`   **Interface de configuration**: Console du router à `/configadvanced`   **Objectif**: Paramètres essentiels du router et paramètres réseau

#### Catégories de configuration

##### Configuration du réseau

Paramètres de bande passante :

```properties
i2np.bandwidth.inboundKBytesPerSecond=100
i2np.bandwidth.outboundKBytesPerSecond=50
i2np.bandwidth.share.percentage=80
```
Configuration des transports:

```properties
# NTCP (TCP-based transport)
i2np.ntcp.port=8887
i2np.ntcp.enable=true
i2np.ntcp.autoip=true

# SSU (UDP-based transport)
i2np.udp.port=8887
i2np.udp.enable=true

# UPnP/NAT-PMP
i2np.upnp.enable=true
```
##### Comportement du router

```properties
# Tunnel participation
router.maxParticipatingTunnels=200
router.sharePercentage=80

# Updates
router.updatePolicy=notify
router.updateURL=http://update.i2p2.i2p/

# Network integration
router.hiddenMode=false
router.clockSkewOffset=0
```
##### Configuration de la console

```properties
# Language and display
routerconsole.lang=en
routerconsole.country=US
routerconsole.summaryRefresh=60

# Browser
routerconsole.browser=default

# Security
routerconsole.enableCompression=true
```
##### Configuration de l'heure

```properties
# NTP
time.disabled=false
time.sntpServerList=0.pool.ntp.org,1.pool.ntp.org
```
**Remarque**: La configuration du router est étendue. Consultez la console du router à `/configadvanced` pour la référence complète des propriétés.

---

## Fichiers de configuration des applications

### Configuration du carnet d'adresses (addressbook/config.txt)

**Emplacement**: `$I2P_CONFIG_DIR/addressbook/config.txt`   **Application**: SusiDNS   **Objectif**: résolution des noms d'hôte et gestion du carnet d'adresses

#### Emplacements des fichiers

##### router_addressbook

- **Par défaut**: `../hosts.txt`
- **Description**: Carnet d'adresses principal (noms d'hôte à l'échelle du système)
- **Format**: Format standard du fichier hosts

##### privatehosts.txt

- **Emplacement**: `$I2P_CONFIG_DIR/addressbook/privatehosts.txt`
- **Description**: Correspondances de noms d’hôte privés
- **Priorité**: La plus élevée (a priorité sur toutes les autres sources)

##### userhosts.txt

- **Emplacement**: `$I2P_CONFIG_DIR/addressbook/userhosts.txt`
- **Description**: Correspondances de noms d’hôte ajoutées par l’utilisateur
- **Gestion**: Via l’interface SusiDNS

##### hosts.txt

- **Emplacement**: `$I2P_CONFIG_DIR/addressbook/hosts.txt`
- **Description**: Carnet d'adresses public téléchargé
- **Source**: Flux d'abonnement

#### Service de noms

##### BlockfileNamingService (Par défaut depuis 0.8.8)

Format de stockage: - **Fichier**: `hostsdb.blockfile` - **Emplacement**: `$I2P_CONFIG_DIR/addressbook/` - **Performances**: résolutions ~10x plus rapides que hosts.txt - **Format**: format de base de données binaire

Service de noms hérité: - **Format**: Fichier hosts.txt en texte brut - **Statut**: Obsolète mais toujours pris en charge - **Cas d'usage**: Édition manuelle, gestion de versions

#### Règles concernant les noms d’hôte

Les noms d'hôte I2P doivent être conformes à :

1. **Exigence relative au TLD**: Doit se terminer par `.i2p`
2. **Longueur maximale**: 67 caractères au total
3. **Jeu de caractères**: `[a-z]`, `[0-9]`, `.` (point), `-` (tiret)
4. **Casse**: minuscules uniquement
5. **Restrictions de début**: Ne peut pas commencer par `.` ou `-`
6. **Motifs interdits**: Ne peut pas contenir `..`, `.-` ou `-.` (depuis 0.6.1.33)
7. **Réservé**: Noms d’hôte Base32 `*.b32.i2p` (52 caractères de base32.b32.i2p)

##### Exemples valides

```
example.i2p
my-site.i2p
test.example.i2p
site123.i2p
```
##### Exemples non valides

```
example.com          # Wrong TLD
-invalid.i2p         # Starts with hyphen
invalid..i2p         # Contains double dot
invalid.-.i2p        # Contains dot-hyphen
UPPERCASE.I2P        # Must be lowercase
verylonghostnameover67charactersthatexceedsthemaximumlength.i2p  # Too long
```
#### Gestion des abonnements

##### subscriptions.txt

- **Emplacement**: `$I2P_CONFIG_DIR/addressbook/subscriptions.txt`
- **Format**: Une URL par ligne
- **Par défaut**: `http://i2p-projekt.i2p/hosts.txt`

##### Format du flux d’abonnement (depuis la version 0.9.26)

Format de flux avancé avec des métadonnées:

```
#
# I2P Address Book Subscription Feed
# Format: hostname=destination [#property=value ...]
#

example.i2p=base64destination #added=20250101 #src=manual
another.i2p=base64destination #added=20250102 #src=feed1
```
Propriétés des métadonnées: - `added`: Date d'ajout du nom d'hôte (format YYYYMMDD) - `src`: Identifiant de la source - `sig`: Signature facultative

**Rétrocompatibilité**: Le format simple hostname=destination est toujours pris en charge.

#### Exemple de configuration

```properties
# Address book locations
router_addressbook=../hosts.txt
privatehosts.txt=$CONFIG/addressbook/privatehosts.txt
userhosts.txt=$CONFIG/addressbook/userhosts.txt
hosts.txt=$CONFIG/addressbook/hosts.txt

# Naming service
naming.service=BlockfileNamingService
naming.service.blockfile.location=$CONFIG/addressbook/hostsdb.blockfile

# Subscriptions
subscriptions.txt=$CONFIG/addressbook/subscriptions.txt
subscriptions.schedule=daily
subscriptions.proxy=false
```
---

### Configuration d'I2PSnark (i2psnark.config.d/i2psnark.config)

**Emplacement**: `$I2P_CONFIG_DIR/i2psnark.config.d/i2psnark.config`   **Application**: client BitTorrent I2PSnark   **Interface de configuration**: Interface Web à l'adresse http://127.0.0.1:7657/i2psnark

#### Arborescence des répertoires

```
$I2P_CONFIG_DIR/i2psnark.config.d/
├── i2psnark.config
├── [torrent-hash-1]/
│   └── *.config
├── [torrent-hash-2]/
│   └── *.config
└── ...
```
#### Configuration principale (i2psnark.config)

Configuration par défaut minimale:

```properties
i2psnark.dir=i2psnark
```
Propriétés supplémentaires gérées via l'interface web:

```properties
# Basic settings
i2psnark.dir=i2psnark
i2psnark.autoStart=false
i2psnark.openTrackers=true

# Network settings
i2psnark.uploaders=8
i2psnark.upBW=40
i2psnark.seedPct=100

# I2CP settings
i2psnark.i2cpHost=127.0.0.1
i2psnark.i2cpPort=7654
```
#### Configuration individuelle du torrent

**Emplacement**: `$I2P_CONFIG_DIR/i2psnark.config.d/[torrent-hash]/*.config`   **Format**: Paramètres par torrent   **Gestion**: Automatique (via l'interface web)

Les propriétés comprennent : - Paramètres de téléversement/téléchargement spécifiques au torrent - Priorités des fichiers - Informations du tracker - Limites du nombre de pairs

**Remarque**: Les paramètres des torrents sont principalement gérés via l'interface web. La modification manuelle n'est pas recommandée.

#### Organisation des données du torrent

Le stockage des données est distinct de la configuration :

```
$I2P_CONFIG_DIR/i2psnark/          # Data directory
├── *.torrent                       # Torrent metadata files
├── *.torrent.downloaded/           # Downloaded file directories
├── file1.dat                       # Direct file downloads
└── ...

$I2P_CONFIG_DIR/i2psnark.config.d/ # Configuration directory
├── i2psnark.config                 # Main config
└── [hashes]/                       # Per-torrent configs
```
---

### Configuration d'I2PTunnel (i2ptunnel.config)

**Emplacement**: `$I2P_CONFIG_DIR/i2ptunnel.config` (hérité) ou `$I2P_CONFIG_DIR/i2ptunnel.config.d/` (moderne)   **Interface de configuration**: Console du router à `/i2ptunnel`   **Changement de format**: Version 0.9.42 (août 2019)

#### Structure des répertoires (Version 0.9.42+)

À partir de la version 0.9.42, le fichier i2ptunnel.config par défaut est automatiquement scindé :

```
$I2P_CONFIG_DIR/
├── i2ptunnel.config.d/
│   ├── http-proxy/
│   │   └── tunnel.config
│   ├── irc-proxy/
│   │   └── tunnel.config
│   ├── ssh-service/
│   │   └── tunnel.config
│   └── ...
└── i2ptunnel.config (legacy, auto-migrated)
```
**Différence critique de format**: - **Format monolithique**: Propriétés préfixées par `tunnel.N.` - **Format scindé**: Propriétés **PAS** préfixées (p. ex., `description=`, et non `tunnel.0.description=`)

#### Comportement de migration

Lors de la première exécution après la mise à jour vers 0.9.42: 1. Le fichier i2ptunnel.config existant est lu 2. Des configurations de tunnel individuelles sont créées dans i2ptunnel.config.d/ 3. Les préfixes sont supprimés des propriétés dans les fichiers séparés 4. Le fichier d'origine est sauvegardé 5. L'ancien format reste pris en charge pour la rétrocompatibilité

#### Sections de configuration

La configuration d’I2PTunnel est documentée en détail dans la section [Référence de configuration d’I2PTunnel](#i2ptunnel-configuration-reference) ci-dessous. Les descriptions des propriétés s’appliquent aux formats monolithique (`tunnel.N.property`) et séparé (`property`).

---

## Référence de configuration d'I2PTunnel

Cette section fournit une référence technique complète pour toutes les propriétés de configuration d’I2PTunnel. Les propriétés sont présentées au format scindé (sans le préfixe `tunnel.N.`). Pour le format monolithique, préfixez toutes les propriétés avec `tunnel.N.` où N est le numéro du tunnel.

**Important**: Les propriétés décrites sous la forme `tunnel.N.option.i2cp.*` sont implémentées dans I2PTunnel (outil I2P de gestion des tunnels) et ne sont **PAS** prises en charge via d'autres interfaces telles que le protocole I2CP ou SAM API.

### Propriétés de base

#### tunnel.N.description (description)

- **Type**: Chaîne de caractères
- **Context**: Tous les tunnels
- **Description**: Description de tunnel lisible par l'utilisateur pour l'affichage dans l'interface utilisateur
- **Example**: `description=HTTP Proxy for outproxy access`

#### tunnel.N.name (nom)

- **Type**: Chaîne de caractères
- **Contexte**: Tous les tunnels
- **Obligatoire**: Oui
- **Description**: Identifiant de tunnel unique et nom d'affichage
- **Exemple**: `name=I2P HTTP Proxy`

#### tunnel.N.type (type)

- **Type**: Énumération
- **Contexte**: Tous les tunnels
- **Obligatoire**: Oui
- **Valeurs**:
  - `client` - tunnel client générique
  - `httpclient` - client proxy HTTP
  - `ircclient` - tunnel client IRC
  - `socksirctunnel` - proxy SOCKS IRC
  - `sockstunnel` - proxy SOCKS (version 4, 4a, 5)
  - `connectclient` - client proxy CONNECT
  - `streamrclient` - client Streamr
  - `server` - tunnel serveur générique
  - `httpserver` - tunnel serveur HTTP
  - `ircserver` - tunnel serveur IRC
  - `httpbidirserver` - serveur HTTP bidirectionnel
  - `streamrserver` - serveur Streamr

#### tunnel.N.interface (interface)

- **Type**: Chaîne (adresse IP ou nom d’hôte)
- **Contexte**: tunnels client uniquement
- **Par défaut**: 127.0.0.1
- **Description**: Interface locale à laquelle se lier pour les connexions entrantes
- **Note de sécurité**: Se lier à 0.0.0.0 autorise les connexions distantes
- **Exemple**: `interface=127.0.0.1`

#### tunnel.N.listenPort (listenPort)

- **Type**: Entier
- **Contexte**: Tunnels clients uniquement
- **Plage**: 1-65535
- **Description**: Port local d'écoute pour les connexions client
- **Exemple**: `listenPort=4444`

#### tunnel.N.targetHost (targetHost)

- **Type**: Chaîne (adresse IP ou nom d'hôte)
- **Contexte**: Tunnels serveur uniquement
- **Description**: Serveur local vers lequel rediriger les connexions
- **Exemple**: `targetHost=127.0.0.1`

#### tunnel.N.targetPort (targetPort)

- **Type**: Entier
- **Context**: Uniquement les tunnels serveur
- **Range**: 1-65535
- **Description**: Port sur targetHost auquel se connecter
- **Example**: `targetPort=80`

#### tunnel.N.targetDestination (targetDestination)

- **Type**: Chaîne de caractères (destinations séparées par des virgules ou des espaces)
- **Contexte**: Uniquement pour les tunnels clients
- **Format**: `destination[:port][,destination[:port]]`
- **Description**: Destinations I2P auxquelles se connecter
- **Exemples**:
  - `targetDestination=example.i2p`
  - `targetDestination=example.i2p:8080`
  - `targetDestination=site1.i2p,site2.i2p:8080`

#### tunnel.N.i2cpHost (i2cpHost)

- **Type**: Chaîne (adresse IP ou nom d’hôte)
- **Par défaut**: 127.0.0.1
- **Description**: Adresse de l’interface I2CP du router I2P
- **Remarque**: Ignoré lors de l’exécution dans le contexte du router
- **Exemple**: `i2cpHost=127.0.0.1`

#### tunnel.N.i2cpPort (i2cpPort)

- **Type**: Entier
- **Valeur par défaut**: 7654
- **Plage**: 1-65535
- **Description**: Port I2CP du router I2P
- **Remarque**: Ignoré lors de l'exécution dans le contexte du router
- **Exemple**: `i2cpPort=7654`

#### tunnel.N.startOnLoad (startOnLoad)

- **Type**: Booléen
- **Default**: true
- **Description**: Indique s'il faut démarrer le tunnel au chargement d'I2PTunnel
- **Example**: `startOnLoad=true`

### Configuration du proxy

#### tunnel.N.proxyList (proxyList)

- **Type**: Chaîne (noms d’hôte séparés par des virgules ou des espaces)
- **Contexte**: Proxies HTTP et SOCKS uniquement
- **Description**: Liste des hôtes d’outproxy (mandataire de sortie vers l’Internet classique)
- **Exemple**: `proxyList=outproxy.example.i2p,backup.example.i2p`

### Configuration du serveur

#### tunnel.N.privKeyFile (privKeyFile)

- **Type**: Chaîne (chemin de fichier)
- **Context**: Serveurs et tunnels clients persistants
- **Description**: Fichier contenant les clés privées d'une destination persistante
- **Path**: Absolu ou relatif au répertoire de configuration d'I2P
- **Example**: `privKeyFile=eepsite/eepPriv.dat`

#### tunnel.N.spoofedHost (spoofedHost)

- **Type**: Chaîne (nom d'hôte)
- **Contexte**: Serveurs HTTP uniquement
- **Par défaut**: Nom d'hôte Base32 de la destination
- **Description**: Valeur de l'en-tête Host transmise au serveur local
- **Exemple**: `spoofedHost=example.i2p`

#### tunnel.N.spoofedHost.NNNN (spoofedHost.NNNN)

- **Type**: Chaîne (nom d'hôte)
- **Contexte**: Serveurs HTTP uniquement
- **Description**: Redéfinition de l'hôte virtuel pour un port entrant spécifique
- **Cas d'utilisation**: Héberger plusieurs sites sur des ports différents
- **Exemple**: `spoofedHost.8080=site1.example.i2p`

### Options spécifiques au client

#### tunnel.N.sharedClient (sharedClient)

- **Type**: Booléen
- **Context**: Tunnels client uniquement
- **Default**: false
- **Description**: Indique si plusieurs clients peuvent partager ce tunnel
- **Example**: `sharedClient=false`

#### tunnel.N.option.persistentClientKey (persistentClientKey)

- **Type**: booléen
- **Contexte**: Uniquement pour les tunnels clients
- **Valeur par défaut**: false
- **Description**: Stocker et réutiliser les clés de destination entre les redémarrages
- **Conflit**: Incompatible avec `i2cp.newDestOnResume=true`
- **Exemple**: `option.persistentClientKey=true`

### Options I2CP (implémentation d'I2PTunnel)

**Important**: Ces propriétés sont préfixées par `option.i2cp.` mais sont **implémentées dans I2PTunnel**, et non dans la couche de protocole I2CP. Elles ne sont pas disponibles via I2CP ou les API SAM.

#### tunnel.N.option.i2cp.delayOpen (option.i2cp.delayOpen)

- **Type**: Booléen
- **Context**: Uniquement pour les tunnels client
- **Default**: false
- **Description**: Retarder la création du tunnel jusqu’à la première connexion
- **Use Case**: Économiser des ressources pour les tunnels rarement utilisés
- **Example**: `option.i2cp.delayOpen=false`

#### tunnel.N.option.i2cp.newDestOnResume (option.i2cp.newDestOnResume)

- **Type**: booléen
- **Context**: Tunnels client uniquement
- **Default**: false
- **Requires**: `i2cp.closeOnIdle=true`
- **Conflict**: Mutuellement exclusif avec `persistentClientKey=true`
- **Description**: Créer une nouvelle destination après expiration du délai d'inactivité
- **Example**: `option.i2cp.newDestOnResume=false`

#### tunnel.N.option.i2cp.leaseSetPrivateKey (option.i2cp.leaseSetPrivateKey)

- **Type**: Chaîne (clé encodée en base64)
- **Context**: Uniquement pour les tunnels serveur
- **Description**: Clé de chiffrement privée persistante du leaseSet (ensemble de baux)
- **Use Case**: Maintenir un leaseSet chiffré cohérent entre les redémarrages
- **Example**: `option.i2cp.leaseSetPrivateKey=AAAA...base64...`

#### tunnel.N.option.i2cp.leaseSetSigningPrivateKey (option.i2cp.leaseSetSigningPrivateKey)

- **Type**: Chaîne (sigtype:base64)
- **Context**: Tunnels serveur uniquement
- **Format**: `sigtype:base64key`
- **Description**: Clé privée persistante de signature du leaseset
- **Example**: `option.i2cp.leaseSetSigningPrivateKey=7:AAAA...base64...`

### Options spécifiques au serveur

#### tunnel.N.option.enableUniqueLocal (option.enableUniqueLocal)

- **Type**: Booléen
- **Contexte**: Uniquement pour les tunnels serveur
- **Valeur par défaut**: false
- **Description**: Utiliser une adresse IP locale unique par destination I2P distante
- **Cas d'utilisation**: Suivre les adresses IP des clients dans les journaux du serveur
- **Note de sécurité**: Peut réduire l'anonymat
- **Exemple**: `option.enableUniqueLocal=false`

#### tunnel.N.option.targetForPort.NNNN (option.targetForPort.NNNN)

- **Type**: Chaîne (hostname:port)
- **Contexte**: Uniquement pour les tunnels serveur
- **Description**: Remplace targetHost/targetPort pour le port entrant NNNN
- **Cas d'utilisation**: Routage basé sur le port vers différents services locaux
- **Exemple**: `option.targetForPort.8080=localhost:8080`

### Configuration du pool de threads

#### tunnel.N.option.i2ptunnel.usePool (option.i2ptunnel.usePool)

- **Type**: Booléen
- **Contexte**: Tunnels serveur uniquement
- **Par défaut**: true
- **Description**: Utiliser un pool de threads pour la gestion des connexions
- **Remarque**: Toujours false pour les serveurs standard (ignoré)
- **Exemple**: `option.i2ptunnel.usePool=true`

#### tunnel.N.option.i2ptunnel.blockingHandlerCount (option.i2ptunnel.blockingHandlerCount)

- **Type**: Entier
- **Contexte**: Uniquement pour les tunnels serveur
- **Valeur par défaut**: 65
- **Description**: Taille maximale du pool de threads
- **Remarque**: Ignoré pour les serveurs standard
- **Exemple**: `option.i2ptunnel.blockingHandlerCount=100`

### Options du client HTTP

#### tunnel.N.option.i2ptunnel.httpclient.allowInternalSSL (option.i2ptunnel.httpclient.allowInternalSSL)

- **Type**: Booléen
- **Contexte**: Clients HTTP uniquement
- **Par défaut**: false
- **Description**: Autoriser les connexions SSL aux adresses .i2p
- **Exemple**: `option.i2ptunnel.httpclient.allowInternalSSL=false`

#### tunnel.N.option.i2ptunnel.httpclient.disableAddressHelper (option.i2ptunnel.httpclient.disableAddressHelper)

- **Type**: Booléen
- **Contexte**: clients HTTP uniquement
- **Par défaut**: false
- **Description**: Désactiver les liens address helper (assistant d’adresse) dans les réponses du proxy
- **Exemple**: `option.i2ptunnel.httpclient.disableAddressHelper=false`

#### tunnel.N.option.i2ptunnel.httpclient.jumpServers (option.i2ptunnel.httpclient.jumpServers)

- **Type**: Chaîne (URL séparées par des virgules ou des espaces)
- **Contexte**: clients HTTP uniquement
- **Description**: URL de jump server (service de saut) pour la résolution de noms d'hôte
- **Exemple**: `option.i2ptunnel.httpclient.jumpServers=http://jump.i2p/jump,http://stats.i2p/jump`

#### tunnel.N.option.i2ptunnel.httpclient.sendAccept (option.i2ptunnel.httpclient.sendAccept)

- **Type**: Booléen
- **Contexte**: Clients HTTP uniquement
- **Valeur par défaut**: false
- **Description**: Transmettre les en-têtes Accept-* (sauf Accept et Accept-Encoding)
- **Exemple**: `option.i2ptunnel.httpclient.sendAccept=false`

#### tunnel.N.option.i2ptunnel.httpclient.sendReferer (option.i2ptunnel.httpclient.sendReferer)

- **Type**: booléen
- **Context**: clients HTTP uniquement
- **Default**: false
- **Description**: Transmettre les en-têtes Referer via le proxy
- **Privacy Note**: Peut divulguer des informations
- **Example**: `option.i2ptunnel.httpclient.sendReferer=false`

#### tunnel.N.option.i2ptunnel.httpclient.sendUserAgent (option.i2ptunnel.httpclient.sendUserAgent)

- **Type**: Booléen
- **Context**: Clients HTTP uniquement
- **Default**: false
- **Description**: Transmettre les en-têtes User-Agent via le proxy
- **Privacy Note**: Peut divulguer des informations sur le navigateur
- **Example**: `option.i2ptunnel.httpclient.sendUserAgent=false`

#### tunnel.N.option.i2ptunnel.httpclient.sendVia (option.i2ptunnel.httpclient.sendVia)

- **Type**: booléen
- **Contexte**: clients HTTP uniquement
- **Par défaut**: false
- **Description**: Transmettre les en-têtes Via à travers le proxy
- **Exemple**: `option.i2ptunnel.httpclient.sendVia=false`

#### tunnel.N.option.i2ptunnel.httpclient.SSLOutproxies (option.i2ptunnel.httpclient.SSLOutproxies)

- **Type**: Chaîne (destinations séparées par des virgules ou des espaces)
- **Contexte**: clients HTTP uniquement
- **Description**: Outproxies (mandataires sortants) SSL internes au réseau pour HTTPS
- **Exemple**: `option.i2ptunnel.httpclient.SSLOutproxies=ssl-outproxy.i2p`

#### tunnel.N.option.i2ptunnel.useLocalOutproxy (option.i2ptunnel.useLocalOutproxy)

- **Type**: Booléen
- **Contexte**: Clients HTTP uniquement
- **Par défaut**: true
- **Description**: Utiliser les greffons de proxy de sortie locaux enregistrés
- **Exemple**: `option.i2ptunnel.useLocalOutproxy=true`

### Authentification du client HTTP

#### tunnel.N.option.proxyAuth (option.proxyAuth)

- **Type**: Énumération
- **Contexte**: Clients HTTP uniquement
- **Par défaut**: false
- **Valeurs**: `true`, `false`, `basic`, `digest`
- **Description**: Exiger une authentification locale pour l'accès au proxy
- **Remarque**: `true` est équivalent à `basic`
- **Exemple**: `option.proxyAuth=basic`

#### tunnel.N.option.proxy.auth.USER.md5 (option.proxy.auth.USER.md5)

- **Type**: Chaîne (hexadécimal en minuscules de 32 caractères)
- **Contexte**: Clients HTTP uniquement
- **Nécessite**: `proxyAuth=basic` ou `proxyAuth=digest`
- **Description**: Hachage MD5 du mot de passe de l'utilisateur USER
- **Obsolescence**: Utilisez SHA-256 à la place (0.9.56+)
- **Exemple**: `option.proxy.auth.alice.md5=5f4dcc3b5aa765d61d8327deb882cf99`

#### tunnel.N.option.proxy.auth.USER.sha256 (option.proxy.auth.USER.sha256)

- **Type**: Chaîne (hexadécimal en minuscules de 64 caractères)
- **Contexte**: Clients HTTP uniquement
- **Nécessite**: `proxyAuth=digest`
- **Depuis**: Version 0.9.56
- **Norme**: RFC 7616
- **Description**: Hachage SHA-256 du mot de passe de l'utilisateur USER
- **Exemple**: `option.proxy.auth.alice.sha256=5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8`

### Authentification du proxy de sortie

#### tunnel.N.option.outproxyAuth (option.outproxyAuth)

- **Type**: booléen
- **Contexte**: clients HTTP uniquement
- **Valeur par défaut**: false
- **Description**: Envoyer les informations d’authentification à l’outproxy (proxy de sortie)
- **Exemple**: `option.outproxyAuth=false`

#### tunnel.N.option.outproxyUsername (option.outproxyUsername)

- **Type**: Chaîne
- **Context**: Clients HTTP uniquement
- **Requires**: `outproxyAuth=true`
- **Description**: Nom d'utilisateur pour l'authentification outproxy
- **Example**: `option.outproxyUsername=user`

#### tunnel.N.option.outproxyPassword (option.outproxyPassword)

- **Type**: Chaîne de caractères
- **Contexte**: clients HTTP uniquement
- **Requiert**: `outproxyAuth=true`
- **Description**: Mot de passe pour l’authentification de l’outproxy (proxy sortant I2P)
- **Sécurité**: Stocké en clair
- **Exemple**: `option.outproxyPassword=secret`

### Options du client SOCKS

#### tunnel.N.option.i2ptunnel.socks.proxy.default (option.i2ptunnel.socks.proxy.default)

- **Type**: Chaîne (destinations séparées par des virgules ou des espaces)
- **Contexte**: Uniquement pour les clients SOCKS
- **Description**: Mandataires de sortie au sein du réseau pour les ports non spécifiés
- **Exemple**: `option.i2ptunnel.socks.proxy.default=outproxy.i2p`

#### tunnel.N.option.i2ptunnel.socks.proxy.NNNN (option.i2ptunnel.socks.proxy.NNNN)

- **Type**: String (destinations séparées par des virgules ou des espaces)
- **Context**: Clients SOCKS uniquement
- **Description**: Outproxies (proxies de sortie) internes au réseau I2P spécifiquement pour le port NNNN
- **Example**: `option.i2ptunnel.socks.proxy.443=ssl-outproxy.i2p`

#### tunnel.N.option.outproxyType (option.outproxyType)

- **Type**: Enum
- **Contexte**: clients SOCKS uniquement
- **Par défaut**: socks
- **Depuis**: Version 0.9.57
- **Valeurs**: `socks`, `connect` (HTTPS)
- **Description**: Type d'outproxy (proxy de sortie) configuré
- **Exemple**: `option.outproxyType=connect`

### Options du serveur HTTP

#### tunnel.N.option.maxPosts (option.maxPosts)

- **Type**: Entier
- **Contexte**: Serveurs HTTP uniquement
- **Par défaut**: 0 (illimité)
- **Description**: Nombre maximal de requêtes POST provenant d'une Destination (identité I2P) unique par postCheckTime
- **Exemple**: `option.maxPosts=10`

#### tunnel.N.option.maxTotalPosts (option.maxTotalPosts)

- **Type**: Entier
- **Context**: Serveurs HTTP uniquement
- **Default**: 0 (illimité)
- **Description**: Nombre maximal de requêtes POST provenant de toutes les destinations par intervalle postCheckTime
- **Example**: `option.maxTotalPosts=50`

#### tunnel.N.option.postCheckTime (option.postCheckTime)

- **Type**: Entier (secondes)
- **Contexte**: serveurs HTTP uniquement
- **Par défaut**: 300
- **Description**: Fenêtre de temps pour la vérification des limites POST
- **Exemple**: `option.postCheckTime=600`

#### tunnel.N.option.postBanTime (option.postBanTime)

- **Type**: Entier (secondes)
- **Contexte**: Serveurs HTTP uniquement
- **Par défaut**: 1800
- **Description**: Durée de bannissement après dépassement de maxPosts pour une destination donnée
- **Exemple**: `option.postBanTime=3600`

#### tunnel.N.option.postTotalBanTime (option.postTotalBanTime)

- **Type**: Entier (secondes)
- **Contexte**: Serveurs HTTP uniquement
- **Valeur par défaut**: 600
- **Description**: Durée de bannissement après dépassement de maxTotalPosts
- **Exemple**: `option.postTotalBanTime=1200`

### Options de sécurité du serveur HTTP

#### tunnel.N.option.rejectInproxy (option.rejectInproxy)

- **Type**: Booléen
- **Contexte**: Serveurs HTTP uniquement
- **Par défaut**: false
- **Description**: Refuser les connexions qui semblent passer par un inproxy (proxy entrant)
- **Exemple**: `option.rejectInproxy=false`

#### tunnel.N.option.rejectReferer (option.rejectReferer)

- **Type**: Booléen
- **Contexte**: Serveurs HTTP uniquement
- **Par défaut**: false
- **Depuis**: Version 0.9.25
- **Description**: Refuser les connexions avec un en-tête Referer
- **Exemple**: `option.rejectReferer=false`

#### tunnel.N.option.rejectUserAgents (option.rejectUserAgents)

- **Type**: Booléen
- **Contexte**: Serveurs HTTP uniquement
- **Valeur par défaut**: false
- **Depuis**: Version 0.9.25
- **Nécessite**: la propriété `userAgentRejectList`
- **Description**: Rejette les connexions avec un User-Agent correspondant
- **Exemple**: `option.rejectUserAgents=false`

#### tunnel.N.option.userAgentRejectList (option.userAgentRejectList)

- **Type**: Chaîne (chaînes de correspondance séparées par des virgules)
- **Contexte**: Serveurs HTTP uniquement
- **Depuis**: Version 0.9.25
- **Casse**: Correspondance sensible à la casse
- **Spécial**: "none" (depuis 0.9.33) correspond à un User-Agent vide
- **Description**: Liste des motifs User-Agent à rejeter
- **Exemple**: `option.userAgentRejectList=Mozilla,Opera,none`

### Options du serveur IRC

#### tunnel.N.option.ircserver.fakeHostname (option.ircserver.fakeHostname)

- **Type**: Chaîne (modèle de nom d’hôte)
- **Contexte**: Serveurs IRC uniquement
- **Valeur par défaut**: `%f.b32.i2p`
- **Jetons**:
  - `%f` = Hachage de destination base32 complet
  - `%c` = Hachage de destination masqué (voir cloakKey)
- **Description**: Format de nom d’hôte envoyé au serveur IRC
- **Exemple**: `option.ircserver.fakeHostname=%c.irc.i2p`

#### tunnel.N.option.ircserver.cloakKey (option.ircserver.cloakKey)

- **Type**: Chaîne (phrase de passe)
- **Contexte**: Serveurs IRC uniquement
- **Par défaut**: Aléatoire par session
- **Restrictions**: Pas de guillemets ni d’espaces
- **Description**: Phrase de passe pour un masquage de nom d’hôte cohérent
- **Cas d’utilisation**: Suivi persistant de l’utilisateur entre redémarrages/serveurs
- **Exemple**: `option.ircserver.cloakKey=mysecretkey`

#### tunnel.N.option.ircserver.method (option.ircserver.method)

- **Type**: Énumération
- **Contexte**: Serveurs IRC uniquement
- **Valeur par défaut**: user
- **Valeurs**: `user`, `webirc`
- **Description**: Méthode d'authentification pour le serveur IRC
- **Exemple**: `option.ircserver.method=webirc`

#### tunnel.N.option.ircserver.webircPassword (option.ircserver.webircPassword)

- **Type**: Chaîne (mot de passe)
- **Context**: Serveurs IRC uniquement
- **Requires**: `method=webirc`
- **Restrictions**: Pas de guillemets ni d'espaces
- **Description**: Mot de passe pour l'authentification du protocole WEBIRC
- **Example**: `option.ircserver.webircPassword=webircpass`

#### tunnel.N.option.ircserver.webircSpoofIP (option.ircserver.webircSpoofIP)

- **Type**: Chaîne (adresse IP)
- **Contexte**: Serveurs IRC uniquement
- **Requiert**: `method=webirc`
- **Description**: Adresse IP usurpée pour le protocole WEBIRC
- **Exemple**: `option.ircserver.webircSpoofIP=10.0.0.1`

### Configuration SSL/TLS

#### tunnel.N.option.useSSL (option.useSSL)

- **Type**: booléen
- **Valeur par défaut**: false
- **Contexte**: Tous les tunnels
- **Comportement**:
  - **Serveurs**: Utiliser SSL pour les connexions au serveur local
  - **Clients**: Exiger SSL de la part des clients locaux
- **Exemple**: `option.useSSL=false`

#### tunnel.N.option.keystoreFile (option.keystoreFile)

- **Type**: Chaîne de caractères (chemin de fichier)
- **Contexte**: Tunnels clients uniquement
- **Par défaut**: `i2ptunnel-(random).ks`
- **Chemin**: Relatif à `$(I2P_CONFIG_DIR)/keystore/` s'il n'est pas absolu
- **Généré automatiquement**: Créé s'il n'existe pas
- **Description**: Fichier keystore (magasin de clés) contenant la clé privée SSL
- **Exemple**: `option.keystoreFile=my-tunnel.ks`

#### tunnel.N.option.keystorePassword (option.keystorePassword)

- **Type**: Chaîne (mot de passe)
- **Context**: Client tunnels uniquement
- **Default**: changeit
- **Auto-generated**: Mot de passe aléatoire si un nouveau magasin de clés est créé
- **Description**: Mot de passe du magasin de clés SSL
- **Example**: `option.keystorePassword=secretpassword`

#### tunnel.N.option.keyAlias (option.keyAlias)

- **Type**: Chaîne de caractères (alias)
- **Contexte**: Tunnels client uniquement
- **Généré automatiquement**: Créé si une nouvelle clé est générée
- **Description**: Alias de la clé privée dans le keystore (magasin de clés)
- **Exemple**: `option.keyAlias=mytunnel-key`

#### tunnel.N.option.keyPassword (option.keyPassword)

- **Type**: Chaîne (mot de passe)
- **Contexte**: Uniquement pour les tunnels client
- **Généré automatiquement**: Mot de passe aléatoire si une nouvelle clé est créée
- **Description**: Mot de passe pour la clé privée dans le keystore (magasin de clés)
- **Exemple**: `option.keyPassword=keypass123`

### Options génériques pour I2CP et le Streaming

Toutes les propriétés `tunnel.N.option.*` (non spécifiquement documentées ci-dessus) sont transmises à l'interface I2CP et à la bibliothèque de streaming, avec le préfixe `tunnel.N.option.` supprimé.

**Important**: Ces options sont distinctes de celles spécifiques à I2PTunnel. Voir : - [Spécification I2CP](/docs/specs/i2cp/) - [Spécification de la bibliothèque de streaming](/docs/specs/streaming/)

Exemples d’options de streaming :

```properties
option.i2cp.messageReliability=BestEffort
option.i2p.streaming.connectDelay=1000
option.i2p.streaming.maxWindowSize=128
```
### Exemple complet de Tunnel

```properties
# HTTP Proxy (split format without tunnel.N. prefix)
name=I2P HTTP Proxy
description=HTTP proxy for accessing I2P sites and outproxy
type=httpclient
interface=127.0.0.1
listenPort=4444
targetDestination=
sharedClient=true
startOnLoad=true

# I2CP configuration
i2cpHost=127.0.0.1
i2cpPort=7654

# HTTP client options
option.i2ptunnel.httpclient.allowInternalSSL=false
option.i2ptunnel.httpclient.disableAddressHelper=false
option.i2ptunnel.httpclient.jumpServers=http://stats.i2p/cgi-bin/jump.cgi
option.i2ptunnel.httpclient.sendAccept=false
option.i2ptunnel.httpclient.sendReferer=false
option.i2ptunnel.httpclient.sendUserAgent=false

# Proxy authentication
option.proxyAuth=false

# Outproxy configuration
option.i2ptunnel.httpclient.SSLOutproxies=false.i2p
proxyList=false.i2p

# Client behavior
option.persistentClientKey=false
option.i2cp.delayOpen=false

# I2CP tunnel options
option.inbound.length=3
option.outbound.length=3
option.inbound.quantity=2
option.outbound.quantity=2
```
---

## Historique des versions et chronologie des fonctionnalités

### Version 0.9.10 (2013)

**Fonctionnalité**: Prise en charge des valeurs vides dans les fichiers de configuration - Les clés avec des valeurs vides (`key=`) sont désormais prises en charge - Auparavant ignorées ou provoquaient des erreurs d'analyse

### Version 0.9.18 (2015)

**Fonctionnalité**: Configuration de l’intervalle de vidage du journaliseur - Propriété: `logger.flushInterval` (29 secondes par défaut) - Réduit les E/S disque tout en maintenant une latence de journalisation acceptable

### Version 0.9.23 (novembre 2015)

**Changement majeur** : Java 7 requis au minimum - La prise en charge de Java 6 est terminée - Requis pour continuer à recevoir les mises à jour de sécurité

### Version 0.9.25 (2015)

**Fonctionnalités**: options de sécurité du serveur HTTP - `tunnel.N.option.rejectReferer` - Rejeter les connexions avec l'en-tête Referer - `tunnel.N.option.rejectUserAgents` - Rejeter des en-têtes User-Agent spécifiques - `tunnel.N.option.userAgentRejectList` - Modèles de User-Agent à rejeter - **Cas d'utilisation**: Limiter les robots d'exploration et les clients indésirables

### Version 0.9.33 (janvier 2018)

**Fonctionnalité**: Filtrage amélioré de l’User-Agent - la chaîne `userAgentRejectList` "none" correspond à un User-Agent vide - Corrections de bogues supplémentaires pour i2psnark, i2ptunnel, streaming, SusiMail

### Version 0.9.41 (2019)

**Dépréciation**: Protocole BOB supprimé d'Android - les utilisateurs Android doivent migrer vers SAM ou I2CP

### Version 0.9.42 (août 2019)

**Changement majeur**: Scission des fichiers de configuration - `clients.config` scindé en une structure de répertoires `clients.config.d/` - `i2ptunnel.config` scindé en une structure de répertoires `i2ptunnel.config.d/` - Migration automatique lors de la première exécution après mise à niveau - Permet l'empaquetage modulaire et la gestion des plugins - L'ancien format monolithique reste pris en charge

**Fonctionnalités supplémentaires**: - Améliorations des performances de SSU - Prévention inter-réseau (Proposition 147) - Prise en charge initiale des types de chiffrement

### Version 0.9.56 (2021)

**Fonctionnalités** : Améliorations de la sécurité et de la journalisation - `logger.gzip` - Compression Gzip pour les journaux en rotation (valeur par défaut : false) - `logger.minGzipSize` - Taille minimale pour la compression (valeur par défaut : 65536 octets) - `tunnel.N.option.proxy.auth.USER.sha256` - Authentification Digest SHA-256 (RFC 7616) - **Sécurité** : SHA-256 remplace MD5 pour l'authentification Digest

### Version 0.9.57 (janvier 2023)

**Fonctionnalité**: configuration du type d’outproxy (proxy de sortie) SOCKS - `tunnel.N.option.outproxyType` - Sélection du type d’outproxy (socks|connect) - Valeur par défaut: socks - Prise en charge de HTTPS CONNECT pour les outproxies HTTPS

### Version 2.6.0 (juillet 2024)

**Changement incompatible** : I2P via Tor bloqué - Connexions provenant des adresses IP des relais de sortie Tor désormais rejetées - **Raison** : Dégrade les performances d'I2P, gaspille les ressources des relais de sortie Tor - **Impact** : Les utilisateurs accédant à I2P via des relais de sortie Tor seront bloqués - Les relais non-sortie et les clients Tor ne sont pas concernés

### Version 2.10.0 (septembre 2025 - à ce jour)

**Fonctionnalités majeures**: - **Cryptographie post-quantique** disponible (activation facultative via Hidden Service Manager (gestionnaire de service caché)) - **Prise en charge du tracker UDP** pour I2PSnark afin de réduire la charge du tracker - **Stabilité du Hidden Mode (mode caché)** améliorations pour réduire l’épuisement de RouterInfo - Améliorations du réseau pour les routers congestionnés - Traversée UPnP/NAT améliorée - Améliorations de NetDB avec suppression agressive des leaseset - Réductions de l’observabilité des événements du router

**Configuration**: Aucune nouvelle propriété de configuration ajoutée

**Changement critique à venir**: La prochaine version (probablement 2.11.0 ou 3.0.0) nécessitera Java 17 ou une version ultérieure

---

## Dépréciations et changements rétro-incompatibles

### Dépréciations critiques

#### Accès I2P-over-Tor (Version 2.6.0+)

- **Statut**: BLOQUÉ depuis juillet 2024
- **Impact**: Connexions depuis les adresses IP des nœuds de sortie Tor rejetées
- **Raison**: Dégrade les performances du réseau I2P sans offrir d'avantages en matière d'anonymat
- **Affecte**: Uniquement les nœuds de sortie Tor, pas les relais ni les clients Tor classiques
- **Alternative**: Utiliser I2P ou Tor séparément, sans les combiner

#### Authentification Digest MD5

- **Statut**: Obsolète (utilisez SHA-256)
- **Propriété**: `tunnel.N.option.proxy.auth.USER.md5`
- **Raison**: MD5 est cassé sur le plan cryptographique
- **Remplacement**: `tunnel.N.option.proxy.auth.USER.sha256` (depuis 0.9.56)
- **Chronologie**: MD5 toujours pris en charge mais déconseillé

### Modifications de l'architecture de configuration

#### Fichiers de configuration monolithiques (Version 0.9.42+)

- **Concernés**: `clients.config`, `i2ptunnel.config`
- **Statut**: Déprécié au profit d’une structure de répertoires scindée
- **Migration**: Automatique lors de la première exécution après la mise à niveau vers la version 0.9.42
- **Compatibilité**: L’ancien format fonctionne toujours (rétrocompatible)
- **Recommandation**: Utiliser le format scindé pour les nouvelles configurations

### Versions de Java requises

#### Prise en charge de Java 6

- **Fin**: Version 0.9.23 (novembre 2015)
- **Minimum**: Java 7 requis depuis la version 0.9.23

#### Exigence Java 17 (à venir)

- **Statut**: CHANGEMENT CRITIQUE À VENIR
- **Cible**: Prochaine version majeure après 2.10.0 (probablement 2.11.0 ou 3.0.0)
- **Minimum actuel**: Java 8
- **Action requise**: Préparer la migration vers Java 17
- **Calendrier**: Sera annoncé avec les notes de version

### Fonctionnalités supprimées

#### Protocole BOB (Android)

- **Retiré**: Version 0.9.41
- **Plateforme**: Android uniquement
- **Alternative**: protocoles SAM ou I2CP
- **Bureau**: BOB (API simple pour clients I2P) toujours disponible sur les plateformes de bureau

### Migrations recommandées

1. **Authentification**: Migrer de MD5 à SHA-256 pour l'authentification Digest (authentification par condensat)
2. **Format de configuration**: Migrer vers une structure de répertoires séparée pour les clients et les tunnels
3. **Environnement d'exécution Java**: Planifier la mise à niveau vers Java 17 avant la prochaine version majeure
4. **Intégration à Tor**: Ne pas acheminer I2P via les nœuds de sortie Tor

---

## Références

### Documentation officielle

- [Spécification de configuration I2P](/docs/specs/configuration/) - Spécification officielle du format de fichier de configuration
- [Spécification des plugins I2P](/docs/specs/plugin/) - Configuration et empaquetage des plugins
- [Structures communes I2P - Correspondance des types](/docs/specs/common-structures/#type-mapping) - Format de sérialisation des données du protocole
- [Format Java Properties](http://docs.oracle.com/javase/1.5.0/docs/api/java/util/Properties.html#load%28java.io.InputStream%29) - Spécification du format de base

### Code source

- [Dépôt du I2P Java Router](https://github.com/i2p/i2p.i2p) - Miroir GitHub
- [Gitea des développeurs I2P](https://i2pgit.org/I2P_Developers/i2p.i2p) - Dépôt officiel du code source d’I2P
- [DataHelper.java](https://github.com/i2p/i2p.i2p/blob/master/core/java/src/net/i2p/data/DataHelper.java) - Implémentation de l’E/S des fichiers de configuration

### Ressources de la communauté

- [Forum I2P](https://i2pforum.net/) - Discussions communautaires actives et assistance
- [Site web I2P](/) - Site web officiel du projet

### Documentation de l'API

- [DataHelper JavaDoc](https://i2pplus.github.io/javadoc/net/i2p/data/DataHelper.html) - Documentation de l'API pour les méthodes liées aux fichiers de configuration

### Statut de la spécification

- **Dernière mise à jour de la spécification**: janvier 2023 (version 0.9.57)
- **Version I2P actuelle**: 2.10.0 (septembre 2025)
- **Précision technique**: La spécification reste exacte jusqu’à la version 2.10.0 (aucune rupture de compatibilité)
- **Maintenance**: Document évolutif mis à jour lorsque le format de configuration est modifié
