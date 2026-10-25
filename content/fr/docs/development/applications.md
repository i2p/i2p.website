---
title: "Développement d'Applications"
description: "Pourquoi écrire des applications spécifiques à I2P, concepts clés, options de développement et guide de démarrage"
slug: "applications"
aliases:
  - "/fr/docs/develop/applications"
  - "/fr/docs/develop/applications/"
  - "/fr/applications"
  - "/fr/applications/"
lastUpdated: "2013-05"
accurateFor: "0.9.6"
---

## Pourquoi écrire du code spécifique à I2P ?

Il existe plusieurs façons d'utiliser des applications dans I2P. En utilisant [I2PTunnel](/docs/api/i2ptunnel/), vous pouvez utiliser des applications classiques sans avoir besoin de programmer un support I2P explicite. Cela est très efficace pour les scénarios client-serveur, où vous devez vous connecter à un seul site web. Vous pouvez simplement créer un tunnel en utilisant I2PTunnel pour vous connecter à ce site web, comme le montre la Figure 1.

Si votre application est distribuée, elle nécessitera des connexions vers un grand nombre de pairs. En utilisant I2PTunnel, vous devrez créer un nouveau tunnel pour chaque pair que vous souhaitez contacter, comme illustré dans la Figure 2. Ce processus peut bien sûr être automatisé, mais l'exécution de nombreuses instances I2PTunnel crée une grande quantité de surcharge. De plus, avec de nombreux protocoles, vous devrez forcer tout le monde à utiliser le même ensemble de ports pour tous les pairs — par exemple, si vous voulez exécuter de manière fiable un chat DCC, tout le monde doit convenir que le port 10001 est Alice, le port 10002 est Bob, le port 10003 est Charlie, et ainsi de suite, car le protocole inclut des informations spécifiques TCP/IP (hôte et port).

Les applications réseau générales envoient souvent beaucoup de données supplémentaires qui pourraient être utilisées pour identifier les utilisateurs. Les noms d'hôte, numéros de port, fuseaux horaires, jeux de caractères, etc. sont souvent envoyés sans en informer l'utilisateur. En tant que tel, concevoir le protocole réseau spécifiquement en gardant l'anonymat à l'esprit peut éviter de compromettre les identités des utilisateurs.

Il y a aussi des considérations d'efficacité à examiner lors de la détermination de la manière d'interagir au-dessus d'I2P. La bibliothèque de streaming et les éléments construits par-dessus fonctionnent avec des handshakes similaires à TCP, tandis que les protocoles I2P de base (I2NP et I2CP) sont strictement basés sur des messages (comme UDP ou dans certains cas IP brut). La distinction importante est qu'avec I2P, la communication s'opère sur un réseau long et large — chaque message de bout en bout aura des latences non négligeables, mais peut contenir des charges utiles de plusieurs KB. Une application qui nécessite une simple requête et réponse peut se débarrasser de tout état et éliminer la latence encourue par les handshakes de démarrage et de fermeture en utilisant des datagrammes (au mieux) sans avoir à se soucier de la détection MTU ou de la fragmentation des messages.

