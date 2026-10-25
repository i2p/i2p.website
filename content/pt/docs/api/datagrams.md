---
title: "Datagramas"
description: "Formatos de mensagem autenticada, respondível e bruta acima do I2CP"
slug: "datagrams"
aliases:
  - "/pt/datagrams"
  - "/pt/datagrams/"
lastUpdated: "2025-04"
accurateFor: "0.9.66"
---

## Visão Geral do Datagrama {#overview}

Os datagramas baseiam-se no [I2CP](/docs/specs/i2cp) base para fornecer mensagens autenticadas e respondíveis em um formato padrão. Isso permite que as aplicações leiam de forma confiável o endereço "de" de um datagrama e saibam que o endereço realmente enviou a mensagem. Isso é necessário para algumas aplicações, já que a mensagem I2P base é completamente bruta - ela não possui endereço "de" (diferentemente dos pacotes IP). Além disso, a mensagem e o remetente são autenticados através da assinatura da carga útil.

Datagramas, assim como [pacotes da biblioteca de streaming](/docs/api/streaming), são uma construção de nível de aplicação. Esses protocolos são independentes dos [transportes](/docs/overview/transport) de baixo nível; os protocolos são convertidos em mensagens I2NP pelo router, e qualquer protocolo pode ser transportado por qualquer transporte.

## Guia de Aplicação {#application}

Aplicações escritas em Java podem usar a API de datagram, enquanto aplicações em outras linguagens podem usar o suporte a datagram do [SAM](/docs/api/samv3). Há também suporte limitado no i2ptunnel no [proxy SOCKS](/docs/api/socks), nos tipos de tunnel 'streamr' e nas classes udpTunnel.

### Comprimento do Datagrama {#length}

O designer da aplicação deve considerar cuidadosamente o compromisso entre datagramas respondíveis vs. não-respondíveis. Além disso, o tamanho do datagrama afetará a confiabilidade, devido à fragmentação do tunnel em mensagens de tunnel de 1KB. Quanto mais fragmentos de mensagem, maior a probabilidade de que um deles seja descartado por um hop intermediário. Mensagens maiores que alguns KB não são recomendadas. Acima de cerca de 10 KB, a probabilidade de entrega diminui drasticamente.

[Veja a página de Especificação de Datagramas.](/docs/specs/datagrams)

Note também que as várias sobrecargas adicionadas pelas camadas inferiores, em particular as garlic messages, impõem uma grande carga sobre mensagens intermitentes como as usadas por uma aplicação Kademlia-sobre-UDP. As implementações estão atualmente ajustadas para tráfego frequente usando a biblioteca de streaming.

### Número de Protocolo e Portas I2CP {#protocol}

O número de protocolo I2CP padrão para datagramas assinados (com resposta possível) é PROTO_DATAGRAM (17). As aplicações podem ou não escolher definir o protocolo no cabeçalho I2CP. O padrão depende da implementação. Deve ser definido para demultiplexar o tráfego de datagrama e streaming recebido no mesmo Destination.

Como os datagramas não são orientados a conexão, a aplicação pode precisar de números de porta para correlacionar datagramas com pares específicos ou sessões de comunicação, como é tradicional com UDP sobre IP. As aplicações podem adicionar portas 'from' e 'to' ao cabeçalho I2CP (gzip) conforme descrito na [página I2CP](/docs/specs/i2cp#format).

Não há nenhum método dentro da API de datagram para especificar se é não-respondível (raw) ou respondível. A aplicação deve ser projetada para esperar o tipo apropriado. O número de protocolo I2CP ou porta deve ser usado pela aplicação para indicar o tipo de datagram. Os números de protocolo I2CP PROTO_DATAGRAM (assinado, também conhecido como Datagram1), PROTO_DATAGRAM_RAW, PROTO_DATAGRAM2, e PROTO_DATAGRAM3 estão definidos na API I2PSession para este propósito. Um padrão de design comum em aplicações cliente/servidor de datagram é usar datagrams assinados para uma solicitação que inclui um nonce, e usar um datagram raw para a resposta, retornando o nonce da solicitação.

**Padrões:**

- PROTO_DATAGRAM = 17
- PROTO_DATAGRAM_RAW = 18
- PROTO_DATAGRAM2 = 19
- PROTO_DATAGRAM3 = 20

### Integridade dos Dados {#integrity}

A integridade dos dados é assegurada pela soma de verificação gzip CRC-32 implementada na [camada I2CP](/docs/specs/i2cp#format). Datagramas autenticados (Datagram1 e Datagram2) também garantem a integridade. Não há campo de soma de verificação no protocolo de datagrama.

### Encapsulamento de Pacotes {#encapsulation}

Cada datagrama é enviado através do I2P como uma única mensagem (ou como um dente individual em uma [Garlic Message](/docs/overview/garlic-routing)). O encapsulamento de mensagens é implementado nas camadas subjacentes [I2CP](/docs/specs/i2cp), [I2NP](/docs/specs/i2np), e [tunnel message](/docs/specs/tunnel-message). Não há mecanismo de delimitador de pacotes ou campo de comprimento no protocolo de datagrama.

## Especificação {#spec}

[Veja a página de Especificação de Datagramas.](/docs/specs/datagrams)
