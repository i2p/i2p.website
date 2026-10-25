---
title: "Pilha de Protocolos"
description: "Visão geral das camadas da pilha de protocolos I2P"
slug: "protocol-stack"
lastUpdated: "2024-01"
accurateFor: "0.9.61"
aliases:
  - "/pt/docs/develop/protocol-stack"
  - "/pt/docs/develop/protocol-stack/"
---

A pilha I2P é um design em camadas que permite comunicação anônima. Cada camada adiciona capacidades específicas sobre aquelas abaixo dela. Consulte o [Índice de Documentação Técnica](/docs/develop/overview) para detalhes adicionais sobre cada componente.

## Camada de Internet {#internet}

**IP** - Internet Protocol permite endereçar hosts na internet regular e rotear pacotes através da internet usando entrega de melhor esforço.

## Camada de Transporte {#transport}

- **TCP** - Protocolo de Controle de Transmissão permite entrega confiável e ordenada de pacotes
- **UDP** - Protocolo de Datagrama do Usuário permite entrega não confiável e fora de ordem de pacotes

## Camada de Transporte I2P {#i2p-transport}

Conexões criptografadas router-para-router (ainda não anônimas):

- **[NTCP2](/docs/specs/ntcp2)** - Transporte TCP baseado em NIO
- **[SSU2](/docs/specs/ssu2)** - Transporte UDP Seguro Semi-confiável

## Camada de Tunnel I2P {#tunnels}

Fornece conexões de túnel criptografadas completamente anônimas:

- **[Mensagens de tunnel](/docs/legacy/tunnel-message)** - Mensagens I2NP criptografadas e instruções
  criptografadas para sua entrega
- **[Mensagens I2NP](/docs/specs/i2np)** - Mensagens de protocolo com criptografia em camadas para
  roteamento anônimo multi-hop

## Camada Garlic do I2P {#garlic}

Fornece entrega de mensagens I2P criptografadas e anônimas de ponta a ponta:

- **[Mensagens garlic](/docs/overview/garlic-routing)** - Mensagens I2NP encapsuladas para entrega anônima

## Camada de Cliente I2P {#client}

- **[I2CP](/docs/specs/i2cp)** - I2P Control Protocol permite que aplicações acessem
  a rede I2P sem ter que usar a API do router diretamente

## Camada de Transporte End-to-End do I2P {#e2e-transport}

- **[Streaming Library](/docs/api/streaming)** - Fornece entrega confiável e em ordem
  similar ao TCP
- **[Datagram Library](/docs/api/datagrams)** - Fornece entrega não confiável similar ao UDP

## Camada de Interface de Aplicação I2P {#app-interface}

Interfaces opcionais para desenvolvedores de aplicações:

- **[I2PTunnel](/docs/api/i2ptunnel)** - Canaliza conexões TCP para dentro e para fora do I2P
- **[SAMv3](/docs/api/samv3)** - Protocolo Simple Anonymous Messaging para aplicações não-Java

## Camada de Proxy de Aplicação I2P {#app-proxy}

Proxies para protocolos padrão da internet:

- **HTTP** - Proxy de navegação web
- **IRC** - Proxy de Internet Relay Chat
- **[SOCKS](/docs/api/socks)** - Proxy SOCKS4/4a/5
- **Streamr** - Proxy de streaming UDP

## Aplicações {#applications}

As aplicações podem interagir com o I2P em várias camadas:

**Aplicações Streaming/Datagram:** - Aplicações nativas do I2P usando as bibliotecas streaming ou datagram diretamente

**Aplicações SAM:** - Aplicações em qualquer linguagem usando o protocolo SAM

**Aplicações Específicas do I2P:** - Aplicações desenvolvidas especificamente para I2P (I2PSnark, SusiMail, etc.)

**Aplicações de Internet Padrão:** - Aplicações regulares usando proxies I2P (navegadores web, clientes IRC, etc.)

## Diagrama de Pilha {#diagram}

![Pilha de Protocolos I2P](/images/protocol_stack.png)

Nota: O SAM pode usar tanto a biblioteca de streaming quanto datagramas.
