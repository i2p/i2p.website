---
title: "Améliorez vos compétences I2P grâce aux LeaseSets chiffrés"
date: 2021-09-07
slug: "level-up-your-i2p-skills-with-encrypted-leasesets"
author: "idk"
description: "On a dit qu’I2P met l’accent sur les services cachés ; nous en examinons une interprétation."
categories: ["general"]
API_Translate: vrai
---

## Améliorez vos compétences en I2P avec des LeaseSets chiffrés

Par le passé, on a dit qu’I2P mettait l’accent sur la prise en charge des services cachés, ce qui est vrai à bien des égards. Cependant, ce que cela implique pour les utilisateurs, les développeurs et les administrateurs de services cachés n’est pas toujours identique. Les LeaseSets chiffrés et leurs cas d’utilisation offrent une fenêtre unique et pratique sur la manière dont I2P rend les services cachés plus polyvalents, plus faciles à administrer, et sur la façon dont I2P étend le concept de service caché pour apporter des avantages en matière de sécurité à des cas d’utilisation potentiellement intéressants.

## Qu'est-ce qu'un LeaseSet ?

Lorsque vous créez un service caché, vous publiez dans l'I2P NetDB un objet appelé "LeaseSet". Le "LeaseSet" est, en termes simples, ce dont les autres utilisateurs d'I2P ont besoin pour découvrir "où" se trouve votre service caché sur le réseau I2P. Il contient des "Leases" qui identifient des tunnels pouvant être utilisés pour atteindre votre service caché, ainsi que la clé publique de votre destination, à laquelle les clients chiffreront les messages. Ce type de service caché est accessible à toute personne disposant de l'adresse, ce qui est probablement le cas d'usage le plus courant pour l'instant.

Parfois, vous ne souhaitez toutefois pas que vos services cachés soient accessibles à n'importe qui. Certaines personnes utilisent des services cachés pour accéder à un serveur SSH sur un PC domestique, ou pour interconnecter un réseau d’appareils IoT. Dans ces cas, il n’est pas nécessaire, et peut même être contre-productif, de rendre votre service caché accessible à tout le monde sur le réseau I2P. C’est là que "Encrypted LeaseSets" entrent en jeu.

## LeaseSets chiffrés: Services TRÈS cachés

Les LeaseSets chiffrés sont des LeaseSets publiés dans la NetDB sous une forme chiffrée, où ni les Leases ni les clés publiques ne sont visibles, sauf si le client possède les clés nécessaires pour déchiffrer le LeaseSet qui s’y trouve. Seuls les clients avec lesquels vous partagez des clés (pour les PSK Encrypted LeaseSets), ou qui partagent leurs clés avec vous (pour les DH Encrypted LeaseSets), pourront voir la destination et personne d’autre.

I2P prend en charge plusieurs stratégies pour les LeaseSets chiffrés. Il est important de comprendre les caractéristiques clés de chaque stratégie pour décider laquelle utiliser. Si un LeaseSet chiffré utilise une stratégie de "clé pré-partagée (PSK)", alors le serveur générera une clé (ou des clés) que l'opérateur du serveur partagera ensuite avec chaque client. Bien sûr, cet échange doit avoir lieu hors bande, éventuellement via un échange sur IRC par exemple. Cette version des LeaseSets chiffrés ressemble un peu à une connexion au Wi-Fi avec un mot de passe. Sauf que ce à quoi vous vous connectez, c'est un service caché.

Si un Encrypted LeaseSet (LeaseSet chiffré) utilise une stratégie "Diffie-Hellman(DH)", alors les clés sont générées côté client. Lorsqu’un client Diffie-Hellman se connecte à une destination avec un Encrypted LeaseSet, il doit d’abord partager ses clés avec l’opérateur du serveur. L’opérateur du serveur décide ensuite s’il autorise le client DH. Cette version d’Encrypted LeaseSets ressemble un peu à SSH avec un fichier `authorized_keys`. Sauf que, ici, ce à quoi vous vous connectez est un service caché.

