---
title: "Développement d'applications"
description: "Pourquoi développer des applications spécifiques à I2P, concepts clés, options de développement et guide de démarrage simple"
slug: "applications"
lastUpdated: "2025-10"
accurateFor: "2.10.0"
type: docs
---

## Pourquoi écrire du code spécifique à I2P ?

Il existe plusieurs façons d'utiliser des applications dans I2P. En utilisant [I2PTunnel](/docs/api/i2ptunnel/), vous pouvez utiliser des applications ordinaires sans avoir besoin de programmer une prise en charge explicite d'I2P. Cela est très efficace pour les scénarios client-serveur, où vous devez vous connecter à un seul site web. Vous pouvez simplement créer un tunnel en utilisant I2PTunnel pour vous connecter à ce site web, comme illustré dans la Figure 1.

Si votre application est distribuée, elle nécessitera des connexions vers un grand nombre de pairs. En utilisant I2PTunnel, vous devrez créer un nouveau tunnel pour chaque pair que vous souhaitez contacter, comme illustré dans la Figure 2. Ce processus peut bien sûr être automatisé, mais l'exécution de nombreuses instances I2PTunnel crée une surcharge importante. De plus, avec de nombreux protocoles, vous devrez forcer tout le monde à utiliser le même ensemble de ports pour tous les pairs — par exemple, si vous voulez exécuter de manière fiable un chat DCC, tout le monde doit convenir que le port 10001 est Alice, le port 10002 est Bob, le port 10003 est Charlie, et ainsi de suite, puisque le protocole inclut des informations spécifiques TCP/IP (hôte et port).

Les applications réseau générales envoient souvent beaucoup de données supplémentaires qui pourraient être utilisées pour identifier les utilisateurs. Les noms d'hôtes, numéros de port, fuseaux horaires, jeux de caractères, etc. sont souvent envoyés sans en informer l'utilisateur. Par conséquent, concevoir le protocole réseau spécifiquement en gardant l'anonymat à l'esprit peut éviter de compromettre l'identité des utilisateurs.

Il y a également des considérations d'efficacité à examiner lors de la détermination de la manière d'interagir au-dessus d'I2P. La bibliothèque streaming et les éléments construits par-dessus fonctionnent avec des handshakes similaires à TCP, tandis que les protocoles I2P de base (I2NP et I2CP) sont strictement basés sur des messages (comme UDP ou dans certains cas IP brut). La distinction importante est qu'avec I2P, la communication s'opère sur un réseau long et large — chaque message de bout en bout aura des latences non négligeables, mais peut contenir des charges utiles allant jusqu'à plusieurs Ko. Une application qui nécessite une simple requête et réponse peut se débarrasser de tout état et réduire la latence encourue par les handshakes de démarrage et de fermeture en utilisant des datagrammes (au mieux de leurs possibilités) sans avoir à se soucier de la détection de MTU ou de la fragmentation des messages.

<figure style="text-align:center; margin: 2rem 0;">
  <img src="/images/i2ptunnel_serverclient.png" alt="Creating a server-client connection using I2PTunnel only requires creating a single tunnel." />
  <figcaption>Figure 1: Creating a server-client connection using I2PTunnel only requires creating a single tunnel.</figcaption>
</figure>
<figure style="text-align:center; margin: 2rem 0;">
  <img src="/images/i2ptunnel_peertopeer.png" alt="Setting up connections for a peer-to-peer applications requires a very large amount of tunnels." />
  <figcaption>Figure 2: Setting up connections for a peer-to-peer applications requires a very large amount of tunnels.</figcaption>
</figure>
En résumé, plusieurs raisons de développer du code spécifique à I2P :

- La création d'un grand nombre d'instances I2PTunnel consomme une quantité non négligeable de ressources, ce qui pose problème pour les applications distribuées (un nouveau tunnel est requis pour chaque pair).
- Les protocoles réseau généraux envoient souvent beaucoup de données supplémentaires qui peuvent être utilisées pour identifier les utilisateurs. Programmer spécifiquement pour I2P permet la création d'un protocole réseau qui ne divulgue pas de telles informations, gardant les utilisateurs anonymes et en sécurité.
- Les protocoles réseau conçus pour être utilisés sur Internet classique peuvent être inefficaces sur I2P, qui est un réseau avec une latence beaucoup plus élevée.

I2P prend en charge une [interface de plugins](/docs/specs/plugin/) standard pour les développeurs afin que les applications puissent être facilement intégrées et distribuées.

Les applications écrites en Java et accessibles/exécutables via une interface HTML au moyen du fichier standard webapps/app.war peuvent être considérées pour inclusion dans la distribution I2P.

## Concepts importants

Il y a quelques changements qui nécessitent un ajustement lors de l'utilisation d'I2P :

### Destinations

Une application fonctionnant sur I2P envoie des messages depuis et reçoit des messages vers un point de terminaison unique cryptographiquement sécurisé — une "destination". En termes TCP ou UDP, une destination pourrait (en grande partie) être considérée comme l'équivalent d'une paire nom d'hôte plus numéro de port, bien qu'il existe quelques différences.

