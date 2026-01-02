---
title: "Installation de Plugins Personnalisés"
description: "Installation, mise à jour et développement de plugins pour le routeur"
slug: "plugins"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

Le framework de plugins d'I2P vous permet d'étendre le router sans toucher à l'installation principale. Les plugins disponibles couvrent la messagerie, les blogs, l'IRC, le stockage, les wikis, les outils de surveillance et bien plus encore.

> **Note de sécurité :** Les plugins s'exécutent avec les mêmes permissions que le router. Traitez les téléchargements tiers de la même manière que vous traiteriez toute mise à jour logicielle signée—vérifiez la source avant l'installation.

## 1. Installer un Plugin

1. Copiez l'URL de téléchargement du plugin depuis la page du projet.  
   ![Copy plugin URL](/images/plugins/plugin-step-0.png)
2. Ouvrez la [page de configuration des plugins](http://127.0.0.1:7657/configplugins) de la console du routeur.  
   ![Open plugin configuration](/images/plugins/plugin-step-1.png)
3. Collez l'URL dans le champ d'installation et cliquez sur **Installer le plugin**.  
   ![Install plugin](/images/plugins/plugin-step-2.png)

Le routeur récupère l'archive signée, vérifie la signature et active le plugin immédiatement. La plupart des plugins ajoutent des liens dans la console ou des services en arrière-plan sans nécessiter de redémarrage du routeur.

## 2. Pourquoi les plugins sont importants

- Distribution en un clic pour les utilisateurs finaux—aucune modification manuelle de `wrapper.config` ou `clients.config`
- Conserve la taille du bundle `i2pupdate.su3` principal réduite tout en livrant des fonctionnalités volumineuses ou spécialisées à la demande
- Les JVM optionnelles par plugin fournissent une isolation des processus lorsque nécessaire
- Vérifications automatiques de compatibilité avec la version du router, l'environnement d'exécution Java et Jetty
- Le mécanisme de mise à jour reflète celui du router : paquets signés et téléchargements incrémentiels
- Les intégrations à la console, packs de langues, thèmes d'interface et applications non-Java (via scripts) sont tous pris en charge
- Permet des répertoires type « app store » organisés tels que `plugins.i2p`

## 3. Gérer les plugins installés

Utilisez les contrôles sur [I2P Router Plugin's](http://127.0.0.1:7657/configclients.jsp#plugin) pour :

- Vérifier les mises à jour d'un seul plugin
- Vérifier tous les plugins en une fois (déclenché automatiquement après les mises à niveau du routeur)
- Installer toutes les mises à jour disponibles en un clic  
  ![Update plugins](/images/plugins/plugin-update-0.png)
- Activer/désactiver le démarrage automatique pour les plugins qui enregistrent des services
- Désinstaller les plugins proprement

## 4. Créez votre propre plugin

1. Consultez la [spécification des plugins](/docs/specs/plugin/) pour les exigences de packaging, de signature et de métadonnées.
2. Utilisez [`makeplugin.sh`](https://github.com/i2p/i2p.scripts/tree/master/plugin/makeplugin.sh) pour encapsuler un binaire ou une webapp existante dans une archive installable.
3. Publiez à la fois les URL d'installation et de mise à jour afin que le router puisse distinguer les installations initiales des mises à niveau incrémentielles.
4. Fournissez les sommes de contrôle et les clés de signature de manière visible sur la page de votre projet pour aider les utilisateurs à vérifier l'authenticité.

Vous cherchez des exemples ? Parcourez le code source des plugins communautaires sur `plugins.i2p` (par exemple, l'échantillon `snowman`).

## 5. Limitations connues

- La mise à jour d'un plugin qui fournit des fichiers JAR simples peut nécessiter un redémarrage du routeur car le chargeur de classes Java met en cache les classes.
- La console peut afficher un bouton **Stop** même si le plugin n'a aucun processus actif.
- Les plugins lancés dans une JVM séparée créent un répertoire `logs/` dans le répertoire de travail actuel.
- La première fois qu'une clé de signataire apparaît, elle est automatiquement approuvée ; il n'existe aucune autorité de signature centrale.
- Windows laisse parfois des répertoires vides après la désinstallation d'un plugin.
- L'installation d'un plugin exclusif à Java 6 sur une JVM Java 5 signale « plugin is corrupt » en raison de la compression Pack200.
- Les plugins de thème et de traduction restent largement non testés.
- Les indicateurs de démarrage automatique ne persistent pas toujours pour les plugins non gérés.

## 6. Exigences et bonnes pratiques

- La prise en charge des plugins est disponible dans I2P **0.7.12 et versions ultérieures**.
- Maintenez votre routeur et vos plugins à jour pour recevoir les correctifs de sécurité.
- Fournissez des notes de version concises afin que les utilisateurs comprennent les changements entre les versions.
- Dans la mesure du possible, hébergez les archives de plugins via HTTPS à l'intérieur d'I2P pour minimiser l'exposition des métadonnées sur le clearnet.

## 7. Pour aller plus loin

- [Spécification des plugins](/docs/specs/plugin/)
- [Framework d'application cliente](/docs/applications/managed-clients/)
- [Dépôt de scripts I2P](https://github.com/i2p/i2p.scripts/) pour les utilitaires d'empaquetage
