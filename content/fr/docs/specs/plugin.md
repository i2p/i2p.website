---
title: "Spécification des plugins"
description: "Règles d'empaquetage .xpi2p / .su3 pour les plugins I2P"
slug: "plugin"
aliases:
  - "/fr/plugin_spec"
  - "/fr/plugin_spec/"
lastUpdated: "2022-01"
accurateFor: "0.9.53"
type: docs
---

## Aperçu

Ce document spécifie un format de fichier .xpi2p (comme le .xpi de Firefox), mais avec un fichier de description plugin.config simple au lieu d'un fichier XML install.rdf. Ce format de fichier est utilisé à la fois pour les installations initiales de plugins et les mises à jour de plugins.

De plus, ce document fournit un bref aperçu de la façon dont le router installe les plugins, ainsi que les politiques et directives pour les développeurs de plugins.

Le format de fichier .xpi2p de base est le même qu'un fichier i2pupdate.sud (le format utilisé pour les mises à jour du router), mais l'installateur permettra à l'utilisateur d'installer l'addon même s'il ne connaît pas encore la clé du signataire.

À partir de la version 0.9.15, le format de fichier SU3 est pris en charge et est préféré. Ce format permet l'utilisation de clés de signature plus robustes.

> **Note :** Nous ne recommandons plus de distribuer les plugins au format xpi2p. Utilisez le format su3.

La structure de répertoires standard permettra aux utilisateurs d'installer les types d'extensions suivants :

- Applications web de la console
- Nouvel eepsite avec cgi-bin, applications web
- Thèmes de la console
- Traductions de la console
- Programmes Java
- Programmes Java dans une JVM séparée
- N'importe quel script shell ou programme

