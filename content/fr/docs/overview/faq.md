---
title: "Questions fréquemment posées"
description: "FAQ complète I2P : aide du router, configuration, reseeds, confidentialité/sécurité, performance et dépannage"
slug: "faq"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

## Aide du Routeur I2P

### Sur quels systèmes I2P peut-il fonctionner ? {#systems}

I2P est écrit en langage de programmation Java. Il a été testé sur Windows, Linux, FreeBSD et OSX. Un portage Android est également disponible.

En termes d'utilisation de la mémoire, I2P est configuré pour utiliser 128 Mo de RAM par défaut. Ceci est suffisant pour la navigation et l'utilisation d'IRC. Cependant, d'autres activités peuvent nécessiter une allocation de mémoire plus importante. Par exemple, si l'on souhaite exécuter un router à bande passante élevée, participer aux torrents I2P ou héberger des services cachés à fort trafic, une quantité de mémoire plus importante est requise.

En termes d'utilisation du processeur, I2P a été testé pour fonctionner sur des systèmes modestes tels que la gamme d'ordinateurs monocartes Raspberry Pi. Comme I2P fait un usage intensif de techniques cryptographiques, un processeur plus puissant sera mieux adapté pour gérer la charge de travail générée par I2P ainsi que les tâches liées au reste du système (c'est-à-dire système d'exploitation, interface graphique, autres processus tels que la navigation Web).

L'utilisation de Sun/Oracle Java ou OpenJDK est recommandée.

### L'installation de Java est-elle nécessaire pour utiliser I2P ? {#java}

Oui, Java est nécessaire pour utiliser I2P Core. Nous incluons Java dans nos installateurs faciles pour Windows, Mac OSX et Linux. Si vous utilisez l'application I2P Android, vous aurez également besoin d'un environnement d'exécution Java comme Dalvik ou ART installé dans la plupart des cas.

### Qu'est-ce qu'un "I2P Site" et comment configurer mon navigateur pour pouvoir les utiliser ? {#I2P-Site}

Un site I2P est un site web normal, sauf qu'il est hébergé à l'intérieur d'I2P. Les sites I2P ont des adresses qui ressemblent à des adresses internet normales, se terminant par ".i2p" d'une manière lisible par l'homme et non cryptographique, pour le bénéfice des utilisateurs. La connexion réelle à un site I2P nécessite de la cryptographie, ce qui signifie que les adresses de sites I2P sont également les longues Destinations "Base64" et les adresses "B32" plus courtes. Vous devrez peut-être effectuer une configuration supplémentaire pour naviguer correctement. La navigation sur les sites I2P nécessite d'activer le proxy HTTP dans votre installation I2P, puis de configurer votre navigateur pour l'utiliser. Pour plus d'informations, consultez la section "Navigateurs" ci-dessous ou le guide "Configuration du navigateur".

### Que signifient les chiffres Actifs x/y dans la console du routeur ? {#active}

Sur la page Pairs de votre console routeur, vous pouvez voir deux nombres - Actifs x/y. Le premier nombre est le nombre de pairs avec lesquels vous avez envoyé ou reçu un message au cours des dernières minutes. Le second nombre est le nombre de pairs vus récemment, celui-ci sera toujours supérieur ou égal au premier nombre.

### Mon routeur a très peu de pairs actifs, est-ce normal ? {#peers}

Oui, cela peut être normal, surtout lorsque le routeur vient d'être démarré. Les nouveaux routeurs ont besoin de temps pour démarrer et se connecter au reste du réseau. Pour améliorer l'intégration au réseau, la disponibilité et les performances, vérifiez ces paramètres :

