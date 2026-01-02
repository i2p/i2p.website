---
title: "Clients Gérés"
description: "Comment les applications gérées par le routeur s'intègrent avec ClientAppManager et le mappeur de ports"
slug: "managed-clients"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## 1. Aperçu général

Les entrées dans [`clients.config`](/docs/specs/configuration/#clients-config) indiquent au router quelles applications lancer au démarrage. Chaque entrée peut s'exécuter en tant que client **géré** (préféré) ou en tant que client **non géré**. Les clients gérés collaborent avec `ClientAppManager`, qui :

- Instancie l'application et suit l'état du cycle de vie pour la console du routeur
- Expose les contrôles de démarrage/arrêt à l'utilisateur et impose des arrêts propres à la sortie du routeur
- Héberge un **registre de clients** léger et un **mappeur de ports** afin que les applications puissent découvrir les services des autres

Les clients non gérés invoquent simplement une méthode `main()` ; utilisez-les uniquement pour du code legacy qui ne peut pas être modernisé.

## 2. Implémenter un client géré

Les clients gérés doivent implémenter soit `net.i2p.app.ClientApp` (pour les applications destinées aux utilisateurs) soit `net.i2p.router.app.RouterApp` (pour les extensions de router). Fournissez l'un des constructeurs ci-dessous afin que le gestionnaire puisse fournir les arguments de contexte et de configuration :

```java
public MyClientApp(I2PAppContext context, ClientAppManager manager, String[] args)
```
```java
public MyRouterApp(RouterContext context, ClientAppManager manager, String[] args)
```
Le tableau `args` contient les valeurs configurées dans `clients.config` ou les fichiers individuels dans `clients.config.d/`. Étendez les classes d'assistance `ClientApp` / `RouterApp` lorsque possible pour hériter du câblage de cycle de vie par défaut.

### 2.1 Lifecycle Methods

Les clients gérés doivent implémenter :

- `startup()` - effectuer l'initialisation et retourner rapidement. Doit appeler `manager.notify()` au moins une fois pour passer de l'état INITIALIZED.
- `shutdown(String[] args)` - libérer les ressources et arrêter les threads d'arrière-plan. Doit appeler `manager.notify()` au moins une fois pour changer l'état vers STOPPING ou STOPPED.
- `getState()` - informer la console si l'application est en cours d'exécution, en démarrage, en arrêt, ou en échec

Le gestionnaire appelle ces méthodes lorsque les utilisateurs interagissent avec la console.

### 2.2 Advantages

- Rapports d'état précis dans la console du routeur
- Redémarrages propres sans fuite de threads ou de références statiques
- Empreinte mémoire réduite une fois l'application arrêtée
- Journalisation et rapport d'erreurs centralisés via le contexte injecté

## 3. Unmanaged Clients (Fallback Mode)

Si la classe configurée n'implémente pas une interface gérée, le routeur la lance en invoquant `main(String[] args)` et ne peut pas suivre le processus résultant. La console affiche des informations limitées et les hooks d'arrêt peuvent ne pas s'exécuter. Réservez ce mode aux scripts ou aux utilitaires ponctuels qui ne peuvent pas adopter les API gérées.

## 4. Client Registry

Les clients gérés et non gérés peuvent s'enregistrer auprès du gestionnaire afin que d'autres composants puissent récupérer une référence par nom :

```java
manager.register(this);
```
L'enregistrement utilise la valeur de retour de `getName()` du client comme clé de registre. Les enregistrements connus incluent `console`, `i2ptunnel`, `Jetty`, `outproxy` et `update`. Récupérez un client avec `ClientAppManager.getRegisteredApp(String name)` pour coordonner les fonctionnalités (par exemple, la console interrogeant Jetty pour obtenir des détails d'état).

Notez que le registre client et le mappeur de ports sont des systèmes séparés. Le registre client permet la communication inter-applications par recherche de nom, tandis que le mappeur de ports associe les noms de services aux combinaisons hôte:port pour la découverte de services.

## 3. Clients non gérés (Mode de secours)

Le mappeur de ports offre un répertoire simple pour les services TCP internes. Enregistrez les ports de loopback afin que les collaborateurs évitent les adresses codées en dur :

```java
context.portMapper().register(PortMapper.SVC_HTTPS_PROXY, 4445);
```
Ou avec une spécification explicite de l'hôte :

```java
context.portMapper().register(PortMapper.SVC_HTTP_PROXY, "127.0.0.1", 4444);
```
Recherchez les services en utilisant `PortMapper.getPort(String name)` (retourne -1 si non trouvé) ou `getPort(String name, int defaultPort)` (retourne la valeur par défaut si non trouvé). Vérifiez le statut d'enregistrement avec `isRegistered(String name)` et récupérez l'hôte enregistré avec `getActualHost(String name)`.

Constantes courantes du service de mappage de ports provenant de `net.i2p.util.PortMapper` :

- `SVC_CONSOLE` - Console du routeur (port par défaut 7657)
- `SVC_HTTP_PROXY` - Proxy HTTP (port par défaut 4444)
- `SVC_HTTPS_PROXY` - Proxy HTTPS (port par défaut 4445)
- `SVC_I2PTUNNEL` - Gestionnaire I2PTunnel
- `SVC_SAM` - Pont SAM (port par défaut 7656)
- `SVC_SAM_SSL` - Pont SAM SSL
- `SVC_SAM_UDP` - SAM UDP
- `SVC_BOB` - Pont BOB (port par défaut 2827)
- `SVC_EEPSITE` - Eepsite standard (port par défaut 7658)
- `SVC_HTTPS_EEPSITE` - Eepsite HTTPS
- `SVC_IRC` - Tunnel IRC (port par défaut 6668)
- `SVC_SUSIDNS` - SusiDNS

