---
title: "Développer des applications respectueuses de la vie privée avec Python et I2P"
date: 2018-10-23
author: "villain"
description: "Concepts de base du développement d’applications I2P avec Python"
categories: ["development"]
---

![i2plib](https://geti2p.net/images/blog/i2plib.jpeg)

[Invisible Internet Project](https://geti2p.net/) (I2P) fournit un cadre pour développer des applications respectueuses de la vie privée. C’est un réseau virtuel fonctionnant au-dessus d’Internet classique, dans lequel les hôtes peuvent échanger des données sans divulguer leur adresse IP "réelle". Les connexions au sein du réseau I2P sont établies entre des adresses virtuelles appelées *I2P destinations*. Il est possible d’avoir autant de destinations que nécessaire, voire d’utiliser une nouvelle destination pour chaque connexion ; elles ne divulguent aucune information sur l’adresse IP réelle à l’autre partie.

Cet article décrit les concepts de base qu’il faut connaître pour développer des applications I2P. Les exemples de code sont écrits en Python en utilisant le framework asynchrone intégré asyncio.

## Activation de l'API SAM et installation d'i2plib

I2P fournit de nombreuses API différentes aux applications clientes. Les applications client-serveur classiques peuvent utiliser I2PTunnel, des proxies HTTP et Socks, les applications Java utilisent généralement I2CP. Pour le développement avec d’autres langages, comme Python, la meilleure option est [SAM](/docs/api/samv3/). SAM est désactivé par défaut dans l’implémentation cliente Java d’origine, il faut donc l’activer. Accédez à Router Console, page "I2P internals" -> "Clients". Cochez "Run at Startup" et cliquez sur "Start", puis "Save Client Configuration".

![Activer l'API SAM](https://geti2p.net/images/enable-sam.jpeg)

[L’implémentation C++ i2pd](https://i2pd.website) inclut SAM activé par défaut.

J'ai développé une bibliothèque Python pratique pour SAM API appelée [i2plib](https://github.com/l-n-s/i2plib). Vous pouvez l'installer avec pip ou télécharger manuellement le code source depuis GitHub.

```bash
pip install i2plib
```
Cette bibliothèque fonctionne avec le [framework asynchrone asyncio](https://docs.python.org/3/library/asyncio.html) intégré à Python ; veuillez noter que les exemples de code sont tirés de fonctions asynchrones (coroutines) qui s'exécutent au sein de la boucle d'événements. Des exemples supplémentaires d'utilisation d'i2plib sont disponibles dans le [dépôt du code source](https://github.com/l-n-s/i2plib/tree/master/docs/examples).

## Destination I2P et création de session

Une destination I2P est littéralement un ensemble de clés de chiffrement et de signature cryptographique. Les clés publiques de cet ensemble sont publiées sur le réseau I2P et sont utilisées pour établir des connexions au lieu d’adresses IP.

Voici comment créer [i2plib.Destination](https://i2plib.readthedocs.io/en/latest/api.html#i2plib.Destination):

```python
dest = await i2plib.new_destination()
print(dest.base32 + ".b32.i2p") # print base32 address
```
L'adresse base32 est un hachage utilisé par d'autres pairs pour découvrir votre Destination complète dans le réseau. Si vous prévoyez d'utiliser cette Destination comme adresse permanente dans votre programme, enregistrez les données binaires de *dest.private_key.data* dans un fichier local.

Vous pouvez maintenant créer une session SAM, ce qui signifie littéralement mettre la Destination en ligne dans I2P :

```python
session_nickname = "test-i2p" # each session must have unique nickname
_, session_writer = await i2plib.create_session(session_nickname, destination=dest)
```
Remarque importante : la Destination restera en ligne tant que le socket de *session_writer* est maintenu ouvert. Si vous souhaitez l’arrêter, vous pouvez appeler *session_writer.close()*."

## Établir des connexions sortantes

Maintenant que la Destination est en ligne, vous pouvez l’utiliser pour vous connecter à d’autres pairs. Par exemple, voici comment vous connecter à "udhdrtrcetjm5sxzskjyr5ztpeszydbh4dpl3pl4utgqqw2v4jna.b32.i2p", envoyer une requête HTTP GET et lire la réponse (il s’agit du serveur web "i2p-projekt.i2p"):

```python
remote_host = "udhdrtrcetjm5sxzskjyr5ztpeszydbh4dpl3pl4utgqqw2v4jna.b32.i2p"
reader, writer = await i2plib.stream_connect(session_nickname, remote_host)

writer.write("GET /en/ HTTP/1.0\nHost: {}\r\n\r\n".format(remote_host).encode())

buflen, resp = 4096, b""
while 1:
    data = await reader.read(buflen)
    if len(data) > 0:
        resp += data
    else:
        break

writer.close()
print(resp.decode())
```
## Accepter les connexions entrantes

Si l’établissement de connexions sortantes est trivial, il y a un point important lorsque vous acceptez des connexions. Une fois qu’un nouveau client est connecté, l’API SAM envoie sur la socket une chaîne ASCII contenant la Destination (identifiant I2P du client) encodée en base64. Étant donné que la Destination et les données peuvent arriver en un seul bloc, vous devez en être conscient.

Voici à quoi ressemble un simple serveur PING-PONG. Il accepte une connexion entrante, enregistre la Destination du client dans la variable *remote_destination* et renvoie la chaîne "PONG" :

```python
async def handle_client(incoming, reader, writer):
    """Client connection handler"""
    dest, data = incoming.split(b"\n", 1)
    remote_destination = i2plib.Destination(dest.decode())
    if not data:
        data = await reader.read(BUFFER_SIZE)
    if data == b"PING":
        writer.write(b"PONG")
    writer.close()

# An endless loop which accepts connetions and runs a client handler
while True:
    reader, writer = await i2plib.stream_accept(session_nickname)
    incoming = await reader.read(BUFFER_SIZE)
    asyncio.ensure_future(handle_client(incoming, reader, writer))
```
## Plus d'informations

Cet article décrit l’utilisation d’un protocole de streaming de type TCP. SAM API fournit également un protocole de type UDP pour envoyer et recevoir des datagrammes. Cette fonctionnalité sera ajoutée à i2plib ultérieurement.

Ce ne sont que des informations de base, mais elles suffisent pour démarrer votre propre projet avec I2P. L’Internet invisible est un excellent outil pour développer toutes sortes d’applications respectueuses de la vie privée. Le réseau n’impose aucune contrainte de conception ; ces applications peuvent être client-serveur aussi bien que P2P.

- [Examples of i2plib usage](https://github.com/l-n-s/i2plib/tree/master/docs/examples)
- [i2plib documentation](https://i2plib.readthedocs.io/en/latest/)
- [i2plib at GitHub](https://github.com/l-n-s/i2plib)
- [SAM API documentation](/docs/api/samv3/)
- [asyncio documentation](https://docs.python.org/3/library/asyncio.html)
- [I2P network technical overview](https://geti2p.net/docs/how/tech-intro)