- Une destination I2P est en elle-même une construction cryptographique — toutes les données qui lui sont envoyées sont chiffrées comme s'il y avait un déploiement universel d'IPsec avec l'emplacement (anonymisé) du point terminal signé comme s'il y avait un déploiement universel de DNSSEC.
- Les destinations I2P sont des identifiants mobiles — elles peuvent être déplacées d'un router I2P à un autre (ou même fonctionner en « multihébergement » — opérer sur plusieurs routers simultanément). Cela diffère considérablement du monde TCP ou UDP où un seul point terminal (port) doit rester sur un seul hôte.
- Les destinations I2P sont volumineuses et peu élégantes — en coulisses, elles contiennent une clé publique ElGamal de 2048 bits pour le chiffrement, une clé publique DSA de 1024 bits pour la signature, et un certificat de taille variable, qui peut contenir une preuve de travail ou des données masquées.

Il existe des moyens de faire référence à ces destinations volumineuses et disgracieuses par des noms courts et élégants (par exemple « irc.duck.i2p »), mais ces techniques ne garantissent pas l'unicité globale (puisqu'elles sont stockées localement dans une base de données sur la machine de chaque personne) et le mécanisme actuel n'est pas particulièrement évolutif ni sécurisé (les mises à jour de la liste d'hôtes sont gérées à l'aide d'« abonnements » aux services de nommage). Il pourrait y avoir un jour un système de nommage sécurisé, lisible par l'homme, évolutif et globalement unique, mais les applications ne devraient pas dépendre de sa mise en place. [Plus d'informations sur le système de nommage](/docs/overview/naming/) sont disponibles.

Bien que la plupart des applications n'aient pas besoin de distinguer les protocoles et les ports, I2P *prend* effectivement en charge cette fonctionnalité. Les applications complexes peuvent spécifier un protocole, un port source et un port de destination, pour chaque message individuellement, afin de multiplexer le trafic sur une seule destination. Consultez la [page sur les datagrammes](/docs/api/datagrams/) pour plus de détails. Les applications simples fonctionnent en écoutant « tous les protocoles » sur « tous les ports » d'une destination.

### Anonymat et Confidentialité

I2P offre un chiffrement et une authentification de bout en bout transparents pour toutes les données transmises sur le réseau — si Bob envoie des données vers la destination d'Alice, seule la destination d'Alice peut les recevoir, et si Bob utilise la bibliothèque de datagrammes ou de streaming, Alice sait avec certitude que c'est la destination de Bob qui a envoyé les données.

Bien entendu, I2P anonymise de manière transparente les données échangées entre Alice et Bob, mais il n'anonymise en rien le contenu de ce qu'ils envoient. Par exemple, si Alice envoie à Bob un formulaire contenant son nom complet, ses pièces d'identité et ses numéros de carte bancaire, I2P ne peut rien y faire. Par conséquent, les protocoles et applications doivent garder à l'esprit quelles informations ils tentent de protéger et quelles informations ils sont prêts à exposer.

### Les datagrammes I2P peuvent atteindre plusieurs Ko

