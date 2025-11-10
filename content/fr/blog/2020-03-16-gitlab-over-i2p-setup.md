---
title: "Configuration de Gitlab via I2P"
date: 2020-03-16
author: "idk"
description: "Héberger des miroirs de dépôts Git I2P et faire la passerelle vers des dépôts Clearnet pour les autres"
categories: ["development"]
---

This is the setup process I use for configuring Gitlab and I2P, with Docker in place to manage the service itself. Gitlab is very easy to host on I2P in this fashion, it can be administered by one person without much difficulty. These instructions should work on any Debian-based system and should easily translate to any system where Docker and an I2P router are available.

## Dépendances et Docker

Comme Gitlab s'exécute dans un conteneur, nous n'avons besoin d'installer sur notre système principal que les dépendances nécessaires au conteneur. Pour plus de commodité, vous pouvez tout installer avec :

```
sudo apt install docker.io
```
## Récupérer les conteneurs Docker

Une fois que vous avez installé docker, vous pouvez récupérer les conteneurs docker nécessaires pour gitlab. *Ne les lancez pas encore.*

```
docker pull gitlab/gitlab-ce
```
## Configurer un proxy HTTP I2P pour Gitlab (Informations importantes, étapes facultatives)

Les serveurs Gitlab à l'intérieur d'I2P peuvent fonctionner avec ou sans la possibilité d'interagir avec des serveurs sur l'internet en dehors d'I2P. Dans le cas où le serveur Gitlab n'est *pas autorisé* à interagir avec des serveurs en dehors d'I2P, il ne peut pas être désanonymisé en clonant un dépôt git depuis un serveur git sur l'internet en dehors d'I2P.

Dans le cas où le serveur Gitlab est *autorisé* à interagir avec des serveurs en dehors d’I2P, il peut agir comme un « pont » pour les utilisateurs, qui peuvent l’utiliser pour mettre en miroir du contenu en dehors d’I2P vers une source accessible via I2P, cependant il *n’est pas anonyme* dans ce cas.

**Si vous souhaitez disposer d'une instance Gitlab en mode pont, non anonyme, avec accès aux dépôts web**, aucune modification supplémentaire n'est nécessaire.

**Si vous souhaitez disposer d’une instance Gitlab exclusivement I2P sans accès aux dépôts exclusivement Web**, vous devrez configurer Gitlab pour utiliser un proxy HTTP I2P. Étant donné que le proxy HTTP I2P par défaut n’écoute que sur `127.0.0.1`, vous devrez en mettre en place un nouveau pour Docker qui écoute sur l’adresse hôte/passerelle du réseau Docker, généralement `172.17.0.1`. Je configure le mien sur le port `4446`.

## Démarrer le conteneur localement

Une fois que tout est en place, vous pouvez démarrer le conteneur et publier votre instance Gitlab localement:

```
docker run --detach \
  --env HTTP_PROXY=http://172.17.0.1:4446 \
  --publish 127.0.0.1:8443:443 --publish 127.0.0.1:8080:80 --publish 127.0.0.1:8022:22 \
  --name gitlab \
  --restart always \
  --volume /srv/gitlab/config:/etc/gitlab:Z \
  --volume /srv/gitlab/logs:/var/log/gitlab:Z \
  --volume /srv/gitlab/data:/var/opt/gitlab:Z \
  gitlab/gitlab-ce:latest
```
Accédez à votre instance GitLab locale et configurez votre compte administrateur. Choisissez un mot de passe fort et définissez des limites de comptes utilisateurs adaptées à vos ressources.

## Configurez vos tunnels de service et enregistrez un nom d’hôte

Une fois que Gitlab est configuré en local, accédez à la console du I2P Router. Vous devrez configurer deux tunnels serveur, l'un menant à l'interface web(HTTP) de Gitlab sur le port TCP 8080, et l'autre à l'interface SSH de Gitlab sur le port TCP 8022.

### Gitlab Web(HTTP) Interface

Pour l’interface Web, utilisez un "HTTP" server tunnel. Depuis http://127.0.0.1:7657/i2ptunnelmgr lancez le "New Tunnel Wizard" et saisissez les valeurs suivantes :

1. Select "Server Tunnel"
2. Select "HTTP Server"
3. Fill in "Gitlab Web Service" or otherwise describe the tunnel
4. Fill in `127.0.0.1` for the host and `8080` for the port
5. Select "Automatically start tunnel when Router Starts"
6. Confirm your selections

### Gitlab SSH Interface

Pour l'interface SSH, utilisez un tunnel serveur "Standard". Depuis http://127.0.0.1:7657/i2ptunnelmgr, lancez le "New Tunnel Wizard" et saisissez les valeurs suivantes :

1. Select "Server Tunnel"
2. Select "Standard Server"
3. Fill in "Gitlab SSH Service" or otherwise describe the tunnel
4. Fill in `127.0.0.1` for the host and `8022` for the port
5. Select "Automatically start tunnel when Router Starts"
6. Confirm your selections

## Re-start the Gitlab Service with the new Hostname

Enfin, si vous avez soit modifié `gitlab.rb`, soit enregistré un nom d’hôte, vous devrez redémarrer le service GitLab pour que les paramètres prennent effet.
