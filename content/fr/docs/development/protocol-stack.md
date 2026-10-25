---
title: "Pile de protocoles"
description: "Aperçu des couches de la pile de protocoles I2P"
slug: "protocol-stack"
lastUpdated: "2024-01"
accurateFor: "0.9.61"
aliases:
  - "/fr/docs/develop/protocol-stack"
  - "/fr/docs/develop/protocol-stack/"
  - "/fr/protocols"
  - "/fr/protocols/"
---

La pile I2P est une conception en couches qui permet la communication anonyme. Chaque couche ajoute des capacités spécifiques par-dessus celles qui se trouvent en dessous. Consultez l'[Index de la Documentation Technique](/docs/develop/overview) pour des détails supplémentaires sur chaque composant.

## Couche Internet {#internet}

**IP** - Internet Protocol permet l'adressage des hôtes sur l'internet régulier et le routage des paquets à travers l'internet en utilisant une livraison au mieux.

## Couche de transport {#transport}

- **TCP** - Transmission Control Protocol permet la livraison fiable et ordonnée des paquets
- **UDP** - User Datagram Protocol permet la livraison non fiable et désordonnée des paquets

## Couche de transport I2P {#i2p-transport}

Connexions chiffrées router-à-router (pas encore anonymes) :

- **[NTCP2](/docs/specs/ntcp2)** - Transport TCP basé sur NIO
- **[SSU2](/docs/specs/ssu2)** - Transport UDP sécurisé semi-fiable

## Couche tunnel I2P {#tunnels}

Fournit des connexions tunnel chiffrées entièrement anonymes :

- **[Messages de tunnel](/docs/legacy/tunnel-message)** - Messages I2NP chiffrés et instructions
  chiffrées pour leur livraison
- **[Messages I2NP](/docs/specs/i2np)** - Messages de protocole avec chiffrement en couches pour
  le routage anonyme multi-saut

## Couche Garlic d'I2P {#garlic}

Fournit une livraison de messages I2P chiffrés et anonymes de bout en bout :

- **[Messages garlic](/docs/overview/garlic-routing)** - Messages I2NP encapsulés pour la livraison anonyme

## Couche Client I2P {#client}

- **[I2CP](/docs/specs/i2cp)** - I2P Control Protocol permet aux applications d'accéder
  au réseau I2P sans avoir à utiliser directement l'API du router

## Couche de transport de bout en bout I2P {#e2e-transport}

- **[Streaming Library](/docs/api/streaming)** - Fournit une livraison fiable et ordonnée similaire à TCP
- **[Datagram Library](/docs/api/datagrams)** - Fournit une livraison non fiable similaire à UDP

## Couche d'interface d'application I2P {#app-interface}

Interfaces optionnelles pour les développeurs d'applications :

- **[I2PTunnel](/docs/api/i2ptunnel)** - Tunnelise les connexions TCP vers et depuis I2P
- **[SAMv3](/docs/api/samv3)** - Protocole Simple Anonymous Messaging pour les applications non-Java

## Couche Proxy d'Application I2P {#app-proxy}

Proxies pour les protocoles internet standard :

- **HTTP** - Proxy de navigation web
- **IRC** - Proxy Internet Relay Chat
- **[SOCKS](/docs/api/socks)** - Proxy SOCKS4/4a/5
- **Streamr** - Proxy de streaming UDP

## Applications {#applications}

Les applications peuvent s'interfacer avec I2P à différents niveaux :

**Applications Streaming/Datagram :** - Applications natives I2P utilisant directement les bibliothèques streaming ou datagram

**Applications SAM :** - Applications dans n'importe quel langage utilisant le protocole SAM

**Applications spécifiques à I2P :** - Applications conçues spécifiquement pour I2P (I2PSnark, SusiMail, etc.)

**Applications Internet Standard :** - Applications régulières utilisant les proxies I2P (navigateurs web, clients IRC, etc.)

## Diagramme de pile {#diagram}

![Pile de protocoles I2P](/images/protocol_stack.png)

Note : SAM peut utiliser à la fois la bibliothèque de streaming et les datagrammes.