Un plugin installe tous ses fichiers dans `~/.i2p/plugins/name/` (`%APPDIR%\I2P\plugins\name\` sur Windows). L'installateur empêchera l'installation ailleurs, bien que le plugin puisse accéder aux bibliothèques situées ailleurs lors de l'exécution.

Ceci doit être considéré uniquement comme un moyen de faciliter l'installation, la désinstallation et la mise à niveau, et de réduire les conflits de base entre plugins.

Il n'y a essentiellement aucun modèle de sécurité une fois que le plugin est en cours d'exécution, cependant. Le plugin s'exécute dans la même JVM et avec les mêmes permissions que le router, et a un accès complet au système de fichiers, au router, à l'exécution de programmes externes, etc.

## Détails

foo.xpi2p est un fichier de mise à jour signé (sud) contenant les éléments suivants :

En-tête .sud standard ajouté au début du fichier zip, contenant les éléments suivants :

```text
40-byte DSA signature
16-byte plugin version in UTF-8, padded with trailing zeroes if necessary
```
Fichier Zip contenant les éléments suivants :

### fichier plugin.config

Ce fichier est requis. Il s'agit d'un fichier de configuration I2P standard, contenant les propriétés suivantes :

#### Propriétés Requises

Les quatre propriétés suivantes sont obligatoires. Les trois premières doivent être identiques à celles du plugin installé pour un plugin de mise à jour.

-   **name** - Sera installé dans ce nom de répertoire. Pour les plugins natifs, vous pourriez vouloir des noms séparés dans différents paquets - foo-windows et foo-linux, par exemple.
-   **key** - Clé publique DSA sous forme de 172 caractères B64 se terminant par '='. Omettre pour le format SU3.
-   **signer** - votrenom@mail.i2p recommandé
-   **version** - Doit être dans un format que VersionComparator peut analyser, par exemple 1.2.3-4. 16 octets maximum (doit correspondre à la version sud). Les séparateurs de numéros valides sont '.', '-', et '_'. Cela doit être supérieur à celle du plugin installé pour un plugin de mise à jour.

#### Propriétés d'affichage

Les valeurs des propriétés suivantes sont affichées sur /configplugins dans la console du router si elles sont présentes :

-   **date** - Java time - long int
-   **author** - `yourname@mail.i2p` recommandé
-   **websiteURL** - `http://foo.i2p/`
-   **updateURL** - `http://foo.i2p/foo.xpi2p` - Le vérificateur de mise à jour vérifiera les octets 41-56 à cette URL pour déterminer si une version plus récente est disponible. Depuis la version 1.7.0 (0.9.53), il est possible d'utiliser les variables `$OS` et `$ARCH` dans l'URL. Non recommandé. N'utilisez pas sauf si vous avez précédemment distribué des plugins au format xpi2p.
-   **updateURL.su3** - `http://foo.i2p/foo.su3` - L'emplacement du fichier de mise à jour au format su3, depuis la version 0.9.15. Depuis la version 1.7.0 (0.9.53), il est possible d'utiliser les variables `$OS` et `$ARCH` dans l'URL.
-   **description** - en anglais
-   **description_xx** - pour la langue xx
-   **license** - La licence du plugin
-   **disableStop=true** - Faux par défaut. Si vrai, le bouton d'arrêt ne sera pas affiché. Utilisez ceci s'il n'y a pas de webapps et pas de clients avec des arguments d'arrêt.

#### Propriétés des liens de la barre de résumé de la console

Les propriétés suivantes sont utilisées pour ajouter un lien dans la barre de résumé de la console :

-   **consoleLinkName** - sera ajouté à la barre de résumé
-   **consoleLinkName_xx** - pour la langue xx
-   **consoleLinkURL** - /appname/index.jsp
-   **consoleLinkTooltip** - pris en charge depuis la version 0.7.12-6
-   **consoleLinkTooltip_xx** - langue xx depuis la version 0.7.12-6

#### Propriétés de l'icône de la console

Les propriétés optionnelles suivantes peuvent être utilisées pour ajouter une icône personnalisée sur la console :

-   **console-icon** - pris en charge depuis la version 0.9.20. Uniquement pour les webapps. Un chemin vers une image 32x32, par exemple /icon.png. Depuis la version 1.7.0 (API 0.9.53), si consoleLinkURL est spécifié, le chemin est relatif à cette URL. Sinon, il est relatif au nom de la webapp. S'applique à toutes les webapps du plugin.
-   **icon-code** - pris en charge depuis la version 0.9.25. Fournit une icône de console pour les plugins sans ressources web. Une chaîne B64 produite en appelant `net.i2p.data.Base64 encode FILE` sur un fichier image png 32x32.

#### Propriétés de l'installateur

Les propriétés suivantes sont utilisées par l'installateur de plugin :

-   **type** - app/theme/locale/webapp/... (non implémenté, probablement pas nécessaire)
-   **min-i2p-version** - La version minimale d'I2P requise par ce plugin
-   **max-i2p-version** - La version maximale d'I2P sur laquelle ce plugin fonctionnera
-   **min-java-version** - La version minimale de Java requise par ce plugin
-   **min-jetty-version** - pris en charge depuis 0.8.13, utilisez 6 pour les webapps Jetty 6
-   **max-jetty-version** - pris en charge depuis 0.8.13, utilisez 5.99999 pour les webapps Jetty 5
-   **required-platform-OS** - non implémenté - sera peut-être seulement affiché, pas vérifié
-   **other-requirements** - non implémenté, par ex. python x.y - pas vérifié par l'installateur, juste affiché à l'utilisateur
-   **dont-start-at-install=true** - Par défaut false. Ne démarrera pas le plugin lors de son installation ou mise à jour.
-   **router-restart-required=true** - Par défaut false. Ceci ne redémarre pas le router ou le plugin lors d'une mise à jour, cela informe juste l'utilisateur qu'un redémarrage est requis.
-   **update-only=true** - Par défaut false. Si true, échouera si une installation n'existe pas.
-   **install-only=true** - Par défaut false. Si true, échouera si une installation existe.
-   **min-installed-version** - pour mettre à jour par-dessus, si une installation existe
-   **max-installed-version** - pour mettre à jour par-dessus, si une installation existe
-   **depends=plugin1,plugin2,plugin3** - non implémenté
-   **depends-version=0.3.4,,5.6.7** - non implémenté

#### Propriétés de traduction

-   **langs=xx,yy,Klingon,...** - (non implémenté) (yy est le drapeau du pays)

### Répertoires et fichiers d'application

Chacun des répertoires ou fichiers suivants est optionnel, mais quelque chose doit être présent sinon cela ne fera rien :

**console/**

-   **locale/** - Seulement les jars contenant de nouveaux bundles de ressources (traductions) pour les applications de l'installation I2P de base. Les bundles pour ce plugin doivent être placés dans console/webapp/foo.war ou lib/foo.jar
-   **themes/** - Nouveaux thèmes pour la console du router. Placez chaque thème dans un sous-répertoire.
-   **webapps/** - (Voir les notes importantes ci-dessous concernant les webapps) .wars - Celles-ci seront exécutées au moment de l'installation sauf si désactivées dans webapps.config. Le nom du war n'a pas besoin d'être identique au nom du plugin. Ne dupliquez pas les noms de war dans l'installation I2P de base.
-   **webapps.config** - Même format que le webapps.config du router. Également utilisé pour spécifier des jars supplémentaires dans $PLUGIN/lib/ ou $I2P/lib pour le classpath de la webapp, avec `webapps.warname.classpath=$PLUGIN/lib/foo.jar,$I2P/lib/bar.jar`

> **Note :** Avant la version 1.7.0 (API 0.9.53), la ligne classpath n'était chargée que si le warname était identique au nom du plugin. À partir de l'API 0.9.53, le paramètre classpath fonctionnera pour n'importe quel warname.

> **Note :** Avant la version router 0.7.12-9, le router cherchait `plugin.warname.startOnLoad` au lieu de `webapps.warname.startOnLoad`. Pour la compatibilité avec les versions router plus anciennes, un plugin souhaitant désactiver un war devrait inclure les deux lignes.

**eepsite/**

(Voir les notes importantes ci-dessous concernant les eepsites)

-   **cgi-bin/**
-   **docroot/**
-   **logs/**
-   **webapps/**
-   **jetty.xml** - L'installateur devra effectuer une substitution de variables ici pour définir le chemin. L'emplacement et le nom de ce fichier n'ont pas vraiment d'importance, tant qu'il est défini dans clients.config - il pourrait être plus pratique de le placer un niveau au-dessus d'ici.

**lib/**

Placez tous les fichiers JAR ici, et spécifiez-les dans une ligne de classpath dans console/webapps.config et/ou clients.config

### fichier clients.config

Ce fichier est optionnel et spécifie les clients qui seront exécutés lorsqu'un plugin est démarré. Il utilise le même format que le fichier clients.config du router. Voir la spécification du fichier de configuration clients.config pour plus d'informations sur le format et les détails importants concernant la façon dont les clients sont démarrés et arrêtés.

-   **clientApp.0.stopargs=foo bar stop baz** - Si présent, la classe sera appelée avec ces arguments pour arrêter le client. Toutes les tâches d'arrêt sont appelées sans délai. Note : Le router ne peut pas déterminer si vos clients non gérés sont en cours d'exécution ou non.
-   **clientApp.0.uninstallargs=foo bar uninstall baz** - Si présent, la classe sera appelée avec ces arguments juste avant de supprimer $PLUGIN. Toutes les tâches de désinstallation sont appelées sans délai.
-   **clientApp.0.classpath=$I2P/lib/foo.bar,$PLUGIN/lib/bar.jar** - Le lanceur de plugin effectuera une substitution de variables dans les lignes args et stopargs comme suit :
    -   `$I2P` - Répertoire d'installation de base d'I2P
    -   `$CONFIG` - Répertoire de configuration d'I2P (généralement ~/.i2p)
    -   `$PLUGIN` - Répertoire d'installation de ce plugin (généralement ~/.i2p/plugins/appname)
    -   `$OS` - Le système d'exploitation hôte sous la forme `windows`, `linux`, `mac`
    -   `$ARCH` - L'architecture hôte sous la forme `386`, `amd64`, `arm64`

(Voir les notes importantes ci-dessous concernant l'exécution de scripts shell ou de programmes externes)

## Tâches de l'installateur de plugins

Ceci répertorie ce qui se passe lorsqu'un plugin est installé par I2P.

1.  Le fichier .xpi2p est téléchargé.
2.  La signature .sud est vérifiée contre les clés stockées. Depuis la version 0.9.14.1, s'il n'y a pas de clé correspondante, l'installation échoue, sauf si une propriété avancée du router est définie pour autoriser toutes les clés.
3.  Vérifier l'intégrité du fichier zip.
4.  Extraire le fichier plugin.config.
5.  Vérifier la version d'I2P, pour s'assurer que le plugin fonctionnera.
6.  Vérifier que les webapps ne dupliquent pas les applications $I2P existantes.
7.  Arrêter le plugin existant (s'il est présent).
8.  Vérifier que le répertoire d'installation n'existe pas encore si update=false, ou demander d'écraser.
9.  Vérifier que le répertoire d'installation existe si update=true, ou demander de créer.
10. Décompresser le plugin dans appDir/plugins/name/
11. Ajouter le plugin à plugins.config

## Tâches de démarrage du plugin

Ceci énumère ce qui se passe lorsque les plugins sont démarrés. D'abord, plugins.config est vérifié pour voir quels plugins doivent être démarrés. Pour chaque plugin :

1.  Vérifier clients.config, et charger et démarrer chaque élément (ajouter les jars configurés au classpath).
2.  Vérifier console/webapp et console/webapp.config. Charger et démarrer les éléments requis (ajouter les jars configurés au classpath).
3.  Ajouter console/locale/foo.jar au classpath de traduction si présent.
4.  Ajouter console/theme au chemin de recherche des thèmes si présent.
5.  Ajouter le lien de la barre de résumé.

## Notes sur l'application web Console

Les applications web de console avec des tâches en arrière-plan doivent implémenter un ServletContextListener (voir seedless ou i2pbote pour des exemples), ou redéfinir destroy() dans le servlet, afin qu'elles puissent être arrêtées. À partir de la version 0.7.12-3 du router, les applications web de console seront toujours arrêtées avant d'être redémarrées, vous n'avez donc pas à vous soucier de multiples instances, tant que vous faites cela. Également à partir de la version 0.7.12-3 du router, les applications web de console seront arrêtées lors de l'arrêt du router.

N'incluez pas les jars de bibliothèques dans la webapp ; placez-les dans lib/ et mettez un classpath dans webapps.config. Vous pourrez alors créer des plugins d'installation et de mise à jour séparés, où le plugin de mise à jour ne contient pas les jars de bibliothèques.

Ne jamais inclure Jetty, Tomcat ou les fichiers JAR de servlet dans votre plugin, car ils peuvent entrer en conflit avec la version présente dans l'installation I2P. Veillez à ne pas inclure de bibliothèques en conflit.

N'incluez pas les fichiers .java ou .jsp ; sinon Jetty les recompilera lors de l'installation, ce qui augmentera le temps de démarrage. Bien que la plupart des installations I2P aient un compilateur Java et JSP fonctionnel dans le classpath, cela n'est pas garanti et peut ne pas fonctionner dans tous les cas.

Pour l'instant, une webapp devant ajouter des fichiers classpath dans $PLUGIN doit avoir le même nom que le plugin. Par exemple, une webapp dans le plugin foo doit être nommée foo.war.

Bien qu'I2P prenne en charge Servlet 3.0 depuis la version 0.9.30 d'I2P, il ne prend PAS en charge l'analyse d'annotations pour @WebContent (pas de fichier web.xml). Plusieurs jars d'exécution supplémentaires seraient nécessaires, et nous ne les fournissons pas dans une installation standard. Contactez les développeurs I2P si vous avez besoin du support pour @WebContent.

## Notes sur les eepsites

Il n'est pas clair comment faire installer un plugin sur un eepsite existant. Le router n'a pas de lien vers l'eepsite, et celui-ci peut ou ne peut pas être en cours d'exécution, et il peut y en avoir plus d'un. Il vaut mieux démarrer votre propre instance Jetty et instance I2PTunnel, pour un tout nouvel eepsite.

Il peut instancier un nouvel I2PTunnel (un peu comme le fait la CLI i2ptunnel), mais il n'apparaîtra pas dans l'interface graphique i2ptunnel bien sûr, c'est une instance différente. Mais c'est acceptable. Ensuite vous pouvez démarrer et arrêter i2ptunnel et jetty ensemble.

Donc ne comptez pas sur le routeur pour fusionner automatiquement ceci avec un eepsite existant. Cela n'arrivera probablement pas. Démarrez un nouveau I2PTunnel et Jetty depuis clients.config. Les meilleurs exemples de ceci sont les plugins zzzot et pebble.

Comment obtenir la substitution de chemin dans jetty.xml ? Voir les plugins zzzot et pebble pour des exemples.

## Notes sur le Démarrage/Arrêt du Client

À partir de la version 0.9.4, le router prend en charge les clients de plugin "gérés". Les clients de plugin gérés sont instanciés et démarrés par le `ClientAppManager`. Le ClientAppManager maintient une référence vers le client et reçoit des mises à jour sur l'état du client. Les clients de plugin gérés sont préférés, car il est beaucoup plus facile d'implémenter le suivi d'état et de démarrer et arrêter un client. Il est également beaucoup plus facile d'éviter les références statiques dans le code du client qui pourraient conduire à une utilisation excessive de la mémoire après l'arrêt d'un client. Consultez la spécification du fichier de configuration clients.config pour plus d'informations sur l'écriture d'un client géré.

Pour les clients de plugin "non gérés", le router n'a aucun moyen de surveiller l'état des clients démarrés via clients.config. L'auteur du plugin devrait gérer les appels multiples de démarrage ou d'arrêt avec élégance, si possible, en maintenant une table d'état statique, ou en utilisant des fichiers PID, etc. Évitez la journalisation ou les exceptions lors de démarrages ou d'arrêts multiples. Ceci s'applique également à un appel d'arrêt sans démarrage préalable. À partir de la version 0.7.12-3 du router, les plugins seront arrêtés lors de l'arrêt du router, ce qui signifie que tous les clients avec des stopargs dans clients.config seront appelés, qu'ils aient été préalablement démarrés ou non.

## Notes sur les scripts shell et les programmes externes

Pour exécuter des scripts shell ou d'autres programmes externes, écrivez une petite classe Java qui vérifie le type de système d'exploitation, puis exécute ShellCommand soit sur le fichier .bat ou .sh que vous fournissez. Une solution généralisée pour cela a été ajoutée dans I2P 1.7.0/0.9.53, le "ShellService" qui effectue le suivi d'état pour une seule commande et communique avec le ClientAppManager.

Les programmes externes ne seront pas arrêtés lorsque le router s'arrête, et une seconde copie se lancera lorsque le router redémarre. Ceci peut généralement être résolu en utilisant un ShellService pour effectuer le suivi d'état. Si cela ne convient pas à votre cas d'usage, vous pourriez écrire une classe wrapper ou un script shell qui effectue le stockage habituel du PID dans un fichier PID, et le vérifier au démarrage.

## Autres directives pour les plugins

-   Consultez la branche monotone i2p.scripts ou l'un des plugins d'exemple sur la page de zzz pour le script shell makeplugin.sh. Celui-ci automatise la plupart des tâches de génération de clés, création de fichiers su3 de plugin et vérification. Vous devriez intégrer ce script dans votre processus de construction de plugin.
-   Pack200 des jars et wars est fortement recommandé pour les plugins, cela réduit généralement les plugins de 60-65%. Consultez l'un des plugins d'exemple sur la page de zzz pour un exemple. Le décompressage Pack200 est pris en charge sur les routeurs 0.7.11-5 ou supérieur, ce qui correspond essentiellement à tous les routeurs qui supportent les plugins.
-   Les plugins ne doivent pas tenter d'écrire quelque part dans $I2P car cela pourrait être en lecture seule, et ce n'est de toute façon pas une bonne politique.
-   Les plugins peuvent écrire dans $CONFIG mais il est recommandé de conserver les fichiers uniquement dans $PLUGIN. Tous les fichiers dans $PLUGIN seront supprimés lors de la désinstallation.
-   $CWD peut être n'importe où ; ne supposez pas qu'il soit dans un endroit particulier, n'essayez pas de lire ou d'écrire des fichiers relatifs à $CWD. Pour un ShellService, c'est toujours identique à $PLUGIN.
-   Les programmes Java devraient découvrir où ils se trouvent avec les getters de répertoire dans I2PAppContext.
-   Le répertoire du plugin est `I2PAppContext.getGlobalContext().getAppDir().getAbsolutePath() + "/plugins/" + appname`, ou mettez un argument $PLUGIN dans la ligne args dans clients.config.
-   Tous les fichiers de configuration doivent être en UTF-8.
-   Pour s'exécuter dans une JVM séparée, utilisez ShellCommand avec `java -cp foo:bar:baz my.main.class arg1 arg2 arg3`.
-   Comme alternative à stopargs dans clients.config, un client Java peut enregistrer un hook d'arrêt avec `I2PAppContext.addShutdownTask()`. Mais cela n'arrêterait pas un plugin lors d'une mise à niveau, donc stopargs est recommandé. De plus, configurez tous les threads créés en mode daemon.
-   N'incluez pas de classes dupliquant celles de l'installation standard. Étendez les classes si nécessaire.
-   Méfiez-vous des différentes définitions de classpath dans wrapper.config entre les anciennes et nouvelles installations.
-   Les clients rejetteront les clés dupliquées avec différents noms de clé, et les noms de clé dupliqués avec différentes clés, et différentes clés ou noms de clé dans les packages de mise à niveau. Protégez vos clés. Ne les générez qu'une seule fois.
-   Ne modifiez pas le fichier plugin.config à l'exécution car il sera écrasé lors de la mise à niveau. Utilisez un fichier de configuration différent dans le répertoire pour stocker la configuration d'exécution.
-   En général, les plugins ne devraient pas nécessiter l'accès à $I2P/lib/router.jar. N'accédez pas aux classes du routeur, sauf si vous faites quelque chose de spécial.
-   Comme chaque version doit être supérieure à la précédente, vous pourriez améliorer votre script de construction pour ajouter un numéro de build à la fin de la version.
-   Les plugins ne doivent jamais appeler `System.exit()`.
-   Veuillez respecter les licences en satisfaisant les exigences de licence pour tout logiciel que vous intégrez.
-   Le routeur définit le fuseau horaire de la JVM sur UTC. Si un plugin a besoin de connaître le fuseau horaire réel de l'utilisateur, il est stocké par le routeur dans la propriété I2PAppContext `i2p.systemTimeZone`.

## Classpaths

Les fichiers jar suivants dans $I2P/lib peuvent être considérés comme faisant partie du classpath standard pour toutes les installations I2P, peu importe l'ancienneté ou la nouveauté de l'installation d'origine.

Toutes les API publiques récentes dans les jars i2p ont le numéro de version depuis-la-release spécifié dans les Javadocs. Si votre plugin nécessite certaines fonctionnalités uniquement disponibles dans les versions récentes, assurez-vous de définir les propriétés min-i2p-version, min-jetty-version, ou les deux, dans le fichier plugin.config.

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Jar</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contains</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">addressbook.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Subscription and blockfile support</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need; use the NamingService interface</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">commons-logging.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Apache Logging</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Empty since release 0.9.30</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">commons-el.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">JSP Expressions Language</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For plugins with JSPs that use EL. As of release 0.9.30 (Jetty 9), this contains the EL 3.0 API.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2p.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Core API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">All plugins will need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">i2ptunnel.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2PTunnel</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For plugins with HTTP or other servers</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">jasper-compiler.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">nothing</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Empty since Jetty 6 (release 0.9)</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">jasper-runtime.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Jasper Compiler and Runtime, and some Tomcat utils</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Needed for plugins with JSPs</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">javax.servlet.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Servlet API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Needed for plugins with JSPs. As of release 0.9.30 (Jetty 9), this contains the Servlet 3.1 and JSP 2.3 APIs.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">jbigi.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Binaries</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">jetty-i2p.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Support utilities</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Some plugins will need. As of release 0.9.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">mstreaming.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Streaming API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Most plugins will need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">org.mortbay.jetty.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Jetty Base</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Only plugins starting their own Jetty instance will need. Recommended way of starting Jetty is with <code>net.i2p.jetty.JettyStart</code> in jetty-i2p.jar.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">router.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Router</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Only plugins using router context will need; most will not</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">routerconsole.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Console libraries</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need, not a public API</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">sam.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SAM API</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">streaming.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Streaming Implementation</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Most plugins will need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">systray.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">URL Launcher</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Most plugins should not need</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">systray4j.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Systray</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need. As of 0.9.26, no longer present.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">wrapper.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Router</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">No plugin should need</td>
    </tr>
  </tbody>
</table>
Les fichiers jar suivants dans $I2P/lib peuvent être considérés comme présents dans toutes les installations I2P, peu importe leur ancienneté ou leur nouveauté, mais ne sont pas nécessairement dans le classpath :

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Jar</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Contains</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">Usage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">jstl.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Standard Taglib</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For plugins using JSP tags</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">standard.jar</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Standard Taglib</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For plugins using JSP tags</td>
    </tr>
  </tbody>
</table>
Tout ce qui n'est pas listé ci-dessus peut ne pas être présent dans le classpath de tout le monde, même si vous l'avez dans le classpath de VOTRE version d'i2p. Si vous avez besoin d'un jar non listé ci-dessus, ajoutez $I2P/lib/foo.jar au classpath spécifié dans clients.config ou webapps.config dans votre plugin.

Auparavant, une entrée classpath spécifiée dans clients.config était ajoutée au classpath pour l'ensemble de la JVM. Cependant, à partir de la version 0.7.13-3, cela a été corrigé en utilisant des chargeurs de classes, et maintenant, comme prévu à l'origine, le classpath spécifié dans clients.config ne concerne que le thread particulier. Par conséquent, spécifiez le classpath complet requis pour chaque client.

## Notes sur la version Java

I2P nécessite Java 7 depuis la version 0.9.24 (janvier 2016). I2P nécessitait Java 6 depuis la version 0.9.12 (avril 2014). Tous les utilisateurs d'I2P sur la dernière version devraient utiliser une JVM 1.7 (7.0).

Si votre plugin **ne nécessite pas la version 1.7** :

-   S'assurer que tous les fichiers java et jsp sont compilés avec source="1.6" target="1.6".
-   S'assurer que tous les fichiers jar des bibliothèques intégrées sont également pour 1.6 ou inférieur.

Si votre plugin **nécessite la version 1.7** :

-   Notez cela sur votre page de téléchargement.
-   Ajoutez min-java-version=1.7 à votre plugin.config

Dans tous les cas, vous **devez** définir un bootclasspath lors de la compilation avec Java 8 pour éviter les plantages à l'exécution.

## Plantage de la JVM lors de la mise à jour

Note - tout ceci devrait maintenant être corrigé.

La JVM a tendance à planter lors de la mise à jour des jars dans un plugin si ce plugin fonctionnait depuis le démarrage d'I2P (même si le plugin a été arrêté par la suite). Ceci a peut-être été corrigé avec l'implémentation du chargeur de classes dans la version 0.7.13-3, mais ce n'est pas certain.

Le plus sûr est de concevoir votre plugin avec le jar à l'intérieur du war (pour une webapp), ou d'exiger un redémarrage après la mise à jour, ou de ne pas mettre à jour les jars dans votre plugin.

En raison du fonctionnement des chargeurs de classes à l'intérieur d'une webapp, il _peut_ être sûr d'avoir des jars externes si vous spécifiez le classpath dans webapps.config. Des tests supplémentaires sont nécessaires pour vérifier cela. Ne spécifiez pas le classpath avec un client 'factice' dans clients.config s'il n'est nécessaire que pour une webapp - utilisez webapps.config à la place.

Le moins sûr, et apparemment la source de la plupart des plantages, sont les clients avec des fichiers jar de plugin spécifiés dans le classpath dans clients.config.

Rien de cela ne devrait poser de problème lors de l'installation initiale - vous ne devriez jamais avoir besoin d'un redémarrage pour l'installation initiale d'un plugin.

## Références

-   [Spécification du fichier de configuration](/docs/specs/configuration)
-   [Cryptographie DSA](/docs/specs/cryptography#DSA)
-   [Spécification des mises à jour](/docs/specs/updates)
