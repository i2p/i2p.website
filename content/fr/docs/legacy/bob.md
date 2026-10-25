---
title: "BOB - Basic Open Bridge"
description: "API dépréciée pour la gestion des destinations"
slug: "bob"
aliases:
  - "/fr/docs/api/bob"
  - "/fr/docs/api/bob/"
  - "/fr/bob"
  - "/fr/bob/"
lastUpdated: "2025-05"
accurateFor: "0.9.8"
---

## Avertissement - Obsolète

Non destiné à être utilisé par de nouvelles applications. BOB, tel que spécifié ici, ne prend en charge que le type de signature DSA-SHA1. BOB ne sera pas étendu pour prendre en charge de nouveaux types de signatures ou d'autres fonctionnalités avancées. Les nouvelles applications doivent utiliser [SAM V3](/docs/api/samv3).

Le support BOB a été supprimé des nouvelles installations de Java I2P à partir de la version 1.7.0 (2022-02). Il fonctionnera toujours dans Java I2P initialement installé en version 1.6.1 ou antérieure, même après les mises à jour, mais il n'est plus supporté et peut cesser de fonctionner à tout moment. BOB est encore supporté par i2pd à partir de 2025-05, mais les applications devraient néanmoins migrer vers SAMv3 pour les raisons mentionnées ci-dessus. Consultez [la documentation i2pd](https://i2pd.readthedocs.io/en/latest/devs/i2pd-specifics/) pour toutes les extensions de l'API documentée ici qui sont supportées par i2pd.

À ce stade, la plupart des bonnes idées de BOB ont été intégrées dans SAMv3, qui offre plus de fonctionnalités et une utilisation plus répandue dans le monde réel. BOB peut encore fonctionner sur certaines installations (voir ci-dessus), mais il ne bénéficie pas des fonctionnalités avancées disponibles dans SAMv3 et n'est essentiellement plus pris en charge, sauf par i2pd.

## Bibliothèques de langage pour l'API BOB

