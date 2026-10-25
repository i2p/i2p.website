---
title: "Protocole Client I2P (I2CP)"
description: "Comment les applications négocient les sessions, tunnels et LeaseSets avec le router I2P."
slug: "i2cp"
aliases:
  - "/fr/docs/api/i2cp"
  - "/fr/docs/api/i2cp/"
  - "/fr/docs/specs/i2cp-spec"
  - "/fr/docs/specs/i2cp-spec/"
category: "Protocoles"
lastUpdated: "2025-07"
accurateFor: "0.9.67"
---

## Aperçu

Ceci est la spécification du protocole de contrôle I2P (I2CP), l'interface de bas niveau entre les clients et le router. Les clients Java utiliseront l'API client I2CP, qui implémente ce protocole.

Il n'existe aucune implémentation connue non-Java d'une bibliothèque côté client qui implémente I2CP. De plus, les applications orientées socket (streaming) auraient besoin d'une implémentation du protocole de streaming, mais il n'existe pas non plus de bibliothèques non-Java pour cela. Par conséquent, les clients non-Java devraient plutôt utiliser le protocole de niveau supérieur SAM [SAMv3](/docs/api/samv3/), pour lequel des bibliothèques existent dans plusieurs langages.

Il s'agit d'un protocole de bas niveau pris en charge à la fois en interne et en externe par le router I2P Java. Le protocole n'est sérialisé que si le client et le router ne sont pas dans la même JVM ; sinon, les objets Java des messages I2CP sont transmis via une interface JVM interne. I2CP est également pris en charge en externe par le router C++ i2pd.

Plus d'informations sont disponibles sur la page de présentation I2CP [I2CP](/docs/specs/i2cp/).

## Sessions

