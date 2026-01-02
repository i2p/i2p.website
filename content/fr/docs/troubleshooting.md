---
title: "Guide de dépannage du router I2P"
description: "Guide de dépannage complet pour les problèmes courants du router I2P, y compris les problèmes de connectivité, de performances et de configuration"
slug: "troubleshooting"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

Les routers I2P rencontrent le plus souvent des problèmes en raison de **problèmes de redirection de port**, d’une **allocation de bande passante insuffisante** et d’un **temps d’amorçage insuffisant**. Ces trois facteurs représentent plus de 70 % des problèmes signalés. Le router nécessite au moins **10 à 15 minutes** après le démarrage pour s’intégrer complètement au réseau, une **bande passante minimale de 128 KB/sec** (256 KB/sec recommandé), et une **redirection de port UDP/TCP** correcte pour atteindre un statut non filtré par pare-feu. Les nouveaux utilisateurs s’attendent souvent à une connectivité immédiate et redémarrent prématurément, ce qui réinitialise la progression de l’intégration et crée un cycle frustrant. Ce guide fournit des solutions détaillées pour tous les principaux problèmes I2P affectant les versions 2.10.0 et ultérieures.

L’architecture d’anonymat d’I2P sacrifie par nature de la vitesse au profit de la confidentialité grâce à des tunnels chiffrés multi-sauts. Comprendre cette conception fondamentale aide les utilisateurs à définir des attentes réalistes et à dépanner efficacement, plutôt que d’interpréter à tort un comportement normal comme des problèmes.

## Le Router ne démarre pas ou plante immédiatement

Les échecs de démarrage les plus courants proviennent de **conflits de ports**, d'**incompatibilité de version de Java** ou de **fichiers de configuration corrompus**. Avant d'approfondir le diagnostic, vérifiez si une autre instance d'I2P est déjà en cours d'exécution.

**Vérifiez l'absence de processus en conflit :**

Linux: `ps aux | grep i2p` ou `netstat -tulpn | grep 7657`

Windows: Gestionnaire des tâches → Détails → recherchez java.exe avec i2p dans la ligne de commande

macOS: Moniteur d’activité → recherchez « i2p »

Si un processus zombie existe, tuez-le : `pkill -9 -f i2p` (Linux/Mac) ou `taskkill /F /IM javaw.exe` (Windows)

**Vérifiez la compatibilité de la version de Java :**

I2P 2.10.0+ nécessite **Java 8 minimum**. Il est recommandé d'utiliser Java 11 ou une version ultérieure. Vérifiez que votre installation affiche "mixed mode" (et non "interpreted mode"):

```bash
java -version
```
Devrait afficher : OpenJDK ou Oracle Java, version 8+, "mixed mode"

**À éviter :** GNU GCJ, implémentations Java obsolètes, modes uniquement interprétés

**Conflits de ports fréquents** surviennent lorsque plusieurs services se disputent les ports par défaut d'I2P. La console du router (nœud I2P) (7657), I2CP (7654), SAM (7656) et le proxy HTTP (4444) doivent être disponibles. Vérifiez la présence de conflits : `netstat -ano | findstr "7657 4444 7654"` (Windows) ou `lsof -i :7657,4444,7654` (Linux/Mac).

**La corruption du fichier de configuration** se manifeste par des plantages immédiats avec des erreurs d'analyse syntaxique dans les journaux. Router.config exige un **encodage UTF-8 sans BOM**, utilise `=` comme séparateur (et non `:`), et interdit certains caractères spéciaux. Sauvegardez puis examinez : `~/.i2p/router.config` (Linux), `%LOCALAPPDATA%\I2P\router.config` (Windows), `~/Library/Application Support/i2p/router.config` (macOS).

Pour réinitialiser la configuration tout en préservant l'identité : Arrêtez I2P, sauvegardez router.keys et le répertoire keyData, supprimez router.config, redémarrez. Le router régénère la configuration par défaut.

**Allocation du heap (tas mémoire) Java trop faible** entraîne des plantages OutOfMemoryError. Modifiez wrapper.config et augmentez `wrapper.java.maxmemory` de la valeur par défaut 128 ou 256 à **512 minimum** (1024 pour les routers à haut débit). Cela nécessite un arrêt complet, attendre 11 minutes, puis un redémarrage - cliquer sur "Restart" dans la console n'appliquera pas la modification.

## Résolution du statut "Network: Firewalled"

Le statut Firewalled (derrière un pare-feu) signifie que le router ne peut pas recevoir de connexions entrantes directes, ce qui oblige à s’appuyer sur des introducers (pairs introducteurs). Bien que le router fonctionne dans cet état, les **performances se dégradent fortement** et la contribution au réseau reste minimale. Pour atteindre un statut non-Firewalled, il faut configurer correctement la redirection de ports.

**Le router sélectionne aléatoirement un port** entre 9000 et 31000 pour les communications. Trouvez votre port à l'adresse http://127.0.0.1:7657/confignet - cherchez "UDP Port" et "TCP Port" (généralement le même numéro). Vous devez rediriger **à la fois UDP et TCP** pour des performances optimales, bien que l'UDP seul permette une fonctionnalité de base.

**Activer la redirection automatique via UPnP** (méthode la plus simple):

1. Accédez à http://127.0.0.1:7657/confignet
2. Cochez "Enable UPnP"
3. Enregistrez les modifications et redémarrez le router
4. Attendez 5-10 minutes et vérifiez que le statut passe de "Network: Firewalled" à "Network: OK"

UPnP nécessite la prise en charge par le router (activée par défaut sur la plupart des routers grand public fabriqués après 2010) et une configuration réseau appropriée.

