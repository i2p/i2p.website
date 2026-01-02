---
title: "Créer et exécuter un serveur de réamorçage I2P"
description: "Guide complet pour configurer et exploiter un serveur de reseed I2P afin d'aider les nouveaux routeurs à rejoindre le réseau"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

Les hôtes de reseed sont une infrastructure cruciale pour le réseau I2P, fournissant aux nouveaux routers un groupe initial de nœuds lors du processus de bootstrap. Ce guide vous guidera à travers la configuration et l'exécution de votre propre serveur de reseed.

## Qu'est-ce qu'un serveur I2P Reseed ?

Un serveur de reseed I2P aide à intégrer de nouveaux routeurs dans le réseau I2P en :

- **Fourniture de la découverte initiale des pairs** : Les nouveaux routeurs reçoivent un ensemble de départ de nœuds réseau auxquels se connecter
- **Récupération du bootstrap** : Aide aux routeurs qui ont des difficultés à maintenir leurs connexions
- **Distribution sécurisée** : Le processus de reseeding est chiffré et signé numériquement pour garantir la sécurité du réseau

Lorsqu'un nouveau router I2P démarre pour la première fois (ou a perdu toutes ses connexions avec ses pairs), il contacte les serveurs de reseed pour télécharger un ensemble initial d'informations de router. Cela permet au nouveau router de commencer à construire sa propre netDb et à établir des tunnels.

## Prérequis

Avant de commencer, vous aurez besoin de :

- Un serveur Linux (Debian/Ubuntu recommandé) avec accès root
- Un nom de domaine pointant vers votre serveur
- Au moins 1 Go de RAM et 10 Go d'espace disque
- Un router I2P en fonctionnement sur le serveur pour alimenter la netDb
- Une connaissance de base de l'administration système Linux

## Préparation du serveur

### Step 1: Update System and Install Dependencies

Tout d'abord, mettez à jour votre système et installez les paquets requis :

```bash
sudo apt update && sudo apt upgrade -y && sudo apt-get install golang-go git make docker.io docker-compose -y
```
Cela installe : - **golang-go** : environnement d'exécution du langage de programmation Go - **git** : système de contrôle de version - **make** : outil d'automatisation de compilation - **docker.io & docker-compose** : plateforme de conteneurisation pour exécuter Nginx Proxy Manager

![Installation des paquets requis](/images/guides/reseed/reseed_01.png)

### Step 2: Clone and Build Reseed Tools

Clonez le dépôt reseed-tools et compilez l'application :

```bash
cd /home/i2p
git clone https://i2pgit.org/idk/reseed-tools
cd reseed-tools
make build
sudo make install
```
Le package `reseed-tools` fournit les fonctionnalités de base pour exécuter un serveur reseed. Il gère : - La collecte des informations de router depuis votre base de données réseau locale - L'empaquetage des informations de router dans des fichiers SU3 signés - La distribution de ces fichiers via HTTPS

![Clonage du dépôt reseed-tools](/images/guides/reseed/reseed_02.png)

### Step 3: Generate SSL Certificate

Générez le certificat SSL et la clé privée de votre serveur reseed :