![Créer une connexion serveur-client en utilisant I2PTunnel ne nécessite que la création d'un seul tunnel.](/images/i2ptunnel_serverclient.png)

*Figure 1 : Créer une connexion serveur-client en utilisant I2PTunnel ne nécessite que la création d'un seul tunnel.*

![La configuration des connexions pour les applications pair-à-pair nécessite un très grand nombre de tunnels.](/images/i2ptunnel_peertopeer.png)

*Figure 2 : La configuration de connexions pour des applications pair-à-pair nécessite un très grand nombre de tunnels.*

En résumé, plusieurs raisons d'écrire du code spécifique à I2P :

- Créer un grand nombre d'instances I2PTunnel consomme une quantité non négligeable de ressources, ce qui pose problème pour les applications distribuées (un nouveau tunnel est requis pour chaque pair).
- Les protocoles réseau généraux envoient souvent beaucoup de données supplémentaires qui peuvent être utilisées pour identifier les utilisateurs. Programmer spécifiquement pour I2P permet la création d'un protocole réseau qui ne divulgue pas de telles informations, gardant les utilisateurs anonymes et sécurisés.
- Les protocoles réseau conçus pour une utilisation sur l'internet classique peuvent être inefficaces sur I2P, qui est un réseau avec une latence beaucoup plus élevée.

I2P prend en charge une [interface de plugins](/docs/specs/plugin/) standard pour les développeurs afin que les applications puissent être facilement intégrées et distribuées.

Les applications écrites en Java et accessibles/exécutables via une interface HTML grâce au fichier webapps/app.war standard peuvent être considérées pour inclusion dans la distribution I2P.

---

## Concepts importants

Il y a quelques changements qui nécessitent un ajustement lors de l'utilisation d'I2P :

### Destination ~= hôte+port

Une application fonctionnant sur I2P envoie des messages depuis et reçoit des messages vers un point de terminaison unique cryptographiquement sécurisé — une "destination". En termes TCP ou UDP, une destination pourrait (largement) être considérée comme l'équivalent d'une paire nom d'hôte plus numéro de port, bien qu'il y ait quelques différences.

- Une destination I2P est en elle-même une construction cryptographique — toutes les données qui lui sont envoyées sont chiffrées comme s'il y avait un déploiement universel d'IPsec avec l'emplacement (anonymisé) du point final signé comme s'il y avait un déploiement universel de DNSSEC.
- Les destinations I2P sont des identifiants mobiles — elles peuvent être déplacées d'un router I2P à un autre (ou peuvent même faire du "multihome" — fonctionner sur plusieurs routers simultanément). C'est très différent du monde TCP ou UDP où un seul point final (port) doit rester sur un seul hôte.
- Les destinations I2P sont inélégantes et volumineuses — en arrière-plan, elles contiennent une clé publique ElGamal de 2048 bits pour le chiffrement, une clé publique DSA de 1024 bits pour la signature, et un certificat de taille variable, qui peut contenir une preuve de travail ou des données masquées.

Il existe des moyens existants pour faire référence à ces destinations volumineuses et disgracieuses par des noms courts et jolis (par exemple "irc.duck.i2p"), mais ces techniques ne garantissent pas l'unicité globale (puisqu'elles sont stockées localement dans une base de données sur la machine de chaque personne) et le mécanisme actuel n'est pas particulièrement évolutif ni sécurisé (les mises à jour de la liste d'hôtes sont gérées en utilisant des "abonnements" aux services de nommage). Il pourrait y avoir un jour un système de nommage sécurisé, lisible par l'humain, évolutif et globalement unique, mais les applications ne devraient pas dépendre de sa mise en place, car il y a ceux qui ne pensent pas qu'une telle bête soit possible. [Plus d'informations sur le système de nommage](/docs/overview/naming/) sont disponibles.

Bien que la plupart des applications n'aient pas besoin de distinguer les protocoles et les ports, I2P *prend* effectivement en charge cette fonctionnalité. Les applications complexes peuvent spécifier un protocole, un port source et un port de destination, message par message, pour multiplexer le trafic sur une seule destination. Consultez la [page des datagrammes](/docs/api/datagrams/) pour plus de détails. Les applications simples fonctionnent en écoutant "tous les protocoles" sur "tous les ports" d'une destination.

### Anonymat et Confidentialité

I2P dispose d'un chiffrement et d'une authentification transparents de bout en bout pour toutes les données transmises sur le réseau — si Bob envoie vers la destination d'Alice, seule la destination d'Alice peut la recevoir, et si Bob utilise la bibliothèque de datagrammes ou de streaming, Alice sait avec certitude que la destination de Bob est celle qui a envoyé les données.

Bien sûr, I2P anonymise de manière transparente les données envoyées entre Alice et Bob, mais il ne fait rien pour anonymiser le contenu de ce qu'ils s'envoient. Par exemple, si Alice envoie à Bob un formulaire avec son nom complet, ses pièces d'identité gouvernementales et ses numéros de carte de crédit, I2P ne peut rien y faire. Ainsi, les protocoles et applications doivent garder à l'esprit quelles informations ils essaient de protéger et quelles informations ils sont prêts à exposer.

### Les datagrammes I2P peuvent atteindre plusieurs Ko

Les applications qui utilisent les datagrammes I2P (qu'ils soient bruts ou avec réponse possible) peuvent essentiellement être considérées en termes d'UDP — les datagrammes sont non ordonnés, au mieux effort, et sans connexion — mais contrairement à UDP, les applications n'ont pas besoin de s'inquiéter de la détection MTU et peuvent simplement envoyer de gros datagrammes. Bien que la limite supérieure soit nominalement de 32 KB, le message est fragmenté pour le transport, réduisant ainsi la fiabilité de l'ensemble. Les datagrammes de plus d'environ 10 KB ne sont actuellement pas recommandés. Voir la [page des datagrammes](/docs/api/datagrams/) pour plus de détails. Pour de nombreuses applications, 10 KB de données suffisent pour une requête ou une réponse entière, leur permettant de fonctionner de manière transparente dans I2P comme une application similaire à UDP sans avoir à écrire de fragmentation, de renvois, etc.

---

## Options de développement

Il existe plusieurs moyens d'envoyer des données via I2P, chacun avec ses propres avantages et inconvénients. La bibliothèque streaming est l'interface recommandée, utilisée par la majorité des applications I2P.

### Bibliothèque de Streaming

La [bibliothèque de streaming complète](/docs/api/streaming/) est maintenant l'interface standard. Elle permet de programmer en utilisant des sockets de type TCP, comme expliqué dans le [guide de développement Streaming](#developing-with-the-streaming-library).

### BOB

BOB est le [Basic Open Bridge](/docs/legacy/bob/), permettant à une application dans n'importe quel langage d'établir des connexions streaming vers et depuis I2P. À l'heure actuelle, il ne prend pas en charge UDP, mais la prise en charge UDP est prévue dans un proche avenir. BOB contient également plusieurs outils, tels que la génération de clés de destination et la vérification qu'une adresse est conforme aux spécifications I2P. Les informations à jour et les applications qui utilisent BOB peuvent être trouvées sur ce [site I2P](http://bob.i2p/).

### SAM, SAM V2, SAM V3

*SAM n'est pas recommandé. SAM V2 est correct, SAMv3 est recommandé.*

SAM est le protocole [Simple Anonymous Messaging](/docs/legacy/sam/), permettant à une application écrite dans n'importe quel langage de communiquer avec un pont SAM via une socket TCP simple et de faire en sorte que ce pont multiplexe tout son trafic I2P, en coordonnant de manière transparente le chiffrement/déchiffrement et la gestion basée sur les événements. SAM prend en charge trois styles de fonctionnement :

- streams, pour quand Alice et Bob veulent s'envoyer des données de manière fiable et dans l'ordre
- datagrammes avec réponse, pour quand Alice veut envoyer un message à Bob auquel Bob peut répondre
- datagrammes bruts, pour quand Alice veut optimiser au maximum la bande passante et les performances, et que Bob ne se soucie pas de savoir si l'expéditeur des données est authentifié ou non (par exemple, les données transférées sont auto-authentifiantes)

SAM V3 vise le même objectif que SAM et SAM V2, mais ne nécessite pas de multiplexage/démultiplexage. Chaque flux I2P est géré par sa propre socket entre l'application et le pont SAM. De plus, les datagrammes peuvent être envoyés et reçus par l'application via des communications par datagrammes avec le pont SAM.

[SAM V2](/docs/legacy/samv2/) est une nouvelle version utilisée par imule qui corrige certains des problèmes dans [SAM](/docs/legacy/sam/).

[SAM V3](/docs/api/samv3/) est utilisé par imule depuis la version 1.4.0.

### I2PTunnel

L'application I2PTunnel permet aux applications de construire des tunnels spécifiques similaires à TCP vers des pairs en créant soit des applications I2PTunnel 'client' (qui écoutent sur un port spécifique et se connectent à une destination I2P spécifique chaque fois qu'un socket vers ce port est ouvert) soit des applications I2PTunnel 'serveur' (qui écoutent une destination I2P spécifique et chaque fois qu'elles reçoivent une nouvelle connexion I2P, elles établissent un proxy sortant vers un hôte/port TCP spécifique). Ces flux sont 8-bit clean, et sont authentifiés et sécurisés via la même bibliothèque de streaming que SAM utilise, mais il y a une surcharge non négligeable impliquée dans la création de multiples instances I2PTunnel uniques, puisque chacune a sa propre destination I2P unique et son propre ensemble de tunnels, clés, etc.

### SOCKS

I2P prend en charge un proxy SOCKS V4 et V5. Les connexions sortantes fonctionnent bien. Les fonctionnalités entrantes (serveur) et UDP peuvent être incomplètes et non testées.

### Ministreaming

*Supprimé*

Il y avait auparavant une bibliothèque simple "ministreaming", mais maintenant ministreaming.jar ne contient que les interfaces pour la bibliothèque streaming complète.

### Datagrammes

*Recommandé pour les applications de type UDP*

La [bibliothèque Datagram](/docs/api/datagrams/) permet d'envoyer des paquets similaires à UDP. Il est possible d'utiliser :

- Datagrammes reproductibles
- Datagrammes bruts

### I2CP

*Non recommandé*

[I2CP](/docs/specs/i2cp/) lui-même est un protocole indépendant du langage, mais pour implémenter une bibliothèque I2CP dans autre chose que Java, il y a une quantité significative de code à écrire (routines de chiffrement, marshalling d'objets, gestion de messages asynchrones, etc). Bien que quelqu'un puisse écrire une bibliothèque I2CP en C ou dans autre chose, il serait très probablement plus utile d'utiliser la bibliothèque SAM en C à la place.

### Applications Web

I2P est livré avec le serveur web Jetty, et configurer pour utiliser le serveur Apache à la place est simple. Toute technologie d'application web standard devrait fonctionner.

---

## Commencer le développement — Un guide simple

Développer avec I2P nécessite une installation I2P fonctionnelle et un environnement de développement de votre choix. Si vous utilisez Java, vous pouvez commencer le développement avec la [bibliothèque streaming](#developing-with-the-streaming-library) ou la bibliothèque datagram. En utilisant un autre langage de programmation, SAM ou BOB peuvent être utilisés.

### Développement avec la bibliothèque Streaming

L'exemple suivant montre comment créer des applications client et serveur de type TCP en utilisant la bibliothèque de streaming.

Cela nécessitera les bibliothèques suivantes dans votre classpath :

- `$I2P/lib/streaming.jar` : La bibliothèque streaming elle-même
- `$I2P/lib/mstreaming.jar` : Factory et interfaces pour la bibliothèque streaming
- `$I2P/lib/i2p.jar` : Classes I2P standard, structures de données, API et utilitaires

Vous pouvez les récupérer à partir d'une installation I2P, ou ajouter les dépendances suivantes depuis Maven Central :

- `net.i2p:i2p`
- `net.i2p.client:streaming`

La communication réseau nécessite l'utilisation de sockets réseau I2P. Pour illustrer ceci, nous allons créer une application où un client peut envoyer des messages texte à un serveur, qui affichera les messages et les renverra au client. En d'autres termes, le serveur fonctionnera comme un écho.

Nous commencerons par initialiser l'application serveur. Cela nécessite d'obtenir un I2PSocketManager et de créer un I2PServerSocket. Nous ne fournirons pas à l'I2PSocketManagerFactory les clés sauvegardées pour une Destination existante, donc elle créera une nouvelle Destination pour nous. Nous demanderons donc à l'I2PSocketManager un I2PSession, afin de pouvoir découvrir la Destination qui a été créée, car nous devrons copier et coller ces informations plus tard pour que le client puisse se connecter à nous.

```java
package i2p.echoserver;

import net.i2p.client.I2PSession;
import net.i2p.client.streaming.I2PServerSocket;
import net.i2p.client.streaming.I2PSocketManager;
import net.i2p.client.streaming.I2PSocketManagerFactory;

public class Main {

    public static void main(String[] args) {
        //Initialize application
        I2PSocketManager manager = I2PSocketManagerFactory.createManager();
        I2PServerSocket serverSocket = manager.getServerSocket();
        I2PSession session = manager.getSession();
        //Print the base64 string, the regular string would look like garbage.
        System.out.println(session.getMyDestination().toBase64());
        //The additional main method code comes here...
    }

}
```
*Exemple de code 1 : initialisation de l'application serveur.*

Une fois que nous avons un I2PServerSocket, nous pouvons créer des instances I2PSocket pour accepter les connexions des clients. Dans cet exemple, nous créerons une seule instance I2PSocket, qui ne peut gérer qu'un seul client à la fois. Un vrai serveur devrait être capable de gérer plusieurs clients. Pour ce faire, plusieurs instances I2PSocket devraient être créées, chacune dans des threads séparés. Une fois que nous avons créé l'instance I2PSocket, nous lisons les données, les affichons et les renvoyons au client.

```java
package i2p.echoserver;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.ConnectException;
import java.net.SocketTimeoutException;
import net.i2p.I2PException;
import net.i2p.client.streaming.I2PSocket;
import net.i2p.util.I2PThread;

import net.i2p.client.I2PSession;
import net.i2p.client.streaming.I2PServerSocket;
import net.i2p.client.streaming.I2PSocketManager;
import net.i2p.client.streaming.I2PSocketManagerFactory;

public class Main {

    public static void main(String[] args) {
        I2PSocketManager manager = I2PSocketManagerFactory.createManager();
        I2PServerSocket serverSocket = manager.getServerSocket();
        I2PSession session = manager.getSession();
        //Print the base64 string, the regular string would look like garbage.
        System.out.println(session.getMyDestination().toBase64());

        //Create socket to handle clients
        I2PThread t = new I2PThread(new ClientHandler(serverSocket));
        t.setName("clienthandler1");
        t.setDaemon(false);
        t.start();
    }

    private static class ClientHandler implements Runnable {

        public ClientHandler(I2PServerSocket socket) {
            this.socket = socket;
        }

        public void run() {
            while(true) {
                try {
                    I2PSocket sock = this.socket.accept();
                    if(sock != null) {
                        //Receive from clients
                        BufferedReader br = new BufferedReader(new InputStreamReader(sock.getInputStream()));
                        //Send to clients
                        BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(sock.getOutputStream()));
                        String line = br.readLine();
                        if(line != null) {
                            System.out.println("Received from client: " + line);
                            bw.write(line);
                            bw.flush(); //Flush to make sure everything got sent
                        }
                        sock.close();
                    }
                } catch (I2PException ex) {
                    System.out.println("General I2P exception!");
                } catch (ConnectException ex) {
                    System.out.println("Error connecting!");
                } catch (SocketTimeoutException ex) {
                    System.out.println("Timeout!");
                } catch (IOException ex) {
                    System.out.println("General read/write-exception!");
                }
            }
        }

        private I2PServerSocket socket;

    }

}
```
*Exemple de code 2 : accepter les connexions des clients et gérer les messages.*

Lorsque vous exécutez le code serveur ci-dessus, il devrait afficher quelque chose comme ceci (mais sans les fins de ligne, cela devrait juste être un énorme bloc de caractères) :

```
y17s~L3H9q5xuIyyynyWahAuj6Jeg5VC~Klu9YPquQvD4vlgzmxn4yy~5Z0zVvKJiS2Lk
poPIcB3r9EbFYkz1mzzE3RYY~XFyPTaFQY8omDv49nltI2VCQ5cx7gAt~y4LdWqkyk3au
...
```
Il s'agit de la représentation base64 de la Destination du serveur. Le client aura besoin de cette chaîne pour atteindre le serveur.

Maintenant, nous allons créer l'application cliente. Encore une fois, plusieurs étapes sont nécessaires pour l'initialisation. Encore une fois, nous devrons commencer par obtenir un I2PSocketManager. Nous n'utiliserons pas d'I2PSession ni d'I2PServerSocket cette fois. Au lieu de cela, nous utiliserons la chaîne Destination du serveur pour démarrer notre connexion. Nous demanderons à l'utilisateur la chaîne Destination, et créerons un I2PSocket en utilisant cette chaîne. Une fois que nous avons un I2PSocket, nous pouvons commencer à envoyer et recevoir des données vers et depuis le serveur.

```java
package i2p.echoclient;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.InterruptedIOException;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.ConnectException;
import java.net.NoRouteToHostException;
import net.i2p.I2PException;
import net.i2p.client.streaming.I2PSocket;
import net.i2p.client.streaming.I2PSocketManager;
import net.i2p.client.streaming.I2PSocketManagerFactory;
import net.i2p.data.DataFormatException;
import net.i2p.data.Destination;

public class Main {

    public static void main(String[] args) {
        I2PSocketManager manager = I2PSocketManagerFactory.createManager();
        System.out.println("Please enter a Destination:");
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String destinationString;
        try {
            destinationString = br.readLine();
        } catch (IOException ex) {
            System.out.println("Failed to get a Destination string.");
            return;
        }
        Destination destination;
        try {
            destination = new Destination(destinationString);
        } catch (DataFormatException ex) {
            System.out.println("Destination string incorrectly formatted.");
            return;
        }
        I2PSocket socket;
        try {
            socket = manager.connect(destination);
        } catch (I2PException ex) {
            System.out.println("General I2P exception occurred!");
            return;
        } catch (ConnectException ex) {
            System.out.println("Failed to connect!");
            return;
        } catch (NoRouteToHostException ex) {
            System.out.println("Couldn't find host!");
            return;
        } catch (InterruptedIOException ex) {
            System.out.println("Sending/receiving was interrupted!");
            return;
        }
        try {
            //Write to server
            BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));
            bw.write("Hello I2P!\n");
            //Flush to make sure everything got sent
            bw.flush();
            //Read from server
            BufferedReader br2 = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            String s = null;
            while ((s = br2.readLine()) != null) {
                System.out.println("Received from server: " + s);
            }
            socket.close();
        } catch (IOException ex) {
            System.out.println("Error occurred while sending/receiving!");
        }
    }

}
```
*Exemple de code 3 : démarrage du client et connexion à l'application serveur.*

Enfin, vous pouvez exécuter à la fois l'application serveur et l'application client. Commencez d'abord par démarrer l'application serveur. Elle affichera une chaîne Destination (comme montré ci-dessus). Ensuite, démarrez l'application client. Lorsqu'elle demande une chaîne Destination, vous pouvez saisir la chaîne affichée par le serveur. Le client enverra alors 'Hello I2P!' (avec un retour à la ligne) au serveur, qui affichera le message et le renverra au client.

Félicitations, vous avez communiqué avec succès via I2P !

---

## Applications existantes

Contactez-nous si vous souhaitez contribuer.

- [I2P-Bote](http://i2pbote.i2p/) - contacter HungryHobo
- [Syndie](http://syndie.i2p2.de/)
- [IMule](http://www.imule.i2p/)
- [I2Phex](http://forum.i2p/viewforum.php?f=25)

Voir aussi tous les plugins sur [plugins.i2p](http://plugins.i2p/), les applications et le code source listés sur [echelon.i2p](http://echelon.i2p/), et le code d'application hébergé sur [git.repo.i2p](http://git.repo.i2p/).

Voir également les applications intégrées dans la distribution I2P - SusiMail et I2PSnark.

---

## Idées d'applications

- Serveur NNTP - il y en a eu quelques-uns dans le passé, aucun actuellement
- Serveur Jabber - il y en a eu quelques-uns dans le passé, et il y en a un actuellement, avec accès à l'internet public
- Serveur de clés PGP et/ou proxy
- Applications de distribution de contenu / DHT - ressusciter feedspace, porter dijjer, chercher des alternatives
- Aider au développement de [Syndie](http://syndie.i2p2.de/)
- Applications web - Toutes les possibilités sont ouvertes pour héberger des applications basées sur serveur web comme des blogs, pastebins, stockage, suivi, flux, etc. Toute technologie web ou CGI comme Perl, PHP, Python, ou Ruby fonctionnera.
- Ressusciter quelques anciennes applications, plusieurs précédemment dans le paquet source i2p - bogobot, pants, proxyscript, q, stasher, socks proxy, i2ping, feedspace
