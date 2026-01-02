---
title: "Hôtes de réensemencement"
description: "Exploitation des services de reseed (distribution initiale du netDb) et des méthodes alternatives d'amorçage"
slug: "reseed"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
---

## À propos des hôtes de réensemencement

De nouveaux routers ont besoin d’une poignée de pairs pour rejoindre le réseau I2P. Les Reseed hosts (serveurs de réamorçage) fournissent cet ensemble de démarrage initial via des téléchargements HTTPS chiffrés. Chaque reseed bundle (archive de réamorçage) est signé par l’hôte, ce qui empêche toute altération par des tiers non authentifiés. Les routers établis peuvent occasionnellement effectuer un reseed si leur ensemble de pairs devient obsolète.

### Processus d’amorçage du réseau

Lorsqu’un router I2P démarre pour la première fois ou a été hors ligne pendant une longue période, il a besoin de données RouterInfo (informations du routeur) pour se connecter au réseau. Comme le router n’a pas encore de pairs, il ne peut pas obtenir ces informations depuis l’intérieur du réseau I2P lui-même. Le mécanisme de reseed (réensemencement) résout ce problème d’amorçage en fournissant des fichiers RouterInfo depuis des serveurs HTTPS externes de confiance.

Le processus de reseed (réamorçage) fournit 75 à 100 fichiers RouterInfo dans un seul paquet signé cryptographiquement. Cela garantit que les nouveaux routers peuvent établir rapidement des connexions sans les exposer à des attaques de type homme du milieu qui pourraient les isoler dans des partitions de réseau distinctes et non approuvées.

### État actuel du réseau