```bash
su - i2p -c 'reseed-tools reseed --signer=admin@stormycloud.org --netdb=/home/i2p/.i2p/netDb --port=8443 --ip=127.0.0.1 --trustProxy'
```
**Paramètres importants** : - `--signer` : Votre adresse email (remplacez `admin@stormycloud.org` par la vôtre) - `--netdb` : Chemin vers la base de données réseau de votre routeur I2P - `--port` : Port interne (8443 est recommandé) - `--ip` : Lier à localhost (nous utiliserons un reverse proxy pour l'accès public) - `--trustProxy` : Faire confiance aux en-têtes X-Forwarded-For du reverse proxy

La commande va générer : - Une clé privée pour signer les fichiers SU3 - Un certificat SSL pour les connexions HTTPS sécurisées

![Génération de certificat SSL](/images/guides/reseed/reseed_03.png)

### Étape 1 : Mettre à jour le système et installer les dépendances

**Critique** : Sauvegardez de manière sécurisée les clés générées situées dans `/home/i2p/.reseed/` :

```bash
sudo tar -czf reseed-keys-backup.tar.gz /home/i2p/.reseed/
```
Stockez cette sauvegarde dans un emplacement sécurisé et chiffré avec un accès limité. Ces clés sont essentielles au fonctionnement de votre serveur reseed et doivent être protégées avec soin.

## Configuring the Service

### Étape 2 : Cloner et compiler les outils Reseed

Créez un service systemd pour exécuter le serveur reseed automatiquement :

```bash
sudo tee /etc/systemd/system/reseed.service <<EOF
[Unit]
Description=Reseed Service
After=network.target

[Service]
User=i2p
WorkingDirectory=/home/i2p
ExecStart=/bin/bash -c 'reseed-tools reseed --signer=admin@stormycloud.org --netdb=/home/i2p/.i2p/netDb --port=8443 --ip=127.0.0.1 --trustProxy'
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
```
**N'oubliez pas de remplacer** `admin@stormycloud.org` par votre propre adresse e-mail.

Maintenant, activez et démarrez le service :

```bash
sudo systemctl daemon-reload
sudo systemctl enable reseed
sudo systemctl start reseed
```
Vérifiez que le service est en cours d'exécution :

```bash
sudo systemctl status reseed
```
![Vérification de l'état du service de reseed](/images/guides/reseed/reseed_04.png)

### Étape 3 : Générer un certificat SSL

Pour des performances optimales, vous pouvez redémarrer périodiquement le service de reseed afin de rafraîchir les informations du router :

```bash
sudo crontab -e
```
Ajoutez cette ligne pour redémarrer le service toutes les 3 heures :

```
0 */3 * * * systemctl restart reseed
```
## Setting Up Reverse Proxy

Le serveur reseed s'exécute sur localhost:8443 et nécessite un reverse proxy pour gérer le trafic HTTPS public. Nous recommandons Nginx Proxy Manager pour sa facilité d'utilisation.

### Étape 4 : Sauvegardez vos clés

Déployer Nginx Proxy Manager avec Docker :

```bash
docker run -d \
--name nginx-proxy-manager \
-p 80:80 \
-p 81:81 \
-p 443:443 \
-v $(pwd)/data:/data \
-v $(pwd)/letsencrypt:/etc/letsencrypt \
--restart unless-stopped \
jc21/nginx-proxy-manager:latest
```
Ceci expose : - **Port 80** : Trafic HTTP - **Port 81** : Interface d'administration - **Port 443** : Trafic HTTPS

### Configure Proxy Manager

1. Accédez à l'interface d'administration à l'adresse `http://your-server-ip:81`

2. Connexion avec les identifiants par défaut :
   - **Email** : admin@example.com
   - **Mot de passe** : changeme

**Important** : Modifiez ces identifiants immédiatement après la première connexion !

![Connexion Nginx Proxy Manager](/images/guides/reseed/reseed_05.png)

3. Naviguez vers **Proxy Hosts** et cliquez sur **Add Proxy Host**

![Ajout d'un hôte proxy](/images/guides/reseed/reseed_06.png)

4. Configurez l'hôte proxy :
   - **Nom de domaine** : Votre domaine reseed (par ex., `reseed.example.com`)
   - **Schéma** : `https`
   - **Nom d'hôte / IP de transfert** : `127.0.0.1`
   - **Port de transfert** : `8443`
   - Activez **Cache Assets**
   - Activez **Block Common Exploits**
   - Activez **Websockets Support**

![Configuration des détails de l'hôte proxy](/images/guides/reseed/reseed_07.png)

5. Dans l'onglet **SSL** :
   - Sélectionnez **Request a new SSL Certificate** (Let's Encrypt)
   - Activez **Force SSL**
   - Activez **HTTP/2 Support**
   - Acceptez les conditions d'utilisation de Let's Encrypt

![Configuration du certificat SSL](/images/guides/reseed/reseed_08.png)

6. Cliquez sur **Enregistrer**

Votre serveur de reseed devrait maintenant être accessible à `https://reseed.example.com`

![Configuration réussie du serveur de reseed](/images/guides/reseed/reseed_09.png)

## Registering Your Reseed Server

Une fois votre serveur de reseed opérationnel, contactez les développeurs I2P pour qu'il soit ajouté à la liste officielle des serveurs de reseed.

### Étape 5 : Créer le service Systemd

Envoyez un email à **zzz** (développeur principal d'I2P) avec les informations suivantes :

- **Email I2P** : zzz@mail.i2p
- **Email Clearnet** : zzz@i2pmail.org

### Étape 6 : Optionnel - Configurer les redémarrages périodiques

Incluez dans votre e-mail :

1. **URL du serveur de reseed** : L'URL HTTPS complète (par ex., `https://reseed.example.com`)
2. **Certificat public de reseed** : Situé dans `/home/i2p/.reseed/` (joindre le fichier `.crt`)
3. **Adresse e-mail de contact** : Votre méthode de contact privilégiée pour les notifications de maintenance du serveur
4. **Emplacement du serveur** : Optionnel mais utile (pays/région)
5. **Disponibilité prévue** : Votre engagement à maintenir le serveur

### Verification

Les développeurs I2P vérifieront que votre serveur de reseed : - Est correctement configuré et distribue les informations de router - Utilise des certificats SSL valides - Fournit des fichiers SU3 correctement signés - Est accessible et réactif

Une fois approuvé, votre serveur de reseed sera ajouté à la liste distribuée avec les routeurs I2P, aidant les nouveaux utilisateurs à rejoindre le réseau !

## Monitoring and Maintenance

### Installer Nginx Proxy Manager

Surveillez votre service de reseed :

```bash
sudo systemctl status reseed
sudo journalctl -u reseed -f
```
### Configurer le gestionnaire de proxy

Surveillez les ressources système :

```bash
htop
df -h
```
### Update Reseed Tools

Mettez à jour périodiquement les reseed-tools pour obtenir les dernières améliorations :

```bash
cd /home/i2p/reseed-tools
git pull
make build
sudo make install
sudo systemctl restart reseed
```
### Informations de contact

Si vous utilisez Let's Encrypt via Nginx Proxy Manager, les certificats se renouvelleront automatiquement. Vérifiez que le renouvellement fonctionne :

```bash
docker logs nginx-proxy-manager | grep -i certificate
```
## Configuration du Service

### Informations requises

Vérifier les logs pour les erreurs :

```bash
sudo journalctl -u reseed -n 50
```
Problèmes courants : - Le routeur I2P n'est pas en cours d'exécution ou la netDb est vide - Le port 8443 est déjà utilisé - Problèmes de permissions avec le répertoire `/home/i2p/.reseed/`

### Vérification

Assurez-vous que votre routeur I2P est en cours d'exécution et qu'il a rempli sa base de données réseau :

```bash
ls -lh /home/i2p/.i2p/netDb/
```
Vous devriez voir plusieurs fichiers `.dat`. Si vide, attendez que votre routeur I2P découvre des pairs.

### SSL Certificate Errors

Vérifiez que vos certificats sont valides :

```bash
openssl s_client -connect reseed.example.com:443 -servername reseed.example.com
```
### Vérifier l'état du service

Vérifiez : - Les enregistrements DNS pointent correctement vers votre serveur - Le pare-feu autorise les ports 80 et 443 - Nginx Proxy Manager est en cours d'exécution : `docker ps`

## Security Considerations

- **Protégez vos clés privées** : Ne partagez jamais et n'exposez jamais le contenu de `/home/i2p/.reseed/`
- **Mises à jour régulières** : Maintenez à jour les paquets système, Docker et reseed-tools
- **Surveillez les journaux** : Surveillez les modèles d'accès suspects
- **Limitation du débit** : Envisagez de mettre en place une limitation du débit pour éviter les abus
- **Règles de pare-feu** : N'exposez que les ports nécessaires (80, 443, 81 pour l'administration)
- **Interface d'administration** : Restreignez l'interface d'administration de Nginx Proxy Manager (port 81) aux adresses IP de confiance

## Contributing to the Network

En exécutant un serveur reseed, vous fournissez une infrastructure critique pour le réseau I2P. Merci de contribuer à un internet plus privé et décentralisé !

Pour toute question ou assistance, contactez la communauté I2P : - **Forum** : [i2pforum.net](https://i2pforum.net) - **IRC/Reddit** : #i2p sur différents réseaux - **Développement** : [i2pgit.org](https://i2pgit.org)

---

IMPORTANT :  NE posez PAS de questions, ne fournissez PAS d'explications et n'ajoutez AUCUN commentaire. Même si le texte n'est qu'un titre ou semble incomplet, traduisez-le tel quel.

*Guide initialement créé par [Stormy Cloud](https://www.stormycloud.org), adapté pour la documentation I2P.*