**Redirection de port manuelle** (requise lorsque l'UPnP échoue):

1. Notez votre port I2P depuis http://127.0.0.1:7657/confignet (p. ex., 22648)
2. Trouvez votre adresse IP locale: `ipconfig` (Windows), `ip addr` (Linux), Préférences Système → Réseau (macOS)
3. Accédez à l'interface d'administration de votre router (généralement 192.168.1.1 ou 192.168.0.1)
4. Accédez à Transfert de port (peut se trouver sous Avancé, NAT ou Serveurs virtuels)
5. Créez deux règles:
   - Port externe: [votre port I2P] → IP interne: [votre ordinateur] → Port interne: [le même] → Protocole: **UDP**
   - Port externe: [votre port I2P] → IP interne: [votre ordinateur] → Port interne: [le même] → Protocole: **TCP**
6. Enregistrez la configuration et redémarrez votre router si nécessaire

**Vérifiez la redirection de port** à l’aide d’outils de test en ligne après la configuration. Si la détection échoue, vérifiez les paramètres du pare-feu - le pare-feu du système ainsi que tout pare-feu d’antivirus doivent autoriser le port I2P.

**Alternative en mode masqué** pour les réseaux restrictifs où la redirection de port est impossible : Activez-la sur http://127.0.0.1:7657/confignet → cochez "Hidden mode". Le router reste derrière un pare-feu mais s’adapte à cet état en utilisant exclusivement des SSU introducers (nœuds introducteurs). Les performances seront réduites, mais cela restera fonctionnel.

## Router bloqué dans les états "Démarrage" ou "Test"

Ces états transitoires durant l’amorçage initial se résolvent généralement en **10-15 minutes pour les nouvelles installations** ou **3-5 minutes pour les routers établis**. Une intervention prématurée aggrave souvent les problèmes.

**"Network: Testing"** indique que le router sonde la joignabilité via différents types de connexions (direct, introducers (nœuds d’introduction), plusieurs versions du protocole). Ceci est normal pendant les 5 à 10 premières minutes après le démarrage. Le router teste plusieurs scénarios afin de déterminer la configuration optimale.

**"Rejecting tunnels: starting up"** apparaît pendant l'amorçage lorsque le router ne dispose pas d'informations suffisantes sur les pairs. Le router ne participera pas au trafic de relais tant qu'il ne sera pas suffisamment intégré. Ce message devrait disparaître au bout de 10 à 20 minutes, une fois que netDb contiendra des informations sur plus de 50 routers.

**Le décalage d’horloge tue les tests de joignabilité.** I2P exige que l’heure système soit à **±60 secondes** de l’heure du réseau. Un écart dépassant 90 secondes entraîne un rejet automatique des connexions. Synchronisez l’horloge de votre système :

Linux: `sudo timedatectl set-ntp true && sudo systemctl restart systemd-timesyncd`

Windows : Panneau de configuration → Date et heure → Heure Internet → Mettre à jour maintenant → Activer la synchronisation automatique

macOS : Préférences Système → Date et heure → Activer "Régler la date et l’heure automatiquement"

Après avoir corrigé le décalage de l’horloge, redémarrez complètement I2P afin d’assurer une intégration correcte.

**Allocation de bande passante insuffisante** empêche la réussite des tests. Le router a besoin d’une capacité adéquate pour construire des tunnels de test. Configurez sur http://127.0.0.1:7657/config:

- **Minimum viable:** Entrant 96 KB/sec, Sortant 64 KB/sec
- **Standard recommandé:** Entrant 256 KB/sec, Sortant 128 KB/sec  
- **Performances optimales:** Entrant 512+ KB/sec, Sortant 256+ KB/sec
- **Pourcentage de partage:** 80 % (permet au router de fournir de la bande passante au réseau)

Une bande passante plus faible peut fonctionner, mais elle fait passer le temps d’intégration de quelques minutes à plusieurs heures.

**netDb corrompue** suite à un arrêt incorrect ou à des erreurs de disque entraîne des boucles de test perpétuelles. Le router ne peut pas terminer les tests sans données de pairs valides:

```bash
# Stop I2P completely
i2prouter stop    # or systemctl stop i2p

# Delete corrupted database (safe - will reseed automatically)
rm -rf ~/.i2p/netDb/*

# Restart and allow 10-15 minutes for reseed
i2prouter start
```
Windows: Supprimez le contenu de `%APPDATA%\I2P\netDb\` ou de `%LOCALAPPDATA%\I2P\netDb\`

**Pare-feu bloquant le réensemencement** empêche l’acquisition des pairs initiaux. Pendant le bootstrap (amorçage), I2P récupère les informations du router depuis des serveurs de réensemencement HTTPS. Les pare-feux d’entreprise ou de FAI peuvent bloquer ces connexions. Configurez le proxy de réensemencement à l’adresse http://127.0.0.1:7657/configreseed si vous opérez derrière des réseaux restrictifs.

## Débits lents, dépassements de délai et échecs de construction de tunnels

La conception d’I2P entraîne intrinsèquement des vitesses **3 à 10 fois plus lentes que sur le clearnet** en raison du chiffrement à plusieurs sauts, de la surcharge des paquets et de l’imprévisibilité du routage. La construction d’un tunnel parcourt plusieurs routers, chacun ajoutant de la latence. Le comprendre évite de prendre un comportement normal pour des problèmes.

**Attentes de performances typiques:**

- Navigation sur les sites .i2p : chargement initial des pages en 10 à 30 secondes, plus rapide après l'établissement du tunnel
- Téléchargement de torrents via I2PSnark : 10-100 Ko/s par torrent, selon le nombre de sources (seeders) et les conditions du réseau  
- Téléchargements de gros fichiers : patience requise - des fichiers de l'ordre du mégaoctet peuvent prendre des minutes, ceux de l'ordre du gigaoctet des heures
- Première connexion la plus lente : la construction du tunnel prend 30-90 secondes ; les connexions suivantes utilisent les tunnels existants

**Taux de réussite d'établissement de tunnel** indique l'état de santé du réseau. Consultez http://127.0.0.1:7657/tunnels:

- **Supérieur à 60 % :** Fonctionnement normal et sain
- **40-60 % :** Marginal, envisager d’augmenter la bande passante ou de réduire la charge
- **Inférieur à 40 % :** Problématique - indique une bande passante insuffisante, des problèmes de réseau ou une sélection de pairs médiocre

**Augmentez l’allocation de bande passante** comme première optimisation. La plupart des lenteurs proviennent d’un manque de bande passante. À l’adresse http://127.0.0.1:7657/config, augmentez les limites progressivement et surveillez les graphiques à l’adresse http://127.0.0.1:7657/graphs.

**Pour DSL/Câble (connexions de 1 à 10 Mbps):** - Entrant: 400 Ko/s - Sortant: 200 Ko/s - Partage: 80% - Mémoire: 384 Mo (modifier wrapper.config)

**Pour les connexions haut débit (10-100+ Mbps):** - Entrant: 1500 KB/sec   - Sortant: 1000 KB/sec - Partage: 80-100% - Mémoire: 512-1024 MB - À envisager: augmenter le nombre de tunnels participants à 2000-5000 à http://127.0.0.1:7657/configadvanced

**Optimisez la configuration des tunnels** pour de meilleures performances. Accédez aux paramètres spécifiques des tunnels à l’adresse http://127.0.0.1:7657/i2ptunnel et modifiez chaque tunnel :

- **Quantité de tunnel:** Augmenter de 2 à 3-4 (plus de chemins disponibles)
- **Quantité de secours:** Régler sur 1-2 (basculement rapide si un tunnel tombe en panne)
- **Longueur de tunnel:** 3 sauts par défaut offrent un bon équilibre; réduire à 2 améliore la vitesse mais diminue l’anonymat

**La bibliothèque cryptographique native (jbigi)** offre des performances 5 à 10 fois supérieures à celles du chiffrement Java pur. Vérifiez qu’elle est chargée sur http://127.0.0.1:7657/logs - recherchez "jbigi loaded successfully" ou "Using native CPUID implementation". Si rien n’apparaît :

Linux: Généralement détecté automatiquement et chargé depuis ~/.i2p/jbigi-*.so Windows: Vérifiez la présence de jbigi.dll dans le répertoire d'installation d'I2P S'il manque: Installez les outils de compilation et compilez à partir des sources, ou téléchargez des binaires précompilés depuis les dépôts officiels

**Maintenez le router en fonctionnement en continu.** Chaque redémarrage réinitialise l'intégration et nécessite 30 à 60 minutes pour reconstruire le réseau de tunnels et les relations avec les pairs. Les routers stables à haute disponibilité bénéficient d'une sélection préférentielle pour la construction de tunnels, créant une boucle de rétroaction positive sur les performances.

## Utilisation élevée du processeur et de la mémoire

Une utilisation excessive des ressources indique généralement une **allocation mémoire insuffisante**, des **bibliothèques cryptographiques natives manquantes**, ou un **engagement excessif dans la participation au réseau**. Les routers bien configurés devraient consommer 10-30 % de CPU lors d’une utilisation active et maintenir une utilisation mémoire stable en dessous de 80 % du heap (tas mémoire) alloué.

**Les problèmes de mémoire se manifestent par :** - Graphiques de mémoire à plateau (bloqués au maximum) - Collecte de mémoire (ramasse-miettes) fréquente (profil en dents de scie avec chutes abruptes) - OutOfMemoryError dans les journaux - Le router devient non réactif sous charge - Arrêt automatique dû à l'épuisement des ressources

**Augmenter l’allocation du tas Java** dans wrapper.config (nécessite un arrêt complet) :

```bash
# Linux: ~/.i2p/wrapper.config
# Windows: %APPDATA%\I2P\wrapper.config  
# Find and modify:
wrapper.java.maxmemory=512

# Recommendations by usage:
# Light browsing only: 256
# Standard use (browsing + light torrenting): 512
# Heavy use (multiple applications, active torrenting): 768-1024
# Floodfill or very high bandwidth: 1024-2048
```
**Critique :** Après avoir modifié wrapper.config, vous devez arrêter complètement (et non redémarrer), attendre 11 minutes pour un arrêt en douceur, puis démarrer à nouveau. Le bouton "Restart" de la console du router ne recharge pas les paramètres de wrapper.config.

**L'optimisation du CPU nécessite une bibliothèque de chiffrement native.** Les opérations BigInteger en Java pur consomment 10 à 20 fois plus de CPU que les implémentations natives. Vérifiez l'état de jbigi à http://127.0.0.1:7657/logs au démarrage. Sans jbigi, l'utilisation du CPU grimpera à 50-100% pendant la construction de tunnels et les opérations de chiffrement.

**Réduire la charge des tunnels participants** si le router est surchargé:

1. Accédez à http://127.0.0.1:7657/configadvanced
2. Définissez `router.maxParticipatingTunnels=1000` (valeur par défaut 8000)
3. Réduisez le pourcentage de partage à http://127.0.0.1:7657/config de 80 % à 50 %
4. Désactivez le mode floodfill si activé : `router.floodfillParticipant=false`

**Limitez la bande passante d’I2PSnark et le nombre de torrents simultanés.** Le téléchargement par torrent consomme des ressources importantes. À http://127.0.0.1:7657/i2psnark:

- Limiter les torrents actifs à 3-5 maximum
- Définir "Up BW Limit" et "Down BW Limit" à des valeurs raisonnables (50-100 KB/sec chacune)
- Arrêter les torrents lorsqu'ils ne sont pas activement nécessaires
- Éviter de partager des dizaines de torrents simultanément

**Surveillez l'utilisation des ressources** au moyen des graphiques intégrés à l'adresse http://127.0.0.1:7657/graphs. La mémoire devrait indiquer une marge disponible, pas un plafonnement. Les pics du CPU pendant la construction de tunnel sont normaux ; une utilisation du CPU durablement élevée indique des problèmes de configuration.

**Pour les systèmes très limités en ressources** (Raspberry Pi, matériel ancien), envisagez **i2pd** (implémentation en C++) comme alternative. i2pd nécessite ~130 Mo de RAM contre 350+ Mo pour Java I2P, et utilise ~7% de CPU contre 70% dans des conditions de charge similaires. Notez qu’i2pd n’inclut pas d’applications intégrées et nécessite des outils externes.

## Problèmes de torrent avec I2PSnark

L'intégration d'I2PSnark avec l'architecture du router I2P nécessite de comprendre que **l'activité BitTorrent dépend entièrement de la santé des tunnels du router**. Les torrents ne démarrent pas tant que le router n'a pas atteint une intégration suffisante avec 10+ pairs actifs et des tunnels fonctionnels.

**Les torrents bloqués à 0 % indiquent généralement :**

1. **Router pas encore pleinement intégré :** Patientez 10-15 minutes après le démarrage d’I2P avant d’espérer une activité torrent
2. **DHT désactivée :** Activez-la sur http://127.0.0.1:7657/i2psnark → Configuration → cochez "Enable DHT" (activée par défaut depuis la version 0.9.2)
3. **Trackers invalides ou inactifs :** Les torrents I2P requièrent des trackers spécifiques à I2P - les trackers du clearnet (Internet public) ne fonctionneront pas
4. **Configuration de tunnel insuffisante :** Augmentez le nombre de tunnels dans I2PSnark Configuration → section Tunnels

**Configurez les tunnels I2PSnark pour de meilleures performances:**

- Tunnels entrants: 3-5 (par défaut: 2 pour Java I2P, 5 pour i2pd)
- Tunnels sortants: 3-5  
- Longueur du tunnel: 3 sauts (réduire à 2 pour plus de vitesse, moins d'anonymat)
- Quantité de tunnels: 3 (offre des performances constantes)

**Trackers torrent I2P essentiels** à inclure : - tracker2.postman.i2p (principal, le plus fiable) - w7tpbzncbcocrqtwwm3nezhnnsw4ozadvi2hmvzdhrqzfxfum7wa.b32.i2p/a

Supprimez tous les trackers clearnet (non-.i2p) : ils n’apportent aucun bénéfice et provoquent des tentatives de connexion qui expirent (timeout, dépassement de délai).

**Erreurs "Torrent not registered"** surviennent lorsque la communication avec le tracker échoue. Clic droit sur le torrent → "Start" force une nouvelle annonce. Si le problème persiste, vérifiez l’accessibilité du tracker en accédant à http://tracker2.postman.i2p dans un navigateur configuré pour I2P. Les trackers hors service doivent être remplacés par des alternatives fonctionnelles.

**Aucun pair ne se connecte** malgré le succès du tracker suggère : - Router derrière un pare-feu (la redirection de ports améliore la situation, mais n'est pas obligatoire) - Bande passante insuffisante (augmenter à 256+ Ko/s)   - Essaim trop petit (certains torrents n'ont que 1-2 sources complètes; patience requise) - DHT désactivé (à activer pour la découverte de pairs sans tracker)

**Activez DHT et PEX (Peer Exchange)** dans la configuration d’I2PSnark. DHT permet de trouver des pairs sans dépendre d’un tracker. PEX découvre des pairs à partir des pairs connectés, ce qui accélère la découverte de l’essaim.

**Corruption des fichiers téléchargés** survient rarement avec la vérification d'intégrité intégrée d'I2PSnark. Si elle est détectée:

1. Clic droit sur le torrent → "Check" force le recalcul du hachage de toutes les pièces
2. Supprimez les données du torrent corrompues (conserve le fichier .torrent)  
3. Clic droit → "Start" pour retélécharger avec vérification des pièces
4. Si la corruption persiste, vérifiez le disque pour détecter des erreurs : `chkdsk` (Windows), `fsck` (Linux)

**Le répertoire surveillé ne fonctionne pas** nécessite une configuration appropriée :

1. Configuration d'I2PSnark → "Watch directory" : Définissez un chemin absolu (par ex., `/home/user/torrents/watch`)
2. Assurez-vous que le processus I2P dispose des permissions de lecture : `chmod 755 /path/to/watch`
3. Placez les fichiers .torrent dans le répertoire de surveillance - I2PSnark les ajoute automatiquement
4. Configurez "Auto start" : Indiquez si les torrents doivent démarrer immédiatement lors de leur ajout

**Optimisation des performances pour le torrenting (utilisation de BitTorrent):**

- Limitez le nombre de torrents actifs simultanés : 3 à 5 maximum pour les connexions standard
- Priorisez les téléchargements importants : arrêtez temporairement les torrents de faible priorité
- Augmentez l’allocation de bande passante du router : plus de bande passante = de meilleures performances pour les torrents
- Soyez patient : le torrent via I2P est par nature plus lent que BitTorrent sur le clearnet
- Continuez à partager après le téléchargement : le réseau repose sur la réciprocité

## Configuration et dépannage de Git via I2P

Les opérations Git via I2P nécessitent soit une **configuration du proxy SOCKS**, soit des **tunnels I2P dédiés** pour l'accès SSH/HTTP. La conception de Git suppose des connexions à faible latence, ce qui rend l'architecture à forte latence d'I2P problématique.

**Configurer Git pour utiliser le proxy SOCKS d'I2P :**

Modifiez ~/.ssh/config (créez-le s'il n'existe pas) :

```
Host *.i2p
    ProxyCommand nc -X 5 -x 127.0.0.1:4447 %h %p
    ServerAliveInterval 60
    ServerAliveCountMax 3
    Compression yes
```
Cette configuration achemine toutes les connexions SSH vers les hôtes .i2p via le proxy SOCKS d'I2P (port 4447). Les paramètres ServerAlive maintiennent la connexion pendant la latence d'I2P.

Pour les opérations Git via HTTP/HTTPS, configurez Git au niveau global :

```bash
git config --global http.proxy socks5h://127.0.0.1:4447
git config --global https.proxy socks5h://127.0.0.1:4447
```
Remarque : `socks5h` effectue la résolution DNS via le proxy - indispensable pour les domaines .i2p.

**Créer un tunnel I2P dédié pour Git via SSH** (plus fiable que SOCKS):

1. Accédez à http://127.0.0.1:7657/i2ptunnel
2. "Nouveau tunnel client" → "Standard"
3. Configurer:
   - Nom: Git-SSH  
   - Type: Client
   - Port: 2222 (port local pour l'accès Git)
   - Destination: [your-git-server].i2p:22
   - Démarrage automatique: Activé
   - Nombre de tunnels: 3-4 (plus élevé pour une meilleure fiabilité)
4. Enregistrez et démarrez le tunnel
5. Configurez SSH pour utiliser le tunnel: `ssh -p 2222 git@127.0.0.1`

**Erreurs d’authentification SSH** via I2P sont généralement dues à :

- Clé non ajoutée à ssh-agent : `ssh-add ~/.ssh/id_rsa`
- Mauvaises permissions du fichier de clé : `chmod 600 ~/.ssh/id_rsa`
- Tunnel non démarré : vérifiez sur http://127.0.0.1:7657/i2ptunnel que le statut est vert
- Le serveur Git exige un type de clé spécifique : générez une clé ed25519 si RSA échoue

**Le dépassement de délai des opérations Git** est lié aux caractéristiques de latence d'I2P:

- Augmenter le délai d'expiration Git: `git config --global http.postBuffer 524288000` (tampon de 500 Mo)
- Augmenter le seuil de basse vitesse: `git config --global http.lowSpeedLimit 1000` et `git config --global http.lowSpeedTime 600` (patiente 10 minutes)
- Utiliser un clone superficiel pour la récupération initiale: `git clone --depth 1 [url]` (récupère uniquement le dernier commit, plus rapide)
- Cloner pendant les périodes de faible activité: La congestion du réseau affecte les performances d'I2P

**Opérations git clone/fetch lentes** sont inhérentes à l'architecture d'I2P. Un dépôt de 100 Mo peut prendre 30 à 60 minutes sur I2P, contre quelques secondes sur le clearnet. Stratégies:

- Utilisez des clones superficiels : `--depth 1` réduit considérablement le transfert de données initial
- Récupérez de manière incrémentielle : Au lieu d’un clone complet, récupérez des branches spécifiques : `git fetch origin branch:branch`
- Envisagez rsync via I2P : Pour des dépôts très volumineux, rsync peut offrir de meilleures performances
- Augmentez le nombre de tunnels : Plus de tunnels offrent un meilleur débit pour des transferts volumineux soutenus

**Les erreurs "Connection refused"** indiquent une mauvaise configuration des tunnels:

1. Vérifiez que le router I2P fonctionne: Consultez http://127.0.0.1:7657
2. Confirmez que le tunnel est actif et vert sur http://127.0.0.1:7657/i2ptunnel
3. Testez le tunnel: `nc -zv 127.0.0.1 2222` (devrait se connecter si le tunnel fonctionne)
4. Vérifiez que la destination est joignable: Accédez à l'interface HTTP de la destination si disponible
5. Consultez les journaux du tunnel sur http://127.0.0.1:7657/logs pour des erreurs spécifiques

**Bonnes pratiques pour Git via I2P:**

- Maintenez le router I2P en fonctionnement en continu pour un accès Git stable
- Utilisez des clés SSH plutôt que l’authentification par mot de passe (moins d’invites interactives)
- Configurez des tunnels persistants plutôt que des connexions SOCKS éphémères
- Envisagez d’héberger votre propre serveur Git I2P pour un meilleur contrôle
- Documentez vos points de terminaison Git en .i2p pour les collaborateurs

## Accès aux eepsites et résolution des noms de domaine .i2p

La raison la plus fréquente pour laquelle les utilisateurs ne parviennent pas à accéder aux sites .i2p est une **configuration incorrecte du proxy du navigateur**. Les sites I2P existent uniquement au sein du réseau I2P et nécessitent un acheminement via le proxy HTTP d'I2P.

**Configurez exactement les paramètres de proxy du navigateur :**

**Firefox (recommandé pour I2P):**

1. Menu → Paramètres → Paramètres réseau → bouton Paramètres
2. Sélectionnez "Configuration manuelle du proxy"
3. Proxy HTTP: **127.0.0.1** Port: **4444**
4. Proxy SSL: **127.0.0.1** Port: **4444**  
5. Proxy SOCKS: **127.0.0.1** Port: **4447** (optionnel, pour les applications SOCKS)
6. Cochez "Proxy DNS lors de l'utilisation de SOCKS v5"
7. OK pour enregistrer

**Paramètres critiques d'about:config de Firefox:**

Accédez à `about:config` et modifiez :

- `media.peerconnection.ice.proxy_only` = **true** (empêche les fuites d’adresse IP via WebRTC)
- `keyword.enabled` = **false** (empêche les adresses .i2p d’être redirigées vers les moteurs de recherche)
- `network.proxy.socks_remote_dns` = **true** (DNS via le proxy)

**Limitations de Chrome/Chromium :**

Chrome utilise les paramètres proxy du système plutôt que des paramètres spécifiques à l'application. Sous Windows : Paramètres → recherchez "proxy" → "Ouvrir les paramètres proxy de votre ordinateur" → Configurez HTTP : 127.0.0.1:4444 et HTTPS : 127.0.0.1:4445.

Meilleure approche : utilisez les extensions FoxyProxy ou Proxy SwitchyOmega pour un routage sélectif du trafic .i2p.

**Erreurs "Website Not Found In Address Book"** signifient que le router ne dispose pas de l'adresse cryptographique du domaine .i2p. I2P utilise des carnets d'adresses locaux plutôt qu’un DNS centralisé. Solutions :

**Méthode 1 : Utiliser des services de saut** (le plus simple pour les nouveaux sites) :

Accédez à http://stats.i2p et recherchez le site. Cliquez sur le lien addresshelper : `http://example.i2p/?i2paddresshelper=base64destination`. Votre navigateur affiche "Enregistrer dans le carnet d'adresses ?" - confirmez pour l'ajouter.

**Méthode 2: Mettre à jour les abonnements du carnet d'adresses:**

1. Accédez à http://127.0.0.1:7657/dns (SusiDNS)
2. Cliquez sur l'onglet "Subscriptions"  
3. Vérifiez les abonnements actifs (par défaut : http://i2p-projekt.i2p/hosts.txt)
4. Ajoutez les abonnements recommandés :
   - http://stats.i2p/cgi-bin/newhosts.txt
   - http://notbob.i2p/hosts.txt
   - http://reg.i2p/export/hosts.txt
5. Cliquez sur "Update Now" pour forcer la mise à jour immédiate des abonnements
6. Attendez 5 à 10 minutes pour le traitement

**Méthode 3: Utiliser des adresses en base32** (fonctionne toujours si le site est en ligne):

Chaque site .i2p possède une adresse Base32 : 52 caractères aléatoires suivis de .b32.i2p (par ex., `ukeu3k5oycgaauneqgtnvselmt4yemvoilkln7jpvamvfx7dnkdq.b32.i2p`). Les adresses Base32 contournent le carnet d’adresses - le router effectue une recherche cryptographique directe.

**Erreurs courantes de configuration du navigateur :**

- Tentative d’HTTPS sur des sites uniquement HTTP : La plupart des sites .i2p n’utilisent que HTTP - essayer `https://example.i2p` échoue
- Oubli du préfixe `http://` : Le navigateur peut lancer une recherche au lieu de se connecter - utilisez toujours `http://example.i2p`
- WebRTC activé : Peut divulguer l’adresse IP réelle - désactivez-le via les paramètres de Firefox ou des extensions
- DNS non passé par le proxy : Le DNS du Clearnet (Internet public/clair) ne peut pas résoudre .i2p - il faut acheminer les requêtes DNS via un proxy
- Mauvais port de proxy : 4444 pour HTTP (et non 4445, qui est un outproxy (proxy sortant) HTTPS vers le clearnet)

**Router non entièrement intégré** empêche l'accès à tous les sites. Vérifiez que l'intégration est suffisante :

1. Vérifiez que http://127.0.0.1:7657 affiche "Network: OK" ou "Network: Firewalled" (et non "Network: Testing")
2. Active peers affiche au minimum 10 (50+ optimal)  
3. Aucun message "Rejecting tunnels: starting up"
4. Attendez 10 à 15 minutes complètes après le démarrage du router avant d'espérer un accès .i2p

**La configuration des clients IRC et de messagerie** suit des schémas de proxy similaires :

**IRC:** Les clients se connectent à **127.0.0.1:6668** (le tunnel proxy IRC d'I2P). Désactivez les paramètres de proxy du client IRC - la connexion à localhost:6668 passe déjà par I2P.

**E-mail (Postman):**  - SMTP: **127.0.0.1:7659** - POP3: **127.0.0.1:7660**   - Pas de SSL/TLS (le chiffrement est assuré par le tunnel I2P) - Identifiants issus de l'inscription du compte sur postman.i2p

Tous ces tunnels doivent afficher le statut "running" (vert) sur http://127.0.0.1:7657/i2ptunnel.

## Échecs d’installation et problèmes de paquets

Les installations basées sur des paquets (Debian, Ubuntu, Arch) échouent parfois en raison de **modifications des dépôts**, **d’expiration de la clé GPG**, ou de **conflits de dépendances**. Les dépôts officiels sont passés de deb.i2p2.de/deb.i2p2.no (fin de vie) à **deb.i2p.net** dans les versions récentes.

**Mettre à jour le dépôt Debian/Ubuntu vers la version actuelle :**

```bash
# Remove old repository entries
sudo rm /etc/apt/sources.list.d/i2p.list

# Add current repository
echo "deb [signed-by=/usr/share/keyrings/i2p-archive-keyring.gpg] https://deb.i2p.net/ $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/i2p.list

# Download and install current signing key
curl -o i2p-archive-keyring.gpg https://geti2p.net/_static/i2p-archive-keyring.gpg
sudo cp i2p-archive-keyring.gpg /usr/share/keyrings/

# Update and install
sudo apt update
sudo apt install i2p i2p-keyring
```
**Les échecs de vérification des signatures GPG** surviennent lorsque les clés du dépôt expirent ou changent :

```bash
# Error: "The following signatures were invalid"
# Solution: Install current keyring package
sudo apt install i2p-keyring

# Manual key import if package unavailable
wget https://geti2p.net/_static/i2p-debian-repo.key.asc
sudo apt-key add i2p-debian-repo.key.asc
```
**Le service ne démarre pas après l'installation du paquet** provient le plus souvent de problèmes liés au profil AppArmor sur Debian/Ubuntu :

```bash
# Check service status
sudo systemctl status i2p.service

# Common error: "Failed at step APPARMOR spawning"
# Solution: Reconfigure without AppArmor
sudo dpkg-reconfigure -plow i2p
# Select "No" for AppArmor when prompted

# Alternative: Set profile to complain mode
sudo aa-complain /usr/sbin/wrapper

# Check logs for specific errors  
sudo journalctl -xe -u i2p.service
```
**Problèmes d’autorisations** avec I2P installé via un paquet:

```bash
# Fix ownership (package install uses 'i2psvc' user)
sudo chown -R i2psvc:i2psvc /var/lib/i2p /var/log/i2p /run/i2p
sudo chmod 750 /var/log/i2p /var/lib/i2p

# Set file descriptor limits (add to /etc/security/limits.conf)
i2psvc soft nofile 4096  
i2psvc hard nofile 8192
```
**Problèmes de compatibilité Java:**

I2P 2.10.0 nécessite **Java 8 au minimum**. Les systèmes plus anciens peuvent avoir Java 7 ou une version antérieure :

```bash
# Check Java version
java -version

# Install appropriate Java (Debian/Ubuntu)
sudo apt install openjdk-11-jre-headless

# Set default Java if multiple versions installed
sudo update-alternatives --config java
```
**Erreurs de configuration du Wrapper** empêchent le démarrage du service:

L'emplacement de Wrapper.config varie selon la méthode d'installation : - Installation utilisateur : `~/.i2p/wrapper.config` - Installation via paquet : `/etc/i2p/wrapper.config` ou `/var/lib/i2p/wrapper.config`

Problèmes courants avec wrapper.config:

- Chemins incorrects : `wrapper.java.command` doit pointer vers une installation Java valide
- Mémoire insuffisante : `wrapper.java.maxmemory` est réglé trop bas (augmentez à 512 ou plus)
- Mauvais emplacement du pidfile : `wrapper.pidfile` doit être un emplacement accessible en écriture
- Binaire wrapper manquant : certaines plateformes n'ont pas de wrapper précompilé (utilisez runplain.sh comme solution de repli)

**Échecs de mise à jour et mises à jour corrompues :**

Les mises à jour de la console du router échouent parfois en cours de téléchargement en raison d’interruptions du réseau. Procédure de mise à jour manuelle :

1. Téléchargez i2pupdate_X.X.X.zip depuis https://geti2p.net/en/download
2. Vérifiez que la somme de contrôle SHA256 correspond au hachage publié
3. Copiez dans le répertoire d'installation d'I2P sous le nom `i2pupdate.zip`
4. Redémarrez le router (nœud I2P) - détecte et extrait automatiquement la mise à jour
5. Attendez 5 à 10 minutes pour l'installation de la mise à jour
6. Vérifiez la nouvelle version à l'adresse http://127.0.0.1:7657

**Migration depuis des versions très anciennes** (pré-0.9.47) vers les versions actuelles peut échouer en raison de clés de signature incompatibles ou de fonctionnalités supprimées. Des mises à jour incrémentielles sont nécessaires :

- Versions antérieures à 0.9.9: Impossible de vérifier les signatures actuelles - mise à jour manuelle nécessaire
- Versions utilisant Java 6/7: Java doit être mis à niveau avant la mise à jour d'I2P vers la 2.x
- Sauts de version majeurs: Mettre à jour d'abord vers une version intermédiaire (0.9.47 recommandée comme jalon)

**Quand utiliser l’installateur vs le paquet :**

- **Paquets (apt/yum):** Idéal pour les serveurs, mises à jour de sécurité automatiques, intégration au système, gestion par systemd
- **Installeur (.jar):** Idéal pour une installation au niveau utilisateur, Windows, macOS, installations personnalisées, disponibilité de la version la plus récente

## Corruption des fichiers de configuration et récupération

La persistance de la configuration d'I2P repose sur plusieurs fichiers essentiels. La corruption résulte généralement d'un **arrêt incorrect**, d'**erreurs de disque**, ou d'**erreurs de modification manuelle**. Comprendre la finalité des fichiers permet une réparation ciblée plutôt qu'une réinstallation complète.

**Fichiers critiques et leurs fonctions:**

- **router.keys** (516+ octets) : Identité cryptographique du router - la perte de ce fichier crée une nouvelle identité
- **router.info** (généré automatiquement) : Informations publiées du router - peut être supprimé sans risque, se régénère  
- **router.config** (texte) : Configuration principale - bande passante, paramètres réseau, préférences
- **i2ptunnel.config** (texte) : Définitions de tunnel - tunnels client/serveur, clés, destinations
- **netDb/** (répertoire) : Base de données des pairs - informations de router pour les participants du réseau
- **peerProfiles/** (répertoire) : Statistiques de performance sur les pairs - influencent la sélection des tunnels
- **keyData/** (répertoire) : Clés de destination pour les eepsites et les services - les perdre change les adresses
- **addressbook/** (répertoire) : Correspondances locales de noms d’hôte .i2p

**Procédure de sauvegarde complète** avant toute modification:

```bash
# Stop I2P first
i2prouter stop  # or: systemctl stop i2p

# Backup directory
BACKUP_DIR=~/i2p-backup-$(date +%Y%m%d-%H%M)
mkdir -p $BACKUP_DIR

# Copy critical files
cp -r ~/.i2p/router.keys $BACKUP_DIR/
cp -r ~/.i2p/*.config $BACKUP_DIR/
cp -r ~/.i2p/keyData $BACKUP_DIR/
cp -r ~/.i2p/addressbook $BACKUP_DIR/
cp -r ~/.i2p/eepsite $BACKUP_DIR/  # if hosting sites

# Optional but recommended
tar -czf $BACKUP_DIR.tar.gz $BACKUP_DIR
```
**Symptômes de corruption de Router.config:**

- Le Router ne démarre pas avec des erreurs d'analyse dans les journaux
- Les paramètres ne persistent pas après le redémarrage
- Des valeurs par défaut inattendues apparaissent  
- Caractères illisibles lors de l'affichage du fichier

**Réparer un router.config corrompu:**

1. Sauvegardez l'existant : `cp router.config router.config.broken`
2. Vérifiez l'encodage du fichier : Doit être UTF-8 sans BOM
3. Validez la syntaxe : Les clés utilisent le séparateur `=` (pas `:`), pas d'espaces en fin de clé, `#` uniquement pour les commentaires
4. Corruptions courantes : Caractères non-ASCII dans les valeurs, problèmes de fin de ligne (CRLF vs LF)
5. Si irréparable : Supprimez router.config - le router génère une configuration par défaut, en préservant l'identité

**Paramètres essentiels de router.config à conserver :**

```properties
i2np.bandwidth.inboundKBytesPerSecond=512
i2np.bandwidth.outboundKBytesPerSecond=256
router.updatePolicy=notify
routerconsole.lang=en
router.hiddenMode=false
```
**Un router.keys perdu ou invalide** crée une nouvelle identité du router. C'est acceptable, sauf si :

- Fonctionnement en floodfill (perd le statut floodfill)
- Hébergement d'eepsites avec une adresse publiée (perd la continuité)  
- Réputation établie sur le réseau

Récupération impossible sans sauvegarde — créez-en une nouvelle : supprimez router.keys, redémarrez I2P ; une nouvelle identité sera créée.

**Distinction cruciale:** router.keys (identité) vs keyData/* (services). La perte de router.keys modifie l'identité du router. La perte de keyData/mysite-keys.dat change l'adresse .i2p de votre eepsite (site I2P) - catastrophique si l'adresse est publiée.

**Sauvegardez les clés de l'eepsite/du service séparément:**

```bash
# Identify your service keys
ls -la ~/.i2p/keyData/

# Backup with descriptive names  
cp ~/.i2p/keyData/myservice-keys.dat ~/backups/myservice-keys-$(date +%Y%m%d).dat

# Store securely (encrypted if sensitive)
gpg -c ~/backups/myservice-keys-*.dat
```
**Corruption de NetDb et de peerProfiles:**

Symptômes : aucun pair actif, impossible de construire des tunnels, "Database corruption detected" dans les journaux

Correctif sans risque (tout sera reseed (réensemencé)/reconstruit automatiquement):

```bash
i2prouter stop
rm -rf ~/.i2p/netDb/*
rm -rf ~/.i2p/peerProfiles/*
i2prouter start
# Wait 10-15 minutes for reseed and integration
```
Ces répertoires ne contiennent que des informations réseau mises en cache - leur suppression force un nouvel amorçage mais n'entraîne aucune perte de données critiques.

**Stratégies de prévention:**

1. **Arrêt propre systématique:** Utilisez `i2prouter stop` ou le bouton "Shutdown" de la console du router - ne forcez jamais l’arrêt
2. **Sauvegardes automatisées:** Tâche cron hebdomadaire de sauvegarde de ~/.i2p vers un disque séparé
3. **Surveillance de l’état des disques:** Vérifiez périodiquement l’état SMART - des disques défaillants corrompent les données
4. **Espace disque suffisant:** Maintenez plus de 1 Go libres - des disques pleins entraînent une corruption
5. **UPS (onduleur) recommandé:** Les coupures de courant pendant les écritures corrompent les fichiers
6. **Contrôle de version des configurations critiques:** Un dépôt Git pour router.config et i2ptunnel.config permet de revenir en arrière

**Les permissions de fichiers sont importantes:**

```bash
# Correct permissions (user install)
chmod 600 ~/.i2p/router.keys
chmod 600 ~/.i2p/*.config  
chmod 700 ~/.i2p/keyData
chmod 755 ~/.i2p

# Never run as root - creates permission problems
```
## Messages d’erreur courants décryptés

La journalisation d'I2P fournit des messages d'erreur spécifiques qui ciblent précisément les problèmes. Comprendre ces messages accélère le dépannage.

**"No tunnels available"** apparaît lorsque le router n'a pas établi suffisamment de tunnels pour fonctionner. C'est normal pendant les 5 à 10 premières minutes après le démarrage. Si cela persiste au-delà de 15 minutes:

1. Vérifiez que le nombre de pairs actifs > 10 à l’adresse http://127.0.0.1:7657
2. Vérifiez que l’allocation de bande passante est suffisante (128+ Ko/s minimum)
3. Examinez le taux de réussite des tunnels (chaînes de relais chiffrées I2P) à http://127.0.0.1:7657/tunnels (devrait être >40 %)
4. Passez en revue les journaux pour connaître les motifs de rejet lors de la construction des tunnels

**"Décalage d'horloge détecté"** ou **"code de déconnexion NTCP2 7"** indique que l'heure du système diffère du consensus du réseau de plus de 90 secondes. I2P exige **une précision de ±60 secondes**. Les connexions avec des routers présentant un décalage horaire sont automatiquement rejetées.

À corriger immédiatement :

```bash
# Linux  
sudo timedatectl set-ntp true
sudo systemctl restart systemd-timesyncd
date  # Verify correct time

# Windows
# Control Panel → Date and Time → Internet Time → Update now

# Verify after sync
http://127.0.0.1:7657/logs  # Should no longer show clock skew warnings
```
**"Build timeout"** ou **"Tunnel build timeout exceeded"** signifie que la construction du tunnel via la chaîne de pairs ne s'est pas terminée dans la fenêtre de délai d'expiration (généralement 60 secondes). Causes :

- **Pairs lents:** Le router a sélectionné des participants non réactifs pour le tunnel
- **Congestion du réseau:** Le réseau I2P subit une forte charge
- **Bande passante insuffisante:** Vos limites de bande passante empêchent la construction du tunnel en temps voulu
- **Router surchargé:** Trop de tunnels participants consomment des ressources

Solutions: Augmenter la bande passante, réduire le nombre de tunnels participants (`router.maxParticipatingTunnels` à http://127.0.0.1:7657/configadvanced), activer la redirection de port pour une meilleure sélection des pairs.

**"Router is shutting down"** ou **"Graceful shutdown in progress"** s'affichent lors d'un arrêt normal ou d'une récupération après un crash. Un arrêt propre peut prendre **jusqu'à 10 minutes** pendant que le router ferme les tunnels, notifie ses pairs et sauvegarde son état.

Si l'état d'arrêt persiste au-delà de 11 minutes, forcer l'arrêt :

```bash
# Linux  
kill -9 $(pgrep -f i2p)

# Windows
taskkill /F /IM javaw.exe
```
**"java.lang.OutOfMemoryError: Java heap space"** indique un épuisement du tas mémoire. Solutions immédiates :

1. Modifiez wrapper.config: `wrapper.java.maxmemory=512` (ou plus)
2. **Arrêt complet requis** - un redémarrage n'appliquera pas la modification
3. Attendez 11 minutes pour un arrêt complet  
4. Démarrez le router à neuf
5. Vérifiez l’allocation mémoire à l’adresse http://127.0.0.1:7657/graphs - cela devrait montrer une marge libre

**Erreurs de mémoire associées:**

- **"GC overhead limit exceeded":** Trop de temps passé dans la collecte de mémoire - augmenter la taille du tas
- **"Metaspace":** Espace des métadonnées des classes Java épuisé - ajouter `wrapper.java.additional.X=-XX:MaxMetaspaceSize=256M`

**Spécifique à Windows :** Kaspersky Antivirus limite le tas Java à 512 Mo, indépendamment des paramètres de wrapper.config - désinstallez-le ou ajoutez I2P aux exclusions.

**"Délai d’attente de connexion expiré"** ou **"Erreur I2CP - port 7654"** lorsque des applications tentent de se connecter au router :

1. Vérifiez que le router fonctionne : http://127.0.0.1:7657 devrait répondre
2. Vérifiez le port I2CP : `netstat -an | grep 7654` devrait afficher LISTENING
3. Assurez-vous que le pare-feu localhost autorise : `sudo ufw allow from 127.0.0.1`  
4. Vérifiez que l’application utilise le bon port (I2CP=7654, SAM=7656)

**"Certificate validation failed"** ou **"RouterInfo corrupt"** lors du réensemencement :

Causes sous-jacentes : décalage d’horloge (à corriger en premier), netDb corrompue, certificats de réensemencement invalides

```bash
# After fixing clock:
i2prouter stop
rm -rf ~/.i2p/netDb/*  # Delete corrupted database
i2prouter start  # Auto-reseeds with fresh data
```
**"Corruption de la base de données détectée"** indique une corruption des données au niveau du disque dans netDb ou peerProfiles :

```bash
# Safe fix - all will rebuild
i2prouter stop  
rm -rf ~/.i2p/netDb/* ~/.i2p/peerProfiles/*
i2prouter start
```
Vérifiez l’état du disque avec des outils S.M.A.R.T. - des corruptions récurrentes suggèrent une défaillance du périphérique de stockage.

## Défis spécifiques à chaque plateforme

Les différents systèmes d’exploitation présentent des défis uniques de déploiement d’I2P liés aux autorisations, aux politiques de sécurité et à l’intégration au système.

### Problèmes de permissions et de services sous Linux

I2P installé via les paquets de la distribution s’exécute en tant qu’utilisateur système **i2psvc** (Debian/Ubuntu) ou **i2p** (autres distributions), et nécessite des autorisations spécifiques :

```bash
# Fix package install permissions  
sudo chown -R i2psvc:i2psvc /var/lib/i2p /var/log/i2p /run/i2p
sudo chmod 750 /var/log/i2p /var/lib/i2p
sudo chmod 644 /var/lib/i2p/*.config

# User install permissions (should be your user)
chown -R $USER:$USER ~/.i2p
chmod 700 ~/.i2p
chmod 600 ~/.i2p/router.keys ~/.i2p/*.config
```
**Limites des descripteurs de fichiers** affectent la capacité du router en matière de connexions. Les limites par défaut (1024) sont insuffisantes pour les routers à haut débit :

```bash
# Check current limits
ulimit -n

# Temporary increase  
ulimit -n 4096

# Permanent fix: Edit /etc/security/limits.conf
i2psvc soft nofile 4096
i2psvc hard nofile 8192

# Systemd override
sudo mkdir -p /etc/systemd/system/i2p.service.d/
sudo nano /etc/systemd/system/i2p.service.d/override.conf

# Add:
[Service]
LimitNOFILE=8192

sudo systemctl daemon-reload
sudo systemctl restart i2p
```
**Conflits AppArmor** courants sur Debian/Ubuntu empêchent le démarrage du service:

```bash
# Error: "Failed at step APPARMOR spawning /usr/sbin/wrapper"
# Cause: AppArmor profile missing or misconfigured

# Solution 1: Disable AppArmor for I2P
sudo aa-complain /usr/sbin/wrapper

# Solution 2: Reconfigure package without AppArmor
sudo dpkg-reconfigure -plow i2p  
# Select "No" when asked about AppArmor

# Solution 3: LXC/Proxmox containers - disable AppArmor in container config
lxc.apparmor.profile: unconfined
```
**Problèmes liés à SELinux** sur RHEL/CentOS/Fedora :

```bash
# Temporary: Set permissive mode
sudo setenforce 0

# Permanent: Generate custom policy
sudo ausearch -c 'java' --raw | audit2allow -M i2p_policy
sudo semodule -i i2p_policy.pp

# Or disable SELinux for I2P process (less secure)
sudo semanage permissive -a i2p_t
```
**Dépannage des services SystemD:**

```bash
# Detailed service status
sudo systemctl status i2p.service -l

# Full logs  
sudo journalctl -xe -u i2p.service

# Follow logs live
sudo journalctl -f -u i2p.service

# Restart with logging
sudo systemctl restart i2p.service && sudo journalctl -f -u i2p.service
```
### Interférences du pare-feu et de l’antivirus Windows

Windows Defender et les produits antivirus tiers signalent fréquemment I2P en raison de modèles de comportement réseau. Une configuration correcte permet d’éviter des blocages inutiles tout en préservant la sécurité.

**Configurer le Pare-feu Windows Defender :**

```powershell
# Run PowerShell as Administrator

# Find Java path (adjust for your Java installation)
$javaPath = "C:\Program Files\Eclipse Adoptium\jdk-11.0.16.101-hotspot\bin\javaw.exe"

# Create inbound rules
New-NetFirewallRule -DisplayName "I2P Java" -Direction Inbound -Program $javaPath -Action Allow
New-NetFirewallRule -DisplayName "I2P UDP" -Direction Inbound -Protocol UDP -LocalPort 22648 -Action Allow  
New-NetFirewallRule -DisplayName "I2P TCP" -Direction Inbound -Protocol TCP -LocalPort 22648 -Action Allow

# Add exclusions to Windows Defender
Add-MpPreference -ExclusionPath "C:\Program Files\i2p"
Add-MpPreference -ExclusionPath "$env:APPDATA\I2P"
Add-MpPreference -ExclusionPath "$env:LOCALAPPDATA\I2P"
Add-MpPreference -ExclusionProcess "javaw.exe"
```
Remplacez le port 22648 par votre port I2P réel indiqué sur http://127.0.0.1:7657/confignet.

**Problème spécifique à Kaspersky Antivirus:** La fonctionnalité "Application Control" de Kaspersky limite le tas Java à 512 Mo, indépendamment des paramètres de wrapper.config. Cela provoque des erreurs OutOfMemoryError sur des routers à haut débit.

Solutions: 1. Ajouter I2P aux exclusions de Kaspersky : Paramètres → Supplémentaire → Menaces et exclusions → Gérer les exclusions 2. Ou désinstaller Kaspersky (recommandé pour le fonctionnement d'I2P)

**Recommandations générales pour les antivirus tiers :**

- Ajouter le dossier d’installation d’I2P à la liste des exclusions  
- Ajouter %APPDATA%\I2P et %LOCALAPPDATA%\I2P à la liste des exclusions
- Exclure javaw.exe de l’analyse comportementale
- Désactiver les fonctionnalités "Network Attack Protection" (protection contre les attaques réseau) susceptibles d’interférer avec les protocoles I2P

### Gatekeeper de macOS bloque l'installation

Gatekeeper de macOS empêche les applications non signées de s’exécuter. Les programmes d’installation d’I2P ne sont pas signés avec un Apple Developer ID, ce qui déclenche des avertissements de sécurité.

**Contourner Gatekeeper pour le programme d’installation I2P:**

```bash
# Method 1: Remove quarantine attribute
xattr -d com.apple.quarantine ~/Downloads/i2pinstall_*.jar
java -jar ~/Downloads/i2pinstall_*.jar

# Method 2: Use System Settings (macOS 13+)
# Try to open installer → macOS blocks it
# System Settings → Privacy & Security → scroll down
# Click "Open Anyway" next to I2P warning
# Confirm in dialog

# Method 3: Control-click installer
# Control-click (right-click) i2pinstall_*.jar
# Select "Open" from menu → "Open" again in dialog
# Bypasses Gatekeeper for this specific file
```
**Après l'installation, l'exécution** peut encore déclencher des avertissements :

```bash
# If I2P won't start due to Gatekeeper:
xattr -dr com.apple.quarantine ~/i2p/
```
**Ne désactivez jamais Gatekeeper de façon permanente** - risque de sécurité pour les autres applications. N'utilisez que des contournements spécifiques à un fichier.

**Configuration du pare-feu de macOS:**

1. Préférences Système → Sécurité et confidentialité → Pare-feu → Options du pare-feu
2. Cliquez sur « + » pour ajouter une application  
3. Accédez à l’installation de Java (par exemple : `/Library/Java/JavaVirtualMachines/jdk-11.jdk/Contents/Home/bin/java`)
4. Ajoutez-la et définissez sur « Autoriser les connexions entrantes »

### Problèmes de l’application I2P sur Android

Les contraintes liées aux versions d'Android et les limitations de ressources posent des défis particuliers.

**Exigences minimales :** - Android 5.0+ (niveau d'API 21+) requis pour les versions actuelles - 512 Mo de RAM minimum, 1 Go+ recommandé   - 100 Mo de stockage pour l’application + les données du router - Restrictions des applications en arrière-plan désactivées pour I2P

**L'application plante immédiatement:**

1. **Vérifiez la version d’Android :** Paramètres → À propos du téléphone → Version d’Android (doit être 5.0+)
2. **Désinstallez toutes les versions d’I2P :** N’installez qu’une seule variante :
   - net.i2p.android (Google Play)
   - net.i2p.android.router (F-Droid)  
   Plusieurs installations entrent en conflit
3. **Effacez les données de l’application :** Paramètres → Applications → I2P → Stockage → Effacer les données
4. **Réinstallez à partir d’un état propre**

**L'optimisation de la batterie tue le router:**

Android ferme de manière agressive les applications en arrière-plan pour économiser la batterie. I2P doit être exclu :

1. Paramètres → Batterie → Optimisation de la batterie (ou Utilisation de la batterie de l’application)
2. Recherchez I2P → Ne pas optimiser (ou Autoriser l’activité en arrière-plan)
3. Paramètres → Applications → I2P → Batterie → Autoriser l’activité en arrière-plan + Supprimer les restrictions

**Problèmes de connexion sur mobile :**

- **L’amorçage nécessite le WiFi :** Le reseed (procédure d’obtention initiale des pairs) initial télécharge une quantité importante de données - utilisez le WiFi, pas le réseau mobile
- **Changements de réseau :** I2P gère mal les basculements de réseau - redémarrez l’application après une transition WiFi/réseau mobile
- **Bande passante pour mobile :** Configurez prudemment à 64-128 KB/sec pour éviter d’épuiser votre forfait de données mobiles

**Optimisation des performances pour mobile:**

1. Application I2P → Menu → Paramètres → Bande passante
2. Réglez des limites appropriées : 64 Ko/s en entrée, 32 Ko/s en sortie pour le réseau mobile
3. Réduisez les tunnels participants : Paramètres → Avancé → Nombre maximum de tunnels participants : 100-200
4. Activez "Arrêter I2P lorsque l'écran est éteint" pour économiser la batterie

**Téléchargement de torrents sur Android :**

- Limiter à 2-3 torrents simultanés maximum
- Réduire l'agressivité de la DHT  
- Utiliser uniquement le WiFi pour les torrents
- Accepter des vitesses plus lentes sur du matériel mobile

## Problèmes de reseed et de bootstrap

Les nouvelles installations d'I2P nécessitent un **reseeding** (réensemencement initial) - récupération des informations initiales sur les pairs depuis des serveurs HTTPS publics pour rejoindre le réseau. Les problèmes de reseeding piègent les utilisateurs sans aucun pair et sans accès au réseau.

**"No active peers" après une nouvelle installation** indique généralement un échec du reseed (importation initiale de pairs). Symptômes :

- Pairs connus: 0 ou reste inférieur à 5
- "Network: Testing" persiste au-delà de 15 minutes
- Les journaux affichent "Reseed failed" ou des erreurs de connexion aux serveurs de reseed (réensemencement)

**Pourquoi le reseed (réensemencement) échoue:**

1. **Pare-feu bloquant HTTPS:** Les pare-feu d'entreprise/FAI bloquent les connexions aux reseed servers (serveurs de démarrage du réseau I2P) (port 443)
2. **Erreurs de certificats SSL:** Le système ne dispose pas de certificats racine à jour
3. **Exigence de proxy:** Le réseau requiert un proxy HTTP/SOCKS pour les connexions externes
4. **Décalage d'horloge:** La validation des certificats SSL échoue lorsque l'heure du système est incorrecte
5. **Censure géographique:** Certains pays/FAI bloquent des reseed servers connus

**Forcer un reseed manuel (réamorçage du réseau):**

1. Accédez à http://127.0.0.1:7657/configreseed
2. Cliquez sur "Save changes and reseed now"  
3. Surveillez http://127.0.0.1:7657/logs pour "Reseed got XX router infos"
4. Attendez 5 à 10 minutes pour le traitement
5. Vérifiez http://127.0.0.1:7657 - Les pairs connus devraient atteindre 50+

**Configurer le proxy de reseed (réensemencement)** pour les réseaux restrictifs :

http://127.0.0.1:7657/configreseed → Configuration du proxy:

- Proxy HTTP: [proxy-server]:[port]
- Ou SOCKS5: [socks-server]:[port]  
- Activer "Utiliser le proxy uniquement pour le réensemencement"
- Identifiants si nécessaire
- Enregistrer et forcer le réensemencement

**Alternative: Proxy Tor pour le réensemencement:**

Si Tor Browser ou le démon Tor est en cours d’exécution :

- Type de proxy: SOCKS5
- Hôte: 127.0.0.1
- Port: 9050 (port SOCKS Tor par défaut)
- Activer et réensemencer

**Réensemencement manuel via un fichier su3** (en dernier recours) :

Lorsque toutes les opérations de reseed automatisées (réensemencement) échouent, obtenez le fichier de reseed par un canal hors bande :

1. Téléchargez i2pseeds.su3 depuis une source de confiance sur une connexion sans restriction (https://reseed.i2p.rocks/i2pseeds.su3, https://reseed-fr.i2pd.xyz/i2pseeds.su3)
2. Arrêtez complètement I2P
3. Copiez i2pseeds.su3 dans le répertoire ~/.i2p/  
4. Démarrez I2P - extrait et traite automatiquement le fichier
5. Supprimez i2pseeds.su3 après le traitement
6. Vérifiez que le nombre de pairs augmente à l'adresse http://127.0.0.1:7657

**Erreurs de certificat SSL lors du réensemencement :**

```
Error: "Reseed: Certificate verification failed"  
Cause: System root certificates outdated or missing
```
Solutions :

```bash
# Linux - update certificates
sudo apt install ca-certificates
sudo update-ca-certificates

# Windows - install KB updates for root certificate trust
# Or install .NET Framework (includes certificate updates)

# macOS - update system
# Software Update includes certificate trust updates
```
**Bloqué à 0 pairs connus depuis plus de 30 minutes :**

Indique un échec complet du réamorçage. Procédure de dépannage :

1. **Vérifiez que l’heure du système est exacte** (problème le plus courant - à corriger EN PREMIER)
2. **Testez la connectivité HTTPS :** Essayez d’accéder à https://reseed.i2p.rocks dans le navigateur - si cela échoue, problème réseau
3. **Vérifiez les journaux I2P** à http://127.0.0.1:7657/logs pour des erreurs de reseed (réamorçage) spécifiques
4. **Essayez une autre URL de reseed :** http://127.0.0.1:7657/configreseed → ajoutez une URL de reseed personnalisée : https://reseed-fr.i2pd.xyz/
5. **Utilisez la méthode manuelle via un fichier su3** si les tentatives automatisées sont épuisées

**Serveurs de réensemencement occasionnellement hors ligne:** I2P inclut plusieurs serveurs de réensemencement codés en dur. Si l’un d’eux échoue, le router essaie automatiquement les autres. Une panne totale de tous les serveurs de réensemencement est extrêmement rare, mais possible.

**Serveurs de reseed (serveurs d’amorçage) actifs** (en octobre 2025):

- https://reseed.i2p.rocks/
- https://reseed-fr.i2pd.xyz/
- https://i2p.novg.net/
- https://i2p-projekt.de/

Ajoutez-les en tant qu’URL personnalisées si vous rencontrez des problèmes avec les paramètres par défaut.

**Pour les utilisateurs dans des régions fortement censurées:**

Envisagez d’utiliser des ponts Snowflake/Meek via Tor pour le réensemencement initial, puis de passer à I2P direct une fois intégré au réseau. Ou obtenez i2pseeds.su3 via stéganographie, par e-mail ou sur une clé USB depuis l’extérieur de la zone de censure.

## Quand demander une aide supplémentaire

Ce guide couvre la grande majorité des problèmes I2P, mais certains nécessitent l’attention des développeurs ou l’expertise de la communauté.

**Demandez de l'aide à la communauté I2P lorsque :**

- Le router plante systématiquement après avoir suivi toutes les étapes de dépannage
- Fuites de mémoire entraînant une croissance continue au-delà du tas mémoire alloué
- Le taux de réussite des tunnels reste inférieur à 20 % malgré une configuration adéquate  
- Nouvelles erreurs dans les journaux non couvertes par ce guide
- Vulnérabilités de sécurité découvertes
- Demandes de fonctionnalités ou suggestions d'amélioration

**Avant de demander de l'aide, rassemblez les informations de diagnostic:**

1. Version d'I2P : http://127.0.0.1:7657 (p. ex., "2.10.0")
2. Version de Java : sortie de `java -version`
3. Système d'exploitation et version
4. Statut du router : État du réseau, nombre de pairs actifs, tunnels participants
5. Configuration de la bande passante : limites entrantes/sortantes
6. Statut de la redirection de ports : Derrière un pare-feu ou OK
7. Extraits de journaux pertinents : 50 dernières lignes affichant les erreurs depuis http://127.0.0.1:7657/logs

**Canaux officiels d'assistance:**

- **Forum:** https://i2pforum.net (clearnet) ou http://i2pforum.i2p (au sein d'I2P)
- **IRC:** #i2p sur Irc2P (irc.postman.i2p via I2P) ou irc.freenode.net (clearnet)
- **Reddit:** https://reddit.com/r/i2p pour les discussions de la communauté
- **Suivi des bogues:** https://i2pgit.org/i2p-hackers/i2p.i2p/-/issues pour les bogues confirmés
- **Liste de diffusion:** i2p-dev@lists.i2p-projekt.de pour les questions de développement

**Les attentes réalistes comptent.** I2P est plus lent que la clearnet (Internet public non chiffré) de par sa conception - les tunnels chiffrés multi-sauts créent une latence inhérente. Un I2P router avec des chargements de page de 30 secondes et des vitesses de torrent de 50 KB/sec **fonctionne correctement**, il n’est pas en panne. Les utilisateurs qui s’attendent à des vitesses de clearnet seront déçus, quelle que soit l’optimisation de la configuration.

## Conclusion

La plupart des problèmes I2P proviennent de trois catégories : manque de patience pendant l’amorçage (bootstrap) — 10 à 15 minutes sont nécessaires —, allocation de ressources insuffisante (au minimum 512 Mo de RAM et 256 Ko/s de bande passante), ou redirection de ports mal configurée. Comprendre l’architecture distribuée d’I2P et sa conception axée sur l’anonymat aide les utilisateurs à distinguer le comportement attendu des problèmes réels.

Le statut "Firewalled" (connectivité entrante bloquée) du router, bien que sous-optimal, n’empêche pas l’utilisation d’I2P - il limite seulement la contribution au réseau et dégrade légèrement les performances. Les nouveaux utilisateurs devraient privilégier la **stabilité plutôt que l’optimisation** : faites fonctionner le router en continu pendant plusieurs jours avant d’ajuster les paramètres avancés, car l’intégration s’améliore naturellement avec le temps de disponibilité.

Lors du dépannage, vérifiez toujours d’abord les fondamentaux : horloge système correctement réglée, bande passante suffisante, router fonctionnant en continu et au moins 10 pairs actifs. La plupart des problèmes se résolvent en corrigeant ces bases plutôt qu’en ajustant des paramètres de configuration obscurs. I2P récompense la patience et le fonctionnement en continu par des performances améliorées, à mesure que le router construit sa réputation et optimise la sélection des pairs au fil des jours et des semaines de fonctionnement.
