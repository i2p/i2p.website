---
title: "Aperçu de I2CP"
description: "Aperçu du protocole client I2P (I2CP) - gestion des sessions, options, format de la charge utile et multiplexage."
slug: "i2cp-overview"
aliases:
  - "/fr/docs/protocol/i2cp"
  - "/fr/docs/protocol/i2cp/"
  - "/fr/i2cp"
  - "/fr/i2cp/"
category: "Protocoles"
lastUpdated: "2025-04"
accurateFor: "0.9.66"
---

## Aperçu

Le protocole client I2P (I2CP) assure une séparation stricte des responsabilités entre le routeur et tout client souhaitant communiquer via le réseau. Il permet des échanges sécurisés et asynchrones en envoyant et en recevant des messages sur une seule socket TCP. Grâce à I2CP, une application cliente indique au routeur son identité (sa « destination »), les compromis souhaités en matière d'anonymat, de fiabilité et de latence, ainsi que les destinataires des messages. En retour, le routeur utilise I2CP pour informer le client de l'arrivée de messages et pour demander l'autorisation d'utiliser certains tunnels.

Le protocole lui-même est implémenté en Java, afin de fournir le SDK client. Ce SDK est exposé dans le paquet i2p.jar, qui implémente le côté client d'I2CP. Les clients ne devraient jamais avoir à accéder au paquet router.jar, qui contient le routeur lui-même ainsi que le côté routeur d'I2CP. Un client non-Java devrait également implémenter la [bibliothèque de streaming](/docs/api/streaming/) pour les connexions de type TCP.

Les applications peuvent tirer parti de l'I2CP de base ainsi que des bibliothèques de [flux](/docs/api/streaming/) et de [datagrammes](/docs/specs/datagrams/) en utilisant le protocole [Simple Anonymous Messaging (SAM)](/docs/api/samv3/), qui ne demande pas aux clients de gérer quelque forme de cryptographie que ce soit. De plus, les clients peuvent accéder au réseau via plusieurs types de proxys - HTTP, CONNECT, et SOCKS 4/4a/5. Alternativement, les clients Java peuvent accéder à ces bibliothèques via ministreaming.jar et streaming.jar. Il existe donc plusieurs options pour les applications Java comme pour celles qui ne le sont pas.

Le chiffrement de bout en bout côté client (chiffrement des données sur la connexion I2CP) a été désactivé dans la version 0.6 d'I2P, laissant en place le chiffrement de bout en bout ElGamal/AES qui est implémenté au niveau du routeur. La seule cryptographie que les bibliothèques clientes doivent encore implémenter est la signature de clés publique/privée DSA pour les [LeaseSets](/docs/specs/i2cp/#msg_CreateLeaseSet) et les [Configurations de session](/docs/specs/i2cp/#struct_SessionConfig), ainsi que la gestion de ces clés.

Dans une installation standard d'I2P, le port 7654 est utilisé par les clients Java externes pour communiquer avec le routeur local via I2CP. Par défaut, le routeur s'associe à l'adresse 127.0.0.1. Pour s'associer à 0.0.0.0, définissez l'option de configuration avancée du routeur `i2cp.tcp.bindAllInterfaces=true` et redémarrez. Les clients situés dans la même machine virtuelle Java (JVM) que le routeur transmettent les messages directement au routeur via une interface JVM interne.