Le protocole a été conçu pour gérer plusieurs "sessions", chacune avec un ID de session de 2 octets, sur une seule connexion TCP, cependant, les sessions multiples n'ont pas été implémentées jusqu'à la version 0.9.21. Voir la [section multisession ci-dessous](#multisession). N'essayez pas d'utiliser plusieurs sessions sur une seule connexion I2CP avec des routeurs antérieurs à la version 0.9.21.

Il semble également qu'il existe certaines dispositions pour qu'un seul client puisse communiquer avec plusieurs routeurs via des connexions séparées. Ceci n'a également pas été testé et n'est probablement pas utile.

Il n'existe aucun moyen de maintenir une session après une déconnexion, ou de la récupérer sur une connexion I2CP différente. Lorsque le socket est fermé, la session est détruite.

## Exemples de séquences de messages

Note : Les exemples ci-dessous ne montrent pas l'octet de protocole (0x2a) qui doit être envoyé du client vers le router lors de la première connexion. Plus d'informations sur l'initialisation de connexion sont disponibles sur la page de présentation I2CP [I2CP](/docs/specs/i2cp/).

### Établissement de Session Standard

```
  Client                                           Router

                           --------------------->  Get Date Message
        Set Date Message  <---------------------
                           --------------------->  Create Session Message
  Session Status Message  <---------------------
Request LeaseSet Message  <---------------------
                           --------------------->  Create LeaseSet Message

```
### Obtenir les limites de bande passante (session simple)

```
  Client                                           Router

                           --------------------->  Get Bandwidth Limits Message
Bandwidth Limits Message  <---------------------

```
### Recherche de Destination (Session Simple)

```
  Client                                           Router

                           --------------------->  Dest Lookup Message
      Dest Reply Message  <---------------------

```
### Message sortant

Session existante, avec i2cp.messageReliability=none

```
  Client                                           Router

                           --------------------->  Send Message Message

```
Session existante, avec i2cp.messageReliability=none et nonce non nul

```
  Client                                           Router

                           --------------------->  Send Message Message
  Message Status Message  <---------------------
  (succeeded)

```
Session existante, avec i2cp.messageReliability=BestEffort

```
  Client                                           Router

                           --------------------->  Send Message Message
  Message Status Message  <---------------------
  (accepted)
  Message Status Message  <---------------------
  (succeeded)

```
### Message entrant

Session existante, avec i2cp.fastReceive=true (depuis la version 0.9.4)

```
  Client                                           Router

 Message Payload Message  <---------------------

```
Session existante, avec i2cp.fastReceive=false (OBSOLÈTE)

```
  Client                                           Router

  Message Status Message  <---------------------
  (available)
                           --------------------->  Receive Message Begin Message
 Message Payload Message  <---------------------
                           --------------------->  Receive Message End Message

```
### Notes multi-sessions {#multisession}

Les sessions multiples sur une seule connexion I2CP sont prises en charge depuis la version 0.9.21 du router. La première session créée est la "session primaire". Les sessions supplémentaires sont des "sous-sessions". Les sous-sessions sont utilisées pour prendre en charge plusieurs destinations partageant un ensemble commun de tunnels. L'application initiale consiste à ce que la session primaire utilise des clés de signature ECDSA, tandis que la sous-session utilise des clés de signature DSA pour la communication avec les anciens eepsites.

Les sous-sessions partagent les mêmes pools de tunnels entrants et sortants que la session principale. Les sous-sessions doivent utiliser les mêmes clés de chiffrement que la session principale. Ceci s'applique à la fois aux clés de chiffrement du leaseSet et aux clés de chiffrement de destination (non utilisées). Les sous-sessions doivent utiliser des clés de signature différentes dans la destination, de sorte que le hash de destination soit différent de la session principale. Comme les sous-sessions utilisent les mêmes clés de chiffrement et tunnels que la session principale, il est évident pour tous que les destinations s'exécutent sur le même router, donc les garanties d'anonymat anti-corrélation habituelles ne s'appliquent pas.

Les sous-sessions sont créées en envoyant un message CreateSession et en recevant un message SessionStatus en réponse, comme d'habitude. Les sous-sessions doivent être créées après que la session principale ait été créée. La réponse SessionStatus contiendra, en cas de succès, un ID de session unique, distinct de l'ID de la session principale. Bien que les messages CreateSession doivent être traités dans l'ordre, il n'y a pas de moyen sûr de corréler un message CreateSession avec la réponse, donc un client ne devrait pas avoir plusieurs messages CreateSession en attente simultanément. Les options SessionConfig pour la sous-session peuvent ne pas être respectées lorsqu'elles diffèrent de la session principale. En particulier, puisque les sous-sessions utilisent le même pool de tunnel que la session principale, les options de tunnel peuvent être ignorées.

Le router enverra des messages RequestVariableLeaseSet séparés pour chaque Destination au client, et le client doit répondre avec un message CreateLeaseSet pour chacune. Les leases pour les deux Destinations ne seront pas nécessairement identiques, même si elles sont sélectionnées depuis le même pool de tunnels.

Une sous-session peut être détruite avec le message DestroySession comme d'habitude. Cela ne détruira pas la session principale ni n'arrêtera la connexion I2CP. Détruire la session principale détruira cependant toutes les sous-sessions et arrêtera la connexion I2CP. Un message Disconnect détruit toutes les sessions.

Notez que la plupart des messages I2CP, mais pas tous, contiennent un ID de session. Pour ceux qui n'en contiennent pas, les clients peuvent avoir besoin d'une logique supplémentaire pour traiter correctement les réponses du router. DestLookup et DestReply ne contiennent pas d'ID de session ; utilisez plutôt les plus récents HostLookup et HostReply. GetBandwidthLimts et BandwidthLimits ne contiennent pas d'ID de session, cependant la réponse n'est pas spécifique à une session.

### Notes de version {#notes}

L'octet de version de protocole initial (0x2a) envoyé par le client ne devrait pas changer. Avant la version 0.8.7, les informations de version du router n'étaient pas disponibles pour le client, empêchant ainsi les nouveaux clients de fonctionner avec les anciens routers. Depuis la version 0.8.7, les chaînes de version de protocole des deux parties sont échangées dans les messages Get/Set Date. À l'avenir, les clients peuvent utiliser ces informations pour communiquer correctement avec les anciens routers. Les clients et routers ne doivent pas envoyer de messages non supportés par l'autre partie, car ils déconnectent généralement la session lors de la réception d'un message non supporté.

Les informations de version échangées correspondent à la version de l'API "core" ou à la version du protocole I2CP, et ne correspondent pas nécessairement à la version du router.

Un résumé de base des versions du protocole I2CP est le suivant. Pour plus de détails, voir ci-dessous.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Version</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Required I2CP Features</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.67</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">PQ Hybrid ML-KEM (enc types 5-7) supported in LS</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Host lookup/reply extensions (see proposal 167)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.62</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">MessageStatus message Loopback error code</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.46</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">X25519 (enc type 4) supported in LS</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.43</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">BlindingInfo message supported; Additional HostReply message failure codes</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">EncryptedLeaseSet options; MessageStatus message Meta LS error code</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.39</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">CreateLeaseSet2 message and options supported; Dest/LS key certs w/ RedDSA Ed25519 sig type supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Preliminary CreateLeaseSet2 message supported (abandoned)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.21</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Multiple sessions on a single I2CP connection supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.20</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Additional SetDate messages may be sent to the client at any time</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.16</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Authentication, if enabled, is required via GetDate before all other messages</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.15</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest/LS key certs w/ EdDSA Ed25519 sig type supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.14</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Per-message override of messageReliability=none with nonzero nonce</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest/LS key certs w/ ECDSA P-256, P-384, and P-521 sig types supported; RSA sig types also supported but currently unused</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Host Lookup and Host Reply messages supported; Authentication mapping in Get Date message supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Request Variable Lease Set message supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Additional Message Status codes defined</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Send Message nonce=0 allowed; Fast receive mode is the default</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Send Message Expires flag tag bits supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Supports up to 16 leases in a lease set (6 previously)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Get Date and Set Date version strings included. If not present, the client or router is version 0.8.6 or older.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Send Message Expires flag bits supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest Lookup and Get Bandwidth messages supported in standard session; Concurrent Dest Lookup messages supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.8.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">i2cp.messageReliability=none supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Get Bandwidth Limits and Bandwidth Limits messages supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Send Message Expires message supported; Reconfigure Session message supported; Ports and protocol numbers in gzip header</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Dest Lookup and Dest Reply messages supported</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.6.5 or lower</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">All messages and features not listed above</td>
</tr>
</table>
## Structures communes {#structures}

### En-tête de message I2CP {#struct-I2CPMessageHeader}

#### Description

En-tête commun à tous les messages I2CP, contenant la longueur du message et le type de message.

#### Sommaire

1.  [Entier](/docs/specs/common-structures/#integer) de 4 octets spécifiant la longueur du
    corps du message
2.  [Entier](/docs/specs/common-structures/#integer) de 1 octet spécifiant le type de
    message.
3.  Le corps du message I2CP, 0 octet ou plus

#### Notes

La limite de longueur de message réelle est d'environ 64 Ko.

### ID de Message {#struct-MessageId}

#### Description

Identifie de manière unique un message en attente sur un router particulier à un moment donné. Ceci est toujours généré par le router et n'est PAS identique au nonce généré par le client.

#### Contenu

1.  4 octets [Integer](/docs/specs/common-structures/#integer)

#### Notes

Les identifiants de messages sont uniques uniquement au sein d'une session ; ils ne sont pas uniques globalement.

### Charge utile {#struct-Payload}

#### Description

Cette structure est le contenu d'un message livré d'une Destination à une autre.

#### Sommaire

1.  4 octets longueur [Integer](/docs/specs/common-structures/#integer)
2.  Ce nombre d'octets

#### Notes

La charge utile est dans un format gzip comme spécifié sur la page de présentation I2CP [I2CP-FORMAT](/docs/specs/i2cp/#format).

La limite de longueur de message réelle est d'environ 64 Ko.

### Configuration de Session {#struct-SessionConfig}

#### Description

Définit les options de configuration pour une session client particulière.

#### Sommaire

1.  [Destination](/docs/specs/common-structures/#destination)
2.  [Mapping](/docs/specs/common-structures/#mapping) d'options
3.  [Date](/docs/specs/common-structures/#date) de création
4.  [Signature](/docs/specs/common-structures/#signature) des 3 champs précédents,
    signée par la [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey)

#### Notes

- Les options sont spécifiées sur la page de présentation I2CP
  [I2CP-OPTIONS](/docs/specs/i2cp/#options).
- Le [Mapping](/docs/specs/common-structures/#mapping) doit être trié par clé afin que
  la signature soit validée correctement dans le router.
- La date de création doit être comprise dans un intervalle de +/- 30 secondes par rapport à l'heure actuelle
  lors du traitement par le router, sinon la configuration sera rejetée.

#### Signatures hors ligne

- Si la [Destination](/docs/specs/common-structures/#destination) est signée hors ligne,
  le [Mapping](/docs/specs/common-structures/#mapping) doit contenir les trois options
  i2cp.leaseSetOfflineExpiration, i2cp.leaseSetTransientPublicKey, et
  i2cp.leaseSetOfflineSignature. La
  [Signature](/docs/specs/common-structures/#signature) est alors générée par la
  [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey) transitoire et
  est vérifiée avec la
  [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) spécifiée dans
  i2cp.leaseSetTransientPublicKey. Voir
  [I2CP-OPTIONS](/docs/specs/i2cp/#options) pour les détails.

### ID de Session {#struct-SessionId}

#### Description

Identifie de manière unique une session sur un router particulier à un moment donné.

#### Sommaire

1.  2 octets [Integer](/docs/specs/common-structures/#integer)

#### Notes

L'ID de session 0xffff est utilisé pour indiquer "aucune session", par exemple pour les recherches de nom d'hôte.

## Messages

Voir aussi la [documentation Javadoc I2CP](http://javadoc.i2p.net/net/i2p/data/i2cp/package-summary.html).

### Types de messages {#types}

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Message</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Direction</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Since</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#BandwidthLimitsMessage">BandwidthLimitsMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">23</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.2</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#BlindingInfoMessage">BlindingInfoMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">42</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.43</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#CreateLeaseSetMessage">CreateLeaseSetMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#CreateLeaseSet2Message">CreateLeaseSet2Message</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.39</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#CreateSessionMessage">CreateSessionMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#DestLookupMessage">DestLookupMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">34</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#DestReplyMessage">DestReplyMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">35</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#DestroySessionMessage">DestroySessionMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#DisconnectMessage">DisconnectMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">bidir.</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">30</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#GetBandwidthLimitsMessage">GetBandwidthLimitsMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">8</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.2</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#GetDateMessage">GetDateMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">32</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#HostLookupMessage">HostLookupMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">38</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.11</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#HostReplyMessage">HostReplyMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">39</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.11</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#MessagePayloadMessage">MessagePayloadMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">31</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#MessageStatusMessage">MessageStatusMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">22</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#ReceiveMessageBeginMessage">ReceiveMessageBeginMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#ReceiveMessageEndMessage">ReceiveMessageEndMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#ReconfigureSessionMessage">ReconfigureSessionMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#ReportAbuseMessage">ReportAbuseMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">bidir.</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">29</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#RequestLeaseSetMessage">RequestLeaseSetMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">21</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">deprecated</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#RequestVariableLeaseSetMessage">RequestVariableLeaseSetMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">37</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.7</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#SendMessageMessage">SendMessageMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#SendMessageExpiresMessage">SendMessageExpiresMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">C -> R</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">36</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.7.1</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#SessionStatusMessage">SessionStatusMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">20</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;"><a href="#SetDateMessage">SetDateMessage</a></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">R -> C</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">33</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
</table>
### BandwidthLimitsMessage {#BandwidthLimitsMessage}

#### Description

Indiquer au client quelles sont les limites de bande passante.

Envoyé du router au client en réponse à un [GetBandwidthLimitsMessage](#GetBandwidthLimitsMessage).

#### Sommaire

1.  4 octets [Integer](/docs/specs/common-structures/#integer) Limite entrante du client
    (Ko/s)
2.  4 octets [Integer](/docs/specs/common-structures/#integer) Limite sortante du client
    (Ko/s)
3.  4 octets [Integer](/docs/specs/common-structures/#integer) Limite entrante du router
    (Ko/s)
4.  4 octets [Integer](/docs/specs/common-structures/#integer) Limite de rafale entrante du router
    (Ko/s)
5.  4 octets [Integer](/docs/specs/common-structures/#integer) Limite sortante du router
    (Ko/s)
6.  4 octets [Integer](/docs/specs/common-structures/#integer) Limite de rafale sortante
    du router (Ko/s)
7.  4 octets [Integer](/docs/specs/common-structures/#integer) Temps de rafale du router
    (secondes)
8.  Neuf [Integer](/docs/specs/common-structures/#integer) de 4 octets (non définis)

#### Notes

Les limites du client peuvent être les seules valeurs définies, et peuvent être les limites réelles du router, ou un pourcentage des limites du router, ou spécifiques au client particulier, selon l'implémentation. Toutes les valeurs étiquetées comme limites du router peuvent être 0, selon l'implémentation. Depuis la version 0.7.2.

### BlindingInfoMessage {#BlindingInfoMessage}

#### Description

Informe le router qu'une Destination est masquée, avec un mot de passe de recherche optionnel et une clé privée optionnelle pour le déchiffrement. Voir les propositions 123 et 149 pour plus de détails.

Le router doit savoir si une destination est masquée. Si elle est masquée et utilise une authentification secrète ou par client, il doit également disposer de ces informations.

Une recherche d'hôte d'une adresse b32 de nouveau format ("b33") indique au router que l'adresse est aveuglée, mais il n'y a pas de mécanisme pour transmettre la clé secrète ou privée au router dans le message de recherche d'hôte. Bien que nous puissions étendre le message de recherche d'hôte pour ajouter cette information, il est plus propre de définir un nouveau message.

Ce message fournit un moyen programmatique pour le client d'informer le router. Sinon, l'utilisateur devrait configurer manuellement chaque destination.

#### Utilisation

Avant qu'un client envoie un message à une destination masquée, il doit soit rechercher le "b33" dans un message Host Lookup, soit envoyer un message Blinding Info. Si la destination masquée nécessite un secret ou une authentification par client, le client doit envoyer un message Blinding Info.

Le router n'envoie pas de réponse à ce message. Envoyé du Client vers le Router.

#### Sommaire

1.  [ID de session](#struct-sessionid)
2.  1 octet [Integer](/docs/specs/common-structures/#integer) Drapeaux

> - Ordre des bits : 76543210 > - Bit 0 : 0 pour tout le monde, 1 pour par-client > - Bits 3-1 : Schéma d'authentification, si le bit 0 est défini à 1 pour >   par-client, sinon 000 >   - 000 : Authentification client DH (ou pas d'authentification par-client) >   - 001 : Authentification client PSK > - Bit 4 : 1 si secret requis, 0 si aucun secret requis > - Bits 7-5 : Inutilisés, définis à 0 pour compatibilité future

3.  1 octet [Integer](/docs/specs/common-structures/#integer) Type de point de terminaison

> - Le Type 0 est un [Hash](/docs/specs/common-structures/#hash) > - Le Type 1 est un nom d'hôte [String](/docs/specs/common-structures/#string) > - Le Type 2 est une [Destination](/docs/specs/common-structures/#destination) > - Le Type 3 est un Sig Type et >   [SigningPublicKey](/docs/specs/common-structures/#signingpublickey)

4.  2 octets [Integer](/docs/specs/common-structures/#integer) Type de Signature Aveugle
5.  4 octets [Integer](/docs/specs/common-structures/#integer) Secondes d'Expiration depuis
    l'époque
6.  Point de terminaison : Données comme spécifié, un des

> - Type 0 : [Hash](/docs/specs/common-structures/#hash) de 32 octets > > - Type 1 : nom d'hôte [String](/docs/specs/common-structures/#string) > > - Type 2 : [Destination](/docs/specs/common-structures/#destination) binaire > >  > >  - Type 3 : type de signature [Integer](/docs/specs/common-structures/#integer) de 2 octets, suivi par > >  -   [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) (longueur telle >       qu'impliquée par le type de signature)

7.  [PrivateKey](/docs/specs/common-structures/#privatekey) Clé de déchiffrement Présente uniquement
    si le bit de drapeau 0 est défini à 1. Une clé privée ECIES_X25519 de 32 octets,
    little-endian
8.  [String](/docs/specs/common-structures/#string) Mot de passe de recherche Présent uniquement si
    le bit de drapeau 4 est défini à 1.

#### Notes

- Depuis la version 0.9.43.
- Le type de point de terminaison Hash n'est probablement pas utile à moins que le router puisse effectuer une recherche inversée dans le carnet d'adresses pour obtenir la Destination.
- Le type de point de terminaison hostname n'est probablement pas utile à moins que le router puisse effectuer une recherche dans le carnet d'adresses pour obtenir la Destination.

### CreateLeaseSetMessage {#CreateLeaseSetMessage}

DÉPRÉCIÉ. Ne peut pas être utilisé pour LeaseSet2, les clés hors ligne, les types de chiffrement non-ElGamal, les types de chiffrement multiples, ou les LeaseSets chiffrés. Utilisez CreateLeaseSet2Message avec tous les routeurs 0.9.39 ou supérieurs.

#### Description

Ce message est envoyé en réponse à un [RequestLeaseSetMessage](#RequestLeaseSetMessage) ou [RequestVariableLeaseSetMessage](#RequestVariableLeaseSetMessage) et contient toutes les structures [Lease](/docs/specs/common-structures/#lease) qui doivent être publiées dans la base de données réseau I2NP.

Envoyé du Client vers le Router.

#### Sommaire

1.  [ID de session](#struct-sessionid)
2.  DSA [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey) ou 20
    octets ignorés
3.  [PrivateKey](/docs/specs/common-structures/#privatekey)
4.  [LeaseSet](/docs/specs/common-structures/#leaseset)

#### Notes

La SigningPrivateKey correspond à la [SigningPublicKey](/docs/specs/common-structures/#signingpublickey) du leaseSet, uniquement si le type de clé de signature est DSA. Ceci est destiné à la révocation de leaseSet, qui n'est pas implémentée et ne le sera probablement jamais. Si le type de clé de signature n'est pas DSA, ce champ contient 20 octets de données aléatoires. La longueur de ce champ est toujours de 20 octets, elle n'est jamais égale à la longueur d'une clé privée de signature non-DSA.

La PrivateKey correspond à la [PublicKey](/docs/specs/common-structures/#publickey) du LeaseSet. La PrivateKey est nécessaire pour déchiffrer les messages routés par garlic encryption.

La révocation n'est pas implémentée. La connexion à plusieurs routers n'est implémentée dans aucune bibliothèque client.

### CreateLeaseSet2Message {#CreateLeaseSet2Message}

#### Description

Ce message est envoyé en réponse à un [RequestLeaseSetMessage](#RequestLeaseSetMessage) ou [RequestVariableLeaseSetMessage](#RequestVariableLeaseSetMessage) et contient toutes les structures [Lease](/docs/specs/common-structures/#lease) qui devraient être publiées dans la base de données réseau I2NP.

Envoyé du Client vers le Router. Depuis la version 0.9.39. L'authentification par client pour EncryptedLeaseSet est prise en charge depuis la version 0.9.41. MetaLeaseSet n'est pas encore pris en charge via I2CP. Voir la proposition 123 pour plus d'informations.

#### Sommaire

1.  [ID de session](#struct-sessionid)
2.  Un octet de type de leaseSet qui suit.

> - Le Type 1 est un [LeaseSet](/docs/specs/common-structures/#leaseset) (déprécié) > - Le Type 3 est un [LeaseSet2](/docs/specs/common-structures/#leaseset2) > - Le Type 5 est un [EncryptedLeaseSet](/docs/specs/common-structures/#leaseset2) > - Le Type 7 est un [MetaLeaseSet](/docs/specs/common-structures/#leaseset2)

3.  [LeaseSet](/docs/specs/common-structures/#leaseset) ou
    [LeaseSet2](/docs/specs/common-structures/#leaseset2) ou
    [EncryptedLeaseSet](/docs/specs/common-structures/#leaseset2) ou
    [MetaLeaseSet](/docs/specs/common-structures/#leaseset2)
4.  Un octet représentant le nombre de clés privées qui suivent.
5.  Liste de [PrivateKey](/docs/specs/common-structures/#privatekey). Une pour chaque clé
    publique dans le lease set, dans le même ordre. (Absent pour Meta LS2)

> - Type de chiffrement (2 octets [Integer](/docs/specs/common-structures/#integer)) > - Longueur de la clé de chiffrement (2 octets [Integer](/docs/specs/common-structures/#integer)) > - [PrivateKey](/docs/specs/common-structures/#privatekey) de chiffrement (nombre d'octets >   spécifiés)

#### Notes

Les PrivateKeys correspondent à chacune des [PublicKey](/docs/specs/common-structures/#publickey) du LeaseSet. Les PrivateKeys sont nécessaires pour déchiffrer les messages routés par garlic encryption.

Voir la proposition 123 pour plus d'informations sur les leaseSets chiffrés.

Le contenu et le format du MetaLeaseSet sont préliminaires et sujets à modification. Aucun protocole n'est spécifié pour l'administration de plusieurs routers. Voir la proposition 123 pour plus d'informations.

La clé privée de signature, précédemment définie pour la révocation et inutilisée, n'est pas présente dans LS2.

La version préliminaire avec le type de message 40 était dans la 0.9.38 mais le format a été modifié. Le type 40 est abandonné et n'est pas pris en charge. Le type 41 n'est pas valide avant la 0.9.39.

### CreateSessionMessage {#CreateSessionMessage}

#### Description

Ce message est envoyé depuis un client pour initier une session, où une session est définie comme la connexion d'une seule Destination au réseau, vers laquelle tous les messages pour cette Destination seront livrés et depuis laquelle tous les messages que cette Destination envoie vers toute autre Destination seront transmis.

Envoyé du Client vers le Router. Le router répond avec un [SessionStatusMessage](#SessionStatusMessage).

#### Sommaire

1.  [Configuration de Session](#struct-sessionconfig)

#### Notes

- Il s'agit du deuxième message envoyé par le client. Précédemment, le client
  a envoyé un [GetDateMessage](#GetDateMessage) et a reçu une
  réponse [SetDateMessage](#SetDateMessage).
- Si la Date dans la Session Config est trop éloignée (plus de +/- 30
  secondes) de l'heure actuelle du router, la session sera
  rejetée.
- S'il existe déjà une session sur le router pour cette Destination, la
  session sera rejetée.
- Le [Mapping](/docs/specs/common-structures/#mapping) dans la Session Config doit être
  trié par clé pour que la signature soit validée correctement dans le
  router.

### DestLookupMessage {#DestLookupMessage}

#### Description

Envoyé du Client au Router. Le router répond avec un [DestReplyMessage](#DestReplyMessage).

#### Sommaire

1.  SHA-256 [Hash](/docs/specs/common-structures/#hash)

#### Notes

À partir de la version 0.7.

À partir de la version 0.8.3, plusieurs recherches en cours sont prises en charge, et les recherches sont supportées à la fois dans I2PSimpleSession et dans les sessions standard.

[HostLookupMessage](#HostLookupMessage) est préféré depuis la version 0.9.11.

### DestReplyMessage {#DestReplyMessage}

#### Description

Envoyé du Router vers le Client en réponse à un [DestLookupMessage](#DestLookupMessage).

#### Sommaire

1.  [Destination](/docs/specs/common-structures/#destination) en cas de succès, ou
    [Hash](/docs/specs/common-structures/#hash) en cas d'échec

#### Notes

À partir de la version 0.7.

À partir de la version 0.8.3, le Hash demandé est retourné si la recherche échoue, afin que le client puisse avoir plusieurs recherches en cours et corréler les réponses aux recherches. Pour corréler une réponse Destination avec une requête, prenez le Hash de la Destination. Avant la version 0.8.3, la réponse était vide en cas d'échec.

### DestroySessionMessage {#DestroySessionMessage}

#### Description

Ce message est envoyé par un client pour détruire une session.

Envoyé du Client vers le Router. Le router devrait répondre avec un [SessionStatusMessage](#SessionStatusMessage) (Destroyed). Cependant, voir les notes importantes ci-dessous.

#### Sommaire

1.  [ID de session](#struct-sessionid)

#### Notes

Le router à ce stade doit libérer toutes les ressources liées à la session.

Jusqu'à l'API 0.9.66, le router I2P Java et les bibliothèques client s'écartent substantiellement de cette spécification. Le router n'envoie jamais de réponse SessionStatus(Destroyed). S'il ne reste aucune session, il envoie un [DisconnectMessage](#DisconnectMessage). S'il y a des sous-sessions ou si la session primaire reste, il ne répond pas.

La bibliothèque client Java répond à un message SessionStatus en détruisant toutes les sessions et en se reconnectant.

La destruction de sous-sessions individuelles sur une connexion avec plusieurs sessions pourrait ne pas être entièrement testée ou fonctionnelle sur diverses implémentations de router et de client. Soyez prudent.

Les implémentations devraient traiter une destruction pour une session primaire comme une destruction pour toutes les sous-sessions, mais permettre une destruction pour une seule sous-session et garder la connexion ouverte, mais Java I2P ne fait pas cela actuellement. Si le comportement de Java I2P est modifié dans les versions ultérieures, cela sera documenté ici.

### DisconnectMessage {#DisconnectMessage}

#### Description

Informe l'autre partie qu'il y a des problèmes et que la connexion actuelle est sur le point d'être détruite. Ceci met fin à toutes les sessions sur cette connexion. Le socket sera fermé sous peu. Envoyé soit du router vers le client, soit du client vers le router.

#### Sommaire

1.  Raison [String](/docs/specs/common-structures/#string)

#### Notes

Seulement implémenté dans la direction router-vers-client, au moins dans Java I2P.

### GetBandwidthLimitsMessage {#GetBandwidthLimitsMessage}

#### Description

Demander au router d'indiquer quelles sont ses limites de bande passante actuelles.

Envoyé du Client au Router. Le router répond avec un [BandwidthLimitsMessage](#BandwidthLimitsMessage).

#### Sommaire

*Aucune*

#### Notes

À partir de la version 0.7.2.

À partir de la version 0.8.3, pris en charge à la fois dans I2PSimpleSession et dans les sessions standard.

### GetDateMessage {#GetDateMessage}

#### Description

Envoyé du Client vers le Router. Le router répond avec un [SetDateMessage](#SetDateMessage).

#### Sommaire

1.  Version de l'API I2CP [String](/docs/specs/common-structures/#string)
2.  Authentification [Mapping](/docs/specs/common-structures/#mapping) (optionnel, depuis
    la version 0.9.11)

#### Notes

- Généralement le premier message envoyé par le client après avoir envoyé
  l'octet de version du protocole.
- La chaîne de version est incluse à partir de la version 0.8.7. Ceci n'est
  utile que si le client et le router ne sont pas dans la même JVM. Si elle n'est pas
  présente, le client est en version 0.8.6 ou antérieure.
- À partir de la version 0.9.11, l'authentification
  [Mapping](/docs/specs/common-structures/#mapping) peut être incluse, avec les clés
  i2cp.username et i2cp.password. Le Mapping n'a pas besoin d'être trié car
  ce message n'est pas signé. Avant et jusqu'à la version 0.9.10,
  l'authentification est incluse dans le
  [Session Config](#struct-sessionconfig)
  Mapping, et aucune authentification n'est imposée pour
  [GetDateMessage](#GetDateMessage),
  [GetBandwidthLimitsMessage](#GetBandwidthLimitsMessage), ou
  [DestLookupMessage](#DestLookupMessage). Quand elle est activée, l'authentification
  via [GetDateMessage](#GetDateMessage) est requise avant tout autre
  message à partir de la version 0.9.16. Ceci n'est utile qu'en dehors du contexte
  router. Il s'agit d'un changement incompatible, mais qui n'affectera que les sessions
  en dehors du contexte router avec authentification, ce qui devrait être rare.

### HostLookupMessage {#HostLookupMessage}

#### Description

Envoyé du Client vers le Router. Le router répond avec un [HostReplyMessage](#HostReplyMessage).

Ceci remplace le [DestLookupMessage](#DestLookupMessage) et ajoute un ID de requête, un délai d'expiration, et la prise en charge de la recherche de nom d'hôte. Comme il prend également en charge les recherches de Hash, il peut être utilisé pour toutes les recherches si le router le prend en charge. Pour les recherches de nom d'hôte, le router interrogera le service de nommage de son contexte. Ceci n'est utile que si le client est en dehors du contexte du router. À l'intérieur du contexte router, le client devrait interroger lui-même le service de nommage, ce qui est beaucoup plus efficace.

#### Sommaire

1.  [Session ID](#struct-sessionid)
2.  4 octets [Integer](/docs/specs/common-structures/#integer) ID de requête
3.  4 octets [Integer](/docs/specs/common-structures/#integer) timeout (ms)
4.  1 octet [Integer](/docs/specs/common-structures/#integer) type de requête
5.  SHA-256 [Hash](/docs/specs/common-structures/#hash) ou nom d'hôte
    [String](/docs/specs/common-structures/#string) ou
    [Destination](/docs/specs/common-structures/#destination)

Types de requête :

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Type</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Lookup key (item 5)</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">As of</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Hash</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">host name String</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Hash</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">host name String</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Destination</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.66</td>
</tr>
</table>
Les types 2-4 demandent que le mappage d'options du LeaseSet soit retourné dans le message HostReply. Voir la proposition 167.

#### Notes

- À partir de la version 0.9.11. Utilisez [DestLookupMessage](#DestLookupMessage) pour
  les routeurs plus anciens.
- L'ID de session et l'ID de requête seront retournés dans le
  [HostReplyMessage](#HostReplyMessage). Utilisez 0xFFFF pour l'ID de session
  s'il n'y a pas de session.
- Le délai d'expiration est utile pour les recherches de Hash. Minimum recommandé 10 000 (10
  sec.). À l'avenir, il pourra également être utile pour les recherches
  de service de nommage distant. La valeur peut ne pas être respectée pour les recherches de nom d'hôte locales,
  qui devraient être rapides.
- La recherche de nom d'hôte en base 32 est prise en charge mais il est préférable de le convertir
  en Hash d'abord.

### HostReplyMessage {#HostReplyMessage}

#### Description

Envoyé du Router au Client en réponse à un [HostLookupMessage](#HostLookupMessage).

#### Sommaire

1.  [Session ID](#struct-sessionid)
2.  [Integer](/docs/specs/common-structures/#integer) d'ID de requête sur 4 octets
3.  [Integer](/docs/specs/common-structures/#integer) de code de résultat sur 1 octet

> - 0: Succès > - 1: Échec > - 2: Mot de passe de recherche requis (depuis 0.9.43) > - 3: Clé privée requise (depuis 0.9.43) > - 4: Mot de passe de recherche et clé privée requis (depuis 0.9.43) > - 5: Échec de déchiffrement du leaseSet (depuis 0.9.43) > - 6: Échec de recherche du leaseSet (depuis 0.9.66) > - 7: Type de recherche non pris en charge (depuis 0.9.66)

4.  [Destination](/docs/specs/common-structures/#destination), présente uniquement si le code de résultat est zéro, sauf qu'elle peut également être retournée pour les types de recherche 2-4. Voir ci-dessous.
5.  [Mapping](/docs/specs/common-structures/#mapping), présente uniquement si le code de résultat est zéro, retournée uniquement pour les types de recherche 2-4. À partir de 0.9.66. Voir ci-dessous.

#### Réponses pour les types de recherche 2-4

La proposition 167 définit des types de recherche supplémentaires qui retournent toutes les options du leaseSet, si présentes. Pour les types de recherche 2-4, le router doit récupérer le leaseSet, même si la clé de recherche est dans le carnet d'adresses.

En cas de succès, le HostReply contiendra les options Mapping du leaseSet, et les inclura comme élément 5 après la destination. S'il n'y a pas d'options dans le Mapping, ou si le leaseSet était de version 1, il sera tout de même inclus comme un Mapping vide (deux octets : 0 0). Toutes les options du leaseSet seront incluses, pas seulement les options d'enregistrement de service. Par exemple, des options pour des paramètres définis dans le futur peuvent être présentes. Le Mapping retourné peut être trié ou non, selon l'implémentation.

En cas d'échec de recherche de leaseSet, la réponse contiendra un nouveau code d'erreur 6 (Échec de recherche de leaseSet) et n'inclura pas de mappage. Lorsque le code d'erreur 6 est retourné, le champ Destination peut être présent ou non. Il sera présent si une recherche de nom d'hôte dans le carnet d'adresses a réussi, ou si une recherche précédente a réussi et que le résultat a été mis en cache, ou si la Destination était présente dans le message de recherche (type de recherche 4).

Si un type de recherche n'est pas pris en charge, la réponse contiendra un nouveau code d'erreur 7 (type de recherche non pris en charge).

#### Notes

- Depuis la version 0.9.11. Voir les notes de [HostLookupMessage](#HostLookupMessage).
- L'ID de session et l'ID de requête sont ceux du [HostLookupMessage](#HostLookupMessage).
- Le code de résultat est 0 pour le succès, 1-255 pour l'échec. 1 indique un échec générique. Depuis la version 0.9.43, les codes d'échec supplémentaires 2-5 ont été définis pour prendre en charge les erreurs étendues pour les recherches "b33". Voir les propositions 123 et 149 pour des informations supplémentaires. Depuis la version 0.9.66, les codes d'échec supplémentaires 6-7 ont été définis pour prendre en charge les erreurs étendues pour les recherches de type 2-4. Voir la proposition 167 pour des informations supplémentaires.

### MessagePayloadMessage {#MessagePayloadMessage}

#### Description

Livrer la charge utile d'un message au client.

Envoyé du router vers le client. Si i2cp.fastReceive=true, ce qui n'est pas la valeur par défaut, le client répond avec un [ReceiveMessageEndMessage](#ReceiveMessageEndMessage).

#### Sommaire

1.  [ID de session](#struct-sessionid)
2.  [ID de message](#struct-messageid)
3.  [Charge utile](#struct-payload)

#### Notes

### MessageStatusMessage {#MessageStatusMessage}

#### Description

Notifie le client du statut de livraison d'un message entrant ou sortant. Envoyé du Router vers le Client. Si ce message indique qu'un message entrant est disponible, le client répond avec un [ReceiveMessageBeginMessage](#ReceiveMessageBeginMessage). Pour un message sortant, il s'agit d'une réponse à un [SendMessageMessage](#SendMessageMessage) ou [SendMessageExpiresMessage](#SendMessageExpiresMessage).

#### Sommaire

1.  [Session ID](#struct-sessionid)
2.  [Message ID](#struct-messageid) généré par le router
3.  1 octet [Integer](/docs/specs/common-structures/#integer) statut
4.  4 octets [Integer](/docs/specs/common-structures/#integer) taille
5.  4 octets [Integer](/docs/specs/common-structures/#integer) nonce précédemment généré
    par le client

#### Notes

Jusqu'à la version 0.9.4, les valeurs de statut connues sont 0 pour message disponible, 1 pour accepté, 2 pour meilleur effort réussi, 3 pour meilleur effort échoué, 4 pour garanti réussi, 5 pour garanti échoué. L'Integer de taille spécifie la taille du message disponible et n'est pertinent que pour statut = 0. Bien que le mode garanti ne soit pas implémenté (le meilleur effort est le seul service), l'implémentation actuelle du router utilise les codes de statut garantis, pas les codes de meilleur effort.

À partir de la version 0.9.5 du router, des codes de statut supplémentaires sont définis, cependant ils ne sont pas nécessairement implémentés. Consultez la [documentation Javadocs de MessageStatusMessage](http://javadoc.i2p.net/net/i2p/data/i2cp/MessageStatusMessage.html) pour plus de détails. Pour les messages sortants, les codes 1, 2, 4 et 6 indiquent un succès ; tous les autres sont des échecs. Les codes d'échec retournés peuvent varier et sont spécifiques à l'implémentation.

Tous les codes de statut :

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Status Code</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">As Of Release</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Name</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Description</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Available</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">DEPRECATED. For incoming messages only. All other status codes below are for outgoing messages. The included size is the size in bytes of the available message. This is unused in "fast receive" mode, which is the default as of release 0.9.4.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Accepted</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Outgoing message accepted by the local router for delivery. The included nonce matches the nonce in the <a href="#SendMessageMessage">SendMessageMessage</a>, and the included Message ID will be used for subsequent success or failure notification.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Best Effort Success</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Probable success (unused)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Best Effort Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Probable failure</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Guaranteed Success</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Probable success</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Guaranteed Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Generic failure, specific cause unknown. May not really be a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">6</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local Success</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local delivery successful. The destination was another client on the same router.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">7</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local delivery failure. The destination was another client on the same router.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">8</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Router Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The local router is not ready, has shut down, or has major problems. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">9</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Network Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The local computer apparently has no network connectivity at all. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">10</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Session</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The I2CP session is invalid or closed. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Message</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The message payload is invalid or zero-length or too big. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Options</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Something is invalid in the message options, or the expiration is in the past or too far in the future. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">13</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Overflow Failure</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Some queue or buffer in the router is full and the message was dropped. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">14</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Message Expired</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The message expired before it could be sent. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">15</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Local Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The client has not yet signed a <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a>, or the local keys are invalid, or it has expired, or it does not have any tunnels in it. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">16</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">No Local Tunnels</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Local problems. No outbound tunnel to send through, or no inbound tunnel if a reply is required. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">17</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Unsupported Encryption</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The certs or options in the <a href="/docs/specs/common-structures/#destination">Destination</a> or its <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a> indicate that it uses an encryption format that we don't support, so we can't talk to it. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">18</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Destination</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Something is wrong with the far-end <a href="/docs/specs/common-structures/#destination">Destination</a>. Bad format, unsupported options, certificates, etc. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">19</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Bad Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">We got the far-end <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a> but something strange is wrong with it. Unsupported options or certificates, no tunnels, etc. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">20</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Expired Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">We got the far-end <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a> but it's expired and we can't get a new one. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">21</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.5</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">No Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Could not find the far-end <a href="/docs/specs/common-structures/#leaseset">LeaseSet</a>. This is a common failure, equivalent to a DNS lookup failure. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">22</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.41</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Meta Leaseset</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The far-end destination's lease set was a meta lease set, and cannot be sent to. The client should request the meta lease set's contents with a HostLookupMessage, and select one of the hashes contained within to look up and send to. This is a guaranteed failure.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">23</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.62</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Loopback Denied</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The message was attempted to be sent from and to the same destination or session. This is a guaranteed failure.</td>
</tr>
</table>
Quand status = 1 (accepté), le nonce correspond au nonce du [SendMessageMessage](#SendMessageMessage), et l'ID de message inclus sera utilisé pour les notifications de succès ou d'échec ultérieures. Sinon, le nonce peut être ignoré.

### ReceiveMessageBeginMessage {#ReceiveMessageBeginMessage}

OBSOLÈTE. Non pris en charge par i2pd.

#### Description

Demander au router de livrer un message dont il a été préalablement notifié. Envoyé du Client vers le Router. Le router répond avec un [MessagePayloadMessage](#MessagePayloadMessage).

#### Sommaire

1.  [ID de session](#struct-sessionid)
2.  [ID de message](#struct-messageid)

#### Notes

Le [ReceiveMessageBeginMessage](#ReceiveMessageBeginMessage) est envoyé en réponse à un [MessageStatusMessage](#MessageStatusMessage) indiquant qu'un nouveau message est disponible pour récupération. Si l'identifiant de message spécifié dans le [ReceiveMessageBeginMessage](#ReceiveMessageBeginMessage) est invalide ou incorrect, le router peut simplement ne pas répondre, ou il peut renvoyer un [DisconnectMessage](#DisconnectMessage).

Ceci n'est pas utilisé en mode "réception rapide", qui est le mode par défaut depuis la version 0.9.4.

### ReceiveMessageEndMessage {#ReceiveMessageEndMessage}

OBSOLÈTE. Non pris en charge par i2pd.

#### Description

Indiquer au router que la livraison d'un message s'est terminée avec succès et que le router peut supprimer le message.

Envoyé du Client vers le Router.

#### Sommaire

1.  [ID de session](#struct-sessionid)
2.  [ID de message](#struct-messageid)

#### Notes

Le [ReceiveMessageEndMessage](#ReceiveMessageEndMessage) est envoyé après qu'un [MessagePayloadMessage](#MessagePayloadMessage) ait entièrement livré la charge utile d'un message.

Ceci n'est pas utilisé en mode "réception rapide", qui est le mode par défaut depuis la version 0.9.4.

### ReconfigureSessionMessage {#ReconfigureSessionMessage}

#### Description

Envoyé du Client vers le Router pour mettre à jour la configuration de session. Le router répond avec un [SessionStatusMessage](#SessionStatusMessage).

#### Sommaire

1.  [ID de session](#struct-sessionid)
2.  [Configuration de session](#struct-sessionconfig)

#### Notes

- À partir de la version 0.7.1.
- Si la Date dans la Configuration de Session est trop éloignée (plus de +/- 30
  secondes) de l'heure actuelle du router, la session sera
  rejetée.
- Le [Mapping](/docs/specs/common-structures/#mapping) dans la Configuration de Session doit être
  trié par clé afin que la signature soit validée correctement dans le
  router.
- Certaines options de configuration ne peuvent être définies que dans le
  [CreateSessionMessage](#CreateSessionMessage), et les changements ici ne seront
  pas reconnus par le router. Les modifications des options de tunnel inbound.\*
  et outbound.\* sont toujours reconnues.
- En général, le router devrait fusionner la configuration mise à jour avec la
  configuration actuelle, donc la configuration mise à jour n'a besoin de contenir que les
  options nouvelles ou modifiées. Cependant, à cause de la fusion, les options ne peuvent pas être
  supprimées de cette manière ; elles doivent être définies explicitement à la valeur
  par défaut désirée.

### ReportAbuseMessage {#ReportAbuseMessage}

OBSOLÈTE, INUTILISÉ, NON PRIS EN CHARGE

#### Description

Informer l'autre partie (client ou router) qu'elle est sous attaque, potentiellement en référence à un MessageId particulier. Si le router est sous attaque, le client peut décider de migrer vers un autre router, et si un client est sous attaque, le router peut reconstruire ses routers ou bannir certains des pairs qui lui ont envoyé des messages délivrant l'attaque.

Envoyé soit du router vers le client ou du client vers le router.

#### Sommaire

1.  [Session ID](#struct-sessionid)
2.  1 octet [Integer](/docs/specs/common-structures/#integer) gravité d'abus (0 étant minimalement abusif, 255 étant extrêmement abusif)
3.  Raison [String](/docs/specs/common-structures/#string)
4.  [Message ID](#struct-messageid)

#### Notes

Inutilisé. Non entièrement implémenté. Le router et le client peuvent tous deux générer un [ReportAbuseMessage](#ReportAbuseMessage), mais aucun des deux n'a de gestionnaire pour le message lorsqu'il est reçu.

### RequestLeaseSetMessage {#RequestLeaseSetMessage}

OBSOLÈTE. Non pris en charge par i2pd. Non envoyé par Java I2P aux clients version 0.9.7 ou supérieure (2013-07). Utilisez RequestVariableLeaseSetMessage.

#### Description

Demande qu'un client autorise l'inclusion d'un ensemble particulier de tunnels entrants. Envoyé du router vers le client. Le client répond avec un [CreateLeaseSetMessage](#CreateLeaseSetMessage).

Le premier de ces messages envoyés sur une session est un signal au client que les tunnels sont construits et prêts pour le trafic. Le router ne doit pas envoyer le premier de ces messages tant qu'au moins un tunnel entrant ET un tunnel sortant n'ont pas été construits. Les clients devraient expirer et détruire la session si le premier de ces messages n'est pas reçu après un certain temps (recommandé : 5 minutes ou plus).

#### Table des matières

1.  [Session ID](#struct-sessionid)
2.  1 octet nombre [Integer](/docs/specs/common-structures/#integer) de tunnels
3.  Autant de paires de :
    1.  [Hash](/docs/specs/common-structures/#hash)
    2.  [TunnelId](/docs/specs/common-structures/#tunnelid)
4.  [Date](/docs/specs/common-structures/#date) de fin

#### Notes

Cela demande un [LeaseSet](/docs/specs/common-structures/#leaseset) avec toutes les entrées [Lease](/docs/specs/common-structures/#lease) configurées pour expirer en même temps. Pour les versions client 0.9.7 ou supérieures, [RequestVariableLeaseSetMessage](#RequestVariableLeaseSetMessage) est utilisé.

### RequestVariableLeaseSetMessage {#RequestVariableLeaseSetMessage}

#### Description

Demander qu'un client autorise l'inclusion d'un ensemble particulier de tunnels entrants.

Envoyé du Router vers le Client. Le client répond avec un [CreateLeaseSetMessage](#CreateLeaseSetMessage) ou [CreateLeaseSet2Message](#CreateLeaseSet2Message).

Le premier de ces messages envoyé sur une session est un signal au client que les tunnels sont construits et prêts pour le trafic. Le router ne doit pas envoyer le premier de ces messages tant qu'au moins un tunnel entrant ET un tunnel sortant n'ont pas été construits. Les clients devraient expirer et détruire la session si le premier de ces messages n'est pas reçu après un certain temps (recommandé : 5 minutes ou plus).

#### Sommaire

1.  [ID de session](#struct-sessionid)
2.  1 octet nombre [Integer](/docs/specs/common-structures/#integer) de tunnels
3.  Autant d'entrées [Lease](/docs/specs/common-structures/#lease)

#### Notes

Ceci demande un [LeaseSet](/docs/specs/common-structures/#leaseset) avec un temps d'expiration individuel pour chaque [Lease](/docs/specs/common-structures/#lease).

À partir de la version 0.9.7. Pour les clients antérieurs à cette version, utilisez [RequestLeaseSetMessage](#RequestLeaseSetMessage).

### SendMessageMessage {#SendMessageMessage}

#### Description

Voici comment un client envoie un message (la charge utile) vers la [Destination](/docs/specs/common-structures/#destination). Le router utilisera une expiration par défaut.

Envoyé du Client au Router. Le router répond avec un [MessageStatusMessage](#MessageStatusMessage).

#### Sommaire

1.  [ID de session](#struct-sessionid)
2.  [Destination](/docs/specs/common-structures/#destination)
3.  [Charge utile](#struct-payload)
4.  4 octets [Integer](/docs/specs/common-structures/#integer) nonce

#### Notes

Dès que le [SendMessageMessage](#SendMessageMessage) arrive complètement intact, le router devrait retourner un [MessageStatusMessage](#MessageStatusMessage) indiquant qu'il a été accepté pour livraison. Ce message contiendra le même nonce envoyé ici. Plus tard, basé sur les garanties de livraison de la configuration de session, le router peut également renvoyer un autre [MessageStatusMessage](#MessageStatusMessage) mettant à jour le statut.

Depuis la version 0.8.1, le router n'envoie aucun [MessageStatusMessage](#MessageStatusMessage) si i2cp.messageReliability=none.

Avant la version 0.9.4, une valeur de nonce de 0 n'était pas autorisée. Depuis la version 0.9.4, une valeur de nonce de 0 est autorisée et indique au router qu'il ne doit envoyer aucun [MessageStatusMessage](#MessageStatusMessage), c'est-à-dire qu'il agit comme si i2cp.messageReliability=none pour ce message uniquement.

Avant la version 0.9.14, une session avec i2cp.messageReliability=none ne pouvait pas être remplacée message par message. À partir de la version 0.9.14, dans une session avec i2cp.messageReliability=none, le client peut demander la livraison d'un [MessageStatusMessage](#MessageStatusMessage) avec le succès ou l'échec de la livraison en définissant le nonce à une valeur non nulle. Le router n'enverra pas le [MessageStatusMessage](#MessageStatusMessage) "accepted" mais il enverra plus tard au client un [MessageStatusMessage](#MessageStatusMessage) avec le même nonce, et une valeur de succès ou d'échec.

### SendMessageExpiresMessage {#SendMessageExpiresMessage}

#### Description

Envoyé du Client vers le Router. Identique à [SendMessageMessage](#SendMessageMessage), sauf qu'il inclut une expiration et des options.

#### Sommaire

1.  [Session ID](#struct-sessionid)
2.  [Destination](/docs/specs/common-structures/#destination)
3.  [Payload](#struct-payload)
4.  Nonce [Integer](/docs/specs/common-structures/#integer) de 4 octets
5.  2 octets de drapeaux (options)
6.  [Date](/docs/specs/common-structures/#date) d'expiration tronquée de 8 octets à 6
    octets

#### Notes

À partir de la version 0.7.1.

En mode "best effort", dès que le SendMessageExpiresMessage arrive complètement intact, le router devrait retourner un MessageStatusMessage indiquant qu'il a été accepté pour livraison. Ce message contiendra le même nonce envoyé ici. Plus tard, selon les garanties de livraison de la configuration de session, le router peut également renvoyer un autre MessageStatusMessage mettant à jour le statut.

À partir de la version 0.8.1, le router n'envoie aucun Message Status Message si i2cp.messageReliability=none.

Avant la version 0.9.4, une valeur de nonce de 0 n'était pas autorisée. À partir de la version 0.9.4, une valeur de nonce de 0 est autorisée, et indique au router qu'il ne doit envoyer aucun Message Status Message, c'est-à-dire qu'il agit comme si i2cp.messageReliability=none pour ce message uniquement.

Avant la version 0.9.14, une session avec i2cp.messageReliability=none ne pouvait pas être remplacée message par message. Depuis la version 0.9.14, dans une session avec i2cp.messageReliability=none, le client peut demander la livraison d'un Message Status Message avec le succès ou l'échec de la livraison en définissant le nonce sur une valeur non nulle. Le router n'enverra pas le Message Status Message "accepted" mais il enverra plus tard au client un Message Status Message avec le même nonce, et une valeur de succès ou d'échec.

#### Champ des drapeaux

À partir de la version 0.8.4, les deux octets supérieurs de la Date sont redéfinis pour contenir des drapeaux. Les drapeaux doivent par défaut être tous à zéro pour la compatibilité ascendante. La Date n'empiétera pas sur le champ des drapeaux avant l'année 10889. Les drapeaux peuvent être utilisés par l'application pour fournir des indications au router quant à savoir si un leaseSet et/ou des ElGamal/AES Session Tags doivent être livrés avec le message. Les paramètres affecteront significativement la quantité de surcharge protocolaire et la fiabilité de livraison des messages. Les bits individuels des drapeaux sont définis comme suit, à partir de la version 0.9.2. Les définitions sont sujettes à changement. Utilisez la classe SendMessageOptions pour construire les drapeaux.

Ordre des bits : 15...0

Bits 15-11

:   Inutilisé, doit être zéro

Bits 10-9

:   Remplacement de fiabilité des messages (Non implémenté, à supprimer).

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Field value</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Description</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">00</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Use session setting i2cp.messageReliability (default)</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">01</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Use "best effort" message reliability for this message, overriding the session setting. The router will send one or more MessageStatusMessages in response. Unused. Use a nonzero nonce value to override a session setting of "none".</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">10</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Use "guaranteed" message reliability for this message, overriding the session setting. The router will send one or more MessageStatusMessages in response. Unused. Use a nonzero nonce value to override a session setting of "none".</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">11</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Unused. Use a nonce value of 0 to force "none" and override a session setting of "best effort" or "guaranteed".</td>
</tr>
</table>
Bit 8

:   Si 1, ne pas inclure un leaseSet dans le garlic avec ce message. Si

    0, the router may bundle a lease set at its discretion.

Bits 7-4

:   Seuil bas de tags. S'il y a moins de tags disponibles que ce nombre,

    send more. This is advisory and does not force tags to be delivered.
    For ElGamal only. Ignored for ECIES-Ratchet.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Field value</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Tag threshold</th>
</tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0000</td><td style="border: 1px solid var(--color-border); padding: 8px;">Use session key manager settings</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0001</td><td style="border: 1px solid var(--color-border); padding: 8px;">2</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0010</td><td style="border: 1px solid var(--color-border); padding: 8px;">3</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0011</td><td style="border: 1px solid var(--color-border); padding: 8px;">6</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0100</td><td style="border: 1px solid var(--color-border); padding: 8px;">9</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0101</td><td style="border: 1px solid var(--color-border); padding: 8px;">14</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0110</td><td style="border: 1px solid var(--color-border); padding: 8px;">20</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0111</td><td style="border: 1px solid var(--color-border); padding: 8px;">27</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1000</td><td style="border: 1px solid var(--color-border); padding: 8px;">35</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1001</td><td style="border: 1px solid var(--color-border); padding: 8px;">45</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1010</td><td style="border: 1px solid var(--color-border); padding: 8px;">57</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1011</td><td style="border: 1px solid var(--color-border); padding: 8px;">72</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1100</td><td style="border: 1px solid var(--color-border); padding: 8px;">92</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1101</td><td style="border: 1px solid var(--color-border); padding: 8px;">117</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1110</td><td style="border: 1px solid var(--color-border); padding: 8px;">147</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1111</td><td style="border: 1px solid var(--color-border); padding: 8px;">192</td></tr>
</table>
Bits 3-0

:   Nombre de tags à envoyer si nécessaire. Ceci est consultatif et ne

    force tags to be delivered. For ElGamal only. Ignored for
    ECIES-Ratchet.

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Field value</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Tags to send</th>
</tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0000</td><td style="border: 1px solid var(--color-border); padding: 8px;">Use session key manager settings</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0001</td><td style="border: 1px solid var(--color-border); padding: 8px;">2</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0010</td><td style="border: 1px solid var(--color-border); padding: 8px;">4</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0011</td><td style="border: 1px solid var(--color-border); padding: 8px;">6</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0100</td><td style="border: 1px solid var(--color-border); padding: 8px;">8</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0101</td><td style="border: 1px solid var(--color-border); padding: 8px;">12</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0110</td><td style="border: 1px solid var(--color-border); padding: 8px;">16</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">0111</td><td style="border: 1px solid var(--color-border); padding: 8px;">24</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1000</td><td style="border: 1px solid var(--color-border); padding: 8px;">32</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1001</td><td style="border: 1px solid var(--color-border); padding: 8px;">40</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1010</td><td style="border: 1px solid var(--color-border); padding: 8px;">51</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1011</td><td style="border: 1px solid var(--color-border); padding: 8px;">64</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1100</td><td style="border: 1px solid var(--color-border); padding: 8px;">80</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1101</td><td style="border: 1px solid var(--color-border); padding: 8px;">100</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1110</td><td style="border: 1px solid var(--color-border); padding: 8px;">125</td></tr>
<tr><td style="border: 1px solid var(--color-border); padding: 8px;">1111</td><td style="border: 1px solid var(--color-border); padding: 8px;">160</td></tr>
</table>
### SessionStatusMessage {#SessionStatusMessage}

#### Description

Informe le client du statut de sa session.

Envoyé du Router au Client, en réponse à un [CreateSessionMessage](#CreateSessionMessage), [ReconfigureSessionMessage](#ReconfigureSessionMessage), ou [DestroySessionMessage](#DestroySessionMessage). Dans tous les cas, y compris en réponse à [CreateSessionMessage](#CreateSessionMessage), le router doit répondre immédiatement (ne pas attendre que les tunnels soient construits).

#### Sommaire

1.  [ID de session](#struct-sessionid)
2.  1 octet [Integer](/docs/specs/common-structures/#integer) statut

<table style="border: 1px solid var(--color-border); border-collapse: collapse;">
<tr style="background-color: var(--color-bg-secondary);">
<th style="border: 1px solid var(--color-border); padding: 8px;">Status</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Since</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Name</th>
<th style="border: 1px solid var(--color-border); padding: 8px;">Definition</th>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">0</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Destroyed</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">The session with the given ID is terminated. May be a response to a <a href="#DestroySessionMessage">DestroySessionMessage</a>.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">1</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Created</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">In response to a <a href="#CreateSessionMessage">CreateSessionMessage</a>, a new session with the given ID is now active.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">2</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Updated</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">In response to a <a href="#ReconfigureSessionMessage">ReconfigureSessionMessage</a>, an existing session with the given ID has been reconfigured.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">3</td>
<td style="border: 1px solid var(--color-border); padding: 8px;"></td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Invalid</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">In response to a <a href="#CreateSessionMessage">CreateSessionMessage</a>, the configuration is invalid. The included session ID should be ignored. In response to a <a href="#ReconfigureSessionMessage">ReconfigureSessionMessage</a>, the new configuration is invalid for the session with the given ID.</td>
</tr>
<tr>
<td style="border: 1px solid var(--color-border); padding: 8px;">4</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">0.9.12</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">Refused</td>
<td style="border: 1px solid var(--color-border); padding: 8px;">In response to a <a href="#CreateSessionMessage">CreateSessionMessage</a>, the router was unable to create the session, perhaps due to limits being exceeded. The included session ID should be ignored.</td>
</tr>
</table>
#### Notes

Les valeurs de statut sont définies ci-dessus. Si le statut est Created, l'ID de session est l'identifiant à utiliser pour le reste de la session.

### SetDateMessage {#SetDateMessage}

#### Description

La date et l'heure actuelles. Envoyées du router au client dans le cadre de la négociation initiale. Depuis la version 0.9.20, peuvent également être envoyées à tout moment après la négociation pour notifier le client d'un décalage d'horloge.

#### Sommaire

1.  [Date](/docs/specs/common-structures/#date)
2.  Version de l'API I2CP [String](/docs/specs/common-structures/#string)

#### Notes

Il s'agit généralement du premier message envoyé par le router. La chaîne de version est incluse depuis la version 0.8.7. Ceci n'est utile que si le client et le router ne sont pas dans la même JVM. Si elle n'est pas présente, le router est en version 0.8.6 ou antérieure.

Des messages SetDate supplémentaires ne seront pas envoyés aux clients dans la même JVM.

## Références

- [Date](/docs/specs/common-structures/#date)
- [Destination](/docs/specs/common-structures/#destination)
- [EncryptedLeaseSet](/docs/specs/common-structures/#leaseset2)
- [Hash](/docs/specs/common-structures/#hash)
- [Aperçu I2CP](/docs/specs/i2cp/)
- [Javadocs I2CP](http://javadoc.i2p.net/net/i2p/data/i2cp/package-summary.html)
- [Integer](/docs/specs/common-structures/#integer)
- [Lease](/docs/specs/common-structures/#lease)
- [LeaseSet](/docs/specs/common-structures/#leaseset)
- [LeaseSet2](/docs/specs/common-structures/#leaseset2)
- [Mapping](/docs/specs/common-structures/#mapping)
- [MetaLeaseSet](/docs/specs/common-structures/#leaseset2)
- [Javadocs MessageStatusMessage](http://javadoc.i2p.net/net/i2p/data/i2cp/MessageStatusMessage.html)
- [PrivateKey](/docs/specs/common-structures/#privatekey)
- [PublicKey](/docs/specs/common-structures/#publickey)
- [RouterIdentity](/docs/specs/common-structures/#routeridentity)
- [SAMv3](/docs/api/samv3/)
- [Signature](/docs/specs/common-structures/#signature)
- [SigningPrivateKey](/docs/specs/common-structures/#signingprivatekey)
- [SigningPublicKey](/docs/specs/common-structures/#signingpublickey)
- [String](/docs/specs/common-structures/#string)
- [TunnelId](/docs/specs/common-structures/#tunnelid)