En octobre 2025, le réseau I2P fonctionne avec la version 2.10.0 du router (version de l'API 0.9.67). Le protocole de réensemencement introduit avec la version 0.9.14 demeure stable et inchangé dans ses fonctionnalités essentielles. Le réseau maintient plusieurs serveurs de réensemencement indépendants, répartis dans le monde entier, afin de garantir la disponibilité et la résistance à la censure.

Le service [checki2p](https://checki2p.com/reseed) surveille tous les serveurs I2P de reseed (réensemencement) toutes les 4 heures, fournissant des vérifications du statut en temps réel et des métriques de disponibilité pour l’infrastructure de reseed.

## Spécification du format de fichier SU3

Le format de fichier SU3 est la base du protocole de réensemencement d'I2P, fournissant une distribution de contenu signée cryptographiquement. Comprendre ce format est essentiel pour implémenter des serveurs et des clients de réensemencement.

### Structure des fichiers

Le format SU3 se compose de trois composants principaux : un en-tête (40 octets ou plus), un contenu (longueur variable) et une signature (longueur indiquée dans l’en-tête).

#### Format de l'en-tête (octets 0-39 minimum)

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Byte Range</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Field</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">0-5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Magic Number</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ASCII string "I2Psu3" (0x493250737533)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">File Format Version</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Current version: 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">8-9</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature Type</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big-endian 16-bit integer. Type 6 = RSA-4096-SHA512 (reseed standard)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">10-11</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signature Length</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big-endian 16-bit integer. 512 bytes (0x0200) for RSA-4096</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">12</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">13</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Version Length</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Minimum 16 bytes (0x10) for compatibility</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">14</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">15</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signer ID Length</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Length of UTF-8 signer identifier string</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">16-23</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Content Length</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Big-endian 64-bit integer, length of content in bytes</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">24</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">25</td><td style="border:1px solid var(--color-border); padding:0.5rem;">File Type</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0x00 = ZIP, 0x01 = XML, 0x02 = HTML, 0x03 = XML.GZ, 0x04 = TXT.GZ, 0x05 = DMG, 0x06 = EXE</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">26</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Reserved</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be 0x00</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">27</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Content Type</td><td style="border:1px solid var(--color-border); padding:0.5rem;">0x00 = unknown, 0x01 = router update, 0x02 = plugin, 0x03 = reseed, 0x04 = news, 0x05 = blocklist</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">28-39</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Padding</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Unused, must be all zeros</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">40-55</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Version String</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ASCII version string, padded with zeros (minimum 16 bytes)</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">56-...</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Signer ID</td><td style="border:1px solid var(--color-border); padding:0.5rem;">UTF-8 encoded signer identifier (e.g., "user@mail.i2p")</td></tr>
  </tbody>
</table>
### Paramètres SU3 spécifiques au réensemencement

Pour les bundles de reseed (réamorçage), le fichier SU3 doit avoir les caractéristiques suivantes :

- **Nom de fichier**: Doit être exactement `i2pseeds.su3`
- **Type de contenu** (octet 27): 0x03 (RESEED, réensemencement)
- **Type de fichier** (octet 25): 0x00 (ZIP)
- **Type de signature** (octets 8-9): 0x0006 (RSA-4096-SHA512)
- **Chaîne de version**: Horodatage Unix en ASCII (secondes depuis l'époque Unix, au format date +%s)
- **Identifiant du signataire**: Identifiant de type adresse e-mail correspondant au CN du certificat X.509

#### Paramètre de requête pour l'identifiant du réseau

Depuis la version 0.9.42, les routers ajoutent `?netid=2` aux requêtes de réensemencement. Cela empêche les connexions inter-réseaux, car les réseaux de test utilisent des identifiants de réseau différents. Le réseau de production I2P actuel utilise l’identifiant de réseau 2.

Exemple de requête : `https://reseed.example.com/i2pseeds.su3?netid=2`

### Structure du contenu ZIP

La section de contenu (après l’en-tête, avant la signature) contient une archive ZIP standard répondant aux exigences suivantes :

- **Compression**: Compression ZIP standard (DEFLATE)
- **Nombre de fichiers**: Généralement 75 à 100 fichiers RouterInfo
- **Structure du répertoire**: Tous les fichiers doivent se trouver à la racine (aucun sous-répertoire)
- **Convention de nommage**: `routerInfo-{44-character-base64-hash}.dat`
- **Alphabet Base64**: Doit utiliser l'alphabet Base64 modifié d'I2P

L'alphabet base64 d'I2P diffère du base64 standard en utilisant `-` et `~` au lieu de `+` et `/` afin de garantir la compatibilité avec les systèmes de fichiers et les URL.

### Signature cryptographique

La signature couvre l’ensemble du fichier depuis l’octet 0 jusqu’à la fin de la section de contenu. La signature elle-même est ajoutée après le contenu.

#### Algorithme de signature (RSA-4096-SHA512)

1. Calculer le hachage SHA-512 de l’octet 0 jusqu’à la fin du contenu
2. Signer le hachage en utilisant "raw" RSA (NONEwithRSA en terminologie Java; RSA sans remplissage)
3. Compléter la signature avec des zéros en tête si nécessaire pour atteindre 512 octets
4. Ajouter la signature de 512 octets à la fin du fichier

#### Processus de vérification de signature

Les clients doivent :

1. Lire les octets 0-11 pour déterminer le type et la longueur de la signature
2. Lire l'en-tête complet pour localiser les limites du contenu
3. Lire le contenu en flux tout en calculant le hachage SHA-512
4. Extraire la signature de la fin du fichier
5. Vérifier la signature à l'aide de la clé publique RSA-4096 du signataire
6. Rejeter le fichier si la vérification de la signature échoue

### Modèle de confiance des certificats

Les clés de signature de reseed (mécanisme d’amorçage du réseau) sont distribuées sous forme de certificats X.509 autosignés avec des clés RSA-4096. Ces certificats sont inclus dans les paquets du router I2P dans le répertoire `certificates/reseed/`.

Format du certificat: - **Type de clé**: RSA-4096 - **Signature**: Auto-signée - **CN du sujet**: Doit correspondre à l'ID du signataire dans l'en-tête SU3 - **Dates de validité**: Les clients devraient faire respecter les périodes de validité du certificat

## Exploiter un hôte Reseed (serveur de réensemencement)

Exploiter un service de reseed (distribution initiale des données du netDb aux nouveaux routers) nécessite une attention particulière à la sécurité, à la fiabilité et à la diversité du réseau. Un plus grand nombre d’hôtes de reseed indépendants accroît la résilience et rend plus difficile pour des attaquants ou des censeurs de bloquer l’arrivée de nouveaux routers.

### Exigences techniques

#### Spécifications du serveur

- **Système d’exploitation**: Unix/Linux (Ubuntu, Debian, FreeBSD testés et recommandés)
- **Connectivité**: Adresse IPv4 statique requise, IPv6 recommandé mais facultatif
- **CPU**: Minimum 2 cœurs
- **RAM**: Minimum 2 Go
- **Bande passante**: Environ 15 Go par mois
- **Disponibilité**: Fonctionnement 24 h/24 et 7 j/7 requis
- **I2P Router**: I2P router bien intégré, fonctionnant en continu

#### Exigences logicielles

- **Java**: JDK 8 ou ultérieur (Java 17+ sera requis à partir d'I2P 2.11.0)
- **Serveur Web**: nginx ou Apache avec prise en charge du proxy inverse (Lighttpd n'est plus pris en charge en raison des limitations de l'en-tête X-Forwarded-For)
- **TLS/SSL**: Certificat TLS valide (Let's Encrypt, autosigné ou AC commerciale)
- **Protection DDoS**: fail2ban ou équivalent (obligatoire, non facultatif)
- **Reseed Tools** (outils de réensemencement initial du netDb): reseed-tools officiels depuis https://i2pgit.org/idk/reseed-tools

### Exigences de sécurité

#### Configuration HTTPS/TLS

- **Protocole**: HTTPS uniquement, pas de repli HTTP
- **Version TLS**: TLS 1.2 minimum
- **Suites de chiffrement**: Doivent inclure des chiffrements forts compatibles avec Java 8+
- **CN/SAN du certificat**: Doit correspondre au nom d’hôte de l’URL servie
- **Type de certificat**: Peut être autosigné s’il a été communiqué à l’équipe de développement, ou délivré par une autorité de certification reconnue

#### Gestion des certificats

Les certificats de signature SU3 et les certificats TLS remplissent des fonctions différentes :

- **Certificat TLS** (`certificates/ssl/`): Sécurise le transport HTTPS
- **Certificat de signature SU3** (`certificates/reseed/`): Signe les paquets de réensemencement

Les deux certificats doivent être fournis au coordinateur du reseed (amorçage initial du réseau) (zzz@mail.i2p) en vue de leur inclusion dans les paquets du router.

#### Protection contre les attaques DDoS et le scraping

Les serveurs Reseed (serveurs de réensemencement) subissent des attaques récurrentes provenant d’implémentations défectueuses, de botnets et d’acteurs malveillants tentant d’aspirer la base de données du réseau. Les mesures de protection comprennent :

- **fail2ban**: Requis pour la limitation du débit et l'atténuation des attaques
- **Diversité des lots**: Distribuer des ensembles de RouterInfo différents à des demandeurs différents
- **Cohérence des lots**: Distribuer le même lot aux requêtes répétées provenant de la même IP dans une fenêtre temporelle configurable
- **Restrictions de journalisation IP**: Ne pas divulguer les journaux ni les adresses IP (exigence de la politique de confidentialité)

### Méthodes d'implémentation

#### Méthode 1 : reseed-tools officiel (recommandé)

L’implémentation canonique maintenue par le projet I2P. Dépôt : https://i2pgit.org/idk/reseed-tools

**Installation**:

```bash
# Install dependencies
sudo apt-get install golang git

# Clone repository
git clone https://i2pgit.org/idk/reseed-tools.git
cd reseed-tools

# Build
make

# Generate keys and start server (first run)
./reseed-tools reseed \
  --signer=your-email@mail.i2p \
  --netdb=/path/to/i2p/netDb \
  --tlsHost=your-domain.tld \
  --port=8443
```
Lors de la première exécution, l'outil générera : - `your-email@mail.i2p.crt` (certificat de signature SU3) - `your-email@mail.i2p.pem` (clé privée de signature SU3) - `your-email@mail.i2p.crl` (liste de révocation de certificats) - fichiers de certificat et de clé TLS

**Fonctionnalités**: - Génération automatique de bundles SU3 (350 variantes, 77 RouterInfos (descripteurs de router I2P) chacune) - Serveur HTTPS intégré - Reconstruction du cache toutes les 9 heures via cron - Prise en charge de l'en-tête X-Forwarded-For avec l'option `--trustProxy` - Compatible avec les configurations de proxy inverse

**Déploiement en production**:

```bash
# Create systemd service
cat > /etc/systemd/system/i2p-reseed.service << EOF
[Unit]
Description=I2P Reseed Server
After=network.target

[Service]
Type=simple
User=i2p-reseed
WorkingDirectory=/opt/i2p-reseed
ExecStart=/opt/i2p-reseed/reseed-tools reseed \
  --signer=your-email@mail.i2p \
  --netdb=/var/lib/i2p/netDb \
  --port=8443 \
  --ip=127.0.0.1 \
  --trustProxy
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl enable i2p-reseed
systemctl start i2p-reseed
```
#### Méthode 2: Implémentation en Python (pyseeder)

Implémentation alternative par le projet PurpleI2P: https://github.com/PurpleI2P/pyseeder

```bash
pip install pyseeder

# Generate SU3 file
echo "your_password" | pyseeder reseed \
  --netdb /path/to/netDb \
  --private-key priv_key.pem \
  --outfile i2pseeds.su3 \
  --signer-id user@mail.i2p

# Serve via built-in server
pyseeder serve \
  --port 8443 \
  --host 0.0.0.0 \
  --private-key priv_key.pem \
  --cert user_at_mail.i2p.crt \
  --file i2pseeds.su3
```
#### Méthode 3 : Déploiement avec Docker

Pour les environnements conteneurisés, plusieurs implémentations prêtes pour Docker existent :

- **DivaExchange i2p-reseed**: https://github.com/diva-exchange/i2p-reseed
- **RTradeLtd/i2p-tools-1**: Ajoute un service onion de Tor et la prise en charge d’IPFS

### Configuration du proxy inverse

#### Configuration de nginx

```nginx
upstream i2p_reseed {
    server 127.0.0.1:8443;
}

server {
    listen 443 ssl http2;
    server_name reseed.example.com;

    ssl_certificate /path/to/tls-cert.crt;
    ssl_certificate_key /path/to/tls-key.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        proxy_pass http://i2p_reseed;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $remote_addr;
        proxy_set_header Host $host;
    }
}
```
#### Configuration d’Apache

```apache
<VirtualHost *:443>
    ServerName reseed.example.com
    
    SSLEngine on
    SSLCertificateFile /path/to/tls-cert.crt
    SSLCertificateKeyFile /path/to/tls-key.key
    SSLProtocol all -SSLv2 -SSLv3 -TLSv1 -TLSv1.1
    
    ProxyRequests Off
    <Proxy *>
        Order deny,allow
        Allow from all
    </Proxy>
    
    ProxyPass / http://127.0.0.1:8443/
    ProxyPassReverse / http://127.0.0.1:8443/
</VirtualHost>
```
### Enregistrement et coordination

Pour inclure votre reseed server (serveur de réensemencement) dans le paquet officiel d'I2P:

1. Terminez la configuration et les tests
2. Envoyez les deux certificats (signature SU3 et TLS) au coordinateur du reseed (réensemencement)
3. Contact : zzz@mail.i2p ou zzz@i2pmail.org
4. Rejoignez #i2p-dev sur IRC2P pour la coordination avec les autres opérateurs

### Meilleures pratiques opérationnelles

#### Surveillance et journalisation

- Activer le format de journalisation combiné d’Apache/nginx pour les statistiques
- Mettre en place la rotation des journaux (ils grossissent rapidement)
- Surveiller la réussite de la génération du bundle et les durées de reconstruction
- Suivre l’utilisation de la bande passante et les schémas de requêtes
- Ne jamais divulguer les adresses IP ni les journaux d’accès détaillés

#### Calendrier de maintenance

- **Toutes les 9 heures**: Reconstruire le cache du bundle SU3 (format de mise à jour signé I2P) (automatisé via cron)
- **Chaque semaine**: Examiner les journaux à la recherche de schémas d'attaque
- **Chaque mois**: Mettre à jour l'I2P router et reseed-tools (outils de réensemencement I2P)
- **Au besoin**: Renouveler les certificats TLS (automatiser avec Let's Encrypt)

#### Sélection des ports

- Par défaut : 8443 (recommandé)
- Alternative : n'importe quel port entre 1024-49151
- Port 443 : requiert des privilèges root ou une redirection de port (redirection iptables recommandée)

Exemple de redirection de port:

```bash
iptables -A PREROUTING -t nat -p tcp --dport 443 -j REDIRECT --to-port 8443
```
## Méthodes alternatives de reseed (réamorçage de netDb)

D'autres options d'amorçage aident les utilisateurs situés derrière des réseaux restrictifs :

### Reseed (réamorçage) basé sur des fichiers

Introduit dans la version 0.9.16, le réensemencement basé sur des fichiers permet aux utilisateurs de charger manuellement des paquets RouterInfo (informations du router). Cette méthode est particulièrement utile pour les utilisateurs situés dans des régions censurées où les serveurs de réensemencement HTTPS sont bloqués.

**Processus**: 1. Un contact de confiance génère un SU3 bundle (fichier SU3 signé) à l'aide de son router 2. Le bundle est transféré via e-mail, une clé USB ou un autre canal hors bande 3. L'utilisateur place `i2pseeds.su3` dans le répertoire de configuration d'I2P 4. Le router détecte et traite automatiquement le bundle au redémarrage

**Documentation**: /blog/2020/06/07/help-your-friends-join-i2p-by-sharing-reseed-bundles/

**Cas d'utilisation**: - Utilisateurs derrière des pare-feux nationaux bloquant les reseed servers (serveurs de réamorçage) - Réseaux isolés nécessitant un bootstrap (amorçage) manuel - Environnements de test et de développement

### Réensemencement via Cloudflare

Acheminer le trafic de reseed (réamorçage) via le CDN de Cloudflare offre plusieurs avantages pour les opérateurs dans les régions fortement censurées.

**Avantages**: - Adresse IP du serveur d’origine masquée aux clients - Protection contre les attaques DDoS grâce à l’infrastructure de Cloudflare - Répartition géographique de la charge via la mise en cache en périphérie - Amélioration des performances pour les clients du monde entier

**Exigences d'implémentation**: - option `--trustProxy` activée dans reseed-tools - Proxy Cloudflare activé pour l'enregistrement DNS - Gestion correcte de l'en-tête X-Forwarded-For

**Points importants**: - Des restrictions de ports Cloudflare s'appliquent (il faut utiliser des ports pris en charge) - La cohérence du regroupement par client nécessite la prise en charge de X-Forwarded-For - La configuration SSL/TLS est gérée par Cloudflare

**Documentation** : https://homepage.np-tokumei.net/post/notes-i2p-reseed-over-cloudflare/

### Stratégies résistantes à la censure

Une étude de Nguyen Phong Hoang (USENIX FOCI 2019) identifie des méthodes d’amorçage supplémentaires pour les réseaux censurés :

#### Fournisseurs de stockage dans le cloud

- **Box, Dropbox, Google Drive, OneDrive**: Héberger des fichiers SU3 sur des liens publics
- **Avantage**: Difficile à bloquer sans perturber les services légitimes
- **Limitation**: Nécessite la distribution manuelle des URL aux utilisateurs

#### Distribution IPFS

- Héberger des paquets de reseed (réensemencement) sur InterPlanetary File System
- Le stockage adressé par contenu empêche toute altération
- Résistant aux tentatives de retrait

#### Services onion de Tor

- Serveurs de réensemencement accessibles via des adresses .onion
- Résistant au blocage par adresse IP
- Nécessite un client Tor sur le système de l’utilisateur

**Documentation de recherche**: https://homepage.np-tokumei.net/post/notes-censorship-resistant-i2p-reseeding/

#### Pays où I2P est connu pour être bloqué

En 2025, il est confirmé que les pays suivants bloquent les I2P reseed servers (serveurs d'amorçage du réseau):
- Chine
- Iran
- Oman
- Qatar
- Koweït

Les utilisateurs de ces régions devraient utiliser des méthodes d’amorçage alternatives ou des stratégies de reseeding (réamorçage du réseau) résistantes à la censure.

## Détails du protocole pour les implémenteurs

### Spécification de la requête de reseed (amorçage initial du netDb)

#### Comportement du client

1. **Sélection du serveur**: Router maintient une liste codée en dur d’URL de reseed (bootstrap/amorçage initial du netDb)
2. **Sélection aléatoire**: Le client sélectionne aléatoirement un serveur dans la liste disponible
3. **Format de requête**: `GET /i2pseeds.su3?netid=2 HTTP/1.1`
4. **User-Agent**: Doit imiter les navigateurs courants (p. ex., "Wget/1.11.4")
5. **Logique de nouvelle tentative**: Si la requête SU3 échoue, se replier sur l’analyse de la page d’index
6. **Validation du certificat**: Vérifier le certificat TLS par rapport au magasin de certificats de confiance du système
7. **Validation de la signature SU3**: Vérifier la signature par rapport aux certificats de reseed connus

#### Comportement du serveur

1. **Sélection du lot**: Sélectionner un sous-ensemble pseudo-aléatoire de RouterInfos depuis netDb
2. **Suivi client**: Identifier les requêtes par l’adresse IP source (en respectant X-Forwarded-For)
3. **Cohérence du lot**: Renvoyer le même lot pour les requêtes répétées dans une fenêtre temporelle (généralement 8-12 heures)
4. **Diversité des lots**: Renvoyer des lots différents à des clients différents pour assurer la diversité du réseau
5. **Content-Type**: `application/octet-stream` ou `application/x-i2p-reseed`

### Format du fichier RouterInfo

Chaque fichier `.dat` dans le paquet de reseed contient une structure RouterInfo (structure d'information du router) :

**Nommage des fichiers**: `routerInfo-{base64-hash}.dat` - Le hachage comporte 44 caractères en utilisant l'alphabet base64 d'I2P - Exemple: `routerInfo-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmn.dat`

**Contenu du fichier**: - RouterIdentity (hachage du router, clé de chiffrement, clé de signature) - Horodatage de publication - Adresses du router (IP, port, type de transport) - Fonctionnalités et options du router - Signature couvrant l'ensemble des données ci-dessus

### Exigences en matière de diversité du réseau

Pour éviter la centralisation du réseau et permettre la détection des attaques Sybil :

- **Pas de dumps NetDb complets**: Ne jamais fournir tous les RouterInfos (descripteurs de router I2P) à un seul client
- **Échantillonnage aléatoire**: Chaque lot contient un sous-ensemble différent des pairs disponibles
- **Taille minimale du lot**: 75 RouterInfos (augmentée par rapport à la valeur initiale de 50)
- **Taille maximale du lot**: 100 RouterInfos
- **Fraîcheur**: Les RouterInfos doivent être récents (dans les 24 heures suivant leur génération)

### Considérations relatives à IPv6

**État actuel** (2025): - Plusieurs serveurs de réensemencement présentent une absence de réponse en IPv6 - Les clients devraient privilégier ou imposer l'IPv4 pour plus de fiabilité - La prise en charge d'IPv6 est recommandée pour les nouveaux déploiements, mais elle n'est pas critique

**Remarque d’implémentation**: Lors de la configuration de serveurs à double pile, assurez-vous que les adresses d’écoute IPv4 et IPv6 fonctionnent correctement, ou désactivez IPv6 s’il ne peut pas être correctement pris en charge.

## Considérations de sécurité

### Modèle de menace

Le protocole de reseed protège contre :

1. **Attaques de l'homme du milieu**: Les signatures RSA-4096 empêchent l'altération des paquets
2. **Partitionnement du réseau**: Plusieurs serveurs de réensemencement indépendants empêchent l'existence d'un point de contrôle unique
3. **Attaques Sybil**: La diversité des paquets limite la capacité de l'attaquant à isoler les utilisateurs
4. **Censure**: Plusieurs serveurs et des méthodes alternatives offrent une redondance

Le protocole de reseed (bootstrap : procédure d’amorçage initiale du réseau I2P) ne protège PAS contre :

1. **Serveurs reseed compromis (serveurs de réensemencement)**: Si un attaquant contrôle les clés privées des certificats de reseed
2. **Blocage complet du réseau**: Si toutes les méthodes de reseed sont bloquées dans une région
3. **Surveillance à long terme**: Les requêtes de reseed révèlent l'adresse IP qui tente de rejoindre I2P

### Gestion des certificats

**Sécurité des clés privées**: - Conservez les clés de signature SU3 hors ligne lorsqu'elles ne sont pas utilisées - Utilisez des mots de passe robustes pour le chiffrement des clés - Maintenez des sauvegardes sécurisées des clés et des certificats - Envisagez des modules matériels de sécurité (HSM) pour les déploiements à forte valeur

**Révocation de certificats**: - Listes de révocation de certificats (CRLs) distribuées via un flux d'actualités - Les certificats compromis peuvent être révoqués par le coordinateur - Routers mettent automatiquement à jour les CRLs avec les mises à jour logicielles

### Atténuation des attaques

**Protection contre les attaques DDoS**: - règles fail2ban pour les requêtes excessives - limitation de débit au niveau du serveur web - limites de connexions par adresse IP - Cloudflare ou un CDN similaire pour une couche supplémentaire

**Prévention du scraping**: - Différents bundles (lots) par adresse IP requérante - Mise en cache temporelle des bundles par adresse IP - Journalisation de motifs indiquant des tentatives de scraping - Coordination avec d'autres opérateurs concernant les attaques détectées

## Tests et validation

### Tester votre serveur de réensemencement

#### Méthode 1 : Installation neuve du Router

1. Installez I2P sur un système vierge
2. Ajoutez votre URL de réensemencement à la configuration
3. Supprimez ou désactivez les autres URL de réensemencement
4. Démarrez le router et surveillez les journaux pour confirmer un réensemencement réussi
5. Vérifiez la connexion au réseau dans les 5 à 10 minutes

Sortie de journal attendue :

```
Reseed got 77 router infos from https://your-reseed.example.com/i2pseeds.su3?netid=2 with 0 errors
Reseed complete, 77 received
```
#### Méthode 2 : validation manuelle de SU3 (format de paquet de mise à jour signé d'I2P)

```bash
# Download bundle
curl -k -A "Wget/1.11.4" https://your-reseed.example.com/i2pseeds.su3 > test.su3

# Verify it's a valid SU3 file
hexdump -C test.su3 | head -n 3
# Should show: 49 32 50 73 75 33 (I2Psu3)

# Extract content (requires su3 tools)
java -cp /path/to/i2p.jar net.i2p.crypto.SU3File verify test.su3 your-cert.crt

# Unzip content
# (Extract content section, skip header+signature, then unzip)
```
#### Méthode 3: surveillance via checki2p

Le service à l’adresse https://checki2p.com/reseed effectue des vérifications automatisées toutes les 4 heures sur tous les serveurs de reseed I2P (reseed : serveur qui fournit les informations initiales du réseau aux nouveaux router I2P) enregistrés. Cela permet :

- Surveillance de la disponibilité
- Métriques du temps de réponse
- Validation des certificats TLS
- Vérification de la signature SU3 (format de paquet de mise à jour d'I2P)
- Données historiques de temps de fonctionnement

Une fois que votre reseed (serveur de réamorçage) est enregistré auprès du projet I2P, il apparaîtra automatiquement sur checki2p dans les 24 heures.

### Dépannage des problèmes courants

**Problème**: "Unable to read signing key" lors du premier lancement - **Solution**: C'est normal. Répondez 'y' pour générer de nouvelles clés.

**Problème**: Le router ne parvient pas à vérifier la signature - **Cause**: Le certificat n'est pas dans le magasin de confiance du router - **Solution**: Placez le certificat dans le répertoire `~/.i2p/certificates/reseed/`

**Problème**: Même bundle livré à différents clients - **Cause**: l’en-tête X-Forwarded-For n’est pas correctement transmis - **Solution**: Activer `--trustProxy` et configurer les en-têtes du proxy inverse

**Problème**: erreurs "Connection refused" - **Cause**: port non accessible depuis Internet - **Solution**: Vérifiez les règles du pare-feu, vérifiez la redirection de port

**Problème**: Utilisation élevée du processeur lors de la reconstruction du bundle - **Cause**: Comportement normal lors de la génération de plus de 350 variantes SU3 (format de fichier de mise à jour d'I2P) - **Solution**: Veillez à disposer de ressources processeur suffisantes, envisagez de réduire la fréquence des reconstructions

## Informations de référence

### Documentation officielle

- **Guide des contributeurs de Reseed (réamorçage)**: /guides/creating-and-running-an-i2p-reseed-server/
- **Exigences de la politique de Reseed**: /guides/reseed-policy/
- **Spécification SU3**: /docs/specs/updates/
- **Dépôt des outils de Reseed**: https://i2pgit.org/idk/reseed-tools
- **Documentation des outils de Reseed**: https://eyedeekay.github.io/reseed-tools/

### Implémentations alternatives

- **PurpleI2P pyseeder**: https://github.com/PurpleI2P/pyseeder
- **DivaExchange i2p-reseed**: https://github.com/diva-exchange/i2p-reseed
- **RTradeLtd i2p-tools-1**: https://github.com/RTradeLtd/i2p-tools-1
- **Reseeder (serveur de réensemencement) WSGI Python**: https://github.com/torbjo/i2p-reseeder

### Ressources communautaires

- **Forum I2P**: https://i2pforum.net/
- **Dépôt Gitea**: https://i2pgit.org/I2P_Developers/i2p.i2p
- **IRC**: #i2p-dev sur IRC2P
- **Surveillance de l'état**: https://checki2p.com/reseed

### Historique des versions

- **0.9.14** (2014): Introduction du format de réensemencement SU3
- **0.9.16** (2014): Ajout du réensemencement basé sur des fichiers
- **0.9.42** (2019): Exigence du paramètre de requête ID de réseau
- **2.0.0** (2022): Introduction du protocole de transport SSU2
- **2.4.0** (2024): Améliorations de l’isolation et de la sécurité de NetDB
- **2.6.0** (2024): Connexions I2P-over-Tor bloquées
- **2.10.0** (2025): Version stable actuelle (en septembre 2025)

### Référence des types de signature

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Type</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:center;">Code</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Algorithm</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Key Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Signature Size</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Hash</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA-SHA1</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">0</td><td style="border:1px solid var(--color-border); padding:0.5rem;">DSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">1024-bit</td><td style="border:1px solid var(--color-border); padding:0.5rem;">40 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-1</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA-SHA256-P256</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">1</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">P-256</td><td style="border:1px solid var(--color-border); padding:0.5rem;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-256</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA-SHA384-P384</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">2</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">P-384</td><td style="border:1px solid var(--color-border); padding:0.5rem;">96 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-384</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA-SHA512-P521</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">3</td><td style="border:1px solid var(--color-border); padding:0.5rem;">ECDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">P-521</td><td style="border:1px solid var(--color-border); padding:0.5rem;">132 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-512</td></tr>
    <tr><td style="border:1px solidvar(--color-border); padding:0.5rem;">RSA-SHA256-2048</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">4</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">2048-bit</td><td style="border:1px solid var(--color-border); padding:0.5rem;">256 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-256</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA-SHA384-3072</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">5</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">3072-bit</td><td style="border:1px solid var(--color-border); padding:0.5rem;">384 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-384</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA-SHA512-4096</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">6</td><td style="border:1px solid var(--color-border); padding:0.5rem;">RSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">4096-bit</td><td style="border:1px solid var(--color-border); padding:0.5rem;">512 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-512</td></tr>
    <tr><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA-SHA512-Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem; text-align:center;">7</td><td style="border:1px solid var(--color-border); padding:0.5rem;">EdDSA</td><td style="border:1px solid var(--color-border); padding:0.5rem;">Ed25519</td><td style="border:1px solid var(--color-border); padding:0.5rem;">64 bytes</td><td style="border:1px solid var(--color-border); padding:0.5rem;">SHA-512</td></tr>
  </tbody>
</table>
**Standard de réensemencement**: Le type 6 (RSA-SHA512-4096) est requis pour les paquets de réensemencement.

## Remerciements

Merci à tous les reseed operator (opérateurs des services d’amorçage du réseau) pour que le réseau reste accessible et résilient. Une reconnaissance particulière aux contributeurs et projets suivants :

- **zzz**: Développeur I2P de longue date et coordinateur du réensemencement
- **idk**: Mainteneur actuel de reseed-tools et responsable des versions
- **Nguyen Phong Hoang**: Recherche sur des stratégies de réensemencement résistantes à la censure
- **PurpleI2P Team**: Implémentations et outils I2P alternatifs
- **checki2p**: Service de surveillance automatisé pour l’infrastructure de réensemencement

L’infrastructure de réensemencement décentralisée du réseau I2P représente un effort collaboratif de la part de dizaines d’opérateurs à travers le monde, garantissant que les nouveaux utilisateurs puissent toujours trouver une voie pour rejoindre le réseau, indépendamment de la censure locale ou des obstacles techniques.
