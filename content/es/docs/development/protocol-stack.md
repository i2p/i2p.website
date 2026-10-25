---
title: "Pila de Protocolos"
description: "Descripción general de las capas del stack de protocolos de I2P"
slug: "protocol-stack"
lastUpdated: "2024-01"
accurateFor: "0.9.61"
aliases:
  - "/es/docs/develop/protocol-stack"
  - "/es/docs/develop/protocol-stack/"
  - "/es/protocols"
  - "/es/protocols/"
---

La pila de I2P es un diseño por capas que permite la comunicación anónima. Cada capa añade capacidades específicas sobre las que están debajo de ella. Consulta el [Índice de Documentación Técnica](/docs/develop/overview) para obtener detalles adicionales sobre cada componente.

## Capa de Internet {#internet}

**IP** - El Protocolo de Internet permite direccionar hosts en la internet regular y enrutar paquetes a través de internet usando entrega de mejor esfuerzo.

## Capa de Transporte {#transport}

- **TCP** - Protocolo de Control de Transmisión permite la entrega confiable y en orden de paquetes
- **UDP** - Protocolo de Datagramas de Usuario permite la entrega no confiable y fuera de orden de paquetes

## Capa de Transporte I2P {#i2p-transport}

Conexiones cifradas de router a router (aún no anónimas):

- **[NTCP2](/docs/specs/ntcp2)** - Transporte TCP basado en NIO
- **[SSU2](/docs/specs/ssu2)** - Transporte UDP Seguro Semi-confiable

## Capa de túneles I2P {#tunnels}

Proporciona conexiones de tunnel anónimas completamente cifradas:

- **[Mensajes de tunnel](/docs/legacy/tunnel-message)** - Mensajes I2NP cifrados e instrucciones cifradas para su entrega
- **[Mensajes I2NP](/docs/specs/i2np)** - Mensajes de protocolo con cifrado en capas para enrutamiento anónimo multi-salto

## Capa Garlic de I2P {#garlic}

Proporciona entrega de mensajes I2P cifrada y anónima de extremo a extremo:

- **[Mensajes garlic](/docs/overview/garlic-routing)** - Mensajes I2NP encapsulados para entrega anónima

## Capa de Cliente I2P {#client}

- **[I2CP](/docs/specs/i2cp)** - I2P Control Protocol permite a las aplicaciones acceder
  a la red I2P sin tener que usar la API del router directamente

## Capa de Transporte Extremo a Extremo de I2P {#e2e-transport}

- **[Streaming Library](/docs/api/streaming)** - Proporciona entrega confiable y en orden
  similar a TCP
- **[Datagram Library](/docs/api/datagrams)** - Proporciona entrega no confiable similar a UDP

## Capa de Interfaz de Aplicación I2P {#app-interface}

Interfaces opcionales para desarrolladores de aplicaciones:

- **[I2PTunnel](/docs/api/i2ptunnel)** - Crea túneles para conexiones TCP dentro y fuera de I2P
- **[SAMv3](/docs/api/samv3)** - Protocolo de Mensajería Anónima Simple para aplicaciones que no son Java

## Capa de Proxy de Aplicaciones I2P {#app-proxy}

Proxies para protocolos estándar de internet:

- **HTTP** - Proxy de navegación web
- **IRC** - Proxy de Internet Relay Chat
- **[SOCKS](/docs/api/socks)** - Proxy SOCKS4/4a/5
- **Streamr** - Proxy de transmisión UDP

## Aplicaciones {#applications}

Las aplicaciones pueden interactuar con I2P en varias capas:

**Aplicaciones Streaming/Datagram:** - Aplicaciones nativas de I2P que utilizan las bibliotecas streaming o datagram directamente

**Aplicaciones SAM:** - Aplicaciones en cualquier lenguaje que utilicen el protocolo SAM

**Aplicaciones Específicas de I2P:** - Aplicaciones diseñadas específicamente para I2P (I2PSnark, SusiMail, etc.)

**Aplicaciones de Internet Estándar:** - Aplicaciones regulares que utilizan proxies I2P (navegadores web, clientes IRC, etc.)

## Diagrama de Pila {#diagram}

![Pila de Protocolos I2P](/images/protocol_stack.png)

Nota: SAM puede usar tanto la biblioteca de streaming como datagramas.
