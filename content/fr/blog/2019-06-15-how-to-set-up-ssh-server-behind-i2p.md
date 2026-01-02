---
title: "Comment configurer un serveur SSH derrière I2P pour un accès personnel"
date: 2019-06-15
author: "idk"
description: "SSH via I2P"
---

# Comment configurer un serveur SSH derrière I2P pour un accès personnel

Ceci est un tutoriel expliquant comment configurer et affiner un tunnel I2P afin de l’utiliser pour accéder à un serveur SSH à distance, en utilisant soit I2P, soit i2pd. Pour l’instant, il part du principe que vous installerez votre serveur SSH via un gestionnaire de paquets et qu’il s’exécute en tant que service.

Considérations: Dans ce guide, je pars de quelques hypothèses. Elles devront être ajustées en fonction des complications qui surviennent dans votre configuration particulière, en particulier si vous utilisez des VM (machines virtuelles) ou des conteneurs pour l’isolation. Cela suppose que l’I2P router et le serveur SSH s’exécutent sur le même localhost. Vous devriez utiliser des clés d’hôte SSH nouvellement générées, soit en utilisant un sshd fraîchement installé, soit en supprimant les anciennes clés et en forçant leur régénération. Par exemple:

```
sudo service openssh stop
sudo rm -f /etc/ssh/ssh_host_*
sudo ssh-keygen -N "" -t rsa -f /etc/ssh/ssh_host_rsa_key
sudo ssh-keygen -N "" -t dsa -f /etc/ssh/ssh_host_dsa_key
sudo ssh-keygen -N "" -t ecdsa -f /etc/ssh/ssh_host_ecdsa_key
sudo ssh-keygen -N "" -t ed25519 -f /etc/ssh/ssh_host_ed25519_key
```
## Step One: Set up I2P tunnel for SSH Server

### Using Java I2P