Certaines implémentations de routeur et de client peuvent également prendre en charge les connexions externes via SSL, comme configuré par l'option `i2cp.SSL=true`. Bien que SSL ne soit pas activé par défaut, son utilisation est fortement recommandée pour tout trafic susceptible d'être exposé à Internet. Le nom d'utilisateur et le mot de passe d'autorisation (le cas échéant), la [clé privée](/docs/specs/common-structures/#type_PrivateKey) et la [clé privée de signature](/docs/specs/common-structures/#type_SigningPrivateKey) pour la [Destination](/docs/specs/common-structures/#struct_Destination) sont tous transmis en clair sauf si SSL est activé. Certaines implémentations de routeur et de client peuvent également prendre en charge les connexions externes via des sockets de domaine.

## Spécification du protocole I2CP

Voir la [page de spécification I2CP](/docs/specs/i2cp/) pour la spécification complète du protocole.

## Initialisation I2CP {#initialization}

Lorsqu'un client se connecte au routeur, il envoie d'abord un unique octet indiquant la version du protocole (0x2A). Ensuite, il envoie un message [GetDate](/docs/specs/i2cp/#msg_GetDate) et attend la réponse [SetDate](/docs/specs/i2cp/#msg_SetDate). Puis, il envoie un message [CreateSession](/docs/specs/i2cp/#msg_CreateSession) contenant la configuration de la session. Il attend ensuite un message [RequestLeaseSet](/docs/specs/i2cp/#msg_RequestLeaseSet) provenant du routeur, indiquant que les tunnels entrants ont été créés, et répond avec un message CreateLeaseSet contenant le LeaseSet signé. Le client peut désormais initier ou recevoir des connexions depuis d'autres destinations I2P.

## Options I2CP {#options}

### Options côté routeur

Les options suivantes sont traditionnellement transmises au routeur via un [SessionConfig](/docs/specs/i2cp/#struct_SessionConfig) contenu dans un message [CreateSession](/docs/specs/i2cp/#msg_CreateSession) ou un message [ReconfigureSession](/docs/specs/i2cp/#msg_ReconfigureSession).

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;" colspan="6">Router-side Options</th>
</tr>
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Option</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">As Of Release</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Recommended Arguments</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Allowable Range</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Default</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Description</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">clientMessageTimeout</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">8*1000 - 120*1000</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">60*1000</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The timeout (ms) for all sent messages. Unused. See the protocol specification for per-message settings.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">crypto.lowTagThreshold</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1-128</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">30</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Minimum number of ElGamal/AES Session Tags before we send more. Recommended: approximately tagsToSend * 2/3</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">crypto.ratchet.inboundTags</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.47</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1-?</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">160</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Inbound tag window for ECIES-X25519-AEAD-Ratchet. Local inbound tagset size. See proposal 144.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">crypto.ratchet.outboundTags</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.47</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1-?</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">160</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Outbound tag window for ECIES-X25519-AEAD-Ratchet. Advisory to send to the far-end in the options block. See proposal 144.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">crypto.tagsToSend</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1-128</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">40</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Number of ElGamal/AES Session Tags to send at a time. For clients with relatively low bandwidth per-client-pair (IRC, some UDP apps), this may be set lower.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">explicitPeers</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">null</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Comma-separated list of Base 64 Hashes of peers to build tunnels through; for debugging only</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.dontPublishLeaseSet</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true, false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Should generally be set to true for clients and false for servers</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.fastReceive</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true, false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">If true, the router just sends the MessagePayload instead of sending a MessageStatus and awaiting a ReceiveMessageBegin.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetAuthType</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0-2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The type of authentication for encrypted LS2. 0 for no per-client authentication (the default); 1 for DH per-client authentication; 2 for PSK per-client authentication. See proposal 123.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetEncType</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4,0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0-65535,...</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The encryption type to be used, as of 0.9.38. Interpreted client-side, but also passed to the router in the SessionConfig, to declare intent and check support. As of 0.9.39, may be comma-separated values for multiple types. See PublicKey in common structures spec for values. See proposals 123, 144, and 145.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetOfflineExpiration</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The expiration of the offline signature, 4 bytes, seconds since the epoch. See proposal 123.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetOfflineSignature</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The base 64 of the offline signature. See proposal 123.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetPrivKey</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">A base 64 X25519 private key for the router to use to decrypt the encrypted LS2 locally, only if per-client authentication is enabled. Optionally preceded by the key type and ':'. Only "ECIES_X25519:" is supported, which is the default. See proposal 123. Do not confuse with i2cp.leaseSetPrivateKey which is for the leaseset encryption keys.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetSecret</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.39</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">""</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Base 64 encoded UTF-8 secret used to blind the leaseset address. See proposal 123.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetTransientPublicKey</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">[type:]b64 The base 64 of the transient private key, prefixed by an optional sig type number or name, default DSA_SHA1. See proposal 123.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetType</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1,3,5,7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1-255</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The type of leaseset to be sent in the CreateLeaseSet2 Message. Interpreted client-side, but also passed to the router in the SessionConfig, to declare intent and check support. See proposal 123.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.messageReliability</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">BestEffort, None</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">BestEffort</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Guaranteed is disabled; None implemented in 0.8.1; the streaming lib default is None as of 0.8.1, the client side default is None as of 0.9.4</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.password</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">string</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;" rowspan="2">For authorization, if required by the router. If the client is running in the same JVM as a router, this option is not required. Warning - username and password are sent in the clear to the router, unless using SSL (i2cp.SSL=true). Authorization is only recommended when using SSL.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.username</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">string</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">inbound.allowZeroHop</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true, false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">If incoming zero hop tunnel is allowed</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">outbound.allowZeroHop</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true, false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">If outgoing zero hop tunnel is allowed</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">inbound.backupQuantity</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">number from 0 to 3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">No limit</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Number of redundant fail-over for tunnels in</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">outbound.backupQuantity</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">number from 0 to 3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">No limit</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Number of redundant fail-over for tunnels out</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">inbound.IPRestriction</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">number from 0 to 4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 to 4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Number of IP bytes to match to determine if two routers should not be in the same tunnel. 0 to disable.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">outbound.IPRestriction</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">number from 0 to 4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 to 4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Number of IP bytes to match to determine if two routers should not be in the same tunnel. 0 to disable.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">inbound.length</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">number from 0 to 3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 to 7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Length of tunnels in</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">outbound.length</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">number from 0 to 3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0 to 7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Length of tunnels out</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">inbound.lengthVariance</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">number from -1 to 2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">-7 to 7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Random amount to add or subtract to the length of tunnels in. A positive number x means add a random amount from 0 to x inclusive. A negative number -x means add a random amount from -x to x inclusive. The router will limit the total length of the tunnel to 0 to 7 inclusive. The default variance was 1 prior to release 0.7.6.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">outbound.lengthVariance</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">number from -1 to 2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">-7 to 7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Random amount to add or subtract to the length of tunnels out. A positive number x means add a random amount from 0 to x inclusive. A negative number -x means add a random amount from -x to x inclusive. The router will limit the total length of the tunnel to 0 to 7 inclusive. The default variance was 1 prior to release 0.7.6.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">inbound.nickname</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">string</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Name of tunnel - generally used in routerconsole, which will use the first few characters of the Base64 hash of the destination by default.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">outbound.nickname</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">string</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Name of tunnel - generally ignored unless inbound.nickname is unset.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">outbound.priority</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">number from -25 to 25</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">-25 to 25</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Priority adjustment for outbound messages. Higher is higher priority.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">inbound.quantity</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">number from 1 to 3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 to 16</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Number of tunnels in. Limit was increased from 6 to 16 in release 0.9; however, numbers higher than 6 are incompatible with older releases.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">outbound.quantity</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">number from 1 to 3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">No limit</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Number of tunnels out</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">inbound.randomKey</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.17</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Base 64 encoding of 32 random bytes</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;" rowspan="2">Used for consistent peer ordering across restarts.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">outbound.randomKey</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.17</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Base 64 encoding of 32 random bytes</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">inbound.*</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Any other options prefixed with "inbound." are stored in the "unknown options" properties of the inbound tunnel pool's settings.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">outbound.*</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Any other options prefixed with "outbound." are stored in the "unknown options" properties of the outbound tunnel pool's settings.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">shouldBundleReplyInfo</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true, false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Set to false to disable ever bundling a reply LeaseSet. For clients that do not publish their LeaseSet, this option must be true for any reply to be possible. "true" is also recommended for multihomed servers with long connection times.

Setting to "false" may save significant outbound bandwidth, especially if the client is configured with a large number of inbound tunnels (Leases). If replies are still required, this may shift the bandwidth burden to the far-end client and the floodfill. There are several cases where "false" may be appropriate:

- Unidirectional communication, no reply required
- LeaseSet is published and higher reply latency is acceptable
- LeaseSet is published, client is a "server", all connections are inbound so the connecting far-end destination obviously has the leaseset already. Connections are either short, or it is acceptable for latency on a long-lived connection to temporarily increase while the other end re-fetches the LeaseSet after expiration. HTTP servers may fit these requirements.</td>
</tr>
</table>
Remarque : des paramètres élevés en quantité, en longueur ou en variance peuvent entraîner des problèmes importants de performance ou de fiabilité.

Remarque : À partir de la version 0.7.7, les noms et valeurs des options doivent utiliser l'encodage UTF-8. Cela est principalement utile pour les surnoms. Avant cette version, les options contenant des caractères multioctets étaient corrompues. Étant donné que les options sont encodées dans une [Mapping](/docs/specs/common-structures/#type_Mapping), les noms et valeurs d'options sont limités à un maximum de 255 octets (et non caractères).

### Options côté client

Les options suivantes sont interprétées côté client et seront prises en compte si elles sont transmises à la I2PSession via l'appel I2PClient.createSession(). La bibliothèque de streaming devrait également transmettre ces options à I2CP. D'autres implémentations peuvent avoir des valeurs par défaut différentes.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;" colspan="6">Client-side Options</th>
</tr>
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Option</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">As Of Release</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Recommended Arguments</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Allowable Range</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Default</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Description</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.closeIdleTime</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1800000</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">300000 minimum</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">(ms) Idle time required (default 30 minutes)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.closeOnIdle</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true, false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Close I2P session when idle</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.encryptLeaseSet</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true, false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Encrypt the lease</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.fastReceive</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true, false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">If true, the router just sends the MessagePayload instead of sending a MessageStatus and awaiting a ReceiveMessageBegin.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.gzip</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.6.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true, false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Gzip outbound data</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetAuthType</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0-2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The type of authentication for encrypted LS2. 0 for no per-client authentication (the default); 1 for DH per-client authentication; 2 for PSK per-client authentication. See proposal 123.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetBlindedType</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.39</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0-65535</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">See prop. 123</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The sig type of the blinded key for encrypted LS2. Default depends on the destination sig type. See proposal 123.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetClient.dh.nnn</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">b64name:b64pubkey</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The base 64 of the client name (ignored, UI use only), followed by a ':', followed by the base 64 of the public key to use for DH per-client auth. nnn starts with 0. See proposal 123.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetClient.psk.nnn</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">b64name:b64privkey</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The base 64 of the client name (ignored, UI use only), followed by a ':', followed by the base 64 of the private key to use for PSK per-client auth. nnn starts with 0. See proposal 123.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetEncType</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0-65535,...</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The encryption type to be used, as of 0.9.38. Interpreted client-side, but also passed to the router in the SessionConfig, to declare intent and check support. As of 0.9.39, may be comma-separated values for multiple types. See also i2cp.leaseSetPrivateKey. See PublicKey in common structures spec for values. See proposals 123, 144, and 145.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetKey</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">For encrypted leasesets. Base 64 SessionKey (44 characters)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetOption.nnn</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">srvKey=srvValue</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">A service record to be placed in the LeaseSet2 options. Example: "_smtp._tcp=1 86400 0 0 25 ...b32.i2p". nnn starts with 0. See proposal 167.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetPrivateKey</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.18</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Base 64 private keys for encryption. Optionally preceded by the encryption type name or number and ':'. For LS1, only one key is supported, and only "0:" or "ELGAMAL_2048:" is supported, which is the default. As of 0.9.39, for LS2, multiple keys may be comma-separated, and each key must be a different encryption type. I2CP will generate the public key from the private key. Use for persistent leaseset keys across restarts. See proposals 123, 144, and 145. See also i2cp.leaseSetEncType. Do not confuse with i2cp.leaseSetPrivKey which is for encrypted LS2.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetSecret</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.39</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">""</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Base 64 encoded UTF-8 secret used to blind the leaseset address. See proposal 123.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetSigningPrivateKey</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.18</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Base 64 private key for signatures. Optionally preceded by the key type and ':'. DSA_SHA1 is the default. Key type must match the signature type in the destination. I2CP will generate the public key from the private key. Use for persistent leaseset keys across restarts.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.leaseSetType</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1,3,5,7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1-255</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The type of leaseset to be sent in the CreateLeaseSet2 Message. Interpreted client-side, but also passed to the router in the SessionConfig, to declare intent and check support. See proposal 123.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.messageReliability</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">BestEffort, None</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">None</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Guaranteed is disabled; None implemented in 0.8.1; None is the default as of 0.9.4</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.reduceIdleTime</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1200000</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">300000 minimum</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">(ms) Idle time required (default 20 minutes, minimum 5 minutes)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.reduceOnIdle</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true, false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Reduce tunnel quantity when idle</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.reduceQuantity</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1 to 5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Tunnel quantity when reduced (applies to both inbound and outbound)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.SSL</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">true, false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">false</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Connect to the router using SSL. If the client is running in the same JVM as a router, this option is ignored, and the client connects to that router internally.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.tcp.host</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">127.0.0.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Router hostname. If the client is running in the same JVM as a router, this option is ignored, and the client connects to that router internally.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.tcp.port</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1-65535</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7654</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Router I2CP port. If the client is running in the same JVM as a router, this option is ignored, and the client connects to that router internally.</td>
</tr>
</table>
Remarque : Tous les arguments, y compris les nombres, sont des chaînes de caractères. Les valeurs vrai/faux sont des chaînes insensibles à la casse. Toute valeur autre qu'une chaîne « true » (insensible à la casse) est interprétée comme faux. Les noms d'options sont sensibles à la casse.

## Format des données utiles I2CP et multiplexage {#format}

Les messages de bout en bout gérés par I2CP (c'est-à-dire les données envoyées par le client dans un [SendMessageMessage](/docs/specs/i2cp/#msg_SendMessage) et reçues par le client dans un [MessagePayloadMessage](/docs/specs/i2cp/#msg_MessagePayload)) sont compressés avec un en-tête gzip standard de 10 octets commençant par 0x1F 0x8B 0x08, tel que spécifié par la [RFC 1952](http://www.ietf.org/rfc/rfc1952.txt). À compter de la version 0.7.1, I2P utilise des parties ignorées de l'en-tête gzip pour inclure des informations sur le protocole, le port d'origine (from-port) et le port de destination (to-port), permettant ainsi aux flux et aux datagrammes d'utiliser la même destination, et rendant fiables les échanges requête/réponse par datagrammes en présence de plusieurs canaux.

La fonction gzip ne peut pas être complètement désactivée, mais définir `i2cp.gzip=false` règle l'effort de compression gzip à 0, ce qui peut permettre d'économiser un peu de CPU. Les implémentations peuvent choisir différents niveaux d'effort gzip selon les sockets ou les messages, en fonction d'une évaluation de la compressibilité du contenu. En raison de la compressibilité du remplissage de destination mise en œuvre dans l'API 0.9.57 (proposition 161), il est recommandé de compresser les paquets SYN de flux dans les deux sens ainsi que les datagrammes avec accusé de réception, même si la charge utile n'est pas compressible. Les implémentations peuvent souhaiter écrire une fonction gzip/gunzip simplifiée pour un effort gzip de 0, ce qui offrirait de grandes améliorations d'efficacité par rapport à une bibliothèque gzip dans ce cas précis.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Bytes</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Content</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0-2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Gzip header 0x1F 0x8B 0x08</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Gzip flags</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4-5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">I2P Source port (Gzip mtime)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">6-7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">I2P Destination port (Gzip mtime)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">8</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Gzip xflags (set to 2 to be indistinguishable from the Java implementation)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">9</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">I2P Protocol (6 = Streaming, 17 = Datagram, 18 = Raw Datagrams) (Gzip OS)</td>
</tr>
</table>
Remarque : les numéros de protocole I2P 224 à 254 sont réservés aux protocoles expérimentaux. Le numéro de protocole I2P 255 est réservé à un usage futur.

L'intégrité des données est vérifiée à l'aide du CRC-32 standard gzip tel que spécifié par la [RFC 1952](http://www.ietf.org/rfc/rfc1952.txt).

## Différences importantes par rapport à l'IP standard {#ip-differences}

Les ports I2CP sont destinés aux sockets et aux datagrammes I2P. Ils n'ont aucun rapport avec vos sockets ou ports locaux. Étant donné qu'I2P ne prenait pas en charge les ports et les numéros de protocole avant la version 0.7.1, les ports et les numéros de protocole sont légèrement différents de ceux utilisés dans l'IP standard, pour des raisons de compatibilité ascendante :

- Le port 0 est valide et a une signification particulière.
- Les ports 1 à 1023 ne sont ni spéciaux ni privilégiés.
- Les serveurs écoutent sur le port 0 par défaut, ce qui signifie « tous les ports ».
- Les clients envoient vers le port 0 par défaut, ce qui signifie « n'importe quel port ».
- Les clients envoient depuis le port 0 par défaut, ce qui signifie « non spécifié ».
- Un serveur peut avoir un service à l'écoute sur le port 0 et d'autres services à l'écoute sur des ports supérieurs. Dans ce cas, le service sur le port 0 est celui par défaut, et une connexion sera établie avec lui si le port de la socket entrante ou du datagramme ne correspond à aucun autre service.
- La plupart des destinations I2P n'exécutent qu'un seul service, vous pouvez donc utiliser les valeurs par défaut et ignorer la configuration du port I2CP.
- Le protocole 0 est valide et signifie « n'importe quel protocole ». Toutefois, cela n'est pas recommandé et ne fonctionnera probablement pas. Le streaming nécessite que le numéro de protocole soit défini à 6.
- Les sockets de streaming sont suivis par un identifiant de connexion interne. Par conséquent, il n'est pas nécessaire que le 5-tuple de dest:port:dest:port:protocole soit unique. Par exemple, il peut exister plusieurs sockets avec les mêmes ports entre deux destinations. Les clients n'ont pas besoin de choisir un « port libre » pour une connexion sortante.

## Travaux futurs {#future}

- Le mécanisme d'autorisation actuel pourrait être modifié pour utiliser des mots de passe hachés.
- La clé privée de signature est incluse dans le message Create Lease Set, ce qui n'est pas nécessaire. La révocation n'est pas implémentée. Elle devrait être remplacée par des données aléatoires ou supprimée.
- Certaines améliorations pourraient être capables d'utiliser des messages précédemment définis mais non implémentés.