En chiffrant votre LeaseSet, non seulement vous rendez impossible aux utilisateurs non autorisés de se connecter à votre destination, mais vous empêchez même les visiteurs non autorisés de découvrir la véritable destination du service caché I2P. Certains lecteurs ont probablement déjà envisagé un cas d’utilisation pour leur propre LeaseSet chiffré.

## Utiliser des LeaseSets chiffrés pour accéder en toute sécurité à la console du router

En règle générale, plus un service a accès à des informations complexes sur votre appareil, plus il est dangereux d’exposer ce service à Internet ou même à un réseau de services cachés comme I2P. Si vous souhaitez exposer un tel service, vous devez le protéger avec, par exemple, un mot de passe ou, dans le cas d’I2P, une option bien plus approfondie et sécurisée pourrait être un LeaseSet chiffré.

**Avant de continuer, veuillez lire et comprendre que si vous effectuez la procédure suivante sans un LeaseSet chiffré, vous compromettrez la sécurité de votre router I2P. Ne configurez pas l'accès à la console de votre router via I2P sans un LeaseSet chiffré. De plus, ne partagez pas les PSK de votre LeaseSet chiffré avec des appareils que vous ne contrôlez pas.**

Un tel service qu’il est utile de partager via I2P, mais UNIQUEMENT avec un Encrypted LeaseSet (LeaseSet chiffré), est la console du router I2P elle-même. Exposer la console du router I2P d’une machine sur I2P avec un Encrypted LeaseSet permet à une autre machine munie d’un navigateur d’administrer l’instance I2P distante. Je trouve cela utile pour surveiller à distance mes services I2P habituels. On peut aussi l’utiliser pour superviser un serveur utilisé pour maintenir un torrent en seed à long terme, afin d’accéder à I2PSnark.

Même si l'explication peut prendre du temps, la configuration d'un LeaseSet chiffré est simple via le Hidden Services Manager UI.

## Sur le "Serveur"

Commencez par ouvrir le Gestionnaire des services cachés à http://127.0.0.1:7657/i2ptunnelmgr et faites défiler jusqu'en bas de la section intitulée "I2P Hidden Services". Créez un nouveau service caché avec l'hôte "127.0.0.1" et le port "7657" avec ces "Tunnel Cryptography Options" et enregistrez le service caché.

Ensuite, sélectionnez votre nouveau tunnel depuis la page principale du Gestionnaire des services cachés (Hidden Services Manager). Les options de cryptographie du tunnel doivent désormais inclure votre première clé pré-partagée. Notez-la pour l’étape suivante, ainsi que l’adresse Base32 chiffrée de votre tunnel.

## Sur le "Client"

Passez maintenant à l’ordinateur client qui se connectera au service caché, et ouvrez Keyring Configuration à l’adresse http://127.0.0.1:7657/configkeyring pour ajouter les clés préparées précédemment. Commencez par coller l’adresse Base32 depuis le serveur dans le champ intitulé : "Full destination, name, Base32, or hash." Ensuite, collez la clé pré‑partagée du serveur dans le champ "Encryption Key". Cliquez sur Enregistrer, et vous êtes prêt à accéder en toute sécurité au service caché en utilisant un LeaseSet chiffré.

## Vous êtes maintenant prêt à administrer I2P à distance

Comme vous pouvez le voir, I2P offre des capacités uniques aux administrateurs de services cachés, leur permettant de gérer en toute sécurité leurs connexions I2P depuis n'importe où dans le monde. D'autres Encrypted LeaseSets que je conserve sur le même appareil pour la même raison pointent vers le serveur SSH, l'instance Portainer que j'utilise pour gérer mes conteneurs de services, et mon instance NextCloud personnelle. Avec I2P, l'auto-hébergement véritablement privé et toujours joignable est un objectif atteignable; en fait, je pense que c'est l'une des choses pour lesquelles nous sommes particulièrement adaptés, grâce aux Encrypted LeaseSets. Avec eux, I2P pourrait devenir la clé de la sécurisation de la domotique auto-hébergée ou simplement devenir l'épine dorsale d'un nouveau web pair à pair plus privé.
