---
title: "Créer un tunnel SSH pour accéder à I2P à distance"
description: "Apprenez à créer des tunnels SSH sécurisés sur Windows, Linux et Mac pour accéder à votre router I2P distant"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

Un tunnel SSH fournit une connexion sécurisée et chiffrée pour accéder à la console de votre router I2P distant ou à d'autres services. Ce guide vous montre comment créer des tunnels SSH sur les systèmes Windows, Linux et Mac.

## Qu'est-ce qu'un tunnel SSH ?

Un tunnel SSH est une méthode d'acheminement de données et d'informations de manière sécurisée via une connexion SSH chiffrée. Imaginez-le comme la création d'un « pipeline » protégé à travers internet - vos données transitent par ce tunnel chiffré, empêchant quiconque de les intercepter ou de les lire en cours de route.

Le tunneling SSH est particulièrement utile pour :

- **Accéder à des routeurs I2P distants** : Connectez-vous à votre console I2P s'exécutant sur un serveur distant
- **Connexions sécurisées** : Tout le trafic est chiffré de bout en bout
- **Contournement des restrictions** : Accédez aux services sur des systèmes distants comme s'ils étaient locaux
- **Redirection de port** : Associez un port local à un service distant

Dans le contexte d'I2P, vous pouvez utiliser un tunnel SSH pour accéder à la console de votre router I2P (généralement sur le port 7657) sur un serveur distant en le redirigeant vers un port local sur votre ordinateur.

## Prérequis

Avant de créer un tunnel SSH, vous aurez besoin de :