Remarque : `httpclient`, `httpsclient` et `httpbidirclient` sont des types de tunnel i2ptunnel (utilisés dans la configuration `tunnel.N.type`), et non des constantes de service de mappage de ports.

## 4. Registre des clients

### 2.1 Méthodes de cycle de vie

À partir de la version 0.9.42, le router prend en charge la répartition de la configuration dans des fichiers individuels au sein du répertoire `clients.config.d/`. Chaque fichier contient les propriétés d'un seul client avec toutes les propriétés préfixées par `clientApp.0.` :

```
clientApp.0.main=net.i2p.router.web.RouterConsoleRunner
clientApp.0.name=Router Console
clientApp.0.args=7657 ::1,127.0.0.1 ./webapps/
clientApp.0.delay=0
clientApp.0.onBoot=true
```
C'est l'approche recommandée pour les nouvelles installations et les plugins.

### 2.2 Avantages

Pour des raisons de rétrocompatibilité, le format traditionnel utilise une numérotation séquentielle :

```
clientApp.0.main=net.i2p.router.web.RouterConsoleRunner
clientApp.0.name=Router Console
clientApp.0.args=7657 ::1,127.0.0.1 ./webapps/
clientApp.1.main=net.i2p.apps.systray.UrlLauncher
clientApp.1.name=URL Launcher
clientApp.1.delay=5
```
### 6.3 Configuration Properties

**Requis :** - `main` - Nom complet de la classe implémentant ClientApp ou RouterApp, ou contenant la méthode statique `main(String[] args)`

**Optionnel :** - `name` - Nom d'affichage pour la console du router (par défaut le nom de la classe) - `args` - Arguments séparés par des espaces ou des tabulations (prend en charge les chaînes entre guillemets) - `delay` - Secondes avant le démarrage (par défaut 120) - `onBoot` - Force `delay=0` si vrai - `startOnLoad` - Active/désactive le client (par défaut vrai)

**Spécifique au plugin :** - `stopargs` - Arguments passés lors de l'arrêt - `uninstallargs` - Arguments passés lors de la désinstallation du plugin - `classpath` - Entrées de classpath supplémentaires séparées par des virgules

**Substitution de variables pour les plugins :** - `$I2P` - Répertoire de base I2P - `$CONFIG` - Répertoire de configuration utilisateur (par ex., ~/.i2p) - `$PLUGIN` - Répertoire du plugin - `$OS` - Nom du système d'exploitation - `$ARCH` - Nom de l'architecture

## 5. Port Mapper

- Privilégier les clients gérés ; ne recourir aux clients non gérés que lorsque c'est absolument nécessaire.
- Garder l'initialisation et l'arrêt légers afin que les opérations de console restent réactives.
- Utiliser des noms de registre et de port descriptifs pour que les outils de diagnostic (et les utilisateurs finaux) comprennent ce que fait un service.
- Éviter les singletons statiques - s'appuyer sur le contexte et le gestionnaire injectés pour partager les ressources.
- Appeler `manager.notify()` lors de toutes les transitions d'état pour maintenir un statut de console précis.
- Si vous devez exécuter dans une JVM séparée, documenter comment les journaux et diagnostics sont exposés à la console principale.
- Pour les programmes externes, envisager d'utiliser ShellService (ajouté dans la version 1.7.0) pour bénéficier des avantages des clients gérés.

## 6. Format de configuration

Les clients gérés ont été introduits dans la **version 0.9.4** (17 décembre 2012) et restent l'architecture recommandée depuis la **version 2.10.0** (9 septembre 2025). Les API principales sont restées stables sans aucun changement incompatible durant cette période :

- Signatures des constructeurs inchangées
- Méthodes de cycle de vie (startup, shutdown, getState) inchangées
- Méthodes d'enregistrement ClientAppManager inchangées
- Méthodes d'enregistrement et de recherche PortMapper inchangées

Améliorations notables : - **0.9.42 (2019)** - structure de répertoire clients.config.d/ pour les fichiers de configuration individuels - **1.7.0 (2021)** - ShellService ajouté pour le suivi d'état des programmes externes - **2.10.0 (2025)** - Version actuelle sans modifications de l'API des clients gérés

La prochaine version majeure nécessitera Java 17+ au minimum (exigence d'infrastructure, et non une modification de l'API).

## References

- [Spécification de clients.config](/docs/specs/configuration/#clients-config)
- [Spécification des fichiers de configuration](/docs/specs/configuration/)
- [Index de la documentation technique I2P](/docs/)
- [Javadoc de ClientAppManager](https://i2p.github.io/i2p.i2p/net/i2p/app/ClientAppManager.html) (API 0.9.66)
- [Javadoc de PortMapper](https://i2p.github.io/i2p.i2p/net/i2p/util/PortMapper.html) (API 0.9.66)
- [Interface ClientApp](https://i2p.github.io/i2p.i2p/net/i2p/app/ClientApp.html) (API 0.9.66)
- [Interface RouterApp](https://i2p.github.io/i2p.i2p/net/i2p/router/app/RouterApp.html) (API 0.9.66)
- [Javadoc alternative (version stable)](https://docs.i2p-projekt.de/javadoc/)
- [Javadoc alternative (miroir clearnet)](https://eyedeekay.github.io/javadoc-i2p/)

> **Remarque :** Le réseau I2P héberge une documentation complète sur http://idk.i2p/javadoc-i2p/ qui nécessite un router I2P pour y accéder. Pour un accès clearnet, utilisez le miroir GitHub Pages ci-dessus.