Les applications qui utilisent les datagrammes I2P (qu'ils soient bruts ou répondables) peuvent essentiellement être considérées en termes d'UDP — les datagrammes sont non ordonnés, au mieux de leurs capacités, et sans connexion — mais contrairement à UDP, les applications n'ont pas besoin de se préoccuper de la détection du MTU et peuvent simplement envoyer de grands datagrammes. Bien que la limite supérieure soit nominalement de 32 Ko, le message est fragmenté pour le transport, ce qui diminue la fiabilité de l'ensemble. Les datagrammes de plus d'environ 10 Ko ne sont actuellement pas recommandés. Consultez la [page sur les datagrammes](/docs/api/datagrams/) pour plus de détails. Pour de nombreuses applications, 10 Ko de données suffisent pour une requête ou une réponse complète, leur permettant de fonctionner de manière transparente dans I2P comme une application de type UDP sans avoir à écrire de fragmentation, de renvois, etc.

## Options de développement

Il existe plusieurs moyens d'envoyer des données via I2P, chacun avec ses propres avantages et inconvénients. La bibliothèque streaming est l'interface recommandée, utilisée par la majorité des applications I2P.

### Bibliothèque de streaming

La [bibliothèque de streaming complète](/docs/specs/streaming/) est désormais l'interface standard. Elle permet de programmer en utilisant des sockets de type TCP, comme expliqué dans le [guide de développement Streaming](#developing-with-the-streaming-library).

### BOB

BOB est le [Basic Open Bridge](/docs/legacy/bob/), permettant à une application dans n'importe quel langage d'établir des connexions streaming vers et depuis I2P. À l'heure actuelle, il ne prend pas en charge UDP, mais la prise en charge UDP est prévue dans un avenir proche. BOB contient également plusieurs outils, tels que la génération de clés de destination et la vérification qu'une adresse est conforme aux spécifications I2P. Des informations à jour et des applications qui utilisent BOB peuvent être trouvées sur ce [site I2P](http://bob.i2p/).

### SAM, SAM V2, SAM V3

*SAM n'est pas recommandé. SAM V2 est acceptable, SAM V3 est recommandé.*

SAM est le protocole [Simple Anonymous Messaging](/docs/legacy/sam/), permettant à une application écrite dans n'importe quel langage de communiquer avec un pont SAM via une socket TCP simple et de faire en sorte que ce pont multiplexe tout son trafic I2P, en coordonnant de manière transparente le chiffrement/déchiffrement et la gestion basée sur les événements. SAM prend en charge trois styles de fonctionnement :

- streams, pour quand Alice et Bob veulent s'envoyer des données de manière fiable et ordonnée
- repliable datagrams, pour quand Alice veut envoyer à Bob un message auquel Bob peut répondre
- raw datagrams, pour quand Alice veut maximiser la bande passante et les performances autant que possible, et que Bob ne se soucie pas de savoir si l'expéditeur des données est authentifié ou non (par exemple, les données transférées sont auto-authentifiantes)

SAMv3 vise le même objectif que SAM et SAMv2, mais ne nécessite pas de multiplexage/démultiplexage. Chaque flux I2P est géré par son propre socket entre l'application et le pont SAM. De plus, les datagrammes peuvent être envoyés et reçus par l'application via des communications par datagrammes avec le pont SAM.

[SAM V2](/docs/legacy/samv2/) est une nouvelle version utilisée par imule qui corrige certains des problèmes présents dans [SAM](/docs/legacy/sam/).

[SAM V3](/docs/api/samv3/) est utilisé par imule depuis la version 1.4.0.

### I2PTunnel

L'application I2PTunnel permet aux applications de construire des tunnels TCP spécifiques vers des pairs en créant soit des applications I2PTunnel 'client' (qui écoutent sur un port spécifique et se connectent à une destination I2P spécifique chaque fois qu'un socket vers ce port est ouvert) soit des applications I2PTunnel 'server' (qui écoutent sur une destination I2P spécifique et chaque fois qu'elles reçoivent une nouvelle connexion I2P, elles redirigent vers un hôte/port TCP spécifique). Ces flux sont 8-bit clean et sont authentifiés et sécurisés via la même bibliothèque de streaming qu'utilise SAM, mais la création de plusieurs instances I2PTunnel uniques implique une surcharge non négligeable, car chacune possède sa propre destination I2P unique et son propre ensemble de tunnels, clés, etc.

### SOCKS

I2P prend en charge un proxy SOCKS V4 et V5. Les connexions sortantes fonctionnent bien. Les fonctionnalités entrantes (serveur) et UDP peuvent être incomplètes et non testées.

### Ministreaming

*Supprimé*

Il existait auparavant une bibliothèque simple "ministreaming", mais maintenant ministreaming.jar ne contient que les interfaces pour la bibliothèque streaming complète.

### Datagrammes

*Recommandé pour les applications de type UDP*

La [bibliothèque Datagram](/docs/api/datagrams/) permet d'envoyer des paquets de type UDP. Il est possible d'utiliser :

- Datagrammes avec réponse
- Datagrammes bruts

### I2CP

*Non recommandé*

[I2CP](/docs/specs/i2cp/) lui-même est un protocole indépendant du langage, mais pour implémenter une bibliothèque I2CP dans un autre langage que Java, il faut écrire une quantité significative de code (routines de chiffrement, sérialisation d'objets, gestion de messages asynchrones, etc.). Bien que quelqu'un puisse écrire une bibliothèque I2CP en C ou dans un autre langage, il serait probablement plus utile d'utiliser la bibliothèque SAM en C à la place.

### Applications Web

I2P est livré avec le serveur web Jetty, et la configuration pour utiliser le serveur Apache à la place est simple. Toute technologie d'application web standard devrait fonctionner.

## Commencer à développer — Un guide simple

Développer avec I2P nécessite une installation I2P fonctionnelle et un environnement de développement de votre choix. Si vous utilisez Java, vous pouvez commencer le développement avec la [bibliothèque streaming](#developing-with-the-streaming-library) ou la bibliothèque datagram. En utilisant un autre langage de programmation, SAM ou BOB peuvent être utilisés.

### Développement avec la bibliothèque Streaming

Ci-dessous se trouve une version réduite et modernisée de l'exemple de la page originale. Pour l'exemple complet, consultez la page historique ou nos exemples Java dans le code source.

```java
// Server example (excerpt)
I2PSocketManager manager = I2PSocketManagerFactory.createManager();
I2PServerSocket server = manager.getServerSocket();
I2PSocket socket = server.accept();
BufferedReader br = new BufferedReader(new InputStreamReader(socket.getInputStream()));
String s;
while ((s = br.readLine()) != null) {
    System.out.println("Received: " + s);
}
```
*Exemple de code : serveur basique recevant des données.*

```java
// Client example (excerpt)
I2PSocketManager manager = I2PSocketManagerFactory.createManager();
Destination dest = new Destination(serverDestBase64);
I2PSocket socket = manager.connect(dest);
BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));
bw.write("Hello I2P!\n");
bw.flush();
```
*Exemple de code : client se connectant et envoyant une ligne.*
