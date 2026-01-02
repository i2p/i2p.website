---
title: "Tutoriel de base sur les tunnels I2P avec des images"
date: 2019-06-02
author: "idk"
description: "Configuration de base d’i2ptunnel"
categories: ["tutorial"]
---

Bien que le router I2P Java soit livré préconfiguré avec un serveur web statique, jetty, pour fournir le premier eepSite de l’utilisateur, beaucoup ont besoin de fonctionnalités plus sophistiquées de leur serveur web et préfèrent créer un eepSite avec un autre serveur. C’est bien sûr possible, et en réalité c’est très simple une fois que vous l’avez fait une première fois.

Bien que ce soit facile à faire, il y a quelques éléments à prendre en compte avant de le faire. Vous voudrez supprimer les caractéristiques identifiantes de votre serveur Web, comme des en-têtes potentiellement identifiants et des pages d'erreur par défaut qui indiquent le type de serveur/distribution. Pour plus d'informations sur les menaces pour l'anonymat posées par des applications mal configurées, voir : [Riseup ici](https://riseup.net/en/security/network-security/tor/onionservices-best-practices), [Whonix ici](https://www.whonix.org/wiki/Onion_Services), [cet article de blog pour quelques erreurs d'opsec (sécurité des opérations)](https://blog.0day.rocks/securing-a-web-hidden-service-89d935ba1c1d), [et la page des applications I2P ici](https://geti2p.net/docs/applications/supported). Bien qu'une grande partie de ces informations concerne les services onion de Tor, les mêmes procédures et principes s'appliquent à l'hébergement d'applications sur I2P.

### Étape 1 : Ouvrez l'assistant Tunnel

Accédez à l'interface web d'I2P à l'adresse 127.0.0.1:7657 et ouvrez le [Hidden Services Manager](http://127.0.0.1:7657/i2ptunnelmgr) (lien vers localhost). Cliquez sur le bouton "Tunnel Wizard" pour commencer.

### Étape deux : Sélectionnez un Server Tunnel

L'assistant de tunnel est très simple. Puisque nous configurons un *serveur* http, il suffit de sélectionner un tunnel *serveur*.

### Étape trois : Sélectionner un HTTP Tunnel

Un tunnel HTTP est le type de tunnel optimisé pour l’hébergement de services HTTP. Il dispose de fonctionnalités de filtrage et de limitation de débit activées, spécialement adaptées à cet usage. Un tunnel standard peut également fonctionner, mais si vous choisissez un tunnel standard, vous devrez gérer vous-même ces fonctionnalités de sécurité. Une analyse plus approfondie de la configuration HTTP Tunnel est disponible dans le tutoriel suivant.

### Étape quatre : Donnez-lui un nom et une description

Pour votre bénéfice et afin de pouvoir vous souvenir et distinguer l’usage que vous faites du tunnel, donnez-lui un bon surnom et une description. Si vous devez revenir ultérieurement pour effectuer d’autres opérations de gestion, c’est ainsi que vous identifierez le tunnel dans le gestionnaire de services cachés.

### Étape cinq : Configurer l’hôte et le port

À cette étape, vous indiquez au serveur web le port TCP sur lequel votre serveur web écoute. Comme la plupart des serveurs web écoutent sur le port 80 ou le port 8080, l’exemple l’illustre. Si vous utilisez des ports alternatifs ou des machines virtuelles ou des conteneurs pour isoler vos services web, vous devrez peut-être ajuster l’hôte, le port, ou les deux.

### Étape six: Décidez s'il faut le démarrer automatiquement

Je ne vois pas comment développer davantage cette étape.

### Étape sept : Passez en revue vos paramètres

Enfin, examinez les paramètres que vous avez sélectionnés. Si vous les validez, enregistrez-les. Si vous n'avez pas choisi de démarrer le tunnel automatiquement, allez dans le gestionnaire de services cachés et démarrez-le manuellement lorsque vous souhaitez rendre votre service disponible.

### Annexe: Options de personnalisation du serveur HTTP

I2P fournit un panneau détaillé pour configurer le tunnel du serveur HTTP de diverses façons personnalisées. Je terminerai ce tutoriel en les passant toutes en revue. Un jour.