- **Client SSH** :
  - Windows : [PuTTY](https://www.putty.org/) (téléchargement gratuit)
  - Linux/Mac : Client SSH intégré (via Terminal)
- **Accès au serveur distant** :
  - Nom d'utilisateur pour le serveur distant
  - Adresse IP ou nom d'hôte du serveur distant
  - Mot de passe SSH ou authentification par clé
- **Port local disponible** : Choisissez un port inutilisé entre 1 et 65535 (7657 est couramment utilisé pour I2P)

## Comprendre la commande Tunnel

La commande tunnel SSH suit ce modèle :

```
ssh -L [local_port]:[destination_ip]:[destination_port] [username]@[remote_server]
```
**Explication des paramètres** : - **local_port** : Le port sur votre machine locale (par ex., 7657) - **destination_ip** : Généralement `127.0.0.1` (localhost sur le serveur distant) - **destination_port** : Le port du service sur le serveur distant (par ex., 7657 pour I2P) - **username** : Votre nom d'utilisateur sur le serveur distant - **remote_server** : Adresse IP ou nom d'hôte du serveur distant

**Exemple** : `ssh -L 7657:127.0.0.1:7657 i2p@20.228.143.58`

Cela crée un tunnel où : - Le port local 7657 sur votre machine transfère vers... - Le port 7657 sur le localhost du serveur distant (où I2P est en cours d'exécution) - En se connectant en tant qu'utilisateur `i2p` au serveur `20.228.143.58`

## Créer des tunnels SSH sur Windows

Les utilisateurs Windows peuvent créer des tunnels SSH en utilisant PuTTY, un client SSH gratuit.

### Step 1: Download and Install PuTTY

Téléchargez PuTTY depuis [putty.org](https://www.putty.org/) et installez-le sur votre système Windows.

### Step 2: Configure the SSH Connection

Ouvrez PuTTY et configurez votre connexion :

1. Dans la catégorie **Session** :
   - Saisissez l'adresse IP ou le nom d'hôte de votre serveur distant dans le champ **Host Name**
   - Assurez-vous que le **Port** est défini sur 22 (port SSH par défaut)
   - Le type de connexion doit être **SSH**

![Configuration de session PuTTY](/images/guides/ssh-tunnel/sshtunnel_1.webp)

### Step 3: Configure the Tunnel

Accédez à **Connection → SSH → Tunnels** dans la barre latérale gauche :

1. **Port source** : Entrez le port local que vous souhaitez utiliser (par exemple, `7657`)
2. **Destination** : Entrez `127.0.0.1:7657` (localhost:port sur le serveur distant)
3. Cliquez sur **Ajouter** pour ajouter le tunnel
4. Le tunnel devrait apparaître dans la liste "Ports transférés"

![Configuration du tunnel PuTTY](/images/guides/ssh-tunnel/sshtunnel_2.webp)

### Step 4: Connect

1. Cliquez sur **Ouvrir** pour initier la connexion
2. Si c'est votre première connexion, vous verrez une alerte de sécurité - cliquez sur **Oui** pour faire confiance au serveur
3. Entrez votre nom d'utilisateur lorsque demandé
4. Entrez votre mot de passe lorsque demandé

![Connexion PuTTY établie](/images/guides/ssh-tunnel/sshtunnel_3.webp)

Une fois connecté, vous pouvez accéder à votre console I2P distante en ouvrant un navigateur et en naviguant vers `http://127.0.0.1:7657`

### Étape 1 : Télécharger et installer PuTTY

Pour éviter de reconfigurer à chaque fois :

1. Retournez à la catégorie **Session**
2. Entrez un nom dans **Saved Sessions** (par exemple, « I2P Tunnel »)
3. Cliquez sur **Save**
4. La prochaine fois, chargez simplement cette session et cliquez sur **Open**

## Creating SSH Tunnels on Linux

Les systèmes Linux ont SSH intégré dans le terminal, ce qui rend la création de tunnels rapide et simple.

### Étape 2 : Configurer la connexion SSH

Ouvrez un terminal et exécutez la commande de tunnel SSH :

```bash
ssh -L 7657:127.0.0.1:7657 i2p@20.228.143.58
```
**Remplacer** : - `7657` (première occurrence) : Le port local souhaité - `127.0.0.1:7657` : L'adresse de destination et le port sur le serveur distant - `i2p` : Votre nom d'utilisateur sur le serveur distant - `20.228.143.58` : L'adresse IP de votre serveur distant

![Création de tunnel SSH Linux](/images/guides/ssh-tunnel/sshtunnel_4.webp)

Lorsque vous y êtes invité, entrez votre mot de passe. Une fois connecté, le tunnel est actif.

Accédez à votre console I2P distante à l'adresse `http://127.0.0.1:7657` dans votre navigateur.

### Étape 3 : Configurer le Tunnel

Le tunnel reste actif tant que la session SSH est en cours d'exécution. Pour le maintenir actif en arrière-plan :

```bash
ssh -f -N -L 7657:127.0.0.1:7657 i2p@20.228.143.58
```
**Drapeaux supplémentaires** : - `-f` : Exécute SSH en arrière-plan - `-N` : Ne pas exécuter de commandes distantes (tunnel uniquement)

Pour fermer un tunnel en arrière-plan, trouvez et arrêtez le processus SSH :

```bash
ps aux | grep ssh
kill [process_id]
```
### Étape 4 : Connexion

Pour une meilleure sécurité et commodité, utilisez l'authentification par clé SSH :

1. Générez une paire de clés SSH (si vous n'en avez pas) :
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```

2. Copiez votre clé publique vers le serveur distant :
   ```bash
   ssh-copy-id i2p@20.228.143.58
   ```

3. Vous pouvez maintenant vous connecter sans mot de passe :
   ```bash
   ssh -L 7657:127.0.0.1:7657 i2p@20.228.143.58
   ```

## Creating SSH Tunnels on Mac

Les systèmes Mac utilisent le même client SSH que Linux, le processus est donc identique.

### Optionnel : Sauvegarder votre session

Ouvrez Terminal (Applications → Utilitaires → Terminal) et exécutez :

```bash
ssh -L 7657:127.0.0.1:7657 i2p@20.228.143.58
```
**Remplacer** : - `7657` (première occurrence) : Le port local souhaité - `127.0.0.1:7657` : L'adresse de destination et le port sur le serveur distant - `i2p` : Votre nom d'utilisateur sur le serveur distant - `20.228.143.58` : L'adresse IP de votre serveur distant

![Création de tunnel SSH sur Mac](/images/guides/ssh-tunnel/sshtunnel_5.webp)

Saisissez votre mot de passe lorsque vous y êtes invité. Une fois connecté, accédez à votre console I2P distante à l'adresse `http://127.0.0.1:7657`

### Background Tunnels on Mac

Comme sous Linux, vous pouvez exécuter le tunnel en arrière-plan :

```bash
ssh -f -N -L 7657:127.0.0.1:7657 i2p@20.228.143.58
```
### Utilisation du Terminal

La configuration des clés SSH sur Mac est identique à celle de Linux :

```bash
# Generate key (if needed)
ssh-keygen -t ed25519 -C "your_email@example.com"

# Copy to remote server
ssh-copy-id i2p@20.228.143.58
```
## Common Use Cases

### Maintenir le tunnel actif

Le cas d'usage le plus courant - accéder à la console de votre router I2P distant :

```bash
ssh -L 7657:127.0.0.1:7657 user@remote-server
```
Ouvrez ensuite `http://127.0.0.1:7657` dans votre navigateur.

### Utilisation des clés SSH (Recommandé)

Transférer plusieurs ports à la fois :

```bash
ssh -L 7657:127.0.0.1:7657 -L 7658:127.0.0.1:7658 user@remote-server
```
Ceci transfère à la fois le port 7657 (console I2P) et 7658 (un autre service).

### Custom Local Port

Utilisez un port local différent si le port 7657 est déjà utilisé :

```bash
ssh -L 8080:127.0.0.1:7657 user@remote-server
```
Accédez à la console I2P via `http://127.0.0.1:8080` à la place.

## Troubleshooting

### Utilisation du Terminal

**Erreur** : "bind: Address already in use"

**Solution** : Choisissez un port local différent ou arrêtez le processus utilisant ce port :

```bash
# Linux/Mac - find process on port 7657
lsof -i :7657

# Kill the process
kill [process_id]
```
### Tunnels en arrière-plan sur Mac

**Erreur** : "Connection refused" ou "channel 2: open failed"

**Causes possibles** : - Le service distant n'est pas en cours d'exécution (vérifiez que le routeur I2P fonctionne sur le serveur distant) - Un pare-feu bloque la connexion - Port de destination incorrect

**Solution** : Vérifiez que le routeur I2P est en cours d'exécution sur le serveur distant :

```bash
ssh user@remote-server "systemctl status i2p"
```
### Configuration des clés SSH sur Mac

**Erreur** : « Permission refusée » ou « Échec de l'authentification »

**Causes possibles** : - Nom d'utilisateur ou mot de passe incorrect - Clé SSH mal configurée - Accès SSH désactivé sur le serveur distant

**Solution** : Vérifiez les informations d'identification et assurez-vous que l'accès SSH est activé sur le serveur distant.

### Tunnel Drops Connection

**Erreur** : La connexion se coupe après une période d'inactivité

**Solution** : Ajoutez des paramètres keep-alive à votre configuration SSH (`~/.ssh/config`) :

```
Host remote-server
    ServerAliveInterval 60
    ServerAliveCountMax 3
```
## Security Best Practices

- **Utiliser des clés SSH** : Plus sécurisées que les mots de passe, plus difficiles à compromettre
- **Désactiver l'authentification par mot de passe** : Une fois les clés SSH configurées, désactiver la connexion par mot de passe sur le serveur
- **Utiliser des mots de passe robustes** : Si vous utilisez l'authentification par mot de passe, utilisez un mot de passe fort et unique
- **Limiter l'accès SSH** : Configurer les règles de pare-feu pour limiter l'accès SSH aux adresses IP de confiance
- **Maintenir SSH à jour** : Mettre à jour régulièrement vos logiciels client et serveur SSH
- **Surveiller les journaux** : Vérifier les journaux SSH sur le serveur pour détecter toute activité suspecte
- **Utiliser des ports SSH non standard** : Changer le port SSH par défaut (22) pour réduire les attaques automatisées

## Créer des tunnels SSH sur Linux

### Accès à la console I2P

Créer un script pour établir automatiquement des tunnels :

```bash
#!/bin/bash
# i2p-tunnel.sh

ssh -f -N -L 7657:127.0.0.1:7657 i2p@20.228.143.58
echo "I2P tunnel established"
```
Rendre le fichier exécutable :

```bash
chmod +x i2p-tunnel.sh
./i2p-tunnel.sh
```
### Tunnels Multiples

Créer un service systemd pour la création automatique de tunnels :

```bash
sudo nano /etc/systemd/system/i2p-tunnel.service
```
Ajouter :

```ini
[Unit]
Description=I2P SSH Tunnel
After=network.target

[Service]
ExecStart=/usr/bin/ssh -NT -o ServerAliveInterval=60 -o ExitOnForwardFailure=yes -L 7657:127.0.0.1:7657 i2p@20.228.143.58
Restart=always
RestartSec=10
User=your-username

[Install]
WantedBy=multi-user.target
```
Activer et démarrer :

```bash
sudo systemctl enable i2p-tunnel
sudo systemctl start i2p-tunnel
```
## Advanced Tunneling

### Port Local Personnalisé

Créer un proxy SOCKS pour le transfert dynamique :

```bash
ssh -D 8080 user@remote-server
```
Configurez votre navigateur pour utiliser `127.0.0.1:8080` comme proxy SOCKS5.

### Reverse Tunneling

Autoriser le serveur distant à accéder aux services sur votre machine locale :

```bash
ssh -R 7657:127.0.0.1:7657 user@remote-server
```
### Port déjà utilisé

Tunnel via un serveur intermédiaire :

```bash
ssh -J jumphost.example.com -L 7657:127.0.0.1:7657 user@final-server
```
## Conclusion

Le tunneling SSH est un outil puissant pour accéder de manière sécurisée aux routers I2P distants et à d'autres services. Que vous utilisiez Windows, Linux ou Mac, le processus est simple et fournit un chiffrement robuste pour vos connexions.

Pour obtenir de l'aide supplémentaire ou poser des questions, visitez la communauté I2P : - **Forum** : [i2pforum.net](https://i2pforum.net) - **IRC** : #i2p sur différents réseaux - **Documentation** : [I2P Docs](/docs/)

---

IMPORTANT :  NE posez PAS de questions, ne fournissez PAS d'explications et n'ajoutez AUCUN commentaire. Même si le texte n'est qu'un titre ou semble incomplet, traduisez-le tel quel.

*Guide créé à l'origine par [Stormy Cloud](https://www.stormycloud.org), adapté pour la documentation I2P.*