- **Partager la bande passante** - Si un router est configuré pour partager la bande passante, il acheminera davantage de trafic pour d'autres routers, ce qui contribue à l'intégrer au reste du réseau et améliore également les performances de sa connexion locale. Cela peut être configuré sur la page [http://localhost:7657/config](http://localhost:7657/config).
- **Interface réseau** - Assurez-vous qu'aucune interface n'est spécifiée sur la page [http://localhost:7657/confignet](http://localhost:7657/confignet). Cela peut réduire les performances, sauf si votre ordinateur est multi-hébergé avec plusieurs adresses IP externes.
- **Protocole I2NP** - Assurez-vous que le router est configuré pour attendre des connexions sur un protocole valide pour le système d'exploitation de l'hôte et des paramètres réseau (Avancés) vides. N'entrez pas d'adresse IP dans le champ 'Nom d'hôte' de la page de configuration réseau. Le protocole I2NP que vous sélectionnez ici ne sera utilisé que si vous n'avez pas déjà une adresse accessible. La plupart des connexions sans fil Verizon 4G et 5G aux États-Unis, par exemple, bloquent UDP et ne peuvent pas être jointes via ce protocole. D'autres utiliseraient UDP de force même s'il leur est disponible. Choisissez un paramètre raisonnable parmi les protocoles I2NP listés.

### Je suis opposé à certains types de contenu. Comment puis-je éviter de les distribuer, de les stocker ou d'y accéder ? {#badcontent}

Aucun de ce contenu n'est installé par défaut. Cependant, comme I2P est un réseau pair-à-pair, il est possible que vous rencontriez du contenu interdit par accident. Voici un résumé de la façon dont I2P vous empêche d'être impliqué inutilement dans des violations de vos convictions.

- **Distribution** - Le trafic est interne au réseau I2P, vous n'êtes pas un [nœud de sortie](#exit) (appelé outproxy dans notre documentation).
- **Stockage** - Le réseau I2P ne fait pas de stockage distribué de contenu, cela doit être spécifiquement installé et configuré par l'utilisateur (avec Tahoe-LAFS, par exemple). C'est une fonctionnalité d'un réseau anonyme différent, [Freenet](http://freenetproject.org/). En exécutant un router I2P, vous ne stockez pas de contenu pour qui que ce soit.
- **Accès** - Votre router ne demandera aucun contenu sans votre instruction spécifique de le faire.

### Est-il possible de bloquer I2P ? {#blocking}

Oui, de loin le moyen le plus simple et le plus courant est de bloquer le bootstrap, ou les serveurs "Reseed". Bloquer complètement tout le trafic obfusqué fonctionnerait également (bien que cela casserait beaucoup, beaucoup d'autres choses qui ne sont pas I2P et la plupart ne sont pas prêts à aller aussi loin). Dans le cas du blocage du reseed, il existe un bundle de reseed sur Github, le bloquer bloquera également Github. Vous pouvez effectuer un reseed via un proxy (beaucoup peuvent être trouvés sur Internet si vous ne voulez pas utiliser Tor) ou partager des bundles de reseed sur une base ami-à-ami hors ligne.

### Dans `wrapper.log` je vois une erreur indiquant "`Protocol family unavailable`" lors du chargement de la Console du Routeur {#protocolfamily}

Souvent, cette erreur se produit avec n'importe quel logiciel Java utilisant le réseau sur certains systèmes configurés pour utiliser IPv6 par défaut. Il existe plusieurs façons de résoudre ce problème :

- Sur les systèmes basés sur Linux, vous pouvez exécuter `echo 0 > /proc/sys/net/ipv6/bindv6only`
- Recherchez les lignes suivantes dans `wrapper.config` :
  ```
  #wrapper.java.additional.5=-Djava.net.preferIPv4Stack=true
  #wrapper.java.additional.6=-Djava.net.preferIPv6Addresses=false
  ```
  Si les lignes sont présentes, décommentez-les en supprimant les "#". Si les lignes ne sont pas présentes, ajoutez-les sans les "#".

Une autre option serait de supprimer le `::1` de `~/.i2p/clients.config`

**AVERTISSEMENT** : Pour que les modifications apportées à `wrapper.config` prennent effet, vous devez arrêter complètement le routeur et le wrapper. Cliquer sur *Redémarrer* dans votre console de routeur ne relira PAS ce fichier ! Vous devez cliquer sur *Arrêter*, attendre 11 minutes, puis démarrer I2P.

### La plupart des sites I2P dans I2P sont inaccessibles ? {#down}

Si vous considérez tous les sites I2P qui ont jamais été créés, oui, la plupart sont hors ligne. Les personnes et les sites I2P vont et viennent. Un bon moyen de débuter sur I2P est de consulter une liste de sites I2P actuellement en ligne. [identiguy.i2p](http://identiguy.i2p) répertorie les sites I2P actifs.

### Pourquoi I2P écoute-t-il sur le port 32000 ? {#port32000}

Le wrapper de service Java Tanuki que nous utilisons ouvre ce port — lié à localhost — afin de communiquer avec le logiciel s'exécutant dans la JVM. Lorsque la JVM est lancée, elle reçoit une clé pour pouvoir se connecter au wrapper. Après que la JVM a établi sa connexion au wrapper, le wrapper refuse toute connexion supplémentaire.

Plus d'informations peuvent être trouvées dans la [documentation du wrapper](http://wrapper.tanukisoftware.com/doc/english/prop-port.html).

### Comment configurer mon navigateur ? {#browserproxy}

La configuration du proxy pour différents navigateurs se trouve sur une page séparée avec des captures d'écran. Des configurations plus avancées avec des outils externes, tels que l'extension de navigateur FoxyProxy ou le serveur proxy Privoxy, sont possibles mais pourraient introduire des fuites dans votre configuration.

### Comment puis-je me connecter à IRC au sein d'I2P ? {#irc}

Un tunnel vers le serveur IRC principal au sein d'I2P, Irc2P, est créé lors de l'installation d'I2P (voir la [page de configuration I2PTunnel](http://localhost:7657/i2ptunnel/index.jsp)), et est automatiquement démarré lorsque le router I2P démarre. Pour vous y connecter, configurez votre client IRC pour se connecter à `localhost 6668`. Les utilisateurs de clients de type HexChat peuvent créer un nouveau réseau avec le serveur `localhost/6668` (n'oubliez pas de cocher "Contourner le serveur proxy" si vous avez un serveur proxy configuré). Les utilisateurs de Weechat peuvent utiliser la commande suivante pour ajouter un nouveau réseau :

```
/server add irc2p localhost/6668
```
### Comment configurer mon propre site I2P ? {#myI2P-Site}

La méthode la plus simple consiste à cliquer sur le lien [i2ptunnel](http://127.0.0.1:7657/i2ptunnel/) dans la console du routeur et à créer un nouveau 'Tunnel Serveur'. Vous pouvez servir du contenu dynamique en définissant la destination du tunnel vers le port d'un serveur web existant, tel que Tomcat ou Jetty. Vous pouvez également servir du contenu statique. Pour cela, définissez la destination du tunnel sur : `0.0.0.0 port 7659` et placez le contenu dans le répertoire `~/.i2p/eepsite/docroot/`. (Sur les systèmes non-Linux, cela peut se trouver à un emplacement différent. Vérifiez la console du routeur.) Le logiciel 'eepsite' est fourni dans le paquet d'installation I2P et est configuré pour démarrer automatiquement au lancement d'I2P. Le site par défaut ainsi créé est accessible à l'adresse http://127.0.0.1:7658. Cependant, votre 'eepsite' est également accessible aux autres via votre fichier de clés eepsite, situé à : `~/.i2p/eepsite/i2p/eepsite.keys`. Pour en savoir plus, lisez le fichier readme à l'adresse : `~/.i2p/eepsite/README.txt`.

### Si j'héberge un site web sur I2P à la maison, contenant uniquement du HTML et du CSS, est-ce dangereux ? {#hosting}

Cela dépend de votre adversaire et de votre modèle de menace. Si vous êtes uniquement préoccupé par les violations de « confidentialité » des entreprises, les criminels typiques et la censure, alors ce n'est pas vraiment dangereux. Les forces de l'ordre vous trouveront probablement de toute façon si elles le veulent vraiment. N'héberger que lorsque vous avez un navigateur d'utilisateur domestique normal (internet) en cours d'exécution rendra vraiment difficile de savoir qui héberge cette partie. Veuillez considérer l'hébergement de votre site I2P comme l'hébergement de tout autre service - c'est aussi dangereux - ou sûr - que vous le configurez et le gérez vous-même.

Note : Il existe déjà un moyen de séparer l'hébergement d'un service i2p (destination) du routeur i2p. Si vous [comprenez comment](/docs/overview/tech-intro#i2pservices) cela fonctionne, vous pouvez simplement configurer une machine séparée comme serveur pour le site web (ou service) qui sera accessible publiquement et transférer cela vers le serveur web via un tunnel SSH [très] sécurisé ou utiliser un système de fichiers partagé et sécurisé.

### Comment I2P trouve-t-il les sites web ".i2p" ? {#addresses}

L'application Carnet d'adresses I2P associe des noms lisibles par l'homme à des destinations à long terme, liées à des services, ce qui la rend plus similaire à un fichier hosts ou à une liste de contacts qu'à une base de données réseau ou à un service DNS. Elle fonctionne également en mode local d'abord : il n'existe pas d'espace de noms global reconnu, vous décidez en fin de compte à quoi correspond un domaine .i2p donné. La solution intermédiaire est un service appelé "Jump Service" qui fournit un nom lisible par l'homme en vous redirigeant vers une page où il vous sera demandé "Autorisez-vous le routeur I2P à appeler $SITE_CRYPTO_KEY par le nom $SITE_NAME.i2p" ou quelque chose dans ce genre. Une fois l'entrée dans votre carnet d'adresses, vous pouvez générer vos propres URL de saut pour aider à partager le site avec d'autres.

### Comment ajouter des adresses au Carnet d'adresses ? {#addressbook}

Vous ne pouvez pas ajouter une adresse sans connaître au moins le base32 ou le base64 du site que vous souhaitez visiter. Le "nom d'hôte" qui est lisible par l'humain n'est qu'un alias pour l'adresse cryptographique, qui correspond au base32 ou au base64. Sans l'adresse cryptographique, il n'y a aucun moyen d'accéder à un site I2P, c'est voulu par conception. La distribution de l'adresse aux personnes qui ne la connaissent pas encore relève généralement de la responsabilité du fournisseur de service Jump. Visiter un site I2P inconnu déclenchera l'utilisation d'un service Jump. stats.i2p est le service Jump le plus fiable.

Si vous hébergez un site via i2ptunnel, il n'aura pas encore d'enregistrement auprès d'un service de saut. Pour lui attribuer une URL localement, visitez la page de configuration et cliquez sur le bouton « Add to Local Address Book ». Ensuite, rendez-vous sur http://127.0.0.1:7657/dns pour rechercher l'URL addresshelper et la partager.

### Quels ports I2P utilise-t-il ? {#ports}

Les ports utilisés par I2P peuvent être divisés en 2 sections :

1. Ports exposés à Internet, qui sont utilisés pour la communication avec d'autres routeurs I2P
2. Ports locaux, pour les connexions locales

Ceux-ci sont décrits en détail ci-dessous.

#### 1. Ports exposés à Internet

Remarque : Depuis la version 0.7.8, les nouvelles installations n'utilisent plus le port 8887 ; un port aléatoire entre 9000 et 31000 est sélectionné lors de la première exécution du programme. Le port sélectionné est affiché sur la [page de configuration](http://127.0.0.1:7657/confignet) du routeur.

**SORTANT**

- UDP depuis le port aléatoire listé sur la [page de configuration](http://127.0.0.1:7657/confignet) vers des ports UDP distants arbitraires, permettant les réponses
- TCP depuis des ports hauts aléatoires vers des ports TCP distants arbitraires
- UDP sortant sur le port 123, permettant les réponses. Ceci est nécessaire pour la synchronisation horaire interne d'I2P (via SNTP - interrogeant un hôte SNTP aléatoire dans pool.ntp.org ou un autre serveur que vous spécifiez)

**ENTRANT**

- (Optionnel, recommandé) UDP vers le port indiqué sur la [page de configuration](http://127.0.0.1:7657/confignet) depuis des emplacements arbitraires
- (Optionnel, recommandé) TCP vers le port indiqué sur la [page de configuration](http://127.0.0.1:7657/confignet) depuis des emplacements arbitraires
- Le TCP entrant peut être désactivé sur la [page de configuration](http://127.0.0.1:7657/confignet)

#### 2. Ports I2P locaux

Les ports I2P locaux n'écoutent que les connexions locales par défaut, sauf indication contraire :

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">PORT</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">PURPOSE</th>
      <th style="border:1px solid var(--color-border); padding:0.6rem; text-align:left; background:var(--color-bg-secondary);">DESCRIPTION</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">1900</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">UPnP SSDP UDP multicast listener</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Cannot be changed. Binds to all interfaces. May be disabled on <a href="http://127.0.0.1:7657/confignet">confignet</a>.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">2827</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">BOB bridge</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">A higher level socket API for clients. Disabled by default. May be enabled/disabled on <a href="http://127.0.0.1:7657/configclients">configclients</a>. May be changed in the bob.config file.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4444</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HTTP proxy</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Configured on <a href="http://127.0.0.1:7657/configclients">configclients</a>, go to the page <a href="http://127.0.0.1:7657/i2ptunnel/">i2ptunnel</a> to start/stop it and on the page <a href="http://127.0.0.1:7657/i2ptunnel/web/0">I2P HTTP Proxy</a> to configure it. Include in your browser's proxy configuration for HTTP</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">4445</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">HTTPS proxy</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Configured on <a href="http://127.0.0.1:7657/configclients">configclients</a>, go to the page <a href="http://127.0.0.1:7657/i2ptunnel/">i2ptunnel</a> to start/stop it and on the page <a href="http://127.0.0.1:7657/i2ptunnel/web/1">I2P HTTPS Proxy</a> to configure it. Include in your browser's proxy configuration for HTTPS</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">6668</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">IRC proxy</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">A tunnel to the inside-the-I2P IRC network. Disabled by default. Configured on the page <a href="http://127.0.0.1:7657/i2ptunnel/web/2">irc.postman.i2p (IRC proxy)</a> and may be enabled/disabled on the page <a href="http://127.0.0.1:7657/i2ptunnel/">i2ptunnel</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7654</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2CP (client protocol) port</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">For advanced client usage. Do not expose to an external network.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7656</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">SAM bridge</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">A socket API for clients. Disabled by default. May be enabled/disabled on <a href="http://127.0.0.1:7657/configclients">configclients</a> and configured on <a href="http://127.0.0.1:7657/sam">sam</a>.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7657 (or 7658 via SSL)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Router console</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">The router console provides valuable information about your router and the network, in addition to giving you access to configure your router and its associated applications.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7659</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">'eepsite' - an example webserver (Jetty)</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Included in the <code>i2pinstall</code> and <code>i2pupdate</code> packages - may be disabled if another webserver is available. May be configured on the page <a href="http://127.0.0.1:7657/i2ptunnel/web/3">eepsite</a> and disabled on the page <a href="http://127.0.0.1:7657/i2ptunnel/">i2ptunnel</a></td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">7660</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">I2PTunnel UDP port for SSH</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Required for Grizzled's/novg's UDP support. Instances disabled by default. May be enabled/disabled and configured to use a different port on the page <a href="http://127.0.0.1:7657/i2ptunnel/">i2ptunnel</a>.</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">123</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">NTP Port</td>
      <td style="border:1px solid var(--color-border); padding:0.6rem;">Used by <a href="http://127.0.0.1:7657/confignet">NTP Time Sync</a>. May be disabled/changed.</td>
    </tr>
  </tbody>
</table>
### Il me manque beaucoup d'hôtes dans mon carnet d'adresses. Quels sont les bons liens d'abonnement ? {#subscriptions}

Le carnet d'adresses se trouve à l'adresse [http://localhost:7657/dns](http://localhost:7657/dns) où vous trouverez plus d'informations.

**Quels sont les bons liens d'abonnement aux carnets d'adresses ?**

Vous pouvez essayer ce qui suit :

- [http://stats.i2p/cgi-bin/newhosts.txt](http://stats.i2p/cgi-bin/newhosts.txt)
- [http://identiguy.i2p/hosts.txt](http://identiguy.i2p/hosts.txt)

### Comment puis-je accéder à la console web depuis mes autres machines ou la protéger par mot de passe ? {#remote_webconsole}

Pour des raisons de sécurité, la console d'administration du routeur n'écoute par défaut que les connexions sur l'interface locale.

Il existe deux méthodes pour accéder à la console à distance :

1. Tunnel SSH
2. Configurer votre console pour qu'elle soit accessible sur une adresse IP publique avec un nom d'utilisateur et un mot de passe

Ceux-ci sont détaillés ci-dessous :

**Méthode 1 : Tunnel SSH**

Si vous utilisez un système d'exploitation de type Unix, c'est la méthode la plus simple pour accéder à distance à votre console I2P. (Note : un logiciel serveur SSH est disponible pour les systèmes fonctionnant sous Windows, par exemple [https://github.com/PowerShell/Win32-OpenSSH](https://github.com/PowerShell/Win32-OpenSSH))

Une fois que vous avez configuré l'accès SSH à votre système, le drapeau '-L' est passé à SSH avec les arguments appropriés - par exemple :

```
ssh -L 7657:localhost:7657 (System_IP)
```
où '(System_IP)' est remplacé par l'adresse IP de votre système. Cette commande transfère le port 7657 (le numéro avant le premier deux-points) vers le port 7657 du système distant (tel que spécifié par la chaîne 'localhost' entre le premier et le second deux-points) (le numéro après le second deux-points). Votre console I2P distante sera désormais accessible sur votre système local à l'adresse 'http://localhost:7657' et restera disponible tant que votre session SSH est active.

Si vous souhaitez démarrer une session SSH sans lancer de shell sur le système distant, vous pouvez ajouter l'option '-N' :

```
ssh -NL 7657:localhost:7657 (System_IP)
```
**Méthode 2 : Configurer votre console pour qu'elle soit accessible sur une adresse IP publique avec un nom d'utilisateur et un mot de passe**

1. Ouvrez `~/.i2p/clients.config` et remplacez :
   ```
   clientApp.0.args=7657 ::1,127.0.0.1 ./webapps/
   ```
   par :
   ```
   clientApp.0.args=7657 ::1,127.0.0.1,(System_IP) ./webapps/
   ```
   où vous remplacez (System_IP) par l'adresse IP publique de votre système

2. Allez sur [http://localhost:7657/configui](http://localhost:7657/configui) et ajoutez un nom d'utilisateur et un mot de passe pour la console si vous le souhaitez - L'ajout d'un nom d'utilisateur et d'un mot de passe est fortement recommandé pour sécuriser votre console I2P contre les manipulations, qui pourraient conduire à une désanonymisation.

3. Accédez à [http://localhost:7657/index](http://localhost:7657/index) et cliquez sur "Graceful restart", ce qui redémarre la JVM et recharge les applications clientes

Une fois démarré, vous devriez maintenant pouvoir accéder à votre console à distance. Chargez la console du router à l'adresse `http://(System_IP):7657` et vous serez invité à saisir le nom d'utilisateur et le mot de passe que vous avez spécifiés à l'étape 2 ci-dessus si votre navigateur prend en charge la fenêtre d'authentification.

NOTE : Vous pouvez spécifier 0.0.0.0 dans la configuration ci-dessus. Cela spécifie une interface, pas un réseau ou un masque de réseau. 0.0.0.0 signifie "se lier à toutes les interfaces", il peut donc être accessible sur 127.0.0.1:7657 ainsi que sur n'importe quelle IP LAN/WAN. Soyez prudent lors de l'utilisation de cette option car la console sera disponible sur TOUTES les adresses configurées sur votre système.

### Comment puis-je utiliser des applications depuis mes autres machines ? {#remote_i2cp}

Veuillez consulter la réponse précédente pour les instructions sur l'utilisation du transfert de port SSH, et consultez également cette page dans votre console : [http://localhost:7657/configi2cp](http://localhost:7657/configi2cp)

### Est-il possible d'utiliser I2P comme proxy SOCKS ? {#socks}

Le proxy SOCKS est fonctionnel depuis la version 0.7.1. SOCKS 4/4a/5 sont pris en charge. I2P n'a pas d'outproxy SOCKS, son utilisation est donc limitée à I2P uniquement.

De nombreuses applications divulguent des informations sensibles qui pourraient vous identifier sur Internet et c'est un risque dont il faut être conscient lors de l'utilisation du proxy SOCKS I2P. I2P filtre uniquement les données de connexion, mais si le programme que vous avez l'intention d'utiliser envoie ces informations en tant que contenu, I2P n'a aucun moyen de protéger votre anonymat. Par exemple, certaines applications de messagerie enverront l'adresse IP de la machine sur laquelle elles s'exécutent à un serveur de messagerie. Nous recommandons des outils ou applications spécifiques à I2P (comme [I2PSnark](http://localhost:7657/i2psnark/) pour les torrents), ou des applications dont il est connu qu'elles sont sûres à utiliser avec I2P, qui incluent des plugins populaires disponibles sur [Firefox](https://www.mozilla.org/).

### Comment accéder à IRC, BitTorrent ou d'autres services sur Internet classique ? {#proxy_other}

Il existe des services appelés Outproxies qui font le pont entre I2P et Internet, comme les nœuds de sortie Tor. La fonctionnalité outproxy par défaut pour HTTP et HTTPS est fournie par `exit.stormycloud.i2p` et est gérée par StormyCloud Inc. Elle est configurée dans le proxy HTTP. De plus, pour aider à protéger l'anonymat, I2P ne vous permet pas par défaut d'établir des connexions anonymes vers Internet classique. Veuillez consulter la page [Socks Outproxy](/docs/api/socks#outproxy) pour plus d'informations.

---

## Reseeds

### Mon routeur fonctionne depuis plusieurs minutes et n'a aucune connexion ou très peu de connexions {#reseed}

Vérifiez d'abord la page [http://127.0.0.1:7657/netdb](http://127.0.0.1:7657/netdb) dans la Console du Routeur – votre base de données réseau. Si vous ne voyez aucun routeur listé depuis I2P mais que la console indique que vous devriez être derrière un pare-feu, alors vous ne pouvez probablement pas vous connecter aux serveurs reseed. Si vous voyez d'autres routeurs I2P listés, essayez de réduire le nombre de connexions maximum [http://127.0.0.1:7657/config](http://127.0.0.1:7657/config) peut-être que votre routeur ne peut pas gérer autant de connexions.

### Comment réamorcer manuellement ? {#manual_reseed}

Dans des circonstances normales, I2P vous connectera automatiquement au réseau en utilisant nos liens de démarrage. Si une perturbation d'Internet empêche le démarrage depuis les serveurs reseed, un moyen facile de démarrer est d'utiliser le navigateur Tor (par défaut, il s'ouvre sur localhost), qui fonctionne très bien avec [http://127.0.0.1:7657/configreseed](http://127.0.0.1:7657/configreseed). Il est également possible de réamorcer (reseed) un routeur I2P manuellement.

Lors de l'utilisation du navigateur Tor pour réamorcer (reseed), vous pouvez sélectionner plusieurs URL à la fois et continuer. Bien que la valeur par défaut qui est de 2 (parmi les multiples URL) fonctionne également, elle sera lente.

---

## Confidentialité-Sécurité

### Mon routeur est-il un "nœud de sortie" (outproxy) vers l'Internet régulier ? Je ne veux pas qu'il le soit. {#exit}

Non, votre router participe au transport du trafic chiffré de bout en bout à travers le réseau i2p vers un point de terminaison de tunnel aléatoire, généralement pas un outproxy, mais aucun trafic n'est transmis entre votre router et Internet au niveau de la couche transport. En tant qu'utilisateur final, vous ne devriez pas exécuter un outproxy si vous n'êtes pas compétent en administration système et réseau.

### Est-il facile de détecter l'utilisation d'I2P en analysant le trafic réseau ? {#detection}

Le trafic I2P ressemble généralement à du trafic UDP, et pas beaucoup plus – et faire en sorte qu'il ne ressemble pas à beaucoup plus est un objectif. Il prend également en charge TCP. Avec un certain effort, l'analyse passive du trafic peut être en mesure de classifier le trafic comme « I2P », mais nous espérons que le développement continu de l'obscurcissement du trafic réduira cela davantage. Même une couche d'obscurcissement de protocole assez simple comme obfs4 empêchera les censeurs de bloquer I2P (c'est un objectif que I2P déploie).

### L'utilisation d'I2P est-elle sûre ? {#safe}

Cela dépend de votre modèle de menace personnel. Pour la plupart des gens, I2P est beaucoup plus sûr que de ne pas utiliser de protection du tout. Certains autres réseaux (comme Tor, mixminion/mixmaster) sont probablement plus sûrs contre certains adversaires. Par exemple, le trafic I2P n'utilise pas TLS/SSL, il n'a donc pas les problèmes du "maillon le plus faible" que Tor a. I2P a été utilisé par beaucoup de personnes en Syrie lors du "Printemps arabe", et récemment le projet a connu une croissance plus importante dans les installations linguistiques plus petites d'I2P au Proche et Moyen-Orient. Le point le plus important à noter ici est qu'I2P est une technologie et vous avez besoin d'un guide/tutoriel pour améliorer votre vie privée/anonymat sur Internet. Vérifiez également votre navigateur ou importez le moteur de recherche d'empreintes numériques pour bloquer les attaques par empreinte numérique avec un ensemble de données très important (c'est-à-dire : longues traînes typiques / structure de données diversifiée très précise) concernant de nombreux éléments d'environnement et n'utilisez pas de VPN pour réduire tous les risques qui en découlent comme le comportement du cache TLS lui-même et la construction technique de l'entreprise fournisseur qui peut être piratée plus facilement qu'un système de bureau personnel. L'utilisation d'un Tor V-Browser isolé avec ses excellentes protections anti-empreintes numériques et une protection appguard globale en temps réel n'autorisant que les communications système nécessaires et une dernière utilisation en VM avec des scripts de désactivation anti-espionnage et un live-CD pour supprimer tout "risque presque permanent possible" et réduire tous les risques par une probabilité décroissante peuvent être une bonne option dans un réseau public et un modèle de risque individuel élevé et pourraient être le mieux que vous puissiez faire avec cet objectif pour l'utilisation d'I2P.

### Je vois les adresses IP de tous les autres nœuds I2P dans la console du routeur. Cela signifie-t-il que mon adresse IP est visible par les autres ? {#netdb_ip}

Oui, pour les autres nœuds I2P qui connaissent votre router. Nous utilisons cela pour nous connecter avec le reste du réseau I2P. Les adresses sont physiquement situées dans des objets "routerInfos (clé,valeur)", soit récupérés à distance, soit reçus d'un pair. Les "routerInfos" contiennent certaines informations (certaines ajoutées de manière opportuniste et optionnelle), "publiées par le pair", concernant le router lui-même pour le démarrage. Aucune donnée concernant les clients n'est présente dans cet objet. En regardant de plus près sous le capot, vous constaterez que tout le monde est comptabilisé avec le nouveau type de création d'identifiants appelé "hachages SHA-256 (low=hachage positif(-clé), high=hachage négatif(+clé))". Le réseau I2P possède sa propre base de données de routerInfos créée lors du téléchargement et de l'indexation, mais cela dépend profondément de la réalisation des tables clé/valeur et de la topologie du réseau ainsi que de l'état de charge / état de bande passante et des probabilités de routage pour les stockages dans les composants de base de données.

### L'utilisation d'un outproxy est-elle sûre ? {#proxy_safe}

Cela dépend de votre définition de « sûr ». Les outproxies sont excellents lorsqu'ils fonctionnent, mais malheureusement ils sont gérés volontairement par des personnes qui peuvent perdre leur intérêt ou ne pas avoir les ressources nécessaires pour les maintenir 24h/24 et 7j/7 – veuillez noter que vous pourriez connaître des périodes pendant lesquelles les services sont indisponibles, interrompus ou peu fiables, et nous ne sommes pas associés à ce service et n'avons aucune influence sur celui-ci.

Les outproxys eux-mêmes peuvent voir votre trafic entrant et sortant, à l'exception des données HTTPS/SSL chiffrées de bout en bout, tout comme votre FAI peut voir votre trafic entrant et sortant de votre ordinateur. Si vous faites confiance à votre FAI, ce ne serait pas pire avec l'outproxy.

### Qu'en est-il des attaques de « désanonymisation » ? {#deanon}

Pour une explication très détaillée, consultez nos articles sur le [Modèle de menace](/docs/overview/threat-model). En général, la désanonymisation n'est pas triviale, mais possible si vous n'êtes pas suffisamment prudent.

---

## Accès Internet/Performances

### Je ne peux pas accéder aux sites Internet classiques via I2P. {#outproxy}

Le proxy vers les sites Internet (eepsites qui sont accessibles sur Internet) est fourni en tant que service aux utilisateurs I2P par des fournisseurs non-bloquants. Ce service n'est pas l'objectif principal du développement d'I2P, et est fourni sur une base volontaire. Les eepsites hébergés sur I2P devraient toujours fonctionner sans outproxy. Les outproxies sont une commodité mais ils ne sont pas parfaits par conception et ne constituent pas une grande partie du projet. Sachez qu'ils peuvent ne pas être en mesure de fournir le service de haute qualité que d'autres services d'I2P peuvent offrir.

### Je ne peux pas accéder aux sites https:// ou ftp:// via I2P. {#https}

Le proxy HTTP par défaut prend en charge uniquement la redirection sortante HTTP et HTTPS.

### Pourquoi mon routeur utilise-t-il trop de CPU ? {#cpu}

Tout d'abord, assurez-vous d'avoir la dernière version de chaque composant lié à I2P – les versions plus anciennes contenaient des sections de code consommant inutilement du processeur. Il existe également un [journal des performances](/docs/overview/performance) qui documente certaines des améliorations des performances d'I2P au fil du temps.

### Mes pairs actifs / pairs connus / tunnels participants / connexions / bande passante varient considérablement dans le temps ! Y a-t-il un problème ? {#vary}

La stabilité générale du réseau I2P est un domaine de recherche en cours. Une partie importante de cette recherche se concentre sur la façon dont de petits changements dans les paramètres de configuration modifient le comportement du router. Comme I2P est un réseau pair-à-pair, les actions des autres pairs auront une influence sur les performances de votre router.

### Qu'est-ce qui rend les téléchargements, les torrents, la navigation web et tout le reste plus lents sur I2P par rapport à l'internet classique ? {#slow}

I2P dispose de différentes protections qui ajoutent un routage supplémentaire et des couches de chiffrement additionnelles. Il fait également rebondir le trafic à travers d'autres pairs (Tunnels) qui ont leur propre vitesse et qualité, certains sont lents, d'autres rapides. Cela ajoute beaucoup de surcharge et de trafic à différents rythmes dans différentes directions. Par conception, tous ces éléments le rendent plus lent par rapport à une connexion directe sur Internet, mais beaucoup plus anonyme et toujours suffisamment rapide pour la plupart des usages.

Ci-dessous un exemple présenté avec une explication pour aider à fournir un contexte sur les considérations de latence et de bande passante lors de l'utilisation d'I2P.

Considérez le diagramme ci-dessous. Il représente une connexion entre un client effectuant une requête via I2P, un serveur recevant la requête via I2P puis répondant également via I2P. Le circuit emprunté par la requête est également représenté.

D'après le diagramme, considérons que les boîtes étiquetées 'P', 'Q' et 'R' représentent un tunnel sortant pour 'A' et que les boîtes étiquetées 'X', 'Y' et 'Z' représentent un tunnel sortant pour 'B'. De même, les boîtes étiquetées 'X', 'Y' et 'Z' représentent un tunnel entrant pour 'B' tandis que les boîtes étiquetées 'P_1', 'Q_1' et 'R_1' représentent un tunnel entrant pour 'A'. Les flèches entre les boîtes indiquent le sens du trafic. Le texte au-dessus et en dessous des flèches détaille quelques exemples de bande passante entre une paire de sauts ainsi que des exemples de latences.

Lorsque le client et le serveur utilisent tous deux des tunnels à 3 sauts tout au long du processus, un total de 12 autres routeurs I2P sont impliqués dans le relais du trafic. 6 pairs relayent le trafic du client vers le serveur, qui est divisé en un tunnel sortant à 3 sauts depuis 'A' ('P', 'Q', 'R') et un tunnel entrant à 3 sauts vers 'B' ('X', 'Y', 'Z'). De même, 6 pairs relayent le trafic du serveur vers le client.

Tout d'abord, nous pouvons considérer la latence - le temps nécessaire pour qu'une requête d'un client traverse le réseau I2P, atteigne le serveur et revienne au client. En additionnant toutes les latences, nous constatons que :

```
    40 + 100 + 20 + 60 + 80 + 10 + 30 ms        (client to server)
  + 60 + 40 + 80 + 60 + 100 + 20 + 40 ms        (server to client)
  -----------------------------------
  TOTAL:                          740 ms
```
Le temps d'aller-retour total dans notre exemple s'élève à 740 ms - certainement beaucoup plus élevé que ce que l'on observerait normalement en naviguant sur des sites web Internet classiques.

Deuxièmement, nous pouvons considérer la bande passante disponible. Celle-ci est déterminée par le lien le plus lent entre les sauts du client au serveur ainsi que lorsque le trafic est transmis par le serveur vers le client. Pour le trafic allant du client vers le serveur, nous voyons que la bande passante disponible dans notre exemple entre les sauts 'R' & 'X' ainsi qu'entre les sauts 'X' & 'Y' est de 32 KB/s. Malgré une bande passante disponible plus élevée entre les autres sauts, ces sauts agiront comme un goulot d'étranglement et limiteront la bande passante maximale disponible pour le trafic de 'A' à 'B' à 32 KB/s. De même, en traçant le chemin du serveur vers le client, on constate qu'il y a une bande passante maximale de 64 KB/s - entre les sauts 'Z_1' & 'Y_1', 'Y_1' & 'X_1' et 'Q_1' & 'P_1'.

Nous recommandons d'augmenter vos limites de bande passante. Cela aide le réseau en augmentant la quantité de bande passante disponible, ce qui améliorera en retour votre expérience I2P. Les paramètres de bande passante se trouvent sur la page [http://localhost:7657/config](http://localhost:7657/config). Veuillez tenir compte des limites de votre connexion internet déterminées par votre FAI, et ajustez vos paramètres en conséquence.

Nous recommandons également de définir une quantité suffisante de bande passante partagée - cela permet aux tunnels participants d'être routés via votre routeur I2P. Autoriser le trafic participant maintient votre routeur bien intégré dans le réseau et améliore vos vitesses de transfert.

I2P est un projet en cours de développement. De nombreuses améliorations et corrections sont mises en œuvre et, de manière générale, utiliser la dernière version améliorera vos performances. Si ce n'est pas déjà fait, installez la dernière version.

### Je pense avoir trouvé un bug, où puis-je le signaler ? {#bug}

Vous pouvez signaler tout bug ou problème que vous rencontrez sur notre système de suivi des bugs, qui est accessible à la fois sur Internet classique et sur I2P. Nous avons un forum de discussion, également disponible sur I2P et sur Internet classique. Vous pouvez également rejoindre notre canal IRC : soit via notre réseau IRC, IRC2P, soit sur Freenode.

- **Notre Bugtracker :**
  - Internet non privé : [https://i2pgit.org/I2P_Developers/i2p.i2p/issues](https://i2pgit.org/I2P_Developers/i2p.i2p/issues)
  - Sur I2P : [http://git.idk.i2p/I2P_Developers/i2p.i2p/issues](http://git.idk.i2p/I2P_Developers/i2p.i2p/issues)
- **Nos forums :** [i2pforum.i2p](http://i2pforum.i2p/)
- **Coller les logs :** Vous pouvez coller tous les logs intéressants sur un service de partage tel que les services internet non privés listés sur le [Wiki PrivateBin](https://github.com/PrivateBin/PrivateBin/wiki/PrivateBin-Directory), ou un service de partage I2P tel que cette [instance PrivateBin](http://paste.crypthost.i2p) ou ce [service de partage sans Javascript](http://pasta-nojs.i2p) et faire un suivi sur IRC dans #i2p
- **IRC :** Rejoignez #i2p-dev Discutez avec les développeurs sur IRC

Veuillez inclure les informations pertinentes de la page des journaux du router disponible à : [http://127.0.0.1:7657/logs](http://127.0.0.1:7657/logs). Nous vous demandons de partager tout le texte de la section « I2P Version and Running Environment » ainsi que toutes les erreurs ou avertissements affichés dans les différents journaux présents sur la page.

---

### J'ai une question ! {#question}

Génial ! Retrouvez-nous sur IRC :

- sur `irc.freenode.net` canal `#i2p`
- sur `IRC2P` canal `#i2p`

ou postez sur [le forum](http://i2pforum.i2p/) et nous le publierons ici (avec la réponse, espérons-le).