- Go - [ccondom](https://bitbucket.org/kallevedin/ccondom)
- Python - i2py-bob (git.repo.i2p)
- Twisted - [txi2p](https://pypi.python.org/pypi/txi2p)
- C++ - [bobcpp](https://gitlab.com/rszibele/bobcpp)

## Aperçu

`KEYS` = paire de clés publique+privée, celles-ci sont en BASE64

`KEY` = clé publique, également en BASE64

`ERROR` comme son nom l'indique retourne le message `"ERROR "+DESCRIPTION+"\n"`, où la `DESCRIPTION` est ce qui s'est mal passé.

`OK` retourne `"OK"`, et si des données doivent être retournées, elles se trouvent sur la même ligne. `OK` signifie que la commande est terminée.

Les lignes `DATA` contiennent les informations que vous avez demandées. Il peut y avoir plusieurs lignes `DATA` par requête.

**REMARQUE :** La commande help est la SEULE commande qui fait exception aux règles... elle peut en fait ne rien retourner ! C'est intentionnel, puisque help est une commande HUMAINE et non une commande d'APPLICATION.

## Connexion et Version

Toute sortie de statut BOB se fait par lignes. Les lignes peuvent se terminer par \\n ou \\r\\n, selon le système. Lors de la connexion, BOB produit deux lignes :

```
BOB version
OK
```
La version actuelle est : 00.00.10

Notez que les versions précédentes utilisaient des chiffres hexadécimaux en majuscules et ne respectaient pas les standards de versioning I2P. Il est recommandé que les versions ultérieures utilisent uniquement les chiffres 0-9.

### Historique des versions

<table style="width:100%; border-collapse:collapse; margin-bottom:1.5rem;">
  <thead>
    <tr>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">I2P Router Version</th>
      <th style="border:1px solid var(--color-border); padding:0.5rem; background:var(--color-bg-secondary); text-align:left;">Changes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">00.00.10</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">0.9.8</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">current version</td>
    </tr>
    <tr>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">00.00.00 - 00.00.0F</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">&nbsp;</td>
      <td style="border:1px solid var(--color-border); padding:0.5rem;">development versions</td>
    </tr>
  </tbody>
</table>
## Commandes

**VEUILLEZ NOTER :** Pour les détails ACTUELS sur les commandes, VEUILLEZ utiliser la commande d'aide intégrée. Il suffit de vous connecter en telnet à localhost 2827 et de taper help pour obtenir la documentation complète de chaque commande.

Les commandes ne deviennent jamais obsolètes ou ne sont jamais modifiées, cependant de nouvelles commandes sont ajoutées de temps en temps.

```
COMMAND     OPERAND                             RETURNS
help        (optional command to get help on)   NOTHING or OK and description of the command
clear                                           ERROR or OK
getdest                                         ERROR or OK and KEY
getkeys                                         ERROR or OK and KEYS
getnick     tunnelname                          ERROR or OK
inhost      hostname or IP address              ERROR or OK
inport      port number                         ERROR or OK
list                                            ERROR or DATA lines and final OK
lookup      hostname                            ERROR or OK and KEY
newkeys                                         ERROR or OK and KEY
option      key1=value1 key2=value2...          ERROR or OK
outhost     hostname or IP address              ERROR or OK
outport     port number                         ERROR or OK
quiet                                           ERROR or OK
quit                                            OK and terminates the command connection
setkeys     KEYS                                ERROR or OK and KEY
setnick     tunnel nickname                     ERROR or OK
show                                            ERROR or OK and information
showprops                                       ERROR or OK and information
start                                           ERROR or OK
status      tunnel nickname                     ERROR or OK and information
stop                                            ERROR or OK
verify      KEY                                 ERROR or OK
visit                                           OK, and dumps BOB's threads to the wrapper.log
zap                                             nothing, quits BOB
```
Une fois configuré, tous les sockets TCP peuvent et vont se bloquer selon les besoins, et il n'y a pas besoin de messages supplémentaires vers/depuis le canal de commande. Cela permet au routeur de réguler le flux sans exploser avec des erreurs de mémoire insuffisante comme le fait SAM lorsqu'il s'étouffe en tentant de faire passer de nombreux flux dans ou hors d'un seul socket -- cela ne peut pas passer à l'échelle quand vous avez beaucoup de connexions !

Ce qui est également agréable avec cette interface particulière, c'est qu'écrire quoi que ce soit pour s'interfacer avec elle est beaucoup, beaucoup plus facile qu'avec SAM. Il n'y a aucun autre traitement à faire après la configuration. Sa configuration est si simple que des outils très simples, comme nc (netcat) peuvent être utilisés pour pointer vers une application. L'intérêt est qu'on pourrait programmer les heures de montée et de descente d'une application, sans avoir à modifier l'application pour cela, ou même sans avoir à arrêter cette application. À la place, vous pouvez littéralement "débrancher" la destination, et la "rebrancher" à nouveau. Tant que les mêmes adresses IP/port et les mêmes clés de destination sont utilisées lors de la remontée du pont, l'application TCP normale s'en fichera et ne le remarquera pas. Elle sera simplement trompée -- les destinations ne sont pas accessibles, et rien n'arrive.

## Exemples

Pour l'exemple suivant, nous allons configurer une connexion de bouclage local très simple, avec deux destinations. La destination "mouth" sera le service CHARGEN du démon superserveur INET. La destination "ear" sera un port local dans lequel vous pouvez vous connecter en telnet, et regarder le joli vomi de test ASCII se déverser.

### Exemple de dialogue de session

Un simple telnet 127.0.0.1 2827 fonctionne.

- A = Application
- C = Réponse de commande de BOB.

```
FROM    TO      DIALOGUE
C       A       BOB 00.00.10
C       A       OK
A       C       setnick mouth
C       A       OK Nickname set to mouth
A       C       newkeys
C       A       OK ZMPz1zinTdy3~zGD~f3g9aikZTipujEvvXOEyYfq4Su-mNKerqG710hFbkR6P-xkouVyNQsqWLI8c6ngnkSwGdUfM7hGccqBYDjIubTrlr~0g2-l0vM7Y8nSqtFrSdMw~pyufXZ0Ys3NqUSb8NuZXpiH2lCCkFG21QPRVfKBGwvvyDVU~hPVfBHuR8vkd5x0teMXGGmiTzdB96DuNRWayM0y8vkP-1KJiPFxKjOXULjuXhLmINIOYn39bQprq~dAtNALoBgd-waZedYgFLvwHDCc9Gui8Cpp41EihlYGNW0cu0vhNFUN79N4DEpO7AtJyrSu5ZjFTAGjLw~lOvhyO2NwQ4RiC4UCKSuM70Fz0BFKTJquIjUNkQ8pBPBYvJRRlRG9HjAcSqAMckC3pvKKlcTJJBAE8GqexV7rdCCIsnasJXle-6DoWrDkY1s1KNbEVH6i1iUEtmFr2IHTpPeFCyWfZ581CAFNRbbUs-MmnZu1tXAYF7I2-oXTH2hXoxCGAAAA
```
**NOTEZ BIEN LA CLÉ DE DESTINATION CI-DESSUS, LA VÔTRE SERA DIFFÉRENTE !**

```
FROM    TO      DIALOGUE
A       C       outhost 127.0.0.1
C       A       OK outhost set
A       C       outport 19
C       A       OK outbound port set
A       C       start
C       A       OK tunnel starting
```
À ce stade, il n'y avait pas d'erreur, une destination avec le surnom "mouth" est configurée. Lorsque vous contactez la destination fournie, vous vous connectez en fait au service `CHARGEN` sur `19/TCP`.

Maintenant pour l'autre moitié, afin que nous puissions effectivement contacter cette destination.

```
FROM    TO      DIALOGUE
C       A       BOB 00.00.10
C       A       OK
A       C       setnick ear
C       A       OK Nickname set to ear
A       C       newkeys
C       A       OK 8SlWuZ6QNKHPZ8KLUlExLwtglhizZ7TG19T7VwN25AbLPsoxW0fgLY8drcH0r8Klg~3eXtL-7S-qU-wdP-6VF~ulWCWtDMn5UaPDCZytdGPni9pK9l1Oudqd2lGhLA4DeQ0QRKU9Z1ESqejAIFZ9rjKdij8UQ4amuLEyoI0GYs2J~flAvF4wrbF-LfVpMdg~tjtns6fA~EAAM1C4AFGId9RTGot6wwmbVmKKFUbbSmqdHgE6x8-xtqjeU80osyzeN7Jr7S7XO1bivxEDnhIjvMvR9sVNC81f1CsVGzW8AVNX5msEudLEggpbcjynoi-968tDLdvb-CtablzwkWBOhSwhHIXbbDEm0Zlw17qKZw4rzpsJzQg5zbGmGoPgrSD80FyMdTCG0-f~dzoRCapAGDDTTnvjXuLrZ-vN-orT~HIVYoHV7An6t6whgiSXNqeEFq9j52G95MhYIfXQ79pO9mcJtV3sfea6aGkMzqmCP3aikwf4G3y0RVbcPcNMQetDAAAA
A       C       inhost 127.0.0.1
C       A       OK inhost set
A       C       inport 37337
C       A       OK inbound port set
A       C       start
C       A       OK tunnel starting
A       C       quit
C       A       OK Bye!
```
Maintenant, tout ce que nous avons à faire est de nous connecter en telnet à 127.0.0.1, port 37337, et d'envoyer la clé de destination ou l'adresse d'hôte du carnet d'adresses que nous voulons contacter. Dans ce cas, nous voulons contacter "mouth", il suffit de coller la clé et c'est parti.

**REMARQUE :** La commande "quit" dans le canal de commande ne déconnecte PAS les tunnels comme SAM.

```
$ telnet 127.0.0.1 37337
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
ZMPz1zinTdy3~zGD~f3g9aikZTipujEvvXOEyYfq4Su-mNKerqG710hFbkR6P-xkouVyNQsqWLI8c6ngnkSwGdUfM7hGccqBYDjIubTrlr~0g2-l0vM7Y8nSqtFrSdMw~pyufXZ0Ys3NqUSb8NuZXpiH2lCCkFG21QPRVfKBGwvvyDVU~hPVfBHuR8vkd5x0teMXGGmiTzdB96DuNRWayM0y8vkP-1KJiPFxKjOXULjuXhLmINIOYn39bQprq~dAtNALoBgd-waZedYgFLvwHDCc9Gui8Cpp41EihlYGNW0cu0vhNFUN79N4DEpO7AtJyrSu5ZjFTAGjLw~lOvhyO2NwQ4RiC4UCKSuM70Fz0BFKTJquIjUNkQ8pBPBYvJRRlRG9HjAcSqAMckC3pvKKlcTJJBAE8GqexV7rdCCIsnasJXle-6DoWrDkY1s1KNbEVH6i1iUEtmFr2IHTpPeFCyWfZ581CAFNRbbUs-MmnZu1tXAYF7I2-oXTH2hXoxCGAAAA
 !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefg
!"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefgh
"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghi
#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghij
$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijk
...
```
Après quelques kilomètres virtuels de ce déversement, appuyez sur `Control-]`

```
...
cdefghijklmnopqrstuvwxyz{|}~ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJK
defghijklmnopqrstuvwxyz{|}~ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKL
efghijklmnopqrstuvwxyz{|}~ !"#$%&'()*+,-./0123456789:;<=
telnet> c
Connection closed.
```
Voici ce qui s'est passé...

```
telnet -> ear -> i2p -> mouth -> chargen -.
telnet <- ear <- i2p <- mouth <-----------'
```
Vous pouvez aussi vous connecter aux SITES I2P !

```
$ telnet 127.0.0.1 37337
Trying 127.0.0.1...
Connected to 127.0.0.1.
Escape character is '^]'.
i2host.i2p
GET / HTTP/1.1

HTTP/1.1 200 OK
Date: Fri, 05 Dec 2008 14:20:28 GMT
Connection: close
Content-Type: text/html
Content-Length: 3946
Last-Modified: Fri, 05 Dec 2008 10:33:36 GMT
Accept-Ranges: bytes

<html>
<head>
  <title>I2HOST</title>
  <link rel="shortcut icon" href="favicon.ico">
</head>
...
<a href="http://sponge.i2p/">--Sponge.</a></pre>
<img src="/counter.gif" alt="!@^7A76Z!#(*&%"> visitors. </body>
</html>
Connection closed by foreign host.
$
```
Plutôt cool, n'est-ce pas ? Essayez d'autres SITES I2P bien connus si vous voulez, des inexistants, etc., pour vous faire une idée du type de sortie à attendre dans différentes situations. Pour la plupart, il est suggéré d'ignorer tous les messages d'erreur. Ils seraient dénués de sens pour l'application, et ne sont présentés que pour le débogage humain.

### Nettoyage

Maintenant que nous en avons terminé avec elles, supprimons nos destinations.

Commençons par voir quels pseudonymes de destination nous avons.

```
FROM    TO      DIALOGUE
A       C       list
C       A       DATA NICKNAME: mouth STARTING: false RUNNING: true STOPPING: false KEYS: true QUIET: false INPORT: not_set INHOST: localhost OUTPORT: 19 OUTHOST: 127.0.0.1
C       A       DATA NICKNAME: ear STARTING: false RUNNING: true STOPPING: false KEYS: true QUIET: false INPORT: 37337 INHOST: 127.0.0.1 OUTPORT: not_set OUTHOST: localhost
C       A       OK Listing done
```
D'accord, les voilà. D'abord, supprimons "mouth".

```
FROM    TO      DIALOGUE
A       C       getnick mouth
C       A       OK Nickname set to mouth
A       C       stop
C       A       OK tunnel stopping
A       C       clear
C       A       OK cleared
```
Maintenant pour supprimer "ear", notez que c'est ce qui arrive quand vous tapez trop vite, et cela vous montre à quoi ressemblent les messages d'ERREUR typiques.

```
FROM    TO      DIALOGUE
A       C       getnick ear
C       A       OK Nickname set to ear
A       C       stop
C       A       OK tunnel stopping
A       C       clear
C       A       ERROR tunnel is active
A       C       clear
C       A       OK cleared
A       C       quit
C       A       OK Bye!
```
## Mode Silencieux

Je ne vais pas me donner la peine de montrer un exemple du côté récepteur d'un pont car c'est très simple. Il y a deux paramètres possibles pour celui-ci, et il est basculé avec la commande "quiet".

Par défaut, ce n'est PAS silencieux, et les premières données qui arrivent dans votre socket d'écoute correspondent à la destination qui établit le contact. Il s'agit d'une seule ligne constituée de l'adresse BASE64 suivie d'un caractère de nouvelle ligne. Tout ce qui suit est destiné à être réellement consommé par l'application.

En mode silencieux, considérez-le comme une connexion Internet normale. Aucune donnée supplémentaire n'arrive du tout. C'est exactement comme si vous étiez simplement connecté à Internet normal. Ce mode permet une forme de transparence similaire à celle disponible sur les pages de paramètres de tunnel de la console du router, de sorte que vous pouvez utiliser BOB pour pointer une destination vers un serveur web, par exemple, et vous n'auriez pas du tout à modifier le serveur web.

## Avantages de BOB

L'avantage d'utiliser BOB pour cela est comme discuté précédemment. Vous pourriez programmer des temps de fonctionnement aléatoires pour l'application, rediriger vers une machine différente, etc. Une utilisation de ceci pourrait être quelque chose comme vouloir essayer de perturber la détection de disponibilité router-vers-destination. Vous pourriez arrêter et démarrer la destination avec un processus totalement différent pour créer des temps de disponibilité et d'indisponibilité aléatoires sur les services. De cette façon, vous ne feriez qu'arrêter la capacité à contacter un tel service, et n'auriez pas à vous embêter à l'arrêter et le redémarrer. Vous pourriez rediriger et pointer vers une machine différente sur votre LAN pendant que vous faites des mises à jour, ou pointer vers un ensemble de machines de sauvegarde selon ce qui fonctionne, etc, etc. Seule votre imagination limite ce que vous pourriez faire avec BOB.
