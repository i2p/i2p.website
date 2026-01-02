---
title: "Comment se porter volontaire en aidant à l’amorçage d’I2P-Bote"
date: 2019-05-20
author: "idk"
description: "Aidez à amorcer I2P-Bote !"
categories: ["development"]
---

Un moyen simple d’aider les personnes à communiquer entre elles en privé consiste à exécuter un pair I2P-Bote qui peut être utilisé par les nouveaux utilisateurs d’I2P-Bote pour amorcer leurs propres pairs I2P-Bote. Malheureusement, jusqu’à présent, le processus de mise en place d’un pair d’amorçage I2P-Bote a été bien plus obscur qu’il ne devrait l’être. En fait, c’est extrêmement simple !

**Qu'est-ce qu'I2P-bote ?**

I2P-bote est un système de messagerie privée construit sur i2p, doté de fonctionnalités supplémentaires qui rendent encore plus difficile la déduction d’informations sur les messages transmis. De ce fait, il peut être utilisé pour transmettre des messages privés de manière sécurisée tout en tolérant une latence élevée et sans dépendre d’un relais centralisé pour envoyer des messages lorsque l’expéditeur se déconnecte. Cela contraste avec la quasi-totalité des autres systèmes de messagerie privée populaires, qui exigent soit que les deux parties soient en ligne, soit s’appuient sur un service partiellement digne de confiance qui transmet les messages au nom des expéditeurs lorsqu’ils se déconnectent.

ou, expliqué comme à un enfant de 5 ans : Il s'utilise de manière similaire à l'e-mail, mais il ne souffre d'aucun des défauts de confidentialité de l'e-mail.

**Étape 1 : Installer I2P-Bote**

I2P-Bote est un plugin i2p, et son installation est très facile. Les instructions originales sont disponibles sur le [bote eepSite, bote.i2p](http://bote.i2p/install/), mais si vous souhaitez les lire sur le clearnet, ces instructions sont fournies gracieusement par bote.i2p :

1. Go to the plugin install form in your routerconsole: http://127.0.0.1:7657/configclients#plugin
2. Paste in the URL http://bote.i2p/i2pbote.su3
3. Click Install Plugin.
4. Once installed, click SecureMail in the routerconsole sidebar or homepage, or go to http://127.0.0.1:7657/i2pbote/

**Deuxième étape : Obtenez l'adresse en base64 de votre nœud I2P-Bote**

C’est la partie où l’on peut se retrouver bloqué, mais n’ayez crainte. Bien que les instructions soient un peu difficiles à trouver, c’est en réalité simple et plusieurs outils et options sont à votre disposition, selon votre situation. Pour les personnes qui souhaitent aider, bénévolement, à faire fonctionner des nœuds d’amorçage, la meilleure méthode consiste à récupérer les informations nécessaires à partir du fichier de clé privée utilisé par le tunnel bote.

**Où sont les clés ?**

I2P-Bote stocke ses clés de destination dans un fichier texte qui, sur Debian, se trouve à `/var/lib/i2p/i2p-config/i2pbote/local_dest.key`. Sur les systèmes non-Debian où i2p est installé par l'utilisateur, la clé se trouvera dans `$HOME/.i2p/i2pbote/local_dest.key`, et sous Windows, le fichier se trouvera dans `C:\ProgramData\i2p\i2pbote\local_dest.key`.

**Méthode A : Convertir la clé en clair en destination base64**

Pour convertir une clé en clair en une destination en base64, il faut prendre la clé et n’en séparer que la partie destination. Pour effectuer cela correctement, il faut suivre les étapes suivantes :

1. First, take the full destination and decode it from i2p's base64 character set into binary.
2. Second, take bytes 386 and 387 and convert them to a single Big-Endian integer.
3. Add the number you computed from the two bytes in step two to 387. This is the length of the base64 destination.
4. Take that nummber of bytes from the front of the full destination to get the destination as a range of bytes.
5. Convert back to a base64 representation using i2p's base64 character set.

Un certain nombre d’applications et de scripts existent pour effectuer ces étapes pour vous. En voici quelques-uns, mais la liste est loin d’être exhaustive :

- [the i2p.scripts collection of scripts(Mostly java and bash)](https://github.com/i2p/i2p.scripts)
- [my application for converting keys(Go)](https://github.com/eyedeekay/keyto)

Ces fonctionnalités sont également disponibles dans un certain nombre de bibliothèques de développement d’applications I2P.

**Raccourci:**


Puisque la destination locale de votre nœud bote est une destination DSA, il est plus rapide de simplement tronquer le fichier local_dest.key aux 516 premiers octets. Pour le faire facilement, exécutez cette commande lorsque vous exécutez I2P-Bote avec I2P sur Debian:

```bash
sudo -u i2psvc head -c 516 /var/lib/i2p/i2p-config/i2pbote/local_dest.key
```
Ou, si I2P est installé pour votre compte utilisateur :

```bash
head -c 516 ~/.i2p/i2pbote/local_dest.key
```
**Méthode B : Effectuer une recherche**

Si cela vous semble un peu trop de travail, vous pouvez rechercher la destination en base64 de votre connexion Bote en interrogeant son adresse en base32 à l'aide de n'importe lequel des moyens disponibles pour rechercher une adresse en base32. L'adresse en base32 de votre nœud Bote est disponible sur la page "Connexion" dans l'application du plugin Bote, à [127.0.0.1:7657/i2pbote/network](http://127.0.0.1:7657/i2pbote/network)

**Troisième étape : Contactez-nous !**

**Mettez à jour le fichier built-in-peers.txt avec votre nouveau nœud**

Maintenant que vous avez la destination correcte pour votre nœud I2P-Bote, l’étape finale consiste à vous ajouter à la liste par défaut des pairs pour [I2P-Bote ici](https://github.com/i2p/i2p.i2p-bote/tree/master/core/src/main/resources/i2p/bote/network) ici. Vous pouvez le faire en créant un fork du dépôt, en vous ajoutant à la liste avec votre nom placé en commentaire, et votre destination de 516 caractères juste en dessous, comme ceci :

```
# idk
QuabT3H5ljZyd-PXCQjvDzdfCec-2yv8E9i6N71I5WHAtSEZgazQMReYNhPWakqOEj8BbpRvnarpHqbQjoT6yJ5UObKv2hA2M4XrroJmydPV9CLJUCqgCqFfpG-bkSo0gEhB-GRCUaugcAgHxddmxmAsJVRj3UeABLPHLYiakVz3CG2iBMHLJpnC6H3g8TJivtqabPYOxmZGCI-P~R-s4vwN2st1lJyKDl~u7OG6M6Y~gNbIzIYeQyNggvnANL3t6cUqS4v0Vb~t~CCtXgfhuK5SK65Rtkt2Aid3s7mrR2hDxK3SIxmAsHpnQ6MA~z0Nus-VVcNYcbHUBNpOcTeKlncXsuFj8vZL3ssnepmr2DCB25091t9B6r5~681xGEeqeIwuMHDeyoXIP0mhEcy3aEB1jcchLBRLMs6NtFKPlioxz0~Vs13VaNNP~78bTjFje5ya20ahWlO0Md~x5P5lWLIKDgaqwNdIrijtZAcILn1h18tmABYauYZQtYGyLTOXAAAA
```
et soumettre une pull request. C'est tout ce qu'il y a à faire, alors aidez à maintenir i2p en vie, décentralisé et fiable.