À l'aide de l'interface web de java I2P, accédez au [Gestionnaire des services cachés](http://127.0.0.1:7657/i2ptunnelmgr) et démarrez l'assistant de tunnel.

#### Tunnel Wizard

Puisque vous configurez ce tunnel pour le serveur SSH, vous devez sélectionner le type de tunnel "Server".

**Espace réservé pour capture d’écran:** Utilisez l’assistant pour créer un tunnel "Server"

Vous devriez l’affiner plus tard, mais le type de tunnel Standard est le plus simple pour commencer.

**Espace réservé pour la capture d’écran:** De type « Standard »

Rédigez une bonne description :


**Espace réservé pour la capture d'écran:** Décrivez à quoi cela sert

Et indiquez où le serveur SSH sera disponible.

**Espace réservé pour la capture d’écran :** Pointez-le vers le futur emplacement de votre serveur SSH

Examinez les résultats et enregistrez vos paramètres.

**Espace réservé pour la capture d’écran:** Enregistrez les paramètres.

#### Advanced Settings

Retournez maintenant au Hidden Services Manager (gestionnaire des services cachés) et examinez les paramètres avancés disponibles. Une chose que vous voudrez certainement modifier est de le configurer pour des connexions interactives plutôt que des connexions de gros volume.

**Espace réservé pour la capture d’écran :** Configurez votre tunnel pour des connexions interactives

Par ailleurs, ces autres options peuvent affecter les performances lors de l’accès à votre serveur SSH. Si votre anonymat ne vous préoccupe pas tant que ça, vous pouvez réduire le nombre de sauts. Si vous rencontrez des problèmes de débit, un nombre de tunnels plus élevé pourrait aider. Prévoir quelques tunnels de secours est probablement une bonne idée. Vous devrez peut‑être affiner un peu la configuration.

**Espace réservé pour capture d'écran:** Si l'anonymat ne vous préoccupe pas, réduisez la longueur du tunnel.

Enfin, redémarrez le tunnel afin que tous vos paramètres prennent effet.

Un autre paramètre intéressant, surtout si vous choisissez d’exécuter un grand nombre de tunnels, est "Reduce on Idle", qui réduira le nombre de tunnels qui s’exécutent lorsque le serveur a connu une inactivité prolongée.

**Espace réservé pour capture d’écran:** Réduire en cas d’inactivité, si vous avez choisi un nombre élevé de tunnels

### Using i2pd

Avec i2pd, toute la configuration se fait au moyen de fichiers plutôt que via une interface web. Pour configurer un tunnel de service SSH pour i2pd, adaptez les paramètres d’exemple suivants à vos besoins en matière d’anonymat et de performances, puis copiez-les dans tunnels.conf

```
[SSH-SERVER]
type = server
host = 127.0.0.1
port = 22
inbound.length = 1
outbound.length = 1
inbound.quantity = 5
outbound.quantity = 5
i2cp.reduceOnIdle = true
keys = ssh-in.dat
```
#### Restart your I2P router

## Étape 1: Configurer un I2P tunnel pour le serveur SSH

Selon la manière dont vous souhaitez accéder à votre serveur SSH, vous pourriez vouloir apporter quelques modifications aux paramètres. Outre les mesures évidentes de durcissement SSH que vous devriez appliquer sur tous les serveurs SSH(Authentification par clé publique, pas de connexion en tant que root, etc), si vous ne souhaitez pas que votre serveur SSH écoute sur d'autres adresses que votre tunnel serveur, vous devez définir AddressFamily sur inet et ListenAddress sur 127.0.0.1.

```
AddressFamily inet
ListenAddress 127.0.0.1
```
Si vous choisissez d’utiliser un port autre que 22 pour votre serveur SSH, vous devrez modifier le port dans la configuration du tunnel I2P.

## Step Three: Set up I2P tunnel for SSH Client

Vous devrez pouvoir accéder à la console du router I2P du serveur SSH afin de configurer votre connexion client. Un aspect intéressant de cette configuration est que la connexion initiale au tunnel I2P est authentifiée, ce qui réduit quelque peu le risque que votre connexion initiale au serveur SSH fasse l'objet d'une attaque MITM (Man-in-the-Middle), comme c'est un risque dans les scénarios de Trust-On-First-Use (confiance lors de la première utilisation).

### Utilisation de Java I2P

#### Assistant de Tunnel

Commencez par lancer l’assistant de configuration du tunnel depuis le gestionnaire des services cachés et sélectionnez un tunnel client.

**Espace réservé pour la capture d'écran :** Utilisez l'assistant pour créer un tunnel client

Ensuite, sélectionnez le type de tunnel standard. Vous affinerez cette configuration plus tard.

**Espace réservé pour capture d’écran :** De type Standard

Fournissez une bonne description.

**Espace réservé pour une capture d’écran:** Ajoutez une bonne description

C’est la seule partie un peu délicate. Allez dans le gestionnaire des services cachés de la console du router I2P et trouvez la "local destination" en base64 du tunnel du serveur SSH. Vous devrez trouver un moyen de copier cette information pour l’étape suivante. En général, je me l’envoie via [Tox](https://tox.chat), n’importe quel canal Off-the-Record (OTR) devrait suffire pour la plupart des gens.

**Espace réservé pour la capture d’écran:** Trouvez la destination à laquelle vous souhaitez vous connecter

Une fois que vous avez trouvé la destination Base64 à laquelle vous souhaitez vous connecter et qui a été transmise à votre appareil client, collez-la ensuite dans le champ de destination du client.

**Espace réservé pour la capture d'écran:** Fixer la destination

Enfin, définissez un port local auquel votre client SSH se connectera. Ce port local sera relié à la destination en base64 et donc au serveur SSH.

**Espace réservé pour la capture d’écran :** Choisissez un port local

Décidez si vous souhaitez qu’il démarre automatiquement.

**Espace réservé pour la capture d'écran:** Décidez si vous souhaitez qu'il se lance automatiquement

#### Paramètres avancés

Comme auparavant, vous aurez intérêt à modifier les paramètres pour qu’ils soient optimisés pour les connexions interactives. De plus, si vous souhaitez configurer une liste blanche de clients sur le serveur, vous devez cocher le bouton radio "Generate key to enable persistent client tunnel identity".

**Espace réservé pour capture d'écran:** Configurez-le pour qu'il soit interactif

### Using i2pd

Vous pouvez configurer cela en ajoutant les lignes suivantes à votre fichier tunnels.conf et en les ajustant selon vos besoins en performances/anonymat.

```
[SSH-CLIENT]
type = client
host = 127.0.0.1
port = 7622
inbound.length = 1
outbound.length = 1
inbound.quantity = 5
outbound.quantity = 5
i2cp.dontPublishLeaseSet = true
destination = thisshouldbethebase32ofthesshservertunnelabovebefore.b32.i2p
keys = ssh-in.dat
```
#### Restart the I2P router on the client

## Step Four: Set up SSH client

Il existe de nombreuses façons de configurer un client SSH pour se connecter à votre serveur sur I2P, mais vous devriez prendre quelques mesures pour sécuriser votre client SSH pour un usage anonyme. Commencez par le configurer pour qu’il ne s’identifie auprès du serveur SSH qu’avec une clé unique et spécifique, afin d’éviter de mêler vos connexions SSH anonymes et non anonymes.

Assurez-vous que votre $HOME/.ssh/config contient les lignes suivantes :

```
IdentitiesOnly yes

Host 127.0.0.1
  IdentityFile ~/.ssh/login_id_ed25519
```
Sinon, vous pourriez créer une entrée .bash_alias pour imposer vos options et vous connecter automatiquement à I2P. Vous voyez l'idée, il faut imposer IdentitiesOnly et fournir un fichier d'identité.

```
i2pssh() {
    ssh -o IdentitiesOnly=yes -o IdentityFile=~/.ssh/login_id_ed25519 serveruser@127.0.0.1:7622
}
```
## Step Five: Whitelist only the client tunnel

C’est plus ou moins facultatif, mais c’est plutôt intéressant et cela empêchera quiconque viendrait à tomber sur votre destination de déterminer que vous hébergez un service SSH.

Tout d’abord, récupérez la destination du tunnel client persistant et transmettez-la au serveur.

**Espace réservé pour la capture d’écran:** Obtenir la destination du client

Ajoutez la destination base64 du client à la liste blanche des destinations du serveur. Vous ne pourrez alors vous connecter au tunnel du serveur qu’à partir de ce tunnel client spécifique, et personne d’autre ne pourra se connecter à cette destination.

**Espace réservé pour la capture d’écran:** Et collez-le dans la liste blanche du serveur

L'authentification mutuelle, c'est le meilleur choix.

**Remarque :** Les images référencées dans la publication d'origine doivent être ajoutées au répertoire `/static/images/` : - server.png, standard.png, describe.png, hostport.png, approve.png - interactive.png, anonlevel.png, idlereduce.png - client.png, clientstandard.png, clientdescribe.png - finddestination.png, fixdestination.png, clientport.png, clientautostart.png - clientinteractive.png, whitelistclient.png, whitelistserver.png
