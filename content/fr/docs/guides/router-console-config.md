---
title: "Guide de configuration de la console du routeur"
description: "Guide complet pour comprendre et configurer la Console du Routeur I2P"
slug: "router-console-config"
lastUpdated: "2025-11"
accurateFor: "2.10.0"
type: docs
---

Ce guide fournit un aperçu de la console du router I2P et de ses pages de configuration. Chaque section explique le rôle de la page et son utilité, vous aidant à comprendre comment surveiller et configurer votre router I2P.

## Accéder à la console du routeur

La Console du Router I2P est le centre de contrôle pour gérer et surveiller votre router I2P. Par défaut, elle est accessible via la [Console du Router I2P](http://127.0.0.1:7657/home) une fois votre router I2P en cours d'exécution.

![Console du routeur - Accueil](/images/router-console-home.png)

La page d'accueil affiche plusieurs sections clés :

- **Applications** - Accès rapide aux applications I2P intégrées comme Email, Torrents, Gestionnaire de Services Cachés et Serveur Web
- **Sites Communautaires I2P** - Liens vers les ressources communautaires importantes incluant forums, documentation et sites web du projet
- **Configuration et Aide** - Outils pour configurer les paramètres de bande passante, gérer les plugins et accéder aux ressources d'aide
- **Informations Réseau et Développeur** - Accès aux graphiques, journaux, documentation technique et statistiques réseau

## Carnet d'adresses

**URL :** [Carnet d'adresses](http://127.0.0.1:7657/dns)

![Console du routeur - Carnet d'adresses](/images/router-console-address-book.png)

Le carnet d'adresses I2P fonctionne de manière similaire au DNS sur le clearnet, vous permettant de gérer des noms lisibles par l'homme pour les destinations I2P (eepsites). C'est ici que vous pouvez consulter et ajouter des adresses I2P à votre carnet d'adresses personnel.

Le système de carnet d'adresses fonctionne à travers plusieurs couches :

- **Enregistrements locaux** - Vos carnets d'adresses personnels qui sont stockés uniquement sur votre routeur
  - **Carnet d'adresses local** - Hôtes que vous ajoutez manuellement ou enregistrez pour votre usage personnel
  - **Carnet d'adresses privé** - Adresses que vous ne souhaitez pas partager avec d'autres ; jamais distribuées publiquement

- **Abonnements** - Sources distantes de carnet d'adresses (comme `http://i2p-projekt.i2p/hosts.txt`) qui mettent automatiquement à jour le carnet d'adresses de votre router avec les sites I2P connus

- **Carnet d'adresses du routeur** - Le résultat fusionné de vos enregistrements locaux et de vos abonnements, consultable par toutes les applications I2P sur votre routeur

- **Carnet d'adresses publié** - Partage public optionnel de votre carnet d'adresses pour que d'autres puissent l'utiliser comme source d'abonnement (utile si vous hébergez un eepsite)

Le carnet d'adresses interroge régulièrement vos abonnements et fusionne le contenu dans le carnet d'adresses de votre routeur, maintenant votre fichier hosts.txt à jour avec le réseau I2P.

## Configuration

**URL :** [Configuration Avancée](http://127.0.0.1:7657/configadvanced)

La section Configuration donne accès à tous les paramètres du routeur via plusieurs onglets spécialisés.

### Advanced

![Router Console Configuration Avancée](/images/router-console-config-advanced.png)

La page de configuration avancée permet d'accéder aux paramètres de bas niveau du routeur qui ne sont généralement pas nécessaires pour un fonctionnement normal. **La plupart des utilisateurs ne doivent pas modifier ces paramètres à moins de comprendre l'option de configuration spécifique et son impact sur le comportement du routeur.**

Fonctionnalités principales :

- **Configuration Floodfill** - Contrôlez si votre routeur participe en tant que pair floodfill, ce qui aide le réseau en stockant et distribuant les informations de la base de données réseau (netDb). Cela peut utiliser davantage de ressources système mais renforce le réseau I2P.

- **Configuration I2P avancée** - Accès direct au fichier `router.config`, affichant tous les paramètres de configuration avancés incluant :
  - Limites de bande passante et paramètres de rafale
  - Paramètres de transport (NTCP2, SSU2, ports UDP et clés)
  - Identification du router et informations de version
  - Préférences de la console et paramètres de mise à jour

La plupart des options de configuration avancées ne sont pas exposées dans l'interface utilisateur car elles sont rarement nécessaires. Pour activer l'édition de ces paramètres, vous devez ajouter `routerconsole.advanced=true` à votre fichier `router.config` manuellement.

**Avertissement :** La modification incorrecte des paramètres avancés peut avoir un impact négatif sur les performances ou la connectivité de votre router. Ne modifiez ces paramètres que si vous savez ce que vous faites.

### Bandwidth

**URL :** [Configuration de la bande passante](http://127.0.0.1:7657/config)

![Configuration de la bande passante de la console du routeur](/images/router-console-config-bandwidth.png)

La page de configuration de la bande passante vous permet de contrôler la quantité de bande passante que votre router contribue au réseau I2P. I2P fonctionne mieux lorsque vous configurez vos débits pour qu'ils correspondent à la vitesse de votre connexion internet.

**Paramètres Clés :**

- **KBps In** - Bande passante entrante maximale que votre routeur acceptera (vitesse de téléchargement)
- **KBps Out** - Bande passante sortante maximale que votre routeur utilisera (vitesse de téléversement)
- **Share** - Pourcentage de votre bande passante sortante dédié au trafic de participation (aide au routage du trafic pour les autres)

**Notes importantes :**

- Toutes les valeurs sont en **octets par seconde** (Ko/s), et non en bits par seconde
- Plus vous allouez de bande passante, plus vous aidez le réseau et améliorez votre propre anonymat
- Votre quantité de partage en envoi (Ko/s sortant) détermine votre contribution globale au réseau
- Si vous n'êtes pas certain de la vitesse de votre réseau, utilisez le **Test de bande passante** pour la mesurer
- Une bande passante de partage plus élevée améliore à la fois votre anonymat et contribue à renforcer le réseau I2P

La page de configuration affiche une estimation du transfert de données mensuel basée sur vos paramètres, vous aidant à planifier l'allocation de bande passante selon les limites de votre forfait internet.

### Client Configuration

**URL:** [Configuration du client](http://127.0.0.1:7657/configclients)

![Configuration des clients de la Console du Router](/images/router-console-config-clients.png)

La page de configuration client vous permet de contrôler quelles applications et services I2P s'exécutent au démarrage. C'est ici que vous pouvez activer ou désactiver les clients I2P intégrés sans les désinstaller.

**Avertissement Important :** Soyez prudent lors de la modification des paramètres ici. La console du routeur et les tunnels d'application sont requis pour la plupart des utilisations d'I2P. Seuls les utilisateurs avancés devraient modifier ces paramètres.

**Clients disponibles :**

- **Tunnels d'application** - Le système I2PTunnel qui gère les tunnels client et serveur (proxy HTTP, IRC, etc.)
- **Console du routeur I2P** - L'interface d'administration web que vous utilisez actuellement
- **Serveur web I2P (eepsite)** - Serveur web Jetty intégré pour héberger votre propre site web I2P
- **Ouvrir la console du routeur dans le navigateur web au démarrage** - Lance automatiquement votre navigateur vers la page d'accueil de la console
- **Pont d'application SAM** - Pont API permettant aux applications tierces de se connecter à I2P

Chaque client affiche : - **Exécuter au démarrage ?** - Case à cocher pour activer/désactiver le démarrage automatique - **Contrôle** - Boutons Démarrer/Arrêter pour un contrôle immédiat - **Classe et arguments** - Détails techniques sur la façon dont le client est lancé

Les modifications du paramètre « Exécuter au démarrage ? » nécessitent un redémarrage du router pour prendre effet. Toutes les modifications sont enregistrées dans `/var/lib/i2p/i2p-config/clients.config.d/`.

### Avancé

**URL:** [Configuration I2CP](http://127.0.0.1:7657/configi2cp)

![Console du routeur Configuration I2CP](/images/router-console-config-i2cp.png)

La page de configuration I2CP (I2P Client Protocol) vous permet de configurer la façon dont les applications externes se connectent à votre routeur I2P. I2CP est le protocole que les applications utilisent pour communiquer avec le routeur afin de créer des tunnels et d'envoyer/recevoir des données via I2P.

**Important :** Les paramètres par défaut fonctionneront pour la plupart des utilisateurs. Toute modification effectuée ici doit également être configurée dans l'application cliente externe. De nombreux clients ne prennent pas en charge SSL ou l'authentification. **Toutes les modifications nécessitent un redémarrage pour prendre effet.**

**Options de Configuration :**

- **Configuration de l'interface I2CP externe**
  - **Activée sans SSL** - Accès I2CP standard (par défaut et plus compatible)
  - **Activée avec SSL requis** - Connexions I2CP chiffrées uniquement
  - **Désactivée** - Bloque les clients externes de se connecter via I2CP

- **Interface I2CP** - L'interface réseau sur laquelle écouter (par défaut : 127.0.0.1 pour localhost uniquement)
- **Port I2CP** - Le numéro de port pour les connexions I2CP (par défaut : 7654)

- **Autorisation**
  - **Exiger un nom d'utilisateur et un mot de passe** - Activer l'authentification pour les connexions I2CP
  - **Nom d'utilisateur** - Définir le nom d'utilisateur requis pour l'accès I2CP
  - **Mot de passe** - Définir le mot de passe requis pour l'accès I2CP

**Note de sécurité :** Si vous exécutez uniquement des applications sur la même machine que votre routeur I2P, conservez l'interface définie sur `127.0.0.1` pour empêcher l'accès distant. Ne modifiez ces paramètres que si vous devez autoriser des applications I2P provenant d'autres appareils à se connecter à votre routeur.

### Bande passante

**URL:** [Configuration réseau](http://127.0.0.1:7657/confignet)

![Console du routeur Configuration réseau](/images/router-console-config-network.png)

La page de Configuration Réseau vous permet de configurer la manière dont votre router I2P se connecte à Internet, y compris la détection d'adresse IP, les préférences IPv4/IPv6, et les paramètres de port pour les transports UDP et TCP.

**Adresse IP accessible de l'extérieur :**

- **Utiliser toutes les méthodes de détection automatique** - Détecte automatiquement votre IP publique en utilisant plusieurs méthodes (recommandé)
- **Désactiver la détection d'adresse IP UPnP** - Empêche l'utilisation d'UPnP pour découvrir votre IP
- **Ignorer l'adresse IP de l'interface locale** - Ne pas utiliser votre IP de réseau local
- **Utiliser uniquement la détection d'adresse IP SSU** - Utilise uniquement le transport SSU2 pour la détection d'IP
- **Mode caché - ne pas publier l'IP** - Empêche la participation au trafic réseau (réduit l'anonymat)
- **Spécifier un nom d'hôte ou une IP** - Définir manuellement votre IP publique ou nom d'hôte

**Configuration IPv4 :**

- **Désactiver les connexions entrantes (Derrière un pare-feu)** - Cochez cette option si vous êtes derrière un pare-feu, un réseau domestique, un FAI, DS-Lite ou un NAT de niveau opérateur qui bloque les connexions entrantes

**Configuration IPv6 :**

- **Préférer IPv4 à IPv6** - Priorise les connexions IPv4
- **Préférer IPv6 à IPv4** - Priorise les connexions IPv6 (par défaut pour les réseaux double pile)
- **Activer IPv6** - Autorise les connexions IPv6
- **Désactiver IPv6** - Désactive toute connectivité IPv6
- **Utiliser IPv6 uniquement (désactiver IPv4)** - Mode IPv6 uniquement expérimental
- **Désactiver les connexions entrantes (Derrière un pare-feu)** - Cochez si votre IPv6 est derrière un pare-feu

**Action en cas de changement d'IP :**

- **Mode portable** - Fonctionnalité expérimentale qui modifie l'identité du routeur et le port UDP lorsque votre adresse IP change pour une anonymat renforcé

**Configuration UDP :**

- **Spécifier le port** - Définir un port UDP spécifique pour le transport SSU2 (doit être ouvert dans votre pare-feu)
- **Désactiver complètement** - Sélectionner uniquement si vous êtes derrière un pare-feu qui bloque tout le trafic UDP sortant

**Configuration TCP :**

- **Spécifier le port** - Définir un port TCP spécifique pour le transport NTCP2 (doit être ouvert dans votre pare-feu)
- **Utiliser le même port configuré pour UDP** - Simplifie la configuration en utilisant un seul port pour les deux transports
- **Utiliser l'adresse IP détectée automatiquement** - Détecte automatiquement votre IP publique (affiche « actuellement inconnue » si pas encore détectée ou bloquée par un pare-feu)
- **Toujours utiliser l'adresse IP détectée automatiquement (Non protégé par un pare-feu)** - Idéal pour les routeurs avec accès direct à Internet
- **Désactiver les connexions entrantes (Protégé par un pare-feu)** - Cochez si les connexions TCP sont bloquées par votre pare-feu
- **Désactiver complètement** - Ne sélectionnez que si vous êtes derrière un pare-feu qui limite ou bloque le TCP sortant
- **Spécifier un nom d'hôte ou une IP** - Configurer manuellement votre adresse accessible de l'extérieur

**Important :** Les modifications des paramètres réseau peuvent nécessiter un redémarrage du router pour prendre pleinement effet. Une configuration appropriée de la redirection de port améliore considérablement les performances de votre router et contribue au réseau I2P.

### Configuration du client

**URL :** [Configuration des pairs](http://127.0.0.1:7657/configpeer)

![Console du Routeur - Configuration des Pairs](/images/router-console-config-peer.png)

La page de Configuration des Pairs fournit des contrôles manuels pour gérer les pairs individuels sur le réseau I2P. Il s'agit d'une fonctionnalité avancée généralement utilisée uniquement pour résoudre les problèmes liés à des pairs problématiques.

**Contrôles Manuels des Pairs :**

- **Hash du routeur** - Entrez le hash du routeur en base64 de 44 caractères du pair que vous souhaitez gérer

**Bannir / Débannir manuellement un pair :**

Bannir un pair l'empêche de participer aux tunnels que vous créez. Cette action : - Empêche le pair d'être utilisé dans vos tunnels clients ou exploratoires - Prend effet immédiatement sans nécessiter de redémarrage - Persiste jusqu'à ce que vous débannissiez manuellement le pair ou redémarriez votre routeur - **Bannir le pair jusqu'au redémarrage** - Bloque temporairement le pair - **Débannir le pair** - Retire le bannissement d'un pair précédemment bloqué

**Ajuster les bonus de profil :**

Les bonus de profil affectent la manière dont les pairs sont sélectionnés pour la participation aux tunnels. Les bonus peuvent être positifs ou négatifs : - **Pairs rapides** - Utilisés pour les tunnels client nécessitant une vitesse élevée - **Pairs à haute capacité** - Utilisés pour certains tunnels exploratoires nécessitant un routage fiable - Les bonus actuels sont affichés sur la page des profils

**Configuration :** - **Vitesse** - Ajuster le bonus de vitesse pour ce pair (0 = neutre) - **Capacité** - Ajuster le bonus de capacité pour ce pair (0 = neutre) - **Ajuster les bonus de pairs** - Appliquer les paramètres de bonus

**Cas d'utilisation :** - Bannir un pair qui cause régulièrement des problèmes de connexion - Exclure temporairement un pair que vous soupçonnez d'être malveillant - Ajuster les bonus pour dé-prioriser les pairs sous-performants - Déboguer les problèmes de construction de tunnel en excluant des pairs spécifiques

**Remarque :** La plupart des utilisateurs n'auront jamais besoin d'utiliser cette fonctionnalité. Le routeur I2P gère automatiquement la sélection et le profilage des pairs en fonction des métriques de performance.

### Configuration I2CP

**URL:** [Configuration Reseed](http://127.0.0.1:7657/configreseed)

![Console du Router Configuration Reseed](/images/router-console-config-reseed.png)

La page de configuration du Reseed vous permet de réensemencer manuellement votre router si le réensemencement automatique échoue. Le réensemencement est le processus d'amorçage utilisé pour trouver d'autres routers lorsque vous installez I2P pour la première fois, ou lorsque votre router dispose de trop peu de références de routers restantes.

**Quand Utiliser le Reseeding Manuel :**

1. Si le réamorçage a échoué, vous devriez d'abord vérifier votre connexion réseau
2. Si un pare-feu bloque vos connexions aux hôtes de réamorçage, vous pouvez avoir accès à un proxy :
   - Le proxy peut être un proxy public distant, ou peut s'exécuter sur votre ordinateur (localhost)
   - Pour utiliser un proxy, configurez le type, l'hôte et le port dans la section Configuration du réamorçage
   - Si vous utilisez Tor Browser, réamorcez à travers celui-ci en configurant SOCKS 5, localhost, port 9150
   - Si vous utilisez Tor en ligne de commande, réamorcez à travers celui-ci en configurant SOCKS 5, localhost, port 9050
   - Si vous avez quelques pairs mais en avez besoin de davantage, vous pouvez essayer l'option I2P Outproxy. Laissez l'hôte et le port vides. Cela ne fonctionnera pas pour un réamorçage initial lorsque vous n'avez aucun pair
   - Ensuite, cliquez sur « Enregistrer les modifications et réamorcer maintenant »
   - Les paramètres par défaut fonctionneront pour la plupart des utilisateurs. Modifiez-les uniquement si HTTPS est bloqué par un pare-feu restrictif et que le réamorçage a échoué

3. Si vous connaissez et faites confiance à quelqu'un qui utilise I2P, demandez-lui de vous envoyer un fichier reseed généré à partir de cette page sur sa console router. Ensuite, utilisez cette page pour effectuer un reseed avec le fichier que vous avez reçu. D'abord, sélectionnez le fichier ci-dessous. Puis, cliquez sur « Reseed depuis un fichier »

4. Si vous connaissez et faites confiance à quelqu'un qui publie des fichiers reseed, demandez-lui l'URL. Ensuite, utilisez cette page pour effectuer un reseed avec l'URL que vous avez reçue. D'abord, saisissez l'URL ci-dessous. Puis, cliquez sur « Reseed depuis une URL »

5. Voir [la FAQ](/docs/overview/faq/) pour les instructions sur le reseeding manuel

**Options de Reseed manuel :**

- **Reseed depuis URL** - Entrez une URL zip ou su3 provenant d'une source de confiance et cliquez sur "Reseed from URL"
  - Le format su3 est préférable, car il sera vérifié comme étant signé par une source de confiance
  - Le format zip n'est pas signé ; utilisez un fichier zip uniquement depuis une source en qui vous avez confiance

- **Reseed depuis un fichier** - Parcourez et sélectionnez un fichier zip ou su3 local, puis cliquez sur "Reseed from file"
  - Vous pouvez trouver des fichiers reseed sur [checki2p.com/reseed](https://checki2p.com/reseed)

- **Créer un fichier Reseed** - Générer un nouveau fichier zip reseed que vous pouvez partager pour que d'autres puissent reseed manuellement
  - Ce fichier ne contiendra jamais l'identité ou l'IP de votre propre router

**Configuration du Reseeding :**

Les paramètres par défaut fonctionneront pour la plupart des utilisateurs. Modifiez-les uniquement si HTTPS est bloqué par un pare-feu restrictif et que le reseed a échoué.

- **URL de reseed** - Liste des URL HTTPS vers les serveurs de reseed (la liste par défaut est intégrée et régulièrement mise à jour)
- **Configuration du proxy** - Configurez un proxy HTTP/HTTPS/SOCKS si vous devez accéder aux serveurs de reseed via un proxy
- **Réinitialiser la liste d'URL** - Restaurer la liste par défaut des serveurs de reseed

**Important :** Le réamorçage manuel ne devrait être nécessaire que dans de rares cas où le réamorçage automatique échoue de façon répétée. La plupart des utilisateurs n'auront jamais besoin d'utiliser cette page.

### Configuration Réseau

**URL :** [Configuration de la famille de routeurs](http://127.0.0.1:7657/configfamily)

![Configuration de la famille de routeurs dans la Console du routeur](/images/router-console-config-family.png)

La page de configuration de la famille de routeurs vous permet de gérer les familles de routeurs. Les routeurs d'une même famille partagent une clé de famille, qui les identifie comme étant exploités par la même personne ou organisation. Cela empêche la sélection de plusieurs routeurs que vous contrôlez pour le même tunnel, ce qui réduirait l'anonymat.

**Qu'est-ce qu'une famille de routeurs ?**

Lorsque vous exploitez plusieurs routeurs I2P, vous devez les configurer pour qu'ils fassent partie de la même famille. Cela garantit : - Vos routeurs ne seront pas utilisés ensemble dans le même chemin de tunnel - Les autres utilisateurs maintiennent un anonymat approprié lorsque leurs tunnels utilisent vos routeurs - Le réseau peut distribuer correctement la participation aux tunnels

**Famille actuelle :**

La page affiche le nom de famille actuel de votre routeur. Si vous ne faites pas partie d'une famille, ce champ sera vide.

**Exporter la clé de famille :**

- **Exportez la clé de famille secrète pour l'importer dans d'autres routeurs que vous contrôlez**
- Cliquez sur « Export Family Key » pour télécharger votre fichier de clé de famille
- Importez cette clé sur vos autres routeurs pour les ajouter à la même famille

**Quitter la famille de routeur :**

- **Ne plus être membre de la famille**
- Cliquez sur « Quitter la famille » pour retirer ce routeur de sa famille actuelle
- Cette action ne peut pas être annulée sans réimporter la clé de famille

**Considérations importantes :**

- **Enregistrement public requis :** Pour que votre famille soit reconnue sur l'ensemble du réseau, votre clé de famille doit être ajoutée au code source d'I2P par l'équipe de développement. Cela garantit que tous les routeurs du réseau connaissent votre famille.
- **Contactez l'équipe I2P** pour enregistrer votre clé de famille si vous exploitez plusieurs routeurs publics
- La plupart des utilisateurs n'exécutant qu'un seul routeur n'auront jamais besoin d'utiliser cette fonctionnalité
- La configuration de famille est principalement utilisée par les opérateurs de plusieurs routeurs publics ou les fournisseurs d'infrastructure

**Cas d'Usage :**

- Exploiter plusieurs routeurs I2P pour la redondance
- Exécuter une infrastructure comme des serveurs reseed ou des outproxies sur plusieurs machines
- Gérer un réseau de routeurs I2P pour une organisation

### Configuration des pairs

**URL :** [Configuration des tunnels](http://127.0.0.1:7657/configtunnels)

![Console du Router Configuration des Tunnels](/images/router-console-config-tunnels.png)

La page de Configuration des Tunnels vous permet d'ajuster les paramètres par défaut des tunnels pour les tunnels exploratoires (utilisés pour la communication du routeur) et les tunnels clients (utilisés par les applications). **Les paramètres par défaut conviennent à la plupart des utilisateurs et ne devraient être modifiés que si vous comprenez les compromis.**

**Avertissements importants :**

⚠️ **Compromis Anonymat vs Performance :** Il existe un compromis fondamental entre l'anonymat et la performance. Des tunnels de plus de 3 hops (par exemple 2 hops + 0-2 hops, 3 hops + 0-1 hops, 3 hops + 0-2 hops), ou une quantité élevée + quantité de secours, peuvent réduire considérablement la performance ou la fiabilité. Une utilisation élevée du CPU et/ou de la bande passante sortante peut en résulter. Modifiez ces paramètres avec prudence et ajustez-les si vous rencontrez des problèmes.

⚠️ **Persistance :** Les modifications des paramètres des tunnels exploratoires sont enregistrées dans le fichier router.config. Les modifications des tunnels clients sont temporaires et ne sont pas sauvegardées. Pour effectuer des modifications permanentes des tunnels clients, consultez la [page I2PTunnel](/docs/api/i2ptunnel).

**Tunnels exploratoires :**

Les tunnels exploratoires sont utilisés par votre routeur pour communiquer avec la base de données réseau (netDb) et participer au réseau I2P.

Options de configuration pour l'Inbound et l'Outbound : - **Length** - Nombre de sauts dans le tunnel (par défaut : 2-3 sauts) - **Randomization** - Variance aléatoire de la longueur du tunnel (par défaut : 0-1 sauts) - **Quantity** - Nombre de tunnels actifs (par défaut : 2 tunnels) - **Backup quantity** - Nombre de tunnels de secours prêts à être activés (par défaut : 0 tunnels)

**Tunnels Client pour le Serveur Web I2P :**

Ces paramètres contrôlent les tunnels pour le serveur web I2P intégré (eepsite).

⚠️ **AVERTISSEMENT D'ANONYMAT** - Les paramètres incluent des tunnels à 1 saut. ⚠️ **AVERTISSEMENT DE PERFORMANCE** - Les paramètres incluent des quantités élevées de tunnels.

Options de configuration pour l'Entrant et le Sortant : - **Longueur** - Longueur du tunnel (par défaut : 1 saut pour le serveur web) - **Randomisation** - Variance aléatoire dans la longueur du tunnel - **Quantité** - Nombre de tunnels actifs - **Quantité de sauvegarde** - Nombre de tunnels de sauvegarde

**Tunnels client pour les clients partagés :**

Ces paramètres s'appliquent aux applications clientes partagées (proxy HTTP, IRC, etc.).

Options de configuration pour l'Entrant et le Sortant : - **Longueur** - Longueur du tunnel (par défaut : 3 sauts) - **Randomisation** - Variance aléatoire dans la longueur du tunnel - **Quantité** - Nombre de tunnels actifs - **Quantité de sauvegarde** - Nombre de tunnels de sauvegarde

**Comprendre les paramètres de tunnel :**

- **Longueur :** Des tunnels plus longs offrent plus d'anonymat mais réduisent les performances et la fiabilité
- **Randomisation :** Ajoute de l'imprévisibilité aux chemins des tunnels, améliorant la sécurité
- **Quantité :** Plus de tunnels améliorent la fiabilité et la distribution de charge mais augmentent l'utilisation des ressources
- **Quantité de secours :** Tunnels pré-construits prêts à remplacer les tunnels défaillants, améliorant la résilience

**Bonnes pratiques :**

- Conservez les paramètres par défaut sauf si vous avez des besoins spécifiques
- N'augmentez la longueur des tunnels que si l'anonymat est critique et que vous pouvez accepter une performance plus lente
- Augmentez la quantité/sauvegarde uniquement si vous rencontrez des échecs de tunnel fréquents
- Surveillez les performances du router après avoir effectué des modifications
- Cliquez sur « Enregistrer les modifications » pour appliquer les changements

### Configuration du Reseed

**URL:** [Configuration de l'interface utilisateur](http://127.0.0.1:7657/configui)

![Interface de configuration de la Console du Routeur](/images/router-console-config-ui.png)

La page de configuration de l'interface utilisateur vous permet de personnaliser l'apparence et l'accessibilité de votre console du router, y compris la sélection du thème, les préférences linguistiques et la protection par mot de passe.

**Thème de la Console du Routeur :**

Choisissez entre les thèmes sombre et clair pour l'interface de la console du router : - **Sombre** - Thème en mode sombre (plus confortable pour les yeux dans les environnements peu éclairés) - **Clair** - Thème en mode clair (apparence traditionnelle)

Options de thème supplémentaires : - **Définir le thème universellement pour toutes les applications** - Appliquer le thème sélectionné à toutes les applications I2P, pas seulement à la console du routeur - **Forcer l'utilisation de la console mobile** - Utiliser l'interface optimisée pour mobile même sur les navigateurs de bureau - **Intégrer les applications Email et Torrent dans la console** - Intégrer Susimail et I2PSnark directement dans l'interface de la console au lieu de les ouvrir dans des onglets séparés

**Langue de la Console du Routeur :**

Sélectionnez votre langue préférée pour l'interface de la console du routeur dans le menu déroulant. I2P prend en charge de nombreuses langues, notamment l'anglais, l'allemand, le français, l'espagnol, le russe, le chinois, le japonais et bien d'autres.

**Contributions aux traductions bienvenues :** Si vous remarquez des traductions incomplètes ou incorrectes, vous pouvez aider à améliorer I2P en contribuant au projet de traduction. Contactez les développeurs sur #i2p-dev via IRC ou consultez le rapport d'état des traductions (lien disponible sur la page).

**Mot de passe de la Console du Router :**

Ajoutez une authentification par nom d'utilisateur et mot de passe pour protéger l'accès à votre console router :

- **Nom d'utilisateur** - Saisissez le nom d'utilisateur pour l'accès à la console
- **Mot de passe** - Saisissez le mot de passe pour l'accès à la console
- **Ajouter un utilisateur** - Créer un nouvel utilisateur avec les identifiants spécifiés
- **Supprimer la sélection** - Supprimer les comptes utilisateur existants

**Pourquoi ajouter un mot de passe ?**

- Empêche l'accès local non autorisé à votre console du routeur
- Essentiel si plusieurs personnes utilisent votre ordinateur
- Recommandé si votre console du routeur est accessible sur votre réseau local
- Protège votre configuration I2P et vos paramètres de confidentialité contre toute modification

**Note de sécurité :** La protection par mot de passe n'affecte que l'accès à l'interface web de la console du routeur à l'adresse [I2P Router Console](http://127.0.0.1:7657). Elle ne chiffre pas le trafic I2P et n'empêche pas les applications d'utiliser I2P. Si vous êtes le seul utilisateur de votre ordinateur et que la console du routeur n'écoute que sur localhost (par défaut), un mot de passe peut ne pas être nécessaire.

### Configuration de la famille de routeurs

**URL :** [Configuration WebApp](http://127.0.0.1:7657/configwebapps)

![Configuration des WebApps de la Console du Router](/images/router-console-config-webapps.png)

La page de configuration WebApp vous permet de gérer les applications web Java qui s'exécutent dans votre routeur I2P. Ces applications sont démarrées par le client webConsole et s'exécutent dans la même JVM que le routeur, fournissant des fonctionnalités intégrées accessibles via la console du routeur.

**Qu'est-ce que les WebApps ?**

Les WebApps sont des applications basées sur Java qui peuvent être : - **Des applications complètes** (par ex. I2PSnark pour les torrents) - **Des interfaces pour d'autres clients** qui doivent être activés séparément (par ex. Susidns, I2PTunnel) - **Des applications web sans interface web** (par ex. carnet d'adresses)

**Notes importantes :**

- Une webapp peut être complètement désactivée, ou elle peut simplement être désactivée au démarrage
- Supprimer un fichier war du répertoire webapps désactive complètement la webapp
- Cependant, le fichier .war et le répertoire de la webapp réapparaîtront lorsque vous mettrez à jour votre routeur vers une version plus récente
- **Pour désactiver définitivement une webapp :** Désactivez-la ici, ce qui est la méthode recommandée

**WebApps disponibles :**

| WebApp | Description |
|--------|-------------|
| **i2psnark** | Torrents - Built-in BitTorrent client for I2P |
| **i2ptunnel** | Hidden Services Manager - Configure client and server tunnels |
| **imagegen** | Identification Image Generator - Creates unique identicons |
| **jsonrpc** | jsonrpc.war - JSON-RPC API interface (disabled by default) |
| **routerconsole** | I2P Router Console - The main administrative interface |
| **susidns** | Address Book - Manage I2P addresses and subscriptions |
| **susimail** | Email - Web-based email client for I2P |
**Contrôles :**

Pour chaque webapp : - **Démarrer au lancement ?** - Case à cocher pour activer/désactiver le démarrage automatique - **Contrôle** - Boutons Démarrer/Arrêter pour un contrôle immédiat   - **Arrêter** - Arrête la webapp en cours d'exécution   - **Démarrer** - Démarre une webapp arrêtée

**Boutons de configuration :**

- **Annuler** - Abandonner les modifications et retourner à la page précédente
- **Enregistrer la configuration WebApp** - Enregistrer vos modifications et les appliquer

**Cas d'usage :**

- Arrêtez I2PSnark si vous n'utilisez pas de torrents pour économiser des ressources
- Désactivez jsonrpc si vous n'avez pas besoin d'un accès API
- Arrêtez Susimail si vous utilisez un client de messagerie externe
- Arrêtez temporairement les webapps pour libérer de la mémoire ou résoudre des problèmes

**Conseil de performance :** Désactiver les applications web inutilisées peut réduire l'utilisation de la mémoire et améliorer les performances du router, en particulier sur les systèmes à ressources limitées.

## Help

**URL :** [Aide](http://127.0.0.1:7657/help)

La page d'aide fournit une documentation complète et des ressources pour vous aider à comprendre et utiliser I2P efficacement. Elle sert de point central pour le dépannage, l'apprentissage et l'obtention d'assistance.

**Ce que vous trouverez :**

- **Guide de démarrage rapide** - Informations essentielles pour les nouveaux utilisateurs qui découvrent I2P
- **Foire aux questions (FAQ)** - Réponses aux questions courantes sur l'installation, la configuration et l'utilisation d'I2P
- **Dépannage** - Solutions aux problèmes courants et aux problèmes de connectivité
- **Documentation technique** - Informations détaillées sur les protocoles, l'architecture et les spécifications d'I2P
- **Guides d'application** - Instructions pour utiliser les applications I2P comme les torrents, le courrier électronique et les services cachés
- **Informations sur le réseau** - Comprendre le fonctionnement d'I2P et ce qui le rend sécurisé
- **Ressources d'assistance** - Liens vers les forums, les canaux IRC et le support communautaire

**Obtenir de l'aide :**

Si vous rencontrez des problèmes avec I2P : 1. Consultez la FAQ pour les questions et réponses courantes 2. Examinez la section de dépannage pour votre problème spécifique 3. Visitez le forum I2P sur [i2pforum.i2p](http://i2pforum.i2p) ou [i2pforum.net](https://i2pforum.net) 4. Rejoignez le canal IRC #i2p pour un support communautaire en temps réel 5. Recherchez dans la documentation pour des informations techniques détaillées

**Astuce :** La page d'aide est toujours accessible depuis la barre latérale de la console du routeur, ce qui facilite l'accès à l'assistance à tout moment.

## Performance Graphs

**URL :** [Graphiques de performance](http://127.0.0.1:7657/graphs)

![Graphiques de Performance de la Console du Routeur](/images/router-console-graphs.png)

La page Graphiques de Performance fournit une surveillance visuelle en temps réel des performances de votre router I2P et de l'activité réseau. Ces graphiques vous aident à comprendre l'utilisation de la bande passante, les connexions aux pairs, la consommation de mémoire et la santé globale du router.

**Graphiques disponibles :**

- **Utilisation de la bande passante**
  - **Débit d'envoi bas niveau (octets/sec)** - Débit du trafic sortant
  - **Débit de réception bas niveau (octets/sec)** - Débit du trafic entrant
  - Affiche l'utilisation actuelle, moyenne et maximale de la bande passante
  - Permet de surveiller si vous approchez de vos limites de bande passante configurées

- **Pairs actifs**
  - **router.activePeers moyenné sur 60 sec** - Nombre de pairs avec lesquels vous communiquez activement
  - Indique l'état de santé de votre connectivité réseau
  - Plus de pairs actifs signifie généralement une meilleure construction de tunnels et participation au réseau

- **Utilisation de la mémoire du routeur**
  - **router.memoryUsed moyenné sur 60 sec** - Consommation mémoire de la JVM
  - Affiche l'utilisation mémoire actuelle, moyenne et maximale en Mo
  - Utile pour identifier les fuites mémoire ou déterminer si vous devez augmenter la taille du tas Java

**Configurer l'affichage du graphique :**

Personnalisez l'affichage et le rafraîchissement des graphiques :

- **Taille du graphique** - Définir la largeur (par défaut : 400 pixels) et la hauteur (par défaut : 100 pixels)
- **Période d'affichage** - Plage de temps à afficher (par défaut : 60 minutes)
- **Délai de rafraîchissement** - Fréquence de mise à jour des graphiques (par défaut : 5 minutes)
- **Type de tracé** - Choisir entre l'affichage des moyennes ou des événements
- **Masquer la légende** - Supprimer la légende des graphiques pour gagner de l'espace
- **UTC** - Utiliser l'heure UTC au lieu de l'heure locale sur les graphiques
- **Persistance** - Stocker les données des graphiques sur disque pour l'analyse historique

**Options avancées :**

Cliquez sur **[Select Stats]** pour choisir les statistiques à représenter graphiquement : - Métriques des tunnels (taux de réussite de construction, nombre de tunnels, etc.) - Statistiques de la base de données réseau (netDb) - Statistiques de transport (NTCP2, SSU2) - Performance des tunnels clients - Et bien d'autres métriques détaillées

**Cas d'usage :**

- Surveiller la bande passante pour vous assurer de ne pas dépasser vos limites configurées
- Vérifier la connectivité des pairs lors du dépannage de problèmes réseau
- Suivre l'utilisation de la mémoire pour optimiser les paramètres de heap Java
- Identifier les tendances de performance au fil du temps
- Diagnostiquer les problèmes de construction de tunnel en corrélant les graphiques

**Conseil :** Cliquez sur « Enregistrer les paramètres et redessiner les graphiques » après avoir effectué des modifications pour appliquer votre configuration. Les graphiques se rafraîchiront automatiquement en fonction de votre paramètre de délai de rafraîchissement.
