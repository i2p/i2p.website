---
title: "Exécuter GitLab sur I2P"
description: "Déploiement de GitLab dans I2P en utilisant Docker et un routeur I2P"
slug: "gitlab"
lastUpdated: "2025-02"
accurateFor: "2.5.0"
---

Héberger GitLab dans I2P est simple : exécutez le conteneur omnibus GitLab, exposez-le sur loopback, et transférez le trafic à travers un tunnel I2P. Les étapes ci-dessous reflètent la configuration utilisée pour `git.idk.i2p` mais fonctionnent pour toute instance auto-hébergée.

## 1. Prérequis

- Debian ou une autre distribution Linux avec Docker Engine installé (`sudo apt install docker.io` ou `docker-ce` depuis le dépôt de Docker).
- Un routeur I2P (Java I2P ou i2pd) avec suffisamment de bande passante pour servir vos utilisateurs.
- Optionnel : une VM dédiée afin que GitLab et le routeur restent isolés de votre environnement de bureau.

## 2. Télécharger l'image GitLab

```bash
docker pull gitlab/gitlab-ce:latest
```
L'image officielle est construite à partir de couches de base Ubuntu et mise à jour régulièrement. Examinez le [Dockerfile](https://gitlab.com/gitlab-org/omnibus-gitlab/-/blob/master/docker/Dockerfile) si vous avez besoin d'une assurance supplémentaire.

## 3. Décider entre le pontage et I2P uniquement

- Les instances **I2P uniquement** ne contactent jamais les hôtes du clearnet. Les utilisateurs peuvent cloner des dépôts depuis d'autres services I2P mais pas depuis GitHub/GitLab.com. Cela maximise l'anonymat.
- Les instances **pontées** se connectent aux hébergeurs Git du clearnet via un proxy HTTP. Cela est utile pour cloner des projets publics dans I2P mais désanonymise les requêtes sortantes du serveur.

Si vous choisissez le mode bridged, configurez GitLab pour utiliser un proxy HTTP I2P lié sur l'hôte Docker (par exemple `http://172.17.0.1:4446`). Le proxy router par défaut écoute uniquement sur `127.0.0.1` ; ajoutez un nouveau tunnel proxy lié à l'adresse de passerelle Docker.

## 4. Démarrer le conteneur

```bash
docker run --detach \
  --env HTTP_PROXY=http://172.17.0.1:4446 \  # omit for I2P-only
  --publish 127.0.0.1:8443:443 \
  --publish 127.0.0.1:8080:80 \
  --publish 127.0.0.1:8022:22 \
  --name gitlab \
  --restart always \
  --volume /srv/gitlab/config:/etc/gitlab:Z \
  --volume /srv/gitlab/logs:/var/log/gitlab:Z \
  --volume /srv/gitlab/data:/var/opt/gitlab:Z \
  gitlab/gitlab-ce:latest
```
- Liez les ports publiés à loopback ; les tunnels I2P les exposeront selon les besoins.
- Remplacez `/srv/gitlab/...` par des chemins de stockage adaptés à votre hôte.

Une fois le conteneur en cours d'exécution, visitez `https://127.0.0.1:8443/`, définissez un mot de passe administrateur et configurez les limites de compte.

## 5. Exposer GitLab via I2P

Créez trois tunnels **serveur** I2PTunnel :

| Purpose | Local target | Suggested inbound port |
| --- | --- | --- |
| HTTPS web UI | `127.0.0.1:8443` | auto-generated |
| HTTP web UI (optional) | `127.0.0.1:8080` | auto-generated |
| SSH push/pull | `127.0.0.1:8022` | auto-generated |
Configurez chaque tunnel avec des longueurs de tunnel et une bande passante appropriées. Pour les instances publiques, 3 sauts avec 4 à 6 tunnels par direction constituent un bon point de départ. Publiez les destinations Base32/Base64 résultantes sur votre page d'accueil afin que les utilisateurs puissent configurer les tunnels clients.

### Destination Enforcement

Si vous utilisez des tunnels HTTP(S), activez l'application de destination afin que seul le nom d'hôte prévu puisse atteindre le service. Cela empêche le tunnel d'être utilisé abusivement comme proxy générique.

## 6. Maintenance Tips

- Exécutez `docker exec gitlab gitlab-ctl reconfigure` à chaque modification des paramètres GitLab.
- Surveillez l'utilisation du disque (`/srv/gitlab/data`)—les dépôts Git croissent rapidement.
- Sauvegardez régulièrement les répertoires de configuration et de données. Les [tâches rake de sauvegarde](https://docs.gitlab.com/ee/raketasks/backup_restore.html) de GitLab fonctionnent à l'intérieur du conteneur.
- Envisagez de placer un tunnel de surveillance externe en mode client pour garantir que le service est accessible depuis le réseau élargi.

## 6. Conseils de maintenance

- [Intégrer I2P dans votre application](/docs/applications/embedding/)
- [Git sur I2P (guide client)](/docs/applications/git/)
- [Bundles Git pour réseaux hors ligne/lents](/docs/applications/git-bundle/)

Une instance GitLab bien configurée fournit un hub de développement collaboratif entièrement à l'intérieur d'I2P. Maintenez le router en bonne santé, restez à jour avec les mises à jour de sécurité de GitLab et coordonnez-vous avec la communauté à mesure que votre base d'utilisateurs grandit.
